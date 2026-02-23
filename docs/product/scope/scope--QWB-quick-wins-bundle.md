# Scope Document — Quick Wins Bundle

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-02-27
**Roadmap item:** Quick Wins Bundle — BLG-FEAT-01, 02, 04, 05, 06, 07
**Target release:** v1.6.1

> ⚠️ Standing Notice: This document describes delivery intent and summarises
> canonical spec decisions for the purposes of implementation. All authoritative
> rules, formulas, field definitions, and constraints live in the canonical
> specifications listed in Section 2. In any conflict between this document and
> those specs, the canonical specs prevail. This document must not be cited as
> canonical intent.

---

## 1. What This Is

The Quick Wins Bundle delivers six small, high-value user-facing improvements to v1.6.1: a current drawdown widget on the dashboard, an R-multiple column in trade history, best/worst trades and win-rate-by-month analytics components, a grace period indicator in the open positions table, and a one-click CSV export of trade history. Each item is self-contained and ships as a direct addition to its target page. There are no new pages, no settings changes, and no data model migrations.

---

## 2. Canonical Specifications (Implementation Source of Truth)

Engineering must implement against these documents at the exact versions listed. This scope document summarises; the specs govern.

| Spec | Version | What it owns for this bundle |
|------|---------|------------------------------|
| `docs/specs/metrics_definitions.md` | v1.5.8 | Current Drawdown formula, failure behaviour, data sources, relationship to days_underwater and progress bar |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.8.2 | `current_drawdown_percent` and `peak_portfolio_value` fields on `GET /portfolio` |
| `docs/specs/api_contracts/position_endpoints.md` | v1.8.3 | `grace_days_remaining` field on `GET /positions` — formula, null rule, day-10 boundary behaviour |
| `docs/specs/api_contracts/trade_endpoints.md` | v1.8.4 | `GET /trades/export/csv` endpoint — headers, 14-column schema, null serialisation, error shape |
| `docs/specs/api_contracts/analytics_endpoints.md` | v1.8.1 | `trades_for_charts` schema (R-multiple source); `monthly_data` schema incl. `trade_count` (win rate chart source) |
| `docs/specs/data_model.md` | v1.7 | No change — all new fields derived at query time, no migration required |
| `docs/specs/frontend/pages/dashboard.md` | v1.1 | Current Drawdown Widget: placement, data sources, three display states, progress bar, no-fallback rule |
| `docs/specs/frontend/pages/trade_history.md` | v1.1 | R-Multiple column: formula, display, null handling, sort; CSV Export Button: placement, trigger, download behaviour |
| `docs/specs/frontend/pages/analytics.md` | v1.2 | Best/Worst Trades component (Component 11); Win Rate by Month chart (Component 12) |
| `docs/specs/frontend/pages/positions.md` | v1.2 | Grace Days Remaining column: display format, null rule, column visibility |
| `docs/specs/api_dependencies.md` | v1.2 | Updated dependency map: Dashboard, Positions, Trade History page dependencies |
| `docs/reference/openapi.yaml` | current | Updated schemas: PortfolioOverview, PositionSummary; new path: GET /trades/export/csv |

---

## 3. Scope

### 3.1 In Scope

**Backend**
- Compute `current_drawdown_percent` and `peak_portfolio_value` server-side and expose via `GET /portfolio` (no data model change — derived from existing `portfolio_history` records at query time)
- Compute `grace_days_remaining` server-side and expose via `GET /positions` (derived from existing `holding_days` and `grace_period` fields at query time; `null` when `grace_period = false`)
- Implement `GET /trades/export/csv` returning full closed trade history as `text/csv` attachment with exactly 14 columns in canonical order, null serialisation as empty string, `Content-Disposition: attachment; filename="trade_history.csv"`

**Frontend**
- Dashboard: add Current Drawdown Widget to stats row — three display states (normal, at-peak "New Peak!", no-history), progress bar sourced from `max_drawdown.percent` via `GET /analytics/metrics`, days_underwater from `advanced_metrics.days_underwater`, no fallback logic
- Trade History: add R-Multiple column — frontend-only derivation from `trades_for_charts`, display to 2 decimal places with sign, dash for null/uncalculable, sort with dash rows at end
- Trade History: add CSV Export button — triggers `GET /trades/export/csv`, browser-native download, server-side only (no client-side CSV generation)
- Analytics: add Best/Worst Trades component (Component 11) — top 3 / bottom 3 by R-multiple from `trades_for_charts`, positioned below Top Performers
- Analytics: add Win Rate by Month chart (Component 12) — bar chart from `monthly_data`, fixed 0–100% Y-axis, 50% reference line, colour-coded bars, tooltip includes `trade_count`
- Positions: add Grace Days Remaining column to Table View — display `"Day {holding_days + 1} of 10"` when integer, dash when null, column always present

### 3.2 Out of Scope

See Section 9 for the full out-of-scope confirmation table.

---

## 4. Calculation Summary

