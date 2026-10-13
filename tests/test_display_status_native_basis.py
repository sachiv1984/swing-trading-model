"""
ST-13 (BLG-BE-149, EPIC-02, v9.12): the Risk page's LOSING/PROFITABLE
(`display_status`, from GET /portfolio and GET /positions) and the lifecycle
badge (`position_state`) are both decided on native P&L, so they agree for a
US position whatever FX does.

The fixture position: bought at $100 (fill_price) with fx 1.25, so
positions.entry_price is £80.00 (GBP for every market, dictionary v0.4).
  - At $101 with live FX 1.30, native P&L is +$10, but the GBP value
    (101 / 1.30 = £77.69) is below the £80.00 GBP cost: GBP P&L < 0.
  - At $95, native P&L is −$50. Before v9.12 the badge compared the GBP
    entry (£80) with the USD price ($95) and showed PROFITABLE.

No database or network: every collaborator is patched.
"""
from contextlib import contextmanager
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pytest

from services import portfolio_service
import services.position_service as position_service
from services.position_lifecycle_service import compute_position_state

LIVE_FX = 1.30


def _us_row(**overrides):
    row = {
        "id": "pos-us-1", "portfolio_id": "pf-1", "ticker": "MU", "market": "US",
        "entry_date": str(date.today() - timedelta(days=20)), "entry_price": 80.0, "fill_price": 100.0,
        "fx_rate": 1.25, "shares": 10, "current_price": 101.0, "current_stop": 92.0, "initial_stop": 90.0,
        "holding_days": 20, "total_cost": 800.0, "atr": 4.0, "status": "open",
    }
    row.update(overrides)
    return row


@contextmanager
def _fake_db():
    yield MagicMock()


def _portfolio_display_status(row, live_price):
    with patch.object(portfolio_service, "get_db", _fake_db), \
         patch.object(portfolio_service, "get_portfolio", return_value={"id": "pf-1", "cash": 1000.0, "last_updated": "x"}), \
         patch.object(portfolio_service, "get_positions", return_value=[row]), \
         patch.object(portfolio_service, "get_current_price", return_value=live_price), \
         patch.object(portfolio_service, "get_live_fx_rate", return_value=LIVE_FX), \
         patch.object(portfolio_service, "get_total_deposits_withdrawals", return_value={"net_cash_flow": 0.0}), \
         patch.object(portfolio_service, "get_drawdown_fields",
                      return_value={"current_drawdown_percent": 0.0, "peak_portfolio_value": 0.0}):
        return portfolio_service.get_portfolio_summary()["positions"][0]["display_status"]


def _positions_display_status(row, live_price):
    with patch.object(position_service, "get_portfolio", return_value={"id": "pf-1"}), \
         patch.object(position_service, "get_positions", return_value=[row]), \
         patch.object(position_service, "get_live_fx_rate", return_value=LIVE_FX), \
         patch.object(position_service, "get_current_price", return_value=live_price), \
         patch.object(position_service, "get_sector_and_industry", return_value=(None, None)), \
         patch.object(position_service, "calculate_position_pnl",
                      side_effect=lambda entry_price, current_price, shares, market, live_fx_rate: (
                          (current_price - entry_price) * shares,
                          (current_price - entry_price) * shares / (live_fx_rate if market == "US" else 1),
                          0.0)):
        return position_service.get_positions_with_prices()[0]["display_status"]


def _badge(row, price):
    return compute_position_state({**row, "current_price": price})


class TestUsDisplayStatusAgreesWithBadge:

    def test_native_gain_with_gbp_loss_is_profitable_everywhere(self):
        row = _us_row()
        assert 101.0 / LIVE_FX < row["entry_price"]  # GBP P&L < 0 against the GBP cost
        assert _badge(row, 101.0) == "PROFITABLE"
        assert _portfolio_display_status(row, 101.0) == "PROFITABLE"
        assert _positions_display_status(row, 101.0) == "PROFITABLE"

    def test_native_loss_near_entry_is_losing_everywhere(self):
        row = _us_row(current_price=95.0)
        assert _badge(row, 95.0) == "LOSING"
        assert _portfolio_display_status(row, 95.0) == "LOSING"
        assert _positions_display_status(row, 95.0) == "LOSING"

    @pytest.mark.parametrize("price,expected", [(101.0, "PROFITABLE"), (95.0, "LOSING")])
    def test_null_fill_price_uses_entry_times_fx(self, price, expected):
        row = _us_row(fill_price=None)  # native entry = £80 × 1.25 = $100
        assert _badge(row, price) == expected
        assert _portfolio_display_status(row, price) == expected
        assert _positions_display_status(row, price) == expected

    def test_us_badge_without_any_native_entry_is_unknown(self):
        assert _badge(_us_row(fill_price=None, fx_rate=None), 101.0) == "UNKNOWN"

    def test_uk_badge_unchanged(self):
        row = _us_row(market="UK", ticker="VOD.L", entry_price=100.0, fill_price=None, fx_rate=1.0)
        assert _badge(row, 101.0) == "PROFITABLE"
        assert _badge(row, 99.0) == "LOSING"
