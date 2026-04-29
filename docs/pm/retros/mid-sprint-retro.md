# Retrospective -- Mid-Sprint

**Date:** 2026-04-29
**Covers:** Days 1-13 (Phases 0 through 4.5)

---

## Start

- **Committing every ~45 minutes** rather than at the end of a session. Several sessions accumulated a lot of work before any commit, which made it harder to isolate what broke what.
- **Running pytest locally before every push**, not just waiting for CI to catch it. Two or three bugs would have been caught earlier.
- **Updating the kanban during the work session**, not at the end. It fell out of sync and needed a catch-up pass.

---

## Stop

- **Debugging by trying random changes.** When something broke, the reflex was to change things and re-run. Forming a hypothesis first and running a minimal experiment is faster and produces a useful note as a side effect.
- **Writing functions with hard-coded assumptions that need to be generalised one session later.** `fit_conformal` was written for P90 only and had to be refactored when P50 calibration was needed.

---

## Continue

- **Writing ADRs the session a decision is made.** ADR-001, ADR-002, and ADR-003 each capture reasoning that would be completely lost a week later.
- **Keeping the physics layer as the architectural spine.** The residual decomposition has stayed clean throughout. Every component connects back to it.
- **Building the SQL layer after the Python pipeline was stable.** Adding TimescaleDB once the data structure was settled meant no rework.

---

## Biggest surprise

P90 conformal coverage held at 0.869 despite a seasonal distribution shift between calibration (Aug-Oct) and test (Oct-Dec) sets. P50, however, broke under the same shift, landing at 0.28 instead of 0.50. The same algorithm behaved very differently for the two quantiles. This turned out to be a more interesting result than a clean result would have been, and the root cause is a well-understood limitation with a known production fix.

---

## Biggest mistake

Not writing `fit_conformal` with a generalised `alpha` parameter from the start. The function was built for P90 only and had to be refactored when P50 calibration was added. Writing it generically would have taken 30 seconds and saved a full debugging round.

---

## What I would tell a teammate starting this phase tomorrow

- The physics baseline is not a toy. It is the reason the XGBoost model works as well as it does. Do not skip it or treat it as a placeholder.
- Data leakage in time-series splits is easy to introduce and hard to notice. Use `shuffle=False` everywhere and think explicitly about what each split boundary means in calendar time.
- When conformal prediction produces unexpected coverage, the first question is whether calibration and test come from the same distribution. Check the dates before debugging the code.
- Read the full error message before changing anything. Most bugs in this project were caught faster by reading carefully rather than skimming and guessing.
- TimescaleDB is worth setting up, but do it after the ML pipeline is stable, not before. The data structure needs to be settled first.

---

## Changes to scope or plan from this retro

- MLflow logging deferred from Phase 3 to Phase 5. Pragmatic decision; it must be wired before the FastAPI endpoint is built.
- Phase 4.5 (TimescaleDB integration) added between Phase 4 and Phase 5. This was always the intent; the budget was available on Day 13.
- No scope cuts needed. Phases 0-4.5 are complete on Day 13 with 9 days remaining for Phases 5-6.
