# signal_endpoints.md

## Overview

This document defines **Signal** domain endpoints:

- Generate momentum signals
- List signals (optionally filtered by status)
- Update signal status

Global response envelopes, error shape, defaults, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [POST /signals/generate](#post-signalsgenerate)
- [GET /signals](#get-signals)
- [PATCH /signals/{signal_id}](#patch-signalssignal_id)

---

## POST /signals/generate

**Purpose**

Generate a ranked set of momentum signals using deterministic server-side logic.

- Returns a summary (counts, date, available cash, market regime) and an array of generated signals.
- Signals may be marked as already held if a position already exists.

**Method & Path**

- `POST /signals/generate`

**Idempotency**

- Not explicitly classified in the contract. Treat as a server-side generation action that returns current deterministic outputs.

### Request

#### Query parameters

- `lookback_days` (integer, optional): momentum lookback period. Default: `252`.
- `top_n` (integer, optional): number of signals to generate. Default: `5`.

No request body.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "signals_generated": 5,
  "new_signals": 4,
  "already_held": 1,
  "signal_date": "2026-02-15",
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
      "suggested_shares": 1.16,
      "total_cost": 986.00,
      "signal_date": "2026-02-15",
      "created_at": "2026-02-15T10:30:00Z"
    }
  ]
}
```

### Validation rules & constraints

- `lookback_days` must be a positive integer when provided.
- `top_n` must be a positive integer when provided.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /signals

**Purpose**

List existing signals.

- Supports filtering by signal status.

**Method & Path**

- `GET /signals`

**Idempotency**

- Safe to refresh (read-only).

### Request

#### Query parameters

- `status` (string, optional): filter by status.

#### Status values

- `new`: not yet acted upon
- `entered`: user entered a position
- `dismissed`: user dismissed the signal
- `expired`: signal expired (> 7 days old)
- `already_held`: position already exists

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
    "signal_date": "2026-02-15"
  }
]
```

### Notes

- Returns `[]` if there are no signals matching the filter.

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

- `entered`: user entered a position
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
  "updated_at": "2026-02-15T10:30:00Z"
}
```

### Validation rules & constraints

- `signal_id` must identify an existing signal.
- `status` must be one of the allowed values.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `404` Signal not found (when `signal_id` does not exist)
- `400` Invalid status value
