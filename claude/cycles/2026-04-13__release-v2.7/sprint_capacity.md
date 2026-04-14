**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-14
**Cycle:** 2026-04-13__release-v2.7

---

# Sprint Capacity — v2.7

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | 2 sprints (~10 working days per sprint) |
| Available FTE | 1.0 (execution engine + delegated human actions) |
| Total capacity | ~20 capacity days |
| Skill constraints | ST-01: Infrastructure/Ops Owner (Render env var update — human action required); ST-09: Strategy Rules owner §13 COMPLIANT pre-existing (SRB-v1.7 Feature 3 — no new gate); ST-08: Yahoo Finance data access — existing validated pattern |

*Workforce capacity file: `claude/roadmap/workforce_capacity.md` — v2.7 items not individually listed; uses historical velocity baseline (0.99 rolling 6-cycle average, 11–15 stories per 2-sprint cycle).*

---

## Item Effort Mapping

### Sprint 1 — EPIC-01, EPIC-02, EPIC-03

| Item | EPIC | Effort Band | Estimated Days |
|------|------|-------------|----------------|
| ST-01 — Enable Supabase Supavisor pooling | EPIC-01 | XS (<1 hour) | ~0.25d |
| ST-02 — Refactor get_portfolio_summary() | EPIC-01 | M (~half day) | ~0.5d |
| ST-03 — QA evidence sign-off gate before PR | EPIC-02 | XS (<1 hour) | ~0.25d |
| ST-04 — Autonomous DoQ sign-off class | EPIC-02 | S (~0.5d) | ~0.5d |
| ST-05 — Extend governance_sync.yml to push main | EPIC-02 | XS (<1 hour) | ~0.25d |
| ST-06 — Fix Playwright page.route() intercepts | EPIC-03 | S (~0.5–1d) | ~0.75d |
| ST-07 — System Status Playwright spec | EPIC-03 | M (~1d) | ~1.0d |
| **Sprint 1 total** | | | **~3.5d** |

### Sprint 2 — EPIC-04, EPIC-05

| Item | EPIC | Effort Band | Estimated Days |
|------|------|-------------|----------------|
| ST-08 — Market Correlation Analysis | EPIC-04 | M (~1–2d) | ~1.5d |
| ST-09 — Supplementary indicator fields | EPIC-04 | M (~1–2d) | ~1.5d |
| ST-10 — Spec Dependency Map | EPIC-05 | M (~1–2d) | ~1.5d |
| ST-11 — Governance Health Score | EPIC-05 | M (~1–2d) | ~1.5d |
| **Sprint 2 total** | | | **~6.0d** |

---

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total estimated effort (conservative) | ~9.5d |
| Total estimated effort (release plan mid-point) | ~12d |
| Total confirmed capacity (2 sprints) | ~20d |
| Utilisation (conservative) | ~48% |
| Utilisation (mid-point) | ~60% |
| Over-allocation | No |

**Capacity verdict:** ✅ PASS — 11 stories at ~9.5–12d estimated effort fits comfortably within 2-sprint capacity at historical velocity. No over-allocation. No scarce skill conflicts requiring scope reduction.
