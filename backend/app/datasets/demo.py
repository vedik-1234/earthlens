"""Demo dataset generator for development and testing."""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class DemoDataGenerator:
    """Generate realistic demo environmental data."""
    
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)
    
    def generate_temperature_series(self, start_year: int, end_year: int, region: str = "global") -> pd.DataFrame:
        """Generate temperature anomaly time series."""
        years = list(range(start_year, end_year + 1))
        
        # Regional base temperatures
        base_temps = {
            "global": 13.5,
            "arctic": -15.0,
            "africa": 25.0,
            "south_america": 22.0,
            "north_america": 8.0,
            "asia": 15.0,
            "australia": 21.0,
        }
        base = base_temps.get(region, 13.5)
        
        # Warming trend
        slope = 0.018
        seasonal_amplitude = 0.65
        noise_std = 0.18
        
        values = []
        for idx, year in enumerate(years):
            # Long-term trend
            trend = base + slope * (year - start_year)
            
            # Seasonal oscillation
            seasonal = seasonal_amplitude * np.sin((idx / max(1, len(years) - 1)) * np.pi * 2.0)
            
            # Random noise
            noise = self.rng.normal(0.0, noise_std)
            
            value = trend + seasonal + noise
            values.append(float(value))
        
        return pd.DataFrame({"year": years, "value": values})
    
    def generate_precipitation_series(self, start_year: int, end_year: int, region: str = "global") -> pd.DataFrame:
        """Generate precipitation time series."""
        years = list(range(start_year, end_year + 1))
        
        # Regional precipitation baselines
        base_precip = {
            "global": 850.0,
            "arctic": 200.0,
            "africa": 650.0,
            "south_america": 1800.0,
            "north_america": 750.0,
            "asia": 920.0,
            "australia": 400.0,
        }
        base = base_precip.get(region, 850.0)
        
        # Precipitation trend
        slope = 0.7
        seasonal_amplitude = 10.0
        noise_std = 8.0
        
        values = []
        for idx, year in enumerate(years):
            trend = base + slope * (year - start_year)
            seasonal = seasonal_amplitude * np.sin((idx / max(1, len(years) - 1)) * np.pi * 2.0)
            noise = self.rng.normal(0.0, noise_std)
            value = max(0, trend + seasonal + noise)
            values.append(float(value))
        
        return pd.DataFrame({"year": years, "value": values})
    
    def generate_vegetation_series(self, start_year: int, end_year: int, region: str = "global") -> pd.DataFrame:
        """Generate vegetation index (NDVI) time series."""
        years = list(range(start_year, end_year + 1))
        
        # Regional vegetation baselines
        base_ndvi = {
            "global": 0.52,
            "arctic": 0.15,
            "africa": 0.45,
            "south_america": 0.68,
            "north_america": 0.55,
            "asia": 0.58,
            "australia": 0.35,
        }
        base = base_ndvi.get(region, 0.52)
        
        # Vegetation trend
        slope = 0.0033
        seasonal_amplitude = 0.05
        noise_std = 0.04
        
        values = []
        for idx, year in enumerate(years):
            trend = base + slope * (year - start_year)
            seasonal = seasonal_amplitude * np.sin((idx / max(1, len(years) - 1)) * np.pi * 2.0)
            noise = self.rng.normal(0.0, noise_std)
            value = np.clip(trend + seasonal + noise, -1.0, 1.0)
            values.append(float(value))
        
        return pd.DataFrame({"year": years, "value": values})
    
    def get_series(self, variable: str, start_year: int, end_year: int, region: str = "global") -> pd.DataFrame:
        """Get a time series for a given variable."""
        if variable == "temperature":
            return self.generate_temperature_series(start_year, end_year, region)
        elif variable == "precipitation":
            return self.generate_precipitation_series(start_year, end_year, region)
        elif variable == "vegetation":
            return self.generate_vegetation_series(start_year, end_year, region)
        else:
            raise ValueError(f"Unknown variable: {variable}")
