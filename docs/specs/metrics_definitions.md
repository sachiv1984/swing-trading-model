# Metrics Definitions - Canonical Specification

**Version:** 1.5.0  
**Owner:** Analytics Team  
**Last Updated:** 2026-02-16  
**Review Cycle:** Monthly

---

## Purpose

This document defines the **canonical calculation method** for every metric in the analytics system. All implementations (backend, frontend, validation) MUST match these specifications exactly.

**Authority**: This document supersedes any conflicting documentation in:
- `api_contracts.md`
- `frontend_spec.md`
- `implementation_notes.md`

If discrepancies exist, this document is correct and others must be updated.

---

## Metric Hierarchy

### Tier 1: Critical Metrics (Directly Affect Trading Decisions)
- Sharpe Ratio
- Max Drawdown
- Days Underwater
- R-Multiple (when available)

### Tier 2: Important Metrics (Inform Strategy Refinement)
- Win Rate
- Profit Factor
- Risk/Reward Ratio
- Expectancy

### Tier 3: Supporting Metrics (Context and Detail)
- Win/Loss Streaks
- Holding Period Analysis
- Trade Frequency

---

## Sharpe Ratio

### Definition
Risk-adjusted return metric comparing average return to volatility.

### Formula

**Method Selection** (Priority Order):

1. **Portfolio-Based** (PREFERRED - requires 30+ daily snapshots):
```
Daily Returns = [(Value_today - Value_yesterday) / Value_yesterday] × 100
Average Daily Return = Mean(Daily Returns)
Standard Deviation = StdDev(Daily Returns)
Sharpe Ratio = (Average Daily Return / Standard Deviation) × √252
```

2. **Trade-Based** (FALLBACK - requires 10+ closed trades):
```
For each trade:
  Annualized Return = (PnL% / Holding Days) × 252
  
Average Annualized Return = Mean(All Annualized Returns)
Standard Deviation = StdDev(All Annualized Returns)
Sharpe Ratio = Average Annualized Return / Standard Deviation
```

3. **Insufficient Data**: Return 0.0

### Implementation Notes

**Why Portfolio-Based is Preferred**:
- More accurate for actual risk experienced
- Captures correlation between positions
- Reflects portfolio-level volatility
- Industry standard method

**Trade-Based Limitations**:
- Assumes trades are independent
- Ignores timing of cash flows
- May overstate or understate true risk
- Use only when portfolio history unavailable

### Data Requirements

| Method | Min Data | Optimal Data | Notes |
|--------|----------|--------------|-------|
| Portfolio | 30 snapshots | 252 snapshots (1 year) | Daily snapshots required |
| Trade | 10 trades | 30+ trades | Closed trades only |

### Response Format
```json
{
  "sharpe_ratio": 1.23,
  "sharpe_method": "portfolio",
  "data_points": 45,
  "confidence": "medium"
}
```

### Validation

**Tolerance**: ±0.01 (1 basis point)

**Test Cases**:
```python
# Portfolio-based with perfect monthly 10% returns
Input: 12 months of +10% returns
Expected: ~12.6 (High Sharpe, low volatility)

# Trade-based with mixed results
Input: 10 trades, 60% win rate, avg win 15%, avg loss -8%
Expected: ~1.5-2.0 (Moderate Sharpe)
```

### Known Limitations

1. **Lookback Period**: Short periods (<3 months) produce unreliable Sharpe ratios
2. **Non-Normal Returns**: Sharpe assumes normal distribution; skewed returns may mislead
3. **Leverage**: Does not adjust for leverage; levered portfolios may show inflated Sharpe
4. **Survivorship Bias**: Only includes active accounts; failed accounts excluded

### Troubleshooting

**Issue**: Sharpe ratio is 0.0 despite profitable trades  
**Cause**: Insufficient data (< 30 snapshots and < 10 trades)  
**Solution**: Wait for more trading history

**Issue**: Sharpe ratio changes drastically between method  
**Cause**: Trade timing not captured in trade-based calculation  
**Solution**: Use portfolio-based method (more accurate)

---

## Max Drawdown

### Definition
Largest peak-to-trough decline in portfolio value, expressed as percentage.

### Formula
```
For each day in portfolio history:
  Running Peak = Maximum(All Previous Values including today)
  Drawdown Today = (Current Value - Running Peak) / Running Peak × 100
  
Max Drawdown = Minimum(All Drawdowns)  # Most negative value
```

### Calculation Method

**Step 1**: Sort portfolio history chronologically  
**Step 2**: Initialize peak = 0  
**Step 3**: For each snapshot:
- If `current_value > peak`: `peak = current_value`, `drawdown = 0`
- Else: `drawdown = ((current_value - peak) / peak) × 100`
- Track: `max_drawdown = min(max_drawdown, drawdown)`

**Step 4**: Return `max_drawdown` (negative number)

### Data Requirements

