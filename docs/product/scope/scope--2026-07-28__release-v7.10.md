Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v7.10
Cycle: 2026-07-28__release-v7.10
Last Updated: 2026-07-28

## Release Scope — v7.10 Reliability, Security & Contract Hardening

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Fix errors masked as HTTP 200 in portfolio_risk.py |
| S2-02 | EPIC-01 | Extend Alpaca backoff audit (BLG-BE-57) to Yahoo Finance, Gemini, and Claude call sites |
| S2-03 | EPIC-01 | Idempotency key pattern for state-mutating POST endpoints |
| S2-04 | EPIC-01 | Deprecated table read-path audit |
| S2-05 | EPIC-02 | Secrets-scanning pre-commit/CI gate (gitleaks/trufflehog) |
| S2-06 | EPIC-02 | AI rate-limit bypass test |
| S2-07 | EPIC-02 | Rate-limit audit on public-facing endpoints ahead of any future auth changes |
| S2-08 | EPIC-02 | Raw exception text returned in API error responses |
| S2-09 | EPIC-03 | Serve production build for Playwright E2E webServer instead of CRA dev server |
| S2-10 | EPIC-03 | Red Flag Journal auth regression test |
| S2-11 | EPIC-03 | Endpoint test suite coverage audit against all backend/routers/ files |
| S2-12 | EPIC-03 | Consumer-driven contract check: frontend API calls vs documented contracts |
| S2-13 | EPIC-04 | `position_endpoints.md` envelope claim doesn't match live `GET /positions` behaviour |
| S2-14 | EPIC-04 | `GET /positions` undocumented lifecycle fields |
| S2-15 | EPIC-04 | `trade_endpoints.md` JSON example omits documented fields |
| S2-16 | EPIC-04 | OpenAPI contract linter in CI for heading-level drift |
| S2-17 | EPIC-05 | Rewrite calendar.js against the react-day-picker v9+ API |
| S2-18 | EPIC-05 | `SystemStatus.js` `categorizeEndpoint()` missing branches |
| S2-19 | EPIC-05 | Consolidate StrategyBenchmark.js page header onto shared PageHeader component |
| S2-20 | EPIC-05 | Keyboard navigation & focus-order audit |
| S2-21 | EPIC-06 | design_gate_prompt.md does not sync .claude_current_state.json root pointer on gate pass |
| S2-22 | EPIC-06 | Recent-rebalance recency advisory at roadmap STEP -1 |
| S2-23 | EPIC-06 | Same-day scheduled-rebalance cycle_id collision handling |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate NOT MET / §13 determinism pre-clearance not run; standing PO perennial-return disposition | Unscheduled, pending gate clearance |
| Arc 5 pre-entry/compliance-gateway UX cluster (12 items) + BLG-SPEC-35 | Escalated to P1 as a value-judgment priority override 2026-07-27/28, but each item's own gate criteria remain unmet | Unscheduled, pending respective gate clearance |
| Remaining ungated P3 candidates not selected this cycle | Capacity — full band reached by the 23 items above | v7.11 candidate pool |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-07-28__release-v7.10
