Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-17

---

# QA Evidence Log — EPIC-04 Backend Completeness

**EPIC:** EPIC-04 — Backend Completeness
**Cycle:** 2026-03-17__release-v2.0
**Branch:** exec/2026-03-17__release-v2.0/EPIC-04
**Sprint goal:** Ship the v2.0 core product scope: fix the P1 portfolio response defect, deliver the UK tax-year P&L report endpoint and frontend view, and expose the signal exposure controls — making all three production-ready in a single sprint.

---

## ST-12 — Fix GET /portfolio missing 4 fields (BLG-BE-01 P1)

**Spec references:**
- `docs/specs/api_contracts/portfolio_endpoints.md` — GET /portfolio response schema
- `docs/testing/v1.7-qa-scenario-gaps.md — GAP-03`

**Commit:** `04ed5e8` on `exec/2026-03-17__release-v2.0/EPIC-04`

**What was built:**
Fixed the empty-positions early-return path in `backend/services/portfolio_service.py`. The path previously returned only cash/value fields, omitting `initial_value`, `net_deposits`, `current_drawdown_percent`, and `peak_portfolio_value`. The fix calls `get_total_deposits_withdrawals()` and `get_drawdown_fields()` in the empty path, matching the non-empty path behaviour. Integration tests `TestGetPortfolioEmpty` and `TestGetPortfolioFieldContract` added and pass.

**Acceptance criteria:**
- [x] `GET /portfolio` returns `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value`
- [x] Values match formulas in `portfolio_endpoints.md`
- [x] `tests/test_portfolio_integration.py` assertions for these 4 fields pass
- [x] GAP-03 scenario in `v1.7-qa-scenario-gaps.md` moves to PASS

**Test scenarios to execute:**
- `docs/testing/v1.7-qa-scenario-gaps.md — GAP-03` (field alignment scenario — marked PASS post-fix)
- `tests/test_portfolio_integration.py::TestGetPortfolioFieldContract` (3 tests)
- `tests/test_portfolio_integration.py::TestGetPortfolioEmpty` (integration test for empty path)

**QA findings:** *(Director of Quality to complete)*

**Disposition:** *(Director of Quality: Pass / Pass with notes / Fail)*

---

## ST-13 — Spec + implement GET /portfolio/prospective-heat (BLG-BE-02 stretch)

**Spec references:**
- `docs/specs/api_contracts/portfolio_endpoints.md v2.0.0` — GET /portfolio/prospective-heat
- `docs/specs/Specs_Index.md §6.3` — DEV-ST05-01 closed

**Commit:** `279e832` on `exec/2026-03-17__release-v2.0/EPIC-04`

**What was built:**
Spec authored in `portfolio_endpoints.md` v2.0.0 (query params, response shape, business rule failures, FX handling). Backend router created at `backend/routers/prospective_heat.py` with UK/US FX logic matching sizing_service pattern. Registered in `backend/main.py`. `@unittest.skip` removed from `TestProspectiveHeat`. 7 tests pass covering: UK basic, existing heat accumulation, US live FX, US FX override, stop ≥ entry, zero shares, zero portfolio value.

**Acceptance criteria:**
- [x] `GET /portfolio/prospective-heat` spec authored in `portfolio_endpoints.md` v2.0.0
- [x] Endpoint implemented in `backend/routers/prospective_heat.py`
- [x] `@unittest.skip` removed; all 7 `TestProspectiveHeat` tests pass
- [x] DEV-ST05-01 deviation closed
- [x] `Specs_Index.md §6.3` updated to RESOLVED

**Test scenarios to execute:**
- `tests/test_portfolio_integration.py::TestProspectiveHeat` (7 tests — run: `DATABASE_URL=postgresql://test:test@localhost/test python3 -m pytest tests/test_portfolio_integration.py::TestProspectiveHeat -v`)

**Process deviation noted:**
- ST-20's commit (`4adbe21` — analytics_scenarios.md) was made on this EPIC-04 branch rather than EPIC-05. This is a cross-branch process deviation (content correct, wrong branch). The commit prefix `[EPIC-04][ST-20]` was used. Content will land in main via this PR. EPIC-05 execution state reflects this.

**QA findings:** *(Director of Quality to complete)*

**Disposition:** *(Director of Quality: Pass / Pass with notes / Fail)*

---

## EPIC-04 Consolidation

**Test scenarios used:**
- `docs/testing/v1.7-qa-scenario-gaps.md — GAP-03`
- `docs/testing/risk_dashboard_scenarios.md` (portfolio heat scenarios — regression check)
- `tests/test_portfolio_integration.py` (integration tests — 10 tests covering ST-12 and ST-13)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-12 | `portfolio_endpoints.md — GET /portfolio` | Empty-path fix in portfolio_service.py; 2 test classes added | 4 missing fields returned; GAP-03 PASS | Pending QA | None |
| ST-13 | `portfolio_endpoints.md v2.0.0 — GET /portfolio/prospective-heat` | Spec + router + 7 tests | Endpoint live; tests pass; skip removed | Pending QA | None (ST-20 cross-branch — process only) |

**QA test coverage:**
- Scenarios run: `v1.7-qa-scenario-gaps.md — GAP-03`, `test_portfolio_integration.py`
- Regression areas checked: GET /portfolio response contract, prospective heat calculation, FX handling
- Known deviations filed: None (ST-20 cross-branch commit is process-level, not spec-level)

**QA sign-off block:** *(Director of Quality completes this)*
> **Authoring note:** When completing the sign-off block, update all AC table rows from "Pending" to "Pass" or "Pass with notes" in the same edit.
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked (GET /portfolio contract, GAP-03, prospective heat)
- Signed off by: Director of Quality
- Date:
- Comments:
