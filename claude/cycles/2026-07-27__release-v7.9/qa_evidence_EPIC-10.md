Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

## Consolidation Block

**EPIC:** EPIC-10 — Pre-commit hook automating the `backend/routers/test.py` registration check
**Cycle:** 2026-07-27__release-v7.9
**Sprint goal:** Ship all 15 v7.9 EPICs — the two P1 UX anchors and the 13 capacity-fill engineering-hardening items — with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_router_test_registration_check.py` (10 unit tests, all passing) + a live end-to-end run against a deliberately-added unregistered route in `backend/routers/news.py` (reverted after confirming block).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-10 | `scripts/check_router_test_registration.py`, `.githooks/pre-commit`, `tests/test_router_test_registration_check.py` | Grep/regex-based checker comparing staged `@router.*` decorators (with router prefix resolved) against `backend/routers/test.py`'s `test_cases` entries, params-aware (`{ticker}` vs `AAPL`-style concrete values). Wired as a native git hook via `.githooks/pre-commit` + `git config core.hooksPath .githooks` (no `pre-commit` framework in this repo to hook into — "or equivalent" per AC-01). | AC-01: Hook added to `.pre-commit-config` (or equivalent) — Pass (`.githooks/pre-commit`, documented setup step). AC-02: Tested against a deliberately-missing case — Pass (unit test + live end-to-end run, both confirm block). AC-03: QA & Testing Owner sign-off — Pass (agent-mediated; found and fixed one real false-positive matching bug during review). | Pass with notes | None |

**QA test coverage:**
- Scenarios run: `backend/.venv/bin/python3 -m pytest tests/test_router_test_registration_check.py -v` — 10/10 passed, including the deliberately-missing-route case and a regression test for the parenthetical-annotation matching bug found during sign-off.
- Regression areas checked: Spot-checked matching logic against real router files (`trade_plans.py`, `portfolio_risk.py`, `watchlist.py`, `analytics.py`) — no false positives on currently-registered routes after the fix.
- Known deviations filed: None — the false-positive matching bug found during review was fixed in this same commit, not deferred.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-10 only, autonomous)
- Criterion 2: All AC verifiable by code review alone — ✓ (unit tests + a live demonstrated block; no UI, no staging run)
- Criterion 3: No frontend-visible change — confirmed no file under `src/pages/**` or `src/components/**` was created or modified — ✓
- Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-27
- Comments: Autonomous class sign-off — all four qualifying criteria met. QA & Testing Owner sign-off (AC-03) obtained separately via agent-mediated review (§5.3): Approved, with one confirmed defect found by direct execution — `TEST_ENTRY_RE`'s matching parsed a human-readable parenthetical annotation (e.g. `"GET /analytics/metrics (all_time)"`) as part of the path, which would have false-positive-blocked a re-staged, already-registered route. Fixed in this same commit (`_clean_entry_path` strips the trailing annotation) with a new regression test (`test_parenthetical_annotation_does_not_break_matching`) verified against the real `backend/routers/test.py` content.
