# ADR-002: Use XGBoost as residual learner to correct physics baseline errors

**Status:** Accepted -- 2026-04-27

---

## Context

The pvlib Ineichen-Perez physics baseline (ADR-001) achieves R²=0.78 and MAE=3,856 MW on daylight hours. It assumes a perfectly clear sky and cannot account for cloud cover, aerosols, or curtailments. Germany averages 60-70% cloud cover, meaning the physics model systematically overestimates output on most days. A supervised learner is needed to predict the residual: `residual = actual_solar - physics_pred`.

The learner receives 6 features: `hour`, `month`, `cloud_cover_lag_1h`, `radiation_lag_1h`, `cloud_cover_rolling_3h`, `physics_pred`. Target: residual in MW. Training data: 21,023 hourly rows (Jan 2022 to Aug 2024). Test data: 5,256 rows (Sep to Dec 2024), strictly held out.

## Decision

Use `XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6)` trained on the residual target.

Three alternatives were considered:

| Option | Pro | Con |
|---|---|---|
| XGBoost (chosen) | Handles non-linear weather interactions; each tree corrects previous errors; strong tabular performance | Requires hyperparameter tuning; no built-in uncertainty |
| Linear regression | Simple, fully interpretable | Cannot model non-linear cloud-radiation interactions; poor residual fit expected |
| Prophet | Designed for trend and seasonality decomposition | Not suited for weather-driven residual correction; no cloud cover input |

## Consequences

- Test set performance: **R²=0.92, MAE=1,552 MW, RMSE=3,095 MW**
- MAE reduced by **60%** vs physics baseline alone
- Top feature by importance: `physics_pred` -- XGBoost amplifies the physics signal and corrects around it
- Point forecast only -- no uncertainty bounds yet. Phase 4 adds calibrated prediction intervals via quantile regression and conformal prediction.
