# analytics.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.1
**Last Updated:** 2026-08-11 (ST-10, EPIC-03, v8.6 — DEV-EPIC02-ST03-01 marked Resolved: CohortAnalysis.js was already migrated to GET /analytics/cohort, commit af22ea6e, 2026-03-16 — tracking-only correction, no new code shipped by this story); prior — 2026-08-11 (v8.6 design gate — §21 Trade Plan Completion Rate added, ST-01/BLG-FEAT-32); prior — 2026-08-11 (Head of Specs Team direct action — DEV-EPIC02-ST03-01 re-triaged: stale v1.10 target and never-filed backlog reference corrected to BLG-FE-155, tracking-field correction only)
**Design Source (v2.1 additions):** docs/design/2026-08-11__release-v8.6/trade-plan-completion-rate-metric/decision_record.md
**Design Source (v2.0 additions):** docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md
**Design Source (v4.6 additions):** docs/specs/si02/si02_fe_component_predesign.md v1.0; docs/specs/si02/si02_fe_interaction_spec.md v1.0
**Design Source (v2.8 additions):** docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md
**Design Source (v2.3 additions):** docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v1.9 additions):** docs/design/2026-03-06__release-v1.9/
**Design Source (v2.1 additions):** docs/design/2026-03-18__release-v2.1/chart-interactivity/ux_spec.md

## Purpose & User Goals
The Performance Analytics page provides deep insight into closed trade performance, risk metrics, and strategy effectiveness. It connects directly to the backend analytics system and is data-driven throughout — no values are calculated or derived on the frontend.

Users can:
- Evaluate risk-adjusted returns (Sharpe ratio, drawdown, expectancy)
- Identify behavioural patterns (hold time, win streaks, exit discipline)
- Compare performance by market (UK vs US)
- Analyse strategy tags to understand which setups work best
- Review time-based and R-multiple distributions
- Analyse performance by cohort period (month/quarter/year)
- View R-multiple distribution computed canonically from backend
- Monitor discipline and compliance metrics
- Export a PDF summary report
- See data freshness indicator (v2.3)
- View market correlation analysis per position (v2.8)
- Monitor behavioural drift across 4 key trading behaviour metrics — advisory, display-only (v4.6)

---

## API Dependency

**Primary endpoint:** `GET /analytics/metrics?period={period}`

All core analytics data is sourced from this call. The frontend transforms the snake_case response to camelCase and passes nested objects directly to child components.

**Additional endpoints (v1.9 additions):**
- `GET /analytics/cohort?period={month|quarter|year}` — Cohort Analysis panel (§15)
- `GET /analytics/r-multiple-distribution` — R-Multiple Distribution Backend panel (§16)
- `GET /analytics/compliance-metrics` — Discipline & Compliance panel (§17)

**Additional endpoints (v2.8 additions):**
- `GET /analytics/market-correlation` — Market Correlation panel (§18)

**Additional endpoints (v4.0 additions):**
- `GET /analytics/arc5-compliance` — Arc 5 Signal Compliance panel (§19)

**Additional endpoints (v4.6 additions):**
- `GET /analytics/behavioural-drift` — Behavioural Drift panel (§20)

**Additional endpoints (v2.0/v6.8 additions):**
- `GET /analytics/tag-performance?tags={csv}` — Trade Plan Tag Filter comparison row (§14a)

**Additional endpoints (v2.1 additions):**
- `GET /analytics/trade-plan-completion-rate` — Trade Plan Completion Rate panel (§21), optionally tier-segmented

The page must never recalculate, derive, or override values returned by the backend.

> **Note on §9 R-Multiple Analysis:** The existing §9 component performs client-side R-multiple calculation from `trades_for_charts` data as an intentional exception. The new §16 component (R-Multiple Distribution Backend) uses server-side computed values from a dedicated endpoint. Both may coexist; §16 is the canonical metric; §9 remains a visualisation aid.

---

## Metrics Staleness Indicator (v2.3 — ST-02 BLG-FEAT-09)

**Design source:** docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md

### Placement

Below the page title, above the period selector.

