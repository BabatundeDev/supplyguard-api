# SupplyGuard AI — Backend API

AI-powered automotive supply chain risk intelligence engine built with FastAPI, scikit-learn, and Prophet.

## Architecture

```
supplyguard-api/
├── main.py                  # FastAPI app entry point
├── requirements.txt
├── data/
│   └── suppliers.py         # 50-supplier training dataset
├── models/
│   ├── risk_model.py        # GradientBoosting risk scorer (R² = 0.98)
│   └── forecast_model.py    # Prophet demand forecaster
└── routers/
    ├── risk.py              # /risk/* endpoints
    ├── forecast.py          # /forecast/* endpoints
    └── alerts.py            # /alerts/* endpoints
```

## Setup

```bash
cd supplyguard-api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The model trains automatically on first startup (~2 seconds).

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info and endpoint map |
| GET | `/health` | Health check |
| POST | `/risk/score` | Score a single supplier |
| GET | `/risk/all-suppliers` | All suppliers with predicted risk |
| POST | `/risk/alternate-suppliers` | Recommend low-risk alternates |
| GET | `/risk/feature-importance` | Model explainability |
| GET | `/risk/portfolio-summary` | Risk by material category |
| GET | `/forecast/demand` | 12-week demand forecast (Prophet) |
| GET | `/forecast/all-materials` | Forecast all materials |
| GET | `/alerts/` | Live disruption alerts |

Interactive docs at: **[http://localhost:8000/docs](https://supplyguard-api-dp47.onrender.com/docs)**
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Set env var `REACT_APP_API_URL` in your React app to the Render URL
