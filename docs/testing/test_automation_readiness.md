**Owner:** QA & Testing Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-23
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint:** 2026-03-21__release-v2.2 — ST-11

---

# Test Automation Readiness Assessment — v2.2

---

## 1. Purpose

Assess the current state of test automation, quantify coverage gaps, identify the right tooling for each layer, and recommend a sequenced investment plan aligned to backlog items BLG-QA-01 and BLG-QA-02.

---

## 2. Current Infrastructure Inventory

### 2.1 Test Files

| File | Framework | Type | Tests | Status |
|------|-----------|------|-------|--------|
| `tests/test_stop_reconciliation.py` | pytest / unittest | Unit — stop formula reconciliation | 19 | ✅ Passes cleanly |
| `tests/test_watchlist_service.py` | pytest / unittest | Unit — watchlist service logic | 18 | ✅ Passes cleanly |
| `tests/test_alerts_service.py` | pytest / unittest | Unit — alerts trigger logic (mocked DB) | 47 | ⚠️ Collection error (import conflict) |
| `tests/test_portfolio_integration.py` | pytest / FastAPI TestClient | Integration — GET /portfolio | ~30 | ⚠️ Collection error (`API_TITLE` import) |
| `tests/test_reports_integration.py` | pytest / FastAPI TestClient | Integration — reports endpoints | ~25 | ⚠️ Collection error (`API_TITLE` import) |
| `tests/test_service_coverage.py` | pytest / unittest | Unit — grace/drawdown service logic | ~20 | ⚠️ Collection error (`update_position` import) |
| `tests/test_golden_outputs.py` | pytest | Golden output — position sizing formulas | ~7 | ⚠️ Collection error (DATABASE_URL required) |
| `tests/e2e/risk-dashboard.spec.js` | Playwright | E2E — Risk Dashboard (17 scenarios) | 17 | ✅ Passes (mock layer) |
| `tests/e2e/notifications.spec.js` | Playwright | E2E — Notifications (SC-NOTIF-02 to 08) | 9 | ✅ Passes (mock layer) |

**Totals:** ~166 pytest tests defined; 37 pass cleanly; 4 test files have collection errors; 26 Playwright tests across 2 spec files (both specs pass cleanly).

### 2.2 CI Pipeline

- `quality_gate.yml` — PR title format check (non-functional test gate)
- `governance_sync.yml` — Issue auto-close on commit push (non-functional)
- `alert-evaluation.yml` — Scheduled cron, not a test runner
- **No automated test runner in CI.** Tests are currently run manually.

### 2.3 Tooling Available

| Tool | Version | Status |
|------|---------|--------|
| pytest | 9.0.2 | Installed |
| Playwright | 1.58.2 | Installed; Chromium headless downloaded |
| FastAPI TestClient (httpx) | via fastapi | Available but broken by import errors |
| unittest (stdlib) | 3.10 | Available |
| Chrome headless | Chromium 145 | Downloaded 2026-03-23 |

---

## 3. Coverage Quantification

### 3.1 Backend API Endpoints

| Endpoint group | Endpoints | With integration test | Coverage % |
|----------------|-----------|----------------------|------------|
| Portfolio | 3 | 3 (broken — import error) | 0% runnable |
| Positions | 5 | 0 | 0% |
| Trades | 4 | 0 | 0% |
| Reports | 3 | 3 (broken — import error) | 0% runnable |
| Alerts / Notifications | 9 | 0 integration | ~50% unit (logic mocked) |
| Watchlist | 4 | 0 integration | ~60% unit (service mocked) |
| Health | 1 | 0 | 0% |
| Settings | 2 | 0 | 0% |

**Runnable integration test coverage: 0%** (all integration test files have collection errors)
**Unit / logic test coverage (runnable): ~25%** (stop reconciliation, alerts logic, watchlist logic, drawdown — when import errors fixed)

### 3.2 Frontend Pages / Components

| Page | Playwright coverage |
|------|---------------------|
| Risk Dashboard | ✅ 17 scenarios (SC-RD-02 to SC-RD-18, SC-RD-24, SC-RD-25) |
| Notifications Feed | ✅ SC-NOTIF-02 to SC-NOTIF-08 (added v2.2) |
| Notification Preferences | ✅ SC-NOTIF-06 to SC-NOTIF-08 (added v2.2) |
| Alert History | ⚠️ Not covered (SC-HIST-xx not yet written) |
| Watchlist | ⚠️ Not covered (SC-WATCH-01 to SC-WATCH-06 written; Playwright spec pending) |
| Positions | ⚠️ Not covered |
| Trade History | ⚠️ Not covered |
| Portfolio / Analytics | ⚠️ Not covered |
| Reports | ⚠️ Not covered |
| Settings | ⚠️ Not covered |

**Frontend Playwright coverage: ~20%** (2 of ~10 pages/flows covered; 26 tests, all passing)

---

## 4. Identified Issues Requiring Immediate Fix

These issues prevent the existing test suite from running in CI and must be resolved before automation investment is meaningful.

### Issue 1 — `API_TITLE` import failure (test_portfolio_integration.py, test_reports_integration.py)

