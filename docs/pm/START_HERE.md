# START HERE :  Day 1 Checklist

**Date:** 2026-04-17 (Friday) · **You are about to begin Day 1 of the P2 sprint.**

Each bullet below is ~10-20 minutes. Do them in order.

---

## Morning :  before opening Claude

- [ ] Read this file end-to-end (5 min).
- [ ] Read `CLAUDE.md` end-to-end (10 min).
- [ ] Read `P2_Energy_Forecasting.md` sections 1-4: thesis, why this matters, scope, architecture (15 min).
- [ ] Read `docs/pm/decisions/ADR-000-scope.md` (10 min).

## In the terminal :  15 minutes

- [ ] `cd /Volumes/ExternalSSD/Users/deepak/Projects/Portfolio/german-renewable-forecasting`
- [ ] `git status`: confirm clean working tree
- [ ] Create public GitHub repo. Ask Claude for the exact `gh` command before running it. *(Claude will explain what `gh` is: the GitHub CLI tool, before showing the command.)*
- [ ] Verify the repo appears public at `https://github.com/DR-DKP/german-renewable-forecasting`

## With Claude :  your first real session

- [ ] Open Claude in this directory
- [ ] First message: **"Day 1 start: let's scaffold the project"**
- [ ] Claude will:
  1. Run the session-start ritual (read CLAUDE.md, kanban, etc.)
  2. Confirm today's focus in one sentence
  3. Teach Docker + TimescaleDB concepts **before** writing any YAML
  4. Build `docker-compose.yml` with a TimescaleDB service
  5. Write `docs/wiki/concepts/01-hypertables.md` at end of session
  6. Update Kanban
- [ ] Commit + push at end of the 3h build block
- [ ] Move Day-1 Kanban cards from **In Progress** → **Done**

---

## End of Day 1 :  success looks like

- ✅ Public GitHub repo
- ✅ `docker compose up` starts a TimescaleDB container
- ✅ At least one Kanban card moved to **Done**
- ✅ ADR-000 visible in `docs/pm/decisions/`
- ✅ First wiki note committed
- ✅ At least one meaningful commit pushed to `main`

**If any of these are red at end-of-day: STOP. Don't start Day 2. Debug with Claude first.**

---

## Saturday rule reminder (Apr 18)

Badminton 10:00-13:00. **No coding.** Before leaving, spend 2 minutes re-reading `CLAUDE.md` §1, the project thesis. That is the only Saturday task.

## Sunday rule reminder (Apr 19)

Flex day. If energetic → Day 2 (dependencies + CI). If not → rest. Tell Claude at session start so today's plan matches.

---

## One-line rule of the sprint

> **Ship boring, document everything, cut ruthlessly.**
