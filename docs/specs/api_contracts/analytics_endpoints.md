# analytics_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.5.0
**Last Updated:** 2026-08-11
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines the **Analytics** domain endpoints.

The implementation uses a **unified endpoint** (`GET /analytics/metrics`) rather than the five separate endpoints originally planned. All analytics data is returned in a single response, with an optional `period` filter controlling which trades and history are included.

A validation endpoint (`POST /validate/calculations`) is also provided for smoke-testing metric correctness against a known dataset.

All analytics are computed **server-side** from closed trade records (`trade_history`) and portfolio snapshots (`portfolio_history`). The frontend must never calculate or derive these metrics.

Global response envelopes, error shape, defaults, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /analytics/metrics](#get-analyticsmetrics)
- [GET /analytics/market-correlation](#get-analyticsmarket-correlation)
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
  "trades_for_charts": [ ... ],
  "last_sync_at": "2026-03-29T09:41:00.000000+00:00"
}
```

#### `last_sync_at` field (v2.0.0 — ST-02 BLG-FEAT-09)

UTC ISO 8601 timestamp of when this metrics computation was performed. Used by the frontend to display a data freshness indicator on the Analytics and Portfolio/Positions pages.

| Field | Type | Notes |
|-------|------|-------|
| `last_sync_at` | string (ISO 8601 UTC) | Timestamp of this API computation. Always present. |

Frontend staleness threshold: 4 hours (default, non-configurable in v2.3). If the field is absent or null, the frontend omits the indicator entirely.

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

**`total_return_pct`:** `total_pnl / net_cash_flow × 100`, where `net_cash_flow = total_deposits − total_withdrawals`. Matches the portfolio-level P&L basis used throughout the system.

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
      "total": 14,
      "passed": 14,
      "warned": 0,
      "failed": 0,
      "by_severity": {
        "critical": { "total": 4, "passed": 4, "warned": 0, "failed": 0 },
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
| `critical` | `sharpe_ratio`, `max_drawdown_percent`, `profit_factor`, `sharpe_ratio_trade_method` | Block deployment. Page on-call engineer. Investigate immediately |
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
| `sharpe_ratio_trade_method` | critical | `(Avg Ann Return / Sample StdDev) — trade method fallback` | ±0.01 |
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
  "critical": { "total": 4, "passed": 4, "warned": 0, "failed": 0 },
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

---

## GET /analytics/cohort

Groups all closed trades by entry period and returns per-cohort performance metrics.

### Request

```
GET /analytics/cohort?period={month|quarter|year}
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `period` | string | No | `month` | Cohort granularity: `month`, `quarter`, or `year` |

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "period": "month",
    "has_enough_data": true,
    "cohorts": [
      {
        "period_label": "Mar 2026",
        "trade_count": 5,
        "win_rate": 60.0,
        "avg_r_multiple": 0.80,
        "total_pnl": 320.50
      }
    ]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `period` | string | Echoes the requested period granularity |
| `has_enough_data` | boolean | `true` if ≥3 distinct cohort periods exist |
| `cohorts` | array | Per-cohort rows, sorted descending by period |
| `cohorts[].period_label` | string | Human-readable label ("Mar 2026", "Q1 2026", "2026") |
| `cohorts[].trade_count` | integer | Count of closed trades with entry_date in this period |
| `cohorts[].win_rate` | float | Percentage of trades with pnl > 0 (1dp) |
| `cohorts[].avg_r_multiple` | float \| null | Mean R-multiple for qualifying trades; null if no stop_price data |
| `cohorts[].total_pnl` | float | Net P&L in GBP for all trades in cohort (2dp) |

**Insufficient history:** `has_enough_data: false` when fewer than 3 distinct cohort periods exist. Frontend shows: "Not enough closed trades to show [period] cohorts".

**Canonical formulas:** `metrics_definitions.md v1.7.0 §Cohort Metrics`.

**R-multiple dependency:** `avg_r_multiple` requires `positions.initial_stop` via LEFT JOIN (`trade_history.position_id → positions.id`). Returns `null` per trade if migration not run or stop not stored.

### Error Responses

- `400 Bad Request`: invalid `period` value (not `month`/`quarter`/`year`)
- `500 Internal Server Error`: database or computation error

---

## GET /analytics/r-multiple-distribution

Returns canonical server-side R-multiple distribution across all closed trades.

### Request

```
GET /analytics/r-multiple-distribution
```

No query parameters. Uses all closed trades (all-time).

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "has_enough_data": true,
    "total_qualifying_trades": 12,
    "buckets": [
      {"range": "< -2R",      "count": 1},
      {"range": "-2R to -1R", "count": 2},
      {"range": "-1R to 0R",  "count": 3},
      {"range": "0R to 1R",   "count": 4},
      {"range": "1R to 2R",   "count": 1},
      {"range": "2R to 3R",   "count": 1},
      {"range": "> 3R",       "count": 0}
    ],
    "median_r": 0.30,
    "pct_above_1r": 16.7,
    "avg_winner_r": 1.40,
    "avg_loser_r": -0.80
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `has_enough_data` | boolean | `true` if ≥5 qualifying trades exist |
| `total_qualifying_trades` | integer | Count of trades with valid stop_price and entry_price > stop_price |
| `buckets` | array | 7 fixed R-multiple range buckets with trade counts |
| `median_r` | float \| null | Median R-multiple across qualifying trades (2dp) |
| `pct_above_1r` | float \| null | % of qualifying trades with R > 1 (1dp) |
| `avg_winner_r` | float \| null | Mean R-multiple for trades with R > 0 (2dp); null if none |
| `avg_loser_r` | float \| null | Mean R-multiple for trades with R ≤ 0 (2dp); null if none |

**Insufficient data:** `has_enough_data: false` when fewer than 5 qualifying trades. Frontend shows: "Close at least 5 trades to see R-multiple distribution."

**Canonical formula:** `R = (exit_price − entry_price) / (entry_price − initial_stop_price)` per `metrics_definitions.md v1.7.0 §R-Multiple (Canonical Server-Side)`.

**Stop dependency:** Requires `positions.initial_stop` via LEFT JOIN. Trades without `initial_stop` or where `initial_stop ≥ entry_price` are excluded from qualifying trades.

**Hard rule:** This endpoint returns server-side computed values only. No client-side R-multiple computation is permitted in the §16 frontend component.

### Error Responses

- `500 Internal Server Error`: database or computation error

---

## GET /analytics/market-correlation

**Purpose**

Return Pearson correlation coefficients between each open position and its relevant
market benchmark over a configurable lookback window:

- US positions are compared against **SPY** (S&P 500 ETF)
- UK positions are compared against **^FTSE** (FTSE 100 index)

Also returns a portfolio-level equal-weighted average correlation.

All data is sourced on-demand from Yahoo Finance. Results are cached with a TTL of
approximately one trading day (8 hours). If Yahoo Finance is unavailable, the endpoint
returns a partial or empty result with an informational note — it does **not** return 500.

**Note to engineers:** Yahoo Finance is an external dependency with known reliability
variability. If persistent unavailability becomes a problem, a formal data source review
is required before any further correlation-dependent features are introduced.

**Method & Path**

- `GET /analytics/market-correlation`

**Idempotency**

- Safe to refresh (read-only). Deterministic within TTL window.

### Request

#### Query parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lookback` | integer | No | `252` | Lookback window in trading days (30–756) |

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "correlations": [
      {
        "ticker": "LGEN",
        "market": "UK",
        "benchmark": "FTSE",
        "correlation": 0.72,
        "severity": "high",
        "lookback_days": 252,
        "data_points": 248
      },
      {
        "ticker": "TSLA",
        "market": "US",
        "benchmark": "SPY",
        "correlation": 0.41,
        "severity": "moderate",
        "lookback_days": 252,
        "data_points": 251
      }
    ],
    "portfolio_correlation": {
      "value": 0.57,
      "severity": "moderate",
      "method": "equal_weighted_average"
    },
    "lookback_days": 252,
    "computed_at": "2026-04-15T10:00:00Z",
    "cached": false,
    "data_source": "Yahoo Finance"
  }
}
```

#### Field notes

| Field | Notes |
|-------|-------|
| `correlation` | Pearson coefficient over daily returns in `[-1, 1]`. `null` if data unavailable. |
| `severity` | `high` (abs > 0.7), `moderate` (0.3–0.7), `low` (< 0.3), `unknown` (null). |
| `data_points` | Number of overlapping trading days used in the correlation calculation. |
| `cached` | `true` when result is served from the 8-hour TTL cache. |
| `portfolio_correlation.method` | Always `equal_weighted_average` in this version. |

### Error responses

- `500 Internal Server Error`: database error fetching open positions or DATABASE_URL not set.
- Partial results (missing `correlation: null`) returned if Yahoo Finance is unavailable for individual tickers — no 500 raised.

---

## GET /analytics/arc5-compliance

Returns Arc 5 signal compliance metrics for the trading system.

### Request

**Method:** GET
**Path:** `/analytics/arc5-compliance`
**Authentication:** API Key required

#### Query parameters

| Parameter | Type | Required | Default | Values | Description |
|-----------|------|----------|---------|--------|-------------|
| `period` | string | No | `7d` | `7d`, `30d` | Rolling window for validation and event metrics |

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "period": "7d",
    "validation_pass_rate_by_rule": {
      "regime_gate": {"pass_rate": 0.75, "pass_count": 15, "fail_count": 5},
      "cash_constraint": {"pass_rate": 0.9, "pass_count": 18, "fail_count": 2},
      "sector_concentration": {"pass_rate": 1.0, "pass_count": 20, "fail_count": 0},
      "earnings_proximity": {"pass_rate": 0.85, "pass_count": 17, "fail_count": 3},
      "sizing_validity": {"pass_rate": 0.95, "pass_count": 19, "fail_count": 1}
    },
    "events_per_week": 3.14,
    "override_rate": 0.4,
    "top_rule_breach": "regime_gate",
    "trade_plan_adherence_rate": 0.6
  }
}
```

