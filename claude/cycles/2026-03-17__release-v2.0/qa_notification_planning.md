**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Complete
**Release:** v2.0
**Cycle:** 2026-03-17__release-v2.0
**Last Updated:** 2026-03-17
**Filed by:** Director of Quality (ST-11 output — DL-003 gate clearance)

---

# QA Notification Planning Session — v2.0

**Date:** 2026-03-17
**Session type:** Pre-sprint QA gate assessment (ST-11 / DL-003)
**Participants:** Director of Quality (lead), Facilitator, Challenger

---

## DL-003 Required Outputs

Per the roadmap auto-advance trigger (DL-003), this session must specify:

### 1. Test types required for alert delivery

| Test type | Description | Feasibility for v2.0 |
|-----------|-------------|---------------------|
| Unit tests | Alert trigger logic (condition evaluation per alert type) | ✅ Feasible — pure logic, no infrastructure |
| Integration tests (backend) | Alert generation → notification queue write | ❌ Requires task queue (absent) |
| Integration tests (email delivery) | Alert → email sent to test inbox | ❌ Requires SMTP mock + email routing in staging |
| E2E tests (in-app feed) | Alert generated → in-app notification rendered | ⚠️ Feasible if in-app feed is decoupled from email delivery |
| QA scenario tests (staging) | End-to-end: position triggers alert, notification delivered | ❌ Requires staging test data + delivery infrastructure |

### 2. Notification delivery modes to be tested

| Mode | Status | Notes |
|------|--------|-------|
| Email (primary) | ❌ Not testable in v2.0 | No SMTP/transactional email provider; no background worker; no staging email routing |
| SMS (optional) | ❌ Not testable in v2.0 | Requires third-party SMS provider; out of scope until email delivery is stable |
| In-app notification feed | ⚠️ Partially testable | Can be decoupled from delivery — but alert generation backend not yet specced |

### 3. Expected test infrastructure

| Infrastructure item | Current status | Required for QA sign-off |
|--------------------|----------------|--------------------------|
| Background job/task queue (Celery + Redis or equivalent) | ❌ Absent — FastAPI backend is fully synchronous | Required for async alert delivery |
| SMTP mock (Mailpit / Mailtrap / similar) | ❌ Absent | Required for email delivery testing in staging |
| Staging email routing (test inbox isolation) | ❌ Absent | Required to prevent test alerts reaching real inboxes |
| Alert trigger test data in staging | ⚠️ Possible per OPERATIONAL_GUIDE §8.2 staging data prerequisites | Requires positions at specific states (near stop, day 8/9, regime flip) |
| Notification spec (`alerts_endpoints.md`) | ❌ Absent | Required before any QA scenario can be authored |

---

## Session Assessment

**Director of Quality findings:**

The backend has no asynchronous processing infrastructure. `GET /backend/main.py` contains no task queue, no worker process, no background job scheduler. Adding async delivery infrastructure is an architectural decision, not a feature implementation — it requires a decision record on the approach (sync inline email vs. dedicated worker + queue) before any implementation begins.

Without this infrastructure decision:
- The notification spec (ST-06) cannot be written to a stable architectural baseline
- QA scenarios (ST-11) cannot be meaningfully authored
- Email delivery testing (ST-08) cannot be validated in staging
- Director of Quality cannot provide a valid sign-off

**Challenger position (recorded):** Synchronous inline email delivery is a legitimate simpler first iteration that could be tested without background infrastructure. This is a valid scoping option but must be an explicit architectural decision (Decision Record) before sprint execution — not discovered mid-sprint.

---

## Session Decision

**DL-003 gate status: Documented — session complete ✅**

**EPIC-03 recommendation: Defer to v2.1**

| Rationale | Evidence |
|-----------|---------|
| No notification spec exists | alerts_endpoints.md is absent; cannot write QA scenarios against unknown spec |
| No async delivery infrastructure | FastAPI backend is synchronous; no queue, no worker |
| Architectural decision required before spec | sync vs. async delivery must be decided before spec authoring begins |
| Single sprint v2.0 scope is viable without EPIC-03 | Core scope (EPIC-01/02/04/05) ~42 hrs mid — within single sprint capacity |

**New backlog item required before v2.1 sprint planning seals:**
- `BLG-TECH-08` — Async notification delivery architecture decision record — P2 — must be completed (ADR authored and signed off) before v2.1 sprint planning seals for any EPIC-03 story

---

## v2.0 Single Sprint Confirmation

With EPIC-03 deferred:

| Group | Stories | Mid hrs |
|-------|---------|---------|
| EPIC-01 (4.3 Signal Exposure) | ST-01, ST-02 | ~4 |
| EPIC-02 (4.1b Tax-Year P&L) | ST-03, ST-04, ST-05 | ~13 |
| EPIC-04 (Backend Completeness) | ST-12 (P1), ST-13 (stretch) | ~9 |
| EPIC-05 (Documentation Pack) | ST-14, ST-15, ST-16, ST-17, ST-20 (stretch) | ~16 |
| **Sprint total (core, excl stretch)** | **11 stories** | **~37 hrs** |
| Stretch (ST-13, ST-20) | 2 stories | ~7 |
| **Sprint total (incl stretch)** | **13 stories** | **~44 hrs** |

*EPIC-06 (Governance Tooling, ST-18/19) remains parallel track — not sprint execution.*

**Single sprint is feasible.** Consistent with v1.9 Sprint 1 baseline (~42 hrs mid, accepted).

---

## RISK-01 Resolution

**RISK-01 (cycle_summary.md Pre-sprint Required Decisions):**
**Resolved as: EPIC-03 deferred to v2.1.**
Sprint Planning Engine STEP -1 checklist item [RISK-01] is resolved — DoQ recommendation accepted, deferral confirmed. EPIC-03 stories (ST-06–ST-11) do not enter sprint execution for v2.0.

---

## Facilitator Close

Session complete. Director of Quality recommendation accepted. EPIC-03 deferred to v2.1. BLG-TECH-08 to be added to backlog. v2.0 proceeds as single sprint.

Signed off: Director of Quality | Facilitator | 2026-03-17
