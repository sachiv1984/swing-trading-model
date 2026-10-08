"""
GET /portfolio price integrity (EPIC-02, v9.11).

ST-10 (BLG-BE-154): when the live price fetch fails, a US position's
current_price is its stored native price converted at the live FX rate,
never stored × 1.38, and price_is_stale is true.

get_portfolio_summary() is exercised with every collaborator patched: no
database, no network.
"""
from contextlib import contextmanager
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pytest

from services import portfolio_service

LIVE_FX = 1.35


@contextmanager
def _fake_db():
    yield MagicMock()


def _us_position(**overrides):
    pos = {
        "id": "pos-us-1", "ticker": "MU", "market": "US", "entry_date": str(date.today() - timedelta(days=20)),
        "entry_price": 100.0, "fill_price": 100.0, "shares": 10, "current_price": 120.0,
        "current_stop": 92.0, "initial_stop": 90.0, "fx_rate": 1.27, "holding_days": 20, "total_cost": 787.4,
    }
    pos.update(overrides)
    return pos


def _summary(positions, live_price=None):
    with patch.object(portfolio_service, "get_db", _fake_db), \
         patch.object(portfolio_service, "get_portfolio", return_value={"id": "pf-1", "cash": 1000.0, "last_updated": "x"}), \
         patch.object(portfolio_service, "get_positions", return_value=positions), \
         patch.object(portfolio_service, "get_current_price", return_value=live_price), \
         patch.object(portfolio_service, "get_live_fx_rate", return_value=LIVE_FX), \
         patch.object(portfolio_service, "get_total_deposits_withdrawals", return_value={"net_cash_flow": 2000.0}), \
         patch.object(portfolio_service, "get_drawdown_fields",
                      return_value={"current_drawdown_percent": 0.0, "peak_portfolio_value": 0.0}):
        return portfolio_service.get_portfolio_summary()


class TestStalePriceFallback:
    def test_failed_fetch_uses_stored_native_price_at_live_fx(self):
        result = _summary([_us_position(current_price=120.0)], live_price=None)
        row = result["positions"][0]
        assert row["current_price"] == round(120.0 / LIVE_FX, 2)
        assert row["current_price"] != round(120.0 * 1.38 / LIVE_FX, 2)
        assert row["price_is_stale"] is True

    def test_low_us_price_is_not_treated_as_gbp(self):
        # The removed heuristic multiplied any US stored price below 500 by 1.38.
        result = _summary([_us_position(current_price=45.0)], live_price=None)
        assert result["positions"][0]["current_price"] == round(45.0 / LIVE_FX, 2)

    def test_missing_stored_price_falls_back_to_native_entry(self):
        result = _summary([_us_position(current_price=None, fill_price=101.0)], live_price=None)
        assert result["positions"][0]["current_price"] == round(101.0 / LIVE_FX, 2)
        assert result["positions"][0]["price_is_stale"] is True

    def test_live_price_is_not_stale(self):
        result = _summary([_us_position()], live_price=130.0)
        row = result["positions"][0]
        assert row["current_price"] == round(130.0 / LIVE_FX, 2)
        assert row["price_is_stale"] is False

    def test_no_hardcoded_fx_constant_in_service(self):
        from pathlib import Path
        src = Path(portfolio_service.__file__).read_text()
        assert "1.38" not in src


class TestHoldingDaysComputedLive:
    """ST-12 (BLG-BE-153): GET /portfolio computes holding_days from entry_date."""

    def test_stale_stored_holding_days_does_not_keep_a_position_in_grace(self):
        entry = (date.today() - timedelta(days=10)).isoformat()
        pos = _us_position(entry_date=entry, holding_days=9)
        row = _summary([pos], live_price=130.0)["positions"][0]
        assert row["holding_days"] == 10
        assert row["grace_period"] is False
        assert row["display_status"] == "PROFITABLE"
        assert row["grace_days_remaining"] is None

    def test_day_nine_is_still_grace(self):
        entry = (date.today() - timedelta(days=9)).isoformat()
        row = _summary([_us_position(entry_date=entry, holding_days=3)], live_price=130.0)["positions"][0]
        assert row["holding_days"] == 9
        assert row["display_status"] == "GRACE"
        assert row["grace_days_remaining"] == 1


class TestLiveHoldingDaysHelper:
    def test_date_object_string_and_datetime(self):
        from datetime import datetime
        from utils.calculations import live_holding_days
        d = date.today() - timedelta(days=4)
        assert live_holding_days({"entry_date": d}) == 4
        assert live_holding_days({"entry_date": d.isoformat()}) == 4
        assert live_holding_days({"entry_date": datetime.combine(d, datetime.min.time())}) == 4
        assert live_holding_days({"entry_date": f"{d.isoformat()}T00:00:00Z"}) == 4

    def test_falls_back_to_stored_value_only_without_entry_date(self):
        from utils.calculations import live_holding_days
        assert live_holding_days({"entry_date": None, "holding_days": 7}) == 7
        assert live_holding_days({"entry_date": "not-a-date", "holding_days": 3}) == 3

    def test_other_readers_no_longer_read_the_stored_column(self):
        """The other stored-holding_days readers named in BLG-BE-153 use the live value."""
        from pathlib import Path
        root = Path(portfolio_service.__file__).parent
        for name, stored_read in [
            ("alerts_service.py", 'holding_days = pos["holding_days"]'),
            ("compliance_service.py", 'holding_days = int(pos.get("holding_days")'),
            ("ai_service.py", 'holding_days = p.get("holding_days"'),
            ("portfolio_service.py", "holding_days = pos.get('holding_days'"),
        ]:
            src = (root / name).read_text()
            assert stored_read not in src, name
            assert "live_holding_days(" in src, name


class TestStopDistanceNative:
    """ST-13 (BLG-BE-155): stop_distance_pct is computed in native currency."""

    def test_us_example_from_the_acceptance_criteria(self):
        # Native price 100, native stop 92, entry FX 1.27, live FX 1.35 -> 8.0.
        pos = _us_position(fx_rate=1.27, current_stop=92.0)
        row = _summary([pos], live_price=100.0)["positions"][0]
        assert row["stop_distance_pct"] == 8.0
        # The GBP figures the browser used would have given a different answer.
        gbp_based = (row["current_price"] - row["current_stop"]) / row["current_price"] * 100
        assert round(gbp_based, 1) != 8.0

    def test_uk_position(self):
        pos = _us_position(market="UK", fill_price=None, entry_price=5.0, current_stop=4.5, fx_rate=1.0)
        row = _summary([pos], live_price=5.0)["positions"][0]
        assert row["stop_distance_pct"] == 10.0

    def test_null_when_no_stop(self):
        row = _summary([_us_position(current_stop=None)], live_price=100.0)["positions"][0]
        assert row["stop_distance_pct"] is None

    def test_negative_when_price_below_stop(self):
        row = _summary([_us_position(current_stop=105.0)], live_price=100.0)["positions"][0]
        assert row["stop_distance_pct"] == -5.0
