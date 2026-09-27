from pathlib import Path

from pydantic import BaseModel, Field
from typing import Optional


class AnalysisRequest(BaseModel):
    variable: str = Field(default="temperature")
    region: str = Field(default="global")
    start_year: int = Field(default=2003)
    end_year: int = Field(default=2025)
    region_bounds: Optional[dict] = None


class TrendDetectRequest(BaseModel):
    region: str = Field(default="global")
    start_year: int = Field(default=2003)
    end_year: int = Field(default=2025)
    region_bounds: Optional[dict] = None


class CompareRequest(BaseModel):
    variable_a: str = Field(default="temperature")
    variable_b: str = Field(default="precipitation")
    region: str = Field(default="global")
    start_year: int = Field(default=2003)
    end_year: int = Field(default=2025)


class ExplanationRequest(BaseModel):
    variable: str = Field(default="temperature")
    region: str = Field(default="global")
    start_year: int = Field(default=2003)
    end_year: int = Field(default=2025)
    trend_value: float = Field(default=0.038)
    p_value: float = Field(default=0.0008)
    total_change: float = Field(default=0.84)
    unit: str = Field(default="°C/year")
