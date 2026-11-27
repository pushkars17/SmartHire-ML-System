from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query

from backend.schemas import CandidateInput, EvaluationResponse
from backend.scorer import score_candidate
from db.database import fetch_evaluations, init_db, save_evaluation

app = FastAPI(
    title="SmartHire ML API",
    description="Internship selection scoring and SQLite evaluation history API",
    version="0.2.0",
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "smarthire-backend"}


@app.post("/predict", response_model=EvaluationResponse)
def predict_candidate(candidate: CandidateInput) -> EvaluationResponse:
    data = candidate.model_dump()
    result = score_candidate(data)

    record = {
        **data,
        "selection_probability": result["selection_probability"],
        "tier": result["tier"],
    }
    eval_id = save_evaluation(record)

    return EvaluationResponse(
        id=eval_id,
        candidate_name=data["candidate_name"] or "Anonymous",
        cgpa=data["cgpa"],
        coding_score=data["coding_score"],
        interview_score=data["interview_score"],
        soft_skills=data["soft_skills"],
        college_tier=data["college_tier"],
        selection_probability=result["selection_probability"],
        tier=result["tier"],
        key_drivers=result["key_drivers"],
    )


@app.get("/evaluations", response_model=List[dict])
def list_evaluations(
    limit: int = Query(default=25, ge=1, le=200),
    tier: Optional[str] = Query(default=None),
) -> List[dict]:
    try:
        return fetch_evaluations(limit=limit, tier=tier)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))