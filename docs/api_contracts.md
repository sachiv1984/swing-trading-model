# API Contracts — Momentum Trading Assistant (v1.2)

## Overview

This document defines the backend API contracts for the **Momentum Trading Assistant** web application.

The system is a **decision-support tool**, not a trading bot.  
All strategy logic is deterministic, server-side, and frozen for MVP.

**Last Updated:** February 12, 2026  
**Version:** 1.2

---

## Design Principles

- Backend is the **single source of truth**
- Frontend must never calculate: ATR, Stops, Market regime, P&L, Currency conversions
- APIs return **fully explained decisions**
- Human-in-the-loop: exits must be explicitly confirmed
- Predictability > flexibility
- **Exit prices are user-entered** (actual broker execution prices)

---

## Critical: Multi-Currency Design

### Database Storage
- `entry_price`: GBP (cost basis for portfolio)
- `fill_price`: Native currency (USD/GBP - actual fill price)
- `current_price`: Native currency (USD/GBP)
- `current_stop`: **Native currency (USD/GBP)** ← Prevents FX fluctuation
- `atr`: Native currency (USD/GBP)

### API Response (Dual Pricing)
Every price field returns BOTH currencies:
- `current_price`: GBP (for portfolio totals)
- `current_price_native`: Native (for display to user)
- `stop_price`: GBP (for portfolio totals)
- `stop_price_native`: Native (for display) **← STABLE, no FX fluctuation!**

**Why This Matters:**
1. Stops in native currency **never change** due to FX rate fluctuations
2. Portfolio calculations remain consistent in GBP
3. Users see prices in their trading currency (USD/GBP)

**Example:**
```
Database: current_stop = $398.09 (USD)
FX Rate changes: 1.37 → 1.40
Display: Still shows $398.09 ✓ (stable!)
GBP equivalent: £290.92 → £284.35 (for portfolio total only)
```

---

## Response Conventions

### Success
```json
{
  "status": "ok",
  "data": { }
}
```

### Error
```json
{
  "status": "error",
  "message": "Human-readable explanation"
}
```

---

## 1. Portfolio Overview

### GET /portfolio

**Purpose:** Primary working screen with live prices and cash management

**Response:**
```json
{
  "status": "ok",
  "data": {
    "cash": 532.62,
    "cash_balance": 532.62,
    "total_value": 5133.52,
    "open_positions_value": 4600.90,
    "total_pnl": 133.52,
    "initial_value": 5000.00,
    "net_deposits": 5000.00,
    "last_updated": "2026-02-03 18:42:10",
    "live_fx_rate": 1.3684,
    "positions": [...]
  }
}
```

**Notes:**
- `total_pnl` = `total_value - net_deposits` (accounts for deposits/withdrawals)
- `net_deposits` = sum of all deposits - sum of all withdrawals
- All values in GBP

---

## 2. Positions List

### GET /positions

