# Metrics Definitions – Canonical Specification
**Version:** 1.5.6  
**Owner:** Analytics Team  
**Last Updated:** 2026-02-17  
**Review Cycle:** Monthly  

---

## Purpose
This document defines the **canonical calculation method** for every metric in the analytics system. All implementations (backend, frontend, validation) **MUST** match these specifications exactly.

**Authority**: This document supersedes any conflicting documentation in:
- `api_contracts.md`
- `frontend_spec.md`
- `implementation_notes.md`

**Completeness Guarantee**: Every metric returned by `GET /analytics/metrics` **MUST** have a corresponding section in this document. Any metric without a section is considered **undocumented and invalid** until this document is updated.

---

## Conventions (Applies Globally)
### Response Envelope
All successful responses use:
```json
{ "status": "ok", "data": {} }
```
All errors use:
```json
{ "status": "error", "message": "Human-readable explanation" }
```

### Currency
All monetary values returned by analytics endpoints are **GBP**.

### Period Filtering
`period` filters trades by `exit_date` and portfolio snapshots by `snapshot_date`.

### Minimum Trades Threshold
If `total_trades < min_required`, the API returns HTTP 200 with `has_enough_data: false` and empty `{}` metric objects.

---

## Metric Hierarchy
### Tier 1: Critical Metrics (Directly Affect Trading Decisions)
- Sharpe Ratio
- Max Drawdown
- Days Underwater
- R-Multiple (visualisation-only)

### Tier 2: Important Metrics (Inform Strategy Refinement)
- Win Rate
- Profit Factor
- Risk/Reward Ratio
- Expectancy

### Tier 3: Supporting Metrics (Context and Detail)
- Win Streak / Loss Streak
- Average Holding Period (Winners vs Losers)
- Trade Frequency
- Capital Efficiency
- Recovery Factor
- Consistency Metrics (object)

---

# Tier 1 Metrics

## Sharpe Ratio
### Definition
Risk-adjusted return metric comparing average return to volatility.

### Canonical Formula
**Method Selection** (priority order):

1) **Portfolio-Based** (preferred; requires 30+ portfolio snapshots):

```text
Daily Returns = [(Value_today - Value_yesterday) / Value_yesterday] × 100
Sharpe = (Mean(Daily Returns) / StdDev(Daily Returns)) × √252
```

2) **Trade-Based** (fallback; requires 10+ closed trades):

```text
For each trade:
  Holding Days = max(1, (exit_date - entry_date).days)
  Annualized Return = (pnl_percent / Holding Days) × 252
Sharpe = Mean(Annualized Returns) / StdDev(Annualized Returns)
```

3) Otherwise: return `0.0` with `sharpe_method = "insufficient_data"`.

### Variance / Standard Deviation Convention (CANONICAL)
Sharpe ratio volatility calculations MUST use **sample standard deviation** (Bessel-corrected), i.e. variance divided by **(n − 1)**.

```text
Sample variance:  s² = Σ(xᵢ − x̄)² / (n − 1)
Sample std dev:   s  = √s²
```

**Important:** The current implementation historically used population variance (÷ n). This is considered **non-conformant** with the canonical spec and is tracked as a backlog item (see Appendix E).

### Data Requirements
- Portfolio method: `portfolio_history.total_value` with ≥30 `snapshot_date` points.
- Trade method: ≥10 trades with `entry_date`, `exit_date`, `pnl_percent`.

### Response Format
Returned under `executive_metrics`:
```json
{ "sharpe_ratio": 1.29, "sharpe_method": "portfolio" }
```

### Validation
Tolerance: ±0.01

### Failure Behaviour
- If method thresholds are not met: `sharpe_ratio = 0.0`, `sharpe_method = "insufficient_data"`.

---

## Max Drawdown
### Definition
Largest peak-to-trough decline in portfolio value over the period. Reported as percent (negative or zero) and amount (positive).

### Canonical Formula (as implemented)
Using `portfolio_history.total_value` in chronological order:

```text
peak_equity = 0
max_dd_amount = 0
max_dd_percent = 0
max_dd_date = null

for each snapshot:
  equity = snapshot.total_value
  if equity > peak_equity: peak_equity = equity
  dd_amount = peak_equity - equity
  dd_percent = (dd_amount / peak_equity) × 100 if peak_equity > 0 else 0
  if dd_amount > max_dd_amount:
    max_dd_amount = dd_amount
    max_dd_percent = dd_percent
    max_dd_date = snapshot.snapshot_date

max_drawdown.percent = -max_dd_percent
max_drawdown.amount  = max_dd_amount
max_drawdown.date    = max_dd_date
```

### Data Requirements
- `portfolio_history` with ≥1 snapshot; meaningful drawdown requires ≥2.

### Response Format
```json
{
  "max_drawdown": { "percent": -7.70, "amount": 419.07, "date": "2026-02-10" }
}
```

