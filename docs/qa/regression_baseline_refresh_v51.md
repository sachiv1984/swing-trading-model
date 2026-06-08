**Owner:** QA Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-15, BLG-QA-48)

---

# Regression Test Suite Baseline Refresh — Post-v5.1

## Purpose

This document records the v5.1 additions to the regression test suite, confirming they are present and accounted for in the baseline. Produced per BLG-QA-48.

**Note:** No formal regression baseline document exists at this time. BLG-QA-50 has been filed to create one (see §3 below). This document serves as an interim record of the v5.1 additions until the formal baseline is produced.

---

## v5.1 Test Additions

### 1. POST /digest/si05/send — backend/routers/test.py

**Status: ✅ CONFIRMED**

The endpoint `POST /digest/si05/send` (SI-05 Phase 1 weekly strategy integrity digest) is present in `backend/routers/test.py`:

```python
# backend/routers/test.py:177
{"name": "POST /digest/si05/send", "method": "POST", "url": f"{base_url}/digest/si05/send", "body": {}, "critical": False},
```

This entry was added as part of v5.1 EPIC-01 ST-01 (SI-05 Phase 1 implementation). The endpoint is tested as non-critical (delivery failures do not block the health check pipeline).

---

### 2. signals-allocation-insufficient.spec.js — Playwright CI Scenarios

**Status: ✅ CONFIRMED**

File: `tests/e2e/signals-allocation-insufficient.spec.js`

5 Playwright scenarios confirmed:

| Scenario ID | Description |
|---|---|
| SC-SIG-AI-01a | Orange "Cannot Size" badge visible on signal card |
| SC-SIG-AI-01b | "Allocation insufficient" panel rendered below card metrics |
| SC-SIG-AI-02a | Reason string rendered within the allocation_insufficient card |
| SC-SIG-AI-02b | Signal with no reason renders card without error |
| SC-SIG-AI-03a | Active signal shows "New Signal" badge, not "Cannot Size" |

These scenarios were added as part of v5.1 EPIC-02 (signals allocation insufficient feature). They run as part of the CI Playwright test suite.

---

## Baseline Status

| Check | Status |
|---|---|
| POST /digest/si05/send in test.py | ✅ Confirmed |
| signals-allocation-insufficient.spec.js (5 scenarios) | ✅ Confirmed |
| Formal regression baseline document | ❌ Does not exist — BLG-QA-50 filed |

---

## Follow-On Actions

**BLG-QA-50** filed: Create a formal regression test baseline document covering all current test.py entries and Playwright specs. See backlog for full scope.

---

## Sign-Off

**QA Lead:** Sprint Execution Engine (autonomous class), 2026-06-08
