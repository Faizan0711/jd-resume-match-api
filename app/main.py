from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.matcher import compare_skills, compute_score, extract_keywords 

app = FastAPI(title="JD-Resume Match Analyzer API", version="0.4.0")


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

    keywords = extract_keywords(payload.job_description, top_k=12)

    return AnalyzeResponse(
        match_score=score,
        matched_skills=matched,
        missing_skills=missing,
        top_keywords=keywords,
        recommendations=[
            "Step 4 done: extracted top JD keywords with weights.",
            "Use these JD terms naturally (truthfully): " + ", ".join([k["term"] for k in keywords[:6]]),
        ],
    )
