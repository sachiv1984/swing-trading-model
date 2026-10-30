"""
GET /positions flags a stale price (ST-07, EPIC-01, v9.14, BLG-BE-168).

GET /portfolio has returned price_is_stale since v9.11; GET /positions showed
the stored price as live. Each position now carries the same flag: true when
the live fetch failed and the stored price is used. No database or network.
"""
from datetime import date, timedelta
from unittest.mock import patch

import services.position_service as position_service


def _row(ticker, stored_price):
    return {
        "id": f"pos-{ticker}", "portfolio_id": "pf-1", "ticker": ticker, "market": "US",
        "entry_date": str(date.today() - timedelta(days=20)), "entry_price": 80.0, "fill_price": 100.0,
        "fx_rate": 1.25, "shares": 10, "current_price": stored_price, "current_stop": 92.0, "initial_stop": 90.0,
        "holding_days": 20, "total_cost": 800.0, "atr": 4.0, "status": "open",
    }


def _positions(prices):
    with patch.object(position_service, "get_portfolio", return_value={"id": "pf-1"}), \
         patch.object(position_service, "get_positions", return_value=[_row("MU", 101.0), _row("WDC", 55.0)]), \
         patch.object(position_service, "get_live_fx_rate", return_value=1.30), \
         patch.object(position_service, "get_current_price", side_effect=lambda t: prices[t]), \
         patch.object(position_service, "get_sector_and_industry", return_value=(None, None)):
        return {p["ticker"]: p for p in position_service.get_positions_with_prices()}


def test_failed_fetch_marks_the_position_stale_and_uses_the_stored_price():
    positions = _positions({"MU": None, "WDC": 60.0})
    assert positions["MU"]["price_is_stale"] is True
    assert positions["MU"]["current_price_native"] == 101.0


def test_live_price_is_not_stale():
    positions = _positions({"MU": None, "WDC": 60.0})
    assert positions["WDC"]["price_is_stale"] is False
    assert positions["WDC"]["current_price_native"] == 60.0
