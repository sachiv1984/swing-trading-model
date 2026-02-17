# signal_endpoints.md

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
| `volatility` | Volatility measure used for inverse-volatility position sizing. Stored for auditability |
| `allocation_gbp` | Capital allocated to this signal based on volatility weighting and available cash at generation time |

### Validation rules & constraints

- `lookback_days` must be a positive integer when provided.
- `top_n` must be a positive integer when provided.

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

- `400` Invalid status value
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
