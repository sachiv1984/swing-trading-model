# analytics_endpoints.md

## Overview

This document defines the **Analytics** domain endpoints.

The implementation uses a **unified endpoint** (`GET /analytics/metrics`) rather than the five separate endpoints originally planned. All analytics data is returned in a single response, with an optional `period` filter controlling which trades and history are included.

A validation endpoint (`POST /validate/calculations`) is also provided for smoke-testing metric correctness against a known dataset.

All analytics are computed **server-side** from closed trade records (`trade_history`) and portfolio snapshots (`portfolio_history`). The frontend must never calculate or derive these metrics.

Global response envelopes, error shape, defaults, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

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

- **Portfolio method** (preferred, requires 30+ portfolio snapshots): computes daily returns from consecutive snapshot values, then `(avg_daily_return / std_dev) × √252`. Uses sample variance (÷ n−1).
- **Trade method** (fallback, requires 10+ trades): annualises each trade's percentage return by holding period, then applies the same formula. Uses sample variance (÷ n−1).
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
  "capital_efficiency": 0.22,
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
| `capital_efficiency` | float | `(total_pnl / mean(total_cost)) × 100`. Cost basis uses `trade_history.total_cost` (GBP) |
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
    "trade_count": 3,
    "pnl": 150.00,
    "win_rate": 66.7
  }
]
```

---

#### `day_of_week` array

Performance grouped by exit day of week. Always 7 entries (Monday–Sunday), zero values for days with no exits.

```json
[
  { "day": "Monday", "trade_count": 0, "avg_pnl": 0.0 },
  { "day": "Tuesday", "trade_count": 2, "avg_pnl": 45.5 }
]
```

---

#### `holding_periods` array

Trades bucketed by holding duration.

```json
[
  { "period": "1-5 days",  "trades": 1, "avg_pnl": -12.23, "win_rate": 0.0 },
  { "period": "6-10 days", "trades": 0, "avg_pnl": 0.0,    "win_rate": 0.0 },
  { "period": "11-20 days","trades": 3, "avg_pnl": 29.96,  "win_rate": 33.3 },
  { "period": "21-30 days","trades": 1, "avg_pnl": 93.68,  "win_rate": 100.0 },
  { "period": "31+ days",  "trades": 0, "avg_pnl": 0.0,    "win_rate": 0.0 }
]
```

---

#### `top_performers` object

```json
{
  "winners": [
    { "ticker": "SNDK", "pnl": 104.98, "pnl_percent": 18.76 },
    { "ticker": "STX",  "pnl": 93.68,  "pnl_percent": 12.23 }
  ],
  "losers": [
    { "ticker": "FRES.L", "pnl": -182.16, "pnl_percent": -16.23 },
    { "ticker": "WDC",    "pnl": -12.23,  "pnl_percent": -1.24 }
  ]
}
```

Up to 5 winners and 5 losers, sorted by P&L descending / ascending respectively.

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
    "entry_price": 55.20,
    "exit_price": 70.40,
    "stop_price": 48.50,
    "pnl": 93.68,
    "pnl_percent": 12.23,
    "exit_reason": "Trailing Stop",
    "holding_days": 19,
    "tags": null
  }
]
```

> **Note on `entry_price`, `exit_price`, `stop_price`:** These fields are included to support client-side R-multiple visualisation: `R = (exit_price − entry_price) / |entry_price − stop_price|`. This is the only analytics calculation performed client-side, and only because the initial stop price is not stored in `trade_history`. R-multiple is a visualisation aid only; it is not a server-computed metric.

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

