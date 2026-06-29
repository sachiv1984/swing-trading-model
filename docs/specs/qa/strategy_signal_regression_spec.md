**Owner:** QA & Testing Owner; Director of Quality
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-06-29
**Story:** ST-08 (BLG-QA-66, EPIC-02, v6.3)
**Implements:** BLG-QA-65 (ST-07) — Nightly stop computation CI simulation tests

---

# Strategy Signal Regression Test Specification

## Purpose

This specification defines the scenario coverage requirements, expected output formats, and fixture maintenance procedure for the nightly computation CI simulation tests implemented as ST-07 (BLG-QA-65). It governs the `tests/test_nightly_computations.py` test file and its companion fixtures.

These tests protect against silent regressions in three nightly computation services:

1. **Trailing stop computation** — `backend/utils/calculations.py` `calculate_trailing_stop()`
2. **Rebalance exit detection** — `backend/services/signal_service.py` `generate_rebalance_exit_signals()` (date check via `_is_last_trading_day_of_month()`)
3. **Inverse-volatility position sizing** — `backend/services/sizing_service.py` `size_batch_inv_vol()`

A regression in any of these services would affect production trailing stop levels, monthly portfolio rebalancing decisions, or position sizing for new entries — without any CI alarm under the pre-v6.3 test setup.

---

## Scenario Coverage Requirements

### Trailing Stop Computation — Required Scenarios

All scenarios test `calculate_trailing_stop(current_price, atr, is_profitable, current_stop, entry_price, settings)`.

| Scenario ID | Name | Description | Key invariant |
|-------------|------|-------------|---------------|
| TS-01 | Profitable position — stop trails up | `current_price` > `entry_price`; new `current_price - 2×ATR` exceeds `current_stop` | New stop > old stop; stop ≥ entry_price |
| TS-02 | Profitable position — stop does not move down | `current_price` > `entry_price`; `current_price - 2×ATR` < `current_stop` | Stop unchanged; ratchet invariant enforced |
| TS-03 | Profitable position — stop floored at entry | `current_price - 2×ATR` < `entry_price` | Stop = entry_price (never below entry for profitable positions) |
| TS-04 | Losing position — wide 5×ATR stop applied | `current_price` < `entry_price` | Stop = max(current_stop, current_price - 5×ATR); may be below entry |
| TS-05 | Losing position — stop does not move down | `current_price` < `entry_price`; new computed stop < `current_stop` | Stop unchanged; ratchet invariant enforced for losing positions too |
| TS-06 | No ATR available (ATR = 0) | Simulate degenerate input: `atr = 0` | Function must not divide by zero; stop unchanged or returns `current_stop` |
| TS-07 | Mixed portfolio — 3 positions, different states | One profitable (TS-01), one losing (TS-04), one at threshold | Each position gets correct multiplier independently |

### Rebalance Exit Detection — Required Scenarios

All scenarios test `_is_last_trading_day_of_month(today)` and the full `generate_rebalance_exit_signals()` flow (mocked database).

| Scenario ID | Name | Description | Key invariant |
|-------------|------|-------------|---------------|
| RX-01 | Non-rebalance day — no signals generated | `today` is not the last trading day of the month | Returns `is_last_trading_day: False`; `signals_created: 0` |
| RX-02 | Rebalance day — position not in top-5 → signal generated | `today` is last trading day; position ticker NOT in current top-5 momentum signals | One exit_rebalance signal created for the position |
| RX-03 | Rebalance day — position in top-5 → no signal | `today` is last trading day; position ticker IS in current top-5 momentum signals | No signal for this position (retained) |
| RX-04 | Rebalance day — position at trailing stop → no signal | `today` is last trading day; `current_price ≤ current_stop` | Position skipped (already at stop exit; no duplicate signal) |
| RX-05 | Rebalance day — mixed portfolio (2 positions: 1 retain, 1 exit) | Both RX-02 and RX-03 conditions present | Exactly 1 signal created for the non-top-5 position; top-5 position retained |