**Purpose:** Get all open positions with live prices (ALWAYS fetches fresh prices)

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": "uuid",
      "ticker": "WDC",
      "market": "US",
      "entry_date": "2026-01-23",
      "entry_price": 243.00,
      "shares": 5.5,
      "current_price": 209.17,
      "current_price_native": 286.16,
      "stop_price": 184.64,
      "stop_price_native": 252.66,
      "pnl": 173.77,
      "pnl_percent": 17.79,
      "holding_days": 11,
      "status": "open",
      "display_status": "PROFITABLE",
      "exit_reason": null,
      "grace_period": false,
      "stop_reason": "Active",
      "atr_value": 18.2607,
      "fx_rate": 1.3528,
      "live_fx_rate": 1.3684
    }
  ]
}
```

**Field Explanations:**
- `entry_price`: Native currency (from `fill_price`)
- `current_price`: GBP (for dashboard calculations)
- `current_price_native`: Native currency (for display)
- `stop_price`: GBP (0 during grace period)
- `stop_price_native`: **Native currency (STABLE)** - use this for display!
- `grace_period`: `true` if within first 10 days
- `display_status`: `"GRACE"` | `"PROFITABLE"` | `"LOSING"`
- `fx_rate`: Rate at entry time
- `live_fx_rate`: Current FX rate

---

## 3. Add Position (Manual Entry)

### POST /portfolio/position

**Purpose:** Manual sync with broker executions, supports fractional shares

**Request:**
```json
{
  "ticker": "FRES",
  "market": "UK",
  "entry_date": "2026-01-31",
  "shares": 27.25,
  "entry_price": 40.98,
  "fx_rate": null,
  "atr_value": 2.58,
  "stop_price": null
}
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "ticker": "FRES.L",
    "total_cost": 1116.70,
    "fees_paid": 9.95,
    "entry_price": 40.98,
    "initial_stop": 28.08,
    "remaining_cash": 4383.30
  }
}
```

**Notes:**
- UK tickers auto-appended with `.L`
- Fees calculated automatically:
  - UK: £9.95 commission + 0.5% stamp duty
  - US: 0.15% FX fee
- Initial stop: `entry_price - (5 × ATR)` (wide stop)

---

## 4. Daily Analysis

### GET /positions/analyze

**Purpose:** 
- Runs full daily monitoring logic
- Updates all position prices, stops, and P&L
- Checks market regime
- Idempotent (safe to refresh)

**Response:**
```json
{
  "status": "ok",
  "data": {
    "analysis_date": "2026-02-03",
    "market_regime": {
      "spy_risk_on": true,
      "ftse_risk_on": true,
      "spy_price": 512.34,
      "spy_ma200": 488.91,
      "ftse_price": 7482.10,
      "ftse_ma200": 7401.44
    },
    "live_fx_rate": 1.3684,
    "summary": {
      "total_value": 4600.90,
      "total_pnl": 133.52,
      "exit_count": 1
    },
    "actions": [
      {
        "ticker": "FRES",
        "action": "EXIT",
        "exit_reason": "Stop Loss Hit",
        "entry_price": 40.98,
        "current_price": 36.68,
        "shares": 27.25,
        "pnl": -117.17,
        "pnl_pct": -10.49,
        "current_stop": 28.08,
        "holding_days": 11,
        "grace_period": false,
        "stop_reason": "Stop triggered"
      }
    ]
  }
}
```

**Stop Logic:**
- **Grace period (days 0-9):** No active stop
- **After grace, profitable (P&L > 0):** Tight 2×ATR trailing stop, enforced at entry minimum
- **After grace, losing (P&L ≤ 0):** Wide 5×ATR stop, can go below entry (room to recover)

**Trailing Rules:**
- Profitable: `stop = max(current_stop, new_stop, entry_price)`
- Losing: `stop = max(current_stop, new_stop)`
- Stops only move UP, never down

---

## 5. Exit Position (v1.2 UPDATED)

### POST /positions/{position_id}/exit

**Purpose:** 
- Exit a position and record in trade history
- **Uses user-provided exit price** (actual fill price from broker)
- Calculates fees and realized P&L with fee breakdown
- Updates portfolio cash balance
- Supports partial exits and custom exit dates

**Request:**
```json
{
  "shares": 27.25,
  "exit_price": 36.68,
  "exit_date": "2026-02-03",
  "exit_reason": "Stop Loss Hit",
  "exit_fx_rate": 1.3684
}
```

**Field Details:**
- `shares`: Number of shares to exit (optional - defaults to all shares)
- `exit_price`: **User-entered exit price from broker** (REQUIRED)
- `exit_date`: Exit date (optional - defaults to today, format: YYYY-MM-DD)
- `exit_reason`: Reason for exit (optional - defaults to "Manual Exit")
- `exit_fx_rate`: **User-entered FX rate (GBP/USD) from broker** (REQUIRED for US stocks, ignored for UK stocks)

**Valid Exit Reasons:**
- "Manual Exit"
- "Stop Loss Hit"
- "Target Reached"
- "Risk-Off Signal"
- "Trailing Stop"
- "Partial Profit Taking"

**Response:**
```json
{
  "status": "ok",
  "data": {
    "ticker": "FRES.L",
    "market": "UK",
    "exit_price": 36.68,
    "shares": 27.25,
    "gross_proceeds": 999.53,
    "exit_fees": 9.95,
    "fee_breakdown": {
      "commission": 9.95,
      "stamp_duty": 0.00,
      "fx_fee": 0.00
    },
    "net_proceeds": 989.58,
    "realized_pnl": -127.12,
    "realized_pnl_pct": -11.40,
    "new_cash_balance": 1522.20,
    "exit_fx_rate": 1.3684,
    "exit_date": "2026-02-03",
    "is_partial_exit": false,
    "remaining_shares": 0
  }
}
```

**Important Implementation Notes:**

### Exit Price (CRITICAL)
- Exit price is **ALWAYS user-provided**
- **Never fetches live market price** - user enters actual broker execution
- This ensures P&L matches actual broker statement
- For US stocks, user enters price in USD (their trading currency)
- For UK stocks, user enters price in GBP

### FX Rate (CRITICAL for US Stocks)
- FX rate is **ALWAYS user-provided** for US stocks
- User enters the GBP/USD rate from their broker statement
- This ensures cash conversion matches broker exactly
- Rate is ignored for UK stocks (always 1.0)
- Frontend must validate FX rate is provided for US stocks

### Fee Calculation
**UK Exits:**
- Commission: £9.95 (fixed)
- No stamp duty on sales
- Total fees: £9.95

**US Exits:**
- FX fee: 0.15% of gross proceeds (in USD)
- No commission
- Converted to GBP using **user-entered FX rate**

### Partial Exits
- If `shares` < position total, position remains open
- Remaining shares keep same entry price and stop
- Cost basis is proportionally reduced
- Example: Exit 10 of 20 shares → 10 shares remain open

### Error Cases
```json
{
  "status": "error",
  "message": "Insufficient shares. Position has 10.5 shares, exit requested 20"
}
```

```json
{
  "status": "error", 
  "message": "Exit price must be greater than 0"
}
```

```json
{
  "status": "error",
  "message": "FX rate is required for US stock exits. Please provide the GBP/USD rate from your broker statement."
}
```

---

## 6. Portfolio History

### POST /portfolio/snapshot

**Purpose:** Create daily snapshot (automated via cron)

**Response:**
```json
{
  "status": "ok",
  "data": {
    "snapshot_date": "2026-02-12",
    "total_value": 5133.52,
    "cash_balance": 532.62,
    "positions_value": 4600.90,
    "total_pnl": 133.52,
    "position_count": 5
  }
}
```

**Notes:**
- Idempotent: Can run multiple times per day (updates existing)
- UNIQUE constraint on (portfolio_id, snapshot_date)
- Recommended: Run at 4 PM UTC weekdays via cron

---

### GET /portfolio/history?days=30

**Purpose:** Retrieve historical portfolio snapshots for charts

**Query Parameters:**
- `days`: Number of days to retrieve (default: 30)

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "snapshot_date": "2026-02-12",
      "total_value": 5133.52,
      "cash_balance": 532.62,
      "positions_value": 4600.90,
      "total_pnl": 133.52,
      "position_count": 5
    },
    {
      "snapshot_date": "2026-02-11",
      "total_value": 5089.20,
      "cash_balance": 532.62,
      "positions_value": 4556.58,
      "total_pnl": 89.20,
      "position_count": 5
    }
  ]
}
```

