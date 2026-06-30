**Filed by:** Base44 Frontend Prompt Owner
**Feature slug:** strategy-benchmark
**Version:** v1
**Story:** ST-11 (BLG-FEAT-53, EPIC-03, v6.3)
**Filed:** 2026-06-30
**Integration status:** Implemented directly (agent-mediated — no Base44 platform submission)

---

# Base44 Prompt — Strategy Benchmark Page

## Context

New page: `src/pages/StrategyBenchmark.js`

The Strategy Benchmark page enables comparison of live trading performance against production_strategy.py backtest results. Data flows: CSV files in `production_results/` → `import_backtest.py` → `POST /strategy/benchmark/import` → database → `GET /strategy/benchmark/summary` + `GET /strategy/benchmark/trades` → this page.

**API client calls:**
- `api.strategyBenchmark.getSummary({ year, market })` → GET /strategy/benchmark/summary
- `api.strategyBenchmark.getTrades({ year, market })` → GET /strategy/benchmark/trades

**Summary response shape:**
```json
{
  "filters": { "year": null, "market": "ALL" },
  "last_imported_at": "2026-06-30T10:15:00Z",
  "available_years": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
  "backtest_stats": { "total_trades": 147, "win_rate_pct": 57.8, "avg_pnl_gbp": 185.0, "total_pnl_gbp": 27195.0, "avg_hold_days": 18.5 },
  "actual_stats": null,
  "yearly_breakdown": [{ "entry_year": 2018, "num_trades": 2, "avg_pnl_gbp": -163.04, "total_pnl_gbp": -326.08, "avg_hold_days": 4.0, "win_rate_pct": 50.0 }]
}
```

`actual_stats` is `null` when no live trades match the filter — display "—" for all actual stat fields (AC-03).

**Trades response shape:**
```json
{
  "filters": { "year": null, "market": "ALL" },
  "backtest_trades": [{ "ticker": "NVDA", "entry_date": "2023-02-28", "exit_date": "2023-03-20", "holding_days": 20, "pnl_gbp": 425.30, "pnl_pct": 14.33, "market": "US", "exit_reason": "Stop", "was_profitable": true, "entry_year": 2023 }],
  "actual_trades": [...]
}
```

## Task

Create `src/pages/StrategyBenchmark.js` with three panels:

**Panel 1 — Performance Parity** (stat cards):
- 5 stat cards in a responsive grid: Total Trades, Win Rate, Avg P&L, Total P&L, Avg Hold
- Each card shows backtest value (top) and actual value (bottom)
- "—" when actual_stats is null
- "Last updated {date}" from last_imported_at

**Panel 2 — Yearly Breakdown** (table):
- Columns: Year, Trades, Win Rate, Avg P&L, Total P&L, Avg Hold
- Rows sorted by year ascending
- Covers all years in backtest data (2018–present)

**Panel 3 — Trade Log** (toggle table):
- Three toggle mode buttons: "Backtest Only", "Actual Only", "Side by Side"
- Default: Backtest Only
- Side by Side merges both lists sorted by entry_date, with source badges (BT / Live)
- Columns: Ticker, Entry Date, Exit Date, Hold, Exit Reason (badge), P&L (£), P&L %

**Exit reason badge mapping:**
| Value | Label | Colour |
|-------|-------|--------|
| "Stop" / "trailing_stop" | Stop | Red (bg-red-600) |
| "Risk-Off" / "risk_off" | Risk-Off | Amber (bg-amber-600) |
| "Rebalance" / "exit_rebalance" | Rebalance | Teal (bg-teal-600) |

**Sticky filters bar** (top of page, z-10, bg-slate-900/95 backdrop-blur):
- Year filter: dropdown with "All Years" + each year from available_years
- Market filter: three pill buttons (ALL / US / UK)
- Changing either filter re-fetches both endpoints

**Navigation (already wired):**
- Registered in `src/pages.config.js` as "StrategyBenchmark"
- Added to Analytics nav group in `src/Layout.js` with BarChart2 icon

## Acceptance criteria checklist

- [ ] AC-01: Page accessible from main navigation (Layout.js Analytics group → "Strategy Benchmark")
- [ ] AC-02: Year filter + market filter apply to all three panels simultaneously
- [ ] AC-03: Panel 1 shows "—" for all actual fields when actual_stats is null
- [ ] AC-04: Panel 2 yearly breakdown covers all years in backtest data
- [ ] AC-05: Panel 3 supports three toggle modes with correct exit reason badges
- [ ] AC-06: Backend POST /strategy/benchmark/import endpoint working (backend-only AC)
- [ ] AC-07: import_backtest.py runnable with `python import_backtest.py` (backend-only AC)
- [ ] AC-08: API endpoints in openapi.yaml and docs/specs/api_contracts/ (backend-only AC)
- [ ] AC-09: New routes registered in backend/routers/test.py (backend-only AC)

## Data-testid attributes

- `strategy-benchmark-page` — page wrapper
- `benchmark-filters` — sticky filters bar
- `benchmark-year-filter` — year dropdown
- `benchmark-market-{all|us|uk}` — market pill buttons
- `benchmark-refresh-btn` — refresh button
- `benchmark-loading` — loading skeleton
- `benchmark-error` — error message
- `benchmark-panel-1` — Panel 1 section
- `benchmark-stat-cards` — stat cards grid
- `benchmark-no-data` — empty state when no backtest data imported
- `benchmark-panel-2` — Panel 2 section
- `benchmark-yearly-table` — yearly breakdown table
- `benchmark-year-row-{year}` — individual year row
- `benchmark-panel-3` — Panel 3 section
- `benchmark-toggle-modes` — toggle mode button group
- `benchmark-mode-{backtest|actual|side-by-side}` — individual toggle buttons
- `benchmark-trade-table` — trade log table
- `benchmark-trades-empty` — empty state for trade log
