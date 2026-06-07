from fastapi import APIRouter, Query
from typing import Literal
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.forecast_model import forecast_demand

router = APIRouter(prefix="/forecast", tags=["Demand Forecasting"])

MaterialType = Literal["Semiconductors", "Battery Metals", "Steel"]


@router.get("/demand")
def get_demand_forecast(
    material: MaterialType = Query(default="Semiconductors"),
    weeks: int = Query(default=12, ge=4, le=26),
):
    """Prophet-based demand forecast for a given material category."""
    return forecast_demand(material=material, weeks=weeks)


@router.get("/all-materials")
def forecast_all_materials(weeks: int = Query(default=12, ge=4, le=26)):
    """Forecast demand across all material categories."""
    results = {}
    for mat in ["Semiconductors", "Battery Metals", "Steel"]:
        results[mat] = forecast_demand(material=mat, weeks=weeks)
    return {"weeks": weeks, "forecasts": results}
