# Risk Register

> **Corporate vocab:** A *risk register* is a live table of things that could go wrong, how likely they are, how bad they would be, and what you are doing about them. Reviewed weekly + whenever a new risk surfaces. The act of writing one is signal; the act of *updating* one is the actual value.

**Columns:**
- **P** = Probability (L / M / H)
- **I** = Impact (L / M / H)
- **Status:** Open / Mitigated / Accepted / Occurred

---

| ID | Risk | P | I | Mitigation | Status | Last review |
|---|---|---|---|---|---|---|
| R01 | SMARD API schema change or downtime during sprint | M | H | On Day 3, snapshot downloaded historical data into repo (git-LFS if needed). All code reads snapshot first, live API second. | Open | 2026-04-17 |
| R02 | pvlib learning curve blocks progress >1 day | M | M | Fallback to simplified Ineichen-Perez analytical formula; ADR-001 documents the trade-off. | Open | 2026-04-17 |
| R03 | Conformal prediction coverage misses target [78%, 82%] | L | H | If empirical coverage <78%: inspect residual distribution, switch to CQR (Conformalized Quantile Regression). | Open | 2026-04-17 |
| R04 | 22-day P2 budget slips | M | H | Pre-declared scope cuts ready: (a) drop dashboard page 3, (b) drop Prophet comparison, (c) defer blog post to post-leave. | Open | 2026-04-17 |
| R05 | Python-beginner debugging cost exceeds 1h/day | M | M | CLAUDE.md teaching contract + wiki accumulation. If 3 blockers/week → pause for remedial reading day. | Open | 2026-04-17 |
| R06 | Parental leave ends with P3 incomplete | M | M | P3 scoped tight to 15 days; 3-day buffer. If slipping → defer blog polish to post-leave. | Open | 2026-04-17 |
| R07 | Burnout from overwork | L | H | Saturday sacred-rest (badminton). No work beyond 4h daily block. Partner aware of schedule. | Open | 2026-04-17 |
| R08 | Scope creep from user asking for deferred items | M | M | CLAUDE.md R9: Claude must flag + log any scope-pressure event before acting. | Open | 2026-04-17 |

---

## Log of occurred risks

*When a risk materialises, move it here with date + what actually happened + lesson learned.*

---

## New risks identified during sprint

*Append as they surface. Claude updates this section at the end of each weekly report.*
