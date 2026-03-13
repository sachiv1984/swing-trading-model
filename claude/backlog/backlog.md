# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-13 (GROOM-20260313-01: 27 items archived; v1.9 Sprint 1/2 completed items removed from active sections)
**Last rebalance:** 2026-03-06 (cycle 2026-03-06__item-3.4 — DL-006)

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

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low — v2.1 candidate)
**Type:** Observability

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing:
  - Validation run count
  - Failure count by metric and severity
  - Validation duration
- Optional Grafana dashboard.

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format.
- Counters and histograms are correct.

**Target**
- v2.1 or when system becomes multi-user.

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-03 — Slippage Tracking
**Priority:** P2
**Effort:** 1-2 hours

> ⚠️ **Orphan Notice:** No roadmap home or cycle activity detected. Review at next Roadmap Rebalance.

Track and display trade slippage and average slippage summary.

**Indicative Formula**

`(Fill Price - Market Price) / Market Price`

Requires data model update.

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

> ⚠️ **Orphan Notice:** No BLG-ID assigned; no explicit roadmap home or cycle activity. Assign a BLG-ID and roadmap home at next Roadmap Rebalance, or close if addressed.

- [TEST-GAP-EPIC-06] Test scenario coverage gap from 2026-03-02__release-v1.7: QA & Testing Owner to create scenarios per verification_report.md §6 (Test Coverage Assessment). Gaps: no scenarios asserting sharpe_ratio_trade_method presence in /validate/calculations response (14 metrics); no scenario asserting portfolio_endpoints.md field alignment; no scenario asserting holding_days in GET /trades. Target: pre-next sprint on analytics, portfolio, or trade endpoint domains.

---

## 7. Spec & Documentation Debt (Head of Specs Review — 2026-03-03)

Review performed: 2026-03-03 by Head of Specs Team.
Scope: all docs/specs/, docs/reference/, docs/governance/, docs/product/, claude/roadmap/, claude/backlog/, backend/main.py cross-referenced against live contracts.

Items are classified as **DRIFT** (spec and implementation/document diverged) or **GAP** (spec section required but absent).

**Review Summary (updated 2026-03-13 — GROOM-20260313-01)**
- ✅ All 10 active items COMPLETE — D1, D3, D4, D8, D9, G1, G2, G3, G4, G5
- All items resolved in v1.9 Sprint 1 (EPIC-06, ST-14 through ST-19)
- No active spec debt items remaining
- All 10 items archived 2026-03-13 — see `claude/backlog/backlog_archive.md`

---

## 8. New Backlog Items — IW-20260304-01 (Cycle 2026-03-04__item-3.4)

Items promoted to backlog from Idea Intake Window IW-20260304-01 (2026-03-04). Decision log: DL-005.

**Section Summary (updated 2026-03-13 — GROOM-20260313-01)**
- ✅ All items COMPLETE and archived — BLG-NEW-04 shipped v1.9 Sprint 1 (EPIC-06, ST-15); archived 2026-03-13
- Previously archived: BLG-NEW-01–03, 05, 07, 08; BLG-NEW-06 (merged into 4.1b)
- No active items remaining in this section

---

## v1.8 Release Slice — 2026-03-04

<!-- release-plan-marker: RP:v1.8:2026-03-04__release-v1.8 -->

**Cycle:** 2026-03-04__release-v1.8
**Release:** v1.8 — Risk Dashboard
**Planned:** 2026-03-04
**Backlog slice:** `claude/cycles/2026-03-04__release-v1.8/stage4_backlog_slice.md`

Items in v1.8 sprint: EPIC-01 (ST-01–ST-04), EPIC-02 (ST-05–ST-08), EPIC-03 (ST-09–ST-10), EPIC-04 (ST-11–ST-12)

---

## 9. Risk Dashboard Deviation Backlog (from 2026-03-04__release-v1.8)

All 11 deviation backlog items (BLG-RD-01–11) shipped in v1.9 Sprint 1 (EPIC-04, ST-06–ST-10). BLG-RD-08 resolved 2026-03-06 (pre-sprint, Head of Specs Team decision). All items archived 2026-03-13 (GROOM-20260313-01). See `claude/backlog/backlog_archive.md`.

