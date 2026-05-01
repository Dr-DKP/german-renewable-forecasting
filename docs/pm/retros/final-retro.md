# Retrospective: Final Sprint

**Date:** 2026-05-01
**Covers:** Phases 0 through 6 (full sprint)

---

## Start

- **Running `docker compose up --build` after every source file change**, not just `docker compose up`. The stale image problem cost real time across multiple sessions.
- **Injecting environment variables for any value that differs between local and Docker runtime.** Hardcoded hostnames like `localhost` inside container code are bugs waiting to happen.
- **Testing the serving layer with an out-of-training-distribution date early.** The gap between predicted and actual in the dashboard would have surfaced the zero-weather-input issue before the final session.

---

## Stop

- **Assuming Python paths that work in notebooks will work when running as a module.** `../data/raw/` relative paths broke the moment the code was called from the project root. Module-relative paths using `Path(__file__).resolve().parents[N]` are the correct pattern.
- **Treating the tracking database as a given in Docker deployments.** MLflow's `runs:/` URI scheme depends on a tracking server with correct paths. In a containerised environment, direct artifact paths are simpler and more portable.

---

## Continue

- **Writing ADRs the moment a decision is made.** All five ADRs in this project were written within the same session as the decision. Reasoning captured in the moment is useful; reasoning reconstructed a week later is speculation.
- **Keeping the physics layer as the architectural spine.** The residual decomposition stayed clean from Phase 2 through to the serving layer. `physics_pred` ended up as the top XGBoost feature, which is exactly what you want from a physics-informed design.
- **Being honest about limitations.** The P50 miscalibration is documented in ADR-003 and visible in the reliability diagram on the dashboard. A project that measures its own failures honestly is more credible than one that only reports clean numbers.
- **Building in phases with clear handoffs.** Each phase produced a committed artifact (notebook, ADR, wiki note) before the next began. This made it possible to pick up after a break without losing context.

---

## Biggest surprise

The XGBoost model treats `physics_pred` as its single most important feature, not the weather variables. This means the model is primarily scaling and correcting the physics signal rather than replacing it. That is the behaviour you would want from a residual learner by design, but seeing it confirmed in the feature importance scores was a good validation that the architecture is working as intended.

---

## Biggest mistake

Not parameterising `fit_conformal` from the start. The function was written for a single quantile and had to be refactored when a second was needed. The fix was small, but the refactor took longer than the original would have. Generic by default, specific only when forced.

---

## What I would tell a teammate starting this project tomorrow

- Start with the physics baseline before writing a single line of ML code. A principled baseline tells you what the model needs to learn and gives you a feature for free.
- Time-series splits must use `shuffle=False`. Leaking future data into training is the most common error in forecasting projects and the hardest to detect after the fact.
- Conformal prediction is not magic. It provides a coverage guarantee only if calibration and test data come from the same distribution. Check the date boundaries before trusting the coverage numbers.
- Docker networking is not the same as localhost. Every service name, port, and path needs to be verified from inside the container, not from the host.
- Ship a working system before polishing the metrics. A running API beats a perfect notebook.

---

## What shipped

| Phase | Key deliverable | Status |
|---|---|---|
| 0: Foundations | Repo, CI, Docker, TimescaleDB | Complete |
| 1: Data | SMARD + Open-Meteo clients, 3 years of data | Complete |
| 2: EDA + Physics | pvlib clear-sky baseline, R²=0.78 | Complete |
| 3: XGBoost residual | Residual learner, R²=0.92, MAE=1,552 MW | Complete |
| 4: Calibrated UQ | Quantile XGBoost + conformal, CRPS=514.6 MW | Complete |
| 4.5: TimescaleDB | Hypertables, ingestion, SQL feature view | Complete |
| 5: API + Docker | FastAPI, Streamlit, docker-compose | Complete |
| 6: Write-up | README, ADR-004, WK03 | Complete |
