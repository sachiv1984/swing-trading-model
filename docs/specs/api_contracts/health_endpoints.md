# health_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.6
**Last Updated:** 2026-08-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Overview

This document defines **Health & Diagnostics** endpoints.

These endpoints are used for:

- Basic service health checks
- Detailed dependency diagnostics
- Automated endpoint test execution

> **Important:** Health endpoints do **not** follow the standard `{ status, data }` response envelope defined in `conventions.md`. They return custom top-level payloads by design.

---

## Endpoints

- [GET /health](#get-health)
- [GET /health/detailed](#get-healthdetailed)
- [GET /health/database](#get-healthdatabase)
- [POST /test/endpoints](#post-testendpoints)
- [GET /test/quick-health](#get-testquick-health)
- [POST /test/rate-limit-scenarios](#post-testrate-limit-scenarios)
- [GET /health/scheduler](#get-healthscheduler)

---

## GET /health

**Purpose**

Provide a lightweight operational health check indicating overall service status, database connectivity, and last operation timestamps.

Typically used by:
- Load balancers
- Uptime monitors
- Deployment verification
- Operational health check playbook (see `docs/operations/health_check_playbook.md`)

**Method & Path**

- `GET /health`

**Idempotency**

- Safe to refresh (read-only).

### Request

No parameters.

### Response (200)

```json
{
  "status": "ok",
  "db": "connected",
  "last_market_status_check": "2026-03-25T09:00:00Z",
  "last_alert_evaluation": "2026-03-25T09:01:00Z",
  "external_apis": {
    "alpaca": {
      "last_successful_call": "2026-08-07T09:14:02+00:00",
      "error_rate": 0.0,
      "p95_latency_ms": 214
    },
    "yahoo_finance": {
      "last_successful_call": "2026-08-07T09:10:47+00:00",
      "error_rate": 0.02,
      "p95_latency_ms": 340
    }
  },
  "ai_journal": {
    "usage_rate": 3.5714,
    "error_rate": 0.0,
    "p95_latency_ms": 1820
  }
}
```

#### Field notes

- `status`: overall service health — `"ok"` when all subsystems are nominal; `"error"` when one or more are failing.
- `db`: database connectivity — `"connected"` when the database is reachable; `"error"` otherwise.
- `last_market_status_check`: ISO 8601 timestamp of the most recent market status check, or `null` if none has run since startup.
- `last_alert_evaluation`: ISO 8601 timestamp of the most recent alert evaluation run, or `null` if none has run since startup.
- `external_apis`: object keyed by external API name (currently `alpaca`, `yahoo_finance`). Each value is `{ last_successful_call: ISO-8601|null, error_rate: float (0–1, over a rolling window of the last 100 calls), p95_latency_ms: int|null }`. An API with no recorded calls since process start reports `last_successful_call: null`, `error_rate: 0.0`, `p95_latency_ms: null`. (ST-08, BLG-OPS-related)
- `ai_journal`: `{ usage_rate: float (AI summaries produced per day, 7-day window), error_rate: float (0–1, 24h window), p95_latency_ms: int|null }`. If no AI journal activity has occurred in the last 7 days (usage) or 24 hours (errors), or the underlying query fails, returns `{ "status": "unavailable" }` instead of the three metric fields. (ST-09)

### Status values

- `"ok"`: all subsystems operational
- `"error"`: one or more subsystems failing (see `db` field and `GET /health/detailed` for diagnostics)

### Notes

- This endpoint is intentionally fast and lightweight.
- Timestamp fields (`last_market_status_check`, `last_alert_evaluation`) may be `null` after a cold start before any background jobs have executed.
- For dependency-level detail use `GET /health/detailed`.

---

## GET /health/detailed

**Purpose**

Provide a comprehensive health report including dependency checks and response timing.

Used for:
- Diagnostics
- Incident investigation
- Internal monitoring dashboards

**Method & Path**

- `GET /health/detailed`

**Idempotency**

- Safe to refresh (read-only).

### Request

No parameters.

### Response (200)

```json
{
  "status": "healthy",
  "timestamp": "2026-02-17T10:30:00Z",
  "version": "1.5.0",
  "response_time_ms": 42.5,
  "checks": {
    "database": {
      "status": "healthy",
      "details": {
        "connected": true,
        "portfolio_exists": true
      }
    },
    "yahoo_finance": {
      "status": "healthy",
      "details": {
        "gbp_usd_rate": 1.3642,
        "accessible": true
      }
    },
    "services": {
      "status": "healthy",
      "details": {
        "position_service": "available",
        "portfolio_service": "available",
        "cash_service": "available"
      }
    },
    "config": {
      "status": "healthy",
      "details": {
        "settings_loaded": true
      }
    }
  }
}
```

#### Field notes

- `version` reflects the deployed backend version. See note under `GET /health`.
- `checks` key names and `details` structures are implementation-specific but stable within a version.
- Internal error details must not expose secrets or credentials.

### Notes

- Returns `"degraded"` overall status if any component is unhealthy.
- Use for post-deployment verification.

---

## GET /health/database

**Purpose**

Return current database size, percentage of the Render free tier limit used, and the configured alert threshold. Triggers a Telegram notification if usage is at or above the threshold.

Used for:
- Operational size monitoring
- FinOps visibility (Render free tier limit: 256 MB)
- Manual admin checks

**Method & Path**

- `GET /health/database`

**Idempotency**

- Safe to refresh (read-only with respect to data). May trigger a Telegram notification as a side effect if the threshold is exceeded and the alert cooldown (1 hour) has elapsed.

### Request

No parameters.

### Configuration

| Environment variable | Default | Description |
|---|---|---|
| `DB_SIZE_ALERT_THRESHOLD_PERCENT` | `80` | Percentage of the 256 MB limit at which a Telegram notification is sent |

### Response (200)

```json
{
  "size_bytes": 52428800,
  "size_mb": 50.0,
  "limit_bytes": 268435456,
  "limit_mb": 256.0,
  "used_percent": 19.53,
  "threshold_percent": 80.0,
  "status": "ok"
}
```

On query failure:

```json
{
  "size_bytes": null,
  "size_mb": null,
  "limit_bytes": 268435456,
  "limit_mb": 256.0,
  "used_percent": null,
  "threshold_percent": 80.0,
  "status": "error",
  "error": "<error message>"
}
```

#### Field notes

- `size_bytes`: raw database size in bytes as reported by `pg_database_size()`.
- `size_mb`: `size_bytes` converted to megabytes (2 d.p.).
- `limit_bytes`: Render free tier PostgreSQL limit — 268,435,456 bytes (256 MB). Fixed constant.
- `limit_mb`: `limit_bytes` in megabytes — always 256.0.
- `used_percent`: `size_bytes / limit_bytes × 100` (2 d.p.).
- `threshold_percent`: value of `DB_SIZE_ALERT_THRESHOLD_PERCENT` env var (default 80).
- `status`: `"ok"` when `used_percent < threshold_percent`; `"warning"` when at or above; `"error"` when the size query failed.

### Status values

- `"ok"`: usage below configured threshold — no action needed.
- `"warning"`: usage at or above threshold — Telegram notification sent (if credentials configured and cooldown elapsed). Notification-only; no automated cleanup.
- `"error"`: database size query failed — check database connectivity.

### Notes

- Alert delivery is **notification-only** — no automated data cleanup or deletion is triggered (§3 compliance).
- Alert cooldown prevents duplicate notifications within a 1-hour window (module-level state; resets on process restart).
- Requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` environment variables for Telegram delivery. If absent, the status is still returned but no notification is sent.

---

## POST /test/endpoints

**Purpose**

Execute a suite of automated endpoint tests and return a structured summary.

Used primarily for:
- Smoke testing
- CI/CD validation
- Manual diagnostics

**Method & Path**

- `POST /test/endpoints`

**Idempotency**

- Read-only with respect to business data, but triggers test execution.

### Request

No request body.

### Response (200)

```json
{
  "timestamp": "2026-02-17T10:30:00Z",
  "summary": {
    "total": 17,
    "passed": 17,
    "failed": 0,
    "errors": 0,
    "success_rate": 100.0
  },
  "results": [
    {
      "endpoint": "GET /portfolio",
      "critical": true,
      "status": "pass",
      "status_code": 200,
      "response_time_ms": 45.0
    },
    {
      "endpoint": "GET /analytics/metrics (all_time)",
      "critical": true,
      "status": "pass",
      "status_code": 200,
      "response_time_ms": 312.0
    },
    {
      "endpoint": "POST /validate/calculations",
      "critical": true,
      "status": "pass",
      "status_code": 200,
      "response_time_ms": 28.0
    }
  ]
}
```

#### Field notes

- `critical` indicates whether a failure on this endpoint is considered a system-level issue.
- `total` reflects all endpoints under test, including analytics and validation endpoints added in v1.5.0.

### Notes

- Failures indicate contract or environment issues.
- This endpoint must never mutate production data.
- Can take 10–30 seconds to complete (live price fetches for position/portfolio endpoints).

---

## GET /test/quick-health

**Purpose**

Quick health check that tests only critical endpoints (`GET /health`, `GET /settings`, `GET /portfolio`). Faster than `POST /test/endpoints`, intended for lightweight liveness checks.

**Method & Path**

- `GET /test/quick-health`

**Idempotency**

- Read-only.

### Request

No request body.

### Response (200)

```json
{
  "status": "healthy",
  "checks": [
    { "name": "Health", "healthy": true, "response_time_ms": 12.4, "status_code": 200 },
    { "name": "Settings", "healthy": true, "response_time_ms": 8.1, "status_code": 200 },
    { "name": "Portfolio", "healthy": true, "response_time_ms": 45.0, "status_code": 200 }
  ]
}
```

#### Field notes

- `status` is `"healthy"` only if every check in `checks` is healthy, else `"degraded"`.
- A check that raises an exception (timeout, connection error) is recorded with `healthy: false` and an `error` field instead of `response_time_ms`/`status_code`.

### Notes

- Base URL is auto-detected from the incoming request unless `API_BASE_URL` is explicitly set.
- Read-only with respect to business data.

---

## POST /test/rate-limit-scenarios

**Purpose**

Verifies rate-limiting logic for `POST /ai/daily-briefing` (limit=10) and `POST /ai/chat` (limit=30) using isolated test keys (`daily-briefing:__test__`, `chat:__test__`), so live traffic and real users are unaffected.

**Method & Path**

- `POST /test/rate-limit-scenarios`

**Idempotency**

- Read-only with respect to business data; resets its own isolated test keys before and after running.

### Request

No request body.

### Response (200)

```json
{
  "results": [
    { "endpoint": "POST /ai/daily-briefing", "status": "pass" },
    { "endpoint": "POST /ai/chat", "status": "pass" }
  ]
}
```

#### Field notes

- `status` is `"pass"` if the limiter correctly allows exactly `limit` requests then rejects the next one, else `"fail"` with an `error` field.

### Notes

- Uses `services.rate_limiter._ai_limiter` directly — does not consume real user rate-limit budget.
- Originating AC: AC-05 for ST-03 (BLG-OPS-81, EPIC-01, v6.3).

---

## Error handling

- Health endpoints do not use the standard error envelope.
- Failures are communicated via:
  - HTTP status codes
  - `status` fields in the response body

---

## Security considerations

- Health endpoints may be restricted or protected in production environments.
- Detailed diagnostics should not be exposed publicly without access controls.

---

## GET /health/scheduler

**Method:** GET  
**Path:** `/health/scheduler`  
**Auth:** API key required  
**Story:** ST-13 (BLG-OPS-79, EPIC-03, v6.3)

Returns last-run status, timestamps, and any error details for each nightly computation job.

**Architecture note:** The scheduler is GitHub Actions (external cron) calling HTTP endpoints — not an in-process background scheduler. The six tracked jobs are triggered by:
- `trailing_stop` — `POST /positions/nightly-stop-update`
- `rebalance_exit` — `POST /signals/rebalance-exit`
- `inv_vol_sizing` — co-invoked by `POST /signals/rebalance-exit`
- `custom_price_alerts` — co-invoked by `POST /alerts/evaluate` (ST-02/BLG-FE-116)
- `screener_refresh` — `POST /screener/run` (ST-01/BLG-OPS-144, EPIC-01, v8.8)
- `risk_off_alerts` — `POST /positions/risk-off-alerts` (ST-02/BLG-OPS-145, EPIC-01, v8.8)

### Request

No request body.

### Response (200)

```json
{
  "scheduler_type": "github_actions_external_cron",
  "trigger_endpoints": {
    "trailing_stop": "POST /positions/nightly-stop-update",
    "rebalance_exit": "POST /signals/rebalance-exit",
    "inv_vol_sizing": "co-invoked by rebalance-exit",
    "custom_price_alerts": "co-invoked by POST /alerts/evaluate",
    "screener_refresh": "POST /screener/run",
    "risk_off_alerts": "POST /positions/risk-off-alerts"
  },
  "overall_status": "ok",
  "jobs": {
    "trailing_stop": {
      "last_run_utc": "2026-06-29T16:00:00+00:00",
      "last_status": "ok",
      "last_error": null,
      "detail": { "positions_updated": 3 }
    },
    "rebalance_exit": {
      "last_run_utc": "2026-06-29T16:00:00+00:00",
      "last_status": "ok",
      "last_error": null,
      "detail": { "is_last_trading_day": false, "signals_created": 0 }
    },
    "inv_vol_sizing": {
      "last_run_utc": "2026-06-29T16:00:00+00:00",
      "last_status": "ok",
      "last_error": null,
      "detail": { "note": "co-invoked by rebalance-exit" }
    },
    "custom_price_alerts": {
      "last_run_utc": "2026-08-18T07:00:00+00:00",
      "last_status": "ok",
      "last_error": null,
      "detail": { "alerts_evaluated": 12, "triggered": 1 }
    },
    "screener_refresh": {
      "last_run_utc": "2026-08-18T07:05:00+00:00",
      "last_status": "ok",
      "last_error": null,
      "detail": { "run_id": "a1b2c3d4-...", "result": { "tickers_scanned": 20 } }
    },
    "risk_off_alerts": {
      "last_run_utc": "2026-08-18T07:10:00+00:00",
      "last_status": "ok",
      "last_error": null,
      "detail": { "flagged": 0 }
    }
  },
  "note": "Status resets on process restart. A never_run status after a recent deploy is normal."
}
```

#### Field notes

| Field | Type | Values |
|-------|------|--------|
| `scheduler_type` | string | Always `"github_actions_external_cron"` |
| `overall_status` | string | `"ok"` — all jobs ok or never_run; `"degraded"` — at least one job errored |
| `jobs[*].last_run_utc` | ISO 8601 timestamp or null | null if job has never run since last deploy |
| `jobs[*].last_status` | string | `"ok"`, `"error"`, `"never_run"` |
| `jobs[*].last_error` | string or null | Error message if `last_status == "error"` |
| `jobs[*].detail` | object or null | Job-specific result summary |

### Notes

- Status is in-memory; a `"never_run"` status after a recent Render deploy is expected and normal.
- `"degraded"` overall_status indicates at least one job's most recent invocation returned an error. Check `last_error` for the specific failure.

---

## Known Deviations

None — all known deviations resolved as of v1.1 (BLG-SPEC-D14, 2026-03-25).

> **Note:** DEV-HEALTH-001 was filed during v2.2 delivery verification. It documented that the `GET /health` implementation in v2.2 diverged from the v1.0 spec schema. This spec was updated to v1.1 in the v2.3 sprint (ST-07, EPIC-03) to document the correct v2.2+ schema. DEV-HEALTH-001 is now closed.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.6 | 2026-08-18 | ST-18 (BLG-SPEC-130, EPIC-05, v8.9): `GET /health/scheduler`'s architecture note and response example only documented 3 of the 6 live jobs `_NIGHTLY_JOB_NAMES`/`get_scheduler_health()` actually track — added `custom_price_alerts`, `screener_refresh`, and `risk_off_alerts` to both, matching `backend/services/health_service.py` exactly. Authority: API Contracts & Documentation Owner. |
| 1.5 | 2026-08-07 | ST-05 (BLG-SPEC-114, EPIC-02, v8.4): `GET /health` example was missing the `external_apis` and `ai_journal` nested objects that `health_service.get_operational_health()` has returned since ST-08/ST-09. Added both to the example and field notes. Authority: API Contracts & Documentation Owner. |
| 1.4 | 2026-08-07 | ST-02 (BLG-SPEC-116, EPIC-02, v8.4): Added `GET /test/quick-health` and `POST /test/rate-limit-scenarios` — both routes existed in `backend/routers/test.py` but were undocumented, causing OpenAPI Drift Detection CI gate failures once `openapi.yaml`'s structural defect was fixed. Also added `GET /health/scheduler` to the Endpoints TOC (pre-existing section, TOC omission only). Authority: API Contracts & Documentation Owner. |
| 1.3 | 2026-06-29 | ST-13 (BLG-OPS-79): Added `GET /health/scheduler` — nightly computation job health monitoring endpoint. Returns last-run status for trailing_stop, rebalance_exit, inv_vol_sizing jobs. Authority: Infrastructure & Operations Owner. |
| 1.2 | 2026-03-25 | ST-08 (BLG-OPS-09): Added `GET /health/database` — database size monitoring endpoint with configurable alert threshold and Telegram notification. Authority: Head of Engineering + FinOps & Resource Architect. |
| 1.1 | 2026-03-25 | ST-07 (BLG-SPEC-D14): `GET /health` section updated to document actual v2.2 schema — `status: ok\|error`, `db: connected\|error`, `last_market_status_check`, `last_alert_evaluation`. DEV-HEALTH-001 closed. Authority: API Contracts & Documentation Owner. |
| 1.0 | 2026-03-18 | Initial spec. |