---

## 10. Test Coverage Gaps (from 2026-03-04__release-v1.8)

TEST-GAP-EPIC-01 closed in v1.9 Sprint 1 (ST-11, 2026-03-09) — Playwright mock layer delivered. Archived 2026-03-13 (GROOM-20260313-01). See `claude/backlog/backlog_archive.md`.

---

## 11. New Backlog Items — Cycle 2026-03-06__item-3.4

Items promoted to backlog from IW-20260304-01 parked carry-forwards. Decision log: DL-006.

**Section 11 Summary (updated 2026-03-13 — GROOM-20260313-01)**
- BLG-NEW-09: ✅ COMPLETE (ST-05, Sprint 2); archived 2026-03-13
- BLG-NEW-10: ✅ COMPLETE — Phase 1 (ST-11, Sprint 1) + Phase 2 (ST-12, Sprint 2); archived 2026-03-13
- BLG-NEW-11: ✅ COMPLETE (ST-14); archived 2026-03-13
- BLG-NEW-12: ✅ COMPLETE (ST-13); archived 2026-03-13
- All §11 items archived — no active items remaining

---

## 12. New Backlog Items — Cycle 2026-03-06__release-v1.9

Items raised during sprint execution. Decision authority: Director of Quality (QA infrastructure), Head of Engineering (technical scope).

---

### BLG-FE-01 — Dashboard full-page error + Retry overlay (DEV-EPIC03-ST05-01)
**Priority:** P3 (Low — v1.10 enhancement)
**Type:** Frontend Enhancement
**Owner:** Head of Engineering
**Source:** DEV-EPIC03-ST05-01 filed in docs/specs/frontend/pages/dashboard.md during v1.9 Sprint 2 QA
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10

When all 5 dashboard endpoint queries fail simultaneously, `DashboardHome.js` shows 5 individual card error states rather than a unified full-page overlay with a prominent Retry button as required by spec §5 "All endpoints failed" state. The `handleRetry()` function exists (correctly invalidates all 5 query keys), but all-failed state detection and overlay rendering are not implemented.

**Scope**
- Add all-failed state detection at `DashboardHome.js` level (e.g., all 5 `isError` flags true)
- Render full-page error overlay with Retry button when all-failed state is detected
- Retry button calls `handleRetry()` (already implemented)

**Acceptance Criteria**
- When all 5 dashboard card queries fail, a full-page error overlay with a Retry button is displayed
- Retry button invalidates all 5 query keys and triggers re-fetch
- Individual card error states still render when only some cards fail
- dashboard.md §5 "All endpoints failed" state fully satisfied

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

## 13. Test Coverage Gaps (from 2026-03-06__release-v1.9 Sprint 2)

Scenarios for v1.9 Sprint 2 features were authored in ST-12 (risk_dashboard_scenarios.md v1.3). They have not yet been executed against the live application — manual acceptance review (code inspection) was used for QA sign-off. These items track formal scenario execution.

---

### TEST-GAP-EPIC-01-v1.9 — Execute v1.9 compliance metrics and trade reflection scenarios
**Priority:** P2
**Type:** QA — scenario execution
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-06__release-v1.9 Sprint 2 — STEP 5 coverage gap
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10 (before next sprint touching analytics or trade reflection domain)

11 scenarios authored in risk_dashboard_scenarios.md v1.3 for EPIC-01 features:
- SC-CM-01–04: Compliance metrics (DisciplineComplianceSection display, loading, error states)
- SC-TR-01–07: Trade reflection modal (open, fill, save, pre-populate, skip, char limit)

These scenarios exist but were not run during Sprint 2 QA. QA sign-off was code-inspection only.

**Acceptance Criteria**
- All 11 scenarios (SC-CM-01–04, SC-TR-01–07) executed against live or staging environment
- Results recorded in risk_dashboard_scenarios.md §6 execution log
- Any failures raised as defects before next sprint on these domains

---

