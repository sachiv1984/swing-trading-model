**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.8
**Cycle:** 2026-04-17__release-v2.8
**Last Updated:** 2026-04-17

---

# Cycle Summary — Release Planning v2.8

## Release Overview

**Release:** v2.8 — Frontend Completion, Test Quality & AI Journal Feature
**Cycle ID:** 2026-04-17__release-v2.8
**Scope:** 6 items / 4 EPICs / 8 stories / 2 sprints
**Capacity verdict:** PASS (~52 hrs across 2 sprints; velocity 0.99)
**Plan status:** Published

---

## Scope Summary

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 2 | ST-01 | Market Correlation Frontend (BLG-FE-14) |
| EPIC-02 | Sprint 1 | ST-02, ST-03 | Test Scenario Coverage (BLG-QA-13) |
| EPIC-03 | Sprint 1 | ST-04, ST-05, ST-06 | Governance Process Hardening (CF-1, CF-2, BLG-GOV-13) |
| EPIC-04 | Sprint 2 | ST-07, ST-08 | AI Journal Summarisation (BLG-FEAT-16) |

**Deferred:** BLG-GOV-08 (v2.9, final deferral), BLG-GOV-11 (v2.9), BLG-FEAT-13 (v2.9+)

---

## Outstanding Carry-Forward Actions (from v2.7)

All 7 carry-forward items from v2.7 reviewed:
- CF-1 (DoQ Date field) → ST-04 in EPIC-03 ✓
- CF-2 (Sprint close terminology) → ST-05 in EPIC-03 ✓
- CF-3 (BLG-GOV-08 PO decision) → PO decided: defer to v2.9 as final deferral ✓
- CF-4 (BLG-FE-14 filed) → confirmed in scope as EPIC-01 ✓
- CF-5 (BLG-QA-13 filed) → confirmed in scope as EPIC-02 ✓
- CF-6 (scope document at planning time) → scope doc created at planning ✓
- CF-7 (sprint planning to add BLG items to backlog.md) → noted for Sprint Planning Engine ✓

---

## Risk Summary

| RISK-ID | Priority | Status |
|---------|----------|--------|
| RISK-01 | Medium | UX page placement decision needed at sprint planning pre-decisions; flagged below |
| RISK-02 | Low | Mitigated — specs confirmed from v2.7 |
| RISK-03 | Medium | Mitigated — CLAUDE.md §6 checklist in AC for each EPIC-03 story |
| RISK-04 | High | Strategy Rules owner sign-off in-sprint; flagged as Pre-sprint Required Decision |

---

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-04] AI Journal Summarisation — Strategy Rules owner sign-off on implementation scope — confirm no AI output integration into signal/scoring pipeline before sprint planning seal. Required for ST-07 and ST-08 to proceed. Owner: Strategy Rules & System Intent Owner
- [ ] [RISK-01] Market Correlation frontend UX placement — Head of UX & Design to confirm page placement (Analytics vs Portfolio page) for ST-01 before sprint planning seal. Owner: Head of UX & Design (fallback: Analytics page per BLG-FE-14 spec)

---

## Planning Observations

| # | Observation |
|---|-------------|
| 1 | BLG-GOV-08 (engine prompt compression) has been deferred 4 consecutive times. PO has made a final deferral decision to v2.9. If not actioned in v2.9, it should be retired from the backlog at v2.9 planning. |
| 2 | BLG-FEAT-16 (AI Journal Summarisation) introduces the first external LLM API dependency. This is a new operational concern — API key management and failure handling must be tested in staging before deployment. |
| 3 | CF-6 carry-forward resolved: scope document created at planning time (not deferred to post-ship) — confirms the fix from v2.7 closure Obs 1 is effective. |

---

## Next Steps

1. Design Gate (Phase 1.5) — `run design-gate --cycle 2026-04-17__release-v2.8`
2. Sprint Planning — `plan sprint --cycle 2026-04-17__release-v2.8`
   - Pre-sprint required decisions: RISK-04 (Strategy Rules sign-off) and RISK-01 (UX placement) must be resolved before sprint planning seal
3. Sprint Execution — `run sprint --cycle 2026-04-17__release-v2.8`
