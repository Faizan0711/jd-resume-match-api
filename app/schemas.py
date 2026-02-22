from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzeRequest(BaseModel):
    job_description: str = Field(..., min_length=20)
    resume_text: str = Field(..., min_length=20)
    must_have_skills: Optional[List[str]] = None


class KeywordScore(BaseModel):
    term: str
    weight: float


class AnalyzeResponse(BaseModel):
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    top_keywords: List[KeywordScore]
    recommendations: List[str]