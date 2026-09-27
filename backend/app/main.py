import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import AnalysisRequest, TrendDetectRequest, CompareRequest, ExplanationRequest
from app.services.analysis_service import AnalysisEngine
from app.services.dataset_service import DatasetService

app = FastAPI(
    title="EarthLens",
    version="1.0.0",
    description="Interactive NASA Earth-observation platform for discovering environmental trends",
    docs_url="/docs",
    redoc_url="/redoc",
)

configured_origins = os.getenv("EARTHLENS_ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
# A wildcard is useful for an ephemeral ngrok demo only. Prefer explicit origins
# in deployed environments.
if os.getenv("EARTHLENS_ENV", "development") == "development":
    allowed_origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analysis_engine = AnalysisEngine()
dataset_service = DatasetService()

@app.get("/")
def root():
    return {"app": "EarthLens", "version": "1.0.0", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": "EarthLens",
        "mode": os.getenv("NASA_DATA_MODE", "demo"),
        "message": "EarthLens backend is running.",
    }

@app.get("/api/datasets")
def get_datasets():
    return {"status": "success", "datasets": dataset_service.list_datasets()}

@app.get("/api/regions")
def get_regions():
    return {"status": "success", "regions": dataset_service.list_regions()}

@app.post("/api/analyze")
def analyze(request: AnalysisRequest):
    try:
        return analysis_engine.analyze(request.variable, request.region, request.start_year, request.end_year)
    except Exception as exc:
        return {"status": "error", "error": "AnalysisError", "message": str(exc)}

@app.post("/api/trend-detect")
def detect_trends(request: TrendDetectRequest):
    try:
        return analysis_engine.detect_trends(request.region, request.start_year, request.end_year)
    except Exception as exc:
        return {"status": "error", "error": "TrendDetectionError", "message": str(exc)}

@app.post("/api/compare")
def compare_variables(request: CompareRequest):
    try:
        return analysis_engine.compare(request.variable_a, request.variable_b, request.region, request.start_year, request.end_year)
    except Exception as exc:
        return {"status": "error", "error": "ComparisonError", "message": str(exc)}

@app.post("/api/explain")
def explain_result(request: ExplanationRequest):
    try:
        return analysis_engine.explain(request.variable, request.region, request.start_year, request.end_year, request.trend_value, request.p_value, request.total_change, request.unit)
    except Exception as exc:
        return {"status": "error", "error": "ExplanationError", "message": str(exc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
