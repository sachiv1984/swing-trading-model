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

## DEL-20260924-02

- **ST Item:** ST-27 — Post-deploy staging verification of the reflection-reminder migration and SQL (never run against a live database)
- **EPIC:** EPIC-07
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner; Product Owner
- **GitHub Issue:** #1789
- **Branch:** exec/2026-09-23__release-v9.7/EPIC-07
- **Delegated at:** 2026-09-24T08:05:53Z
- **What is needed:** The reflection-reminder work (`BLG-FEAT-98`, shipped v9.6) added startup DDL (two `alert_type` CHECK extensions and a partial unique index `uq_notifications_reflection_reminder_trade`) and an evaluation query using `ON CONFLICT ((context->>'trade_id')) WHERE ...` — covered only by structural mocked-cursor tests, never executed against real PostgreSQL. Per the item's own explicit note: "Requires a real (non-mocked) DB/SQL run — route to Infrastructure & Operations Owner for a delegated staging slot; code review alone does not satisfy this AC." This session has no safe `DATABASE_URL` for a real staging run (per this session's own operating constraint: the only configured `DATABASE_URL` points at real STAGING Supabase and must not be queried without explicit human approval — not obtained this session). Needed: (1) run the verification queries in `data_model.md` DS-19 against staging and confirm both CHECK constraints and the partial unique index are present; (2) run `POST /alerts/evaluate` twice and confirm the second run creates 0 duplicate reflection-reminder rows; (3) Product Owner to confirm or change the 30-day look-back (`REFLECTION_REMINDER_LOOKBACK_DAYS`) and the `trade_history.created_at` close-timestamp choice.
- **Spec reference:** `docs/specs/data_model.md` DS-19; `docs/specs/api_contracts/alerts_endpoints.md` (reflection_reminder)
- **Unblock criteria:** All 3 items above completed and evidence recorded in `qa_evidence_EPIC-07.md`.
- **Commit format required:** `[EPIC-07][ST-27] <description>` pushed to `exec/2026-09-23__release-v9.7/EPIC-07`
- **Status:** Pending
