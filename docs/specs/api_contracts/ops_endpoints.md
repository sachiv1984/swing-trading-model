**Owner:** Infrastructure & Operations Owner; API Contracts & Documentation Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-09-10 (ST-13, BLG-OPS-94 — added POST /ops/purge-audit-logs)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Ops / Cost Monitoring Endpoints — API Contract

This document specifies operations and cost-monitoring endpoints for the Momentum Trading Assistant — external API call-count instrumentation and reporting, distinct from `ai_endpoints.md`'s Claude spend-tracking endpoints (which track per-call cost/tokens, not call volume).

All endpoints in this document are read-only aggregates over `api_call_log` (`backend/database.py`) — no side effects, no writes triggered by a GET request.

---

## Table of Contents

- [GET /ops/alpaca-call-report](#get-opsalpaca-call-report)
- [GET /ops/research-session-report](#get-opsresearch-session-report)
- [POST /ops/purge-audit-logs](#post-opspurge-audit-logs)

---

## GET /ops/alpaca-call-report

Returns Alpaca Data API call counts for the requested window (today, or the last 7 days), aggregated from `api_call_log`.

Added for ST-11 (BLG-OPS-17, EPIC-03, v9.3) — the reference instrumentation pattern for external-API call-count tracking, reused by `GET /ops/research-session-report` below (RISK-03). Every call to `backend/services/alpaca_service.py::get_ohlcv_bars()` — the sole Alpaca Data API call site in this codebase — logs one `api_call_log` row per invocation (not per internal retry attempt), tagged `service="alpaca"`.

**§13 Status:** N/A — no AI output; a call-count aggregate.

### Request

```
GET /ops/alpaca-call-report?window=daily
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `window` | string | No | `daily` (default, today UTC) or `weekly` (last 7 days). Any other value returns 422 (FastAPI `pattern` validation). |

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "service": "alpaca",
    "window": "daily",
    "total_calls": 42,
    "success_count": 40,
    "failure_count": 2
  }
}
```

| Field | Type | Description |
|-------|------|--------------|
| `service` | string | Always `"alpaca"` for this endpoint. |
| `window` | string | Echoes the requested window. |
| `total_calls` | integer | Total `get_ohlcv_bars()` invocations logged in the window. |
| `success_count` | integer | Invocations that returned bar data (HTTP 200 with a non-error response). |
| `failure_count` | integer | Invocations that failed (rate limit exhausted, 403, 5xx exhausted, request exception, or unexpected status). |

### Error responses

| Status | Condition |
|--------|-----------|
| 422 | `window` is not `daily` or `weekly`. |
| 500 | Internal failure — returns zeroed counts rather than propagating the error (matches `get_monthly_claude_cost`'s existing fail-safe convention in `ai_endpoints.md`), so this endpoint does not return a 500 body under normal operation. |

---

## GET /ops/research-session-report

Returns per-session external-call counts for `GET /research/{ticker}` over the last 7 days, with a computed baseline (mean calls/session) and sessions flagged as anomalous when their call count exceeds a configurable multiplier (default 2×) of that baseline.

Added for ST-12 (BLG-OPS-20, EPIC-03, v9.3). Reuses ST-11's `api_call_log` instrumentation (RISK-03) rather than a separate logging mechanism — one `session_id` (a UUID) is generated per cache-miss `GET /research/{ticker}` request, and each of that request's 4 external-source calls (`_get_price_data`, `_get_market_cap`, `_get_news`, `_get_earnings` — the endpoint's genuinely external calls; `_get_regime`, `_get_signal`, `_get_sector`, `_get_screener` are internal/DB-backed and not logged here) is tagged with that session_id. A cache-hit request makes no external calls and is not logged.

**§13 Status:** N/A — no AI output; a call-count/anomaly-detection aggregate.

### Request

```
GET /ops/research-session-report
```

No parameters.

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "service": "research",
    "period_days": 7,
    "session_count": 12,
    "baseline_calls_per_session": 3.8,
    "anomaly_multiplier": 2.0,
    "sessions": [
      {"session_id": "a1b2c3d4-...", "call_count": 4, "anomalous": false},
      {"session_id": "e5f6a7b8-...", "call_count": 9, "anomalous": true}
    ]
  }
}
```

| Field | Type | Description |
|-------|------|--------------|
| `service` | string | Always `"research"` for this endpoint. |
| `period_days` | integer | Always `7` — the fixed lookback window. |
| `session_count` | integer | Number of distinct research request sessions in the window. |
| `baseline_calls_per_session` | float | Mean `call_count` across all sessions in the window. `0.0` if no sessions. |
| `anomaly_multiplier` | float | The threshold multiplier applied (`ANOMALY_MULTIPLIER` in `backend/routers/cost_monitoring.py`, default `2.0`, matching this story's ">2x baseline" acceptance criterion). |
| `sessions` | array | One entry per session, ordered by `call_count` descending. |
| `sessions[].session_id` | string | The UUID generated for that research request. |
| `sessions[].call_count` | integer | External calls logged for that session (max 4, per the 4 external-source helpers). |
| `sessions[].anomalous` | boolean | `true` when `call_count > baseline_calls_per_session × anomaly_multiplier` (always `false` when the baseline is `0`). |

### Error responses

| Status | Condition |
|--------|-----------|
| 500 | Internal failure — returns an empty `sessions` array and zeroed baseline rather than propagating the error, so this endpoint does not return a 500 body under normal operation. |

### Implementation constraints

- Read-only endpoint: no writes to any table.
- 7-day fixed lookback (not currently configurable via query parameter).
- A session with 0 external calls (all 4 helpers unexpectedly skipped) never appears — only sessions with at least 1 logged call are counted, since `session_id IS NOT NULL` is required by the underlying query and a session_id is only ever logged alongside a call.

---

## POST /ops/purge-audit-logs

Deletes `gemini_audit_log` rows older than 90 days and `claude_audit_log` rows older than 730 days (24 months) — enforcing the retention windows documented in `docs/ops/ai_audit_log_retention_policy.md`.

Added for ST-13 (BLG-OPS-94, EPIC-03, v9.3). Idempotent — safe to call repeatedly (e.g. from a daily scheduled workflow, matching this codebase's other maintenance endpoints like `POST /portfolio/snapshot`); deletes nothing when no rows qualify. Protected by the app-wide `X-API-Key` middleware (`backend/main.py::api_key_middleware`), same as every other non-GET endpoint when `API_KEY` is configured — no route-local auth dependency.

**§13 Status:** N/A — no AI output; a maintenance/deletion operation on audit metadata only (no AI-generated content is itself stored in either table — see each table's schema in `docs/ops/gemini_cost_tracking.md` / `render_log_retention_policy.md` §3.1).

### Request

```
POST /ops/purge-audit-logs
```

No parameters, no request body.

### Response — 200 OK

```json
{
  "status": "ok",
  "data": {
    "gemini_audit_log_rows_deleted": 0,
    "claude_audit_log_rows_deleted": 0
  }
}
```

| Field | Type | Description |
|-------|------|--------------|
| `gemini_audit_log_rows_deleted` | integer | Rows deleted from `gemini_audit_log` (older than 90 days). `0` if none qualified, or on internal failure (fail-safe — see below). |
| `claude_audit_log_rows_deleted` | integer | Rows deleted from `claude_audit_log` (older than 730 days). `0` if none qualified, or on internal failure. |

### Error responses

| Status | Condition |
|--------|-----------|
| 401 | Missing or invalid `X-API-Key` header (when `API_KEY` is configured in the deployment environment). |
| 500 | Not expected under normal operation — each underlying purge function (`purge_gemini_audit_log_older_than_90_days`, `purge_claude_audit_log_older_than_730_days`) fails safe internally (returns `0` rather than propagating an exception), matching this table's sibling functions' existing convention. |

### Implementation constraints

- Hard `DELETE`, not a soft-delete/archive flag — per `docs/ops/ai_audit_log_retention_policy.md`'s "delete" procedure choice (no archival store configured for this codebase; see that document's rationale).
- Each table's purge runs independently — a failure purging one table does not prevent the other from being attempted (both purge functions are always called; each fails safe on its own).
- No response field distinguishes "0 rows deleted because none qualified" from "0 rows deleted because of an internal failure" — both currently produce the same `0` value, matching the pre-existing `purge_gemini_audit_log_older_than_90_days()` fail-safe convention this endpoint extends to `claude_audit_log`. A future story could add an explicit `error` field per table if this ambiguity becomes operationally significant.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-09-10 | ST-13 (EPIC-03, v9.3, BLG-OPS-94): Added `POST /ops/purge-audit-logs` — deletes gemini_audit_log (>90 days) and claude_audit_log (>730 days) rows per the new retention policy (`docs/ops/ai_audit_log_retention_policy.md`). `openapi.yaml` updated in the same commit. Infrastructure & Operations Owner sign-off. |
| 1.0 | 2026-09-10 | ST-11/ST-12 (EPIC-03, v9.3, BLG-OPS-17/BLG-OPS-20): Initial specification. Added `GET /ops/alpaca-call-report` and `GET /ops/research-session-report`. `openapi.yaml` updated in the same commit. Infrastructure & Operations Owner sign-off (per sprint_backlog.md AC). |
