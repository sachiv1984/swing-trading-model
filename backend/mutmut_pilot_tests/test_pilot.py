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
from unittest.mock import patch

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
