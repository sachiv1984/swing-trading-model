# analytics_endpoints.md

> **Implementation status:** Planned — not yet implemented.  
> Backend endpoints, service layer, and database queries do not exist yet.  
> This contract is the authoritative specification for implementation.  
> Data sources are confirmed to exist in `trade_history` and `portfolio_history` tables.

## Overview

This document defines **Analytics** domain endpoints:

- Overall performance summary statistics
- Monthly performance breakdown
- Best and worst trade analysis
- Drawdown history

All analytics are computed **server-side** from closed trade records and portfolio snapshots. The frontend must never calculate or derive these metrics.

Global response envelopes, error shape, defaults, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /analytics/summary](#get-analyticssummary)
- [GET /analytics/monthly](#get-analyticsmonthly)
- [GET /analytics/trades/best](#get-analyticstradesbest)
- [GET /analytics/trades/worst](#get-analyticstradesworst)
- [GET /analytics/drawdown](#get-analyticsdrawdown)

---

## GET /analytics/summary

**Purpose**

Return overall portfolio performance statistics computed from all closed trades and portfolio snapshots.

- Requires a minimum number of closed trades to produce meaningful output (configurable via settings: `min_trades_for_analytics`).
- All monetary values are in GBP.

**Method & Path**

- `GET /analytics/summary`

**Idempotency**

- Safe to refresh (read-only). Deterministic recomputation from stored records.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "total_trades": 42,
  "win_rate": 58.5,
  "total_pnl": 5200.00,
  "total_return_pct": 36.4,
  "annualized_return_pct": 24.1,
  "profit_factor": 2.31,
  "expectancy_per_trade": 123.81,
  "average_winner": 480.00,
  "average_loser": -207.50,
  "largest_winner": 3200.00,
  "largest_loser": -620.00,
  "average_holding_days": 22,
  "sharpe_ratio": 1.29,
  "max_drawdown_pct": 25.38,
  "max_drawdown_gbp": 3807.00,
  "sufficient_data": true,
  "min_trades_required": 10
}
```

#### Field notes

- `win_rate` is expressed as a percentage (0–100).
- `total_return_pct` is calculated as `total_pnl / net_cash_flow × 100`, where `net_cash_flow = total_deposits − total_withdrawals`. This matches the portfolio-level P&L basis used throughout the system.
- `profit_factor` is gross profit divided by gross loss. Values above `1.0` indicate a net-profitable strategy.
- `expectancy_per_trade` is average P&L per trade in GBP.
- `sharpe_ratio` uses daily returns derived from portfolio snapshots. Returns `null` if insufficient snapshot history exists.
- `max_drawdown_pct` and `max_drawdown_gbp` reflect the largest peak-to-trough decline in portfolio value.
- `sufficient_data` is `false` when closed trade count is below `min_trades_required`. In this case, all statistical fields return `null`.
- `annualized_return_pct` returns `null` if the portfolio has been active for fewer than 30 days.

### Validation rules & constraints

- All calculations are server-side.
- Returns a valid response with `sufficient_data: false` (not an error) when trade count is below the minimum threshold.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /analytics/monthly

**Purpose**

Return a month-by-month performance breakdown derived from closed trades.

- Each row represents a calendar month.
- Only months with at least one closed trade are included.

**Method & Path**

- `GET /analytics/monthly`

**Idempotency**

- Safe to refresh (read-only).

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array)

```json
[
  {
    "month": "2026-02",
    "trades": 6,
    "wins": 4,
    "losses": 2,
    "win_rate": 66.7,
    "total_pnl": 1240.00,
    "average_pnl": 206.67,
    "best_trade_pnl": 820.00,
    "worst_trade_pnl": -185.00
  },
  {
    "month": "2026-01",
    "trades": 8,
    "wins": 4,
    "losses": 4,
    "win_rate": 50.0,
    "total_pnl": 560.00,
    "average_pnl": 70.00,
    "best_trade_pnl": 640.00,
    "worst_trade_pnl": -310.00
  }
]
```

#### Field notes

- `month` is formatted as `YYYY-MM`.
- Results are sorted by `month` descending (newest first).
- Returns `[]` if there are no closed trades.
- All P&L values are in GBP.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /analytics/trades/best

**Purpose**

Return the top-performing closed trades ranked by absolute P&L (GBP), descending.

**Method & Path**

- `GET /analytics/trades/best`

**Idempotency**

- Safe to refresh (read-only).

### Request

#### Query parameters

- `limit` (integer, optional): number of trades to return. Default: `10`. Maximum: `50`.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array)

```json
[
  {
    "id": "750e8400-e29b-41d4-a716-446655440000",
    "ticker": "NVDA",
    "market": "US",
    "entry_date": "2026-01-15",
    "exit_date": "2026-02-15",
    "shares": 10.5,
    "entry_price": 622.00,
    "exit_price": 920.00,
    "pnl": 3200.00,
    "pnl_pct": 35.8,
    "holding_days": 31,
    "exit_reason": "Target Reached",
    "tags": ["momentum", "winner"]
  }
]
```

#### Field notes

- Sorted by `pnl` descending (largest winner first).
- Returns `[]` if there are no closed trades.
- Notes (`entry_note`, `exit_note`) are intentionally excluded from this summary view.

### Validation rules & constraints

- `limit` must be a positive integer when provided.
- `limit` is capped at `50` regardless of the value submitted.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /analytics/trades/worst

**Purpose**

Return the worst-performing closed trades ranked by absolute P&L (GBP), ascending.

**Method & Path**

- `GET /analytics/trades/worst`

**Idempotency**

- Safe to refresh (read-only).

### Request

#### Query parameters

- `limit` (integer, optional): number of trades to return. Default: `10`. Maximum: `50`.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array)

```json
[
  {
    "id": "850e8400-e29b-41d4-a716-446655440001",
    "ticker": "AAPL",
    "market": "US",
    "entry_date": "2026-01-20",
    "exit_date": "2026-02-01",
    "shares": 20.0,
    "entry_price": 180.00,
    "exit_price": 168.00,
    "pnl": -620.00,
    "pnl_pct": -8.8,
    "holding_days": 12,
    "exit_reason": "Stop Loss Hit",
    "tags": ["momentum", "loser"]
  }
]
```

#### Field notes

- Sorted by `pnl` ascending (largest loss first).
- Returns `[]` if there are no closed trades.
- Notes (`entry_note`, `exit_note`) are intentionally excluded from this summary view.

### Validation rules & constraints

- `limit` must be a positive integer when provided.
- `limit` is capped at `50` regardless of the value submitted.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /analytics/drawdown

**Purpose**

Return the portfolio's drawdown history derived from daily portfolio snapshots.

- Each record represents a snapshot date with its corresponding drawdown from the preceding peak.
- Requires portfolio snapshot history to exist (see `POST /portfolio/snapshot` in `portfolio_endpoints.md`).

**Method & Path**

- `GET /analytics/drawdown`

**Idempotency**

- Safe to refresh (read-only). Deterministic recomputation from snapshots.

### Request

#### Query parameters

- `days` (integer, optional): number of days of history to include in `history`. Default: `90`.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "max_drawdown_pct": 25.38,
  "max_drawdown_gbp": 3807.00,
  "max_drawdown_date": "2026-01-10",
  "current_drawdown_pct": 4.20,
  "current_drawdown_gbp": -637.00,
  "history": [
    {
      "snapshot_date": "2026-02-15",
      "total_value": 15000.00,
      "peak_value": 15637.00,
      "drawdown_pct": 4.20,
      "drawdown_gbp": -637.00
    },
    {
      "snapshot_date": "2026-02-14",
      "total_value": 14800.00,
      "peak_value": 15637.00,
      "drawdown_pct": 5.36,
      "drawdown_gbp": -837.00
    }
  ]
}
```

#### Field notes

- `max_drawdown_pct` and `max_drawdown_gbp` reflect the largest peak-to-trough decline over the **full** snapshot history, not limited to the `days` window.
- `max_drawdown_date` is the date on which the maximum drawdown trough occurred.
- `current_drawdown_pct` and `current_drawdown_gbp` reflect the drawdown as of the most recent snapshot.
- `history` is limited to the `days` window and sorted by `snapshot_date` descending (newest first).
- `drawdown_gbp` is always zero or negative. Zero indicates the portfolio is at or above its prior peak.
- Returns `null` for all summary fields and `[]` for `history` if no snapshots exist.

### Validation rules & constraints

- `days` must be a positive integer when provided.
- Peak calculation uses all available snapshot history, not just the `days` window.

### Errors

Errors use the standard error envelope from **conventions.md**.
