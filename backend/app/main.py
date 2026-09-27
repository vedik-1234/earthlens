from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.models.schemas import AnalysisRequest, TrendDetectRequest, CompareRequest, ExplanationRequest
from app.services.analysis_service import AnalysisEngine
from app.services.dataset_service import DatasetService

app = FastAPI(title="EarthLens", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analysis_engine = AnalysisEngine()
dataset_service = DatasetService()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": "EarthLens",
        "mode": os.getenv("NASA_DATA_MODE", "demo"),
        "message": "EarthLens backend is running."
    }

@app.get("/api/datasets")
def datasets():
    return {"datasets": dataset_service.list_datasets()}

@app.post("/api/analyze")
def analyze(request: AnalysisRequest):
    try:
        return analysis_engine.analyze(request)
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "message": "Unable to complete the requested trend analysis. Check the selected variable, region, and time window.",
            "is_demo": True,
        }

@app.post("/api/trend-detect")
def detect(request: TrendDetectRequest):
    try:
        return analysis_engine.detect_trends(request)
    except Exception as exc:
        return {"status": "error", "error": str(exc), "message": "Trend detection could not be completed."}

@app.post("/api/compare")
def compare(request: CompareRequest):
    try:
        return analysis_engine.compare(request)
    except Exception as exc:
        return {"status": "error", "error": str(exc), "message": "Comparison could not be completed."}

@app.post("/api/explain")
def explain(request: ExplanationRequest):
    try:
        return analysis_engine.explain(request)
    except Exception as exc:
        return {"status": "error", "error": str(exc), "message": "Explanation generation failed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