#### `data` schema

| Field | Type | Description |
|-------|------|-------------|
| `period` | string | The period used for validation metrics (`7d` or `30d`) |
| `validation_pass_rate_by_rule` | object | Per-rule pass rates from `pre_entry_validation_log`. Empty `{}` if no data. |
| `validation_pass_rate_by_rule.<rule>.pass_rate` | float\|null | Pass rate 0–1; null if no data |
| `validation_pass_rate_by_rule.<rule>.pass_count` | integer | Passes in period |
| `validation_pass_rate_by_rule.<rule>.fail_count` | integer | Failures in period |
| `events_per_week` | float | Avg red flag events per day × 7 (rolling 7-day always) |
| `override_rate` | float\|null | Overrides / validation attempts in last 7 days; null if no attempts |
| `top_rule_breach` | string\|null | Most frequently failing rule_type in period; null if no failures |
| `trade_plan_adherence_rate` | float\|null | Trades with linked plan / total closed trades (all-time); null if no trades or position_id migration not run |

**Rule types:** `regime_gate`, `cash_constraint`, `sector_concentration`, `earnings_proximity`, `sizing_validity`

### Errors

- `500 Internal Server Error`: database error or `DATABASE_URL` not set.

---

## GET /analytics/tag-performance

Returns win rate and average R-multiple per requested trade-plan tag.

