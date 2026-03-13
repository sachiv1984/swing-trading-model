# Metrics Definitions – Canonical Specification
**Version:** 1.7.0
**Owner:** Analytics Team
**Last Updated:** 2026-03-11
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

**Implementation conformance:** Sample variance (÷ n−1) is implemented in `_calculate_sharpe()` for both portfolio and trade methods as of BLG-TECH-01 (2026-02-20). See Appendix E, Backlog Item 1 — resolved.

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

## Current Drawdown
### Definition

`current_drawdown_percent` is the percentage decline of the current portfolio value from the all-time peak portfolio value recorded in `portfolio_history`. It is a **live, point-in-time metric** --- distinct from Max Drawdown, which records the largest historical peak-to-trough decline.

Current Drawdown is zero when the portfolio is at an all-time high. It is negative when the portfolio is below its peak.

### Canonical Formula

text

```
peak_portfolio_value = MAX(portfolio_history.total_value)

current_drawdown_percent =
  (current_portfolio_value - peak_portfolio_value) / peak_portfolio_value × 100
```

Result is ≤ 0.0. Zero means the portfolio is at peak.

### Data Requirements

-   `portfolio_history` table with ≥1 snapshot (for `peak_portfolio_value`)
-   Current `total_value` from the live portfolio state

### Data Sources (API)

This metric is **served via `GET /portfolio`**, not `GET /analytics/metrics`. Two new response fields are added to the `GET /portfolio` data object:

| Field | Type | Description |
| --- | --- | --- |
| `current_drawdown_percent` | float (≤ 0.0) | Current drawdown as a percentage. Negative or zero. |
| `peak_portfolio_value` | float (GBP) | All-time peak total portfolio value from `portfolio_history`. |

Both fields are always present in the response. Default to `0.0` when no `portfolio_history` exists.

### Related Fields (from GET /analytics/metrics)

The Current Drawdown widget also reads from `GET /analytics/metrics`:

| Field | Path | Used for |
| --- | --- | --- |
| `days_underwater` | `advanced_metrics.days_underwater` | Days since equity peak (trade-sequence method --- see Days Underwater section) |
| `max_drawdown.percent` | `advanced_metrics.max_drawdown.percent` | Historical maximum drawdown --- used to contextualise current drawdown as a proportion of worst-ever |

### Failure Behaviour

-   No `portfolio_history` snapshots: `current_drawdown_percent = 0.0`, `peak_portfolio_value = 0.0`
-   `peak_portfolio_value = 0`: widget renders "Establishing Peak" empty state; no percentage displayed.

### Validation

Not included in `POST /validate/calculations` --- this is a live point-in-time metric derived from current portfolio state, not a historical analytics metric.

### Implementation Note

