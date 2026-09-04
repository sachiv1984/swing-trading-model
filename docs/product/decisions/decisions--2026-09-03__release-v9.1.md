Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.1
Cycle: 2026-09-03__release-v9.1
Last Updated: 2026-09-03

## Planning Decisions — v9.1 Frontend Accessibility, Backend Reliability & Governance/Spec Debt Consolidation

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope widened to top of the confirmed ~24–28 day capacity band (final: 27.50 days, 41 items, 5 EPICs) | Explicit user instruction: "use full capacity". No ungated build-and-ship U-item existed to anchor scope (all 15 P1 items gate-conditional), so scope was assembled from the ungated P2/P3 pool across 5 curated themes. | Product Owner | 2026-09-03 |
| `BLG-FEAT-92` reconciled as a sub-scope of `BLG-FEAT-30`, not a separate schedulable item; inherits `BLG-FEAT-30`'s gate condition (screener live ≥60 days AND ≥60 closed trades with attribution) | `BLG-FEAT-92`'s funnel view requires the same screener-attribution linkage `BLG-FEAT-30` is chartered to build; it cannot be implemented independently regardless of its own missing formal Gate field. Resolves the reconciliation ambiguity flagged as overdue at `2026-08-17__release-v8.9` and `2026-08-21__release-v9.0` (3rd consecutive cycle reviewed). | Product Owner (delegated authority) | 2026-09-03 |
| `BLG-GOV-74`, `BLG-GOV-311`, `BLG-SPEC-132` (all 3 passed-provisional-target items named in `backlog_health_20260903.md` §"Items Requiring Product Owner Decision" #2) reassigned into v9.1 scope rather than re-deferred | Each carried a `Provisional-Target` that has already passed without a formal re-defer or kill decision — leaving them unscheduled again would be a 4th silent re-defer of the same pattern `shared_standards.md §6.4` exists to catch for prompt patches. All 3 are low-effort (S or less) and directly actionable. | Product Owner | 2026-09-03 |
| `BLG-GOV-105` (confirmed ✅ CLOSED duplicate of `BLG-GOV-45`) and `BLG-GOV-315` (fix already applied same-day via `execution_prompt.md` v3.71) confirmed not live scope, flagged for `groom backlog` archival | Both are stale-but-resolved backlog entries, not open work. `BLG-GOV-105` requires no further Strategy Rules & System Intent Owner confirmation — its own body text already states the superseding fact. | Product Owner (delegated authority) | 2026-09-03 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (frontend accessibility) sequenced first for design-gate clearance | Only EPIC with observable UI ACs (colour-contrast, accessible-name/label fixes) — `design_gate_required = true` for this cycle; running its design gate first unblocks sprint planning for the remaining backend/QA/governance-only EPICs without a dependency wait. | Product Owner | 2026-09-03 |
| EPIC-02 ST-08 (`BLG-TECH-18`, npm dependency production-build regression) sequenced ahead of the other EPIC-02 items | It is a currently-reproducible build-breaking bug (blocks the quarterly dependency-upgrade cadence policy's own next pass); the other 3 EPIC-02 items are non-blocking hygiene/consolidation work. | Product Owner | 2026-09-03 |

### Accepted risks

None. *(No Accepted Risk escalations raised this cycle — 0 open, 0 deferred escalations.)*

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-09-03__release-v9.1
