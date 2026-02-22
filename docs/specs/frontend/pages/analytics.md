# analytics.md

**Owner:** Frontend Specifications & UX Documentation Owner  
**Status:** Canonical  
**Version:** 1.2
**Last Updated:** February 22, 2026

## Purpose & User Goals
The Performance Analytics page provides deep insight into closed trade performance, risk metrics, and strategy effectiveness. It connects directly to the backend analytics system and is data-driven throughout — no values are calculated or derived on the frontend.

Users can:
- Evaluate risk-adjusted returns (Sharpe ratio, drawdown, expectancy)
- Identify behavioural patterns (hold time, win streaks, exit discipline)
- Compare performance by market (UK vs US)
- Analyse strategy tags to understand which setups work best
- Review time-based and R-multiple distributions
- Export a PDF summary report

---

## API Dependency

**Single endpoint:** `GET /analytics/metrics?period={period}`

All data on this page — including every metric, chart, and table — is sourced from this one call. The frontend transforms the snake_case response to camelCase and passes the nested objects directly to child components.

The page must never recalculate, derive, or override values returned by the backend.

---

## Period Filter

A `Select` in the page header controls the `period` query parameter. Options map to the API enum exactly:

| Label | Value |
|-------|-------|
| Last 7 Days | `last_7_days` |
| Last Month | `last_month` |
| Last Quarter | `last_quarter` |
| Last Year | `last_year` |
| Year to Date | `ytd` |
| All Time | `all_time` |

Default on load: `last_month`.

Changing the period re-fetches `GET /analytics/metrics?period={value}`.

---

## Page States

### Loading State
- A full-page spinner replaces content while the API call is in progress.
- Page header is visible but all components are hidden.

### Error State
- A full-page error panel replaces content if the API call fails.
- Shows an error icon, "Failed to Load Analytics" heading, the error message, and the backend URL for debugging.
- No retry button is required (period change will re-trigger).

### Not Enough Data State
Shown when `summary.has_enough_data` is `false` (i.e. `total_trades < min_required`).
- Period selector remains active.
- Export button is disabled.
- A centred message shows: "Need at least {min_required} closed trades to show analytics. You currently have {total_trades} trade(s) in the selected period."
- No charts or metric components render.

### Main Render State
Shown when `summary.has_enough_data` is `true`. All components render in order.

---

## Export PDF

An "Export PDF" button appears in the page header alongside the period selector.

- Disabled when `has_enough_data` is `false`.
- On click, generates a print-optimised HTML report in a new window and triggers the browser print dialog.
- The report includes: executive summary cards, key insights, and advanced metrics table.
- Content is based on the current period's data.

---

## Component Rendering Order

When data is available and sufficient, components render in this order:

1. **Executive Summary Cards** — six metric cards
2. **Key Insights** — 3–5 generated text insights
3. **Advanced Metrics Grid** — eight metrics in a 2-column grid
4. **Monthly Performance Heatmap** — calendar-style P&L tiles
5. **Underwater Equity Curve** — drawdown chart from `trades_for_charts`
6. **Market Comparison** — UK vs US side-by-side panels
7. **Performance by Exit Reason** — sortable table from `exit_reasons`
8. **Time-Based Analysis** — tabbed charts (day of week / monthly / holding period / entry scatter)
9. **R-Multiple Analysis** — distribution chart + tag breakdown from `trades_for_charts`
10. **Best / Worst Trades** — top 3 / bottom 3 by R-multiple from trades_for_charts  ← NEW (BLG-FEAT-04)
11. **Top Performers** — top 5 winners and top 5 losers from `top_performers`
12. **Win Rate by Month** — bar chart from monthly_data  ← NEW (BLG-FEAT-05)
13. **Consistency Metrics** — three consistency cards from `consistency_metrics`
14. **Performance by Strategy Tag** — sortable tag performance table from `trades_for_charts`

---

## Component Specifications

### 1. Executive Summary Cards
Source: `executive_metrics` + `advanced_metrics`