### Validation
- Percent tolerance: ±0.1 (percentage points).

### Failure Behaviour
- If no snapshots: return zeros and `date: null`.

---

## Days Underwater
### Definition
`advanced_metrics.days_underwater` is defined as the **maximum number of days since the peak running equity**, computed from the cumulative sequence of trade P&L (trade-sequence method).

### Canonical Formula (trade-sequence based)
Trades ordered by `exit_date` ascending:

```text
running_equity = 0
peak_equity = 0
peak_date = null
max_days_underwater = 0

for each trade:
  running_equity += trade.pnl
  if running_equity >= peak_equity:
    peak_equity = running_equity
    peak_date = trade.exit_date
    current_days_underwater = 0
  else if peak_date is not null:
    current_days_underwater = (trade.exit_date - peak_date).days
    max_days_underwater = max(max_days_underwater, current_days_underwater)

days_underwater = max_days_underwater
```

### Data Requirements
- Closed trades with `pnl` and `exit_date`.

### Response Format
Returned under `advanced_metrics`:
```json
{ "days_underwater": 0, "peak_date": "2026-02-11" }
```

### Validation
Exact match (integer days).

### Notes
A portfolio-snapshot definition of “days underwater” exists in earlier drafts, but the live API field `advanced_metrics.days_underwater` is trade-sequence based.

---

## R-Multiple (Visualisation-Only)
### Definition
Ratio of profit/loss to initial risk based on stop distance. Used only for client-side visualisation.

### Formula
```text
R = (exit_price - entry_price) / (entry_price - stop_price)
```

### Implementation
Client-side only for visualisation (not part of `GET /analytics/metrics`).

---

# Tier 2 Metrics

## Win Rate
### Definition
Percentage of closed trades with positive P&L.

### Formula
```text
win_rate = (count(pnl > 0) / total_trades) × 100
```

### Validation
Tolerance: ±0.5 (percentage points).

### Failure Behaviour
- If no trades: `0.0`.

---

## Profit Factor
### Definition
Gross profit divided by gross loss. Returns `0.0` when there are no losing trades.

### Formula
```text
gross_profit = sum(pnl where pnl > 0)
gross_loss   = abs(sum(pnl where pnl < 0))
profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0.0
```

### Validation
Tolerance: ±0.02

---

## Risk/Reward Ratio
### Definition
Average winner divided by absolute average loser. Returns `0.0` if there are no losing trades.

### Formula
```text
avg_win  = mean(pnl where pnl > 0)
avg_loss = mean(pnl where pnl < 0)  # negative
risk_reward_ratio = avg_win / abs(avg_loss) if avg_loss != 0 else 0.0
```

### Validation
Tolerance: ±0.02

### Failure Behaviour
- No losers: returns 0.0.

---

## Expectancy
### Definition
Expected average GBP profit/loss per trade computed from win rate and average win/loss sizes.

### Formula
```text
loss_rate = 100 - win_rate
expectancy = (win_rate/100 × avg_win) + (loss_rate/100 × avg_loss)
```

### Validation
Tolerance: ±0.10 (GBP).

---

# Tier 3 Metrics

## Recovery Factor
### Definition
Period net profit divided by maximum drawdown amount (currency). Returns `0.0` if the period is unprofitable or drawdown is zero.

### Formula
```text
period_profit = last_total_value - first_total_value
recovery_factor = period_profit / max_drawdown_amount if period_profit > 0 and max_drawdown_amount > 0 else 0.0
```

### Validation
Tolerance: ±0.05

---

## Capital Efficiency
### Definition
Percent return generated per unit of average deployed capital **in GBP** over the measurement window.

### Canonical Formula (SPEC — GBP-SAFE)
This metric MUST use a GBP-denominated cost basis to avoid currency mixing across markets.

```text
total_pnl_gbp = Sum(trade.pnl)  # trade_history.pnl is GBP
avg_position_value_gbp = Mean(trade.total_cost)  # trade_history.total_cost is GBP

capital_efficiency = (total_pnl_gbp / avg_position_value_gbp) × 100
if avg_position_value_gbp == 0: capital_efficiency = 0.0
```

### Data Requirements
Closed trades from `trade_history` with:
- `pnl` (GBP)
- `total_cost` (GBP)

### Response Format
Returned under `advanced_metrics`:
```json
{ "capital_efficiency": 0.17 }
```

### Validation
Tolerance: ±0.05

### Failure Behaviour
- No trades → 0.0
- avg_position_value_gbp == 0 → 0.0

### Implementation Conformance
**Known non-conformance (current implementation):** Some implementations compute `avg_position_value` as `entry_price × shares` (native currency), which mixes USD and GBP in multi-market portfolios. This is **non-conformant** with the canonical spec and is tracked as a backlog item (see Appendix E).

---

## Trade Frequency
### Definition
Trades per week computed from the span between the first trade entry and the last trade exit in the period.

