**Owner:** Director of Quality; QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-13 (ST-19, BLG-QA-206, EPIC-03, v9.12 — C4.1.7-01/02/03/05/06/07/08 moved to Asserted by `tests/e2e/position-sizing-widget-behaviours.spec.js`); prior — 2026-10-13 (ST-09, BLG-QA-205, EPIC-02, v9.12 — C4.1.5-01/02/03 and C4.1.6-01/02 moved to Asserted by `tests/test_sizing_fx_and_cash.py`); prior — 2026-10-09 (ST-16, BLG-BE-143, EPIC-03, v9.11 — C6.3-02 moved to Asserted by `TestInGraceStopParity` after the §6.3 in-grace ruling); prior history retained — see prior entries in version control
**Source:** ST-11 (BLG-QA-185, EPIC-03, cycle `2026-09-30__release-v9.9`)

---

# Strategy-Rule → Test Traceability Matrix (§4–§8)

## Purpose

`BLG-BE-119` found that `strategy_rules.md`'s entry-price-floor clause was exercised by no golden test. Until now nothing mapped each normative clause of the strategy rules to a test that asserts it. This matrix does that for §4 (position entry), §4.1 (sizing calculator), §4.2 (pre-entry advisory checks), §5 (initial stop), §6 (grace period), §7 (trailing stop framework) and §8 (exit conditions). It reports the share of clauses that have an asserting test.

`docs/testing/spec_to_test_traceability_matrix.md` (v2.2) maps API/frontend specs to tests. This document is its strategy-rules counterpart and does not replace it.

## Method

- **Clauses:** each sentence or bullet in §4–§8 that states a checkable behaviour (a formula, threshold, condition, output or prohibition) is one clause. Purely descriptive or rationale text ("Purpose", "Rationale", "the calculator proposes a share quantity only", the RISK-01 background narrative) is excluded. Each of §4.1.4's five invalid conditions is not counted separately, because one test exercises them as a set.
- **Asserting test:** a test in `tests/` or `tests/e2e/` that runs in CI and **fails if the clause is broken**. Running the code path without checking the clause's outcome does not count. `backend/mutmut_pilot_tests/` is excluded: it is a one-off mutation-testing pilot that no CI workflow runs.
- **Status:**
  - **Asserted:** at least one such test asserts the clause against the implementation it governs.
  - **Partial:** the clause is asserted only for part of its behaviour, only against a mocked API (frontend test with no backend computation behind it), or only on a non-live code path (e.g. the replay engine rather than the live exit check).
  - **None:** no asserting test found.
- Mapped by reading the clause and the implementing function, then searching `tests/` for tests of that function. Snapshot as of `main` + EPIC-03 at 2026-10-05.

## Summary

| | Clauses | Share |
|---|---:|---:|
| Asserted | 46 | **93.9%** |
| Partial | 2 | 4.1% |
| None | 1 | 2.0% |
| **Total normative clauses** | **49** | |
| Asserted or partial | 48 | 98.0% |

