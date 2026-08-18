# position_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 2.6.0
**Last Updated:** 2026-08-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines **Position** domain endpoints:

- List open positions (trading screen)
- Run daily monitoring analysis
- Exit (full or partial) using user-confirmed broker execution details
- Update journal notes
- Update tags
- Retrieve the tag catalogue

Global response envelopes, error shape, defaults, and multi-currency/stop rules are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.6.0 | 2026-08-17 | ST-02 (BLG-BE-103, EPIC-01, v8.9): Added `current_trailing_stop_native` field to `GET /positions` response — the native-currency counterpart of `current_trailing_stop` (which is GBP-converted for US-market positions). Fixes a currency-basis defect where the frontend rendered the GBP-converted value next to the native currency symbol. `initial_stop` and `stop_price_native` were already native; this closes the gap for the third stop field. |
| 2.5.2 | 2026-08-07 | ST-04 (BLG-SPEC-113, EPIC-02, v8.4): `GET /positions` example was missing 5 live fields returned by `position_service.py`'s `positions_list.append({...})` — `total_cost`, `sector`, `industry`, `exit_reason`, `stop_reason`. Added to example and field notes, cross-checked against the live dict. No functional change. |
| 2.5.1 | 2026-07-29 | v7.10 ST-13 (BLG-SPEC-102) + ST-14 (BLG-SPEC-103): Corrected `GET /positions` response documentation to match live behaviour — the endpoint returns the raw `data` array directly, not the standard `{ status, data }` envelope. Added undocumented lifecycle fields `position_state`, `state_entered_at`, `days_in_state` to the response schema and field notes. No functional change. |
| 2.5.0 | 2026-07-13 | v7.0 ST-15 (BLG-FEAT-68): Added `last_reviewed_at` field to `GET /positions` response (ISO timestamp \| null — position review cadence nudge). Added `PATCH /positions/{position_id}/mark-reviewed` — sets `last_reviewed_at = NOW()`. Display-only; no automated action beyond the explicit user-triggered timestamp update. |
| 2.4.0 | 2026-07-10 | v6.9 ST-02 (BLG-FEAT-65): Added `GET /positions/{position_id}/gap-risk` — overnight/weekend gap risk flag for a single position, combining the DS-04 earnings calendar with historical OHLCV gap statistics. Implemented as a dedicated per-position endpoint rather than a field on `GET /positions` (pre-authorised alternative per the story notes) because the historical-OHLCV lookup is too slow to run inline for every open position on every list load. Display-only; §13 sign-off required (AC-04). |
| 2.3.0 | 2026-07-10 | v6.9 ST-01 (BLG-FEAT-64): Added `GET /positions/{position_id}/compliance-recheck` — re-applies the 5 SI-01 pre-entry deterministic rule checks against an open position's current state (current regime, current signal conditions, current heat/sizing), not its entry-time snapshot. On-demand only, no automation. Display-only; §13 sign-off required (AC-04). |
| 2.2.0 | 2026-06-24 | v6.2 ST-01 (BLG-FEAT-46): Added `current_trailing_stop` field to `GET /positions` response. Added `POST /positions/nightly-stop-update` endpoint. v6.2 ST-05 (BLG-FEAT-49): Added `risk_off_exit` field to `GET /positions` response. Added `POST /positions/risk-off-alerts` endpoint. |
| 2.0.0 | 2026-03-29 | ST-01 (BLG-FEAT-11, v2.3): Added `GET /positions/compliance` — returns ATR-based per-position stop compliance, stop age, and size compliance flags. Display-only; §13.3 constraint enforced. Strategy Rules & System Intent Owner DoQ sign-off required at delivery verification (SPS=4). |
| 1.8.3 | 2026-02-25 | BLG-FEAT-06 (A-S03): Added `grace_days_remaining` (integer \| null) to `GET /positions` response. Derived server-side as `max(0, 10 - holding_days)` when `grace_period = true`; `null` when `grace_period = false`. Always present. No data model change required. QWB decision D4. |
| 1.8.3 | 2026-02-27 | A-QA-05 (F-02): Removed contradictory sentence "Returns 0 on day 10 (grace period ends)" from `grace_days_remaining` field note. Canonical behaviour is `null` when `grace_period = false` (consistent with decision D4 and `implementation_notes.md`). No behaviour change — correction only. |

