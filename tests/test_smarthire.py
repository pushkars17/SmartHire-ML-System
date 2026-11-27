from pathlib import Path
from fastapi.testclient import TestClient

from backend.api import app
from backend.scorer import score_candidate
from db.database import fetch_evaluations, init_db, save_evaluation

client = TestClient(app)


def test_scorer_high_profile():
    result = score_candidate(
        {
            "cgpa": 9.1,
            "coding_score": 90.0,
            "interview_score": 88.0,
            "soft_skills": 85.0,
            "college_tier": 1,
        }
    )
    assert result["selection_probability"] >= 0.72
    assert result["tier"] == "Strong Hire"
    assert len(result["key_drivers"]) >= 1


def test_db_save_and_fetch(tmp_path: Path):
    test_db = tmp_path / "test_smarthire.db"
    init_db(test_db)

    row_id = save_evaluation(
        {
            "candidate_name": "Test Candidate",
            "cgpa": 8.2,
            "coding_score": 76.0,
            "interview_score": 74.0,
            "soft_skills": 78.0,
            "college_tier": 2,
            "selection_probability": 0.68,
            "tier": "Consider",
        },
        db_path=test_db,
    )
    assert row_id > 0

    rows = fetch_evaluations(limit=10, db_path=test_db)
    assert len(rows) == 1
    assert rows[0]["candidate_name"] == "Test Candidate"


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"