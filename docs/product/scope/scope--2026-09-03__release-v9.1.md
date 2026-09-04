Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.1
Cycle: 2026-09-03__release-v9.1
Last Updated: 2026-09-03

## Release Scope — v9.1 Frontend Accessibility, Backend Reliability & Governance/Spec Debt Consolidation

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Frontend accessibility & UI consolidation (5 axe-core violation fixes across DashboardHome/TradePlan/Settings, PositionSizingWidget/WhatIfSizingPreview debounce-hook consolidation, keyboard-navigation spec section) |
| S2-02 | EPIC-02 | Backend reliability & technical debt (npm dependency production-build regression fix, fail-open exception logging, sector-lookup consolidation, raw-SQL-out-of-routers extraction) |
| S2-03 | EPIC-03 | QA & test coverage (3 Arc5ComplianceSection Playwright gaps, DEV-* quality trend index, DoD/DoQ severity spot-checks, regression suite runtime budget) |
| S2-04 | EPIC-04 | Governance process debt & overdue dispositions (governance_sync.yml auto-close fix, 3 passed-provisional-target items resolved, recurrence-check false-positive fix, Displacement Debt Register creation, 2 spec-debt doc corrections, Specs_Index.md changelog table) |
| S2-05 | EPIC-05 | Spec & knowledge debt / AI governance register (empty-state/glossary/traceability spec consolidation, canonical AI feature touchpoint register, effort-band and PVR/Skill-Silo metric structuring, terminology definitions) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-92` (Screener-to-trade conversion funnel view) | Reconciled this cycle as a sub-scope of `BLG-FEAT-30` (shares the same screener-attribution linkage) — inherits `BLG-FEAT-30`'s gate (screener live ≥60 days AND ≥60 closed trades with attribution), currently NOT MET. See `decisions--2026-09-03__release-v9.1.md`. | After `BLG-FEAT-30`'s gate clears |
| `BLG-FEAT-73` (SI-02 frontend) | PO disposition (2026-08-17) sets re-check no earlier than 2026-11-09 or 10 new linked `trade_plans`, whichever first. Neither condition met. | Next re-check trigger |
| `BLG-FEAT-74` (PO-05 Replay Mode) | §13 determinism pre-clearance review not yet scheduled or run. | After §13 pre-clearance |
| `BLG-GOV-105` | Already ✅ CLOSED (confirmed duplicate of `BLG-GOV-45`, shipped v4.6); stale entry pending archival, not live scope. 3rd consecutive cycle flagged. | `groom backlog` archival |
| `BLG-GOV-315` | Underlying process-prompt fix already applied same-day (2026-09-03, `execution_prompt.md` v3.70→v3.71); backlog item itself pending archival as a leftover-already-complete entry. | `groom backlog` archival |

Remaining ungated P2/P3 pool not selected (well over 150 items) remains available in `backlog.md` for future release cycles; none were displaced from a committed scope.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-09-03__release-v9.1
