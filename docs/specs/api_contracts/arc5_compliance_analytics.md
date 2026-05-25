**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0.0
**Last Updated:** 2026-05-25
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
    "trade_plan_adherence_rate": 0.72
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

---

### Graceful Degradation

If a source table does not exist in the database (e.g. `pre_entry_validation_log` or `red_flag_events`), the endpoint catches `psycopg2.errors.UndefinedTable`, rolls back the cursor, and returns an empty or zero value for that metric rather than raising an error. The response always returns HTTP 200 with the `status: "ok"` envelope.

---

### Error Response (500)

```json
{
  "detail": "Arc 5 compliance metrics failed: <exception message>"
}
```

Raised for unexpected server-side failures unrelated to missing tables (e.g. database connection error, configuration error).
