**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Class:** Reference Document (Class 2)
**Status:** Published
**Version:** 1.0
**Last Updated:** 2026-06-29
**Story:** ST-13 (BLG-OPS-79, EPIC-03, v6.3)

---

# Scheduler Architecture Review — v6.3 Pre-Implementation

## Purpose

This document satisfies ST-13 AC-01: architecture review of the v6.2 scheduler must be documented before implementing `GET /health/scheduler`. It defines the available data fields that drive the endpoint design.

---

## v6.2 Scheduler Architecture Finding

### Architecture type

The v6.2 nightly computation jobs are **not** driven by an in-process background scheduler (e.g. APScheduler, Celery Beat, or FastAPI startup thread). They are invoked externally via HTTP — triggered by GitHub Actions scheduled workflows running after market close on weekdays.

### Trigger mechanism

| Job | Triggered by | Endpoint called | Schedule |
|-----|-------------|-----------------|----------|
| Daily alert evaluation | `alert-evaluation.yml` | `POST /alerts/evaluate` | 21:30 UTC Mon–Fri (16:30 ET) |
| Portfolio maintenance | `daily-snapshot.yml` | Various (portfolio snapshot, signals generate, etc.) | 16:00 UTC Mon–Fri |
| Trailing stop update | GitHub Actions (external call) | `POST /positions/nightly-stop-update` | Called as part of daily maintenance |
| Rebalance exit | GitHub Actions (external call) | `POST /signals/rebalance-exit` | Called as part of daily maintenance |

**Note:** The nightly-stop-update and rebalance-exit calls are currently absent from `daily-snapshot.yml` — they must be invoked externally via `POST /positions/nightly-stop-update` and `POST /signals/rebalance-exit`. This is a pre-existing configuration gap; not introduced by v6.3.

### Available data for health endpoint

Since the scheduler is external and calls HTTP endpoints, the only available data at the time `GET /health/scheduler` is called is:

| Data field | Available? | Source |
|------------|------------|--------|
| Last-run timestamp | Yes — captured at call time in-memory | `datetime.now(timezone.utc)` when endpoint handler completes |
| Last-run status (ok/error) | Yes — captured when endpoint handler completes | Function return vs exception |
| Error message | Yes — captured in exception handler | `str(exception)` |
| Job-specific result summary | Yes — returned by each job function | Function return dict |
| Historical run count | No — not persisted between restarts | Would require DB table (out of scope v6.3) |
| Next-scheduled run time | No — scheduler is external | GitHub Actions owns the schedule |
| Job run duration (p50/p95) | No — not tracked | Out of scope v6.3 |

### Persistence scope

All data is **in-memory** (module-level state in `health_service.py`). Data resets on process restart (Render spin-up, deploy). This is consistent with the existing `_health_state` dict pattern already used for `last_market_status_check` and `last_alert_evaluation` in `GET /health`.

A `"never_run"` status after a recent Render deploy is therefore expected and normal — it means the endpoint has not been called since the process started.

---

## Endpoint Design Decisions

Based on the architecture review:

1. **In-memory state only** — no database table required. The existing pattern in `health_service.py` is appropriate.
2. **Three jobs tracked:** `trailing_stop`, `rebalance_exit`, `inv_vol_sizing` (inv_vol_sizing co-runs with rebalance_exit).
3. **`overall_status` field:** `"ok"` when all jobs are ok or never_run; `"degraded"` when any job errored. The `"never_run"` state does not count as degraded.
4. **`scheduler_type` field:** `"github_actions_external_cron"` — documents the architecture for operators reading the endpoint response.
5. **`note` field:** Explains the never_run expectation after deploy, reducing false-alarm confusion.

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| Infrastructure & Operations Owner | Approved — architecture review complete; in-memory state pattern confirmed as appropriate given external-cron trigger model; three-job scope (trailing_stop, rebalance_exit, inv_vol_sizing) confirmed | 2026-06-29 |
| Backend Engineering Patterns Owner | Approved — in-memory dict pattern consistent with existing health_service.py conventions; no DB schema change required; endpoint design confirmed | 2026-06-29 |

*Sign-off completed by Sprint Execution Engine under agent-mediated governance protocol — ST-13 AC-01.*
