# alerts_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.1
**Last Updated:** 2026-03-20
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**ADR Reference:** `docs/adr/ADR-003-notification-delivery-architecture.md` — FastAPI BackgroundTasks delivery architecture
**Design Gate:** `claude/cycles/2026-03-18__release-v2.1/` — EPIC-02
**Signed off by:** Head of Specs Team
**Sign-off date:** 2026-03-20

---

## Overview

This document defines the **Alerts & Notifications** domain endpoints for EPIC-02 (v2.1).

The domain covers four concerns:

1. **Alert rule configuration** — per-type enable/disable and threshold settings (`/alerts/rules`)
2. **Alert evaluation** — trigger evaluation of all active rules against current portfolio state (`/alerts/evaluate`)
3. **Notification feed** — the log of triggered alert instances, with read/unread state (`/notifications`)
4. **Notification preferences** — per-type email delivery configuration (`/notifications/preferences`)

### Architecture mode

Notification delivery uses **FastAPI `BackgroundTasks`** (ADR-003, Option C). Email delivery is enqueued as a background task after the triggering API response is returned. No Redis, Celery, or external worker infrastructure is required.

Delivery tracking fields (`delivered`, `delivery_attempted_at`, `delivery_attempts`, `delivery_error`) are stored on the `notifications` table. Re-delivery is attempted on the next evaluation cycle if `delivered = false` and `delivery_attempts < 3`.

> **Note — table naming:** ADR-003's implementation contract sketch uses the name `alerts` for the delivery-tracking table. This spec supersedes that sketch. The canonical table name is `notifications`. The `deliver_notification` function signature and retry model from ADR-003 apply unchanged; only the table name differs.

### Router ordering constraint

The FastAPI router must declare `/notifications/mark-all-read` **before** `/notifications/{id}`. If declared after, FastAPI will route `POST /notifications/mark-all-read` to the `PATCH /notifications/{id}` handler with `id = "mark-all-read"`. This is a backend implementation requirement, not a contract difference.

### Alert types

| Type key | Description | Trigger condition |
|----------|-------------|-------------------|
| `stop_loss_approach` | Stop price close to current price | `(current_price − current_stop) / current_price × 100 ≤ threshold_percent` — evaluated per open position with `current_stop` and `current_price` populated |
| `grace_period_warning` | Position entering final grace days | `holding_days ≥ min_hold_days − 2` AND `holding_days < min_hold_days` — fires on the last two days of the grace period regardless of the configured `min_hold_days` value |
| `market_regime_change` | Market regime transitions to risk-off | `GET /market/status` regime changes to `risk_off` |
| `daily_portfolio_summary` | Daily portfolio digest | Scheduled trigger (once per day per portfolio) |

Global response envelopes, error shape, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise.

---

## Endpoints

### Alert Rules

