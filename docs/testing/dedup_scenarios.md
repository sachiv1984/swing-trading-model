**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-04-06
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `backend/services/alerts_service.py` — `_notif_exists_today_for_ticker()` v2.4 fix (ST-02, 2026-03-31__release-v2.4)
**Sprint:** 2026-04-05__release-v2.5 — ST-13 (closes TEST-GAP-EPIC-01-v24)

---

# Acceptance Test Scenarios — Notification Dispatch Deduplication

---

## 1. Scope

These scenarios verify two deduplication behaviours introduced in v2.4 EPIC-01 ST-02:

1. **SC-DEDUP-01**: When an alert condition fires for a ticker that already has a notification of the same type dispatched today, no second notification is inserted.
2. **SC-DEDUP-02**: When deduplication suppresses a notification for one ticker, the evaluation pipeline continues uninterrupted — other tickers and other alert types are still evaluated and dispatched.

Spec reference: `backend/services/alerts_service.py` — `_notif_exists_today_for_ticker()`, `stop_loss_approach` and `grace_period_warning` dedup paths.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| Dedup helper | `backend/services/alerts_service.py` — `_notif_exists_today_for_ticker()` |
| stop_loss_approach dedup | `backend/services/alerts_service.py` lines 364–368 |
| grace_period_warning dedup | `backend/services/alerts_service.py` lines 409–413 |
| Dedup log string | `"Dedup: <type> for <ticker> already dispatched today — skipping"` |

---

## 3. Prerequisites

- Staging database with at least one portfolio and position
- Notifications table accessible
- Alerts evaluation endpoint callable: `POST /alerts/evaluate` (or equivalent trigger)

---

## 4. Test Scenarios

### SC-DEDUP-01 — Duplicate notification suppressed for same rule + same day

**Category:** Correctness
**Priority:** P1

**Setup:**
- Position ticker: e.g. `FRES.L` or any position approaching stop-loss
- `notifications` table already contains a `stop_loss_approach` notification for this ticker today (UTC)

**Test action:**
- Trigger alerts evaluation: `POST /alerts/evaluate` (or fire daily cron)
- Check `notifications` table after evaluation run

**Expected result:**
- No new `stop_loss_approach` notification row inserted for this ticker for today
- Log contains: `"Dedup: stop_loss_approach for FRES.L already dispatched today — skipping"`
- Notification count for this (portfolio, type, ticker, today) remains exactly 1

**Failure conditions:**
- A second notification is inserted (dedup not firing)
- Log does not contain the dedup message
- Notification count for the same ticker + type + day exceeds 1

---

### SC-DEDUP-02 — Evaluation pipeline continues after dedup fires

**Category:** Correctness
**Priority:** P1

**Setup:**
- Position A: ticker `FRES.L` — `stop_loss_approach` notification already dispatched today
- Position B: ticker `NVDA` — no notifications yet today, also approaching stop-loss

**Test action:**
- Trigger alerts evaluation covering both positions
- Check `notifications` table after evaluation

**Expected result:**
- `FRES.L` notification suppressed (dedup fires — same as SC-DEDUP-01)
- `NVDA` notification inserted normally — pipeline continued after dedup for FRES.L
- Total new notifications: exactly 1 (for NVDA, not for FRES.L)

**Failure conditions:**
- Both notifications suppressed (dedup incorrectly halts pipeline after first suppression)
- Neither notification created
- NVDA notification missing while FRES.L was correctly skipped

---

## 5. Known Deviations

None.