### Display

- Normal: `Data as of N mins ago` (grey, secondary typography)
- Stale (≥4h): `⚠ Data as of Nh ago — may be outdated` (amber)
- Hover tooltip: absolute ISO timestamp (e.g. `Updated: 2026-03-24 09:41 UTC`)
- If `last_sync_at` absent or null: indicator hidden

### Relative time rules

< 1 min → "just now" | 1–59 min → "N mins ago" | 1–23 h → "Nh ago" | ≥24 h → "N days ago"

### Data source

Backend exposes `last_sync_at` field on `GET /analytics/metrics` response (or a separate endpoint). If the field is absent, the indicator is omitted entirely. openapi.yaml must be updated if field is added to the response schema.

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
15. **Cohort Analysis** — trade performance grouped by entry period (month/quarter/year) ← NEW (v1.9, ST-03)
16. **R-Multiple Distribution (Backend)** — canonical server-side R-multiple distribution chart ← NEW (v1.9, ST-04)
17. **Discipline & Compliance** — journal completion rate, stop-based exit rate, avg position size ← NEW (v1.9, ST-01)
18. **Market Correlation** — per-position Pearson correlation with severity colour-coding + portfolio-level weighted average ← NEW (v2.8, ST-01)
19. **Arc 5 Signal Compliance** — red flag event frequency, override rate, top rule breach, trade plan adherence ← NEW (v4.0, ST-02/ST-04)
20. **Behavioural Drift** — 4 drift metrics (entry timing, sizing adherence, post-loss sizing, regime adherence) displayed as percentage deviation cards ← NEW (v4.6, ST-06/ST-07)
21. **Trade Plan Completion Rate** — plans created/completed/abandoned + completion rate, optionally segmented by setup quality score tier ← NEW (v8.6, ST-01)

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

#### Drill-Down: Click Tile → Monthly Trade View

Clicking a heatmap tile (with at least 1 trade) opens a **Monthly Trades modal** showing the trades from that month.

**Modal contents:**
- Title: `"Trades — [Month YYYY]"` (e.g. `"Trades — Jan 2026"`)
- A table of trades from that month sourced from `trades_for_charts`, filtered by `exit_date` month.
- Columns: Ticker, Exit Date, P&L (GBP, signed, colour-coded), R-Multiple (if available), Exit Reason.
- Summary line at top: `"[n] trades · Total P&L: £X.XX"`
- Close button (X) in modal header. Also closes on backdrop click or Escape key.

**Tile selected state:** While the modal is open, the originating tile receives a 2px inset ring in the design system focus/accent colour.

**Tile with 0 trades:** Not clickable; cursor: default; no modal opens.

**Data source:** `trades_for_charts` (already loaded on the analytics page). No additional API call. Month attribution uses `exit_date`.

---

### 5. Underwater Equity Curve
Source: `trades_for_charts`

An area chart showing drawdown percentage below peak equity over time, calculated from the cumulative P&L sequence of `trades_for_charts`.

- X axis: `exit_date` (formatted as "Mon DD")
- Y axis: drawdown % (always ≤ 0)
- The maximum drawdown point is marked with a red dot labelled "Max DD"
- A tooltip shows: date, drawdown %, current equity, peak equity
- Tooltip positioning: follows cursor within chart bounds; flips to left side if cursor is in the right 30% of the chart.

#### Zoom

**Trigger:** Scroll wheel over the chart, or pinch on touch. Desktop fallback: `+` / `−` buttons in the chart's top-right corner.

**Behaviour:**
- Time-axis (x-axis) zoom only. Y-axis auto-scales to the zoomed range.
- Minimum zoom: 4 data points.
- Maximum zoom: full data range (default state).
- Scroll/pinch zooms centred on the cursor position.
- **Pan:** When zoomed in, click-drag pans left/right within the zoomed range.
- **Reset button:** Appears in the chart top-right only when zoomed in. Label: "Reset". Clicking restores the full range and hides the Reset button.
- A muted "Scroll to zoom" hint label may appear on first interaction and fade after 3s.

