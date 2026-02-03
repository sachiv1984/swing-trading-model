# Strategy Rules - Momentum Trading Assistant

**Version:** 1.1  
**Last Updated:** February 3, 2026

This document outlines the trading strategy rules and position management logic implemented in the **Position Manager Web App**.

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
  - Market (US/UK - auto-detected from ticker)

### Automatic Fee Calculation
- **UK Positions:**
  - Commission: £9.95 flat fee
  - Stamp Duty: 0.5% of gross cost
  - Total fees added to position cost
  
- **US Positions:**
  - FX Fee: 0.15% of gross cost in USD
  - Commission: £0 (zero commission brokers)
  - Fees calculated in GBP using live FX rate

### Initial Stop Calculation
```
Initial Stop = Entry Price - (2 × ATR)
```

This provides initial downside protection at entry.

---

## 2. Grace Period (Days 0-10)

### Purpose
Prevent premature stop-outs on new positions due to normal market volatility.

### Rules
- **Duration:** 10 days from entry (days 0-9 inclusive)
- **Stop Exists:** Initial stop is calculated and stored in database
- **Stop NOT Enforced:** Position cannot be stopped out during this period
- **UI Display:** Shows "Grace period (X/10 days)" instead of stop price
- **Manual Exit:** Still allowed during grace period

### Example
- Day 0-9: Grace period active, no stop loss
- Day 10+: Stop loss becomes active and enforced

---

## 3. Trailing Stop-Loss Rules (After Grace Period)

### ATR-Based Stops
- **ATR Period:** 14 days (rolling window)
- **Calculation:** Average True Range from daily high/low/close data

### Stop Multipliers (Based on Profitability)

**Profitable Positions (P&L > 0%):**
```python
ATR Multiplier = 2  # Tight trailing stop
New Stop = Current Price - (2 × ATR)
Purpose: Protect profits, lock in gains
```

**Losing Positions (P&L ≤ 0%):**
```python
ATR Multiplier = 5  # Wide stop
New Stop = Current Price - (5 × ATR)
Purpose: Give position room to recover
```

### Trailing Logic
```python
# Stops only move UP, never down
Updated Stop = max(Current Stop, New Stop)
```

### Stop Update Frequency
- Stops recalculated daily via `/positions/analyze` endpoint
- Can be triggered manually or via automated cron job
- Recommended: Run at market close (4 PM UTC weekdays)

### Example - Profitable Position
```
Entry: $500
Current Price: $600 (+20%)
ATR: $20
New Stop: $600 - (2 × $20) = $560
Previous Stop: $500 (at entry)
Updated Stop: max($500, $560) = $560 ✓
```

### Example - Losing Position
```
Entry: £100
Current Price: £90 (-10%)
ATR: £5
New Stop: £90 - (5 × £5) = £65
Previous Stop: £100 (at entry)  
Updated Stop: max(£100, £65) = £100 ✓ (stays at entry)
```

**Key Point:** Stops never move below entry price, providing entry-level protection.

---

## 4. Exit Conditions

Positions are exited under three conditions:

### 1. Stop Loss Hit
```python
if holding_days >= 10 and current_price <= stop_price:
    EXIT
```

- Only after grace period
- Price must fall below trailing stop
- Automatic recommendation from `/positions/analyze`
- Requires manual confirmation to execute

### 2. Risk-Off Market Signal

**Market Regime Check:**
- **US Stocks:** SPY > 200-day MA = Risk-On
- **UK Stocks:** FTSE > 200-day MA = Risk-On

```python
if market_risk_off:
    EXIT  # Regardless of stop price
```

Purpose: Exit all positions when market conditions deteriorate.

### 3. Manual Exit
- User-initiated via "Exit" button
- Available at any time (even during grace period)
- No stop loss required
- Executes at current market price

---

## 5. Multi-Currency Support

### GBP as Base Currency
All portfolio calculations done in GBP:
- Total portfolio value
- Cash balance
- P&L tracking
- Stop prices (stored in database)

### USD Positions
- Prices fetched in USD from Yahoo Finance
- Live FX rate fetched daily (GBP/USD)
- Converted to GBP for portfolio aggregation
- Displayed in USD to user (native currency)

