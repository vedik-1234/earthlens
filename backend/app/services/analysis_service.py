import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple

from app.datasets.registry import DATASETS, REGIONS
from app.datasets.demo import DemoDataGenerator
from app.utils.errors import InsufficientDataError, AnalysisError


class AnalysisEngine:
    """Scientific analysis engine for trend detection and statistical testing."""
    
    def __init__(self):
        self.datasets = DATASETS
        self.regions = REGIONS
        self.demo_gen = DemoDataGenerator()
        self.significance_threshold = 0.05
    
    def _get_series(self, variable: str, start_year: int, end_year: int, region: str) -> pd.DataFrame:
        """Retrieve a time series for analysis."""
        if variable not in self.datasets:
            raise ValueError(f"Variable '{variable}' is not supported in the dataset registry.")
        
        if start_year >= end_year:
            raise ValueError("The selected time range is invalid. Please choose an end year later than the start year.")
        
        if region not in self.regions:
            raise ValueError(f"Region '{region}' is not available. Check available regions.")
        
        # Use demo data generator for now (production would fetch from NASA APIs)
        return self.demo_gen.get_series(variable, start_year, end_year, region)
    
    def _analyze_linear_trend(self, x: np.ndarray, y: np.ndarray, variable: str) -> Dict:
        """Perform linear regression analysis on time series data."""
        if len(x) < 3:
            raise InsufficientDataError(
                "Not enough valid observations are available for this region and time period to estimate a reliable trend."
            )
        
        # Linear regression
        slope, intercept, r_value, p_value, stderr = stats.linregress(x, y)
        
        # Fitted values
        fitted = intercept + slope * x
        
        # 95% confidence interval for slope
        t_stat = stats.t.ppf(0.975, len(x) - 2)
        ci_margin = t_stat * stderr
        ci_low = slope - ci_margin
        ci_high = slope + ci_margin
        
        # Summary statistics
        r_squared = r_value ** 2
        start_value = float(y[0])
        end_value = float(y[-1])
        total_change = float(end_value - start_value)
        
        # Percent change (if meaningful)
        if abs(start_value) > 1e-9:
            percent_change = float((total_change / abs(start_value)) * 100.0)
        else:
            percent_change = None
        
        mean_value = float(np.mean(y))
        
        return {
            "slope": float(slope),
            "intercept": float(intercept),
            "r_squared": float(r_squared),
            "p_value": float(p_value),
            "stderr": float(stderr),
            "confidence_interval": [float(ci_low), float(ci_high)],
            "fitted": fitted,
            "residuals": y - fitted,
            "start_value": start_value,
            "end_value": end_value,
            "total_change": total_change,
            "percent_change": percent_change,
            "mean_value": mean_value,
            "sample_size": len(x),
            "statistically_significant": p_value < self.significance_threshold,
        }
    
    def analyze(self, variable: str, region: str, start_year: int, end_year: int) -> Dict:
        """Perform a complete trend analysis for a variable in a region."""
        try:
            # Get data
            df = self._get_series(variable, start_year, end_year, region)
            df = df.dropna()
            
            if len(df) < 3:
                raise InsufficientDataError(
                    "Not enough valid observations are available for this region and time period to estimate a reliable trend."
                )
            
            x = df["year"].to_numpy(dtype=float)
            y = df["value"].to_numpy(dtype=float)
            
            # Perform analysis
            analysis = self._analyze_linear_trend(x, y, variable)
            
            # Get dataset metadata
            dataset = self.datasets[variable]
            
            # Build result
            result = {
                "status": "success",
                "variable": variable,
                "region": region,
                "period": f"{start_year}-{end_year}",
                "trend": round(analysis["slope"], 6),
                "unit": dataset["units"],
                "starting_value": round(analysis["start_value"], 4),
                "ending_value": round(analysis["end_value"], 4),
                "total_change": round(analysis["total_change"], 4),
                "percent_change": round(analysis["percent_change"], 4) if analysis["percent_change"] is not None else None,
                "p_value": round(analysis["p_value"], 6),
                "confidence_interval": [
                    round(analysis["confidence_interval"][0], 6),
                    round(analysis["confidence_interval"][1], 6)
                ],
                "r_squared": round(analysis["r_squared"], 4),
                "sample_size": int(analysis["sample_size"]),
                "statistically_significant": bool(analysis["statistically_significant"]),
                "significance_threshold": self.significance_threshold,
                "mean_value": round(analysis["mean_value"], 4),
                "data_source": "Demo dataset (development only)",
                "is_demo": True,
                "dataset_name": dataset["label"],
                "dataset_source": dataset["source"],
                "dataset_source_url": dataset["source_url"],
                "measurement_information": dataset["description"],
                "time_range": f"{start_year}-{end_year}",
                "spatial_resolution": "Regional summary from development configuration",
                "missing_data_handling": "Missing values are removed before fitting the regression model.",
                "statistical_method": "Linear regression with Ordinary Least Squares (OLS), p-value from t-distribution, and 95% confidence interval for the slope.",
                "limitations": "This implementation assumes a roughly linear trend and does not explicitly account for seasonality, autocorrelation, or heteroscedasticity. Confidence intervals are approximate and assume normality of residuals.",
                "trend_direction": "increasing" if analysis["slope"] > 0 else "decreasing" if analysis["slope"] < 0 else "stable",
                "series": [{"year": int(yr), "value": float(val)} for yr, val in zip(df["year"].tolist(), df["value"].tolist())],
                "fitted": [{"year": int(yr), "value": float(val)} for yr, val in zip(df["year"].tolist(), analysis["fitted"].tolist())],
            }
            
            return result
        
        except (ValueError, InsufficientDataError) as e:
            return {
                "status": "error",
                "error": str(e),
                "message": str(e),
            }
        except Exception as e:
            return {
                "status": "error",
                "error": "Internal analysis error",
                "message": "An unexpected error occurred during trend analysis.",
                "details": str(e),
            }
    
    def detect_trends(self, region: str, start_year: int, end_year: int) -> Dict:
        """Scan for measurable trends across all available variables."""
        findings = []
        
        for variable in ["temperature", "precipitation", "vegetation"]:
            try:
                result = self.analyze(variable, region, start_year, end_year)
                
                if result["status"] == "success":
                    findings.append({
                        "variable": variable,
                        "label": self.datasets[variable]["label"],
                        "direction": result["trend_direction"],
                        "trend": result["trend"],
                        "unit": result["unit"],
                        "period": result["period"],
                        "p_value": result["p_value"],
                        "statistically_significant": result["statistically_significant"],
                        "total_change": result["total_change"],
                        "source": result["data_source"],
                    })
            except Exception:
                continue
        
        return {
            "status": "success",
            "results": findings,
            "criteria": [
                "Magnitude of trend (|slope|)",
                "Statistical significance (p-value < 0.05)",
                "Valid data coverage (N >= 3)",
                "Temporal consistency"
            ],
            "region": region,
            "period": f"{start_year}-{end_year}",
        }
    
    def compare(self, variable_a: str, variable_b: str, region: str, start_year: int, end_year: int) -> Dict:
        """Compare trends between two variables."""
        result_a = self.analyze(variable_a, region, start_year, end_year)
        result_b = self.analyze(variable_b, region, start_year, end_year)
        
        if result_a["status"] != "success" or result_b["status"] != "success":
            return {
                "status": "error",
                "message": "One or both analyses failed."
            }
        
        # Calculate correlation
        a_values = np.array([entry["value"] for entry in result_a["series"]], dtype=float)
        b_values = np.array([entry["value"] for entry in result_b["series"]], dtype=float)
        
        if len(a_values) > 1 and len(b_values) > 1:
            corr_matrix = np.corrcoef(a_values, b_values)
            correlation = float(corr_matrix[0, 1]) if not np.isnan(corr_matrix[0, 1]) else 0.0
        else:
            correlation = 0.0
        
        return {
            "status": "success",
            "variable_a": result_a,
            "variable_b": result_b,
            "association": {
                "correlation": round(correlation, 4),
                "interpretation": "Statistical association detected between the selected variables." if abs(correlation) > 0.3 else "Weak or no association detected.",
                "caution": "This result describes an observed relationship. It does not establish causation or mechanism.",
            },
        }
    
    def explain(self, variable: str, region: str, start_year: int, end_year: int, trend_value: float, p_value: float, total_change: float, unit: str) -> Dict:
        """Generate a human-readable explanation of analysis results."""
        direction = "increasing" if trend_value > 0 else "decreasing" if trend_value < 0 else "stable"
        significance = "meets" if p_value < 0.05 else "does not meet"
        confidence_level = "95%" if p_value < 0.05 else "lower"
        
        summary = f"The selected region shows an estimated {direction} trend of {trend_value} {unit} over the {start_year}-{end_year} period. "
        summary += f"The statistical test gives a p-value of {p_value}, which {significance} the standard 5% significance threshold. "
        summary += f"This means the observed trend {significance} conventional criteria for statistical significance."
        
        return {
            "status": "success",
            "summary": summary,
            "segments": [
                {
                    "type": "observed_data",
                    "title": "What was measured",
                    "text": f"The region was analyzed for {variable} from {start_year} to {end_year}. This represents {end_year - start_year + 1} years of observations."
                },
                {
                    "type": "statistical_result",
                    "title": "Statistical finding",
                    "text": f"A linear trend model was fit to the data. The estimated slope is {trend_value} {unit}, with a p-value of {p_value}. The total change over the period was {total_change}."
                },
                {
                    "type": "interpretation",
                    "title": "What this means",
                    "text": f"The observed trend {significance} the chosen significance threshold (p < 0.05). This analysis describes the observed relationship in the selected region and does not establish its cause."
                },
                {
                    "type": "possible_explanations",
                    "title": "What could explain this",
                    "text": "Possible explanations may include natural climate variability, measurement or data coverage changes, regional climate forcing, land-use change, or other factors. This statistical test alone does not establish which explanation is correct."
                },
                {
                    "type": "limitations",
                    "title": "Limitations of this analysis",
                    "text": "This analysis assumes a linear relationship, does not account for seasonality or autocorrelation, and may be affected by data quality issues or gaps. Trends are approximate and should be interpreted with scientific caution."
                },
            ],
        }
