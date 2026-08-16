# alerts_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.7
**Last Updated:** 2026-08-14 (ST-09, EPIC-02, v8.8, BLG-BE-84 — GET /notifications now exposes `context`; `alert_type` field description corrected to include `custom_price_alert`, missed since v0.5); prior — 2026-07-23
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**ADR Reference:** `docs/adr/ADR-003-notification-delivery-architecture.md` — FastAPI BackgroundTasks delivery architecture
**Design Gate:** `claude/cycles/2026-03-18__release-v2.1/` — EPIC-02
**Signed off by:** Head of Specs Team
**Sign-off date:** 2026-03-20

---

## Overview

This document defines the **Alerts & Notifications** domain endpoints for EPIC-02 (v2.1).

The domain covers five concerns:

1. **Alert rule configuration** — per-type enable/disable and threshold settings (`/alerts/rules`)
2. **Alert evaluation** — trigger evaluation of all active rules against current portfolio state (`/alerts/evaluate`)
3. **Notification feed** — the log of triggered alert instances, with read/unread state (`/notifications`)
4. **Notification preferences** — per-type email delivery configuration (`/notifications/preferences`)
5. **Custom price alerts** — user-defined, per-ticker threshold alerts, unconstrained by open positions (`/price-alerts`, v7.5 / ST-02 / BLG-FE-116)

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

### Custom Price Alerts

