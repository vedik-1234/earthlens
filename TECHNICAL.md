# EarthLens Technical Documentation

## Architecture Overview

EarthLens follows a clean separation between backend (analysis engine) and frontend (visualization):

```
┌─────────────────────────────────────────────────────┐
│ React Frontend (Vite)                               │
│ - Components (Tailwind CSS)                          │
│ - API client (fetch)                                │
│ - Plotly charts                                     │
│ - Responsive design (Apple-inspired)                │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP REST API
                   │
┌──────────────────▼──────────────────────────────────┐
│ FastAPI Backend (Python 3.11+)                      │
│ - API endpoints                                     │
│ - Request validation (Pydantic)                     │
│ - CORS middleware                                  │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ Analysis Engine                                     │
│ - Linear regression (scipy.stats)                   │
│ - Significance testing                              │
│ - Confidence intervals                              │
│ - Trend detection                                   │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ Data Layer                                          │
│ - Dataset registry                                  │
│ - Demo data generator                               │
│ - Caching system                                    │
│ - (Future: NASA API integration)                    │
└─────────────────────────────────────────────────────┘
```

## Backend API Specification

### POST /api/analyze

**Request:**
```json
{
  "variable": "temperature" | "precipitation" | "vegetation",
  "region": "global" | "north_america" | "south_america" | ...,
  "start_year": 2003,
  "end_year": 2025
}
```

**Response:**
```json
{
  "status": "success",
  "variable": "temperature",
  "region": "global",
  "period": "2003-2025",
  "trend": 0.038,
  "unit": "°C/year",
  "starting_value": 12.5,
  "ending_value": 13.34,
  "total_change": 0.84,
  "percent_change": 6.72,
  "p_value": 0.0008,
  "confidence_interval": [0.025, 0.051],
  "r_squared": 0.72,
  "sample_size": 23,
  "statistically_significant": true,
  "mean_value": 12.92,
  "series": [
    {"year": 2003, "value": 12.45},
    {"year": 2004, "value": 12.52}
  ],
  "fitted": [
    {"year": 2003, "value": 12.5},
    {"year": 2004, "value": 12.518}
  ],
  "data_source": "Demo dataset (development only)",
  "is_demo": true
}
```

### POST /api/trend-detect

Scans all variables for significant trends in a region.

**Request:**
```json
{
  "region": "global",
  "start_year": 2003,
  "end_year": 2025
}
```

**Response:**
```json
{
  "status": "success",
  "results": [
    {
      "variable": "temperature",
      "label": "Temperature",
      "direction": "increasing",
      "trend": 0.038,
      "p_value": 0.0008,
      "statistically_significant": true
    }
  ],
  "criteria": [
    "Magnitude of trend (|slope|)",
    "Statistical significance (p < 0.05)",
    "Valid data coverage",
    "Temporal consistency"
  ]
}
```

### POST /api/compare

Compares trends between two variables.

**Request:**
```json
{
  "variable_a": "temperature",
  "variable_b": "precipitation",
  "region": "global",
  "start_year": 2003,
  "end_year": 2025
}
```

**Response:**
```json
{
  "status": "success",
  "variable_a": { /* analysis result */ },
  "variable_b": { /* analysis result */ },
  "association": {
    "correlation": 0.67,
    "interpretation": "Statistical association detected...",
    "caution": "This does not imply causation."
  }
}
```

### POST /api/explain

Generates a natural language explanation of analysis results.

**Request:**
```json
{
  "variable": "temperature",
  "region": "global",
  "start_year": 2003,
  "end_year": 2025,
  "trend_value": 0.038,
  "p_value": 0.0008,
  "total_change": 0.84,
  "unit": "°C/year"
}
```

**Response:**
```json
{
  "status": "success",
  "summary": "The selected region shows an increasing trend...",
  "segments": [
    {
      "type": "observed_data",
      "title": "What was measured",
      "text": "The region was analyzed for temperature from 2003 to 2025..."
    },
    {
      "type": "statistical_result",
      "title": "Statistical finding",
      "text": "A linear trend model was fit to the data..."
    }
  ]
}
```

