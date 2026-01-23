# Strategy Rules

This document outlines the trading strategy rules and position management logic used in the **Position Manager Web App**.

---

## 1. Position Entry Rules

- Positions are entered via the “Entry Signals” module.
- Each position includes:
  - Ticker symbol
  - Entry price
  - Number of shares
  - Initial stop-loss level
  - Entry date

- Positions cannot be exited before a minimum holding period (default: 10 days).

---

## 2. Stop-Loss Rules

- **ATR-based stops** are used to manage risk.
- Parameters:
  - `initial_atr_mult`: 5 → used for new or losing positions (wide stop)
  - `profit_atr_mult`: 2 → used for profitable positions (tight stop)
  - `atr_period`: 14 → period for Average True Range calculation

- Stop-loss is **trailing**:
  - Stops can only move up to protect profits.
  - Stops are **inactive during the grace period** (minimum holding period).

- Stop-loss is triggered if:
  - Current price ≤ trailing stop after grace period.

---

## 3. Market Regime Rules

- Market risk-on/off status is checked daily:
  - **SPY** for US equities
  - **FTSE** for UK equities
- Risk-on conditions:
  - Current price > 200-day moving average
- Exit positions if market is risk-off.

---

## 4. Position Exit Rules

Positions are exited under the following conditions:

1. **Stop-Loss Hit**
   - Price falls below calculated stop after grace period.
2. **Risk-Off Market Signal**
   - Market regime is risk-off for the position’s region.
3. **Manual Exit**
   - Optional manual override from the web interface.

---

## 5. Profit & Loss

- P&L is tracked daily:
  - Absolute: `(Current Price - Entry Price) * Shares`
  - Percentage: `((Current Price - Entry Price)/Entry Price) * 100`

- P&L is used to adjust ATR-based stops.

---

## 6. Grace Period

- Default: 10 days
- Purpose: prevent early stop-outs for new positions
- Stop-loss becomes active after this period

---

## 7. Portfolio Aggregation

- Total portfolio value = cash + current positions value
- Daily summary includes:
  - Cash
  - Positions value
  - Total P&L
  - Risk-on/off market status