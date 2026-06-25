# signal_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.6
**Last Updated:** 2026-06-24
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines **Signal** domain endpoints:

- Generate momentum signals
- List signals (optionally filtered by status)
- Update signal status
- Delete a signal

Global response envelopes, error shape, defaults, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

> **Data model note:** The `signals` table schema is formally documented in `data_model.md` Section 7. Key design points relevant to these endpoints: a `UNIQUE(portfolio_id, ticker, signal_date)` constraint prevents duplicate signal records for the same ticker on the same day; `position_id` is only set when `status = 'entered'`; `suggested_shares` is always an integer (whole shares only at generation time).

---

## Endpoints

- [POST /signals/generate](#post-signalsgenerate)
- [POST /signals/rebalance-exit](#post-signalsrebalance-exit)
- [GET /signals](#get-signals)
- [PATCH /signals/{signal_id}](#patch-signalssignal_id)
- [DELETE /signals/{signal_id}](#delete-signalssignal_id)

---

## POST /signals/generate

**Purpose**

Generate a ranked set of momentum signals using deterministic server-side logic.

- Returns a summary (counts, date, available cash, market regime) and an array of generated signals.
- Signals may be marked as already held if a matching open position exists.

**Method & Path**

- `POST /signals/generate`

**Idempotency**

- Not explicitly classified. Treat as a server-side generation action that returns current deterministic outputs based on live market data. Repeated calls on the same day may return different rankings if prices have changed. The `UNIQUE(portfolio_id, ticker, signal_date)` database constraint prevents duplicate signal records for the same ticker on the same day — re-running generation does not accumulate duplicates.

### Request

#### Query parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lookback_days` | integer | No | `252` | Momentum lookback period in days |
| `top_n` | integer | No | `5` | Number of signals to generate |

No request body.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "signals_generated": 5,
  "new_signals": 4,
  "already_held": 1,
  "signal_date": "2026-02-17",
  "fx_rate": 1.3650,
  "available_cash": 5000.00,
  "market_regime": {
    "spy_risk_on": true,
    "ftse_risk_on": true
  },
  "signals": [
    {
      "id": "950e8400-e29b-41d4-a716-446655440000",
      "ticker": "TSLA",
      "market": "US",
      "rank": 1,
      "momentum_percent": 45.2,
      "current_price": 850.00,
      "price_gbp": 623.00,
      "atr_value": 18.50,
      "volatility": 2.2,
      "initial_stop": 780.00,
      "status": "new",
      "allocation_gbp": 1000.00,
      "suggested_shares": 1,
      "total_cost": 986.00,
      "signal_date": "2026-02-17",
      "created_at": "2026-02-17T10:30:00Z"
    }
  ]
}
```

#### Field notes

| Field | Notes |
|-------|-------|
| `suggested_shares` | Always an integer (whole shares). Fractional share sizing is not supported in signal generation. Actual position entry via `POST /portfolio/position` supports fractional shares |
| `current_price` | Native currency price at signal generation time. Point-in-time — will diverge from live price as time passes. Do not use as a live price |
| `price_gbp` | GBP equivalent at signal generation time. Point-in-time |
| `atr_value` | ATR at generation time. Stored for auditability; not updated after generation |
| `initial_stop` | Suggested stop in native currency: `current_price − (atr_multiplier_initial × ATR)`. Uses `atr_multiplier_initial` at generation time |
| `volatility` | Volatility measure computed at generation time. Stored for auditability; not used for position sizing |
| `allocation_gbp` | Estimated GBP cost of the inv-vol position size (from `sizing_service.size_batch_inv_vol()` — includes estimated fees). (v6.2 ST-04 BLG-FEAT-48: changed from fixed risk-based `size_position()` to inverse-volatility batch sizing. Manual sizing via `POST /portfolio/size` remains unchanged.) |
| `relative_strength_pct` | **Supplementary (ST-09, display-only).** Stock momentum % minus benchmark momentum % over `lookback_days`. US benchmark: SPY; UK benchmark: ^FTSE. Labelled "vs. benchmark (informational)" in UI. Does **not** affect `rank` or signal ordering. `null` if benchmark data unavailable. |
| `week52_high_proximity_pct` | **Supplementary (ST-09, display-only).** `(current_native_price − 52w_high) / 52w_high × 100`. Negative value means price is below the 52-week high. `null` if insufficient history. |
| `avg_daily_volume_20d` | **Supplementary (ST-09, display-only).** Average daily trading volume over the last 20 trading days (integer, native exchange units). `null` if data unavailable. |
| `price_vs_50d_ma` | **Supplementary (ST-09, display-only).** `(current_native_price − 50d_MA) / 50d_MA × 100`. Positive = above MA, negative = below MA. Does **not** affect `rank`. `null` if insufficient history. |
| `reason` | Human-readable sizing note. Set when sizing produces `suggested_shares = 0` (e.g. invalid initial stop, or `sizing_service.size_position()` returns `valid: false`). `null` when sizing completes normally. |

### Validation rules & constraints

- `lookback_days` must be a positive integer when provided.
- `top_n` must be a positive integer when provided.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## POST /signals/rebalance-exit

**Purpose** (v6.2 ST-03 BLG-FEAT-47)

Generates `exit_rebalance` signals on the last trading day of each calendar month for open positions not in the current top-5 momentum list.

**Method & Path**

- `POST /signals/rebalance-exit`

**Logic:**
1. If today is not the last trading day of the month (weekend-aware), returns immediately with `is_last_trading_day: false` and no records created.
2. Fetches the most recent momentum signal batch to determine the current top-5 tickers.
3. For each open position NOT in the top-5 list, creates an `exit_rebalance` signal.
4. Deduplication: skips any position whose `current_price ≤ current_stop` (trailing stop already triggered — exit_rebalance is redundant).
5. Uses `UNIQUE(portfolio_id, ticker, signal_date)` — re-running on the same day updates rather than duplicating.

**Inv-vol sizing note:** `exit_rebalance` signals do not include share sizing fields (`suggested_shares = 0`). These are exit signals, not entries.

### Request

No body required.

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "run_date": "2026-06-30",
    "is_last_trading_day": true,
    "signals_created": 2,
    "top5_tickers": ["NVDA", "AAPL", "MSFT", "GOOGL", "META"],
    "exit_rebalance_signals": [
      {
        "ticker": "TSLA",
        "market": "US",
        "status": "exit_rebalance",
        "reason": "Month-end rebalance: TSLA not in top-5 momentum list as of 2026-06-30"
      }
    ]
  }
}
```

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /signals

**Purpose**

List existing signals, optionally filtered by status.

**Method & Path**

- `GET /signals`

**Idempotency**

- Safe to refresh (read-only).

### Request

#### Query parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter by signal status. If omitted, all signals are returned |

#### Status values

| Value | Description |
|-------|-------------|
| `new` | Not yet acted upon |
| `entered` | User entered a position based on this signal |
| `dismissed` | User dismissed the signal |
| `expired` | Signal expired (> 7 days old without action) |
| `already_held` | A matching open position already existed when the signal was generated |
| `allocation_insufficient` | Legacy status (v1.3/v1.4). No longer generated by the signal service as of v6.0 (BLG-BE-36). Existing database records retaining this status remain valid and are returned by `GET /signals` without modification. |
| `exit_rebalance` | Month-end rebalance exit signal. Position not in current top-5 momentum list on the last trading day of the month. Generated by `POST /signals/rebalance-exit`. (v6.2 ST-03 BLG-FEAT-47) |

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array)

```json
[
  {
    "id": "950e8400-e29b-41d4-a716-446655440000",
    "ticker": "TSLA",
    "status": "new",
    "momentum_percent": 45.2,
    "signal_date": "2026-02-17"
  }
]
```

### Notes

- Returns `[]` if no signals match the filter.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## PATCH /signals/{signal_id}

**Purpose**

Update the status of a signal.

**Method & Path**

- `PATCH /signals/{signal_id}`

**Idempotency**

- Mutating. Replaces signal status with the provided value.

### Request

#### Path parameters

- `signal_id` (string, required): UUID of the signal.

#### Body

```json
{
  "status": "entered"
}
```

#### Allowed status values

- `entered`: user entered a position based on this signal
- `dismissed`: user dismissed the signal
- `expired`: signal expired
- `watchlisted`: user added the ticker to the watchlist from this signal

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "id": "950e8400-e29b-41d4-a716-446655440000",
  "ticker": "TSLA",
  "status": "entered",
  "updated_at": "2026-02-17T10:30:00Z"
}
```

### Validation rules & constraints

- `signal_id` must identify an existing signal.
- `status` must be one of the allowed values listed above.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Invalid status value (not one of: entered, dismissed, expired, watchlisted)
- `404` Signal not found

---

## DELETE /signals/{signal_id}

**Purpose**

Permanently delete a signal record.

Typically used to remove stale or unwanted signals from the list. This is a hard delete — the record cannot be recovered.

**Method & Path**

- `DELETE /signals/{signal_id}`

**Idempotency**

- Non-idempotent. A second call for the same `signal_id` returns `404`.

### Request

#### Path parameters

- `signal_id` (string, required): UUID of the signal to delete.

No request body.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "deleted": true,
  "id": "950e8400-e29b-41d4-a716-446655440000"
}
```

### Errors

Errors use the standard error envelope from **conventions.md**.

- `404` Signal not found

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.5 | 2026-06-19 | ST-01 (BLG-BE-36, v6.0): Replace cash-allocation sizing model with risk-based `sizing_service.size_position()` per `strategy_rules.md §4.1`. `suggested_shares` now reflects `portfolio_value × risk_percent / stop_distance` — independent of concurrent signal count. `allocation_gbp` is now estimated_cost from the canonical sizing calculator. `reason` field updated: no longer describes cap-overshoot; now set when sizing produces 0 shares (invalid stop, or sizing invalid). `allocation_insufficient` status is legacy — no longer generated. `volatility` field description corrected (not used for sizing). API Contracts & Documentation Owner. |
| 1.4 | 2026-06-03 | Hotfix: Revise `allocation_insufficient` semantics — now only fires when total cash < price of 1 share. When 20% cap prevents 1 share but total cash is sufficient, signal stays `new` with `suggested_shares = 1` and `reason` note. Update `reason` field description accordingly. |
| 1.3 | 2026-06-03 | ST-06 (BLG-FEAT-43, v5.0): Add `allocation_insufficient` status for signals where 1 share exceeds position allocation; add `reason` field with human-readable explanation; `reason` is `null` for all other statuses. DB: `signals` table extended with nullable `reason` column; `signals_status_check` constraint extended. Frontend: `SignalCard` displays reason inline with orange styling. API Contracts & Documentation Owner. |
| 1.2 | 2026-05-18 | ST-01 (BLG-FE-33, v3.7): Add `watchlisted` as an allowed PATCH status value — user added ticker to watchlist from signal card. Updated Allowed status values section and Errors 400 description. Corresponds to `signals_status_check` DB constraint extension in `data_model.md` v2.8. API Contracts & Documentation Owner. |
| 1.1 | 2026-04-15 | ST-09 (BLG-BE-10, v2.7): Add 4 supplementary indicator fields to `POST /signals/generate` response per signal: `relative_strength_pct`, `week52_high_proximity_pct`, `avg_daily_volume_20d`, `price_vs_50d_ma`. All display-only — §13 COMPLIANT (SRB-v1.7 Feature 3). Fields do not affect `rank` or signal ordering. API Contracts & Documentation Owner. |
| 1.0 | 2026-03-18 | Initial version |
