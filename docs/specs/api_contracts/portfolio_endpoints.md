# portfolio_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.8.1
**Last Updated:** 2026-08-19 (ST-04 correction, EPIC-02, v8.9, BLG-BE-104 — fixed concentration_reason example/field-note text mislabeling sector % of portfolio value as "% of portfolio heat"); prior — 2026-08-18 (ST-05, EPIC-02, v8.9, BLG-FEAT-91 — POST /portfolio/size gains heat_impact_percent response field); prior — 2026-08-18 (ST-04, EPIC-02, v8.9, BLG-BE-104 — POST /portfolio/size gains ticker request field and concentration_adjusted/concentration_reason response fields); prior history retained — see prior entries in version control.
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines **Portfolio** domain endpoints:

- Portfolio overview (working screen)
- Add position (via portfolio)
- Position sizing calculator
- Daily snapshot upsert
- Snapshot history retrieval

Global response envelopes, error shape, defaults, and multi-currency rules are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /portfolio](#get-portfolio)
- [POST /portfolio/position](#post-portfolioposition)
- [POST /portfolio/size](#post-portfoliosize)
- [GET /portfolio/prospective-heat](#get-portfolioprospective-heat)
- [POST /portfolio/snapshot](#post-portfoliosnapshot)
- [GET /portfolio/history](#get-portfoliohistory)

---

## GET /portfolio

**Purpose**

Primary working screen returning cash balances, portfolio totals, and **open positions** with refreshed live prices on every call.

> **Position detail depth:** This endpoint returns a summary view of open positions. For the full enriched position object — including native currency prices, stop context, ATR, FX rates, and journal fields — use `GET /positions`.

**Method & Path**

- `GET /portfolio`

**Idempotency**

- Safe to refresh. Each call refreshes prices.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "cash": 5000.00,
  "cash_balance": 5000.00,
  "total_value": 15000.00,
  "open_positions_value": 10000.00,
  "total_pnl": 1000.00,
  "initial_value": 14000.00,
  "net_deposits": 14000.00,
  "live_fx_rate": 1.3642,
  "last_updated": "2026-02-17T10:30:00Z",
  "current_drawdown_percent": -8.20,
  "peak_portfolio_value": 16340.00,
  "portfolio_heat_percent": 4.75,
  "position_risks": [
    { "ticker": "NVDA", "position_risk_gbp": 87.50 }
  ],
  "positions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "ticker": "NVDA",
      "market": "US",
      "entry_date": "2026-02-01",
      "entry_price": 622.00,
      "shares": 10.5,
      "current_price": 570.87,
      "current_value": 5994.14,
      "pnl": 851.57,
      "pnl_pct": 16.56,
      "current_stop": 607.50,
      "holding_days": 14,
      "status": "open",
      "display_status": "PROFITABLE",
      "fx_rate": 1.2650,
      "grace_period": false,
      "grace_days_remaining": null,
      "live_fx_rate": 1.2750
    }
  ]
}
```

#### Field notes (portfolio-level)

- `cash` and `cash_balance` are both the available cash balance. `cash_balance` is retained for legacy compatibility.
- `total_value` is cash plus open positions value.
- `open_positions_value` is the sum of current values across all open positions.
- `total_pnl` is realised plus unrealised P&L.
- `net_deposits` is total deposits minus total withdrawals. Used as the cost basis for portfolio-level return calculations.
- `last_updated` is an ISO 8601 timestamp.
- `positions` is an array of open positions; returns `[]` if none.
- `current_drawdown_percent` is the percentage decline of the current portfolio value from the all-time peak value in `portfolio_history`. Calculated as `(total_value - peak_portfolio_value) / peak_portfolio_value × 100`. Result is ≤ 0.0; zero means the portfolio is at its all-time high. Defaults to `0.0` when no `portfolio_history` exists. See `metrics_definitions.md` §Current Drawdown for the canonical definition.
- `peak_portfolio_value` is the all-time high of `portfolio_history.total_value` across all recorded snapshots (not period-scoped). Expressed in GBP. Defaults to `0.0` when no `portfolio_history` exists.
- `portfolio_heat_percent` is total open-position risk (sum of `position_risks[].position_risk_gbp`) as a percentage of `total_value`. Rounded to 2 d.p. `0.0` when `total_value` is `0` or no open positions carry risk (no `initial_stop`). **Documentation backfill (ST-12, EPIC-03, v7.10, BLG-QA-128)** — this field has always been returned by `services/portfolio_service.py::get_portfolio_summary()` and is consumed by `src/pages/RiskDashboard.js`; it was simply never added to this contract's response schema until now, surfaced by a consumer-driven contract check.
- `position_risks` is an array of `{ticker, position_risk_gbp}` — GBP risk (entry price minus stop, converted to GBP) per open position with a set `initial_stop`; positions without one are excluded. Same documentation-backfill note as `portfolio_heat_percent` above — consumed by `src/pages/RiskDashboard.js` for the risk-per-position breakdown.

#### Field notes (position summary object)

The position objects returned here are a **summary shape**. Key omissions versus the full object from `GET /positions`:

| Omitted field | Available at |
|---------------|-------------|
| `initial_stop` | `GET /positions` |
| `atr_value` | `GET /positions` |
| `entry_note`, `exit_note` | `GET /positions` |
| `tags` | `GET /positions` |

**`pnl_pct`** is the percentage P&L field in this position summary object — the percentage return relative to entry price, expressed as a signed percentage. In trade history responses (`GET /trades`), the same value appears as both `pnl_pct` and `pnl_percent` for backward compatibility; in position objects only `pnl_pct` is returned.

**`current_price`** is always expressed in GBP, regardless of the instrument's native currency. For US positions, the live USD price is converted to GBP using `live_fx_rate` at time of call. `entry_price` is in native currency (USD for US, GBP for UK). `fx_rate` is the stored rate at time of entry; `live_fx_rate` is the rate used for the current price conversion.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## POST /portfolio/position

**Purpose**

Create a new position based on user-entered broker execution details. Supports fractional shares. Creates the position and deducts the total cost from available cash.

**Method & Path**

- `POST /portfolio/position`

**Idempotency**

- Mutating (non-idempotent). Repeating the request creates additional positions and changes cash.

### Request

#### Body

```json
{
  "ticker": "NVDA",
  "market": "US",
  "entry_date": "2026-02-17",
  "shares": 10.5,
  "entry_price": 850.00,
  "fx_rate": 1.3642,
  "atr_value": 15.32,
  "stop_price": 780.00,
  "entry_note": "Breakout above $800 resistance",
  "tags": ["momentum", "breakout"]
}
```

#### Required fields

- `ticker` (string, max 20)
- `entry_date` (string, `YYYY-MM-DD`)
- `shares` (number, min `0.0001`)
- `entry_price` (number, min `0.01`)

#### Optional fields

- `market` (string: `"US"` or `"UK"`; default: auto-detect from ticker suffix)
- `fx_rate` (number; required for US if not auto-detected)
- `atr_value` (number; auto-fetched by server if not provided)
- `stop_price` (number; calculated as `entry_price − (5 × ATR)` if not provided)
- `entry_note` (string, max 500; empty string treated as `null`)
- `tags` (array; max 10; each max 20 characters; lowercase, numbers, hyphens only)
- `trade_plan_id` (string, UUID; ST-01 v7.3 — explicit link from the "Start Trade from Plan" action. When provided, this exact trade plan is linked (`position_id` set, `status` set to `active`) in place of the ticker/market best-effort auto-link (BLG-BE-46). Silently ignored if the plan does not exist, belongs to another portfolio, or is already linked to a position — position creation is never blocked by a link failure.)

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "ticker": "NVDA",
  "total_cost": 8925.00,
  "fees_paid": 10.00,
  "entry_price": 850.00,
  "initial_stop": 780.00,
  "remaining_cash": 4075.00,
  "position_id": "550e8400-e29b-41d4-a716-446655440000",
  "fx_rate_used": 1.3642,
  "trade_plan_linked": true,
  "trade_plan_id": "660e8400-e29b-41d4-a716-446655440111"
}
```

#### Response fields

| Field | Type | Description |
|-------|------|-------------|
| `fx_rate_used` | number | ST-03 (EPIC-01, v8.0): the effective GBP/USD rate applied to this entry (user-provided `fx_rate` if supplied, else the live rate at entry time). `1.0` for UK tickers. Same value persisted to `positions.fx_rate`. Per `strategy_rules.md §4.1.5`'s auditability requirement — previously computed and persisted but not returned in this response. |
| `trade_plan_linked` | boolean | ST-03 (BLG-BE-91, EPIC-02, v8.6): `true` if this position was linked to a trade plan at creation — either the explicit `trade_plan_id` supplied in the request, or the best-effort ticker/market auto-match (`BLG-BE-46`). `false` if no trade plan was linked (position created with no pre-trade plan behind it). Surfaces the previously-silent linkage outcome so the entry flow is not left to infer it; does not block position creation either way. |
| `trade_plan_id` | string \| null | ST-03 (BLG-BE-91, EPIC-02, v8.6): UUID of the trade plan that was linked, or `null` when `trade_plan_linked` is `false`. |

### Validation rules & constraints

- `ticker` must be a valid format; max 20 characters.
- `entry_date` must be a valid date and must not be in the future.
- `shares` must be greater than 0.
- `entry_price` must be greater than 0.
- `tags` must follow tag rules (lowercase letters, numbers, hyphens only; max 20 characters each; max 10 tags).

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Insufficient funds
- `400` Invalid ticker format
- `400` Invalid date (future date)
- `400` Invalid shares (negative or zero)
- `400` Invalid tag format

---

## POST /portfolio/size

**Purpose**

Calculate a suggested share quantity for a prospective new position based on portfolio risk parameters.

Returns a deterministic sizing result including suggested shares, risk amount, estimated cost, and cash feasibility. Does not create a position or mutate any state. The backend is the authoritative source of all calculations — the frontend must not derive or recalculate any returned value.

All calculation rules are defined canonically in `strategy_rules.md §4.1`.

**Method & Path**

- `POST /portfolio/size`

**Idempotency**

- Idempotent for the same inputs. Safe to call repeatedly, including on debounced keystrokes. Does not mutate portfolio state, cash balances, or position records.

### Request

#### Body

```json
{
  "entry_price": 850.00,
  "stop_price": 780.00,
  "risk_percent": 1.00,
  "market": "US",
  "fx_rate": 1.3642,
  "ticker": "MSFT"
}
```

#### Required fields

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `entry_price` | number | > 0 | Prospective entry price in the instrument's native currency (GBP for UK, USD for US) |
| `stop_price` | number | > 0 | Intended initial stop price in the instrument's native currency |
| `risk_percent` | number | > 0 | Percentage of portfolio value to risk on this position, e.g. `1.00` for 1% |

#### Optional fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `market` | string | `"UK"` | `"US"` or `"UK"`. Used for fee estimation in the cash feasibility gate |
| `fx_rate` | number | Live system rate | User-provided FX rate override for US positions. If omitted, the system live rate is used |
| `ticker` | string | `null` | Candidate ticker (ST-04, BLG-BE-104). When provided, enables sector-concentration-aware size adjustment — see `concentration_adjusted`/`concentration_reason` below. Omitting it preserves sizing behaviour exactly as it was before ST-04 (no adjustment attempted) |

### Response (200) — Valid result

Response uses the standard success envelope from **conventions.md**.

```json
{
  "status": "ok",
  "data": {
    "valid": true,
    "suggested_shares": 17.8571,
    "risk_amount": 125.00,
    "stop_distance": 70.00,
    "estimated_cost": 15178.57,
    "estimated_fees": 0.00,
    "fx_rate_used": 1.3642,
    "cash_sufficient": true,
    "available_cash": 20000.00,
    "concentration_adjusted": false,
    "concentration_reason": null,
    "heat_impact_percent": 0.80
  }
}
```

### Response (200) — Concentration-reduced (ST-04, BLG-BE-104)

```json
{
  "status": "ok",
  "data": {
    "valid": true,
    "suggested_shares": 8.9286,
    "risk_amount": 125.00,
    "stop_distance": 70.00,
    "estimated_cost": 7589.29,
    "estimated_fees": 0.00,
    "fx_rate_used": 1.3642,
    "cash_sufficient": true,
    "available_cash": 20000.00,
    "concentration_adjusted": true,
    "concentration_reason": "Reduced 50% — 2 open positions already in Technology (25.0% of portfolio value).",
    "heat_impact_percent": 0.40
  }
}
```

### Response (200) — Insufficient cash

```json
{
  "status": "ok",
  "data": {
    "valid": true,
    "suggested_shares": 17.8571,
    "risk_amount": 125.00,
    "stop_distance": 70.00,
    "estimated_cost": 15178.57,
    "estimated_fees": 0.00,
    "fx_rate_used": 1.3642,
    "cash_sufficient": false,
    "available_cash": 8000.00,
    "max_affordable_shares": 9.3750,
    "concentration_adjusted": false,
    "concentration_reason": null,
    "heat_impact_percent": 0.80
  }
}
```

### Response (200) — Invalid inputs

```json
{
  "status": "ok",
  "data": {
    "valid": false,
    "reason": "INVALID_STOP_DISTANCE",
    "reason_detail": "Stop price must be below entry price"
  }
}
```

### Field notes

| Field | Notes |
|-------|-------|
| `valid` | `true` if inputs satisfy all validity rules in `strategy_rules.md §4.1.4`. `false` if any rule is breached or portfolio value snapshot is missing |
| `suggested_shares` | Share quantity floored to 4 decimal places per canonical spec. Present only when `valid: true` |
| `risk_amount` | `PortfolioValue × RiskPercent` in GBP |
| `stop_distance` | `EntryPrice − StopPrice` in the instrument's native currency |
| `estimated_cost` | `SuggestedShares × EntryPrice + EstimatedFees` in GBP |
| `estimated_fees` | Fee estimate using current settings parameters (commission, stamp duty, FX fee as applicable) |
| `fx_rate_used` | The FX rate applied in this calculation. Always returned when `valid: true` for auditability. `1.0` for UK positions |
| `cash_sufficient` | `true` if `estimated_cost <= available_cash` |
| `available_cash` | Current `portfolios.cash` in GBP. Returned when `valid: true` to support cash display in the UI |
| `max_affordable_shares` | Present and always populated when `cash_sufficient: false`. Floored to 4 decimal places. Maximum share quantity the user can afford given `available_cash` |
| `concentration_adjusted` | (ST-04, BLG-BE-104) `true` when `suggested_shares` was reduced from the volatility-only baseline due to sector concentration against the user's existing open positions. Present when `valid: true`; always `false` when `ticker` was omitted from the request |
| `concentration_reason` | (ST-04, BLG-BE-104) Human-readable reason string, e.g. `"Reduced 50% — 2 open positions already in Technology (25.0% of portfolio value)."`, or a non-reducing flag message when exposure is elevated but below the reduce threshold. `null` when no concentration condition applies (including whenever `ticker` was omitted). This is the string the frontend renders verbatim — see `trade_plan.md §10.7` |
| `heat_impact_percent` | (ST-05, BLG-FEAT-91) Incremental portfolio heat impact of adding `suggested_shares` at these terms — same calculation as `GET /portfolio/prospective-heat`'s `incremental_heat_percent` (reused, not duplicated; see `services/portfolio_service.py::calculate_prospective_heat`). Present when `valid: true`. `null` when `suggested_shares <= 0` or the underlying portfolio-value/position data is unavailable — this is not an error condition, callers render it as "—". Included so `PositionSizingWidget` (§10.7) and the What-If Sizing Preview (§5d) can source heat impact from this single call rather than a second endpoint call |
| `reason` | Machine-readable reason code. Present only when `valid: false`. See reason codes table below |
| `reason_detail` | Human-readable description of the invalid condition. Present only when `valid: false`. **For development and logging use only — must not be used as user-facing display text.** The frontend derives its own plain-language messages from the `reason` code |

### Reason codes

| Code | Condition |
|------|-----------|
| `INVALID_RISK_PERCENT` | `risk_percent <= 0` |
| `INVALID_ENTRY_PRICE` | `entry_price <= 0` |
| `INVALID_STOP_PRICE` | `stop_price <= 0` |
| `INVALID_STOP_DISTANCE` | `stop_price >= entry_price` (stop distance is zero or negative) |
| `NO_PORTFOLIO_VALUE_SNAPSHOT` | No snapshot exists in `portfolio_history`. Backend cannot determine portfolio value for risk calculation |

### Validation rules & constraints

- All three required fields must be present. Missing fields return HTTP 400.
- Business rule failures (invalid inputs per `strategy_rules.md §4.1.4`) return HTTP 200 with `valid: false` — not HTTP 400.
- `market` must be `"US"` or `"UK"` if provided. Invalid market value returns HTTP 400.
- `fx_rate` must be > 0 if provided. Invalid FX rate returns HTTP 400.
- The endpoint never auto-fills, stores, or applies `SuggestedShares` to any position. It is a read-only calculation.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Missing required field (`entry_price`, `stop_price`, or `risk_percent`)
- `400` Invalid `market` value
- `400` Invalid `fx_rate` value (≤ 0)
- `500` Internal error

---

## POST /portfolio/snapshot

**Purpose**

Create or update a **daily portfolio snapshot** (idempotent upsert by portfolio + date). Intended to be called once per day, typically automated at market close.

**Method & Path**

- `POST /portfolio/snapshot`

**Idempotency**

- Idempotent upsert: calling multiple times on the same day updates the same snapshot record for that date.

### Request

No body required.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "id": "650e8400-e29b-41d4-a716-446655440000",
  "snapshot_date": "2026-02-17",
  "total_value": 15000.00,
  "cash_balance": 5000.00,
  "positions_value": 10000.00,
  "total_pnl": 1000.00,
  "position_count": 3,
  "created_at": "2026-02-17T10:30:00Z"
}
```

### Notes

- If a snapshot already exists for today's date, the backend updates it in place.
- If no snapshot exists for today, the backend creates a new one.
- Snapshots feed the Sharpe ratio (portfolio method) and drawdown calculations in `GET /analytics/metrics`. A minimum of 30 snapshots is required for the portfolio-method Sharpe ratio.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /portfolio/history

**Purpose**

Retrieve historical portfolio snapshots for charting and analytics.

**Method & Path**

- `GET /portfolio/history`

**Idempotency**

- Safe to refresh.

### Request

#### Query parameters

- `days` (integer, optional): number of days to retrieve. Default: `30`.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema (array)

```json
[
  {
    "id": "650e8400-e29b-41d4-a716-446655440000",
    "snapshot_date": "2026-02-17",
    "total_value": 15000.00,
    "cash_balance": 5000.00,
    "positions_value": 10000.00,
    "total_pnl": 1000.00,
    "position_count": 3
  }
]
```

### Notes

- Returns an empty array `[]` if no snapshots exist.
- Sorted by `snapshot_date` ascending (oldest first) to support charting.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /portfolio/prospective-heat

**Purpose**

Calculate what the portfolio heat percentage would be if a prospective new position were added. Returns the current heat plus the incremental heat from the proposed trade. Does not create a position or mutate any state.

Calculation rules: `docs/specs/metrics_definitions.md §Portfolio Heat`.

**Method & Path**

- `GET /portfolio/prospective-heat`

**Idempotency**

- Read-only. Safe to call repeatedly, including on debounced keystrokes. Does not mutate portfolio state, cash balances, or position records.

### Request

#### Query Parameters

| Parameter | Type | Required | Constraint | Description |
|-----------|------|----------|------------|-------------|
| `ticker` | string | Yes | Non-empty | Instrument ticker (informational only — used for the response label) |
| `shares` | number | Yes | > 0 | Number of shares in the prospective position |
| `entry_price` | number | Yes | > 0 | Prospective entry price in the instrument's native currency |
| `stop_price` | number | Yes | > 0 | Prospective stop price in the instrument's native currency |
| `market` | string | No | `"UK"` or `"US"` | Default: `"UK"`. Used for FX conversion |
| `fx_rate` | number | No | > 0 | FX rate override for US positions. If omitted for US, the system live rate is used |

**Example:**
```
GET /portfolio/prospective-heat?ticker=AAPL&shares=10&entry_price=185.00&stop_price=175.00&market=US
```

### Response (200) — Valid result

Response uses the standard success envelope from **conventions.md**.

```json
{
  "status": "ok",
  "data": {
    "valid": true,
    "current_heat_percent": 8.4,
    "prospective_heat_percent": 10.1,
    "incremental_heat_percent": 1.7,
    "prospective_risk_gbp": 85.00,
    "portfolio_value_gbp": 5000.00,
    "ticker": "AAPL",
    "fx_rate_used": 1.3642
  }
}
```

#### Response fields

| Field | Type | Description |
|-------|------|-------------|
| `valid` | boolean | `true` if all inputs are valid and calculation succeeded |
| `current_heat_percent` | number | Current portfolio heat before adding the prospective position (2 dp) |
| `prospective_heat_percent` | number | Portfolio heat if the prospective position were added (2 dp) |
| `incremental_heat_percent` | number | Difference: `prospective_heat_percent − current_heat_percent` (2 dp) |
| `prospective_risk_gbp` | number | GBP risk of the prospective position: `(entry_price − stop_price) × shares / fx_rate_used` |
| `portfolio_value_gbp` | number | Current portfolio value used as the denominator (from `GET /portfolio`) |
| `ticker` | string | Echo of the `ticker` query parameter |
| `fx_rate_used` | number | ST-03 (EPIC-01, v8.0): the effective GBP/USD rate applied (user-provided `fx_rate` if supplied, else the live rate). `1.0` for UK tickers. Per `strategy_rules.md §4.1.5`'s auditability requirement — previously computed but not returned. |

### Response (200) — Invalid inputs

```json
{
  "status": "ok",
  "data": {
    "valid": false,
    "error": "stop_price must be less than entry_price"
  }
}
```

**Business rule failures that return `valid: false`:**
- `stop_price >= entry_price` (stop must be below entry)
- `shares <= 0`
- `entry_price <= 0` or `stop_price <= 0`
- Portfolio value is zero (cannot calculate heat percentage)

### Calculation

```text
prospective_risk_gbp    = (entry_price − stop_price) × shares / fx_rate_used
current_risk_gbp        = Sum(position_risk_gbp) for all open positions  [from portfolio_service]
total_risk_gbp          = current_risk_gbp + prospective_risk_gbp
prospective_heat_pct    = total_risk_gbp / portfolio_value_gbp × 100
current_heat_pct        = current_risk_gbp / portfolio_value_gbp × 100
incremental_heat_pct    = prospective_heat_pct − current_heat_pct

fx_rate_used:
  market = "UK"  → 1.0 (GBP instruments; no conversion needed)
  market = "US"  → fx_rate parameter if provided, else system live rate
```

All results are rounded to 2 decimal places.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-02-17 | Initial spec — GET /portfolio, POST /portfolio/position, POST /portfolio/size, POST /portfolio/snapshot, GET /portfolio/history |
| 1.8.2 | 2026-02-25 | BLG-FEAT-01: Added `current_drawdown_percent` and `peak_portfolio_value` fields to GET /portfolio portfolio-level response (QWB pre-alignment D1) |
| 1.9.0 | 2026-03-02 | S2-07 (EPIC-06/BLG-TECH-08): Spec updated to match live `portfolio_service.py` implementation. Position object example and field notes corrected — removed stale fields (`current_price_native`, `stop_price`, `stop_price_native`, `pnl_percent`); added live fields (`current_value`, `pnl_pct`, `current_stop`, `fx_rate`, `grace_days_remaining`, `live_fx_rate`). Key omissions table corrected (fx_rate/live_fx_rate ARE returned by this endpoint). pnl_pct note corrected. OBS-QWB-R1-01 resolved. TASK-25/26/27 complete. API Contracts owner sign-off granted 2026-03-02 (Delegated Authority). |
| 2.0.0 | 2026-03-17 | ST-13 (EPIC-04): GET /portfolio/prospective-heat added — calculates portfolio heat including a prospective new position. Response shape, query parameters, calculation rules, and business rule failures defined. |
| 2.5.0 | 2026-07-27 | ST-02 (EPIC-02, v7.9, BLG-FEAT-67): GET /portfolio/sector-regime-trend added — weekly-bucketed sector concentration + regime status trend, backed by a new sector_regime_history table (data_model.md, going-forward capture only). Documents the corrected data-dependency premise (Metrics Definitions & Analytics Owner amendment) — no prior historical sector/regime data existed to aggregate. |
| 2.5.1 | 2026-07-29 | ST-12 (EPIC-03, v7.10, BLG-QA-128): documentation backfill — `portfolio_heat_percent` and `position_risks` added to GET /portfolio's response schema and field notes. Both fields have always been returned by the live implementation and are consumed by `src/pages/RiskDashboard.js`; they were simply never documented here. Surfaced by a consumer-driven contract check (`scripts/check_consumer_contract_drift.js`). No behaviour change. |
| 2.6.0 | 2026-07-30 | ST-03 (EPIC-01, v8.0, BLG-SPEC-107): FX conversion audit trail completeness check against `strategy_rules.md §4.1.5`'s "FX rate used must be returned ... for auditability" requirement. Found and fixed 3 gaps where an FX-derived GBP amount was computed but the rate used was never returned: `POST /portfolio/position` (`fx_rate_used` added — was already persisted to `positions.fx_rate` but never surfaced in this response), `GET /portfolio/prospective-heat` (`fx_rate_used` added), and `GET /portfolio/pre-entry-validation`'s `cash_constraint` check (`fx_rate_used` added). `POST /portfolio/size` was already compliant (`fx_rate_used` already returned). |
| 2.6.1 | 2026-08-12 | ST-03 (EPIC-02, v8.6, BLG-BE-91): `POST /portfolio/position` response gains `trade_plan_linked` (boolean) and `trade_plan_id` (UUID or null) — surfaces whether a trade plan was linked at position creation (explicit `trade_plan_id` request field, or the ticker/market best-effort auto-match) instead of only a server-side log line. Part of the "trade-plan linkage is the enforced default path, not silently optional" story; see `docs/specs/data_model.md` DS-12 for the paired DB-level safeguard. |
| 2.7.0 | 2026-08-18 | ST-04 (EPIC-02, v8.9, BLG-BE-104): `POST /portfolio/size` gains optional request field `ticker` and response fields `concentration_adjusted` (boolean) and `concentration_reason` (string or null) — reflects the user's existing open-position sector concentration in the suggested size, reusing (not redefining) `strategy_rules.md §4.2.2`'s canonical 30% threshold. See `trade_plan.md §10.7` for the frontend display contract. |
| 2.8.0 | 2026-08-18 | ST-05 (EPIC-02, v8.9, BLG-FEAT-91): `POST /portfolio/size` gains response field `heat_impact_percent` (number or null) — incremental portfolio heat impact of the suggested position, reusing `GET /portfolio/prospective-heat`'s calculation (`services/portfolio_service.py::calculate_prospective_heat`, extracted this story) rather than a second endpoint call. Feeds the new What-If Sizing Preview panel (`trade_plan.md §5d`) and `PositionSizingWidget` (§10.7). |
| 2.8.1 | 2026-08-19 | ST-04 correction (EPIC-02, v8.9, BLG-BE-104): fixed `concentration_reason`'s example/field-note text, which mislabeled the sector's share of total portfolio *value* as "% of portfolio heat" — a distinct, already-defined metric on this same endpoint (`heat_impact_percent`, ST-05 above). Found by agent-mediated Director of Quality review of PR #1453. No response shape or calculation change — text only, matching the corrected `backend/services/sizing_service.py` wording. |

---

## GET /portfolio/drawdown-status

Returns current portfolio drawdown status vs a configurable threshold.

**Drawdown calculation:**
```
current_drawdown_pct = (30d_peak − current_total_value) / 30d_peak × 100
30d_peak             = MAX(total_value) over portfolio_history last 30 days
threshold_pct        = settings.drawdown_threshold_pct (default 10.0; range 5–50)
threshold_breached   = current_drawdown_pct >= threshold_pct
```

**Response (threshold not breached):**
```json
{ "status": "ok", "data": { "current_drawdown_pct": 3.2, "threshold_pct": 10.0, "threshold_breached": false } }
```

**Response (threshold breached):**
```json
{ "status": "ok", "data": {
    "current_drawdown_pct": 12.4, "threshold_pct": 10.0, "threshold_breached": true,
    "portfolio_heat_pct": 6.3, "regime_status": "Bearish",
    "positions_by_state": { "GRACE": 2, "PROFITABLE": 1, "LOSING": 3, "EXIT ZONE": 1, "UNKNOWN": 0 }
} }
```

**Error/missing data:** `threshold_breached: false` returned silently; positions page loads normally.

---

## GET /portfolio/concentration-status

Returns positions and sectors exceeding configurable concentration thresholds.

**Calculation:**
```
position_heat_pct     = position_risk_gbp / total_risk_gbp × 100
sector_concentration  = sum(sector_risk_gbp) / total_risk_gbp × 100  [DS-03 sector field]
pos_threshold_pct     = settings.concentration_position_threshold_pct (default 15.0; range 5–50)
sector_threshold_pct  = settings.concentration_sector_threshold_pct (default 30.0; range 10–80)
```

Positions without sector data are excluded from the sector calculation. No error raised.

**Response:**
```json
{ "status": "ok", "data": {
    "any_breach": true,
    "position_threshold_pct": 15.0, "sector_threshold_pct": 30.0,
    "breaching_positions": [{ "ticker": "NVDA", "heat_pct": 22.1, "limit_pct": 15.0 }],
    "breaching_sectors": [{ "sector": "Technology", "concentration_pct": 41.2, "limit_pct": 30.0 }]
} }
```

**Changelog (portfolio_endpoints.md):**

| Version | Date | Change |
|---------|------|--------|
| 2.1.0 | 2026-05-14 | ST-04/ST-06 (EPIC-02 v3.4): Added GET /portfolio/drawdown-status and GET /portfolio/concentration-status (IT-04/IT-05 Arc 3). |
| 2.2.0 | 2026-05-15 | ST-02 (EPIC-01, v3.5): Add GET /portfolio/paper-positions — IT-06 Alpaca paper trading positions panel. |
| 2.4.0 | 2026-06-23 | ST-06 (EPIC-03, v6.1): Add GET /portfolio/sector-weights — open-position sector exposure breakdown for SectorHeatMap component. |
| 2.3.0 | 2026-05-20 | ST-02 (EPIC-01, v3.8): Add GET /portfolio/pre-entry-validation — SI-01 non-blocking advisory pre-entry rule check (§13 PASS). |

---

## GET /portfolio/paper-positions

Returns current Alpaca paper account positions with P&L. Returns `{"paper_tracking_enabled": false}` when `ALPACA_PAPER_API_KEY` is not configured.

§13 compliance: display-only; no automated order execution.

**Response (200) — credentials configured, positions exist:**
```json
{
  "status": "ok",
  "paper_tracking_enabled": true,
  "positions": [
    {
      "ticker": "AAPL",
      "paper_entry_price": 170.50,
      "current_market_price": 180.00,
      "paper_pnl_usd": 950.00,
      "paper_pnl_pct": 5.57,
      "date_opened": null,
      "position_size": 100
    }
  ]
}
```

**Response (200) — credentials not configured:**
```json
{"paper_tracking_enabled": false}
```

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| paper_tracking_enabled | boolean | false when ALPACA_PAPER_API_KEY absent |
| positions | array | Paper account positions |
| positions[].ticker | string | Ticker symbol |
| positions[].paper_entry_price | float | Average entry price from Alpaca paper account |
| positions[].current_market_price | float | Current market price |
| positions[].paper_pnl_usd | float | Unrealised P&L in USD |
| positions[].paper_pnl_pct | float | Unrealised P&L as percentage |
| positions[].date_opened | string \| null | Date opened (null — not available from Alpaca positions API) |
| positions[].position_size | float | Number of shares |

**Errors:**

| Code | Condition |
|------|-----------|
| 500 | Alpaca API error or network failure |

---

## GET /portfolio/pre-entry-validation

Returns an advisory pre-entry validation result for a proposed position. All checks are non-blocking — results are informational and do not prevent trade plan submission.

**§13 compliance:** Decision support only. Not a submission gate. Decision record: `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`
**Strategy reference:** `claude/strategy/strategy_rules.md §4.2`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ticker | string | Yes | Ticker symbol |
| quantity | float | Yes | Proposed number of shares |
| market | string | No | `US` (default) or `UK` |
| entry_price | float | No | Enables sizing validity check (§4.1.4) |
| stop_price | float | No | Enables sizing validity check (§4.1.4) |

### Response (200 OK)

```json
{
  "status": "ok",
  "data": {
    "ticker": "AAPL",
    "market": "US",
    "quantity": 10,
    "advisory_status": "warn",
    "override_required": true,
    "checks": [
      {
        "rule": "regime_gate",
        "status": "pass",
        "detail": "US market is Risk-On (SPY above 200-day MA)",
        "severity": "fail"
      },
      {
        "rule": "cash_constraint",
        "status": "pass",
        "detail": "Estimated cost £2,150.00 within available cash £5,000.00",
        "severity": "fail",
        "estimated_cost_gbp": 2150.0,
        "available_cash_gbp": 5000.0,
        "fx_rate_used": 1.3642
      },
      {
        "rule": "sector_concentration",
        "status": "warn",
        "detail": "Projected Technology sector allocation 32.4% would exceed 30% advisory limit",
        "severity": "warn",
        "sector": "Technology",
        "projected_sector_pct": 32.4,
        "threshold_pct": 30.0
      },
      {
        "rule": "earnings_proximity",
        "status": "pass",
        "detail": "Next earnings 2026-07-30 (71 days) — outside 5-day proximity window",
        "severity": "warn",
        "earnings_date": "2026-07-30",
        "days_until_earnings": 71
      },
      {
        "rule": "sizing_validity",
        "status": "skipped",
        "detail": "Provide entry_price and stop_price query params for sizing validity check",
        "severity": "fail"
      }
    ]
  }
}
```

### Response fields — `data`

| Field | Type | Description |
|-------|------|-------------|
| ticker | string | Ticker from query |
| market | string | Market from query (`US` or `UK`) |
| quantity | float | Quantity from query |
| advisory_status | string | Aggregate: `pass` \| `warn` \| `fail` (skipped excluded) |
| override_required | boolean | `true` when advisory_status is `warn` or `fail` |
| checks | array | Per-rule check results (5 rules) |

### Response fields — `checks[]`

| Field | Type | Description |
|-------|------|-------------|
| rule | string | Rule identifier: `regime_gate` \| `cash_constraint` \| `sector_concentration` \| `earnings_proximity` \| `sizing_validity` |
| status | string | `pass` \| `warn` \| `fail` \| `skipped` |
| detail | string | Human-readable explanation |
| severity | string | Worst-case severity of this check: `fail` or `warn` |
| fx_rate_used | number | `cash_constraint` only (ST-03, EPIC-01, v8.0): GBP/USD rate used to convert the US-ticker live price to GBP for `estimated_cost_gbp`. `1.0` for UK tickers (no conversion applied). Per `strategy_rules.md §4.1.5`'s auditability requirement. |

Additional fields per rule type when available: `estimated_cost_gbp`, `available_cash_gbp`, `sector`, `projected_sector_pct`, `threshold_pct`, `earnings_date`, `days_until_earnings`, `stop_distance`.

### Notes

- `skipped` status: data required for the check is unavailable (no live price, no sector data, params not supplied). Skipped checks are excluded from `advisory_status` aggregation.
- `sizing_validity` check requires both `entry_price` and `stop_price` query params; returns `skipped` if either is absent.
- `earnings_proximity` applies to US tickers only; returns `skipped` for UK tickers.
- Override acknowledgement recorded on trade plan object (ST-03) is metadata only — no effect on any calculation.

**Errors:**

| Code | Condition |
|------|-----------|
| 422 | Missing required query params (`ticker` or `quantity`) |

---

## GET /portfolio/red-flag-journal

Returns a paginated log of strategy deviation events. Populated when the operator acknowledges a pre-entry validation override or dismisses a strategy prompt.

**§13 compliance:** Display-only audit log. No automated decisions or recommendations. Decision record: `docs/product/decisions/` (SI-03, v3.9).

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1, min: 1) |
| page_size | integer | No | Items per page (default: 20, max: 100) |
| event_type | string | No | Filter by event type: `pre_entry_override`, `checklist_skipped`, `stop_prompt_dismissed`, `drawdown_prompt_dismissed` |
| ticker | string | No | Filter by ticker symbol (case-insensitive) |
| since | string | No | ISO date filter — return events on or after this timestamp |
| severity | string | No | Filter by severity level: `info` \| `warning` \| `critical` (v4.6 ST-09) |

### Response (200 OK)

```json
{
  "status": "ok",
  "data": {
    "total": 12,
    "page": 1,
    "page_size": 20,
    "items": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "event_type": "pre_entry_override",
        "ticker": "AAPL",
        "position_id": null,
        "context": { "source": "trade_plan", "override_acknowledged": true },
        "created_at": "2026-05-22T10:30:00+00:00",
        "severity": "warning"
      }
    ]
  }
}
```

### Response fields — `data`

| Field | Type | Description |
|-------|------|-------------|
| total | integer | Total matching events |
| page | integer | Current page |
| page_size | integer | Items per page |
| items | array | Event records |

### Response fields — `items[]`

| Field | Type | Description |
|-------|------|-------------|
| id | UUID string | Event ID |
| event_type | string | `pre_entry_override` \| `checklist_skipped` \| `stop_prompt_dismissed` \| `drawdown_prompt_dismissed` |
| ticker | string | Ticker symbol (uppercase) |
| position_id | UUID string \| null | Linked position ID if available |
| context | object \| null | JSON context snapshot at event time |
| created_at | ISO 8601 string | Event timestamp |
| severity | string | Event severity: `info` \| `warning` \| `critical` (v4.6 ST-09; defaults: `pre_entry_override` → `warning`, SI-02 drift events → `critical`, others → `info`) |

### Errors

| Code | Condition |
|------|-----------|
| 500 | Database error |



## GET /portfolio/sector-weights

Returns open-position sector breakdown by market value exposure.

**Source:** ST-06, EPIC-03, v6.1

### Request

No parameters required.

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "sectors": [
      { "sector_name": "Technology", "position_count": 3, "exposure_pct": 42.5 },
      { "sector_name": "Financials", "position_count": 2, "exposure_pct": 31.0 },
      { "sector_name": "Healthcare", "position_count": 1, "exposure_pct": 18.2 },
      { "sector_name": "Industrials", "position_count": 1, "exposure_pct": 8.3 }
    ],
    "total_positions": 7,
    "concentration_alert": true
  }
}
```

