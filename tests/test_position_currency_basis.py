"""
BLG-BE-103 regression tests (ST-02, EPIC-01, v8.9).

`initial_stop` is returned in native currency, but `current_trailing_stop`
and `stop_price` were converted to GBP for US-market positions while the
frontend renders all three stop fields with the position's native currency
symbol (derived from `position.market`) — producing a mismatched-basis
number on the Trail Stop tile (see PositionCard.js / Positions.js).

Fix: `current_trailing_stop_native` is now included in
get_positions_with_prices()'s response alongside the pre-existing
`stop_price_native`, giving every stop field an unambiguous native-currency
sibling for the frontend to pair with the native currency symbol.

This test verifies the currency-basis contract directly against
get_positions_with_prices() for a profitable US-market position, using the
same numbers documented in BLG-BE-103's own worked example
(WDC: native current_stop $163.31, live_fx_rate 1.3558).
"""
import os
import sys
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.position_service as position_service  # noqa: E402


def _us_position(current_stop=163.31, entry_price=434.30):
    entry_date = (date.today() - timedelta(days=20)).isoformat()
    return {
        "id": "pos-wdc",
        "ticker": "WDC",
        "market": "US",
        "entry_price": entry_price,
        "entry_date": entry_date,
        "shares": 10,
        "initial_stop": 163.31,
        "current_stop": current_stop,
        "current_price": 508.80,
        "atr": 54.1986,
        "fx_rate": 1.27,
        "total_cost": entry_price * 10,
        "position_state": "PROFITABLE",
        "state_history": [],
        "state_entered_at": None,
        "risk_off_exit": False,
        "last_reviewed_at": None,
    }


class TestCurrentTrailingStopNativeField:
    def test_native_field_present_and_unconverted_for_us_position(self):
        live_fx_rate = 1.3558
        pos = _us_position()

        with patch.object(position_service, "get_portfolio", return_value={"id": "pf-1"}), \
             patch.object(position_service, "get_positions", return_value=[pos]), \
             patch.object(position_service, "get_current_price", return_value=508.80), \
             patch.object(position_service, "get_live_fx_rate", return_value=live_fx_rate), \
             patch.object(position_service, "get_sector_and_industry", return_value=("Technology", "Hardware")), \
             patch.object(position_service, "compute_grace_days_remaining", return_value=0):
            result = position_service.get_positions_with_prices()

        assert len(result) == 1
        row = result[0]

        # initial_stop is native (pre-existing, unconverted)
        assert row["initial_stop"] == 163.31

        # stop_price_native (pre-existing) and current_trailing_stop_native
        # (new, BLG-BE-103) must both be native-currency and therefore equal
        # to each other for a position whose stop hasn't moved this run.
        assert row["current_trailing_stop_native"] == 163.31
        assert row["stop_price_native"] == 163.31

        # current_trailing_stop remains GBP-converted (unchanged contract for
        # existing consumers, e.g. portfolio-level aggregation) — must differ
        # from the native value by the live FX rate for a US position.
        assert row["current_trailing_stop"] == round(163.31 / live_fx_rate, 2)
        assert row["current_trailing_stop"] != row["current_trailing_stop_native"]

    def test_native_and_gbp_fields_equal_for_uk_position(self):
        """UK positions have no currency conversion at all — native and GBP
        fields must be identical (sanity check that the new field doesn't
        introduce a UK regression)."""
        pos = _us_position()
        pos["market"] = "UK"
        pos["ticker"] = "TST.L"

        with patch.object(position_service, "get_portfolio", return_value={"id": "pf-1"}), \
             patch.object(position_service, "get_positions", return_value=[pos]), \
             patch.object(position_service, "get_current_price", return_value=508.80), \
             patch.object(position_service, "get_live_fx_rate", return_value=1.3558), \
             patch.object(position_service, "get_sector_and_industry", return_value=("Technology", "Hardware")), \
             patch.object(position_service, "compute_grace_days_remaining", return_value=0):
            result = position_service.get_positions_with_prices()

        row = result[0]
        assert row["current_trailing_stop"] == row["current_trailing_stop_native"]
        assert row["stop_price"] == row["stop_price_native"]
