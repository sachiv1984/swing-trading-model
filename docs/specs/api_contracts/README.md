# README.md

## Momentum Trading Assistant — API Contracts

**Owner:** API Contracts & Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 2.1.1
**Last Updated:** 2026-03-20
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

This directory contains the **backend API contracts** for the *Momentum Trading Assistant* web application.

The system is a **decision-support tool**, not an automated trading bot. All trading logic is deterministic and executed server-side. The backend is the single source of truth; the frontend is responsible only for display, user input, and orchestration.

---

## Audience

These API contracts are intended for:

- **Frontend engineers** integrating the web UI with the backend APIs
- **Backend engineers** implementing and maintaining API behavior
- **QA and automation engineers** validating contract compliance and deterministic behavior

---

## How to Use This Documentation

1. **Start with `conventions.md`**
   This file defines global rules that apply to *all* endpoints, including:
   - Authentication and authorization
   - Request and response envelopes
   - Error semantics
   - Pagination, filtering, and versioning
   - Common headers and HTTP status codes

2. **Navigate to the relevant domain file**
   Each domain-specific file contains only the endpoints for that functional area, making reviews and ownership clear.

3. **Treat these files as contracts**
   - Frontend clients must not infer or calculate values that are provided by the backend.
   - Backend changes that affect request/response shapes must be reflected here.

---

## Base URLs

- **Production:** `https://api.example.com`
- **Development:** `http://localhost:8000`

---

## Core Design Principles

The following principles apply across all APIs:

- **Backend as single source of truth**
  - All calculations (ATR, stops, P&L, FX conversions, regime detection) are server-side.
  - Frontend must never calculate or derive these values.

- **Human-in-the-loop execution**
  - The system never executes trades automatically.
  - Users must explicitly confirm exits and provide actual broker execution prices.

- **Deterministic behavior**
  - Identical inputs always produce identical outputs.
  - No experiments, A/B testing, or non-deterministic logic.

- **Multi-currency correctness**
  - Monetary values are returned in both GBP and native currency where applicable.
  - Stops are stored, enforced, and trailed **only in native currency**.
  - FX rate changes must never move stop levels.

- **Explainability**
  - Recommendations, stop movements, and exit signals include clear reasoning.

---

## Documentation Structure

The API contracts are split by concern to support incremental review and clear ownership.

### Cross-cutting standards
- **`conventions.md`**
  Global API rules and conventions that apply to every endpoint.

### Domain-specific endpoints
- **`portfolio_endpoints.md`**
  Portfolio overview, position creation, position sizing calculator, daily snapshots, and portfolio history (`GET /portfolio/history`). The portfolio overview returns a summary position shape; use `position_endpoints.md` for the full enriched position object.

- **`position_endpoints.md`**
  Open positions (full detail including native prices, stop context, ATR, FX, and journal fields), daily analysis, exits, notes, tags, and tag discovery.

- **`trade_endpoints.md`**
  Closed trade history and trade-level statistics.

- **`cash_endpoints.md`**
  Deposits, withdrawals, cash transactions, and cash summaries.

- **`settings_endpoints.md`**
  Strategy configuration and fee parameters (`GET /settings`, `PUT /settings`). Covers grace period, ATR multipliers, commissions, stamp duty, and analytics thresholds.

- **`analytics_endpoints.md`**
  Comprehensive trading analytics via `GET /analytics/metrics` (executive metrics, advanced metrics, monthly trends, top performers, drawdown, and more), plus `POST /validate/calculations` for smoke-testing metric correctness. Validation results include per-metric severity and a `by_severity` summary breakdown.

- **`signal_endpoints.md`**
  Signal generation, signal listing, signal status updates, and signal deletion.

- **`health_endpoints.md`**
  Health checks, diagnostics, and endpoint test execution.

- **`market_endpoints.md`**
  Market regime status (`GET /market/status`): SPY and FTSE regime classification vs 200-day MA, plus live GBP/USD FX rate.

- **`reports_endpoints.md`**
  Tax-year P&L statement (`GET /reports/tax-year`): structured financial record of all realised gains and losses within a specified UK tax year (6 April to 5 April). Includes per-trade breakdown, summary totals, and indicative unrealised P&L. For UK-based accounts only. Not a substitute for qualified tax advice.

- **`alerts_endpoints.md`**
  Alerts & Notifications domain. Alert rules CRUD (`GET/POST/PATCH/DELETE /alerts/rules`); alert evaluation engine trigger (`POST /alerts/evaluate`); notification feed (`GET /notifications`, `PATCH /notifications/{id}`, `POST /notifications/mark-all-read`); notification preferences (`GET/PATCH /notifications/preferences`). Delivery via FastAPI BackgroundTasks per ADR-003.

Each endpoint file follows a consistent structure:
- HTTP method and path
- Purpose and behavior
- Request schema (path, query, body)
- Response schema (success and error)
- Validation rules and constraints
- Example requests and responses

---

## Versioning

- **Current contract version:** 2.1.1
- **Change type:** v2.1 Sprint — ST-13 (reports_endpoints.md v0.3 — format=csv added to GET /reports/tax-year).
- **Previous version:** 2.1.0

**Error Response Standard:** Canonical error response rules are defined in `conventions.md §13`. All endpoint error sections reference this standard via their "Errors use the standard error envelope from conventions.md" clause.

### Changelog (Summary)

- **2.1.1 (2026-03-20)**
- reports_endpoints.md v0.3: `format=csv` added to `GET /reports/tax-year`. 5-row metadata block + 17-column trades table. `format` validation tightened (unknown value → 400). ST-13 — v2.1 release planning cycle 2026-03-18__release-v2.1.

