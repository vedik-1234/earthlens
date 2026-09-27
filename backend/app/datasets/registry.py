import os
from pathlib import Path

import numpy as np
import pandas as pd

DATASETS = {
    "temperature": {
        "name": "surface_temperature",
        "label": "Temperature",
        "description": "Land and sea surface temperature anomaly and warming trend.",
        "units": "°C/year",
        "source": "NASA Earthdata / MODIS / climate data products",
        "source_url": "https://www.earthdata.nasa.gov/",
        "type": "temperature",
        "region": "global",
        "real_endpoint": "https://example.nasa.gov/opendap/temperature",
        "keys": ["temperature", "land_surface_temperature", "sst"],
    },
    "precipitation": {
        "name": "precipitation",
        "label": "Precipitation",
        "description": "Precipitation accumulation and variability over time.",
        "units": "mm/month",
        "source": "NASA GPM / IMERG precipitation dataset",
        "source_url": "https://gpm.nasa.gov/data/imerg",
        "type": "precipitation",
        "region": "global",
        "real_endpoint": "https://example.nasa.gov/opendap/precipitation",
        "keys": ["precipitation", "rainfall", "daily_precip"],
    },
    "vegetation": {
        "name": "vegetation_index",
        "label": "Vegetation",
        "description": "Normalized difference vegetation index and productivity trends.",
        "units": "NDVI",
        "source": "NASA MODIS vegetation products",
        "source_url": "https://modis.gsfc.nasa.gov/data/",
        "type": "vegetation",
        "region": "global",
        "real_endpoint": "https://example.nasa.gov/opendap/vegetation",
        "keys": ["ndvi", "vegetation_index", "evi"],
    },
}

REGIONS = {
    "global": {"name": "Global", "bounds": [-180, -90, 180, 90]},
    "north_america": {"name": "North America", "bounds": [-168, 10, -52, 72]},
    "south_america": {"name": "South America", "bounds": [-82, -56, -34, 13]},
    "africa": {"name": "Africa", "bounds": [-18, -35, 55, 38]},
    "asia": {"name": "Asia", "bounds": [25, -10, 180, 80]},
    "australia": {"name": "Australia", "bounds": [112, -45, 154, -10]},
    "arctic": {"name": "Arctic", "bounds": [-180, 60, 180, 90]},
}

CACHE_DIR = Path(os.getenv("CACHE_DIR", "/tmp/earthlens-cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class DatasetService:
    def list_datasets(self):
        return [
            {
                "id": key,
                **config,
                "region_options": list(REGIONS.keys()),
            }
            for key, config in DATASETS.items()
        ]

    def get_dataset(self, variable):
        if variable not in DATASETS:
            raise ValueError(f"Unsupported variable: {variable}")
        return DATASETS[variable]

    def get_demo_series(self, variable, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        base = {"temperature": 12.4, "precipitation": 86.0, "vegetation": 0.51}[variable]
        slope = {"temperature": 0.018, "precipitation": 0.7, "vegetation": 0.0034}[variable]
        seasonal = {"temperature": 0.7, "precipitation": 12.0, "vegetation": 0.06}[variable]
        values = []
        rng = np.random.default_rng(42)
        for i, year in enumerate(years):
            drift = base + slope * (year - start_year)
            wave = seasonal * np.sin((i / max(1, len(years) - 1)) * np.pi * 2.0)
            noise = rng.normal(0.0, 0.18)
            values.append(float(drift + wave + noise))
        return pd.DataFrame({"year": years, "value": values})

    def build_region_summary(self, variable, region, start_year, end_year):
        df = self.get_demo_series(variable, start_year, end_year)
        return {
            "region": region,
            "variable": variable,
            "source": "Demo dataset (development only)",
            "year_range": f"{start_year}-{end_year}",
            "series": df.to_dict(orient="records"),
        }
