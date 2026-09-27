# EarthLens

EarthLens is a NASA-inspired scientific exploration platform for detecting and quantifying environmental change using real Earth-observation and climate datasets, with a strong emphasis on transparent statistics and reproducible analysis.

## Challenge connection

This project addresses the NASA Space Apps Challenge 2026 theme, “Be An Earth System Trend Detective!” by helping users answer:

- What environmental variable is changing?
- Where is it changing?
- How much is it changing?
- How has it changed over time?
- Is the change statistically significant?
- Does the trend vary by region?

## How EarthLens addresses the challenge

EarthLens focuses on the core challenge questions directly:

- What is changing?: users select environmental variables such as temperature, precipitation, and vegetation.
- Where is it changing?: the app supports global and regional analysis with a map-based region selector.
- How much is it changing?: the scientific engine computes absolute change, percent change, and slope per year.
- Is it statistically significant?: every trend includes p-values, confidence intervals, and model diagnostics.

## Architecture

- Frontend: React + Vite + Tailwind CSS + Plotly + Leaflet
- Backend: FastAPI + NumPy + pandas + SciPy + statsmodels + xarray
- Data layer: NASA dataset configuration registry with pluggable dataset providers and cache
- Scientific engine: time-series regression, significance testing, and transparent result metadata

## NASA data sources

The project is designed around NASA Earthdata-compatible services and NASA-housed datasets, including:

- NASA MODIS land surface temperature and vegetation products
- NASA GPM IMERG precipitation products
- NASA Earthdata OPeNDAP and dataset metadata endpoints
- Dataset registry architecture allows additional NASA records to be added without changing the application logic

The initial app is built to work with a realistic, pluggable dataset configuration. In local development, a clearly labeled demo dataset is used when remote NASA services are unavailable so the application remains runnable.

## Scientific methodology

The core workflow is:

1. Select a variable and region.
2. Download or access the relevant NASA data slice.
3. Aggregate the time series for the selected region.
4. Fit a linear trend model.
5. Estimate confidence intervals and p-values.
6. Visualize spatial and temporal patterns.
7. Present statistically transparent results with metadata and caveats.

The first implementation uses linear regression because it is interpretable and practical for a hackathon. It explicitly documents assumptions, including roughly linear change over time, temporal independence assumptions, and limitations associated with seasonality and autocorrelation.

## Statistical methodology

Each analysis computes:

- mean value
- starting and ending values
- absolute change
- percent change (when meaningful)
- linear slope
- 95% confidence interval for the slope
- p-value
- R²
- sample size
- uncertainty

The backend uses:

- `scipy.stats.linregress` for slope and p-values
- `statsmodels` for robust linear trend modeling
- confidence intervals to communicate uncertainty
- significance threshold p < 0.05 by default

## Project structure

```text
earthlens/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── datasets/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env.example
├── README.md
├── docker-compose.yml
├── start.sh
├── start.bat
└── .gitignore
```

## Setup instructions

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev -- --host 0.0.0.0 --port 5173
```

### Launch both apps together

```bash
./start.sh
```

On Windows:

```bat
start.bat
```

## Environment variables

Example values are provided in:

- `backend/.env.example`
- `frontend/.env.example`

Important variables include:

- `EARTHLENS_ENV`
- `NASA_DATA_MODE`
- `CACHE_DIR`
- `BACKEND_URL`
- `VITE_API_URL`

## API documentation

FastAPI automatically exposes OpenAPI docs at:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Limitations

- Real NASA data access depends on remote service availability and network access.
- Some public NASA endpoints require Earthdata authentication or retrieval workflow complexity.
- This implementation prioritizes scientific clarity and reproducibility over full planetary-scale raster processing.
- Linear regression is a first-pass method and does not fully resolve complex seasonal or autocorrelated behavior.

## Future improvements

- Add richer spatial grid analysis for rasters.
- Integrate Earthdata login flows for authenticated downloads.
- Expand dataset registry to include more NASA climate products.
- Add robust region-drawing selection for arbitrary polygons.
- Extend trend detection with seasonal decomposition and autocorrelation-aware models.

## License

This project is created for the NASA Space Apps Challenge 2026 and is intended for educational and exploratory use.

## Important note

The application is designed to work with real NASA data sources wherever possible, but a clearly labeled demo dataset is included for local development and offline or rate-limited situations. The production app distinguishes this mode in the UI and API results so users can tell when they are viewing a development-only dataset rather than a NASA product.

## Design and science goals

EarthLens blends a premium scientific interface with rigorous environmental analysis. The result is intended to feel like a modern Earth-observation application while remaining understandable to a high-school student and transparent to a scientist.

This repository starts with a complete app skeleton and a working analysis pipeline that can be extended with additional NASA products and richer spatial workflows.

---

This project is under active development as a challenge build.

---

This README is intentionally written to reflect the NASA Space Apps Challenge brief and the EarthLens product requirements.

---

EarthLens is a scientific exploration platform designed to make environmental change understandable, measurable, and visually interpretable.

---

Choose a variable, a region, and a period, then investigate how Earth’s systems are changing.

---

EarthLens helps users move from raw NASA data to transparent, evidence-based scientific interpretation.

---

The goal is not to make a glamorous climate dashboard; it is to build a credible tool that supports real scientific inquiry.

---

EarthLens is a challenge-ready science application rooted in data, statistics, and careful interpretation.

---

Explore NASA Earth-observation data, discover patterns, and understand the evidence.

---

Start investigating Earth’s changing systems with EarthLens.

---

Welcome to EarthLens.

---

The Earth is changing. EarthLens helps you measure it.

---

A premium, transparent, and scientifically grounded environmental trend detector.
