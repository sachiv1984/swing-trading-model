# trade_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.3.0
**Last Updated:** 2026-05-15
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines **Trade** domain endpoints.

- Retrieve immutable, closed trade history
- Includes trade-level statistics and a list of closed trades

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /trades](#get-trades)
- [GET /trades/export/csv](#get-tradesexportcsv)
- [GET /trades/{trade_id}/reflection](#get-tradestrade_idreflection)
- [POST /trades/{trade_id}/reflection](#post-tradestrade_idreflection)

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
  "avg_slippage_pct": -0.05,
  "avg_fee_drag_pct": 0.38,
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
      "fill_price": 621.25,
      "slippage_pct": -0.12,
      "fee_drag_pct": 0.38,
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
| `avg_slippage_pct` | Portfolio average slippage across all trades where `fill_price` is present. Computed server-side as the mean of per-trade `slippage_pct`. `null` when no trades have `fill_price` recorded |
| `avg_fee_drag_pct` | Portfolio average fee drag across all trades where `gross_proceeds > 0`. Computed server-side as the mean of per-trade `fee_drag_pct`. `null` when no qualifying trades exist. Always non-negative |
| `fill_price` | Actual fill price in native currency at entry. `null` for trades entered before v2.1 (Fill Price capture not yet active) |
| `slippage_pct` | Per-trade slippage as a percentage: `(fill_price − entry_price) / entry_price * 100`. Negative = favourable (filled below market). Positive = unfavourable (filled above market). `null` when `fill_price` is `null`. Rounded to 2 decimal places |
| `fee_drag_pct` | Per-trade fee drag as a percentage: `exit_fees / gross_proceeds * 100`. Always non-negative. `null` when `gross_proceeds` is null or zero. Rounded to 2 decimal places |
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

---

## GET /trades/{trade_id}/reflection

**Purpose:** Retrieve an existing reflection for a closed trade. Used to pre-populate the reflection modal when a user re-opens it.

**Method & Path:** `GET /trades/{trade_id}/reflection`

### Path parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trade_id | UUID string | Yes | `id` from `trade_history` |

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "id": "uuid",
    "trade_id": "uuid",
    "trade_rationale": "string | null",
    "what_worked": "string | null",
    "what_didnt_work": "string | null",
    "discipline_assessment": "string | null",
    "key_takeaway": "string | null",
    "created_at": "ISO-8601 string",
    "updated_at": "ISO-8601 string"
  }
}
```

### Errors

| Code | Condition |
|------|-----------|
| 404 | No reflection saved for this trade, or trade_id not found |
| 500 | Database error |

---

## POST /trades/{trade_id}/reflection

**Purpose:** Create or update (upsert) the reflection for a closed trade. All five reflection fields are optional — any subset, including all null, is accepted. Idempotent — repeated calls update the existing record.

**Method & Path:** `POST /trades/{trade_id}/reflection`

### Path parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trade_id | UUID string | Yes | `id` from `trade_history` |

### Request body

```json
{
  "trade_rationale": "string | null",
  "what_worked": "string | null",
  "what_didnt_work": "string | null",
  "discipline_assessment": "string | null",
  "key_takeaway": "string | null"
}
```

All fields optional. Max 500 characters each (validated at API layer; error 422 if exceeded via standard validation, or 404 ValueError path).

### Response (200)

Same shape as GET response — returns the full saved reflection after upsert.

### Errors

| Code | Condition |
|------|-----------|
| 404 | trade_id not found in trade_history |
| 500 | Database error |

---

## GET /trades/{trade_id}/plan-vs-reality

**Auth:** Required (X-API-Key)

Returns the plan vs reality comparison for a closed trade that has a linked trade plan. Computes comparison on-demand from trade_history, positions, and trade_plans data.

### Path parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trade_id | UUID string | Yes | `id` from `trade_history` |

### Response (200) — closed trade with plan

```json
{
  "status": "ok",
  "data": {
    "plan_linked": true,
    "trade_plan_id": "uuid",
    "r_achieved": 1.8,
    "r_target": 2.0,
    "r_delta": -0.2,
    "entry_delta_pct": null,
    "stop_discipline": "on_plan",
    "exit_reason_actual": "target hit",
    "exit_reason_planned": "Close below 50-day MA",
    "lifecycle_state_at_exit": "GRACE",
    "plan_adherence_flag": "on_plan",
    "deviation_note": null
  }
}
```

**`entry_delta_pct`** is null until `planned_entry_price` is snapshotted to `trade_plans` (deferred to Arc 4 proper per `arc4_data_requirements.md §3.1`).

### Response (200) — position still open

```json
{"status": "trade_open"}
```

### Response fields

| Field | Type | Description |
|-------|------|-------------|
| plan_linked | boolean | Whether a trade plan was linked |
| trade_plan_id | uuid | ID of the linked trade plan |
| r_achieved | float \| null | Actual R-multiple: (exit − entry) / (entry − initial_stop) |
| r_target | float \| null | Planned R target from trade_plans.r_target |
| r_delta | float \| null | r_achieved − r_target |
| entry_delta_pct | float \| null | Entry timing accuracy (% deviation from planned entry). null pending Arc 4 snapshot. |
| stop_discipline | string | "on_plan" / "minor_deviation" / "deviation" / "not_captured" |
| exit_reason_actual | string \| null | trade_history.exit_reason |
| exit_reason_planned | string \| null | trade_plans.early_exit_conditions |
| lifecycle_state_at_exit | string \| null | Position lifecycle state at close |
| plan_adherence_flag | string | "on_plan" / "entry_deviation" / "stop_deviation" / "early_exit" |
| deviation_note | string \| null | User annotation (populated via ST-06 frontend view) |

### Errors

| Code | Condition |
|------|-----------|
| 404 | trade_id not found in trade_history, or no trade plan linked to the trade's position |
| 500 | Database error |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.8.4 | 2026-02-17 | Initial spec — GET /trades, GET /trades/export/csv. Both `pnl_pct` and `pnl_percent` fields documented for backward compatibility |
| 1.9.0 | 2026-03-02 | S2-08 (EPIC-06/BLG-TECH-09): Backend fix — `holding_days` added to `formatted_trades` dict in `trade_service.py` (was present in DB and spec but absent from API response). `GET /trades` now returns `holding_days` per spec. OBS-QWB-R3-01 resolved. TASK-28/29/30 complete. API Contracts owner sign-off granted 2026-03-02 (Delegated Authority). |
| 2.0.0 | 2026-03-11 | ST-02 (EPIC-01, v1.9): Add GET /trades/{trade_id}/reflection and POST /trades/{trade_id}/reflection. Schema: trade_reflections table (data_model.md v1.8). Spec: trade_reflection.md §7. |
| 2.1.0 | 2026-03-20 | ST-14 (EPIC-05, v2.1): Add `fill_price` (float\|null) and `slippage_pct` (float\|null) per trade; add `avg_slippage_pct` (float\|null) to top-level summary. Data model gate cleared: Data Model & Domain Schema Owner + Head of Specs Team countersigned 2026-03-20. |
| 2.2.0 | 2026-04-06 | ST-09 (EPIC-03, v2.5): Add `fee_drag_pct` (float\|null) per trade; add `avg_fee_drag_pct` (float\|null) to top-level summary. No schema change. |
| 2.3.0 | 2026-05-15 | ST-05 (EPIC-02, v3.5): Add GET /trades/{trade_id}/plan-vs-reality — PO-01 Plan vs Reality comparison endpoint. New JSONB column `plan_vs_reality` on `trade_history`; new `planned_stop_price` column on `trade_plans`. Migration: ensure_plan_vs_reality_columns(). |
| 2.2.0 | 2026-04-06 | ST-09 (EPIC-03, v2.5): Add `fee_drag_pct` (float\|null) per trade (`exit_fees / gross_proceeds * 100`); add `avg_fee_drag_pct` (float\|null) to top-level summary. No schema change — uses existing `exit_fees` and `gross_proceeds` columns. Head of Specs Team co-authorship confirmed. |
