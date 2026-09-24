Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-24

# QA Evidence — EPIC-04 (QA & Test Coverage) — 2026-09-23__release-v9.7

**EPIC:** EPIC-04 — QA & Test Coverage
**Cycle:** 2026-09-23__release-v9.7
**Sprint goal:** Ship PO-05 Lightweight Replay Mode end-to-end and clear the full-capacity, category-balanced debt-clearance slice across Frontend/UX correctness, Backend financial reliability, QA coverage, Governance process debt, Spec/data-model debt, and Ops/security verification — 29 stories, 28.00 days.
**Test scenarios used:** `tests/test_conftest_database_url_guard.py`, `tests/test_playwright_skip_only_check.py`, `tests/test_negative_path_v92_v93_routers.py`, `tests/test_claude_endpoint_cost_windows_live.py`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-14 | N/A — `spec_reference_not_applicable: true` (test-isolation bug fix, no prior canonical spec) | `tests/conftest.py` now forces `DATABASE_URL` to a stub outside CI's opt-in, guarded by `tests/test_conftest_database_url_guard.py`; also fixed 2 pre-existing tests that were silently relying on the leaky behaviour | Running the suite with a real-looking `DATABASE_URL` and no opt-in makes zero real connections; Phase B CI still runs `tests/test_schema.py` against real Postgres with the opt-in set | Pass | None |
| ST-15 | `.github/workflows/playwright-skip-only-check.yml` | New CI check that fails when a merged Playwright spec contains `.skip()`/`.only()`; `tests/test_playwright_skip_only_check.py` fires on a deliberately-introduced test case | CI check added and fires on a deliberately-introduced test case; exception mechanism documented | Pass | None |
| ST-16 | `docs/ops/endpoint_test_coverage_audit_2026-09-24.md` | Documented recurring pre-sprint endpoint-coverage audit method; first run completed this cycle | Audit method documented; first run completed, gaps filed as their own items | Pass | None |
| ST-17 | `tests/test_negative_path_v92_v93_routers.py` | Negative-path tests backfilled for the 3 newest v9.2/v9.3 routers | 3 routers identified; negative-path tests added and passing for each | Pass | None |
| ST-18 | `backend/database.py#get_claude_endpoint_cost_windows` | `tests/test_claude_endpoint_cost_windows_live.py` — a real-Postgres Phase B test executing the actual, non-stubbed `get_claude_endpoint_cost_windows()` against a local Postgres 18 instance, asserting recent/baseline window boundary correctness including the outside-both-windows exclusion case | The query has been run against a real Postgres instance with confirmed-correct recent/baseline window boundaries, via a new test that executes the real (non-stubbed) function and asserts its output shape/values | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_conftest_database_url_guard.py`, `tests/test_playwright_skip_only_check.py`, `tests/test_negative_path_v92_v93_routers.py`, `tests/test_claude_endpoint_cost_windows_live.py` (2 tests, run against a real local Postgres 18 instance — `DATABASE_URL=postgresql://ci:ci@localhost:5432/ci_test`, the same DB CI's own `pytest-phase-b` job uses; confirmed both pass, confirmed the file skips cleanly under Phase A/stub `DATABASE_URL`)
- Regression areas checked: full backend suite re-run under Phase A/stub `DATABASE_URL` — 1715 passed, 12 skipped, 0 failed (no regressions from ST-14's conftest change or the new ST-18 test file)
- Known deviations: None found — all stories' deviation checks completed with nothing to file

**ST-18 delegation note:** originally classified `delegated_backend` (`DEL-20260924-01`, routed to Data Model & Domain Schema Owner / Infrastructure & Operations Owner) on the assumption that only a live/synthetic Postgres connection could satisfy the AC and this sandbox had no safe `DATABASE_URL` for it. On investigation, a local Postgres 18 instance was already running in this sandbox (unrelated to the staging Supabase `DATABASE_URL`) — the same one CI's own `pytest-phase-b` job targets. Reclassified `autonomous` once the real test was built and confirmed passing against it; no human action was ultimately needed. See `delegation_log.md` `DEL-20260924-01` (Status: Unblocked) for full detail.

**Autonomous-class eligibility note (BLG-GOV-19):** not applied for this EPIC, on a conservative reading. ST-18's verification connects to a real running Postgres server via `psycopg2` — literal "live system interaction" under Criterion 2, even though the instance is an ephemeral local test database (not staging/production, no application data). Per the `execution_prompt.md` §3.2.A live-interaction-bar precedent (BLG-GOV-335): "where it cannot tell, treat Criterion 1 as unmet" — the engine may not resolve a borderline eligibility call in its own favour. Using the Standard Sign-Off Block below instead.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend component in this EPIC
- Signed off by: Director of Quality
- Date:
- Comments: Pending human Director of Quality review — see Autonomous-class eligibility note above for why this EPIC did not take the autonomous-class path despite all 5 stories being `autonomous`-classified.
