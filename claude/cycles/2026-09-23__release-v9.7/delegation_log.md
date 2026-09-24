Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-24

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
- **Status:** Pending
