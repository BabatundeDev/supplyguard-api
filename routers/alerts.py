from fastapi import APIRouter
from datetime import datetime, timedelta
import random, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.risk_model import bulk_predict
from data.suppliers import get_dataframe

router = APIRouter(prefix="/alerts", tags=["Disruption Alerts"])

GEOPOLITICAL_EVENTS = [
    {"region": "Asia Pacific", "msg": "Taiwan Strait shipping lane restrictions detected",      "sev": "critical"},
    {"region": "China",        "msg": "Export controls tightened on rare earth materials",      "sev": "critical"},
    {"region": "Russia",       "msg": "Additional sanctions impact metal supply routes",         "sev": "critical"},
    {"region": "Congo DRC",    "msg": "Cobalt mining output reduced due to unrest",             "sev": "high"},
    {"region": "Taiwan",       "msg": "Semiconductor fab capacity cut by 12% this quarter",     "sev": "high"},
    {"region": "Ukraine",      "msg": "Steel production corridor disrupted",                     "sev": "high"},
    {"region": "Global",       "msg": "US tariff update on East Asian semiconductor imports",   "sev": "medium"},
    {"region": "Chile",        "msg": "Lithium export quota revision under review",              "sev": "medium"},
    {"region": "India",        "msg": "VoltPath India new facility online — capacity +20%",     "sev": "low"},
    {"region": "Germany",      "msg": "EuroSemi GmbH signs 3-year supply agreement",            "sev": "low"},
]

SUPPLIER_ALERTS_TEMPLATES = [
    "Lead time extended by {n} days",
    "Q{q} capacity reduced by {p}%",
    "Price increase of {p}% flagged for next quarter",
    "New certification obtained — quality grade upgraded",
    "On-time delivery rate improved to {p}%",
]


def _generate_supplier_alerts(n: int = 4) -> list:
    df = get_dataframe()
    predicted = bulk_predict(df)
    high_risk = predicted[predicted["predicted_risk"] >= 60].to_dict("records")

    alerts = []
    now = datetime.now()
    for i, sup in enumerate(high_risk[:n]):
        score = float(sup["predicted_risk"])
        sev = "critical" if score >= 80 else "high"
        delta = timedelta(minutes=random.randint(5, 180))
        alerts.append({
            "id": f"sup_{i+1}",
            "type": "supplier",
            "severity": sev,
            "supplier": sup["name"],
            "region": sup["country"],
            "message": f"{sup['name']} risk score elevated to {round(score)} — alternate sourcing recommended",
            "risk_score": round(score, 1),
            "timestamp": (now - delta).isoformat(),
            "time_ago": f"{int(delta.total_seconds() // 60)} min ago",
        })
    return alerts


@router.get("/")
def get_alerts(include_supplier_alerts: bool = True):
    """Return current disruption alerts — geopolitical and supplier-level."""
    now = datetime.now()
    geo_alerts = []
    for i, ev in enumerate(GEOPOLITICAL_EVENTS):
        delta = timedelta(minutes=random.randint(2, 1440))
        mins = int(delta.total_seconds() // 60)
        time_ago = f"{mins} min ago" if mins < 60 else f"{mins // 60} hr ago" if mins < 1440 else "1 day ago"
        geo_alerts.append({
            "id": f"geo_{i+1}",
            "type": "geopolitical",
            "severity": ev["sev"],
            "region": ev["region"],
            "message": ev["msg"],
            "timestamp": (now - delta).isoformat(),
            "time_ago": time_ago,
        })

    supplier_alerts = _generate_supplier_alerts() if include_supplier_alerts else []
    all_alerts = geo_alerts + supplier_alerts

    # Sort: critical first, then high, then by time
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    all_alerts.sort(key=lambda x: (sev_order.get(x["severity"], 4), x["timestamp"]))

    return {
        "total": len(all_alerts),
        "critical": sum(1 for a in all_alerts if a["severity"] == "critical"),
        "high": sum(1 for a in all_alerts if a["severity"] == "high"),
        "medium": sum(1 for a in all_alerts if a["severity"] == "medium"),
        "low": sum(1 for a in all_alerts if a["severity"] == "low"),
        "alerts": all_alerts,
    }
