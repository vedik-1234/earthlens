import math
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.api import OLS, add_constant

from app.datasets.registry import DATASETS, REGIONS


@dataclass
class TrendResult:
    variable: str
    region: str
    period: str
    trend: float
    unit: str
    starting_value: float
    ending_value: float
    total_change: float
    percent_change: float | None
    p_value: float
    confidence_interval: list[float]
    r_squared: float
    sample_size: int
    statistically_significant: bool
    significance_threshold: float
    mean_value: float
    data_source: str
    is_demo: bool
    dataset_name: str
    dataset_source: str
    measurement_information: str
    time_range: str
    spatial_resolution: str
    missing_data_handling: str
    statistical_method: str
    limitations: str
    map_layers: list[dict]


class AnalysisEngine:
    def __init__(self):
        self.datasets = DATASETS
        self.regions = REGIONS

    def _build_demo_series(self, variable, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        base = {
            "temperature": 12.6,
            "precipitation": 84.0,
            "vegetation": 0.52,
        }[variable]
        slope = {
            "temperature": 0.018,
            "precipitation": 0.7,
            "vegetation": 0.003,
        }[variable]
        seasonal = {
            "temperature": 0.6,
            "precipitation": 10.0,
            "vegetation": 0.05,
        }[variable]
        values = []
        for idx, year in enumerate(years):
            drift = base + slope * (year - start_year)
            wave = seasonal * np.sin((idx / max(1, len(years) - 1)) * np.pi * 2)
            noise = np.random.default_rng(197 + idx).normal(0.0, 0.14)
            values.append(float(drift + wave + noise))
        return pd.DataFrame({"year": years, "value": values})

    def _analyze_linear_trend(self, series, years, variable):
        df = pd.DataFrame({"year": years, "value": series})
        df = df.dropna()
        if len(df) < 3:
            raise ValueError("Not enough valid observations are available for this region and time period to estimate a reliable trend.")

        x = df["year"].to_numpy(dtype=float)
        y = df["value"].to_numpy(dtype=float)
        slope, intercept, r_value, p_value, stderr = stats.linregress(x, y)
        fitted = intercept + slope * x
        residuals = y - fitted
        r_squared = r_value ** 2
        ci_low, ci_high = stats.t.interval(0.95, len(x) - 2, loc=slope, scale=stderr)
        start_value = float(y[0])
        end_value = float(y[-1])
        total_change = float(end_value - start_value)
        percent_change = None if abs(start_value) < 1e-9 else float((total_change / start_value) * 100.0)
        mean_value = float(np.mean(y))

        return {
            "trend": float(slope),
            "unit": self.datasets[variable]["units"],
            "starting_value": start_value,
            "ending_value": end_value,
            "total_change": total_change,
            "percent_change": percent_change,
            "p_value": float(p_value),
            "confidence_interval": [float(ci_low), float(ci_high)],
            "r_squared": float(r_squared),
            "sample_size": int(len(df)),
            "mean_value": mean_value,
            "fitted": fitted,
            "observed": y,
            "years": x,
            "statistically_significant": bool(p_value < 0.05),
        }

    def _build_map_layers(self, variable, region, slope, p_value):
        trend_class = "Increasing" if slope > 0 and p_value < 0.05 else "Decreasing" if slope < 0 and p_value < 0.05 else "No significant trend"
        return [
            {"type": "trend", "label": "Magnitude", "value": abs(slope), "class": trend_class},
            {"type": "significance", "label": "p-value", "value": p_value, "class": "p_value"},
            {"type": "layer", "label": "Region", "value": region},
        ]

    def analyze(self, request):
        variable = request.variable
        region = request.region
        start_year = request.start_year
        end_year = request.end_year

        if variable not in self.datasets:
            raise ValueError(f"Variable '{variable}' is not supported in the current EarthLens dataset registry.")
        if start_year >= end_year:
            raise ValueError("The selected time range is invalid. Please choose an end year later than the start year.")

        series_df = self._build_demo_series(variable, start_year, end_year)
        years = series_df["year"].to_numpy()
        values = series_df["value"].to_numpy()
        result = self._analyze_linear_trend(values, years, variable)

        dataset = self.datasets[variable]
        period = f"{start_year}-{end_year}"
        trend_result = {
            "variable": variable,
            "region": region,
            "period": period,
            "trend": round(result["trend"], 6),
            "unit": dataset["units"],
            "starting_value": round(result["starting_value"], 4),
            "ending_value": round(result["ending_value"], 4),
            "total_change": round(result["total_change"], 4),
            "percent_change": round(result["percent_change"], 4) if result["percent_change"] is not None else None,
            "p_value": round(result["p_value"], 6),
            "confidence_interval": [round(result["confidence_interval"][0], 6), round(result["confidence_interval"][1], 6)],
            "r_squared": round(result["r_squared"], 4),
            "sample_size": result["sample_size"],
            "statistically_significant": result["statistically_significant"],
            "significance_threshold": 0.05,
            "mean_value": round(result["mean_value"], 4),
            "source": dataset["source"],
            "data_source": "Demo dataset (development only)",
            "is_demo": True,
            "dataset_name": dataset["label"],
            "dataset_source": dataset["source"],
            "measurement_information": dataset["description"],
            "time_range": period,
            "spatial_resolution": "Regional summary from demo configuration",
            "missing_data_handling": "Missing values are removed before fitting the trend model.",
            "statistical_method": "Linear regression with p-value and 95% confidence interval for slope.",
            "limitations": "This first implementation assumes a roughly linear trend and does not explicitly model seasonality or temporal autocorrelation.",
            "map_layers": self._build_map_layers(variable, region, result["trend"], result["p_value"]),
            "series": [{"year": int(y), "value": float(v)} for y, v in zip(list(series_df["year"]), list(series_df["value"]))],
            "fitted": [{"year": int(y), "value": float(v)} for y, v in zip(list(series_df["year"]), list(result["fitted"]))],
            "trend_direction": "increasing" if result["trend"] > 0 else "decreasing" if result["trend"] < 0 else "stable",
        }
        return trend_result

    def detect_trends(self, request):
        variables = ["temperature", "precipitation", "vegetation"]
        results = []
        for variable in variables:
            try:
                result = self.analyze(type("R", (), {
                    "variable": variable,
                    "region": request.region,
                    "start_year": request.start_year,
                    "end_year": request.end_year,
                })())
                results.append({
                    "variable": variable,
                    "label": self.datasets[variable]["label"],
                    "trend": result["trend"],
                    "unit": result["unit"],
                    "period": result["period"],
                    "p_value": result["p_value"],
                    "direction": result["trend_direction"],
                    "statistically_significant": result["statistically_significant"],
                    "source": result["data_source"],
                })
            except Exception:
                continue
        return {"results": results, "criteria": ["magnitude of slope", "p-value", "consistency across valid observations", "data coverage"]}

    def compare(self, request):
        result_a = self.analyze(type("R", (), {
            "variable": request.variable_a,
            "region": request.region,
            "start_year": request.start_year,
            "end_year": request.end_year,
        })())
        result_b = self.analyze(type("R", (), {
            "variable": request.variable_b,
            "region": request.region,
            "start_year": request.start_year,
            "end_year": request.end_year,
        })())

        x = np.array([point["value"] for point in result_a["series"]], dtype=float)
        y = np.array([point["value"] for point in result_b["series"]], dtype=float)
        corr, _ = np.corrcoef(x, y)
        corr_value = float(corr[0, 1]) if len(x) > 1 and not np.isnan(corr[0, 1]) else 0.0

        return {
            "variable_a": result_a,
            "variable_b": result_b,
            "association": {
                "correlation": round(corr_value, 4),
                "interpretation": "Statistical association detected between the selected variables.",
                "caution": "This does not imply causation."
            }
        }

    def explain(self, request):
        direction = "increasing" if request.trend_value > 0 else "decreasing" if request.trend_value < 0 else "stable"
        significance = "meets the chosen significance threshold" if request.p_value < 0.05 else "does not meet the chosen significance threshold"
        return {
            "summary": f"The selected region shows an estimated {direction} trend of {request.trend_value} {request.unit} over the selected period. The statistical test gives a p-value of {request.p_value}. This means the observed trend {significance}.",
            "segments": [
                {"type": "observed_data", "text": f"The region was analyzed for {request.variable} from {request.start_year} to {request.end_year}."},
                {"type": "statistical_result", "text": f"The fitted trend is {request.trend_value} {request.unit}, with total change of {request.total_change} and a p-value of {request.p_value}."},
                {"type": "interpretation", "text": f"This analysis describes the observed relationship in the selected region and does not establish its cause."},
                {"type": "possible_explanations", "text": "Possible explanations may include natural variability, regional forcing, or changes in data coverage, but those are not established by this statistical test alone."}
            ]
        }
