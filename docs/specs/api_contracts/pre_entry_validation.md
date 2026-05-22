# pre_entry_validation.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0.0
**Last Updated:** 2026-05-22
**Shipped:** v3.8 — ST-02, EPIC-01, cycle 2026-05-19__release-v3.8
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines the **Pre-Entry Validation** endpoint — the Arc 5 Strategy Integrity advisory rule check run before a trade plan is submitted (SI-01).

The pre-entry validation panel checks 5 strategy rules and returns advisory results. **All results are non-blocking.** No result prevents a trade plan from being submitted or executed. The endpoint is decision support only, consistent with strategy_rules.md §3 and §4.1.7.

**§13 compliance:** This endpoint is decision support only — not a submission gate. No result from this endpoint prevents or blocks any user action.

**Decision record:** `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`

**Strategy reference:** `claude/strategy/strategy_rules.md §4.2`

**Backend implementation:** `backend/routers/pre_entry_validation.py`

Global response envelopes, error shape, and defaults are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /portfolio/pre-entry-validation](#get-portfoliopre-entry-validation)

---

## GET /portfolio/pre-entry-validation

**Purpose**

Returns an advisory pre-entry validation result for a proposed position. Runs 5 strategy checks and aggregates a non-binding advisory status.

**Method & Path**

- `GET /portfolio/pre-entry-validation`

**Idempotency**

- Safe and idempotent for the same market/portfolio state. Results may differ across calls if portfolio state changes (live prices, open positions, cash balance, regime). Does not mutate state.

### Request

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| ticker | string | Yes | — | Ticker symbol |
| quantity | float | Yes | — | Proposed number of shares |
| market | string | No | `US` | Market: `US` or `UK` |
| entry_price | float | No | — | Enables sizing validity check (strategy_rules.md §4.2.5 / §4.1.4) |
| stop_price | float | No | — | Enables sizing validity check (strategy_rules.md §4.2.5 / §4.1.4) |

Both `entry_price` and `stop_price` must be supplied together to activate the sizing validity check; supplying only one returns `skipped` for that check.

### Response (200 OK)

```json
{
  "status": "ok",
  "data": {
    "ticker": "AAPL",
    "market": "US",
    "quantity": 10,
    "advisory_status": "warn",
    "override_required": true,
    "checks": [
      {
        "rule": "regime_gate",
        "status": "pass",
        "detail": "US market is Risk-On (SPY above 200-day MA)",
        "severity": "fail"
      },
      {
        "rule": "cash_constraint",
        "status": "pass",
        "detail": "Estimated cost £2,150.00 within available cash £5,000.00",
        "severity": "fail",
        "estimated_cost_gbp": 2150.0,
        "available_cash_gbp": 5000.0
      },
      {
        "rule": "sector_concentration",
        "status": "warn",
        "detail": "Projected Technology sector allocation 32.4% would exceed 30% advisory limit",
        "severity": "warn",
        "sector": "Technology",
        "projected_sector_pct": 32.4,
        "threshold_pct": 30.0
      },
      {
        "rule": "earnings_proximity",
        "status": "pass",
        "detail": "Next earnings 2026-07-30 (71 days) — outside 5-day proximity window",
        "severity": "warn",
        "earnings_date": "2026-07-30",
        "days_until_earnings": 71
      },
      {
        "rule": "sizing_validity",
        "status": "skipped",
        "detail": "Provide entry_price and stop_price query params for sizing validity check",
        "severity": "fail"
      }
    ]
  }
}
```

### Response Fields — `data`

| Field | Type | Description |
|-------|------|-------------|
| ticker | string | Ticker from query |
| market | string | Market from query — `US` or `UK` (uppercased) |
| quantity | float | Quantity from query |
| advisory_status | string | Aggregate status: `pass` \| `warn` \| `fail`. Excludes `skipped` checks from aggregation. Rule: `fail` > `warn` > `pass`. |
| override_required | boolean | `true` when `advisory_status` is `warn` or `fail` |
| checks | array | Per-rule check results — always 5 elements, one per rule |

### Response Fields — `checks[]`

| Field | Type | Description |
|-------|------|-------------|
| rule | string | Rule identifier — see Rules table |
| status | string | `pass` \| `warn` \| `fail` \| `skipped` |
| detail | string | Human-readable advisory explanation |
| severity | string | Worst-case severity of this rule type: `fail` or `warn` (independent of actual status) |

Additional fields appear on specific rules when applicable (see Rules table).

### Rules

Five rules are always evaluated and always returned, in this order:

| # | Rule | Strategy ref | Severity | UK applicable | Additional fields |
|---|------|-------------|----------|---------------|-------------------|
| 1 | `regime_gate` | §4.2.1, §8.2 | fail | Yes (FTSE 100 200-day MA) | — |
| 2 | `cash_constraint` | §4.2.4, §4.1.6 | fail | Yes | `estimated_cost_gbp`, `available_cash_gbp` |
| 3 | `sector_concentration` | §4.2.2 | warn | Yes | `sector`, `projected_sector_pct`, `threshold_pct` |
| 4 | `earnings_proximity` | §4.2.3 | warn | No — `skipped` for UK | `earnings_date`, `days_until_earnings` |
| 5 | `sizing_validity` | §4.2.5, §4.1.4 | fail | Yes | `stop_distance` |

#### Rule details

**regime_gate** — checks whether the market is Risk-On (index above 200-day MA). US: SPY; UK: FTSE 100. Status `fail` if Risk-Off. Status `skipped` if regime data unavailable.

**cash_constraint** — checks whether the estimated cost of the proposed position is within available cash. Estimated cost = `quantity × live_price` (converted to GBP at live FX rate for US). Status `fail` if estimated cost > available cash. Status `skipped` if live price or portfolio unavailable.

**sector_concentration** — checks projected sector allocation post-entry against the 30% advisory limit (strategy_rules.md §4.2.2). Status `warn` if projected allocation ≥ 30%. Status `skipped` if sector data or live price unavailable.

**earnings_proximity** — US tickers only. Checks whether earnings are within 5 days (strategy_rules.md §4.2.3). Status `warn` if within window. Status `skipped` for UK tickers or when earnings data unavailable.

**sizing_validity** — checks stop distance validity (entry_price > stop_price > 0). Status `fail` if stop distance ≤ 0 or if either price ≤ 0. Status `skipped` if `entry_price` or `stop_price` not supplied.

### `skipped` Status

A `skipped` status means the data required for the check was unavailable or the check does not apply. Skipped checks are excluded from `advisory_status` aggregation — they do not influence the overall result. Common causes:

| Rule | Skipped when |
|------|-------------|
| `regime_gate` | Regime service unavailable |
| `cash_constraint` | Live price unavailable or portfolio not found |
| `sector_concentration` | Sector data or live price unavailable, or portfolio value is zero |
| `earnings_proximity` | UK ticker; or earnings data service unavailable |
| `sizing_validity` | `entry_price` or `stop_price` not supplied |

### Override Acknowledgement

When `override_required` is `true`, the frontend advisory panel displays an acknowledgement prompt. The acknowledgement is recorded on the trade plan object as metadata (ST-03) and creates a `pre_entry_override` event in the Red Flag Journal (SI-03). The acknowledgement has no effect on any calculation.

### Errors

| Code | Condition |
|------|-----------|
| 422 | Missing required query params — `ticker` or `quantity` not supplied |

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-05-22 | Initial contract authored — spec debt closure for SI-01 (shipped v3.8). Content extracted from portfolio_endpoints.md §GET /portfolio/pre-entry-validation and expanded with detailed per-rule documentation, skipped status table, sizing validity parameter rules, and override acknowledgement path. BLG-SPEC-34. Authority: API Contracts & Documentation Owner (OA-02, 2026-05-22__scheduled). |
