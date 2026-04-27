"""
creating the inputs XGBoost will learn from.
why it matters?: XGBoost cannot learn from raw timestamps. It needs number
that encode what time means physically. Is it morning? Is it Summer?
Is it cloudy? these `encoding` will be features for ML model.
"""


import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    df comes in already merged (solar + weather + physics_pred), 
    with `time` as the index.
    """
    result = df.copy()
    # time encoding; extract from index
    result["hour"] = result.index.hour
    result["month"] = result.index.month
    # define lag features
    # lag features (.shift(1) moves every value down one row 
    # so row N gets the value that was at row N-1 (one h ago)
    result["cloud_cover_lag_1h"] = result["cloud_cover"].shift(1)
    result["radiation_lag_1h"] = result["shortwave_radiation"].shift(1)
    # rolling feature on cloud_cover
    result["cloud_cover_rolling_3h"] = result["cloud_cover"].rolling(3).mean()
    # drop NaN values
    result = result.dropna()

    return result