**Current Drawdown** (canonical: `metrics_definitions.md` v1.5.8, `portfolio_endpoints.md` v1.8.2)
`current_drawdown_percent = (peak_portfolio_value − current_total_value) / peak_portfolio_value × 100`
Result is ≤ 0.0. Zero = portfolio is at or above all-time peak. Both fields default to `0.0` when no `portfolio_history` records exist.

**Grace Days Remaining** (canonical: `position_endpoints.md` v1.8.3)
`grace_days_remaining = max(0, 10 − holding_days)` when `grace_period = true`; `null` when `grace_period = false`. On day 10, `grace_period` is `false` → field returns `null`, not `0`. Display: `"Day {holding_days + 1} of 10"` (e.g. `holding_days = 3` → "Day 4 of 10").

**R-Multiple** (canonical: `metrics_definitions.md` v1.5.8)
`R = (exit_price − entry_price) / (entry_price − stop_price)`
Frontend-only calculation. Source data: `trades_for_charts` from `GET /analytics/metrics`. Null when `stop_price` is absent or `entry_price = stop_price`.

**Win Rate by Month** (canonical: `analytics.md` v1.2)
Bar height = `win_rate` (%) per month from `monthly_data`. Tooltip includes `trade_count` for context. Empty state shown when fewer than 2 months of data available.

---

## 5. API Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/portfolio` | Modified — adds `current_drawdown_percent` (float, ≤ 0.0) and `peak_portfolio_value` (float) to existing response. Both fields always present. |
| `GET` | `/positions` | Modified — adds `grace_days_remaining` (integer \| null) to each position object. Always present on every object. |
| `GET` | `/trades/export/csv` | New — returns full closed trade history as `text/csv` attachment. 14 columns. No parameters in v1.6.1. |
| `GET` | `/analytics/metrics` | Unchanged — existing `trades_for_charts` and `monthly_data` fields consumed as-is. |

---

## 6. Acceptance Criteria

Derived from canonical specs per QA review — QA & Testing Owner, 2026-02-27. Full test scenarios at `docs/testing/QWB-quick-wins-bundle-test-scenarios.md` v1.0.

**Backend**

- B-01: `GET /portfolio` returns both `current_drawdown_percent` and `peak_portfolio_value` on every response, with correct types and always-present behaviour
- B-02: `current_drawdown_percent` matches `(total_value − peak_portfolio_value) / peak_portfolio_value × 100` within floating-point tolerance; `peak_portfolio_value` equals `MAX(portfolio_history.total_value)` all-time
- B-03: Both fields return `0.0` (not null, not absent) when no `portfolio_history` records exist
- B-04: `GET /positions` returns `grace_days_remaining` on every position object regardless of grace state
- B-05: `grace_days_remaining` equals `max(0, 10 − holding_days)` when `grace_period = true`
- B-06: `grace_days_remaining` is `null` (not `0`, not absent) when `grace_period = false`, including at `holding_days = 10`
- B-07: `grace_days_remaining` key is always present — never omitted from the response object
- B-08: `GET /trades/export/csv` returns HTTP 200 with `Content-Type: text/csv` and `Content-Disposition: attachment; filename="trade_history.csv"`
- B-09: CSV header row contains exactly 14 columns in canonical order: `ticker, market, entry_date, exit_date, shares, entry_price, exit_price, pnl, pnl_pct, holding_days, exit_reason, tags, entry_note, exit_note`
- B-10: Null fields serialised as empty string, not the string `"null"`
- B-11: Tags serialised as semicolon-separated string within the single `tags` column
- B-12: CSV returned as a single string — no streaming or chunked response behaviour required
- B-13: Empty trade history returns header row only (no data rows), not a 404 or empty body

**Frontend**

- F-01: Current Drawdown Widget present in Dashboard stats row
- F-02: Widget displays `current_drawdown_percent` with correct sign and format (e.g. "−8.2%")
- F-03: Widget displays `peak_portfolio_value` in GBP format
- F-04: Progress bar present, sourced from `max_drawdown.percent` via `GET /analytics/metrics`
- F-05: `days_underwater` displayed, sourced from `advanced_metrics.days_underwater`
- F-06: "New Peak!" at-peak display state shown when `current_drawdown_percent = 0.0`
- F-07: No-history display state shown when `peak_portfolio_value = 0.0`; no fallback calculation attempted
- F-08: R-Multiple column present in Trade History table
- F-09: R-Multiple displays to 2 decimal places with sign (e.g. "+2.34R", "−1.50R")
- F-10: Null/uncalculable R-multiple displays dash (—)
- F-11: R-Multiple column is sortable; dash rows appear at end in both ascending and descending sort
- F-12: R-Multiple is frontend-only — no additional API call made to retrieve it
- F-13: Grace Days Remaining column present in Open Positions Table View
- F-14: Column displays `"Day {holding_days + 1} of 10"` when `grace_days_remaining` is an integer
- F-15: Column displays dash or empty when `grace_days_remaining` is null; never displays "Day 0 of 10", "0", or "null"
- F-16: Best/Worst Trades component present on Analytics page, positioned below Top Performers
- F-17: Component shows top 3 trades by R-multiple (highest) and bottom 3 (lowest)
- F-18: Trades with null R-multiple excluded from ranking
- F-19: Each card shows ticker, R-multiple, P&L, and entry date
- F-20: Positive R-multiple cards styled with positive colour; negative with negative colour
- F-21: Empty state displayed when fewer than 1 completed trade exists
- F-22: Partial state displayed (e.g. top 2, bottom 2) when fewer than 3 qualifying trades on either side
- F-23: Win Rate by Month chart present on Analytics page
- F-24: Chart displays as bar chart grouped by calendar month
- F-25: Y-axis fixed at 0–100%
- F-26: 50% reference line present
- F-27: Bars colour-coded (above/below 50%); tooltip includes `trade_count`
- F-28: CSV Export button present in Trade History page header area
- F-29: Clicking CSV Export button triggers `GET /trades/export/csv` and initiates browser-native file download; no client-side CSV generation

