"""Tests for evaluation metrics."""

import numpy as np
from src.evaluation.metrics import rmse, mae, coverage, sharpness


def test_rmse_perfect():
    y = np.array([1.0, 2.0, 3.0])
    assert rmse(y, y) == 0.0


def test_mae_known():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([2.0, 3.0, 4.0])
    assert mae(y_true, y_pred) == 1.0


def test_coverage_full():
    y = np.array([1.0, 2.0, 3.0])
    lower = np.array([0.0, 1.0, 2.0])
    upper = np.array([2.0, 3.0, 4.0])
    assert coverage(y, lower, upper) == 1.0


def test_sharpness():
    lower = np.array([0.0, 1.0])
    upper = np.array([2.0, 3.0])
    assert sharpness(lower, upper) == 2.0
