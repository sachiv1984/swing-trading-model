**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-30 (ST-40, BLG-OPS-105, EPIC-06, v9.14 — created)
**Cycle:** 2026-10-29__release-v9.14 (ST-40)

---

# CI Pipeline Runtime Audit — October 2026

## 1. Purpose

CI runtime has been creeping up with no recent audit of which test files are slowest (BLG-OPS-105). This audit profiles CI runtime by workflow and by test file from 3 recent `main` runs, records the 10 slowest contributors, and files each optimisation or parallelisation candidate as a backlog item.

It extends `ci_pipeline_baseline.md` (Playwright shard timing, v4.3 to v9.3), which measured workflows and shards but not individual test files.

## 2. Method

**Runs.** The 3 most recent successful `main` runs of each test suite, read on 2026-10-30 with `gh run list`, `gh run view --json jobs` and the job logs (`gh api .../actions/jobs/<id>/logs`):

| Suite | Run IDs (head commit) |
|-------|-----------------------|
| Playwright E2E Acceptance Tests (`playwright.yml`, 8 shards × 4 workers) | 41033319578 (`0e3960cc`), 41024971878 (`48eab523`), 40846221756 (`28d475fb`) |
| CI Pytest Suite (`ci-tests.yml`, Phase A and Phase B) | 41033462963 (`df2eae33`), 41033319696 (`0e3960cc`), 41030631640 (`2b75d3b4`) |
| Every other workflow on a push to `main` | the runs for `0e3960cc`, `59d65647` and `d9b81134` |

**Playwright per-spec timing.** The `list` reporter prints each test's duration. A spec file's time is the sum of its tests' durations; with 4 workers per shard this is worker time, not shard wall time.