No additional API call for zoom/pan — all interaction is over the already-loaded `trades_for_charts` data series.

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

**Tooltip (per bar):** On hover: R-multiple range (e.g. `"1.0R – 2.0R"`), trade count (e.g. `"4 trades"`), percentage of total closed trades (e.g. `"22%"`). Percentage computed from the distribution data already present in the chart (total count is available from the same `trades_for_charts` set). Tooltip positioning: follows cursor; flips if near chart edge.

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

#### 14a. Trade Plan Tag Filter (v2.0 — ST-05, BLG-FEAT-52)

**Design source:** `docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md`

Separate from the table above — this filter operates on **trade-plan tags** (`trade_plans.trade_tags`, independent of the position/journal `tags` field used by the §14 table itself, which is unaffected).

- Multi-select dropdown directly above the §14 heading: "Filter by trade plan tag"
- Selected tags appear as dismissible pills below the dropdown (OR logic across selections — matches `positions.md` Tag filter interaction pattern)
- **Data source:** `GET /analytics/tag-performance?tags={csv}`
- When ≥1 tag selected: a comparison row renders above the §14 table showing win rate + avg R-multiple per selected tag
- No tags selected: comparison row hidden; §14 table renders as today, unaffected
- No matching closed trades for a selected tag: "No closed trades for selected tag(s)"
- Loading: inline skeleton on the comparison row. Error: comparison row hidden silently — does not block §14 table

**§13 Compliance:** Display-only. No automated action taken on tag values.

---

### 15. Cohort Analysis
Source: `GET /analytics/cohort?period={month|quarter|year}`

**Design source:** docs/design/2026-03-06__release-v1.9/cohort-analysis/ux_spec.md

A performance table grouping closed trades by entry period.

**Period selector:** Three toggle buttons (Month / Quarter / Year) rendered above the table. Active state highlighted. Changing period triggers a new API call with the updated period parameter.

**Table columns:**
| Column | Source field | Format |
|--------|-------------|--------|
| Period | `period_label` | e.g., "Mar 2026" |
| Trades | `trade_count` | integer |
| Win Rate | `win_rate` | percentage, 1dp |
| Avg R-Multiple | `avg_r_multiple` | 1dp with "R" suffix |
| Total P&L | `total_pnl` | signed GBP, 2dp; green if positive, red if negative |

Rows sorted descending by period (most recent first). Requires canonical definitions in `metrics_definitions.md` (cohort metric formulas).

**States:**
- Loading: skeleton table rows
- Loaded: table rendered
- Insufficient history: message "Not enough closed trades to show [period] cohorts" (fewer than 3 periods available)
- Error: section-level error card

---

### 16. R-Multiple Distribution (Backend)
Source: `GET /analytics/r-multiple-distribution`

**Design source:** docs/design/2026-03-06__release-v1.9/r-multiple-distribution/ux_spec.md

A bar chart of R-multiple values computed server-side. Uses the canonical R-multiple formula from `metrics_definitions.md`. This is the authoritative R-multiple distribution; the §9 component remains as a supplementary visualisation aid.

**Chart:**
- X-axis: R-multiple range buckets (bucket boundaries defined by Metrics Definitions owner in `metrics_definitions.md`)
- Y-axis: trade count
- Bars: green for positive R buckets, red for negative R buckets
- Hover tooltip: trade count and R-multiple range for hovered bar

**Summary stats row (below chart):**
| Stat | Source field |
|------|-------------|
| Median R | `median_r` |
| % trades > 1R | `pct_above_1r` |
| Avg Winner | `avg_winner_r` |
| Avg Loser | `avg_loser_r` |

**Minimum data:** 5 closed trades required. Below threshold: "Close at least 5 trades to see R-multiple distribution."

**Hard rule:** All values sourced from backend. No client-side R-multiple computation in this component.

**States:** Loading (skeleton chart), Loaded, Insufficient data (message), Error (section-level card).

---

### 17. Discipline & Compliance
Source: `GET /analytics/compliance-metrics`

**Design source:** docs/design/2026-03-06__release-v1.9/compliance-metrics/ux_spec.md

