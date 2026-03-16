# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-15 (groom backlog GROOM-20260315-01 — 30 items archived; 7 retained)
**Last rebalance:** 2026-03-15 (cycle 2026-03-15__item-5.3 — DL-008)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

These items ensure analytical correctness, validation integrity, and operational safety.
They are not user-facing, but they directly affect trust in outputs and release confidence.

---

### BLG-OPS-01 — Provision development environment
**Priority:** P1 (High — blocks safe QA workflow)
**Type:** Operations / Infrastructure
**Origin:** v1.9 Sprint 2 post-merge QA — raised 2026-03-13
**Target release:** v1.10 (prerequisite before Sprint 1 begins)

The project has no development environment. All QA must currently be performed against the production (`main`) deployment, which means:
- Bug fixes cannot be tested before they land in production
- The merge gate condition "QA sign-off on live app" forces merging to main before a human can test
- Post-merge bug discovery (as occurred in v1.9 Sprint 2) is the only available feedback loop

This creates a structural governance gap: the human Director of Quality sign-off rule requires testing a live running application, but there is no non-production environment to test against.

**Scope**
- Provision a staging/dev environment that tracks `main` (or a designated `staging` branch)
- Environment must run both frontend and backend with real (or seeded) data
- CI/CD pipeline should deploy to staging automatically on merge to `main`
- QA sign-off process updated to use staging URL, not production

**Acceptance Criteria**
- Staging environment accessible via a stable URL
- Deploys automatically when `main` is updated
- Governance process updated: QA sign-off block references staging URL
- Production is not the first place bugs are discovered

---

### BLG-TECH-06 — Fix CohortAnalysis client-side computation (DEV-EPIC02-ST03-01)
**Priority:** P2 (Medium — regression risk)
**Type:** Technical debt / Architecture
**Origin:** DEV-EPIC02-ST03-01 filed in analytics.md v1.4 during v1.9 QA
**Target release:** v1.10

`CohortAnalysis.js` computes cohort groupings and `avg_r` client-side via `buildCohorts()` from a `filteredTrades` prop, instead of calling the canonical `GET /analytics/cohort` endpoint that was implemented in EPIC-02/ST-03. This violates the analytics.md §15 hard rule: all values sourced from backend.

Numerical output is currently correct (same formula), but divergence risk exists if trade data shape changes server-side.

**Scope**
- Refactor `CohortAnalysis.js` to call `api.analytics.cohort(period)` via `useQuery`
- Remove `buildCohorts()` client-side computation logic
- Remove `trades`/`filteredTrades` prop dependency for computation
- Verify rendered output matches backend response field names

**Acceptance Criteria**
- `CohortAnalysis.js` sources all values from `GET /analytics/cohort`
- No client-side R-multiple or cohort aggregation computation
- analytics.md §15 hard rule fully satisfied
- Regression: existing period toggle and table display unchanged

---

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low)
**Type:** Observability
**Target release:** v2.1 (or when system becomes multi-user)

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing:
  - Validation run count
  - Failure count by metric and severity
  - Validation duration
- Optional Grafana dashboard.

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format.
- Counters and histograms are correct.

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-03 — Slippage Tracking
**Priority:** P2
**Target release:** v2.1
**Effort:** Low–Medium (data model update required — schema migration + trade entry capture logic + display)

Track and display trade slippage per trade and as a portfolio average.

**Indicative Formula**

`(Fill Price - Market Price) / Market Price`

Requires data model update — Fill Price must be captured at trade entry (not currently stored). This is the primary pre-work gate: `data_model.md` must define the Fill Price field and migration path before implementation begins.

> **Disposition (2026-03-15 — Product Owner):** Assigned to v2.1 alongside Chart Interactivity and Watchlists. No displacement required — v2.1 is not yet planned. Pull into v2.1 release planning when capacity is available. Orphan status resolved.

---

## 3. Deferred / v2.1 Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 4. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 5. Lifecycle Governance Notes

- This backlog is not canonical and must never override:
  - Strategy rules
  - Metrics definitions
  - API contracts
- Any shipped feature must be backed by:
  - Canonical specification
  - Updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation.

---

## 6. Test Coverage Gaps (from Delivery Verification)

> ⚠️ **Orphan Notice:** No BLG-ID assigned. Assign BLG-ID and target release at v1.10 sprint planning.

- [TEST-GAP-EPIC-06] Test scenario coverage gap from 2026-03-02__release-v1.7: QA & Testing Owner to create scenarios per verification_report.md §6 (Test Coverage Assessment). Gaps: no scenarios asserting sharpe_ratio_trade_method presence in /validate/calculations response (14 metrics); no scenario asserting portfolio_endpoints.md field alignment; no scenario asserting holding_days in GET /trades. **Target release: v1.10** — assign BLG-ID at v1.10 sprint planning.

