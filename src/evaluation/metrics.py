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

def crps(y_true, quantile_preds: dict) -> float:
    """
    Computes the Mean Pinball Loss across multiple quantiles as a 
    proxy for Continuous Ranked Probability Score (CRPS).
    """
    # Define the target quantiles (alphas)
    alphas = {"q10": 0.1, "q50": 0.5, "q90": 0.9}
    
    losses = []
    
    # Loop over each quantile to calculate its specific pinball loss
    for name, alpha in alphas.items():
        # Get the array of predictions for this specific quantile
        preds = quantile_preds[name]
        
        # Calculate the raw error (residuals)
        error = y_true - preds
        
        # Apply the Pinball Loss formula using np.where
        # If error >= 0: the prediction was too low (underestimated)
        # If error < 0: the prediction was too high (overestimated)
        loss = np.where(error >= 0, 
                        alpha * error, 
                        (alpha - 1) * error)
        
        # Store the mean loss for this specific quantile
        losses.append(loss.mean())
    
    # Return the average loss across all quantiles
    return float(np.mean(losses))