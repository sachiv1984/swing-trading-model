**Owner:** Backend Engineering Patterns Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Backend Engineering Patterns

This document records canonical backend engineering decisions and patterns for the Momentum Trading Assistant. It is the authoritative cross-reference for architecture decisions that affect multiple features or the overall system design. Individual ADRs are the detailed records; this document provides the indexed summary and implementation contract.

---

## Architectural Decision Index

| ADR | Title | Decision | Status | Date |
|-----|-------|----------|--------|------|
| ADR-002 | Frontend-Only R-Multiple Calculation | R-Multiple computed client-side in `RMultipleAnalysis.js` — backend data (stop_price) not reliably available for historical trades | Accepted | 2026-02-16 |
| ADR-003 | Notification Delivery Architecture | FastAPI `BackgroundTasks` for email delivery — no external worker infrastructure; tasks enqueued after API response returns | Accepted | 2026-03-18 |

---

## ADR-003 — Notification Delivery Pattern Summary

**Full record:** `docs/adr/ADR-003-notification-delivery-architecture.md`

**Decision:** Use FastAPI `BackgroundTasks` for notification delivery.

**Pattern:** Alert evaluation triggers delivery as a background task (non-blocking). Email fires after the API response is returned to the client. No Redis, Celery, or external worker process required.

**Key constraints for implementers:**
- `deliver_notification(alert)` must never raise — catch all exceptions, log via structured logger, record on alert row
- Alert table must carry: `delivered: bool`, `delivery_attempted_at: timestamptz`, `delivery_attempts: int`, `delivery_error: text | null`
- Retry policy: re-enqueue on next evaluation cycle if `delivered = false` and `delivery_attempts < 3`; abandon after 3 failures
- Email provider selection deferred to ST-04 — recommend SendGrid or Mailgun API (not SMTP)

**Migration path:** If Celery is ever needed, abstract delivery behind `NotificationDeliveryService` protocol; swap implementation without changing callers.

---

## General Patterns

### Background work

Use FastAPI `BackgroundTasks` for non-critical post-response work (notifications, audit log writes, cache invalidation) that must not block the user. Do not use background tasks for critical-path writes that must complete atomically with the request.

### Structured logging

All backend events must use the structured logging standard defined in `docs/specs/structured_logging_standards.md`. Notification delivery events must log: `alert_id`, `alert_type`, `delivery_attempt`, `outcome`, and `error` (if failed).

### Database migrations

All schema changes must follow the migration governance standard defined in `docs/governance/database_migration_governance.md`. Alert table additions (ADR-003 delivery tracking columns) require a migration authored per that standard.

### API endpoint authoring

All new endpoints must be added to `docs/reference/openapi.yaml` in the same commit as the contract spec. See `CLAUDE.md §2`.

---

*For detailed rationale behind each decision, see the referenced ADR.*