Validate all analytics calculations against a fixed internal test dataset (5 known trades + 12 portfolio snapshots). Returns a pass/fail/warn result for each metric, with expected value, actual value, diff, tolerance, and severity.

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
        "severity": "critical",
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
        "severity": "critical",
        "tolerance": 0.1,
        "formula": "((Peak - Trough) / Peak) × 100"
      },
      {
        "metric": "capital_efficiency",
        "expected": 0.22,
        "actual": 0.22,
        "diff": 0.0,
        "status": "pass",
        "severity": "medium",
        "tolerance": 0.05,
        "formula": "(Total PnL / Mean(total_cost)) × 100"
      }
    ],
    "summary": {
      "total": 13,
      "passed": 13,
      "warned": 0,
      "failed": 0,
      "by_severity": {
        "critical": { "total": 3, "passed": 3, "warned": 0, "failed": 0 },
        "high":     { "total": 3, "passed": 3, "warned": 0, "failed": 0 },
        "medium":   { "total": 6, "passed": 6, "warned": 0, "failed": 0 },
        "low":      { "total": 1, "passed": 1, "warned": 0, "failed": 0 }
      }
    },
    "timestamp": "2026-02-21T00:24:41.984760Z"
  }
}
```

---

#### `validations` array — per-result object fields

| Field | Type | Notes |
|-------|------|-------|
| `metric` | string | Metric identifier |
| `expected` | number | Ground truth value from `validation_data.py` |
| `actual` | number | Value computed by the analytics service |
| `diff` | number | `abs(actual − expected)` |
| `status` | string | `"pass"`, `"warn"`, or `"fail"` — see status values below |
| `severity` | string | `"critical"`, `"high"`, `"medium"`, or `"low"` — see severity model below |
| `tolerance` | number | Maximum acceptable `diff` for a `"pass"` |
| `formula` | string | Human-readable formula description |
| `method` | string | Sharpe only: `"portfolio"`, `"trade"`, or `"insufficient_data"` |

---

#### `validation.status` values

- `"pass"` — `diff` is within `tolerance`
- `"warn"` — `diff` exceeds `tolerance` but is within `2 × tolerance` (reserved for future use)
- `"fail"` — `diff` exceeds `tolerance`

---

#### Severity model

Severity is assigned per metric and is fixed regardless of pass/fail status. It governs how a failure should be actioned. The four-tier model matches `docs/operations/validation_system.md`.

| Severity | Metrics | Action on failure |
|----------|---------|-------------------|
| `critical` | `sharpe_ratio`, `max_drawdown_percent`, `profit_factor` | Block deployment. Page on-call engineer. Investigate immediately |
| `high` | `recovery_factor`, `expectancy`, `risk_reward_ratio` | Require manual sign-off before deploy. Alert analytics team |
| `medium` | `win_streak`, `loss_streak`, `avg_hold_winners`, `avg_hold_losers`, `trade_frequency`, `capital_efficiency` | Log warning. Investigate if persistent (3+ consecutive runs) |
| `low` | `days_underwater` | Log only. Review monthly |

---

#### Metrics validated

| Metric | Severity | Formula | Tolerance |
|--------|----------|---------|-----------|
| `sharpe_ratio` | critical | `(Avg Return / Std Dev) × √252` | ±0.01 |
| `max_drawdown_percent` | critical | `((Peak − Trough) / Peak) × 100` | ±0.1% |
| `profit_factor` | critical | `Gross Profit / Gross Loss` | ±0.02 |
| `recovery_factor` | high | `Net Profit / Max Drawdown` | ±0.05 |
| `expectancy` | high | `(Win Rate × Avg Win) + (Loss Rate × Avg Loss)` | ±£0.10 |
| `risk_reward_ratio` | high | `Avg Win / Avg Loss` | ±0.02 |
| `win_streak` | medium | Max consecutive winning trades | Exact |
| `loss_streak` | medium | Max consecutive losing trades | Exact |
| `avg_hold_winners` | medium | Avg days held, winning trades | ±0.5 days |
| `avg_hold_losers` | medium | Avg days held, losing trades | ±0.5 days |
| `trade_frequency` | medium | Trades per week | ±0.2 |
| `capital_efficiency` | medium | `(Total PnL / Mean(total_cost)) × 100` | ±0.05 |
| `days_underwater` | low | Days since peak equity | Exact |

---

#### `summary.by_severity` object

Aggregated counts per severity tier. Always present with all four keys, even if a tier has zero metrics.

```json
"by_severity": {
  "critical": { "total": 3, "passed": 3, "warned": 0, "failed": 0 },
  "high":     { "total": 3, "passed": 3, "warned": 0, "failed": 0 },
  "medium":   { "total": 6, "passed": 6, "warned": 0, "failed": 0 },
  "low":      { "total": 1, "passed": 1, "warned": 0, "failed": 0 }
}
```

---

### Errors

| Code | Condition |
|------|-----------|
| 500 | Calculation failure in the analytics service |

---

## Known limitations & backlog

- **`total_return_pct`** is not yet returned by `GET /analytics/metrics`. When implemented, the canonical formula is `total_pnl / net_cash_flow × 100`.
- **ValidationService** (`services/validation_service.py`) is a stub and not invoked. Active validation logic lives in `routers/validation.py`. This is tracked as BLG-TECH-03 (consolidate into service layer, deliver alongside BLG-TECH-02).
- **No portfolio_id filter** in the analytics router database queries. Will produce incorrect results in multi-portfolio configurations.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.5.0 | 2026-02-17 | Initial rewrite: unified endpoint, validation endpoint, known limitations recorded |
| 1.7.0 | 2026-02-17 | Added `entry_price`, `exit_price`, `stop_price` to `trades_for_charts`; R-multiple note added |
| 1.8.1 | 2026-02-21 | BLG-TECH-02 contract: added `severity` field to each validation result object; added `by_severity` aggregation to `summary`; added severity model table; updated metrics validated table to include severity column and `capital_efficiency` row; updated response example; removed resolved known limitation entries for Sharpe variance and capital efficiency currency basis (resolved via BLG-TECH-01). API Contracts Owner. |