**Pytest per-file timing.** CI runs pytest with `-v` and no `--durations`, so per-file time is the gap between consecutive result lines in the timestamped Phase B log (a test's time includes its fixtures). A local `pytest tests --durations=15` run on 2026-10-30 (3068 passed, 30 skipped) agreed on the slowest tests: the retry tests at 3.00s each and `test_deliberately_broken_ratchet_is_falsified`. Subprocess-spawning tests (`test_root_logging_config.py`, `test_backend_import_path_isolation.py`) are 1.5–3× slower locally than in CI.

**Shard phases.** Per shard: setup is job start to the first test result line (checkout, `npm ci`, browser cache, OS dependencies and the `webServer` build), and the test phase is first to last result line.

## 3. Runtime by Workflow

Wall time from run creation to completion, mean of the sampled `main` runs (n = number of runs that ran the workflow; path filters skip some workflows on some commits).

| Workflow | Mean wall time | n |
|----------|---------------:|--:|
| Playwright E2E Acceptance Tests | 232s (229, 232, 235) | 3 |
| Deploy to Staging (Render) | 211s | 1 |
| CI Pytest Suite | 136s (129, 131, 147) | 3 |
| Critical-Path Smoke Tests (Playwright) | 110s | 3 |
| Frontend Production Build | 89s | 1 |
| Deploy to GitHub Pages | 80s | 3 |
| Dependency Vulnerability Scan | 46s | 3 |
| Analytics Validation Gate | 37s | 3 |
| Secret Scanning; Portfolio Integration Tests | 23s each | 3 |
| Endpoint Coverage Report; Service Layer Coverage Gate | 20s each | 3 |
| 7 lint and drift gates (UI Copy, Golden Output, Governance Sync, Non-Registry, OpenAPI Drift, Strategy Copy, Skip/Only) | 11–18s each | 1–3 |

The repository is public, so none of this is billed (`ci_usage_reports/2026-08.md`). The cost is feedback time, set by the slowest workflow: the Playwright E2E suite.

### 3.1 Playwright E2E per shard

Mean of 3 runs, seconds.

| Shard | Job | Setup | Test phase | Summed test time (run 41033319578) |
|------:|----:|------:|-----------:|-----------------------------------:|
| 1 | 224 | 90 | **131** | **385** |
| 2 | 141 | 70 | 68 | 259 |
| 3 | 168 | 83 | 82 | 274 |
| 4 | 178 | 89 | 87 | 307 |
| 5 | 157 | 83 | 72 | 297 |
| 6 | 153 | 78 | 72 | 202 |
| 7 | 147 | 71 | 74 | 338 |
| 8 | 179 | 87 | 90 | 280 |

Setup (mean 81s) is about half of every shard's job. Of it, `npm ci` takes 17s, `playwright install-deps` 13s and the browser cache 4s, and about 45s is the production React build that `playwright.config.js`'s `webServer` runs before the first test, once in every shard. Shard 1 carries `accessibility-axe-scan.spec.js`, `chart-interactivity.spec.js` and `arc5-compliance-section.spec.js`, so its test phase is 46% above the next slowest, and it sets the workflow's critical path.

### 3.2 Pytest

Phase A (no database) took 21–24s per run. Phase B (full suite, real Postgres) took 120–125s, of which the test phase was 79–89s (3,053–3,065 tests) and the rest was setup.

## 4. Runtime by Test File

### 4.1 Playwright: 15 slowest spec files

Summed test durations, mean of 3 runs (per-run values in brackets). 142 spec files, 2,293s summed in total.

| Spec file | Mean | Runs |
|-----------|-----:|------|
| `trade-plan.spec.js` | 73.8s | 73.4, 74.7, 73.3 |
| `accessibility-axe-scan.spec.js` | 73.1s | 74.0, 72.5, 72.8 |
| `chart-interactivity.spec.js` | 59.8s | 59.9, 59.8, 59.8 |
| `system-status.spec.js` | 59.0s | 68.1, 55.6, 53.2 |
| `ticker-universe.spec.js` | 44.7s | 54.9, 40.3, 39.0 |
| `arc5-compliance-section.spec.js` | 44.6s | 44.9, 44.6, 44.2 |
| `trade-debrief.spec.js` | 41.7s | 52.2, 36.8, 36.1 |
| `screener.spec.js` | 40.6s | 31.7, 45.0, 45.2 |
| `monthly-pnl-narrative.spec.js` | 37.9s | 38.5, 42.8, 32.4 |
| `epic03-v34-frontend.spec.js` | 35.9s | 21.1, 42.9, 43.8 |
| `loading-states.spec.js` | 34.9s | 34.8, 34.9, 35.1 |
| `plan-vs-reality.spec.js` | 29.6s | 30.0, 33.9, 24.9 |
| `v7.2-dashboard-tradeplan-ux-hardening.spec.js` | 29.4s | 29.6, 29.6, 28.9 |
| `reports-performance-tab.spec.js` | 28.8s | 33.0, 26.5, 26.9 |
| `strategy-benchmark.spec.js` | 28.5s | 34.4, 27.0, 24.2 |

Slowest single tests: `monitor-exit-queue.spec.js` SC-MEQ-01 (7.2s), `standing-alert.spec.js` SC-SA-03 (6.2s, waits to show the alert does not auto-dismiss) and the two `monthly-pnl-narrative.spec.js` SC-MPN-09 axe scans (6.0s, 5.9s). No single test exceeds 7.5s; the slow specs are slow because they have many 1–5s tests, not one outlier.

### 4.2 Pytest Phase B: 15 slowest test files

Mean of 3 runs. 242 files, 84s summed.

| Test file | Mean | Runs | Why |
|-----------|-----:|------|-----|
| `test_gemini_claude_retry_backoff.py` | 12.0s | 12.0, 12.0, 12.0 | Real retry backoff (3.0s per exhausted-retry test) |
| `test_upstream_call_helper.py` | 7.6s | 7.6, 7.6, 7.6 | Real retry backoff |
| `test_regime_retry_backoff.py` | 6.5s | 6.5, 6.5, 6.5 | Real retry backoff |
| `test_root_logging_config.py` | 5.7s | 4.9, 6.5, 5.8 | Spawns `uvicorn` subprocesses |
| `test_strategy_invariants_property.py` | 5.2s | 4.3, 5.9, 5.3 | Hypothesis property search |
| `test_alpaca_paper_sync_close_positions_backoff.py` | 4.0s | 4.0, 4.0, 4.0 | Real retry backoff |
| `test_utils_stub_leak_guard.py` | 3.2s | 2.8, 3.6, 3.2 | Subprocess |
| `test_backend_import_path_isolation.py` | 3.1s | 2.6, 3.5, 3.1 | Imports every backend module in a subprocess |
| `test_root_logging_json_output_e2e.py` | 2.8s | 2.4, 3.2, 2.9 | Subprocess |
| `test_conftest_database_url_guard.py` | 2.8s | 2.4, 3.2, 2.7 | Subprocess |
| `test_alpaca_paper_sync_idempotent_retry.py` | 2.5s | 2.5, 2.5, 2.5 | Real retry backoff |
| `test_retry_backoff.py` | 2.0s | 2.0, 2.0, 2.0 | Real retry backoff |
| `test_screener_data_service.py` | 1.6s | 1.8, 1.1, 2.0 | — |
| `test_chat_answer_rating_db.py` | 1.6s | 2.5, 1.1, 1.1 | Real Postgres |
| `test_check_strategy_copy.py` | 1.2s | 1.1, 1.4, 1.1 | Scans `src/` |

The six retry files sum to about 35s, 40% of the Phase B test phase, and all of it is `sleep`.

## 5. The 10 Slowest Contributors

Ranked by runner time per push to `main` (seconds, means from §3–§4). "Critical path" marks contributors that lengthen the slowest workflow's wall time.

| # | Contributor | Runner time | Critical path | Candidate |
|--:|-------------|------------:|:-------------:|-----------|
| 1 | Production React build in each of the 8 Playwright shards (`webServer`) | ~360s (45s × 8) | Yes, ~45s | **BLG-OPS-206** |
| 2 | Dependency install in each Playwright shard (`npm ci`, `install-deps`, cache) | ~290s (~36s × 8) | Yes, ~36s | None: already cached (`ci_pipeline_baseline.md` §9); the rest is OS packages |
| 3 | `trade-plan.spec.js` | 73.8s | No (shard 8) | Covered by BLG-QA-241's rebalance if needed |
| 4 | `accessibility-axe-scan.spec.js` | 73.1s | **Yes (shard 1)** | **BLG-QA-241** |
| 5 | `chart-interactivity.spec.js` | 59.8s | **Yes (shard 1)** | **BLG-QA-241** |
| 6 | `system-status.spec.js` | 59.0s | No (shard 7) | None |
| 7 | `ticker-universe.spec.js` | 44.7s | No (shard 7) | None |
| 8 | `arc5-compliance-section.spec.js` | 44.6s | **Yes (shard 1)** | **BLG-QA-241** |
| 9 | `trade-debrief.spec.js` | 41.7s | No (shard 7) | None |
| 10 | Real retry backoff in 6 pytest files | ~35s | Yes, of Pytest Phase B | **BLG-QA-242** |

The next contributors are `screener.spec.js` (40.6s) and the Deploy to Staging wait for Render (211s wall, but almost all of it is waiting for Render to deploy, not runner work).

## 6. Candidates Filed

| Candidate | Expected saving | Backlog item |
|-----------|-----------------|--------------|
| Build the E2E bundle once per run and share it with the 8 shards | ~45s off every shard's critical path; ~300 runner-seconds per run after the one shared build | BLG-OPS-206 |
| Rebalance shard 1 (split its two largest specs, or `fullyParallel`) | Shard 1's test phase from 131s toward the ~80s mean; the E2E wall time falls by up to ~50s | BLG-QA-241 |
| Stub the backoff sleep in the 6 retry test files | ~30s off Pytest Phase B (about a quarter of the CI Pytest Suite's wall time) | BLG-QA-242 |

Considered and not filed: the per-shard dependency install (already cached; the remaining time is OS packages and `npm ci` against a cache), the subprocess-based pytest files (each checks behaviour that needs a fresh interpreter), and more shards (each shard adds ~81s of fixed setup, `ci_pipeline_baseline.md` §9). BLG-QA-77's runtime trend tracking stays gated: CI runtime is not reported as a bottleneck.

## 7. Sign-Off

- [x] CI runtime profiled by workflow (§3) and by test file (§4: Playwright per-spec timing; pytest per-file timing from the `-v` log, cross-checked with local `--durations`) from 3 recent `main` runs per suite
- [x] The 10 slowest contributors recorded (§5)
- [x] Each optimisation or parallelisation candidate filed as a backlog item (§6: BLG-OPS-206, BLG-QA-241, BLG-QA-242)
- Prepared by: Sprint Execution Engine (ST-40)
- Date: 2026-10-30