A section displaying three compliance scalar metrics as stat cards. Section title: "Discipline & Compliance".

**Three metric cards in a horizontal row (responsive: stacks on narrow viewports):**

| Card | Source field | Format |
|------|-------------|--------|
| Journal Completion Rate | `journal_completion_rate` | percentage, 1dp; sub-label: "last N trades" |
| Stop-Based Exit Rate | `stop_exit_rate` | percentage, 1dp; sub-label: "last N trades" |
| Avg Position Size | `avg_position_size_pct` | percentage, 2dp; sub-label: "of portfolio, last N trades" |

Metric definitions are canonical per `metrics_definitions.md`. Denominator/period reflected in sub-label per API response.

**Insufficient data:** Individual card shows "–" with tooltip "Insufficient trade history" when denominator is zero or null.

**States:** Loading (skeleton cards), Loaded, Error (section-level card).

**Hard rule:** All values backend-computed. No frontend derivation.

---

### 18. Market Correlation
Source: `GET /analytics/market-correlation`

**Design source:** docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md

Section title: "Market Correlation". Appended after §17 in the rendering order.

**Portfolio-level summary (above table):**

| Element | Source | Display |
|---------|--------|---------|
| Weighted average | `portfolio_weighted_avg_correlation` | 2dp value + severity badge |
| Severity | `portfolio_correlation_severity` | Colour-coded pill |

**Per-position table:**

| Column | Source field | Format |
|--------|-------------|--------|
| Ticker | `symbol` | Uppercase |
| Correlation | `pearson_correlation` | 2dp; "N/A" if null |
| Severity | `severity` | Colour-coded severity badge |
| vs. Market | `benchmark_symbol` | Ticker label |

**Severity colour scheme:**
- `high` → Rose-500 (red)
- `moderate` → Amber-500 (amber)
- `low` → Emerald-500 (green)
- null → Slate-500, "N/A" text, no badge; row sorts to bottom

Default table sort: severity descending (high → moderate → low → N/A).

**Null handling:** Position with `pearson_correlation: null` renders "N/A" with no severity badge. Portfolio summary with all nulls shows "N/A" but section still renders.

**States:** Loading (skeleton rows), Loaded, No positions ("No open positions to correlate."), Error (section-level card).

**Hard rules:**
- All values sourced from backend. No client-side correlation computation.
- Section does NOT render when `has_enough_data = false`.
- Uses Analytics page 8h cache TTL.

---

### 19. Arc 5 Signal Compliance
Source: `GET /analytics/arc5-compliance`

**Design source:** docs/design/2026-05-22__release-v4.0/arc5-analytics-metrics/ux_spec.md

Section title: "Arc 5 Signal Compliance". Appended after §18 in the rendering order.

**Four metric cards in a horizontal row (responsive: stacks on narrow viewports):**

| Card | Source field | Format |
|------|-------------|--------|
| Red Flag Events/Week | `events_per_week` | integer; sub-label: "rolling 7 days" |
| Override Rate | `override_rate` | percentage, 1dp; sub-label: "overrides / validation attempts" |
| Top Rule Breach | `top_rule_breach` | text label (e.g. "regime_gate"); sub-label: "most frequent event type" |
| Trade Plan Adherence | `trade_plan_adherence_rate` | percentage, 1dp; sub-label: "trades with plan / total closed trades" |

Metric definitions are canonical per `metrics_definitions.md`.

**Insufficient data:** Individual card shows "–" with tooltip "Insufficient data" when source field is null or denominator is zero. `top_rule_breach` null → "–" with tooltip "No events in period".

**States:** Loading (skeleton cards), Loaded, Error (section-level card).

**Hard rule:** All values backend-computed. No frontend derivation.

---

### 20. Behavioural Drift

Source: `GET /analytics/behavioural-drift`

**Design source:** `docs/specs/si02/si02_fe_component_predesign.md` v1.0; `docs/specs/si02/si02_fe_interaction_spec.md` v1.0