---

## Endpoints

- [GET /positions](#get-positions)
- [GET /positions/compliance](#get-positionscompliance)
- [GET /positions/search/tags](#get-positionssearchtags)
- [GET /positions/analyze](#get-positionsanalyze)
- [POST /positions/{position_id}/exit](#post-positionsposition_idexit)
- [PATCH /positions/{position_id}/note](#patch-positionsposition_idnote)
- [PATCH /positions/{position_id}/tags](#patch-positionsposition_idtags)
- [GET /positions/tags](#get-positionstags)
- [GET /positions/{position_id}/compliance-recheck](#get-positionsposition_idcompliance-recheck)
- [GET /positions/{position_id}/gap-risk](#get-positionsposition_idgap-risk)

---

## GET /positions

**Purpose**

Returns all **open positions** with live prices, stop context, FX context, and journal metadata.

**Method & Path**

- `GET /positions`

**Idempotency**

- Safe to refresh. Fetches refreshed prices on every call.

### Request

No parameters.

### Response (200)

This endpoint does **not** use the standard `{ status, data }` response envelope (see conventions.md §2.2). The response body is the raw array of open positions directly.

#### Response schema (array)

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "ticker": "NVDA",
    "market": "US",
    "entry_date": "2026-02-01",
    "entry_price": 622.00,
    "shares": 10.5,
    "current_price": 623.00,
    "current_price_native": 850.00,
    "stop_price": 607.50,
    "stop_price_native": 829.00,
    "initial_stop": 545.00,
    "pnl": 2394.00,
    "pnl_percent": 3.7,
    "holding_days": 14,
    "status": "open",
    "grace_period": false,
    "display_status": "PROFITABLE",
    "grace_days_remaining": null,
    "atr_value": 15.32,
    "fx_rate": 1.3642,
    "live_fx_rate": 1.3650,
    "current_trailing_stop": 560.50,
    "current_trailing_stop_native": 764.00,
    "risk_off_exit": false,
    "entry_note": "Breakout above $800 resistance",
    "exit_note": null,
    "exit_reason": null,
    "stop_reason": "Active",
    "total_cost": 6531.00,
    "sector": "Technology",
    "industry": "Semiconductors",
    "tags": ["momentum", "breakout"],
    "last_reviewed_at": "2026-07-01T09:00:00+00:00",
    "position_state": "PROFITABLE",
    "state_entered_at": "2026-07-01T09:00:00+00:00",
    "days_in_state": 14
  }
]
```

#### Field notes

| Field | Notes |
|-------|-------|
| `current_price` | GBP — used for portfolio calculations |
| `current_price_native` | USD or GBP — used for display (what the trader sees in their broker) |
| `stop_price` | Current trailing stop in GBP. `0.0` during grace period |
| `stop_price_native` | Current trailing stop in native currency. `0.0` during grace period |
| `initial_stop` | The stop calculated at entry (`entry_price − (5 × ATR)`), in GBP. Informational; used to show how far the stop has trailed |
| `display_status` | `"GRACE"` (days 0–9), `"PROFITABLE"` (day 10+, P&L > 0), or `"LOSING"` (day 10+, P&L ≤ 0) |
| `fx_rate` | The GBP/USD rate at time of entry (stored) |
| `live_fx_rate` | The current GBP/USD rate (fetched live) |
| `exit_note` | Always `null` for open positions. Present for schema consistency with closed trade records |
| `exit_reason` | Always `null` for open positions. Present for schema consistency with closed trade records — populated on close |
| `stop_reason` | Human-readable stop status string, e.g. `"Grace period ({holding_days}/10 days)"` during the grace window, `"Active"` otherwise |
| `total_cost` | float (GBP). `entry_price × shares` at entry, rounded. Used for position sizing / concentration calculations |
| `sector` | string \| `null`. GICS-style sector classification for the ticker, used by `GET /portfolio/sector-weights` and `GET /portfolio/concentration-status` |
| `industry` | string \| `null`. Finer-grained classification than `sector` |
| `tags` | Array of tag strings. Empty array if no tags set |
| `current_trailing_stop` | The computed trailing stop in GBP (profit-lock logic: profit → `price − 2×ATR`, else `entry − 5×ATR`, ratcheted). Always present and non-zero after the first nightly update. `0` if no stop has been computed yet. Unlike `stop_price`, this field is always non-zero — it is informational even during the grace period. (v6.2 ST-01 BLG-FEAT-46) |
| `current_trailing_stop_native` | Native-currency counterpart of `current_trailing_stop` above — same value, unconverted for US-market positions (identical to `current_trailing_stop` for UK positions, where native == GBP). Frontend consumers pairing a stop value with the native currency symbol (derived from `market`) must use this field, not `current_trailing_stop` — using the GBP-converted field with the native symbol was BLG-BE-103, a currency-basis defect fixed in v8.9 ST-02. (v8.9 ST-02 BLG-BE-103) |
| `risk_off_exit` | `boolean`. `true` when the position's market index (SPY for US, FTSE for UK) is below its 200-day MA. Cleared to `false` when the index recovers. Set nightly by `POST /positions/risk-off-alerts`. (v6.2 ST-05 BLG-FEAT-49) |
| `pnl_percent` | Percentage P&L relative to entry cost. Same value as would be seen in `pnl_pct` in trade records. Both field names exist in the system for compatibility; `pnl_percent` is the canonical name in position responses |
| `grace_days_remaining` | `integer` when `grace_period = true`; `null` when `grace_period = false`. Derived server-side as `max(0, 10 - holding_days)` during the grace period. Represents the number of days remaining in the grace window. On day 10, `grace_period` becomes `false` and this field returns `null` — not `0`. Intended display format: `"Day {holding_days + 1} of 10"`. Always present in the response object. |
| `last_reviewed_at` | ISO-8601 timestamp \| `null`. `null` means the position has never been marked reviewed. Set by `PATCH /positions/{id}/mark-reviewed`. (v7.0 ST-15 BLG-FEAT-68) |
| `position_state` | `string`. One of `"GRACE"`, `"PROFITABLE"`, `"LOSING"`, `"EXIT ZONE"`, `"UNKNOWN"`. Server-computed lifecycle state, distinct from `display_status` — recalculated and persisted (with transition history) on each `GET /positions` call. `"UNKNOWN"` when required inputs (entry price, current price, ATR, entry date) are unavailable. (v7.10 ST-14 BLG-SPEC-103) |
| `state_entered_at` | ISO-8601 timestamp \| `null`. Timestamp of the most recent transition into the current `position_state`. `null` only in the `position_state = "UNKNOWN"` fallback case. (v7.10 ST-14 BLG-SPEC-103) |
| `days_in_state` | `integer`. Whole days elapsed since `state_entered_at`. `0` on the day of transition or when `state_entered_at` is `null`. (v7.10 ST-14 BLG-SPEC-103) |

> **Note:** For a summary view of open positions alongside portfolio totals, use `GET /portfolio`. This endpoint returns the full enriched position object including native prices, stop context, and journal fields; `GET /portfolio` returns a lighter position shape.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## POST /positions/nightly-stop-update

**Purpose** (v6.2 ST-01 BLG-FEAT-46)

Recomputes the trailing stop for every open position using the profit-lock strategy logic and stores the result in the database.

**Method & Path**

- `POST /positions/nightly-stop-update`

**Strategy constants (must match `production_strategy.py` OPTIMAL_PARAMS):**
- `INITIAL_ATR_MULT = 5` — wide stop when position is not in profit
- `PROFIT_ATR_MULT = 2` — tight stop when position is in profit
- `ATR_PERIOD = 14` — 14-day ATR

**Ratchet invariant:** `stored_stop = max(previous_stop, newly_calculated_stop)` — stop only ever moves up.

### Request

No body required.

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "run_date": "2026-06-24",
    "positions_processed": 3,
    "updated": 3,
    "skipped": 0,
    "results": [
      {
        "ticker": "NVDA",
        "market": "US",
        "status": "updated",
        "previous_stop": 545.00,
        "new_stop": 562.80,
        "stop_moved": true,
        "atr_mult": 2.0,
        "reason": "Profitable (tight 2x ATR)"
      }
    ]
  }
}
```

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## POST /positions/risk-off-alerts

**Purpose** (v6.2 ST-05 BLG-FEAT-49)

Runs the nightly market-regime check and sets or clears the `risk_off_exit` flag on each open position based on whether its market index is below MA200.

**Method & Path**

- `POST /positions/risk-off-alerts`

**Logic:**
- `SPY < MA200` → set `risk_off_exit = true` for all open US positions
- `FTSE < MA200` → set `risk_off_exit = true` for all open UK positions
- Index recovers → clear `risk_off_exit = false` for the relevant market
- **Market isolation:** US risk-off does not affect UK positions and vice versa.

### Request

No body required.

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "run_date": "2026-06-24",
    "market_regime": { "spy_risk_on": true, "ftse_risk_on": false },
    "us_risk_off": false,
    "uk_risk_off": true,
    "us_positions_flagged": 0,
    "us_positions_cleared": 2,
    "uk_positions_flagged": 1,
    "uk_positions_cleared": 0
  }
}
```

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /positions/analyze

**Purpose**

Runs deterministic daily monitoring logic across open positions and returns an action summary.

**Method & Path**

- `GET /positions/analyze`

**Idempotency**

- Safe to refresh. Deterministic recomputation on every call.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "analysis_date": "2026-02-17",
  "market_regime": {
    "spy_risk_on": true,
    "ftse_risk_on": true,
    "spy_price": 580.00,
    "spy_ma200": 550.00,
    "ftse_price": 8200.00,
    "ftse_ma200": 8000.00
  },
  "live_fx_rate": 1.3650,
  "summary": {
    "total_value": 15000.00,
    "total_pnl": 1000.00,
    "exit_count": 0
  },
  "actions": [
    {
      "ticker": "NVDA",
      "action": "HOLD",
      "entry_price": 622.00,
      "current_price": 623.00,
      "shares": 10.5,
      "pnl": 2394.00,
      "pnl_pct": 3.7,
      "current_stop": 607.50,
      "holding_days": 14,
      "grace_period": false,
      "stop_reason": "Trailing (profitable)"
    },
    {
      "ticker": "AAPL",
      "action": "EXIT",
      "exit_reason": "Risk-Off Signal",
      "entry_price": 180.00,
      "current_price": 175.00,
      "shares": 20,
      "pnl": -100.00,
      "pnl_pct": -2.8,
      "current_stop": 171.00,
      "holding_days": 8,
      "grace_period": true,
      "stop_reason": "Market regime"
    }
  ]
}
```

#### Action types

- `HOLD`: position healthy; no user action required.
- `EXIT`: exit recommended (stop hit, risk-off signal, or trailing stop triggered); user must confirm exit with their actual broker execution price.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## POST /positions/{position_id}/exit

**Purpose**

User-confirmed exit using actual broker execution details.

- Supports full exit (default) or partial exit (by specifying `shares`).
- **Exit price is always user-provided** — the backend never fetches a live price to use as the exit price.
- For **US** positions, `exit_fx_rate` is required.

**Method & Path**

- `POST /positions/{position_id}/exit`

**Idempotency**

- Mutating (non-idempotent). Repeating the request records additional exits.

### Request

#### Path parameters

- `position_id` (string, required): UUID of the position.

#### Body

```json
{
  "shares": 10.5,
  "exit_price": 920.00,
  "exit_date": "2026-02-17",
  "exit_reason": "Target Reached",
  "exit_fx_rate": 1.3650,
  "exit_note": "Hit target, took profits"
}
```

#### Required fields

- `exit_price` (number, min `0.01`): actual broker execution price.

#### Optional fields

- `shares` (number): shares to exit; default is all remaining shares.
- `exit_date` (string, `YYYY-MM-DD`): default is today (UTC).
- `exit_reason` (string): one of:
  - `Manual Exit` (default)
  - `Stop Loss Hit`
  - `Target Reached`
  - `Risk-Off Signal`
  - `Trailing Stop`
  - `Partial Profit Taking`
- `exit_fx_rate` (number): **required for US stocks**; ignored for UK stocks.
- `exit_note` (string, max 500): journal note. Empty string treated as `null`.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "ticker": "NVDA",
  "market": "US",
  "exit_price": 920.00,
  "shares": 10.5,
  "gross_proceeds": 9660.00,
  "exit_fees": 10.00,
  "fee_breakdown": {
    "commission": 5.00,
    "stamp_duty": 0.00,
    "fx_fee": 5.00
  },
  "net_proceeds": 9650.00,
  "realized_pnl": 3200.00,
  "realized_pnl_pct": 35.8,
  "new_cash_balance": 14650.00,
  "exit_fx_rate": 1.3650,
  "exit_date": "2026-02-17",
  "is_partial_exit": false,
  "remaining_shares": 0
}
```

### Validation rules & constraints

- `position_id` must identify an existing open position.
- `exit_price` must be greater than 0.
- If provided, `shares` must be > 0 and must not exceed position size.
- `exit_reason` must be one of the allowed values listed above.
- For US positions, `exit_fx_rate` is required; the backend rejects requests without it.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Missing `exit_fx_rate` for US stock
- `400` Shares exceed position size
- `400` Invalid `exit_reason`
- `404` Position not found

---

## PATCH /positions/{position_id}/note

**Purpose**

Update entry and/or exit notes for a position. Works for both open and closed positions.

**Method & Path**

- `PATCH /positions/{position_id}/note`

**Idempotency**

- Mutating. Replaces provided fields with submitted values.

### Request

#### Path parameters

- `position_id` (string, required): UUID of the position.

#### Body

```json
{
  "entry_note": "Updated reasoning after analysis",
  "exit_note": "Hit target, took profits"
}
```

#### Fields

- `entry_note` (string or `null`, max 500): set `null` to clear.
- `exit_note` (string or `null`, max 500): set `null` to clear.

**At least one field is required.**

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "ticker": "NVDA",
  "entry_note": "Updated reasoning after analysis",
  "exit_note": "Hit target, took profits",
  "updated_at": "2026-02-17T10:30:00Z"
}
```

### Validation rules & constraints

- At least one of `entry_note` or `exit_note` must be provided.
- Notes must not exceed 500 characters.
- Empty string `""` is treated as `null`.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` No fields provided
- `400` Note exceeds 500 characters
- `404` Position not found

---

## PATCH /positions/{position_id}/tags

**Purpose**

Replace all tags for a position. Works for both open and closed positions.

**Method & Path**

- `PATCH /positions/{position_id}/tags`

**Idempotency**

- Mutating. Replaces the full tag set with the provided array.

### Request

#### Path parameters

- `position_id` (string, required): UUID of the position.

#### Body

```json
{
  "tags": ["momentum", "breakout", "winner"]
}
```

#### Fields

- `tags` (array, required): pass an empty array `[]` to clear all tags.

#### Tag rules

- Lowercase letters, numbers, hyphens only
- Regex: `^[a-z0-9-]+$`
- Max 20 characters per tag
- Max 10 tags per position

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "ticker": "NVDA",
  "tags": ["momentum", "breakout", "winner"],
  "updated_at": "2026-02-17T10:30:00Z"
}
```

### Validation rules & constraints

- Tags must meet the formatting requirements above.
- Each tag max 20 characters.
- No more than 10 tags per position.
- The submitted array replaces all existing tags.

### Errors

Errors use the standard error envelope from **conventions.md**.

- `400` Invalid tag format
- `400` Tag exceeds 20 characters
- `400` More than 10 tags
- `404` Position not found

---

## GET /positions/tags

**Purpose**

Retrieve all unique tags used across positions (for UI autocomplete and tag filter suggestions).

**Method & Path**

- `GET /positions/tags`

**Idempotency**

- Safe to refresh.

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "tags": ["breakout", "momentum", "winner", "loser", "earnings"],
  "total_positions": 42,
  "positions_with_tags": 38
}
```

#### Field notes

- `tags` is sorted alphabetically (case-insensitive).
- Returns tags from both open and closed positions.
- `total_positions` includes open and closed positions.
- Returns an empty array if no tags exist.

### Errors

Errors use the standard error envelope from **conventions.md**.

---

## GET /positions/search/tags

**Purpose**

Search open and closed positions by one or more tags. Returns all positions that match **any** of the provided tags (OR match, not AND).

**Method & Path**

- `GET /positions/search/tags`

**Idempotency**

- Safe to repeat (read-only).

### Request

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tags` | string | Yes | Comma-separated list of tags to search for. Example: `momentum,breakout`. Each tag is matched case-insensitively. At least one tag is required. |

#### Example

```
GET /positions/search/tags?tags=momentum,breakout
```

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

Array of matching position objects. Each position object follows the same shape as positions returned by `GET /positions`.

```json
{
  "status": "ok",
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "ticker": "AAPL",
      "tags": ["momentum", "breakout"]
    }
  ]
}
```

#### Matching rules

- Positions are matched if any tag in the request matches any tag on the position (OR semantics).
- Tag matching is case-insensitive.
- Both open and closed positions are searched.
- Returns an empty array if no positions match (not an error).

### Errors

Errors use the standard error envelope from **conventions.md**.

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `tags` query parameter is missing or empty after parsing |
| `500` | Internal server error |

---

## GET /positions/compliance

**Purpose**

Returns ATR-based strategy compliance flags for all open positions. Supports the Strategy Compliance Panel on the Positions page (Table View only).

**Scope constraint (§13.3):** Display-only. No automated notification, alert, or action is generated by this endpoint or the panel that consumes it. Strategy Rules & System Intent Owner DoQ sign-off required at delivery verification (SPS=4).

**Method & Path**

- `GET /positions/compliance`

**Idempotency**

- Safe to repeat (read-only).

### Request

No parameters.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "overall_status": "Compliant",
  "compliant_count": 3,
  "total_count": 3,
  "positions": [
    {
      "position_id": "550e8400-e29b-41d4-a716-446655440000",
      "ticker": "AAPL",
      "market": "US",
      "stop_compliant": true,
      "stop_age_days": 5,
      "size_compliant": true
    }
  ]
}
```

#### Field notes

**Top-level:**

| Field | Type | Notes |
|-------|------|-------|
| `overall_status` | string | `"Compliant"` / `"Needs Attention"` / `"Review Required"`. Derived from per-position flags (see logic below). |
| `compliant_count` | integer | Number of positions where all assessable flags are `true`. |
| `total_count` | integer | Total open positions assessed. |
| `positions` | array | Per-position compliance records. |

**Per-position:**

| Field | Type | Notes |
|-------|------|-------|
| `position_id` | string (UUID) | Matches the `id` field in `GET /positions`. |
| `ticker` | string | Display ticker (no `.L` suffix for UK stocks). |
| `market` | string | `"UK"` or `"US"`. |
| `stop_compliant` | boolean \| null | `true` if `(entry_price − current_stop) / atr ≤ 2.5`. `false` if stop is missing or too wide. `null` if position is in grace period (stop not yet active) or ATR is unavailable. |
| `stop_age_days` | integer \| null | Approximate days since the stop was last set. `null` for grace-period positions. Note: this is a conservative approximation using `holding_days` as the positions table does not record a dedicated `stop_updated_at` timestamp. |
| `size_compliant` | boolean \| null | `true` if initial risk amount (stop distance × shares, in GBP) is within `risk_percent` of portfolio value × 1.10 tolerance. `null` if no portfolio snapshot is available or risk data is insufficient. |

**`overall_status` derivation:**

| Condition | Value |
|-----------|-------|
| All positions fully compliant (all assessable flags `true`) | `"Compliant"` |
| Some non-compliant positions (< 50% of total) | `"Needs Attention"` |
| Many non-compliant positions (≥ 50% of total) | `"Review Required"` |
| No open positions | `"Compliant"` |

### Errors

Errors use the standard error envelope from **conventions.md**.

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Portfolio not found |
| `500` | Internal server error |

---

## GET /positions/{position_id}

**Added:** v3.3 (Arc 3 — IT-01)
**Spec:** `backend/services/position_lifecycle_service.py`, `docs/reference/openapi.yaml`

Returns a single open position by ID with live prices and lifecycle state fields.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `position_id` | string (UUID) | Yes | Position identifier |

### Response (200 OK)

Returns the position object enriched with live price data and Arc 3 lifecycle fields:

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Position UUID |
| `ticker` | string | Display ticker (no `.L` suffix for UK) |
| `market` | string | `"UK"` or `"US"` |
| `position_state` | string \| null | Arc 3 state: `EXIT ZONE`, `PROFITABLE`, `LOSING`, `GRACE`, `UNKNOWN` |
| `state_entered_at` | string \| null | ISO 8601 timestamp when current state was entered |
| `days_in_state` | integer \| null | Trading days in current state |
| `current_price` | number | Live price in GBP |
| `pnl` | number | Unrealised P&L in GBP |
| `pnl_percent` | number | P&L as percentage |

### Errors

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Position not found |
| `500` | Internal server error |

---

## POST /positions/{position_id}/refresh-state

**Added:** v3.3 (Arc 3 — IT-01)
**Spec:** `backend/services/position_lifecycle_service.py`, `docs/reference/openapi.yaml`

Explicitly recalculates and persists the Arc 3 lifecycle state for a position.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `position_id` | string (UUID) | Yes | Position identifier |

### Response (200 OK)

```json
{
  "status": "ok",
  "data": {
    "position_id": "<uuid>",
    "position_state": "GRACE",
    "state_entered_at": "2026-05-10T00:00:00",
    "days_in_state": 2
  }
}
```

### Errors

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Position not found |
| `500` | Internal server error |

---

## GET /positions/{position_id}/compliance-recheck

**Added:** v6.9 (ST-01, BLG-FEAT-64)

**Purpose**

Re-applies the 5 existing SI-01 pre-entry deterministic rule checks against an open
position's **current** state (current regime, current signal conditions, current
heat/sizing) rather than its entry-time snapshot. Manual, on-demand, single-position
check — does not replace or duplicate SI-02 (drift detection), which remains a
separate gated capability.

**Scope constraint (§13):** Display-only. Pure re-application of the existing
deterministic rule set — no new statistical model, scoring, or prediction. No
automated action (exit, alert, notification) is triggered. On-demand only — no
polling or background job. Strategy Rules & System Intent Owner DoQ sign-off
required at delivery verification.

**Method & Path**

- `GET /positions/{position_id}/compliance-recheck`

**Idempotency**

- Safe to repeat (read-only). Reflects current conditions at time of call.

### Request

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `position_id` | string (UUID) | Yes | Position identifier |

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "overall_status": "fail",
  "checks": [
    { "rule_key": "regime_gate", "status": "pass", "detail": "US market is Risk-On (SPY above 200-day MA)" },
    { "rule_key": "cash_constraint", "status": "fail", "detail": "Estimated cost £2,150.00 exceeds available cash £500.00" },
    { "rule_key": "sector_concentration", "status": "warn", "detail": "Current Energy sector allocation 34.2% exceeds 30.0% advisory limit" },
    { "rule_key": "earnings_proximity", "status": "pass", "detail": "Next earnings 2026-08-01 (22 days) — outside 5-day proximity window" },
    { "rule_key": "sizing_validity", "status": "pass", "detail": "Stop distance 15.0 is valid (entry 215.0, stop 200.0)" }
  ]
}
```

#### Field notes

| Field | Notes |
|-------|-------|
| `overall_status` | `"pass"` / `"warn"` / `"fail"`. Aggregated fail > warn > pass across the 5 checks; `skipped` checks excluded from aggregation (same aggregation rule as `GET /portfolio/pre-entry-validation`). |
| `checks` | Array of exactly 5 entries — the same rule keys as `strategy_rules.md` §4.2: `regime_gate`, `cash_constraint`, `sector_concentration`, `earnings_proximity`, `sizing_validity`. |
| `checks[].rule_key` | One of the 5 canonical SI-01 rule keys above. |
| `checks[].status` | `"pass"` / `"warn"` / `"fail"` / `"skipped"` (skipped when required data is unavailable, e.g. no live price). |
| `checks[].detail` | Human-readable explanation, matching the phrasing convention of `GET /portfolio/pre-entry-validation`. |

**Current-state adaptation notes:**
- `sizing_validity` uses the position's current effective stop (trailing stop if set, else the entry-time initial stop) against its original entry price — reflecting current risk state, not the entry-time snapshot.
- `sector_concentration` excludes the position being rechecked from the baseline sector-value sum before adding back its own live-priced contribution, avoiding the double-count that a literal reuse of the prospective-entry formula would produce for an already-open position.
- `cash_constraint` and `regime_gate` re-run unmodified — they reflect current market/cash conditions regardless of whether the position is new or already open.

### Errors

Errors use the standard error envelope from **conventions.md**.

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Position not found, or position is not open |
| `500` | Internal server error |

---

## GET /positions/{position_id}/gap-risk

**Added:** v6.9 (ST-02, BLG-FEAT-65)

**Purpose**

Returns the overnight/weekend gap risk flag for a single open position, combining
the DS-04 earnings calendar with historical OHLCV gap statistics.

**Scope constraint (§13):** Display-only. Surfaces a known calendar event (earnings
date) and a historical statistic (average gap magnitude) — does not predict gap
direction or magnitude for the upcoming event. No automated action is triggered.
Strategy Rules & System Intent Owner DoQ sign-off required at delivery verification.

**Implementation note:** The story anticipated a `gap_risk` field on the existing
`GET /positions` response; a dedicated per-position endpoint was used instead
(pre-authorised alternative per the story notes) because the historical-OHLCV
lookup is too slow to run inline for every open position on every list load. This
mirrors the existing per-ticker `GET /earnings/{ticker}` pattern already used by
the Positions page Earnings column, and the Alerts column already defines an
independent per-cell loading state, so a lazily-fetched endpoint fits the
documented UX without slowing the bulk list.

**Method & Path**

- `GET /positions/{position_id}/gap-risk`

**Idempotency**

- Safe to repeat (read-only).

### Request

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `position_id` | string (UUID) | Yes | Position identifier |

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "flagged": true,
  "reasons": ["earnings", "weekend_hold"],
  "avg_gap_pct": 2.3,
  "event_count": 14,
  "insufficient_history": false
}
```

#### Field notes

| Field | Notes |
|-------|-------|
| `flagged` | `boolean`. `true` when either an earnings date falls before the position's next trading session, or it is a weekend-hold position at Friday close. |
| `reasons` | Array, subset of `["earnings", "weekend_hold"]`, in that order. Empty when `flagged = false`. Both can be present simultaneously (e.g. Friday close + Monday earnings). |
| `avg_gap_pct` | `float \| null`. Historical average overnight or weekend gap magnitude for the ticker (whichever gap type applies — weekend takes precedence when both reasons apply, per the ux_spec.md §4 combined example). `null` when `insufficient_history = true`. |
| `event_count` | `integer`. Number of historical gap events used to compute `avg_gap_pct`. |
| `insufficient_history` | `boolean`. `true` when fewer than the backend-defined minimum event count (currently 10) is available. The flag is still shown when `true` — insufficient history does not suppress the flag, only the numeric average. |

**Determinism note:** Earnings proximity uses a same-day-or-next-day calendar window (`days_until_earnings` in `[0, 1]`) as "before the position's next trading session" — a deterministic calendar check only; no attempt is made to infer before/after-market release timing, which the upstream earnings data source does not reliably expose. Weekend-hold is a pure day-of-week check (Friday), computed server-side; the frontend renders the flag as returned with no client-side day-of-week logic.

### Errors

Errors use the standard error envelope from **conventions.md**.

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Position not found |
| `500` | Internal server error |

---

## PATCH /positions/{position_id}/mark-reviewed

**Added:** v7.0 (ST-15, BLG-FEAT-68)

**Purpose**

Sets `last_reviewed_at = NOW()` for the given position — the confirm action for the
position review cadence nudge (§Last Reviewed Column, `positions.md`).

**Scope constraint (§13):** Display-only. No automated action beyond the explicit
user-triggered timestamp update. No recommendation, no directional signal.

**Method & Path**

- `PATCH /positions/{position_id}/mark-reviewed`

**Idempotency**

- Mutating, but idempotent in effect — repeat calls simply reset `last_reviewed_at`
  to a later `NOW()`. No confirmation modal on the frontend; low-stakes, reversible
  in spirit (the flag re-fires again after the threshold naturally re-elapses).

### Request

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `position_id` | string (UUID) | Yes | Position identifier |

No body.

### Response (200)

Response uses the standard success envelope from **conventions.md**.

#### `data` schema

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "last_reviewed_at": "2026-07-13T10:00:00+00:00"
}
```

### Errors

Errors use the standard error envelope from **conventions.md**.

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Position not found |
| `500` | Internal server error |
