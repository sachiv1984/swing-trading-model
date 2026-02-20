# Product Changelog — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-02-20

> This document is a human-maintained record of what was shipped in each product version and when. It records delivery milestones and notable decisions. It is not an immutable system record — for point-in-time system status reports, see `docs/operations/status_reports/`.

---

## v1.6 — Position Sizing Calculator (February 2026)

### Position Sizing Calculator ✅ Complete

**Backend**
- New endpoint: `POST /portfolio/size` — calculates suggested share count from entry price, stop price, and risk percentage
- All sizing calculations are server-side and authoritative; frontend performs no financial calculations
- Three response shapes: valid with sufficient cash, valid with insufficient cash (`max_affordable_shares` always present), invalid inputs (`reason` machine-readable code)
- Reason codes: `INVALID_RISK_PERCENT`, `INVALID_ENTRY_PRICE`, `INVALID_STOP_PRICE`, `INVALID_STOP_DISTANCE`, `NO_PORTFOLIO_VALUE_SNAPSHOT`
- HTTP 400 for malformed requests; HTTP 200 with `valid: false` for all business rule failures
- FX handling: UK positions `fx_rate_used: 1.0`; US positions use live rate or explicit user override
- `suggested_shares` floored to 4dp (conservative — never rounds up)
- `default_risk_percent` field added to `settings` table via safe migration (`NOT NULL DEFAULT 1.00`; existing rows receive `1.00` automatically)
- `GET /settings` and `PUT /settings` updated to expose and accept `default_risk_percent`
- `PUT /settings` rejects `default_risk_percent` of 0 or below, or above 100 (HTTP 422)

**Frontend**
- Position Sizing Calculator widget embedded in Trade Entry form, directly above the Shares field — always visible, no toggle or activation required
- Risk % field pre-populated from `settings.default_risk_percent` on form load
- Debounced live calculation: `POST /portfolio/size` called 300ms after user stops typing in Entry Price, Stop Price, FX Rate, or Risk %
- Eight widget states implemented: idle, loading, valid auto-fill, valid with existing shares, insufficient cash, invalid input (amber), invalid system (grey), post-submit reset
- Auto-fills Shares field when `valid: true`, `cash_sufficient: true`, and Shares is empty
- "Use suggested shares" affordance shown when Shares field already has a user-entered value
- `max_affordable_shares` shown as muted informational text when `cash_sufficient: false` — shares not auto-filled
- Plain-language amber messages for user input errors; muted grey for system conditions; raw reason codes never shown in UI
- Form submission not blocked by any widget state — widget is decision support only
- Network failure: dashes shown, form remains submittable, retries on next keystroke
- Risk % persists across navigation within the session via `sessionStorage`; cleared on tab close
- `default_risk_percent` field added to Settings page, Strategy Parameters section, with helper text clarifying it is a convenience default not an enforced limit

**Defects resolved during verification**
- DEF-002 — INVALID_ENTRY_PRICE amber message not rendered (root cause: missing key in AMBER_MESSAGES map + null coercion in parent TradeEntry.js)
- DEF-003 — INVALID_STOP_PRICE amber message not rendered (same root cause as DEF-002)
- DEF-004 — Settings page silently swallowed invalid save (root cause: missing onError handler in saveMutation)
- DEF-006 — Risk % reset to settings default after navigation (root cause: component local state lost on unmount; fixed via sessionStorage persistence)

**Verification**
- Verification report: `docs/product/verification/3.2-position-sizing-calculator-verification.md` (v1.4)
- Director of Quality sign-off: 2026-02-20

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
- 100% test pass rate monitoring established

---

## v1.2 — Exit Flexibility & Backend Refactor (February 2026)

### Exit Features

- Partial exit support: specify share count to exit
- Custom exit date for backdating reconciliation
- User-provided exit price from actual broker execution
- User-provided FX rate for US stocks (from broker statement)
- Exit reason selection dropdown
- Detailed fee breakdown in exit response
- Proportional cost basis calculation for partial exits

### Backend Architecture

- Complete refactor to service layer architecture
- 67% code reduction in `main.py` (1,439 → 470 lines)
- Five service modules: position, portfolio, trade, cash, signal
- Clean separation of concerns: HTTP → Service → Utils → Database
- 100% testable business logic

---

## v1.1 — Cash Management & Portfolio History (early 2026)

- Deposit and withdrawal tracking
- Transaction history
- Accurate P&L accounting incorporating cash flows
- Cash management modal UI
- Daily portfolio snapshots
- Historical performance data
- Performance chart visualisation
- Automated snapshot creation via cron

---

## v1.0 — Initial Release

### Core Trading Features

- Portfolio management
- Manual position entry with fractional share support
- Daily position analysis
- ATR-based trailing stops
- Grace period (10 calendar days, stop calculated but not enforced)
- Market regime detection: SPY / FTSE vs 200-day moving average
- Multi-currency support: USD and GBP
- Live price fetching via Yahoo Finance
- Fee calculation: UK (commission + stamp duty), US (FX fees)

### Dashboard & UI

- Responsive dashboard with draggable widgets
- Portfolio value display
- Open positions summary
- Total P&L tracking
- Cash balance management
- Dark mode UI

### Technical Infrastructure

- PostgreSQL database
- FastAPI backend
- React frontend with TanStack Query
- Real-time FX rate conversion
- Error handling and validation
- Production deployment on Render
- Frontend hosting on GitHub Pages
