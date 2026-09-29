Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-29

---

## Per-Story Evidence

### ST-07 — Remaining ad hoc `timeout=`/retry call sites not yet on the shared upstream-call helper

**Spec reference:** `backend/utils/upstream_call.py`, `tests/test_upstream_call_helper.py`
**Commit:** `ac569bb5943de3dd60056baae423c77ba50b8ff2`

**What was built:** Resolved all 9 call sites named in BLG-BE-128's follow-up list from ST-13 (v9.6). 7 migrated to `get_timeout()`: `screener_data_service.py`'s Stooq/Twelve Data timeouts (config-only — new `"stooq"`/`"twelve_data"` provider entries, no retry-wrap added); `live_trading_assistant.py`, `database.py`, `routers/research.py`'s direct Yahoo Finance chart-API calls (to the existing `"yfinance"`/`"yfinance_history"` values, which already matched the hardcoded literals they replaced); `news_service.py`'s Alpaca News call (to `"alpaca"`, existing retry loop untouched); `si05_digest_service.py` and `ai_endpoint_anomaly_service.py`'s Telegram calls (to a new `"telegram"` provider entry, each call site's own distinct retry shape untouched). 2 explicitly documented as not migrated, with the reason recorded in both `upstream_call.py`'s module docstring and an inline comment at the call site: `health_service.py` (internal self-test against the app's own endpoints, not a 3rd-party upstream provider) and `routers/ticker_universe.py` (`ThreadPoolExecutor` future-result timeout, a different mechanism from a direct HTTP request timeout, and deliberately tighter than the general `"yfinance"` value for interactive UX reasons).

**Acceptance criteria:**
1. Every call site listed in BLG-BE-128 is either migrated to `utils.upstream_call` or has an explicit, documented reason it is not.
2. No behaviour change to any already-working fallback/rate-limit logic (Stooq/Twelve Data cooldown timers, `_TWELVE_DATA_RATE_LIMIT`) as a side effect of any migration performed.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-07 | `backend/utils/upstream_call.py` | 9/9 call sites resolved (7 migrated, 2 documented-not-migrated) | AC-1: all 9 sites resolved — Pass. AC-2: config-only substitution at every site, no retry logic added/changed/removed, `_twelve_data_rate_wait()`/`_TWELVE_DATA_RATE_LIMIT` untouched — Pass | Pass | None |

**Test coverage:** `tests/test_upstream_call_helper.py` — `TestST07NewProviderConfig` (6 cases: `get_timeout`/no-retry-budget for the 3 new providers), `TestST07ScreenerFallbackTiersUseConfiguredTimeout` (2 cases: Stooq/Twelve Data), `TestST07DirectYahooCallSitesUseConfiguredTimeout` (3 cases: research.py, live_trading_assistant.py x2), `TestST07AlpacaNewsUsesConfiguredTimeout` (1 case), `TestST07TelegramCallSitesUseConfiguredTimeout` (2 cases) — 14 new tests, all passing. `database.py`'s own call site is not independently unit-testable (conftest.py replaces `sys.modules["database"]` with an all-`MagicMock` stub for the whole test session, by design, so that every backend module importing `database` gets a safe stub rather than a real DB connection) — verified instead by code review (identical edit shape to the two directly-tested sibling call sites) and the full backend suite (1861 → 1875 tests) passing with no import or behavioural regression. Existing suites covering the touched files (`tests/test_screener_data_service.py`, `tests/test_si05_digest_service.py`, `tests/test_ai_endpoint_anomaly_service.py`, `tests/test_ticker_universe.py`, `tests/test_health_extensions.py`, `tests/test_health_response_schema.py`, `tests/test_research_signal_lookup.py`) all pass unchanged, confirming no behaviour regression at any migrated or documented-not-migrated site.

**Deviations:** None found — deviation check completed.

---

### ST-08 — Extend the v9.7 float→Decimal fee-rounding audit to tax-year statement calculations

**Spec reference:** `docs/ops/money_arithmetic_audit_tax_year_2026-09-29.md`, `tests/test_tax_year_statement_rounding_audit.py`
**Commit:** `1ef40035a97fbba374ace33eae870797dd72c5b4`

