Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

## Consolidation Block

**EPIC:** EPIC-07 — Nightly backtest data-integrity smoke test as a standing CI gate
**Cycle:** 2026-07-27__release-v7.9
**Sprint goal:** Ship all 15 v7.9 EPICs — the two P1 UX anchors and the 13 capacity-fill engineering-hardening items — with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_backtest_data_integrity_smoke.py` (8 unit tests, all passing) + a live run of `scripts/backtest_data_integrity_smoke_test.py` against the real, checked-in `production_results/all_trades_20260122_141632.csv`.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-07 | `scripts/backtest_data_integrity_smoke_test.py`, `.github/workflows/backtest.yml` | New standing smoke test checking the point-in-time eligibility invariant (`BLG-BE-59` class) and idempotency/no-duplicate-trades invariant (`BLG-BE-63` class) against the imported backtest data; the third historical incident (`BLG-BE-60`, P&L reproducibility) is not reimplemented — already live via `import_backtest.py`'s `check_drift_alert`. Wired as a new hard-fail CI step in `backtest.yml`, with its failure now also routed through the existing Telegram alert step. | AC-01: Smoke test added to CI — Pass. AC-02: Passes on current data — Pass (verified against real `production_results/all_trades_*.csv`, 217 rows, 0 violations). AC-03: Head of Engineering sign-off — Pass (agent-mediated; found and fixed a real alert-wiring gap during review). | Pass | None |

**QA test coverage:**
- Scenarios run: `backend/.venv/bin/python3 -m pytest tests/test_backtest_data_integrity_smoke.py -v` — 8/8 passed, including synthetic BLG-BE-59/63-class violation cases and an end-to-end injected-duplicate failure case. Direct script run against real data confirms AC-02.
- Regression areas checked: `production_strategy.py`'s `compute_signals`/`_load_tickers` reviewed directly to confirm the point-in-time invariant (`entry_date >= ticker_universe.created_at`) is correctly modelled, not a misreading of the BLG-BE-59 bug.
- Known deviations filed: None — the alert-wiring gap found during review (smoke-test failure would have silently skipped the Telegram alert) was fixed in this same commit, not deferred.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-07 only, autonomous)
- Criterion 2: All AC verifiable by code review alone — ✓ (unit tests + a direct script run against real checked-in data; no UI, no staging run)
- Criterion 3: No frontend-visible change — confirmed no file under `src/pages/**` or `src/components/**` was created or modified — ✓
- Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-27
- Comments: Autonomous class sign-off — all four qualifying criteria met. Head of Engineering sign-off (AC-03) obtained separately via agent-mediated review (§5.3): Approved. Reviewer independently confirmed the point-in-time invariant design against `production_strategy.py`, confirmed the BLG-BE-60 non-reimplementation was a reasonable scoping decision (not a gap), and found one real CI wiring gap — a smoke-test failure would fail the job but silently skip the Telegram alert (the alert step's condition only checked the import step's exit code). Fixed in this same commit: the smoke test step now captures its exit code the same way the import step does, and the alert step's condition and message logic were extended to cover it.
