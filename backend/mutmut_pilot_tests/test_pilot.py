"""
ST-15 (BLG-QA-184, EPIC-03, v9.8) mutation-testing pilot -- real test
coverage for the two target modules (strategy_rules.md §4.1 Position
Sizing Calculator, §7.2/§7.3 stop-ratchet), used as the pytest selection
for a scoped `mutmut run`. See
docs/testing/mutation_testing_pilot_sizing_and_stop_ratchet.md for the
mutation score this suite produced and BLG-QA-198 for why this pilot needed
its own isolated conftest.py rather than reusing tests/conftest.py.

Deliberately standalone (does not import from the repo's tests/ package) --
see mutmut_pilot_tests/conftest.py's own docstring for why.
"""
from unittest.mock import MagicMock, patch

import pytest

from utils.calculations import calculate_trailing_stop
from services import sizing_service
from services.sizing_service import _floor_4dp, size_position

import database


# ---------------------------------------------------------------------------
# calculations.py::calculate_trailing_stop (strategy_rules.md §7.2/§7.3)
# ---------------------------------------------------------------------------

class TestCalculateTrailingStop:
    def test_profitable_position_tight_stop(self):
        # §7.2 profitable: Stop = max(CurrentPrice - ProfitATRMultiplier*ATR, EntryPrice)
        new_stop, reason, mult = calculate_trailing_stop(
            current_price=110, atr=5, is_profitable=True, current_stop=100,
            entry_price=100, settings={"atr_multiplier_trailing": 2},
        )
        assert new_stop == 100.0
        assert "tight" in reason.lower()
        assert mult == 2.0

    def test_profitable_position_breakeven_floor(self):
        # §7.2 breakeven floor: a profitable stop must never sit below entry.
        # 110 - 2*5 = 100 == entry, so this case is exactly at the floor;
        # push ATR up so the naive calc would go below entry and confirm
        # the floor clamps it back to entry.
        new_stop, _, _ = calculate_trailing_stop(
            current_price=110, atr=20, is_profitable=True, current_stop=95,
            entry_price=100, settings={"atr_multiplier_trailing": 2},
        )
        assert new_stop >= 100.0

    def test_losing_position_wide_stop(self):
        # §7.2 losing/breakeven: Stop = CurrentPrice - InitialATRMultiplier*ATR
        new_stop, reason, mult = calculate_trailing_stop(
            current_price=90, atr=5, is_profitable=False, current_stop=60,
            entry_price=100, settings={"atr_multiplier_initial": 5},
        )
        assert new_stop == 65.0
        assert "wide" in reason.lower() or "loss" in reason.lower()
        assert mult == 5.0

    def test_stop_never_moves_down_ratchet(self):
        # §7.3 hard constraint: UpdatedStop = max(CurrentStop, NewlyCalculatedStop)
        new_stop, _, _ = calculate_trailing_stop(
            current_price=80, atr=5, is_profitable=False, current_stop=90,
            entry_price=100, settings={"atr_multiplier_initial": 5},
        )
        # naive calc would be 80 - 5*5 = 55, well below current_stop=90
        assert new_stop == 90.0

    def test_stop_never_moves_down_when_profitable_too(self):
        new_stop, _, _ = calculate_trailing_stop(
            current_price=95, atr=1, is_profitable=True, current_stop=98,
            entry_price=90, settings={"atr_multiplier_trailing": 2},
        )
        # naive calc: 95 - 2*1 = 93, below current_stop=98 -- ratchet holds
        assert new_stop == 98.0

    def test_new_stop_actually_participates_in_the_ratchet_max(self):
        # Mutation-testing pilot finding (ST-15, BLG-QA-184): a mutant that
        # dropped `new_stop` entirely from `max(current_stop, new_stop,
        # entry_price)` survived every other test here, because in each
        # case above current_stop or entry_price already happened to be the
        # true max -- so removing new_stop from consideration never changed
        # the observable result. This case makes new_stop itself the
        # largest of the three (130 - 2*5 = 120 > current_stop=100 and
        # > entry_price=100), so dropping it from the max would wrongly
        # return 100 instead of 120.
        new_stop, _, _ = calculate_trailing_stop(
            current_price=130, atr=5, is_profitable=True, current_stop=100,
            entry_price=100, settings={"atr_multiplier_trailing": 2},
        )
        assert new_stop == 120.0

    def test_default_atr_multipliers_used_when_settings_omit_them(self):
        # Mutation-testing pilot finding: every other case here always
        # supplies an explicit atr_multiplier_trailing/initial, so a mutant
        # that changed the settings.get(...) fallback default (2.0/5.0) or
        # its key name survived undetected. This exercises both defaults
        # directly with an empty settings dict.
        profitable_stop, _, profitable_mult = calculate_trailing_stop(
            current_price=110, atr=5, is_profitable=True, current_stop=90,
            entry_price=90, settings={},
        )
        assert profitable_mult == 2.0
        assert profitable_stop == 100.0  # 110 - 2.0*5 = 100

        losing_stop, _, losing_mult = calculate_trailing_stop(
            current_price=90, atr=5, is_profitable=False, current_stop=50,
            entry_price=100, settings={},
        )
        assert losing_mult == 5.0
        assert losing_stop == 65.0  # 90 - 5.0*5 = 65

    def test_explicit_trailing_multiplier_value_and_key_name_both_matter(self):
        # Mutation-testing pilot finding: the other explicit-multiplier
        # cases above use values (2, 5) that coincide with the function's
        # own defaults, so a mutant that mangled the settings key name
        # (falling back to that same-valued default) produced an identical
        # result and survived. Using a value that actually differs from the
        # default (3.0 vs the 2.0 default) makes both the value AND the key
        # name it's read under independently observable.
        new_stop, _, mult = calculate_trailing_stop(
            current_price=200, atr=10, is_profitable=True, current_stop=50,
            entry_price=50, settings={"atr_multiplier_trailing": 3.0},
        )
        assert mult == 3.0
        assert new_stop == 170.0  # 200 - 3.0*10 = 170 (would be 180 if the default 2.0 were used)

    def test_explicit_initial_multiplier_value_and_key_name_both_matter(self):
        new_stop, _, mult = calculate_trailing_stop(
            current_price=90, atr=10, is_profitable=False, current_stop=0,
            entry_price=100, settings={"atr_multiplier_initial": 7.0},
        )
        assert mult == 7.0
        assert new_stop == 20.0  # 90 - 7.0*10 = 20 (would be 40 if the default 5.0 were used)


