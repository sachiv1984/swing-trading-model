**Owner:** Backend Engineering Patterns Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-30 (ST-21, EPIC-03, v9.14, BLG-BE-166 — first listing; 34 call sites: 28 fixed, 3 already once per process, 3 filed)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# ensure_* DDL Before Writes: Call-Site Listing

## Why this listing exists

Many write paths call an `ensure_*` function before they write. These functions run `CREATE TABLE ... IF NOT EXISTS` or `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`. Each call opens a connection, and each `ALTER TABLE` takes an ACCESS EXCLUSIVE lock even when it changes nothing. `create_claude_audit_entry()` ran four of them before every AI call's audit row (BLG-BE-166).

ST-21 adds `database.ensure_once`, a decorator that records a function's first successful run in the process and skips later calls. A failed run is not recorded, so the next call tries again. Startup (`main.py` `on_startup`) goes through the same wrapper, so a startup run also covers the first write. `database.reset_ensure_once()` clears the record for tests.

**Trade-off:** if a table is dropped while the process runs (for example a staging reset), the decorated function will not recreate it until the process restarts. Writes to that table then fail as they would for any missing table; audit writes stay non-blocking.

## How the listing was produced

An AST scan of `backend/` (excluding `.venv`) for every function, other than an `ensure_*` function itself and `on_startup`, that calls an `ensure_*` function and also writes (an `INSERT` in its source, or a `create_`/`insert_`/`log_`/`record_`/`upsert_`/`save_`/`add_` call). It found **34 call sites** (one per calling function and `ensure_*` function pair) in 28 functions. Rows below group sites that share an `ensure_*` function or a caller. `get_monthly_pnl_report` is a read path, but it calls the same `ensure_*` as a write path, so it is listed.

## Call sites

| # | Call site | ensure_* called | Outcome |
|---|-----------|-----------------|---------|
| 1 | `database.create_claude_audit_entry` | `ensure_claude_audit_log_table` | Fixed (`ensure_once`) |
| 2 | `database.create_claude_audit_entry` | `ensure_claude_audit_log_compliance_check_column` | Fixed (`ensure_once`) |
| 3 | `database.create_claude_audit_entry` | `ensure_claude_audit_log_latency_column` | Fixed (`ensure_once`) |
| 4 | `database.create_claude_audit_entry` | `ensure_claude_audit_log_prompt_hash_columns` | Fixed (`ensure_once`) |
| 5 | `database.create_gemini_audit_entry` | `ensure_gemini_audit_log_table` | Fixed (`ensure_once`) |
| 6 | `database.create_ai_output_boundary_sample` | `ensure_ai_output_boundary_samples_table` | Fixed (`ensure_once`) |
| 7 | `database.log_api_call` | `ensure_api_call_log_table` | Already once per process (`_api_call_log_ready`, v9.13 ST-31) |
| 8 | `database.log_api_calls` | `ensure_api_call_log_table` | Already once per process (`_api_call_log_ready`, v9.13 ST-31) |
| 9 | `database.create_trade_debrief` | `ensure_trade_debriefs_table` | Fixed (`ensure_once`) |
| 10 | `database.upsert_monthly_pnl_narrative` | `ensure_monthly_pnl_narratives_table` | Fixed (`ensure_once`) |
| 11 | `database.upsert_last_good_fx_rate` | `ensure_fx_rate_last_good_table` | Fixed (`ensure_once`) |
| 12 | `database.create_chat_answer_rating` | `ensure_chat_answer_ratings_table` | Fixed (`ensure_once`) |
| 13 | `database.create_position_audit_log_entry` | `ensure_position_audit_log_table` | Fixed (`ensure_once`) |
| 14 | `database.create_position_state_history_entry` | `ensure_position_state_history_table` | Fixed (`ensure_once`) |
| 15 | `database.create_trade_plan_audit_log_entry` | `ensure_trade_plan_audit_log_table` | Fixed (`ensure_once`) |
| 16 | `database.log_pre_entry_validation_results` | `ensure_pre_entry_validation_log_table` | Fixed (`ensure_once`) |
| 17 | `database.log_trailing_stop_recommendation` | `ensure_trailing_stop_recommendation_log_table` | Fixed (`ensure_once`) |
| 18 | `database.create_sector_regime_snapshot` | `ensure_sector_regime_history_table` | Fixed (`ensure_once`) |
| 19 | `database.create_backtest_rule_run` | `ensure_backtest_rule_run_tables` | Fixed (`ensure_once`) |
| 20 | `routers/trade_plans._maybe_write_override_event`, `_maybe_write_checklist_skipped_event` | `ensure_red_flag_events_table` | Fixed (`ensure_once`) |
| 21 | `routers/trade_plans.create_plan` | `ensure_trade_plans_table` | Already once per process (`_trade_plans_table_ensured`) |
| 22 | `routers/trade_plans.create_plan` | `ensure_si02_trade_plans_columns`, `ensure_strategy_version_at_entry_columns`, `ensure_triggered_by_price_alert_id_column` | Fixed (`ensure_once`) |
| 23 | `services/ai_endpoint_anomaly_service._send_anomaly_telegram_alert_deduped`, `_clear_anomaly_alert_fingerprint` | `ensure_scheduled_alert_dedup_table` | Fixed (`ensure_once`) |
| 24 | `services/gemini_service.check_and_alert_daily_cost`, `_alert` | `ensure_scheduled_alert_dedup_table` | Fixed (`ensure_once`) |
| 25 | `services/position_service.exit_position` | `ensure_planned_entry_price_column` | Fixed (`ensure_once`) |
| 26 | `utils/idempotency.replay_or_create` | `ensure_idempotency_keys_table` | Fixed (`ensure_once`) |
| 27 | `database.insert_monthly_pnl_snapshot_if_absent`, `services/reports_service.get_monthly_pnl_report` | `ensure_monthly_pnl_snapshots_table(conn)` | Filed (BLG-BE-200): runs in the caller's connection and transaction, so recording success when the function returns could record a DDL that later rolls back |
| 28 | `services/alerts_service.evaluate_alerts` | `ensure_alerts_tables` (defined in `alerts_service`, not `database`) | Filed (BLG-BE-200): a scheduled job, not a per-request path; `ensure_once` lives in `database`, which tests replace with a stub at import |

**Count:** 34 call sites. 28 fixed by `ensure_once` (rows 1–6, 9–20, 22–26); 3 already ran once per process (rows 7, 8, 21); 3 filed as BLG-BE-200 (row 27's two sites and row 28).

## Verification

- `tests/test_claude_audit_ensure_once.py`: a second audit insert in the same process runs no DDL; the first insert still adds the missing columns; a failed ensure is retried on the next insert.
- Full backend suite passes (`backend/.venv/bin/python3 -m pytest tests`).