### Response fields — `data`

| Field | Type | Description |
|-------|------|-------------|
| sectors | array | Sectors sorted by exposure_pct descending |
| sectors[].sector_name | string | Sector label (from `positions.sector`; falls back to `"Unclassified"`) |
| sectors[].position_count | integer | Number of open positions in this sector |
| sectors[].exposure_pct | number | Market value of sector / total open positions market value × 100 (1 dp) |
| total_positions | integer | Total open position count |
| concentration_alert | boolean | `true` when any single sector `exposure_pct ≥ 40` |

### Notes

- Positions missing a `sector` value are grouped under `"Unclassified"`.
- Market value uses `current_price` if available, else falls back to `entry_price`.
- US positions are converted to GBP using the live FX rate.
- On any error, returns `{"sectors": [], "total_positions": 0, "concentration_alert": false}` — does not propagate exceptions to the UI.

### Errors

| Code | Condition |
|------|-----------|
| 500 | Internal error (silently falls back to empty sectors response) |

---

## GET /portfolio/sector-regime-trend

Weekly-bucketed historical trend of sector concentration and market regime status (ST-02, EPIC-02, v7.9, BLG-FEAT-67).

**Source:** ST-02, EPIC-02, v7.9

**Data dependency note (required correction — Metrics Definitions & Analytics Owner amendment, 2026-07-27):** unlike `GET /portfolio/sector-weights` above (computed live on every call), this endpoint reads from a new `sector_regime_history` table populated once per weekday by the existing daily snapshot job (`POST /portfolio/snapshot` → `portfolio_service.create_daily_snapshot`), starting from this story's ship date. **No historical sector or regime data existed before this table** — neither `GET /portfolio/sector-weights` nor `GET /market/status` ever persisted their live-computed figures anywhere, so there is nothing to retroactively backfill from. This corrects the original backlog item's premise ("purely a historical view of data already captured", "no new data collection required") — that premise did not hold; this endpoint introduces new data collection, going forward only. Immediately after ship, this endpoint returns `insufficient_history: true` (0 weeks available) — this is the expected initial state, not a fallback or degraded mode. `AC-01`/`AC-02` (populated trend charts) become satisfiable once 8 weeks of snapshots have accumulated.

