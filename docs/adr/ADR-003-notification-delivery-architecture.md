**Owner:** Head of Engineering
**Class:** Canonical Specification (Class 1)
**Status:** Accepted
**Version:** 1.0
**Last Updated:** 2026-03-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Signed off by:** Head of Engineering
**Sign-off date:** 2026-03-18
**ADR ID:** ADR-003
**Resolves:** BLG-TECH-08 (Async notification delivery architecture decision record)

---

# ADR-003: Notification Delivery Architecture

---

## Status

**Accepted** — 2026-03-18

---

## Context

The 3.5 Alerts & Notifications feature (EPIC-02, v2.1) requires the backend to deliver email notifications when specific alert conditions are met:

- Stop loss approach (current stop within threshold of current price)
- Grace period warning (days 8–9 of grace period)
- Market regime change to risk-off
- Daily portfolio summary

Before this EPIC could be specced or implemented, an architectural decision was required on **how notifications are delivered**: synchronously on the API response path, or asynchronously via a background worker infrastructure.

**Current system state:**

- FastAPI (Python) backend running on Render (PaaS)
- Supabase (managed Postgres) for persistence
- Single user, self-hosted deployment
- No existing Redis, Celery, or message queue infrastructure
- No background worker processes running
- No SLA requirements; no concurrent users

---

## Options Considered

### Option A — Synchronous inline delivery (email sent on API response path)

Email is sent as part of the API request that triggers an alert evaluation. The response is held until the email client call returns.

**Pros:**
- Simplest implementation — no infrastructure change
- Easy to test (email result visible in the response cycle)
- No new dependencies

**Cons:**
- API response latency increases by email RTT (typically 200ms–2s for SMTP/API calls)
- If email service is down, the API call fails — poor separation of concerns
- Ties user-facing latency to third-party service reliability

**Verdict:** Rejected. Coupling API response latency to email delivery is a poor trade-off even at single-user scale. Alert evaluation results and delivery are logically separate concerns.

---

### Option B — Asynchronous delivery via Celery + Redis

A Redis task queue and Celery worker process are added to the deployment. Alert evaluation enqueues a delivery task; Celery worker processes the queue independently.

**Pros:**
- True decoupled delivery — API response is immediate regardless of email outcome
- Retry logic built into Celery
- Clean separation of concerns; natural scale path

**Cons:**
- Requires Redis server (persistent process, memory overhead, operational monitoring)
- Requires Celery worker (persistent process, crash recovery, Render worker dyno)
- Adds Flower or equivalent for worker monitoring
- Significant operational overhead for a system with one user and no SLA
- Render deployment complexity increases: web dyno + worker dyno + Redis add-on
- Monthly infrastructure cost increase (~£10–25/month for Redis + worker dyno on Render)

**Verdict:** Rejected. For a single-user, self-hosted system, Celery + Redis is infrastructure overkill. The operational cost and complexity are disproportionate to the delivery requirement.

---

### Option C — FastAPI BackgroundTasks (selected)

FastAPI's built-in `BackgroundTasks` feature allows functions to be scheduled to run after a response is returned to the client. Email delivery is enqueued as a background task when an alert evaluation triggers a delivery.

**How it works:**

```python
from fastapi import BackgroundTasks

@router.post("/alerts/evaluate")
async def evaluate_alerts(background_tasks: BackgroundTasks, ...):
    triggered_alerts = evaluate_alert_rules(portfolio_state)
    for alert in triggered_alerts:
        background_tasks.add_task(deliver_notification, alert)
    return {"status": "ok", "data": {"alerts_triggered": len(triggered_alerts)}}
```

Email delivery (`deliver_notification`) runs after the response is sent. From the user's perspective, the API call is fast. Email errors do not affect the API response.

