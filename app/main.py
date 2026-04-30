
# Import Libraries and Modules
import mlflow.xgboost
import numpy as np
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from src.physics.clear_sky import compute_physics_pred

# Constants
RUN_ID = "7010b71b911640e09a5a0f5d42b78338"
Q_HAT_P50 = 2.1
Q_HAT_P90 = 770.1
# models dict
models = {}

# lifespan function loads all three quantile models
@asynccontextmanager
async def lifespan(app):
    models["q10"] = mlflow.xgboost.load_model(f"runs:/{RUN_ID}/q10")
    models["q50"] = mlflow.xgboost.load_model(f"runs:/{RUN_ID}/q50")
    models["q90"] = mlflow.xgboost.load_model(f"runs:/{RUN_ID}/q90")
    print("Models loaded.")
    yield
app = FastAPI(lifespan=lifespan)

# /health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy" if models else "degraded",
        "models_loaded": list(models.keys()),
        "timestamps": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "endpoints": ["/health", "/forecast"]
    }

# /forecast endpoint
@app.get("/forecast")
def forecast(date: str):
    # define time format
    try:
        times = pd.date_range(date, periods=24, freq="h", tz="UTC")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    # compute physics prediction
    physics = compute_physics_pred(times)
    # build feature matrix X as DataFrame matching FEATURE_COLS exactly
    X = pd.DataFrame({
        "hour": times.hour,
        "month": times.month,
        "cloud_cover_lag_1h": 0.0,
        "radiation_lag_1h": 0.0,
    "cloud_cover_rolling_3h": 0.0,
    "physics_pred": physics.values
    }, index=times)
    # predict
    p10 = physics.values + models["q10"].predict(X)
    p50 = physics.values + models["q50"].predict(X) + Q_HAT_P50
    p90 = physics.values + models["q90"].predict(X) + Q_HAT_P90
    # enforce p10 <= p50 <= p90 (independent quantile models can cross)
    stacked = np.sort(np.stack([p10, p50, p90], axis=1), axis=1)
    p10, p50, p90 = stacked[:, 0], stacked[:, 1], stacked[:, 2]
    # return a list of dicts one per hour
    return {"date": date, "forecast": [
    {"time": str(t), "physics_mw": round(float(physics.values[i]), 1), "p10_mw": round(float(p10[i]), 1),
     "p50_mw": round(float(p50[i]), 1), "p90_mw": round(float(p90[i]), 1)}
    for i, t in enumerate(times)
    ]}
