# Specs Index (Canonical)

**Owner:** Head of Specs Team
**Purpose:** Single map of canonical product truth
**Audience:** Product, Engineering, Analytics, Strategy
**Status:** Authoritative
**Last Updated:** 2026-09-03 (post-ship closure 2026-08-21__release-v9.0; §40 Test Coverage Gaps — v9.0 added, 2 findings both not_applicable; full-document TSG reconciliation sweep resolved 1 long-stale Open entry, TSG-v40-01; 2 other long-stale entries (TSG-v22-02, TSG-v23-01) re-confirmed genuinely still open, not stale-but-resolved); prior — 2026-08-12 (post-ship closure 2026-08-11__release-v8.6; §39 Test Coverage Gaps — v8.6 added, 0 new gaps; full-document TSG reconciliation sweep resolved 2 long-stale Open entries, TSG-v33-03 and TSG-v6.8-01); prior — 2026-08-07 (sprint execution 2026-08-07__release-v8.4, ST-09/EPIC-02: added `schema_versioning_trade_plan_position.md` to §3.2 Canonical Documents); prior history retained — see prior entries in version control.

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
- `schema_versioning_trade_plan_position.md` — Class 1 Canonical, v1.0, Active (created 2026-08-07, ST-09/EPIC-02/v8.4): migration-history index and field-deprecation policy scoped to `trade_plans` and `positions`. `data_model.md` remains authoritative if the two ever disagree.

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
- `reports_endpoints.md` — Class 1 Canonical, v0.9, Active (created 2026-03-17, ST-03; updated v0.4 by ST-11 cycle 2026-04-29__release-v3.1; updated v0.9 2026-07-20 ST-04 v7.5 EPIC-04 BLG-FE-118 — GET /reports/daily-pnl added for the Trade History Calendar View): GET /reports/tax-year (UK tax-year P&L) + GET /reports/monthly-pnl (monthly P&L summary) + GET /reports/daily-pnl (daily P&L summary). Dual sign-off: Head of Specs Team + Financial Reporting & Records Owner.
- `trade_plan_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-04-30, ST-01, cycle 2026-04-29__release-v3.1): POST /trade-plans, GET /trade-plans/{id}, PUT /trade-plans/{id}, DELETE /trade-plans/{id}, GET /trade-plans/by-position/{position_id}, GET /trade-plans/by-ticker/{ticker}. Sign-off: Sprint Execution Engine (autonomous class).
- `pre_trade_research_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-04-30, ST-04, cycle 2026-04-29__release-v3.1): GET /research/{ticker} — aggregates signal, regime, sector, screener, earnings (all sub-sources null-safe). Sign-off: Sprint Execution Engine (autonomous class).
- `earnings_endpoints.md` — Class 1 Canonical, v0.1, Active (created 2026-04-30, ST-07, cycle 2026-04-29__release-v3.1): GET /earnings/{ticker} — upcoming earnings date via yfinance; proximity flag. Sign-off: Sprint Execution Engine (autonomous class).
- `alerts_endpoints.md` — Class 1 Canonical, v0.3, Active (created 2026-03-20, ST-02; updated v0.3 2026-03-24, ST-05): Alert rules CRUD, alert evaluation, notification feed, notification preferences, alert history (GET /alerts/history). Architecture: FastAPI BackgroundTasks per ADR-003. Sign-off: Head of Specs Team (2026-03-20).
- `digest_endpoints.md` — Class 1 Canonical, v0.3, Active (created 2026-04-03, ST-08, cycle 2026-03-31__release-v2.4; updated v0.2 ST-03 cycle 2026-06-21__release-v5.1 — POST /digest/si05/send + DEV-v51-EPIC01-01 known deviation; updated v0.3 ST-03/ST-04 cycle 2026-06-08__release-v5.2 — pass_rate computation documented per BLG-SPEC-47 resolution; authentication requirements section added per BLG-SPEC-48): GET /digest/weekly; POST /digest/si05/send. Sign-off: QA Lead + DoQ (v0.1); API Contracts & Documentation Owner + Head of Specs Team (v0.3, 2026-06-08).
- `health_endpoints.md` — Class 1 Canonical, v1.3, Active (created 2026-03-18; updated v1.1 by ST-07 cycle 2026-03-24__release-v2.3; updated v1.2 by ST-08 adding GET /health/database; updated v1.3 by ST-08/ST-09 cycle 2026-04-25__release-v3.0 adding external_apis + ai_journal sections to GET /health): GET /health + GET /health/database operational health check endpoints. Sign-off: Head of Specs Team (v1.3, 2026-04-26).
- `analytics_endpoints.md` — Class 1 Canonical, v2.2.0, Active (updated 2026-04-15, ST-08, cycle 2026-04-13__release-v2.7: GET /analytics/market-correlation; updated v2.2.0 2026-06-09 ST-05 cycle 2026-06-08__release-v5.3 — GET /analytics/compliance-metrics added per BLG-SPEC-50). Sign-off: Head of Specs Team; API Contracts & Documentation Owner (v2.2.0).
- `signal_endpoints.md` — Class 1 Canonical, v1.2, Active (updated 2026-05-18, ST-01, cycle 2026-05-18__release-v3.7): PATCH /signals/{id} updated to accept `watchlisted` as valid status value; `watchlisted` added to signals table CHECK constraint (signal-to-watchlist workflow). Sign-off: Sprint Execution Engine (autonomous class). Previous: v1.1 (2026-04-15, ST-09, v2.7): POST /signals/generate supplementary display-only indicator fields; Strategy Rules Owner sign-off.
- `ai_endpoints.md` — Class 1 Canonical, v1.1, Active (created v1.0 2026-04-18, ST-07, cycle 2026-04-17__release-v2.8; updated v1.1 2026-06-09, ST-04, cycle 2026-06-08__release-v5.3 — GET /ai/journal-summary/history added per BLG-SPEC-49): POST /ai/journal-summary; GET /ai/journal-summary/history. Sign-off: Sprint Execution Engine (autonomous class); API Contracts & Documentation Owner (v1.1).
- `news_endpoints.md` — Class 1 Canonical, v1.0, Active (created 2026-06-09, ST-06, cycle 2026-06-08__release-v5.3 — BLG-SPEC-51): GET /news/{ticker}. Sign-off: API Contracts & Documentation Owner.
- `watchlist_endpoints.md` — Class 1 Canonical, v1.0, Active (created 2026-06-09, ST-07, cycle 2026-06-08__release-v5.3 — BLG-SPEC-52): GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id}. Sign-off: API Contracts & Documentation Owner + Head of Specs Team.
- `saved_filters_endpoints.md` — Class 1 Canonical, v1.0, Active (created 2026-07-20, ST-04, cycle 2026-07-17__release-v7.5 — BLG-FE-118): GET/POST /saved-filters, DELETE /saved-filters/{id} — named, server-side Trade History filter presets. Sign-off: API Contracts & Documentation Owner + Head of Specs Team.
- `ticker_universe_api_contract.md` — Class 2 Canonical (created 2026-04-25, ST-01, cycle 2026-04-25__release-v3.0; updated 2026-05-22 ST-06 v3.9 — company_name field added to GET /ticker-universe response): GET /ticker-universe, POST /ticker-universe, DELETE /ticker-universe/{ticker}; seed data contract; company_name field. Sign-off: Sprint Execution Engine (autonomous class).
- `screener_api_contract.md` — Class 2 Canonical (created 2026-04-23 v2.9; implementation delivered 2026-04-25 v3.0 ST-04; updated v1.1 2026-05-22 ST-04 v3.9 — degraded_run and failure_rate fields added; updated v1.2 2026-06-22 ST-04 v6.0 — tickers_requested, tickers_loaded, tickers_failed, last_full_run_utc, run_quality fields added to GET /screener/results response; DegradedRunBanner replaced by ScreenerQualityPanel): GET /screener/results, POST /screener/run; request/response schemas, pagination, error codes, quality telemetry fields. Sign-off: Sprint Execution Engine (autonomous class) v6.0.
- `alpaca_integration_contract.md` — Class 2 Canonical (created 2026-04-23 v2.9 ST-02): Alpaca Markets API contract for OHLCV bars and News endpoints; rate limits, error codes, fallback strategy, API version pin.
- `portfolio_endpoints.md` — Class 1 Canonical (created v2.0; updated v2.3 2026-05-22 ST-07 v3.9 — GET /portfolio/red-flag-journal added; red_flag_events table; SI-01 override event write path; updated v2.4 2026-05-31 ST-09 v4.6 — severity field + filter query parameter added to red_flag_events endpoints): GET /portfolio, GET /portfolio/pre-entry-validation, GET /portfolio/prospective-heat, GET /portfolio/red-flag-journal + other portfolio endpoints. Sign-off: Sprint Execution Engine (autonomous class).
- `behavioural_drift_contract.md` — Class 1 Canonical, v1.0, Active (created 2026-05-31, ST-04, cycle 2026-05-30__release-v4.6): GET /analytics/behavioural-drift — SI-02 4-metric behavioural drift response schema; §13 binding conditions; green/amber/red band thresholds; insufficient_data path. Sign-off: Sprint Execution Engine (autonomous class).
- `_external_api_template.md` — Template (created 2026-05-31, ST-21, cycle 2026-05-30__release-v4.6; BLG-SPEC-32): Standard template for external API integration contracts; 6 required sections (Overview, Authentication, Endpoints, Error Handling, Rate Limits, Change Log). Conformance advisory for existing contracts (Anthropic, Alpaca) noted in document. Sign-off: Head of Specs Team.
- `strategy_version_comparison_contract.md` — Pre-authored contract v0.1.0 (created 2026-06-02, ST-07, cycle 2026-06-01__release-v4.8; BLG-SPEC-43): GET /analytics/strategy-version-comparison — SI-04 strategy version comparison endpoint contract pre-authored before SI-04 sprint; response schema, query parameters, error cases, §13 binding conditions. Placeholder entry in openapi.yaml. Implementation gated on SI-04 sprint planning. Sign-off: Strategy Rules & System Intent Owner + Head of Specs Team (autonomous class).
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

