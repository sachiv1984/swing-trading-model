# Specs Index (Canonical)

**Owner:** Head of Specs Team
**Purpose:** Single map of canonical product truth
**Audience:** Product, Engineering, Analytics, Strategy
**Status:** Authoritative
**Last Updated:** 2026-05-09

---

## 1. Purpose of This Index

This document defines **where authoritative truth lives** across the system.

It answers:
- Which spec owns which decisions
- How specs relate to one another
- Which document prevails in case of conflict

If two specs disagree, **this index determines the escalation path**.

---

## 2. How to Use This Index

When asking:
- "Where is X defined?"
- "Which rules apply?"
- "Who owns this decision?"
- "Can I change this safely?"

Start here.

This index does **not** restate rules.
It points to the **single canonical source**.

---

## 3. Canonical Spec Domains

### 3.1 Strategy

**What it owns**
- Trading intent
- Risk philosophy
- Position lifecycle rules
- Strategy parameter governance

**Canonical Documents**
- `strategy_rules.md`

**Owner**
- Strategy Rules & System Intent Owner

---

### 3.2 Data Model

**What it owns**
- Meaning of fields (price, stop, P&L, value)
- Currency semantics
- Lifecycle and state representations

**Canonical Documents**
- `data_model.md`
- `data_model/settings_model.md` — Class 1 Canonical, v0.1, Active (created 2026-03-08, ST-17): all settings field names, types, validation rules, defaults, and semantics.

**Owner**
- Data Model & Domain Schema Owner

---

### 3.3 Metrics & Analytics

**What it owns**
- Definitions of performance metrics
- Canonical formulas and tolerances
- Data sufficiency and failure behavior

**Canonical Documents**
- `metrics_definitions.md`

**Owner**
- Metrics Definitions & Analytics Canonical Owner

---

### 3.4 API Contracts

**What it owns**
- Request/response schemas
- Field guarantees and defaults
- Idempotency and error semantics
- Backward compatibility rules

**Canonical Location**
- `docs/specs/api_contracts/`

