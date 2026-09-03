# trade_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.5.1
**Last Updated:** 2026-08-21 (BLG-BE-108, ST-03, v9.0: clarified "linked journal entries" sourcing for POST/GET /trades/{trade_id}/debrief — resolves ESC-EXEC-20260821-01)
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
- [GET /trades/{trade_id}/debrief](#get-tradestrade_iddebrief)
- [POST /trades/{trade_id}/debrief](#post-tradestrade_iddebrief)

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
      "tags": ["momentum", "winner"],
      "commission_gbp": 12.50,
      "spread_cost_gbp": 3.20,
      "net_r_multiple": 2.145
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
| `commission_gbp` | Commission paid at entry and exit (GBP). `null` until recorded via `PATCH /trades/{id}/costs` |
| `spread_cost_gbp` | Bid-ask spread cost estimate (GBP). `null` until recorded via `PATCH /trades/{id}/costs` |
| `net_r_multiple` | Net-of-costs R-multiple: `(pnl − commission_gbp − spread_cost_gbp) / initial_risk_gbp`. `null` when `commission_gbp` or `spread_cost_gbp` is absent, or when `stop_price_at_entry` is unavailable. Rounded to 3 decimal places |
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

## PATCH /trades/{trade_id}/costs

**Auth:** Required (X-API-Key)

Record or update commission and spread costs (in GBP) for a closed trade. Both fields are optional — send only the fields to update. A subsequent call overwrites the previous value. Once both fields are populated, `GET /trades` will compute and return `net_r_multiple` for the trade.

**Story:** ST-03 (EPIC-02, v6.0) — BLG-FEAT-20

### Path parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trade_id | UUID string | Yes | `id` from `trade_history` |

### Request body

```json
{
  "commission_gbp": 12.50,
  "spread_cost_gbp": 3.20
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `commission_gbp` | float \| null | No | Total commission paid (GBP), entry + exit |
| `spread_cost_gbp` | float \| null | No | Estimated bid-ask spread cost (GBP) |

### Response (200)

```json
{
  "status": "ok",
  "data": { "trade_id": "uuid-string" }
}
```

### Errors

| Code | Condition |
|------|-----------|
| 404 | trade_id not found in trade_history for the active portfolio |
| 500 | Database error |

---

## GET /trades/{trade_id}/debrief

**Auth:** Required (X-API-Key)

**Story:** ST-06 (EPIC-02, v8.9) — BLG-FEAT-90

Returns the existing AI-generated post-trade debrief for a closed trade, if one has already been generated. Does not trigger generation — see `POST /trades/{trade_id}/debrief` below for on-demand generation. §13 review: `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (CONDITIONAL, 9 binding conditions).

**"Linked journal entries" sourcing (BLG-BE-108, ST-03, v9.0 — Product Owner decision, resolves `ESC-EXEC-20260821-01`):** the AC's "linked journal entries where present" draws on **both** of the following, not one or the other — passed to the model as free-text prompt context only, never as a source of numbers (§13 Condition 2 applies solely to quantitative claims):
1. The trade's own `entry_note`/`exit_note` — the fields the UI itself labels "Trade Journal", directly adjacent to the Debrief panel in `TradeHistoryTable.js`. Included first, as the user's own contemporaneous reflection.
2. Red Flag Journal events for this ticker (the original implementation) — system-detected compliance flags, retained as additional context for the focus-area recommendation.

### Path parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trade_id | UUID string | Yes | `id` from `trade_history` |

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "available": true,
    "summary_text": "Entered at 100.0, exited at 108.5. P&L: +8.50 (+8.50%). Exit reason: Target Reached. Held 12 day(s). Plan called for entry at 100.0, planned stop 95.0, R target 2.0",
    "focus_area_text": "Your exit was 3 days earlier than the 15-day median holding period across your last 5 closed trades in this setup type.",
    "generation_status": "ok",
    "model_version": "claude-haiku-4-5",
    "prompt_version": "v1.0",
    "generated_at": "2026-08-20T09:00:00Z"
  }
}
```

### Response fields

| Field | Type | Description |
|-------|------|--------------|
| available | boolean | Always true when a debrief exists (404 otherwise) |
| summary_text | string | Deterministic, non-AI factual plan-vs-reality summary — computed from `trade_history`/`trade_plans`, never model-generated (§13 Condition 2) |
| focus_area_text | string \| null | The one AI-generated pattern-surfacing sentence, or null if omitted — see `generation_status` |
| generation_status | string | `"ok"` (focus area present), `"fallback_no_focus_area"` (§13 Condition 9 compliance check failed twice — summary still shown), or `"ai_unavailable"` (no `ANTHROPIC_API_KEY`, or the `anthropic` package is absent, or a generation error occurred) |
| model_version | string | Model used to generate `focus_area_text` |
| prompt_version | string | Prompt template version |
| generated_at | ISO 8601 datetime | When this debrief was last (re)generated |

### Errors

| Code | Condition |
|------|-----------|
| 404 | No debrief generated yet for this trade — call `POST /trades/{trade_id}/debrief` to generate one |
| 500 | Database error |

---

## POST /trades/{trade_id}/debrief

**Auth:** Required (X-API-Key)

**Story:** ST-06 (EPIC-02, v8.9) — BLG-FEAT-90

Generate (or regenerate) the AI post-trade debrief for a closed trade, on demand. Regeneration overwrites the prior debrief for this trade. **Implementation note:** generation is on-demand only — there is no hook into the live position-close event path; the story's own acceptance criteria explicitly names on-demand as an accepted fallback ("real-time generation, or on-demand if real-time isn't feasible").

Always returns 200 with a debrief — the deterministic `summary_text` is never unavailable, even when the AI-generated `focus_area_text` is omitted. See `generation_status` in the response.

**§13 Condition 9 (output-side enforcement):** before `focus_area_text` is returned or persisted, the generated text is scanned for prescriptive phrasing (Condition 1) and every numeric token in it is cross-checked against the deterministic source values passed into the prompt (Condition 2). On a failure, generation is retried once; a second failure on the regenerated text is terminal for this call — the debrief is returned with `focus_area_text: null` and `generation_status: "fallback_no_focus_area"`, never with non-compliant text. Every generation call's compliance-check outcome is logged to `claude_audit_log` (Condition 5/9), independent of the debrief response itself.

### Path parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trade_id | UUID string | Yes | `id` from `trade_history` |

### Response (200)

Same shape as `GET /trades/{trade_id}/debrief` above.

### Errors

| Code | Condition |
|------|-----------|
| 404 | trade_id not found in trade_history |
| 500 | Database error |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 2.5.1 | 2026-08-21 | ST-03 (EPIC-01, v9.0, BLG-BE-108): Clarified "linked journal entries" sourcing for GET/POST /trades/{trade_id}/debrief — draws on both `entry_note`/`exit_note` and Red Flag Journal events, per Product Owner decision resolving `ESC-EXEC-20260821-01`. No request/response schema change — `backend/services/debrief_service.py::_journal_context_for_trade` internal implementation only. |
| 2.5.0 | 2026-08-20 | ST-06 (EPIC-02, v8.9, BLG-FEAT-90): Add GET /trades/{trade_id}/debrief and POST /trades/{trade_id}/debrief — Automated AI Post-Trade Debrief. New table `trade_debriefs` (data_model.md#DS-16). §13 review CONDITIONAL (9 binding conditions): `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`. AI Compliance & Governance Officer sign-off recorded in `qa_evidence_EPIC-02.md`. |
| 1.8.4 | 2026-02-17 | Initial spec — GET /trades, GET /trades/export/csv. Both `pnl_pct` and `pnl_percent` fields documented for backward compatibility |
| 1.9.0 | 2026-03-02 | S2-08 (EPIC-06/BLG-TECH-09): Backend fix — `holding_days` added to `formatted_trades` dict in `trade_service.py` (was present in DB and spec but absent from API response). `GET /trades` now returns `holding_days` per spec. OBS-QWB-R3-01 resolved. TASK-28/29/30 complete. API Contracts owner sign-off granted 2026-03-02 (Delegated Authority). |
| 2.0.0 | 2026-03-11 | ST-02 (EPIC-01, v1.9): Add GET /trades/{trade_id}/reflection and POST /trades/{trade_id}/reflection. Schema: trade_reflections table (data_model.md v1.8). Spec: trade_reflection.md §7. |
| 2.1.0 | 2026-03-20 | ST-14 (EPIC-05, v2.1): Add `fill_price` (float\|null) and `slippage_pct` (float\|null) per trade; add `avg_slippage_pct` (float\|null) to top-level summary. Data model gate cleared: Data Model & Domain Schema Owner + Head of Specs Team countersigned 2026-03-20. |
| 2.2.0 | 2026-04-06 | ST-09 (EPIC-03, v2.5): Add `fee_drag_pct` (float\|null) per trade; add `avg_fee_drag_pct` (float\|null) to top-level summary. No schema change. |
| 2.3.0 | 2026-05-15 | ST-05 (EPIC-02, v3.5): Add GET /trades/{trade_id}/plan-vs-reality — PO-01 Plan vs Reality comparison endpoint. New JSONB column `plan_vs_reality` on `trade_history`; new `planned_stop_price` column on `trade_plans`. Migration: ensure_plan_vs_reality_columns(). |
| 2.2.0 | 2026-04-06 | ST-09 (EPIC-03, v2.5): Add `fee_drag_pct` (float\|null) per trade (`exit_fees / gross_proceeds * 100`); add `avg_fee_drag_pct` (float\|null) to top-level summary. No schema change — uses existing `exit_fees` and `gross_proceeds` columns. Head of Specs Team co-authorship confirmed. |
| 2.4.0 | 2026-06-19 | ST-03 (EPIC-02, v6.0): Add `PATCH /trades/{trade_id}/costs` endpoint; add `commission_gbp`, `spread_cost_gbp`, `net_r_multiple` to `GET /trades` per-trade response. Schema migration: data_model.md DS-08 (v2.9). |
| 2.4.1 | 2026-07-29 | v7.10 ST-15 (BLG-SPEC-104): `GET /trades` JSON example updated to include `commission_gbp`, `spread_cost_gbp`, `net_r_multiple` — these fields were documented in the field notes table since 2.4.0 but omitted from the example object. Also corrected header `**Version:**` from 2.3.0 to reflect the already-published 2.4.0 changelog row (per shared_standards.md §9.1). No functional change. |
