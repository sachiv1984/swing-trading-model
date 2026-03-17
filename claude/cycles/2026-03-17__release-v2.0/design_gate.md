**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-17
**Cycle:** 2026-03-17__release-v2.0

---

# Design Gate Record — 2026-03-17__release-v2.0

## Gate Status: PASSED

Completed: 2026-03-17
PMO Lead: confirmed
Head of UX & Design: confirmed
Frontend Specs & UX Documentation Owner: confirmed
Head of Specs Team: confirmed — specs lifecycle-compliant

---

## Item Classification Summary

| Item | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Author signals page frontend spec | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-02 | Implement top_n / lookback_days controls | Design Required | UX decision record (inline this gate) | `docs/specs/frontend/pages/signals.md` v0.1 | ✅ Cleared |
| ST-03 | Author tax-year P&L report spec | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-04 | Implement GET /reports/tax-year endpoint | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Frontend: tax-year P&L report view | Design Required | UX decision record (inline this gate) | `docs/specs/frontend/pages/reports.md` v0.1 | ✅ Cleared |
| ST-06 | Spec: alerts endpoint *(deferred v2.1)* | Design Not Applicable | N/A — deferred | N/A | ✅ Cleared |
| ST-07 | Backend: alert rules engine *(deferred)* | Design Not Applicable | N/A — deferred | N/A | ✅ Cleared |
| ST-08 | Backend: notification delivery *(deferred)* | Design Not Applicable | N/A — deferred | N/A | ✅ Cleared |
| ST-09 | Frontend: notification preferences *(deferred)* | Design Not Applicable | N/A — deferred | N/A | ✅ Cleared |
| ST-10 | Frontend: in-app notification feed *(deferred)* | Design Not Applicable | N/A — deferred | N/A | ✅ Cleared |
| ST-11 | QA: notification delivery test scenarios *(deferred)* | Design Not Applicable | N/A — deferred | N/A | ✅ Cleared |
| ST-12 | Fix GET /portfolio missing 4 fields (P1) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-13 | Spec + implement GET /portfolio/prospective-heat | Design Pre-Approved | ProspectiveHeatPanel frontend component already exists | No standalone spec — component already in UI | ✅ Cleared |
| ST-14 | Production Deployment Runbook | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-15 | Positions Table Data Dictionary | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-16 | Database Migration Governance Standard | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-17 | Spec Coverage Inventory | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-20 | CohortAnalysis regression scenario *(stretch)* | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-18 | Roadmap stage document consolidation | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-19 | Ideas register | Design Not Applicable | N/A | N/A | ✅ Cleared |

---

## Blocked Items

None.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Approved by |
|------|----------|-------------|
| ST-02 | UX decision record: Signals page controls (top_n, lookback_days) — layout, defaults, debounce, validation, empty state | Head of UX & Design; Product Owner |
| ST-05 | UX decision record: Tax-year P&L report view — year selector, summary bar, trades table, unrealised card, empty state, scope note, disclaimer | Head of UX & Design; Product Owner |

UX decisions are recorded in-session as part of this gate record. No separate wireframe files produced — interaction decisions are textual and fully specified in the frontend spec documents.

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version |
|------|------|---------|
| ST-02 | `docs/specs/frontend/pages/signals.md` | v0.1 |
| ST-05 | `docs/specs/frontend/pages/reports.md` | v0.1 |

---

## Notes

- EPIC-03 (ST-06–ST-11): All six stories deferred to v2.1 per QA session outcome (DL-003 gate — `qa_notification_planning.md`). Classified as Design Not Applicable for this gate. ST-09 and ST-10 are Design Required items but do not enter this gate; they will require a design gate pass in the v2.1 cycle.
- ST-13 (prospective-heat): ProspectiveHeatPanel is already rendered in the frontend; the backend endpoint is being added behind it. The Design Pre-Approved classification was confirmed by Product Owner — no new UI design is required.
- ST-01 note: ST-01 (signals page spec authoring) is Design Not Applicable at this gate because the spec it produces (signals.md) was authored as the design artefact for ST-02, classified and cleared above. The spec was produced within this design gate session, not during sprint execution.