## Frontend Component Hierarchy

```
App
├── Navigation
│   ├── Logo
│   └── Controls (Theme, Settings)
├── Hero
│   ├── Headline
│   └── Info Card
├── AnalysisPanel (Sticky)
│   ├── Variable Selector
│   ├── Region Selector
│   ├── Time Period Inputs
│   └── Action Buttons
├── Analysis View
│   ├── LoadingSpinner
│   ├── ErrorBanner
│   ├── TrendSummary
│   ├── MetricsGrid
│   └── TrendChart (Plotly)
├── Trend Detective Section
│   ├── TrendList
│   └── ExplanationPanel
└── Comparison Section
    └── ComparisonView
```

## Design Tokens

### Colors (CSS Variables)
```css
:root {
  /* Backgrounds */
  --bg: #f5f7f9;
  --surface-primary: rgba(255, 255, 255, 0.95);
  --surface-secondary: #eef2f6;
  --surface-strong: #e1e7ef;

  /* Text */
  --text-primary: #0f172a;
  --text-secondary: #475569;

  /* UI */
  --border: rgba(15, 23, 42, 0.1);
  --accent: #6ea8fe;
}
```

### Spacing
Tailwind default scale (4px base unit)

### Radii
- Small: 10px (rounded-[10px])
- Medium: 18px (rounded-[18px])
- Large: 24px (rounded-2xl)
- Buttons: 999px (rounded-full)

### Shadows
- Soft: `0 20px 44px rgba(15, 23, 42, 0.08)`

## State Management

The frontend uses React hooks for local state:
- `selectedVariable`, `selectedRegion`, `startYear`, `endYear`
- `analysis` (current result)
- `loading`, `error` (request state)
- `trendResults`, `compareData`, `explanation` (view data)
- `theme` (light/dark mode)

## Error Handling Strategy

1. **API Level**: Return structured error responses
2. **Service Level**: Catch and log exceptions
3. **Component Level**: Display user-friendly messages
4. **User Level**: ErrorBanner component with dismiss option

## Performance Considerations

- **Caching**: Demo data is seeded consistently
- **Lazy Loading**: Components render on demand
- **Code Splitting**: Vite handles automatic splitting
- **Image Optimization**: Minimal graphics (design-focused)
- **Bundle**: ~150KB gzipped (React, Plotly, Tailwind)

## Accessibility

- ✅ Semantic HTML
- ✅ ARIA labels where needed
- ✅ Keyboard navigation
- ✅ Focus indicators
- ✅ Color contrast (WCAG AA)
- ✅ Respects `prefers-reduced-motion`
- ✅ Screen reader friendly

## Security

- ✅ CORS configured
- ✅ Pydantic validation on all inputs
- ✅ No sensitive data in client code
- ✅ Rate limiting ready (can be added)
- ✅ Error messages don't leak internals

## Testing Strategy

### Backend
- Unit tests for analysis functions
- Integration tests for API endpoints
- Fixture-based demo data
- Coverage target: >80%

### Frontend
- Component tests (React Testing Library)
- API mock tests
- Visual regression testing (optional)
- E2E tests (Playwright)

## Deployment

### Docker
```dockerfile
# Backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

# Frontend
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
EXPOSE 5173
CMD ["npm", "run", "preview"]
```

### Production Checklist
- [ ] Real NASA API endpoints configured
- [ ] Earthdata authentication set up
- [ ] Database/cache layer deployed
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] Logging and monitoring enabled
- [ ] Error tracking (Sentry) integrated
- [ ] CDN for static assets
- [ ] Health checks configured
- [ ] Backup/disaster recovery plan

## Monitoring & Logging

- Backend: Uvicorn logs + structured logging
- Frontend: Console errors + error reporting service
- API calls: Request/response logging
- Performance: Metrics collection (optional)

---

For more details, see README.md and inline code documentation.