### Dual Price Display
- **Backend:** Stores prices in GBP (calculations)
- **Frontend:** Displays prices in native currency (USD/GBP)

---

## 6. Profit & Loss Calculation

### Position-Level P&L
```python
# In native currency
P&L = (Current Price - Entry Price) × Shares

# Percentage
P&L % = ((Current Price - Entry Price) / Entry Price) × 100
```

### Portfolio-Level P&L
```python
# Accounts for deposits/withdrawals
Net Cash Flow = Total Deposits - Total Withdrawals
Portfolio P&L = Current Total Value - Net Cash Flow
```

This ensures accurate P&L even when adding/removing cash.

---

## 7. Daily Workflow

### Recommended Daily Routine

**1. Morning (Pre-Market)**
- Review overnight news
- Check market regime (SPY/FTSE vs 200MA)

**2. During Market Hours**
- Monitor positions in dashboard
- Manual entries for new positions

**3. Post-Market (4 PM UTC)**
```bash
# Automated via cron
curl http://api/positions/analyze  # Update stops, check exits
curl -X POST http://api/portfolio/snapshot  # Record daily snapshot
```

**4. Review Analysis Results**
- Check for EXIT recommendations
- Review stop prices
- Execute exits if recommended

---

## 8. Position States

### GRACE (Days 0-9)
- New position
- Stop calculated but not enforced
- No exit unless manual or risk-off

### PROFITABLE (Day 10+, P&L > 0)
- Tight 2×ATR trailing stop
- Stop actively enforced
- Protecting gains

### LOSING (Day 10+, P&L ≤ 0)
- Wide 5×ATR stop
- Room to recover
- Stop at entry minimum

### EXIT
- Stop hit or risk-off signal
- Awaiting manual confirmation
- Position still open until confirmed

---

## 9. Risk Management Summary

### Position-Level Risk
- **Grace Period:** 10 days to establish position
- **Losing Positions:** Wide 5×ATR stop (room to breathe)
- **Profitable Positions:** Tight 2×ATR stop (protect gains)
- **Minimum Protection:** Stop never below entry price

### Portfolio-Level Risk
- **Market Regime:** Exit all on risk-off signal
- **Currency Risk:** Tracked via live FX rates
- **Cash Management:** Track deposits for accurate P&L

### Trade Sizing (Recommended)
```
Risk per Trade = 1-2% of Portfolio
Position Size = Risk Amount / Stop Distance

Example:
Portfolio: £10,000
Risk: 2% = £200
Stop Distance: £5
Shares: £200 / £5 = 40 shares
```

*Note: Position sizing calculator planned for v1.3*

---

## 10. Settings & Configuration

Current configuration (stored in database):

```python
min_hold_days = 10              # Grace period
atr_multiplier_initial = 5      # Wide stop for losing positions
atr_multiplier_trailing = 2     # Tight stop for profitable positions
atr_period = 14                 # ATR calculation window
uk_commission = 9.95            # UK trading fee
stamp_duty_rate = 0.005         # UK stamp duty (0.5%)
fx_fee_rate = 0.0015            # US FX fee (0.15%)
```

These match the backtest parameters that produced:
- 26.37% CAGR
- 1.29 Sharpe Ratio
- -25.38% Maximum Drawdown

---

## 11. Important Distinctions from Typical Systems

### What This System IS:
✅ Decision support tool  
✅ Manual trade execution  
✅ Trailing stop recommendations  
✅ Risk management framework  

### What This System IS NOT:
❌ Automated trading bot  
❌ Signal generator for entries  
❌ Broker integration  
❌ Real-time tick data  

---

## 12. Key Principles

1. **Human-in-the-Loop:** All exits require manual confirmation
2. **Predictability:** Strategy rules are frozen and deterministic
3. **Backend Authority:** All calculations done server-side
4. **Grace Period First:** No premature exits on new positions
5. **Trail Profits:** Protect gains with tight stops
6. **Room for Recovery:** Wide stops on losing positions
7. **Never Below Entry:** Minimum protection at entry level

---

**Document Status:** Current  
**Matches:** Backtest v1.0, API v1.1  
**Last Review:** February 3, 2026
