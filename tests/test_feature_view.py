import numpy as np
import pandas as pd
from src.features.feature_view import build_features
# create test data
def create_fake_solar_data(rows=24):
    """ Creates a mock DataFrame mimicking merged solar/weather data"""
    # create continuous hourly index
    times = pd.date_range(start="2023-01-01", periods=rows, freq="h")
    # build DataFrame with core raw columns
    df = pd.DataFrame({
        "time": times,
        "solar_mw": np.random.uniform(0,5000,size=rows),
        "cloud_cover": np.random.uniform(0, 100, size=rows),
        "shortwave_radiation": np.random.uniform(0, 800, size=rows),
        "temperature_2m": np.random.uniform(10, 25, size=rows)
    })
    df = df.set_index("time")
    return df

# create test function
def test_time_columns_exist():
    df = create_fake_solar_data(rows=24)
    result = build_features(df)
    assert "hour" in result.columns
    assert "month" in result.columns
    assert "cloud_cover_lag_1h" in result.columns
    assert "radiation_lag_1h" in result.columns
    assert result.isna().sum().sum() == 0 # result.isna() → DataFrame of True/False. .sum() → count of True per column. .sum() again → total across all columns