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
- [ ] D1.1 — `gh repo create` + push, public
- [ ] D1.2 — `docker-compose.yml` with TimescaleDB service
- [ ] D1.3 — Commit CLAUDE.md, P2 plan, README stub
- [ ] D1.4 — Commit ADR-000
- [ ] D1.5 — Seed Kanban + risk register
- [ ] D2.1 — `requirements.txt` + `environment.yml`
- [ ] D2.2 — `tests/test_smoke.py`
- [ ] D2.3 — GitHub Actions CI (ruff + pytest)
- [ ] D2.4 — First concept note `01-hypertables.md`

### Phase 1 — Data Foundation (Days 3-5) — *unpacked as Phase 0 closes*
- [ ] SMARD client
- [ ] Open-Meteo client
- [ ] Notebook 01 ingestion + sanity checks

### Phase 2 — EDA + Physics Baseline (Days 6-8) — *unpacked later*
- [ ] EDA notebook 02
- [ ] pvlib clear-sky implementation
- [ ] Notebook 03 physics baseline
- [ ] ADR-001 + WK01 report

### Phase 3 — Features + XGBoost Residual (Days 9-12) — *unpacked later*
- [ ] SQL feature view
- [ ] Training matrix assembler
- [ ] XGBoost residual + MLflow
- [ ] Notebook 04 comparison
- [ ] ADR-002

### Phase 4 — Calibrated UQ (Days 13-16) — *unpacked later*
- [ ] Quantile XGBoost
- [ ] Conformal wrapper (MAPIE)
- [ ] Reliability diagrams + CRPS
- [ ] Notebook 05
- [ ] Mid-sprint retro + WK02 + ADR-003

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

*(Move exactly one card here during the "Plan" block of the day. WIP limit: 1.)*

---

## 🔎 Review

*(Code written, not yet committed / wiki-noted.)*

---

## ✅ Done

*(Closed cards move here at end of day.)*

---

## 🚫 Deferred (with reason)

- Wind generation → ADR-000
- Multi-region (TSO zones) → ADR-000
- Intraday 6h horizon → ADR-000
- LSTM → ADR-000
- Gridded NWP → ADR-000
- Real-time streaming → ADR-000
- LLM / agentic layer → P3 scope
