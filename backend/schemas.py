from typing import List, Optional
from pydantic import BaseModel, Field


class CandidateInput(BaseModel):
    candidate_name: Optional[str] = Field(default="Anonymous", max_length=120)
    cgpa: float = Field(..., ge=0.0, le=10.0, description="CGPA on a 10-point scale")
    coding_score: float = Field(..., ge=0.0, le=100.0, description="Coding assessment score (0-100)")
    interview_score: float = Field(..., ge=0.0, le=100.0, description="Interview score (0-100)")
    soft_skills: float = Field(..., ge=0.0, le=100.0, description="Soft skills score (0-100)")
    college_tier: int = Field(..., ge=1, le=3, description="College tier: 1 (Top), 2 (Mid), 3 (Other)")


class EvaluationResponse(BaseModel):
    id: int
    candidate_name: str
    cgpa: float
    coding_score: float
    interview_score: float
    soft_skills: float
    college_tier: int
    selection_probability: float
    tier: str
    key_drivers: List[str]