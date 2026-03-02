**Owner:** Head of Engineering
**Status:** Draft — Pending Head of Specs Team class assignment (TASK-16)
**Version:** 0.1.0
**Last Updated:** 2026-03-02
**Cycle:** 2026-03-02__release-v1.7
**Maps to:** S2-04 (EPIC-04)

> **Note:** Document class has not yet been assigned by the Head of Specs Team (TASK-16 open). This document is not authoritative until TASK-16 is complete and the header is updated with an approved class, owner confirmation, and lifecycle status.

---

# Structured Logging Standards

## Purpose

This document defines the structured logging standards for the swing trading model backend. These standards ensure that:

1. Logs are machine-parseable and queryable.
2. Async failures in v2.0 Alerts are observable and debuggable via correlation IDs.
3. Sensitive data is never logged.
4. Log volume is proportionate to operational value.

All backend services **MUST** conform to this standard from v1.7 onwards.

---

## TASK-11 — Log Levels and Usage Policy

Four log levels are defined. Every log statement must use exactly one of these levels. Usage outside the defined policy is a code review blocker.

### Level Definitions

| Level | Value | When to use |
|-------|-------|-------------|
| `ERROR` | 40 | An operation failed and could not recover. Action required. Examples: database write failed, external API returned 5xx, unhandled exception in a route handler. |
| `WARNING` | 30 | An unexpected condition was handled gracefully, but the system may degrade if it recurs. Examples: FX rate fetch fell back to default, validation score exceeded tolerance, retry succeeded after first failure. |
| `INFO` | 20 | Normal operational events worth recording for audit or diagnostics. Examples: service started, portfolio snapshot created, signal generation completed. |
| `DEBUG` | 10 | Detailed execution trace for development and debugging only. **Must not appear in production logs.** Examples: intermediate calculation values, individual row fetched, branching decision taken. |

### Level Policy Rules

1. **`ERROR` implies action required.** An ERROR log must be paired with an alert or a monitoring threshold in v2.0. Do not ERROR on conditions that are expected or recoverable without intervention.
2. **`WARNING` does not halt execution.** If execution halts, use `ERROR` instead.
3. **`INFO` must be sparse.** No more than 3–5 INFO events per API request in steady state. Verbose INFO is treated as DEBUG.
4. **`DEBUG` is stripped in production.** The production log level is `INFO`. DEBUG statements are acceptable in code but must be filtered at the logger configuration level.

---

## TASK-12 — Structured Log Format

All log output **MUST** be valid JSON, one object per line (JSON Lines / NDJSON format).

### Required Fields

Every log record **MUST** include all of the following fields:

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `timestamp` | string | ISO-8601 UTC (`YYYY-MM-DDTHH:MM:SS.ffffffZ`) | Time the event occurred. Always UTC. Never local time. |
| `level` | string | `"ERROR"`, `"WARNING"`, `"INFO"`, `"DEBUG"` | Log level. Always uppercase. |
| `correlation_id` | string | UUID v4 or `"none"` | Request or job correlation ID. `"none"` only for startup events with no request context. |
| `service` | string | `"api"`, `"validation"`, `"analytics"`, `"signals"`, `"scheduler"` | Originating service component. |
| `message` | string | Free text (max 500 chars) | Human-readable description of the event. Must not contain PII or secrets. |

### Optional Domain Fields

These fields may be added when relevant. All are optional.

| Field | Type | Description |
|-------|------|-------------|
| `endpoint` | string | HTTP method and path, e.g. `"POST /validate/calculations"` |
| `status_code` | integer | HTTP response status code |
| `duration_ms` | integer | Request or operation duration in milliseconds |
| `ticker` | string | Ticker symbol if the event is position-scoped |
| `position_id` | string | UUID of the affected position |
| `error_type` | string | Exception class name, e.g. `"KeyError"`, `"psycopg2.OperationalError"` |
| `error_detail` | string | Exception message — sanitised; must not contain raw SQL, credentials, or user data |
| `job_id` | string | UUID for async/scheduled jobs (v2.0 Alerts) |
| `retry_count` | integer | Number of retries attempted before this log event |

### Canonical Example

```json
{
  "timestamp": "2026-03-02T10:15:30.123456Z",
  "level": "ERROR",
  "correlation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "service": "api",
  "message": "Database write failed for portfolio snapshot",
  "endpoint": "POST /portfolio/snapshot",
  "status_code": 500,
  "duration_ms": 142,
  "error_type": "psycopg2.OperationalError",
  "error_detail": "connection to server lost"
}
```

