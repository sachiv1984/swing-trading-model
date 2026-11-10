"""
ST-16 (BLG-BE-175, EPIC-05, v9.16): a US position with a NULL fill_price exits
without error, and the closed trade's native entry is entry_price x fx_rate.

positions.entry_price is GBP for every market (data_model_positions_dictionary.md
v0.4). exit_position() used to read the native entry as
position.get('fill_price', position['entry_price']), which returns None when the
key exists but is NULL; trade_history.entry_price is NOT NULL, so the exit
failed. It now uses native_entry_price(), the same fallback as the recompute
paths: fill_price, else entry_price x the stored fx_rate, else x the exit rate.

Runs the real exit_position() with only the DB layer mocked (same pattern as
tests/test_trade_parameter_snapshot.py) and checks the trade_history row and
the response.
"""
import sys
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent))

import services.position_service as position_service  # noqa: E402

EXIT_FX = 1.30


def _us_position(**overrides):
    position = {
        "id": "pos-1",
        "ticker": "AAPL",
        "market": "US",
        "status": "open",
        "shares": 10,
        "total_cost": 800.0,
        "fees_paid": 0.0,
        "entry_price": 80.0,   # GBP
        "fx_rate": 1.25,       # USD per GBP at entry
        "fill_price": None,
        "entry_date": "2026-10-01",
        "atr": None,
        "active_atr_multiplier": None,
    }
    position.update(overrides)
    return position


def _exit(position, exit_price=130.0, shares=None):
    writes = []
    with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 0.0}), \
         patch.object(position_service, "get_positions", return_value=[position]), \
         patch.object(position_service, "get_settings", return_value=[{"fx_fee_rate": 0}]), \
         patch.object(position_service, "update_portfolio_cash"), \
         patch.object(position_service, "create_trade_history", side_effect=lambda pid, td: writes.append(td)), \
         patch.object(position_service, "update_position"), \
         patch.object(position_service, "get_trade_plans_by_position", return_value=[]), \
         patch.object(position_service, "ensure_planned_entry_price_column", return_value=None):
        result = position_service.exit_position(
            position_id="pos-1", exit_price=exit_price, shares=shares,
            exit_date="2026-11-10", exit_fx_rate=EXIT_FX,
        )
    assert len(writes) == 1
    return result, writes[0]


def test_null_fill_price_uses_entry_price_times_stored_fx_rate():
    result, row = _exit(_us_position())
    # Native entry: £80 x 1.25 = $100.
    assert row["entry_price"] == pytest.approx(100.0)
    assert row["entry_fx_rate"] == pytest.approx(1.25)
    # Realised P&L: net proceeds $1,300 / 1.30 = £1,000, less the £800 cost.
    assert result["realized_pnl"] == pytest.approx(200.0, abs=0.01)
    assert row["pnl"] == pytest.approx(result["realized_pnl"], abs=0.01)


def test_null_fill_price_and_null_fx_rate_falls_back_to_the_exit_rate():
    _, row = _exit(_us_position(fx_rate=None))
    assert row["entry_price"] == pytest.approx(80.0 * EXIT_FX)
    # The entry rate is unknown, so it is not invented.
    assert row["entry_fx_rate"] is None


def test_decimal_columns_from_the_database_are_handled():
    # get_positions() returns NUMERIC columns as Decimal; Decimal x float raises.
    position = _us_position(entry_price=Decimal("80.0000"), fx_rate=Decimal("1.2500"))
    _, row = _exit(position)
    assert row["entry_price"] == pytest.approx(100.0)


def test_partial_exit_with_null_fill_price():
    result, row = _exit(_us_position(), shares=4)
    assert row["entry_price"] == pytest.approx(100.0)
    assert result["is_partial_exit"] is True


def test_stored_fill_price_is_still_used_when_present():
    _, row = _exit(_us_position(fill_price=101.5))
    assert row["entry_price"] == pytest.approx(101.5)


def test_uk_exit_is_unchanged():
    position = _us_position(ticker="VOD.L", market="UK", fx_rate=None, entry_price=1.20, total_cost=12.0)
    writes = []
    with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 0.0}), \
         patch.object(position_service, "get_positions", return_value=[position]), \
         patch.object(position_service, "get_settings", return_value=[{"uk_commission": 0, "stamp_duty_rate": 0}]), \
         patch.object(position_service, "update_portfolio_cash"), \
         patch.object(position_service, "create_trade_history", side_effect=lambda pid, td: writes.append(td)), \
         patch.object(position_service, "update_position"), \
         patch.object(position_service, "get_trade_plans_by_position", return_value=[]), \
         patch.object(position_service, "ensure_planned_entry_price_column", return_value=None):
        position_service.exit_position(position_id="pos-1", exit_price=1.30, exit_date="2026-11-10")
    assert writes[0]["entry_price"] == pytest.approx(1.20)
    assert writes[0]["entry_fx_rate"] == 1.0
