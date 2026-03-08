"""
Prophet baseline model for solar and wind generation forecasting.

Phase 1: Establish baseline performance with minimal tuning.
Prophet handles seasonality, holidays, and trend changes automatically.
"""


def train_prophet(df, target_col: str, forecast_horizon: int = 24):
    """Train Prophet model on generation time-series."""
    raise NotImplementedError("Phase 1 — Prophet baseline in progress")


def predict_with_uncertainty(model, periods: int, interval_width: float = 0.80):
    """Generate forecast with prediction intervals."""
    raise NotImplementedError("Phase 1 — Prophet baseline in progress")
