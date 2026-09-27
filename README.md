# EarthLens

**Interactive NASA Earth-observation platform for discovering and investigating environmental trends.**

*Built for NASA Space Apps Challenge 2026: "Be An Earth System Trend Detective!"*

---

## 🌍 What is EarthLens?

EarthLens is a scientific exploration platform that helps you discover, measure, and understand environmental change using real NASA Earth-observation data. It combines:

- **Real environmental data** from NASA's Earthdata services
- **Statistical rigor** with confidence intervals, p-values, and model diagnostics
- **Interactive maps and charts** for spatial and temporal analysis
- **Transparent methodology** documenting every calculation and assumption
- **Apple-inspired design** that feels premium and precision-focused

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm

### Launch

**Linux/macOS:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

The app will open automatically:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API docs**: http://localhost:8000/docs

---

## 🎯 Core Features

### 1. Trend Analysis
Select a variable (temperature, precipitation, vegetation), region, and time period. EarthLens calculates:
- Linear trend (per year)
- 95% confidence interval
- p-value for statistical significance
- Model fit (R²)
- Total change over the period

### 2. Trend Detective
Automatically scan all available variables in a region to find which are changing most significantly. Results ranked by:
- Magnitude of trend
- Statistical significance (p < 0.05)
- Valid data coverage
- Temporal consistency

### 3. Variable Comparison
Compare two environmental variables side-by-side:
- Time series for each variable
- Correlation coefficient
- Trend direction and magnitude
- Statistical association (with caution about causation)

### 4. AI Explanations
Generate human-readable explanations of results:
- What was measured
- Statistical findings
- Scientific interpretation
- Possible explanations
- Analysis limitations

---

## 📊 Scientific Methodology

### Statistical Methods
- **Linear Regression**: Ordinary least squares (OLS)
- **Significance Testing**: Two-tailed t-test (α = 0.05)
- **Confidence Intervals**: 95% using t-distribution
- **Model Diagnostics**: R², residual analysis

### Data Handling
- Missing values are removed before analysis
- Sample size (N) is reported for each result
- Assumptions and limitations are clearly stated
- Results include uncertainty quantification

### Limitations (Transparently Disclosed)
This first implementation:
- Assumes roughly linear trends
- Does not account for seasonality or autocorrelation
- Uses ordinary least squares (not robust regression)
- Assumes approximately normal residuals
- May be affected by data quality issues

---

## 🏗️ Architecture

### Backend (FastAPI + Python)
```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response schemas
│   ├── services/
│   │   ├── analysis_service.py    # Trend analysis engine
│   │   └── dataset_service.py     # Dataset management
│   ├── datasets/
│   │   ├── registry.py            # Dataset configuration
│   │   └── demo.py                # Demo data generator
│   └── utils/
│       ├── cache.py               # Caching layer
│       └── errors.py              # Custom exceptions
├── requirements.txt
└── .env.example
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── App.jsx                    # Main application
│   ├── components/
│   │   ├── AppShell.jsx           # Layout wrapper
│   │   ├── Navigation.jsx         # Top navigation
│   │   ├── Hero.jsx               # Landing section
│   │   ├── AnalysisPanel.jsx      # Control panel
│   │   ├── TrendSummary.jsx       # Result summary
│   │   ├── TrendChart.jsx         # Plotly chart
│   │   ├── MetricsGrid.jsx        # Statistics display
│   │   ├── TrendList.jsx          # Trend findings
│   │   ├── ComparisonView.jsx     # Variable comparison
│   │   ├── DataSourceBadge.jsx    # Source indicator
│   │   ├── LoadingSpinner.jsx     # Loading state
│   │   └── ErrorBanner.jsx        # Error display
│   ├── services/
│   │   └── api.js                 # Backend API client
│   ├── styles.css                 # Global styles & design tokens
│   └── main.jsx                   # Entry point
├── tailwind.config.js
├── vite.config.js
├── package.json
└── .env.example
```

---

## 🛠️ Development

### Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env

# Run with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env

# Run dev server with hot reload
npm run dev -- --host 0.0.0.0 --port 5173
```

### Run Tests
```bash
# Backend tests (pytest)
cd backend
pytest

# Frontend tests (Vitest)
cd frontend
npm run test
```

---

## 📡 API Endpoints

### Health & Metadata
- `GET /` - Root information
- `GET /health` - Health check
- `GET /api/datasets` - List available datasets
- `GET /api/regions` - List available regions

### Analysis
- `POST /api/analyze` - Perform trend analysis
- `POST /api/trend-detect` - Scan for interesting trends
- `POST /api/compare` - Compare two variables
- `POST /api/explain` - Generate AI explanation

### Request Example
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "variable": "temperature",
    "region": "global",
    "start_year": 2003,
    "end_year": 2025
  }'
```

