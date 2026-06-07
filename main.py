from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys, os
sys.path.append(os.path.dirname(__file__))

from routers import risk, forecast, alerts
from models.risk_model import get_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-train the model on startup so first request is instant
    print("[SupplyGuard AI] Training risk model on startup...")
    get_model()
    print("[SupplyGuard AI] Risk model ready.")
    yield
    print("[SupplyGuard AI] Shutting down.")


app = FastAPI(
    title="SupplyGuard AI",
    description="AI-powered automotive supply chain risk intelligence API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(risk.router)
app.include_router(forecast.router)
app.include_router(alerts.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "SupplyGuard AI",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "risk_score":        "POST /risk/score",
            "all_suppliers":     "GET  /risk/all-suppliers",
            "alternate_sources": "POST /risk/alternate-suppliers",
            "feature_importance":"GET  /risk/feature-importance",
            "portfolio_summary": "GET  /risk/portfolio-summary",
            "demand_forecast":   "GET  /forecast/demand?material=Semiconductors&weeks=12",
            "all_forecasts":     "GET  /forecast/all-materials",
            "alerts":            "GET  /alerts/",
            "docs":              "GET  /docs",
        },
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
