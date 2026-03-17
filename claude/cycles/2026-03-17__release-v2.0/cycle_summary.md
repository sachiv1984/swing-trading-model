**Owner:** Facilitator
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v2.0
**Cycle:** 2026-03-17__release-v2.0
**Last Updated:** 2026-03-17

---

# Cycle Summary — v2.0 Reporting & Alerts

**Run type:** Release planning
**Date:** 2026-03-17
**Mode:** standard
**Capacity check:** WARN
**Escalations:** 0

---

## Release Scope

| Epic | Theme | Stories | Sprint |
|------|-------|---------|--------|
| EPIC-01 | 4.3 Signal Exposure Enhancement | ST-01, ST-02 | Sprint 1 |
| EPIC-02 | 4.1b Tax-Year P&L Statement | ST-03–ST-05 | Sprint 1 (spec) + Sprint 2 (impl) |
| EPIC-03 | 3.5 Alerts & Notifications *(conditional)* | ST-06–ST-11 | Sprint 2 if QA gate clears |
| EPIC-04 | Backend Completeness — P1 fix + stretch | ST-12, ST-13 | Sprint 1 (ST-12 item 1) |
| EPIC-05 | Documentation & Standards Pack | ST-14–ST-17, ST-20 | Parallel track |
| EPIC-06 | Governance Tooling | ST-18–ST-19 | Parallel track |

**Total stories:** 20 (ST-01 to ST-20)
**Conditional:** ST-06–ST-11 (EPIC-03) — require QA gate 3 clearance (DL-003)
**Stretch:** ST-13, ST-20

---

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| BLG-BE-01 P1 fix included in v2.0 Sprint 1 item 1 | Avoids v1.11 governance overhead; P1 must ship as early as possible |
| EPIC-03 treated as conditional scope | QA gate 3 (DL-003) still pending; cannot enter sprint execution until cleared |
| EPIC-06 (governance tooling) as parallel track | BLG-GOV-01 + BLG-GOV-02 are 40 hrs mid — too large to fit in product sprints; run as governance work alongside |
| No escalations raised | All risks mitigated by conditional flags and sequencing constraints |

---

## Capacity Summary

| Scenario | Mid hrs | Assessment |
|----------|---------|------------|
| EPIC-01 + EPIC-02 + EPIC-04 + EPIC-05 (core) | ~42 hrs | Within 2-sprint baseline |
| + EPIC-03 (if gate clears) | ~72 hrs | WARN — may require 3 sprints |
| + EPIC-06 (parallel track) | ~112 hrs | Parallel track; not sprint execution |

Sprint 1 recommendation: ST-12 (P1), ST-01/02, ST-03, ST-14/15/16, ST-11 (~14 hrs mid — light)
Sprint 2 recommendation: ST-04/05, ST-17, EPIC-03 if gate cleared (~40 hrs mid with EPIC-03)

---

## Readiness Gaps

| Gap | Resolution path |
|-----|----------------|
| No signals page frontend spec | ST-01 authors it in Sprint 1 |
| No tax-year P&L spec | ST-03 authors it in Sprint 1 |
| No alerts/notification spec | ST-06 conditional on QA gate 3 (DL-003) |
| QA gate 3 (notification delivery) uncleared | ST-11 materialises the gate clearance output; must complete before ST-07–ST-10 start |

---

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] QA gate 3 clearance for 3.5 Alerts — Complete the QA planning session for notification delivery (test types, delivery modes, test infrastructure) and document output in `qa_notification_planning.md`. Determines whether EPIC-03 enters Sprint 2 or defers to v2.1. — Owner: Director of Quality
- [ ] [RISK-02] Tax-year P&L spec sign-off — ST-03 (reports_endpoints.md) must be authored and signed off by Head of Specs Team and Financial Reporting & Records Owner before ST-04 (backend) begins. Sprint planning must verify ST-03 is in scope for Sprint 1 or that its sign-off is pre-confirmed. — Owner: Head of Specs Team

---

## Next Steps

1. `run design-gate --cycle 2026-03-17__release-v2.0` — required before sprint planning (Phase 1.5)
2. `plan sprint --cycle 2026-03-17__release-v2.0` — Phase 2 sprint planning
3. Director of Quality to run QA notification planning session (ST-11 / DL-003 gate clearance) — can be done before sprint planning to pre-clear RISK-01
4. Head of Specs Team + Financial Reporting & Records Owner to pre-clear ST-03 scope (RISK-02)
