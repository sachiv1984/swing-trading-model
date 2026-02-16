# position_endpoints.md

## Overview

This document defines **Position** domain endpoints:

- List open positions (trading screen)
- Run daily monitoring analysis
- Exit (full or partial) using user-confirmed broker execution details
- Update journal notes
- Update tags
- Retrieve the tag catalogue

Global response envelopes, error shape, defaults, and multi-currency/stop rules are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /positions](#get-positions)
- [GET /positions/analyze](#get-positionsanalyze)
- [POST /positions/{position_id}/exit](#post-positionsposition_idexit)
- [PATCH /positions/{position_id}/note](#patch-positionsposition_idnote)
- [PATCH /positions/{position_id}/tags](#patch-positionsposition_idtags)
- [GET /positions/tags](#get-positionstags)

---

## GET /positions

**Purpose**

Returns all **open positions** with live prices, stop context, FX context, and journal metadata.

**Method & Path**

- `GET /positions`

**Idempotency**

- Safe to refresh. Fetches refreshed prices.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array)

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "ticker": "NVDA",
    "market": "US",
    "entry_date": "2026-02-01",
    "entry_price": 622.00,
    "shares": 10.5,
    "current_price": 623.00,
    "current_price_native": 850.00,
    "stop_price": 607.50,
    "stop_price_native": 829.00,
    "initial_stop": 545.00,
    "initial_stop_native": 743.00,
    "pnl": 2394.00,
    "pnl_percent": 3.7,
    "holding_days": 14,
    "status": "open",
    "grace_period": false,
    "display_status": "PROFITABLE",
    "atr_value": 15.32,
    "fx_rate": 1.3642,
    "live_fx_rate": 1.3650,
    "entry_note": "Breakout above $800 resistance",
    "exit_note": null,
    "tags": ["momentum", "breakout"]
  }
]
```

#### Validation notes & constraints

- `display_status` values: `GRACE`, `PROFITABLE`, `LOSING`.
- `entry_note` and `exit_note` may be `string` or `null`.
- `tags` is an array; may be empty.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /positions/analyze

**Purpose**

Runs deterministic daily monitoring logic across open positions and returns an action summary.

**Method & Path**

- `GET /positions/analyze`

**Idempotency**

- Safe to refresh. Deterministic recomputation.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "analysis_date": "2026-02-15",
  "market_regime": {
    "spy_risk_on": true,
    "ftse_risk_on": true,
    "spy_price": 580.00,
    "spy_ma200": 550.00,
    "ftse_price": 8200.00,
    "ftse_ma200": 8000.00
  },
  "live_fx_rate": 1.3650,
  "summary": {
    "total_value": 15000.00,
    "total_pnl": 1000.00,
    "exit_count": 0
  },
  "actions": [
    {
      "ticker": "NVDA",
      "action": "HOLD",
      "entry_price": 622.00,
      "current_price": 623.00,
      "shares": 10.5,
      "pnl": 2394.00,
      "pnl_pct": 3.7,
      "current_stop": 607.50,
      "holding_days": 14,
      "grace_period": false,
      "stop_reason": "Trailing (profitable)"
    },
    {
      "ticker": "AAPL",
      "action": "EXIT",
      "exit_reason": "Risk-Off Signal",
      "entry_price": 180.00,
      "current_price": 175.00,
      "shares": 20,
      "pnl": -100.00,
      "pnl_pct": -2.8,
      "current_stop": 171.00,
      "holding_days": 8,
      "grace_period": true,
      "stop_reason": "Market regime"
    }
  ]
}
```

#### Action types

- `HOLD`: position healthy; no user action required.
- `EXIT`: exit recommended (e.g., stop hit, risk-off signal, trailing stop); user must confirm exit with broker execution price.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## POST /positions/{position_id}/exit

**Purpose**

User-confirmed exit using actual broker execution details.

- Supports full exit (default) or partial exit (by specifying `shares`).
- **Exit price is always user-provided.**
- For **US** positions, `exit_fx_rate` is required.

**Method & Path**

- `POST /positions/{position_id}/exit`

**Idempotency**

- Mutating (non-idempotent). Repeating the request records additional exits.

### Request

#### Path parameters

- `position_id` (string, required): UUID of the position.

#### Body

```json
{
  "shares": 10.5,
  "exit_price": 920.00,
  "exit_date": "2026-02-15",
  "exit_reason": "Target Reached",
  "exit_fx_rate": 1.3650,
  "exit_note": "Hit target, took profits"
}
```

#### Required fields

- `exit_price` (number, min `0.01`): actual broker execution price.

#### Optional fields

- `shares` (number): number of shares to exit (default: all remaining shares).
- `exit_date` (string, `YYYY-MM-DD`): default is today (UTC).
- `exit_reason` (string): one of:
  - `Manual Exit` (default)
  - `Stop Loss Hit`
  - `Target Reached`
  - `Risk-Off Signal`
  - `Trailing Stop`
  - `Partial Profit Taking`
- `exit_fx_rate` (number): **required for US stocks**; ignored for UK stocks.
- `exit_note` (string, max 500): journal note (empty string treated as `null`).

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "ticker": "NVDA",
  "market": "US",
  "exit_price": 920.00,
  "shares": 10.5,
  "gross_proceeds": 9660.00,
  "exit_fees": 10.00,
  "fee_breakdown": {
    "commission": 5.00,
    "stamp_duty": 0.00,
    "fx_fee": 5.00
  },
  "net_proceeds": 9650.00,
  "realized_pnl": 3200.00,
  "realized_pnl_pct": 35.8,
  "new_cash_balance": 14650.00,
  "exit_fx_rate": 1.3650,
  "exit_date": "2026-02-15",
  "is_partial_exit": false,
  "remaining_shares": 0
}
```

### Validation rules & constraints

- `position_id` must identify an existing position.
- `exit_price` must be greater than 0.
- If provided, `shares` must be > 0 and must not exceed position size.
- `exit_reason` must be one of the allowed values.
- For US positions, `exit_fx_rate` is required; backend rejects requests without it.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Missing `exit_fx_rate` for US stock
- `400` Shares exceed position size
- `400` Invalid `exit_reason`
- `404` Position not found

---

## PATCH /positions/{position_id}/note

**Purpose**

Update entry and/or exit notes for a position (works for open and closed positions).

**Method & Path**

- `PATCH /positions/{position_id}/note`

**Idempotency**

- Mutating. Replaces provided fields.

### Request

#### Path parameters

- `position_id` (string, required): UUID of the position.

#### Body

```json
{
  "entry_note": "Updated reasoning after analysis",
  "exit_note": "Hit target, took profits"
}
```

#### Fields

- `entry_note` (string or `null`, max 500): set `null` to clear.
- `exit_note` (string or `null`, max 500): set `null` to clear.

**At least one field is required.**

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "ticker": "NVDA",
  "entry_note": "Updated reasoning after analysis",
  "exit_note": "Hit target, took profits",
  "updated_at": "2026-02-15T10:30:00Z"
}
```

### Validation rules & constraints

- At least one of `entry_note` or `exit_note` must be provided.
- Notes must not exceed 500 characters.
- Empty string `""` is treated as `null`.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` No fields provided
- `400` Note exceeds 500 characters
- `404` Position not found

---

## PATCH /positions/{position_id}/tags

**Purpose**

Replace all tags for a position. Works for open and closed positions.

**Method & Path**

- `PATCH /positions/{position_id}/tags`

**Idempotency**

- Mutating. Replaces the tag set with the provided array.

### Request

#### Path parameters

- `position_id` (string, required): UUID of the position.

#### Body

```json
{
  "tags": ["momentum", "breakout", "winner"]
}
```

#### Fields

- `tags` (array, required): pass an empty array `[]` to clear all tags.

#### Tag rules

- Lowercase letters, numbers, hyphens only
- Regex: `^[a-z0-9-]+$`
- Max 20 characters per tag
- Max 10 tags per position

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "ticker": "NVDA",
  "tags": ["momentum", "breakout", "winner"],
  "updated_at": "2026-02-15T10:30:00Z"
}
```

### Validation rules & constraints

- Tags must meet formatting requirements.
- Each tag max length 20.
- No more than 10 tags.
- Tag array replaces all existing tags.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Invalid tag format
- `400` Tag exceeds 20 characters
- `400` More than 10 tags
- `404` Position not found

---

## GET /positions/tags

**Purpose**

Retrieve all unique tags used across positions (for UI autocomplete/suggestions).

**Method & Path**

- `GET /positions/tags`

**Idempotency**

- Safe to refresh.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "tags": ["breakout", "momentum", "winner", "loser", "earnings"],
  "total_positions": 42,
  "positions_with_tags": 38
}
```

### Notes

- `tags` is sorted alphabetically (case-insensitive).
- Returns an empty array if no tags exist.

### Errors

Errors use the standard error envelope from **conventions.md**.
