**Owner:** Backend Engineering Patterns Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-20
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Nightly Batch Job Idempotency Audit

**Added:** ST-06 (EPIC-06, v7.6, BLG-BE-62)

## 1. Purpose

Audits whether the project's scheduled nightly batch jobs are idempotent — does re-running a job against identical input state produce identical output, or does it silently accumulate drift (duplicate rows, compounding state changes)? This is the same class of defect confirmed and fixed in `BLG-BE-59` (retroactive ticker-universe eligibility corrupting historical backtest rankings) and `BLG-BE-60` (`total_pnl_gbp` non-reproducible night-to-night with zero exits), both shipped v7.1. This audit checks whether the same defect class exists elsewhere in the project's remaining scheduled jobs.

## 2. Scope

Per this item's acceptance criteria, four jobs were audited:

1. `.github/workflows/daily-snapshot.yml` — Job 1: `GET /positions/analyze`
2. `.github/workflows/daily-snapshot.yml` — Job 2: `POST /portfolio/snapshot`
3. `.github/workflows/daily-snapshot.yml` — Job 3: `POST /signals/generate`
4. `.github/workflows/backtest.yml` — the nightly backtest import step (`import_backtest.py` → `POST /strategy/benchmark/import`)

## 3. Method

For each job, the audit traced the handler from the workflow trigger down to its actual database write statement(s) — not inferred from docstrings or comments alone (a docstring claiming "idempotent" was verified against the actual SQL in every case below, per `LL-v3.7-EX-03`-class discipline: code inference is insufficient without direct confirmation of the underlying operation).

## 4. Findings

### 4.1 `GET /positions/analyze` (`backend/services/position_service.py::analyze_positions`)

**Verdict: Idempotent.**

The only database write in this function is `update_position(str(pos['id']), {...})` — an `UPDATE` keyed on the position's own primary key, not an `INSERT`. Re-running with the same live price input overwrites the same row with the same values; re-running with a different live price (the normal case, since price is fetched fresh on every call) produces a different but still single, non-accumulating row state.

Critically, an `"action": "EXIT"` in this endpoint's response is **advisory only** — it does not close the position, write a `trade_history` row, or mutate `positions.status`. Per `strategy_rules.md §13` ("human-in-the-loop by design"), exit execution is always a separate, user-initiated action (`TradeEntry.js` / the exit flow). This means repeated runs of `/positions/analyze` carry zero risk of duplicate closures or duplicate `trade_history` rows — there is no closure write path in this function at all.

### 4.2 `POST /portfolio/snapshot` (`backend/services/portfolio_service.py::create_daily_snapshot` → `backend/database.py::create_portfolio_snapshot`)

**Verdict: Idempotent — confirmed via SQL, not docstring.**

```sql
INSERT INTO portfolio_history (portfolio_id, snapshot_date, total_value, cash_balance,
                                positions_value, total_pnl, position_count)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (portfolio_id, snapshot_date)
DO UPDATE SET total_value = EXCLUDED.total_value, ...
```

The `ON CONFLICT (portfolio_id, snapshot_date) DO UPDATE` clause means any number of runs on the same day converge on one row per `(portfolio_id, snapshot_date)`. The docstring's "Uses UPSERT logic" claim is accurate and verified.

### 4.3 `POST /signals/generate` (`backend/services/signal_service.py::generate_momentum_signals` → `backend/database.py::create_signal`)

**Verdict: Idempotent — confirmed via SQL.**

```sql
INSERT INTO signals (portfolio_id, ticker, market, signal_date, rank, ...)
VALUES (...)
ON CONFLICT (portfolio_id, ticker, signal_date)
DO UPDATE SET rank = EXCLUDED.rank, ...
```

Same pattern as §4.2 — `ON CONFLICT (portfolio_id, ticker, signal_date) DO UPDATE` means re-running on the same day for the same ticker converges on one row, not a duplicate.

### 4.4 Nightly backtest import (`import_backtest.py` → `POST /strategy/benchmark/import` → `backend/database.py::upsert_backtest_data`)

**Verdict: Idempotent by design — and the fix vehicle for a previously-confirmed instance of this exact defect class.**

`upsert_backtest_data`'s own docstring (verified against its actual `DELETE` + `INSERT` sequence, executed inside a single transaction that rolls back on failure) documents that this was itself a deliberate fix: "The previous upsert-only approach had no way to remove rows that stopped being generated, which is exactly how 5 fictional trades from a fixed phantom-date bug stayed in the table." `production_strategy.py` recomputes the full trade history from scratch on every run, so a full delete-then-reinsert of `backtest_trades`, `backtest_yearly_performance`, and `backtest_open_positions` (the last per `BLG-FEAT-54` AC-03) is the correct idempotent pattern here — an incremental-append approach would be the actual bug, not the fix.

This job is also where `BLG-BE-59` and `BLG-BE-60` were fixed (v7.1): `BLG-BE-59` gated ticker eligibility on `ticker_universe.created_at` so a newly-added ticker cannot retroactively change historical rankings; `BLG-BE-60` added `DRIFT_ALERT_THRESHOLD_GBP` — `import_backtest.py::check_drift_alert` — which surfaces (rather than silently absorbs) an unexplained `total_pnl_gbp` swing on a run with zero new closed trades (`trades_imported == trades_deleted`). Both remain in place and were re-confirmed present during this audit (`import_backtest.py` lines 30–70).

## 5. Cross-Reference to BLG-BE-59 / BLG-BE-60

Both prior fixes concerned the **compute** side of the nightly backtest (which trades the model produces, and whether the same input state reproduces the same P&L). This audit's §4.4 finding concerns the **import/persistence** side (how those computed results are written to the database) and confirms it uses the correct full-replace pattern independently of the compute-side fixes — the two layers were both audited, not just one.

## 6. Additional Non-Idempotency Risks Found

None. All four audited jobs use either a pure `UPDATE` (no accumulation possible) or an explicit `ON CONFLICT ... DO UPDATE` / full-transaction-scoped delete-then-reinsert pattern. No follow-up backlog items were required by this audit.

## 7. Observation (Out of Scope, Not Actioned)

`backend/main.py`'s `POST /positions/nightly-stop-update`, `POST /positions/risk-off-alerts`, and `POST /signals/rebalance-exit` each call `record_nightly_job(...)`, implying they are intended as scheduled nightly jobs, but no `.github/workflows/*.yml` cron trigger was found calling any of the three (only a reference in `quality_gate.yml`, which is a CI test-suite context, not a production schedule). Whether these are triggered by some other mechanism, are legacy/dormant, or represent a scheduling gap is outside this item's AC scope (idempotency of the four named jobs) — noted here for visibility only, not filed as a backlog item since it is a different question (whether a job runs at all) from the one this item was scoped to answer (whether a job that does run is idempotent).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | ST-06 (EPIC-06, v7.6, BLG-BE-62): Initial audit. All four scoped jobs (position analysis, portfolio snapshot, signal generation, nightly backtest import) confirmed idempotent via direct SQL/code inspection, not docstring inference. No non-idempotency risks found; no follow-up items filed. Cross-references BLG-BE-59/BLG-BE-60 as the confirmed prior instance of this defect class (compute-side; this audit covers the import/persistence side). |
