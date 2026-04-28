"""
Conformal prediction takes the raw P90 interval and 
adjusts it so it mathematically guarantees 90% coverage on future data
"""

import numpy as np
import pandas as pd
def fit_conformal(q_model, X_cal, y_cal, alpha:float) -> float:
    # raw P90 prediction on calibration set
    q_pred = q_model.predict(X_cal)
    # nonconformity score (one per row)
    scores = y_cal - q_pred
    # 10th, 50th, 90th percentile of scores
    q_hat = np.quantile(scores, alpha)

    return q_hat

# generalize q_hat on other model
def predict_interval(models, q_hat_p50, q_hat_p90, X) -> pd.DataFrame:
    p10 = models["q10"].predict(X)
    p50 = models["q50"].predict(X) + q_hat_p50
    p90 = models["q90"].predict(X) + q_hat_p90

    return pd.DataFrame({"p10": p10, "p50": p50, "p90": p90}, index=X.index)