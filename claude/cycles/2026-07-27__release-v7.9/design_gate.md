**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-27
**Cycle:** 2026-07-27__release-v7.9

# Design Gate Record — 2026-07-27__release-v7.9

## Gate Status: PASSED

Completed: 2026-07-27
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| EPIC-01 / BLG-FEAT-66 | Watchlist staleness and decay review | Design Required | New user-facing "Added" column, stale-state styling, and a new "Keep" action (AC-02/AC-03 are observable UI) | `docs/design/2026-07-27__release-v7.9/watchlist-staleness-review/ux_spec.md` | `docs/specs/frontend/pages/watchlist.md` v0.5 | ✅ Cleared | Head of UX & Design |
| EPIC-02 / BLG-FEAT-67 | Historical sector/regime exposure trend | Design Required | New chart rendering (sector trend, regime timeline) plus an observable insufficient-history state | `docs/design/2026-07-27__release-v7.9/sector-regime-exposure-trend/ux_spec.md` | `docs/specs/frontend/pages/risk_dashboard.md` v0.1.10 | ✅ Cleared | Head of UX & Design |
| EPIC-03 / BLG-SPEC-105 | Formalise trade_plan-to-position FK linkage schema | Design Pre-Approved | Documentation-only addition to `data_model.md`; spec debt, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-04 / BLG-FEAT-85 | Monthly P&L CSV cost-basis reconciliation | Design Pre-Approved | Backend export column addition; no in-app UI rendering | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-05 / BLG-FEAT-87 | "Why is my stop moving" explainer tooltip | Design Required | New observable UI element (tooltip, visible rendering/interaction) | `docs/design/2026-07-27__release-v7.9/trailing-stop-explainer-tooltip/ux_spec.md` | `docs/specs/frontend/pages/positions.md` v2.5 | ✅ Cleared | Head of UX & Design |
| EPIC-06 / BLG-BE-73 | Audit trail for manual position overrides | Design Pre-Approved | Backend audit-log entries only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-07 / BLG-BE-74 | Nightly backtest data-integrity smoke test | Design Not Applicable | CI/CD only, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-08 / BLG-OPS-121 | Staging credential provisioning for SI-02 gate re-checks | Design Not Applicable | Infrastructure/credential provisioning, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-09 / BLG-QA-124 | Shared cross-EPIC smoke-test tagging | Design Not Applicable | CI/process tooling, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-10 / BLG-QA-125 | Pre-commit hook for `test.py` registration check | Design Not Applicable | Tooling only, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-11 / BLG-FE-130 | WCAG contrast checklist addendum for chart colour palettes | Design Not Applicable | Documentation addendum to `design_system.md`; no shipped UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-12 / BLG-OPS-120 | Cost-tag cloud infrastructure spend by EPIC | Design Not Applicable | Infra tagging/reporting, no in-app UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-13 / BLG-FE-129 | Dark-mode AC checklist addendum for Base44 prompt drafts | Design Not Applicable | Process template edit, no shipped UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-14 / BLG-GOV-258 | Displacement debt register | Design Not Applicable | Governance process artefact, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| EPIC-15 / BLG-QA-123 | Visual-regression baseline refresh cadence for Grid View | Design Not Applicable | Cadence definition/process, no shipped UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items (if any)

None. All 15 items cleared.

## Notes

- **Invocation note:** the session command was issued as `run design gate v7.9`, shorthand for the canonical `run design-gate --cycle "2026-07-27__release-v7.9"`. The cycle reference was unambiguous (single active cycle matching v7.9, per `.claude_current_state.json`), so the run proceeded on that basis rather than halting on formatting alone.
- **Placement correction (EPIC-02 / BLG-FEAT-67):** the backlog item's problem statement placed the new trend chart "alongside the existing `SectorHeatMap` ... on the Positions or Reports page." This does not match the shipped codebase — `SectorHeatMap` (`src/components/risk/SectorHeatMap.js`) renders on the Risk Dashboard page (`risk_dashboard.md` §8a), not Positions or Reports; the backlog item also misstated the ship version as v6.2 (actually v6.1, per `risk_dashboard.md` design-source history). Corrected placement to Risk Dashboard §8b at this design gate — see the design artefact §2 and `risk_dashboard.md` §8b placement note for full rationale. Product Owner confirmed the correction; no AC substance changed.
- **Frontend spec files are not §14-tracked governance documents.** `watchlist.md`, `risk_dashboard.md`, and `positions.md` are Class 1/2 Supporting/Canonical Specification documents, not entries in `OPERATIONAL_GUIDE.md` §14's Playbook Governance table (which enumerates only the governance engine prompts themselves). No `claude/system/prompt_change_log.md` entry was made for these three files — that log tracks §14-governed prompt/guide version bumps, and none of the three files appear in that table.
- No disagreements between Product Owner and Head of UX & Design on any item's classification.
