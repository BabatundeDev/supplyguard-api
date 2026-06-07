# SupplyGuard AI — Backend API

> AI-powered automotive supply chain risk intelligence engine built for the **ET AutoTech Hackathon 2026**.

![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-F7931E?style=for-the-badge&logo=scikit-learn)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=for-the-badge)

---

## 🚀 Live Endpoints

| Service | URL |
|---|---|
| Base API | [supplyguard-api-dp47.onrender.com](https://supplyguard-api-dp47.onrender.com) |
| Interactive Docs | [supplyguard-api-dp47.onrender.com/docs](https://supplyguard-api-dp47.onrender.com/docs) |
| Frontend App | [supplyguard-dashboard.vercel.app](https://supplyguard-dashboard.vercel.app) |
| Frontend Repo | [BabatundeDev/SupplyGuard](https://github.com/BabatundeDev/SupplyGuard) |

---

## 🧠 What is SupplyGuard AI?

A production-grade FastAPI backend that powers real-time supply chain risk intelligence for the automotive industry. The AI engine uses a GradientBoosting model trained on 50 suppliers across 8 countries to predict risk scores, recommend alternate suppliers, and forecast demand — all served via REST API.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service info and endpoint map |
| GET | `/health` | Health check |
| POST | `/risk/score` | Score a single supplier with AI |
| GET | `/risk/all-suppliers` | All 50 suppliers with predicted risk scores |
| POST | `/risk/alternate-suppliers` | Recommend low-risk alternate suppliers |
| GET | `/risk/feature-importance` | Model explainability — top risk drivers |
| GET | `/risk/portfolio-summary` | Portfolio risk breakdown by material |
| GET | `/forecast/demand` | 12-week demand forecast (Holt-Winters) |
| GET | `/forecast/all-materials` | Forecast all material categories |
| GET | `/alerts/` | Live geopolitical and supplier disruption alerts |

---

## 🤖 AI Models

### Risk Scoring Model
- **Algorithm:** GradientBoostingRegressor (scikit-learn)
- **Training data:** 50 suppliers across 8 countries and 5 material categories
- **Features:** country_risk, lead_time, rating, price_volatility, capacity_util, geo_score
- **Performance:** R² = 0.982 across 5-fold cross-validation
- **Top risk driver:** country_risk followed by geo_score

### Demand Forecasting Model
- **Algorithm:** Holt-Winters Exponential Smoothing (statsmodels)
- **Seasonal periods:** 52 weeks
- **Confidence interval:** 80%
- **Materials:** Semiconductors, Battery Metals, Steel
- **Horizon:** 4 to 26 weeks configurable

---

## 🏗 Project Structure

```
supplyguard-api/
├── main.py                     # FastAPI app + CORS + lifespan
├── requirements.txt
├── .python-version             # Python 3.11 pin
├── data/
│   └── suppliers.py            # 50-supplier training dataset
├── models/
│   ├── risk_model.py           # GradientBoosting risk scorer
│   └── forecast_model.py       # Holt-Winters demand forecaster
└── routers/
    ├── risk.py                 # /risk/* endpoints
    ├── forecast.py             # /forecast/* endpoints
    └── alerts.py               # /alerts/* endpoints
```

---

## ⚡ Getting Started

### Prerequisites
- Python 3.11+

### Install and run

```bash
git clone https://github.com/BabatundeDev/supplyguard-api.git
cd supplyguard-api
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

The risk model trains automatically on startup in about 2 seconds.

Open `http://localhost:8000/docs` for the interactive Swagger UI.

---

## 🔍 Example API Calls

### Score a supplier
```bash
curl -X POST https://supplyguard-api-dp47.onrender.com/risk/score \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TestSupplier",
    "country_risk": 75,
    "lead_time": 18,
    "rating": 4.2,
    "price_volatility": 0.72,
    "capacity_util": 0.88,
    "geo_score": 78
  }'
```

### Get demand forecast
```bash
curl "https://supplyguard-api-dp47.onrender.com/forecast/demand?material=Semiconductors&weeks=12"
```

### Get all alerts
```bash
curl "https://supplyguard-api-dp47.onrender.com/alerts/"
```

---

## 🚀 Deployment

Deployed on **Render** free tier.

| Field | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python -m uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Python Version | 3.14 (auto-detected) |

> Note: Free tier instances spin down after inactivity. First request after sleep may take 50 seconds to wake up. Subsequent requests are instant.

---

## 🏆 Judging Criteria Alignment

| Criteria | Weight | How we address it |
|---|---|---|
| Correctness & Performance | 30% | R² = 0.982 risk model + live working endpoints |
| Technical Depth | 20% | ML pipeline + REST API + modular architecture |
| Innovation & Creativity | 10% | Geopolitical risk scoring + AI alternate sourcing |
| Automotive Ecosystem Impact | 10% | Addresses real supply chain disruption problem |

---

## 👨‍💻 Built By

**Babatunde** — ET AutoTech Hackathon 2026 | Theme 1: AI for Resilient Automotive Supply Chains

---

## 📄 License

MIT
