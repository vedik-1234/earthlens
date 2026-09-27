from pathlib import Path

from fastapi import FastAPI

__all__ = ["app"]

app = FastAPI(title="EarthLens API")

@app.get("/ping")
def ping():
    return {"ok": True}
