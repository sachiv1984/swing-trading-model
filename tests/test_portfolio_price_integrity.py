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