**Pros:**
- No new infrastructure — BackgroundTasks is built into FastAPI, zero deployment change
- Response is non-blocking — email delivery does not add latency to API calls
- Failure isolation — background task exceptions are caught and logged without surfacing to the caller
- Simple to test — background tasks can be awaited synchronously in tests
- Delivery status tracked in the alerts table (`delivered: bool`, `delivery_attempted_at`, `delivery_error: str | null`)
- Natural migration path — the `deliver_notification` interface can be abstracted; if Celery is ever needed, replacing `background_tasks.add_task(fn, args)` with `celery_task.delay(args)` requires minimal change

**Cons:**
- Not truly decoupled: background tasks run in the same process and worker thread pool as the web server. Under very high load, background tasks compete with request handling. At single-user scale, this is not a concern.
- If the Render dyno restarts between task enqueue and execution, the task is lost. At current scale: acceptable. Alert delivery failure is non-critical — the alert rule will re-evaluate on the next trigger cycle.
- No built-in retry mechanism. Mitigation: track `delivery_attempts` in the alerts table; re-trigger on next evaluation cycle if `delivered = false` and `delivery_attempts < 3`.

**Verdict:** Selected. Provides the right trade-off for current scale: no infrastructure change, non-blocking delivery, clean failure isolation, and a clear migration path if scale ever demands it.

---

## Decision

**Use FastAPI `BackgroundTasks` for notification delivery.**

Email notifications are enqueued as background tasks after the triggering API response is returned. No Redis, Celery, or external worker infrastructure is required.

---

## Implementation Contract

### Alert model additions (data_model.md update required)

```sql
ALTER TABLE alerts ADD COLUMN delivered BOOLEAN DEFAULT FALSE;
ALTER TABLE alerts ADD COLUMN delivery_attempted_at TIMESTAMPTZ;
ALTER TABLE alerts ADD COLUMN delivery_attempts INTEGER DEFAULT 0;
ALTER TABLE alerts ADD COLUMN delivery_error TEXT;
```

### Delivery interface

```python
async def deliver_notification(alert: Alert) -> None:
    """
    Background task: deliver email notification for a triggered alert.
    Called via FastAPI BackgroundTasks after API response is sent.
    Failures are logged and recorded on the alert row; never raised.
    """
    try:
        await send_email(
            to=settings.notification_email,
            subject=format_subject(alert),
            body=format_body(alert),
        )
        await mark_alert_delivered(alert.id)
    except Exception as e:
        logger.error("notification_delivery_failed", alert_id=alert.id, error=str(e))
        await record_delivery_failure(alert.id, str(e))
```

### Retry model

- `delivery_attempts` incremented on each attempt (success or failure)
- On next alert evaluation cycle: if `delivered = false` and `delivery_attempts < 3`, re-enqueue
- After 3 failed attempts: alert marked `delivery_error` and no further retries

### Email provider

Decision deferred to ST-04 implementation. Recommended: SendGrid or Mailgun API (HTTP, not SMTP) for reliability and delivery tracking. If cost is a concern, SMTP via a Gmail service account is acceptable at single-user scale.

---

## Consequences

**Positive:**
- Zero infrastructure change required — EPIC-02 can be implemented without Render plan upgrade or new services
- API response latency unaffected by email delivery
- Simple operational model — no worker processes to monitor

**Negative:**
- Background task delivery is best-effort, not guaranteed-exactly-once
- Task loss on dyno restart is possible (acceptable at current scale)
- No real-time delivery monitoring (mitigated by delivery status in alerts table)

**Future considerations:**
- If the system ever becomes multi-user or requires guaranteed delivery: abstract the delivery interface behind `NotificationDeliveryService` protocol; swap BackgroundTasks implementation for Celery without changing callers
- If daily portfolio summary requires scheduled triggering (not request-triggered): consider a lightweight scheduler (APScheduler, or Render cron job hitting an internal endpoint) — this does not require Celery

---

## References

- BLG-TECH-08: `claude/backlog/backlog.md`
- EPIC-02 v2.1 release plan: `claude/cycles/2026-03-18__release-v2.1/release_plan.md`
- ST-01 acceptance criteria: `claude/cycles/2026-03-18__release-v2.1/stage4_backlog_slice.md`
- Backend engineering patterns: `docs/specs/api_contracts/backend_engineering_patterns.md`