### TEST-GAP-EPIC-02-v1.9 — Execute v1.9 cohort analysis and R-multiple distribution scenarios
**Priority:** P2
**Type:** QA — scenario execution
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-06__release-v1.9 Sprint 2 — STEP 5 coverage gap
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10 (before next sprint touching analytics domain)

8 scenarios authored in risk_dashboard_scenarios.md v1.3 for EPIC-02 features:
- SC-CA-01–04: Cohort analysis (period toggle, table display, insufficient-data state)
- SC-RM-01–04: R-multiple distribution (bar chart, stat cards, minimum-trades threshold)

Note: DEV-EPIC02-ST03-01 (P2 — client-side cohort computation) affects SC-CA-01–04 test expectations — expected to pass numerically but source-layer verification requires BLG-TECH-06 fix.

**Acceptance Criteria**
- All 8 scenarios (SC-CA-01–04, SC-RM-01–04) executed against live or staging environment
- SC-CA scenarios note DEV-EPIC02-ST03-01 caveat in results
- Results recorded in risk_dashboard_scenarios.md §6 execution log

---

### TEST-GAP-EPIC-03-v1.9 — Execute v1.9 dashboard homepage scenarios
**Priority:** P2
**Type:** QA — scenario execution
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-06__release-v1.9 Sprint 2 — STEP 5 coverage gap
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10 (before next sprint touching dashboard domain)

10 scenarios authored in risk_dashboard_scenarios.md v1.3 for EPIC-03 features:
- SC-DH-01–10: Dashboard homepage (card layout, data display, error isolation, navigation, responsive)

Note: SC-DH-07 (all-failed full-page retry) will fail until BLG-FE-01 is resolved.

**Acceptance Criteria**
- Scenarios SC-DH-01–06, SC-DH-08–10 executed against live or staging environment (SC-DH-07 deferred until BLG-FE-01 fix)
- Results recorded in risk_dashboard_scenarios.md §6 execution log

---

## Closed Items

Items archived in `claude/backlog/backlog_archive.md`. Listed most recent first.

| Item ID | Title | Shipped | Cycle | Story |
|---------|-------|---------|-------|-------|
| BLG-RD-01 | Entity store fallback masks API error states | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-02 | GracePeriodPanel empty vs error state | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-08 |
| BLG-RD-03 | PositionRiskTable sorted descending | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-04 | Stop Price column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-05 | GRACE badge colour amber instead of blue | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-06 | GBP value at risk absent from HeatGauge | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-10 |
| BLG-RD-07 | Days in Grace column absent | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-09 | ProspectiveHeatPanel missing threshold label | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-09 |
| BLG-RD-10 | US entry prices in USD not GBP | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
| BLG-RD-11 | current_stop in USD for US positions | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-07 |
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
| BLG-FEAT-08 | Basic Compliance Metrics | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | ST-02 |
| BLG-NEW-09 | R-Multiple Distribution Report | v1.9 Sprint 2 | 2026-03-06__release-v1.9 | ST-05 |
| BLG-NEW-10 | Canonical Test Scenario Library (Phase 1+2) | v1.9 Sprint 1+2 | 2026-03-06__release-v1.9 | ST-11, ST-12 |
| BLG-RD-08 | Drawdown data source (RESOLVED pre-sprint) | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-06 investigation |
| TEST-GAP-EPIC-01 | Risk Dashboard scenario execution infrastructure | v1.9 Sprint 1 | 2026-03-06__release-v1.9 | ST-11 |

---

## v1.9 Release Slice — 2026-03-06

<!-- release-plan-marker: RP:v1.9:2026-03-06__release-v1.9 -->

**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9 — User Value & Insight
**Planned:** 2026-03-06
**Backlog slice:** `claude/cycles/2026-03-06__release-v1.9/stage4_backlog_slice.md`

**Sprint 1 (✅ SHIPPED 2026-03-09):** EPIC-04 (ST-06–ST-10), EPIC-05 partial (ST-11, ST-13), EPIC-06 (ST-14–ST-19)
**Sprint 2 (✅ SHIPPED 2026-03-13):** EPIC-01 (ST-01–ST-02), EPIC-02 (ST-03, ST-05), EPIC-03 (ST-04), EPIC-05 partial (ST-12)
