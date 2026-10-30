"""
ST-12 (BLG-BE-167, EPIC-02, v9.14): GET /portfolio's P&L block handles a US
position whose fill_price is NULL.

`pos.get('fill_price', pos['entry_price'])` returned None for a NULL column and
the P&L line raised TypeError. v9.12 (ST-13, BLG-BE-149, cc7774e9) changed it
to `fill_price or entry_price × fx_rate`; this pins that with a live price.

The fixture: entry_price £80.00 (GBP for every market) at fx 1.25, so the
native entry is $100. At a live $110 and live FX 1.30, native P&L is
10 × $10 = $100, i.e. £76.92, and pnl_pct is 10%.

No database or network: every collaborator is patched.
"""
from contextlib import contextmanager
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

from services import portfolio_service

LIVE_FX = 1.30


@contextmanager
def _fake_db():
    yield MagicMock()


def _portfolio_row(row, live_price):
    with patch.object(portfolio_service, "get_db", _fake_db), \
         patch.object(portfolio_service, "get_portfolio", return_value={"id": "pf-1", "cash": 1000.0, "last_updated": "x"}), \
         patch.object(portfolio_service, "get_positions", return_value=[row]), \
         patch.object(portfolio_service, "get_current_price", return_value=live_price), \
         patch.object(portfolio_service, "get_live_fx_rate", return_value=LIVE_FX), \
         patch.object(portfolio_service, "get_total_deposits_withdrawals", return_value={"net_cash_flow": 0.0}), \
         patch.object(portfolio_service, "get_drawdown_fields",
                      return_value={"current_drawdown_percent": 0.0, "peak_portfolio_value": 0.0}):
        return portfolio_service.get_portfolio_summary()["positions"][0]


def test_us_position_with_null_fill_price_uses_entry_price():
    row = {
        "id": "pos-us-1", "portfolio_id": "pf-1", "ticker": "MU", "market": "US",
        "entry_date": str(date.today() - timedelta(days=20)), "entry_price": 80.0, "fill_price": None,
        "fx_rate": 1.25, "shares": 10, "current_price": 105.0, "current_stop": 92.0, "initial_stop": 90.0,
        "holding_days": 20, "total_cost": 800.0, "atr": 4.0, "status": "open",
    }
    pos = _portfolio_row(row, live_price=110.0)
    assert pos["price_is_stale"] is False
    assert pos["pnl"] == round(10 * (110.0 - 100.0) / LIVE_FX, 2)  # £76.92
    assert pos["pnl_pct"] == 10.0
