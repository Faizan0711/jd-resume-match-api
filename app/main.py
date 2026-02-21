from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.matcher import compare_skills, compute_score  

app = FastAPI(title="JD-Resume Match Analyzer API", version="0.2.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    matched, missing = compare_skills(payload.job_description, payload.resume_text)
    score = compute_score(
        payload.job_description,
        payload.resume_text,
        must_have_skills=payload.must_have_skills,
    )

    return AnalyzeResponse(
        match_score=score,
        matched_skills=matched,
        missing_skills=missing,
        top_keywords=[],
        recommendations=[
            "Step 3 done: match_score is now computed from skill overlap + must-haves.",
            "Next: keyword extraction (top JD terms) and better recommendations."
        ],
    )