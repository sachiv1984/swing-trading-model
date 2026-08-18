# Metrics Definitions – Canonical Specification
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 1.17.0
**Last Updated:** 2026-08-17
**Review Cycle:** Monthly
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

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

## R-Multiple (Canonical Server-Side)
### Definition
The canonical R-multiple computation performed server-side using stored position initial stop prices. This is the authoritative R-multiple for distribution reporting and analytics. The `GET /analytics/r-multiple-distribution` endpoint uses this formula.

### Canonical Formula
```text
R = (exit_price - entry_price) / (entry_price - initial_stop_price)
```

Where:
- `exit_price` — the price at which the trade was closed (from `trade_history.exit_price`)
- `entry_price` — the price at which the position was entered (from `trade_history.entry_price`)
- `initial_stop_price` — the initial stop loss set at position entry (from `positions.initial_stop`)

### Qualifying Conditions
A trade qualifies for server-side R-multiple computation only if:
1. `initial_stop_price` is non-null (positions.initial_stop is populated)
2. `entry_price > initial_stop_price` (denominator > 0; short-side and lock-in stops above entry are excluded)
3. `exit_price` is non-null

Trades that do not qualify are excluded from distribution calculations; they do not contribute to bucket counts or summary statistics.

### Sign Convention
- Positive R: trade exited above entry price (profit)
- Negative R: trade exited below entry price (loss)
- Zero: trade exited at exactly entry price (break-even)

### Data Sources
- `trade_history.entry_price` — native currency
- `trade_history.exit_price` — native currency
- `positions.initial_stop` — native currency (joined via `trade_history.position_id → positions.id`)

### Response Format
Served via `GET /analytics/r-multiple-distribution`:
```json
{
  "has_enough_data": true,
  "total_qualifying_trades": 12,
  "buckets": [
    {"range": "< -2R", "count": 1},
    {"range": "-2R to -1R", "count": 2},
    {"range": "-1R to 0R", "count": 3},
    {"range": "0R to 1R", "count": 4},
    {"range": "1R to 2R", "count": 1},
    {"range": "2R to 3R", "count": 1},
    {"> 3R", "count": 0}
  ],
  "median_r": 0.3,
  "pct_above_1r": 16.7,
  "avg_winner_r": 1.4,
  "avg_loser_r": -0.8
}
```

### Minimum Data Requirement
5 qualifying trades required. Below threshold: `has_enough_data: false`.

### Failure Behaviour
- No positions.initial_stop data (migration not run): all trades non-qualifying; returns `has_enough_data: false`.
- Fewer than 5 qualifying trades: `has_enough_data: false`.

### Cross-Currency Normalization (BLG-SPEC-59)

**Applies to:** the canonical server-side R-multiple formula above and every metric derived from it (median R, `pct_above_1r`, `avg_winner_r`, `avg_loser_r`, cohort average R).

**Finding: no FX conversion is required.** Unlike absolute GBP-denominated metrics (Position Risk §below, Capital Efficiency §below) which explicitly apply `fx_adjustment` to avoid mixing USD and GBP currency units, R-multiple is **dimensionless by construction** — it is a ratio of two differences expressed in the same native currency:

```text
R = (exit_price − entry_price) / (entry_price − initial_stop_price)
```

`exit_price`, `entry_price`, and `initial_stop_price` are always the same native currency for a given trade (all three columns are populated from the same position — a UK position's three prices are all GBP; a US position's three prices are all USD). The currency unit cancels algebraically in both numerator and denominator, so the resulting `R` value carries no currency dimension.

**Consequence for aggregation:** because per-trade R values are already currency-neutral, aggregating R across a mixed portfolio of US and UK trades (mean, median, bucket counts, cohort averages) requires **no FX conversion at any step**. This differs from GBP-safety metrics like Capital Efficiency §below, where `pnl` and `total_cost` are absolute monetary values that must be normalised to a single currency (GBP) before summing or averaging — R-multiple has no equivalent risk, because it is never summed or averaged as a currency amount.

**Explicit non-requirement:** implementations must **not** apply `position.fx_rate` or any `fx_adjustment` factor to R-multiple inputs or outputs. Doing so would incorrectly treat a dimensionless ratio as a currency amount and silently corrupt the result (e.g. multiplying a US trade's R by `1/fx_rate` would scale it relative to GBP trades, breaking the ratio's currency-neutral property that makes cross-market R comparison valid in the first place).

