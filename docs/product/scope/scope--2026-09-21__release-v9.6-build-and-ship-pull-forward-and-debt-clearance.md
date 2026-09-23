Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.6
Cycle: 2026-09-21__release-v9.6
Last Updated: 2026-09-23 (post-ship closure — superseded on ship)

Superseded by: v9.6 ship — 2026-09-23
Changelog: docs/product/changelog.md#v96
Verification report: claude/cycles/2026-09-21__release-v9.6/verification_report.md
Cycle: 2026-09-21__release-v9.6

## Release Scope — v9.6 Build-and-Ship Pull-Forward & Full-Capacity Debt Clearance

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Product Features & Frontend Build-and-Ship — "Clone as new plan" on the Trade Plans list, stale-plan marker on the Trade Plans list, CSV export for Screener results and Watchlist, in-app TradeReflection reminder 48h after a trade closes, a named next action in every empty state, one shared number/currency formatting helper migrated across the three highest-traffic tables |
| S2-02 | EPIC-02 | Financial Reporting & Records Integrity — net-vs-gross-of-fees audit of Monthly P&L with a visible NULL-fee count, month-end immutable snapshot of Monthly P&L / the tax-year table with a restatement diff |
| S2-03 | EPIC-03 | Backend & Platform Engineering Debt — ratify and test `calculate_trailing_stop`'s entry-price floor against `strategy_rules.md` §7.2/§7.3, negative-`limit` validation on `GET /backtest-rule-changes/runs`, 500-character truncation in the JSON Lines log formatter, float-vs-Decimal money-arithmetic audit with rounding-boundary golden tests, a shared upstream-call helper with uniform timeout and bounded retry |
| S2-04 | EPIC-04 | Operations & Security Debt — dead-man's-switch alert when nightly-stop-update has not succeeded within 26 hours, GitHub Actions secrets ownership map, synthetic uptime monitor live-fire confirmation, CI-minutes and artifact-storage visibility with explicit retention on the three uploads that lack it |
| S2-05 | EPIC-05 | QA & Test Coverage Debt — quarterly full-suite Playwright re-run against a fresh staging seed, flaky-test disposition addendum to the DoQ checklist, standing regression check for the OpenAPI Drift Detection gate, fix of an unrestored `sys.modules["database"]` swap in a test file |
| S2-06 | EPIC-06 | Spec & Documentation Debt — apply and confirm the DS-17 unique index on the live `positions` table, standalone PO-05 §13 determinism pre-clearance, canonical colour-blind-safe chart palette spec, lightweight ADR log for cross-cutting backend decisions, canonical Sharpe-ratio lookback window |
| S2-07 | EPIC-07 | Governance Process Debt — lapsed-date gate detection in the release-planning scan (and verification of the six items it names), §13 boundary review cadence decision, sprint-capacity band re-baseline decision, fixed-cadence `governance-drift` audit, Claude model deprecation monitoring procedure, sprint-velocity trend chart |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` | Substantively gate-blocked by their own body text (no formal `Gate` field, but each states it may not enter sprint planning yet) | Re-assess once each item's own named re-check condition clears; `BLG-FEAT-74`'s path runs through `BLG-SPEC-160` (in scope, ST-23) |
| `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FEAT-63`, `BLG-FE-84`, `BLG-GOV-140`, `BLG-GOV-141`, `BLG-GOV-142`, `BLG-OPS-88` | Within-sprint date gate (2026-09-24 AI review) — classified conditional per §1.4b, not firm capacity | v9.7 planning, once the review clears or re-gates them |
| `BLG-GOV-335`, `BLG-GOV-336`, `BLG-GOV-337`, `BLG-GOV-326` | Already complete or already satisfied by shipped work — not open scope | Archive at the next `groom backlog` |
| 121 further formally gated/conditional backlog items (131 scanned − 2 cleared − 8 conditional above) | No clearance evidence this cycle (unchanged data-density / AI-adoption / §13-review gates) | Re-assess at next rebalance/release planning |
| 44 further ready P2/P3/P4 items (33.75 estimated days) | Left unselected purely on capacity grounds — including 12 items (4.80 days) tagged `Provisional-Target: v9.6` (`BLG-SPEC-149`–`155`, `BLG-FE-178`/`179`, `BLG-QA-179`/`180`/`181`) | Available for v9.7 |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-09-21__release-v9.6