---

## 7. New Backlog Items — Cycle 2026-03-06__release-v1.9

Items raised during sprint execution. Decision authority: Director of Quality (QA infrastructure), Head of Engineering (technical scope).

---

### BLG-API-01 — Backend API integration tests (FastAPI TestClient)
**Priority:** P2
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** ST-11 decision session 2026-03-09 — Head of Engineering and Director of Quality identified gap
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10

**Problem**
The Playwright mock layer (ST-11) tests frontend rendering behaviour given known API payloads. It does not test whether the backend `GET /portfolio` and `GET /portfolio/prospective-heat` routers return correctly-shaped responses for real database rows. The golden output gate tests pure-math functions; it does not test the router-to-service pipeline end-to-end.

**Scope**
- Add FastAPI `TestClient` integration tests for `GET /portfolio` and `GET /portfolio/prospective-heat` endpoints
- Use fixture data (no live DB required — inject via dependency override or in-memory SQLite)
- Verify: response shape matches `portfolio_endpoints.md` contract, GBP conversion applies for US positions, heat formula produces correct output for known inputs
- Add as a CI step in a new workflow or extend `golden-outputs.yml`

**Acceptance Criteria**
- `TestClient` tests present in `tests/` covering at minimum: portfolio endpoint response shape, US position GBP conversion, heat formula output, prospective-heat endpoint calculation
- Tests are CI-safe (no live DB, no external calls)
- Director of Quality confirms CI step present and passing

**Last Updated:** 2026-03-09

---

## 8. New Backlog Items — Cycle 2026-03-15__item-5.3

Items promoted to backlog from idea pool during roadmap rebalance cycle 2026-03-15__item-5.3.

---

### BLG-NEW-13 — Spec Coverage Inventory
**Priority:** P2 (Medium)
**Type:** Governance / Spec
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260304-02 (IW-20260304-01 — promoted 2026-03-15)
**Cycle added:** 2026-03-15__item-5.3
**Effort:** ~1–2 days (analysis + documentation)
**Target release:** v2.0 (or v1.10 if capacity allows)

Systematic audit of all canonical spec sections (docs/specs/) against implementation coverage. Produces a living inventory identifying which spec sections are tested, which are partially covered, and which have no coverage or implementation verification. Complements BLG-NEW-11 (Canonical Terms Glossary). Creates an actionable gap list for future backlog prioritisation.

**Scope**
- Review all docs/specs/ sections against live implementation and test coverage
- Rate each section: covered / partial / gap
- Cross-reference open backlog items against identified gaps
- Define a review cadence (e.g. per audit cycle or per major release)
- Output: a structured Coverage Inventory document (Class 2 Supporting document)

**Acceptance Criteria**
- Coverage Inventory document produced covering all docs/specs/ sections
- Each spec section rated: covered / partial / gap
- Gap items cross-referenced against open backlog items where possible
- Review cadence defined
- Registered in Specs_Index.md

---

## 9. New Backlog Items — Cycle 2026-03-15__release-v1.10

Items raised during v1.10 sprint execution and QA sign-off.

---

### BLG-BE-01 — GET /portfolio missing 4 required fields (GAP-03 finding)
**Priority:** P1
**Type:** Backend Bug
**Owner:** Head of Engineering
**Source:** GAP-03 staging execution — DoQ sign-off 2026-03-16 (EPIC-03 ST-07)
**Cycle added:** 2026-03-15__release-v1.10
**Target release:** v1.11

**Problem**
`GET /portfolio` does not return `initial_value`, `net_deposits`, `current_drawdown_percent`, or `peak_portfolio_value` in the staging API response. These 4 fields are required by `portfolio_endpoints.md` v1.9.0 (added at v1.8.2 per changelog). The backend implementation is diverged from the spec.

**Evidence**
Staging response (`2026-03-16`) contained only: `cash`, `cash_balance`, `total_value`, `open_positions_value`, `total_pnl`, `last_updated`, `live_fx_rate`, `portfolio_heat_percent`, `position_risks`, `positions`. The 4 fields above were absent.

**Scope**
- Add `initial_value` (portfolio initial capital value in GBP)
- Add `net_deposits` (total deposits minus total withdrawals — cost basis for portfolio-level return)
- Add `current_drawdown_percent` (current value vs all-time peak; default `0.0` when no history)
- Add `peak_portfolio_value` (all-time high of portfolio_history.total_value; default `0.0` when no history)
- Per `portfolio_endpoints.md` §GET /portfolio and §Field Derivation Notes
- Update ST-05 integration tests (`tests/test_portfolio_integration.py`) to assert these 4 fields

