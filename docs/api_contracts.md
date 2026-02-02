# API Contracts — Momentum Trading Assistant (v1.1)

## Overview

This document defines the backend API contracts for the **Momentum Trading Assistant** web application.

The system is a **decision-support tool**, not a trading bot.  
All strategy logic is deterministic, server-side, and frozen for MVP.

**Last Updated:** February 2026  
**Version:** 1.1 (includes cash management, portfolio history, multi-currency support)

---

## Design Principles

- Backend is the **single source of truth**
- Frontend must never calculate:
  - ATR
  - Stops
  - Market regime
  - P&L
  - Currency conversions
- APIs return **fully explained decisions**
- Human-in-the-loop: exits must be explicitly confirmed
- Predictability > flexibility

---

## Authentication (MVP)

- Single-user system
- Authentication is out of scope for v1
- Endpoints assume an authenticated session

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

## 1. Dashboard

### GET /dashboard

**Status:** Deprecated - Use GET /portfolio instead

---

## 2. Portfolio Overview

### GET /portfolio

### Purpose
- Primary working screen
- Returns complete portfolio state with live prices
- All calculations in GBP
- Accounts for deposits/withdrawals

### Response
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
    "last_updated": "2026-01-31 18:42:10",
    "live_fx_rate": 1.3685,
    "positions": [
      {
        "id": "uuid",
        "ticker": "PLTR",
        "market": "US",
        "entry_date": "2026-01-23",
        "entry_price": 21.45,
        "shares": 300,
        "current_price": 18.65,
        "current_value": 4095.00,
        "pnl": 79.30,
        "pnl_pct": 14.36,
        "current_stop": 21.45,
        "holding_days": 8,
        "status": "GRACE",
        "fx_rate": 1.3528,
        "live_fx_rate": 1.3685
      }
    ]
  }
}
```

### Notes
- `current_price` is in GBP for dashboard calculations
- `total_pnl` accounts for fees and deposits/withdrawals
- `net_deposits` = total deposits - total withdrawals
- True P&L = total_value - net_deposits

---

## 3. Positions List

### GET /positions

### Purpose
- Get all open positions with live prices
- Returns both GBP (for calculations) and native currency (for display)
- Always fetches fresh prices from market

### Response
```json
[
  {
    "id": "uuid",
    "ticker": "WDC",
    "market": "US",
    "entry_date": "2026-01-23",
    "entry_price": 243.00,
    "shares": 5.5,
    "current_price": 182.85,
    "current_price_native": 250.38,
    "stop_price": 243.00,
    "stop_price_native": 332.51,
    "pnl": 29.06,
    "pnl_percent": 2.98,
    "holding_days": 8,
    "status": "open",
    "display_status": "GRACE",
    "exit_reason": null,
    "grace_period": true,
    "stop_reason": "Grace period (8/10 days)",
    "atr_value": 12.50,
    "fx_rate": 1.3528,
    "live_fx_rate": 1.3685
  }
]
```

### Field Explanations
- `current_price`: Price in GBP (for Dashboard widget calculations)
- `current_price_native`: Price in native currency (USD/GBP for display)
- `stop_price`: Stop in GBP (0 during grace period)
- `stop_price_native`: Stop in native currency (0 during grace period)
- `grace_period`: true if within first 10 days
- `display_status`: GRACE | PROFITABLE | LOSING

---

## 4. Add Position (Manual Entry)

### POST /portfolio/position

### Purpose
- Manual sync with broker executions
- Supports fractional shares
- Auto-calculates fees based on market

### Request
```json
{
  "ticker": "FRES",
  "market": "UK",
  "entry_date": "2026-01-31",
  "shares": 27.25,
  "entry_price": 40.98,
  "fx_rate": null,
  "atr_value": 1.20,
  "stop_price": null
}
```

### Response
```json
{
  "status": "ok",
  "data": {
    "ticker": "FRES.L",
    "total_cost": 1116.70,
    "fees_paid": 9.95,
    "entry_price": 40.98,
    "initial_stop": 38.58,
    "remaining_cash": 4383.30
  }
}
```

### Notes
- UK tickers auto-appended with `.L`
- Fees calculated automatically:
  - UK: £9.95 commission + 0.5% stamp duty
  - US: 0.15% FX fee
- Stop calculated as: entry_price - (2 × ATR)

---

## 5. Daily Analysis (Core Engine)

### GET /positions/analyze

### Purpose
- Runs full daily monitoring logic
- Updates all position prices, stops, and P&L
- Checks market regime
- Idempotent (safe to refresh)

### Response
```json
{
  "status": "ok",
  "data": {
    "analysis_date": "2026-01-31",
    "market_regime": {
      "spy_risk_on": true,
      "ftse_risk_on": true,
      "spy_price": 512.34,
      "spy_ma200": 488.91,
      "ftse_price": 7482.10,
      "ftse_ma200": 7401.44
    },
    "live_fx_rate": 1.3685,
    "summary": {
      "total_value": 4600.90,
      "total_pnl": 133.52,
      "exit_count": 0
    },
    "actions": [
      {
        "ticker": "WDC",
        "action": "HOLD",
        "stop_reason": "Grace period (8/10 days)",
        "entry_price": 243.00,
        "current_price": 250.38,
        "shares": 5.5,
        "pnl": 29.06,
        "pnl_pct": 2.98,
        "current_stop": 0,
        "holding_days": 8,
        "grace_period": true
      }
    ]
  }
}
```

### Stop Logic
- **Grace period (days 1-10):** No active stop
- **After grace period (profitable):** Tight 2×ATR trailing stop
- **After grace period (losing):** Wide 5×ATR stop

---

## 6. Cash Management (New in v1.1)

### POST /cash/transaction

### Purpose
- Record deposits and withdrawals
- Updates portfolio cash balance
- Required for accurate P&L calculation

### Request
```json
{
  "type": "deposit",
  "amount": 1000.00,
  "date": "2026-01-31",
  "note": "Monthly savings"
}
```

### Response
```json
{
  "status": "ok",
  "data": {
    "transaction": {
      "id": "uuid",
      "type": "deposit",
      "amount": 1000.00,
      "date": "2026-01-31",
      "note": "Monthly savings",
      "created_at": "2026-01-31T18:42:10"
    },
    "new_balance": 1532.62
  }
}
```

### Validation
- Withdrawals cannot exceed available cash
- Amount must be positive
- Type must be "deposit" or "withdrawal"

---

### GET /cash/transactions

### Purpose
- List all cash transactions
- Used for transaction history in modal

### Query Parameters
- `order`: ASC | DESC (default: DESC)

### Response
```json
{
  "status": "ok",
  "data": [
    {
      "id": "uuid",
      "type": "deposit",
      "amount": 5000.00,
      "date": "2026-01-23",
      "note": "Initial deposit",
      "created_at": "2026-01-23T10:00:00"
    }
  ]
}
```

---

### GET /cash/summary

### Purpose
- Get aggregated cash flow statistics

### Response
```json
{
  "status": "ok",
  "data": {
    "total_deposits": 6000.00,
    "total_withdrawals": 500.00,
    "net_cash_flow": 5500.00,
    "current_cash": 532.62
  }
}
```

---

## 7. Portfolio History (New in v1.1)

### POST /portfolio/snapshot

### Purpose
- Create daily snapshot of portfolio performance
- Should be called once per day (automated via cron)
- Idempotent (safe to call multiple times per day)

### Response
```json
{
  "status": "ok",
  "data": {
    "id": "uuid",
    "portfolio_id": "uuid",
    "snapshot_date": "2026-01-31",
    "total_value": 5133.52,
    "cash_balance": 532.62,
    "positions_value": 4600.90,
    "total_pnl": 133.52,
    "position_count": 5,
    "created_at": "2026-01-31T16:00:00"
  }
}
```

---

### GET /portfolio/history

### Purpose
- Retrieve historical portfolio snapshots
- Used for performance charts

### Query Parameters
- `days`: Number of days to retrieve (default: 30)

### Response
```json
{
  "status": "ok",
  "data": [
    {
      "date": "2026-01-23",
      "total_value": 5000.00,
      "cash_balance": 5000.00,
      "positions_value": 0,
      "total_pnl": 0,
      "position_count": 0
    },
    {
      "date": "2026-01-24",
      "total_value": 5050.20,
      "cash_balance": 532.62,
      "positions_value": 4517.58,
      "total_pnl": 50.20,
      "position_count": 5
    }
  ]
}
```

---

## 8. Settings

### GET /settings

### Purpose
- Get strategy configuration

### Response
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

### POST /settings

### Purpose
- Create initial settings

### PATCH /settings/{id}

### Purpose
- Update settings

---

## 9. Trade History

### GET /trades

### Response
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

## Key Changes from v1.0

### New Features
1. **Cash Management**
   - Track deposits/withdrawals
   - Accurate P&L accounting
   - Transaction history

2. **Portfolio History**
   - Daily snapshots
   - Performance tracking over time
   - Chart data support

3. **Multi-Currency Support**
   - Live FX rates from Yahoo Finance
   - Dual price fields (GBP + native)
   - Proper currency conversion

4. **Enhanced Position Data**
   - Grace period status
   - Stop reason explanations
   - Both display and calculation values

### Breaking Changes
- `/positions` now returns both GBP and native prices
- `/portfolio` includes `net_deposits` field
- P&L calculation now accounts for cash transactions

---

## Explicit Non-Requirements (v1.1)

- No PATCH endpoints for positions
- No partial updates
- No strategy configuration APIs beyond settings
- No charting APIs (frontend responsibility)
- No broker integrations
- No multi-user identifiers
- No trade notes (planned for v1.2)

---

## Versioning
- All endpoints are implicitly v1.1
- Strategy rules are versioned internally only

---

## Next Version (v1.2) Preview

Planned additions:
- Trade notes/journal
- Performance analytics endpoints
- Alert/notification system
- Position sizing calculator