---

## 7. Effort Estimate

**~8–10.5 hours.** Revised from the original roadmap estimate of ~6–8 hours to account for spec authoring overhead across 9 documents confirmed during pre-alignment. All spec work is now complete — implementation estimate is the full remaining figure.

---

## 8. Pre-Implementation Checklist

All items confirmed complete before this document was written:

- [x] `docs/specs/metrics_definitions.md` updated (v1.5.8) — Current Drawdown section added
- [x] `docs/specs/api_contracts/portfolio_endpoints.md` updated (v1.8.2) — drawdown fields added
- [x] `docs/specs/api_contracts/position_endpoints.md` updated (v1.8.3) — `grace_days_remaining` added; day-10 contradiction corrected (A-QA-05)
- [x] `docs/specs/api_contracts/trade_endpoints.md` updated (v1.8.4) — `GET /trades/export/csv` added
- [x] `docs/specs/api_contracts/analytics_endpoints.md` confirmed (v1.8.1) — no change required; existing fields consumed
- [x] `docs/specs/data_model.md` confirmed (v1.7) — no migration required; all new fields derived at query time
- [x] `docs/specs/frontend/pages/dashboard.md` updated (v1.1) — Current Drawdown Widget section added
- [x] `docs/specs/frontend/pages/trade_history.md` updated (v1.1) — R-Multiple column and CSV Export Button sections added
- [x] `docs/specs/frontend/pages/analytics.md` updated (v1.2) — Best/Worst Trades and Win Rate by Month sections added
- [x] `docs/specs/frontend/pages/positions.md` updated (v1.2) — Grace Days Remaining column section added; A-QA-04 confirmed
- [x] `docs/specs/api_dependencies.md` updated (v1.2) — new dependencies added for Dashboard, Positions, Trade History
- [x] `docs/reference/openapi.yaml` updated — PortfolioOverview, PositionSummary schemas and `GET /trades/export/csv` path added (same PR as API contract changes)
- [x] Decisions record committed (`docs/product/decisions/QWB-quick-wins-bundle.md`) — 13 decisions closed, zero deferrals
- [x] QA review complete — all acceptance criteria confirmed derivable — QA & Testing Owner, 2026-02-27
- [x] Test scenarios document committed (`docs/testing/QWB-quick-wins-bundle-test-scenarios.md` v1.0) — 42 scenarios, 100% coverage confirmed

---

## 9. Out of Scope Confirmation

| Item | Decision |
|------|----------|
| Server-side R-multiple calculation | D2 — frontend-only per `metrics_definitions.md` v1.5.8 classification (Tier 1 — Visualisation-Only). No API change required. |
| `stop_price` in `GET /trades` direct response | D2a — field absent from `GET /trades`; sourced from `trades_for_charts` in `GET /analytics/metrics`. No contract change. |
| BLG-TECH-06 (unspecified tech item) | D6 — explicitly deferred; separate delivery required outside this bundle. |
| Customisable Dashboard Layout / WidgetLibrary | D11 — roadmap deferral stands. Prototype `WidgetLibrary.jsx` discarded. Each item ships as a direct, fixed addition to its target page. |
| Date range filtering on CSV export | D5 — v1.6.1 scope note in `trade_endpoints.md` v1.8.4. Full history only. Filtering is a planned future enhancement. |
| Fallback / derived drawdown when `portfolio_history` empty | D10 — no fallback. `GET /portfolio` always returns both fields; `0.0` sentinel value used when no history exists. |
| Colour thresholds for drawdown widget | D9 — implementation detail. Engineering owns. Not spec-governed for v1.6.1. |
| "New Peak!" display text and emoji styling | D12 — implementation detail. Frontend Spec owner governs visual consistency. |
| Column sorting for Grace Days Remaining | `positions.md` v1.2 — sorting not required for v1.6.1. Informational column only. |
| Partial CSV export (date filter, ticker filter) | Out of scope — v1.6.1 delivers full history only per D5. |
