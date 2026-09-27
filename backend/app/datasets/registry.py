from pathlib import Path

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
