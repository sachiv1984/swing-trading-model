**Owner:** QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-09
**Source:** ST-10 (BLG-QA-92, EPIC-02, v9.3 sprint execution)

---

# Backend Test Suite Runtime Baseline

## Purpose

ST-10's acceptance criteria: record the current `backend/.venv/bin/python3 -m pytest` runtime as a documented baseline for future regression comparison. Per CLAUDE.md §9, the suite must be run via the project virtualenv (`backend/.venv/bin/python3 -m pytest`), not system Python.

This is distinct from `docs/ops/ci_pipeline_baseline.md` (whole-CI-pipeline wall-clock, all workflows including Playwright) and `docs/qa/regression_test_suite_baseline.md` (Playwright/frontend suite inventory) — this baseline covers the **backend pytest suite specifically**.

## Measurement

**Command:** `backend/.venv/bin/python3 -m pytest --tb=no -q` (from repo root)
**Date:** 2026-09-09
**Environment:** local session container, 2 vCPUs, pytest run single-process (no `-n auto`/xdist — this suite has no parallel-worker configuration; a full-suite run is single-threaded)
**Branch/commit context:** `exec/2026-09-09__release-v9.3/EPIC-02`, built on `main` after EPIC-01's merge (PR #1629)

## Result

```
1385 passed, 10 skipped, 159 warnings in 60.57s (0:01:00)
```

- **Total tests collected:** 1395 (1385 passed + 10 skipped)
- **Wall-clock runtime:** ~60.6s (pytest-reported); ~63.2s including Python interpreter startup (measured via shell `time`)
- **Skips:** 10 — not itemised here; pre-existing, unrelated to this baseline (environment-conditional skips, e.g. tests requiring credentials not present in this session)

## Where the Time Goes (top 15 slowest, `--durations=15`)

| Test | Duration |
|------|----------|
| `test_gemini_claude_retry_backoff.py::TestCallClaudeRetryBackoff::test_retries_on_transient_5xx_then_succeeds` | 3.00s |
| `test_gemini_claude_retry_backoff.py::TestCallClaudeRetryBackoff::test_gives_up_after_persistent_transient_failures_and_raises` | 3.00s |
| `test_gemini_claude_retry_backoff.py::test_generate_setup_thesis_surfaces_graceful_error_after_retries_exhausted` | 3.00s |
| `test_regime_retry_backoff.py::test_check_market_regime_defaults_to_risk_on_after_persistent_failures` | 3.00s |
| `test_root_logging_config.py::TestRootLoggingConfig::test_root_logger_configured_at_info_with_a_handler` | 2.66s |
| `test_root_logging_config.py::TestRootLoggingConfig::test_uvicorn_loggers_do_not_propagate_to_root_no_duplicate_lines` | 2.52s |
| `test_root_logging_config.py::TestRootLoggingConfig::test_basicconfig_is_a_no_op_if_root_already_has_a_handler` | 2.45s |
| `test_root_logging_config.py::TestRootLoggingConfig::test_application_logger_reaches_root_handler` | 2.45s |
| `test_rate_limit_endpoints.py::test_health_rate_limit_returns_429_after_60_requests` | 2.08s |
| `test_backtest_rule_service.py::TestRunCandidateBacktest::test_full_run_persists_and_returns_comparison` | 1.57s |
| `test_retry_backoff.py::test_yahoo_price_gives_up_after_persistent_connection_errors` | 1.50s |
| `test_alpaca_paper_sync_idempotent_retry.py::test_open_gives_up_after_persistent_failures_swallows_error` | 1.50s |
| `test_alpaca_paper_sync_close_positions_backoff.py::test_positions_gives_up_after_persistent_failures_still_raises` | 1.50s |
| `test_regime_retry_backoff.py::test_fetch_index_regime_gives_up_after_persistent_failures_returns_none` | 1.50s |
| `test_alpaca_paper_sync_close_positions_backoff.py::test_close_gives_up_after_persistent_failures_swallows_error` | 1.50s |

**Observation (informational, not actionable within ST-10's scope):** the top 15 slowest tests alone account for ~34.7s — roughly 57% of the total 60.57s runtime — and are almost entirely retry/backoff tests exercising real (not mocked) `time.sleep`-based exponential backoff across several independent modules (Gemini/Claude API calls, market regime fetch, Yahoo pricing, Alpaca paper-trading sync). These are legitimate real-delay tests, not slow assertions — a future optimisation could inject a fake clock/mock `time.sleep` in these specific modules' retry-backoff test fixtures if suite runtime becomes a pain point, but this is not filed as a backlog item here since ST-10's scope is recording the baseline, not identifying or fixing runtime debt.

## How to Use This Baseline

For future regression comparison: re-run `backend/.venv/bin/python3 -m pytest --tb=no -q` and compare the reported total against **60.57s** (single-process, 2-vCPU environment). A large regression (e.g., >20% slower with no proportional growth in test count) may indicate a newly-introduced slow test, an accidental removal of a mock (causing a real network/sleep call), or environment drift — worth investigating before accepting as new-normal. Test count growth is expected over time as new stories add coverage; compare **time-per-test** (currently ~43.7ms/test average, `60.57s / 1385`) alongside the raw total for a fairer trend signal.

## Acceptance

- Recorded by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — a runtime measurement/documentation deliverable, no observable UI behaviour)
- Date: 2026-09-09
