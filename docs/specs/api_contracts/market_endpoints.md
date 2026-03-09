**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-03-08
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# market_endpoints.md

## Overview

This document defines the **Market** domain endpoint:

- Retrieve current market regime and live FX rate

This endpoint provides the data used by the Signals page to display real-time market conditions. It does not modify any state.

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /market/status](#get-marketstatus)

---

## GET /market/status

**Purpose**

Return the current market regime for SPY (US) and FTSE (UK) indices, each expressed as a risk-on / risk-off classification based on the 200-day moving average, plus the live GBP/USD FX rate.

This endpoint is used by:
- Signals page: to display current regime before signal generation
- Position analysis: as context for exit recommendations

**Method & Path**

- `GET /market/status`

**Idempotency**

- Safe to refresh (read-only). Each call fetches live data.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "spy": {
    "price": 542.31,
    "ma200": 489.17,
    "is_risk_on": true
  },
  "ftse": {
    "price": 8143.22,
    "ma200": 7891.45,
    "is_risk_on": true
  },
  "fx_rate": 1.2847,
  "last_updated": "2026-03-08T10:30:00.123456"
}
```

#### Field notes

| Field | Type | Description |
|-------|------|-------------|
| `spy.price` | float | Current SPY ETF price (USD), rounded to 2 decimal places |
| `spy.ma200` | float | SPY 200-day moving average (USD), rounded to 2 decimal places |
| `spy.is_risk_on` | boolean | `true` if SPY price > MA200 (risk-on signal for US market) |
| `ftse.price` | float | Current FTSE 100 index price (GBP), rounded to 2 decimal places |
| `ftse.ma200` | float | FTSE 100 200-day moving average (GBP), rounded to 2 decimal places |
| `ftse.is_risk_on` | boolean | `true` if FTSE price > MA200 (risk-on signal for UK market) |
| `fx_rate` | float | Live GBP/USD exchange rate, rounded to 4 decimal places |
| `last_updated` | string (ISO 8601) | Timestamp of when this response was generated (UTC) |

#### Regime semantics

| Condition | `is_risk_on` | Interpretation |
|-----------|-------------|---------------|
| Price > MA200 | `true` | Risk-on: market is above long-term trend; strategy may hold or enter positions |
| Price ≤ MA200 | `false` | Risk-off: market is below long-term trend; strategy recommends caution / exits |

Regime classification is per `docs/claude/strategy/strategy_rules.md`. The MA period (200 days) is a strategy parameter.

### Errors

Errors use the standard error envelope from **conventions.md**.

| HTTP Status | Condition |
|-------------|-----------|
| `500` | External data fetch failure (Yahoo Finance unavailable, FX rate fetch failed) |

On error, the response body follows the standard error envelope:
```json
{
  "status": "error",
  "message": "Failed to fetch market status: <detail>"
}
```

### Behaviour notes

- External data is fetched live on each call. There is no caching.
- If the external data source (Yahoo Finance) is unavailable, the endpoint returns HTTP 500 with an error message.
- The `fx_rate` is also used by `GET /portfolio` (returned in the portfolio response as `live_fx_rate`). Both calls fetch live data independently.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-08 | Initial canonical specification. Endpoint existed in implementation since v1.7; spec authored per ST-16 (v1.9 Sprint 1, EPIC-06). |
