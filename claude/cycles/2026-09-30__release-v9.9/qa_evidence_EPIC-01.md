Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-01

# QA Evidence Log — EPIC-01

**EPIC:** EPIC-01 — Backend Reliability & Data Integrity
**Cycle:** 2026-09-30__release-v9.9
**Sprint goal:** Ship a single canonical ATR/stop-recalculation implementation with timestamp visibility on `GET /positions` (`BLG-BE-135`), while clearing the queued backend, security, QA, governance, spec, and frontend debt items that make up the rest of v9.9's full-capacity scope.
**Test scenarios used:** `tests/test_reports_integration.py`, `tests/test_upstream_call_helper.py`, `tests/test_atr_consolidation.py`, `tests/test_position_atr_timestamp_persistence.py`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `strategy_rules.md#7.1`, `data_model.md#DS-22`, `position_endpoints.md#GET /positions`, `openapi.yaml`, `docs/product/decisions/st01_atr_consolidation_ruling.md` | RISK-01 ruling (agent-mediated, Strategy Rules & System Intent Owner): 3 ATR formulas are deliberately distinct, not duplicates. Consolidated the 3 byte-identical close-to-close approximation copies (strategy_engine.py, database.py) into `utils/pricing.py::compute_atr_close_approximation`; left live stop-loss and screener formulas unchanged. Added `stop_calculated_at`/`atr_calculated_at`/`active_atr_multiplier` persistence (DS-22 migration, applied to staging + production) and exposed all 3 on `GET /positions`. | ATR implementation count reduced / cadence documented / fields exposed — see Deviations | Pass_with_deviation | `BLG-BE-135`'s literal "1 canonical source across all 4 files" wording is intentionally not met for `pricing.py`/`screener_engine.py` — the AC itself permits "engineering constrained to match the documented cadence, per the Owner's ruling," which the RISK-01 ruling satisfies. Full rationale: `docs/product/decisions/st01_atr_consolidation_ruling.md`. |
| ST-02 | `reports_endpoints.md#GET /reports/monthly-pnl` | Added year bounds check to `GET /reports/monthly-pnl`, mirroring `GET /reports/tax-year`'s existing check. | 400 (not 404/raw error) for out-of-range year; regression test added | Pass | None |
| ST-03 | spec_reference_not_applicable — config/timeout-sourcing fix, no prior canonical spec | `gemini_service.py`'s daily-cost Telegram alert now sources its timeout from `get_timeout("telegram")`. | Timeout sourced from config; no behaviour change | Pass | None |
| ST-04 | spec_reference_not_applicable — config/timeout-sourcing fix, no prior canonical spec | `utils/pricing.py::calculate_atr`'s Yahoo Finance fallback now sources its timeout from `get_timeout("yfinance")`. | Timeout sourced from config; no behaviour change | Pass | None |
| ST-05 | spec_reference_not_applicable — config/timeout-sourcing fix, no prior canonical spec | `alpaca_paper_sync_service.py`'s 3 Alpaca call sites now source their timeout from `get_timeout("alpaca")`. | All 3 call sites sourced from config; no behaviour change | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_reports_integration.py` (ST-02, 60 tests), `tests/test_upstream_call_helper.py` (ST-03/04/05, 40 tests), `tests/test_atr_consolidation.py` (ST-01 consolidation, 3 tests), `tests/test_position_atr_timestamp_persistence.py` (ST-01 timestamp/multiplier persistence, 6 tests)
- Regression areas checked: full backend suite run after every commit in this EPIC — final state 1959 passed, 12 skipped (pre-existing, unrelated to this EPIC — see `tests/test_api_contracts.py::TestReportsEndpoints::test_get_tax_year_report_returns_ok`'s order-dependency gap, confirmed present before this EPIC's first commit and tracked as ST-10/EPIC-03 in this same sprint, not introduced here)
- Known deviations: ST-01's `Pass_with_deviation` disposition above (RISK-01 ruling scope vs. literal AC wording) — no other deviations found; all deviation checks completed with nothing else to file

---

## Standard Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):** Criterion 1 unmet — ST-01 is `delegated_backend`, not all stories are `autonomous`. Standard Sign-Off Block applies, per the Mixed-Class EPIC Signer Format Note.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend-visible change in this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3)
- Signed off by: Sprint Execution Engine (agent-mediated, Data Model & Domain Schema Owner role — §5.3)
- Date: 2026-10-01
- Comments: ST-01's RISK-01 ruling and DS-22 migration review/application are agent-mediated per §5.3, on explicit user direction throughout (grounding the ATR ruling in backtest data availability; authorizing and then confirming the DS-22 migration once staging+production write access was arranged outside this session). ST-02/03/04/05 are autonomous, code-review-verifiable, no frontend-visible change. This EPIC-level block does not itself satisfy the STEP 4 merge gate's separate "QA sign-off comment from Director of Quality on PR" and "Product Owner acceptance" rows — both remain always-human per `execution_prompt.md` §5.3 and are expected to halt at STEP 4 pending human action.
