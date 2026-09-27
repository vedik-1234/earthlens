import os
from pathlib import Path
import numpy as np
import pandas as pd

from app.datasets.registry import DATASETS, REGIONS
from app.datasets.demo import DemoDataGenerator


class DatasetService:
    """Service for dataset management, discovery, and retrieval."""
    
    def __init__(self):
        self.datasets = DATASETS
        self.regions = REGIONS
        self.demo_gen = DemoDataGenerator()
    
    def list_datasets(self) -> list:
        """List all available datasets."""
        return [
            {
                "id": key,
                **config,
                "region_options": list(REGIONS.keys()),
            }
            for key, config in DATASETS.items()
        ]
    
    def get_dataset(self, variable: str) -> dict:
        """Get metadata for a specific dataset."""
        if variable not in DATASETS:
            raise ValueError(f"Variable '{variable}' is not supported in the dataset registry.")
        return DATASETS[variable]
    
    def list_regions(self) -> dict:
        """List all available regions."""
        return {
            key: {
                **config,
                "id": key,
            }
            for key, config in REGIONS.items()
        }
    
    def get_region(self, region_id: str) -> dict:
        """Get metadata for a specific region."""
        if region_id not in REGIONS:
            raise ValueError(f"Region '{region_id}' is not available.")
        return {**REGIONS[region_id], "id": region_id}
    
    def get_demo_series(self, variable: str, start_year: int, end_year: int, region: str = "global") -> pd.DataFrame:
        """Get a demo time series for development/testing."""
        return self.demo_gen.get_series(variable, start_year, end_year, region)
    
    def build_region_summary(self, variable: str, region: str, start_year: int, end_year: int) -> dict:
        """Build a summary of a variable in a region."""
        df = self.get_demo_series(variable, start_year, end_year, region)
        dataset = self.get_dataset(variable)
        
        return {
            "variable": variable,
            "region": region,
            "dataset_name": dataset["label"],
            "dataset_source": dataset["source"],
            "period": f"{start_year}-{end_year}",
            "series": df.to_dict(orient="records"),
            "statistics": {
                "count": len(df),
                "mean": float(df["value"].mean()),
                "std": float(df["value"].std()),
                "min": float(df["value"].min()),
                "max": float(df["value"].max()),
            },
        }