Section title: "Behavioural Drift". Appended after §19 in the rendering order. Rendered as a collapsible section with a visible "Advisory" badge at all times (per §13 advisory-only binding).

**Section heading:** "Behavioural Drift   [Advisory]"

The "Advisory" badge is an amber pill, always visible without hover. This satisfies the §13 display-only binding condition.

**Collapse/expand:** Section includes a chevron toggle. Collapse state persisted to `localStorage` key `si02.driftPanel.collapsed`. When collapsed, a compact status indicator is shown: "! N metrics drifting" (when `status === "drift_detected"`); no indicator when `status === "no_drift"`.

**Four metric cards in a 2-column grid (sm+), 1 column (mobile) — matching Arc5ComplianceSection layout:**

Each card shows:
- Metric label (top-left, uppercase small caps)
- Measured value + unit (primary, bold)
- Threshold reference line (e.g. "Threshold: ≤ 1.0 days")
- Deviation percentage, coloured by status (e.g. "+140% above threshold")
- Advisory note (when `status === "breached"` only; amber text, `text-xs`)
- Coloured card border driven by metric status

| Metric ID | Label | Unit | Threshold direction |
|-----------|-------|------|---------------------|
| `entry_timing_drift` | Entry Timing | days | lte |
| `sizing_adherence` | Sizing Adherence | pct_of_portfolio | lte |
| `consecutive_loss_sizing` | Post-Loss Sizing | pct_of_portfolio | lte |
| `regime_context` | Regime Adherence | pct | gte |

**Status colour scheme:**
- `ok` → `border-emerald-500/60` (green)
- `approaching` → `border-amber-500/60` (amber); no advisory note
- `breached` → `border-rose-500/60` (red); advisory note shown

**Section-level states:**
- `loading`: four skeleton cards; heading + advisory badge visible and static
- `insufficient_data`: single muted panel — "Behavioural drift analysis requires at least 20 closed trades. Currently {trade_count} trade(s) recorded. This panel will activate automatically once the threshold is reached." No metric cards.
- `no_drift`: four metric cards, all green; subdued "All metrics within threshold" indicator in section heading
- `drift_detected`: metric cards with colour-coded borders; amber/red accent on section heading consistent with highest-severity metric
- `error`: single panel — "Unable to load drift analysis." + Retry button

**Period binding:** The component receives a `period` prop from `PerformanceAnalytics` and passes it as `?period=<value>` to `GET /analytics/behavioural-drift`. Default: `last_90_days`. Re-fetches on period change and on window focus (staleTime: 5 min).

**Hard rules:**
- All values backend-computed. No client-side drift metric derivation.
- "Advisory" badge must be visible at all times including loading and insufficient-data states.
- No UI affordance may imply automated remediation — §13 binding constraint.
- Section does NOT gate, block, or modify any trade plan, position entry, or exit workflow.

**States:** Loading (skeleton cards), Loaded, Insufficient data (muted message), Error (section-level card with Retry).

**Playwright coverage required:** per `si02_fe_interaction_spec.md §10` — 13 test cases (DFT-01 through DFT-13) covering all 5 states, collapse/expand, period change re-fetch, tooltips, and accessibility.

---

### 21. Trade Plan Completion Rate

Source: `GET /analytics/trade-plan-completion-rate`

**Design source:** `docs/design/2026-08-11__release-v8.6/trade-plan-completion-rate-metric/decision_record.md`

Appended after §20 in the rendering order. Three summary cards (matching the §13 Consistency Metrics layout):