- [GET /price-alerts](#get-price-alerts)
- [POST /price-alerts](#post-price-alerts)
- [DELETE /price-alerts/{id}](#delete-price-alertsid)

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

## Custom Price Alerts

User-defined, per-ticker threshold alerts (ST-02, BLG-FE-116, EPIC-02, v7.5). Unlike `/alerts/rules` (singleton-per-type, `alert_rules` table), a portfolio may have an arbitrary number of `price_alerts` rows, each scoped to any ticker (not limited to open positions or the watchlist). Evaluated as a step inside `POST /alerts/evaluate` — no separate trigger endpoint. Readiness baseline: `docs/specs/blg_fe_116_pre_implementation_readiness_pass.md`.

## GET /price-alerts

**Purpose**

Return all custom price alerts for the portfolio, most recently created first.

**Method & Path**

- `GET /price-alerts`

**Idempotency**

- Safe to refresh (read-only).

#### Request

No parameters.

#### Response (200)

```json
{
  "status": "ok",
  "data": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "ticker": "AAPL",
      "condition": "above",
      "threshold_price": 150.0,
      "active": true,
      "triggered_at": null,
      "created_at": "2026-07-17T10:00:00Z",
      "updated_at": "2026-07-17T10:00:00Z"
    }
  ]
}
```

##### Field definitions

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | UUID | No | Price alert identifier |
| `ticker` | string | No | Any ticker accepted by the pricing utility — not constrained to open positions or watchlist |
| `condition` | string | No | `above` or `below` |
| `threshold_price` | float | No | Trigger price, `> 0` |
| `active` | boolean | No | `true` until triggered (single-fire) or explicitly deactivated |
| `triggered_at` | string (ISO 8601) | Yes | `null` until fired |
| `created_at` | string (ISO 8601) | No | Alert creation timestamp |
| `updated_at` | string (ISO 8601) | No | Last update timestamp |

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Internal server error |

---

## POST /price-alerts

**Purpose**

Create a custom price alert.

**Method & Path**

- `POST /price-alerts`

#### Request Body

```json
{
  "ticker": "AAPL",
  "condition": "above",
  "threshold_price": 150.0
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | Yes | 1–10 alphanumeric characters (uppercased server-side); same validation as the Watchlist "Add Ticker" field |
| `condition` | string | Yes | Must be `above` or `below` |
| `threshold_price` | float | Yes | Must be `> 0` |

#### Validation rules

- `ticker` must match `^[A-Z0-9.]{1,10}$` (case-insensitive on input, uppercased before storage)
- `condition` must be `above` or `below`
- `threshold_price` must be `> 0`
- The portfolio must have fewer than 50 active (`active = true`) price alerts — this cap bounds both abuse and the nightly evaluation job's runtime (readiness pass AC-03/AC-04)

#### Response (200)

```json
{
  "status": "ok",
  "data": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "ticker": "AAPL",
    "condition": "above",
    "threshold_price": 150.0,
    "active": true,
    "triggered_at": null,
    "created_at": "2026-07-17T10:00:00Z",
    "updated_at": "2026-07-17T10:00:00Z"
  }
}
```

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `ticker` missing or invalid format |
| `400` | `condition` missing or not one of `above`/`below` |
| `400` | `threshold_price` missing or not `> 0` |
| `400` | Active-alert cap (50) exceeded — message: `"You've reached the maximum number of active price alerts."` |
| `500` | Internal server error |

---

## DELETE /price-alerts/{id}

**Purpose**

Delete a custom price alert (active or already-triggered).

**Method & Path**

- `DELETE /price-alerts/{id}`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Price alert identifier |

#### Response (200)

Uses the standard DELETE envelope from **conventions.md §12**:

```json
{
  "status": "ok",
  "data": {
    "deleted": true,
    "id": "770e8400-e29b-41d4-a716-446655440002"
  }
}
```

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `404` | `id` not found |
| `500` | Internal server error |

---

### Evaluation & Notification Feed Integration

- `POST /alerts/evaluate` evaluates all `active = true` price alerts as an additional step (reuses the existing scheduled trigger — no second cron). For each: fetch current price via `utils.pricing.get_current_price(ticker)`, compare against `threshold_price` per `condition`; on trigger, write a `notifications` row (`alert_type: 'custom_price_alert'`), set `active = false`, `triggered_at = now()`.
- Triggered custom price alerts appear in `GET /notifications` using the existing feed row shape — no new feed-row variant. Title format: `"Price Alert — {TICKER} {above/below} {threshold}"`.
- `GET /health/scheduler` surfaces evaluation status under the `custom_price_alerts` job key (`trigger_endpoints.custom_price_alerts = "co-invoked by POST /alerts/evaluate"`).
- §13 pre-check: **PASS** (readiness pass AC-05) — notification-only, no order placement or position mutation, advisory only.

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
| `stop_loss_approach` | For each open position where `current_stop IS NOT NULL` and `current_price IS NOT NULL`: fire if `(current_price − current_stop) / current_price × 100 ≤ threshold_percent`. **Calendar-day deduplication:** one notification per position per alert type per UTC calendar day. If evaluation runs multiple times on the same day, only the first dispatch is sent; subsequent evaluations for the same (portfolio, type, ticker, date) are logged and skipped. |
| `grace_period_warning` | For each open position: fire if `holding_days >= settings.min_hold_days − 2` AND `holding_days < settings.min_hold_days`. With default `min_hold_days = 10`: fires on days 8 and 9. **Calendar-day deduplication:** same (portfolio, type, ticker, date) key as `stop_loss_approach`. Duplicate dispatches are logged and skipped. |
| `market_regime_change` | Fire when regime transitions to `risk_off` (state change only, not sustained state). Deduplication via in-process last-known regime state — cold start does not fire; only genuine transitions fire. |
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
| `since_days` | integer | No | none | Restrict to notifications created within the last N days. Applied before pagination. Added (v0.6, ST-02/EPIC-02/v7.7) so `weekly_digest.md`'s `Alerts Fired (7d)` / `Alerts Dismissed (7d)` values can deep-link here (`/notifications?since_days=7`). |
| `read` | boolean | No | none | Restrict to read-only (`true`) or unread-only (`false`) items. Applied before pagination. Added (v0.6, ST-02/EPIC-02/v7.7) for the `Alerts Dismissed (7d)` deep-link (`/notifications?since_days=7&read=true`). |

#### Validation rules

- `page` must be a positive integer if provided.
- `since_days` must be a positive integer if provided.

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
        "created_at": "2026-03-20T09:15:00Z",
        "context": null
      },
      {
        "id": "880e8400-e29b-41d4-a716-446655440001",
        "alert_type": "custom_price_alert",
        "title": "Price Alert — TSLA above 250.00",
        "message": "TSLA crossed above your threshold of 250.00 (current: 251.30).",
        "read": false,
        "created_at": "2026-08-14T14:00:00Z",
        "context": {
          "ticker": "TSLA",
          "condition": "above",
          "threshold_price": 250.0,
          "current_price": 251.3,
          "price_alert_id": "990e8400-e29b-41d4-a716-446655440002"
        }
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
| `alert_type` | string | No | `stop_loss_approach` \| `grace_period_warning` \| `market_regime_change` \| `daily_portfolio_summary` \| `custom_price_alert` (doc-currency correction, ST-09 EPIC-02 v8.8 — `custom_price_alert` has existed since v0.5/ST-02/v7.5/BLG-FE-116 but was missed here) |
| `title` | string | No | Human-readable alert title (e.g. `"Stop Loss Approach — AAPL"`) |
| `message` | string | No | One-line description of the event |
| `read` | boolean | No | `false` for unread; `true` after mark-read |
| `created_at` | string (ISO 8601) | No | Timestamp the notification was created |
| `context` | object | Yes | *(v0.7 — ST-09, EPIC-02, v8.8, BLG-BE-84)* Alert-type-specific metadata, stored at creation time. Was already persisted but never exposed by this endpoint before this story. For `custom_price_alert`: `{ticker, condition, threshold_price, current_price, price_alert_id}` — `price_alert_id` is the triggering `price_alerts` row's id, used by the frontend's "create trade plan from this alert" path (`trade_plan_endpoints.md`'s `triggered_by_price_alert_id`). Null/absent for other alert types (no context is written for them today). |

#### Error Responses

| HTTP Status | Condition |
|-------------|-----------|
| `400` | `page` is not a positive integer |
| `400` | `since_days` is not a positive integer |
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

## GET /alerts/history

Return alert evaluation history — the audit log of every rule evaluated by `POST /alerts/evaluate`.

**Query parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `last_n_days` | integer | No | Return evaluations from the last N calendar days. Default: 30. |
| `last_n_records` | integer | No | Return the last N records regardless of date. Takes precedence over `last_n_days` when both supplied. |

**Response (200):**

```json
{
  "status": "ok",
  "data": {
    "evaluations": [
      {
        "id": "uuid",
        "evaluation_timestamp": "2026-03-23T21:00:00Z",
        "rule_type": "stop_loss_approach",
        "symbol": "AAPL",
        "triggered": true,
        "notification_sent": true,
        "values_compared": {
          "stop_price": 42.10,
          "current_price": 43.50,
          "gap_pct": 3.3,
          "threshold_pct": 5.0
        }
      }
    ],
    "total": 47
  }
}
```

**Field descriptions:**

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Evaluation record ID |
| `evaluation_timestamp` | ISO 8601 | UTC timestamp of the evaluation |
| `rule_type` | string | One of the four alert type keys |
| `symbol` | string \| null | Position ticker for position-specific rules; `null` for `market_regime_change` and `daily_portfolio_summary` |
| `triggered` | boolean | Whether a new notification was created in this evaluation |
| `notification_sent` | boolean | Whether delivery was enqueued (false if triggered=false, or preference disabled, or calendar-day dedup applied) |
| `values_compared` | object | Key-value map of comparison values used in the evaluation. Schema varies by rule type (see below). |

**`values_compared` by rule type:**

| Rule type | Keys |
|-----------|------|
| `stop_loss_approach` | `stop_price`, `current_price`, `gap_pct`, `threshold_pct` |
| `grace_period_warning` | `holding_days`, `min_hold_days`, `days_remaining` |
| `market_regime_change` | `spy_risk_on`, `ftse_risk_on` (present only when triggered) |
| `daily_portfolio_summary` | `open_positions` |

**Error responses:**

| HTTP Status | Condition |
|-------------|-----------|
| `500` | Internal server error |

---

## Data Model Cross-Reference

All tables defined below are specified in full in `docs/specs/data_model.md §8`.

| Table | Purpose |
|-------|---------|
| `alert_rules` | Per-type rule configuration (enabled, threshold) |
| `notifications` | Triggered alert instances with delivery tracking |
| `notification_preferences` | Per-type email delivery preferences |
| `alert_evaluations` | Audit log of every rule evaluation (v0.3) |
| `price_alerts` | User-defined, per-ticker threshold alerts (v0.5, ST-02/BLG-FE-116) |

Delivery tracking columns on `notifications` (`delivered`, `delivery_attempted_at`, `delivery_attempts`, `delivery_error`) implement the retry model specified in ADR-003.

---

## Known Deviations

### DEV-ST04-01 — Notification delivery channel: Telegram instead of email

- **Description:** Notification delivery is implemented via Telegram Bot API. The spec and ADR-003 specify email delivery (Gmail SMTP). Email delivery is not active on Render free tier due to SMTP blocking (Gmail) and paid domain requirement (Brevo).
- **Canonical requirement:** `POST /alerts/evaluate` triggers email delivery via SMTP when a rule fires.
- **Priority:** P2
- **Target resolution release:** v2.2 (pending paid infrastructure)
- **Owner:** Head of Engineering + Infrastructure & Operations Owner
- **Backlog reference:** BLG-OPS-04 — Alert evaluation scheduling: trigger mechanism and rule behaviour design
- **Acceptance record:** Product Owner 2026-03-20; Director of Quality 2026-03-20. Core delivery behaviour confirmed on staging. Channel deviation accepted given Render free-tier constraint.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.6 | 2026-07-23 | ST-02 (v7.7, EPIC-02, BLG-FE-114): Added optional `since_days` / `read` query params to `GET /notifications` so `weekly_digest.md`'s `Alerts Fired (7d)` / `Alerts Dismissed (7d)` values can deep-link into the filtered Notification Feed. Both applied before pagination; absent params preserve prior unfiltered behaviour. |
| 0.5 | 2026-07-17 | ST-02 (v7.5, EPIC-02, BLG-FE-116): Added `## Custom Price Alerts` domain — `GET/POST /price-alerts`, `DELETE /price-alerts/{id}`. New `price_alerts` table (many-rows-per-portfolio, distinct from singleton `alert_rules`). Evaluation folded into the existing `POST /alerts/evaluate` step (no new cron). `GET /health/scheduler` surfaces a `custom_price_alerts` job key. Readiness baseline: `docs/specs/blg_fe_116_pre_implementation_readiness_pass.md`. |
| 0.4 | 2026-04-01 | ST-02 (v2.4): Trigger evaluation rules table updated — deduplication behaviour documented for all four alert types. `stop_loss_approach` and `grace_period_warning` dedup logging added (log and skip on second evaluation same UTC day). Calendar-day dedup key: (portfolio, type, ticker, date). |
| 0.3 | 2026-03-23 | ST-05 (v2.2): Added `## GET /alerts/history` endpoint. Added `alert_evaluations` table to Data Model Cross-Reference. `POST /alerts/evaluate` now persists one evaluation record per rule/position evaluated (calendar-day dedup applied to stop_loss_approach and grace_period_warning). |
| 0.2 | 2026-03-21 | Post-ship closure: Known Deviations section added. DEV-ST04-01 (Telegram delivery) filed per post_ship_closure STEP 5 — deviation compliance. |
| 0.1 | 2026-03-20 | Initial version. Full endpoint spec for EPIC-02 Alerts & Notifications. ST-02 — v2.1 release planning cycle 2026-03-18__release-v2.1. Architecture: FastAPI BackgroundTasks per ADR-003. HoST sign-off 2026-03-20: 4 review findings addressed (router ordering, grace period formula, proximity formula, table naming note). |