Six cards in a responsive grid (1 → 2 → 3 columns):

| Card | Value | Source field |
|------|-------|-------------|
| Sharpe Ratio | `sharpe_ratio` (2dp) | `executive_metrics.sharpe_ratio` |
| Max Drawdown | `max_drawdown.percent` (1dp%) + amount + date | `executive_metrics.max_drawdown` |
| Recovery Factor | `recovery_factor` (2dp) | `executive_metrics.recovery_factor` |
| Expectancy | `£expectancy` (2dp) | `executive_metrics.expectancy` |
| Time Underwater | `days_underwater` days (or "At Peak 🎉" if 0) + peak equity | `advanced_metrics.days_underwater`, `advanced_metrics.portfolio_peak_equity` |
| Profit Factor | `profit_factor` (2dp) | `executive_metrics.profit_factor` |

Each card has a coloured gradient icon, subtitle, and a benchmark badge (Excellent / Good / Needs Improvement) where applicable.

---

### 2. Key Insights
Source: `executive_metrics` + `advanced_metrics.avg_hold_winners` / `avg_hold_losers`

Generates up to 5 text insight strings from the metric values:
- Sharpe ratio quality assessment
- Hold time comparison (winners vs losers — discipline check)
- Profit factor commentary
- Expectancy edge assessment
- Risk/reward ratio commentary

Insights are generated client-side from the metric values returned by the API. They are observational, not advisory.

---

### 3. Advanced Metrics Grid
Source: `advanced_metrics` + `executive_metrics`

Eight metrics in a 2-column grid, grouped in pairs:

| Metric | Source |
|--------|--------|
| Profit Factor (target >1.5) | `executive_metrics.profit_factor` |
| Risk/Reward Ratio (target >2.0) | `executive_metrics.risk_reward_ratio` |
| Win Streak | `advanced_metrics.win_streak` |
| Loss Streak | `advanced_metrics.loss_streak` |
| Avg Hold Time (Winners) | `advanced_metrics.avg_hold_winners` |
| Avg Hold Time (Losers) | `advanced_metrics.avg_hold_losers` |
| Trade Frequency | `advanced_metrics.trade_frequency` |
| Capital Efficiency | `advanced_metrics.capital_efficiency` |

---

### 4. Monthly Performance Heatmap
Source: `monthly_data`

A grid of calendar-style tiles, one per month in the response. Each tile shows:
- Month label
- P&L value (with sign prefix)
- Trade count

Tile colour is determined by P&L magnitude:

| Range | Colour |
|-------|--------|
| > £500 | Emerald-500 |
| £100 – £500 | Emerald-400 |
| ±£100 | Slate-600 |
| -£100 to -£500 | Rose-400 |
| < -£500 | Rose-500 |

Hover shows a tooltip with full detail (month, P&L, trades, win rate).

---

### 5. Underwater Equity Curve
Source: `trades_for_charts`

An area chart showing drawdown percentage below peak equity over time, calculated from the cumulative P&L sequence of `trades_for_charts`.

- X axis: `exit_date` (formatted as "Mon DD")
- Y axis: drawdown % (always ≤ 0)
- The maximum drawdown point is marked with a red dot labelled "Max DD"
- A tooltip shows: date, drawdown %, current equity, peak equity

Empty state: shown if fewer than 3 trades available.

> Note: This chart derives drawdown from the trade-by-trade P&L sequence in `trades_for_charts`. This is a visualisation aid. The authoritative `max_drawdown` figure comes from `executive_metrics.max_drawdown`, which is calculated server-side from portfolio snapshots.

---

### 6. Market Comparison
Source: `market_comparison.UK` and `market_comparison.US`

Two side-by-side panels (stacks to single column on mobile), one for each market.

Each panel shows:
- Trade count (badge)
- Win rate
- Total P&L (signed, GBP)
- Average win (GBP)
- Average loss (GBP, shown as positive magnitude)
- Best performer (ticker + P&L)
- Worst performer (ticker + P&L)