| Requirement | Min | Optimal | Notes |
|-------------|-----|---------|-------|
| Snapshots | 2 | 252 (1 year) | Daily snapshots |
| Trading History | None | 3+ months | More data = more accurate |

### Response Format
```json
{
  "max_drawdown": {
    "percent": -25.38,
    "amount": 1250.00,
    "date": "2026-01-15",
    "days_to_recovery": 45,
    "recovered": true
  }
}
```

### Validation

**Tolerance**: ±0.1% (10 basis points)

**Test Cases**:
```python
# Simple peak-trough-recovery
Input: [10000, 12000, 9000, 11000]
Expected: -25.0% (from 12000 to 9000)

# Multiple drawdowns
Input: [10000, 9000, 10500, 8500, 11000]
Expected: -19.05% (from 10500 to 8500)
```

### Interpretation

| Max DD | Risk Level | Typical Use Case |
|--------|------------|------------------|
| 0% to -10% | Low | Conservative, capital preservation |
| -10% to -20% | Moderate | Balanced growth |
| -20% to -30% | High | Aggressive growth |
| > -30% | Very High | Speculative |

### Known Limitations

1. **Historical**: Only reflects past drawdowns, not future risk
2. **Path Dependent**: Depends on when you started measuring
3. **Recovery Blind**: Doesn't show how long recovery took
4. **No Probability**: Can't predict likelihood of future drawdowns

---

## Days Underwater

### Definition
Number of **calendar days** since portfolio last reached its all-time peak equity.

### Formula
```
Peak Equity = Maximum(All Historical Equity Values)
Peak Date = Date when Peak Equity was achieved

IF Current Equity >= Peak Equity:
  Days Underwater = 0  # Currently at peak
ELSE:
  Days Underwater = Today - Peak Date  # Days since peak
```

### Calculation Method

**Step 1**: Find all-time peak equity from portfolio history  
**Step 2**: Find date when peak occurred  
**Step 3**: Calculate: `days_underwater = (today - peak_date).days`  
**Step 4**: If current equity ≥ peak equity, return 0

### Data Requirements

| Requirement | Min | Notes |
|-------------|-----|-------|
| Portfolio History | 1 snapshot | Returns 0 if insufficient data |
| Current Equity | Required | From `/portfolio` endpoint |

### Response Format
```json
{
  "days_underwater": 0,
  "peak_equity": 15234.50,
  "peak_date": "2026-02-10",
  "current_equity": 15450.00,
  "is_at_peak": true
}
```

### Validation

**Tolerance**: Exact match (integer days)

**Test Cases**:
```python
# At peak
Input: peak = 15000, current = 15000
Expected: 0 days

# Below peak (10 days ago)
Input: peak = 15000 on 2026-02-05, current = 14500 on 2026-02-15
Expected: 10 days

# New peak
Input: peak = 15000, current = 15500
Expected: 0 days (new peak established)
```

### Interpretation

| Days UW | Status | Action |
|---------|--------|--------|
| 0 | At Peak | Normal operations |
| 1-30 | Recent Drawdown | Monitor closely |
| 31-90 | Extended Drawdown | Review strategy |
| 90+ | Prolonged Drawdown | Consider reset |

### Important Notes

**This metric measures TIME, not DEPTH**:
- A portfolio 1% below peak for 90 days = 90 days underwater
- A portfolio 30% below peak for 10 days = 10 days underwater
- Use with Max Drawdown for complete picture

### Known Limitations

1. **Path Dependent**: Sensitive to historical peak timing
2. **No Severity**: Doesn't indicate how far underwater
3. **Misleading for New Accounts**: Short history = low days underwater
4. **Volatile Peaks**: Briefly hitting new peak resets counter

---

## R-Multiple

### Definition
Ratio of actual profit/loss to initial risk (measured by stop distance).

### Formula
```
Initial Risk = Entry Price - Stop Price
Actual PnL = Exit Price - Entry Price
R-Multiple = Actual PnL / Initial Risk
```

### Examples
```
Trade 1: Entry $100, Stop $95, Exit $110
Initial Risk = $5
Actual PnL = $10
R-Multiple = 10 / 5 = 2.0R (Won 2× risk)

Trade 2: Entry $100, Stop $95, Exit $92
Initial Risk = $5
Actual PnL = -$8
R-Multiple = -8 / 5 = -1.6R (Lost 1.6× risk)
```

### Data Requirements

| Field | Required | Source | Notes |
|-------|----------|--------|-------|
| entry_price | Yes | Positions table | Native currency |
| stop_price | Yes | Positions table | Must be set at entry |
| exit_price | Yes | Trade history | User-provided |
| shares | Yes | Positions table | For total PnL |

**Critical**: R-Multiple **cannot be calculated** without initial stop_price.

### Calculation Method

**Implementation Location**: FRONTEND ONLY  
**File**: `src/components/analytics/RMultipleAnalysis.js`