# ---------------------------------------------------------------------------
# sizing_service.py::_floor_4dp (strategy_rules.md §4.1.3)
# ---------------------------------------------------------------------------

class TestFloor4dp:
    def test_exact_value_unchanged(self):
        assert _floor_4dp(20.0) == 20.0

    def test_non_terminating_decimal_floors_not_rounds(self):
        # 45.45454545... must floor to 45.4545, not round to 45.4546
        assert _floor_4dp(375.0 / 8.25) == 45.4545

    def test_floors_down_never_up(self):
        assert _floor_4dp(30.00009) == 30.0


# ---------------------------------------------------------------------------
# sizing_service.py::size_position (strategy_rules.md §4.1, full path)
# golden vectors adapted from tests/golden_outputs.json PS-01/PS-02/PS-03
# ---------------------------------------------------------------------------

def _mock_portfolio(cash=5000.0, portfolio_id="p1"):
    return {"id": portfolio_id, "cash": cash}


def _mock_snapshot(total_value):
    return {"total_value": total_value}


class _Unconfigured:
    """Return value of a database mock a test did not configure. Any use
    raises, so a test that forgets one of the three mocks fails loudly
    instead of inheriting another test's stale return_value (ST-41,
    BLG-QA-201, v9.11)."""

    def __init__(self, name):
        self._name = name

    def _fail(self, *_a, **_k):
        raise AssertionError(f"database.{self._name} was not configured by this test")

    __bool__ = __getitem__ = __iter__ = __len__ = get = _fail

    def __getattr__(self, attr):
        self._fail()


_DB_MOCKS = ("get_portfolio", "get_latest_snapshot", "get_settings")


@pytest.fixture(autouse=True)
def _fresh_database_mocks():
    """Each test gets fresh, unconfigured mocks for the three database reads
    size_position makes, restored after the test (ST-41, BLG-QA-201). They
    were previously assigned on the session-wide stub with no reset, so a
    test inherited whatever the previous test had set."""
    patches = []
    for name in _DB_MOCKS:
        mock = MagicMock(return_value=_Unconfigured(name))
        # sizing_service imported these by name, so patch both bindings with
        # the same mock; tests configure it through database.<name>.
        patches += [patch.object(database, name, mock), patch.object(sizing_service, name, mock)]
    for p in patches:
        p.start()
    yield
    for p in reversed(patches):
        p.stop()


@pytest.fixture(autouse=True)
def _no_heat_impact():
    # Isolates size_position's pure sizing arithmetic from
    # portfolio_service.calculate_prospective_heat's own DB reads --
    # that function is out of this pilot's scope (heat impact has its own
    # dedicated test coverage elsewhere in tests/test_sizing_heat_impact.py).
    with patch.object(sizing_service, "calculate_prospective_heat", return_value={"valid": False}):
        yield