### Formula
```text
if trade_count < 2: 0.0
else:
  day_span = (last_exit_date - first_entry_date).days
  trade_frequency = (trade_count / day_span) × 7 if day_span > 0 else 0.0
```

### Validation
Tolerance: ±0.2

---

## Win Streak / Loss Streak
### Definition
Maximum consecutive winning trades and maximum consecutive losing trades, ordered by `exit_date` ascending. The current implementation treats `pnl <= 0` as a loss for streak counting.

### Validation
Exact match.

---

## Average Holding Period (Winners vs Losers)
### Definition
Average `holding_days` for winners (`pnl > 0`) and losers (`pnl < 0`), rounded to 1 decimal place.

### Data Note (Holding Days)
Implementations MUST treat stored `holding_days` as authoritative for holding-period metrics.

### Validation
±0.5 days for each average.

---

## Consistency Metrics
### Definition
Object containing four fields derived from `monthly_data` (last 12 months in the filtered dataset).

### Fields
- `consecutive_profitable_months`: longest run of months with `pnl > 0`.
- `current_streak`: current run ending at the most recent month with `pnl > 0`.
- `win_rate_std_dev`: population std dev of monthly win_rate, rounded to 2 dp.
- `pnl_std_dev`: population std dev of monthly pnl, rounded to 2 dp.

### Failure Behaviour
If `monthly_data` is empty, return zeros for all fields.

---

## Appendix A: Data Lineage (Referential)

This Metrics Definitions document is the canonical source for **metric semantics and formulas**.

Canonical data lineage and field mapping live in:
- `data_model.md` (database schema, GBP vs native currency rules, API field mappings)
- `analytics_endpoints.md` (endpoint schema, response object shapes, and data sourcing rules)

Any future lineage changes MUST be made in those documents and referenced here.

---

## Appendix B — API Schema Coverage (Quick Audit Checklist)
The `GET /analytics/metrics` response contains the following top-level fields and MUST remain in sync with this spec:
- `summary`, `executive_metrics`, `advanced_metrics`, `market_comparison`, `exit_reasons`, `monthly_data`, `day_of_week`, `holding_periods`, `top_performers`, `consistency_metrics`, `trades_for_charts`.

---

## Appendix C — Validation Alignment (Source of Truth)
Validation is performed by `POST /validate/calculations` comparing computed metrics to `test_data/validation_data.py` expected values and tolerances.

### Metrics validated (current)
- `sharpe_ratio` (±0.01)
- `max_drawdown_percent` (±0.1)
- `recovery_factor` (±0.05)
- `expectancy` (±0.10)
- `profit_factor` (±0.02)
- `risk_reward_ratio` (±0.02)
- `win_rate` (±0.5)
- `win_streak` (exact)
- `loss_streak` (exact)
- `avg_hold_winners` (±0.5)
- `avg_hold_losers` (±0.5)
- `trade_frequency` (±0.2)
- `capital_efficiency` (±0.05)
- `days_underwater` (exact)

---

## Appendix D — Change Log
| Date | Version | Change | Author |
|---|---|---|---|
| 2026-02-16 | 1.5.0 | Initial comprehensive spec | Analytics Team |
| 2026-02-17 | 1.5.1 | FIX-MD-01: Add missing system metrics | Analytics Team |
| 2026-02-17 | 1.5.2 | FIX-MD-02: Add Risk/Reward Ratio and Expectancy | Analytics Team |
| 2026-02-17 | 1.5.3 | FIX-MD-03: Align Days Underwater to trade-sequence method | Analytics Team |
| 2026-02-17 | 1.5.5 | FIX-MD-04 backlog + FIX-MD-05: Specify Sharpe sample variance (canonical) and capital efficiency GBP-safe cost basis | Analytics Team |
| 2026-02-17 | 1.5.6 | ADVISORY-MD-D: Remove drift-prone lineage appendix; reference `data_model.md` and `analytics_endpoints.md` as lineage sources | Analytics Team |

---

## Appendix E — Known Deviations & Backlog Items
### Backlog Item 1 — Sharpe variance method
**Issue:** Current implementation uses population variance (÷ n) for Sharpe volatility.

**Canonical requirement:** Sample variance (÷ n−1).

**Action:** Update `_calculate_sharpe()` to compute variance using (n−1) for both portfolio and trade methods; update any future non-zero Sharpe validation expected values.

### Backlog Item 2 — Capital Efficiency currency basis
**Issue:** Some implementations compute average position value as `entry_price × shares` (native currency), mixing USD and GBP.

**Canonical requirement:** Use `trade_history.total_cost` (GBP) as the cost basis.

**Action:** Update capital efficiency calculation to use `Mean(total_cost)` in GBP; ensure `GET /analytics/metrics` continues to return the same field name (`capital_efficiency`) and update expected values if required.
