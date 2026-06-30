**Owner:** Backend Engineering Patterns Owner; Product Owner
**Class:** API Contract (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-30
**Story:** ST-11 (BLG-FEAT-53, EPIC-03, v6.3)

---

# Strategy Benchmark API Contract

Endpoints supporting the Strategy Benchmark page — comparison of live trade performance against production_strategy.py backtest results.

Data flow: `production_strategy.py` → CSV files in `production_results/` → `import_backtest.py` → `POST /strategy/benchmark/import` → `backtest_trades` + `backtest_yearly_performance` tables → `GET /strategy/benchmark/summary` / `GET /strategy/benchmark/trades` → frontend.

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
  "imported_at": "2026-06-30T10:15:00Z"
}
```

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

## Error states

All endpoints return standard FastAPI 422 for invalid query parameters. No 404 responses — empty data returns empty arrays or null fields per the schema above.

---

*Contract authored by Sprint Execution Engine — agent-mediated governance protocol, ST-11, cycle 2026-06-26__release-v6.3.*