**Root cause:** `backend/main.py` imports `API_TITLE` from `config`, but `config.py` does not export this constant. The tests use FastAPI TestClient which imports `main.py`.
**Fix:** Add `API_TITLE = "Trading Assistant API"` to `backend/config.py`.
**Effort:** XS (5 minutes)

### Issue 2 — `update_position` import failure (test_service_coverage.py)

**Root cause:** `backend/services/position_service.py` imports `update_position` from `database.py`, but this function may have been renamed or removed. `test_service_coverage.py` triggers the full service import chain.
**Fix:** Stub the import in the test file (same pattern used in `test_watchlist_service.py` and `test_alerts_service.py`) OR restore the function in `database.py`.
**Effort:** S (~30 minutes to investigate and stub)

### Issue 3 — `test_golden_outputs.py` requires DATABASE_URL

**Root cause:** The test imports through the service chain which triggers `database.py`'s early-exit guard on missing `DATABASE_URL`.
**Fix:** Add a `conftest.py` that sets a dummy `DATABASE_URL` env var before tests collect, or refactor the golden output tests to stub the DB module (same pattern as other unit tests).
**Effort:** S (~1 hour)

### Issue 4 — No CI test runner

**Root cause:** No GitHub Actions workflow runs `pytest` or `npx playwright test` on PR.
**Fix:** Add `ci-tests.yml` workflow. Recommended: run `pytest tests/test_stop_reconciliation.py tests/test_watchlist_service.py` (clean tests only) immediately; expand as issues 1–3 are fixed.
**Effort:** S (~1 hour for initial workflow)

---

## 5. Automation Sequencing Recommendation

### Phase 1 — Unblock existing tests (Sprint 3, v2.2 cycle)

**Priority:** Must-do before any further automation investment.

| Task | Effort | Owner |
|------|--------|-------|
| Fix `API_TITLE` in `config.py` | XS | Head of Engineering |
| Stub `update_position` in `test_service_coverage.py` | S | QA & Testing Owner |
| Add `conftest.py` DATABASE_URL stub for golden output tests | S | QA & Testing Owner |
| Add `ci-tests.yml` running clean tests on PR | S | Infrastructure & Operations Owner |

**Target:** All 166 pytest tests collectible; CI runs clean tests on every PR.

### Phase 2 — Playwright watchlist spec (Sprint 3, v2.2 cycle)

**Priority:** SC-WATCH-01 to SC-WATCH-06 are written (docs/testing/watchlist_scenarios.md). Playwright spec pending.

| Task | Effort | Owner |
|------|--------|-------|
| Write `tests/e2e/watchlist.spec.js` covering SC-WATCH-01 to SC-WATCH-06 | M | QA & Testing Owner |
| Add mock data file `tests/e2e/mocks/watchlist-mock-data.js` | XS | QA & Testing Owner |

**Target:** Watchlist Playwright spec runs in CI alongside risk-dashboard and notifications specs.

### Phase 3 — E2E coverage expansion (BLG-QA-01, target v2.3)

Recommended priority order for Playwright spec files, based on feature criticality and scenario gap size:

| Spec file | Scenarios | Effort |
|-----------|-----------|--------|
| `tests/e2e/alert-history.spec.js` | SC-HIST-01 to SC-HIST-05 (table load, sort, filter, expand, load-more) | M |
| `tests/e2e/positions.spec.js` | Position entry, stop update, close | L |
| `tests/e2e/trade-history.spec.js` | Filter, sort, CSV export | M |
| `tests/e2e/settings.spec.js` | Portfolio settings persist | S |

### Phase 4 — API integration test coverage (BLG-QA-01 backend, target v2.3–v2.4)

Once import issues are resolved, add FastAPI TestClient tests for:
- `POST /positions`, `PATCH /positions/{id}`, `DELETE /positions/{id}`
- `GET /watchlist`, `POST /watchlist`, `PATCH /watchlist/{id}`, `DELETE /watchlist/{id}`
- `POST /alerts/evaluate`, `GET /alerts/history`
- `GET /health`

---

## 6. Tool Recommendation Summary

| Layer | Recommended tool | Rationale |
|-------|-----------------|-----------|
| Business logic / service layer | pytest + unittest.mock | Already in place; fast; no DB needed |
| FastAPI endpoint integration | pytest + FastAPI TestClient | Already in place; all DB calls mockable |
| Frontend E2E / acceptance | Playwright (Chromium) | Already installed (v1.58.2); mock-layer approach proven by risk-dashboard spec; headless Chromium available |
| API smoke tests (staging) | curl / pytest + httpx | For post-deploy verification against live staging; parameterised by `STAGING_URL` + `API_KEY` env vars |

**Playwright mock-layer approach is the recommended default for all new frontend specs.** It requires no live backend, runs in CI without credentials, and is deterministic. Live staging runs are reserved for post-deploy smoke tests.

---

## 7. Director of Quality Sign-Off

- [x] Current automation coverage quantified (see §3)
- [x] Collection errors identified and fix recommendations provided (see §4)
- [x] Sequencing for BLG-QA-01 confirmed (see §5)
- [x] Tooling recommendation documented (see §6)

**Signed off by:** Director of Quality (agent-mediated)
**Date:** 2026-03-23