---

## 7. Trade History

### GET /trades

**Purpose:** Performance review

**Response:**
```json
{
  "status": "ok",
  "data": {
    "total_trades": 18,
    "win_rate": 61.1,
    "total_pnl": 4820.75,
    "trades": [
      {
        "ticker": "NVDA",
        "entry_date": "2025-09-12",
        "exit_date": "2025-11-02",
        "pnl": 1240.50,
        "pnl_pct": 22.4,
        "exit_reason": "Stop Loss Hit"
      }
    ]
  }
}
```

---

## 8. Cash Management

### POST /cash/transaction

**Purpose:** Record deposits and withdrawals for accurate P&L

**Request:**
```json
{
  "type": "deposit",
  "amount": 1000.00,
  "date": "2026-02-03",
  "note": "Monthly savings"
}
```

**Field Details:**
- `type`: "deposit" or "withdrawal" (required)
- `amount`: Amount in GBP, must be > 0 (required)
- `date`: Transaction date YYYY-MM-DD (optional, defaults to today)
- `note`: Optional description (max 200 characters)

**Response:**
```json
{
  "status": "ok",
  "data": {
    "transaction": {
      "id": "uuid",
      "type": "deposit",
      "amount": 1000.00,
      "date": "2026-02-03",
      "note": "Monthly savings",
      "created_at": "2026-02-03T18:42:10"
    },
    "new_balance": 1532.62
  }
}
```

