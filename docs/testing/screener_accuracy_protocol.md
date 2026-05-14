Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-14
Source: BLG-QA-18 (ST-14, v3.4)
Harness: tests/mock_harness/ (BLG-QA-08)
Schema reference: docs/specs/screener_results_schema.md
Strategy reference: claude/strategy/strategy_rules.md §11

---

# Screener Accuracy Test Protocol

**Purpose:** Formal protocol for verifying the Arc 1 screener engine returns correct include/exclude decisions for tickers with known input values. Establishes a repeatable baseline before any sprint touching screener filter logic.

**Executors:** QA & Testing Owner (routine runs), Director of Quality (sign-off)
**Prerequisite:** BLG-QA-08 mock harness operational (`tests/mock_harness/api_mock_harness.py`)
**Fixture library:** `docs/testing/screener_test_data_library.md`

---

## Strategy Rules §11 Parameter Reference

The following parameters from `claude/strategy/strategy_rules.md §11` govern screener gate logic:

| Parameter | Canonical Value | Source |
|-----------|----------------|--------|
| ATR period | 14 days rolling | §11 |
| Initial/losing stop multiplier | 5 × ATR | §11 |
| Profitable stop multiplier | 2 × ATR | §11 |
| Regime gate | 200-day MA of relevant index (SPY for US, FTSE for UK) | §6.1–6.4 |

**Operational screener parameters** (defined in DS-01 implementation; must be confirmed at test run time):
- ATR minimum threshold: documented in DS-01 spec (current value: confirm from `backend/routers/screener.py` or DS-01 migration notes)
- Signal score minimum threshold: documented in DS-01 spec (current value: confirm from implementation)

> These operational thresholds are not yet in §11. When they are formalised, this protocol must be updated to reference the §11 entry. Until then, the executing QA engineer must confirm the threshold values from the DS-01 source before running boundary-case scenarios.

---

## Test Fixture Inventory

Load fixtures via `ScreenerMockHarness.from_scenario(scenario_name)` from `tests/mock_harness/fixtures/`. All expected outcomes are based on the fixture parameters defined in `docs/testing/screener_test_data_library.md`.

| Fixture | Scenario | Expected outcome | Gate tested |
|---------|----------|-----------------|-------------|
| `screener_pass_us.json` | MOCK-PASS-US — passes all filters | Included in results | All gates pass |
| `screener_pass_uk.json` | MOCK-PASS-UK — passes all filters (UK) | Included in results | All gates pass |
| `screener_fail_regime_us.json` | MOCK-FAIL-REGIME-US — SPY below 200-day MA | Excluded | Regime gate |
| `screener_fail_regime_uk.json` | MOCK-FAIL-REGIME-UK — FTSE below 200-day MA | Excluded | Regime gate |
| `screener_fail_atr.json` | MOCK-FAIL-ATR — ATR below minimum threshold | Excluded | ATR gate |
| `screener_fail_signal.json` | MOCK-FAIL-SIGNAL — signal score below threshold | Excluded | Signal gate |
| `screener_stale_data.json` | MOCK-STALE-DATA — insufficient price history | Excluded | Data sufficiency gate |
| `screener_uk_pence.json` | MOCK-UK-PENCE — pence-denominated UK ticker | Included; price in GBP (pence conversion applied) | Pass + conversion |
| `screener_no_news.json` | MOCK-NO-NEWS — no Alpaca news | Included; `news_headline_count = 0` | Pass + empty news |
| `screener_borderline_atr.json` | MOCK-BORDERLINE-ATR — ATR exactly at threshold | Implementation-defined; document actual result | ATR boundary |
| `screener_multi_us.json` | MOCK-MULTI-US — multiple US tickers | Multiple included; ranked by `signal_score` descending | Ranking order |
| `screener_mixed_market.json` | MOCK-MIXED-MARKET — US + UK tickers | Both included; correct market routing per ticker | Market routing |

---

## Test Execution Procedure

### Pre-Run Setup

