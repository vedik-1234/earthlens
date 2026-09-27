import numpy as np
import pandas as pd
from scipy import stats

from app.datasets.registry import DATASETS, REGIONS


class AnalysisEngine:
    def __init__(self):
        self.datasets = DATASETS
        self.regions = REGIONS

    def _build_demo_series(self, variable, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        base = {"temperature": 12.5, "precipitation": 85.0, "vegetation": 0.52}[variable]
        slope = {"temperature": 0.018, "precipitation": 0.8, "vegetation": 0.0033}[variable]
        seasonal = {"temperature": 0.65, "precipitation": 10.0, "vegetation": 0.05}[variable]
        values = []
        rng = np.random.default_rng(99)
        for idx, year in enumerate(years):
            drift = base + slope * (year - start_year)
            wave = seasonal * np.sin((idx / max(1, len(years) - 1)) * np.pi * 2.0)
            noise = rng.normal(0.0, 0.18)
            values.append(float(drift + wave + noise))
        return pd.DataFrame({"year": years, "value": values})

    def _analyze_linear_trend(self, values, years, variable):
        df = pd.DataFrame({"year": years, "value": values}).dropna()
        if len(df) < 3:
            raise ValueError(
                "Not enough valid observations are available for this region and time period to estimate a reliable trend."
            )

        x = df["year"].to_numpy(dtype=float)
        y = df["value"].to_numpy(dtype=float)
        slope, intercept, r_value, p_value, stderr = stats.linregress(x, y)
        fitted = intercept + slope * x
        ci_low, ci_high = stats.t.interval(0.95, len(x) - 2, loc=slope, scale=stderr)
        start_value = float(y[0])
        end_value = float(y[-1])
        total_change = float(end_value - start_value)
        percent_change = None if abs(start_value) < 1e-9 else float((total_change / start_value) * 100.0)
        mean_value = float(np.mean(y))
        r_squared = float(r_value ** 2)

        return {
            "trend": float(slope),
            "unit": self.datasets[variable]["units"],
            "starting_value": start_value,
            "ending_value": end_value,
            "total_change": total_change,
            "percent_change": percent_change,
            "p_value": float(p_value),
            "confidence_interval": [float(ci_low), float(ci_high)],
            "r_squared": r_squared,
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
            {"type": "trend", "label": "Trend magnitude", "value": abs(slope), "class": trend_class},
            {"type": "significance", "label": "p-value", "value": p_value, "class": "significance"},
            {"type": "region", "label": "Region", "value": region, "class": "region"},
        ]

    def analyze(self, request):
        variable = request.variable
        if variable not in self.datasets:
            raise ValueError(f"Variable '{variable}' is not supported.")
        if request.start_year >= request.end_year:
            raise ValueError("The selected time range is invalid. Please choose an end year later than the start year.")

        series_df = self._build_demo_series(variable, request.start_year, request.end_year)
        analysis = self._analyze_linear_trend(series_df["value"].to_numpy(), series_df["year"].to_numpy(), variable)
        dataset = self.datasets[variable]

        return {
            "variable": variable,
            "region": request.region,
            "period": f"{request.start_year}-{request.end_year}",
            "trend": round(float(analysis["trend"]), 6),
            "unit": dataset["units"],
            "starting_value": round(float(analysis["starting_value"]), 4),
            "ending_value": round(float(analysis["ending_value"]), 4),
            "total_change": round(float(analysis["total_change"]), 4),
            "percent_change": round(float(analysis["percent_change"]), 4) if analysis["percent_change"] is not None else None,
            "p_value": round(float(analysis["p_value"]), 6),
            "confidence_interval": [round(float(analysis["confidence_interval"][0]), 6), round(float(analysis["confidence_interval"][1]), 6)],
            "r_squared": round(float(analysis["r_squared"]), 4),
            "sample_size": int(analysis["sample_size"]),
            "statistically_significant": bool(analysis["statistically_significant"]),
            "significance_threshold": 0.05,
            "mean_value": round(float(analysis["mean_value"]), 4),
            "data_source": "Demo dataset (development only)",
            "is_demo": True,
            "dataset_name": dataset["label"],
            "dataset_source": dataset["source"],
            "measurement_information": dataset["description"],
            "time_range": f"{request.start_year}-{request.end_year}",
            "spatial_resolution": "Regional summary from development configuration",
            "missing_data_handling": "Missing values are removed before fitting the regression.",
            "statistical_method": "Linear regression with p-value and 95% confidence interval for the slope.",
            "limitations": "This first implementation assumes a roughly linear trend and does not explicitly model seasonality or temporal autocorrelation.",
            "map_layers": self._build_map_layers(variable, request.region, analysis["trend"], analysis["p_value"]),
            "series": [{"year": int(y), "value": float(v)} for y, v in zip(series_df["year"].tolist(), series_df["value"].tolist())],
            "fitted": [{"year": int(y), "value": float(v)} for y, v in zip(series_df["year"].tolist(), analysis["fitted"].tolist())],
            "trend_direction": "increasing" if analysis["trend"] > 0 else "decreasing" if analysis["trend"] < 0 else "stable",
            "status": "success",
        }

    def detect_trends(self, request):
        findings = []
        for variable in ["temperature", "precipitation", "vegetation"]:
            try:
                result = self.analyze(type("Request", (), {
                    "variable": variable,
                    "region": request.region,
                    "start_year": request.start_year,
                    "end_year": request.end_year,
                })())
                findings.append({
                    "variable": variable,
                    "label": self.datasets[variable]["label"],
                    "direction": result["trend_direction"],
                    "trend": result["trend"],
                    "unit": result["unit"],
                    "period": result["period"],
                    "p_value": result["p_value"],
                    "statistically_significant": result["statistically_significant"],
                    "source": result["data_source"],
                })
            except Exception:
                continue
        return {
            "results": findings,
            "criteria": ["magnitude of trend", "statistical significance", "valid data coverage", "spatial consistency"],
            "status": "success",
        }

    def compare(self, request):
        result_a = self.analyze(type("Request", (), {
            "variable": request.variable_a,
            "region": request.region,
            "start_year": request.start_year,
            "end_year": request.end_year,
        })())
        result_b = self.analyze(type("Request", (), {
            "variable": request.variable_b,
            "region": request.region,
            "start_year": request.start_year,
            "end_year": request.end_year,
        })())
        xa = np.array([entry["value"] for entry in result_a["series"]], dtype=float)
        xb = np.array([entry["value"] for entry in result_b["series"]], dtype=float)
        corr = np.corrcoef(xa, xb)[0, 1]
        return {
            "variable_a": result_a,
            "variable_b": result_b,
            "association": {
                "correlation": float(corr) if not np.isnan(corr) else 0.0,
                "interpretation": "Statistical association detected between the selected variables.",
                "caution": "This does not imply causation."
            },
            "status": "success",
        }

    def explain(self, request):
        direction = "increasing" if request.trend_value > 0 else "decreasing" if request.trend_value < 0 else "stable"
        significance = "meets the chosen significance threshold" if request.p_value < 0.05 else "does not meet the chosen significance threshold"
        return {
            "summary": f"The selected region shows an estimated {direction} trend of {request.trend_value} {request.unit} over the selected period. The statistical test gives a p-value of {request.p_value}. This means the observed trend {significance}.",
            "segments": [
                {"type": "observed_data", "text": f"The region was analyzed for {request.variable} from {request.start_year} to {request.end_year}."},
                {"type": "statistical_result", "text": f"The fitted trend is {request.trend_value} {request.unit}, with total change of {request.total_change} and p-value {request.p_value}."},
                {"type": "interpretation", "text": "This analysis describes the observed relationship in the selected region and does not establish its cause."},
                {"type": "possible_explanations", "text": "Possible explanations may include natural variability, data coverage changes, or regional forcing, but those hypotheses are not proven by this result alone."},
            ],
            "status": "success",
        }
