# Product Changelog — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-01

> This document is a human-maintained record of what was shipped in each product version and when. It records delivery milestones and notable decisions. It is not an immutable system record — for point-in-time system status reports, see `docs/operations/status_reports/`.

---

## v1.6.1 — Quick Wins Bundle (March 2026)

**Shipped:** 2026-03-01
**Director of Quality sign-off:** 2026-03-01
**Verification report:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0
**Scope document:** `docs/product/scope/scope--QWB-quick-wins-bundle.md` (Superseded)

Six self-contained user-facing improvements. No new pages. No data model migrations.

---

### BLG-FEAT-01 — Current Drawdown Widget ✅ Complete

**Backend**
- `GET /portfolio` extended with two always-present fields: `current_drawdown_percent` (float, ≤ 0.0) and `peak_portfolio_value` (float, GBP)
- Calculated server-side: `(peak − current) / peak × 100`. Peak = `MAX(portfolio_history.total_value)` all-time. Both default to `0.0` when no `portfolio_history` exists
- Spec: `portfolio_endpoints.md` v1.8.2

**Frontend — Dashboard**
- Current Drawdown Widget added as fifth card in stats row
- Three display states: in-drawdown (% + peak equity + days underwater + progress bar), at-peak ("New Peak!"), no-history
- Progress bar sourced from `max_drawdown.percent` via `GET /analytics/metrics`. `days_underwater` sourced from `advanced_metrics.days_underwater` — no fallback calculation
- Spec: `dashboard.md` v1.1

---

### BLG-FEAT-02 — R-Multiple Column in Trade History ✅ Complete

**Frontend — Trade History**
- R-multiple column added to trade history table
- Frontend-only calculation: `R = (exit_price − entry_price) / (entry_price − stop_price)`. Source: `trades_for_charts` from `GET /analytics/metrics`, joined by trade `id`
- Display: signed, 2dp, R suffix (e.g. `+2.31R`, `−0.54R`). Em dash when `stop_price` absent or denominator is zero
- Column sortable; em-dash rows sort to end
- Spec: `trade_history.md` v1.1, `metrics_definitions.md` v1.5.8

---

### BLG-FEAT-04 — Best / Worst Trades Widget ✅ Complete

**Frontend — Performance Analytics**
- Best/Worst Trades component added below Top Performers on Performance Analytics page
- Two panels: top 3 and bottom 3 closed trades by R-multiple. Trades without `stop_price` excluded from ranking
- Partial panels when fewer than 3 qualifying trades; empty state when none
- Card content: ticker, R-multiple, P&L (GBP), exit date, exit reason
- Spec: `analytics.md` v1.2

---

### BLG-FEAT-05 — Win Rate by Month Chart ✅ Complete

**Frontend — Performance Analytics**
- Win Rate by Month bar chart added below Best/Worst Trades
- Source: `monthly_data` from `GET /analytics/metrics`
- Y-axis fixed 0–100. Bars green when `win_rate > 50%`, red at or below 50%. Dashed reference line at 50%
- Tooltip shows month, win rate %, and `trade_count`
- Returns null (no render) when `monthly_data` is empty
- Spec: `analytics.md` v1.2

---

### BLG-FEAT-06 — Grace Period Indicator ✅ Complete

**Backend**
- `GET /positions` extended with `grace_days_remaining` (integer | null) on every position object. Always present
- Formula: `max(0, 10 − holding_days)` when `grace_period = true`; `null` when `grace_period = false`. On day 10, `grace_period` becomes `false` → field returns `null`, not `0`
- Spec: `position_endpoints.md` v1.8.3

**Frontend — Positions**
- Grace Days Remaining column added to open positions table
- Display: `"Day {holding_days + 1} of 10"` when in grace; dash (`—`) when `null`
- Spec: `positions.md` v1.2

---

### BLG-FEAT-07 — CSV Export of Trade History ✅ Complete

**Backend**
- New endpoint: `GET /trades/export/csv`
- `Content-Type: text/csv`, `Content-Disposition: attachment; filename="trade_history.csv"`
- 14 columns: `ticker, market, entry_date, exit_date, shares, entry_price, exit_price, pnl, pnl_pct, holding_days, exit_reason, tags, entry_note, exit_note`
- Null fields → empty string. Tags array → semicolon-separated string. Empty history → header row only (HTTP 200)
- Spec: `trade_endpoints.md` v1.8.4