### Request

| Parameter | Type | Required | Description |
|-----------|------|----------|--------------|
| `weeks` | integer | No | Number of most-recent weeks to return. Default 12. |

### Response (200) — sufficient history (≥8 weeks available)

```json
{
  "status": "ok",
  "data": {
    "insufficient_history": false,
    "weeks": [
      {
        "week_start": "2026-06-01",
        "sectors": [
          { "sector_name": "Technology", "exposure_pct": 42.5 },
          { "sector_name": "Financials", "exposure_pct": 31.0 },
          { "sector_name": "Other", "exposure_pct": 26.5 }
        ],
        "regime_us": true,
        "regime_uk": false
      }
    ]
  }
}
```

### Response (200) — insufficient history (<8 weeks available)

```json
{
  "status": "ok",
  "data": {
    "insufficient_history": true,
    "weeks_available": 3
  }
}
```

### Response fields — `data`

| Field | Type | Description |
|-------|------|-------------|
| `insufficient_history` | boolean | `true` when fewer than 8 distinct weeks of snapshots exist yet |
| `weeks_available` | integer | Present only when `insufficient_history: true` — how many distinct weeks exist so far |
| `weeks` | array | Present only when `insufficient_history: false`. Oldest week first, most recent last. |
| `weeks[].week_start` | string (ISO date) | Monday of the ISO week this bucket represents |
| `weeks[].sectors` | array | Top 5 sectors by the most recent week's exposure, plus an `"Other"` bucket summing the remainder (only present if there is a remainder) — this grouping is held constant across all returned weeks, not re-ranked per week |
| `weeks[].sectors[].sector_name` | string | Sector label, or `"Other"` |
| `weeks[].sectors[].exposure_pct` | number | Exposure % for that sector in that week (1 dp) |
| `weeks[].regime_us` | boolean or null | SPY-based US regime status snapshotted that day (`true` = risk-on) |
| `weeks[].regime_uk` | boolean or null | FTSE-based UK regime status snapshotted that day (`true` = risk-on) |

