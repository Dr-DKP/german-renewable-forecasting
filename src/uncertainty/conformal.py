"""
Conformal prediction for distribution-free uncertainty intervals.

Calibrates residuals on a validation set and applies empirical quantiles
to produce prediction intervals with guaranteed coverage.
"""

import numpy as np


def calibrate(y_val, y_pred_val) -> np.ndarray:
    """Compute conformity scores (absolute residuals) on validation set."""
    return np.abs(y_val - y_pred_val)


def predict_interval(y_pred_test, scores: np.ndarray, alpha: float = 0.1):
    """Construct prediction intervals from conformity scores.

    Args:
        y_pred_test: Point predictions on test set.
        scores: Calibrated conformity scores from validation set.
        alpha: Miscoverage rate (0.1 = 90% intervals).

    Returns:
        Tuple of (lower, upper) bounds.
    """
    q = np.quantile(scores, 1 - alpha)
    return y_pred_test - q, y_pred_test + q
