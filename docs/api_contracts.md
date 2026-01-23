# API Contracts — Momentum Trading Assistant (MVP)

## Overview

This document defines the backend API contracts for the **Momentum Trading Assistant** web application.

The system is a **decision-support tool**, not a trading bot.  
All strategy logic is deterministic, server-side, and frozen for MVP.

---

## Design Principles

- Backend is the **single source of truth**
- Frontend must never calculate:
  - ATR
  - Stops
  - Market regime
  - P&L
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
{
  "status": "ok",
  "data": { }
}

### Error
{
  "status": "error",
  "message": "Human-readable explanation"
}

## 1. Dashboard

### GET /dashboard

### Purpose
- Daily snapshot
- First screen after login

Response
```json
{
  "portfolio_value": 24500.75,
  "cash": 8200.00,
  "cash_pct": 33.5,
  "positions_value": 16300.75,
  "open_positions": 5,
  "exit_alerts": 2,
  "market_status": {
    "date": "2026-01-22",
    "spy": {
      "risk_on": true,
      "price": 512.34,
      "ma200": 488.91
    },
    "ftse": {
      "risk_on": false,
      "price": 7482.10,
      "ma200": 7601.44
    }
  }
}

## 2. Portfolio Overview

### GET /portfolio

Purpose
	•	Primary working screen
	•	Replaces CLI portfolio view

Response 
{
  "cash": 8200.00,
  "last_updated": "2026-01-22 18:42:10",
  "positions": [
    {
      "ticker": "PLTR",
      "market": "US",
      "entry_date": "2025-12-05",
      "entry_price": 21.45,
      "shares": 300,
      "current_price": 25.30,
      "current_value": 7590.00,
      "pnl": 1155.00,
      "pnl_pct": 17.9,
      "current_stop": 23.10,
      "holding_days": 48,
      "status": "PROFITABLE"
    }
  ]
}

Allowed status values
	•	GRACE
	•	PROFITABLE
	•	LOSING
	•	EXIT


## 3. Add Position (Manual Entry)

### POST /portfolio/position

Purpose
	•	Manual sync with broker executions

Response
{
  "ticker": "FRES.L",
  "entry_date": "2026-01-10",
  "shares": 400,
  "fill_price": 5.82,
  "fill_currency": "GBP",
  "fx_rate": null,
  "atr": 0.12,
  "custom_stop": null
}

Response
{
  "ticker": "FRES.L",
  "total_cost": 2340.96,
  "fees_paid": 11.70,
  "entry_price": 5.85,
  "initial_stop": 5.25,
  "remaining_cash": 5859.04
}

## 4. Position Detail

### GET /positions/{ticker}

Purpose
	•	Explain why a position is being held or exited

Response
{
  "ticker": "PLTR",
  "market": "US",
  "entry_date": "2025-12-05",
  "entry_price": 21.45,
  "shares": 300,
  "holding_days": 48,
  "current_price": 25.30,
  "atr": 0.92,
  "current_stop": 23.10,
  "stop_logic": {
    "atr_multiplier": 2,
    "reason": "Profitable position using tight trailing stop"
  },
  "pnl": 1155.00,
  "pnl_pct": 17.9,
  "risk_status": "RISK_ON"
}

## 5. Daily Analysis (Core Engine)

### GET /positions/analyze

Purpose
	•	Runs full daily monitoring logic
	•	Idempotent (safe to refresh)

Response
{
  "analysis_date": "2026-01-22",
  "summary": {
    "total_value": 16300.75,
    "total_pnl": 2150.30,
    "exit_count": 2
  },
  "actions": [
    {
      "ticker": "AAPL",
      "action": "EXIT",
      "exit_reason": "Stop Loss Hit",
      "entry_price": 182.40,
      "current_price": 174.10,
      "shares": 50,
      "pnl": -415.00,
      "pnl_pct": -4.5,
      "current_stop": 175.20,
      "holding_days": 32
    },
    {
      "ticker": "PLTR",
      "action": "HOLD",
      "stop_reason": "Profitable (tight 2x ATR)",
      "current_stop": 23.10
    }
  ]
}

## 6. Confirm Exit Execution

### POST /positions/exit-confirm

Purpose
	•	Manual confirmation after broker execution

Request
{
  "ticker": "AAPL",
  "exit_price": 174.05,
  "exit_date": "2026-01-22"
}

Response
{
  "ticker": "AAPL",
  "net_proceeds": 8702.50,
  "realized_pnl": -412.50,
  "new_cash_balance": 12890.25
}

## 7. Trade History

### GET /trades

Purpose
	•	Performance review
	•	Not required for daily use

Response
{
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
      "exit_reason": "Risk-Off Signal"
    }
  ]
}

Explicit Non-Requirements (MVP)
	•	No PATCH endpoints
	•	No partial updates
	•	No strategy configuration APIs
	•	No charting APIs
	•	No broker integrations
	•	No multi-user identifiers


Versioning
	•	All endpoints are implicitly v1
	•	Strategy rules are versioned internally only

Final Guidance

Do not optimise, generalise, or parameterise the strategy.
If something feels like it should be configurable, flag it for v2 — do not build it.

