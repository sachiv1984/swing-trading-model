**Owner:** Backend Engineering Patterns Owner; Product Owner
**Class:** API Contract (Class 2)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-08-18 (ST-07, EPIC-02, v8.9, BLG-FEAT-89 — added POST /strategy/backtest-rule-change/run, GET /strategy/backtest-rule-change/runs, GET /strategy/backtest-rule-change/runs/{run_id}); prior — 2026-07-02 (ST-08, EPIC-03, v6.4, BLG-FEAT-54 — open positions panel)
**Story:** ST-07 (BLG-FEAT-89, EPIC-02, v8.9); ST-11 (BLG-FEAT-53, EPIC-03, v6.3); ST-08 (BLG-FEAT-54, EPIC-03, v6.4)

---

# Strategy Benchmark API Contract

Endpoints supporting the Strategy Benchmark page — comparison of live trade performance against production_strategy.py backtest results.

Data flow: `production_strategy.py` → CSV files in `production_results/` → `import_backtest.py` → `POST /strategy/benchmark/import` → `backtest_trades` + `backtest_yearly_performance` + `backtest_open_positions` tables → `GET /strategy/benchmark/summary` / `GET /strategy/benchmark/trades` / `GET /strategy/benchmark/open-positions` → frontend.

All endpoints require `X-API-Key` header authentication.

---

## POST /strategy/benchmark/import

Upserts backtest trade records and yearly performance data parsed from production_strategy.py CSV outputs. Called by `import_backtest.py`. Safe to re-run — all inserts use `ON CONFLICT DO UPDATE`.

**Auth:** X-API-Key required

**Request body (application/json):**

```json
{
  "trades": [
    {
      "ticker": "NVDA",
      "entry_date": "2023-02-28",
      "exit_date": "2023-03-20",
      "holding_days": 20,
      "entry_price": 234.50,
      "exit_price": 268.10,
      "pnl_gbp": 425.30,
      "pnl_pct": 14.33,
      "market": "US",
      "exit_reason": "Stop",
      "was_profitable": true,
      "entry_year": 2023
    }
  ],
  "yearly_performance": [
    {
      "entry_year": 2023,
      "num_trades": 30,
      "avg_pnl_gbp": 180.50,
      "total_pnl_gbp": 5415.00,
      "avg_hold_days": 18.2,
      "win_rate_pct": 56.7
    }
  ]
}
```

**Field notes:**
- `exit_reason`: Raw value from CSV — one of `"Stop"`, `"Risk-Off"`, `"Rebalance"`. Frontend normalises for badge display.
- `market`: `"US"` or `"UK"`. Defaults to `"US"` if absent.
- `trades` and `yearly_performance` may be empty arrays (valid import run with no data).

**Response (200):**

```json
{
  "status": "ok",
  "trades_imported": 147,
  "years_imported": 8,
  "open_positions_imported": 3,
  "trades_deleted": 145,
  "years_deleted": 8,
  "open_positions_deleted": 4,
  "imported_at": "2026-06-30T10:15:00Z",
  "previous_total_pnl_gbp": 111890.12,
  "total_pnl_gbp_delta": 335.88,
  "previous_total_unrealized_pnl_gbp": 412.50
}
```

**Field notes (drift diagnostic):**
- `previous_total_pnl_gbp` / `previous_total_unrealized_pnl_gbp`: the aggregate totals as they stood immediately before this import overwrote them (snapshotted into `backtest_import_history`). `null` on the very first import.
- `total_pnl_gbp_delta`: `new total_pnl_gbp - previous_total_pnl_gbp`. With a stable ticker universe, this should track `previous_total_unrealized_pnl_gbp` (less any exit fees) if the only change was open positions closing — a delta far outside that range warrants investigation rather than being assumed to be normal market movement.

---

## GET /strategy/benchmark/summary

Returns Panel 1 stats (backtest vs live side-by-side) and Panel 2 yearly breakdown. Supports year and market query filters.

**Auth:** X-API-Key required

**Query parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `year` | integer | No | Filter to a specific entry year. Omit for all years. |
| `market` | string | No | `US`, `UK`, or `ALL`. Omit or `ALL` for all markets. |

**Response (200):**

```json
{
  "filters": { "year": 2023, "market": "US" },
  "last_imported_at": "2026-06-30T10:15:00Z",
  "available_years": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
  "backtest_stats": {
    "total_trades": 30,
    "win_rate_pct": 56.7,
    "avg_pnl_gbp": 180.50,
    "total_pnl_gbp": 5415.00,
    "avg_hold_days": 18.2
  },
  "actual_stats": {
    "total_trades": 5,
    "win_rate_pct": 60.0,
    "avg_pnl_gbp": 210.00,
    "total_pnl_gbp": 1050.00,
    "avg_hold_days": 22.0
  },
  "yearly_breakdown": [
    {
      "entry_year": 2023,
      "num_trades": 30,
      "avg_pnl_gbp": 180.50,
      "total_pnl_gbp": 5415.00,
      "avg_hold_days": 18.2,
      "win_rate_pct": 56.7
    }
  ]
}
```