**Frontend — Trade History**
- CSV Export button added to Trade History page; triggers browser-native download
- Spec: `trade_history.md` v1.1

---

### Canonical Specs Updated

| Spec | Version | Change |
|------|---------|--------|
| `docs/specs/metrics_definitions.md` | v1.5.8 | New section: Current Drawdown |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.8.2 | New fields: `current_drawdown_percent`, `peak_portfolio_value` |
| `docs/specs/api_contracts/position_endpoints.md` | v1.8.3 | New field: `grace_days_remaining`; A-QA-05 day-10 contradiction corrected |
| `docs/specs/api_contracts/trade_endpoints.md` | v1.8.4 | New endpoint: `GET /trades/export/csv` |
| `docs/specs/frontend/pages/dashboard.md` | v1.1 | Current Drawdown Widget added |
| `docs/specs/frontend/pages/trade_history.md` | v1.1 | R-Multiple column + CSV Export button added |
| `docs/specs/frontend/pages/analytics.md` | v1.2 | Best/Worst Trades (§11) + Win Rate by Month (§12) added |
| `docs/specs/frontend/pages/positions.md` | v1.2 | Grace Days Remaining column added |
| `docs/specs/api_dependencies.md` | v1.2 | New dependencies added |

---

### Verification Summary

- **Scenarios:** 47 total — 45 pass, 2 deferred (F-17: data prerequisite; F-27: environment state), 0 fail
- **Defects:** 0 raised at any severity
- **Observations:** 2 pre-existing issues raised for backlog (BLG-TECH-08, BLG-TECH-09)
- **Sign-off:** Director of Quality, 2026-03-01. Verdict: Pass with logged deferrals

---

## v1.6 — Position Sizing Calculator (February 2026)

### Position Sizing Calculator ✅ Complete

**Sign-off:** Director of Quality, 2026-02-20
**Verification report:** `docs/product/verification/3.2-position-sizing-calculator-verification.md` (v1.4)

**Backend**
- `POST /portfolio/size` endpoint — calculates suggested share quantity for a prospective new position. Idempotent. No state mutation. Returns three distinct response shapes: valid result, insufficient cash (with `max_affordable_shares` always present), and invalid inputs (with machine-readable `reason` code)
- `default_risk_percent` field added to `settings` table — supports widget pre-population. Database migration applied; all existing rows default to `1.00`
- `GET /settings` and `PUT /settings` updated to expose and accept `default_risk_percent`

**Frontend**
- Position Sizing Calculator widget — always visible in Trade Entry form, directly above the Shares field
- Risk % field pre-populated from `settings.default_risk_percent` on form load
- Eight widget states implemented: idle, loading, valid auto-fill, valid with existing shares, insufficient cash, invalid input, invalid system, post-submit reset
- Auto-fills Shares field when result is valid and field is empty; "Use suggested shares" affordance shown when Shares already populated
- Debounced API call (300ms) on input change — does not block form submission in any state
- `default_risk_percent` field added to Settings page — Strategy Parameters section

**Canonical specifications updated**
- `strategy_rules.md` v1.3 — §4.1 sizing calculator rules
- `portfolio_endpoints.md` v1.8.0 — `POST /portfolio/size` contract
- `settings_endpoints.md` v1.8.0 — `default_risk_percent` field
- `data_model.md` v1.7 — settings column and migration script
- `position_form.md` v1.2 — widget spec and all eight states
- `settings.md` v1.1 — Strategy Parameters section
- `openapi.yaml` v1.8.0 — aligned with above contract changes

---

### BLG-TECH-01 — Sharpe Variance + Capital Efficiency Fix ✅ Complete

**Closed:** 2026-02-21
**Canonical Owner sign-off:** 2026-02-21
**Validation result:** 13/13 pass at 2026-02-21T00:24:41Z

This item was the v1.6 quality gate. v1.6 did not ship until these fixes were verified.

