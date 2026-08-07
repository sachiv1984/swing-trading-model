**Owner:** API Contracts & Documentation Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 1.3.1
**Last Updated:** 2026-08-07
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# settings_endpoints.md

**Data Model Reference:** `docs/specs/data_model/settings_model.md` — canonical field definitions, types, defaults, constraints, and semantics for the settings domain.

---

## Overview

This document defines **Settings** domain endpoints:

- Retrieve current strategy configuration and fee parameters
- Create initial settings record
- Update strategy configuration and fee parameters by ID

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

> **v1.1.0 — Method correction (2026-03-05):** The update endpoint was previously documented as `PUT /settings`. The live implementation uses `PATCH /settings/{settings_id}` (update by ID) and `POST /settings` (create new settings). This document now reflects the canonical live behaviour. No backend change was required. Decision record: ESC-20260304-01 option (a).

---

## Endpoints

- [GET /settings](#get-settings)
- [POST /settings](#post-settings)
- [PATCH /settings/{settings_id}](#patch-settingssettings_id)

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
    "min_trades_for_analytics": 10,
    "default_risk_percent": 1.00,
    "concentration_position_threshold_pct": 15.0,
    "concentration_sector_threshold_pct": 30.0,
    "created_at": "2026-01-05T09:12:41Z",
    "updated_at": "2026-08-02T14:37:09Z"
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
| `default_risk_percent` | float | `1.00` | Default risk percentage pre-populated in the Position Sizing Calculator widget on the Trade Entry page. Represents percentage of portfolio value to risk per position, e.g. `1.00` = 1%. This is a user preference default, not an enforced position limit — users may override it per trade |
| `concentration_position_threshold_pct` | float | `15.0` | Alert threshold: fires when a single position's heat exceeds this percentage of total portfolio heat. Read by `GET /portfolio/concentration-status` |
| `concentration_sector_threshold_pct` | float | `30.0` | Alert threshold: fires when a single sector's combined heat exceeds this percentage of total portfolio heat. Read by `GET /portfolio/concentration-status` |
| `created_at` | string (ISO-8601) | — | Timestamp the settings row was created (single global row, set once) |
| `updated_at` | string (ISO-8601) | — | Timestamp of the most recent `PATCH /settings/{settings_id}` / `POST /settings` write |

**Strategy parameter context:**

The default values (`min_hold_days: 10`, `atr_multiplier_initial: 5.0`, `atr_multiplier_trailing: 2.0`) reflect the backtest-optimised parameters that produced 26.37% CAGR, 1.29 Sharpe Ratio, and −25.38% maximum drawdown. These are configurable but changes affect all future stop calculations.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## POST /settings

**Purpose**

Create a new settings record. Used to initialise the settings row if one does not exist.

**Method & Path**

- `POST /settings`

**Idempotency**

- Non-idempotent. Each call creates a new settings record.

### Request

#### Body

All fields are optional. Fields not provided use system defaults.

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
  "min_trades_for_analytics": 10,
  "default_risk_percent": 1.00,
  "concentration_position_threshold_pct": 15.0,
  "concentration_sector_threshold_pct": 30.0
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
| `default_risk_percent` | float | Must be > 0 and ≤ 100 |
| `concentration_position_threshold_pct` | float | Optional; no enforced range |
| `concentration_sector_threshold_pct` | float | Optional; no enforced range |

### Response (200)

Response uses the standard success envelope from **conventions.md**.

Returns the created settings object.

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
  "default_risk_percent": 1.00,
  "concentration_position_threshold_pct": 15.0,
  "concentration_sector_threshold_pct": 30.0
}
```

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Invalid field value (e.g. negative commission, multiplier ≤ 0, `default_risk_percent` ≤ 0 or > 100)

---

## PATCH /settings/{settings_id}

**Purpose**

Update one or more strategy configuration or fee parameters on an existing settings record.

All fields are optional — only the fields provided are updated. Fields not included in the request retain their current values.

**Method & Path**

- `PATCH /settings/{settings_id}`

**Idempotency**

- Idempotent for the same input. Repeating the same request produces the same result.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `settings_id` | string (UUID) | Yes | The UUID of the settings record to update |

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
  "min_trades_for_analytics": 10,
  "default_risk_percent": 1.00,
  "concentration_position_threshold_pct": 15.0,
  "concentration_sector_threshold_pct": 30.0
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
| `default_risk_percent` | float | Must be > 0 and ≤ 100 |
| `concentration_position_threshold_pct` | float | Optional; no enforced range |
| `concentration_sector_threshold_pct` | float | Optional; no enforced range |

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
  "default_risk_percent": 1.00,
  "concentration_position_threshold_pct": 15.0,
  "concentration_sector_threshold_pct": 30.0,
  "updated_at": "2026-02-19T10:30:00Z"
}
```

### Validation rules & constraints

- Strategy parameter changes (`min_hold_days`, ATR multipliers) take effect on the **next** call to `GET /positions/analyze`. Open positions are not retroactively affected.
- Fee parameter changes (`uk_commission`, `stamp_duty_rate`, etc.) apply to new transactions only. Existing trade history is not recalculated.
- `default_risk_percent` changes take effect immediately on the next load of the Trade Entry page. No existing trades or open positions are affected.
- `concentration_position_threshold_pct` and `concentration_sector_threshold_pct` changes take effect on the next call to `GET /portfolio/concentration-status`.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Invalid field value (e.g. negative commission, multiplier ≤ 0, `default_risk_percent` ≤ 0 or > 100)
- `404` Settings record with provided `settings_id` not found

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.3.1 | 2026-08-07 | ST-03 (BLG-SPEC-112, EPIC-02, v8.4): `GET /settings` example was missing `created_at`/`updated_at`, both of which the live response includes. Added with representative ISO-8601 values, plus field notes rows. Authority: API Contracts & Documentation Owner. |
| 1.3.0 | 2026-06-03 | Add `concentration_position_threshold_pct` (default 15%) and `concentration_sector_threshold_pct` (default 30%) to all endpoints. DB columns added via `ensure_settings_concentration_columns` migration. Read by `GET /portfolio/concentration-status`. Settings page gains Risk Limits section. |
| 1.2.0 | 2026-03-18 | (prior update) |
| 1.1.0 | 2026-03-05 | Replaced `PUT /settings` with `PATCH /settings/{settings_id}` and `POST /settings` to match live implementation. ESC-20260304-01 option (a). Added lifecycle header. |
| 1.0.0 | (pre-v1.8) | Initial version — `GET /settings` and `PUT /settings` (superseded). |