**Null behaviour:**
- `actual_stats`: `null` when no live trades match the active filters. Frontend must display `"—"` for all actual stat fields when `actual_stats` is `null` (AC-03).
- `backtest_stats`: `null` when no backtest data has been imported yet.
- `last_imported_at`: `null` when no import has been run.

---

## GET /strategy/benchmark/trades

Returns Panel 3 trade log data. Returns `backtest_trades` and `actual_trades` separately so the frontend can display the appropriate subset based on the selected toggle mode.

**Auth:** X-API-Key required

**Query parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `year` | integer | No | Filter to a specific entry year. |
| `market` | string | No | `US`, `UK`, or `ALL`. |

**Response (200):**

```json
{
  "filters": { "year": null, "market": "ALL" },
  "backtest_trades": [
    {
      "id": 1,
      "ticker": "NVDA",
      "entry_date": "2023-02-28",
      "exit_date": "2023-03-20",
      "holding_days": 20,
      "entry_price": 234.50,
      "exit_price": 268.10,
      "pnl_gbp": 425.30,
      "pnl_pct": 14.33,
      "market": "US",
      "exit_reason": "Stop",
      "was_profitable": true,
      "entry_year": 2023,
      "imported_at": "2026-06-30T10:15:00Z"
    }
  ],
  "actual_trades": [
    {
      "ticker": "AAPL",
      "entry_date": "2024-03-01",
      "exit_date": "2024-03-22",
      "holding_days": 21,
      "entry_price": 175.40,
      "exit_price": 182.10,
      "pnl_gbp": 312.50,
      "pnl_pct": 3.82,
      "market": "US",
      "exit_reason": "trailing_stop",
      "was_profitable": true,
      "entry_year": 2024
    }
  ]
}
```

**Exit reason badge mapping (frontend responsibility):**

| exit_reason value | Badge label | Badge colour |
|-------------------|-------------|--------------|
| `"Stop"` (backtest) / `"trailing_stop"` (live) | Stop | Red |
| `"Risk-Off"` (backtest) / `"risk_off"` (live) | Risk-Off | Amber |
| `"Rebalance"` (backtest) / `"exit_rebalance"` (live) | Rebalance | Teal |
| Other / null | — | Slate |

**Toggle modes (frontend responsibility):**
- `backtest only`: render `backtest_trades` list; hide `actual_trades`
- `actual only`: render `actual_trades` list; hide `backtest_trades`
- `side-by-side`: render both lists in separate columns or interspersed with source labels

---

## GET /strategy/benchmark/open-positions

Returns Panel 0 open (unrealized) positions. Sourced from `backtest_open_positions`, which is fully replaced (not upserted) on each nightly import, the same pattern as `backtest_trades`. No `year` parameter — open positions are current-state, not historical-per-year data (a position may have been entered in a prior year and remain open today).

**Auth:** X-API-Key required

**Query parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `market` | string | No | `US`, `UK`, or `ALL`. |

**Response (200):**

```json
{
  "filters": { "market": "ALL" },
  "open_positions": [
    {
      "ticker": "MSFT",
      "market": "US",
      "entry_date": "2026-05-12",
      "entry_price": 412.30,
      "current_price": 438.90,
      "unrealized_pnl_gbp": 266.00,
      "unrealized_pnl_pct": 6.45,
      "days_held": 51
    }
  ],
  "summary": {
    "count": 5,
    "total_unrealized_pnl_gbp": 46230.00
  }
}
```

**Null behaviour:** `summary.total_unrealized_pnl_gbp` is `null` when `count` is `0`. Individual position fields (`entry_price`, `current_price`, `unrealized_pnl_gbp`, `unrealized_pnl_pct`) are `null` only if the source CSV row was missing that value at import time.

**Sort order:** Results are ordered by `unrealized_pnl_pct` descending (largest movers first) — not user-sortable in v1.0.

---

## POST /strategy/backtest-rule-change/run

ST-07 (BLG-FEAT-89, EPIC-02, v8.9). Runs a candidate `strategy_rules.md` parameter change against a bounded historical window, entirely in-app (no external script step), and compares it against the live rule set over the identical universe/window. Persists the run for later audit (AC-03).

**Design source:** `docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md`

**Scope note (RISK-02):** the full nightly `production_strategy.py` run covers the entire `ticker_universe` over ~8 years and is budgeted 90 minutes of CI compute (`.github/workflows/backtest.yml`) — infeasible to run synchronously in a web request. This endpoint runs a bounded backtest instead: the first 20 active tickers from `ticker_universe` (alphabetical) over the trailing 4 years. Both the candidate and live-parameter baseline are computed over the identical bounded universe/window in the same run, so the comparison is apples-to-apples; absolute figures will not match the full nightly Benchmark tab (different universe/window by design) — `universe_tickers`/`universe_start_date`/`universe_end_date` in the response make this explicit.

