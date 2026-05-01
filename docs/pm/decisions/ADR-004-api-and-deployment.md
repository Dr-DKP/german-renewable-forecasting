# ADR-004: FastAPI + Streamlit + Docker Compose as the serving layer

**Status:** Accepted -- 2026-05-01

---

## Context

The forecasting pipeline produces calibrated probabilistic outputs (P10/P50/P90). These need to be accessible to an end user without requiring them to run Jupyter notebooks or install Python. The serving layer must expose a machine-readable API for downstream consumers (a P3 agentic system is already planned) and a human-readable dashboard for portfolio demonstration.

Three constraints shaped the decision: the system must start from a single command (`docker compose up`), all services must be reproducible on any machine without manual setup, and the architecture must be explainable to a hiring panel in two sentences.

## Decision

**API:** FastAPI, served via Uvicorn.
**Dashboard:** Streamlit, 3 pages: probabilistic forecast, model info, project about.
**Orchestration:** Docker Compose with three services: `timescaledb`, `api`, `dashboard`.

The API loads three XGBoost quantile models at startup via MLflow artifact paths. The Streamlit dashboard calls the API over HTTP -- it does not access the models or database directly. The TimescaleDB service powers the `/actual` endpoint, enabling actual-vs-forecast overlays.

Model artifacts are mounted as a bind mount (`./mlruns`) rather than copied into the image, so retraining on the host is immediately reflected without rebuilding.

Three alternatives were considered:

| Option | Pro | Con |
|---|---|---|
| FastAPI + Streamlit + Docker Compose (chosen) | Clean separation of concerns; API is reusable by P3; Docker makes it one-command reproducible | More moving parts than a single-file notebook |
| Flask + Matplotlib | Simpler; fewer dependencies | No async support; Matplotlib charts are static; harder to maintain |
| Streamlit only (no API) | Fewest files | Dashboard and model logic are coupled; P3 agentic system cannot call a Python app directly; not a realistic production pattern |

## Consequences

- The API (`/health`, `/forecast`, `/actual`) is a stable contract that P3 can call without changes.
- Weather inputs in `/forecast` are currently hardcoded to zero (no live weather feed). Physics shape is correct; amplitude depends on cloud cover. This is a known limitation, documented in the README. The Open-Meteo forecast API (no credentials required) is the planned fix.
- MLflow 3.x stores artifacts under `mlruns/1/models/m-{uuid}/artifacts/` rather than under run IDs. Loading by direct path is required in Docker because the SQLite tracking database stores host-absolute artifact paths that are unreachable inside a container.
- The `API_URL` environment variable defaults to `http://localhost:8000` for local runs and is overridden to `http://api:8000` inside the Docker network.
