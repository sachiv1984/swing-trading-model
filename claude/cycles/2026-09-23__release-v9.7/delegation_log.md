Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-24 (DEL-20260924-01 -> Unblocked)

# Delegation Log — 2026-09-23__release-v9.7

## DEL-20260924-01

- **ST Item:** ST-18 — Validate `get_claude_endpoint_cost_windows()` SQL against a real Postgres instance
- **EPIC:** EPIC-04
- **Classification:** delegated_backend
- **Assigned to:** Data Model & Domain Schema Owner / Infrastructure & Operations Owner
- **GitHub Issue:** #1780
- **Branch:** exec/2026-09-23__release-v9.7/EPIC-04
- **Delegated at:** 2026-09-24T07:46:16Z
- **What is needed:** `backend/database.py::get_claude_endpoint_cost_windows()` uses `FILTER` clauses and `(param || ' hours')::interval`/`(param || ' days')::interval` string-concatenation arithmetic — no test in the repo executes this SQL against a real Postgres server (every test path goes through `tests/conftest.py`'s session-scoped `database`-module stub, or a private isolated import that never actually runs the query). Two acceptable routes, either satisfies the AC: (a) run the query manually against a real or synthetic Postgres instance and confirm the recent/baseline window boundaries and `FILTER` aggregates behave as documented; or (b) add a synthetic-DB test (e.g. a local Postgres/sqlite-compatible fixture, following the pattern used for `tests/test_positions_open_ticker_entry_date_unique_migration.py`) that actually executes the real (non-stubbed) function. This sandbox has no safe `DATABASE_URL` to use for either route — the only configured `DATABASE_URL` is a real STAGING Supabase instance, which per this session's own operating constraints must not be queried without explicit human approval (and ST-14/BLG-QA-188, this same EPIC, now actively forces that URL to a stub outside CI/opt-in — see `tests/conftest.py`).
- **Spec reference:** `backend/database.py#get_claude_endpoint_cost_windows`
- **Unblock criteria:** Either (a) a human runs the query against a real/synthetic Postgres instance and shares the confirmed recent/baseline window boundary output back into this cycle (to be recorded in `qa_evidence_EPIC-04.md`), or (b) a synthetic-DB test is added and passes in CI.
- **Commit format required:** `[EPIC-04][ST-18] <description>` pushed to `exec/2026-09-23__release-v9.7/EPIC-04`
- **Status:** Unblocked — route (b) taken. A real-Postgres Phase B test (`tests/test_claude_endpoint_cost_windows_live.py`) was added that executes the actual non-stubbed `get_claude_endpoint_cost_windows()` against a local Postgres 18 instance already running in this sandbox (`localhost:5432/ci_test` — the same DB CI's own `pytest-phase-b` job uses; NOT the staging Supabase `DATABASE_URL`), asserting recent/baseline window boundary correctness including the outside-both-windows exclusion case. The original framing of route (b) as a "sqlite-compatible fixture" was superseded on investigation — SQLite cannot execute this query's Postgres-only `FILTER`/`::interval` syntax at all, so a real local Postgres was used instead. Confirmed passing (`DATABASE_URL=postgresql://ci:ci@localhost:5432/ci_test backend/.venv/bin/python3 -m pytest tests/test_claude_endpoint_cost_windows_live.py -v` → 2 passed), confirmed it skips cleanly under Phase A/stub `DATABASE_URL`, and confirmed no regressions in the full suite (1715 passed, 12 skipped). No human action was needed after all. Commit SHA: `41e79e7729d20159cdba8dbb7165f0e761bcc74d` (test file landed in a `[GOVERNANCE]` conflict-resolution merge commit as an untracked file swept in alongside it — disclosed here rather than re-committed separately). Unblocked 2026-09-24T09:33:05Z.
