**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-06
**Cycle:** 2026-05-05__release-v3.2
**EPIC:** EPIC-03 — Governance & Process Hardening

---

# QA Evidence Log — EPIC-03 (v3.2)

---

## ST-11 — Trade Plan domain test scenario registration (TEST-GAP-EPIC-01)

**Spec references:** `tests/e2e/trade-plan.spec.js`
**Source:** TEST-GAP-EPIC-01 (v3.1 delivery verification)

**Acceptance Criteria:**
- `tests/e2e/trade-plan.spec.js` test file exists and is runnable
- All SC-TP-01 to SC-TP-07 scenarios (or current count) registered in execution_state.json `test_scenarios` field
- Backend CRUD integration tests for `/trade-plans` endpoints reviewed — if gaps exist, new tests authored and registered
- TEST-GAP-EPIC-01 backlog item can be marked complete after this story ships
- No regression in existing test pass rate

**What was built:**
Verified `tests/e2e/trade-plan.spec.js` exists and contains SC-TP-01 to SC-TP-07 (7 scenarios covering form rendering, pre-population, regime context, save behaviour, and regression). Backend CRUD integration tests confirmed in `tests/test_api_contracts.py` (GET/POST/PUT/DELETE /trade-plans and /trade-plans/{id} all covered). Registered all scenarios in `execution_state.json` EPIC-03 `test_scenarios` field.

**Test scenarios to execute:**
- SC-TP-01: Form renders with all required fields
- SC-TP-02: Ticker/market pre-populated from query params
- SC-TP-03: Regime context auto-populated from GET /market/status
- SC-TP-04: Save button disabled when ticker is empty
- SC-TP-05: Existing plan banner shown when position already has a plan
- SC-TP-06: Success banner shown after saving
- SC-TP-07: No regression — Positions and Watchlist pages still render

**QA findings:**
Playwright test run 2026-05-06 (engine): `npx playwright test tests/e2e/trade-plan.spec.js` — **8/8 passed (14.3s)**. SC-TP-01 through SC-TP-07b all pass. Backend CRUD integration coverage confirmed in `tests/test_api_contracts.py`. No regression detected.

**Disposition:**
Pass

---

## ST-12 — Earnings Calendar and UK screener test registration (TEST-GAP-EPIC-03)

**Spec references:** `tests/e2e/earnings-calendar.spec.js`, `tests/e2e/screener-uk-suffix.spec.js`
**Source:** TEST-GAP-EPIC-03 (v3.1 delivery verification)

**Acceptance Criteria:**
- Both test files exist and are runnable in CI
- SC-EARN-01 to SC-EARN-09 and SC-UK-01 to SC-UK-04 registered in execution_state.json `test_scenarios`
- TEST-GAP-EPIC-03 backlog item can be marked complete after this story ships
- No regression in existing test pass rate

**What was built:**
Verified `tests/e2e/earnings-calendar.spec.js` (SC-EARN-01 to SC-EARN-09, 9 scenarios) and `tests/e2e/screener-uk-suffix.spec.js` (SC-UK-01 to SC-UK-04, 4 scenarios) both exist. Registered all 13 scenarios in `execution_state.json` EPIC-03 `test_scenarios` field. As part of ST-10, the `networkidle` call in `earnings-calendar.spec.js` `goto` helper was replaced with `domcontentloaded`.

**Test scenarios to execute:**
- SC-EARN-01: Screener page has "Earnings" column header
- SC-EARN-02: Screener row shows days until earnings when data available
- SC-EARN-03: Screener row shows "—" when earnings data unavailable (null)
- SC-EARN-04: Watchlist page has "Earnings" column header
- SC-EARN-05: Watchlist row shows days until earnings when data available
- SC-EARN-06: Watchlist row shows "—" when earnings data unavailable (null)
- SC-EARN-07: Positions page has "Earnings" column header
- SC-EARN-08: Positions row shows amber warning when earnings ≤5 days away
- SC-EARN-09: Positions row shows plain days (no warning) when earnings >5 days away
- SC-UK-01: UK ticker `BP.L` displayed as `BP` in results table (no .L)
- SC-UK-02: US ticker displayed unchanged
- SC-UK-03: Watchlist promotion popover header shows stripped UK ticker
- SC-UK-04: POST /watchlist body sends stripped ticker (no .L)

