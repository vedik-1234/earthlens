"""Pydantic request/response schemas with validation."""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional


class AnalysisRequest(BaseModel):
    """Request to analyze environmental trend."""
    variable: str = Field(default='temperature')
    region: str = Field(default='global')
    start_year: int = Field(default=2003, ge=1980, le=2100)
    end_year: int = Field(default=2025, ge=1980, le=2100)
    region_bounds: Optional[dict] = None

    @field_validator('start_year', 'end_year')
    def validate_years(cls, v):
        if v < 1980 or v > 2100:
            raise ValueError('Year must be between 1980 and 2100')
        return v


class TrendDetectRequest(BaseModel):
    """Request to detect interesting trends."""
    region: str = Field(default='global')
    start_year: int = Field(default=2003, ge=1980, le=2100)
    end_year: int = Field(default=2025, ge=1980, le=2100)
    region_bounds: Optional[dict] = None


class CompareRequest(BaseModel):
    """Request to compare two variables."""
    variable_a: str = Field(default='temperature')
    variable_b: str = Field(default='precipitation')
    region: str = Field(default='global')
    start_year: int = Field(default=2003, ge=1980, le=2100)
    end_year: int = Field(default=2025, ge=1980, le=2100)


class ExplanationRequest(BaseModel):
    """Request for AI-generated explanation."""
    variable: str = Field(default='temperature')
    region: str = Field(default='global')
    start_year: int = Field(default=2003, ge=1980, le=2100)
    end_year: int = Field(default=2025, ge=1980, le=2100)
    trend_value: float = Field(default=0.038)
    p_value: float = Field(default=0.0008, ge=0.0, le=1.0)
    total_change: float = Field(default=0.84)
    unit: str = Field(default='°C/year')


class SignupRequest(BaseModel):
    """User signup request."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class SigninRequest(BaseModel):
    """User signin request."""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class DatasetConfig(BaseModel):
    """Dataset configuration."""
    name: str
    label: str
    description: str
    units: str
    source: str
    source_url: str
    type: str
    region: str
    real_endpoint: Optional[str] = None
    keys: Optional[list[str]] = None
