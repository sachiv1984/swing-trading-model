# trade_endpoints.md

## Overview

This document defines **Trade** domain endpoints.

- Retrieve immutable, closed trade history
- Includes trade-level statistics and a list of closed trades

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /trades](#get-trades)
- [GET /trades/export/csv](#get-trades-export-csv)

---

## GET /trades

**Purpose**

Retrieve all **closed trades** along with summary statistics.

- Records are immutable (closed positions only).
- Results are sorted by `exit_date` descending (newest first).

**Method & Path**

- `GET /trades`

**Idempotency**

- Safe to refresh (read-only).

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
  "trades": [
    {
      "id": "750e8400-e29b-41d4-a716-446655440000",
      "ticker": "NVDA",
      "market": "US",
      "entry_date": "2026-01-15",
      "exit_date": "2026-02-17",
      "shares": 10.5,
      "entry_price": 622.00,
      "exit_price": 920.00,
      "pnl": 3200.00,
      "pnl_pct": 35.8,
      "pnl_percent": 35.8,
      "holding_days": 33,
      "exit_reason": "Target Reached",
      "entry_note": "Breakout above $800",
      "exit_note": "Hit target",
      "tags": ["momentum", "winner"]
    }
  ]
}
```

#### Field notes

| Field | Notes |
|-------|-------|
| `trades` | Closed trades only. Empty array if no closed trades exist |
| `pnl_pct` and `pnl_percent` | Both fields are returned with the same value for compatibility |
| `holding_days` | Number of calendar days from `entry_date` to `exit_date` inclusive |
| `exit_reason` | The reason recorded at exit. `null` values are normalised to `"Manual Exit"` in the analytics service but stored as-is here |
| `entry_note`, `exit_note` | May be `string` or `null` |
| `tags` | Array of tag strings copied from the position at time of exit. May be empty array |

### Validation rules & constraints

- Trade records are read-only via this endpoint.
- The endpoint returns an empty `trades` array when there are no closed trades.

### Errors

Errors use the standard error envelope from **conventions.md**.

--- 

## GET /trades/export/csv

**Purpose**

Export the full closed trade history as a downloadable CSV file. Intended for tax reporting, external analysis, and record-keeping.

**Method & Path**

-   `GET /trades/export/csv`

**Idempotency**

-   Safe to repeat (read-only). Returns a fresh export on every call.

### Request

No parameters. No request body.

> **v1.6.1 scope note:** Date range filtering is not supported in v1.6.1. The endpoint always returns the full closed trade history. Filtering is a planned future enhancement.

### Response (200)

```
Content-Type: text/csv
Content-Disposition: attachment; filename="trade_history.csv"
```

The response body is a UTF-8 encoded CSV file. The first row is a header row.

#### CSV columns (in order)

| Column | Source field | Notes |
| --- | --- | --- |
| `ticker` | `trade_history.ticker` | Stock symbol |
| `market` | `trade_history.market` | `"US"` or `"UK"` |
| `entry_date` | `trade_history.entry_date` | Format: `YYYY-MM-DD` |
| `exit_date` | `trade_history.exit_date` | Format: `YYYY-MM-DD` |
| `shares` | `trade_history.shares` | Up to 4 decimal places |
| `entry_price` | `trade_history.entry_price` | Native currency (USD for US, GBP for UK) |
| `exit_price` | `trade_history.exit_price` | Native currency |
| `pnl` | `trade_history.pnl` | GBP. Signed (negative = loss) |
| `pnl_pct` | `trade_history.pnl_pct` | Percentage of entry cost. Signed |
| `holding_days` | `trade_history.holding_days` | Integer. Calendar days from entry to exit inclusive |
| `exit_reason` | `trade_history.exit_reason` | String or empty string if null |
| `tags` | `trade_history.tags` | Semicolon-separated string. Empty string if no tags |
| `entry_note` | `trade_history.entry_note` | String or empty string if null |
| `exit_note` | `trade_history.exit_note` | String or empty string if null |

#### Example CSV output

csv

```
ticker,market,entry_date,exit_date,shares,entry_price,exit_price,pnl,pnl_pct,holding_days,exit_reason,tags,entry_note,exit_note
NVDA,US,2026-01-15,2026-02-17,10.5,622.00,920.00,3200.00,35.8,33,Target Reached,momentum;winner,Breakout above $800,Hit target
AAPL,US,2026-01-20,2026-02-10,20.0,180.00,175.00,-100.00,-2.8,21,Risk-Off Signal,,,,
```

#### Null handling

All nullable fields (`exit_reason`, `tags`, `entry_note`, `exit_note`) are returned as empty strings in the CSV --- never as `"null"` or omitted. Tags array is serialised as a semicolon-separated string; empty array becomes an empty string.

#### Empty export

If no closed trades exist, the response is a CSV containing only the header row. HTTP status is still 200.

### Errors

Errors use the standard error envelope from **conventions.md**. Note: on error, the response is JSON (not CSV), even though the successful response is CSV.

| Code | Condition |
| --- | --- |
| 500 | Database error during trade history retrieval |