- `_calculate_sharpe()` updated to use sample variance (÷ n−1) for both portfolio-based and trade-based Sharpe methods
- Capital efficiency updated to use `Mean(total_cost)` in GBP from `trade_history` — eliminates USD/GBP mixing for portfolios with both markets
- `validation_data.py` expected values updated: `capital_efficiency` 0.17 → 0.22; `total_cost` fields added
- Validation metric count increased from 12 to 13 (capital efficiency added as explicitly validated metric)
- `metrics_definitions.md` v1.5.7 — Appendix E Backlog Items 1 and 2 marked resolved with closure detail
- `analytics_endpoints.md` v1.8.1 — resolved known limitations removed; severity contract added (A5/A6 actions completed alongside this closure)

---

## v1.5 — Performance Analytics (February 2026)

### Performance Analytics Page ✅ Complete

**Backend**
- Unified analytics endpoint: `GET /analytics/metrics?period=` (six period options: last 7 days, last month, last quarter, last year, YTD, all time)
- All metrics computed server-side from `trade_history` and `portfolio_history`; frontend performs no calculations
- Period filtering on both trade exit date and portfolio snapshot date
- `has_enough_data` gate: configurable minimum trade threshold (default 10, set via Settings)
- `POST /validate/calculations` endpoint: smoke-tests all metric calculations against a known 5-trade validation dataset with per-metric tolerance checks and CSV export

**Metrics delivered**
- Executive: Sharpe ratio (portfolio-based when 30+ snapshots available, trade-based fallback), max drawdown (percent, amount, date), recovery factor, expectancy per trade, profit factor, risk/reward ratio
- Advanced: win streak, loss streak, average hold time for winners vs losers, trade frequency (per week), capital efficiency, days underwater, portfolio peak equity
- Market comparison: win rate, total P&L, average win/loss, best and worst performer — UK and US independently
- Exit reason analysis: count, win rate, total P&L, average P&L, percentage of trades — per exit reason
- Monthly performance: P&L, trade count, win rate, cumulative — last 12 months
- Day of week: average P&L and trade count per weekday
- Holding period buckets: 1–5, 6–10, 11–20, 21–30, 31+ days — average P&L, count, win rate
- Top 5 winners and top 5 losers by P&L
- Consistency metrics: consecutive profitable months, current streak, win rate standard deviation, P&L standard deviation
- R-multiple analysis and tag performance derived from `trades_for_charts`

**Frontend**
- 12-component page render: executive summary cards, key insights, advanced metrics grid, monthly heatmap, underwater equity chart, market comparison, exit reason table, time-based charts, R-multiple analysis, top performers, consistency metrics, strategy tag performance
- Period selector drives single re-fetch of unified endpoint
- Loading, error, and not-enough-data states
- Key insights: up to 5 generated observations from metric values (Sharpe quality, hold time discipline check, profit factor commentary, expectancy edge, risk/reward)
- PDF export: print-optimised HTML report covering executive summary, key insights, and advanced metrics table
- snake_case → camelCase transformation on API response
- System Status page updated: analytics and validation endpoints categorised and included in automated endpoint testing suite

---

## v1.4 — Trade Journal & Notes System (February 2026)

### Trade Journal & Notes System ✅ Complete

- Entry notes when creating positions (500 character limit)
- Exit notes when closing positions (500 character limit)
- Tag system for categorising trades, with autocomplete from existing tags
- Tag validation: lowercase, hyphens only, up to 10 tags per position
- Tag filtering in trade history (OR logic)
- Expandable trade rows showing full journal entries
- Journal view mode in Positions page
- Visual entry/exit note cards with colour-coded headers
- Strategy tag pills with gradient styling
- Database schema updates: `entry_note`, `exit_note`, `tags` fields on positions and trade history
- GIN indexes on tags fields for fast filtering
- Backend endpoints: updateNote, updateTags, getTags

---

## v1.3 — System Health & Monitoring (February 2026)

- Health check endpoint (`GET /health`) for load balancers
- Detailed system status (`GET /health/detailed`)
- Automated endpoint testing (`POST /test/endpoints`) — 11 endpoints at launch
- Frontend status dashboard page with real-time monitoring
- Component-level health checks: Database, Yahoo Finance, Services, Config
- One-click endpoint testing with pass/fail results
- Auto-refresh at 5-second intervals
- Response time tracking
- 100% test pass rate at launch
