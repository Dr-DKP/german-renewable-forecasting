"""
Evaluation metrics for energy generation forecasting.

Point forecast metrics: RMSE, MAE, MAPE
Uncertainty metrics: Coverage, Sharpness (interval width)
"""

import numpy as np


def rmse(y_true, y_pred) -> float:
    """Root Mean Squared Error."""
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true, y_pred) -> float:
    """Mean Absolute Error."""
    return float(np.mean(np.abs(y_true - y_pred)))


def mape(y_true, y_pred) -> float:
    """Mean Absolute Percentage Error (excludes zero actuals)."""
    mask = y_true != 0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def coverage(y_true, lower, upper) -> float:
    """Empirical coverage: fraction of actuals within prediction interval."""
    return float(np.mean((y_true >= lower) & (y_true <= upper)))


def sharpness(lower, upper) -> float:
    """Average width of prediction intervals (narrower = better, given good coverage)."""
    return float(np.mean(upper - lower))