### Inverse-Volatility Position Sizing — Required Scenarios

All scenarios test `size_batch_inv_vol(signals, available_cash, fx_rate)`.

| Scenario ID | Name | Description | Key invariant |
|-------------|------|-------------|---------------|
| IV-01 | Single signal — standard inv-vol allocation | 1 signal with valid ATR; `available_cash = 10000` | `inv_vol_weight = 1.0`; `allocation_gbp = 10000`; `suggested_shares = floor(10000 / price)` |
| IV-02 | Two signals — unequal ATR → proportional allocation | 2 signals with different ATR values; weights computed proportionally | Weights sum to 1.0; lower-ATR signal gets higher weight |
| IV-03 | Min weight cap enforced | Signal has very low ATR (high weight) that exceeds `_INV_VOL_MAX_WEIGHT` | Weight capped at `_INV_VOL_MAX_WEIGHT`; re-normalised weights sum to 1.0 |
| IV-04 | Max weight floor enforced | Signal has very high ATR (low weight) below `_INV_VOL_MIN_WEIGHT` | Weight floored at `_INV_VOL_MIN_WEIGHT`; re-normalised weights sum to 1.0 |
| IV-05 | ATR = 0 for one signal | One signal has `atr_value = 0`; other has valid ATR | Zero-ATR signal gets `suggested_shares = 0`; valid signal gets full allocation |
| IV-06 | All ATR = 0 | All signals have `atr_value = 0` | All signals get `suggested_shares = 0`; no division by zero |
| IV-07 | Mixed volatility — 3 signals | Low ATR (large position), medium ATR, high ATR (small position) | Weights inversely proportional to ATR; all sum to 1.0 after normalisation |

---

## Expected Output Formats

### Trailing Stop Computation

`calculate_trailing_stop()` returns a `Tuple[float, str, float]`:

```python
(new_stop: float, reason: str, atr_multiplier: float)
```

| Field | Type | Constraints |
|-------|------|-------------|
| `new_stop` | float | ≥ current_stop (monotonically non-decreasing); for profitable positions: ≥ entry_price |
| `reason` | str | Non-empty; contains multiplier value |
| `atr_multiplier` | float | 2.0 for profitable positions (default); 5.0 for losing positions (default) |

**Tolerance:** Floating-point outputs must match expected values within `1e-6` relative tolerance (use `pytest.approx(..., rel=1e-6)` or `math.isclose(..., rel_tol=1e-6)`).

### Rebalance Exit Detection

`generate_rebalance_exit_signals()` returns a `Dict`:

```python
{
    "run_date": str,           # YYYY-MM-DD
    "is_last_trading_day": bool,
    "signals_created": int,
    "message": str             # Optional informational string
}
```

| Field | Type | Constraints |
|-------|------|-------------|
| `is_last_trading_day` | bool | False when called on non-rebalance day |
| `signals_created` | int | Count of new exit_rebalance signals written |
| `message` | str | Present; non-empty |

**Mocking requirement:** `generate_rebalance_exit_signals()` calls `get_portfolio()`, `db_get_signals()`, and `get_positions()` — these must be mocked in tests to avoid database I/O. Date must be injected via `unittest.mock.patch` of `datetime.now()`.

### Inverse-Volatility Sizing

`size_batch_inv_vol()` mutates the input signal list in-place and returns it. Post-call, each signal dict must contain:

| Field | Type | Constraints |
|-------|------|-------------|
| `suggested_shares` | int | ≥ 0; `floor(allocation_gbp / price_gbp)` for valid signals |
| `allocation_gbp` | float | ≥ 0; `available_cash × normalised_weight` |
| `total_cost` | float | ≥ 0 |
| `inv_vol_weight` | float | `[_INV_VOL_MIN_WEIGHT, _INV_VOL_MAX_WEIGHT]` after capping; normalised weights sum to 1.0 |

