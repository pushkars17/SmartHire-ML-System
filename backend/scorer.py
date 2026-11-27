import math
from typing import Dict, List


def score_candidate(payload: Dict) -> Dict:
    cgpa_norm = float(payload["cgpa"]) / 10.0
    coding_norm = float(payload["coding_score"]) / 100.0
    interview_norm = float(payload["interview_score"]) / 100.0
    soft_norm = float(payload["soft_skills"]) / 100.0
    tier = int(payload["college_tier"])

    tier_bonus = {1: 0.08, 2: 0.03, 3: 0.0}.get(tier, 0.0)

    # Calibrated linear logit + sigmoid probability
    logit = (
        -3.85
        + 3.25 * coding_norm
        + 2.60 * interview_norm
        + 1.30 * cgpa_norm
        + 0.85 * soft_norm
        + tier_bonus
    )
    probability = round(1.0 / (1.0 + math.exp(-logit)), 4)

    if probability >= 0.72:
        decision_tier = "Strong Hire"
    elif probability >= 0.45:
        decision_tier = "Consider"
    else:
        decision_tier = "Review"

    drivers: List[str] = []
    if coding_norm >= 0.75:
        drivers.append("High Coding Score")
    elif coding_norm < 0.50:
        drivers.append("Needs Coding Practice")

    if interview_norm >= 0.75:
        drivers.append("Strong Interview")
    elif interview_norm < 0.55:
        drivers.append("Needs Interview Prep")

    if cgpa_norm >= 0.80:
        drivers.append("Strong CGPA")
    if soft_norm >= 0.75:
        drivers.append("Good Soft Skills")
    if not drivers:
        drivers.append("Balanced Baseline Profile")

    return {
        "selection_probability": probability,
        "tier": decision_tier,
        "key_drivers": drivers,
    }