All values are null-safe; shows "No trades yet" when no data for that market.

---

### 7. Performance by Exit Reason
Source: `exit_reasons`

A table showing one row per exit reason with columns:
- Exit Reason
- Count
- Win Rate (%)
- Total P&L (signed, GBP)
- Avg P&L (signed, GBP)
- % of Trades

No sorting. Displayed in API order.

---

### 8. Time-Based Analysis
Four tabs, each containing a chart:

**Day of Week tab** — Source: `day_of_week`
Bar chart of average P&L by day of week. Summary row beneath shows trade count per day.

**Monthly tab** — Source: `monthly_data`
Composed chart: bars for monthly P&L (left axis) + line for cumulative P&L (right axis).

**Holding Period tab** — Source: `holding_periods`
Bar chart of average P&L by holding period bucket. Summary row beneath shows trade count and win rate per bucket.

**Entry Analysis tab** — Source: `trades_for_charts`
Scatter chart of entry price vs P&L, colour-coded by market (UK = cyan, US = violet).

---

### 9. R-Multiple Analysis
Source: `trades_for_charts`

Requires trades with `entry_price`, `exit_price`, and `stop_price` present. R-multiple is calculated client-side as:
```
risk = |entry_price - stop_price|
r_multiple = (exit_price - entry_price) / risk
```

> Note: R-multiple cannot be calculated server-side as the initial stop price is not stored in `trade_history`. This is an intentional exception to the "no frontend calculation" rule — it is a visualisation aid, not a financial metric.

Minimum 10 qualifying trades required to render. Shows a message if fewer trades are available.

Displays:
- Bar chart of R-multiple distribution across 7 buckets (< -2R, -2R to -1R, -1R to 0R, 0R to 1R, 1R to 2R, 2R to 3R, > 3R)
- Statistics grid: Avg R, Max R (best trade), Max loss (worst trade), Win rate, Avg winner R, Avg loser R
- Expandable section: R-Multiple by Tag table (sortable by Avg R, count, win rate)

---

### 10. Top Performers
Source: `top_performers.winners` and `top_performers.losers`

Two side-by-side panels: Top 5 Winning Trades and Top 5 Losing Trades.

Each trade card shows:
- Ticker
- Entry date
- P&L (signed, GBP)
- P&L % (signed)
- Days held
- Exit reason

---

### 11. Best / Worst Trades

Source: `trades_for_charts` from `GET /analytics/metrics`

Two side-by-side panels: **Top 3 Trades by R-Multiple** and **Bottom 3 Trades by R-Multiple**.

#### Ranking

Trades ranked by R-multiple (frontend-calculated). Canonical formula per `metrics_definitions.md` v1.5.7:

```
R = (exit_price - entry_price) / (entry_price - stop_price)
```

Top 3 = highest positive R-multiple values. Bottom 3 = lowest (most negative) R-multiple values.

Trades where `stop_price` is null or zero are excluded from ranking (R-multiple cannot be calculated).

If fewer than 3 qualifying trades exist for either panel, render available trades and leave remaining card slots empty (do not pad with unqualified trades or show placeholders).

#### Minimum data requirement

Requires at least 1 qualifying trade to render. If no qualifying trades exist (no `stop_price` present on any trade in `trades_for_charts`), render the component's empty state.

#### Trade card contents

Each card shows:

-   Ticker (bold)
-   R-multiple value: signed, 2dp, "R" suffix (e.g. `+3.12R` / `-0.54R`)
-   P&L (GBP, signed --- secondary label)
-   Exit date (tertiary label)
-   Exit reason (tertiary label)

#### Colour treatment

-   Top 3 panel header and R-multiple values: profit colour (green tone per `design_system.md`)
-   Bottom 3 panel header and R-multiple values: loss colour (red tone per `design_system.md`)

#### Layout

Responsive: 1 column (mobile, panels stack) → 2 columns (lg, panels side-by-side). Each panel title: "Best Trades (R-Multiple)" and "Worst Trades (R-Multiple)".

