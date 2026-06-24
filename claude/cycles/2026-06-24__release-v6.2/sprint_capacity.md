**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-24
**Cycle:** 2026-06-24__release-v6.2

---

# Sprint Capacity — 2026-06-24__release-v6.2

---

## Capacity Baseline

| Field | Value |
|-------|-------|
| Sprint duration | 2 sprints (~2–3 weeks each) |
| Available FTE | Solo developer (evenings/weekends) |
| Per-sprint capacity | ~12–14 working-effort days |
| Warn threshold | > 14 days per sprint |
| Skill constraints | None — all required skills held by sole operator |

**Source:** `claude/roadmap/workforce_capacity.md` (effective 2026-05-27 — revised upward from 8–10d to 12–14d/sprint to reflect sustained actual pace).

---

## Item Effort Mapping

### Sprint 1 — EPIC-01 + EPIC-03

| EPIC | Story | Title | Effort | Delegation Class |
|------|-------|-------|--------|-----------------|
| EPIC-01 | ST-01 | Nightly trailing stop computation — backend service | ~2 days | delegated_backend |
| EPIC-01 | ST-02 | Trailing stop display and breach badge — frontend | ~1 day | delegated_frontend |
| EPIC-01 | ST-03 | Month-end rebalance exit signal generation | ~1.5 days | delegated_backend |
| EPIC-01 | ST-04 | Inverse-volatility position sizing for signal-driven entries | ~2 days | delegated_backend |
| EPIC-01 | ST-05 | Risk-off exit alerts for existing positions | ~0.5 day | delegated_backend |
| EPIC-03 | ST-10 | execution_prompt autonomous class hard gate (BLG-GOV-135) | < 0.25 day | autonomous |
| EPIC-03 | ST-11 | execution_prompt test_scenarios path validation (BLG-GOV-136) | < 0.25 day | autonomous |
| EPIC-03 | ST-12 | api_performance_baseline.md — 2 new v6.1 endpoints (BLG-OPS-75) | < 0.25 day | autonomous |
| EPIC-03 | ST-13 | Playwright spec auto-registration via glob pattern (BLG-QA-62) | ~0.75 day | delegated_qa |
| **Sprint 1 total** | | | **~8.5 days** | |

### Sprint 2 — EPIC-02 (Conditional — §13 review required)

| EPIC | Story | Title | Effort | Delegation Class |
|------|-------|-------|--------|-----------------|
| EPIC-02 | ST-06 | AI daily briefing — backend endpoint | ~2 days | delegated_backend |
| EPIC-02 | ST-07 | AI Daily Briefing card — frontend | ~0.5 day | delegated_frontend |
| EPIC-02 | ST-08 | Conversational AI trade advisor — backend endpoint | ~1 day | delegated_backend |
| EPIC-02 | ST-09 | AI chat widget — frontend | ~0.5 day | delegated_frontend |
| **Sprint 2 total** | | | **~4 days** | |

---

## Total Effort vs Capacity

| Sprint | Estimated Effort | Available Capacity | Utilisation | Status |
|--------|-----------------|-------------------|-------------|--------|
| Sprint 1 (EPIC-01 + EPIC-03) | ~8.5 days | ~12–14 days | ~61–71% | PASS |
| Sprint 2 (EPIC-02) | ~4 days | ~12–14 days | ~29–33% | PASS |
| **Overall** | **~12.5 days** | **~24–28 days** | **~45–52%** | **PASS** |

**Note on release planning WARN:** `release_plan.md` recorded capacity_check = `warn` because total estimated effort (12.5 days) was assessed against a single-sprint baseline at release planning time. With the 2-sprint phasing plan (Sprint 1: 8.5d, Sprint 2: 4d), each sprint is well within the 12–14d/sprint capacity baseline. The 2-sprint plan resolves the WARN — Product Owner acknowledgement of this phasing satisfies the capacity WARN condition.

---

## Conditional (Deferred at Planning)

EPIC-02 is included in Sprint 2 of this sprint plan but is conditional on the following gate being cleared before sprint planning seals:

| EPIC | Stories | Effort | Gate Condition |
|------|---------|--------|---------------|
| EPIC-02 | ST-06, ST-07, ST-08, ST-09 | ~4 days | Strategy Rules §13 review for BLG-FEAT-50 (AI daily briefing) and BLG-FEAT-51 (AI chat advisor) — must be recorded in `docs/product/decisions/decisions--2026-06-24__release-v6.2.md` before sprint planning seals. Owner: Strategy Rules & System Intent Owner. |

**Gate re-invocation advisory:** If the §13 review is completed after the sprint backlog seals (e.g., EPIC-02 was deferred post-seal), do not add EPIC-02 stories informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-24__release-v6.2 --reason "EPIC-02 §13 review completed"`) to add them through the authorised path.