**What was built:** Traced every money-arithmetic call site feeding `services.reports_service.get_tax_year_report()` back to its source. Confirmed the entry/exit fee rate-multiplications it ultimately depends on (via stored `total_cost`/`net_proceeds`/`pnl` columns) already use the `Decimal`/`ROUND_HALF_UP` fix from v9.7 ST-08 (BLG-BE-127) — `calculate_exit_proceeds()` was traced line-by-line to confirm it composes the fixed `calculate_uk_exit_fees`/`calculate_us_exit_fees` rather than re-deriving fee arithmetic inline. The tax-year statement layer itself introduces no new rate multiplication — only summation and single-step rounding of already-computed values. Golden-scanned the one arithmetic step in that layer that could in principle introduce its own float-accumulation drift (the summary aggregation's `round(sum(pnls), 2)`): 2,000 random trade sets plus 28 deliberately-constructed half-penny-boundary-adjacent sets, 0 disagreements against an independently-derived Decimal sum. Confirmed carried-forward-loss (`carried_forward_loss_gbp`) has no backend implementation to audit — Design Only per its own decision record (v9.4 ST-17, BLG-FR-03) — and added a regression guard so this disposition cannot silently go stale if an implementation is later added without this audit being revisited.

**Acceptance criteria:**
1. Tax-year statement and carried-forward-loss calculations are confirmed Decimal-consistent at rounding boundaries, or a specific gap is filed with the same rigor as BLG-BE-127.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-08 | `docs/ops/money_arithmetic_audit_tax_year_2026-09-29.md` | Full audit trace + golden scan of tax-year statement arithmetic; carried-forward-loss confirmed not applicable | AC-1: confirmed Decimal-consistent (golden scan, 0 disagreements across 2,028 scanned cases); carried-forward-loss confirmed not applicable (no implementation exists) — Pass | Pass | None |

**Test coverage:** `tests/test_tax_year_statement_rounding_audit.py` — `TestSummaryAggregationGoldenScan` (2 cases: 2,000-trial random scan + 28 half-penny-boundary cases), `TestGetTaxYearReportRealFunctionBoundaryCases` (2 cases: real `get_tax_year_report()` with boundary-adjacent data, and a regression guard confirming `carried_forward_loss_gbp` remains absent) — 4 new tests, all passing. Full backend suite (1875 → 1879 tests) green.

**Deviations:** None found — deviation check completed. No gap filed per AC's first disjunct (confirmed Decimal-consistent).

---

## EPIC-Level Consolidation

**EPIC:** EPIC-02 — Backend Reliability & Financial Correctness
**Cycle:** 2026-09-28__release-v9.8
**Sprint goal:** Clear the full v9.8 full-capacity debt slice — 39 stories across 6 EPICs spanning frontend/UX consistency, backend reliability, QA/test coverage, operations/security hardening, spec & API contract debt, and governance/process debt — with no anchor feature, at exactly the top of the confirmed ~24–28 day sprint capacity band.
**Test scenarios used:** `tests/test_upstream_call_helper.py`, `tests/test_tax_year_statement_rounding_audit.py`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-07 | `backend/utils/upstream_call.py` | 9 call sites resolved (7 migrated, 2 documented-not-migrated) | Both ACs met | Pass | None |
| ST-08 | `docs/ops/money_arithmetic_audit_tax_year_2026-09-29.md` | Tax-year statement arithmetic audit + golden scan; carried-forward-loss not applicable | AC met | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_upstream_call_helper.py` (34 tests, includes 14 new ST-07 cases), `tests/test_tax_year_statement_rounding_audit.py` (4 new tests), full backend suite (`backend/.venv/bin/python3 -m pytest tests/ -q --ignore=tests/e2e`) — 1879 passed, 12 skipped, 0 failed
- Regression areas checked: screener data service (Stooq/Twelve Data/Yahoo fallback tiers), Alpaca news, SI-05 Telegram digest delivery, AI endpoint anomaly Telegram alerts, ticker validation, health self-test, research price lookup, tax-year report generation — all existing suites pass unchanged
- Known deviations: None found — all stories' deviation checks completed with nothing to file

No frontend-visible change in this EPIC — no file under `src/components/**` or `src/pages/**` was created or modified. Both stories are backend/test/docs changes only.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ (ST-07, ST-08 both autonomous)
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required, no live system interaction — ✓ (both stories verified via local pytest against mocked dependencies; no live DB, staging, or production API calls made)
- [x] Criterion 3: No frontend-visible change — confirmed no file under `src/components/**` or `src/pages/**` was created or modified — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-09-29
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review/test-verifiable with no live-system interaction, no frontend changes, engine signer populated). Full backend suite green (1879 passed, 12 skipped) before this sign-off.