**% of clauses with an asserting test: 79.6% (39/49)** — 85.7% counting partial coverage. (Was 51.0% before ST-04, v9.10, 67.3% before ST-16, v9.11, which moved C6.3-02 to Asserted once §6.3's in-grace behaviour was ruled, and 69.4% before ST-09, v9.12, which asserted the five §4.1.5/§4.1.6 clauses.)

Where coverage is strong: the backend sizing arithmetic (§4.1.1–§4.1.4), the pre-entry advisory checks (§4.2.1–§4.2.5), and the stop formulas and ratchet (§5, §7.2, §7.3). The last two are covered by golden tests, reconciliation tests and, since ST-12, property-based tests.

Where it is weak:
- §4.1.7's sizing-widget UI behaviours: debounce, loading state, no-overwrite / "use this", no auto-fill on invalid or insufficient-cash results, and non-blocking submission.
- The on-load half of §7.1-02: the on-load path reuses the stored ATR rather than refetching it. (The live exit decision behind §6.3 and §8 was a gap until ST-04, v9.10, added `tests/test_live_exit_decision.py`.)

Follow-ups for every Partial/None clause are filed, grouped by area, as `BLG-QA-205`–`BLG-QA-208` (see the last column).

## Matrix

### §4 Position entry rules

| ID | Clause | Status | Asserting test(s) | Follow-up |
|----|--------|--------|-------------------|-----------|
| C4-01 | Required at entry: ticker, entry date, entry price, shares, ATR | None | — no test asserts the required-field set of `POST /portfolio/position` | BLG-QA-208 |
| C4-02 | Fees applied automatically by market (UK / US) | Asserted | `tests/test_money_arithmetic_golden.py::TestFeeCalculationsAgreeElsewhere`; `tests/test_trade_service.py` | — |
| C4-03 | Fractional shares supported | Asserted | `tests/test_golden_outputs.py::TestPositionSizingSpecFormulas` (fractional `suggested_shares`, e.g. PS02) | — |

### §4.1 Position sizing calculator

| ID | Clause | Status | Asserting test(s) | Follow-up |
|----|--------|--------|-------------------|-----------|
| C4.1.1-01 | `StopDistance = EntryPrice − StopPrice` | Asserted | `tests/test_golden_outputs.py::TestPositionSizingSpecFormulas` (PS01–PS05) | — |
| C4.1.1-02 | Portfolio value = latest `portfolio_history.total_value` snapshot | Asserted | `tests/test_strategy_invariants_property.py::test_valid_inputs_produce_valid_conservative_size`, `::test_missing_or_nonpositive_portfolio_value_is_invalid` | — |
| C4.1.2-01 | `RiskAmount = PortfolioValue × RiskPercent` | Asserted | `tests/test_golden_outputs.py::TestPositionSizingSpecFormulas` | — |
| C4.1.2-02 | Available cash must not be the risk basis | Asserted | `tests/test_strategy_invariants_property.py::test_valid_inputs_produce_valid_conservative_size` (cash ≠ portfolio value; risk bounded by portfolio value) | — |
| C4.1.3-01 | `RawShares = RiskAmount / StopDistance` | Asserted | `tests/test_golden_outputs.py::TestPositionSizingSpecFormulas` | — |
| C4.1.3-02 | `SuggestedShares = floor(RawShares, 4dp)`, conservative | Asserted | `tests/test_money_arithmetic_golden.py::TestSuggestedSharesFloorBoundaries`; `tests/test_golden_outputs.py::TestPositionSizingImplementation`; ST-12 property test | — |
| C4.1.4-01 | Invalid if RiskPercent ≤ 0, PortfolioValue ≤ 0, EntryPrice ≤ 0, StopPrice ≤ 0, or StopDistance ≤ 0 | Asserted | `tests/test_strategy_invariants_property.py::test_invalid_inputs_always_rejected_with_deterministic_reason`, `::test_missing_or_nonpositive_portfolio_value_is_invalid` | — |
| C4.1.4-02 | If invalid: shares not applied; deterministic reason code returned | Asserted | `tests/test_strategy_invariants_property.py::test_invalid_inputs_always_rejected_with_deterministic_reason` | — |
| C4.1.4-03 | Missing snapshot → `NO_PORTFOLIO_VALUE_SNAPSHOT` | Asserted | `tests/test_strategy_invariants_property.py::test_missing_or_nonpositive_portfolio_value_is_invalid` | — |
| C4.1.5-01 | A user-provided FX rate overrides the live rate | Asserted | `tests/test_sizing_fx_and_cash.py`::TestFxHandling::test_us_override_replaces_live_rate_and_is_echoed (live rate not read; override drives shares and is echoed); also `tests/e2e/what-if-sizing-preview.spec.js` V-WHATIF-05 (request side, mocked API) | — |
| C4.1.5-02 | Default FX is the system-provided live rate | Asserted | `tests/test_sizing_fx_and_cash.py`::TestFxHandling::test_us_without_override_uses_live_rate | — |
| C4.1.5-03 | The FX rate used is returned in the sizing response | Asserted | `tests/test_sizing_fx_and_cash.py`::TestFxHandling (live, override and UK 1.0 echoes) | — |
| C4.1.6-01 | `EstimatedCost > AvailableCash` → insufficient-cash result (`cash_sufficient: false`) | Asserted | `tests/test_sizing_fx_and_cash.py`::TestCashConstraint (UK and US insufficient; sufficient negative case) | — |
| C4.1.6-02 | Insufficient-cash result may include `MaxAffordableShares` | Asserted | `tests/test_sizing_fx_and_cash.py`::TestCashConstraint::test_insufficient_result_includes_affordable_max_shares, `::test_us_insufficient_result_includes_affordable_max_shares` (present, and affordable including fees) | — |
| C4.1.7-01 | Calculator always visible in the Position Entry form (no toggle) | Asserted | `tests/e2e/position-sizing-widget-behaviours.spec.js` SC-PSW-01 (visible on load; no switch, checkbox or activation button) | — |
| C4.1.7-02 | Auto-recalculates on entry/stop/risk change, debounced 300ms | Asserted | `tests/e2e/position-sizing-widget-behaviours.spec.js` SC-PSW-02 (controlled clock: no call 240 ms after the last keystroke, one call at 300 ms; entry, stop and risk % changes each recalculate) | — |
| C4.1.7-03 | Loading state shown between debounce firing and response | Asserted | `tests/e2e/position-sizing-widget-behaviours.spec.js` SC-PSW-03 (spinner while a delayed mocked response is pending) | — |
| C4.1.7-04 | Valid result + empty shares field → auto-filled with SuggestedShares | Asserted | `tests/e2e/smoke-critical-paths.spec.js` PATH-1 (waits on the auto-fill; mocked API) | — |
| C4.1.7-05 | Valid result + manually entered shares → not overwritten; "use this" affordance shown | Asserted | `tests/e2e/position-sizing-widget-behaviours.spec.js` SC-PSW-05 (manual 7 kept; "Use suggested shares" applies 10 and hides) | — |
| C4.1.7-06 | INSUFFICIENT_CASH → no auto-fill; MaxAffordableShares informational only | Asserted | `tests/e2e/position-sizing-widget-behaviours.spec.js` SC-PSW-06 (shares stay empty; muted "Max affordable" line; no use button) | — |
| C4.1.7-07 | Invalid result → no auto-fill; inline plain-language message | Asserted | `tests/e2e/position-sizing-widget-behaviours.spec.js` SC-PSW-07 (`INVALID_RISK_PERCENT` message; shares stay empty) | — |
| C4.1.7-08 | Invalid or cash-constrained result does not block form submission | Asserted | `tests/e2e/position-sizing-widget-behaviours.spec.js` SC-PSW-08 (invalid and cash-constrained cases both submit) | — |

### §4.2 Pre-entry advisory checks

| ID | Clause | Status | Asserting test(s) | Follow-up |
|----|--------|--------|-------------------|-----------|
| C4.2.1 | Regime gate: FAIL if target market risk-off (US SPY / UK FTSE 200-day MA) | Asserted | `tests/test_pre_entry_validation.py::TestRegimeGate` | — |
| C4.2.2 | Sector concentration: WARN if projected sector allocation ≥ 30% | Asserted | `tests/test_pre_entry_validation.py::TestSectorConcentration` | — |
| C4.2.3 | Earnings proximity: WARN within 0–5 calendar days; US tickers only | Asserted | `tests/test_pre_entry_validation.py::TestEarningsProximity` | — |
| C4.2.4 | Cash constraint: FAIL if estimated cost > available cash | Asserted | `tests/test_pre_entry_validation.py::TestCashConstraint` | — |
| C4.2.5 | Sizing validity: FAIL if stop distance ≤ 0 or either price ≤ 0; only when both supplied | Asserted | `tests/test_pre_entry_validation.py::TestSizingValidity` | — |
| C4.2.6 | Advisory checks never prevent, gate or auto-reject plan submission | Partial | `tests/test_pre_entry_validation.py::TestAggregateStatus::test_response_always_200_on_fail` (API level only; no UI submission-not-blocked assertion) | BLG-QA-208 |

### §5 Initial stop calculation

| ID | Clause | Status | Asserting test(s) | Follow-up |
|----|--------|--------|-------------------|-----------|
| C5-01 | `InitialStop = EntryPrice − (InitialATRMultiplier × ATR)` | Asserted | `tests/test_golden_outputs.py::TestStopLossSpecFormulas::test_SL01_initial_stop`; `tests/test_stop_reconciliation.py::test_SL01_initial_stop_reconciles` | — |
| C5-02 | The stop exists immediately and is stored/tracked from day one | Asserted | `tests/test_live_exit_decision.py::TestEntryPersistsInitialStop` (`add_position` writes `initial_stop` and `current_stop`) | — |

### §6 Grace period

| ID | Clause | Status | Asserting test(s) | Follow-up |
|----|--------|--------|-------------------|-----------|
| C6.2 | Grace period is 10 calendar days (days 0–9) | Asserted | `tests/test_portfolio_integration.py::test_grace_period_when_holding_days_lt_10`; `tests/test_stop_reconciliation.py::test_grace_period_days` | — |
| C6.3-01 | During grace: stop-loss enforcement disabled; no stop-based exit recommendation | Asserted | `tests/test_live_exit_decision.py::TestGraceBoundary` (live `should_exit_position`, day 9 vs day 10), `::TestGracePeriodStillStoresStop`; `tests/test_service_layer_direct_coverage.py::test_grace_period_returns_none` | — |
| C6.3-02 | During grace: the stop price is calculated (at entry, §5) and stored, and is not recalculated or ratcheted until day 10 | Asserted | `tests/test_live_exit_decision.py::TestEntryPersistsInitialStop` (calculated and stored at entry); `::TestInGraceStopParity` (on-load and nightly paths both leave the stored stop untouched on days 0/5/9, including an already-raised stop; both recalculate from day 10). Wording follows `strategy_rules.md` §6.3 v1.15 (ST-16, v9.11, ruling ESC-EXEC-20261008-01) | — |
| C6.3-03 | During grace: manual exit is always permitted | Asserted | `tests/test_live_exit_decision.py::TestManualExitInsideGrace` (days 0, 3, 9) | — |

### §7 Trailing stop-loss framework

| ID | Clause | Status | Asserting test(s) | Follow-up |
|----|--------|--------|-------------------|-----------|
| C7.1-01 | ATR period: 14 days (rolling) | Asserted | `tests/test_stop_reconciliation.py::test_atr_period_days`; `tests/test_replay_service.py::test_atr_warm_up_boundary_14_rows_is_the_minimum` | — |
| C7.1-02 | ATR recalculated daily, via on-load recompute and a nightly job | Partial | `tests/test_live_exit_decision.py::TestNightlyRecomputesAtr` (nightly job fetches a fresh ATR); `tests/test_live_exit_decision.py::TestOnLoadRecompute` (on-load recomputes the stop); `tests/test_nightly_computations.py`. The on-load path reuses the stored ATR and only fetches one when it is missing, so the on-load half of the clause is a behaviour gap, not a test gap | ST-06 (BLG-FE-193, tooltip claim) |
| C7.1-03 | RISK-01: backtest/signal ATR copies delegate to the one canonical close-approximation | Asserted | `tests/test_atr_consolidation.py` | — |
| C7.2-01 | Losing/breakeven: `Stop = CurrentPrice − (InitialATRMultiplier × ATR)` | Asserted | `tests/test_golden_outputs.py::test_SL02_losing_trailing_stop`; `tests/test_nightly_computations.py::test_TS04_losing_wide_stop_applied`; `tests/test_trailing_stop_breakeven_floor.py::test_losing_position_not_floored_at_entry` | — |
| C7.2-02 | Profitable: `Stop = max(CurrentPrice − (ProfitATRMultiplier × ATR), EntryPrice)` | Asserted | `tests/test_golden_outputs.py::test_SL03_profitable_trailing_stop`, `::test_SL08_profitable_floor_binds`; `tests/test_trailing_stop_breakeven_floor.py`; ST-12 property test | — |
| C7.2-03 | `position_manager.py` is deliberately not on the live stop path (floor exception) | Asserted | `tests/test_trailing_stop_breakeven_floor.py::TestPositionManagerNotOnLiveStopPath` | — |
| C7.3 | `UpdatedStop = max(CurrentStop, NewlyCalculatedStop)` — stops never move down | Asserted | `tests/test_golden_outputs.py` SL04–SL07; `tests/test_nightly_computations.py` TS02/TS05; `tests/test_stop_reconciliation.py::test_stop_decrease_would_be_detected`; `tests/test_strategy_invariants_property.py` (single-step + path properties) | — |

### §8 Exit conditions

| ID | Clause | Status | Asserting test(s) | Follow-up |
|----|--------|--------|-------------------|-----------|
| C8-00 | A position may exit under exactly three conditions | Asserted | `tests/test_live_exit_decision.py::TestClosedSetOfExitReasons` (automated decision returns only Stop Loss Hit / Risk-Off Signal); `::TestManualExitInsideGrace` (manual exit) | — |
| C8.1-01 | Stop-loss trigger active only after grace; fires when price breaches the trailing stop | Asserted | `tests/test_live_exit_decision.py::TestGraceBoundary`, `::TestPriceVersusStop` (at/below/above stop); `tests/test_replay_service.py::test_stop_exit_on_a_sharp_crash` | — |
| C8.1-02 | Stop exit is recommended and requires manual confirmation | Asserted | `tests/test_live_exit_decision.py::TestStopExitNeedsManualConfirmation` (`analyze_positions` returns EXIT without writing a trade or closing the position) | — |
| C8.2 | Risk-off (200-day MA of the relevant index) → exit regardless of stop | Asserted | `tests/test_live_exit_decision.py::TestRiskOffOverrides` (overrides grace and stop), `::TestStopExitNeedsManualConfirmation::test_risk_off_recommends_exit_inside_grace`; `tests/test_replay_service.py::test_risk_off_exit_on_a_regime_dip`; `tests/test_screener_batch_service.py::test_fetch_regime_returns_risk_off_when_price_below_ma` | — |
| C8.3 | Manual exit is user-initiated and available at any time | Asserted | `tests/test_live_exit_decision.py::TestManualExitInsideGrace` | — |

## Follow-up items

| Item | Area | Clauses |
|------|------|---------|
| BLG-QA-205 | Backend sizing: FX default/override/echo and §4.1.6 cash-constraint result. **Done** in ST-09, v9.12 | C4.1.5-01, C4.1.5-02, C4.1.5-03, C4.1.6-01, C4.1.6-02 |
| BLG-QA-206 | Playwright coverage of §4.1.7 sizing-widget behaviours. **Done** in ST-19, v9.12 | C4.1.7-01, C4.1.7-02, C4.1.7-03, C4.1.7-05, C4.1.7-06, C4.1.7-07, C4.1.7-08 |
| BLG-QA-207 | Live exit decision and grace-period behaviour (`should_exit_position`, stop persistence at entry). **Done** in ST-04, v9.10; C7.1-02 stays Partial for a behaviour reason, see its row | C5-02, C6.3-01, C6.3-02, C6.3-03, C7.1-02, C8-00, C8.1-01, C8.1-02, C8.2, C8.3 |
| BLG-QA-208 | Entry required-field set and advisory panel non-blocking at the UI | C4-01, C4.2.6 |

## Maintenance

Re-run this mapping when `strategy_rules.md` §4–§8 changes (`§12.3` change control) or when a follow-up above lands. Update the row and the Summary counts in the same commit.
