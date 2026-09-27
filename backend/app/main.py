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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analysis_engine = AnalysisEngine()
dataset_service = DatasetService()


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "app": "EarthLens",
        "version": "1.0.0",
        "description": "Interactive NASA Earth-observation platform",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": "EarthLens",
        "mode": os.getenv("NASA_DATA_MODE", "demo"),
        "message": "EarthLens backend is running.",
    }


@app.get("/api/datasets")
def get_datasets():
    """List all available datasets."""
    return {
        "status": "success",
        "datasets": dataset_service.list_datasets(),
    }


@app.get("/api/regions")
def get_regions():
    """List all available regions."""
    return {
        "status": "success",
        "regions": dataset_service.list_regions(),
    }


@app.post("/api/analyze")
def analyze(request: AnalysisRequest):
    """Perform a trend analysis for a selected variable and region."""
    try:
        result = analysis_engine.analyze(
            variable=request.variable,
            region=request.region,
            start_year=request.start_year,
            end_year=request.end_year,
        )
        return result
    except Exception as exc:
        return {
            "status": "error",
            "error": "AnalysisError",
            "message": "Unable to complete the requested trend analysis. Check the selected variable, region, and time window.",
            "details": str(exc),
        }


@app.post("/api/trend-detect")
def detect_trends(request: TrendDetectRequest):
    """Detect interesting trends across all available variables."""
    try:
        result = analysis_engine.detect_trends(
            region=request.region,
            start_year=request.start_year,
            end_year=request.end_year,
        )
        return result
    except Exception as exc:
        return {
            "status": "error",
            "error": "TrendDetectionError",
            "message": "Trend detection could not be completed.",
            "details": str(exc),
        }


@app.post("/api/compare")
def compare_variables(request: CompareRequest):
    """Compare trends between two variables."""
    try:
        result = analysis_engine.compare(
            variable_a=request.variable_a,
            variable_b=request.variable_b,
            region=request.region,
            start_year=request.start_year,
            end_year=request.end_year,
        )
        return result
    except Exception as exc:
        return {
            "status": "error",
            "error": "ComparisonError",
            "message": "Comparison could not be completed.",
            "details": str(exc),
        }


@app.post("/api/explain")
def explain_result(request: ExplanationRequest):
    """Generate an AI explanation for analysis results."""
    try:
        result = analysis_engine.explain(
            variable=request.variable,
            region=request.region,
            start_year=request.start_year,
            end_year=request.end_year,
            trend_value=request.trend_value,
            p_value=request.p_value,
            total_change=request.total_change,
            unit=request.unit,
        )
        return result
    except Exception as exc:
        return {
            "status": "error",
            "error": "ExplanationError",
            "message": "Explanation generation failed.",
            "details": str(exc),
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
