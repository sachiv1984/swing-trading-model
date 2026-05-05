**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.2
**Cycle:** 2026-05-05__release-v3.2
**Last Updated:** 2026-05-05
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cycle Summary — v3.2 Arc 2 Pre-Trade Research & Planning

---

## Release Overview

| Field | Value |
|-------|-------|
| Release | v3.2 |
| Theme | Arc 2 continuation — Pre-Trade Research View, Prospective Heat, Entry Checklist |
| Cycle ID | 2026-05-05__release-v3.2 |
| Plan date | 2026-05-05 |
| Mode | standard |
| Capacity outcome | ⚠ WARN (~15 days estimated vs ~11 days available; phasing mitigates) |
| Design gate required | ✅ Yes — BLG-FE-22 UX spec prerequisite |

---

## Stories (17 total)

| Sprint | EPIC | Stories | Focus |
|--------|------|---------|-------|
| Sprint 1 | EPIC-01 | ST-01 to ST-04 | Pre-Trade Research View frontend (PT-02 + PT-03) |
| Sprint 1 | EPIC-03 | ST-07 to ST-12 | Governance patches + test gap remediation |
| Sprint 2 | EPIC-02 | ST-05, ST-06 | Pre-Trade Entry Checklist (PT-05) |
| Sprint 2 | EPIC-04 | ST-13 to ST-17 | Documentation, security, BLG-GOV-11 |

---

## Key Outcomes

- **Arc 2 primary deliverable:** PT-02 Pre-Trade Research View frontend ships in Sprint 1 (backend was shipped v3.1)
- **Arc 2 secondary deliverable:** PT-03 prospective heat at entry integrated into research view (Sprint 1)
- **Arc 2 tertiary deliverable:** PT-05 Pre-Trade Entry Checklist shipped in Sprint 2
- **Governance debt cleared:** 4 v3.1 deferred OAs (OA-02 to OA-05) actioned as EPIC-03 stories
- **Test debt cleared:** 2 v3.1 test scenario gaps (TEST-GAP-EPIC-01 and TEST-GAP-EPIC-03) resolved
- **Documentation debt cleared:** BLG-FE-16, BLG-FE-21 frontend docs; BLG-GOV-11 (3rd deferral — mandatory)
- **Security:** BLG-SEC-05 (Alpaca credential policy) and BLG-GOV-18 (external API register) actioned

---

## Scope Not Included

| Item | Reason |
|------|--------|
| BLG-FEAT-13 (gated feature rollout) | Deferred v3.3 (2nd consecutive deferral — mandatory next cycle) |
| BLG-FEAT-20 (net-of-costs tracking) | Retargeted to Arc 3/4 data model context |
| BLG-FE-22 (Screener UX spec) | Design gate prerequisite — delivered in Phase 1.5, not a sprint story |

---

## Risks Carried Forward to Sprint Planning

| RISK-ID | Description | Disposition |
|---------|-------------|-------------|
| RISK-01 | BLG-FE-22 UX spec not complete before sprint planning seal | Resolved by: design gate required (see Pre-sprint Required Decisions below) |
| RISK-02 | PT-05 depends on PT-02 merge | Resolved by: Sprint 2 sequencing; Sprint Planning Engine must enforce EPIC-01 merge before EPIC-02 begins |
| RISK-03 | 4 governance prompt patches (ST-07 to ST-10) in same sprint — §6 checklist coordination overhead | Mitigated by: each story confirms §6 checklist in QA evidence log |

---

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] BLG-FE-22 Screener morning routine UX spec — UX spec must be complete and its navigation model adopted into ST-04 acceptance criteria before sprint planning seals — Owner: Head of UX & Design + Frontend Specifications & UX Documentation Owner

---

## Outstanding Actions Entering v3.2

| # | Action | Owner | Status |
|---|--------|-------|--------|
| OA-01 (from v3.1) | v3.1 scope document creation (retroactive) — PMO Lead to create or confirm not required | PMO Lead | Open — before sprint planning |
| OA-02 to OA-05 (from v3.1) | D-01 to D-04 deferred LL items — actioned as ST-07 to ST-10 in EPIC-03 | Head of Specs Team / QA | In-scope v3.2 |
| OA-06 (from v3.1) | Endpoint coverage drift in api_performance_baseline.md — BLG-OPS-13 scope extended | Infra & Ops Owner | BLG-OPS-13 tracking |

---

## Next Steps

1. **Design gate (Phase 1.5):** `run design-gate --cycle 2026-05-05__release-v3.2` — BLG-FE-22 must be delivered as the primary design gate output
2. **Sprint planning (Phase 2):** `plan sprint --cycle 2026-05-05__release-v3.2` — after design gate passes and BLG-FE-22 is complete
3. **Sprint execution (Phase 3):** `run sprint --cycle 2026-05-05__release-v3.2`
