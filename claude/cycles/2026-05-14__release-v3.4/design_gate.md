**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-14
**Cycle:** 2026-05-14__release-v3.4

# Design Gate Record — 2026-05-14__release-v3.4

## Gate Status: PASSED

Completed: 2026-05-14
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Position lifecycle state: frontend (IT-01) | Design Pre-Approved | `docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md` | `docs/specs/frontend/pages/positions.md` v1.6 | ✅ Cleared |
| ST-02 | Grace Period Decision Support frontend (IT-02) | Design Pre-Approved | `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md` | `docs/specs/frontend/pages/positions.md` v1.6 | ✅ Cleared |
| ST-03 | Stop Management Workflow frontend (IT-03) | Design Pre-Approved | `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md` | `docs/specs/frontend/pages/positions.md` v1.6 | ✅ Cleared |
| ST-04 | Drawdown-Triggered Review Prompt backend (IT-04) | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Drawdown-Triggered Review Prompt frontend (IT-04) | Design Required | `docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md` v1.0 | `docs/specs/frontend/pages/positions.md` v1.6 | ✅ Cleared |
| ST-06 | Position Concentration Limits backend + frontend (IT-05) | Design Required | `docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md` v1.0 | `docs/specs/frontend/pages/positions.md` v1.6 | ✅ Cleared |
| ST-07 | Research page UK suffix + negative earnings display | Design Pre-Approved | `docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §C, §D` | `docs/specs/frontend/pages/research_view.md` v1.0 | ✅ Cleared |
| ST-08 | Signals page: default to most recent day | Design Pre-Approved | `docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §E` | `docs/specs/frontend/pages/signals.md` v0.2 | ✅ Cleared |
| ST-09 | Watchlist research status indicator | Design Pre-Approved | `docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §F` | `docs/specs/frontend/pages/watchlist.md` v0.3 | ✅ Cleared |
| ST-10 | Trade plan status badges + abandonment UI | Design Pre-Approved | `docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §A, §B` | `docs/specs/frontend/pages/trade_plan.md` v0.3 | ✅ Cleared |
| ST-11 | Research view component library | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-12 | Screener morning routine UX spec | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-13 | trade_plan.md §6.2 spec update + AI journal review cadence | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-14 | Screener accuracy test protocol | Design Not Applicable | N/A | N/A | ✅ Cleared |

## Blocked Items

None.

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| ST-05 (IT-04 frontend) | Drawdown-Triggered Review Prompt UX spec v1.0 | `docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md` | Product Owner 2026-05-14 |
| ST-06 (IT-05 frontend) | Position Concentration Limits Warning UX spec v1.0 | `docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md` | Product Owner 2026-05-14 |

## Frontend Spec Versions Locked for Sprint Planning

| Item(s) | Spec | Version |
|---------|------|---------|
| ST-01, ST-02, ST-03, ST-05, ST-06 | `docs/specs/frontend/pages/positions.md` | v1.6 |
| ST-07 | `docs/specs/frontend/pages/research_view.md` | v1.0 |
| ST-08 | `docs/specs/frontend/pages/signals.md` | v0.2 |
| ST-09 | `docs/specs/frontend/pages/watchlist.md` | v0.3 |
| ST-10 | `docs/specs/frontend/pages/trade_plan.md` | v0.3 |

## Notes

1. **ST-03 artefact path discrepancy:** The backlog slice (stage4_backlog_slice.md) references `docs/design/2026-05-09__release-v3.3/stop-trail-panel/ux_spec.md`. The actual artefact is at `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md`. The content is correct and confirmed by the `positions.md` v1.5 Design Source header. The backlog path reference is a minor documentation error — noted here; no action required before Sprint Planning, but the correct path should be used in PR descriptions and implementation.

2. **EPIC-03 items (ST-07–ST-10):** All four items were fully spec'd in the v3.3 design gate (artefact: `trade-plan-quick-wins/ux_spec.md`) and the corresponding frontend specs updated then. These are deferred implementation items, not new design work. Confirmed Design Pre-Approved.

3. **EPIC-02 dependency cleared:** EPIC-02 (ST-05, ST-06) was explicitly listed in the backlog slice as requiring design gate clearance before Sprint Planning. Both items now have approved UX specs. The EPIC-02 dependency is resolved.