**Error Cases:**
```json
{
  "status": "error",
  "message": "Invalid transaction type. Must be 'deposit' or 'withdrawal'"
}
```

```json
{
  "status": "error",
  "message": "Insufficient funds. Available cash: £500.00, withdrawal: £1000.00"
}
```

---

### GET /cash/transactions

**Purpose:** List all cash transactions

**Query Parameters:**
- `order`: `ASC` | `DESC` (default: `DESC` = newest first)

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": "uuid",
      "type": "deposit",
      "amount": 1000.00,
      "date": "2026-02-03",
      "note": "Monthly savings",
      "created_at": "2026-02-03T18:42:10"
    },
    {
      "id": "uuid",
      "type": "withdrawal",
      "amount": 500.00,
      "date": "2026-02-01",
      "note": "Expenses",
      "created_at": "2026-02-01T10:15:00"
    }
  ]
}
```

**Notes:**
- Returns empty array if no transactions exist
- Sorted by date according to order parameter
- All amounts in GBP

---

### GET /cash/summary

**Purpose:** Get aggregated cash flow statistics

**Response:**
```json
{
  "status": "ok",
  "data": {
    "total_deposits": 15000.00,
    "total_withdrawals": 2000.00,
    "net_cash_flow": 13000.00,
    "current_cash": 5432.10
  }
}
```

**Notes:**
- `net_cash_flow` = total_deposits - total_withdrawals
- Used for calculating true portfolio P&L
- Portfolio P&L = current_value - net_cash_flow

---

## 9. Signal Generation

### POST /signals/generate

**Purpose:** Generate momentum signals based on current portfolio state

**Query Parameters:**
- `lookback_days`: Momentum calculation period (default: 252 = 1 year)
- `top_n`: Number of top momentum stocks to signal (default: 5)

**Example Request:**
```
POST /signals/generate?lookback_days=252&top_n=5
```

**Response:**
```json
{
  "status": "ok",
  "data": {
    "signals_generated": 5,
    "new_signals": 3,
    "already_held": 2,
    "signal_date": "2026-02-12",
    "fx_rate": 1.3684,
    "available_cash": 5000.00,
    "market_regime": {
      "spy_risk_on": true,
      "ftse_risk_on": true
    },
    "signals": [
      {
        "ticker": "NVDA",
        "market": "US",
        "rank": 1,
        "momentum_percent": 45.2,
        "current_price": 850.00,
        "price_gbp": 621.07,
        "atr_value": 15.32,
        "volatility": 0.0234,
        "initial_stop": 773.40,
        "status": "new",
        "allocation_gbp": 1000.00,
        "suggested_shares": 1,
        "total_cost": 622.57
      },
      {
        "ticker": "TSLA",
        "market": "US",
        "rank": 2,
        "momentum_percent": 38.5,
        "current_price": 245.00,
        "price_gbp": 179.01,
        "atr_value": 8.50,
        "volatility": 0.0312,
        "initial_stop": 202.50,
        "status": "already_held",
        "allocation_gbp": 0,
        "suggested_shares": 0,
        "total_cost": 0
      }
    ]
  }
}
```

**Signal Fields:**
- `ticker`: Stock symbol
- `market`: "US" or "UK"
- `rank`: Momentum rank (1 = highest momentum)
- `momentum_percent`: Return over lookback period (%)
- `current_price`: Current price in native currency
- `price_gbp`: Current price in GBP
- `atr_value`: Average True Range (for stop calculation)
- `volatility`: 60-day rolling volatility
- `initial_stop`: Suggested initial stop price
- `status`: "new" (can enter) or "already_held" (already in portfolio)
- `allocation_gbp`: Suggested position size in GBP
- `suggested_shares`: Recommended number of shares
- `total_cost`: Total cost including fees (GBP)

**Notes:**
- Only generates signals in risk-on market conditions
- Filters by 200-day MA trend (price > MA200)
- Equal-weight position sizing across new signals
- Signals saved to database for later review
- Can take 30-60 seconds to complete (downloads price data)

---

### GET /signals

**Purpose:** Get all signals, optionally filtered by status

**Query Parameters:**
- `status`: Optional filter - "new", "entered", "dismissed", "expired", "already_held"

**Example Requests:**
```
GET /signals
GET /signals?status=new
GET /signals?status=already_held
```

**Response:**
```json
[
  {
    "id": "uuid",
    "portfolio_id": "uuid",
    "ticker": "NVDA",
    "market": "US",
    "rank": 1,
    "momentum_percent": 45.2,
    "current_price": 850.00,
    "price_gbp": 621.07,
    "atr_value": 15.32,
    "volatility": 0.0234,
    "initial_stop": 773.40,
    "status": "new",
    "allocation_gbp": 1000.00,
    "suggested_shares": 1,
    "total_cost": 622.57,
    "signal_date": "2026-02-12",
    "created_at": "2026-02-12T09:30:00"
  }
]
```

**Notes:**
- Returns empty array if no signals exist
- Signals ordered by rank (best first)
- All prices in native currency

---

### PATCH /signals/{signal_id}

**Purpose:** Update signal status (typically after taking action)

**Request:**
```json
{
  "status": "entered"
}
```

**Valid Status Transitions:**
- "new" → "entered" (position opened)
- "new" → "dismissed" (user skipped)
- "new" → "expired" (signal too old)

**Response:**
```json
{
  "status": "ok",
  "data": {
    "id": "uuid",
    "ticker": "NVDA",
    "status": "entered",
    "updated_at": "2026-02-12T14:30:00"
  }
}
```

---

### DELETE /signals/{signal_id}

**Purpose:** Delete a signal

**Response:**
```json
{
  "status": "ok"
}
```

**Notes:**
- Permanently removes signal from database
- Cannot be undone
- Typically used to clean up old/stale signals

---

## 10. Market Status

### GET /market/status

**Purpose:** Get current market regime and FX rate (for Signals page)

**Response:**
```json
{
  "status": "ok",
  "data": {
    "spy": {
      "price": 512.34,
      "ma200": 488.91,
      "is_risk_on": true
    },
    "ftse": {
      "price": 7482.10,
      "ma200": 7401.44,
      "is_risk_on": true
    },
    "fx_rate": 1.3684,
    "last_updated": "2026-02-12T14:30:00"
  }
}
```

**Field Explanations:**
- `spy.price`: Current SPY price
- `spy.ma200`: SPY 200-day moving average
- `spy.is_risk_on`: true if SPY > MA200
- `ftse.price`: Current FTSE price  
- `ftse.ma200`: FTSE 200-day moving average
- `ftse.is_risk_on`: true if FTSE > MA200
- `fx_rate`: Current GBP/USD exchange rate
- `last_updated`: Timestamp of data

**Notes:**
- Used to determine if market conditions favor new positions
- Risk-on = price > 200-day MA
- Risk-off = price < 200-day MA
- Data fetched from Yahoo Finance in real-time

---

## 11. Health & Status (NEW in v1.3)

### GET /health

**Purpose:** Basic health check for load balancers and monitoring

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T14:30:00",
  "version": "1.2.0"
}
```