class TestSizePositionGoldenVectors:
    def test_ps01_uk_round_result_no_floor_needed(self):
        database.get_portfolio.return_value = _mock_portfolio(cash=10000.0)
        database.get_latest_snapshot.return_value = _mock_snapshot(10000.0)
        database.get_settings.return_value = [{}]

        result = size_position(entry_price=100.0, stop_price=95.0, risk_percent=1.0, market="UK")

        assert result["valid"] is True
        assert result["stop_distance"] == 5.0
        assert result["risk_amount"] == 100.0
        assert result["suggested_shares"] == 20.0
        # gross_cost = 20*100=2000; stamp_duty=round_half_up(2000*0.005)=10.0; commission=9.95
        assert result["estimated_fees"] == 19.95
        assert result["estimated_cost"] == 2019.95

    def test_ps02_uk_floor_required_non_terminating_decimal(self):
        database.get_portfolio.return_value = _mock_portfolio(cash=100000.0)
        database.get_latest_snapshot.return_value = _mock_snapshot(25000.0)
        database.get_settings.return_value = [{}]

        result = size_position(entry_price=150.25, stop_price=142.0, risk_percent=1.5, market="UK")

        assert result["valid"] is True
        assert result["stop_distance"] == 8.25
        assert result["risk_amount"] == 375.0
        assert result["suggested_shares"] == 45.4545

    def test_ps03_uk_small_risk_round_result(self):
        database.get_portfolio.return_value = _mock_portfolio(cash=8000.0)
        database.get_latest_snapshot.return_value = _mock_snapshot(8000.0)
        database.get_settings.return_value = [{}]

        result = size_position(entry_price=75.0, stop_price=73.0, risk_percent=0.75, market="UK")

        assert result["valid"] is True
        assert result["stop_distance"] == 2.0
        assert result["risk_amount"] == 60.0
        assert result["suggested_shares"] == 30.0

    def test_invalid_stop_distance_rejected(self):
        # §4.1.4 validity: stop_price >= entry_price is invalid regardless of DB state
        result = size_position(entry_price=100.0, stop_price=100.0, risk_percent=1.0, market="UK")
        assert result["valid"] is False
        assert result["reason"] == "INVALID_STOP_DISTANCE"

    def test_cash_insufficient_includes_max_affordable_shares(self):
        # Large suggested position vs. tiny available cash -> §4.1.6 gate
        database.get_portfolio.return_value = _mock_portfolio(cash=10.0)
        database.get_latest_snapshot.return_value = _mock_snapshot(10000.0)
        database.get_settings.return_value = [{}]

        result = size_position(entry_price=100.0, stop_price=95.0, risk_percent=1.0, market="UK")

        assert result["valid"] is True
        assert result["cash_sufficient"] is False
        assert "max_affordable_shares" in result


class TestDatabaseMockIsolation:
    """ST-41 (BLG-QA-201, v9.11): the golden-vector tests are order-independent."""

    def test_unconfigured_mock_fails_loudly(self):
        with pytest.raises(AssertionError, match="database.get_portfolio was not configured"):
            size_position(entry_price=100.0, stop_price=95.0, risk_percent=1.0, market="UK")

    def test_a_test_sees_fresh_mocks_not_another_tests_values(self):
        assert isinstance(database.get_portfolio.return_value, _Unconfigured)
        assert isinstance(database.get_latest_snapshot.return_value, _Unconfigured)
        assert isinstance(database.get_settings.return_value, _Unconfigured)



# ---------------------------------------------------------------------------
# ST-39 (BLG-QA-199, EPIC-06, v9.11): size_position's US-market path
# (strategy_rules.md §4.1.5 FX handling) and size_batch_inv_vol.
# ---------------------------------------------------------------------------