**Acceptance Criteria**
- `GET /portfolio` response includes all 4 fields with correct values
- `current_drawdown_percent` and `peak_portfolio_value` default to `0.0` when no portfolio_history exists
- `net_deposits` equals total deposits minus total withdrawals
- ST-05 integration tests extended to assert these fields
- GAP-03 scenario (`docs/testing/v1.7-qa-scenario-gaps.md`) passes on staging

---

## Closed Items

Items archived in `claude/backlog/backlog_archive.md`. Listed most recent first.

| Item ID | Title | Shipped | Cycle | Story |
|---------|-------|---------|-------|-------|
| BLG-FEAT-08 | Basic Compliance Metrics | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | EPIC-03/ST-01 |
| BLG-NEW-09 | R-Multiple Distribution Report | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | EPIC-02/ST-04 |
| BLG-NEW-10 | Canonical Test Scenario Library | v1.9 | 2026-03-06__release-v1.9 | EPIC-05/ST-11, ST-12 |
| BLG-RD-01 | Entity store fallback masks API error states | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-02 | GracePeriodPanel empty vs error state | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-03 | PositionRiskTable sorted descending | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-04 | Stop Price column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-05 | GRACE badge colour amber instead of blue | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-06 | GBP value at risk absent from HeatGauge | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-07 | Days in Grace column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-08 | Drawdown data source resolved | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-06 |
| BLG-RD-09 | ProspectiveHeatPanel missing threshold label | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-10 | US entry prices in USD not GBP | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
| BLG-RD-11 | current_stop in USD for US positions | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
| TEST-GAP-EPIC-01 | Risk Dashboard scenario execution infrastructure gap | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-11 |
| BLG-NEW-04 | AI-Assisted Workflow Governance Policy | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-15 |
| BLG-NEW-11 | Canonical Terms Glossary | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-14 |
| BLG-NEW-12 | Service Layer Test Coverage Standard | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-13 |
| BLG-SPEC-D1 | API Contracts README version frozen | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D3 | GET /market/status undocumented | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-16 |
| BLG-SPEC-D4 | GET /positions/search/tags undocumented | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D8 | System_status_report.md missing header | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-D9 | Broken cross-references to lifecycle guide | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G1 | settings_model.md missing | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-17 |
| BLG-SPEC-G2 | Error Response Standard not defined | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-18 |
| BLG-SPEC-G3 | structured_logging_standards.md not in Specs Index | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G4 | ADR-002 in wrong location | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-SPEC-G5 | validation_system.md owner field non-compliant | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-19 |
| BLG-NEW-08 | Automated OpenAPI Drift Detection in CI | v1.8 | 2026-03-04__release-v1.8 | ST-08 |
| BLG-NEW-07 | Running API Changelog Document | v1.8 | 2026-03-04__release-v1.8 | ST-12 |
| BLG-NEW-05 | Dependency Vulnerability Scanning in CI | v1.8 | 2026-03-04__release-v1.8 | ST-07 |
| BLG-NEW-03 | Define and Document Unavailability Failure Mode | v1.8 | 2026-03-04__release-v1.8 | ST-11 |
| BLG-NEW-02 | Backtest vs Live Stop Reconciliation Report | v1.8 | 2026-03-04__release-v1.8 | ST-06 |
| BLG-NEW-01 | Golden Output Regression Baseline for CI | v1.8 | 2026-03-04__release-v1.8 | ST-05 |
| BLG-SPEC-D7 | openapi.yaml frozen at v1.8.1 | v1.8 | 2026-03-04__release-v1.8 | ST-10 |
| BLG-SPEC-D2 | settings_endpoints.md spec/implementation mismatch | v1.8 | 2026-03-04__release-v1.8 | ST-09 |
| BLG-NEW-06 | Realised vs Unrealised P&L Labelling | N/A | 2026-03-04__item-3.4 | Merged into 4.1b |

---

---

## v1.10 Release Slice — 2026-03-15

<!-- release-plan-marker: RP:v1.10:2026-03-15__release-v1.10 -->

**Cycle:** 2026-03-15__release-v1.10
**Release:** v1.10 — Operations & Quality Foundation
**Planned:** 2026-03-15
**Backlog slice:** `claude/cycles/2026-03-15__release-v1.10/stage4_backlog_slice.md`

Items in v1.10 sprint: EPIC-01 (ST-01–ST-03), EPIC-02 (ST-04), EPIC-03 (ST-05–ST-07)

---

*For delivery history, see `docs/product/changelog.md`.*
*For the active roadmap, see `claude/roadmap/current_roadmap.md`.*
