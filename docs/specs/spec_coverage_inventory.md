**Owner:** Head of Specs Team
**Class:** Class 3 Operational Record
**Status:** Filed
**Version:** 1.0
**Audit Date:** 2026-03-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint Item:** ST-17 — EPIC-05 (v2.0)
**GH Issue:** #79

---

# Spec Coverage Inventory — v2.0 Audit

## Purpose

This document records the results of a systematic audit of all `docs/specs/` sections, performed as ST-17 of the v2.0 sprint. Each spec document (or logical section within a document) is rated against:

- **Implementation coverage** — does backend/frontend code exist for what the spec defines?
- **Test coverage** — are integration or acceptance tests in place?
- **Lifecycle compliance** — does the document carry a compliant header per `document_lifecycle_guide.md` v2.6?

**Rating scheme:**

| Rating | Meaning |
|--------|---------|
| `covered` | Spec section is current, implementation exists, tests exist or are explicitly linked |
| `partial` | Spec exists and is partially implemented, or implementation exists without tests, or known minor divergence |
| `gap` | Spec section references behaviour with no implementation; or spec itself is absent for a known feature; or a known spec-to-code divergence is unresolved |

**Review cadence:** This inventory is to be refreshed at the start of each major release cycle (`run planning --version vX.Y`) and after any audit cycle (`run audit`). Minimum: once per 3 cycles.

---

## 1. API Contracts (`docs/specs/api_contracts/`)

### 1.1 `conventions.md`

| Section | Rating | Notes |
|---------|--------|-------|
| §1 Authentication & Authorization | `gap` | Explicitly "not defined" — authentication is out-of-scope by design decision but represents a real coverage gap for future multi-user work |
| §2 Standard Request/Response Formats | `covered` | Success/error envelopes implemented and consistent across all endpoints |
| §3 Error Handling Conventions | `covered` | Standard error handling implemented |
| §4 Defaults & Optional Field Behaviour | `covered` | Applied consistently |
| §5 Multi-Currency & Pricing Conventions | `covered` | GBP/USD conversion implemented |
| §6 Idempotency | `covered` | Documented and followed |
| §7 Exit & FX Rules | `covered` | Implemented in exit flows |
| §8 Validation Rules | `covered` | Implemented |
| §9 Pagination & Filtering | `partial` | Pagination not implemented (single-user scale). Acceptable for v1 but will be required pre multi-user |
| §10 Versioning | `covered` | API versioning approach documented |
| §11 Health Endpoint Exception | `covered` | Health endpoints exempt from envelope — implemented |
| §12 DELETE Response Convention | `covered` | Implemented |
| §13 Error Response Standard | `covered` | Canonical error envelope, HTTP status mapping, and usage rules in place |

**Lifecycle compliance:** Non-compliant — missing `Class`, `Status`, `Version`, `Last Updated`, `Lifecycle Guide` header block. Pre-dates lifecycle guide adoption.

---

### 1.2 `portfolio_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| GET /portfolio | `covered` | All 4 previously-missing fields (`initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value`) delivered by ST-12 (v2.0). GAP-03 resolved. |
| POST /portfolio/position | `covered` | Implemented |
| POST /portfolio/size | `covered` | Position sizing calculator implemented |
| POST /portfolio/snapshot | `covered` | Daily snapshot upsert implemented |
| GET /portfolio/history | `covered` | Snapshot history implemented |
| GET /portfolio/prospective-heat | `gap` | **Open gap (BLG-BE-02, P3).** No spec section exists in this file; no backend implementation. Referenced by ProspectiveHeatPanel. Tests skipped (`@unittest.skip TestProspectiveHeat`). ST-13 (v2.0 stretch) targets resolution. |

**Lifecycle compliance:** Non-compliant — no lifecycle header block. Pre-dates lifecycle guide adoption.

---

### 1.3 `signal_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| POST /signals/generate | `covered` | Signal generation implemented with `top_n` and `lookback_days` query params |
| GET /signals | `covered` | ST-02 (v2.0) added `top_n` and `lookback_days` query params to frontend consumption |
| PATCH /signals/{signal_id} | `covered` | Status update (dismiss, enter) implemented |
| DELETE /signals/{signal_id} | `covered` | Implemented |

