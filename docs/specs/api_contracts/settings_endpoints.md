# settings_endpoints.md

## Overview

This document defines **Settings** domain endpoints:

- Retrieve current strategy configuration and fee parameters
- Update strategy configuration and fee parameters

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /settings](#get-settings)
- [PUT /settings](#put-settings)

---

## GET /settings

**Purpose**

Return the current strategy configuration, trading fee parameters, and UI preferences.

Settings control strategy behaviour (grace period, ATR multipliers) and fee calculations (commissions, stamp duty, FX fees). These values are configurable to allow re-optimisation without code changes.

**Method & Path**

- `GET /settings`

**Idempotency**

- Safe to refresh (read-only).

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array, single element)

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "min_hold_days": 10,
    "atr_multiplier_initial": 5.0,
    "atr_multiplier_trailing": 2.0,
    "atr_period": 14,
    "default_currency": "GBP",
    "theme": "dark",
    "uk_commission": 9.95,
    "us_commission": 0.00,
    "stamp_duty_rate": 0.005,
    "fx_fee_rate": 0.0015,
    "min_trades_for_analytics": 10
  }
]
```

> **Note:** The response is an array containing a single settings object. This reflects the database schema (single global settings row).

#### Field notes

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `min_hold_days` | integer | `10` | Grace period duration in days. Stop losses are not enforced during this window (days 0–9 inclusive) |
| `atr_multiplier_initial` | float | `5.0` | ATR multiplier for **losing** positions (wide stop, room to recover) |
| `atr_multiplier_trailing` | float | `2.0` | ATR multiplier for **profitable** positions (tight trailing stop, protect gains) |
| `atr_period` | integer | `14` | Rolling window in days for ATR calculation |
| `default_currency` | string | `"GBP"` | Portfolio base currency (display only) |
| `theme` | string | `"dark"` | UI theme preference (`"dark"` or `"light"`) |
| `uk_commission` | float | `9.95` | Fixed commission per UK trade in GBP |
| `us_commission` | float | `0.00` | Fixed commission per US trade (zero-commission brokers) |
| `stamp_duty_rate` | float | `0.005` | UK stamp duty rate on purchases (0.5%) |
| `fx_fee_rate` | float | `0.0015` | FX conversion fee rate for USD trades (0.15%) |
| `min_trades_for_analytics` | integer | `10` | Minimum closed trades required before analytics metrics are computed |

**Strategy parameter context:**

The default values (`min_hold_days: 10`, `atr_multiplier_initial: 5.0`, `atr_multiplier_trailing: 2.0`) reflect the backtest-optimised parameters that produced 26.37% CAGR, 1.29 Sharpe Ratio, and −25.38% maximum drawdown. These are configurable but changes affect all future stop calculations.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## PUT /settings

**Purpose**

Update one or more strategy configuration or fee parameters.

All fields are optional — only the fields provided are updated. Fields not included in the request retain their current values.

**Method & Path**

- `PUT /settings`

**Idempotency**

- Idempotent for the same input. Repeating the same request produces the same result.

### Request

#### Body

All fields are optional. Include only the fields to be changed.

```json
{
  "min_hold_days": 10,
  "atr_multiplier_initial": 5.0,
  "atr_multiplier_trailing": 2.0,
  "atr_period": 14,
  "default_currency": "GBP",
  "theme": "dark",
  "uk_commission": 9.95,
  "us_commission": 0.00,
  "stamp_duty_rate": 0.005,
  "fx_fee_rate": 0.0015,
  "min_trades_for_analytics": 10
}
```

#### Field constraints

| Field | Type | Constraint |
|-------|------|------------|
| `min_hold_days` | integer | Must be ≥ 1 |
| `atr_multiplier_initial` | float | Must be > 0 |
| `atr_multiplier_trailing` | float | Must be > 0 |
| `atr_period` | integer | Must be ≥ 1 |
| `default_currency` | string | `"GBP"` only (multi-currency support is position-level, not portfolio-level) |
| `theme` | string | `"dark"` or `"light"` |
| `uk_commission` | float | Must be ≥ 0 |
| `us_commission` | float | Must be ≥ 0 |
| `stamp_duty_rate` | float | Must be ≥ 0 and ≤ 1 |
| `fx_fee_rate` | float | Must be ≥ 0 and ≤ 1 |
| `min_trades_for_analytics` | integer | Must be ≥ 1 |

### Response (200)

Response uses the standard success envelope from **conventions.md**.

Returns the full updated settings object.

#### `data` schema

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "min_hold_days": 10,
  "atr_multiplier_initial": 5.0,
  "atr_multiplier_trailing": 2.0,
  "atr_period": 14,
  "default_currency": "GBP",
  "theme": "dark",
  "uk_commission": 9.95,
  "us_commission": 0.00,
  "stamp_duty_rate": 0.005,
  "fx_fee_rate": 0.0015,
  "min_trades_for_analytics": 10,
  "updated_at": "2026-02-17T10:30:00Z"
}
```

### Validation rules & constraints

- Strategy parameter changes (`min_hold_days`, ATR multipliers) take effect on the **next** call to `GET /positions/analyze`. Open positions are not retroactively affected.
- Fee parameter changes (`uk_commission`, `stamp_duty_rate`, etc.) apply to new transactions only. Existing trade history is not recalculated.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Invalid field value (e.g. negative commission, multiplier ≤ 0)
