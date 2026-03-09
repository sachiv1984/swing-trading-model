# QA Evidence — EPIC-05 (Test Infrastructure)

**Cycle:** 2026-03-06__release-v1.9
**EPIC:** EPIC-05
**Prepared by:** Director of Quality
**Date:** 2026-03-09
**Status:** Complete — all 2 stories signed off

---

## Story Sign-Off Summary

| Story | Title | Result | Signed Off |
|-------|-------|--------|------------|
| ST-11 | Canonical Test Scenario Library Phase 1 | Pass | 2026-03-09 |
| ST-13 | Service Layer Test Coverage Standard | Pass | 2026-03-09 |

---

## ST-11 — Canonical Test Scenario Library Phase 1 (Risk Dashboard)

**Commit:** `76be77d`
**Method:** Code review + Playwright test list verification

### Acceptance Criteria Review

| Criterion | Evidence | Result |
|-----------|----------|--------|
| 17 previously-blocked scenarios automated | `npx playwright test --list` confirmed 17 tests in 5 describe blocks | Pass |
| No live backend required | All API calls intercepted via `page.route()` mock layer | Pass |
| Mock data matches risk_dashboard_scenarios.md §4 | TD-01–TD-10 in `tests/e2e/mocks/portfolio-mock-data.js` | Pass |
| CI gate added | `.github/workflows/playwright.yml` triggers on risk component changes | Pass |
| risk_dashboard_scenarios.md updated | v1.0.1 → v1.1, §5 rewritten with automation coverage table | Pass |
| TEST-GAP-EPIC-01 resolved | Backlog entry updated to CLOSED | Pass |

### Decision Record

Approach agreed via structured facilitation session (Facilitator, Challenger, QA authority, Frontend Lead). Seeded DB approach eliminated as infeasible (no test deployment tier). Mock layer approach selected. BLG-API-01 raised to cover backend TestClient coverage gap in v1.10.

### QA Observations

None blocking.

**QA Gate: PASS — Director of Quality, 2026-03-09**

---

## ST-13 — Service Layer Test Coverage Standard

**Commit:** `8c0108b`
**Method:** Static code review + local test execution evidence

### Acceptance Criteria Review

| Criterion | Evidence | Result |
|-----------|----------|--------|
| Tier 1 scope defined (grace_service, drawdown_service) | Decision session held; scope recorded in execution_state.json notes | Pass |
| 18 unit tests written, all pass | `pytest tests/test_service_coverage.py -v` → 18 passed | Pass |
| 100% line coverage on both Tier 1 services | pytest-cov report: grace_service 100%, drawdown_service 100% | Pass |
| 80% threshold enforced (`--fail-under=80`) | `--cov-fail-under=80` in CI workflow + local run | Pass |
| CI gate added | `.github/workflows/service-coverage.yml` — triggers on all exec/** + main/develop PRs | Pass |
| backend_engineering_patterns_owner.md updated | v1.0 → v1.1; §11 Service Test Coverage Standard added | Pass |
| pytest + pytest-cov added to requirements.txt | `pytest==9.0.2`, `pytest-cov==7.0.0` appended | Pass |
| All tests CI-safe (no live DB) | DB dependencies mocked via `unittest.mock.patch` | Pass |

### Test Coverage Detail

**Test execution (local):**
```
tests/test_service_coverage.py::TestGraceService::test_grace_day_0_returns_10 PASSED
tests/test_service_coverage.py::TestGraceService::test_grace_day_1_returns_9 PASSED
tests/test_service_coverage.py::TestGraceService::test_grace_day_5_returns_5 PASSED
tests/test_service_coverage.py::TestGraceService::test_grace_day_9_returns_1 PASSED
tests/test_service_coverage.py::TestGraceService::test_grace_day_10_in_grace_returns_0 PASSED
tests/test_service_coverage.py::TestGraceService::test_grace_day_15_clamps_to_0 PASSED
tests/test_service_coverage.py::TestGraceService::test_not_in_grace_returns_none PASSED
tests/test_service_coverage.py::TestGraceService::test_return_type_is_int_when_in_grace PASSED
tests/test_service_coverage.py::TestGraceService::test_return_type_is_none_when_not_in_grace PASSED
tests/test_service_coverage.py::TestDrawdownService::test_no_history_returns_zero_fields PASSED
tests/test_service_coverage.py::TestDrawdownService::test_at_peak_returns_zero_drawdown PASSED
tests/test_service_coverage.py::TestDrawdownService::test_10pct_drawdown PASSED
tests/test_service_coverage.py::TestDrawdownService::test_50pct_drawdown PASSED
tests/test_service_coverage.py::TestDrawdownService::test_drawdown_is_never_positive PASSED
tests/test_service_coverage.py::TestDrawdownService::test_result_fields_always_present PASSED
tests/test_service_coverage.py::TestDrawdownService::test_drawdown_rounding_4dp PASSED
tests/test_service_coverage.py::TestDrawdownService::test_peak_rounded_2dp PASSED
tests/test_service_coverage.py::TestDrawdownService::test_boundary_fractional_drawdown PASSED

----------- coverage: platform linux, python 3.12.8-final-0 -----------
Name                          Stmts   Miss  Cover
-------------------------------------------------
services/grace_service.py         5      0   100%
services/drawdown_service.py      9      0   100%
-------------------------------------------------
TOTAL                            14      0   100%

Required test coverage of 80% reached. Total coverage: 100.00%
18 passed in 1.53s
```

### Spec Alignment

- `grace_service.py`: formula `max(0, 10 - holding_days)` verified against `position_endpoints.md` v1.8.3
- `drawdown_service.py`: formula `(current - peak) / peak * 100`, clamped ≤ 0.0, verified against `metrics_definitions.md` v1.5.8 §Current Drawdown

### QA Observations

None. No deviations filed.

**QA Gate: PASS — Director of Quality, 2026-03-09**

---

## EPIC-05 QA Gate Sign-Off

All acceptance criteria met for both stories in EPIC-05.

- ST-11: 17 Playwright acceptance tests automated (previously 0). CI gate active.
- ST-13: 18 service unit tests, 100% coverage (threshold 80%). CI gate active.
- TEST-GAP-EPIC-01: CLOSED
- BLG-API-01: Raised (backend TestClient gap, target v1.10)

**EPIC-05 QA Gate: PASS**
**Director of Quality — 2026-03-09**
