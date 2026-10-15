**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 0.3
**Last Updated:** 2026-10-13 (ST-17, EPIC-03, v9.12, BLG-BE-146 — added GET /market/atr/{ticker}, the read-only 14-day ATR preview for Trade Entry); prior — 2026-10-08 (ST-19, EPIC-03, v9.11, BLG-BE-140 — added GET /market/regime, the read-only regime source for the Dashboard regime widgets); prior — 2026-03-08 (initial canonical specification)
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
- [GET /market/regime](#get-marketregime)
- [GET /market/atr/{ticker}](#get-marketatrticker)

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

## GET /market/regime

**Purpose**

Return the US and UK market regime (risk-on / risk-off) for display, without running position analysis. Added in v9.11 (ST-19, BLG-BE-140). The Dashboard regime widgets (`MarketRegime.list` in `src/api/base44Client.js`) previously read the regime from `GET /positions/analyze`, which fetches live prices and ATR for every open position and writes stops, so viewing the regime could move a stop.

**Method & Path**

- `GET /market/regime`

**Idempotency**

- Read-only, with no side effects. It reads `check_market_regime()`'s result, the same source `GET /positions/analyze` and `GET /market/status` use, which is cached for 5 minutes. It reads no position, writes nothing and fetches no FX rate.

### Request

No parameters.

### Response (200)

```json
{
  "status": "ok",
  "data": [
    { "market": "US", "status": "risk_on" },
    { "market": "UK", "status": "risk_off" }
  ],
  "as_of": "2026-10-08T09:15:02.123456"
}
```

#### Field notes

| Field | Type | Description |
|-------|------|-------------|
| `data[].market` | string | `US` (SPY) or `UK` (FTSE) |
| `data[].status` | string | `risk_on` when the index is above its 200-day moving average, `risk_off` otherwise (`strategy_rules.md` market regime rule; the same classification as `GET /market/status`'s `is_risk_on`) |
| `as_of` | ISO 8601 datetime \| null | When the regime was computed (the cached result's timestamp) |

If the index data is unavailable, `check_market_regime()` defaults to risk-on for that market, as it does for every other caller.

### Errors

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Unexpected failure computing the regime |

```json
{
  "status": "error",
  "message": "Internal server error"
}
```

---

## GET /market/atr/{ticker}

**Purpose**

Return a ticker's 14-day ATR so Trade Entry can show the system initial stop, the risk and the suggested shares before save. Added in v9.12 (ST-17, BLG-BE-146). Design source: `docs/design/2026-10-12__release-v9.12/trade-entry-atr-preview/decision_record.md`. Frontend spec: `docs/specs/frontend/components/position_form.md` v1.9 §ATR (14-day), §Initial Stop.

**Method & Path**

- `GET /market/atr/{ticker}?market=UK|US`

**Idempotency**

- Read-only, with no side effects. It writes nothing and reads no position. Each call fetches price history.

### Request

| Parameter | In | Type | Required | Description |
|-----------|----|------|----------|-------------|
| `ticker` | path | string | Yes | Ticker symbol. A UK ticker may be given with or without `.L`. |
| `market` | query | string | Yes | `UK` or `US`. A ticker ending `.L` is treated as `UK` whatever `market` says, as `POST /portfolio/position` does. |

The ticker is normalised exactly as `POST /portfolio/position` normalises it (upper case; `.L` added for UK), and the ATR is fetched through the same `calculate_atr()` call. The stop computed from this ATR (`entry − 5 × atr`, `strategy_rules.md` §5, §11) therefore equals the `initial_stop` that save stores for the same inputs, unless prices update in between.

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "ticker": "AAPL",
    "market": "US",
    "atr": 3.1372,
    "atr_period": 14,
    "as_of": "2026-10-13T10:15:02.123456+00:00"
  }
}
```

#### Field notes

| Field | Type | Description |
|-------|------|-------------|
| `ticker` | string | Display ticker (no `.L` suffix for UK) |
| `market` | string | `UK` or `US` after normalisation |
| `atr` | float \| null | 14-day ATR in native currency (GBP for UK, USD for US), not rounded. `null` when it cannot be fetched; save then falls back to 2% of entry (`atr_source = fallback`). |
| `atr_period` | integer | Always `14` |
| `as_of` | ISO 8601 datetime (UTC) | When the ATR was fetched |

Trade Entry never places the returned ATR into its ATR input, so `atr_source` at save stays `fetched` (the field is submitted blank).

### Errors

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `market` is not `UK` or `US`, or the ticker is blank |
| `500` | Unexpected failure fetching the ATR |

```json
{
  "status": "error",
  "message": "market must be 'UK' or 'US'"
}
```

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-08 | Initial canonical specification. Endpoint existed in implementation since v1.7; spec authored per ST-16 (v1.9 Sprint 1, EPIC-06). |
| 0.2 | 2026-10-08 | ST-19 (EPIC-03, v9.11, BLG-BE-140): Added `GET /market/regime`, a read-only regime source, so viewing the regime no longer runs the stop-writing `GET /positions/analyze`. |
| 0.3 | 2026-10-13 | ST-17 (EPIC-03, v9.12, BLG-BE-146): Added `GET /market/atr/{ticker}`, the read-only 14-day ATR preview that lets Trade Entry show the stop, risk and size before save. |
