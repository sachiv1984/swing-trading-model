**Owner:** Backend Engineering Patterns Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-21__release-v7.7
**Story:** ST-09 (EPIC-09)
**Backlog source:** BLG-GOV (nightly backtest job surface, sole owner alongside EPIC-10 per sprint_planning_notes.md Shared File Ownership Advisory)

---

# Nightly Backtest Job — Idempotency / Double-Run Audit

## Scope

Verify whether the nightly backtest job (`.github/workflows/backtest.yml`, `production_strategy.py`, `import_backtest.py`, and the backend write path `upsert_backtest_data` in `backend/database.py`) is safe against double-run/retry — i.e. a manual re-trigger while a scheduled run is still executing, a retry after a mid-run failure, or two overlapping invocations, must not produce duplicated or divergent results.

## Pipeline Overview

1. **`production_strategy.py`** (compute step) — reads `ticker_universe` from the DB (`SELECT` only, no writes) and pulls historical price data from `yfinance`, recomputes the entire backtest trade history from scratch, writes timestamped CSVs to the ephemeral CI runner's local `production_results/` directory.
2. **`import_backtest.py`** (import step) — parses the latest CSVs and `POST`s the full parsed dataset to `POST /strategy/benchmark/import`.
3. **`upsert_backtest_data`** (`backend/database.py`) — the only DB write in the pipeline. Deletes all rows from `backtest_trades`, `backtest_yearly_performance`, and `backtest_open_positions`, then re-inserts the freshly-computed full dataset, all inside a single transaction (commit only on success; rollback on any exception, per `get_db()`'s context manager).

## Findings

### 1. Compute step is read-only and side-effect-free
`production_strategy.py`'s only DB interaction (`_load_tickers()`) is a `SELECT` against `ticker_universe`. All other data comes from `yfinance` (external, read-only) and is written only to local CSV files in the CI runner's own ephemeral filesystem — discarded when the job ends. Re-running this step any number of times, concurrently or sequentially, has zero risk of corrupting shared state: each run independently recomputes its own CSVs from the same deterministic inputs (modulo any intervening `yfinance` data revision, which is an accepted, pre-existing characteristic of the pipeline — see `import_backtest.py`'s `check_drift_alert` / BLG-BE-60, not a double-run concern).

### 2. Import step's only failure mode is a clean non-zero exit
`import_backtest.py`'s `main()` calls `sys.exit(1)` on a non-200 response (line 255) and lets any `requests` exception (timeout, connection error) propagate uncaught, which also exits non-zero. There is no partial-write path client-side — either the single `POST` succeeds and the server has fully committed the new snapshot, or it fails and nothing client-side is left in an inconsistent state (there is nothing to leave inconsistent; the script holds no state across the single call).

### 3. The write path is atomic and safe against retry
`upsert_backtest_data`'s `DELETE` + re-`INSERT` sequence for all three tables executes inside one `get_db()` transaction. Per `get_db()`'s own implementation (`backend/database.py` lines 28–39): the transaction commits only if the `with` block completes without exception, and rolls back entirely on any exception. A retry (whether from a CI re-run or a manual `workflow_dispatch`) after a failed prior attempt simply re-executes the full replace against whatever the current (unchanged, since the failed attempt rolled back) DB state is — no duplicate rows, no partial application, no divergence. The `ON CONFLICT` clauses on the `INSERT`s are redundant with the immediately-preceding `DELETE` within the same transaction (belt-and-braces, not load-bearing for idempotency) but are not harmful.

### 4. Concurrent overlapping runs are safe, and now additionally guarded at the CI level
Two genuinely concurrent invocations (e.g. the scheduled cron fires while a manual `workflow_dispatch` re-run from an earlier failure is still executing) would each independently compute their own CSVs (no shared-state conflict per Finding 1) and then each call `upsert_backtest_data`. Postgres's row-level locking on `DELETE` serializes the two transactions: whichever commits first is briefly visible, then the second transaction's `DELETE`+`INSERT` proceeds and its snapshot becomes the final, authoritative state. This "most recent computation wins" outcome is exactly the intended full-replace semantics — not a correctness bug. As defense-in-depth (avoiding two ~90-minute compute runs racing for no benefit, not because the DB layer was unsafe), a `concurrency: {group: nightly-backtest, cancel-in-progress: false}` block was added to `backtest.yml` in this same story — overlapping runs now queue rather than execute in parallel.

### 5. `backtest_import_history` (audit trail) — minor, non-business-critical note
The pre-replace snapshot inserted into `backtest_import_history` uses `ON CONFLICT (imported_at) DO NOTHING`, keyed by the *previous* run's `imported_at` timestamp. In an extremely tight concurrent-run race (now precluded by the CI concurrency guard above), it is theoretically possible for this audit-trail insert to be skipped for one of the two runs if both observed the same "previous" state before either committed. This would not affect the live `backtest_trades`/`backtest_yearly_performance`/`backtest_open_positions` tables (Finding 4 already establishes those resolve correctly) — only a historical audit-log row could be affected, and only in a race window the CI concurrency guard now eliminates in practice. Not filed as a backlog item — the guard added in this story already closes the practical exposure, and the audit table is non-authoritative reference data, not livedata.

## Determination

**No correctness gap found.** The nightly backtest job's write path was already idempotent and retry-safe by design (atomic full-replace transaction, no incremental/append writes that could duplicate). One defense-in-depth hardening was applied in this story: a `concurrency` group on `backtest.yml` to queue rather than run overlapping invocations, eliminating even the theoretical need to reason about concurrent-transaction serialization in production. A compliance-note comment was added to `upsert_backtest_data` in `backend/database.py` referencing this audit, per the pattern established at SI-02's §13 review (binding condition 7).

No P1/P2 correctness backlog item filed — the audit found the design already safe, and the one hardening applied (concurrency guard) was made directly rather than deferred.

## Sign-Off

**Signed off by:** Backend Engineering Patterns Owner (agent-mediated, §5.3)
**Date:** 2026-07-24
**Determination:** Audit complete — no gap found; one defense-in-depth hardening applied (backtest.yml concurrency group).
