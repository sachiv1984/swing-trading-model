# health_endpoints.md

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
- [POST /test/endpoints](#post-testendpoints)

---

## GET /health

**Purpose**

Provide a lightweight health check indicating overall service status and version.

Typically used by:
- Load balancers
- Uptime monitors
- Deployment verification

**Method & Path**

- `GET /health`

**Idempotency**

- Safe to refresh (read-only).

### Request

No parameters.

### Response (200)

```json
{
  "status": "healthy",
  "timestamp": "2026-02-15T10:30:00Z",
  "version": "1.4.1"
}
```

### Status values

- `healthy`: all systems operational
- `degraded`: partial issues, service still functional
- `unhealthy`: critical failure

### Notes

- This endpoint is intentionally fast and lightweight.
- No dependency-level detail is included.

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
  "timestamp": "2026-02-15T10:30:00Z",
  "version": "1.4.1",
  "response_time_ms": 42.5,
  "checks": {
    "database": {
      "status": "healthy",
      "details": {
        "connection": "ok",
        "response_time_ms": 5.2
      }
    },
    "yahoo_finance": {
      "status": "healthy",
      "details": {
        "last_fetch": "2026-02-15T10:29:00Z",
        "response_time_ms": 150.0
      }
    },
    "services": {
      "status": "healthy"
    },
    "config": {
      "status": "healthy"
    }
  }
}
```

### Notes

- Dependency names and structure are implementation-specific but stable within a version.
- Internal error details must still not expose secrets or credentials.

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
  "timestamp": "2026-02-15T10:30:00Z",
  "summary": {
    "total": 12,
    "passed": 11,
    "failed": 1,
    "errors": 0,
    "success_rate": 91.7
  },
  "results": [
    {
      "endpoint": "GET /portfolio",
      "status": "pass",
      "status_code": 200,
      "expected_status": 200,
      "response_time_ms": 45.0
    },
    {
      "endpoint": "POST /positions/{id}/exit",
      "status": "fail",
      "status_code": 404,
      "expected_status": 200,
      "response_time_ms": 12.0,
      "error": "Position not found"
    }
  ]
}
```

### Notes

- Failures indicate contract or environment issues.
- This endpoint must never mutate production data.

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
