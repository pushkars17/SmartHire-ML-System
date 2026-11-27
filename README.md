# SmartHire ML System

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-Tidymodels%20%2F%20ranger-276DC3?logo=r&logoColor=white)](https://www.tidymodels.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Persistence-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Automated%20Tests-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)

**SmartHire ML System** is an end-to-end internship candidate screening and decision-support platform. It pairs an **R (`tidymodels` / `ranger`) analytics and modeling pipeline** with a **Python full-stack web application** built on **FastAPI**, **SQLite**, **Plotly**, and **Streamlit**.

---

## Key Features

- **Single Candidate Scorer:** Calculates a calibrated selection probability, assigns a decision tier (`Strong Hire`, `Consider`, `Review`), highlights key profile drivers, and displays a normalized 0–100 skill snapshot chart.
- **Quick Profile Presets:** Load sample candidate profiles (`Custom Input`, `Strong Hire Candidate`, `Borderline / Consider`, `Needs Prep / Review`) with one click.
- **What-If Improvement Simulator:** Test how improvements in `Coding`, `Interview`, or `Soft Skills` change the selection probability, with live delta metrics and baseline-vs-simulated comparison charts.
- **Batch CSV Screening:** Upload CSV files to score multiple candidates in one run, inspect tier counts, and export scored results back to CSV.
- **SQLite Evaluation History:** Automatically logs evaluations to `db/smarthire.db` with live KPIs, decision-tier filtering, candidate name search, and CSV export.
- **Preserved R Workflow:** Keeps the complete `tidymodels` / `ranger` R pipeline intact inside `r_pipeline/`.

---

## System Architecture

```text
+-------------------------------------------------------------------+
|                     Streamlit Web Frontend                        |
|  Single Scorer | What-If Simulator | Batch CSV | SQLite History   |
+---------------------------------+---------------------------------+
                                  | HTTP (JSON)
                                  v
+-------------------------------------------------------------------+
|                     FastAPI Backend Service                       |
| Pydantic Validation (schemas.py) -> Calibrated Scorer (scorer.py) |
+---------------------------------+---------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|               SQLite Persistence Layer (db/database.py)           |
|        Evaluations Table, Tier Filters & History Queries          |
+-------------------------------------------------------------------+

Parallel Analytics Layer:
data/raw/ -> r_pipeline/ (00_setup.R .. 05_visualization.R) -> output/
```

---

## Technology Stack

| Layer | Technology / Tool | Role in SmartHire ML |
|---|---|---|
| Statistical & ML Pipeline | R, `tidymodels`, `ranger` | Data cleaning, EDA, statistical tests, and Random Forest modeling on the internship selection dataset |
| Backend API | FastAPI, Uvicorn | REST API service (`/health`, `/predict`, `/evaluations`) with automatic OpenAPI / Swagger UI |
| Schema Validation | Pydantic | Request and response validation, range checks, and type safety |
| Database | SQLite | Local persistent storage for evaluations, probabilities, decision tiers, and timestamps |
| Frontend Dashboard | Streamlit, Pandas | Multi-tab web UI for scoring, What-If simulation, batch CSV uploads, and history search/export |
| Data Visualization | Plotly | Interactive skill snapshots, baseline-vs-simulated charts, and decision tier distribution bars |
| Testing & QA | Pytest, FastAPI `TestClient` | Automated tests covering scorer logic, SQLite persistence, and API endpoints |

---

## Scoring & Decision Tiers

`backend/scorer.py` normalizes candidate inputs (`cgpa`, `coding_score`, `interview_score`, `soft_skills`, and `college_tier`), computes a calibrated sigmoid selection probability, identifies key profile drivers, and maps the score to a decision tier:

| Decision Tier | Probability Range | Summary |
|---|---|---|
| **Strong Hire** | ≥ 72.0% | Strong readiness across technical, interview, and academic/skill metrics |
| **Consider** | 45.0% – 71.9% | Viable candidate; focused coding or interview prep can raise selection odds |
| **Review** | < 45.0% | Needs foundational skill development before shortlisting |

---

## Project Structure

```text
SmartHire-ML-System/
├── backend/
│   ├── __init__.py
│   ├── api.py                 # FastAPI routes (/health, /predict, /evaluations)
│   ├── schemas.py             # Pydantic input and output models
│   └── scorer.py              # Probability scoring, tier assignment & driver logic
├── db/
│   ├── __init__.py
│   ├── database.py            # SQLite connection, schema init, insert & query functions
│   └── smarthire.db           # Local SQLite database file (auto-created on startup)
├── frontend/
│   └── app.py                 # Streamlit multi-tab screening application
├── r_pipeline/
│   ├── 00_setup.R
│   ├── 01_data_cleaning.R
│   ├── 02_eda.R
│   ├── 03_statistics.R
│   ├── 04_modeling.R
│   └── 05_visualization.R
├── tests/
│   ├── __init__.py
│   └── test_smarthire.py      # Unit and API tests using pytest
├── data/
│   ├── raw/                   # Raw dataset files
│   └── processed/             # Processed datasets
├── output/                    # Plots, metrics & generated artifacts
├── docs/                      # Project documentation & reports
└── README.md
```

---

## Local Setup & Execution

### 1. Install Python Packages

```bash
pip install fastapi uvicorn pydantic requests streamlit pandas plotly pytest httpx
```

### 2. Run Automated Tests

```bash
python -m pytest -v
```

### 3. Start FastAPI Backend

```bash
uvicorn backend.api:app --reload --port 8000
```

Swagger API docs are available at <http://127.0.0.1:8000/docs>.

### 4. Start Streamlit Frontend (Second Terminal)

```bash
streamlit run frontend/app.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check confirming backend service status |
| `POST` | `/predict` | Scores a candidate profile, saves the evaluation to SQLite, and returns probability, tier, and key drivers |
| `GET` | `/evaluations` | Fetches saved evaluations from SQLite with optional `limit` and `tier` (`ALL`, `Strong Hire`, `Consider`, `Review`) parameters |

---

## Future Improvements

- [ ] Load a trained, serialized ML model artifact alongside the calibrated probability scorer.
- [ ] Add role-specific rubric weights (Software Engineering, Data Science, AI/ML internships).
- [ ] Package the backend and frontend with Docker and `docker-compose` for streamlined deployment.

---

## Author

**Pushkar Sharma** (`@pushkars17`)

- **GitHub:** [https://github.com/pushkars17](https://github.com/pushkars17)
- **Repository:** [SmartHire-ML-System](https://github.com/pushkars17/SmartHire-ML-System)
