from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.risk_model import predict_risk, get_feature_importance, bulk_predict, get_dataframe, FEATURE_COLS
from data.suppliers import get_dataframe as get_df

router = APIRouter(prefix="/risk", tags=["Risk Scoring"])


class RiskRequest(BaseModel):
    name: Optional[str] = "Unknown Supplier"
    country_risk: float = Field(..., ge=0, le=100, description="Country risk index 0-100")
    lead_time: float = Field(..., ge=1, le=90,  description="Lead time in days")
    rating: float = Field(..., ge=1, le=5,      description="Supplier rating 1-5")
    price_volatility: float = Field(..., ge=0, le=1, description="Price volatility 0-1")
    capacity_util: float = Field(..., ge=0, le=1,    description="Capacity utilisation 0-1")
    geo_score: float = Field(..., ge=0, le=100,      description="Geopolitical risk score 0-100")


class AlternateRequest(BaseModel):
    supplier_name: str
    material: str
    current_risk: float
    top_n: int = Field(default=3, ge=1, le=5)


@router.post("/score")
def score_supplier(req: RiskRequest):
    """Predict risk score for a single supplier."""
    result = predict_risk(req.model_dump())
    return {
        "supplier": req.name,
        "input_features": req.model_dump(exclude={"name"}),
        **result,
    }


@router.get("/all-suppliers")
def get_all_suppliers():
    """Return all suppliers with AI-predicted risk scores."""
    df = get_df()
    predicted = bulk_predict(df)

    suppliers = []
    for _, row in predicted.iterrows():
        score = float(row["predicted_risk"])
        label = "Critical" if score >= 70 else ("Medium" if score >= 40 else "Low")
        color = "#FF4D4D" if score >= 70 else ("#F5A623" if score >= 40 else "#2ECC9A")
        suppliers.append({
            "name": row["name"],
            "country": row["country"],
            "material": row["material"],
            "risk_score": score,
            "risk_label": label,
            "risk_color": color,
            "lead_time": int(row["lead_time"]),
            "rating": float(row["rating"]),
            "price_volatility": float(row["price_volatility"]),
            "geo_score": float(row["geo_score"]),
            "country_risk": float(row["country_risk"]),
        })

    avg_risk = round(sum(s["risk_score"] for s in suppliers) / len(suppliers), 1)
    critical = [s for s in suppliers if s["risk_label"] == "Critical"]

    return {
        "total_suppliers": len(suppliers),
        "avg_portfolio_risk": avg_risk,
        "critical_count": len(critical),
        "suppliers": sorted(suppliers, key=lambda x: -x["risk_score"]),
    }


@router.post("/alternate-suppliers")
def find_alternates(req: AlternateRequest):
    """Recommend alternate low-risk suppliers for the same material."""
    df = get_df()
    predicted = bulk_predict(df)

    same_material = predicted[
        (predicted["material"] == req.material) &
        (predicted["name"] != req.supplier_name)
    ].sort_values("predicted_risk")

    alternates = []
    for _, row in same_material.head(req.top_n).iterrows():
        score = float(row["predicted_risk"])
        risk_reduction = round(req.current_risk - score, 1)
        alternates.append({
            "name": row["name"],
            "country": row["country"],
            "material": row["material"],
            "risk_score": score,
            "risk_label": "Critical" if score >= 70 else ("Medium" if score >= 40 else "Low"),
            "lead_time": int(row["lead_time"]),
            "rating": float(row["rating"]),
            "risk_reduction": risk_reduction,
            "recommendation": (
                "Strongly recommended" if risk_reduction > 40
                else "Recommended" if risk_reduction > 20
                else "Consider"
            ),
        })

    return {
        "original_supplier": req.supplier_name,
        "material": req.material,
        "current_risk": req.current_risk,
        "alternates": alternates,
        "best_alternate": alternates[0] if alternates else None,
    }


@router.get("/feature-importance")
def feature_importance():
    """Return model feature importance for explainability."""
    imp = get_feature_importance()
    ranked = sorted(imp.items(), key=lambda x: -x[1])
    return {
        "feature_importance": imp,
        "ranked": [{"feature": k, "importance": v, "percentage": round(v * 100, 1)}
                   for k, v in ranked],
        "top_driver": ranked[0][0] if ranked else None,
    }


@router.get("/portfolio-summary")
def portfolio_summary():
    """High level risk summary across all materials."""
    df = get_df()
    predicted = bulk_predict(df)

    summary = []
    for material, group in predicted.groupby("material"):
        avg = round(float(group["predicted_risk"].mean()), 1)
        summary.append({
            "material": material,
            "avg_risk": avg,
            "risk_label": "Critical" if avg >= 70 else ("Medium" if avg >= 40 else "Low"),
            "supplier_count": len(group),
            "high_risk_count": int((group["predicted_risk"] >= 70).sum()),
        })

    return {"materials": sorted(summary, key=lambda x: -x["avg_risk"])}
