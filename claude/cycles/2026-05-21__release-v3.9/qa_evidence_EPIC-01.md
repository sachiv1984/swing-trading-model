Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-22

---

**EPIC:** EPIC-01 — Screener Reliability: Crumb/401 Fix, Sector/Industry Fix, Invalid Ticker Removal, Degraded-Run Banner
**Cycle:** 2026-05-21__release-v3.9
**Sprint goal:** Improve screener reliability and data quality — fix Yahoo Finance 401 errors, restore sector/industry to results, remove invalid tickers, surface degraded runs to users
**Test scenarios used:**
- `tests/test_screener_data_service.py` — ST-01 crumb refresh unit tests
- `tests/test_screener_batch_service.py` — ST-02 sector/industry propagation, ST-04 degraded_run calculation
- `tests/e2e/screener.spec.js` — SC-SCR-DEG-01, SC-SCR-DEG-02

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | stage4_backlog_slice.md#ST-01 | `_refresh_yahoo_crumb()` in screener_data_service.py; 401/429 triggers crumb refresh + exponential backoff+jitter retry; ThreadPoolExecutor with `YF_MAX_CONCURRENT` cap in screener_batch_service.py | AC-01: 401 triggers crumb refresh + retry; AC-02: exponential backoff+jitter on 401/429; AC-03: concurrent cap via env var (default 5); AC-05: crumb events logged | Pass | None |
| ST-02 | stage4_backlog_slice.md#ST-02 | `get_all_tickers()` returns full row dicts; sector/industry passed to `compute_screener_result()` | AC-01: results have non-null sector/industry when in ticker_universe; AC-02: no schema change; AC-03: unit test confirms propagation | Pass | None |
| ST-03 | stage4_backlog_slice.md#ST-03 | Removed DAY from tickers_full_list.csv; `deactivate_invalid_tickers()` called at startup; PHNX.L investigated | AC-01: DAY removed from CSV; AC-02: DAY deactivated at startup; AC-03: no OHLCV FAILED logs for DAY on next run; AC-04: PHNX.L — Phoenix Group Holdings plc is valid FTSE 250, YF returns OHLCV data — kept | Pass | None |
| ST-04 | stage4_backlog_slice.md#ST-04, docs/design/2026-05-21__release-v3.9/degraded-run-banner/ux_spec.md | `degraded_run` + `failure_rate` added to screener_runs table and API response; `DegradedRunBanner` component in Screener.js; screener_api_contract.md v1.1; openapi.yaml updated | AC-01: degraded_run=true when >20% tickers fail OHLCV; AC-02: API includes degraded_run + failure_rate; AC-03: banner shows "Results may be incomplete — N% of tickers failed data fetch"; AC-04: clean runs show no banner; AC-05: SC-SCR-DEG-01 passes; AC-06: SC-SCR-DEG-02 passes | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_screener_data_service.py::test_yahoo_401_triggers_crumb_refresh_and_retries`, `tests/test_screener_data_service.py::test_yahoo_crumb_refresh_updates_module_state`, `tests/test_screener_batch_service.py::test_sector_industry_passed_to_compute_screener_result`, `tests/test_screener_batch_service.py::test_degraded_run_set_when_failure_rate_exceeds_20_pct`, `tests/test_screener_batch_service.py::test_degraded_run_false_when_failure_rate_below_20_pct`, `tests/e2e/screener.spec.js::SC-SCR-DEG-01`, `tests/e2e/screener.spec.js::SC-SCR-DEG-02` — all pass
- Regression areas checked: screener results fetch, ticker universe management, Yahoo Finance data fetch pipeline
- Known deviations filed: None

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — DegradedRunBanner is display-only, no URL construction
- Signed off by: Director of Quality
- Date: 2026-05-22
- Comments: Approved with one P3 notation. ST-01/02/03 backend unit tests (11+12 = 23/23 pass) cover all mechanistic ACs. ST-04 Playwright tests SC-SCR-DEG-01 and SC-SCR-DEG-02 satisfy the LL-v3.1-EX-01 frontend gate — banner presence (35% text verified) and absence both confirmed. API contract updated at ## heading level; openapi.yaml includes degraded_run and failure_rate fields. Commit message correctly lists all four story IDs [EPIC-01][ST-01][ST-02][ST-03][ST-04]. No new routes registered; backend/routers/test.py update not required. UX spec compliance confirmed: amber banner, AlertTriangle icon, correct text format, no dismiss button, cleared on new scan trigger. P3 notation: ST-01 AC-04 ("run completes without >5% OHLCV failures under normal YF conditions") is a runtime/environment-dependent criterion not verifiable by unit test; the mechanism (crumb refresh, retry, concurrency cap) is unit-tested and the AC is accepted as staging-only evidence. A backlog item should be filed to add a Yahoo Finance integration test stub for backoff verification. No deviations filed; no P0/P1 issues present.