| Card | Field | Format |
|------|-------|--------|
| Plans Created | `plans_created` | integer |
| Completion Rate | `completion_rate` | percentage, 1dp; green ≥60%, amber 40–59%, red <40% (mirrors §13 Win Rate Consistency's qualitative-threshold convention) |
| Plans Abandoned | `plans_abandoned` | integer + `(N%)` of `plans_created`, in the canonical secondary-text token (`text-slate-600 dark:text-slate-400`) |

A one-line summary beneath the cards: `"{plans_completed} of {plans_created} plans completed"`.

**Optional quality-tier breakdown:** a small table, one row per PT-04 quality tier (`Excellent` / `Good` / `Fair` / `Low` — labels per `trade_plan.md` §7a), each row showing that tier's own `completion_rate`. Rendered only when the response includes tier-segmented data; omitted entirely (not an empty table) when it doesn't.

**States:**
- Loading: skeleton cards
- Loaded: cards + summary line (+ tier table if present)
- Empty (`plans_created === 0`): `DataState` `empty` branch — "No trade plans created yet." (not a `0%` completion rate)
- Error: section-level error card

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

## Known Deviations

### DEV-EPIC02-ST03-01 — Cohort Analysis: client-side cohort computation instead of GET /analytics/cohort — RESOLVED

**Story:** ST-03 — Cohort Analysis (original); ST-10 (EPIC-03, v8.6, BLG-FE-155) — resolution
**Description:** `CohortAnalysis.js` received a `trades` prop from `PerformanceAnalytics.js` and computed cohort groupings, win rates, avg R-multiple, and net P&L entirely client-side via `buildCohorts()`, instead of calling `GET /analytics/cohort?period=` despite that endpoint being implemented and wired in `base44Client.js`.
**Canonical requirement:** analytics.md §15 hard rule — "All values sourced from backend. No client-side R-multiple computation in this component." API Dependency section lists `GET /analytics/cohort?period={month|quarter|year}` as the source for §15.
**Priority:** P2 — spec hard-rule violation. Values were numerically correct (same formula); the deviation was architectural (wrong computation layer).
**Impact:** avg_r_multiple in the cohort table used client-side R computation from `stop_price`, which may be `null` for trades without stop data (returns `null` avg R). Backend endpoint uses `initial_stop` via LEFT JOIN and has the same null-return behaviour, so displayed values were consistent throughout — no live correctness bug at any point.
**Resolution:** `CohortAnalysis.js` was already migrated to source all displayed values (`period_label`, `trade_count`, `win_rate`, `avg_r_multiple`, `total_pnl`) directly from `api.analytics.cohort(period)`'s response, with no local `buildCohorts()` computation path remaining — confirmed by code review of the current file, 2026-08-11. This shipped in commit `af22ea6e` ("[EPIC-02][ST-04] Refactor CohortAnalysis to use backend endpoint"), 2026-03-16 (`v1.10`) — the deviation record and its backlog reference were simply never updated to reflect that the fix had already shipped, which is what `BLG-FE-155`'s re-triage (2026-08-11) and this story (ST-10) close out. No further code change was required or made by ST-10.
**Owner:** Head of Engineering + Base44 Frontend Prompt Owner
**Backlog reference:** `BLG-FE-155` — resolution recorded here 2026-08-11; ready for archival at next `groom backlog` run.

---

## Change Log

| Version | Date | Change |
| --- | --- | --- |
| 2.1 | 2026-08-11 | v8.6 design gate (ST-01, EPIC-01, BLG-FEAT-32): §21 Trade Plan Completion Rate added — 3 summary cards (plans_created, completion_rate, plans_abandoned) + optional PT-04 quality-tier breakdown table. API Dependency updated with `GET /analytics/trade-plan-completion-rate`. Component Rendering Order updated to 21 items. Design source: trade-plan-completion-rate-metric/decision_record.md. Approved: Product Owner 2026-08-11. Head of Specs Team confirmed. |
| 2.0 | 2026-07-08 | v6.8 design gate — §14a Trade Plan Tag Filter added (ST-05, BLG-FEAT-52): multi-select filter on `trade_plans.trade_tags` (independent from §14's existing position/journal `tags` field), dismissible pills, OR logic; comparison row (win rate + avg R per selected tag) via new `GET /analytics/tag-performance?tags={csv}` endpoint; existing §14 table unaffected. API Dependency updated. Design source: trade-tagging/ux_spec.md. Approved: Product Owner 2026-07-08. Head of Specs Team confirmed. |
| 1.9 | 2026-05-30 | v4.6 design gate (ST-06/ST-07, EPIC-02): §20 Behavioural Drift section added — 4 drift metric cards (entry timing, sizing adherence, post-loss sizing, regime adherence); Option B Percentage Deviation Display; 5 states (loading, insufficient_data, no_drift, drift_detected, error); collapse/expand with localStorage persistence; §13 advisory-only constraints enforced. API Dependency updated with `GET /analytics/behavioural-drift`. Component Rendering Order updated to 20 items. Purpose & User Goals updated. Design source: `docs/specs/si02/si02_fe_component_predesign.md` v1.0 + `docs/specs/si02/si02_fe_interaction_spec.md` v1.0. Approved: Head of UX & Design + Product Owner 2026-05-30. Head of Specs Team confirmed compliant. Nav decision: drift panel integrates as §20 section within PerformanceAnalytics (no new sidebar nav item; consistent with §19 Arc 5 Signal Compliance pattern; ST-11 Arc 5 nav cohesion review to validate in Sprint 2). |
| 1.8 | 2026-05-23 | v4.0 design gate (ST-02/ST-04, EPIC-01): §19 Arc 5 Signal Compliance section added — 4 stat cards (events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate). API Dependency updated with `GET /analytics/arc5-compliance`. Component Rendering Order updated to 19 items. Design source: docs/design/2026-05-22__release-v4.0/arc5-analytics-metrics/ux_spec.md. Approved: Head of UX & Design + Product Owner 2026-05-23. Head of Specs Team confirmed compliant. |
| 1.7 | 2026-04-17 | v2.8 design gate (ST-01, EPIC-01): §18 Market Correlation section added — portfolio-level weighted average card + per-position Pearson correlation table. Severity scheme: high=Rose-500, moderate=Amber-500, low=Emerald-500, null=Slate-500. Sort: severity descending. API Dependency updated with `GET /analytics/market-correlation`. Component Rendering Order updated to 18 items. Design source: docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md. Head of Specs Team confirmed compliant. |
| 1.6 | 2026-03-24 | ST-02 (BLG-FEAT-09, v2.3): §Metrics Staleness Indicator — "data as of" timestamp below page title; amber badge when stale (≥4h default); hover shows absolute ISO timestamp. Design source: docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md. Approved: Product Owner 2026-03-24. Design gate: 2026-03-24__release-v2.3. |
| 1.5 | 2026-03-18 | v2.1 chart interactivity (ST-11, CHART-IX): §4 heatmap — tile click drill-down to Monthly Trades modal. §5 equity curve — zoom (scroll/pinch/buttons), pan (click-drag), Reset button. §9 R-Multiple Analysis — hover tooltip per bar (range, count, % of total). Design source: docs/design/2026-03-18__release-v2.1/chart-interactivity/ux_spec.md. Design gate: 2026-03-18__release-v2.1. |
| 1.4 | 2026-03-13 | QA review (v1.9 Sprint 2): File deviation DEV-EPIC02-ST03-01 — CohortAnalysis.js uses client-side computation instead of GET /analytics/cohort. P2. Director of Quality sign-off. |
| 1.3 | 2026-03-06 | v1.9 additions: §15 Cohort Analysis (ST-03), §16 R-Multiple Distribution Backend (ST-04), §17 Discipline & Compliance (ST-01). Updated API Dependency section to list additional endpoints. Updated Purpose & User Goals. Updated Component Rendering Order to items 15–17. Governance header upgraded to Class 1 compliant format. Design sources: docs/design/2026-03-06__release-v1.9/. |
| 1.2 | 2026-02-26 | F-02 fix: correct Win Rate by Month tooltip field name from `total_trades` to `trade_count` to match `analytics_endpoints.md` monthly_data schema. QA finding A-QA-01. |
| 1.1 | 2026-02-25 | BLG-FEAT-04: Add Best / Worst Trades component spec (R-multiple ranking, top 3 / bottom 3, trades_for_charts source). BLG-FEAT-05: Add Win Rate by Month bar chart spec (monthly_data source, 50% reference line, colour-coded bars). Components inserted at positions 11 and 12 in rendering order. QWB D3. |
| 1.0 | 2026-02-18 | Initial version. |
