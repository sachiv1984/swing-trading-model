"""
GET /portfolio and GET /positions carry the FX rate's source and fetch time
(ST-05, EPIC-01, v9.14, BLG-BE-169), from get_fx_rate_info() for the rate
the service fetched. No database or network: every collaborator is patched.
"""
from contextlib import contextmanager
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

from services import portfolio_service
import services.position_service as position_service

FX = {"fx_rate": 1.3301, "fx_rate_source": "last_known", "fx_rate_as_of": "2026-10-27T15:30:00+00:00"}


def _row():
    return {
        "id": "pos-us-1", "portfolio_id": "pf-1", "ticker": "MU", "market": "US",
        "entry_date": str(date.today() - timedelta(days=20)), "entry_price": 80.0, "fill_price": 100.0,
        "fx_rate": 1.25, "shares": 10, "current_price": 101.0, "current_stop": 92.0, "initial_stop": 90.0,
        "holding_days": 20, "total_cost": 800.0, "atr": 4.0, "status": "open",
    }


@contextmanager
def _fake_db():
    yield MagicMock()


def _portfolio(positions):
    with patch.object(portfolio_service, "get_db", _fake_db), \
         patch.object(portfolio_service, "get_portfolio", return_value={"id": "pf-1", "cash": 1000.0, "last_updated": "x"}), \
         patch.object(portfolio_service, "get_positions", return_value=positions), \
         patch.object(portfolio_service, "get_current_price", return_value=101.0), \
         patch.object(portfolio_service, "get_live_fx_rate", return_value=FX["fx_rate"]), \
         patch.object(portfolio_service, "get_fx_rate_info", return_value=FX) as info, \
         patch.object(portfolio_service, "get_total_deposits_withdrawals", return_value={"net_cash_flow": 0.0}), \
         patch.object(portfolio_service, "get_drawdown_fields",
                      return_value={"current_drawdown_percent": 0.0, "peak_portfolio_value": 0.0}):
        summary = portfolio_service.get_portfolio_summary()
    info.assert_called_with(FX["fx_rate"])
    return summary


def test_portfolio_reports_the_fx_source_with_positions():
    summary = _portfolio([_row()])
    assert summary["live_fx_rate"] == FX["fx_rate"]
    assert summary["fx_rate_source"] == "last_known"
    assert summary["fx_rate_as_of"] == FX["fx_rate_as_of"]


def test_portfolio_reports_the_fx_source_with_no_positions():
    summary = _portfolio([])
    assert summary["fx_rate_source"] == "last_known"
    assert summary["fx_rate_as_of"] == FX["fx_rate_as_of"]


def test_positions_report_the_fx_source():
    with patch.object(position_service, "get_portfolio", return_value={"id": "pf-1"}), \
         patch.object(position_service, "get_positions", return_value=[_row()]), \
         patch.object(position_service, "get_live_fx_rate", return_value=FX["fx_rate"]), \
         patch.object(position_service, "get_fx_rate_info", return_value=FX), \
         patch.object(position_service, "get_current_price", return_value=101.0), \
         patch.object(position_service, "get_sector_and_industry", return_value=(None, None)):
        position = position_service.get_positions_with_prices()[0]
    assert position["live_fx_rate"] == FX["fx_rate"]
    assert position["fx_rate_source"] == "last_known"
    assert position["fx_rate_as_of"] == FX["fx_rate_as_of"]
