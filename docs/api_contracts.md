# API Contracts — Momentum Trading Assistant (v1.4.1)

**Status:** Complete & Current  
**Last Updated:** February 15, 2026  
**Version:** 1.4.1 (Complete specification)

---

## Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [Response Conventions](#response-conventions)
4. [Defaults & Optional Fields](#defaults--optional-fields)
5. [Multi-Currency & Pricing Rules](#multi-currency--pricing-rules)
6. [Idempotency & Side-Effect Semantics](#idempotency--side-effect-semantics)
7. [Error Semantics](#error-semantics)
8. [Position Representations](#position-representations)
9. [Exit Price & FX Rules](#exit-price--fx-rules)
10. [Frontend Responsibilities](#frontend-responsibilities)
11. [Detailed Endpoint Specifications](#detailed-endpoint-specifications)
12. [Versioning](#versioning)

---

## Overview

This document defines the backend API contracts for the **Momentum Trading Assistant** web application.

The system is a **decision-support tool**, not a trading bot.  
All strategy logic is **deterministic, server-side**, and frozen for MVP.

The backend is the **single source of truth**.  
The frontend must never calculate indicators, stops, P&L, or FX conversions.

**Base URL:** `https://api.example.com` (Production) or `http://localhost:8000` (Development)

---

## Design Principles

### Core Principles

1. **Backend is Single Source of Truth**
   - All calculations performed server-side
   - Frontend displays only, never calculates

2. **Frontend Must Never Calculate:**
   - ATR (Average True Range)
   - Stop prices (initial, trailing, grace period)
   - Market regime (risk-on/risk-off)
   - P&L (profit/loss)
   - Currency conversions (GBP ↔ USD)

3. **APIs Return Fully Explained Decisions**
   - Every recommendation includes reasoning
   - Stop adjustments explain why
   - Exit recommendations show calculations

4. **Human-in-the-Loop**
   - Exits must be explicitly confirmed by user
   - No automatic trade execution
   - User provides actual broker execution prices

5. **Predictability Over Flexibility**
   - Deterministic behavior
   - No A/B tests or experiments
   - Same inputs always produce same outputs

6. **Exit Prices are Always User-Entered**
   - Reflects actual broker executions
   - Enables reconciliation with statements
   - No assumptions about execution prices

---

## Response Conventions

### Success Response (ALL endpoints)

All successful responses **MUST** be wrapped as:

```json
{
  "status": "ok",
  "data": {}
}
```

**Rules:**
- `data` MUST always be present
- `data` may be an object or an array
- No endpoint may return a raw object or array at the top level
- HTTP status code: `200`

**Example:**
```json
{
  "status": "ok",
  "data": {
    "cash_balance": 5000.00,
    "total_value": 15000.00
  }
}
```

---

### Error Response (ALL endpoints)

All error responses **MUST** be wrapped as:

```json
{
  "status": "error",
  "message": "Human-readable explanation"
}
```

**Rules:**
- `message` MUST be user-readable
- Internal error details MUST NOT be exposed
- Errors are deterministic and explain *why* the request failed
- HTTP status code: `400` (validation), `404` (not found), or `500` (system)

**Examples:**
```json
{
  "status": "error",
  "message": "Insufficient funds. Available: £500, Required: £1000"
}
```

```json
{
  "status": "error",
  "message": "Position not found"
}
```

---

## Defaults & Optional Fields

Unless otherwise stated, the following defaults apply **server-side**:

| Field | Default Behaviour | Notes |
|-------|------------------|-------|
| `exit_reason` | `"Manual Exit"` | When not provided |
| `exit_date` | Today (UTC) | Current date when not provided |
| `shares` (exit) | All shares in position | Full exit when not provided |
| `fx_rate` (UK stocks) | `1.0` | UK stocks always 1.0 |
| `stop_price` (entry) | `entry_price - (5 × ATR)` | Auto-calculated if not provided |
| `atr_value` (entry) | Auto-fetched from Yahoo Finance | Server calculates if not provided |
| `entry_note` | `null` | Empty string treated as null |
| `tags` | `[]` | Empty array when not provided |

**Frontend clients MUST NOT infer or calculate defaults.**

---

## Multi-Currency & Pricing Rules

### Dual-Currency Guarantee

Any field representing a **price, stop, or valuation** MUST return **both**:
- A **GBP value** (for portfolio calculations)
- A **native currency value** (for display)

#### Required Pattern

| Concept | GBP Field | Native Field | Notes |
|---------|-----------|--------------|-------|
| Current price | `current_price` | `current_price_native` | Live market price |
| Stop price | `stop_price` | `stop_price_native` | Trailing/grace stops |
| Initial stop | `initial_stop` | `initial_stop_native` | At position entry |
| Entry price | `entry_price` | `entry_price_native` | Historical entry |

**Example Response:**
```json
{
  "ticker": "NVDA",
  "market": "US",
  "current_price": 623.00,
  "current_price_native": 850.00,
  "stop_price": 607.50,
  "stop_price_native": 829.00,
  "fx_rate": 1.3642
}
```

---

### Native-Currency Stop Stability (Hard Guarantee)

> **Stops are stored, enforced, and trailed in native currency ONLY.**

**FX rate changes:**
- MUST NOT move stops
- MAY change GBP equivalents for portfolio totals only

**This applies to:**
- Grace-period stops
- Trailing stops
- Profitable & losing stop logic
- Partial exits

**Example:**
```
Initial: NVDA @ $850, stop @ $780 (5 ATR below)
FX changes: 1.36 → 1.40

CORRECT:
- Stop remains $780 (unchanged)
- GBP equivalent: £557 → £557 (recalculated)

WRONG:
- Stop moves to $810 (violates stability)
```

---

## Idempotency & Side-Effect Semantics

### Idempotent (Safe to Refresh)

| Endpoint | Notes |
|----------|-------|
| `GET /portfolio` | Refreshes live prices, always safe |
| `GET /positions` | Fetches fresh prices from market |
| `GET /positions/analyze` | Deterministic recomputation |
| `GET /market/status` | Live market data |
| `GET /signals` | No mutation |
| `GET /trades` | Historical data only |
| `GET /cash/transactions` | Read-only |
| `GET /cash/summary` | Read-only |
| `GET /positions/tags` | Read-only |
| `GET /health` | Read-only |
| `GET /health/detailed` | Read-only |
| `GET /test/endpoints` | Read-only tests |
| `GET /settings` | Read-only |

---

### Mutating (Non-Idempotent)

| Endpoint | Behaviour |
|----------|-----------|
| `POST /portfolio/position` | Creates a position, deducts cash |
| `POST /positions/{id}/exit` | Creates trade record, updates cash |
| `POST /cash/transaction` | Records deposit/withdrawal |
| `PATCH /positions/{id}/note` | Updates journal notes |
| `PATCH /positions/{id}/tags` | Updates position tags |
| `PATCH /signals/{id}` | Updates signal status |
| `DELETE /signals/{id}` | Permanent deletion |

**Important:** Calling mutating endpoints multiple times has different effects each time.

---

### Snapshot Special Case

| Endpoint | Behaviour |
|----------|-----------|
| `POST /portfolio/snapshot` | **Idempotent upsert** (by portfolio + date) |

- If snapshot for date exists: updates values
- If snapshot for date missing: creates new
- Safe to call multiple times per day

---

## Error Semantics

| Category | HTTP Status | Description | Example |
|----------|-------------|-------------|---------|
| Validation error | 400 | Invalid or missing input | "shares must be > 0" |
| Business rule violation | 400 | Valid input, invalid state | "Insufficient funds" |
| Resource not found | 404 | Entity does not exist | "Position not found" |
| System error | 500 | Internal failure (no internals exposed) | "Service temporarily unavailable" |

**Error Response Always:**
```json
{
  "status": "error",
  "message": "Human-readable explanation"
}
```

---

## Position Representations

Different endpoints intentionally return **different shapes**:

| Endpoint | Purpose | Shape |
|----------|---------|-------|
| `GET /positions` | Trading screen | Live prices, stops, FX context |
| `GET /positions/{id}` | Deep inspection | Full details, diagnostics |
| `GET /trades` | Historical records | Immutable, closed trades only |

**These representations are NOT interchangeable.**

**Example - Trading Screen Position:**
```json
{
  "id": "uuid",
  "ticker": "NVDA",
  "current_price": 623.00,
  "current_price_native": 850.00,
  "stop_price": 607.50,
  "stop_price_native": 829.00,
  "grace_period": false,
  "display_status": "PROFITABLE"
}
```

**Example - Trade History:**
```json
{
  "id": "uuid",
  "ticker": "NVDA",
  "entry_price": 622.00,
  "exit_price": 920.00,
  "pnl": 3200.00,
  "exit_reason": "Target Reached"
}
```

---

## Exit Price & FX Rules

### Exit Price (Hard Requirement)

- Exit price is **ALWAYS user-provided**
- Live prices are **never fetched** for exits
- Ensures reconciliation with broker statements
- No assumptions about slippage or execution

**Frontend must:**
1. Prompt user for actual exit price from broker
2. Submit exact value (no rounding)
3. Never use `current_price` as exit price

---

### FX Rate (US Stocks Only)

- FX rate is **ALWAYS user-provided** for US exits
- Must match broker statement exactly
- Backend MUST reject US exits without FX rate
- Ignored for UK stocks (rate = 1.0)

**Frontend must:**
1. Show current FX rate as reference
2. Allow user to enter actual broker FX rate
3. Validate FX rate present for US stocks
4. Skip FX input for UK stocks

**Example - US Exit Request:**
```json
{
  "exit_price": 920.00,
  "exit_fx_rate": 1.3650
}
```

**Example - UK Exit Request:**
```json
{
  "exit_price": 1250.00
}
```

---

## Frontend Responsibilities

Frontend clients MUST:

1. **Never Calculate**
   - ATR, stops, P&L, or FX conversions
   - Always use server-provided values

2. **Always Submit User-Entered Exit Prices**
   - Never use `current_price` for exits
   - Prompt user for actual broker execution

3. **Always Submit FX Rate for US Exits**
   - Required field for US stocks
   - Use broker statement value

4. **Display Native-Currency Stops to Users**
   - Show `stop_price_native` in UI
   - Never show GBP stops for US stocks

5. **Treat Empty Strings as `null` for Notes**
   - Convert `""` to `null` before sending
   - Backend treats both as no note

6. **Validate Tags Client-Side**
   - Lowercase, numbers, hyphens only
   - Max 20 characters per tag
   - Max 10 tags per position

---

## Detailed Endpoint Specifications

### 1. Portfolio Overview

**Endpoint:** `GET /portfolio`

**Purpose:** Primary working screen with live prices and cash management.

**Request:** No parameters

**Response:**
```json
{
  "status": "ok",
  "data": {
    "cash": 5000.00,
    "cash_balance": 5000.00,
    "total_value": 15000.00,
    "open_positions_value": 10000.00,
    "total_pnl": 1000.00,
    "initial_value": 14000.00,
    "net_deposits": 14000.00,
    "live_fx_rate": 1.3642,
    "last_updated": "2026-02-15T10:30:00Z",
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
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `cash` | number | Available cash balance |
| `cash_balance` | number | Same as cash (legacy) |
| `total_value` | number | Cash + open positions value |
| `open_positions_value` | number | Sum of all open positions |
| `total_pnl` | number | Realized + unrealized P&L |
| `initial_value` | number | Starting capital + net deposits |
| `net_deposits` | number | Total deposits - withdrawals |
| `live_fx_rate` | number | Current GBP/USD rate |
| `last_updated` | string | ISO 8601 timestamp |
| `positions` | array | All open positions |

**Notes:**
- Refreshes prices on every call
- Safe to call repeatedly
- Returns empty positions array if none open

---

### 2. Positions List

**Endpoint:** `GET /positions`

**Purpose:** Returns all **open positions** with live prices and stop context.

**Request:** No parameters

**Response:**
```json
{
  "status": "ok",
  "data": [
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
}
```

**Additional Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `initial_stop` | number | Original stop at entry (GBP) |
| `initial_stop_native` | number | Original stop (native currency) |
| `grace_period` | boolean | True if in 5-day grace period |
| `display_status` | string | GRACE \| PROFITABLE \| LOSING |
| `atr_value` | number | Current ATR value |
| `fx_rate` | number | FX rate at entry |
| `live_fx_rate` | number | Current FX rate |
| `entry_note` | string\|null | Journal note at entry |
| `exit_note` | string\|null | Journal note at exit |
| `tags` | array | Position tags |

---

### 3. Add Position

**Endpoint:** `POST /portfolio/position`

**Purpose:** Manual sync with broker executions. Supports fractional shares.

**Request Body:**
```json
{
  "ticker": "NVDA",
  "market": "US",
  "entry_date": "2026-02-15",
  "shares": 10.5,
  "entry_price": 850.00,
  "fx_rate": 1.3642,
  "atr_value": 15.32,
  "stop_price": 780.00,
  "entry_note": "Breakout above $800 resistance",
  "tags": ["momentum", "breakout"]
}
```

**Required Fields:**
- `ticker` (string, max 20 chars)
- `entry_date` (string, YYYY-MM-DD)
- `shares` (number, min 0.0001)
- `entry_price` (number, min 0.01)

**Optional Fields:**
- `market` (string, "US" or "UK", default: auto-detect)
- `fx_rate` (number, required for US if not auto-detected)
- `atr_value` (number, auto-fetched if not provided)
- `stop_price` (number, auto-calculated if not provided)
- `entry_note` (string, max 500 chars)
- `tags` (array, max 10, each max 20 chars, lowercase/numbers/hyphens)

**Response:**
```json
{
  "status": "ok",
  "data": {
    "ticker": "NVDA",
    "total_cost": 8925.00,
    "fees_paid": 10.00,
    "entry_price": 850.00,
    "initial_stop": 780.00,
    "remaining_cash": 4075.00,
    "position_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Errors:**
- 400: Insufficient funds
- 400: Invalid ticker format
- 400: Invalid date (future date)
- 400: Invalid shares (negative or zero)
- 400: Invalid tag format

---

### 4. Daily Analysis

**Endpoint:** `GET /positions/analyze`

**Purpose:** Runs deterministic daily monitoring logic.

**Request:** No parameters

**Response:**
```json
{
  "status": "ok",
  "data": {
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
}
```

**Action Types:**

| Action | Reason | User Action Required |
|--------|--------|---------------------|
| `HOLD` | Position healthy | None |
| `EXIT` | Stop hit | Confirm exit with broker price |
| `EXIT` | Risk-off signal | Confirm exit with broker price |
| `EXIT` | Trailing stop | Confirm exit with broker price |

---

### 5. Exit Position

**Endpoint:** `POST /positions/{position_id}/exit`

**Purpose:** User-confirmed exit using broker execution prices.

**Parameters:**
- `position_id` (path, required): UUID of position to exit

**Request Body:**
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

**Required Fields:**
- `exit_price` (number, min 0.01): Actual broker execution price

**Optional Fields:**
- `shares` (number): Shares to exit (default: all)
- `exit_date` (string, YYYY-MM-DD): Exit date (default: today)
- `exit_reason` (string): One of:
  - "Manual Exit" (default)
  - "Stop Loss Hit"
  - "Target Reached"
  - "Risk-Off Signal"
  - "Trailing Stop"
  - "Partial Profit Taking"
- `exit_fx_rate` (number): **Required for US stocks**, FX rate from broker
- `exit_note` (string, max 500 chars): Journal note

**Response:**
```json
{
  "status": "ok",
  "data": {
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
}
```

**Errors:**
- 400: Missing exit_fx_rate for US stock
- 400: Shares exceed position size
- 400: Invalid exit_reason
- 404: Position not found

---

### 6. Portfolio Snapshot

**Endpoint:** `POST /portfolio/snapshot`

**Purpose:** Create or update daily portfolio snapshot (idempotent).

**Request:** No body required

**Response:**
```json
{
  "status": "ok",
  "data": {
    "id": "650e8400-e29b-41d4-a716-446655440000",
    "snapshot_date": "2026-02-15",
    "total_value": 15000.00,
    "cash_balance": 5000.00,
    "positions_value": 10000.00,
    "total_pnl": 1000.00,
    "position_count": 3,
    "created_at": "2026-02-15T10:30:00Z"
  }
}
```

**Notes:**
- Idempotent: updates if snapshot exists for date
- Should be called once per day (automated)
- Used for historical charts and analytics

---

**Endpoint:** `GET /portfolio/history`

**Purpose:** Retrieve historical portfolio snapshots for charting.

**Parameters:**
- `days` (query, optional): Number of days to retrieve (default: 30)

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": "650e8400-e29b-41d4-a716-446655440000",
      "snapshot_date": "2026-02-15",
      "total_value": 15000.00,
      "cash_balance": 5000.00,
      "positions_value": 10000.00,
      "total_pnl": 1000.00,
      "position_count": 3,
      "created_at": "2026-02-15T10:30:00Z"
    },
    {
      "snapshot_date": "2026-02-14",
      "total_value": 14800.00,
      "cash_balance": 5000.00,
      "positions_value": 9800.00,
      "total_pnl": 800.00,
      "position_count": 3
    }
  ]
}
```

**Notes:**
- Returns array sorted by date descending (newest first)
- Empty array if no snapshots exist
- Used by analytics for Sharpe ratio, drawdown calculations

---

### 7. Trade History

**Endpoint:** `GET /trades`

**Purpose:** Retrieve all closed trades with statistics.

**Request:** No parameters

**Response:**
```json
{
  "status": "ok",
  "data": {
    "total_trades": 42,
    "win_rate": 58.5,
    "total_pnl": 5200.00,
    "trades": [
      {
        "id": "750e8400-e29b-41d4-a716-446655440000",
        "ticker": "NVDA",
        "market": "US",
        "entry_date": "2026-01-15",
        "exit_date": "2026-02-15",
        "shares": 10.5,
        "entry_price": 622.00,
        "exit_price": 920.00,
        "pnl": 3200.00,
        "pnl_pct": 35.8,
        "pnl_percent": 35.8,
        "exit_reason": "Target Reached",
        "holding_days": 31,
        "entry_note": "Breakout above $800",
        "exit_note": "Hit target",
        "tags": ["momentum", "winner"]
      }
    ]
  }
}
```

**Notes:**
- Immutable records of closed positions
- Both `pnl_pct` and `pnl_percent` included for compatibility
- Sorted by exit_date descending

---

### 8. Cash Management

#### Record Transaction

**Endpoint:** `POST /cash/transaction`

**Request Body:**
```json
{
  "type": "deposit",
  "amount": 5000.00,
  "date": "2026-02-15",
  "note": "Initial funding"
}
```

**Required Fields:**
- `type` (string): "deposit" or "withdrawal"
- `amount` (number, min 0.01): Transaction amount

**Optional Fields:**
- `date` (string, YYYY-MM-DD): Transaction date (default: today)
- `note` (string, max 200 chars): Description

**Response:**
```json
{
  "status": "ok",
  "data": {
    "transaction": {
      "id": "850e8400-e29b-41d4-a716-446655440000",
      "type": "deposit",
      "amount": 5000.00,
      "date": "2026-02-15",
      "note": "Initial funding",
      "created_at": "2026-02-15T10:30:00Z"
    },
    "new_balance": 10000.00
  }
}
```

**Errors:**
- 400: Withdrawal exceeds available cash
- 400: Invalid transaction type

---

#### List Transactions

**Endpoint:** `GET /cash/transactions`

**Parameters:**
- `order` (query, optional): "ASC" or "DESC" (default: DESC)

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": "850e8400-e29b-41d4-a716-446655440000",
      "type": "deposit",
      "amount": 5000.00,
      "date": "2026-02-15",
      "note": "Initial funding",
      "created_at": "2026-02-15T10:30:00Z"
    }
  ]
}
```

---

#### Cash Summary

**Endpoint:** `GET /cash/summary`

**Response:**
```json
{
  "status": "ok",
  "data": {
    "total_deposits": 15000.00,
    "total_withdrawals": 1000.00,
    "net_cash_flow": 14000.00,
    "current_cash": 5000.00
  }
}
```

---

### 9. Trade Journal

#### Update Position Notes

**Endpoint:** `PATCH /positions/{position_id}/note`

**Purpose:** Update entry or exit notes for a position.

**Parameters:**
- `position_id` (path, required): UUID of position

**Request Body:**
```json
{
  "entry_note": "Updated reasoning after analysis",
  "exit_note": "Hit target, took profits"
}
```

**Fields:**
- `entry_note` (string\|null, max 500 chars): Entry note (null to clear)
- `exit_note` (string\|null, max 500 chars): Exit note (null to clear)

**At least one field required.**

**Response:**
```json
{
  "status": "ok",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "ticker": "NVDA",
    "entry_note": "Updated reasoning after analysis",
    "exit_note": "Hit target, took profits",
    "updated_at": "2026-02-15T10:30:00Z"
  }
}
```

**Notes:**
- Empty string `""` treated as `null`
- Can update entry_note, exit_note, or both
- Pass `null` to clear a note
- Works for both open and closed positions

**Errors:**
- 400: No fields provided
- 400: Note exceeds 500 characters
- 404: Position not found

---

#### Update Position Tags

**Endpoint:** `PATCH /positions/{position_id}/tags`

**Purpose:** Update tags for categorizing positions.

**Parameters:**
- `position_id` (path, required): UUID of position

**Request Body:**
```json
{
  "tags": ["momentum", "breakout", "winner"]
}
```

**Fields:**
- `tags` (array, required): Array of tags (empty array to clear all)

**Tag Rules:**
- Lowercase letters, numbers, hyphens only
- Pattern: `^[a-z0-9-]+$`
- Max 20 characters per tag
- Max 10 tags per position

**Response:**
```json
{
  "status": "ok",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "ticker": "NVDA",
    "tags": ["momentum", "breakout", "winner"],
    "updated_at": "2026-02-15T10:30:00Z"
  }
}
```

**Notes:**
- Replaces all existing tags
- Pass empty array `[]` to clear all tags
- Tags stored lowercase
- Works for both open and closed positions

**Errors:**
- 400: Invalid tag format (uppercase, spaces, special chars)
- 400: Tag exceeds 20 characters
- 400: More than 10 tags
- 404: Position not found

---

#### Get All Tags

**Endpoint:** `GET /positions/tags`

**Purpose:** Retrieve all unique tags used across positions.

**Request:** No parameters

**Response:**
```json
{
  "status": "ok",
  "data": {
    "tags": ["breakout", "momentum", "winner", "loser", "earnings"],
    "total_positions": 42,
    "positions_with_tags": 38
  }
}
```

**Fields:**
- `tags` (array): Sorted alphabetically, all unique tags
- `total_positions` (number): Total positions in system
- `positions_with_tags` (number): Positions with at least one tag

**Notes:**
- Used for autocomplete/suggestions in UI
- Returns empty array if no tags exist
- Sorted case-insensitive alphabetically

---

### 10. Signal Generation

**Endpoint:** `POST /signals/generate`

**Parameters:**
- `lookback_days` (query, optional): Momentum lookback period (default: 252)
- `top_n` (query, optional): Number of signals to generate (default: 5)

**Response:**
```json
{
  "status": "ok",
  "data": {
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
}
```

---

**Endpoint:** `GET /signals`

**Parameters:**
- `status` (query, optional): Filter by status

**Status Values:**
- `new`: Not yet acted upon
- `entered`: User entered position
- `dismissed`: User dismissed signal
- `expired`: Signal expired (>7 days old)
- `already_held`: Position already exists

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": "950e8400-e29b-41d4-a716-446655440000",
      "ticker": "TSLA",
      "status": "new",
      "momentum_percent": 45.2,
      "signal_date": "2026-02-15"
    }
  ]
}
```

---

**Endpoint:** `PATCH /signals/{signal_id}`

**Request Body:**
```json
{
  "status": "entered"
}
```

**Status Values:**
- `entered`: User entered position
- `dismissed`: User dismissed signal
- `expired`: Signal expired

**Response:**
```json
{
  "status": "ok",
  "data": {
    "id": "950e8400-e29b-41d4-a716-446655440000",
    "ticker": "TSLA",
    "status": "entered",
    "updated_at": "2026-02-15T10:30:00Z"
  }
}
```

---

### 11. Market Status

**Endpoint:** `GET /market/status`

**Response:**
```json
{
  "status": "ok",
  "data": {
    "spy": {
      "price": 580.00,
      "ma200": 550.00,
      "is_risk_on": true
    },
    "ftse": {
      "price": 8200.00,
      "ma200": 8000.00,
      "is_risk_on": true
    },
    "fx_rate": 1.3650,
    "last_updated": "2026-02-15T10:30:00Z"
  }
}
```

---

### 12. Health & Diagnostics

#### Basic Health

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-15T10:30:00Z",
  "version": "1.4.1"
}
```

**Status Values:**
- `healthy`: All systems operational
- `degraded`: Some issues, still functional
- `unhealthy`: Critical issues

---

#### Detailed Health

**Endpoint:** `GET /health/detailed`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-15T10:30:00Z",
  "version": "1.4.1",
  "response_time_ms": 42.5,
  "checks": {
    "database": {
      "status": "healthy",
      "details": {
        "connection": "ok",
        "response_time_ms": 5.2
      }
    },
    "yahoo_finance": {
      "status": "healthy",
      "details": {
        "last_fetch": "2026-02-15T10:29:00Z",
        "response_time_ms": 150.0
      }
    },
    "services": {
      "status": "healthy"
    },
    "config": {
      "status": "healthy"
    }
  }
}
```

---

#### Endpoint Tests

**Endpoint:** `POST /test/endpoints`

**Response:**
```json
{
  "timestamp": "2026-02-15T10:30:00Z",
  "summary": {
    "total": 12,
    "passed": 11,
    "failed": 1,
    "errors": 0,
    "success_rate": 91.7
  },
  "results": [
    {
      "endpoint": "GET /portfolio",
      "status": "pass",
      "status_code": 200,
      "expected_status": 200,
      "response_time_ms": 45.0
    },
    {
      "endpoint": "POST /positions/{id}/exit",
      "status": "fail",
      "status_code": 404,
      "expected_status": 200,
      "response_time_ms": 12.0,
      "error": "Position not found"
    }
  ]
}
```

---

### 13. Settings

**Endpoint:** `GET /settings`

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": "450e8400-e29b-41d4-a716-446655440000",
      "min_hold_days": 5,
      "atr_multiplier_initial": 5.0,
      "atr_multiplier_trailing": 3.0,
      "atr_period": 20,
      "default_currency": "GBP",
      "uk_commission": 5.00,
      "us_commission": 5.00,
      "stamp_duty_rate": 0.005,
      "fx_fee_rate": 0.0025,
      "min_trades_for_analytics": 10
    }
  ]
}
```

---

## Versioning

- **Contract Version:** 1.4.1
- **Change Type:** Complete specification (non-breaking)
- **Client Impact:** None (clarifications only)
- **Previous Version:** 1.4.0

### Changelog

**1.4.1 (2026-02-15):**
- Added complete endpoint specifications
- Added journal endpoints documentation
- Added complete field descriptions
- Added request/response examples
- No breaking changes

**1.4.0 (2026-02-01):**
- Added trade journal features
- Added tag management
- Added notes support

---

## Summary

This document provides complete API contract specifications for the Momentum Trading Assistant v1.4.1.

**Key Points:**
- All endpoints use `{status, data}` wrapper
- Backend is single source of truth
- Exit prices always user-provided
- Multi-currency support with native/GBP duality
- Stops stored in native currency only
- Complete field specifications included
- All journal endpoints documented

**For Implementation:**
- See OpenAPI spec for complete schemas
- Follow frontend responsibilities strictly
- Never calculate server-side values client-side
- Always validate before sending requests

---

**Document End**
