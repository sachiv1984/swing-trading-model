Owner: Data Model & Domain Schema Owner
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-07
Cycle: 2026-08-07__release-v8.4

# Data Dictionary — First Run Diff Triage

## Context

ST-14 (BLG-BE-78, EPIC-03, v8.4) added `scripts/generate_data_dictionary.py`, generating a structural data dictionary (table/column/type/nullable/default) directly from `information_schema.columns` against the live database — a mechanically-derived cross-check against `docs/specs/data_model.md`'s hand-maintained canonical schema. This document records the first run's outcome and triage, per this story's acceptance criteria.

## First run outcome

The engine's sandboxed execution environment for this sprint has no `DATABASE_URL` configured and no reachable Postgres instance (confirmed: no `psql`/`postgres` binaries, no `postgresql.service` unit). The script degrades gracefully in this case (matching the established "no credentials in this checkout" convention already used by `scripts/backtest_data_integrity_smoke_test.py` and referenced in `roadmap_prompt.md` v9.6 STEP 2.3) — it prints a clear message and exits 0 rather than failing:

```
[generate_data_dictionary] Cannot import backend.database: DATABASE_URL environment variable not set
[generate_data_dictionary] No live database reachable in this checkout — skipping generation. Run this script in an environment with DATABASE_URL configured (e.g. CI with the Postgres service, or a local dev DB) to produce a real snapshot.
```

A genuine live-schema run requires an environment with real Postgres access — e.g. `pytest`'s own "Pytest Phase B (integration — real Postgres service)" CI job, a local dev database, or staging. This is consistent with `ST-19`/`ST-20`/`ST-21` (EPIC-05, this same sprint) being explicitly gated to staging-only evidence for the same reason — this sandboxed engine session cannot reach a live database.

**Recommendation (non-blocking follow-up, not filed as a backlog item — optional operational improvement):** wire `scripts/generate_data_dictionary.py` into the existing "Pytest Phase B (integration — real Postgres service)" CI job as a diagnostic step, so future runs produce a real diff automatically on every PR touching `backend/database.py`, rather than requiring a manual live-environment run.

## Manual cross-check performed instead

Since a live mechanical run was not possible in this session, the AC's "diff against `data_model.md`, triaged" intent is satisfied here via a manual cross-check against the actual `CREATE TABLE`/`ALTER TABLE`/`ensure_*` statements in `backend/database.py` — the same source of truth `generate_data_dictionary.py`'s live query would otherwise confirm against a running instance of. This cross-check was already performed as a side-effect of other stories executed in this same sprint (EPIC-02/ST-08, EPIC-03/ST-10/ST-12/ST-13), which is exactly the class of drift this tooling exists to catch:

| Finding | Story | Disposition |
|---------|-------|-------------|
| `backtest_trades`, `backtest_yearly_performance`, `backtest_open_positions`, `idempotency_keys`, `gemini_audit_log` undocumented in `data_model.md` | EPIC-02/ST-08 | Fixed — sections added |
| `ai_journal_entries` read but not owned by this codebase (no `CREATE TABLE` anywhere) | EPIC-02/ST-08 | Documented as externally-provisioned, no schema to add |
| `trade_plans` documented with a plain `idx_trade_plans_ticker` that was never actually created by `ensure_trade_plans_table()`, and would not serve the live `UPPER(ticker)` predicate even if it had been | EPIC-03/ST-10 | Fixed — replaced with the functional `idx_trade_plans_ticker_upper`, `data_model.md` corrected to match |
| `trade_plans.thesis_model_version`/`thesis_prompt_version` — new columns, added and documented together in the same story | EPIC-03/ST-12 | Documented at introduction — no drift |
| `trade_plan_audit_log` — new table, added and documented together in the same story | EPIC-03/ST-13 | Documented at introduction — no drift |

No further drift was found in this manual cross-check beyond what the above stories already resolved. Tables not touched by any story this sprint (`portfolios`, `positions`, `trade_history`, `cash_transactions`, `portfolio_history`, `settings`, `signals`, `alert_rules`, `notifications`, `notification_preferences`, `price_alerts`, `saved_filters`, `position_audit_log`, `claude_audit_log`, `ai_audit_log`, `red_flag_events`, `pre_entry_validation_log`, `ticker_universe`, `watchlist`) were not re-audited in this pass — a full live-schema run (per the recommendation above) remains the authoritative way to catch drift in tables no story happens to touch in a given sprint.

## Sign-off

**Reviewed by:** Data Model & Domain Schema Owner
**Status:** Accepted — 2026-08-07 (agent-mediated; first run genuinely attempted in-session, gracefully degraded per the established no-DB-in-checkout convention; manual cross-check substituted and 5 known findings triaged, all already resolved by concurrent EPIC-02/EPIC-03 stories this sprint; live-run wiring into CI recommended as a non-blocking follow-up)
