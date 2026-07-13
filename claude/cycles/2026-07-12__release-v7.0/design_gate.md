**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-12
**Cycle:** 2026-07-12__release-v7.0

# Design Gate Record — 2026-07-12__release-v7.0

## Gate Status: PASSED

Completed: 2026-07-12
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-SPEC-80) | Grid View badge placement subsection | Design Pre-Approved | Spec debt — documents existing approved v6.2/v6.9 badge visuals for Grid View; no new visual decision | N/A | `docs/specs/frontend/pages/positions.md` v2.1 (locked reference; ST-01 authors the missing subsection during sprint execution) | ✅ Cleared | Head of UX & Design |
| ST-02 (BLG-FE-102) | Grid View RISK OFF badge | Design Pre-Approved | Visual treatment (#1E40AF, "RISK OFF") fully specified in positions.md §Alerts Column; parity implementation only | N/A | `docs/specs/frontend/pages/positions.md` v2.1 | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-FE-97) | Grid View trailing-stop + breach | Design Pre-Approved | positions.md §Trailing Stop Column already has an explicit Grid View placement line (v2.1, "Trailing stop value shown in card summary...") | N/A | `docs/specs/frontend/pages/positions.md` v2.1 | ✅ Cleared | Head of UX & Design |
| ST-04 (BLG-QA-95) | Grid View badge Playwright coverage | Design Not Applicable | Test-only, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 (BLG-FE-104) | Combined-badge differentiation review | Design Required | Explicit design review requested; no combined-render check existed | `docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md` | `docs/specs/frontend/pages/positions.md` v2.2 | ✅ Cleared | Head of UX & Design |
| ST-06 (BLG-SPEC-71) | reports.md Tax Year P&L reconciliation | Design Pre-Approved | Spec debt, no code/UI change | N/A | `docs/specs/frontend/pages/reports.md` v0.6 (locked reference at gate time; ST-06 itself reconciles the section during sprint execution) | ✅ Cleared | Head of UX & Design |
| ST-07 (BLG-BE-50) | trailing_stop_action_rate capture | Design Not Applicable | Backend logging table, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 (BLG-FE-95) | Dashboard/StrategyBenchmark heading contrast | Design Required | No canonical light-theme heading token existed (only secondary-text token, BLG-FE-89) | `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md` | `docs/specs/frontend/pages/dashboard.md` v2.8, `docs/specs/frontend/pages/strategy_benchmark.md` v0.3 | ✅ Cleared | Head of UX & Design |
| ST-09 (BLG-FE-96) | Breach badge colour/label conformance | Design Pre-Approved | positions.md already specifies #EA580C / "⚠ BREACH"; pure conformance fix, no design decision | N/A | `docs/specs/frontend/pages/positions.md` v2.1 | ✅ Cleared | Head of UX & Design |
| ST-10 (BLG-SPEC-73) | Gate Progress Indicator copy | Design Pre-Approved | Wording-only AC, FI-P3-02 exception applies, no visual/colour/layout change | N/A | `docs/specs/frontend/pages/dashboard.md` v2.7 (locked reference at gate time) | ✅ Cleared | Head of UX & Design |
| ST-11 (BLG-BE-51) | Audit-log endpoint filters | Design Not Applicable | Backend-only, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 (BLG-BE-38) | Sector Concentration data join | Design Pre-Approved | Bug fix to existing rendering path (data now populates an already-specified UI state); no UI/spec change | N/A | N/A (Sector Concentration panel spec unaffected) | ✅ Cleared | Head of UX & Design |
| ST-13 (BLG-FEAT-69) | Tax-year P&L CSV export | Design Required | Existing v2.1 spec note ("no button, URL-parameter only") was stale, never implemented, and inconsistent with the shipped PDF button — required a fresh decision | `docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md` | `docs/specs/frontend/pages/reports.md` v0.7 | ✅ Cleared | Head of UX & Design |
| ST-14 (BLG-FEAT-70) | Realized/unrealized P&L split | Design Required | New data column, layout change to Monthly P&L section | `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md` | `docs/specs/frontend/pages/reports.md` v0.7 | ✅ Cleared | Head of UX & Design |
| ST-15 (BLG-FEAT-68) | Position review cadence nudge | Design Required | New UI: days-since-review display, flag state, Mark Reviewed action | `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md` | `docs/specs/frontend/pages/positions.md` v2.2 | ✅ Cleared | Head of UX & Design |

## Blocked Items

None. 15/15 items classified; all 5 Design Required items have approved artefacts and updated specs.

## Notes

- **Stale spec correction (ST-13):** `reports.md` carried a v2.1 (2026-03-18) API Reference note claiming CSV export needs no UI control ("URL parameter only; no button"), attributed at the time to that cycle's own sprint-local "ST-13" — a coincidental sprint-numbering collision with this cycle's ST-13, not the same work item. Confirmed via `backend/routers/` grep that CSV export was never implemented. The note was superseded rather than reused, since it was inconsistent with the shipped PDF button on the same page and would not have produced a discoverable feature.
- **Pre-existing implementation deviation observed (ST-08, StrategyBenchmark.js):** `strategy_benchmark.md` §2 Page Header specifies the shared `PageHeader` component, but the shipped page uses a hand-rolled header (icon + bare `<h1>` + `<p>`). Out of scope for this contrast-only fix — noted in the spec and flagged here as a candidate follow-up (component consolidation), not actioned this cycle.
- **ST-01/ST-02/ST-03/ST-06/ST-09/ST-10/ST-12** are classified Design Pre-Approved on the basis that the visual/wording decision already exists in an approved spec or requires no new UI decision; the stories themselves still author or reconcile spec text/behaviour during sprint execution as documented in their own ACs — this gate does not pre-empt that work, only confirms no separate design-review step is required first.
- No disagreements between Head of UX & Design and Product Owner this cycle; no downgrades from the §6 "default to Design Required" rule were needed for any item.
