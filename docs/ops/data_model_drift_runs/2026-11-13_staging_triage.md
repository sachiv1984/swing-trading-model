**Owner:** QA & Testing Owner; Data Model & Domain Schema Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-13 (created, ST-20, EPIC-07, v9.17, BLG-QA-223)
**Source:** ST-20 (BLG-QA-223, EPIC-07, v9.17 sprint execution)

# Drift Detector Triage — Staging, 2026-11-13

## Run

- **Output:** [`2026-11-13_staging.json`](2026-11-13_staging.json), saved unchanged from the run
- **Command:** `PGOPTIONS="-c default_transaction_read_only=on" python3 scripts/check_data_model_drift.py docs/specs/data_model.md --json`, exit 0
- **Detector revision:** branch `exec/2026-11-11__release-v9.17/EPIC-07` at `02587c70`, which includes the ST-20 rollback-block exclusion (`f1299c5c`)
- **`data_model.md` revision:** v2.69, on `main` after EPIC-04's DS-40 migration (PR #2257)
- **Database:** staging, read-only session. Run by the execution session with the user's permission, 2026-11-13. No other query was run.
- **Purpose:** confirm BLG-QA-223 AC 1 and run the post-EPIC-04 check that the v9.17 sprint plan asks for (ST-20 notes)

## Findings

| Finding | Disposition |
|---------|-------------|
| `idx_trade_plans_ticker` | **Not reported.** BLG-QA-223 AC 1 is met. The name appears only in the v2.21 → v2.22 `Reversible:` block, which the detector now skips. |
| `IF` (missing index) | **Detector false positive, fixed in the same story.** It comes from the prose "`CREATE INDEX IF NOT EXISTS`)" in `data_model.md` DS-36's Deploy order note, where the backtick after `EXISTS` stopped the optional `IF NOT EXISTS` group matching. `INDEX_RE` now refuses `IF` as a name. Test: `test_prose_create_index_if_not_exists_does_not_yield_if`. |
| `idx_portfolio_history_portfolio`, `idx_trade_reflections_trade`, `settings_risk_percent_check` | **Known.** The same dispositions as `data_model.md` §Drift Detector Triage (2026-10-13): documentation fixes. Still reported, so the documented names are unchanged. |
| `idx_position_audit_log_position_id`, `idx_sector_regime_history_portfolio_date`, `idx_trade_plan_audit_log_trade_plan_id` | **Known pattern.** These tables are created lazily, so they do not exist on staging (same triage). |
| `idx_momentum_signal_runs_portfolio_date` | **New since 2026-10-13, not confirmed this run.** DS-39 (v2.68) creates `momentum_signal_runs` and this index in an ensure-function on first use (`backend/database.py`), the same lazy pattern as the audit-log tables. The run cannot tell whether the table exists on staging, because the detector skips tables that are absent. Confirming it needs one catalog query (`information_schema.tables` for `momentum_signal_runs`). |
| Tables (columns, nullability, defaults) | **None reported.** |
| DS-40 (`positions.stop_last_moved_date`, `previous_stop`, EPIC-04) | **No drift.** Neither column is reported, so both are documented and match on staging. |
