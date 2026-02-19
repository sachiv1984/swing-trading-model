# portfolio_endpoints.md

## Overview

This document defines **Portfolio** domain endpoints:

- Portfolio overview (working screen)
- Add position (via portfolio)
- Position sizing calculator
- Daily snapshot upsert
- Snapshot history retrieval

Global response envelopes, error shape, defaults, and multi-currency rules are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /portfolio](#get-portfolio)
- [POST /portfolio/position](#post-portfolioposition)
- [POST /portfolio/size](#post-portfoliosize)
- [POST /portfolio/snapshot](#post-portfoliosnapshot)
- [GET /portfolio/history](#get-portfoliohistory)

---

## GET /portfolio

**Purpose**

Primary working screen returning cash balances, portfolio totals, and **open positions** with refreshed live prices on every call.

> **Position detail depth:** This endpoint returns a summary view of open positions. For the full enriched position object — including native currency prices, stop context, ATR, FX rates, and journal fields — use `GET /positions`.

**Method & Path**

- `GET /portfolio`

**Idempotency**

- Safe to refresh. Each call refreshes prices.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "cash": 5000.00,
  "cash_balance": 5000.00,
  "total_value": 15000.00,
  "open_positions_value": 10000.00,
  "total_pnl": 1000.00,
  "initial_value": 14000.00,
  "net_deposits": 14000.00,
  "live_fx_rate": 1.3642,
  "last_updated": "2026-02-17T10:30:00Z",
  "positions": [
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
      "pnl": 2394.00,
      "pnl_percent": 3.7,
      "holding_days": 14,
      "status": "open",
      "grace_period": false,
      "display_status": "PROFITABLE"
    }
  ]
}
```

#### Field notes (portfolio-level)

- `cash` and `cash_balance` are both the available cash balance. `cash_balance` is retained for legacy compatibility.
- `total_value` is cash plus open positions value.
- `open_positions_value` is the sum of current values across all open positions.
- `total_pnl` is realised plus unrealised P&L.
- `net_deposits` is total deposits minus total withdrawals. Used as the cost basis for portfolio-level return calculations.
- `last_updated` is an ISO 8601 timestamp.
- `positions` is an array of open positions; returns `[]` if none.

#### Field notes (position summary object)

The position objects returned here are a **summary shape**. Key omissions versus the full object from `GET /positions`:

| Omitted field | Available at |
|---------------|-------------|
| `initial_stop` | `GET /positions` |
| `atr_value` | `GET /positions` |
| `fx_rate`, `live_fx_rate` | `GET /positions` |
| `entry_note`, `exit_note` | `GET /positions` |
| `tags` | `GET /positions` |

**`pnl_percent`** is present in the summary object. This is the percentage P&L relative to entry cost. The same value appears as `pnl_pct` in trade history records — both names exist in the system for compatibility. `pnl_percent` is the canonical name in position responses.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## POST /portfolio/position

**Purpose**

Create a new position based on user-entered broker execution details. Supports fractional shares. Creates the position and deducts the total cost from available cash.

**Method & Path**

- `POST /portfolio/position`

**Idempotency**

- Mutating (non-idempotent). Repeating the request creates additional positions and changes cash.

### Request

#### Body

```json
{
  "ticker": "NVDA",
  "market": "US",
  "entry_date": "2026-02-17",
  "shares": 10.5,
  "entry_price": 850.00,
  "fx_rate": 1.3642,
  "atr_value": 15.32,
  "stop_price": 780.00,
  "entry_note": "Breakout above $800 resistance",
  "tags": ["momentum", "breakout"]
}
```

#### Required fields

- `ticker` (string, max 20)
- `entry_date` (string, `YYYY-MM-DD`)
- `shares` (number, min `0.0001`)
- `entry_price` (number, min `0.01`)

#### Optional fields

- `market` (string: `"US"` or `"UK"`; default: auto-detect from ticker suffix)
- `fx_rate` (number; required for US if not auto-detected)
- `atr_value` (number; auto-fetched by server if not provided)
- `stop_price` (number; calculated as `entry_price − (5 × ATR)` if not provided)
- `entry_note` (string, max 500; empty string treated as `null`)
- `tags` (array; max 10; each max 20 characters; lowercase, numbers, hyphens only)

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "ticker": "NVDA",
  "total_cost": 8925.00,
  "fees_paid": 10.00,
  "entry_price": 850.00,
  "initial_stop": 780.00,
  "remaining_cash": 4075.00,
  "position_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Validation rules & constraints

- `ticker` must be a valid format; max 20 characters.
- `entry_date` must be a valid date and must not be in the future.
- `shares` must be greater than 0.
- `entry_price` must be greater than 0.
- `tags` must follow tag rules (lowercase letters, numbers, hyphens only; max 20 characters each; max 10 tags).

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Insufficient funds
- `400` Invalid ticker format
- `400` Invalid date (future date)
- `400` Invalid shares (negative or zero)
- `400` Invalid tag format

---

## POST /portfolio/size

**Purpose**

Calculate a suggested share quantity for a prospective new position based on portfolio risk parameters.

Returns a deterministic sizing result including suggested shares, risk amount, estimated cost, and cash feasibility. Does not create a position or mutate any state. The backend is the authoritative source of all calculations — the frontend must not derive or recalculate any returned value.

All calculation rules are defined canonically in `strategy_rules.md §4.1`.

**Method & Path**

- `POST /portfolio/size`

**Idempotency**

- Idempotent for the same inputs. Safe to call repeatedly, including on debounced keystrokes. Does not mutate portfolio state, cash balances, or position records.

### Request

#### Body

```json
{
  "entry_price": 850.00,
  "stop_price": 780.00,
  "risk_percent": 1.00,
  "market": "US",
  "fx_rate": 1.3642
}
```

#### Required fields

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `entry_price` | number | > 0 | Prospective entry price in the instrument's native currency (GBP for UK, USD for US) |
| `stop_price` | number | > 0 | Intended initial stop price in the instrument's native currency |
| `risk_percent` | number | > 0 | Percentage of portfolio value to risk on this position, e.g. `1.00` for 1% |

#### Optional fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `market` | string | `"UK"` | `"US"` or `"UK"`. Used for fee estimation in the cash feasibility gate |
| `fx_rate` | number | Live system rate | User-provided FX rate override for US positions. If omitted, the system live rate is used |

### Response (200) — Valid result

Response uses the standard success envelope from **conventions.md**.

```json
{
  "status": "ok",
  "data": {
    "valid": true,
    "suggested_shares": 17.8571,
    "risk_amount": 125.00,
    "stop_distance": 70.00,
    "estimated_cost": 15178.57,
    "estimated_fees": 0.00,
    "fx_rate_used": 1.3642,
    "cash_sufficient": true,
    "available_cash": 20000.00
  }
}
```

### Response (200) — Insufficient cash

```json
{
  "status": "ok",
  "data": {
    "valid": true,
    "suggested_shares": 17.8571,
    "risk_amount": 125.00,
    "stop_distance": 70.00,
    "estimated_cost": 15178.57,
    "estimated_fees": 0.00,
    "fx_rate_used": 1.3642,
    "cash_sufficient": false,
    "available_cash": 8000.00,
    "max_affordable_shares": 9.3750
  }
}
```

### Response (200) — Invalid inputs

```json
{
  "status": "ok",
  "data": {
    "valid": false,
    "reason": "INVALID_STOP_DISTANCE",
    "reason_detail": "Stop price must be below entry price"
  }
}
```

### Field notes

| Field | Notes |
|-------|-------|
| `valid` | `true` if inputs satisfy all validity rules in `strategy_rules.md §4.1.4`. `false` if any rule is breached or portfolio value snapshot is missing |
| `suggested_shares` | Share quantity floored to 4 decimal places per canonical spec. Present only when `valid: true` |
| `risk_amount` | `PortfolioValue × RiskPercent` in GBP |
| `stop_distance` | `EntryPrice − StopPrice` in the instrument's native currency |
| `estimated_cost` | `SuggestedShares × EntryPrice + EstimatedFees` in GBP |
| `estimated_fees` | Fee estimate using current settings parameters (commission, stamp duty, FX fee as applicable) |
| `fx_rate_used` | The FX rate applied in this calculation. Always returned when `valid: true` for auditability. `1.0` for UK positions |
| `cash_sufficient` | `true` if `estimated_cost <= available_cash` |
| `available_cash` | Current `portfolios.cash` in GBP. Returned when `valid: true` to support cash display in the UI |
| `max_affordable_shares` | Present and always populated when `cash_sufficient: false`. Floored to 4 decimal places. Maximum share quantity the user can afford given `available_cash` |
| `reason` | Machine-readable reason code. Present only when `valid: false`. See reason codes table below |
| `reason_detail` | Human-readable description of the invalid condition. Present only when `valid: false`. **For development and logging use only — must not be used as user-facing display text.** The frontend derives its own plain-language messages from the `reason` code |

### Reason codes

| Code | Condition |
|------|-----------|
| `INVALID_RISK_PERCENT` | `risk_percent <= 0` |
| `INVALID_ENTRY_PRICE` | `entry_price <= 0` |
| `INVALID_STOP_PRICE` | `stop_price <= 0` |
| `INVALID_STOP_DISTANCE` | `stop_price >= entry_price` (stop distance is zero or negative) |
| `NO_PORTFOLIO_VALUE_SNAPSHOT` | No snapshot exists in `portfolio_history`. Backend cannot determine portfolio value for risk calculation |

### Validation rules & constraints

- All three required fields must be present. Missing fields return HTTP 400.
- Business rule failures (invalid inputs per `strategy_rules.md §4.1.4`) return HTTP 200 with `valid: false` — not HTTP 400.
- `market` must be `"US"` or `"UK"` if provided. Invalid market value returns HTTP 400.
- `fx_rate` must be > 0 if provided. Invalid FX rate returns HTTP 400.
- The endpoint never auto-fills, stores, or applies `SuggestedShares` to any position. It is a read-only calculation.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Missing required field (`entry_price`, `stop_price`, or `risk_percent`)
- `400` Invalid `market` value
- `400` Invalid `fx_rate` value (≤ 0)
- `500` Internal error

---

## POST /portfolio/snapshot

**Purpose**

Create or update a **daily portfolio snapshot** (idempotent upsert by portfolio + date). Intended to be called once per day, typically automated at market close.

**Method & Path**

- `POST /portfolio/snapshot`

**Idempotency**

- Idempotent upsert: calling multiple times on the same day updates the same snapshot record for that date.

### Request

No body required.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "id": "650e8400-e29b-41d4-a716-446655440000",
  "snapshot_date": "2026-02-17",
  "total_value": 15000.00,
  "cash_balance": 5000.00,
  "positions_value": 10000.00,
  "total_pnl": 1000.00,
  "position_count": 3,
  "created_at": "2026-02-17T10:30:00Z"
}
```

### Notes

- If a snapshot already exists for today's date, the backend updates it in place.
- If no snapshot exists for today, the backend creates a new one.
- Snapshots feed the Sharpe ratio (portfolio method) and drawdown calculations in `GET /analytics/metrics`. A minimum of 30 snapshots is required for the portfolio-method Sharpe ratio.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /portfolio/history

**Purpose**

Retrieve historical portfolio snapshots for charting and analytics.

**Method & Path**

- `GET /portfolio/history`

**Idempotency**

- Safe to refresh.

### Request

#### Query parameters

- `days` (integer, optional): number of days to retrieve. Default: `30`.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array)

```json
[
  {
    "id": "650e8400-e29b-41d4-a716-446655440000",
    "snapshot_date": "2026-02-17",
    "total_value": 15000.00,
    "cash_balance": 5000.00,
    "positions_value": 10000.00,
    "total_pnl": 1000.00,
    "position_count": 3
  }
]
```

### Notes

- Returns an empty array `[]` if no snapshots exist.
- Sorted by `snapshot_date` ascending (oldest first) to support charting.

### Errors

Errors use the standard error envelope from **conventions.md**.