**Source:** ST-05, BLG-FEAT-52, v6.8. Reads only `trade_plans.trade_tags` and existing closed-trade linkage — no dependency on `trade_annotations`/PO-02.

### Request

**Method:** GET
**Path:** `/analytics/tag-performance`
**Authentication:** API Key required

#### Query parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tags` | string | Yes | Comma-separated trade-plan tags (e.g. `breakout,earnings-play`) |

### Response (200)

```json
{
  "status": "ok",
  "data": [
    {"tag": "breakout", "win_rate": 62.5, "avg_r_multiple": 1.8, "trade_count": 8},
    {"tag": "earnings-play", "win_rate": 40.0, "avg_r_multiple": -0.3, "trade_count": 5}
  ]
}
```

#### `data` schema (array, one entry per requested tag)

| Field | Type | Description |
|-------|------|--------------|
| `tag` | string | Echoed tag (lowercase) |
| `win_rate` | number | % of linked closed trades with `pnl > 0` (1 dp). 0.0 if no matching trades. |
| `avg_r_multiple` | number\|null | Mean R-multiple across matching trades with a resolvable stop (`(exit-entry)/(entry-stop)`); null if no qualifying trade has a resolvable stop |
| `trade_count` | integer | Closed trades linked to a plan carrying this tag |

