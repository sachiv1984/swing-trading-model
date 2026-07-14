Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v7.1
Cycle: 2026-07-14__release-v7.1
Last Updated: 2026-07-14

Superseded by: v7.1 ship — 2026-07-14
Changelog: docs/product/changelog.md#v7-1--nightly-backtest-data-integrity--2026-07-14
Verification report: claude/cycles/2026-07-14__release-v7.1/verification_report.md
Cycle: 2026-07-14__release-v7.1

## Release Scope — v7.1 Nightly Backtest Data Integrity

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Gate nightly backtest ticker eligibility on `ticker_universe.created_at` (point-in-time integrity) — `BLG-BE-59` |
| S2-02 | EPIC-01 | Nightly backtest `total_pnl_gbp` not reproducible night-to-night with zero exits — `BLG-BE-60` |
| S2-03 | EPIC-02 | Table View RISK OFF badge colour/label spec compliance — `BLG-FE-107` |
| S2-04 | EPIC-03 | Position review-cadence nudge: backend/data-integrity hardening pass — `BLG-BE-61` |
| S2-05 | EPIC-03 | Position review-cadence nudge: frontend/QA polish pass — `BLG-QA-106` |
| S2-06 | EPIC-03 | Realized/unrealized P&L split: spec & metrics hardening pass — `BLG-SPEC-83` |
| S2-07 | EPIC-03 | Tax-year P&L CSV export: spec & test hardening pass — `BLG-SPEC-84` |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| `BLG-BE-62` | Idempotent nightly batch-job pattern audit — broader cross-job scope, `Provisional-Target: TBD` | TBD |
| `BLG-SPEC-85` | `trailing_stop_action_rate` spec entry — P3, `Provisional-Target: TBD` | TBD |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-07-14__release-v7.1
