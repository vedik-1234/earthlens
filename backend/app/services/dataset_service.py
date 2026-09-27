import os
from pathlib import Path

import numpy as np
import pandas as pd

DATASETS = {
    "temperature": {
        "id": "temperature",
        "label": "Temperature",
        "name": "surface_temperature",
        "units": "°C/year",
        "source": "NASA Earthdata / MODIS / climate products",
        "description": "Temperature trend across a defined region and time range.",
        "real_endpoint": "https://www.earthdata.nasa.gov/",
        "type": "temperature",
    },
    "precipitation": {
        "id": "precipitation",
        "label": "Precipitation",
        "name": "precipitation",
        "units": "mm/month",
        "source": "NASA GPM IMERG",
        "description": "Precipitation variability and accumulation.",
        "real_endpoint": "https://gpm.nasa.gov/data/imerg",
        "type": "precipitation",
    },
    "vegetation": {
        "id": "vegetation",
        "label": "Vegetation",
        "name": "vegetation_index",
        "units": "NDVI",
        "source": "NASA MODIS vegetation products",
        "description": "Vegetation productivity and greening trends.",
        "real_endpoint": "https://modis.gsfc.nasa.gov/data/",
        "type": "vegetation",
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
        return [{"id": key, **config, "region_options": list(REGIONS.keys())} for key, config in DATASETS.items()]

    def get_dataset(self, variable):
        if variable not in DATASETS:
            raise ValueError(f"Variable '{variable}' is not supported in the dataset registry.")
        return DATASETS[variable]

    def get_demo_series(self, variable, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        base = {"temperature": 12.5, "precipitation": 85.0, "vegetation": 0.52}[variable]
        slope = {"temperature": 0.018, "precipitation": 0.8, "vegetation": 0.0033}[variable]
        seasonal = {"temperature": 0.65, "precipitation": 10.0, "vegetation": 0.05}[variable]
        values = []
        rng = np.random.default_rng(21)
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
            "series": df.to_dict(orient="records"),
        }