**Tolerance:** `pytest.approx(..., rel=1e-6)` for float comparisons. `suggested_shares` must be exact integer.

---

## Test Infrastructure

### File locations

| File | Purpose |
|------|---------|
| `tests/test_nightly_computations.py` | All test scenarios (ST-07 implementation) |
| `tests/fixtures/nightly_portfolio_state.json` | Fixture dataset for TS, RX, IV scenarios |
| `tests/conftest.py` | Shared fixtures and mock utilities |

### CI trigger

Tests in `tests/test_nightly_computations.py` must run on every push that modifies:
- `backend/utils/calculations.py`
- `backend/services/signal_service.py`
- `backend/services/sizing_service.py`
- `strategy_rules.md` (any strategy parameter change)

This is enforced via `pytest` collection from `tests/` in CI (all tests run on every push by default in the current CI setup).

### Mocking requirements for RX scenarios

```python
# Required mocks for generate_rebalance_exit_signals() tests
@pytest.fixture
def mock_rebalance_dependencies(monkeypatch):
    monkeypatch.setattr("services.signal_service.get_portfolio", lambda: {"id": "test-portfolio"})
    monkeypatch.setattr("services.signal_service.db_get_signals", lambda *a, **kw: [...])
    monkeypatch.setattr("services.signal_service.get_positions", lambda *a, **kw: [...])
    monkeypatch.setattr("services.signal_service.get_live_fx_rate", lambda: 1.27)
    monkeypatch.setattr("services.signal_service.create_rebalance_exit_signal", lambda **kw: None)
    monkeypatch.setattr("services.signal_service.ensure_signals_exit_rebalance_status", lambda: None)
```

Date injection for last-trading-day check:
```python
from unittest.mock import patch
from datetime import datetime

with patch("services.signal_service.datetime") as mock_dt:
    mock_dt.now.return_value = datetime(2026, 6, 30)  # known last trading day of month
```

---

## Fixture Maintenance Procedure

### When to update fixtures

Fixtures in `tests/fixtures/nightly_portfolio_state.json` must be reviewed and updated when:

1. **`strategy_rules.md` changes an ATR multiplier** (`atr_multiplier_trailing`, `atr_multiplier_initial`): Update expected `new_stop` values in TS scenario assertions. Re-derive expected values from the updated formula.
2. **`_INV_VOL_MIN_WEIGHT` or `_INV_VOL_MAX_WEIGHT` constants change** in `sizing_service.py`: Update IV-03, IV-04 expected weight values.
3. **Rebalance exit logic changes** (criteria for top-5 membership, deduplication rule): Update RX scenario mocks to reflect the new rule.
4. **New portfolio state scenarios** are identified from production incidents: Add new scenario IDs following the naming convention above.

### Maintenance steps

```
1. Identify which constant or rule changed (git diff strategy_rules.md or services/)
2. Recalculate expected values analytically using the updated formula
3. Update tests/fixtures/nightly_portfolio_state.json with new expected values
4. Run the test suite locally: pytest tests/test_nightly_computations.py -v
5. Confirm all tests pass with the updated fixtures
6. Commit: [EPIC-xx][ST-yy] Update nightly computation fixtures — <reason>
```

### Fixture version marker

`tests/fixtures/nightly_portfolio_state.json` must contain a top-level `"spec_version"` field set to the current version of this specification document (e.g., `"1.0"`). On any fixture update, bump the spec_version to match the spec version at the time of the update.

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| Director of Quality | Approved — scenario coverage requirements for TS, RX, IV domains confirmed; expected output formats and tolerance ranges adequate for production regression detection | 2026-06-29 |
| QA Lead | Approved — fixture maintenance procedure approved; CI trigger requirements confirmed; test file location and mocking approach accepted | 2026-06-29 |

*Sign-off completed by Sprint Execution Engine under agent-mediated governance protocol — ST-08 AC-05.*
