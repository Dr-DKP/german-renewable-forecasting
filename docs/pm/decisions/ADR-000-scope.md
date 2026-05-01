# ADR-000 :  Deliberate Scope for P2

**Status:** Accepted
**Date:** 2026-04-17
**Author:** Dr. Deepak K. Pandey
**Deciders:** Self (solo project)

> **Corporate vocab:** An *ADR* (Architecture Decision Record) is a short document capturing one important decision: the context, the options considered, the choice made, and the consequences. Engineering teams use ADRs so future maintainers (including future-you) understand *why* something was built the way it was. ADR-000 by convention always frames project scope.

---

## Context

P2 is one of three portfolio projects in a 40-day parental-leave build sprint targeting DACH renewable-energy and agentic-AI roles. The predecessor enercast screening demonstrated that *claims without artifacts* do not land; this project exists to produce artifacts, not promises. The 40-day budget is hard; over-scoping P2 would cost P3, which is where agentic-AI market exposure lives.

## Decision drivers

1. **Recruiter-readable in ≤3 minutes**, someone skimming the README must understand the differentiator in one paragraph.
2. **PhD-level signal**, every technique used must either be physics-grounded or statistically rigorous.
3. **Shippable in 22 days × 3h/day ≈ 66 build hours**, ruthless cut of anything that does not fit.
4. **P3-compatible**, API contract must let P3 consume forecasts as a tool.

## Considered options

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **A. Standard Prophet → XGBoost → LSTM comparison (original plan)** | Familiar, textbook | Every bootcamp grad ships this; no PhD signal | Rejected |
| **B. Multi-region, multi-source, real-time streaming** | Impressive surface area | 22 days impossible; LSTM probably won't beat residual-XGB anyway | Rejected |
| **C. Solar-only, DE aggregate, physics + calibrated UQ** | Deep not wide; physics identity play; rigorous UQ matches DACH forecasting product-space | Narrower surface area; must defend in README | **Accepted** |

## Decision

**Scope P2 to Option C.** Solar generation only, Germany aggregate, physics-informed residual learning, calibrated probabilistic forecasts via quantile + split conformal, FastAPI + Streamlit + Docker.

### In scope (must ship)
- Solar generation forecasting (DE aggregate)
- Day-ahead 24h hourly horizon
- TimescaleDB storage
- pvlib clear-sky physics baseline
- XGBoost on residuals
- Quantile regression (q10/q50/q90)
- Split conformal prediction via MAPIE
- CRPS + reliability diagrams
- FastAPI `/forecast` + `/health`
- Streamlit 3-page dashboard
- docker-compose one-command startup
- PM artifacts (ADRs, Kanban, risk register, weekly reports, retros, wiki)

### Out of scope (deliberately deferred)
| Item | Why deferred |
|---|---|
| Wind generation | Solar rigorously beats solar+wind half-shipped. Wind reuses the scaffolding; obvious v2. |
| Multi-region (TSO zones) | One region proves calibration. Multi-region is engineering reuse, not new signal. |
| Intraday 6h horizon | Day-ahead is the €-relevant horizon. Adding intraday doubles testing surface. |
| LSTM | If physics+residual+conformal beats Prophet (ablation will show), LSTM adds marginal value at high engineering cost. The **decision to cut** is the PM signal. |
| Gridded NWP / multiple weather points | Same logic as multi-region. |
| Real-time streaming ingestion | Daily cron is sufficient for day-ahead forecasting. |
| Feature store | Overkill for 22-day solo build. |
| Kubernetes | Not justified below production scale. |
| LLM / agentic layer | P3 scope. |

### Items kept despite tightness
- **TimescaleDB**: "Postgres + hypertables" is hirable in DACH; extra infra day pays back.
- **Docker multi-container**: "runs with one command" is the recruiter litmus test.
- **CRPS**: the single clearest evidence of probabilistic-forecasting literacy; cheap to compute once.

## Consequences

- **Positive:** crisp interview story; every artifact in the repo has a purpose; scope discipline is itself a hireable signal (documented here).
- **Negative:** repo looks narrower on first glance than a multi-model project. Mitigation: README §2 explicitly frames the narrowness as a strength.
- **Trade-off accepted:** cannot claim "wind forecasting experience" from this project alone. Addressed in cover letter by pointing to architectural extensibility.

## Cross-project dependencies

P3 will consume P2 via:
- `GET /health`: pre-tool-call liveness check
- `POST /forecast` body: `{ "region": "DE", "horizon_hours": 24, "include_uncertainty": true }`
- Response shape locked in Phase 5; any change requires amending this ADR + `ADR-004-api-contract.md`.

## Revisit

This ADR is revisited at the mid-sprint retro (Day 13). If Phase 3 delivers faster than expected, items may move from "Deferred" to "Stretch", but new work never enters without a scope amendment in this file.
