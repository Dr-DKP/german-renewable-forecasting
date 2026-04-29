# ADR-003: Use quantile XGBoost + split conformal prediction for calibrated uncertainty quantification

**Status:** Accepted -- 2026-04-29

---

## Context

The XGBoost residual learner from ADR-002 gives one number per forecast hour. That is not useful for a grid operator who needs to know how much backup capacity to keep running. The question is not "what will solar output be?" but "what is the range it could plausibly fall in?" We need P10, P50, and P90 bounds per hour, where the stated coverage actually holds on real test data.

Three things matter here: the intervals need to be calibrated (what we say must match what happens), sharp (as narrow as possible), and the P90 guarantee has to be mathematical, not just a hope.

## Decision

We used a two-stage approach.

**Stage 1 -- Quantile XGBoost:** Three separate XGBRegressor models trained with `objective="reg:quantileerror"` and `quantile_alpha` set to 0.1, 0.5, and 0.9. Pinball loss penalises under- and over-prediction asymmetrically, so each model learns to predict the right percentile of the residual distribution rather than its mean.

**Stage 2 -- Split conformal prediction:** A calibration set (Aug to Oct 2024, 10% of data) was held out. We computed nonconformity scores on it: `score_i = actual_residual_i - q90_model.predict(X_cal_i)`. The 90th percentile of those scores gives `q_hat = 770.1 MW`. Adding this to every future P90 prediction provides a coverage guarantee that holds regardless of the shape of the residual distribution, as long as the calibration and test data come from the same distribution.

Data split used:
- Train: Jan 2022 to Aug 2024 (70%)
- Calibration: Aug to Oct 2024 (10%)
- Test: Oct to Dec 2024 (20%)

## Alternatives considered

| Option | Pro | Con |
|---|---|---|
| Quantile XGBoost without conformal | Fast and interpretable | No formal coverage guarantee |
| Quantile XGBoost + split conformal (chosen) | Mathematical guarantee under exchangeability | Needs separate calibration set; breaks under distribution shift |
| MAPIE library | Cleaner API, multiple conformal variants | Same algorithm underneath; adds a dependency without adding understanding |
| Bootstrap ensemble | No distributional assumptions | Computationally expensive; still no formal guarantee |

## Consequences

| Metric | Value | Target |
|---|---|---|
| P10 coverage | 0.036 | 0.10 |
| P50 coverage | 0.28 | 0.50 |
| P90 coverage | 0.869 | 0.90 |
| Sharpness | 3,842 MW | narrower than 47,000 MW (full output range) |
| CRPS | 514.6 MW | below point MAE of 1,552 MW |

**Known limitation -- P50 seasonal miscalibration:** The calibration set covers autumn solar patterns (Aug to Oct) while the test set covers winter (Oct to Dec). These are different distributions, which violates the exchangeability assumption conformal prediction relies on. P50 coverage is 0.28 instead of 0.50. P90 holds better because upper-bound corrections transfer more stably across seasons.

The fix for production is rolling calibration: recompute `q_hat` using only the most recent N days before each forecast, so the calibration window always matches the current season.