1. Confirm mock harness is operational: `python -m pytest tests/ -k "mock_harness" --collect-only`
2. Confirm `tests/mock_harness/fixtures/` contains all 12 fixture files from the inventory above
3. Note the current ATR minimum threshold and signal score minimum threshold from DS-01 source code (confirm values haven't changed since last protocol run)
4. Record run date, executor name, and confirmed threshold values at top of the run record

---

### Scenario Execution Steps

For each fixture in the inventory:

**Step 1 — Load fixture**
```python
harness = ScreenerMockHarness.from_scenario("<fixture_name>")
```

**Step 2 — Execute screener run**
Trigger `POST /screener/run` against the mock harness. Wait for run completion.

**Step 3 — Retrieve results**
Call `GET /screener/results?run_id=<run_id>`. Parse the results list.

**Step 4 — Verify outcome**

| Check | Pass condition |
|-------|---------------|
| Include/exclude decision | Ticker in results if expected outcome = "Included"; absent if expected outcome = "Excluded" |
| Price currency | `currency` field = USD for US tickers, GBP for UK tickers |
| ATR period | `atr_period` = 14 (matches §11) |
| Signal score present | `signal_score` is non-null for included tickers |
| Run metadata | `run_id` and `run_timestamp` present in response |

**Step 5 — Record result**
Update the run record table (see Recording Format below) with Pass/Fail/Blocked for each scenario.

---

### Boundary Case Verification

These scenarios require explicit attention at each run:

#### BC-01 — ATR Threshold Boundary (MOCK-BORDERLINE-ATR)

1. Note the ATR minimum threshold confirmed in pre-run setup
2. Verify the borderline fixture's ATR value is exactly at threshold (±0.001 tolerance)
3. Run the scenario and record the actual outcome
4. If included: document this as "at-threshold = included" in run record
5. If excluded: document as "at-threshold = excluded" in run record
6. The outcome establishes the boundary behaviour for this deployment — it must be consistent across runs

#### BC-02 — Regime Gate Pass/Fail

For MOCK-FAIL-REGIME-US:
1. Confirm fixture has SPY closing price below its 200-day MA
2. Verify ticker is absent from results
3. Verify no error is returned (clean exclusion, not an error)

For MOCK-PASS-US:
1. Confirm fixture has SPY closing price above its 200-day MA
2. Verify ticker is present in results

#### BC-03 — Signal Score Threshold Edge

1. From MOCK-FAIL-SIGNAL fixture: confirm signal_score value is just below minimum threshold
2. Verify ticker is excluded
3. From MOCK-PASS-US fixture: confirm signal_score is above threshold
4. Verify ticker is included and signal_score matches fixture value

---

## Acceptance Criteria for Protocol Pass

The screener accuracy test run **PASSES** when all of the following are true:

- [ ] 11 of 12 scenarios produce the expected include/exclude outcome (MOCK-BORDERLINE-ATR is exempt from hard pass/fail — its outcome is recorded as reference data)
- [ ] All included tickers have `currency` = correct value for their market
- [ ] All included tickers have `atr_period` = 14
- [ ] Ranking order in MOCK-MULTI-US is `signal_score` descending (no ties broken incorrectly)
- [ ] MOCK-UK-PENCE ticker price is in GBP (not pence — conversion confirmed)
- [ ] No test scenario produces a 5xx error response from the screener endpoint

The run **FAILS** (and must be escalated before any sprint touching screener logic proceeds) when:
- Any of the 11 definitive scenarios produces an incorrect outcome
- A 5xx error appears in any scenario
- Price/currency conversion is incorrect for UK tickers

---

## Recording Format

Create a new test run record file at `docs/testing/screener_accuracy_run_<YYYY-MM-DD>.md` for each executed run.

```
# Screener Accuracy Protocol Run — <YYYY-MM-DD>
Executor: <name>
Sprint context: <sprint/cycle or "pre-sprint check">
ATR minimum threshold (confirmed): <value>
Signal score minimum threshold (confirmed): <value>

| Scenario | Fixture | Expected | Actual | Result |
|----------|---------|----------|--------|--------|
| MOCK-PASS-US | screener_pass_us.json | Included | | |
| MOCK-PASS-UK | screener_pass_uk.json | Included | | |
| MOCK-FAIL-REGIME-US | screener_fail_regime_us.json | Excluded | | |
| MOCK-FAIL-REGIME-UK | screener_fail_regime_uk.json | Excluded | | |
| MOCK-FAIL-ATR | screener_fail_atr.json | Excluded | | |
| MOCK-FAIL-SIGNAL | screener_fail_signal.json | Excluded | | |
| MOCK-STALE-DATA | screener_stale_data.json | Excluded | | |
| MOCK-UK-PENCE | screener_uk_pence.json | Included (GBP) | | |
| MOCK-NO-NEWS | screener_no_news.json | Included (0 news) | | |
| MOCK-BORDERLINE-ATR | screener_borderline_atr.json | Reference data | | |
| MOCK-MULTI-US | screener_multi_us.json | Ranked desc | | |
| MOCK-MIXED-MARKET | screener_mixed_market.json | Both included | | |

BC-01 ATR boundary behaviour: <included/excluded at threshold>
BC-02 Regime gate: <pass>
BC-03 Signal threshold: <pass>

Overall: PASS / FAIL
Sign-off: Director of Quality — <date>
```

---

## Escalation

If the protocol **FAILS**:

1. Do not begin or continue any sprint story that touches `backend/routers/screener.py`, `backend/services/screener_service.py`, or any frontend screener filter logic
2. File a backlog item (BLG-QA category) with the failing scenario details
3. Escalate to Head of Engineering for root cause within 24 hours
4. Re-run the protocol after the fix is confirmed on main
