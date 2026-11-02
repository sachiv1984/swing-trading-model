**Owner:** Metrics Definitions & Analytics Canonical Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-02 (created — ST-50, EPIC-07, v9.14, BLG-GOV-184)
**Cycle:** 2026-10-29__release-v9.14 (EPIC-07, ST-50)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Canonical definition:** `docs/specs/metrics_definitions.md` §Win Rate — `win_rate = (count(pnl > 0) / total_trades) × 100`, 0.0 when there are no trades, tolerance ±0.5 percentage points

---

# Win Rate — Surface Consistency Check

## Purpose

`BLG-GOV-184` asked whether every surface that shows a win rate computes it the same way. This record lists each surface found, compares its computation with the canonical definition, and names the backlog item for each discrepancy. It fixes nothing: discrepancies are filed, not corrected here.

## Method

1. `grep -rniE 'win.?rate|winRate|win_rate'` over `backend/` (excluding tests and the virtualenv) and `src/`, on `main` at `0f7ba5e6` plus this branch, 2026-11-02.
2. For each hit that computes a value (not one that only displays an API field), read the numerator, the denominator, the population of trades it runs over, and the value it returns for no trades.
3. Compare with the canonical definition. A difference only in rounding that stays within ±0.5 points, or a field documented under a different name or scale, is recorded as a documented variation, not a discrepancy.

The four surfaces named in the item map to the code as follows: dashboard → Dashboard widgets (`src/components/dashboard/widgets/StatsWidgets.js`, `src/components/charts/WinRateChart.js`); P&L report → `backend/services/reports_service.py`; drift analytics → `GET /analytics/strategy-version-comparison` (`backend/database.py`) and the Performance Analytics consistency panel; journal → no journal surface shows a win rate (the journal summary prompt in `ai_service.py` does not compute one). The grep found nine further surfaces, listed below.

## Results

| # | Surface | Code | Population | Win test | Empty case | Result |
|---|---------|------|-----------|----------|-----------|--------|
| 1 | Analytics summary, `GET /analytics/metrics` | `analytics_service.py` (overall, market comparison, exit reasons, monthly, holding periods, cohorts) | Closed trades (`trade_history`) in the period | `pnl > 0` | 0.0 | Consistent |
| 2 | Trade history statistics, `GET /trades` summary | `trade_service.py` `get_trade_history_with_stats()` | Closed trades | `pnl > 0` | 0 | Consistent |
| 3 | P&L report (tax-year summary, PDF and CSV export) | `reports_service.py` | Closed trades in the tax year | `realised_pnl_gbp > 0` (= `pnl`, rounded to 2 dp) | 0.0 | Consistent |
| 4 | Tag performance, `GET /analytics/tag-performance` | `database.py` tag bucket query | Closed trades with that tag and a determinable R | `pnl > 0` (NULL counted as a loss) | 0.0 | Consistent (population is the tag's R-determinable trades, as its contract states) |
| 5 | Setup quality score, `GET /trade-plans/setup-quality-score` | `routers/trade_plans.py` | Closed trades for the setup type, at or above the minimum | `pnl > 0` | gate response, no rate | Consistent |
| 6 | Drift analytics: strategy version comparison | `database.py` `_fetch` for `GET /analytics/strategy-version-comparison`; `StrategyBenchmark.js` multiplies by 100 | Closed trades in the version window | `pnl > 0` | `None` | Documented variation in scale (0.0–1.0, contract `analytics_endpoints.md`) and empty case. **Discrepancy in wording:** the contract defines it as "closed positive (R > 0)", the code uses `pnl > 0` — see `BLG-SPEC-212` |
| 7 | Replay, `POST /replay` | `replay_service.py` `win_rate_pct` | Replayed trades | simulated win flag | `None` | Documented variation: a simulated population under a separately named field |
| 8 | Strategy benchmark (backtest import) | `database.py` `backtest_trades` SQL `win_rate_pct` | Imported backtest trades | `was_profitable` flag | `NULL` | Documented variation: backtest population under a separately named field |
| 9 | Performance Analytics page (headline, monthly, market, exit reason, day/holding buckets, consistency) | `src/pages/PerformanceAnalytics.js` | Closed trades in the selected period | `pnl > 0` | 0 | Consistent. Some cards round with `toFixed(0)`, which stays within ±0.5 points |
| 10 | Tag performance card | `src/components/analytics/TagPerformance.js` | Closed trades with that tag | `pnl > 0` | n/a (tags with trades only) | Consistent |
| 11 | **Trade History page summary** | `src/pages/TradeHistory.js` (`winningTrades = filteredTrades.filter((t) => t.pnl >= 0)`) | Closed trades after the page filters | **`pnl >= 0`** | 0 | **Discrepancy:** a break-even trade counts as a win, so the page's win rate is higher than the canonical one whenever a filtered trade has `pnl = 0` (also moves avg win). See `BLG-FE-239` |
| 12 | **Dashboard Win Rate widget** | `StatsWidgets.js` `WinRateWidget` with `closedPositions` from `Dashboard.js` | `/positions` rows with `status = "closed"` | `pnl > 0` | 0 | **Discrepancy:** `GET /positions` returns open positions only, so `closedPositions` is always empty and the widget always shows 0%. See `BLG-FE-240` |
| 13 | **Dashboard Win Rate chart widget** | `WinRateChart.js`, rendered as `<WinRateChart trades={closedPositions} />` | as #12 | none | none | **Discrepancy:** the component reads `winRate`, `wins` and `losses` props, but the Dashboard passes only `trades`, so it renders from undefined values. See `BLG-FE-240` |
| — | Journal | — | — | — | — | No win rate shown or computed |

Display-only consumers of the fields above (Monthly heatmap, Win Rate by Month, Market comparison, Cohort analysis, Key insights, Export modal, Reports page) render the API value they are given and add no computation of their own.

## Findings

- 10 of 13 computing surfaces match the canonical definition, or differ only in a documented name, scale or population.
- 3 discrepancies, all on frontend surfaces that compute their own rate rather than reading an API field:
  - `BLG-FE-239` — Trade History counts `pnl = 0` as a win.
  - `BLG-FE-240` — both Dashboard win-rate widgets are fed from open positions, so they cannot show a real win rate.
- 1 contract wording gap: `BLG-SPEC-212` — the strategy-version-comparison contract defines `win_rate` by R, the code by P&L.

## Owner Review

**Metrics Definitions & Analytics Canonical Owner — 2026-11-02** (Sprint Execution Engine, agent-mediated in that role per `execution_prompt.md` §5.3). Each row was checked against the code cited. The canonical definition stands unchanged; the discrepancies are correctness defects in the surfaces, not in `metrics_definitions.md`. Outcome: **Recorded; discrepancies filed.**
