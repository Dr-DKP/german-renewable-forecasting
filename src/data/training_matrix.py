"""
Assembling full DataFrame with merged sola and weather data in perquet. 
Then add physics_pred, residual, and features to this DataFrame.
"""

# import libraries and modules
import pandas as pd
from pathlib import Path
from src.physics.clear_sky import compute_physics_pred
from src.features.feature_view import build_features

_RAW = Path(__file__).resolve().parents[2] / "data" / "raw"

def build_training_matrix() -> tuple[pd.DataFrame, pd.Series]:
    df_solar = pd.read_parquet(_RAW / "solar_2022_2024.parquet")
    df_weather = pd.read_parquet(_RAW / "weather_2022_2024.parquet")
    # Merge solar + weather on time (timestamps as index)
    df = pd.merge(df_solar, df_weather, on="time").set_index("time")
    # Add physics prediction
    df["physics_pred"] = compute_physics_pred(df.index)
    # compute residual
    df["residual"] = df["solar_mw"] - df["physics_pred"]
    # Build Features
    df_features = build_features(df)
    # Split into X and y
    feature_cols = ["hour", "month", "cloud_cover_lag_1h",
                   "radiation_lag_1h", "cloud_cover_rolling_3h", "physics_pred"]
    X = df_features[feature_cols]
    y = df_features["residual"]
    
    return X, y