- **2.1.0 (2026-03-20)**
- alerts_endpoints.md: created — full Alerts & Notifications domain. Alert rules CRUD, alert evaluation, notification feed (paginated), mark-read, notification preferences. Delivery via FastAPI BackgroundTasks per ADR-003. Data model: `data_model.md` v1.9 (3 new tables). ST-02 — v2.1 release planning cycle 2026-03-18__release-v2.1.

- **2.0.0 (2026-03-17)**
- reports_endpoints.md: created — `GET /reports/tax-year` endpoint. Tax-year P&L statement for UK tax years (6 April to 5 April). Attribution by `exit_date`. Response includes `tax_year_start`, `tax_year_end`, `tax_year_label`, `generated_at`, summary totals (realised P&L, gross profit/loss, win/loss counts, win rate, estimated unrealised P&L), and full per-trade breakdown. Future year returns 400. UK-only scope. ST-03 — v2.0 release planning cycle 2026-03-17__release-v2.0.


- **1.8.4 (2026-02-25)**
- trade_endpoints.md: added GET /trades/export/csv endpoint. Returns full closed trade history as text/csv attachment. 14 columns confirmed in decisions record D5. No request parameters in v1.6.1. openapi.yaml updated in same PR. QWB BLG-FEAT-07, decision D5.

- **1.8.3 (2026-02-25)**
- position_endpoints.md: added grace_days_remaining (integer | null) to GET /positions response. Derived server-side as max(0, 10 - holding_days) when grace_period = true; null otherwise. Always present. No data model change required. QWB BLG-FEAT-06, decision D4.

- **1.8.2 (2026-02-25)**
-  portfolio_endpoints.md: added current_drawdown_percent (float, ≤0.0, GBP percentage) and peak_portfolio_value (float, GBP) to GET /portfolio response data object. Both fields always present; default 0.0 when no portfolio_history exists. QWB BLG-FEAT-01, decision D1.

- **1.8.1 (2026-02-21)**
  - `analytics_endpoints.md`: added `severity` field to each `POST /validate/calculations` validation result object (values: `critical` | `high` | `medium` | `low`); added `by_severity` object to `summary` with `total`/`passed`/`warned`/`failed` counts per tier; added severity model reference table mapping metrics to severity tiers and required actions on failure; updated metrics validated table to include severity column and `capital_efficiency` row (previously absent from table); updated response example; removed resolved known limitation entries for Sharpe variance and capital efficiency (resolved in BLG-TECH-01). This is the canonical contract spec for BLG-TECH-02 engineering implementation.
  - `docs/reference/openapi.yaml`: version bumped to 1.8.1; `ValidationResponse` schema description updated to note `severity` field and `by_severity` summary additions.

- **1.8.0 (2026-02-19)**
  - `portfolio_endpoints.md`: added `POST /portfolio/size` — Position Sizing Calculator endpoint. Returns suggested share quantity, risk amount, stop distance, estimated cost, fees, FX rate used, and cash feasibility for a prospective new position. No state mutation. Idempotent. Authoritative backend calculation per `strategy_rules.md §4.1`. Includes three distinct response shapes: valid result, insufficient cash (with `max_affordable_shares` always present), and invalid inputs (with machine-readable `reason` code and development-only `reason_detail`).
  - `settings_endpoints.md`: added `default_risk_percent` field to `GET /settings` response and `PUT /settings` request/response. Type: float. Default: `1.00`. Constraint: > 0 and ≤ 100. Represents the pre-population default for the Position Sizing Calculator risk percentage input — a user preference, not an enforced limit.
  - `docs/reference/openapi.yaml`: updated in alignment with the above contract changes per governance rules.

- **1.7.0 (2026-02-17)**
  - `analytics_endpoints.md`: removed stale editorial note from overview; added `entry_price`, `exit_price`, `stop_price` to `trades_for_charts` schema with note explaining client-side R-multiple use
  - `position_endpoints.md`: added `pnl_percent` field note to `GET /positions` response
  - `portfolio_endpoints.md`: added `pnl_percent` field note to position summary object in `GET /portfolio` response
  - `conventions.md`: added Section 12 — DELETE response convention (shape, non-idempotency rule)

- **1.6.0 (2026-02-17)**
  - `settings_endpoints.md` created — `GET /settings` and `PUT /settings` were previously undocumented
  - `conventions.md`: removed stale version number
  - `health_endpoints.md`: corrected stale version in response examples; added `version` field note; updated `POST /test/endpoints` example
  - `position_endpoints.md`: removed `initial_stop_native`; added field notes table; added `exit_note` field note; added cross-reference to `GET /portfolio`
  - `portfolio_endpoints.md`: added note on position summary depth; added field omission table; added snapshot note
  - `signal_endpoints.md`: added `DELETE /signals/{signal_id}`
  - `trade_endpoints.md`: added `holding_days` to response schema; added field notes table; clarified `exit_reason` null normalisation

- **1.5.0 (2026-02-17)**
  - `analytics_endpoints.md` rewritten to reflect the completed implementation:
    - Five planned endpoints replaced by unified `GET /analytics/metrics?period=`
    - Full nested response structure documented
    - `POST /validate/calculations` added
    - Known limitations and backlog items recorded
  - README: `GET /portfolio/history` correctly attributed to `portfolio_endpoints.md`
  - README: `analytics_endpoints.md` description updated to reflect actual scope

- **1.4.1 (2026-02-15)**
  - Complete endpoint specifications
  - Full request/response examples
  - Journal and tag endpoints fully documented
  - No breaking changes

- **1.4.0 (2026-02-01)**
  - Trade journal support
  - Position tagging
  - Entry and exit notes

---

## Guiding Rule

If a behavior, field, or calculation is not explicitly documented in these contracts, **clients must not assume it exists**.