### 6.4 API contract gaps from v5.2 endpoint coverage audit (BLG-SPEC-49–52)

**Status:** RESOLVED — 2026-06-09 (v5.3 EPIC-01 ST-04/05/06/07; all 4 backlog items completed — see §3.4 for updated contract file entries)
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Backlog items:** BLG-SPEC-49 ✅, BLG-SPEC-50 ✅, BLG-SPEC-51 ✅, BLG-SPEC-52 ✅

Four backend endpoints exist in `backend/routers/` and `docs/reference/openapi.yaml` but have no corresponding `## METHOD /path` entry in `docs/specs/api_contracts/`. These are spec debt items from prior releases:

| Backlog item | Endpoint | Contract file needed |
|---|---|---|
| BLG-SPEC-49 | GET /ai/journal-summary/history | ai_endpoints.md (or new file) |
| BLG-SPEC-50 | GET /analytics/compliance-metrics | analytics_endpoints.md or arc5_compliance_analytics.md |
| BLG-SPEC-51 | GET /news/{ticker} | pre_trade_research_endpoints.md or new news_endpoints.md |
| BLG-SPEC-52 | Watchlist endpoints | new watchlist_endpoints.md |

Each contract must include `## METHOD /path` heading, request/response schema, error codes, and openapi.yaml confirmation. Per CLAUDE.md §2.

---

### 6.5 Reports.js Tax Year P&L tab — two spec-authored sections never implemented (BLG-SPEC-71)

**Identified:** 2026-07-09 (v6.8 EPIC-02 ST-06 implementation session)
**Status:** RESOLVED — 2026-07-13 (v7.0 EPIC-02 ST-06, cycle 2026-07-12__release-v7.0)
**Backlog item:** BLG-SPEC-71 — COMPLETE
**Owner:** Head of Specs Team / Frontend Specifications & UX Documentation Owner
**Resolution:** ST-06 reconciled `docs/specs/frontend/pages/reports.md` §Arc 5 Compliance Summary and §Gross vs Net Comparison — both sections marked "Design Only — Implementation Pending", matching `Reports.js`'s actual shipped behaviour. No deviation — documentation now matches code.

~~`docs/specs/frontend/pages/reports.md` §Arc 5 Compliance Summary (v4.1) and §Gross vs Net Comparison (v6.0) both carry changelog entries and sign-off records claiming these sections were added to the Tax Year P&L tab, but neither is actually rendered in `src/pages/Reports.js`. Root cause confirmed via `git log -S`: both were spec-authoring-only stories whose changelog wording was indistinguishable from a shipped-feature entry.~~

---

### 6.6 SI-02 Gate Status Condition 2/3 thresholds — engine-filled placeholder, not yet product-reviewed (BLG-SPEC-72)

