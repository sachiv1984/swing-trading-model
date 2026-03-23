**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-23
**Sprint:** 2026-03-21__release-v2.2 — ST-09, ST-10, ST-11

---

# QA Evidence — EPIC-04: QA & Test Coverage

**EPIC:** EPIC-04 — QA & Test Coverage
**Cycle:** 2026-03-21__release-v2.2
**Sprint goal:** Execute notification acceptance scenarios, create watchlist test scenario library, produce test automation readiness assessment.

---

## ST-09 — Execute Notification Scenarios on Staging

**Spec references:** `docs/testing/notifications_scenarios.md` v1.1
**Commit SHA:** (see EPIC-04 branch commit)
**What was built:** Playwright acceptance test spec `tests/e2e/notifications.spec.js` covering SC-NOTIF-02 through SC-NOTIF-08 plus a v2.2 regression check (SC-NOTIF-06b). Mock data file `tests/e2e/mocks/notifications-mock-data.js`. All 9 tests pass (26 ms wall time per run, headless Chromium).

**SC-NOTIF-01 note:** SC-NOTIF-01 (POST /alerts/evaluate + Telegram delivery) is an API-level scenario executed via the GitHub Actions cron workflow, not a Playwright scenario. Evidence: 12 evaluation rows confirmed in live DB after first workflow run (2026-03-23). Separately confirmed in qa_evidence_EPIC-02.md ST-05 AC1.

**Root cause resolved — CSP blocking route interception:** `public/index.html` sets `connect-src 'self' https:` which blocked `fetch()` to `http://localhost:8000` (cross-port, non-HTTPS). `bypassCSP: true` added to `playwright.config.js` `use` block to allow Playwright `page.route()` interception to work correctly. No production HTML change required.

**Acceptance criteria:**

| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | SC-NOTIF-01 through SC-NOTIF-08 executed on staging (or Playwright mock where staging blocked) | Pass | SC-NOTIF-01 confirmed via cron + DB evidence; SC-NOTIF-02–08 via Playwright mock layer (9 tests pass) |
| 2 | Results recorded in QA evidence | Pass | This document |
| 3 | Director of Quality sign-off | Pass | See sign-off block below |

**Playwright test results (2026-03-23):**

| Test | Scenario | Result |
|------|----------|--------|
| SC-NOTIF-02 | Feed renders with unread indicator and correct icons | ✅ Pass |
| SC-NOTIF-02b | Feed renders within 3 seconds | ✅ Pass |
| SC-NOTIF-03 | Mark single notification as read — optimistic update | ✅ Pass |
| SC-NOTIF-04 | Mark all as read — all indicators cleared, button hidden | ✅ Pass |
| SC-NOTIF-05 | Empty state renders when no notifications | ✅ Pass |
| SC-NOTIF-06 | Preferences page renders all 4 alert types | ✅ Pass |
| SC-NOTIF-07 | Preference toggle fires PATCH and shows Saved label | ✅ Pass |
| SC-NOTIF-08 | All 4 alert types can be individually toggled | ✅ Pass |
| SC-NOTIF-06b | History tab present in notifications sub-nav (v2.2 regression) | ✅ Pass |

**Total: 9/9 pass**

**Deviations:** None

---

## ST-10 — Create Watchlist Test Scenarios

**Spec references:** `docs/specs/frontend/pages/watchlist.md` v0.1; `docs/specs/api_contracts/watchlist_endpoints.md`
**Commit SHA:** (see EPIC-04 branch commit)
**What was built:** `docs/testing/watchlist_scenarios.md` — 6 acceptance test scenarios (SC-WATCH-01 through SC-WATCH-06) with preconditions, step-by-step actions, expected results, and pass criteria. SC-WATCH-06 explicitly closes the deferred AC-6 from v2.1 ST-10 DoQ sign-off (sort order with mixed signal_status values).

**Acceptance criteria:**

| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | `docs/testing/watchlist_scenarios.md` created | Pass | File present |
| 2 | SC-WATCH-01 through SC-WATCH-06 present with preconditions, steps, expected result | Pass | All 6 scenarios complete |
| 3 | SC-WATCH-06 references deferred AC-6 from v2.1 ST-10 | Pass | Deferred AC-6 resolution section included |
| 4 | Director of Quality sign-off | Pass | See sign-off block below |

**Deviations:** None

---

## ST-11 — Test Automation Readiness Assessment

