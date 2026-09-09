**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.2.0
**Last Updated:** 2026-09-09 (ST-04, EPIC-01, v9.3 — `total_closed_trades` is now nullable: `null` distinguishes a missing/broken `trade_history` table from a genuine zero-trades portfolio); prior — 2026-09-07 (ST-01, EPIC-01, v9.2 — added `total_closed_trades` field, backs the low-trade-volume advisory)
**Shipped:** v4.0 — ST-01, EPIC-01, cycle 2026-05-22__release-v4.0
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Arc 5 Compliance Analytics API Contract

## Overview

This document defines the **Arc 5 Compliance Analytics** endpoint — the Arc 5 Strategy Integrity compliance metrics surface (SI-01, SI-03).

The endpoint returns a snapshot of compliance health across five metrics computed from `pre_entry_validation_log` and `red_flag_events` tables. All metrics are server-computed. The frontend must never calculate or derive these values.

**§13 compliance:** This endpoint is read-only and display-only. It does not produce recommendations, gate trade entry, or trigger automated actions. Its sole purpose is surfacing compliance trend data for operator review.

**Canonical metrics definition:** `docs/specs/metrics_definitions.md §Arc 5 Compliance Metrics`

**Backend implementation:** `backend/routers/analytics.py`

Global response envelopes, error shape, and defaults are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

- [GET /analytics/arc5-compliance](#get-analyticsarc5-compliance)

---

## GET /analytics/arc5-compliance

**Purpose**

Return Arc 5 signal compliance metrics for a rolling time window. Covers:

- **Validation pass/fail rate by rule** — per pre-entry rule, the ratio of passes to total validation attempts in the period
- **Red flag event frequency** — count of red flag events in the last 7 days, normalised per day
- **Override rate** — ratio of pre-entry override events to total validation attempts in the last 7 days
- **Top rule breach** — the most frequently failing pre-entry rule in the period
- **Trade plan adherence rate** — ratio of closed trades with an associated trade plan to total closed trades (all-time)

**Method & Path**

- `GET /analytics/arc5-compliance`

**Idempotency**

- Safe and idempotent. Read-only. Deterministic from stored records at time of call.

---

### Request

#### Query Parameters

| Parameter | Type | Required | Default | Allowed values |
|-----------|------|----------|---------|----------------|
| period | string | No | `7d` | `7d`, `30d` |

`period` controls the rolling window for `validation_pass_rate_by_rule` and `top_rule_breach`. `events_per_week` and `override_rate` always use a fixed 7-day window regardless of `period`.

---

### Response (200)

```json
{
  "status": "ok",
  "data": {
    "period": "7d",
    "validation_pass_rate_by_rule": {
      "regime_gate": {
        "pass_rate": 0.85,
        "pass_count": 17,
        "fail_count": 3
      },
      "earnings_proximity": {
        "pass_rate": 1.0,
        "pass_count": 20,
        "fail_count": 0
      }
    },
    "events_per_week": 1.43,
    "override_rate": 0.1,
    "top_rule_breach": "regime_gate",
    "trade_plan_adherence_rate": 0.72,
    "total_closed_trades": 34
  }
}
```

#### `data` schema

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| period | string | No | Echoes the requested period (`7d` or `30d`) |
| validation_pass_rate_by_rule | object | No | Map of rule_type → pass/fail breakdown. Empty object `{}` if no validation records exist in the period or if `pre_entry_validation_log` table does not exist. |
| events_per_week | number | No | Red flag events in the last 7 days divided by 7. Returns `0.0` if no events or if `red_flag_events` table does not exist. |
| override_rate | number | Yes | Pre-entry override events ÷ total validation attempts in the last 7 days. `null` if no validation attempts exist. |
| top_rule_breach | string | Yes | `rule_type` value of the most frequently failing rule in the period. `null` if no failures exist. |
| trade_plan_adherence_rate | number | Yes | Closed trades with associated trade plan ÷ total closed trades (all-time). `null` if no closed trades exist. |
| total_closed_trades | integer | Yes | All-time closed trade count — the denominator of `trade_plan_adherence_rate`. `0` if `trade_history` exists and is genuinely empty (no closed trades yet). `null` if `trade_history` is missing or broken (schema error) — distinct from the genuine-empty case since v1.2.0 (ST-04, EPIC-01, v9.3, BLG-BE-111); before that fix both cases returned `0`, indistinguishable to the frontend. Added v1.1.0 to back the frontend low-trade-volume advisory (`docs/specs/frontend/components/arc5_compliance_section.md` §Low-Trade-Volume Advisory) — that advisory's rendering does not currently branch on `total_closed_trades` being `null` vs. `0` (see Frontend note below). |

#### `validation_pass_rate_by_rule` entry schema

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| pass_rate | number | Yes | Passes ÷ total. `null` if total is zero. Rounded to 4 decimal places. |
| pass_count | integer | No | Count of validation attempts with `status = 'pass'` |
| fail_count | integer | No | Count of validation attempts with `status != 'pass'` |

---

### Data Sources

| Metric | Source table | Window |
|--------|-------------|--------|
| validation_pass_rate_by_rule | `pre_entry_validation_log.validated_at` | `period` param |
| top_rule_breach | `pre_entry_validation_log.validated_at` where `status = 'fail'` | `period` param |
| events_per_week | `red_flag_events.created_at` | Fixed 7 days |
| override_rate | `red_flag_events` (event_type = `pre_entry_override`) + `pre_entry_validation_log` | Fixed 7 days |
| trade_plan_adherence_rate | `trade_history` JOIN `trade_plans` ON `position_id` | All-time |
| total_closed_trades | `trade_history` (row count) — same query as `trade_plan_adherence_rate`'s denominator | All-time |

---

### Graceful Degradation

If a source table does not exist in the database (e.g. `pre_entry_validation_log` or `red_flag_events`), the endpoint catches `psycopg2.errors.UndefinedTable`, rolls back the cursor, and returns an empty or zero value for that metric rather than raising an error. The response always returns HTTP 200 with the `status: "ok"` envelope.

**Exception — `total_closed_trades` (v1.2.0):** unlike the other metrics' empty/zero degradation, a `trade_history` schema error (`UndefinedColumn`/`UndefinedTable`) returns `total_closed_trades: null`, not `0` — `0` is reserved for a genuinely empty (but present and queryable) `trade_history` table. A schema error is an operational fault, not "zero trades so far," and must not be silently rendered as the latter.

---

### Error Response (500)

```json
{
  "detail": "Arc 5 compliance metrics failed: <exception message>"
}
```

Raised for unexpected server-side failures unrelated to missing tables (e.g. database connection error, configuration error).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.2.0 | 2026-09-09 | ST-04 (EPIC-01, v9.3, BLG-BE-111): `total_closed_trades` is now nullable — `null` on a `trade_history` schema error (`UndefinedColumn`/`UndefinedTable`), `0` reserved for a genuine zero-trades portfolio. Previously both cases returned `0`, indistinguishable to the frontend. Fixed in `database.get_arc5_trade_plan_adherence_rate()`; no other field changed. See Frontend note under the field table re: `arc5_compliance_section.md`'s low-trade-volume advisory not yet branching on this distinction. |
| 1.1.0 | 2026-09-07 | Added `total_closed_trades` field (all-time closed trade count, `trade_plan_adherence_rate`'s own denominator) — ST-01, EPIC-01, v9.2, BLG-FEAT-44. Backs the frontend low-trade-volume advisory. No breaking change to existing fields. |
| 1.0.0 | 2026-05-25 | Initial contract — ST-01, EPIC-01, v4.0. |
