import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import joblib, os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data.suppliers import get_dataframe, FEATURE_COLS

_pipeline: Pipeline | None = None

def _build_pipeline() -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.08,
            max_depth=4,
            min_samples_split=3,
            subsample=0.85,
            random_state=42,
        )),
    ])

def get_model() -> Pipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = _train()
    return _pipeline

def _train() -> Pipeline:
    df = get_dataframe()
    X = df[FEATURE_COLS].values
    y = df["risk_score"].values

    pipe = _build_pipeline()
    pipe.fit(X, y)

    scores = cross_val_score(pipe, X, y, cv=5, scoring="r2")
    print(f"[RiskModel] R² CV scores: {scores.round(3)} | Mean: {scores.mean():.3f}")
    return pipe

def predict_risk(features: dict) -> dict:
    model = get_model()
    row = np.array([[
        features["country_risk"],
        features["lead_time"],
        features["rating"],
        features["price_volatility"],
        features["capacity_util"],
        features["geo_score"],
    ]])
    score = float(np.clip(model.predict(row)[0], 0, 100))
    score = round(score, 1)

    if score >= 70:
        label, color = "Critical", "#FF4D4D"
    elif score >= 40:
        label, color = "Medium", "#F5A623"
    else:
        label, color = "Low", "#2ECC9A"

    # Feature importance
    imp = model.named_steps["model"].feature_importances_
    importance = {f: round(float(v), 4) for f, v in zip(FEATURE_COLS, imp)}

    return {
        "risk_score": score,
        "risk_label": label,
        "risk_color": color,
        "feature_importance": importance,
        "confidence": round(min(0.95, 0.70 + (score / 100) * 0.25), 2),
    }

def bulk_predict(df_input: pd.DataFrame) -> pd.DataFrame:
    model = get_model()
    X = df_input[FEATURE_COLS].values
    scores = np.clip(model.predict(X), 0, 100).round(1)
    df_input = df_input.copy()
    df_input["predicted_risk"] = scores
    return df_input

def get_feature_importance() -> dict:
    model = get_model()
    imp = model.named_steps["model"].feature_importances_
    return {f: round(float(v), 4) for f, v in zip(FEATURE_COLS, imp)}
