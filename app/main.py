from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.matcher import compare_skills

app = FastAPI(title="JD-Resume Match Analyzer API", version="0.2.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    matched, missing = compare_skills(payload.job_description, payload.resume_text)

    return AnalyzeResponse(
        match_score=0,  # Step 3: scoring
        matched_skills=matched,
        missing_skills=missing,
        top_keywords=[],  # Step 4
        recommendations=[
            "Step 2 done: skill extraction + comparison works.",
            "Next: implement scoring (0–100) and keyword weighting."
        ],
    )