#### Empty state

If no qualifying trades: display a muted message --- "No trades with stop data available."

---

### 12. Win Rate by Month

Source: `monthly_data` from `GET /analytics/metrics`

A bar chart showing win rate (%) for each calendar month in the selected period.

#### Data mapping

-   X-axis: month labels (e.g. "Jan 26", "Feb 26") derived from `monthly_data[].month`
-   Y-axis: win rate (%), 0--100 range. Fixed scale; does not auto-scale.
-   Bar value: `monthly_data[].win_rate`

#### Reference line

A horizontal reference line at 50% (break-even win rate). Rendered as a muted dashed line. Does not have an interactive label --- it is orientation only.

#### Colour treatment

-   Bars above 50%: profit colour (green tone per `design_system.md`)
-   Bars at or below 50%: loss colour (red tone per `design_system.md`)

Each bar uses a single colour determined by its own value --- not a gradient.

#### Tooltip

- On hover/touch: show month label, win rate (%), and trade count for that month. Trade count sourced from monthly_data[].trade_count.

**Rationale:** analytics_endpoints.md canonical schema names this field trade_count. total_trades does not exist in monthly_data. Correcting to match the API contract.

#### Minimum data requirement

Requires at least 1 month of data. If `monthly_data` is empty, the component does not render (consistent with `has_enough_data = false` guard).

#### Layout

Full-width within the analytics page column. Chart height: consistent with other bar charts on the page (implementation choice within this constraint).

#### Empty state

If `monthly_data` is empty, component does not render. No explicit empty state message needed --- the page-level insufficient data guard handles this case.

---

### 13. Consistency Metrics
Source: `consistency_metrics`

Three cards:

| Card | Field |
|------|-------|
| Consecutive Months Profitable | `consecutive_profitable_months` + current streak note |
| Win Rate Consistency | `win_rate_std_dev` (%) + qualitative label (Very consistent / Consistent / Variable) |
| Monthly P&L Volatility | `pnl_std_dev` (GBP, 0dp) |

---

### 14. Performance by Strategy Tag
Source: `trades_for_charts` (uses `tags` and `pnl` fields)

A sortable table showing one row per tag used across trades in the selected period.

Columns:
- Tag (pill)
- Count
- Win Rate (%)
- Total P&L (signed, GBP)
- Avg P&L (signed, GBP)

Sortable by: count, win rate, total P&L. Default sort: total P&L descending.

A summary line beneath the table names the top-performing tag by the currently selected sort metric.

Returns `null` (renders nothing) if no tagged trades exist.

---

## Responsive Behavior
- Period selector and export button stack or compress at smaller widths
- Summary cards: 1 column (mobile) → 2 columns (sm) → 3 columns (lg)
- Market Comparison panels: 1 column (mobile) → 2 columns (lg)
- Top Performers panels: 1 column (mobile) → 2 columns (lg)
- Charts scale responsively within their containers
- All tables support horizontal scroll on small screens

---

## Empty & Null Safety
All component props are null-safe with safe defaults. If the API returns partial data for a specific sub-object, the relevant component renders its empty state rather than crashing. The root-level insufficient data check (`has_enough_data`) is the primary gate.

---

## Change Log

| Version | Date | Change |
| --- | --- | --- |
| 1.2 | 2026-02-26 | F-02 fix: correct Win Rate by Month tooltip field name from `total_trades` to `trade_count` to match `analytics_endpoints.md` monthly_data schema. QA finding A-QA-01.
| 1.1 | 2026-02-25 | BLG-FEAT-04: Add Best / Worst Trades component spec (R-multiple ranking, top 3 / bottom 3, trades_for_charts source). BLG-FEAT-05: Add Win Rate by Month bar chart spec (monthly_data source, 50% reference line, colour-coded bars). Components inserted at positions 11 and 12 in rendering order. QWB D3. |
| 1.0 | 2026-02-18 | Initial version. |