**Lifecycle compliance:** Non-compliant — no lifecycle header block.

---

### 1.4 `analytics_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| GET /analytics/metrics | `covered` | Unified endpoint implemented; all major metric groups present |
| POST /validate/calculations | `covered` | Smoke-test validation endpoint implemented |
| GET /analytics/cohort | `partial` | Endpoint spec exists (§557–615). Implementation status unconfirmed. No test scenarios documented yet — ST-20 (v2.0 stretch, #80) would address the test gap. |
| GET /analytics/r-multiple-distribution | `partial` | Spec exists. Test coverage not confirmed in this audit. |
| `total_return_pct` field | `gap` | Explicitly noted in spec: "not yet returned by GET /analytics/metrics". Canonical formula documented but not implemented. No backlog item assigned. **Action: file backlog item.** |

**Lifecycle compliance:** Non-compliant — no lifecycle header block.

---

### 1.5 `reports_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| GET /reports/tax-year | `covered` | ST-03 spec (pre-completed) + ST-04 backend implementation (v2.0). Tax-year boundary, response schema, and error cases all specced and implemented. |

**Lifecycle compliance:** Partial — file has an Overview section but no formal lifecycle header block. Recommend adding `Owner`, `Class`, `Status`, `Version`, `Last Updated`, `Lifecycle Guide` to match `market_endpoints.md` pattern.

---

### 1.6 `settings_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| GET /settings | `covered` | Implemented |
| PATCH /settings/{settings_id} | `covered` | Implemented |
| POST /settings | `covered` | Implemented |
| Data model cross-reference | `covered` | `settings_model.md` registered as canonical source (ST-17 v1.9 Sprint 1) |

**Lifecycle compliance:** Partial — has `Owner`, `Status`, `Version`, `Last Updated` but missing `Class` and `Lifecycle Guide`.

---

### 1.7 `cash_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| POST /cash | `covered` | Deposit/withdrawal recording implemented |
| GET /cash | `covered` | Transaction listing implemented |
| GET /cash/summary | `covered` | Summary totals implemented |

**Lifecycle compliance:** Non-compliant — no lifecycle header block.

---

### 1.8 `position_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| GET /positions | `covered` | Full enriched position object with live prices, stops, ATR |
| POST /positions/monitor | `covered` | Daily monitoring analysis implemented |
| POST /positions/{id}/exit | `covered` | Full and partial exit implemented |
| PATCH /positions/{id} | `covered` | Journal note update implemented |

**Lifecycle compliance:** Non-compliant — no lifecycle header block.

---

### 1.9 `trade_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| GET /trades | `covered` | Trade history with statistics implemented |
| GET /trades/export/csv | `covered` | CSV export implemented |
| GET /trades/{trade_id}/reflection | `covered` | Added in v1.9 Sprint 1 (ST-02). Schema in `data_model.md v1.8`. |
| POST /trades/{trade_id}/reflection | `covered` | Added in v1.9 Sprint 1 |

**Lifecycle compliance:** Non-compliant — no lifecycle header block.

---

### 1.10 `health_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| GET /health | `covered` | Basic health check implemented |
| GET /health/details | `covered` | Dependency diagnostics implemented |

**Lifecycle compliance:** Non-compliant — no lifecycle header block.

---

### 1.11 `market_endpoints.md`

| Section | Rating | Notes |
|---------|--------|-------|
| GET /market/status | `covered` | Live SPY/FTSE market regime status implemented. Spec created ST-16 (v1.9 Sprint 1). |

**Lifecycle compliance:** Compliant — full `Owner`, `Class`, `Status`, `Version`, `Last Updated`, `Lifecycle Guide` header.

---

### 1.12 `api_changelog.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Changelog entries | `covered` | Entries present for all major contract versions through v2.0.0 |

**Lifecycle compliance:** Partial — has `Owner`, `Status`, `Version`, `Last Updated` but missing `Class` and `Lifecycle Guide`.

---

### 1.13 `README.md`

| Section | Rating | Notes |
|---------|--------|-------|
| API contracts index | `covered` | All endpoint files registered; version history maintained |

**Lifecycle compliance:** Partial — has `Owner`, `Class`, `Status`, `Version` but missing `Last Updated` and `Lifecycle Guide`.

---

## 2. Data Model (`docs/specs/data_model*.md`)

### 2.1 `data_model.md`

| Section | Rating | Notes |
|---------|--------|-------|
| §1 Portfolios table | `covered` | Schema implemented; fields documented |
| §2 Positions table | `covered` | Full schema including all stop/ATR/FX fields |
| §3 Trade History table | `covered` | Exit fields, R-multiple, reflection FK |
| §4 Cash Transactions table | `covered` | Deposit/withdrawal schema implemented |
| §5 Portfolio History table | `covered` | Snapshot schema implemented |
| §6 Settings table | `covered` | Cross-referenced to `settings_model.md` |
| §7 Signals table | `covered` | Full schema including `suggested_shares` integer constraint |
| Planned: Trade Reflections table | `covered` | Implemented in v1.9 Sprint 1. §501 "Planned Future Schema Changes" section should be updated to mark this as complete. **Action: update data_model.md §501.** |
| Planned: Alerts (v2.0) | `partial` | Schema outlined but EPIC-03 deferred to v2.1 (no async infrastructure). Remains as forward-looking documentation. |
| Planned: Multi-User (v2.0) | `gap` | v2.0 scoped this out explicitly. Multi-user target is post-v2.0. No action required this cycle. |

**Lifecycle compliance:** Non-compliant — has `Version`, `Status`, `Owner`, `Last Updated` but missing `Class` and `Lifecycle Guide`. Pre-dates lifecycle guide adoption.

---

### 2.2 `data_model/settings_model.md`

| Section | Rating | Notes |
|---------|--------|-------|
| All settings fields | `covered` | Class 1 Canonical created ST-17 (v1.9 Sprint 1). Full field names, types, validation, defaults. |

**Lifecycle compliance:** Compliant — full lifecycle header.

---

### 2.3 `data_model_positions_dictionary.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Positions table field dictionary | `covered` | Created ST-15 (v2.0). All fields documented with types, nullable, derivation. |

**Lifecycle compliance:** Compliant — full lifecycle header.

---

## 3. Metrics (`docs/specs/metrics_definitions.md`)

| Section | Rating | Notes |
|---------|--------|-------|
| Sharpe Ratio | `covered` | Sample variance method confirmed conformant (BLG-TECH-01 resolved) |
| Max Drawdown | `covered` | Formula implemented |
| Current Drawdown | `covered` | Field now returned by both `GET /portfolio` (resolved ST-12) and `GET /analytics/metrics` |
| Win Rate | `covered` | Implemented |
| Profit Factor | `covered` | Implemented |
| Capital Efficiency | `covered` | GBP-safe cost basis confirmed conformant (BLG-TECH-01 resolved) |
| R-Multiple | `covered` | Frontend-calculated from `trades_for_charts`; `trade_history.md` v1.1 adds column spec |
| Advanced Metrics Grid | `covered` | All metrics in `advanced_metrics` object implemented |
| Appendix E backlog items | `covered` | Both resolved |

**Lifecycle compliance:** Non-compliant — has `Version`, `Owner`, `Last Updated` but missing `Class`, `Status`, `Lifecycle Guide`. Also: `Owner` is listed as "Analytics Team" rather than a named governance role (non-compliant with `document_lifecycle_guide.md §7`). **Action: update Owner field to role name.**

---

## 4. Structured Logging (`docs/specs/structured_logging_standards.md`)

| Section | Rating | Notes |
|---------|--------|-------|
| Log format standards | `covered` | Implemented in backend |
| Log levels | `covered` | Implemented |
| Correlation ID generation | `covered` | HTTP request-level correlation IDs implemented |
| Async failure observability | `partial` | Standard documented for v2.0 Alerts (EPIC-03). EPIC-03 deferred to v2.1, so async job correlation IDs not yet required. This section will be activated when v2.1 async infrastructure ships. |

**Lifecycle compliance:** Compliant — full lifecycle header. Class 1 Canonical, sign-off recorded.

---

## 5. Frontend Pages (`docs/specs/frontend/pages/`)

### 5.1 `dashboard.md`

| Section | Rating | Notes |
|---------|--------|-------|
| All dashboard components | `covered` | v2.0 dashboard spec implemented (v1.9 EPIC-03). Class 1 Canonical v2.0. |

**Lifecycle compliance:** Compliant — full lifecycle header.

---

### 5.2 `positions.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Positions page | `covered` | Full positions list with enriched data implemented |
| Exit flow | `covered` | Exit modal and partial exit implemented |
| Journal fields | `covered` | Journal notes editable |

**Lifecycle compliance:** Partial — has `Owner`, `Status`, `Version`, `Last Updated` but missing `Class` and `Lifecycle Guide`.

---

### 5.3 `analytics.md`

| Section | Rating | Notes |
|---------|--------|-------|
| §1–§12 (Executive Summary through Win Rate) | `covered` | All components implemented (v1.4) |
| §13 R-Multiple Analysis | `covered` | Implemented in v1.9 |
| §14 Holding Period Analysis | `covered` | Implemented |
| §15 CohortAnalysis | `partial` | Spec exists. Component implemented. Backend endpoint (`GET /analytics/cohort`) status unconfirmed. Test scenarios not yet documented — ST-20 (#80, P3 stretch) targets this. |

**Lifecycle compliance:** Compliant — full lifecycle header. Class 1 Canonical v1.4.

---

### 5.4 `risk_dashboard.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Risk Dashboard components | `covered` | Implemented (v1.8) |
| ProspectiveHeatPanel | `partial` | Frontend component exists but backend endpoint `GET /portfolio/prospective-heat` not yet specced/implemented (see §1.2 gap, BLG-BE-02). Panel renders with degraded state. |
| §11 Deviations | `partial` | BLG-RD-01 through BLG-RD-11 active. Not all resolved. These represent known minor divergences from spec. |

**Lifecycle compliance:** Compliant — full lifecycle header.

---

### 5.5 `settings.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Settings page | `covered` | All strategy parameters, fees, UI prefs, analytics thresholds implemented |

**Lifecycle compliance:** Partial — has `Owner`, `Status`, `Version`, `Last Updated` but missing `Class` and `Lifecycle Guide`.

---

### 5.6 `signals.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Signals page with top_n/lookback_days controls | `covered` | ST-02 (v2.0) implemented controls per this spec (v0.1). |

**Lifecycle compliance:** Compliant — full lifecycle header (Class 2 Supporting, created v2.0).

---

### 5.7 `reports.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Tax Year P&L view | `covered` | ST-05 (v2.0) implemented tab + full view per this spec (v0.1). |

**Lifecycle compliance:** Partial — has lifecycle header but `Class` is listed as "Supporting Document (Class 2)" while the document has some canonical content. Review warranted at next version increment.

---

### 5.8 `trade_history.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Trade History page | `covered` | Implemented including R-Multiple column (v1.1) |

**Lifecycle compliance:** Partial — has `Owner`, `Status`, `Version`, `Last Updated` but missing `Class` and `Lifecycle Guide`.

---

### 5.9 `system_status.md`

| Section | Rating | Notes |
|---------|--------|-------|
| System Status page | `covered` | Health indicators and data source status implemented |

**Lifecycle compliance:** Partial — has `Owner`, `Status`, `Version`, `Last Updated` but missing `Class` and `Lifecycle Guide`.

---

### 5.10 `trade_reflection.md`

| Section | Rating | Notes |
|---------|--------|-------|
| Trade Reflection modal | `covered` | Implemented in v1.9 Sprint 1. Class 1 Canonical. |

**Lifecycle compliance:** Compliant — full lifecycle header.

---

## 6. Frontend Components (`docs/specs/frontend/components/`)

All five component specs (`cash_management_modal.md`, `exit_modal.md`, `journal_components.md`, `position_detail_modal.md`, `position_form.md`) are **covered** for implementation.

**Lifecycle compliance (all five):** Non-compliant — have `Owner`, `Status`, `Version`, `Last Updated` but missing `Class` and `Lifecycle Guide`. These are pre-lifecycle-guide-adoption documents.

---

## 7. Frontend Patterns (`docs/specs/frontend/patterns/`)

### 7.1 `api_dependencies.md`

**Coverage:** `partial` — Maps surfaces to endpoints. Updated to v1.1 (2026-02-19). May not reflect v2.0 additions (Reports tab, Signals controls). **Action: update api_dependencies.md at v2.0 post-ship.**

**Lifecycle compliance:** Partial — missing `Class` and `Lifecycle Guide`.

---

### 7.2 `error_handling.md`

**Coverage:** `covered` — Error handling patterns implemented consistently across all surfaces.

**Lifecycle compliance:** Non-compliant — missing `Class` and `Lifecycle Guide`.

---

### 7.3 `frontend/README.md`

**Coverage:** `covered` — Index document for frontend spec set.

**Lifecycle compliance:** Non-compliant — no lifecycle header block. Missing all required fields.

---

## 8. Gap Cross-Reference — Open Backlog Items

| Gap ID | Spec Section | Backlog Item | Status | Target |
|--------|-------------|-------------|--------|--------|
| GAP-03 | portfolio_endpoints.md — GET /portfolio 4 fields | BLG-BE-01 | **RESOLVED** — ST-12 (v2.0) | v2.0 |
| BLG-BE-02 | portfolio_endpoints.md — GET /portfolio/prospective-heat | BLG-BE-02 (P3) | **Open** — ST-13 stretch (v2.0) | v2.0 or v2.1 |
| — | analytics_endpoints.md — `total_return_pct` not returned | *(no backlog item)* | **New gap identified** — needs backlog item | v2.1 |
| — | analytics_endpoints.md — GET /analytics/cohort test coverage | ST-20 (#80, P3 stretch) | Open | v2.0 stretch |
| — | api_dependencies.md — v2.0 additions not reflected | *(no backlog item)* | **New gap identified** — needs update post-ship | v2.0 post-ship |
| — | data_model.md §501 — trade_reflections "Planned" section not updated to "complete" | *(no backlog item)* | **New gap identified** — minor doc debt | v2.1 |

---

## 9. Lifecycle Compliance Summary

**Compliant** (full header per `document_lifecycle_guide.md`):

| Document | Class | Version |
|----------|-------|---------|
| `api_contracts/market_endpoints.md` | Class 1 Canonical | v0.1 |
| `data_model/settings_model.md` | Class 1 Canonical | v0.1 |
| `data_model_positions_dictionary.md` | Class 1 Canonical | v0.1 |
| `structured_logging_standards.md` | Class 1 Canonical | v0.1.0 |
| `frontend/pages/analytics.md` | Class 1 Canonical | v1.4 |
| `frontend/pages/dashboard.md` | Class 1 Canonical | v2.0 |
| `frontend/pages/risk_dashboard.md` | Class 1 Canonical | v0.1.8 |
| `frontend/pages/signals.md` | Class 2 Supporting | v0.1 |
| `frontend/pages/reports.md` | Class 2 Supporting | v0.1 |
| `frontend/pages/trade_reflection.md` | Class 1 Canonical | v0.1 |

**Non-compliant** (missing `Class` field, `Lifecycle Guide` reference, or both):

| Document | Missing Fields | Priority |
|----------|---------------|----------|
| `api_contracts/conventions.md` | Class, Status, Version, Last Updated, Lifecycle Guide | P2 |
| `api_contracts/portfolio_endpoints.md` | All header fields | P2 |
| `api_contracts/signal_endpoints.md` | All header fields | P2 |
| `api_contracts/analytics_endpoints.md` | All header fields | P2 |
| `api_contracts/cash_endpoints.md` | All header fields | P2 |
| `api_contracts/health_endpoints.md` | All header fields | P2 |
| `api_contracts/position_endpoints.md` | All header fields | P2 |
| `api_contracts/trade_endpoints.md` | All header fields | P2 |
| `api_contracts/reports_endpoints.md` | All header fields | P2 |
| `api_contracts/settings_endpoints.md` | Class, Lifecycle Guide | P3 |
| `api_contracts/api_changelog.md` | Class, Lifecycle Guide | P3 |
| `api_contracts/README.md` | Last Updated, Lifecycle Guide | P3 |
| `data_model.md` | Class, Lifecycle Guide | P2 |
| `metrics_definitions.md` | Class, Status, Lifecycle Guide; Owner is team not role | P2 |
| `frontend/pages/positions.md` | Class, Lifecycle Guide | P3 |
| `frontend/pages/settings.md` | Class, Lifecycle Guide | P3 |
| `frontend/pages/system_status.md` | Class, Lifecycle Guide | P3 |
| `frontend/pages/trade_history.md` | Class, Lifecycle Guide | P3 |
| `frontend/components/cash_management_modal.md` | Class, Lifecycle Guide | P3 |
| `frontend/components/exit_modal.md` | Class, Lifecycle Guide | P3 |
| `frontend/components/journal_components.md` | Class, Lifecycle Guide | P3 |
| `frontend/components/position_detail_modal.md` | Class, Lifecycle Guide | P3 |
| `frontend/components/position_form.md` | Class, Lifecycle Guide | P3 |
| `frontend/patterns/api_dependencies.md` | Class, Lifecycle Guide | P3 |
| `frontend/patterns/error_handling.md` | Class, Lifecycle Guide | P3 |
| `frontend/README.md` | All header fields | P3 |

**Total docs audited:** 38
**Compliant:** 10 (26%)
**Non-compliant:** 28 (74%)

**Note:** All non-compliant documents pre-date lifecycle guide v2.0 adoption (prior to 2026-03-02). The compliance deficit is a known doc-debt item, not a governance failure. Remediation is a bulk-update task.

---

## 10. Actions Identified

| # | Action | Owner | Priority | Target |
|---|--------|-------|----------|--------|
| A-01 | File backlog item for `total_return_pct` implementation gap in `GET /analytics/metrics` | Head of Specs Team | P3 | v2.1 backlog |
| A-02 | Update `api_dependencies.md` to reflect v2.0 additions (Reports page, Signals controls) | Frontend Specifications & UX Documentation Owner | P3 | v2.0 post-ship |
| A-03 | Update `data_model.md` §501 — mark Trade Reflections "Planned" entry as complete | Data Model & Domain Schema Owner | P3 | v2.1 |
| A-04 | Bulk lifecycle header remediation for 28 non-compliant spec docs (add `Class` + `Lifecycle Guide`) | Head of Specs Team | P2 | v2.1 sprint |
| A-05 | Update `metrics_definitions.md` Owner from "Analytics Team" to named governance role | Metrics Definitions & Analytics Canonical Owner | P2 | v2.1 sprint |
| A-06 | Resolve ST-20 (#80) — author CohortAnalysis test scenarios for `analytics.md §15` | QA & Testing Owner | P3 | v2.0 stretch |
| A-07 | Resolve ST-13 (#83) — spec and implement `GET /portfolio/prospective-heat` | Head of Engineering + Head of Specs Team | P3 | v2.0 stretch or v2.1 |

---

## 11. Review Cadence

| Trigger | Action |
|---------|--------|
| Start of each major release cycle (`run planning --version vX.Y`) | Review §8 Gap Cross-Reference; check if any "new gap identified" actions have been filed |
| Every 3 cycles (`run audit`) | Full re-audit of all sections; refresh ratings; update §9 compliance table |
| Any new Class 1 spec created | Register in this inventory's §1–7 immediately (same commit as spec creation) |
| Any known gap resolved | Update rating in §1–7 and close §8 row in same commit |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-17 | Initial inventory. ST-17 / EPIC-05 (v2.0). 38 documents audited. 7 actions identified. Head of Specs Team. |