- [GET /alerts/rules](#get-alertsrules)
- [POST /alerts/rules](#post-alertsrules)
- [PATCH /alerts/rules/{rule_id}](#patch-alertsrulesrule_id)
- [DELETE /alerts/rules/{rule_id}](#delete-alertsrulesrule_id)

### Alert Evaluation

- [POST /alerts/evaluate](#post-alertsevaluate)

### Notifications

- [GET /notifications](#get-notifications)
- [PATCH /notifications/{id}](#patch-notificationsid)
- [POST /notifications/mark-all-read](#post-notificationsmark-all-read)

### Notification Preferences

- [GET /notifications/preferences](#get-notificationspreferences)
- [PATCH /notifications/preferences](#patch-notificationspreferences)

---

## Alert Rules

## GET /alerts/rules

**Purpose**

Return all alert rules for the portfolio. If no rules exist (first use), the backend seeds defaults for all four alert types before returning.

**Method & Path**

- `GET /alerts/rules`

**Idempotency**

- Safe to refresh (read-only).

#### Request

No parameters.

#### Response (200)

Response uses the standard success envelope from **conventions.md**.

##### `data` schema (array)

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "type": "stop_loss_approach",
    "enabled": true,
    "threshold_percent": 5.0,
    "created_at": "2026-03-20T00:00:00Z",
    "updated_at": "2026-03-20T00:00:00Z"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "type": "grace_period_warning",
    "enabled": true,
    "threshold_percent": null,
    "created_at": "2026-03-20T00:00:00Z",
    "updated_at": "2026-03-20T00:00:00Z"
  }
]
```

##### Field definitions

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | No | Alert rule identifier |
| `type` | string | No | One of: `stop_loss_approach`, `grace_period_warning`, `market_regime_change`, `daily_portfolio_summary` |
| `enabled` | boolean | No | Whether this rule is evaluated during `POST /alerts/evaluate` |
| `threshold_percent` | float | Yes | Only for `stop_loss_approach` — trigger when current stop is within this % of current price. `null` for all other types. Default: `5.0` |
| `created_at` | string (ISO 8601) | No | Rule creation timestamp |
| `updated_at` | string (ISO 8601) | No | Last update timestamp |

##### Default values (seeded on first use)

| Type | `enabled` | `threshold_percent` |
|------|-----------|---------------------|
| `stop_loss_approach` | `true` | `5.0` |
| `grace_period_warning` | `true` | `null` |
| `market_regime_change` | `true` | `null` |
| `daily_portfolio_summary` | `true` | `null` |

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Internal server error |

---

## POST /alerts/rules

**Purpose**

Create an alert rule. Primarily used to restore a rule after deletion. Under normal operation, rules are seeded automatically by `GET /alerts/rules`. Returns `400` if a rule for the given type already exists (use `PATCH /alerts/rules/{rule_id}` to update).

**Method & Path**

- `POST /alerts/rules`

#### Request Body

```json
{
  "type": "stop_loss_approach",
  "enabled": true,
  "threshold_percent": 5.0
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Alert type. Must be one of the four valid type keys. |
| `enabled` | boolean | No | Default: `true` |
| `threshold_percent` | float | No | Required only for `stop_loss_approach`. Must be `> 0` and `≤ 100`. Ignored for other types. |

#### Validation rules

- `type` must be one of: `stop_loss_approach`, `grace_period_warning`, `market_regime_change`, `daily_portfolio_summary`
- A rule for the given `type` must not already exist for this portfolio
- `threshold_percent` must be `> 0` and `≤ 100` when provided
- `threshold_percent` is required when `type = stop_loss_approach`

#### Response (200)

```json
{
  "status": "ok",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "type": "stop_loss_approach",
    "enabled": true,
    "threshold_percent": 5.0,
    "created_at": "2026-03-20T10:00:00Z",
    "updated_at": "2026-03-20T10:00:00Z"
  }
}
```

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `type` missing or invalid |
| `400` | Rule for this `type` already exists |
| `400` | `threshold_percent` invalid or missing for `stop_loss_approach` |
| `500` | Internal server error |

---

## PATCH /alerts/rules/{rule_id}

**Purpose**

Update an alert rule. Supports partial update — include only the fields to change.

**Method & Path**

- `PATCH /alerts/rules/{rule_id}`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `rule_id` | UUID | Alert rule identifier |

#### Request Body

```json
{
  "enabled": false,
  "threshold_percent": 10.0
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled` | boolean | No | Enable or disable this rule |
| `threshold_percent` | float | No | Only for `stop_loss_approach`. Must be `> 0` and `≤ 100` if provided. |

At least one field must be present.

#### Validation rules

- `rule_id` must exist
- `threshold_percent` must be `> 0` and `≤ 100` if provided
- `threshold_percent` is ignored (not an error) if the rule type is not `stop_loss_approach`

#### Response (200)

Returns the updated alert rule object (same shape as `GET /alerts/rules` items).

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `400` | No updatable fields provided |
| `400` | `threshold_percent` out of valid range |
| `404` | `rule_id` not found |
| `500` | Internal server error |

---

## DELETE /alerts/rules/{rule_id}

**Purpose**

Delete an alert rule. The rule may be recreated via `POST /alerts/rules`.

**Method & Path**

- `DELETE /alerts/rules/{rule_id}`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `rule_id` | UUID | Alert rule identifier |

#### Response (200)

Uses the standard DELETE envelope from **conventions.md §12**:

```json
{
  "status": "ok",
  "data": {
    "deleted": true,
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `404` | `rule_id` not found |
| `500` | Internal server error |

---

## Alert Evaluation

## POST /alerts/evaluate

**Purpose**

Evaluate all enabled alert rules against the current portfolio state. For each triggered rule, a notification record is written and email delivery is enqueued as a FastAPI `BackgroundTask` (per ADR-003). The response is returned immediately — delivery happens after the response is sent.

Re-delivery: on each evaluation, if a prior notification has `delivered = false` and `delivery_attempts < 3`, delivery is re-enqueued.

**Method & Path**

- `POST /alerts/evaluate`

**Idempotency**

- Not idempotent. Each call may generate new notification records.
- `daily_portfolio_summary`: one notification per portfolio per calendar day (UTC). Duplicate evaluation on the same day does not create a second summary notification.

**Trigger evaluation rules**

| Type | Rule |
|------|------|
| `stop_loss_approach` | For each open position where `current_stop IS NOT NULL` and `current_price IS NOT NULL`: fire if `(current_price − current_stop) / current_price × 100 ≤ threshold_percent`. One notification per position per evaluation (no deduplication across evaluations — ST-03 may implement a cooldown). |
| `grace_period_warning` | For each open position: fire if `holding_days >= settings.min_hold_days − 2` AND `holding_days < settings.min_hold_days`. With default `min_hold_days = 10`: fires on days 8 and 9. |
| `market_regime_change` | Fire when `GET /market/status` regime transitions to `risk_off` (state change, not sustained state). Implementation should track last-known regime in application state or a dedicated column. |
| `daily_portfolio_summary` | Fire once per calendar day (UTC) per portfolio. Deduplication: check for existing `daily_portfolio_summary` notification with `created_at::date = CURRENT_DATE` before inserting. |

#### Request

No body required.

#### Response (200)

```json
{
  "status": "ok",
  "data": {
    "rules_evaluated": 4,
    "notifications_created": 2,
    "delivery_tasks_enqueued": 2,
    "redelivery_tasks_enqueued": 0
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `rules_evaluated` | integer | Number of enabled rules evaluated |
| `notifications_created` | integer | New notification records written this call |
| `delivery_tasks_enqueued` | integer | Background tasks enqueued for new notifications (where email is enabled in preferences) |
| `redelivery_tasks_enqueued` | integer | Background tasks enqueued for prior notifications where `delivered = false` and `delivery_attempts < 3` |

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Internal server error |

---

## Notifications

## GET /notifications

**Purpose**

Return the notification feed for the portfolio, newest first. Supports page-based pagination (50 items per page).

**Method & Path**

- `GET /notifications`

**Idempotency**

- Safe to refresh (read-only).

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | `1` | Page number (1-indexed). |

#### Validation rules

- `page` must be a positive integer if provided.

#### Response (200)

```json
{
  "status": "ok",
  "data": {
    "notifications": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440000",
        "alert_type": "stop_loss_approach",
        "title": "Stop Loss Approach — AAPL",
        "message": "AAPL stop (210.00) is within 4.2% of current price (219.05). Consider reviewing your stop.",
        "read": false,
        "created_at": "2026-03-20T09:15:00Z"
      }
    ],
    "total": 3,
    "page": 1,
    "per_page": 50,
    "has_more": false
  }
}
```

##### Field definitions — `data`

| Field | Type | Description |
|-------|------|-------------|
| `notifications` | array | Notification items, newest first |
| `total` | integer | Total notification count for this portfolio |
| `page` | integer | Current page number |
| `per_page` | integer | Items per page (always `50`) |
| `has_more` | boolean | `true` if more pages exist beyond current page |

##### Field definitions — `notifications[]`

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | No | Notification identifier |
| `alert_type` | string | No | One of the four alert type keys |
| `title` | string | No | Human-readable alert title (e.g. `"Stop Loss Approach — AAPL"`) |
| `message` | string | No | One-line description of the event |
| `read` | boolean | No | `false` for unread; `true` after mark-read |
| `created_at` | string (ISO 8601) | No | Timestamp the notification was created |

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `page` is not a positive integer |
| `500` | Internal server error |

---

## PATCH /notifications/{id}

**Purpose**

Mark a single notification as read. Sets `read = true`. Idempotent — calling again on an already-read notification returns success without error.

**Method & Path**

- `PATCH /notifications/{id}`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Notification identifier |

#### Request

No body required.

#### Response (200)

Returns the updated notification object (same shape as items in `GET /notifications`):

```json
{
  "status": "ok",
  "data": {
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "alert_type": "stop_loss_approach",
    "title": "Stop Loss Approach — AAPL",
    "message": "AAPL stop (210.00) is within 4.2% of current price (219.05). Consider reviewing your stop.",
    "read": true,
    "created_at": "2026-03-20T09:15:00Z"
  }
}
```

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `404` | Notification `id` not found |
| `500` | Internal server error |

---

## POST /notifications/mark-all-read

**Purpose**

Mark all unread notifications as read. Idempotent — if all notifications are already read, returns success with `marked_read_count: 0`.

**Method & Path**

- `POST /notifications/mark-all-read`

#### Request

No body required.

#### Response (200)

```json
{
  "status": "ok",
  "data": {
    "marked_read_count": 12
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `marked_read_count` | integer | Number of notifications updated from `read = false` to `read = true`. `0` if all were already read. |

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Internal server error |

---

## Notification Preferences

## GET /notifications/preferences

**Purpose**

Return notification preferences for all four alert types. If no preferences exist (first use), the backend seeds defaults (all email enabled) before returning.

**Method & Path**

- `GET /notifications/preferences`

**Idempotency**

- Safe to refresh (read-only).

#### Request

No parameters.

#### Response (200)

```json
{
  "status": "ok",
  "data": {
    "preferences": [
      {
        "alert_type": "stop_loss_approach",
        "email_enabled": true
      },
      {
        "alert_type": "grace_period_warning",
        "email_enabled": true
      },
      {
        "alert_type": "market_regime_change",
        "email_enabled": true
      },
      {
        "alert_type": "daily_portfolio_summary",
        "email_enabled": true
      }
    ]
  }
}
```

##### Field definitions

| Field | Type | Description |
|-------|------|-------------|
| `preferences` | array | One entry per alert type. Always 4 items (one per type). |
| `alert_type` | string | Alert type key |
| `email_enabled` | boolean | `true` = send email when this alert type triggers; `false` = suppress email |

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Internal server error |

---

## PATCH /notifications/preferences

**Purpose**

Update notification preferences for one or more alert types. Partial update — include only the types to change. Unspecified types are unaffected.

**Method & Path**

- `PATCH /notifications/preferences`

#### Request Body

A JSON object where each key is an alert type and the value is a preferences update object:

```json
{
  "stop_loss_approach": { "email_enabled": false },
  "grace_period_warning": { "email_enabled": true }
}
```

#### Validation rules

- All keys must be valid alert type keys.
- At least one key must be present.
- `email_enabled` must be a boolean.

#### Response (200)

Returns the full updated preferences list (same shape as `GET /notifications/preferences`):

```json
{
  "status": "ok",
  "data": {
    "preferences": [
      { "alert_type": "stop_loss_approach", "email_enabled": false },
      { "alert_type": "grace_period_warning", "email_enabled": true },
      { "alert_type": "market_regime_change", "email_enabled": true },
      { "alert_type": "daily_portfolio_summary", "email_enabled": true }
    ]
  }
}
```

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `400` | No valid alert type keys provided |
| `400` | Unknown alert type key in request body |
| `400` | `email_enabled` is not a boolean |
| `500` | Internal server error |

---

## Data Model Cross-Reference

All tables defined below are specified in full in `docs/specs/data_model.md §8`.

| Table | Purpose |
|-------|---------|
| `alert_rules` | Per-type rule configuration (enabled, threshold) |
| `notifications` | Triggered alert instances with delivery tracking |
| `notification_preferences` | Per-type email delivery preferences |

Delivery tracking columns on `notifications` (`delivered`, `delivery_attempted_at`, `delivery_attempts`, `delivery_error`) implement the retry model specified in ADR-003.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-20 | Initial version. Full endpoint spec for EPIC-02 Alerts & Notifications. ST-02 — v2.1 release planning cycle 2026-03-18__release-v2.1. Architecture: FastAPI BackgroundTasks per ADR-003. HoST sign-off 2026-03-20: 4 review findings addressed (router ordering, grace period formula, proximity formula, table naming note). |
