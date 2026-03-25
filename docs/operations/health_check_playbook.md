**Owner:** Infrastructure & Operations Owner
**Class:** Operational Runbook (Class 5)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-25
**Cycle:** 2026-03-24__release-v2.3 (ST-09, BLG-OPS-07, EPIC-03)

---

# System Health Check Playbook

This playbook documents how to interpret and respond to each health signal returned by `GET /health`.

**Schema reference:** `docs/specs/api_contracts/health_endpoints.md` v1.1

**Related:** `GET /health/detailed` for full dependency diagnostics.

---

## Health Check Endpoint

```
GET /health
```

**Expected healthy response:**

```json
{
  "status": "ok",
  "db": "connected",
  "last_market_status_check": "<ISO-8601 timestamp>",
  "last_alert_evaluation": "<ISO-8601 timestamp>"
}
```

---

## Field Interpretations

### `status`

| Value | Meaning |
|-------|---------|
| `"ok"` | All subsystems nominal |
| `"error"` | One or more subsystems failing — check `db` and timestamps |

### `db`

| Value | Meaning |
|-------|---------|
| `"connected"` | Database is reachable and queries are succeeding |
| `"error"` | Database connection failed or query returned an error |

### `last_market_status_check`

The ISO-8601 timestamp of the most recent market status check job execution. `null` indicates no check has run since the last restart.

**Staleness threshold:** If older than 30 minutes during market hours, investigate.

### `last_alert_evaluation`

The ISO-8601 timestamp of the most recent alert evaluation run. `null` indicates no evaluation has run since the last restart.

**Staleness threshold:** If older than 15 minutes during active trading hours, investigate.

---

## Failure Mode Diagnosis & Recovery

### Failure Mode 1 — Database Error (`"db": "error"`)

**Symptom:** `GET /health` returns `"db": "error"` with `"status": "error"`.

**Diagnosis steps:**

1. Check `GET /health/detailed` for the `checks.database` section — it includes `connected` (bool) and `portfolio_exists` (bool).
2. Check Render dashboard for the PostgreSQL service status.
3. Check backend logs for database connection errors.

**Common causes:**

| Cause | Indicator | Fix |
|-------|-----------|-----|
| Render PostgreSQL service restart | Short outage in logs | Wait for restart to complete (typically < 2 min); verify `db: connected` returns |
| Database credentials rotated | `authentication failed` in logs | Update `DATABASE_URL` environment variable in Render; redeploy |
| Database at capacity | `no space left on device` or slow queries | Check DB size via the database monitoring alert (BLG-OPS-09); prune old data per governance §3 policy |
| Migration not applied | `relation does not exist` errors | Run pending migrations: `alembic upgrade head` in the backend service |

**Recovery verification:** `GET /health` returns `"db": "connected"`.

---

### Failure Mode 2 — Market Status Check Stalled

**Symptom:** `last_market_status_check` is `null` or older than 30 minutes during market hours.

**Diagnosis steps:**

1. Check backend logs for errors in the market status background job.
2. Verify the external market data source (Yahoo Finance) is reachable.
3. Check if the backend service has restarted recently (a restart resets the timestamp to `null` until the first job completes).

**Common causes:**

| Cause | Indicator | Fix |
|-------|-----------|-----|
| Fresh deployment / cold start | `null` value; recent deploy in Render | Wait 5 minutes for background job to run; timestamp will populate |
| External market data source unreachable | Network errors in logs | Check Yahoo Finance availability; no action required — job retries automatically |
| Background job exception | Exception stack trace in logs | Investigate root cause; if a code bug, file a backlog item |

**Recovery verification:** `last_market_status_check` updates to a recent timestamp within 15 minutes.

---

### Failure Mode 3 — Alert Evaluation Stalled

**Symptom:** `last_alert_evaluation` is `null` or older than 15 minutes during active trading hours.

**Diagnosis steps:**

1. Check backend logs for errors in the alert evaluation background job.
2. Verify the database connection is healthy (`"db": "connected"`).
3. Check if the backend service restarted recently.

**Common causes:**

| Cause | Indicator | Fix |
|-------|-----------|-----|
| Fresh deployment / cold start | `null` value; recent deploy in Render | Wait for first evaluation cycle (typically < 5 minutes); timestamp will populate |
| Database query error during evaluation | DB-related errors in logs | Resolve database issue first (see Failure Mode 1) |
| Alert evaluation job exception | Exception stack trace in logs | Investigate root cause; if a code bug, file a backlog item |
| No alert rules configured | `last_alert_evaluation` stays `null` after startup | Expected if no alert rules exist — not a failure |

**Recovery verification:** `last_alert_evaluation` updates to a recent timestamp within 10 minutes of the job resuming.

---

## Routine Health Check Procedure

Perform this check after every deployment and during any incident investigation:

1. Call `GET /health` and record the response.
2. Confirm `"status": "ok"` and `"db": "connected"`.
3. Confirm `last_market_status_check` is non-null and recent (within 30 min during market hours).
4. Confirm `last_alert_evaluation` is non-null and recent (within 15 min during active trading).
5. If any field indicates a problem, follow the relevant failure mode diagnosis above.
6. For deeper diagnostics, call `GET /health/detailed` to inspect all subsystem check results.

---

## Related Documentation

- `docs/specs/api_contracts/health_endpoints.md` — API contract for `GET /health` and `GET /health/detailed`
- `docs/operations/production_deployment_runbook.md` — Full deployment procedure
- `docs/operations/unavailability_policy.md` — Service unavailability SLA and communication policy