**Validation:** a regression fixture should include at least one qualifying USD trade and one qualifying GBP trade with deliberately different `fx_rate` values and confirm `avg_winner_r`/`avg_loser_r`/`median_r` are unaffected by the FX rate difference (i.e. R depends only on each trade's own three native-currency prices, never on `fx_rate`).

### Sign-off

- **Metrics Definitions & Analytics Owner:** agent-mediated sign-off cleared 2026-07-09 (ST-08, EPIC-03, v6.8)

---

## Cohort Metrics
### Definition
Per-cohort aggregated trading performance, grouping closed trades by their entry period. Cohort period granularity: month, quarter, or year.

### Canonical Formulas
```text
# Trade count per cohort
cohort_trade_count = count(trades where entry_date falls in cohort period)

# Win rate per cohort (same formula as overall win rate)
cohort_win_rate = (count(pnl > 0) / cohort_trade_count) × 100

# Total net P&L per cohort
cohort_total_pnl = sum(trade.pnl) for trades in cohort  # GBP

# Average R-multiple per cohort (server-side canonical formula, qualifying trades only)
cohort_avg_r_multiple = mean(R) for qualifying trades in cohort
  where R = (exit_price - entry_price) / (entry_price - initial_stop_price)
  and entry_price > initial_stop_price
  Returns null if no qualifying trades in cohort.
```

### Period Definitions
| Granularity | Grouping Key | Period Label Format |
|-------------|-------------|---------------------|
| `month` | `entry_date` truncated to YYYY-MM | "Mar 2026" |
| `quarter` | `entry_date` year + quarter number | "Q1 2026" |
| `year` | `entry_date` year | "2026" |

Rows sorted descending by period key (most recent first).

### Insufficient History
Fewer than 3 distinct cohort periods available: `has_enough_data: false`. Frontend shows: "Not enough closed trades to show [period] cohorts".

### Response Format
Served via `GET /analytics/cohort?period={month|quarter|year}`:
```json
{
  "period": "month",
  "has_enough_data": true,
  "cohorts": [
    {
      "period_label": "Mar 2026",
      "trade_count": 5,
      "win_rate": 60.0,
      "avg_r_multiple": 0.8,
      "total_pnl": 320.50
    }
  ]
}
```

### Data Sources
- `trade_history.entry_date` — for cohort period grouping
- `trade_history.pnl` — GBP
- `trade_history.entry_price`, `trade_history.exit_price` — for R-multiple
- `positions.initial_stop` — joined via `trade_history.position_id`

### Failure Behaviour
- No closed trades: empty `cohorts` array, `has_enough_data: false`.
- No `initial_stop` data: `avg_r_multiple: null` for all cohorts; other metrics unaffected.

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
Maximum consecutive winning trades and maximum consecutive losing trades, ordered by `exit_date` ascending.

**Consecutive Losing Streak (`loss_streak`):** The maximum number of consecutive closed trades with `pnl <= 0` in the filtered dataset, ordered by `exit_date` ascending. Historical closed trades only — open positions are excluded. A zero-pnl trade (`pnl == 0`) counts as a loss for streak counting purposes.

**Consecutive Winning Streak (`win_streak`):** The maximum number of consecutive closed trades with `pnl > 0` in the filtered dataset.

### Formula
```text
win_streak = loss_streak = cur_w = cur_l = 0
for each trade t (ordered exit_date ASC):
    if t.pnl > 0: cur_w += 1; cur_l = 0
    else:         cur_l += 1; cur_w = 0
    win_streak  = max(win_streak,  cur_w)
    loss_streak = max(loss_streak, cur_l)
```

### Response location
`advanced_metrics.loss_streak` and `advanced_metrics.win_streak` in `GET /analytics/metrics` response.

### Display
Displayed in the analytics dashboard alongside expectancy and win rate.

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

## Fee Drag

**Added:** v1.9.0 — ST-09 (EPIC-03, v2.5)

Fee drag measures the proportion of gross sale proceeds consumed by broker exit fees. It is a per-trade cost metric and portfolio aggregate.

### Canonical Formula

```
fee_drag_pct = exit_fees / gross_proceeds × 100
```

Where:
- `exit_fees` — total broker exit fees in GBP (commission + platform charges at exit, as recorded in `trade_history.exit_fees`)
- `gross_proceeds` — gross sale proceeds in GBP before exit fees (`trade_history.gross_proceeds`)

**Qualifying condition:** `gross_proceeds > 0`. If `gross_proceeds` is null or zero, `fee_drag_pct` is `null` for that trade.

**Sign convention:** Always non-negative. Fee drag is always a cost; green/red colour treatment is not applicable. Amber/neutral tone is used in the UI.

**Precision:** Rounded to 2 decimal places.

### Portfolio Average

```
avg_fee_drag_pct = mean(fee_drag_pct) across all trades where fee_drag_pct is not null
```

Computed server-side as a simple arithmetic mean. Returned as `avg_fee_drag_pct` in the `GET /trades` response envelope. `null` when no qualifying trades exist.

### Data Source

| Field | Source |
|-------|--------|
| `fee_drag_pct` (per trade) | `GET /trades` → `trades[].fee_drag_pct` |
| `avg_fee_drag_pct` | `GET /trades` → top-level `avg_fee_drag_pct` |

Computed in `backend/services/trade_service.py` from `trade_history.exit_fees` and `trade_history.gross_proceeds`. No schema change required — these columns already exist.

### Display

- **Trade History table:** "Fee Drag %" column (after Slippage column). Format: `+X.XX%`. Amber colour. Sortable ascending/descending.
- **Trade History summary bar:** "Avg Fee Drag" StatsCard. Format: `+X.XX%`. Amber gradient. Always rendered (no null state once trades exist).

### Relationship to Other Metrics

Fee drag is distinct from slippage:
- **Slippage** = entry-side execution cost (fill price vs limit price)
- **Fee drag** = exit-side cost (fees as a proportion of sale proceeds)

Both are logged per trade. Neither is included in P&L calculations — they are analytical overlays only.

---

## Thesis Adoption Rate

**Added:** v1.12.0 — ST-08 (EPIC-03, v6.5, BLG-FEAT-41)

Thesis adoption rate measures whether Claude-generated trade theses (`POST /trade-plans/{plan_id}/generate-thesis`, shipped v4.0) are actually kept and used at entry, versus discarded. It is an early signal of feature value and cost-per-use justification, complementing the ST-07 feedback mechanism (BLG-FE-46).

### Definition

```
thesis_adoption_rate = COUNT(trade_plans with non-empty setup_thesis, restricted to plans a thesis was generated for)
                        / COUNT(DISTINCT trade_plans a thesis was generated for)
```

- **Numerator:** trade plans where a thesis was generated AND `trade_plans.setup_thesis` is non-empty at entry (i.e. the user kept the generated thesis, whether unedited or lightly edited — see ST-07's feedback mechanism for finer-grained adoption signal).
- **Denominator:** distinct trade plans for which `POST /trade-plans/{plan_id}/generate-thesis` was called at least once.
- **Returns:** `null` if the denominator is 0 (no thesis generation calls recorded yet).

### Query Approach

**Join key correction (verified against `backend/database.py` at implementation time):** the sprint scope for this item names `claude_audit_log` as the join target, but `claude_audit_log` (see `backend/database.py` `ensure_claude_audit_log_table`) has no `plan_id` column — it cannot be joined to `trade_plans`. The table that actually carries the per-plan linkage is `gemini_audit_log` (`backend/database.py` `ensure_gemini_audit_log_table`), which has an indexed `plan_id UUID` column populated by `generate_setup_thesis()` (`backend/services/gemini_service.py`) on every `POST /trade-plans/{plan_id}/generate-thesis` call. This matches the AC's intent (join the AI thesis-generation audit trail to `trade_plans`) even though the literal table name differs — see implementation note below.

```sql
SELECT
  COUNT(*) FILTER (WHERE tp.setup_thesis IS NOT NULL AND tp.setup_thesis != '') AS adopted,
  COUNT(*) AS total_generated
FROM trade_plans tp
WHERE tp.id IN (
  SELECT DISTINCT plan_id
  FROM gemini_audit_log
  WHERE plan_id IS NOT NULL
);

-- thesis_adoption_rate = adopted::float / NULLIF(total_generated, 0)
```

**Why `plan_id IS NOT NULL` isolates thesis-generation calls:** `gemini_audit_log` is also written by `generate_full_plan()` (`POST /trade-plans/generate-plan`, called before a plan exists — no `plan_id` available, always `NULL`). Only `generate_setup_thesis()` (`POST /trade-plans/{plan_id}/generate-thesis`, requires an existing plan) passes a non-null `plan_id`. `gemini_audit_log` does not store the calling endpoint, so this `plan_id IS NOT NULL` filter is the only way to isolate thesis-generation rows from full-plan-generation rows in that table.

### Data Source

| Field | Source |
|-------|--------|
| `setup_thesis` | `trade_plans.setup_thesis` (existing column) |
| Thesis-generated flag | `gemini_audit_log.plan_id` (existing column, indexed `idx_gal_plan_id`) — no schema change required |

### Implementation Note

No new endpoint or schema change is required to compute this metric — both source columns already exist. This section documents the query approach only; no `GET` endpoint has been built for this metric as of v6.5 (ST-08 scope is metric definition, not endpoint delivery per `stage4_backlog_slice.md#ST-08`: "Design Not Applicable — no UI acceptance criterion").

**Caveat:** the query does not account for `trade_plans` rows deleted after thesis generation — a dangling `gemini_audit_log.plan_id` reference would silently drop from the denominator. Not a defect (no delete-cascade concern is evident today), but worth a one-line check if this metric is later exposed via an endpoint.

### Sign-off

- **Metrics Definitions & Analytics Owner:** agent-mediated sign-off cleared 2026-07-03 (ST-08, EPIC-03, v6.5)
- **Financial Reporting & Records Owner:** agent-mediated sign-off cleared 2026-07-03 (ST-08, EPIC-03, v6.5)
- **Product Owner:** pending — Product Owner sign-off is always a human decision (execution_prompt.md §5.3), not agent-mediated. See PR review comment for Product Owner acceptance of this story.

---

## Trailing Stop Action Rate

**Added:** v1.13.0 — ST-10 (EPIC-03, v6.8, BLG-SPEC-61)

Trailing stop action rate measures whether the system's ATR-based trail-stop recommendations (`GET /positions/{id}/stop-trail`) are actually applied by the user, versus shown and ignored. It is the ratio needed to evaluate the ROI of the v6.2 trailing-stop feature investment (BLG-FEAT-46), analogous in purpose to Thesis Adoption Rate (§above) for AI thesis generation.

**Scope clarification (important — two distinct trailing-stop mechanisms exist in this system):**

1. **Automatic nightly ratchet** (`run_nightly_trailing_stop_update()`, `backend/services/position_service.py:509`) — recomputes and writes `positions.current_stop` for every open position every night, fully automatically, with no user decision point. This is the value shown as "Trail Stop" in Table/Grid views (`positions.md` §Trailing Stop Column). It is **not** in scope for this metric — there is no "action" to measure because the system always applies it.
2. **Manual trail-stop recommendation** (`GET /positions/{id}/stop-trail`, `backend/main.py:1431`, surfaced via the "Trail Stop" button/modal for PROFITABLE/EXIT ZONE positions, `positions.md` §Trail Stop Action) — computes `atr_trail_stop = current_price − (ATR × 2.0)` and displays it as a recommendation (`recommendation: "Raise stop to {atr_trail_stop}"`, explicitly `§13 display-only`). The user then either applies it (clicking the modal's confirm button, which issues `PATCH /positions/{id}` with `stop_price: atr_trail_stop`) or dismisses the modal, leaving the stop unchanged. **This is the computed-vs-acted-upon decision point BLG-SPEC-61 is measuring.**

### Definition

```
trailing_stop_action_rate = COUNT(recommendations where the recommended stop was applied within the capture window)
                             / COUNT(recommendations generated)
```

- **Numerator:** trail-stop recommendations (`GET /positions/{id}/stop-trail` calls) for which a subsequent `PATCH /positions/{id}` set `stop_price` to (or above) the recommended `atr_trail_stop` value for the same position, within the capture window.
- **Denominator:** total trail-stop recommendations generated (`GET /positions/{id}/stop-trail` calls, one per modal open).
- **Returns:** `null` if the denominator is 0 (no recommendations generated yet).

### Data Capture Requirement (instrumented — ST-07, BLG-BE-50, v7.0)

Both sides of this ratio are now capturable. `trailing_stop_recommendation_log` is written on every `GET /positions/{id}/stop-trail` call (`backend/main.py`'s `get_stop_trail_endpoint`, fire-and-forget via `database.log_trailing_stop_recommendation()`), following the existing `pre_entry_validation_log` pattern (`backend/database.py`):

```sql
CREATE TABLE trailing_stop_recommendation_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    position_id UUID NOT NULL REFERENCES positions(id),
    current_stop_at_recommendation DECIMAL(10,4),
    recommended_stop DECIMAL(10,4) NOT NULL,
    recommended_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

The action-rate query joins each log row to the earliest `PATCH /positions/{id}` that set `stop_price >= recommended_stop` within the capture window — **24 hours from `recommended_at`, Product Owner-confirmed at v7.0 sprint planning (delegated authority, consistent with the `2026-07-10__release-v6.9` sign-off precedent)**. No separate PATCH-side capture table was needed: `positions.stop_price` (the current value) and `positions.updated_at` (set on every `update_position()` call) already provide the join target — `stop_price >= recommended_stop AND updated_at BETWEEN recommended_at AND recommended_at + INTERVAL '24 hours'`.

**Still open (not part of ST-07's scope — capture only):** no dedicated `GET /analytics/...` endpoint computes and returns `trailing_stop_action_rate` yet; the join above is documented and computable ad hoc against the two tables, but exposing it as a first-class metric endpoint is separate follow-up work.

### Tooling Assessment (AC-02)

**Note on this AC:** `stage4_backlog_slice.md#ST-10` AC-02 reads "Tooling assessment recorded on whether version tagging adds drift-detection value beyond existing `quality_gate.yml` OpenAPI validation" — wording that describes CI/OpenAPI-contract drift tooling (the subject of the unrelated ST-12/BLG-GOV-134 story in this same EPIC), not trailing-stop metrics. This appears to be a sealed-artefact copy/paste carry-over from sprint planning rather than a deliberate AC for this story; flagged here transparently per `execution_prompt.md` standard-mode ambiguity handling (proceed with an explicit assumption, do not silently guess or block the whole item). The backlog slice is sealed and cannot be corrected retroactively, so AC-02 is answered on its literal terms below rather than left unaddressed.

Applying the question as literally asked to this metric's documentation: `metrics_definitions.md` already uses manual version tagging (the `**Version:**` header plus the `## Document History` table). Assessed whether this adds drift-detection value beyond `quality_gate.yml`'s OpenAPI validation (which checks that `docs/reference/openapi.yaml` reflects `backend/routers/` endpoints — a mechanically detectable code-vs-contract signal): **not directly comparable, and no new automated tooling is recommended at this time.** Metric *formula* drift (backend calculation logic silently diverging from this document) has no code-side symbol as clean as a `@router.get` decorator to key an automated check off; the existing safeguard is the agent-mediated sign-off gate at write time (§5.3), which is a prevention control rather than a detection control like the OpenAPI gate. If metric-implementation drift incidents occur in production (analogous to the Capital Efficiency currency-basis defect resolved as Appendix E, Backlog Item 2), an automated drift check would become justified — noted as a future candidate, not actioned now.

### Validation Tolerances (ST-03, BLG-SPEC-85, v8.9)

The rate itself is bounded by construction (`0.0`–`1.0`, or `null` per the Returns rule above) — the tolerances below define when a reading should be trusted as statistically meaningful versus flagged for review, mirroring the explicit numeric bands used elsewhere in this document (e.g. Portfolio Heat's Low/Moderate/High/Extreme thresholds).

| Condition | Numeric bound | Interpretation |
|-----------|---------------|-----------------|
| Insufficient sample | Denominator (recommendations generated) `< 5` in the reporting window | Reading is not statistically meaningful — display as "insufficient data", do not treat as a genuine low/high rate |
| Expected range (sufficient sample) | `0.05 ≤ rate ≤ 0.95` with denominator `≥ 5` | Normal operating range — no action needed |
| Anomalously low | `rate < 0.05` with denominator `≥ 10` | Recommendations are being generated but essentially never applied — investigate UI friction on the confirm action or a possible mismatch between `recommended_stop` and what users are actually setting |
| Anomalously high | `rate > 0.95` with denominator `≥ 10` | Near-universal application — plausible if the confirm flow is low-friction, but also consistent with the join over-matching (e.g. capture window too wide, or unrelated PATCHes coincidentally clearing the `stop_price >= recommended_stop` condition); spot-check a sample of joined rows before trusting the reading |
| Stale capture | No new `trailing_stop_recommendation_log` row for `> 30 days` while ≥1 open position is `PROFITABLE`/`EXIT ZONE`-eligible | Capture pipeline likely broken (endpoint not being hit, or `log_trailing_stop_recommendation()` failing silently) — treat any rate computed after this point as unreliable until confirmed |
| Capture window | Fixed at `24 hours` from `recommended_at` (Product Owner-confirmed, v7.0 planning) | Not itself a tolerance band, restated here for completeness — a PATCH landing after 24h is correctly excluded from the numerator, not a data quality issue |

### Sign-off

- **Metrics Definitions & Analytics Owner:** agent-mediated sign-off cleared 2026-07-09 (ST-10, EPIC-03, v6.8); Validation Tolerances subsection agent-mediated sign-off cleared 2026-08-17 (ST-03, EPIC-01, v8.9)

---

## Realized / Unrealized P&L Split

**Added:** v1.16.0 — ST-06 (EPIC-03, v7.1, BLG-SPEC-83)

Formalises the realized-vs-unrealized P&L split shipped in v7.0 (EPIC-03 ST-14, `BLG-FEAT-70`, Tax Year and Monthly P&L reports) — no prior entry existed in this document for it.

### Definitions

- **Realized P&L (`realised_pnl_gbp`):** the GBP profit/loss of a **closed** trade — `exit_proceeds_gbp − total_cost_gbp` (fees already netted into both legs at their respective transaction time). One value per closed trade; summed across trades for a period total.
- **Unrealized P&L (`estimated_unrealised_pnl`):** the GBP profit/loss of currently **open** positions, marked to a reference price. A current-snapshot figure with no period/year attribution.

### Ownership Decision (stored vs. computed-on-read)

- **Realized:** stored. `trade_history.pnl` is written once, at exit time (`exit_position()`, `backend/services/position_service.py`), and never recomputed afterward. Reports sum this stored, immutable value — a closed trade's realized P&L cannot drift after the fact.
- **Unrealized:** **not** uniformly computed-on-read across the app — this is the one genuine ownership ambiguity this hardening pass surfaced (see reports.md `DEV-REPORTS-ST06-01`, `BLG-SPEC-87`):
  - The Positions page (`GET /positions` → `get_positions_with_prices()`) computes `pnl` **live**, against the current market price, on every request.
  - The Reports page's `estimated_unrealised_pnl` (`get_estimated_unrealised_pnl()`, `backend/services/reports_service.py`) sums the **stored** `positions.pnl` column, which is refreshed only once per night by the automatic trailing-stop ratchet (`run_nightly_trailing_stop_update()`) — a snapshot, not a live read, despite reading from the same underlying column name.
  - **This document's canonical position:** the Reports figure is a nightly snapshot by current implementation, not by documented design intent — `BLG-SPEC-87` tracks resolving this (either make it live, or explicitly label it as a snapshot). Until resolved, do not assume the two pages' unrealized figures agree at any given moment.

### Currency & Rounding Rules (Base44 frontend prompt)

- **Currency:** GBP only, for both realized and unrealized. US-market trades/positions are converted to GBP server-side (via the stored or live FX rate, per the ownership rule above) before the `pnl`/`realised_pnl_gbp` field is populated — the frontend never performs currency conversion for these fields.
- **Rounding:** `round(value, 2)` (2 decimal places) is applied server-side at computation time for every realized and unrealized figure returned by `/reports/*` and `/positions` (confirmed in `reports_service.py` and `position_service.py`). The frontend must display the value as received — no client-side re-rounding, which would risk producing a different-looking value than what a re-fetch of the same underlying row would show.
- **Sign convention:** positive = profit, negative = loss, matching every other P&L figure in the app (no separate sign convention for this feature).

### Reconciliation Rule

`realised_pnl_gbp` (summed over a period, or lifetime) plus `estimated_unrealised_pnl` (current snapshot) is an **approximate**, not exact, tie-back to the portfolio-level `total_pnl` field (`GET /portfolio`, balance-sheet method: `total_value − net_cash_flow`) — the two are independently derived and can diverge by the live-vs-snapshot valuation gap described above, plus minor FX-timing and rounding effects. See `docs/specs/frontend/pages/reports.md` §Combined Total Line for the full reconciliation rule text and a verified production example (2026-07-14: realised £1,100.46 + unrealised −£126.25 = £974.21 vs `total_pnl` £988.19, diff £13.98/≈1.4%).

### Visual Treatment

Profit `text-emerald-400`, loss `text-rose-400` — aligned with (not distinct from) the pre-existing Open Positions Panel P&L colour convention, so the same figure reads consistently wherever it appears. See `positions.md` and `reports.md` §Unrealised P&L Card for the full visual spec (closed this cycle via direct design gate edit to `reports.md` v0.9).

### Data Sources (API)

- `GET /reports/tax-year` — `summary.total_realised_pnl`, per-trade `trades[].realised_pnl_gbp`, `estimated_unrealised_pnl`
- `GET /reports/monthly-pnl` — per-month `data[].realised_pnl_gbp`, `estimated_unrealised_pnl`
- `GET /positions` — per-position live `pnl` (open positions only)
- `GET /portfolio` — `total_pnl` (lifetime, balance-sheet method — see Reconciliation Rule)

### Sign-off

- **Metrics Definitions & Analytics Owner:** agent-mediated sign-off cleared 2026-07-14 (ST-06, EPIC-03, v7.1)

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
| 2026-08-17 | 1.17.0 | ST-03 (EPIC-01, v8.9, BLG-SPEC-85): Add Validation Tolerances subsection to Trailing Stop Action Rate — numeric bounds for insufficient-sample, expected range, anomalously low/high, and stale-capture conditions, replacing the previously qualitative-only description. Metrics Definitions & Analytics Owner agent-mediated sign-off cleared 2026-08-17. | Metrics Definitions & Analytics Owner |
| 2026-07-14 | 1.16.0 | ST-06 (EPIC-03, v7.1, BLG-SPEC-83): Add Realized/Unrealized P&L Split section — formalises the v7.0 feature (no prior entry existed). Documents stored-vs-computed-on-read ownership decision (realized: stored at exit, immutable; unrealized: live on Positions page vs nightly-snapshot on Reports page — a genuine ambiguity surfaced this cycle, tracked as `BLG-SPEC-87`), currency/rounding rules (GBP, 2dp server-side, no client re-rounding), reconciliation rule (approximate tie-back to portfolio `total_pnl`, verified against production data), and visual treatment (aligned with Open Positions Panel convention). Metrics Definitions & Analytics Owner sign-off cleared 2026-07-14. | Metrics Definitions & Analytics Owner |
| 2026-02-16 | 1.5.0 | Initial comprehensive spec | Analytics Team |
| 2026-02-17 | 1.5.1 | FIX-MD-01: Add missing system metrics | Analytics Team |
| 2026-02-17 | 1.5.2 | FIX-MD-02: Add Risk/Reward Ratio and Expectancy | Analytics Team |
| 2026-02-17 | 1.5.3 | FIX-MD-03: Align Days Underwater to trade-sequence method | Analytics Team |
| 2026-02-17 | 1.5.5 | FIX-MD-04 backlog + FIX-MD-05: Specify Sharpe sample variance (canonical) and capital efficiency GBP-safe cost basis | Analytics Team |
| 2026-02-17 | 1.5.6 | ADVISORY-MD-D: Remove drift-prone lineage appendix; reference `data_model.md` and `analytics_endpoints.md` as lineage sources | Analytics Team |
| 2026-02-21 | 1.5.7 | BLG-TECH-01 resolution: mark Appendix E Backlog Items 1 and 2 as resolved. Update inline conformance notes in Sharpe Ratio and Capital Efficiency sections. Update Capital Efficiency response format example value to 0.22. Validation confirmed 13/13 pass at 2026-02-21T00:24:41Z. Canonical Owner sign-off granted. | Metrics Definitions & Analytics Canonical Owner |
| 2026-02-25 | 1.5.8 | BLG-FEAT-01: Add Current Drawdown section. Defines current_drawdown_percent formula, data sources (GET /portfolio new fields), relationship to days_underwater and max_drawdown metrics, failure behaviour, and implementation notes. QWB pre-alignment D1. | Metrics Definitions owner |
| 2026-03-12 | 1.7.0 | ST-03 (EPIC-02 v1.9): Add Cohort Metrics section — canonical formulas for cohort trade count, win rate, avg R-multiple, total P&L; period definitions (month/quarter/year); response format for GET /analytics/cohort. ST-04 (EPIC-02 v1.9): Add R-Multiple (Canonical Server-Side) section — server-side formula, qualifying conditions, sign convention, distribution bucket format for GET /analytics/r-multiple-distribution; minimum 5 qualifying trades. Analytics Team.
| 2026-03-02 | 1.6.0 | EPIC-03 (v1.7): Add Portfolio Risk Metrics section — canonical Position Risk formula (GBP-adjusted, FX handling for US positions, pence conversion for UK), Portfolio Heat formula (sum of position risks / portfolio value × 100), and explicit display threshold bands (Low <10%, Moderate 10–20%, High 20–30%, Extreme ≥30%) with canonical hex colour codes. TASK-06 through TASK-10 complete. Head of Specs Team lifecycle sign-off granted 2026-03-02 (Delegated Authority). v1.8 pre-alignment gate cleared. | Metrics Definitions & Analytics Owner + Head of Specs Team |
| 2026-03-11 | 1.7.0 | EPIC-01/02 (v1.9): Add Discipline & Compliance Metrics section (ST-01) — Journal Completion Rate, Stop-Based Exit Rate, Average Position Size % formulas for GET /analytics/compliance-metrics. Add Cohort Analysis Metrics section (ST-03 batch) — period grouping, per-cohort field definitions, minimum data threshold. Add R-Multiple Distribution (Backend) section (ST-04 batch) — canonical server-side R-multiple formula, 8 fixed buckets, summary statistics. Appendix B updated to list all three new endpoints. Metrics Definitions & Analytics Owner + Head of Engineering sign-off granted 2026-03-11 (EPIC-01 ST-01 delivery). | Metrics Definitions & Analytics Owner + Head of Engineering |
| 2026-04-06 | 1.9.0 | ST-09 (EPIC-03, v2.5): Add Fee Drag section — canonical formula (`exit_fees / gross_proceeds × 100`), portfolio average (`avg_fee_drag_pct`), qualifying conditions, sign convention, data source (existing columns, no schema change), display spec. Head of Specs Team co-authorship confirmed (ST-09 design gate cleared). | Metrics Definitions & Analytics Owner + Head of Specs Team |
| 2026-07-13 | 1.15.0 | ST-07 (EPIC-02, v7.0, BLG-BE-50): Trailing Stop Action Rate — instrumented the capture side. `trailing_stop_recommendation_log` table created and populated on every `GET /positions/{id}/stop-trail` call (`database.log_trailing_stop_recommendation()`, fire-and-forget). Capture window (24h) Product Owner-confirmed at planning. No PATCH-side schema change needed — `positions.stop_price`/`updated_at` already support the action-rate join. Metric-computation endpoint remains separate follow-up work. |
| 2026-07-03 | 1.12.0 | ST-08 (EPIC-03, v6.5, BLG-FEAT-41): Add Thesis Adoption Rate section — definition (adopted / generated), query approach joining `trade_plans.setup_thesis` to `gemini_audit_log.plan_id` (corrects the sprint scope's literal `claude_audit_log` reference, which has no `plan_id` column — see section's Query Approach note), data source, no schema/endpoint change required. Metrics Definitions & Analytics Owner + Financial Reporting & Records Owner + Product Owner sign-off. | Metrics Definitions & Analytics Owner |

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

---

## Arc 5 Compliance Metrics

**Introduced:** v4.0 (ST-01, BLG-FEAT-36)
**Endpoint:** `GET /analytics/arc5-compliance`
**Log Table:** `pre_entry_validation_log`

### validation_pass_rate_by_rule

- **Definition:** For each `rule_type`, `pass_rate = pass_count / (pass_count + fail_count)` over the requested `period`.
- **Rule types:** `regime_gate`, `cash_constraint`, `sector_concentration`, `earnings_proximity`, `sizing_validity`
- **Source table:** `pre_entry_validation_log` — logged by `GET /portfolio/pre-entry-validation` on every call (non-blocking write)
- **Default period:** rolling 7 days (`validated_at >= NOW() - INTERVAL '7 days'`)
- **Returns:** `{}` if no log data exists yet

### events_per_week

- **Definition:** `COUNT(*) FROM red_flag_events WHERE created_at >= NOW() - INTERVAL '7 days'` divided by 7.0 (always rolling 7 days regardless of `period` parameter)
- **Unit:** events per day × 7 (float)
- **Source:** `red_flag_events` table

### override_rate

- **Definition:** `COUNT(*) FROM red_flag_events WHERE event_type='pre_entry_override' AND created_at >= NOW()-7d` / `COUNT(*) FROM pre_entry_validation_log WHERE validated_at >= NOW()-7d`
- **Returns:** null if no validation attempts in the last 7 days
- **Always rolling 7 days**

### top_rule_breach

- **Definition:** `rule_type` with the highest `fail_count` in `pre_entry_validation_log` over the requested `period`
- **Returns:** null if no failures

### trade_plan_adherence_rate

- **Definition:** `COUNT(DISTINCT th.id) FROM trade_history th JOIN trade_plans tp ON tp.position_id=th.position_id` / `COUNT(*) FROM trade_history`
- **Window:** all-time (not period-filtered)
- **Returns:** null if no closed trades, or if `position_id` migration not run (`UndefinedColumn` caught gracefully)
- **Gate condition confirmed:** PO confirmed 2026-05-23 that trade-plan position_id linkage is actively captured

---

## Arc 5 Compliance Composite Score

**Introduced:** v4.1 (ST-08, BLG-FEAT-40)
**Endpoint data source:** `GET /analytics/arc5-compliance`
**Display:** percentage (0–100%)

### Formula

```
composite_score = (1 - override_rate) * 0.40 +
                  (1 - min(events_per_week / 10, 1)) * 0.30 +
                  trade_plan_adherence_rate * 0.20 +
                  (1 - top_rule_breach_severity_normalized) * 0.10
```

**Result range:** 0.0–1.0 (displayed as a percentage, e.g. 0.82 → 82%).

### Input Fields

| Field | Source | Notes |
|-------|--------|-------|
| `override_rate` | `GET /analytics/arc5-compliance` | Proportion of pre-entry validations overridden. Null treated as 0.0. |
| `events_per_week` | `GET /analytics/arc5-compliance` | Rolling 7-day red flag events per week. Clamped to 10 before normalisation. |
| `trade_plan_adherence_rate` | `GET /analytics/arc5-compliance` | All-time proportion of closed trades with linked trade plan. Null treated as 0.0. |
| `top_rule_breach` | `GET /analytics/arc5-compliance` | Rule type with highest fail count. Mapped to `top_rule_breach_severity_normalized`. |

### Severity Mapping

`top_rule_breach_severity_normalized` is derived from the `top_rule_breach` rule type:

| Rule type | Normalised severity |
|-----------|---------------------|
| `regime_gate` | 1.0 (high) |
| `sector_concentration` | 0.5 (medium) |
| `earnings_proximity` | 0.5 (medium) |
| `cash_constraint` | 0.5 (medium) |
| `sizing_validity` | 0.0 (low) |
| null | 0.0 (no breach) |

### Composite Score Unavailability

When any required input field is unavailable from the API (e.g. null `override_rate` with no data), the composite score is not computed. Individual metric components are displayed instead (per FEAT-42 §AC-05 fallback).

### v6.9 On-Demand Compliance Recheck — Confirmed No Formula Gap (ST-10, EPIC-03, v8.2, BLG-GOV-214)

**Question:** Does the v6.9 on-demand compliance recheck feature (`GET /positions/{position_id}/compliance-recheck`, `docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md`) affect any input to the Arc 5 composite formula above?

**Finding: No gap — confirmed already correct.** The on-demand recheck is session-local and non-persisted by design (its own service module states "no persisted state, no automation — §13"). It does not write to `pre_entry_validation_log` (source of `validation_pass_rate_by_rule`, `override_rate`, `top_rule_breach`) or `red_flag_events` (source of `events_per_week`) — verified by inspecting `backend/services/compliance_recheck_service.py` for writes to either table (none found) and confirming `compliance_recheck` is not among `red_flag_events`' `_VALID_EVENT_TYPES` enum (`pre_entry_override`, `checklist_skipped`, `stop_prompt_dismissed`, `drawdown_prompt_dismissed` only). The composite formula's four inputs are therefore entirely sourced from tables the recheck feature never touches — no formula update required.

### Sign-off

- **Metrics Definitions & Analytics Owner:** agent-mediated sign-off cleared 2026-05-27 (ST-08, EPIC-03, v4.1)
- **Product Owner:** agent-mediated sign-off cleared 2026-05-27 (ST-08, EPIC-03, v4.1)
- **Metrics Definitions & Analytics Canonical Owner (v6.9 no-gap confirmation):** agent-mediated sign-off cleared 2026-08-04 (ST-10, EPIC-03, v8.2, BLG-GOV-214)
