**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-11
**Cycle:** 2026-04-11__release-v2.6

# Design Gate Record — 2026-04-11__release-v2.6

## Gate Status: PASSED

Completed: 2026-04-11
PMO Lead: confirmed
Head of UX & Design: confirmed

---

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Migrate Reports Performance Tab to FastAPI Backend | Design Pre-Approved | N/A | `docs/specs/frontend/pages/reports.md` v0.2 | ✅ Cleared |
| ST-02 | Wire Signals Dismissal and Position Creation to FastAPI | Design Pre-Approved | N/A | `docs/specs/frontend/pages/signals.md` v0.1 | ✅ Cleared |
| ST-03 | Replace Base44 Cash Balance with GET /cash/summary | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-04 | Fix 4 Pytest Collection Errors | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Add CI Test Runner Workflow | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-06 | Fee Drag Playwright Spec | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-07 | Fee Drag Backend Pytest Unit Tests | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-08 | StatsCard Tooltip Prop | Design Pre-Approved | Tooltip spec in `trade_history.md` v1.5 §Avg Fee Drag | `docs/specs/frontend/pages/trade_history.md` v1.6 | ✅ Cleared |
| ST-09 | Trade History StatsCard Bar Layout (7-Card) | Design Required | `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md` | `docs/specs/frontend/pages/trade_history.md` v1.6 | ✅ Cleared |
| ST-10 | Trade History Column Header Styling | Design Required | `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md` | `docs/specs/frontend/pages/trade_history.md` v1.6 | ✅ Cleared |
| ST-11 | Flexible Column Sorting | Design Required | `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md` | `docs/specs/frontend/pages/trade_history.md` v1.6 | ✅ Cleared |
| ST-12 | execution_prompt.md STEP 5.1 Unpushed-Commit Check | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-13 | Prompt Log Hygiene: §6 Edit Reminders for 3 Engines | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-14 | Upgrade decision_log.md Hard Gate in roadmap_prompt.md | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-15 | Frontend Performance Budget Spec | Design Not Applicable | N/A | N/A | ✅ Cleared |

---

## Blocked Items

None.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| ST-09, ST-10, ST-11 | UX Decision Record — Trade History Polish (v2.6) | `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md` | Product Owner |

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version |
|------|------|---------|
| ST-01 | `docs/specs/frontend/pages/reports.md` | v0.2 |
| ST-02 | `docs/specs/frontend/pages/signals.md` | v0.1 |
| ST-08 | `docs/specs/frontend/pages/trade_history.md` | v1.6 |
| ST-09 | `docs/specs/frontend/pages/trade_history.md` | v1.6 |
| ST-10 | `docs/specs/frontend/pages/trade_history.md` | v1.6 |
| ST-11 | `docs/specs/frontend/pages/trade_history.md` | v1.6 |

---

## Notes

- **ST-08 Design Pre-Approved rationale:** EPIC-03 overview explicitly identifies ST-09, ST-10, ST-11 as requiring Head of UX design decisions before implementation — ST-08 is not listed. The tooltip spec (ⓘ icon placement, hover text, null behaviour) is fully defined in `trade_history.md` v1.5 §Avg Fee Drag. ST-08 implements existing spec; no new design decision required.
- **ST-09 7-card note:** Backlog item (BLG-FE-11) was filed during v2.5 referencing 6 cards. With Avg Fee Drag added in v2.5 ST-09, the bar is now 7 cards. Design artefact addresses 7-card layout.
- **Consolidated artefact:** ST-09, ST-10, ST-11 share one UX decision record. Concerns are distinct (layout, styling, sorting) with no overlap. Product Owner approval covers all three.
- **trade_history.md v1.6:** Head of Specs Team confirmed lifecycle-compliant (Class 1 retained, version 1.5→1.6, Last Updated 2026-04-11). No CLAUDE.md §6 edit checklist applies — `trade_history.md` is a frontend spec, not a governance prompt or OPERATIONAL_GUIDE.
