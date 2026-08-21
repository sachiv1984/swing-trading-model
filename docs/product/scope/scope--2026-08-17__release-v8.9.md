Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.9
Cycle: 2026-08-17__release-v8.9
Last Updated: 2026-08-21

Superseded by: v8.9 ship — 2026-08-21
Changelog: docs/product/changelog.md#v8.9
Verification report: claude/cycles/2026-08-17__release-v8.9/verification_report.md
Cycle: 2026-08-17__release-v8.9

## Release Scope — v8.9 Live Risk-Management Correctness & Trade Intelligence Expansion

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Live risk-management correctness (trailing-stop breakeven-floor ratchet fix, stop-field currency-basis display fix, supporting metrics spec entry) |
| S2-02 | EPIC-02 | Trade sizing & post-trade intelligence (correlation/sector-concentration-aware sizing, pre-commit what-if sizing simulator, automated AI post-trade debrief, in-app backtesting engine) |
| S2-03 | EPIC-03 | Backend reliability & performance (trade-plan tags latency investigation, duration-logging verification, audit-trail transaction wrapping, dead-code confirmation) |
| S2-04 | EPIC-04 | Test coverage & QA hardening (job-registration wiring tests, setup_type data-quality decision, service-layer unit test gaps, changelog Playwright coverage) |
| S2-05 | EPIC-05 | Operations & spec currency (local dev venv version-pin enforcement, idea window-summary archival, health-endpoint job-list spec currency) |
| S2-06 | EPIC-06 | Governance process debt closure (state-field ownership registry fix, execution_state.json timestamp drift, Displacement Debt Register wiring, stale roadmap-annotation-marker pruning rule) |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-92` | Own item text names an unresolved scope-overlap dependency on gated `BLG-FEAT-30` requiring explicit PO/Head of Specs Team reconciliation before entering sprint planning. | Next cycle, after reconciliation |
| `BLG-GOV-105` | Already ✅ CLOSED (confirmed duplicate, 2026-07-12); stale entry pending archival. | `groom backlog` archival |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-08-17__release-v8.9
