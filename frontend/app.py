import os
from typing import Any, Dict, List

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

API_BASE_URL = os.getenv("SMARTHIRE_API_URL", "http://127.0.0.1:8000")

PRESETS: Dict[str, Dict[str, Any]] = {
    "Custom Input": {
        "candidate_name": "Riya Sharma",
        "cgpa": 8.4,
        "coding_score": 78.0,
        "interview_score": 75.0,
        "soft_skills": 80.0,
        "college_tier": 1,
    },
    "Strong Hire Candidate": {
        "candidate_name": "Aarav Mehta",
        "cgpa": 9.3,
        "coding_score": 92.0,
        "interview_score": 88.0,
        "soft_skills": 86.0,
        "college_tier": 1,
    },
    "Borderline / Consider": {
        "candidate_name": "Neha Patel",
        "cgpa": 8.0,
        "coding_score": 66.0,
        "interview_score": 68.0,
        "soft_skills": 72.0,
        "college_tier": 2,
    },
    "Needs Prep / Review": {
        "candidate_name": "Karan Verma",
        "cgpa": 6.6,
        "coding_score": 42.0,
        "interview_score": 48.0,
        "soft_skills": 55.0,
        "college_tier": 3,
    },
}

st.set_page_config(
    page_title="SmartHire ML — Internship Screening Command",
    page_icon="🎯",
    layout="wide",
)


