Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-14

# QA Evidence — EPIC-01 (Nightly Backtest Data Integrity)

## Consolidation Block

**EPIC:** EPIC-01 — Nightly Backtest Data Integrity
**Cycle:** 2026-07-14__release-v7.1
**Sprint goal:** Eliminate the two P1 nightly-backtest data-integrity bugs feeding the Strategy Benchmark page (EPIC-01), bring the Table View RISK OFF badge into spec compliance (EPIC-02), and close out the four v7.0 post-ship hardening gaps (EPIC-03) — delivering all v7.1 mandatory anchors plus capacity-filling hardening in a single sprint.
**Test scenarios used:** `tests/test_production_strategy.py` (new — 11 scenarios: `TestComputeSignalsCreatedAtGating` ×4, `TestBacktestDeterminism` ×1, `TestDriftAlert` ×6)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-01 | N/A — `spec_reference_not_applicable: true` (bug fix, no prior canonical spec) | `compute_signals()` now masks each ticker's momentum to `NaN` (not just its final signal) before rank computation, for all dates before that ticker's own `ticker_universe.created_at`. `_load_tickers()` returns a `{ticker: created_at}` map alongside the ticker list (DB path only; CSV fallback returns `None` per ticker, preserving prior no-DB behaviour). | AC-01: eligibility gated on own `created_at`. AC-02: adding a ticker only affects selections from today forward. AC-03: no change to trades preceding a newly-added ticker's `created_at`. | Pass | None |
| ST-02 | N/A — `spec_reference_not_applicable: true` (bug fix, no prior canonical spec) | Fix vehicle (RISK-01) selected at kickoff: option (c) — `import_backtest.py` now calls a new pure `check_drift_alert()` function after every import; a `total_pnl_gbp` swing beyond a documented £50 threshold on a run with zero new closed trades (`trades_imported == trades_deleted`) exits with code 2 and a fixed `BACKTEST_DRIFT_ALERT:` log line instead of being silently logged. `production_strategy.py`'s script body was wrapped in `main()`/`if __name__ == "__main__":` (dead `matplotlib` import also removed) so `compute_signals()`/`backtest()` are importable and testable without live yfinance calls — this is what makes the AC-02 controlled re-run comparison possible at all. | AC-01: fix vehicle selected and implemented (option c). AC-02: two consecutive runs with zero new exits produce byte-identical `total_pnl_gbp` — verified via a controlled re-run comparison (`TestBacktestDeterminism`, fixed synthetic inputs, `backtest()` called twice, `assert_frame_equal`/`assert_series_equal`). AC-03: threshold (£50) and alert destination (stderr, `BACKTEST_DRIFT_ALERT:` prefix, exit code 2) documented and testable (`TestDriftAlert`, 6 scenarios). | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_production_strategy.py` (11/11 passing), full existing suite re-run for regression (`backend/.venv/bin/python3 -m pytest tests/` — 650 passed, 2 skipped, no regressions)
- Regression areas checked: nightly backtest signal computation, backtest engine determinism, import drift-check; confirmed no other module imports `production_strategy.py`'s functions (grep — it is a standalone script invoked by the GH Actions `backtest.yml` job), so the `main()`-wrap refactor has no other call-site impact
- Known deviations filed: None

**Process note:** A cosmetic `.github/workflows/backtest.yml` cleanup (removing the now-unused `matplotlib` from the job's `pip install` line) was committed then reverted in a follow-up commit on this branch — the push token lacks `workflow` OAuth scope to modify workflow files. Left as a harmless unused-dependency install; not filed as a backlog item (trivial, no functional impact, no spec or AC involvement).

---

## Autonomous Class Sign-Off (BLG-GOV-19)

**Autonomous class eligibility check:**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-01, ST-02 both autonomous)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ (both stories' backlog-slice "Staging-only ACs" fields state "None"; ST-02's conditional staging-only AC does not trigger because fix vehicle option (c), not (a)/(b), was selected)
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/components/**` or `src/pages/**` was created or modified (`git diff --stat main...HEAD` — only `production_strategy.py`, `import_backtest.py`, `tests/test_production_strategy.py`, `.github/workflows/backtest.yml` touched) — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-14
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review/test-verifiable, no frontend changes, engine signer populated). Full regression suite (650 tests) re-run clean alongside the 11 new scenarios.
