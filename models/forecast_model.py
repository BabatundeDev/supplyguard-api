import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")


def _generate_historical_data(material: str = "Semiconductors") -> pd.DataFrame:
    np.random.seed(42)
    base_demand = {"Semiconductors": 420, "Battery Metals": 310, "Steel": 550}
    base = base_demand.get(material, 420)

    dates = pd.date_range(end=datetime.today(), periods=104, freq="W")
    trend = np.linspace(0, base * 0.3, len(dates))
    seasonality = base * 0.12 * np.sin(2 * np.pi * np.arange(len(dates)) / 52)
    noise = np.random.normal(0, base * 0.05, len(dates))
    spike = np.zeros(len(dates))
    spike[80:85] = base * 0.20

    demand = np.clip(base + trend + seasonality + noise + spike,
                     base * 0.6, base * 2.0).round(0)
    return pd.DataFrame({"ds": dates, "y": demand})


def forecast_demand(material: str = "Semiconductors", weeks: int = 12) -> dict:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    df = _generate_historical_data(material)
    series = df["y"].values

    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal="add",
        seasonal_periods=52,
        initialization_method="estimated",
    ).fit(optimized=True)

    forecast_vals = model.forecast(weeks)
    std_err = np.std(model.resid) * 1.28  # 80% confidence interval

    result_rows = []
    for i, val in enumerate(forecast_vals):
        demand = max(0, round(float(val), 0))
        result_rows.append({
            "week":   f"W{i + 1}",
            "date":   (datetime.today() + timedelta(weeks=i + 1)).strftime("%Y-%m-%d"),
            "demand": demand,
            "upper":  max(0, round(float(val + std_err), 0)),
            "lower":  max(0, round(float(val - std_err), 0)),
        })

    demands = [r["demand"] for r in result_rows]
    peak_week = result_rows[int(np.argmax(demands))]
    avg_demand = round(float(np.mean(demands)), 0)
    current_avg = float(df["y"].tail(4).mean())
    reorder_week = next(
        (r["week"] for r in result_rows if r["demand"] > current_avg * 1.10),
        result_rows[-1]["week"],
    )

    return {
        "material": material,
        "weeks":    weeks,
        "forecast": result_rows,
        "insights": {
            "peak_week":                peak_week["week"],
            "peak_demand":              peak_week["demand"],
            "avg_weekly_demand":        avg_demand,
            "reorder_recommended_week": reorder_week,
            "trend": "increasing" if demands[-1] > demands[0] else "decreasing",
        },
    }