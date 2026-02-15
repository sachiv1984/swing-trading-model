# Strategy Rules – Momentum Trading Assistant

**Version:** 1.2  **Last Updated:** February 15, 2026

This document outlines the trading strategy rules and position management logic implemented in the **Position Manager Web App**. It reflects the rules used in the production backtest and live system, with clarifications to ensure full accuracy.

---

## 1. Position Entry Rules

### Manual Entry

- Positions are entered manually via the web interface
- Each position requires:
  - Ticker symbol
  - Entry date
  - Number of shares (fractional supported)
  - Entry price
  - ATR value (for stop calculation)
  - Market (US/UK – auto-detected from ticker)

**Note:** While the strategy itself is rule-based, this system uses **manual execution based on generated signals** rather than automated order placement.

### Automatic Fee Calculation

#### UK Positions (Backtest Model)

- Stamp Duty: **0.5%** of gross buy cost
- No explicit commission modelled
- No sell-side fees

#### US Positions

- FX Fee: **0.15%** of gross cost in USD
- Commission: £0 (zero-commission brokers)
- Fees converted to GBP using live FX rate

---

## 2. Initial Stop Calculation

At entry, an initial protective stop is calculated using a **wide ATR multiple**:

```text
Initial Stop = Entry Price - (5 × ATR)
```

**Purpose:**

- Prevent premature exits
- Allow normal price discovery after entry
- Provide downside protection without tight constraint

This stop is stored immediately but is **not enforced during the grace period**.

---

## 3. Grace Period (Days 0–10)

### Purpose

Prevent premature stop-outs on new positions due to normal market volatility.

### Rules

- **Duration:** 10 calendar days from entry (days 0–9 inclusive)
- **Stop Exists:** Initial stop is calculated and stored
- **Stop NOT Enforced:** Position cannot be stopped out during this period
- **UI Display:** Shows `Grace period (X/10 days)` instead of stop price
- **Manual Exit:** Always allowed

### Timeline

- Day 0–9: Grace period active, no stop enforcement
- Day 10+: Stop-loss rules become active

---

## 4. Trailing Stop-Loss Rules (After Grace Period)

### ATR-Based Stops

- **ATR Period:** 14 days (rolling)
- **ATR Source:** Daily high / low / close data

### Stop Multipliers (Profit-Lock Logic)

#### Profitable Positions (P&L > 0%)

```python
ATR Multiplier = 2
New Stop = Current Price - (2 × ATR)
```

- Tight trailing stop
- Locks in gains
- Reduces drawdowns after profits emerge

#### Losing Positions (P&L ≤ 0%)

```python
ATR Multiplier = 5
New Stop = Current Price - (5 × ATR)
```

- Wide stop
- Allows room for recovery
- Avoids noise-driven exits

### Trailing Logic

```python
Updated Stop = max(Current Stop, New Stop)
```

**Key Rule:**

- Stops **never move downwards**
- Once tightened, a stop is never loosened
- Stops may initially be below entry price

---

## 5. Stop Update Frequency

- Stops are recalculated **daily** via `/positions/analyze`
- Can be triggered manually or by automated cron job
- Recommended timing: **market close (4 PM UTC, weekdays)**

---

## 6. Exit Conditions

Positions are exited under **three conditions**:

### 1. Stop Loss Hit

```python
if holding_days >= 10 and current_price <= stop_price:
    EXIT
```

- Only enforced after grace period
- Triggered by trailing stop logic
- Exit is **recommended automatically**
- Requires **manual confirmation** to execute

---

### 2. Risk-Off Market Signal

#### Market Regime Definition

- **US Stocks:** SPY > 200-day MA → Risk-On
- **UK Stocks:** FTSE > 200-day MA → Risk-On

```python
if market_risk_off:
    EXIT
```

- Applies regardless of stop price
- Designed to protect capital during regime shifts

---

### 3. Manual Exit

- User-initiated at any time
- Available even during grace period
- Executes at current market price

---

## 7. Multi-Currency Support

### GBP as Base Currency

All portfolio calculations are performed in GBP:

- Portfolio value
- Cash balance
- P&L tracking
- Stop prices (stored in database)

### USD Positions

- Market data fetched in USD
- Live GBP/USD FX rate applied
- Converted to GBP for aggregation
- Displayed in USD to user

---

## 8. Profit & Loss Calculation

### Position-Level P&L

```python
P&L = (Current Price - Entry Price) × Shares
P&L % = ((Current Price - Entry Price) / Entry Price) × 100
```

### Portfolio-Level P&L

```python
Net Cash Flow = Deposits - Withdrawals
Portfolio P&L = Current Value - Net Cash Flow
```

Ensures accuracy when capital is added or removed.

---

## 9. Position States

### GRACE (Days 0–9)

- Stop calculated but inactive
- No automatic exit
- Manual exit allowed

### LOSING (Day 10+, P&L ≤ 0)

- Wide 5×ATR trailing stop
- Stop may remain below entry

### PROFITABLE (Day 10+, P&L > 0)

- Tight 2×ATR trailing stop
- Profit-lock behaviour active

### EXIT

- Stop hit or risk-off signal
- Awaiting manual confirmation

---

## 10. Risk Management Summary

### Position-Level Risk

- 10-day grace period
- Wide stops while losing
- Tight stops once profitable
- No stop loosening

### Portfolio-Level Risk

- Market regime override (risk-off exit)
- Currency risk tracked via FX rates
- Cash flow–aware P&L

---

## 11. Trade Sizing (Informational)

```text
Risk per Trade = 1–2% of Portfolio
Position Size = Risk Amount / Stop Distance
```

*Note: The backtest uses inverse-volatility weighting. This sizing logic is informational and planned for future implementation.*

---

## 12. Settings & Configuration

```python
min_hold_days = 10
atr_multiplier_initial = 5
atr_multiplier_trailing = 2
atr_period = 14
stamp_duty_rate = 0.005
fx_fee_rate = 0.0015
```

These align with the production backtest that achieved:

- **26.37% CAGR**
- **1.29 Sharpe Ratio**
- **−25.38% Maximum Drawdown**

---

## 13. System Boundaries

### This System IS

- Decision-support tool
- Manual execution framework
- Deterministic rule engine
- Risk-managed trailing stop system

### This System IS NOT

- Automated trading bot
- Broker integration
- Real-time tick execution engine

---

## 14. Core Principles

1. Human-in-the-loop execution
2. Rules are deterministic and frozen
3. Backend is the source of truth
4. Grace period prevents noise exits
5. Profits are protected aggressively
6. Losses are given room to resolve
7. Stops only tighten, never loosen

---

**Document Status:** Current  **Matches:** Backtest v1.0, API v1.1  **Last Review:** February 15, 2026