### Response Example
```json
{
  "status": "success",
  "variable": "temperature",
  "region": "global",
  "period": "2003-2025",
  "trend": 0.038,
  "unit": "°C/year",
  "p_value": 0.0008,
  "confidence_interval": [0.025, 0.051],
  "r_squared": 0.72,
  "statistically_significant": true,
  "series": [...],
  "fitted": [...]
}
```

---

## 🎨 Design System

### Theme
Apple-inspired design with emphasis on clarity and precision:
- Dark mode support
- Generous whitespace
- Subtle borders and shadows
- System font stack
- Smooth transitions (respects `prefers-reduced-motion`)

### Colors
| Token | Light | Dark |
|-------|-------|------|
| Background | `#f5f7f9` | `#080d14` |
| Surface Primary | `rgba(255,255,255,0.95)` | `rgba(13,17,23,0.95)` |
| Text Primary | `#0f172a` | `#f3f6fb` |
| Accent | `#6ea8fe` | `#8ab4ff` |

### Components
- Buttons with focus states
- Cards with hover effects
- Rounded corners (18-28px)
- Soft shadows
- Accessible focus indicators

---

## 📦 Environment Variables

### Backend (.env)
```
EARTHLENS_ENV=development
NASA_DATA_MODE=demo
CACHE_DIR=/tmp/earthlens-cache
EARTHDATA_EMAIL=
EARTHDATA_PASSWORD=
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

---

## 🔄 Data Flow

1. **User selects** variable, region, and time period
2. **Frontend sends** POST request to `/api/analyze`
3. **Backend** retrieves or generates time series data
4. **Analysis engine** performs linear regression
5. **Calculation of** confidence intervals, p-values, R²
6. **Results returned** with full metadata
7. **Frontend displays** summary, statistics, and visualization
8. **User can request** AI explanation or compare variables

---

## 🚨 Error Handling

Common error scenarios:
- **Insufficient data**: "Not enough valid observations..."
- **Invalid region**: "Region '...' is not available"
- **Invalid date range**: "End year must be later than start year"
- **API unavailable**: "The analysis service is unavailable"

All errors include:
- Human-readable message
- Technical error details
- Suggested remediation

---

## 📈 NASA Data Sources

EarthLens is designed to work with:
- **MODIS** (land surface temperature, vegetation)
- **GPM IMERG** (precipitation)
- **Earthdata OPeNDAP** endpoints
- **NASA climate models** (where available)

The current implementation uses **demo data** for development. Production deployment requires:
- Earthdata authentication credentials
- API endpoint configuration
- Data caching strategy
- Rate limiting handling

---

## 🔮 Future Improvements

### Spatial Analysis
- Grid-based trend calculation
- Regional variation detection
- Anomaly mapping
- Polygon region selection

### Advanced Statistics
- Seasonal decomposition
- Autocorrelation testing
- Robust regression methods
- Time series forecasting

### Data Integration
- Real NASA API endpoints
- Earthdata login flow
- NetCDF/HDF5 data loading
- Multi-dataset fusion

### UI Enhancements
- Interactive map with layer controls
- Time slider for animations
- Custom region drawing
- Export to GeoJSON/CSV

---

## 🧪 Testing

### Backend
```bash
cd backend
pytest --cov=app
```

### Frontend
```bash
cd frontend
npm run test
npm run test:e2e
```

---

## 📝 Scientific Transparency

Every result includes:
- ✅ Dataset name and source URL
- ✅ Time range and spatial resolution
- ✅ Sample size (N)
- ✅ Statistical method used
- ✅ Significance threshold (α = 0.05)
- ✅ Known limitations
- ✅ Missing data handling
- ✅ Calculation methodology

---

## 🤝 Contributing

Contributions welcome! Areas:
- Real NASA API integration
- Additional datasets
- Advanced statistical methods
- Interactive map features
- UI/UX improvements
- Documentation

---

## 📜 License

MIT License - See LICENSE file

---

## 🙏 Credits

**Built for NASA Space Apps Challenge 2026**

Inspired by:
- Apple's Human Interface Guidelines
- Plotly scientific visualization
- NASA Earthdata documentation
- SciPy and statsmodels communities

---

## 🔗 Resources

- [NASA Earthdata](https://www.earthdata.nasa.gov/)
- [MODIS Data](https://modis.gsfc.nasa.gov/)
- [GPM IMERG](https://gpm.nasa.gov/data/imerg)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Plotly JavaScript](https://plotly.com/javascript/)

---

## 📧 Support

Questions or issues? Open a GitHub issue or check the API documentation at `/docs`.

---

**EarthLens: Understand Earth's changing systems with science and precision.**