**Notes:**
- Fast response (<10ms)
- Use for load balancer health checks
- Returns 200 OK if system is running

---

### GET /health/detailed

**Purpose:** Comprehensive system status check

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T14:30:00",
  "version": "1.2.0",
  "response_time_ms": 45.3,
  "checks": {
    "database": {
      "status": "healthy",
      "details": {
        "connected": true,
        "portfolio_exists": true
      }
    },
    "yahoo_finance": {
      "status": "healthy",
      "details": {
        "gbp_usd_rate": 1.3684,
        "accessible": true
      }
    },
    "services": {
      "status": "healthy",
      "details": {
        "position_service": "available",
        "portfolio_service": "available",
        "cash_service": "available"
      }
    },
    "config": {
      "status": "healthy",
      "details": {
        "settings_loaded": true
      }
    }
  }
}
```

**Status Values:**
- `healthy`: Component working normally
- `degraded`: Component working with issues
- `unhealthy`: Component not working

**Overall Status:**
- `healthy`: All components healthy
- `degraded`: One or more components degraded or unhealthy

**Notes:**
- Checks database connectivity
- Verifies external service access (Yahoo Finance)
- Tests service layer availability
- Validates configuration
- Use for post-deployment verification

---

### GET /test/endpoints

**Purpose:** Test all API endpoints (for verification and monitoring)

**Response:**
```json
{
  "timestamp": "2026-02-12T14:30:00",
  "summary": {
    "total": 11,
    "passed": 11,
    "failed": 0,
    "errors": 0,
    "success_rate": 100.0
  },
  "results": [
    {
      "endpoint": "GET /",
      "status": "pass",
      "status_code": 200,
      "expected_status": 200,
      "response_time_ms": 5.2
    },
    {
      "endpoint": "GET /health",
      "status": "pass",
      "status_code": 200,
      "expected_status": 200,
      "response_time_ms": 3.1
    },
    {
      "endpoint": "GET /positions",
      "status": "pass",
      "status_code": 200,
      "expected_status": 200,
      "response_time_ms": 234.5
    }
  ]
}
```

**Notes:**
- Tests all GET endpoints that don't require parameters
- Returns pass/fail status for each
- Includes response times
- Use for post-deployment smoke tests
- Can take 10-30 seconds to complete

---

## 12. Settings

### GET /settings

**Purpose:** Get user settings and strategy parameters

**Response:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": "uuid",
      "min_hold_days": 10,
      "atr_multiplier_initial": 5,
      "atr_multiplier_trailing": 2,
      "atr_period": 14,
      "default_currency": "GBP",
      "uk_commission": 9.95,
      "us_commission": 0,
      "stamp_duty_rate": 0.005,
      "fx_fee_rate": 0.0015
    }
  ]
}
```

