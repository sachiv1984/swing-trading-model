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
  "timestamp": "2026-02-17T10:30:00Z",
  "version": "1.5.0"
}
```

#### Field notes

- `version` reflects the deployed backend version and advances with each release. Treat as informational; do not use for contract compatibility checks.

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

## Error handling

- Health endpoints do not use the standard error envelope.
- Failures are communicated via:
  - HTTP status codes
  - `status` fields in the response body

---

## Security considerations

- Health endpoints may be restricted or protected in production environments.
- Detailed diagnostics should not be exposed publicly without access controls.