### Notes

- Weekly bucketing takes the **last** snapshot within each ISO week (Monday–Sunday) as that week's representative value — not an average.
- On any error, returns `{"insufficient_history": true, "weeks_available": 0, "error": "<message>"}` — does not propagate exceptions to the UI.

### Errors

| Code | Condition |
|------|-----------|
| 500 | Internal error (silently falls back to insufficient-history response) |

---

## GET /portfolio/gate-metrics

Returns trade count and data density gate progress metrics for the active portfolio.

Used to surface progress toward the 20/50/100 closed-trade gates. Called by the SI-05 weekly digest service and available for future dashboard display.

**Source:** ST-04, EPIC-02, v5.5

### Request

No parameters required.

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "closed_trades_count": 12,
    "closed_trades_with_plans": 5,
    "active_positions_count": 3,
    "ai_journal_entry_count": null,
    "oldest_trade_date": "2024-01-15",
    "newest_trade_date": "2025-11-30"
  }
}
```

### Response fields — `data`

| Field | Type | Description |
|-------|------|-------------|
| closed_trades_count | integer | Total closed trades in `trade_history` for this portfolio |
| closed_trades_with_plans | integer | Closed trades that have at least one associated `trade_plans` entry (linked via `position_id`) |
| active_positions_count | integer | Open positions with `status = 'active'` |
| ai_journal_entry_count | integer \| null | Count from `ai_journal_entries` table if it exists; `null` if table absent |
| oldest_trade_date | ISO 8601 string \| null | `MIN(exit_date)` across all closed trades; `null` if no trades |
| newest_trade_date | ISO 8601 string \| null | `MAX(exit_date)` across all closed trades; `null` if no trades |

### Errors

| Code | Condition |
|------|-----------|
| 500 | Database error (returns `{"status": "error", "error": "..."}`) |