### Errors

| Code | Condition |
|------|-----------|
| 400 | `tags` parameter missing or empty |
| 404 | Portfolio not found |
| 500 | Database error |

---

## GET /analytics/trade-plan-completion-rate

Returns the trade plan completion rate: how many created trade plans resulted in a closed trade vs were abandoned.

**Source:** ST-01, BLG-FEAT-32, EPIC-01, v8.6.

### Request

**Method:** GET
**Path:** `/analytics/trade-plan-completion-rate`
**Authentication:** API Key required

No parameters.

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "plans_created": 24,
    "plans_completed": 15,
    "plans_abandoned": 4,
    "completion_rate": 62.5
  }
}
```

#### `data` schema

| Field | Type | Description |
|-------|------|--------------|
| `plans_created` | integer | All `trade_plans` rows for this portfolio |
| `plans_completed` | integer | Plans linked to a position (`trade_plans.position_id`) with at least one closed `trade_history` row for that position |
| `plans_abandoned` | integer | Plans with `status = 'abandoned'` |
| `completion_rate` | number\|null | `plans_completed / plans_created * 100` (1 dp); `null` if `plans_created` is 0 — the frontend renders the empty state ("No trade plans created yet.") rather than a misleading `0%` |

### Errors

| Code | Condition |
|------|-----------|
| 404 | Portfolio not found |
| 500 | Database error |

---

## GET /analytics/compliance-metrics

**Purpose**

Returns discipline and compliance scalars for all closed trades. Used by the frontend analytics dashboard.

**Method & Path**

- `GET /analytics/compliance-metrics`

**Request**

No parameters.

**Response (200)**

```json
{
  "status": "ok",
  "data": {
    "journal_completion_rate": 80.0,
    "stop_exit_rate": 60.0,
    "avg_position_size_pct": 2.5,
    "trade_count": 15
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `journal_completion_rate` | float | % of closed trades with at least one journal note (entry or exit). Range 0–100. |
| `stop_exit_rate` | float | % of closed trades exited via Stop Loss Hit or Trailing Stop. Range 0–100. |
| `avg_position_size_pct` | float | Mean `(total_cost / portfolio_value_at_entry) × 100` across closed trades. |
| `trade_count` | integer | Total closed trade count (denominator for all metrics). |

**Canonical formulas:** `docs/qa/test_scenarios/metrics_definitions.md` §Discipline & Compliance Metrics (v1.7.0)

**Error responses**

| Status | Condition |
|--------|-----------|
| 500 | Database connection failed or query error |

**Backend:** `backend/routers/analytics.py` (`get_compliance_metrics`)

---

## Known limitations & backlog

- **ValidationService** (`services/validation_service.py`) is a stub and not invoked. Active validation logic lives in `routers/validation.py`. This is tracked as BLG-TECH-03 (consolidate into service layer, deliver alongside BLG-TECH-02).
- **No portfolio_id filter** in the analytics router database queries. Will produce incorrect results in multi-portfolio configurations.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 2.5.0 | 2026-08-11 | v8.6 ST-01 (BLG-FEAT-32, EPIC-01): Added `GET /analytics/trade-plan-completion-rate` — `plans_created`/`plans_completed`/`plans_abandoned`/`completion_rate` for the Performance Analytics page §21. `plans_completed` derived via the `trade_plans.position_id = trade_history.position_id` equijoin. API Contracts & Documentation Owner sign-off. |
| 2.4.0 | 2026-07-09 | v6.8 ST-05 (BLG-FEAT-52, EPIC-02): Added `GET /analytics/tag-performance` — win rate and average R-multiple per trade-plan tag. Reads only `trade_plans.trade_tags` and existing closed-trade linkage; no dependency on `trade_annotations`/PO-02. API Contracts & Documentation Owner sign-off. |
| 2.3.0 | 2026-06-09 | v5.3 ST-05 (BLG-SPEC-50, EPIC-01): Added `GET /analytics/compliance-metrics` — discipline and compliance scalars endpoint. API Contracts & Documentation Owner sign-off. |
| 2.2.0 | 2026-05-23 | ST-01 (BLG-FEAT-36, v4.0): Add `GET /analytics/arc5-compliance` endpoint — Arc 5 compliance metrics (validation_pass_rate_by_rule, events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate). Adds pre_entry_validation_log table. Metrics canonical per metrics_definitions.md §Arc 5 Compliance Metrics. API Contracts & Documentation Owner. |
| 2.1.0 | 2026-04-15 | ST-08 (BLG-FEAT-17, v2.7): Add `GET /analytics/market-correlation` endpoint spec — per-position Pearson correlation vs SPY/FTSE benchmark, portfolio-level equal-weighted average, 252-day default lookback, 8-hour TTL cache, graceful Yahoo Finance fallback. API Contracts & Documentation Owner. |
| 2.0.0 | 2026-03-29 | ST-02 (BLG-FEAT-09, v2.3): Add `last_sync_at` field to `GET /analytics/metrics` response — UTC ISO 8601 timestamp of metrics computation time. Frontend uses this for the Metrics Staleness Indicator (4h default threshold, amber badge when stale). API Contracts & Documentation Owner. |
| 1.5.0 | 2026-02-17 | Initial rewrite: unified endpoint, validation endpoint, known limitations recorded |
| 1.7.0 | 2026-02-17 | Added `entry_price`, `exit_price`, `stop_price` to `trades_for_charts`; R-multiple note added |
| 1.8.1 | 2026-02-21 | BLG-TECH-02 contract: added `severity` field to each validation result object; added `by_severity` aggregation to `summary`; added severity model table; updated metrics validated table to include severity column and `capital_efficiency` row; updated response example; removed resolved known limitation entries for Sharpe variance and capital efficiency currency basis (resolved via BLG-TECH-01). API Contracts Owner. |
| 1.9.2 | 2026-03-12 | ST-03 (EPIC-02 v1.9): Add GET /analytics/cohort endpoint spec — cohort period grouping, response schema, has_enough_data threshold (≥3 periods), avg_r_multiple null rule for missing stop data. ST-04 (EPIC-02 v1.9): Add GET /analytics/r-multiple-distribution endpoint spec — 7 fixed buckets, summary stats (median_r, pct_above_1r, avg_winner_r, avg_loser_r), has_enough_data threshold (≥5 qualifying trades), stop dependency note, hard rule against client-side computation. API Contracts & Documentation Owner. |
| 1.9.0 | 2026-03-02 | BLG-TECH-06 (EPIC-06/S2-06): Add `sharpe_ratio_trade_method` to validated metrics table (severity: critical, formula: Avg Ann Return / Sample StdDev — trade method, tolerance ±0.01). Update response example summary total from 13 → 14 and `by_severity.critical.total` from 3 → 4. Update severity model table critical tier. OBS-01 formally resolved. TASK-21 through TASK-24 complete. API Contracts & Documentation Owner sign-off granted 2026-03-02 (Delegated Authority). |