Owner: Product Owner
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-05 (initial decision, ESC-EXEC-20261105-04)
Cycle: 2026-11-03__release-v9.15
Story: ST-45 (EPIC-07, BLG-GOV-196)
Escalation ref: ESC-EXEC-20261105-04

---

# Priority 3 — Deferred Initiatives: Sunset Review

**Decision date:** 2026-11-05
**Decided by:** Product Owner (the user, in session), accepting the engine's recommendation as drafted in `ESC-EXEC-20261105-04`
**Subject:** the seven initiatives in `claude/roadmap/initiative_register.md` "Priority 3 — Deferred". They had not been re-confirmed since first recorded (`BLG-GOV-196`).
**AC reference:** `claude/cycles/2026-11-03__release-v9.15/stage4_backlog_slice.md#ST-45`

---

## Ruling per Initiative

| Initiative | Register rationale | Ruling | Reason |
|-----------|--------------------|--------|--------|
| Position Correlation Analysis | Not urgent; single-user scale | **Flag for review** | Market Correlation Analysis (MKT-COR) shipped v2.7 and may already cover part of it. The next `run roadmap` should decide whether the remainder is still a separate initiative or should be retired as covered. |
| Backtesting Module | High value; significant scope | **Flag for review** | PO-05 Lightweight Replay Mode on the roadmap replays historical signals against the strategy rules on the strategy backtest engine. The two overlap, so the next `run roadmap` should decide whether a separate backtesting module is still wanted. |
| Multi-Portfolio Support | Low value at current scale | **Re-confirmed deferred** | The system is single-user with one portfolio, and nothing has changed that. |
| Mobile App | Web experience sufficient | **Re-confirmed deferred** | The web app remains the delivery channel. Telegram already covers mobile alerts (SI-05 digest, alerts). |
| Full Compliance Scoring | Lightweight version in v1.9 | **Flag for review** | The Arc 5 composite compliance score shipped v4.1 (`metrics_definitions.md` v1.11) and is surfaced in Reports and the SI-05 digest. The item may now be done, or need a new definition of "full". |
| BLG-TECH-05 Prometheus | Defer until multi-user or operational need | **Re-confirmed deferred** | Still single-user, and no operational need has arisen: health checks, staging smoke tests and the AI cost and anomaly alerts cover monitoring today. |
| Customisable Dashboard Layout | High build cost; low current priority | **Flag for review** | The Site Structure & Usability programme is redesigning the Dashboard ("Today" spec, v9.15). That is the right point to decide whether a customisable layout is still wanted. |

Summary: 3 re-confirmed as deliberately deferred, 4 flagged for review.

## Effect

- `initiative_register.md` is unchanged (`sprint_backlog.md` ST-45 Notes). Any change, including retiring or re-scoping a flagged initiative, is left to the next `run roadmap`.
- **Carry-forward (AC 2, `post-merge`, tracked by BLG-GOV-408):** this record is an input to the next `run roadmap`, which reads the four flagged initiatives and decides each one.
- `BLG-GOV-196` is met by this record once ST-45 merges, apart from that carry-forward.