---

## Key Implementation Notes

### Currency Consistency
**CRITICAL:** All stops stored in native currency to prevent FX fluctuation issues.

**Before (GBP storage):**
```
Stop in DB: £421 (GBP)
FX changes: 1.37 → 1.40
Display: $421 × 1.37 = $576 → $421 × 1.40 = $589 ❌ Appears to move!
```

**After (Native storage):**
```
Stop in DB: $576 (USD)
FX changes: 1.37 → 1.40
Display: $576 ✓ (stable!)
```

### Grace Period
- Days 0-9: Stop exists but not enforced
- Day 10+: Stop becomes active

### Stop Multipliers
- Profitable: 2× ATR (tight, protect gains)
- Losing: 5× ATR (wide, room to recover)

### Trailing Logic
- Profitable: Stop enforced at entry minimum
- Losing: Stop can go below entry (wide protection)

### Exit Price Philosophy (v1.2)
**Why user-entered exit prices:**
1. **Accuracy**: Matches actual broker execution, not theoretical live price
2. **Slippage**: Accounts for real-world slippage and execution quality
3. **Reconciliation**: P&L matches broker statements exactly
4. **Trust**: User sees fees and proceeds before confirmation
5. **Flexibility**: Can backdate exits for reconciliation

**Frontend responsibilities:**
- Validate exit_price > 0
- Show calculated fees before submission
- Display gross vs net proceeds
- Show FX conversion for US stocks
- Pre-fill with current_price_native as suggestion

---

## Breaking Changes from v1.1

### Exit Endpoint Changes (v1.2)
1. **exit_price now REQUIRED** - was optional (fetched live price)
2. **exit_fx_rate now REQUIRED for US stocks** - was optional
3. **fee_breakdown added to response** - detailed fee display
4. **shares parameter added** - supports partial exits
5. **exit_reason validation** - must use predefined list

### Backwards Compatibility
- Old clients calling without exit_price will receive 400 error
- Old clients calling without exit_fx_rate (US stocks) will receive 400 error
- Frontend must be updated to always provide these fields
- Response structure expanded but existing fields unchanged

---

## Explicit Non-Requirements (MVP)

- No PATCH endpoints for positions
- No partial updates
- No strategy configuration APIs beyond settings
- No charting APIs (frontend responsibility)
- No broker integrations
- No multi-user identifiers

---

**Document Version:** 1.2  
**Last Review:** February 12, 2026  
**Status:** Current