**Rationale**: 
- Requires stop_price which isn't always in trade_history
- Position-level metric, not portfolio-level
- Frontend has full position context
```javascript
// Frontend calculation
const calculateRMultiples = () => {
  return trades
    .filter(t => t.stop_price && t.entry_price && t.exit_price)
    .map(t => {
      const risk = Math.abs(t.entry_price - t.stop_price);
      const pnl = t.exit_price - t.entry_price;
      const rMultiple = risk === 0 ? 0 : pnl / risk;
      return { ...t, rMultiple };
    });
};
```

### Response Format

**Note**: This metric is NOT in `/analytics/metrics` endpoint.  
**Access**: Via frontend calculation only.
```javascript
// Frontend state
{
  tradesWithR: [
    {
      ticker: "NVDA",
      rMultiple: 2.5,
      entry_price: 850,
      stop_price: 820,
      exit_price: 925
    }
  ],
  avgR: 1.2,
  distribution: {
    "negative": 20,  // 20% of trades
    "0-1R": 30,
    "1-2R": 30,
    "2R+": 20
  }
}
```

### Validation

**Not applicable** - Frontend-only calculation, no backend validation.

### Known Limitations

1. **Stop Must Exist**: Trades without stops excluded from analysis
2. **Frontend Only**: Not available in API endpoints
3. **No Historical Trend**: Can't query "R-Multiple over time" via API
4. **Manual Stops**: Relies on user setting accurate stops at entry

### Future Considerations

**Should R-Multiple move to backend?**

**Pros**:
- Consistent with other metrics
- Available via API
- Can be validated
- Historical trending possible

**Cons**:
- Requires stop_price in trade_history (data migration)
- Many historical trades lack stops
- Frontend implementation working well

**Decision**: Leave frontend-only for now, revisit in v2.0.

---

## Win Rate

### Definition
Percentage of closed trades that resulted in profit.

### Formula
```
Winners = Count(Trades where PnL > 0)
Total Trades = Count(All Closed Trades)
Win Rate = (Winners / Total Trades) × 100
```

### Data Requirements

| Requirement | Min | Optimal |
|-------------|-----|---------|
| Closed Trades | 10 | 30+ |

### Response Format
```json
{
  "win_rate": 58.5,
  "winners": 23,
  "losers": 17,
  "total_trades": 40,
  "scratch_trades": 0
}
```

### Validation

**Tolerance**: ±0.5%

### Known Limitations

1. **Size Blind**: Doesn't account for win/loss magnitude
2. **Misleading Alone**: 90% win rate with small wins and large losses = losing strategy
3. **Always Use With**: Profit Factor, Risk/Reward Ratio

---

## Profit Factor

### Definition
Ratio of gross profits to gross losses.

### Formula
```
Gross Profit = Sum(All Winning Trades PnL)
Gross Loss = Absolute Value(Sum(All Losing Trades PnL))
Profit Factor = Gross Profit / Gross Loss
```

### Interpretation

| Profit Factor | Assessment |
|---------------|------------|
| < 1.0 | Losing strategy |
| 1.0 - 1.5 | Marginal |
| 1.5 - 2.0 | Good |
| 2.0 - 3.0 | Excellent |
| > 3.0 | Exceptional (verify) |

### Response Format
```json
{
  "profit_factor": 2.45,
  "gross_profit": 12500.00,
  "gross_loss": 5100.00,
  "interpretation": "excellent"
}
```

### Validation

**Tolerance**: ±0.02

---

## Appendix A: Data Lineage
```
User Deposits Cash
    ↓
cash_transactions table
    ↓
Portfolio Cash Balance Updated
    ↓
User Enters Position
    ↓
positions table (entry_price, shares, stop_price)
    ↓
Daily Price Updates (Yahoo Finance API)
    ↓
positions.current_price updated
    ↓
Daily P&L Calculated
    ↓
Position Exited
    ↓
trade_history table (entry_price, exit_price, pnl, holding_days)
    ↓
Analytics Metrics Calculated
    ↓
    ├→ Sharpe Ratio (from portfolio_history or trade_history)
    ├→ Max Drawdown (from portfolio_history)
    ├→ Win Rate (from trade_history)
    ├→ Profit Factor (from trade_history)
    └→ R-Multiple (frontend-only, from trade_history + positions)
    ↓
Displayed in UI
```

---

## Appendix B: Change Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-02-16 | 1.5.0 | Initial comprehensive spec | Analytics Team |
| TBD | 1.5.1 | Add Kelly Criterion | TBD |

---

## Appendix C: Review Checklist

Monthly Review (First Monday):
- [ ] Verify all implementations match spec
- [ ] Run validation suite (`POST /validate/calculations`)
- [ ] Check for new metrics to document
- [ ] Update test cases if formulas changed
- [ ] Confirm data lineage still accurate
