from fastapi import FastAPI
from app.schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(title="JD-Resume Match Analyzer API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    # Step 1 stub: returns a predictable placeholder response
    # In Step 2, we'll replace this with real matching logic.
    return AnalyzeResponse(
        match_score=50,
        matched_skills=[],
        missing_skills=[],
        top_keywords=[],
        recommendations=[
            "Step 1 is running. Next we’ll implement skill extraction + scoring."
        ],
    )