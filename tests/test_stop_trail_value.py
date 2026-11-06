"""
ST-06 (BLG-BE-173, EPIC-01, v9.15): GET /positions/{position_id}/stop-trail's
atr_trail_stop is the §7.2 stop calculate_trailing_stop() produces for the
same inputs with the §11 multipliers (backend/strategy_parameters.py),
breakeven floor included, instead of current_price − 2.0 × ATR.

The real calculations module is loaded from its file, for the same
suite-order reason as tests/test_add_position_stop_handling.py.
"""
import importlib.util
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

BACKEND = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(BACKEND))

_spec = importlib.util.spec_from_file_location("_real_calculations_st06_v915", BACKEND / "utils" / "calculations.py")
real_calcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(real_calcs)

from strategy_parameters import PROFIT_ATR_MULTIPLIER, stop_multiplier_settings  # noqa: E402


def _client():
    from tests._real_database import real_database_imports
    with real_database_imports():
        from fastapi.testclient import TestClient
        import main
    return TestClient(main.app, raise_server_exceptions=False), main


@contextmanager
def _db_returning(row):
    cur = MagicMock()
    cur.fetchone.return_value = row
    cur.__enter__ = lambda s: cur
    cur.__exit__ = lambda s, *a: False
    conn = MagicMock()
    conn.cursor.return_value = cur
    conn.__enter__ = lambda s: conn
    conn.__exit__ = lambda s, *a: False
    yield conn


def _stop_trail(*, entry, price, atr, current_stop, initial_stop=None, market="US"):
    client, main = _client()
    row = {
        "id": "pos-1", "ticker": "AAPL" if market == "US" else "LGEN.L", "market": market,
        "entry_price": entry, "initial_stop": initial_stop, "current_stop": current_stop, "atr": atr,
        "trade_plan_id": None, "r_target": None,
    }
    import database
    with _db_returning(row) as conn, \
         patch.object(database, "get_db", return_value=conn), \
         patch.object(database, "log_trailing_stop_recommendation"), \
         patch.object(main, "get_portfolio", return_value={"id": "portfolio-1"}), \
         patch.object(main, "get_current_price", return_value=price), \
         patch.object(main, "calculate_trailing_stop", new=real_calcs.calculate_trailing_stop):
        response = client.get("/positions/pos-1/stop-trail")
    assert response.status_code == 200, response.text
    return response.json()["data"]


def _expected(price, atr, entry, profitable):
    value, _, _ = real_calcs.calculate_trailing_stop(
        current_price=price, atr=atr, is_profitable=profitable,
        current_stop=float("-inf"), entry_price=entry, settings=stop_multiplier_settings(),
    )
    return round(value, 4)


class TestAtrTrailStopMatchesLiveFormula:
    def test_profitable_position_uses_the_profit_multiplier(self):
        data = _stop_trail(entry=100.0, price=130.0, atr=4.0, current_stop=110.0)
        assert data["atr_trail_stop"] == _expected(130.0, 4.0, 100.0, True)
        assert data["atr_trail_stop"] == round(130.0 - PROFIT_ATR_MULTIPLIER * 4.0, 4)

    def test_breakeven_floor_binds(self):
        # 105 − 2 × 4 = 97 is below the entry of 100, so the floor gives 100.
        data = _stop_trail(entry=100.0, price=105.0, atr=4.0, current_stop=90.0)
        assert data["atr_trail_stop"] == _expected(105.0, 4.0, 100.0, True)
        assert data["atr_trail_stop"] == 100.0
        assert data["trail_difference"] == 10.0

    def test_trail_difference_stays_signed_when_the_stop_is_already_higher(self):
        data = _stop_trail(entry=100.0, price=130.0, atr=4.0, current_stop=125.0)
        assert data["atr_trail_stop"] == 122.0
        assert data["trail_difference"] == -3.0
        assert data["recommendation"] == "Trail stop is below current stop — no action required"

    @pytest.mark.parametrize("entry,price,atr", [(100.0, 140.0, 3.5), (250.0, 251.0, 2.0), (72.18, 80.0, 1.0449)])
    def test_matches_calculate_trailing_stop(self, entry, price, atr):
        data = _stop_trail(entry=entry, price=price, atr=atr, current_stop=None)
        assert data["atr_trail_stop"] == _expected(price, atr, entry, price > entry)


def test_no_literal_multiplier_in_the_handler():
    source = (BACKEND / "main.py").read_text()
    start = source.index('@app.get("/positions/{position_id}/stop-trail")')
    end = source.index('if __name__ == "__main__":', start)
    handler = source[start:end]
    assert not re.search(r"atr\s*\*\s*\d", handler)
    assert "trail_multiplier = " not in handler
