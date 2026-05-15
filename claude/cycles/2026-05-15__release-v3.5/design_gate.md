**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-15
**Cycle:** 2026-05-15__release-v3.5

# Design Gate Record — 2026-05-15__release-v3.5

## Gate Status: PASSED

Completed: 2026-05-15
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

---

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | §13 Compliance Review: Alpaca Paper Trading | Design Not Applicable | Strategy/governance determination doc; no user-visible UI effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | IT-06 Backend: Alpaca Paper Trading Sync Service | Design Not Applicable | Backend service, database, and API endpoint only; no frontend component in this story | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | IT-06 Frontend: Paper Positions Display Panel | Design Required | New UI panel on Positions page showing Alpaca paper account positions; new data displayed; conditional rendering based on env config | `docs/ux_specs/paper-trading/ux_spec.md` v1.0 | `docs/specs/frontend/pages/positions.md` v1.7 | ✅ Cleared | Head of UX & Design |
| ST-04 | BLG-GOV-21: Arc 4 Data Requirements Capture | Design Not Applicable | Documentation-only deliverable; produces a data requirements reference document with no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | PO-01 Backend: Plan vs Reality Calculation Service | Design Not Applicable | Backend service, data model migration, and API endpoint only; no frontend component in this story | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | PO-01 Frontend: Plan vs Reality Comparison View | Design Required | New `PlanVsReality` component in Trade History expandable row; new data surface; conditional rendering for closed trades with trade plan | `docs/ux_specs/plan-vs-reality/ux_spec.md` v1.0 | `docs/specs/frontend/pages/trade_history.md` v1.8 | ✅ Cleared | Head of UX & Design |
| ST-07 | BLG-SPEC-29: Correct grace-period-alert ux_spec.md sessionStorage | Design Pre-Approved | Corrects existing UX spec to match already-shipped implementation (sessionStorage vs localStorage). No implementation change. Locked spec: `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md` | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | BLG-SPEC-30: Correct stop-management-workflow ux_spec.md HTTP verb | Design Pre-Approved | Corrects existing UX spec to match already-shipped implementation (PATCH vs PUT). No implementation change. Locked spec: `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md` | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | BLG-SPEC-31: React Query v5 onSuccess Codebase Scan | Design Not Applicable | Technical codebase scan and potential refactor; no new UI design required | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | BLG-QA-19: Research View Regression Test Protocol | Design Not Applicable | QA documentation only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | BLG-GOV-22: sprint_planning_prompt.md Shared Ownership Patch | Design Not Applicable | Governance prompt edit only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | execution_prompt.md: Deviation Filing Advisory Patches | Design Not Applicable | Governance prompt edit only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Sprint Close / LL Formatting Improvements | Design Not Applicable | Governance prompt edit only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |

---

## Blocked Items

None. All items cleared.

---

## Notes

### ST-03 Conditionality
ST-03 (Paper Positions Display Panel) is conditional on ST-01 yielding a PASS determination. If ST-01 yields FAIL, ST-03 scope is removed in-sprint and this design artefact is not used. The UX spec is created now to unblock sprint planning — no design work will be wasted as it can be deferred to a future cycle if §13 FAIL.

### ST-07 and ST-08 — AC Path Discrepancy
The ACs for ST-07 and ST-08 reference `docs/ux_specs/grace-period-alert/ux_spec.md` and `docs/ux_specs/stop-management-workflow/ux_spec.md` respectively. The actual canonical design artefacts are at:
- ST-07: `docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md`
- ST-08: `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md`

Both files exist and contain the Known Deviations entries (DEV-v3.4-01) that ST-07 and ST-08 will resolve. During execution, the sprint team should update the existing v3.3 design artefacts (not create new files at the `docs/ux_specs/` paths unless a deliberate migration is intended). This discrepancy is recorded here for sprint team awareness — no gate impact as both items are Design Pre-Approved.

### BLG-FE-26 Advisory (from release plan)
BLG-FE-26 (Research page UX review: regime lozenge and font consistency) deferred again per Product Owner decision — not in v3.5 scope. Arc 4/5 design gate target. No gate impact.

### Design Gate Bypass
No bypass requested or granted for this cycle. All Design Required items cleared through full design gate process.
