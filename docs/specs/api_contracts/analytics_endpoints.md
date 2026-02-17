# analytics_endpoints.md

## Overview

This document defines the **Analytics** domain endpoints.

The implementation uses a **unified endpoint** (`GET /analytics/metrics`) rather than the five separate endpoints originally planned. All analytics data is returned in a single response, with an optional `period` filter controlling which trades and history are included.

A validation endpoint (`POST /validate/calculations`) is also provided for smoke-testing metric correctness against a known dataset.

All analytics are computed **server-side** from closed trade records (`trade_history`) and portfolio snapshots (`portfolio_history`). The frontend must never calculate or derive these metrics.

Global response envelopes, error shape, defaults, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

> **Note:** `GET /portfolio/history` is documented in `portfolio_endpoints.md`. The README should list it there, not under analytics.

---

## Endpoints

- [GET /analytics/metrics](#get-analyticsmetrics)
- [POST /validate/calculations](#post-validatecalculations)

---

## GET /analytics/metrics

**Purpose**

Return comprehensive portfolio analytics for a given time period. Includes executive-level statistics, advanced metrics, per-market breakdowns, monthly trends, exit reason analysis, holding period buckets, day-of-week performance, top/worst performers, and consistency metrics.

Requires a minimum number of closed trades to produce meaningful output (configurable via `settings.min_trades_for_analytics`, default `10`).

All monetary values are in GBP.

**Method & Path**

- `GET /analytics/metrics`

**Idempotency**

- Safe to refresh (read-only). Deterministic recomputation from stored records.

---

### Request

#### Query parameters

| Parameter | Type | Required | Default | Allowed values |
|-----------|------|----------|---------|----------------|
| `period` | string | No | `all_time` | `all_time`, `last_7_days`, `last_month`, `last_quarter`, `last_year`, `ytd` |

Period filters trades by `exit_date` and portfolio snapshots by `snapshot_date`. `all_time` includes all records.

---

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema — top level

```json
{
  "summary": { ... },
  "executive_metrics": { ... },
  "advanced_metrics": { ... },
  "market_comparison": { ... },
  "exit_reasons": [ ... ],
  "monthly_data": [ ... ],
  "day_of_week": [ ... ],
  "holding_periods": [ ... ],
  "top_performers": { ... },
  "consistency_metrics": { ... },
  "trades_for_charts": [ ... ]
}
```

---

#### `summary` object

```json
{
  "total_trades": 5,
  "win_rate": 40.0,
  "total_pnl": 2.06,
  "has_enough_data": true,
  "min_required": 10
}
```

| Field | Type | Notes |
|-------|------|-------|
| `total_trades` | integer | Closed trades in the selected period |
| `win_rate` | float | Percentage of trades with positive P&L (0–100) |
| `total_pnl` | float | Sum of all realised P&L in GBP |
| `has_enough_data` | boolean | `false` when `total_trades < min_required`. When false, `executive_metrics` and `advanced_metrics` return `{}` |
| `min_required` | integer | Minimum trades threshold from `settings.min_trades_for_analytics` |

---

#### `executive_metrics` object

Present when `has_enough_data` is `true`. Returns `{}` otherwise.

```json
{
  "sharpe_ratio": 1.29,
  "sharpe_method": "portfolio",
  "max_drawdown": {
    "percent": -7.70,
    "amount": 419.07,
    "date": "2026-02-10"
  },
  "recovery_factor": 0.36,
  "expectancy": 0.39,
  "profit_factor": 1.01,
  "risk_reward_ratio": 1.51
}
```

| Field | Type | Notes |
|-------|------|-------|
| `sharpe_ratio` | float | See Sharpe calculation method below. Returns `0.0` if insufficient data |
| `sharpe_method` | string | `"portfolio"` (30+ snapshots), `"trade"` (10+ trades), or `"insufficient_data"` |
| `max_drawdown.percent` | float | Largest peak-to-trough decline as a percentage. Always zero or negative (e.g. `-7.70`) |
| `max_drawdown.amount` | float | Absolute GBP value of the drawdown (positive) |
| `max_drawdown.date` | string \| null | Date of the trough (`YYYY-MM-DD`), or `null` if no snapshots |
| `recovery_factor` | float | Period net profit divided by max drawdown. `0.0` if drawdown is zero or period is unprofitable |
| `expectancy` | float | `(win_rate × avg_win) + (loss_rate × avg_loss)` in GBP per trade |
| `profit_factor` | float | Gross profit divided by gross loss. Values above `1.0` indicate a net-profitable strategy. `0.0` if no losing trades |
| `risk_reward_ratio` | float | Average winner divided by absolute average loser. `0.0` if no losing trades |

**Sharpe ratio calculation:**

- **Portfolio method** (preferred, requires 30+ portfolio snapshots): computes daily returns from consecutive snapshot values, then `(avg_daily_return / std_dev) × √252`.
- **Trade method** (fallback, requires 10+ trades): annualises each trade's percentage return by holding period, then applies the same formula.
- If neither threshold is met, returns `0.0` with `sharpe_method: "insufficient_data"`.

**`total_return_pct` note:** This field is not currently returned by the implementation. When added, the canonical definition is `total_pnl / net_cash_flow × 100`, where `net_cash_flow = total_deposits − total_withdrawals`. This matches the portfolio-level P&L basis used throughout the system.

---

#### `advanced_metrics` object

Present when `has_enough_data` is `true`. Returns `{}` otherwise.

```json
{
  "win_streak": 2,
  "loss_streak": 3,
  "avg_hold_winners": 15.5,
  "avg_hold_losers": 10.7,
  "trade_frequency": 1.8,
  "capital_efficiency": 0.17,
  "days_underwater": 0,
  "peak_date": "2026-02-03",
  "portfolio_peak_equity": 5444.29
}
```

| Field | Type | Notes |
|-------|------|-------|
| `win_streak` | integer | Maximum consecutive winning trades in the period |
| `loss_streak` | integer | Maximum consecutive losing trades in the period |
| `avg_hold_winners` | float | Average days held for profitable trades |
| `avg_hold_losers` | float | Average days held for losing trades |
| `trade_frequency` | float | Trades per week, calculated from span between first entry and last exit |
| `capital_efficiency` | float | `total_pnl / avg_position_value × 100` |
| `days_underwater` | integer | Maximum days since peak running equity, calculated from trade P&L sequence |
| `peak_date` | string \| null | Exit date of the trade at which running equity was highest |
| `portfolio_peak_equity` | float | Peak `total_value` from portfolio snapshots in the period. `0.0` if no snapshots |

---

#### `market_comparison` object

Breakdown of metrics by market. Always present (values `0.0` / `null` if no trades for that market).

```json
{
  "US": {
    "total_trades": 4,
    "win_rate": 50.0,
    "total_pnl": 184.10,
    "avg_win": 99.33,
    "avg_loss": -7.28,
    "best_performer": { "ticker": "SNDK", "pnl": 104.98 },
    "worst_performer": { "ticker": "FRES.L", "pnl": -182.16 }
  },
  "UK": {
    "total_trades": 1,
    "win_rate": 0.0,
    "total_pnl": -182.16,
    "avg_win": 0.0,
    "avg_loss": -182.16,
    "best_performer": null,
    "worst_performer": { "ticker": "FRES.L", "pnl": -182.16 }
  }
}
```

---

#### `exit_reasons` array

One entry per distinct exit reason found in the period.

```json
[
  {
    "reason": "Trailing Stop",
    "count": 2,
    "win_rate": 100.0,
    "total_pnl": 198.66,
    "avg_pnl": 99.33,
    "percentage": 40.0
  },
  {
    "reason": "Manual Exit",
    "count": 3,
    "win_rate": 0.0,
    "total_pnl": -196.72,
    "avg_pnl": -65.57,
    "percentage": 60.0
  }
]
```

- `null` exit reasons are normalised to `"Manual Exit"`.
- `percentage` is the share of total trades for this reason.

---

#### `monthly_data` array

Month-by-month breakdown of closed trades. Limited to the last 12 months of available data (not affected by the `period` filter — always last 12 months from the filtered dataset).

```json
[
  {
    "month": "2026-01",
    "pnl": -23.69,
    "trades": 2,
    "win_rate": 0.0,
    "cumulative": -23.69
  },
  {
    "month": "2026-02",
    "pnl": 25.75,
    "trades": 3,
    "win_rate": 66.0,
    "cumulative": 2.06
  }
]
```

- `month` is `YYYY-MM`, sorted ascending.
- `cumulative` is running sum of `pnl` across months.
- `win_rate` is rounded to the nearest integer (no decimal).
- Only months with at least one closed trade are included.

---

#### `day_of_week` array

Performance by exit day of week. Always five entries (Mon–Fri). Zero values for days with no trades.

```json
[
  { "day": "Mon", "avg_pnl": 0.0, "trades": 0 },
  { "day": "Tue", "avg_pnl": -65.57, "trades": 3 },
  { "day": "Wed", "avg_pnl": 0.0, "trades": 0 },
  { "day": "Thu", "avg_pnl": 0.0, "trades": 0 },
  { "day": "Fri", "avg_pnl": 49.33, "trades": 2 }
]
```

---

#### `holding_periods` array

Performance bucketed by holding duration. Always five entries.

```json
[
  { "period": "1-5 days",  "avg_pnl": 0.0,   "trades": 0, "win_rate": 0 },
  { "period": "6-10 days", "avg_pnl": -97.20, "trades": 2, "win_rate": 0 },
  { "period": "11-20 days","avg_pnl": 31.78,  "trades": 3, "win_rate": 67 },
  { "period": "21-30 days","avg_pnl": 0.0,    "trades": 0, "win_rate": 0 },
  { "period": "31+ days",  "avg_pnl": 0.0,    "trades": 0, "win_rate": 0 }
]
```

---

#### `top_performers` object

Top 5 winners and top 5 losers from the filtered period.

```json
{
  "winners": [
    {
      "ticker": "SNDK",
      "entry_date": "2026-01-23",
      "pnl": 104.98,
      "pnl_percent": 18.76,
      "days_held": 12,
      "exit_reason": "Trailing Stop"
    }
  ],
  "losers": [
    {
      "ticker": "FRES.L",
      "entry_date": "2026-01-23",
      "pnl": -182.16,
      "pnl_percent": -16.23,
      "days_held": 10,
      "exit_reason": "Manual Exit"
    }
  ]
}
```

- `winners` contains only trades with `pnl > 0`, sorted descending.
- `losers` contains only trades with `pnl < 0`, sorted ascending (most negative first).
- Up to 5 entries each. Empty arrays if no qualifying trades.

---

#### `consistency_metrics` object

```json
{
  "consecutive_profitable_months": 1,
  "current_streak": 1,
  "win_rate_std_dev": 33.0,
  "pnl_std_dev": 24.72
}
```

| Field | Type | Notes |
|-------|------|-------|
| `consecutive_profitable_months` | integer | Longest run of months with positive `pnl` |
| `current_streak` | integer | Current run of profitable months (resets to 0 on a loss month) |
| `win_rate_std_dev` | float | Standard deviation of monthly win rates |
| `pnl_std_dev` | float | Standard deviation of monthly P&L values |

Returns zero values if `monthly_data` is empty.

---

#### `trades_for_charts` array

Lightweight trade list for frontend chart rendering. Always present (empty if no trades).

```json
[
  {
    "id": "87ad66e0-c789-4490-9399-055b580b6312",
    "ticker": "STX",
    "market": "US",
    "entry_date": "2026-01-23",
    "exit_date": "2026-02-11",
    "pnl": 93.68,
    "pnl_percent": 12.23,
    "exit_reason": "Trailing Stop",
    "holding_days": 19,
    "tags": null
  }
]
```

---

### Insufficient data response

When `total_trades < min_required`, the response is still HTTP 200 with `has_enough_data: false`. All nested metric objects return empty:

```json
{
  "status": "ok",
  "data": {
    "summary": {
      "total_trades": 3,
      "win_rate": 0.0,
      "total_pnl": 0.0,
      "has_enough_data": false,
      "min_required": 10
    },
    "executive_metrics": {},
    "advanced_metrics": {},
    "market_comparison": {},
    "exit_reasons": [],
    "monthly_data": [],
    "day_of_week": [],
    "holding_periods": [],
    "top_performers": { "winners": [], "losers": [] },
    "consistency_metrics": {},
    "trades_for_charts": []
  }
}
```

---

### Errors

Errors use the standard error envelope from **conventions.md**.

| Code | Condition |
|------|-----------|
| 400 | `period` value not in the allowed enum |
| 500 | Database error or calculation failure |

---

## POST /validate/calculations

**Purpose**

Validate all analytics calculations against a fixed internal test dataset (5 known trades + 12 portfolio snapshots). Returns a pass/fail/warn result for each metric, with expected value, actual value, diff, and tolerance.

No request body required.

**Method & Path**

- `POST /validate/calculations`

**Idempotency**

- Safe to repeat. Uses only internal test data, no database writes.

---

### Request

No parameters. No request body.

---

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "validations": [
      {
        "metric": "sharpe_ratio",
        "expected": 0.0,
        "actual": 0.0,
        "diff": 0.0,
        "status": "pass",
        "tolerance": 0.01,
        "formula": "(Avg Return / Std Dev) × √252",
        "method": "insufficient_data"
      },
      {
        "metric": "max_drawdown_percent",
        "expected": -7.70,
        "actual": -7.70,
        "diff": 0.0,
        "status": "pass",
        "tolerance": 0.1,
        "formula": "((Peak - Trough) / Peak) × 100"
      },
      {
        "metric": "profit_factor",
        "expected": 1.01,
        "actual": 1.01,
        "diff": 0.0,
        "status": "pass",
        "tolerance": 0.02,
        "formula": "Gross Profit / Gross Loss"
      }
    ],
    "summary": {
      "total": 12,
      "passed": 12,
      "warned": 0,
      "failed": 0
    },
    "timestamp": "2026-02-17T10:30:00Z"
  }
}
```

#### Metrics validated

| Metric | Formula | Tolerance |
|--------|---------|-----------|
| `sharpe_ratio` | `(Avg Return / Std Dev) × √252` | ±0.01 |
| `max_drawdown_percent` | `((Peak − Trough) / Peak) × 100` | ±0.1% |
| `recovery_factor` | `Net Profit / Max Drawdown` | ±0.05 |
| `expectancy` | `(Win Rate × Avg Win) + (Loss Rate × Avg Loss)` | ±£0.10 |
| `profit_factor` | `Gross Profit / Gross Loss` | ±0.02 |
| `risk_reward_ratio` | `Avg Win / Avg Loss` | ±0.02 |
| `win_streak` | Max consecutive winning trades | Exact |
| `loss_streak` | Max consecutive losing trades | Exact |
| `avg_hold_winners` | Avg days held, winning trades | ±0.5 days |
| `avg_hold_losers` | Avg days held, losing trades | ±0.5 days |
| `trade_frequency` | Trades per week | ±0.2 |
| `days_underwater` | Days since peak equity | Exact |

#### `validation.status` values

- `"pass"` — actual is within tolerance of expected
- `"warn"` — actual is outside tolerance but within 2× tolerance (reserved for future use)
- `"fail"` — actual is outside tolerance

---

### Errors

| Code | Condition |
|------|-----------|
| 500 | Calculation failure in the analytics service |

---

## Known limitations & backlog

- **`total_return_pct`** is not yet returned by `GET /analytics/metrics`. When implemented, the canonical formula is `total_pnl / net_cash_flow × 100`.
- **ValidationService** (`services/validation_service.py`) is a stub and not invoked. The active validation logic lives in `routers/validation.py`. Backlog: consolidate or remove the stub class.
- **Sharpe variance** currently uses population variance (`÷ n`). Sample variance (`÷ n−1`) is the convention for financial time series and should be adopted.
- **Capital efficiency** uses `entry_price × shares` for cost basis, which mixes USD and GBP for portfolios with both markets. Should use `total_cost` (always GBP) from `trade_history`.
- **No portfolio_id filter** in the analytics router database queries. Will produce incorrect results in multi-portfolio configurations.
