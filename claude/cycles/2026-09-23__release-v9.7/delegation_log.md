Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-24 (DEL-20260924-03 created for ST-01b, Pending; prior — DEL-20260924-01 and DEL-20260924-02 -> Unblocked)

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
- **Status:** Unblocked — completed in-session with a human running the staging steps, 2026-09-24 (same session as delegation; distinct from a cross-session delegation). Items (1)-(2) were run by the operator against STAGING only (Supabase SQL Editor for the queries; `POST https://trading-assistant-api-staging.onrender.com/alerts/evaluate` for the evaluations). (1) First run found staging still on pre-v9.6 code: both `alert_type` CHECK constraints lacked `reflection_reminder` (a stale staging deploy, not a code defect -- `ensure_alerts_tables()` only applies DS-19 when a v9.6 backend boots). After the operator redeployed staging, both constraints list `reflection_reminder` and `uq_notifications_reflection_reminder_trade` exists with the DS-19 definition (partial unique index on `context->>'trade_id'` WHERE `alert_type = 'reflection_reminder'`). (2) Two `POST /alerts/evaluate` runs: the first reported `reflection_reminders` candidates 14 / notifications_created 14 / error null; row count 0 -> 14; the second reported candidates 0 / notifications_created 0 / error null; row count stayed 14; the duplicate-per-`trade_id` query returned no rows. An earlier attempt created 0 rows because the 14 seeded trades had not yet crossed the 48h mark when it ran -- not a defect. (3) Product Owner decision (human, 2026-09-24): keep `REFLECTION_REMINDER_LOOKBACK_DAYS = 30` and keep `trade_history.created_at` (falling back to `exit_date`) as the close timestamp -- no change. Evidence recorded in `qa_evidence_EPIC-07.md`. Commit SHA: `62ac42e03b57e545603ac92921f68e3f5a175a49` (evidence commit; recorded here per the two-phase delegation write rule). No credential is recorded in this repo.

## DEL-20260924-03

- **ST Item:** ST-01b — PO-05: Backend replay mechanics
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #1792
- **Branch:** exec/2026-09-23__release-v9.7/EPIC-01
- **Delegated at:** 2026-09-24T17:30:59Z
- **What is needed:** Build the replay backend exactly as locked in `docs/product/decisions/po05_replay_scope_confirmation.md` (rev 3) §2 (D1–D6) and §5: `POST /replay/run` (router → service → database), a deterministic per-trade exit simulation built on `backend/services/strategy_engine.py` (no Alpaca call, no persistence, no write path); the F3 extraction of the per-position stop / initial-stop / `is_risk_on` logic into shared functions with a pre-refactor golden-file regression test proving `backtest()` output is unchanged; manual request-body parsing so every rejection returns the 400 error envelope; the contract `docs/specs/api_contracts/replay_endpoints.md` (`## POST /replay/run`), `docs/reference/openapi.yaml`, `api_changelog.md`, `Specs_Index.md`, `docs/ops/api_performance_baseline.md`, `backend/routers/test.py` registration (body `{"trade_ids": ["00000000-0000-0000-0000-000000000000"]}`), `SystemStatus.js` count and `SC-SS-01b`, all in the same commit set; the test list in §5; and a recorded synchronous run time at the bounds (100 trades / 25 tickers).
- **Spec reference:** `docs/product/decisions/po05_replay_scope_confirmation.md` (locked wire contract); `docs/product/decisions/po05_section13_preassessment.md` (six binding conditions, traced in scope note §3); `docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md`
- **Unblock criteria:** Commit(s) `[EPIC-01][ST-01]` pushed to `exec/2026-09-23__release-v9.7/EPIC-01` (the commit-message hook accepts numeric story tags only, so ST-01a/b/c all use `[ST-01]`) satisfying the scope note's §5 backend list, with `qa_evidence_EPIC-01.md` updated.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-09-23__release-v9.7/EPIC-01`
- **Start gate:** **do not start before the Product Owner's merge of the PR carrying the scope note** (scope note §6) — a different scope decision would waste this story's effort. The frontend story ST-01c depends on this one.
- **Status:** Cancelled — reclassified to `autonomous` 2026-09-25. The Product Owner start gate (a decision on scope note §7 item 1) was cleared by the user's direct, explicit instruction in-session ("carry on with ST-01b and c") rather than by a PR merge; the engine builds ST-01b and ST-01c itself rather than delegating to a human Head of Engineering. Cross-reference: execution_state.json epics.EPIC-01.stories.ST-01b/ST-01c.