class TestSizePositionUSMarket:
    def _configure(self, cash=10000.0, value=10000.0, settings=None):
        database.get_portfolio.return_value = _mock_portfolio(cash=cash)
        database.get_latest_snapshot.return_value = _mock_snapshot(value)
        database.get_settings.return_value = [settings or {}]

    def test_us_with_explicit_fx_rate(self):
        self._configure()
        result = size_position(entry_price=100.0, stop_price=95.0, risk_percent=1.0, market="US", fx_rate=1.25)
        # risk 100 GBP / (5 USD x 1.25) = 16 shares
        assert result["valid"] is True
        assert result["fx_rate_used"] == 1.25
        assert result["suggested_shares"] == 16.0
        assert result["risk_amount"] == 100.0
        # gross 1,600 USD; fx fee round_half_up(1600 x 0.0015) = 2.40 USD; commission 0
        assert result["estimated_fees"] == 1.92          # 2.40 / 1.25
        assert result["estimated_cost"] == 1281.92       # (1600 + 2.40) / 1.25
        assert result["cash_sufficient"] is True

    def test_us_uses_live_fx_when_no_override(self):
        self._configure()
        with patch.object(sizing_service, "get_live_fx_rate", return_value=1.6) as live:
            result = size_position(entry_price=100.0, stop_price=95.0, risk_percent=1.0, market="US")
        live.assert_called_once()
        assert result["fx_rate_used"] == 1.6
        assert result["suggested_shares"] == 12.5         # 100 / (5 x 1.6)

    def test_uk_never_reads_live_fx(self):
        self._configure()
        with patch.object(sizing_service, "get_live_fx_rate", side_effect=AssertionError("UK must not use FX")):
            result = size_position(entry_price=100.0, stop_price=95.0, risk_percent=1.0, market="UK", fx_rate=1.25)
        assert result["fx_rate_used"] == 1.0

    def test_us_custom_fee_settings(self):
        self._configure(settings={"us_commission": 2.0, "fx_fee_rate": 0.01})
        result = size_position(entry_price=100.0, stop_price=95.0, risk_percent=1.0, market="US", fx_rate=1.25)
        # fees: commission 2 + 1% of 1,600 = 18 USD -> 14.40 GBP
        assert result["estimated_fees"] == 14.4
        assert result["estimated_cost"] == 1294.4         # (1600 + 18) / 1.25

    def test_us_cash_insufficient_max_affordable_uses_fx_and_fx_fee(self):
        self._configure(cash=100.0)
        result = size_position(entry_price=100.0, stop_price=95.0, risk_percent=1.0, market="US", fx_rate=1.25)
        assert result["cash_sufficient"] is False
        # 100 GBP / (100 x 1.0015 / 1.25) = 1.24813..., floored to 4 dp
        assert result["max_affordable_shares"] == 1.2481


def _signal(atr, price_gbp, market="UK", current_price=None):
    return {"atr_value": atr, "price_gbp": price_gbp, "current_price": current_price or price_gbp, "market": market}


class TestSizeBatchInvVol:
    @pytest.fixture(autouse=True)
    def _settings(self):
        database.get_settings.return_value = [{}]

    def test_weights_capped_then_renormalised(self):
        # inverse ATR 1, 0.5, 0.25 -> raw 0.5714/0.2857/0.1429; cap at 0.20 ->
        # 0.20/0.20/0.1429; renormalised -> 0.368421/0.368421/0.263158
        out = sizing_service.size_batch_inv_vol([_signal(1, 100), _signal(2, 50), _signal(4, 10)], 10000)
        assert [s["inv_vol_weight"] for s in out] == [0.368421, 0.368421, 0.263158]
        assert [s["allocation_gbp"] for s in out] == [3684.21, 3684.21, 2631.58]
        assert [s["suggested_shares"] for s in out] == [36, 73, 263]
        assert all(s["reason"] is None for s in out)

    def test_minimum_weight_floor_applies(self):
        # one very volatile signal among calm ones: raw weight below 5% is raised to 5%
        sigs = [_signal(1, 10)] * 1 + [_signal(1, 10) for _ in range(9)] + [_signal(100, 10)]
        out = sizing_service.size_batch_inv_vol(sigs, 10000)
        raw_small = (1 / 100) / (10 + 1 / 100)
        assert raw_small < 0.05
        calm_raw = 1 / (10 + 1 / 100)                       # each calm signal, within the caps
        expected_small = 0.05 / (10 * calm_raw + 0.05)      # capped values renormalised
        assert out[-1]["inv_vol_weight"] == round(expected_small, 6)

    def test_whole_shares_floor_not_round(self):
        out = sizing_service.size_batch_inv_vol([_signal(1, 300)], 999)
        # single signal: raw 1.0 capped to 0.20, renormalised back to 1.0; 999 / 300 = 3.33 -> 3
        assert out[0]["inv_vol_weight"] == 1.0
        assert out[0]["suggested_shares"] == 3

    def test_missing_price_gets_zero_shares_with_reason(self):
        out = sizing_service.size_batch_inv_vol([_signal(1, 0), _signal(1, 50)], 1000)
        assert out[0]["suggested_shares"] == 0
        assert out[0]["total_cost"] == 0
        assert out[0]["reason"] == "Inv-vol sizing: price_gbp unavailable"

    def test_allocation_too_small_for_one_share(self):
        out = sizing_service.size_batch_inv_vol([_signal(1, 5000)], 1000)
        assert out[0]["suggested_shares"] == 0
        assert out[0]["total_cost"] == 0
        assert out[0]["reason"] == "Inv-vol sizing yielded 0 shares for this allocation"

    def test_no_valid_atr_sizes_nothing(self):
        out = sizing_service.size_batch_inv_vol([_signal(0, 10), _signal(None, 10)], 1000)
        assert all(s["suggested_shares"] == 0 and s["inv_vol_weight"] == 0 for s in out)
        assert out[0]["reason"] == "Inv-vol sizing: no valid ATR values"