**Canonical Documents**
- `README.md`
- `conventions.md` — includes §13 Error Response Standard (canonical error envelope, HTTP status mapping)
- `*_endpoints.md`
- `market_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-03-08, ST-16): GET /market/status
- `reports_endpoints.md` — Class 1 Canonical, v0.4, Active (created 2026-03-17, ST-03; updated v0.4 by ST-11 cycle 2026-04-29__release-v3.1): GET /reports/tax-year (UK tax-year P&L) + GET /reports/monthly-pnl (monthly P&L summary). Dual sign-off: Head of Specs Team + Financial Reporting & Records Owner.
- `trade_plan_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-04-30, ST-01, cycle 2026-04-29__release-v3.1): POST /trade-plans, GET /trade-plans/{id}, PUT /trade-plans/{id}, DELETE /trade-plans/{id}, GET /trade-plans/by-position/{position_id}, GET /trade-plans/by-ticker/{ticker}. Sign-off: Sprint Execution Engine (autonomous class).
- `pre_trade_research_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-04-30, ST-04, cycle 2026-04-29__release-v3.1): GET /research/{ticker} — aggregates signal, regime, sector, screener, earnings (all sub-sources null-safe). Sign-off: Sprint Execution Engine (autonomous class).
- `earnings_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-04-30, ST-07, cycle 2026-04-29__release-v3.1): GET /earnings/{ticker} — upcoming earnings date via yfinance; proximity flag. Sign-off: Sprint Execution Engine (autonomous class).
- `alerts_endpoints.md` — Class 1 Canonical, v0.3, Active (created 2026-03-20, ST-02; updated v0.3 2026-03-24, ST-05): Alert rules CRUD, alert evaluation, notification feed, notification preferences, alert history (GET /alerts/history). Architecture: FastAPI BackgroundTasks per ADR-003. Sign-off: Head of Specs Team (2026-03-20).
- `digest_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-04-03, ST-08, cycle 2026-03-31__release-v2.4): GET /digest/weekly — 7-day trading digest (realised P&L, alert activity, compliance trend, staleness summary). Deterministic data fields only. Sign-off: QA Lead + DoQ (2026-04-01/03).
- `health_endpoints.md` — Class 1 Canonical, v1.3, Active (created 2026-03-18; updated v1.1 by ST-07 cycle 2026-03-24__release-v2.3; updated v1.2 by ST-08 adding GET /health/database; updated v1.3 by ST-08/ST-09 cycle 2026-04-25__release-v3.0 adding external_apis + ai_journal sections to GET /health): GET /health + GET /health/database operational health check endpoints. Sign-off: Head of Specs Team (v1.3, 2026-04-26).
- `analytics_endpoints.md` — Class 1 Canonical, v2.1.0, Active (updated 2026-04-15, ST-08, cycle 2026-04-13__release-v2.7): GET /analytics/market-correlation (Pearson correlation vs benchmark, TTL-cached). Sign-off: Head of Specs Team.
- `signal_endpoints.md` — Class 1 Canonical, v1.1, Active (updated 2026-04-15, ST-09, cycle 2026-04-13__release-v2.7): POST /signals/generate — added 4 supplementary display-only indicator fields (relative_strength_pct, week52_high_proximity_pct, avg_daily_volume_20d, price_vs_50d_ma). §13 COMPLIANT (display-only). Sign-off: Strategy Rules Owner.
- `ai_endpoints.md` — Class 1 Canonical, v1.0, Active (created 2026-04-18, ST-07, cycle 2026-04-17__release-v2.8): POST /ai/journal-summary — LLM-based journal entry summarisation; Anthropic API; graceful failure returns HTTP 200 with summary:null; display-only; SRB-v1.7 conditionally compliant. Sign-off: Sprint Execution Engine (autonomous class); DoQ EPIC-level Director of Quality 2026-04-20.
- `ticker_universe_api_contract.md` — Class 2 Canonical (created 2026-04-25, ST-01, cycle 2026-04-25__release-v3.0): GET /ticker-universe, POST /ticker-universe, DELETE /ticker-universe/{ticker}; seed data contract. Sign-off: Sprint Execution Engine (autonomous class).
- `screener_api_contract.md` — Class 2 Canonical (created 2026-04-23 v2.9; implementation delivered 2026-04-25 v3.0 ST-04): GET /screener/results, POST /screener/run; request/response schemas, pagination, error codes.
- `alpaca_integration_contract.md` — Class 2 Canonical (created 2026-04-23 v2.9 ST-02): Alpaca Markets API contract for OHLCV bars and News endpoints; rate limits, error codes, fallback strategy, API version pin.
- `api_changelog.md` — *Running changelog; must be updated with every contract version increment*

**Supporting Reference**
- `docs/reference/openapi.yaml` — *Supporting reference only; must not diverge from canonical contracts*

**Owner**
- API Contracts & Documentation Owner

**Enforcement**
- Any pull request that changes canonical API contracts or backend API behavior **must** be reviewed inline against:
  - Canonical Markdown contracts **and**
  - `docs/reference/openapi.yaml`
- Approval is blocked if OpenAPI alignment is skipped for contract-affecting changes.

---

### 3.4b Arc 1 Screener Specifications

**What it owns**
- Screener result record schema and field semantics
- Screener filter ordering and gate logic
- Market routing rules (US/UK data sources)
- Screener run parameter logging requirements

**Canonical Documents**
- `screener_results_schema.md` — Class 2 Canonical, v1.0, Active (created 2026-04-23, ST-01, cycle 2026-04-22__release-v2.9): screener output fields, filter ordering, market routing, logging requirement. References `claude/strategy/strategy_rules.md §11` as parameter source. Sign-off: Head of Specs Team (autonomous class, 2026-04-23).
- `api_contracts/alpaca_integration_contract.md` — Class 2 Canonical (created 2026-04-23, ST-02): Alpaca Markets API contract for OHLCV bars and News endpoints; rate limits, error codes, fallback strategy, API version pin.
- `api_contracts/screener_api_contract.md` — Class 2 Canonical (created 2026-04-23, ST-03): Internal screener API (`GET /screener/results`, `POST /screener/run`); request/response schemas, pagination, error codes.
- `frontend/pages/screener_results.md` — Class 2 (created 2026-04-23, ST-04, cycle 2026-04-22__release-v2.9): Screener results page UX spec; column layout, sort/filter, data freshness indicator, empty states, watchlist promotion flow, progressive loading. DEV-01 P3 (news panel DS-02 deferred) resolved in v3.0 ST-07 (BLG-FE-18 delivered 2026-04-27).

**Owner**
- Head of Specs Team (schema) + API Contracts & Documentation Owner (contracts) + Frontend Specifications & UX Documentation Owner (UX spec)

---

### 3.5 Frontend & UX Semantics

**What it owns**
- User-visible meanings and mental models
- Page-level user goals, states, and flows
- Reusable UI component behavior
- Cross-cutting UX patterns
- Visual and interaction consistency

**Canonical Location**
- `specs/frontend/`

**Canonical Documents**
- `frontend/README.md`
- `frontend/design_system.md`
- Page, component, and pattern specifications

**Owner**
- Frontend Specifications & UX Documentation Owner

---

### 3.5b Observability & Logging

**What it owns**
- Structured log format standards
- Log levels and usage policy
- Correlation ID generation and propagation scheme
- Async failure observability approach

**Canonical Documents**
- `docs/specs/structured_logging_standards.md` — Class 1 Canonical Specification, v0.1.0, Active (created 2026-03-02, EPIC-04)

**Owner**
- Head of Engineering

---

### 3.6 Glossary (System-Level Reference)

**What it owns**
- Shared terminology used across specs
- Cross-domain language consistency
- Canonical meanings of commonly referenced terms

**Reference Document**
- `docs/reference/glossary.md` — Class 2 Supporting, v1.1, Active (updated 2026-03-08, ST-14): lifecycle-compliant header; terms added: portfolio heat, stop distance, cohort, journal completion rate, stop-based exit rate

**Authority**
- Language only — canonical definitions, formulas, and rules live in domain specs

**Owner**
- Head of Specs Team

**Notes**
- The glossary must not introduce new behavior or override domain specifications
- In case of conflict, the relevant domain canonical spec prevails

---

## 4. Conflict Resolution Order

In case of conflict, precedence is resolved in the following order:

1. **Specs Index**
2. Domain Canonical Spec
3. Supporting Specs
4. Reference Artifacts (e.g. OpenAPI, Glossary)
5. Code
6. UI behavior
7. Tribal knowledge

No downstream system may override upstream intent.

---

## 5. Change Governance & Enforcement

- Changes to **domain canonical specs** require domain owner approval
- Changes affecting multiple domains require Head of Specs Team review
- **Supporting reference artifacts must be reviewed inline with their canonical specs**
- Silent divergence between specs and behavior is treated as a **system bug**
- All documentation must comply with the lifecycle rules defined in:
  - `claude/charter/document_lifecycle_guide.md`

---

## 6. Pending Spec Work — Named Owner Assignments

This section tracks canonical spec gaps that have been identified but not yet filled. Items here block the features or releases noted. No feature may enter pre-alignment until its upstream spec gap is closed.

---

### 6.1 Settings Canonical Specification *(v1.6.1 pre-work gate)*

**Status:** RESOLVED — 2026-03-09 (v1.9 Sprint 1, ST-17). See §3.2 for registration.
**Backlog item:** BLG-SPEC-G1 — COMPLETE
**Resolved by:** `docs/specs/data_model/settings_model.md` Class 1 Canonical v0.1, Active — created 2026-03-08. All settings field names, types, validation rules, defaults, and semantics. Registered in §3.2 above. Cross-referenced from `settings_endpoints.md`.

~~Gap description: Settings behaviour was defined only within `settings_endpoints.md`. No standalone canonical document owned the settings model independently of the API layer.~~

---

### 6.2 Error Response Standard *(v1.6.1 pre-work gate)*

**Status:** RESOLVED — 2026-03-09 (v1.9 Sprint 1, ST-18). See §3.4 for registration.
**Backlog item:** BLG-SPEC-G2 — COMPLETE
**Resolved by:** `docs/specs/api_contracts/conventions.md` §13 Error Response Standard added — canonical error envelope shape, all error codes, HTTP status mapping, rule distinguishing HTTP 400 (malformed input) from HTTP 200 with `valid: false` (business rule failure). Registered in §3.4 above.

~~Gap description: Error response shapes were partially covered but not canonically defined for all failure modes.~~

---

### 6.3 GET /portfolio/prospective-heat endpoint — spec and implementation gap

**Status:** RESOLVED — 2026-03-17 (v2.0 Sprint, ST-13, cycle 2026-03-17__release-v2.0)
**Deviation:** DEV-ST05-01 (P3) — v1.10 sprint execution
**Backlog item:** BLG-BE-02 (P3) — COMPLETE
**Owner:** Head of Engineering + Head of Specs Team
**Resolution:** ST-13 (v2.0 EPIC-04) spec authored in `portfolio_endpoints.md v2.0.0 §GET /portfolio/prospective-heat`; endpoint implemented in backend; `@unittest.skip` removed from `TestProspectiveHeat`; all integration tests pass. Commit 279e832.

~~`GET /portfolio/prospective-heat` endpoint is not defined in `docs/specs/api_contracts/portfolio_endpoints.md` and has no backend implementation. Referenced by the ProspectiveHeatPanel frontend component. Integration tests written in `tests/test_portfolio_integration.py` are currently skipped (`@unittest.skip`) pending spec authoring.~~

---

## 7. Open Compliance Issues

This section records known lifecycle or governance compliance gaps that have been identified and are pending resolution. Items here do not block current work but must be resolved by the owner before the document is next updated.

---

### 7.1 `docs/operations/validation_system.md` — Owner field non-compliant

**Identified:** 2026-02-21
**Status:** RESOLVED — 2026-03-09 (v1.9 Sprint 1, ST-19)
**Backlog item:** BLG-SPEC-G5 — COMPLETE
**Resolution:** `Owner: Platform Team` updated to a named governance role per `claude/charter/document_lifecycle_guide.md §7`. Resolved by Infrastructure & Operations Documentation Owner in ST-19.

---

### 7.2 `GET /portfolio` — 4 required fields missing from API response vs `portfolio_endpoints.md`

**Identified:** 2026-03-16 (GAP-03 staging execution — v1.10 sprint QA)
**Status:** RESOLVED — 2026-03-17 (v2.0 Sprint, ST-12)
**Backlog item:** BLG-BE-01 (P1) — COMPLETE
**Owner:** Head of Engineering
**Resolution:** ST-12 (v2.0) added `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value` to `GET /portfolio` response. GAP-03 scenario passes. Commit 04ed5e8.

---

## 7b. Spec Dependency Map

The Spec Dependency Map is a point-in-time reference document mapping all canonical spec cross-references. Produced in v2.7 (ST-10, EPIC-05).

- `docs/specs/spec_dependency_map.md` — Class 4 Planning Document (read-only reference), v1.0, Active (created 2026-04-16, ST-10, cycle 2026-04-13__release-v2.7). Head of Specs Team sign-off on completeness at authoring time. Explicit staleness acknowledgement in document header.

---

## 8. Coverage Inventory

The Coverage Inventory is the authoritative cross-domain record of spec-to-implementation coverage, lifecycle compliance status, and open documentation gaps. It is refreshed every 3 cycles (at `run audit`) and at the start of each major release.

- `docs/specs/spec_coverage_inventory.md` — Class 3 Operational Record, v1.0, Filed 2026-03-17 (ST-17, EPIC-05). 38 documents audited; 7 actions identified.

---

## 9. Test Coverage Gaps — v2.1 (2026-03-18__release-v2.1)

Identified during delivery verification (verification_report.md §6 — TSG-v21-01 through TSG-v21-03). All three gaps have backlog items and are tracked for resolution before the next sprint touching the relevant domain.

### 9.1 TSG-v21-01 — EPIC-02: notifications_scenarios.md not formally executed

**Identified:** 2026-03-21 (delivery verification 2026-03-18__release-v2.1)
**Status:** RESOLVED — 2026-03-24 (v2.2, ST-09, cycle 2026-03-21__release-v2.2)
**Owner:** QA & Testing Owner
**Gap:** `docs/testing/notifications_scenarios.md` (SC-NOTIF-01 through SC-NOTIF-08) exists but was not formally executed and referenced in `qa_evidence_EPIC-02.md`. Remaining 3 alert types require test data with open positions.
**Resolution:** SC-NOTIF-01 through SC-NOTIF-08 executed on staging; 9 Playwright tests pass; results recorded in `qa_evidence_EPIC-04.md` (ST-09). Backlog item TEST-GAP-EPIC-02 closed.

### 9.2 TSG-v21-02 — EPIC-03: no watchlist test scenario file exists

**Identified:** 2026-03-21 (delivery verification 2026-03-18__release-v2.1)
**Status:** RESOLVED — 2026-03-24 (v2.2, ST-10, cycle 2026-03-21__release-v2.2)
**Owner:** QA & Testing Owner
**Gap:** No test scenario file exists for the watchlist feature (EPIC-03, ST-08/09/10). Spec refs: `docs/specs/api_contracts/watchlist_endpoints.md`, `docs/specs/frontend/pages/watchlist.md`.
**Resolution:** `docs/testing/watchlist_scenarios.md` created covering SC-WATCH-01 through SC-WATCH-06 (including deferred ST-10 AC-6 sort order). Backlog item TEST-GAP-EPIC-03 closed.

### 9.3 TSG-v21-03 — EPIC-05: no slippage tracking test scenarios exist

**Identified:** 2026-03-21 (delivery verification 2026-03-18__release-v2.1)
**Status:** RESOLVED — 2026-04-03 (v2.4, ST-12, cycle 2026-03-31__release-v2.4)
**Owner:** QA & Testing Owner
**Gap:** No scenario file covers slippage tracking (ST-14). Spec ref: `docs/specs/frontend/pages/trade_history.md`.
**Resolution:** `docs/testing/slippage_scenarios.md` created covering SC-SLIP-01 through SC-SLIP-04 + SC-SLIP-05/06; Playwright spec `tests/e2e/slippage-tracking.spec.js`; manual runbook v1.1; SC-SLIP-01 staging execution complete 2026-04-02 (all 6 checks Pass). Backlog item TEST-GAP-EPIC-05-SLIP closed.

---

## 10. Test Coverage Gaps — v2.2 (2026-03-21__release-v2.2)

Identified during delivery verification (verification_report.md §6 — TSG-v22-01 through TSG-v22-03). Gaps are tracked for resolution per stated disposition.

### 10.1 TSG-v22-01 — EPIC-01: no scenario for API key authentication

**Identified:** 2026-03-24 (delivery verification 2026-03-21__release-v2.2)
**Status:** Open — backlog item BLG-QA-01 Phase 4
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Gap:** No automated test scenario covers X-API-Key authentication (401 path, frontend header injection, exempt endpoints). Core security control; zero scenario coverage. Manual acceptance only at ship.
**Required action:** Add API auth integration tests (401 path, valid key, exempt endpoints) to CI as part of BLG-QA-01 Phase 4.
**Resolution target:** BLG-QA-01 Phase 4 (Playwright E2E automation cycle)

### 10.2 TSG-v22-02 — EPIC-03: no scenario for GET /health operational health response schema

**Identified:** 2026-03-24 (delivery verification 2026-03-21__release-v2.2)
**Status:** Partially resolved — health_endpoints.md updated to v1.2 (ST-07/ST-08, cycle 2026-03-24__release-v2.3). Automated test scenario SC-HEALTH-01 not yet created. Gap remains for schema validation.
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Gap:** Automated test for GET /health and GET /health/database response schemas not yet in CI.
**Required action:** Add SC-HEALTH-01 scenario in a future cycle.
**Resolution target:** v2.6 (not addressed in v2.4 or v2.5)

### 10.3 TSG-v23-01 — EPIC-02: R-Multiple chart visual scenarios staging-blocked (BLG-BE-04)

**Identified:** 2026-03-30 (delivery verification 2026-03-24__release-v2.3)
**Status:** Blocker resolved — scenarios now executable (pending QA execution)
**Owner:** QA & Testing Owner
**Gap:** V-CHART-05a/b/c scenarios require `stop_price` field in `/trades` API response. BLG-BE-04 (stop_price absent from trade_history) blocked these 3 R-Multiple visual scenarios.
**Update (2026-04-03):** BLG-BE-04 resolved by ST-03 in cycle 2026-03-31__release-v2.4. `stop_price` field now present on analytics trade endpoint response. V-CHART-05a/b/c are now executable against staging. QA & Testing Owner to schedule execution in v2.5 cycle.
**Update (2026-04-10):** V-CHART-05a/b/c not executed in v2.5 — no story scheduled for this in the v2.5 backlog slice. Gap carries forward.
**Required action:** QA & Testing Owner to execute V-CHART-05a/b/c on staging against live deployment.
**Resolution target:** v2.6

### 10.4 TSG-v24-01 — EPIC-01: no test scenarios for backend correctness fixes

**Identified:** 2026-04-03 (delivery verification 2026-03-31__release-v2.4)
**Status:** RESOLVED — 2026-04-10 (v2.5, ST-13, cycle 2026-04-05__release-v2.5)
**Owner:** QA & Testing Owner
**Gap:** EPIC-01 shipped three backend correctness fixes (ST-01 ATR conversion, ST-02 notification deduplication, ST-03 stop_price join) with no automated test scenarios. These are correctness-critical behaviours.
**Resolution:** SC-ATR-01, SC-DEDUP-01, SC-DEDUP-02, SC-STOP-01 authored and filed in `docs/testing/atr_scenarios.md`, `docs/testing/dedup_scenarios.md`, `docs/testing/stop_price_scenarios.md`. Backlog item TEST-GAP-EPIC-01-v24 closed.

---

## 11. Test Coverage Gaps — v2.5 (2026-04-05__release-v2.5)

Identified during delivery verification (verification_report.md §6 — TSG-V25-01 through TSG-V25-02).

### 11.1 TSG-V25-01 — EPIC-01 test scenarios listed but not applicable to EPIC-01 v2.5 AC

**Identified:** 2026-04-10 (delivery verification 2026-04-05__release-v2.5)
**Status:** Closed — not_applicable
**Owner:** QA & Testing Owner
**Assessment:** ATR/dedup/stop_price scenarios (SC-ATR-01, SC-DEDUP-01/02, SC-STOP-01) were listed under EPIC-01 test_scenarios in execution_state.json but cover v2.4 algorithmic correctness AC, not v2.5 endpoint availability AC. Correctly classified not_applicable at verification. No gap.

### 11.2 TSG-V25-02 — Fee drag Playwright spec not authored for v2.5 Trade History

**Identified:** 2026-04-10 (delivery verification 2026-04-05__release-v2.5)
**Status:** Open — backlog item BLG-QA-07
**Owner:** QA & Testing Owner
**Gap:** ST-09 delivered the fee drag metric (column + StatsCard) on Trade History. No Playwright spec exists for SC-FEE-01 through SC-FEE-04 (`docs/testing/fee-drag-scenarios.md`). Trade History has `slippage-tracking.spec.js` as a model.
**Required action:** Author `tests/e2e/fee-drag-trade-history.spec.js` covering SC-FEE-01–SC-FEE-04. See BLG-QA-07 for scope.
**Resolution target:** v2.6

---

## 13. Test Coverage Gaps — v2.7 (2026-04-13__release-v2.7)

Identified during delivery verification (verification_report.md §6 — TSG-v27-01).

### 13.1 TSG-v27-01 — EPIC-04: no test scenarios for market correlation or supplementary indicator fields

**Identified:** 2026-04-16 (delivery verification 2026-04-13__release-v2.7)
**Status:** RESOLVED — 2026-04-20 (v2.8, ST-02/ST-03, cycle 2026-04-17__release-v2.8)
**Owner:** QA & Testing Owner
**Gap:** EPIC-04 registered two legacy scenario files (`docs/testing/analytics_scenarios.md` v1.0 from 2026-03-17, `docs/testing/signals_scenarios.md` v1.0 from 2026-03-18) that predate v2.7 and cover different functionality. No scenarios exist for `GET /analytics/market-correlation` (ST-08) or the four new supplementary indicator fields on `POST /signals/generate` (ST-09).
**Resolution:** SC-CORR-01–04 added to analytics_scenarios.md v1.1 (ST-02); SC-SIG-IND-01–02 added to signals_scenarios.md v1.1 (ST-03). BLG-QA-13 closed.

---

## 14. Test Coverage Gaps — v2.8 (2026-04-17__release-v2.8)

Identified during delivery verification (verification_report.md §6 — TSG-v28-01).

### 14.1 TSG-v28-01 — EPIC-04: no test scenarios for AI Journal Summarisation

**Identified:** 2026-04-20 (delivery verification 2026-04-17__release-v2.8)
**Status:** ✅ Resolved — 2026-04-24 (cycle 2026-04-22__release-v2.9, ST-15)
**Owner:** QA & Testing Owner
**Gap:** EPIC-04 shipped with no test scenario documentation in `docs/testing/`. POST /ai/journal-summary graceful LLM failure path and AI Journal Summary frontend behaviours (collapsed by default, non-dismissible disclaimer, 4 states) have no formal scenario coverage.
**Resolution:** `docs/testing/ai_scenarios.md` created by ST-15 (cycle 2026-04-22__release-v2.9) with 4 scenarios covering happy path, graceful LLM failure, collapsed by default, and disclaimer always visible. TEST-GAP-EPIC-04 closed.

---

## 15. Test Coverage Gaps — v2.9 (2026-04-22__release-v2.9)

Identified during delivery verification (verification_report.md §6 — TSG-v29-01, TSG-v29-02).

### 15.1 TSG-v29-02 — EPIC-04: no unit tests for ai_audit_service.py

**Identified:** 2026-04-24 (delivery verification 2026-04-22__release-v2.9)
**Status:** ✅ RESOLVED — 2026-04-26 (v3.0, ST-10, cycle 2026-04-25__release-v3.0)
**Owner:** QA & Testing Owner
**Gap:** `backend/services/ai_audit_service.py` (shipped v2.9 ST-14) has no unit tests.
**Resolution:** ST-10 (v3.0 EPIC-03) created `tests/test_ai_audit_service.py` with 12 unit tests covering `ensure_ai_audit_table`, `log_ai_summary_run`, and `query_audit_log`. All tests pass in CI. TEST-GAP-ST14 closed.

---

---

## 16. Test Coverage Gaps — v3.0 (2026-04-25__release-v3.0)

Identified during delivery verification (verification_report.md §6 — TSG-v30-01).

### 16.1 TSG-v30-01 — EPIC-02/03: test_scenarios field not populated in execution_state.json

**Identified:** 2026-04-27 (delivery verification 2026-04-25__release-v3.0)
**Status:** Not applicable — functional E2E and unit test coverage confirmed in CI
**Owner:** QA & Testing Owner
**Assessment:** EPIC-02 and EPIC-03 `test_scenarios` fields not populated during mid-sprint reclassification from `delegated_frontend` to `autonomous`. All relevant Playwright E2E specs (screener.spec.js, visual-snapshots.spec.js, keyboard-shortcuts.spec.js) and unit test files (test_health_extensions.py, test_ai_audit_service.py) ran and passed in CI. Administrative gap only — no functional AC coverage missing. No backlog item required. Root cause addressed as deferred process improvement to execution_prompt.md §3.1.A.

---

## 17. Test Coverage Gaps — v3.1 (2026-04-29__release-v3.1)

Identified during delivery verification (verification_report.md §6 — TSG-v31-01 through TSG-v31-04).

### 17.1 TSG-v31-01 — EPIC-01: trade-plan.spec.js not registered in test_scenarios; backend CRUD integration scenarios absent

**Identified:** 2026-05-05 (delivery verification 2026-04-29__release-v3.1)
**Status:** ✅ Resolved — 2026-05-08 (post-ship closure v3.2 / ST-11)
**Owner:** QA & Testing Owner
**Gap:** `tests/e2e/trade-plan.spec.js` (SC-TP-01–07) was created during EPIC-01 delivery but not registered in `execution_state.json test_scenarios`. Backend CRUD integration test scenarios for `/trade-plans` endpoints also warranted beyond the existing smoke test.
**Resolution:** ST-11 (EPIC-03, v3.2) registered `tests/e2e/trade-plan.spec.js` in `test_scenarios` (SC-TP-01–07, 8 tests). DEL-20260506-01 confirmed completed by Director of Quality 2026-05-06. TEST-GAP-EPIC-01 closed. Backlog item closed.

### 17.2 TSG-v31-02 — EPIC-02: no Playwright coverage for GET /research/{ticker}

**Identified:** 2026-05-05 (delivery verification 2026-04-29__release-v3.1)
**Status:** ✅ Resolved — 2026-05-08 (post-ship closure v3.2 / EPIC-01 delivery)
**Owner:** QA & Testing Owner
**Assessment:** Pre-Trade Research View frontend deferred to v3.2. Backend aggregation endpoint covered by smoke test (test.py 49 entries).
**Resolution:** PT-02 frontend (EPIC-01, v3.2) delivered `tests/e2e/pre-trade-research.spec.js` covering SC-RES-01 to SC-RES-13 (14 tests, 14/14 pass). Playwright coverage for research view now complete. TSG closed.

### 17.3 TSG-v31-03 — EPIC-03: earnings-calendar.spec.js and screener-uk-suffix.spec.js not registered in test_scenarios

**Identified:** 2026-05-05 (delivery verification 2026-04-29__release-v3.1)
**Status:** ✅ Resolved — 2026-05-08 (post-ship closure v3.2 / ST-12)
**Owner:** QA & Testing Owner
**Gap:** `tests/e2e/earnings-calendar.spec.js` (SC-EARN-01–09) and `tests/e2e/screener-uk-suffix.spec.js` (SC-UK-01–04) created during EPIC-03 delivery but not registered in `execution_state.json test_scenarios`.
**Resolution:** ST-12 (EPIC-03, v3.2) registered both test files in `test_scenarios`. DEL-20260506-02 confirmed completed by Director of Quality 2026-05-06. TEST-GAP-EPIC-03 closed. Backlog item closed.

### 17.4 TSG-v31-04 — EPIC-04: no test scenarios

**Identified:** 2026-05-05 (delivery verification 2026-04-29__release-v3.1)
**Status:** Not applicable — governance documentation and prompt patches are not testable via scenario files
**Owner:** N/A
**Assessment:** All EPIC-04 stories were governance, documentation, and prompt patch deliveries. No behavioural test scenarios applicable.

---

## 18. Test Coverage Gaps — v3.2 (2026-05-05__release-v3.2)

Identified during delivery verification (verification_report.md §6 — TSG-v32-01).

### 18.1 TSG-v32-01 — EPIC-02: no Playwright coverage for entry checklist observable ACs

**Identified:** 2026-05-07 (delivery verification 2026-05-05__release-v3.2)
**Status:** ✅ Resolved — 2026-05-13 (v3.3, ST-11)
**Owner:** QA & Testing Owner
**Gap:** `tests/e2e/entry-checklist.spec.js` not yet created. 7 observable ACs (SC-CL-01 to SC-CL-07) lack Playwright coverage: checklist renders with 4 default items, items toggleable, state persists on save, stop_defined pre-check, research_reviewed pre-check, research link navigation, read-only checklist in research view.
**Required action:** QA & Testing Owner to author `tests/e2e/entry-checklist.spec.js` covering SC-CL-01 to SC-CL-07.
**Resolution target:** v3.3
**Backlog item:** BLG-QA-14 (filed 2026-05-06)
**Resolution:** `tests/e2e/entry-checklist.spec.js` authored by ST-11 (EPIC-03, v3.3) covering SC-CL-01 to SC-CL-07. Note: DEV-v33-03 (P3) — test file covers actual implementation field names (early_exit_conditions/r_target) which differ from spec (stop_level/risk_reward_notes).

---

## 19. Test Coverage Gaps — v3.3 (2026-05-09__release-v3.3)

Identified during delivery verification (verification_report.md §6 — TSG-v33-01 through TSG-v33-03).

### 19.1 TSG-v33-01 — EPIC-01: no Playwright coverage for lifecycle badge display

**Identified:** 2026-05-13 (delivery verification 2026-05-09__release-v3.3)
**Status:** Open — backlog item TEST-GAP-EPIC-01-v33
**Owner:** QA & Testing Owner
**Gap:** ST-03 (lifecycle badge frontend) returned to backlog. When implemented, SC-LS-01 to SC-LS-04 must be authored: lifecycle badge visibility (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN), arc3_lifecycle_display flag OFF (no badge), GRACE days_in_state display, EXIT ZONE colour rendering.
**Resolution target:** v3.4 (before or concurrent with ST-03 frontend implementation)
**Backlog item:** TEST-GAP-EPIC-01-v33 (filed 2026-05-13)

---

### 19.2 TSG-v33-02 — EPIC-02: no Playwright coverage for grace period alert and trail stop panels

**Identified:** 2026-05-13 (delivery verification 2026-05-09__release-v3.3)
**Status:** Open — backlog item TEST-GAP-EPIC-02-v33
**Owner:** QA & Testing Owner
**Gap:** ST-05 (grace period alert frontend) and ST-07 (trail stop panel) returned to backlog. When implemented, SC-GP-01 to SC-GP-03 and SC-TS-01 to SC-TS-03 must be authored: alert card render, display fields, dismiss/localStorage behaviour; trail stop button, panel fields, §13 confirm interaction.
**Resolution target:** v3.4 (before or concurrent with ST-05/ST-07 frontend implementation)
**Backlog item:** TEST-GAP-EPIC-02-v33 (filed 2026-05-13)

---

### 19.3 TSG-v33-03 — EPIC-03: SC-RV-18 and SC-RV-19 null-handling scenarios not in test library

**Identified:** 2026-05-13 (delivery verification 2026-05-09__release-v3.3)
**Status:** Open — backlog item TEST-GAP-EPIC-03-v33
**Owner:** QA & Testing Owner
**Gap:** research_view_protocol.md §2.3 flags SC-RV-18 (regime null only) and SC-RV-19 (all fields null — degraded mode) as needing explicit Playwright scenarios. These were not authored at sprint close. When research view frontend is implemented, these scenarios must be added to research_view_scenarios.md.
**Resolution target:** v3.4 (before research view frontend implementation)
**Backlog item:** TEST-GAP-EPIC-03-v33 (filed 2026-05-13)

---

## 12. Guiding Principle

> Specs explain decisions.
> This index ensures those decisions form a coherent system.