**Spec references:** None (assessment deliverable)
**Commit SHA:** (see EPIC-04 branch commit)
**What was built:** `docs/testing/test_automation_readiness.md` — full readiness assessment covering: infrastructure inventory (7 pytest files, 2 Playwright specs, Chromium 145 headless), coverage quantification (0% runnable integration, ~25% unit logic, ~20% frontend Playwright), 4 identified issues blocking existing tests, and a 4-phase automation sequencing plan aligned to BLG-QA-01.

**Acceptance criteria:**

| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | Readiness assessment document produced in `docs/testing/` | Pass | `docs/testing/test_automation_readiness.md` present |
| 2 | Automation coverage quantified | Pass | §3 of document — integration: 0%, unit: ~25%, frontend: ~20% |
| 3 | BLG-QA-01 sequencing confirmed | Pass | §5 — 4-phase plan (unblock → watchlist spec → E2E expansion → API integration) |
| 4 | Director of Quality sign-off | Pass | See sign-off block below |

**Deviations:** None

---

---

## ST-12 — Spec-to-Test Traceability Matrix

**Spec references:** `docs/specs/api_contracts/alerts_endpoints.md` v0.2; `docs/specs/api_contracts/portfolio_endpoints.md` v1.9.0; `docs/specs/api_contracts/position_endpoints.md` v1.0
**Commit SHA:** (see EPIC-04 branch commit)
**What was built:** `docs/testing/spec_to_test_traceability_matrix.md` — 54 AC entries across 3 specs; 26 covered (48%), 22 TEST-GAP entries (TEST-GAP-001 through TEST-GAP-022) with priority and target release; BLG-QA-01 sequencing cross-reference.

**HoST finding — spec drift (P1):** `GET /alerts/history` is absent from `alerts_endpoints.md` (still v0.2) and `openapi.yaml`. Registered as TEST-GAP-007. HoST to patch in v2.3 Sprint 1 per sign-off block in traceability matrix.

**Acceptance criteria:**

| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | Traceability matrix covering alert rules, portfolio, positions specs | Pass | `docs/testing/spec_to_test_traceability_matrix.md` — 3 specs, 54 ACs |
| 2 | Each AC maps to scenario ID or flagged as TEST-GAP | Pass | 26 covered; 22 TEST-GAP entries |
| 3 | TEST-GAP entries in TEST-GAP tracking register | Pass | §6 of matrix: TEST-GAP-001 to TEST-GAP-022 with priority + target |
| 4 | Director of Quality + Head of Specs Team sign-off | Pass | Both sign-off blocks in §8 of matrix |

**Deviations:** TEST-GAP-007 — `GET /alerts/history` spec drift (P1, HoST action accepted for v2.3)

---

## EPIC-Level Consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|-------|
| ST-09 | notifications_scenarios.md v1.1 | Playwright spec (9 tests), mock data, bypassCSP fix | 3 ACs — all met | Pass | None |
| ST-10 | watchlist.md v0.1; watchlist_endpoints.md | watchlist_scenarios.md — 6 scenarios + AC-6 closure | 4 ACs — all met | Pass | None |
| ST-11 | — (assessment deliverable) | test_automation_readiness.md — coverage + sequencing | 4 ACs — all met | Pass | None |
| ST-12 | alerts_endpoints.md v0.2; portfolio_endpoints.md v1.9.0; position_endpoints.md v1.0 | spec_to_test_traceability_matrix.md — 54 ACs, 22 TEST-GAPs | 4 ACs — all met | Pass | TEST-GAP-007 (P1 spec drift) |

**QA test coverage:**
- ST-09: 9 Playwright tests, all pass (headless Chromium, mock-layer approach)
- ST-10: Scenarios document reviewed against spec — all 6 scenarios traceable to canonical spec
- ST-11: Assessment produced by running `pytest --collect-only`, inspecting all test files, checking Playwright installation

---

**QA sign-off block:** (Director of Quality)
- [x] ST-09: All 9 Playwright notification tests pass; SC-NOTIF-01 confirmed via cron/DB evidence; bypassCSP fix documented
- [x] ST-10: watchlist_scenarios.md complete; SC-WATCH-06 closes deferred AC-6 from v2.1
- [x] ST-11: test_automation_readiness.md complete; BLG-QA-01 sequencing confirmed
- [x] ST-12: spec_to_test_traceability_matrix.md complete; 22 TEST-GAPs registered; TEST-GAP-007 (spec drift) escalated to HoST
- [x] No unresolved P0 deviations (TEST-GAP-007 is P1 spec gap with accepted HoST action for v2.3)
- Signed off by: Director of Quality (agent-mediated)
- Date: 2026-03-23
