# Kanban — P2 Sprint

**Mirror this board on GitHub Projects for public visibility.** Update daily during the "Close" block.

> **Corporate vocab:** *Kanban board* = a visual work-in-progress tracker (Japanese for "signal card"). Columns represent stages of work. *WIP limit* (work-in-progress limit) caps how many cards can be in a column simultaneously — forcing focus. For this project, limit **In Progress** to 1 card.

---

## Column definitions

| Column | Meaning |
|---|---|
| 📋 Backlog | Scoped, not yet started |
| 🏃 In Progress | Actively worked on (WIP limit: 1) |
| 🔎 Review | Code done, needs test / wiki note / commit |
| ✅ Done | Committed, pushed, wiki-noted, closed |
| 🚫 Deferred | Explicitly deferred (links to ADR) |

---

## 📋 Backlog

### Phase 0 — Foundations (Days 1-2)
- [x] D1.1 — `gh repo create` + push, public
- [x] D1.2 — `docker-compose.yml` with TimescaleDB service
- [x] D1.3 — Commit CLAUDE.md, P2 plan, README stub
- [x] D1.4 — Commit ADR-000
- [x] D1.5 — Seed Kanban + risk register
- [x] D2.1 — `requirements.txt` + `environment.yml`
- [x] D2.2 — `tests/test_smoke.py`
- [x] D2.3 — GitHub Actions CI (ruff + pytest)
- [x] D2.4 — First concept note `01-hypertables.md`

### Phase 1 — Data Foundation (Days 3-5) — *unpacked as Phase 0 closes*
- [x] SMARD client
- [x] Open-Meteo client
- [x] Notebook 01 ingestion + sanity checks

### Phase 2 — EDA + Physics Baseline (Days 6-8)
- [x] EDA notebook 02
- [x] pvlib clear-sky implementation (`src/physics/clear_sky.py`)
- [x] Notebook 03 physics baseline (R²=0.78)
- [x] ADR-001 + WK01 report

### Phase 3 — Features + XGBoost Residual (Days 9-12)
- [x] Feature engineering (`src/features/feature_view.py`)
- [x] Training matrix assembler (`src/data/training_matrix.py`)
- [x] XGBoost residual learner (R²=0.92, MAE=1552 MW) — MLflow deferred, not blocking
- [x] Notebook 04 comparison
- [x] ADR-002

### Phase 4 — Calibrated UQ (Days 13-16)
- [x] Quantile XGBoost (P10/P50/P90)
- [x] Conformal calibration (split conformal, generalised alpha)
- [x] Reliability diagrams + CRPS (514.6 MW) + sharpness (3842 MW)
- [x] Notebook 05
- [ ] Mid-sprint retro + WK02 + ADR-003 — due next session

### Phase 4.5 — TimescaleDB Integration (added 2026-04-28)
- [x] `sql/create_tables.sql` — hypertable DDL
- [x] `src/data/db_ingestion.py` — parquet → TimescaleDB
- [x] `sql/feature_view.sql` — SQL lag feature view

### Phase 5 — API + Dashboard + Docker (Days 17-19)
- [ ] FastAPI /forecast + /health
- [ ] Streamlit 3-page dashboard
- [ ] docker-compose + clone-test
- [ ] ADR-004

### Phase 6 — Write-up (Days 20-22)
- [ ] README revamp
- [ ] Blog post + LinkedIn draft
- [ ] Demo video + final retro + WK03

---

## 🏃 In Progress

- Phase 5 — FastAPI /forecast + /health endpoints

---

## 🔎 Review

*(Code written, not yet committed / wiki-noted.)*

---

## ✅ Done

- **Phase 4.5 — TimescaleDB Integration** — completed 2026-04-29
  - `sql/create_tables.sql` — two hypertables: `solar_generation`, `weather_observations`
  - `src/data/db_ingestion.py` — 26,281 solar rows + 26,304 weather rows loaded
  - `sql/feature_view.sql` — SQL view with LAG + rolling AVG + EXTRACT time features
  - `tests/test_smoke.py` — 4 tests: connection, extension, hypertable metadata, row count

- **Phase 0 — Foundations** — completed 2026-04-20
  - Repo public on GitHub, docker-compose + TimescaleDB running
  - smoke test passing locally, CI green on GitHub Actions
  - wiki notes 01–07 written, requirements fixed, README cleaned

- **Phase 4 -- Calibrated UQ** -- completed 2026-04-28
  - `src/models/quantile_model.py` -- P10/P50/P90 quantile XGBoost
  - `src/models/conformal.py` -- split conformal calibration (generalised to any alpha)
  - `src/evaluation/metrics.py` -- CRPS added
  - `notebooks/05_uq.ipynb` -- P90 coverage=0.90, CRPS=514.6 MW, sharpness=3842 MW
  - P50 miscalibration documented (seasonal exchangeability violation)
  - wiki note 11 pending

- **Phase 3 -- Features + XGBoost Residual** -- completed 2026-04-27
  - `src/features/feature_view.py` -- lag, rolling, time encoding features
  - `src/data/training_matrix.py` -- assembles X (26,279 x 6) and y (residual)
  - `notebooks/04_xgboost_residual.ipynb` -- R²=0.92, MAE=1,552 MW (vs physics R²=0.78)
  - `docs/pm/decisions/ADR-002` written
  - wiki note 10-xgboost-residual-learning.md written

- **Phase 2 -- Physics Baseline** -- completed 2026-04-23
  - `src/physics/clear_sky.py` — pvlib Ineichen-Perez, SCALING_FACTOR=37.5
  - `tests/test_clear_sky.py` — 3 tests, CI green
  - `notebooks/03_physics_baseline.ipynb` — R²=0.78, MAE=3856 MW
  - `docs/pm/decisions/ADR-001-physics-model-choice.md` written
  - WK01 report written

- **Phase 2 — EDA notebook** — completed 2026-04-23
  - Monthly/hourly patterns confirmed, cloud cover scatter, radiation scatter
  - pvlib clear-sky GHI computed, scaling factor = 37.5 MW per W/m²
  - Residual formula visualised on July 2023 week
  - wiki note 09-clear-sky-irradiance.md written

- **Phase 1 — Data Foundation** — completed 2026-04-21
  - `src/data/smard_client.py` — live API tested, tz bug fixed
  - `src/data/openmeteo_client.py` — built and tested
  - `tests/test_smard_client.py` + `tests/test_openmeteo_client.py` — CI green
  - `notebooks/01_ingestion.ipynb` — 3 years pulled, diurnal pattern confirmed, SMARD 2MW floor noted
  - wiki note 08-rest-apis.md written

---

## 🚫 Deferred (with reason)

- Wind generation → ADR-000
- Multi-region (TSO zones) → ADR-000
- Intraday 6h horizon → ADR-000
- LSTM → ADR-000
- Gridded NWP → ADR-000
- Real-time streaming → ADR-000
- LLM / agentic layer → P3 scope