**QA findings:**
Playwright test run 2026-05-06 (engine): `npx playwright test tests/e2e/earnings-calendar.spec.js tests/e2e/screener-uk-suffix.spec.js` — **13/13 passed (17.1s)**. SC-EARN-01 to SC-EARN-09 (9 scenarios) and SC-UK-01 to SC-UK-04 (4 scenarios) all pass. `networkidle` replaced with `domcontentloaded` in goto helper (ST-10). No regression detected.

**Disposition:**
Pass

---

## EPIC-03 Consolidation Block

**EPIC:** EPIC-03 — Governance & Process Hardening
**Cycle:** 2026-05-05__release-v3.2
**Sprint goal:** Ship the Pre-Trade Research View (PT-02) and Prospective Heat integration (PT-03) in Sprint 1 and the Pre-Trade Entry Checklist (PT-05) in Sprint 2, completing Arc 2's primary user-value deliverables, while clearing four v3.1 governance deferred actions and five documentation/security backlog items.
**Test scenarios used:** tests/e2e/trade-plan.spec.js (SC-TP-01–07), tests/e2e/earnings-calendar.spec.js (SC-EARN-01–09), tests/e2e/screener-uk-suffix.spec.js (SC-UK-01–04)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-07 | `claude/system/sprint_planning_prompt.md#STEP-0` | Branch safety check hard gate added to STEP 0; v2.5→v2.6; OPERATIONAL_GUIDE §7/§14 updated; prompt_change_log entry added | Branch check present, halts if not main, version bumped, OG updated, change log entry | Pass | None |
| ST-08 | `claude/system/execution_prompt.md#STEP-5.1` | deviations_filed enforcement check added to STEP 5.1; auto-corrects false flag with no deviation; surfaces warning if deviation exists | STEP 5.1 checks flag, auto-corrects, surfaces warning, version bumped, OG updated | Pass | None |
| ST-09 | `claude/system/execution_prompt.md#§3.1.A` | Post-story test files check (step 12) added to §3.1.A; explicit named step | Step 12 present, named, explicit, not embedded | Pass | None |
| ST-10 | `claude/system/execution_prompt.md#§14` | §14 Playwright Test Authoring Standard added; all networkidle occurrences in tests/e2e/ replaced with domcontentloaded or removed | Standard documented, networkidle scanned and replaced, version bumped | Pass | None |
| ST-11 | `tests/e2e/trade-plan.spec.js` | Verified trade-plan.spec.js exists with SC-TP-01–07; backend CRUD tests confirmed; scenarios registered in execution_state.json | All AC verified per QA | Pass | None |
| ST-12 | `tests/e2e/earnings-calendar.spec.js`, `tests/e2e/screener-uk-suffix.spec.js` | Verified both test files exist; all 13 scenarios registered in execution_state.json | Both files runnable; scenarios registered; TEST-GAP-EPIC-03 closed | Pass | None |

**QA test coverage:**
- Scenarios run: SC-TP-01–07, SC-EARN-01–09, SC-UK-01–04 (referenced)
- Regression areas checked: Sprint planning workflow, sprint execution workflow, Playwright test authoring standard
- Known deviations filed: None

**QA sign-off block:**
> **Authoring note (LL-v1.10-P4-1):** When completing the sign-off block, update all AC table rows from "Pending" to "Pass" or "Pass with notes" in the same edit.
> **Date field requirement (LL-v2.3-EX-01):** Date: field must be non-blank before PR can be opened.
- [x] All acceptance criteria verified against canonical spec (ST-07–10: code review; ST-11/12: Playwright 21/21 pass)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (no regression in existing test pass rate)
- [x] ST-07–ST-10: all AC code-review-verifiable; no frontend changes; autonomous class criteria met per BLG-GOV-19
- [x] ST-11: Playwright 8/8 pass (SC-TP-01–07); ST-12: Playwright 13/13 pass (SC-EARN-01–09, SC-UK-01–04)
- Signed off by: Director of Quality
- Date: 2026-05-06
- Comments: ST-11/12 are test registration stories; Playwright evidence is the canonical verification method. All 21 tests pass. ST-07–10 verified by code review per autonomous class eligibility (BLG-GOV-19). Overall EPIC-03 QA verdict: Pass.