The `peak_portfolio_value` field in `GET /portfolio` represents the all-time high across **all** `portfolio_history` snapshots regardless of the period filter. It is not period-scoped. This is consistent with the purpose of the widget (showing risk relative to the user's personal all-time best, not a windowed subset).

The progress bar in the Current Drawdown widget displays current drawdown as a proportion of `max_drawdown.percent` from `GET /analytics/metrics`. Colour thresholds (green ≤5%, amber ≤10%, orange ≤20%, red >20%) are a UX convention owned by Engineering --- they are not canonical business rules and are not defined in this document.

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
A portfolio-snapshot definition of "days underwater" exists in earlier drafts, but the live API field `advanced_metrics.days_underwater` is trade-sequence based.

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
{ "capital_efficiency": 0.22 }
```

### Validation
Tolerance: ±0.05

### Failure Behaviour
- No trades → 0.0
- avg_position_value_gbp == 0 → 0.0

### Implementation Conformance
**Conformant as of BLG-TECH-01 (2026-02-20).** `_calculate_advanced_metrics()` uses `Mean(trade.total_cost)` (GBP) as the cost basis. The previous non-conformant implementation (`entry_price × shares`, which mixed USD and GBP in multi-market portfolios) has been corrected. See Appendix E, Backlog Item 2 — resolved.

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

---

# Portfolio Risk Metrics

## Position Risk

### Definition
The GBP-denominated risk capital exposed by a single open position — the maximum loss if the stop price is hit from the current entry. This is the canonical "R" unit for portfolio heat calculation.

### Canonical Formula (TASK-06 — v1.7)

```text
# For GBP-denominated positions (UK market):
Position_Risk_GBP = (entry_price_gbp − stop_price_gbp) × shares

# For non-GBP positions (US market, priced in USD):
Position_Risk_GBP = (entry_price_usd − stop_price_usd) × shares ÷ fx_rate_gbp_usd

# General form:
Position_Risk_GBP = (entry_price_native − stop_price_native) × shares × fx_adjustment

where:
  fx_adjustment = 1.0            for GBP positions (UK market)
  fx_adjustment = 1 / fx_rate   for USD positions (US market)
  fx_rate = GBP/USD rate at time of position entry (stored as position.fx_rate)
```

**Important constraints:**
- `entry_price` and `stop_price` must be in the same native currency before applying fx_adjustment.
- UK prices stored in pence must be converted to pounds before applying the formula: `price_gbp = price_pence / 100`.
- Position Risk is always ≥ 0. If stop_price ≥ entry_price (e.g. lock-in stop above entry), Position Risk = 0.
- Position Risk is a point-in-time metric: it uses the entry stop, not a trailing stop.

### Data Sources
- `positions.entry_price` — native currency
- `positions.stop_price` — native currency
- `positions.shares`
- `positions.fx_rate` — GBP/USD rate at entry (1.0 for GBP positions)
- `positions.market` — `"UK"` or `"US"` (determines fx_adjustment)

---

## Portfolio Heat

### Definition
The aggregate stop-loss risk exposure of all open positions, expressed as a percentage of total portfolio value. Answers: "If every open position hits its stop simultaneously, what percentage of the portfolio is lost?"

### Canonical Formula (TASK-07 — v1.7)

```text
Portfolio_Heat_Percent = (Sum of Position_Risk_GBP for all open positions) / Portfolio_Value_GBP × 100

where:
  Portfolio_Value_GBP = portfolio.total_value (GBP, from GET /portfolio)
  Position_Risk_GBP   = canonical Position Risk formula above, for each open position
```

**Important constraints:**
- Portfolio Heat uses **open positions only** — closed trades are excluded.
- Portfolio Value is the live total portfolio value (cash + open position market values), not invested capital only.
- If Portfolio_Value_GBP = 0, return 0.0.
- Portfolio Heat is a live, point-in-time metric — it is not stored in `portfolio_history` and is not period-filterable.

### Response Format
Served via `GET /portfolio` as an additional field in the `data` object:
```json
{
  "portfolio_heat_percent": 12.4,
  "position_risks": [
    { "ticker": "AAPL", "position_risk_gbp": 85.20 },
    { "ticker": "FRES.L", "position_risk_gbp": 42.00 }
  ]
}
```

---

## Portfolio Heat Display Thresholds (TASK-08 — v1.7)

These are canonical business thresholds, not UX conventions. All implementations (backend, frontend, reporting) **MUST** use these exact bands.

| Band | Range | Colour | Meaning |
|------|-------|--------|---------|
| Low | 0% ≤ heat < 10% | Green (`#22c55e`) | Portfolio is within safe risk parameters |
| Moderate | 10% ≤ heat < 20% | Amber (`#f59e0b`) | Risk is elevated; monitor positions |
| High | 20% ≤ heat < 30% | Orange (`#f97316`) | Risk is high; consider reducing exposure |
| Extreme | heat ≥ 30% | Red (`#ef4444`) | Critically over-exposed; immediate review required |

**Threshold rationale:**
- A 10% maximum portfolio heat target is the canonical risk management rule for this strategy (per `claude/strategy/strategy_rules.md` §5).
- The 10% boundary therefore defines the green/amber transition.
- Each subsequent 10-point band represents a proportional escalation of risk severity.
- Colour codes are canonical hex values; frontend must not substitute alternatives without a spec update.

### Validation
Portfolio Heat is a live metric and is **not** included in `POST /validate/calculations`. Threshold correctness is verified by frontend integration tests only.

---

---

# Discipline & Compliance Metrics

Served via `GET /analytics/compliance-metrics`. These metrics measure adherence to the trading plan's journalling and risk management rules. No period filter — computed across all closed trades. The response includes `trade_count` (the denominator) so the frontend can render "last N trades" sub-labels.

## Journal Completion Rate

### Definition
Percentage of closed trades where the trader recorded at least one journal note (entry note or exit note).

### Canonical Formula

```text
trades_with_notes = count(trades where entry_note IS NOT NULL AND entry_note != ''
                           OR exit_note IS NOT NULL AND exit_note != '')
journal_completion_rate = (trades_with_notes / total_trades) × 100
if total_trades = 0: return 0.0
```

### Data Sources
- `trade_history.entry_note` (TEXT, nullable)
- `trade_history.exit_note` (TEXT, nullable)

### Response Format
Returned in `GET /analytics/compliance-metrics` data object:
```json
{ "journal_completion_rate": 72.5, "trade_count": 40 }
```

### Failure Behaviour
- No trades: `journal_completion_rate = 0.0`, `trade_count = 0`.

---

## Stop-Based Exit Rate

### Definition
Percentage of closed trades where the exit was triggered by a stop-loss or trailing-stop mechanism (i.e., the trader did not exit manually).

### Canonical Formula

```text
stop_exits = count(trades where exit_reason IN ('Stop Loss Hit', 'Trailing Stop'))
stop_exit_rate = (stop_exits / total_trades) × 100
if total_trades = 0: return 0.0
```

### Data Sources
- `trade_history.exit_reason` — canonical values per data_model.md §3 Exit Reason Values.

### Response Format
```json
{ "stop_exit_rate": 55.0, "trade_count": 40 }
```

### Failure Behaviour
- No trades: `stop_exit_rate = 0.0`.
- Null `exit_reason` values are treated as non-stop exits (they map to `"Manual Exit"`).

---

## Average Position Size (% of Portfolio)

### Definition
Average size of a closed trade as a percentage of the portfolio value at the time of trade entry. Answers: "On average, how large a fraction of the portfolio did each trade represent at entry?"

### Canonical Formula

```text
For each closed trade t:
  portfolio_value_at_entry(t) = total_value from portfolio_history
                                 where snapshot_date <= t.entry_date
                                 ORDER BY snapshot_date DESC LIMIT 1

  position_size_pct(t) = (t.total_cost / portfolio_value_at_entry(t)) × 100

avg_position_size_pct = mean(position_size_pct(t))
                        computed only over trades where portfolio_value_at_entry(t) > 0
```

### Data Sources
- `trade_history.total_cost` — GBP entry cost
- `trade_history.entry_date`
- `portfolio_history.total_value`, `portfolio_history.snapshot_date`

### Response Format
```json
{ "avg_position_size_pct": 4.82, "trade_count": 40 }
```

### Failure Behaviour
- No trades: `avg_position_size_pct = 0.0`.
- No portfolio snapshots (or no snapshot on or before any trade entry): `avg_position_size_pct = 0.0`.
- Trades with no matching snapshot are excluded from the average; if all trades are excluded, returns `0.0`.

---

# Cohort Analysis Metrics

Served via `GET /analytics/cohort?period={month|quarter|year}`. Groups closed trades by entry period and returns aggregate performance per cohort.

## Cohort Metric Definitions

### Period Grouping

```text
period = "month":   group by date_trunc('month', entry_date)
                    label format: "MMM YYYY"  (e.g. "Mar 2026")

period = "quarter": group by date_trunc('quarter', entry_date)
                    label format: "QN YYYY"   (e.g. "Q1 2026")

period = "year":    group by date_trunc('year', entry_date)
                    label format: "YYYY"      (e.g. "2026")
```

### Per-Cohort Fields

| Field | Formula |
|-------|---------|
| `period_label` | Formatted period string (see above) |
| `trade_count` | `count(*)` for trades in that period |
| `win_rate` | `count(pnl > 0) / trade_count × 100`, rounded to 1dp |
| `avg_r_multiple` | Mean R-multiple for trades with a valid stop price (see R-Multiple formula below); `null` if no stop-price data available |
| `total_pnl` | `sum(pnl)` GBP, rounded to 2dp |

### Minimum Data Threshold
If fewer than 3 periods are available, the endpoint returns `{ "has_enough_data": false, "cohorts": [] }`.

### Ordering
Rows ordered descending by period (most recent first).

---

# R-Multiple Distribution (Backend)

Served via `GET /analytics/r-multiple-distribution`. Computes server-side R-multiple for each closed trade (using the canonical formula below), then buckets the distribution.

## Canonical R-Multiple Formula (Backend)

```text
R(t) = (exit_price(t) - entry_price(t)) / (entry_price(t) - stop_price(t))

where:
  stop_price(t) = positions.initial_stop for the originating position
                  (joined via trade_history.position_id → positions.id)
  entry_price(t) = trade_history.entry_price (native currency)
  exit_price(t)  = trade_history.exit_price  (native currency)

Constraint: if stop_price IS NULL OR stop_price >= entry_price: trade excluded from distribution.
Constraint: prices must be in the same native currency before applying the formula.
```

**Note:** This is the same formula as the Tier 1 R-Multiple (Visualisation-Only) entry above. This section provides the backend-canonical definition for server-side computation and validation.

## Distribution Buckets

Eight fixed buckets:

| Bucket label | Range |
|---|---|
| `< -3R` | R < -3.0 |
| `-3R to -2R` | -3.0 ≤ R < -2.0 |
| `-2R to -1R` | -2.0 ≤ R < -1.0 |
| `-1R to 0R` | -1.0 ≤ R < 0.0 |
| `0R to 1R` | 0.0 ≤ R < 1.0 |
| `1R to 2R` | 1.0 ≤ R < 2.0 |
| `2R to 3R` | 2.0 ≤ R < 3.0 |
| `> 3R` | R ≥ 3.0 |

## Summary Statistics

| Field | Formula |
|-------|---------|
| `median_r` | Median R across all trades with valid R, rounded to 2dp |
| `pct_above_1r` | `count(R ≥ 1.0) / count(valid R trades) × 100`, rounded to 1dp |
| `avg_winner_r` | Mean R for trades with R > 0, rounded to 2dp; `null` if none |
| `avg_loser_r` | Mean R for trades with R < 0, rounded to 2dp; `null` if none |

## Response Format

```json
{
  "status": "ok",
  "data": {
    "has_enough_data": true,
    "trade_count": 28,
    "buckets": [
      { "label": "< -3R",     "count": 1 },
      { "label": "-3R to -2R","count": 2 },
      { "label": "-2R to -1R","count": 4 },
      { "label": "-1R to 0R", "count": 6 },
      { "label": "0R to 1R",  "count": 5 },
      { "label": "1R to 2R",  "count": 7 },
      { "label": "2R to 3R",  "count": 2 },
      { "label": "> 3R",      "count": 1 }
    ],
    "median_r": 0.72,
    "pct_above_1r": 35.7,
    "avg_winner_r": 1.54,
    "avg_loser_r": -0.91
  }
}
```

## Minimum Data Threshold
Requires ≥ 5 trades with a valid stop price. Below threshold: `has_enough_data: false`, `buckets: []`, summary stats `null`.

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

Additional endpoints introduced in v1.7.0:
- `GET /analytics/compliance-metrics` — `journal_completion_rate`, `stop_exit_rate`, `avg_position_size_pct`, `trade_count`
- `GET /analytics/cohort?period={month|quarter|year}` — `has_enough_data`, `cohorts[]` (period_label, trade_count, win_rate, avg_r_multiple, total_pnl)
- `GET /analytics/r-multiple-distribution` — `has_enough_data`, `trade_count`, `buckets[]`, `median_r`, `pct_above_1r`, `avg_winner_r`, `avg_loser_r`

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
| 2026-02-21 | 1.5.7 | BLG-TECH-01 resolution: mark Appendix E Backlog Items 1 and 2 as resolved. Update inline conformance notes in Sharpe Ratio and Capital Efficiency sections. Update Capital Efficiency response format example value to 0.22. Validation confirmed 13/13 pass at 2026-02-21T00:24:41Z. Canonical Owner sign-off granted. | Metrics Definitions & Analytics Canonical Owner |
| 2026-02-25 | 1.5.8 | BLG-FEAT-01: Add Current Drawdown section. Defines current_drawdown_percent formula, data sources (GET /portfolio new fields), relationship to days_underwater and max_drawdown metrics, failure behaviour, and implementation notes. QWB pre-alignment D1. | Metrics Definitions owner |
| 2026-03-02 | 1.6.0 | EPIC-03 (v1.7): Add Portfolio Risk Metrics section — canonical Position Risk formula (GBP-adjusted, FX handling for US positions, pence conversion for UK), Portfolio Heat formula (sum of position risks / portfolio value × 100), and explicit display threshold bands (Low <10%, Moderate 10–20%, High 20–30%, Extreme ≥30%) with canonical hex colour codes. TASK-06 through TASK-10 complete. Head of Specs Team lifecycle sign-off granted 2026-03-02 (Delegated Authority). v1.8 pre-alignment gate cleared. | Metrics Definitions & Analytics Owner + Head of Specs Team |
| 2026-03-11 | 1.7.0 | EPIC-01/02 (v1.9): Add Discipline & Compliance Metrics section (ST-01) — Journal Completion Rate, Stop-Based Exit Rate, Average Position Size % formulas for GET /analytics/compliance-metrics. Add Cohort Analysis Metrics section (ST-03 batch) — period grouping, per-cohort field definitions, minimum data threshold. Add R-Multiple Distribution (Backend) section (ST-04 batch) — canonical server-side R-multiple formula, 8 fixed buckets, summary statistics. Appendix B updated to list all three new endpoints. Metrics Definitions & Analytics Owner + Head of Engineering sign-off granted 2026-03-11 (EPIC-01 ST-01 delivery). | Metrics Definitions & Analytics Owner + Head of Engineering |

---

## Appendix E — Known Deviations & Backlog Items

### Backlog Item 1 — Sharpe variance method
**Status: ✅ RESOLVED — 2026-02-21 (BLG-TECH-01)**

**Issue:** Implementation used population variance (÷ n) for Sharpe volatility.

**Canonical requirement:** Sample variance (÷ n−1).

**Resolution:** `_calculate_sharpe()` updated to use sample variance (÷ n−1) for both portfolio and trade methods (commit ref: AP-06, 2026-02-20). Validation confirmed: `POST /validate/calculations` 13/13 pass at 2026-02-21T00:24:41Z. Canonical Owner sign-off granted 2026-02-21.

---

### Backlog Item 2 — Capital Efficiency currency basis
**Status: ✅ RESOLVED — 2026-02-21 (BLG-TECH-01)**

**Issue:** Implementation computed average position value as `entry_price × shares` (native currency), mixing USD and GBP in multi-market portfolios.

**Canonical requirement:** Use `trade_history.total_cost` (GBP) as the cost basis.

**Resolution:** `_calculate_advanced_metrics()` updated to use `Mean(trade.total_cost)` (GBP) as cost basis (commit ref: AP-07, 2026-02-20). `validation_data.py` expected value updated from 0.17 → 0.22 to reflect corrected basis. `capital_efficiency` validation block added to `routers/validation.py` (was previously absent). Validation confirmed: `POST /validate/calculations` 13/13 pass at 2026-02-21T00:24:41Z. Canonical Owner sign-off granted 2026-02-21.
