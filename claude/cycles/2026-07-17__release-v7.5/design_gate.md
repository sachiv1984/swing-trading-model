**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-17
**Cycle:** 2026-07-17__release-v7.5

# Design Gate Record — 2026-07-17__release-v7.5

## Gate Status: PASSED

Completed: 2026-07-17
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (EPIC-01, BLG-FE-115) | Global Cmd/Ctrl-K command palette | Design Required | New cross-page UI surface, new interaction pattern, new component | `docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md` | `docs/specs/frontend/pages/navigation.md` v1.3 | ✅ Cleared | Head of UX & Design |
| ST-02 (EPIC-02, BLG-FE-116) | User-defined custom price alerts | Design Required | New CRUD UI surface, new data displayed | `docs/design/2026-07-17__release-v7.5/custom-price-alerts/ux_spec.md` | `docs/specs/frontend/pages/notifications.md` v0.4 | ✅ Cleared | Head of UX & Design |
| ST-03 (EPIC-03, BLG-FE-117) | Bulk actions on Watchlist/Trade Plans | Design Required | New multi-select interaction pattern, new component (bulk-action toolbar), applied to two pages | `docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md` | `docs/specs/frontend/pages/watchlist.md` v0.4, `docs/specs/frontend/pages/trade_plan.md` v1.1 | ✅ Cleared | Head of UX & Design |
| ST-04 (EPIC-04, BLG-FE-118) | Saved filter views and calendar view | Design Required | New UI surface (calendar), new interaction (named filter presets), new data displayed (day-level P&L) | `docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md` | `docs/specs/frontend/pages/trade_history.md` v1.11 | ✅ Cleared | Head of UX & Design |

All 4 items classified **Design Required** per §6 default rule (user-facing UI change in every case) — no disagreement between Product Owner and Head of UX & Design; no downgrade requested.

## Blocked Items

None.

## Notes

**Root-cause resolution (RISK-01 / prior `AMD-20260717-01` recurrence risk):** `release_plan.md` §1.4a flagged that all 4 items were pulled from v7.4's sealed sprint scope by amendment `AMD-20260717-01` because their design artefacts did not exist before Design Gate ran, and the structural error was that artefact production had been scheduled as sprint-execution work sequenced *after* the point Design Gate evaluates. This run resolves that structural gap directly: all 4 wireframe/interaction specs and UX decision records were produced as this Design Gate's own STEP 2 work — a precursor step strictly between Release Planning (Phase 1B, already Published) and Sprint Planning (Phase 2, not yet started) — not inside any EPIC's sprint-execution scope. The same root cause is therefore not repeated.

**Grounding:** all 4 artefacts were built directly on top of the existing pre-implementation readiness passes already on file (`docs/specs/blg_fe_115/116/117/118_pre_implementation_readiness_pass.md`, filed 2026-07-16 against ST-04/05/06/07 in the prior cycle) rather than re-deriving technical scope from scratch — each readiness pass's schema, endpoint-pattern, and §13 pre-check findings are referenced as the artefact's explicit dependency and were not altered here (this engine's write scope does not extend to those documents; none required a change).

**RISK-03 (EPIC-02 backend data-model scoping):** the release plan flagged the `price_alerts` backend data model and evaluation-pipeline integration as a design-gate-adjacent precursor risk. This was already fully scoped in `blg_fe_116_pre_implementation_readiness_pass.md` (schema, evaluation-pipeline extension, health-check surfacing, §13 PASS) prior to this cycle — confirmed sufficient and unchanged by this gate. No outstanding backend-scoping gap blocks Sprint Planning for EPIC-02.

**Placement decisions requiring explicit call:** two items had backlog AC text that did not name a specific page/section; Head of UX & Design made an explicit placement decision in each case, confirmed by Product Owner:
- ST-02: new "Custom Price Alerts" section added to the existing Notifications Preferences page (`notifications.md`), below the existing fixed-type Alert Thresholds section — not a new top-level page.
- ST-04: both saved filter presets and the calendar view were placed on Trade History (`trade_history.md`) rather than split across two pages — grounded in Trade History having the richest existing filter set and the calendar's date-sourcing being built on `trade_history.exit_date` (see artefact §1 Placement Decision for full rationale).

No escalations raised. No items require sprint-execution follow-up beyond the standard implementation of what is now specified.