def call_predict(base_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    resp = requests.post(f"{base_url.rstrip('/')}/predict", json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def call_evaluations(base_url: str, limit: int = 100, tier: str = "ALL") -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {"limit": limit}
    if tier != "ALL":
        params["tier"] = tier
    resp = requests.get(f"{base_url.rstrip('/')}/evaluations", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def build_profile_chart(payload: Dict[str, Any]) -> go.Figure:
    labels = [
        "Coding Score (/100)",
        "Interview Score (/100)",
        "Soft Skills (/100)",
        "CGPA Scaled (/100)",
    ]
    values = [
        float(payload["coding_score"]),
        float(payload["interview_score"]),
        float(payload["soft_skills"]),
        round(float(payload["cgpa"]) * 10.0, 1),
    ]
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            text=[f"{v:.1f}" for v in values],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Normalized Candidate Skill Snapshot (0-100 Scale)",
        xaxis=dict(range=[0, 112], title="Score"),
        yaxis=dict(autorange="reversed"),
        height=270,
        margin=dict(l=10, r=20, t=45, b=20),
    )
    return fig


def build_whatif_comparison_chart(base_scores: Dict[str, float], sim_scores: Dict[str, float]) -> go.Figure:
    metrics = ["Coding", "Interview", "Soft Skills"]
    base_vals = [base_scores["coding"], base_scores["interview"], base_scores["soft"]]
    sim_vals = [sim_scores["coding"], sim_scores["interview"], sim_scores["soft"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Baseline", x=metrics, y=base_vals))
    fig.add_trace(go.Bar(name="Simulated", x=metrics, y=sim_vals))
    fig.update_layout(
        title="Baseline vs. Simulated Skill Scores",
        barmode="group",
        yaxis=dict(range=[0, 105], title="Score (0-100)"),
        height=280,
        margin=dict(l=10, r=20, t=45, b=20),
    )
    return fig


def build_tier_distribution_chart(df: pd.DataFrame) -> go.Figure:
    tier_order = ["Strong Hire", "Consider", "Review"]
    counts = [int((df["tier"] == t).sum()) for t in tier_order]
    fig = go.Figure(
        go.Bar(
            x=tier_order,
            y=counts,
            text=counts,
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Evaluations by Decision Tier",
        xaxis=dict(title="Decision Tier"),
        yaxis=dict(title="Candidates", rangemode="tozero"),
        height=270,
        margin=dict(l=10, r=20, t=45, b=20),
    )
    return fig


# --- Sidebar ---
with st.sidebar:
    st.header("Connection & Presets")
    api_url = st.text_input("FastAPI Base URL", value=API_BASE_URL)

    if st.button("Check API Health", use_container_width=True):
        try:
            r = requests.get(f"{api_url.rstrip('/')}/health", timeout=5)
            if r.ok:
                st.success(f"Backend Online: {r.json()}")
            else:
                st.error(f"Unexpected status: {r.status_code}")
        except Exception as exc:
            st.error(f"Offline / Unreachable: {exc}")

    st.divider()
    preset_choice = st.selectbox("Load Sample Profile", options=list(PRESETS.keys()))
    st.caption("Select a preset to populate candidate form defaults.")

preset = PRESETS[preset_choice]

# --- Header ---
st.title("SmartHire ML — Internship Screening Command")
st.caption(
    "Full-stack candidate screening with FastAPI inference, What-If simulation, batch CSV scoring, and SQLite persistence"
)

# --- Top Summary KPIs from DB ---
try:
    all_rows = call_evaluations(api_url, limit=200, tier="ALL")
    total_evals = len(all_rows)
    strong_count = sum(1 for row in all_rows if row.get("tier") == "Strong Hire")
    consider_count = sum(1 for row in all_rows if row.get("tier") == "Consider")
    avg_prob = (
        round(sum(float(row.get("selection_probability", 0.0)) for row in all_rows) / total_evals * 100, 1)
        if total_evals > 0
        else 0.0
    )
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Evaluations", total_evals)
    k2.metric("Strong Hire", strong_count)
    k3.metric("Consider", consider_count)
    k4.metric("Avg Selection Prob.", f"{avg_prob}%")
except Exception:
    st.info("Start the FastAPI backend to view live database metrics and saved history.")

st.divider()

# --- Main Tabs ---
tab_single, tab_whatif, tab_batch, tab_history = st.tabs(
    [
        "Single Candidate Scorer",
        "What-If Simulator",
        "Batch CSV Screening",
        "Saved History (SQLite)",
    ]
)

# --- Tab 1: Single Candidate Scorer ---
with tab_single:
    col_form, col_out = st.columns([1.05, 1.15], gap="large")

    with col_form:
        st.subheader("Candidate Profile Input")
        with st.form("single_candidate_form"):
            candidate_name = st.text_input("Candidate Name", value=preset["candidate_name"])
            cgpa = st.slider("CGPA (0.0 - 10.0)", 0.0, 10.0, float(preset["cgpa"]), 0.1)
            coding_score = st.slider("Coding Test Score (0 - 100)", 0.0, 100.0, float(preset["coding_score"]), 1.0)
            interview_score = st.slider("Interview Score (0 - 100)", 0.0, 100.0, float(preset["interview_score"]), 1.0)
            soft_skills = st.slider("Soft Skills Score (0 - 100)", 0.0, 100.0, float(preset["soft_skills"]), 1.0)
            college_tier = st.selectbox(
                "College Tier",
                options=[1, 2, 3],
                index=[1, 2, 3].index(int(preset["college_tier"])),
                format_func=lambda x: {
                    1: "Tier 1 (Premier / Top)",
                    2: "Tier 2 (Mid / Regional)",
                    3: "Tier 3 (Other)",
                }[x],
            )
            submitted = st.form_submit_button("Evaluate Candidate", type="primary", use_container_width=True)

    with col_out:
        st.subheader("Evaluation Breakdown")
        current_payload = {
            "candidate_name": candidate_name.strip() or "Anonymous",
            "cgpa": cgpa,
            "coding_score": coding_score,
            "interview_score": interview_score,
            "soft_skills": soft_skills,
            "college_tier": college_tier,
        }

        if submitted:
            try:
                result = call_predict(api_url, current_payload)
                st.session_state["last_result"] = result
                st.session_state["last_payload"] = current_payload
            except Exception as exc:
                st.error(f"Prediction request failed: {exc}")

        active_result = st.session_state.get("last_result")
        active_payload = st.session_state.get("last_payload", current_payload)

        if active_result:
            prob_pct = round(float(active_result["selection_probability"]) * 100, 2)
            tier_label = active_result["tier"]

            m1, m2, m3 = st.columns(3)
            m1.metric("Selection Probability", f"{prob_pct}%")
            m2.metric("Decision Tier", tier_label)
            m3.metric("Saved DB ID", f"#{active_result['id']}")

            if tier_label == "Strong Hire":
                st.success(f"{active_result['candidate_name']} shows strong readiness for internship selection.")
            elif tier_label == "Consider":
                st.warning(f"{active_result['candidate_name']} is a viable candidate; targeted prep can improve selection odds.")
            else:
                st.error(f"{active_result['candidate_name']} currently needs focused skill improvement before shortlisting.")

            st.write("**Key Profile Drivers:**")
            drivers = active_result.get("key_drivers", [])
            if drivers:
                st.write(", ".join(f"`{d}`" for d in drivers))

            st.plotly_chart(build_profile_chart(active_payload), use_container_width=True)
        else:
            st.info("Configure candidate details on the left and click Evaluate Candidate.")

# --- Tab 2: What-If Simulator ---
with tab_whatif:
    st.subheader("What-If Improvement Simulator")
    st.caption("Simulate skill score improvements and compare selection probability against the baseline profile.")

    base_p = st.session_state.get("last_payload", preset)
    base_res = st.session_state.get("last_result")

    w_col1, w_col2 = st.columns([1, 1.15], gap="large")
    with w_col1:
        sim_coding = st.slider("Simulated Coding Score", 0.0, 100.0, float(base_p["coding_score"]), 1.0)
        sim_interview = st.slider("Simulated Interview Score", 0.0, 100.0, float(base_p["interview_score"]), 1.0)
        sim_soft = st.slider("Simulated Soft Skills Score", 0.0, 100.0, float(base_p["soft_skills"]), 1.0)

        sim_payload = {
            "candidate_name": f"{base_p['candidate_name']} (Sim)",
            "cgpa": float(base_p["cgpa"]),
            "coding_score": sim_coding,
            "interview_score": sim_interview,
            "soft_skills": sim_soft,
            "college_tier": int(base_p["college_tier"]),
        }
        try:
            sim_resp = requests.post(f"{api_url.rstrip('/')}/predict", json=sim_payload, timeout=10)
            if sim_resp.ok:
                sim_data = sim_resp.json()
                sim_prob = round(float(sim_data["selection_probability"]) * 100, 2)
                base_prob = (
                    round(float(base_res["selection_probability"]) * 100, 2)
                    if base_res
                    else sim_prob
                )
                delta_prob = round(sim_prob - base_prob, 2)

                s1, s2 = st.columns(2)
                s1.metric("Simulated Probability", f"{sim_prob}%", delta=f"{delta_prob:+.2f}%")
                s2.metric("Simulated Tier", sim_data["tier"])
                st.write("**Simulated Drivers:**", ", ".join(f"`{d}`" for d in sim_data.get("key_drivers", [])))
            else:
                st.warning("Backend must be running to compute simulations.")
        except Exception as exc:
            st.info(f"Connect to the backend to run simulations ({exc}).")

    with w_col2:
        st.plotly_chart(
            build_whatif_comparison_chart(
                {
                    "coding": float(base_p["coding_score"]),
                    "interview": float(base_p["interview_score"]),
                    "soft": float(base_p["soft_skills"]),
                },
                {
                    "coding": sim_coding,
                    "interview": sim_interview,
                    "soft": sim_soft,
                },
            ),
            use_container_width=True,
        )

# --- Tab 3: Batch CSV Screening ---
with tab_batch:
    st.subheader("Batch CSV Candidate Screening")
    st.caption("Required columns: `candidate_name`, `cgpa`, `coding_score`, `interview_score`, `soft_skills`, `college_tier`")

    sample_df = pd.DataFrame(
        [
            {"candidate_name": "Ananya Rao", "cgpa": 9.1, "coding_score": 88, "interview_score": 84, "soft_skills": 85, "college_tier": 1},
            {"candidate_name": "Rohan Das", "cgpa": 7.9, "coding_score": 65, "interview_score": 66, "soft_skills": 72, "college_tier": 2},
            {"candidate_name": "Vikram Joshi", "cgpa": 6.4, "coding_score": 38, "interview_score": 45, "soft_skills": 52, "college_tier": 3},
        ]
    )

    st.download_button(
        label="Download Sample CSV Template",
        data=sample_df.to_csv(index=False).encode("utf-8"),
        file_name="smarthire_sample_candidates.csv",
        mime="text/csv",
    )

    uploaded_file = st.file_uploader("Upload Candidates CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.write("Input Preview:", batch_df.head(10))

            if st.button("Run Batch Scoring", type="primary"):
                scored_rows: List[Dict[str, Any]] = []
                errors: List[str] = []

                for idx, row in batch_df.iterrows():
                    item = {
                        "candidate_name": str(row.get("candidate_name", f"Candidate_{idx+1}")),
                        "cgpa": float(row["cgpa"]),
                        "coding_score": float(row["coding_score"]),
                        "interview_score": float(row["interview_score"]),
                        "soft_skills": float(row["soft_skills"]),
                        "college_tier": int(row["college_tier"]),
                    }
                    try:
                        res = call_predict(api_url, item)
                        scored_rows.append(
                            {
                                **item,
                                "selection_probability": res["selection_probability"],
                                "tier": res["tier"],
                                "key_drivers": ", ".join(res.get("key_drivers", [])),
                            }
                        )
                    except Exception as row_exc:
                        errors.append(f"Row {idx + 1}: {row_exc}")

                if scored_rows:
                    out_df = pd.DataFrame(scored_rows)
                    st.success(f"Scored {len(out_df)} candidates and saved results to SQLite.")

                    b1, b2, b3 = st.columns(3)
                    b1.metric("Strong Hire", int((out_df["tier"] == "Strong Hire").sum()))
                    b2.metric("Consider", int((out_df["tier"] == "Consider").sum()))
                    b3.metric("Review", int((out_df["tier"] == "Review").sum()))

                    st.dataframe(out_df, use_container_width=True)

                    st.download_button(
                        label="Download Scored Results CSV",
                        data=out_df.to_csv(index=False).encode("utf-8"),
                        file_name="smarthire_scored_candidates.csv",
                        mime="text/csv",
                    )

                if errors:
                    st.error("Some rows failed:\n" + "\n".join(errors))
        except Exception as exc:
            st.error(f"Could not process CSV: {exc}")

# --- Tab 4: Saved History ---
with tab_history:
    st.subheader("Saved Evaluations (SQLite)")
    f_col1, f_col2, f_col3 = st.columns([1, 1, 1.2])
    with f_col1:
        tier_filter = st.selectbox(
            "Filter by Tier",
            options=["ALL", "Strong Hire", "Consider", "Review"],
            key="history_tier_filter",
        )
    with f_col2:
        limit_val = st.slider("Rows to Fetch", min_value=5, max_value=200, value=50, step=5)
    with f_col3:
        search_name = st.text_input("Search Candidate Name", value="")

    try:
        rows = call_evaluations(api_url, limit=limit_val, tier=tier_filter)
        if rows:
            hist_df = pd.DataFrame(rows)
            if search_name.strip():
                hist_df = hist_df[
                    hist_df["candidate_name"].astype(str).str.contains(search_name.strip(), case=False, na=False)
                ]

            if not hist_df.empty:
                st.plotly_chart(build_tier_distribution_chart(hist_df), use_container_width=True)
                st.dataframe(hist_df, use_container_width=True)
                st.download_button(
                    label="Export Filtered History CSV",
                    data=hist_df.to_csv(index=False).encode("utf-8"),
                    file_name="smarthire_evaluation_history.csv",
                    mime="text/csv",
                )
            else:
                st.write("No records match the current search and filter criteria.")
        else:
            st.write("No evaluation records match the selected filter.")
    except Exception:
        st.info("Saved evaluation history will appear here once the backend is running.")