**§13 compliance:** deterministic simulation over historical market data (no ML model, no adaptive inference), applied to a candidate rule set instead of the live one — same category as the existing Benchmark/Version Comparison tabs. Output is comparative statistical context for a human decision; this endpoint never writes to `strategy_rules.md` or any live rule configuration.

**Request body (application/json):** all fields optional — any omitted field falls back to the live `strategy_rules.md` value.

```json
{
  "lookback": 252,
  "top_n": 5,
  "atr_mult": 2,
  "rebalance_freq": "ME",
  "min_position_pct": 0.05,
  "max_position_pct": 0.20,
  "min_hold_days": 15,
  "risk_off_mode": "single",
  "stop_loss_mode": "profit_lock",
  "initial_atr_mult": 5,
  "profit_atr_mult": 2,
  "initiated_by": "Product Owner"
}
```

**Response (200):**

```json
{
  "status": "ok",
  "data": {
    "id": "3f1b2c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
    "created_at": "2026-08-18T10:00:00Z",
    "initiated_by": "Product Owner",
    "rule_diff_summary": "min_hold_days: 10 -> 15",
    "candidate_params": { "lookback": 252, "top_n": 5, "min_hold_days": 15, "...": "..." },
    "live_params": { "lookback": 252, "top_n": 5, "min_hold_days": 10, "...": "..." },
    "universe_tickers": ["AAPL", "ABBV", "..."],
    "universe_start_date": "2022-08-18",
    "universe_end_date": "2026-08-18",
    "candidate_result": {
      "trade_count": 34,
      "win_rate_pct": 58.82,
      "max_drawdown_pct": -14.21,
      "r_multiple_buckets": [
        { "label": "< -3R", "count": 0 },
        { "label": "-3R to -2R", "count": 1 },
        { "label": "-2R to -1R", "count": 3 },
        { "label": "-1R to 0R", "count": 8 },
        { "label": "0R to 1R", "count": 10 },
        { "label": "1R to 2R", "count": 7 },
        { "label": "2R to 3R", "count": 3 },
        { "label": "> 3R", "count": 2 }
      ],
      "median_r": 0.42
    },
    "live_result": { "trade_count": 31, "win_rate_pct": 54.84, "max_drawdown_pct": -15.03, "r_multiple_buckets": ["..."], "median_r": 0.35 }
  }
}
```

**Field notes:**

| Field | Notes |
|-------|-------|
| `rule_diff_summary` | Auto-generated: `"{param}: {live_value} -> {candidate_value}; ..."` for every overridden field, or `"No parameter changes from live rule set"` if none |
| `r_multiple_buckets` | 8 fixed buckets, identical scheme to `GET /analytics/r-multiple-distribution` (`metrics_definitions.md` "R-Multiple Distribution (Backend)") |
| `median_r` / bucket R values | Canonical formula (`metrics_definitions.md` "R-Multiple (Canonical Server-Side)"): `R = (exit_price - entry_price) / (entry_price - initial_stop_price)`. Trades without a qualifying initial stop are excluded, same qualifying conditions as the canonical formula |
| `max_drawdown_pct` | Computed from the run's own equity curve over the bounded window — not comparable in magnitude to the full nightly backtest's Max DD % |

**Errors:**
- `400` Business-rule failure (`BacktestRuleChangeError`): unknown candidate parameter field name, no active tickers in `ticker_universe`, or no usable price data for the bounded universe
- `500` Unexpected server error

---

## GET /strategy/backtest-rule-change/runs

ST-07. Run History — most recent first (AC-03). Summary fields only (no full `r_multiple_buckets` payload, to keep the list response light).

**Query parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max runs to return. Default 20. |

**Response (200):**

```json
{
  "status": "ok",
  "data": [
    {
      "id": "3f1b2c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
      "initiated_by": "Product Owner",
      "rule_diff_summary": "min_hold_days: 10 -> 15",
      "universe_start_date": "2022-08-18",
      "universe_end_date": "2026-08-18",
      "universe_size": 20,
      "candidate_result": { "trade_count": 34, "win_rate_pct": 58.82, "max_drawdown_pct": -14.21, "median_r": 0.42 },
      "live_result": { "trade_count": 31, "win_rate_pct": 54.84, "max_drawdown_pct": -15.03, "median_r": 0.35 },
      "created_at": "2026-08-18T10:00:00Z"
    }
  ]
}
```

---

## GET /strategy/backtest-rule-change/runs/{run_id}

ST-07. Full run detail — re-view a prior run's stored output without re-running (AC-03: "expandable to re-view its stored output"). Same response shape as `POST /strategy/backtest-rule-change/run`'s `data` object.

**Errors:**
- `404` Run not found

---

## Error states

All endpoints return standard FastAPI 422 for invalid query parameters. No 404 responses — empty data returns empty arrays or null fields per the schema above.

---

*Contract authored by Sprint Execution Engine — agent-mediated governance protocol, ST-11, cycle 2026-06-26__release-v6.3.*