**Identified:** 2026-07-09 (v6.8 EPIC-02 ST-06, Product Owner PR review)
**Status:** RESOLVED — 2026-08-03 (ST-14, EPIC-05, v8.1)
**Backlog item:** BLG-SPEC-72
**Owner:** Product Owner / Head of UX & Design

The locked `si02-gate-visibility-indicator/ux_spec.md` left Gate Condition 2 unlabeled and gave no numeric MET threshold for Condition 3. The implementing engine filled the gap with Condition 2 = "linked closed trades ≥ 20" and Condition 3 = `trade_plan_adherence_rate > 0` — both spec-conformant but never explicitly product-reviewed.

**Resolution (2026-08-03):** Product Owner reviewed and decided: Condition 2 confirmed at the existing `linked closed trades >= 20` (consistent with Condition 1's own bar and the separate `BLG-GOV-107` backend gate — not changed). Condition 3 changed to `trade_plan_adherence_rate >= 0.50` (a majority-discipline bar; no prior threshold existed for this metric anywhere in the spec, so `> 0` was a true placeholder, not a defensible starting point). Codified in `docs/specs/frontend/pages/reports.md` v0.11→v0.12. `SI02GateStatusSection` updated to match, with new Playwright coverage.

---

### 6.7 Gate Progress Indicator copy diverges from dashboard.md §6 (BLG-SPEC-73)

**Identified:** 2026-07-09 (v6.8 EPIC-03 ST-11, dark Playwright spec fix)
**Status:** RESOLVED — 2026-07-13 (v7.0 EPIC-02 ST-10, cycle 2026-07-12__release-v7.0)
**Backlog item:** BLG-SPEC-73 — COMPLETE
**Owner:** Head of UX & Design / Head of Specs Team
**Resolution:** ST-10 updated `dashboard.md` §6 Display table to document the shipped `GateProgressStrip.js` copy verbatim; the Known Deviations note was removed. Wording-only change — FI-P3-02 code-review exception applies.

~~`dashboard.md` §6 specifies Gate Progress Indicator copy as `{N}/20 trades (PT-04/SI-02 gate)` / `Gate cleared ✓`; the shipped `GateProgressStrip.js` instead renders `{N}/{threshold} closed trades · {M} more to unlock quality insights` / `Quality insights unlocked ✓`. Both sides are internally consistent but disagree with each other.~~

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
**Status:** RESOLVED — 2026-07-16 (post-ship closure 2026-07-16__release-v7.3, STEP 7.3 TSG reconciliation; BLG-QA-01 confirmed COMPLETE in `backlog_archive.md`, retired 2026-03-16, cycle 2026-03-15__release-v1.10)
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
**Status:** RESOLVED — 2026-07-16 (post-ship closure 2026-07-16__release-v7.3, STEP 7.3 TSG reconciliation; BLG-QA-07 confirmed COMPLETE in `backlog_archive.md` — ST-06, PR #219/39efe64, SC-FEE-01–04 pass, shipped v2.6)
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
**Status:** ✅ RESOLVED — 2026-05-14 (v3.4, ST-01 EPIC-01)
**Owner:** QA & Testing Owner
**Gap:** ST-03 (lifecycle badge frontend) returned to backlog. When implemented, SC-LS-01 to SC-LS-04 must be authored: lifecycle badge visibility (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN), arc3_lifecycle_display flag OFF (no badge), GRACE days_in_state display, EXIT ZONE colour rendering.
**Resolution:** ST-01 (EPIC-01, v3.4) implemented LifecycleBadge and authored SC-LS-01–04 in `tests/e2e/epic01-v34-lifecycle.spec.js`. 4/4 scenarios pass. TEST-GAP-EPIC-01-v33 closed.

---

### 19.2 TSG-v33-02 — EPIC-02: no Playwright coverage for grace period alert and trail stop panels

**Identified:** 2026-05-13 (delivery verification 2026-05-09__release-v3.3)
**Status:** ✅ RESOLVED — 2026-05-14 (v3.4, ST-02/ST-03 EPIC-01)
**Owner:** QA & Testing Owner
**Gap:** ST-05 (grace period alert frontend) and ST-07 (trail stop panel) returned to backlog. When implemented, SC-GP-01 to SC-GP-03 and SC-TS-01 to SC-TS-03 must be authored: alert card render, display fields, dismiss/localStorage behaviour; trail stop button, panel fields, §13 confirm interaction.
**Resolution:** ST-02 (GracePeriodAlertZone, SC-GP-01–03) and ST-03 (TrailStopModal, SC-TS-01–03) implemented in EPIC-01 v3.4. All 6 scenarios pass in `tests/e2e/epic01-v34-lifecycle.spec.js`. TEST-GAP-EPIC-02-v33 closed.

---

### 19.3 TSG-v33-03 — EPIC-03: SC-RV-18 and SC-RV-19 null-handling scenarios not in test library

**Identified:** 2026-05-13 (delivery verification 2026-05-09__release-v3.3)
**Status:** ✅ RESOLVED — 2026-08-12 (post-ship closure 2026-08-11__release-v8.6, STEP 7.3 TSG reconciliation sweep)
**Owner:** QA & Testing Owner
**Gap:** research_view_protocol.md §2.3 flags SC-RV-18 (regime null only) and SC-RV-19 (all fields null — degraded mode) as needing explicit Playwright scenarios. These were not authored at sprint close. When research view frontend is implemented, these scenarios must be added to research_view_scenarios.md.
**Resolution target:** v3.4 (before research view frontend implementation)
**Resolution:** Both scenarios confirmed present and passing in `tests/e2e/pre-trade-research.spec.js` (`SC-RV-18: regime=null — page renders without crash; Back button visible`; `SC-RV-19: All fields null — degraded mode; no crash; Back button accessible`). The referenced backlog item `TEST-GAP-EPIC-03-v33` could not be located in `claude/backlog/backlog.md` under that literal ID (predates the current `BLG-*` ID convention) — resolution confirmed directly against the live test file instead of via backlog cross-reference. This closes a long-stale Open TSG entry the STEP 7.3 sweep exists to catch.
**Backlog item:** TEST-GAP-EPIC-03-v33 (filed 2026-05-13)

---

---

## 20. Test Coverage Gaps — v3.4 (2026-05-14__release-v3.4)

Identified during delivery verification (verification_report.md §6 — TSG-v34-01).

### 20.1 TSG-v34-01 — EPIC-04: no test scenarios for documentation/spec creation stories

**Identified:** 2026-05-14 (delivery verification 2026-05-14__release-v3.4)
**Status:** Not applicable — documentation and specification creation tasks have no observable UI or backend computation to test
**Owner:** N/A
**Assessment:** All EPIC-04 stories (ST-11/12/13/14) create spec or doc artefacts. No behavioural scenarios applicable. Disposition: not_applicable. No backlog item required.

---

## 21. Test Coverage Gaps — v3.7 (2026-05-18__release-v3.7)

Identified during delivery verification (verification_report.md §6). **Zero test coverage gaps** across all three EPICs.

| EPIC | Disposition | Notes |
|------|-------------|-------|
| EPIC-01 | not_applicable — fully covered | 7 Playwright scenarios: SC-SIG-WL-01/02/03 (signals-add-to-watchlist.spec.js) + SC-TP-SIG-01/02/03/04 (trade-plan-signal-context.spec.js); all observable AC covered |
| EPIC-03 | not_applicable — governance patches | Autonomous governance prompt + template files only; no observable UI behaviour |
| EPIC-04 | not_applicable — autonomous/infrastructure | Conftest consolidation, pycache hygiene, typography staging, scoring doc refresh; no core user journey |

No backlog items required. All coverage complete or explicitly not_applicable.

---

## 22. Test Coverage Gaps — v3.9 (2026-05-21__release-v3.9)

Identified during delivery verification (verification_report.md §6). **Zero test coverage gaps** across all four EPICs.

| EPIC | Disposition | Notes |
|------|-------------|-------|
| EPIC-01 | not_applicable — fully covered | Unit tests: test_screener_data_service.py, test_screener_batch_service.py; Playwright SC-SCR-DEG-01/02; all observable ACs covered. ST-01 AC-04 staging-only evidence (BLG-QA-24 process notation — not a gap) |
| EPIC-02 | not_applicable — fully covered | SC-TU-DISP-01 (3 sub-tests: .L strip, US unaffected, API request preserved); SC-TU-COMP-01 (3 sub-tests: column header, known ticker, LSE ticker); all observable ACs covered |
| EPIC-03 | not_applicable — fully covered | SC-RFJ-01/02/03 Playwright (events list, empty state, event_type filter) + 5 unit tests (test_red_flag_journal.py); all observable ACs covered |
| EPIC-04 | not_applicable — governance class | Governance prompt + template changes only; no observable UI behaviour; all ACs verifiable by diff |

No TEST-GAP backlog items required.

---

## 23. Test Coverage Gaps — v4.0 (2026-05-22__release-v4.0)

Identified during delivery verification (verification_report.md §6 — TSG-v40-01 through TSG-v40-03). Two gaps actioned with backlog items; one not_applicable.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| TSG-v40-01 | EPIC-01 | PerformanceAnalytics Arc5ComplianceSection rendering (ST-02/ST-04 observable ACs: stat cards visible, loading skeleton, error state) not covered by Playwright E2E | backlog_item_created — BLG-QA-28 (v4.1 provisional target) |
| TSG-v40-02 | EPIC-02 | No test scenarios — starlette security pin, ticker validation (CI bypass), security review story | not_applicable — all EPIC-02 stories are backend/security class; CI tests cover accessible paths via SKIP_TICKER_VALIDATION bypass |
| TSG-v40-03 | EPIC-03 | Gemini "Improve with AI" button and live thesis generation (ST-12 staging-only ACs) not covered by Playwright | backlog_item_created — BLG-QA-29 (covers live key and frontend button staging verification) |

### 23.1 TSG-v40-01 — EPIC-01: Arc5ComplianceSection rendering not covered by Playwright

**Identified:** 2026-05-25 (delivery verification 2026-05-22__release-v4.0)
**Status:** ✅ RESOLVED — 2026-09-03 (post-ship closure 2026-08-21__release-v9.0, STEP 7.3 TSG reconciliation full-document sweep). Playwright tests created 2026-05-27 (v4.1 ST-11 AC-01, arc5-compliance-section.spec.js, 4 scenarios). Remaining staging-verification ACs (BLG-QA-28 ACs 02–04) confirmed shipped and retired: `backlog_archive.md` records `BLG-QA-28` as ✅ Complete, retired 2026-05-29, shipped v4.3 (`docs/product/changelog.md#v4.3`) — found still marked "Partially resolved" here despite having shipped over 3 months (16+ cycles) earlier; no closure between v4.3 and this one had re-checked this entry.
**Owner:** QA & Testing Owner
**Gap:** ST-02/ST-04 introduced Arc5ComplianceSection.js with observable ACs (stat cards rendering, loading skeleton, error state) on PerformanceAnalytics page (§19). No Playwright E2E scenarios cover these observable ACs. Code review only was performed per CLAUDE.md §2; BLG-QA-28 filed before PR opened.
**Backlog item:** BLG-QA-28 — Staging verification for Arc5ComplianceSection (v4.2 provisional target; Playwright automation delivered v4.1)

### 23.2 TSG-v40-03 — EPIC-03: Gemini "Improve with AI" button staging-only ACs not covered

**Identified:** 2026-05-25 (delivery verification 2026-05-22__release-v4.0)
**Status:** RESOLVED — 2026-07-16 (post-ship closure 2026-07-16__release-v7.3, STEP 7.3 TSG reconciliation; BLG-QA-29 confirmed COMPLETE in `backlog_archive.md`, retired 2026-05-29, shipped v4.3)
**Owner:** QA & Testing Owner
**Gap:** ST-12 introduced "Improve with AI" button on TradePlan edit page and POST /trade-plans/{plan_id}/generate-thesis. Observable ACs (button visibility in edit mode, endpoint call, setup_thesis population) require live GEMINI_API_KEY and are not testable in CI. Code review only per CLAUDE.md §2; BLG-QA-29 filed before PR opened.
**Backlog item:** BLG-QA-29 — Staging verification for Gemini thesis generation (covers live key and frontend button staging verification)

---

## 24. Test Coverage Gaps — v4.1 (2026-05-26__release-v4.1)

Identified during delivery verification (verification_report.md §6). No test scenario gaps — all EPICs dispositioned as not_applicable or fully covered.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| — | EPIC-01 | Governance prompt files only — no observable UI behaviour | not_applicable |
| — | EPIC-02 | Spec documentation verification only — pre-met path; no code changes | not_applicable |
| — | EPIC-03 | All scenarios run: research-view-signal-type.spec.js (4 tests), arc5-compliance-section.spec.js (4 tests), test_daily_cost_alert.py (5 unit tests) — no coverage gap | fully_covered |
| — | EPIC-04 | Governance/ops documents only — no observable UI behaviour | not_applicable |

No TSG backlog items required.

---

## 25. Test Coverage Gaps — v4.2 (2026-05-27__release-v4.2)

Identified during delivery verification (verification_report.md §6). No test scenario gaps — all EPICs dispositioned as not_applicable.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| — | EPIC-01 | No observable UI behaviour; governance/security/policy scope; all ACs verifiable by document review and code inspection | not_applicable |
| — | EPIC-02 | No observable UI behaviour; operational baseline/documentation scope; ACs verifiable by live environment measurements and document review | not_applicable |
| — | EPIC-03 | No observable UI behaviour; backend/spec/docs scope; CLAUDE.md §2 compliance verified by code review; pytest passed | not_applicable |
| — | EPIC-04 | No observable UI behaviour; governance/pre-planning scope; all ACs verifiable by document review | not_applicable |

No TSG backlog items required.

---

## 26. Test Coverage Gaps — v4.5 (2026-05-30__release-v4.5)

Identified during delivery verification (verification_report.md §6). **Zero test coverage gaps** — all EPICs governance/spec-only class.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| — | EPIC-01 | Governance prompt patches only; no behavioral/frontend change; all AC document-inspection-verifiable | not_applicable — governance sprint; no core user journey affected; no Playwright coverage needed |
| — | EPIC-02 | Agent role header format update only; no behavioral change; no observable UI effect | not_applicable — file content change invisible to end users; no Playwright coverage needed |
| — | EPIC-03 | Spec documents produced (decision record, metric definition, data schema); no code shipped; no behavioral/UI change | not_applicable — pre-planning spec deliverables; SI-02 implementation sprint will commission scenarios |

No TSG backlog items required.

**New SI-02 pre-planning spec documents filed this cycle:**
- `docs/specs/metrics/si02_drift_score.md` — SI-02 drift detection score metric definition (ST-07): 4 drift metrics, 90-day rolling window, green/amber/red threshold bands, SI-05 integration points. Owner: Metrics Definitions & Analytics Canonical Owner + Head of Specs Team. Pre-planning specification for SI-02 implementation sprint.
- `docs/specs/data_model/si02_data_schema.md` — SI-02 data schema pre-definition (ST-08): 5 new trade_plans columns (signal_id, risk_percent_used, portfolio_value_at_entry, pre_entry_validation_snapshot, effective_settings_snapshot), 3 indexes, DS-07 migration script. Owner: Data Model & Domain Schema Owner + Head of Specs Team. Pre-planning specification for SI-02 implementation sprint.
- `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md` — SI-02 §13 formal boundary review decision record (ST-06): PASS determination; 9 binding conditions documented. Class 3 Operational Record (permanent). Owner: Strategy Rules & System Intent Owner.

---

## 27. Test Coverage Gaps — v5.0 (2026-06-03__release-v5.0)

Identified during delivery verification (verification_report.md §6 — TSG-v50-01).

### 27.1 TSG-v50-01 — EPIC-03: no Playwright coverage for allocation_insufficient SignalCard badge

**Identified:** 2026-06-03 (delivery verification 2026-06-03__release-v5.0)
**Status:** RESOLVED — 2026-06-04 (v5.1, EPIC-01, ST-11, cycle 2026-06-21__release-v5.1) — SignalCard allocation_insufficient Playwright E2E coverage (5 scenarios) delivered; BLG-FE-61 closed.
**Owner:** QA & Testing Owner
**Gap (resolved):** ST-06 (allocation_insufficient signal status) introduced a visible frontend change: SignalCard renders an orange "Cannot Size" badge and displays the reason string inline when `signal.status === 'allocation_insufficient'`. Playwright coverage (5 scenarios: SC-SIG-ALLOC-01, SC-SIG-ALLOC-02) delivered in v5.1.
**Resolution:** BLG-FE-61 closed — v5.1 cycle 2026-06-21__release-v5.1 — post-ship closure 2026-06-22 (gap identified as stale open during v6.0 closure Specs Index review)

---

## 28. Test Coverage Gaps — v6.0 (2026-06-19__release-v6.0)

Identified during delivery verification (verification_report.md §6 — TSG-v60-01 through TSG-v60-04). One backlog item required.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| TSG-v60-01 | EPIC-01 | docs/testing/signals_scenarios.md listed in execution_state.json test_scenarios for EPIC-01 but not referenced as run in QA evidence — broader signal domain scenarios may contain stale assertions after cash-allocation model removal (ST-01 replaced with risk-based sizing) | **RESOLVED — 2026-07-03 (v6.5 ST-06, cycle 2026-07-02__release-v6.5).** All scenarios in `signals_scenarios.md` reviewed against the risk-based sizing model — zero references to suggested_shares/sizing/cash-allocation found; no stale scenarios to update. Outcome committed as `signals_scenarios.md` v1.2→v1.3 changelog entry. Resolves 3-cycle carry-forward (v6.2→v6.3→v6.4); backlog item BLG-QA-61 closed. |
| TSG-v60-02 | EPIC-02 | docs/testing/staging_visual_test_script_EPIC-02.md listed but not run in sprint QA | deferred — post-deploy staging review; all CI-verifiable ACs satisfied by Playwright (morning-briefing.spec.js, net-r-trade-history.spec.js) |
| TSG-v60-03 | EPIC-03 | docs/testing/screener_accuracy_protocol.md and docs/testing/staging_visual_test_script_EPIC-03.md listed but not run in sprint QA | deferred — post-deploy staging review; screener-quality.spec.js covers all 7 AC-07 requirements |
| TSG-v60-04 | EPIC-04 | test_scenarios = [] | not_applicable — documentation-only EPIC; no frontend-visible ACs; no automated test scenarios applicable |

### 28.1 TSG-v60-01 — EPIC-01: signals_scenarios.md not run against ST-01 sizing model changes

**Identified:** 2026-06-22 (delivery verification 2026-06-19__release-v6.0)
**Status:** RESOLVED — 2026-07-03 (v6.5 ST-06, cycle 2026-07-02__release-v6.5) — backlog item BLG-QA-61 closed
**Owner:** QA & Testing Owner
**Gap:** ST-01 removed the cash-allocation model for `suggested_shares` and replaced it with `size_position()` per strategy_rules.md §4.1. `docs/testing/signals_scenarios.md` was listed in execution_state.json test_scenarios but was not referenced as run in QA evidence. New `tests/test_signal_sizing.py` covered story-specific ACs but broader domain regression via signals_scenarios.md was not confirmed. Any scenario asserting specific suggested_shares values based on the old cash-allocation formula (cash / n_signals) will produce incorrect expected values.
**Required action:** QA & Testing Owner to review docs/testing/signals_scenarios.md against ST-01 changes, update any stale scenario assertions, and confirm coverage status before next sprint touching signal generation domain.
**Resolution target:** Before next sprint on signal generation domain
**Backlog item:** BLG-QA-61 (filed 2026-06-22 during delivery verification)

---

## 29. Test Coverage Gaps — v6.1 (2026-06-22__release-v6.1)

Identified during delivery verification (verification_report.md §6 — TSG-v61-01 through TSG-v61-04). No backlog items required.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| TSG-v61-01 | EPIC-01 | Governance prompts (release_planning_prompt.md STEP 4.1, sprint_planning_prompt.md STEP -1.3) — no Playwright coverage applicable | not_applicable — prompt-only changes; no frontend-visible ACs; no automated test scenarios applicable |
| TSG-v61-02 | EPIC-02 | CI registration (playwright.yml) and api_performance_baseline.md update | not_applicable — infrastructure and docs only; no observable UI changes; CI itself validates the registered specs |
| TSG-v61-03 | EPIC-03 | Sector heat-map (SC-SHM-01..04) and gate proximity indicator (SC-GP-01..04) | not_applicable — full Playwright coverage delivered in sprint (8 scenarios across 2 features); no residual gap |
| TSG-v61-04 | EPIC-04 | Setup Quality Score frontend (SC-SQS-01..06) | not_applicable — full Playwright coverage delivered in sprint (6 scenarios); no residual gap |

No open TSG items for v6.1. All observable ACs have Playwright coverage confirmed in CI.

---

## 30. Test Coverage Gaps — v6.2 (2026-06-24__release-v6.2)

Identified during delivery verification (verification_report.md §6 — no gap items). No backlog items required.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| — | EPIC-01 | Trailing stop display, breach badge, rebalance exit label, risk-off alert (16 E2E scenarios in epic01-v62-stops-alerts.spec.js @ 534b137f) | not_applicable — full Playwright coverage confirmed in CI |
| — | EPIC-02 | AI daily briefing card, AI chat widget (9 Playwright scenarios SC-AB-01..04, SC-AC-01..05 in epic02-v62-ai-briefing-chat.spec.js) | not_applicable — full Playwright coverage confirmed in CI |
| — | EPIC-03 | execution_prompt governance changes, api_performance_baseline ops doc, playwright.config.js CI change | not_applicable — autonomous/governance/CI class; no frontend-visible ACs |

No open TSG items for v6.2. All observable ACs have Playwright coverage confirmed in CI (EPIC-01, EPIC-02). EPIC-03 not_applicable (autonomous/CI class).

**TSG backlog reconciliation (§7.3):**
- TSG-v60-01 (BLG-QA-61): signals_scenarios.md review — **remains Open** — BLG-QA-61 not resolved in v6.2 sprint; no resolution action taken.
- All other open TSG entries checked; no v6.2 stories close any outstanding TSG items.

---

## 31. Test Coverage Gaps — v6.3 (2026-06-26__release-v6.3)

Identified during delivery verification (verification_report.md §6 — 2 gap items). Backlog items created.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| TSG-v63-01 | EPIC-01 | AI journal error states not covered by Playwright — ST-01 (BLG-BE-39) fixed the silent failure but error state paths (network error, API timeout, empty notes) have no automated test coverage | **RESOLVED — 2026-07-02 (v6.4 ST-12, cycle 2026-07-02__release-v6.4).** SC-TH-AI-01/02/03 added to `tests/e2e/trade-history-ai-journal-summary.spec.js`; backlog item TEST-GAP-EPIC-01 closed. |
| TSG-v63-02 | EPIC-03 | Strategy Benchmark page (StrategyBenchmark.js) — test_scenarios pending; no Playwright E2E coverage for the page's 5 observable ACs (navigation, year filter, panel rendering, toggle modes, badge language) | **RESOLVED — 2026-07-02 (v6.4 ST-13, cycle 2026-07-02__release-v6.4).** SC-SB-01/02/03/04 added to `tests/e2e/strategy-benchmark.spec.js` (scoped to Panels 1/3 per sprint_backlog.md; Panel 0 tracked separately as TSG-v64-01); backlog item TEST-GAP-EPIC-03 closed. |

**TSG backlog reconciliation (§7.3):**
- TSG-v60-01 (BLG-QA-61): signals_scenarios.md review — **remains Open** — BLG-QA-61 not resolved in v6.4 sprint either (3rd consecutive cycle without resolution; per the v6.3 note this is now a 2-cycle recurrence escalation). Escalated to Head of Specs Team — see `lessons_learnt_closure.md` Carry-Forward, cycle 2026-07-02__release-v6.4.
- All other open TSG entries checked; no v6.4 stories close any other outstanding pre-v6.4 TSG items.

---

## 32. Test Coverage Gaps — v6.4 (2026-07-02__release-v6.4)

Identified during delivery verification (verification_report.md §6 — 1 gap item). Backlog item created.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| TSG-v64-01 | EPIC-03 | ST-08/AC-01 — Open Positions Panel 0 conditional rendering on Strategy Benchmark page has no Playwright coverage this sprint (ST-13/TEST-GAP-EPIC-03 scoped to Panels 1/3 only; AC-01 cleared by code review only) | **RESOLVED — 2026-07-03 (v6.5 ST-05, cycle 2026-07-02__release-v6.5).** SC-SB-05a/b, SC-SB-06a/b, SC-SB-07a added to `tests/e2e/strategy-benchmark.spec.js` (Panel 0 conditional rendering, Market-filter interaction, API-error state); backlog item TEST-GAP-EPIC-03-v64 closed. |

**TSG backlog reconciliation (§7.3):**
- No pre-v6.4 TSG items closed by this cycle beyond TSG-v63-01/02 (recorded in §31 above).

---

## 33. Test Coverage Gaps — v6.5 (2026-07-02__release-v6.5)

Identified during delivery verification (verification_report.md §6 — no gap items). No backlog items required.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| — | EPIC-01 | Governance/documentation/config-only EPIC (audit.py config sync, README hygiene, OPERATIONAL_GUIDE/prompt version-sync drift) — `test_scenarios: []` | not_applicable — no frontend-visible ACs; verification method was direct file review |
| — | EPIC-02 | API baseline registration + Playwright coverage for Strategy Benchmark Panel 0 + signals_scenarios.md review | not_applicable — full Playwright coverage confirmed in `tests/e2e/strategy-benchmark.spec.js` (13/13 passing) |
| — | EPIC-03 | Claude thesis feedback mechanism + adoption rate metric | not_applicable — full Playwright coverage confirmed in `tests/e2e/trade-plan.spec.js` (29/29 passing, 6 new SC-TP-23a–f scenarios) |

No open TSG items for v6.5. All observable ACs have Playwright coverage confirmed in CI (EPIC-02, EPIC-03). EPIC-01 not_applicable (governance/documentation/config class).

**TSG backlog reconciliation (§7.3):**
- TSG-v60-01 (BLG-QA-61): **RESOLVED this cycle** — see §28 above. Closes a 2-cycle recurrence escalation open since v6.2.
- TSG-v64-01 (TEST-GAP-EPIC-03-v64): **RESOLVED this cycle** — see §32 above.
- All other open TSG entries checked; no other pre-v6.5 TSG items closed by this cycle.

---

## 34. Test Coverage Gaps — v6.6 (2026-07-04__release-v6.6)

Identified during delivery verification (verification_report.md §6 — no gap items). No backlog items required.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| — | EPIC-01 | ST-01 audit/findings-only story (Design Not Applicable, no in-story fix) + ST-02 Red Flag Journal filter persistence | not_applicable — ST-01 has no runnable ACs (audit report is the deliverable); ST-02 fully covered by `tests/e2e/red-flag-journal-filter-persistence.spec.js` (2/2 passing, SC-RFJ-05a/05b) |
| — | EPIC-02 | Backlog-ID collision audit (BLG-QA-72) + `_DB_STUB_FUNCTIONS` AST-scan derivation (BLG-QA-73) | not_applicable — backend/governance-data class, no frontend-visible AC; verification method was full local `pytest` before/after comparison plus direct document/archive audit |

No open TSG items for v6.6. All observable ACs have Playwright coverage confirmed in CI (EPIC-01/ST-02). EPIC-01/ST-01 and EPIC-02 not_applicable (audit / backend-governance class, no frontend-visible AC).

**TSG backlog reconciliation (§7.3):**
- No pre-v6.6 open TSG items existed at cycle start (all resolved as of §33/v6.5). Nothing to reconcile.

---

## 35. Test Coverage Gaps — v6.7 (2026-07-06__release-v6.7)

Identified during delivery verification (verification_report.md §6 — no gap items). No backlog items required.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| — | EPIC-01 | Dark-theme contrast fix (ST-01) + light-theme companion pairing (ST-02) + shared design token (ST-03) | not_applicable — ST-01/ST-02 fully covered by `tests/e2e/secondary-text-contrast.spec.js` (SC-CTR-01a/01b/02a/02b, 4/4 passing); ST-03 is documentation-only (design token transcription into `design_system.md`), no runnable AC |
| — | EPIC-02 | Full AUD-2026-07-06 governance-hardening bundle (ST-04–ST-07) | not_applicable — governance/documentation/process class, no frontend-visible AC; verification method was direct read of each modified write step |

No open TSG items for v6.7. All observable ACs have Playwright coverage confirmed in CI (EPIC-01/ST-01/ST-02). EPIC-01/ST-03 and EPIC-02 not_applicable (documentation / governance-process class, no frontend-visible AC).

**TSG backlog reconciliation (§7.3):**
- No pre-v6.7 open TSG items existed at cycle start (all resolved as of §34/v6.6). Nothing to reconcile.

---

## 36. Test Coverage Gaps — v6.8 (2026-07-08__release-v6.8)

Identified during delivery verification (verification_report.md §6 — 1 gap item). Backlog item created.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| TSG-v6.8-01 | EPIC-03 | `Watchlist.js` (core Watchlist page) has zero baseline Playwright coverage — ST-14's decomposition relied on manual smoke testing + diff review, not automated regression coverage | **✅ RESOLVED — 2026-08-12 (post-ship closure 2026-08-11__release-v8.6, STEP 7.3 TSG reconciliation sweep).** `BLG-QA-86` shipped v8.3 ST-16 ("Add baseline Playwright coverage for `Watchlist.js`", `docs/product/changelog.md#v8.3`), archived COMPLETE in `backlog_archive.md`. Last checked-and-left-open at v7.8's own reconciliation (line above, superseded); no closure between v7.9 and v8.5 re-ran this specific check. |

**TSG backlog reconciliation (§7.3):**
- No pre-v6.8 open TSG items existed at cycle start (all resolved as of §35/v6.7). Nothing to reconcile.

---

## 37. Test Coverage Gaps — v7.7 (2026-07-21__release-v7.7)

Identified during delivery verification (verification_report.md §6 — 5 gap items, all dispositioned `not_applicable`). No backlog items required.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| TSG-v7.7-01 | EPIC-03 | No committed Playwright scenario for AiDailyBriefing light-theme rendering | not_applicable — staging-only AC by design (CI cannot execute a live-rendering visual check); human staging run performed with date recorded (2026-07-23), satisfying CLAUDE.md's frontend testing gate exception |
| TSG-v7.7-02 | EPIC-05 | `test_scenarios = []` | not_applicable — investigation/recommendation output, no shipped UI, autonomous/no-UI short-circuit |
| TSG-v7.7-03 | EPIC-06 | `test_scenarios = []` | not_applicable — CI/infra workflow change, no frontend-visible AC |
| TSG-v7.7-04 | EPIC-07 | `test_scenarios = []` | not_applicable — governance/documentation review, no frontend-visible AC |
| TSG-v7.7-05 | EPIC-10 | `test_scenarios = []` | not_applicable — CI/infra workflow change, no frontend-visible AC |

No open TSG items for v7.7. EPIC-01/02/04/08/11 all have populated `test_scenarios` confirmed run against the sign-off commit (see verification_report.md §6).

**TSG backlog reconciliation (§7.3):**
- TSG-v6.8-01 (`BLG-QA-86`, Watchlist.js baseline Playwright coverage) checked against this cycle's shipped scope — `BLG-QA-86` remains open in `backlog.md` (not touched by any v7.7 story); entry left unchanged.
- No other open TSG entries existed at cycle start.

---

## 38. Test Coverage Gaps — v7.8 (2026-07-24__release-v7.8)

Identified during delivery verification (verification_report.md §6 — 1 gap item, dispositioned `not_applicable`). No backlog items required.

| gap_id | EPIC | Description | Disposition |
|--------|------|-------------|-------------|
| TSG-v7.8-01 | EPIC-07 | `test_scenarios = []` | not_applicable — pure-documentation/process artefact (API key rotation-and-audit schedule), no frontend-visible AC, no code shipped |

No open TSG items for v7.8. EPIC-01/02/03/04/05/06/08/09/10/11/12 all have populated `test_scenarios` confirmed run against the sign-off commit (see verification_report.md §6); EPIC-01/03/04/05/06's Playwright specs were executed locally against a real browser this cycle (system `snap` Chromium, per `sprint_close.md` Process Notes), not merely written-but-unexecuted.

Three documentation-completeness gaps (not test coverage gaps) were also surfaced this cycle during EPIC-11/ST-11 pilot contract-test authoring — filed directly as backlog items rather than TSG entries since they concern existing contract-doc accuracy, not missing test coverage: `BLG-SPEC-102` (`position_endpoints.md` envelope claim vs. live behaviour), `BLG-SPEC-103` (`GET /positions` undocumented lifecycle fields), `BLG-SPEC-104` (`trade_endpoints.md` example omits 3 documented fields). See `claude/cycles/2026-07-24__release-v7.8/qa_evidence_EPIC-11.md` and `verification_report.md §5(a)`.

**TSG backlog reconciliation (§7.3):**
- TSG-v6.8-01 (`BLG-QA-86`, Watchlist.js baseline Playwright coverage) checked against this cycle's shipped scope — `BLG-QA-86` remains open in `backlog.md` (not touched by any v7.8 story); entry left unchanged.
- No other open TSG entries existed at cycle start (§27's TSG-v50-01 was already RESOLVED prior to this cycle).

---

## 39. Test Coverage Gaps — v8.6 (2026-08-11__release-v8.6)

Identified during delivery verification (`verification_report.md §6`): **0 new test scenario gaps this cycle** — all 6 EPICs have either confirmed-run coverage or a valid `not_applicable` short-circuit (EPIC-06). No new `TSG-*` entries required.

**TSG backlog reconciliation (§7.3 — full-document sweep, per `post_ship_closure.md` v2.26's no-fixed-section-number scan rule):**
- **TSG-v33-03** (`docs/specs/frontend/pages/analytics.md`-adjacent — SC-RV-18/SC-RV-19 research-view null-handling scenarios, §19.3 above): found still marked Open since 2026-05-13 (v3.3). Both scenarios confirmed present and passing in `tests/e2e/pre-trade-research.spec.js`. Marked ✅ RESOLVED this cycle.
- **TSG-v6.8-01** (`BLG-QA-86`, Watchlist.js baseline Playwright coverage, §36 above): found still marked Open since 2026-07-08 (v6.8), last checked-and-left-open at v7.8 (§38). `BLG-QA-86` in fact shipped v8.3 ST-16 (`docs/product/changelog.md#v8.3`) — the reconciliation check itself was not re-run at any closure between v7.9 and v8.5. Marked ✅ RESOLVED this cycle.
- All other historical TSG entries (§9–§38) already carry `RESOLVED`/`not_applicable`/`OPEN`-with-confirmed-still-open dispositions; no further stale entries found in this sweep.

This closes 2 long-stale Open entries the STEP 7.3 sweep exists to catch (one 15+ cycles stale, one 5+ cycles stale) — recorded as a Friction Log item in `lessons_learnt_closure.md` for this cycle: the per-cycle reconciliation note (§7.3) only checks entries the closure engine already knows to look at, and does not itself guarantee a full-document sweep unless explicitly re-run; this closure's use of the full-scan convention (introduced `post_ship_closure.md` v2.26, LL-v8.4-Closure-01) is what caught them.

---

## 40. Test Coverage Gaps — v9.0 (2026-08-21__release-v9.0)

Identified during delivery verification (`verification_report.md §6`): 2 findings, both `not_applicable` — no new actionable `TSG-*` entries required.

| gap_id | EPIC | Description | Qualifying reason | Disposition |
|--------|------|-------------|-------------------|-------------|
| TSG-v9.0-01 | EPIC-03 | `execution_state.json.test_scenarios` field left empty despite real test files being run and confirmed in `qa_evidence_EPIC-03.md` | Metadata-completeness gap, not a coverage gap — no frontend-visible AC in this EPIC | not_applicable |
| TSG-v9.0-02 | EPIC-05 | No dedicated test scenario files — all 5 stories are review/documentation deliverables verified via full backend suite regression only | Ops/backend-review-only class, no frontend-visible AC, no core user journey affected | not_applicable |

Both are tracked as a lessons-learnt friction item, not backlog debt (`lessons_learnt_cycle.md` Phase 4, this cycle) — no `BLG-*` filing required per the STEP 5.2 short-circuit.

**TSG backlog reconciliation (§7.3 — full-document sweep, per `post_ship_closure.md`'s no-fixed-section-number scan rule):**
- **TSG-v40-01** (`BLG-QA-28`, Arc5ComplianceSection staging verification, §23.1 above): found still marked "Partially resolved" since 2026-05-27, carried across 16+ cycles. `BLG-QA-28`'s remaining staging-verification ACs (02–04) in fact shipped and were retired 2026-05-29 (v4.3) — confirmed via `backlog_archive.md`. No closure between v4.3 and this one had re-checked this entry. Marked ✅ RESOLVED this cycle.
- **TSG-v22-02** (`SC-HEALTH-01`, `GET /health` schema validation scenario, §10.2 above): re-confirmed still genuinely Open — no `SC-HEALTH-01` scenario file exists anywhere in `tests/`. Open since 2026-03-24 (~24 cycles). Not a stale-but-actually-resolved case like TSG-v40-01 above; this is a real, still-unactioned gap. Left Open — authoring the scenario is outside post-ship closure's write scope.
- **TSG-v23-01** (`V-CHART-05a/b/c`, R-Multiple chart tooltip staging visual scenarios, §10.3 above): re-confirmed still genuinely Open — `docs/testing/staging_visual_test_script_ST-06.md` still shows all three scenarios `[ ] STAGING-BLOCKED`, unexecuted since the underlying blocker (`BLG-BE-04`) resolved 2026-04-03. Open since 2026-03-30 (~24 cycles). Left Open — staging execution is outside post-ship closure's write scope; recorded as an Outstanding Action (see closure record §6).
- All other historical TSG entries (§9–§39) already carry `RESOLVED`/`not_applicable`/confirmed-still-open dispositions; no further stale-but-actually-resolved entries found in this sweep.

---

## 12. Guiding Principle

> Specs explain decisions.
> This index ensures those decisions form a coherent system.