import os
from pathlib import Path
import json
import hashlib

CACHE_DIR = Path(os.getenv("CACHE_DIR", "/tmp/earthlens-cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_key(variable: str, region: str, start_year: int, end_year: int) -> str:
    """Generate a unique cache key for a dataset query."""
    key = f"{variable}_{region}_{start_year}_{end_year}"
    return hashlib.md5(key.encode()).hexdigest()

def get_cached_data(cache_key: str) -> dict | None:
    """Retrieve cached data if it exists."""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None

def set_cached_data(cache_key: str, data: dict) -> None:
    """Store data in the cache."""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    except IOError:
        pass
