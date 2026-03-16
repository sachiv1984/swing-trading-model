**Owner:** Director of Quality
**Status:** Signed Off (with findings — see ST-07 notes)
**Version:** 1.1
**Last Updated:** 2026-03-16

---

# QA Evidence — EPIC-03: QA Infrastructure & Coverage

**Cycle:** 2026-03-15__release-v1.10
**EPIC:** EPIC-03
**Branch:** exec/2026-03-15__release-v1.10/EPIC-03
**QA Environment:** https://trading-assistant-staging.onrender.com
**Sprint goal:** Establish staging as canonical pre-merge QA environment and close the CohortAnalysis architecture violation, backend integration test gap, and v1.7 QA scenario gaps carried since v1.7–v1.9.

---

## ST-05 — FastAPI TestClient integration tests for portfolio endpoints

**Classification:** autonomous
**Commit:** 5860411
**Spec references:** `docs/specs/api_contracts/portfolio_endpoints.md`

**What was built:**
`tests/test_portfolio_integration.py` — 15 TestClient tests for `GET /portfolio`. Covers: response shape (all required fields present), GBP conversion for UK positions (entry_price and current_price in GBP), GBP conversion for US positions (USD→GBP via live_fx_rate), portfolio heat calculation for known inputs, grace period / display_status logic. All DB and pricing calls mocked — CI-safe.

**Deviation DEV-ST05-01 (P3):** `GET /portfolio/prospective-heat` not defined in `portfolio_endpoints.md` and not implemented in `backend/main.py`. Tests for this endpoint skipped with `@unittest.skip`. Deferred to a future spec cycle — no P0/P1 impact.

| AC | Status | Notes |
|---|---|---|
| TestClient tests for GET /portfolio — response shape | Pass | 4 shape tests |
| GBP conversion for US positions | Pass | 4 conversion tests |
| Portfolio heat correct for known inputs | Pass | 3 heat tests |
| All tests CI-safe (no live DB) | Pass | All DB/pricing calls mocked |
| Tests pass in isolation | Pass | No ordering dependencies |
| TestClient tests for GET /portfolio/prospective-heat | Deviation | DEV-ST05-01 (P3) — endpoint not in spec; tests skipped |

---

## ST-06 — Add integration test CI step

**Classification:** autonomous
**Commit:** 5860411 (same commit as ST-05 — workflow in same PR)
**Spec references:** `docs/specs/api_contracts/portfolio_endpoints.md`

**What was built:**
`.github/workflows/integration-tests.yml` — GitHub Actions workflow running `test_portfolio_integration` on every PR to `main` and every push to `exec/**` and `main`. Step clearly named "Portfolio Integration Tests (ST-05)". Build fails if any test fails.

| AC | Status | Notes |
|---|---|---|
| CI step runs ST-05 tests on every PR and push to main | Pass | Triggers on pull_request + push |
| Integrated into new workflow | Pass | integration-tests.yml (new file) |
| Build fails if any integration test fails | Pass | pytest exit code propagates |
| CI run time visible in PR checks (step named clearly) | Pass | Job name: "Portfolio Integration Tests (ST-05)" |
| Director of Quality confirms CI step present and passing | Pending | Confirmed once CI runs on this PR |

---

## ST-07 — Author v1.7 missing QA test scenarios (BLG-QA-01)

**Classification:** delegated_qa
**Commit:** e01d658
**Spec references:**
- `claude/cycles/2026-03-02__release-v1.7/verification_report.md#6`
- `docs/testing/v1.7-qa-scenario-gaps.md`

**What was built:**
`docs/testing/v1.7-qa-scenario-gaps.md` — 4 scenarios closing the 3 v1.7 verification gaps (gap 1 split into GAP-01 + GAP-02):
- GAP-01: `sharpe_ratio_trade_method` present in POST /validate/calculations
- GAP-02: exactly 14 validated metrics returned
- GAP-03: GET /portfolio field alignment vs `portfolio_endpoints.md` v1.9.0
- GAP-04: `holding_days` present on GET /trades records

Scenarios follow canonical format (scenario ID, setup, steps, expected result). All scenarios executable against staging. Registered in `docs/testing/` alongside the existing canonical scenario library.

| AC | Status | Notes |
|---|---|---|
| 3 gap scenarios authored (4 created — gap 1 split) | Pass | GAP-01 through GAP-04 |
| Canonical scenario format followed | Pass | Setup / Steps / Expected result / Notes |
| Scenarios executable against staging | Pass | All 4 executed 2026-03-16 |
| Registered in canonical test scenario library | Pass | docs/testing/v1.7-qa-scenario-gaps.md |
| BLG-QA-01 assigned; TEST-GAP-EPIC-06 resolved | Pass | TEST-GAP-EPIC-06 retired in sign-off |
| Director of Quality sign-off | Pass | Signed 2026-03-16 — see findings below |

---

## EPIC-level Consolidation

| ST Item | Spec Reference | What was built | Result | Deviations |
|---|---|---|---|---|
| ST-05 | portfolio_endpoints.md | 15 TestClient integration tests for GET /portfolio | Pass — CI green | DEV-ST05-01 P3 — prospective-heat skipped |
| ST-06 | portfolio_endpoints.md | integration-tests.yml CI workflow | Pass — CI step visible, named correctly | None |
| ST-07 | verification_report v1.7 §6 | 4 QA scenarios (GAP-01 through GAP-04) | Signed off with findings — see sign-off block | BLG-BE-01 filed (GAP-03 finding) |

**QA sign-off block:** (Director of Quality)
- [x] ST-05 integration tests verified: CI step "Portfolio Integration Tests (ST-05)" ran and all 15 tests passed on PR #72
- [x] ST-06 verified: CI step visible in PR checks, named "Portfolio Integration Tests (ST-05)"
- [x] ST-07 GAP-01 executed on staging and passed — `sharpe_ratio_trade_method` confirmed present in POST /validate/calculations response
- [x] ST-07 GAP-02 executed on staging and passed — exactly 14 validated metrics returned
- [ ] ST-07 GAP-03 — **FAIL** — GET /portfolio does not return `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value`. Fields in spec since v1.8.2 but absent from response. Filed as BLG-BE-01. Test coverage gap closed; implementation gap tracked separately.
- [ ] ST-07 GAP-04 — **BLOCKED** — staging has 0 closed trades; `holding_days` cannot be verified on GET /trades. Scenario valid and retained. Accepted as staging test data gap.
- [x] TEST-GAP-EPIC-06 retired — test coverage gaps closed as formal scenarios; implementation findings (GAP-03) filed as BLG-BE-01
- [x] DEV-ST05-01 (P3) acknowledged — prospective-heat deferred, no P0/P1 impact
- Signed off by: Director of Quality
- Date: 2026-03-16
- Comments: ST-05 and ST-06 fully verified via CI. ST-07 scenarios authored and executed — GAP-01/02 pass, GAP-03 reveals backend bug (BLG-BE-01), GAP-04 blocked by staging data. EPIC-03 objectives met: staging is canonical QA env, integration tests in CI, v1.7 test gaps closed as scenarios. BLG-BE-01 requires attention in next sprint.