### Format Rules

1. Output must be valid JSON. Multiline values must be escaped — no literal newlines inside a log record.
2. Do not nest required fields. All required fields are top-level keys.
3. Timestamps must be UTC and include microseconds where possible.
4. Field names use `snake_case`.
5. Unknown fields must not be omitted silently — if a required field cannot be populated, use `"none"` for string fields and `0` for numeric fields.

---

## TASK-13 — Correlation ID Scheme

Correlation IDs enable request tracing across logs, API responses, and (in v2.0) async job chains.

### Generation

- **Per-request correlation IDs:** Generated at the API gateway layer (FastAPI middleware) as a UUID v4 at the start of each incoming HTTP request.
- **Per-job correlation IDs:** Generated by the scheduler at job creation time (v2.0 Alerts). A single job retains the same correlation ID across all retry attempts.

### Implementation (FastAPI Middleware)

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response
```

### Propagation Rules

1. **Inbound:** If the incoming request includes an `X-Correlation-ID` header, reuse it. This allows client-initiated tracing.
2. **Outbound:** All log records within a request **MUST** include the same `correlation_id`.
3. **Response header:** The `X-Correlation-ID` header **MUST** be echoed in every API response so clients can reference it when reporting issues.
4. **Async jobs (v2.0):** The job correlation ID must be included in all log records produced by that job, including retries. The scheduler must persist `job_id` alongside `correlation_id` to support job-level grouping.

### Surfacing in API Responses

For error responses, the correlation ID must be included in the response body to assist support:

```json
{
  "status": "error",
  "message": "Validation failed: calculation error",
  "correlation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

This is mandatory for 500-level responses and recommended for 400-level responses.

---

## TASK-14 — Async Failure Observability (v2.0 Alerts)

v2.0 Alerts will introduce background/scheduled jobs (e.g. alert evaluation, notification dispatch). These jobs run outside the HTTP request cycle and cannot surface errors via HTTP status codes. Structured logging is the primary observability mechanism.

### Requirements for Async Jobs

1. **Job lifecycle events must be logged at INFO:**
   - Job started: `{ "message": "Alert job started", "job_id": "...", "alert_id": "..." }`
   - Job completed: `{ "message": "Alert job completed", "job_id": "...", "duration_ms": 120 }`
   - Job failed: `{ "message": "Alert job failed", "job_id": "...", "error_type": "...", "retry_count": 2 }` at `ERROR`

2. **All retries must be logged at WARNING** with `retry_count` incremented.

3. **Final failure (exhausted retries) must be logged at ERROR** and must trigger a monitoring alert (v2.0 alerting infrastructure).

4. **Correlation ID continuity:** A job that spawns sub-tasks must propagate its `correlation_id` to all sub-tasks. Sub-tasks may append a suffix (e.g. `f47ac10b-...-subtask-1`) but must not replace the root correlation ID.

5. **No silent failures.** A job that exits without logging a completion or failure event is a bug.

### Log Query Patterns (for v2.0 operators)

| Goal | Query |
|------|-------|
| All events for a request | `correlation_id = "f47ac10b-..."` |
| All failures in a time window | `level = "ERROR" AND timestamp >= "..."` |
| All events for an async job | `job_id = "..."` |
| Retry storms | `level = "WARNING" AND retry_count > 2` |

---

## TASK-15 — What NOT to Log

The following must **never** appear in any log record, regardless of level:

| Category | Examples |
|----------|---------|
| Credentials and secrets | Database passwords, API keys, `DATABASE_URL`, `GITHUB_TOKEN` |
| Full request/response bodies | POST body JSON, full API responses from Yahoo Finance |
| Personally Identifiable Information | Not applicable (no user accounts in current system) |
| Raw SQL queries with parameters | `SELECT * FROM portfolio WHERE id = '...'` with user-supplied values |
| Internal stack traces in `message` | Stack traces go to `error_detail` (sanitised), not `message` |
| Financial account numbers | Not applicable (no brokerage integration in current system) |

**Rule:** If in doubt, do not log it. Redact or omit. Logging too little is recoverable; logging sensitive data is not.

---

## Changelog

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 0.1.0 | 2026-03-02 | Initial draft — TASK-11/12/13/14/15 complete. Pending TASK-16 Head of Specs Team class assignment and sign-off. | Head of Engineering |
