"""
US/UK x FX matrix for every money path that derives a native entry price.

Why this file exists (2026-11-12, quality review after v9.16): US/UK and FX
bugs were the most frequent class of defect found in v9.12-v9.16
(BLG-BE-209, BLG-BE-210, BLG-FE-281, BLG-QA-254). Each was fixed on one path
while the same fallback, copied elsewhere, stayed wrong. This file runs one
shared matrix of position rows through every implementation, so a copy that
disagrees fails here even when its own story's tests pass.

The matrix: UK, and US with fill_price present or NULL x fx_rate present or
NULL. positions.entry_price is GBP for every market
(data_model_positions_dictionary.md v0.4). For a US row the native entry is
fill_price, else entry_price x the stored fx_rate, else entry_price x the
live rate.

Known disagreements are marked xfail(strict=True) with the backlog item that
fixes them. When the fix lands the xfail turns into an XPASS failure, which
tells the implementer to remove the marker.

New money path? Add it to this matrix in the same commit.

No database or network: every collaborator is patched.
"""
import re
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from routers import portfolio_risk
from services import portfolio_service
from services.position_lifecycle_service import _native_entry
from services.position_service import native_entry_price
from services.trade_service import _compute_net_r

LIVE_FX = 1.30
SHARES = 10
INITIAL_STOP_NATIVE = 90.0
REPO_ROOT = Path(__file__).resolve().parent.parent


def _row(market, fill_price, fx_rate, entry_price):
    return {
        "id": "pos-1", "portfolio_id": "pf-1",
        "ticker": "VOD.L" if market == "UK" else "MU", "market": market,
        "entry_date": str(date.today() - timedelta(days=20)),
        "entry_price": entry_price, "fill_price": fill_price, "fx_rate": fx_rate,
        "shares": SHARES, "current_price": None, "current_stop": 92.0,
        "initial_stop": INITIAL_STOP_NATIVE, "holding_days": 20, "atr": 4.0,
        "status": "open",
    }


# (id, row, expected native entry, GBP rate the entry was bought at)
MATRIX = [
    ("UK", _row("UK", None, 1.0, 100.0), 100.0, 1.0),
    ("US-fill-fx", _row("US", 100.0, 1.25, 80.0), 100.0, 1.25),
    ("US-nofill-fx", _row("US", None, 1.25, 80.0), 100.0, 1.25),
    ("US-fill-nofx", _row("US", 100.0, None, 80.0), 100.0, LIVE_FX),
    ("US-nofill-nofx", _row("US", None, None, 80.0), 80.0 * LIVE_FX, LIVE_FX),
]
IDS = [m[0] for m in MATRIX]
CASES = [m[1:] for m in MATRIX]

# portfolio_risk.py falls back to a hard-coded 1.27 for a NULL fx_rate, where
# every other path uses the live rate (found 2026-11-12 by this matrix).
_HARDCODED_127 = pytest.mark.xfail(
    strict=True,
    reason="BLG-BE-213: portfolio_risk.py uses a hard-coded 1.27 when fx_rate is NULL; other paths use the live rate",
)


def _with_marks(case_ids_to_mark, mark):
    return [
        pytest.param(*case, id=case_id, marks=[mark] if case_id in case_ids_to_mark else [])
        for case_id, case in zip(IDS, CASES)
    ]


@contextmanager
def _fake_db():
    yield MagicMock()


def _portfolio_summary_position(row, live_price):
    with patch.object(portfolio_service, "get_db", _fake_db), \
         patch.object(portfolio_service, "get_portfolio", return_value={"id": "pf-1", "cash": 1000.0, "last_updated": "x"}), \
         patch.object(portfolio_service, "get_positions", return_value=[row]), \
         patch.object(portfolio_service, "get_current_price", return_value=live_price), \
         patch.object(portfolio_service, "get_live_fx_rate", return_value=LIVE_FX), \
         patch.object(portfolio_service, "get_total_deposits_withdrawals", return_value={"net_cash_flow": 0.0}), \
         patch.object(portfolio_service, "get_drawdown_fields",
                      return_value={"current_drawdown_percent": 0.0, "peak_portfolio_value": 0.0}):
        summary = portfolio_service.get_portfolio_summary()
    return summary["positions"][0], summary["position_risks"][0]["position_risk_gbp"]


def _expected_risk_gbp(expected_native, buy_rate):
    return round((expected_native - INITIAL_STOP_NATIVE) * SHARES / buy_rate, 2)


class TestNativeEntryAgreesOnEveryPath:

    @pytest.mark.parametrize("row,expected_native,buy_rate", CASES, ids=IDS)
    def test_position_service_native_entry_price(self, row, expected_native, buy_rate):
        assert native_entry_price(row, LIVE_FX) == pytest.approx(expected_native)

    @pytest.mark.parametrize("row,expected_native,buy_rate", CASES, ids=IDS)
    def test_lifecycle_badge_native_entry(self, row, expected_native, buy_rate):
        with patch("utils.pricing.get_live_fx_rate", return_value=LIVE_FX):
            assert _native_entry({**row, "live_fx_rate": LIVE_FX}) == pytest.approx(expected_native)

    @pytest.mark.parametrize("row,expected_native,buy_rate", CASES, ids=IDS)
    def test_portfolio_summary_pnl_uses_the_native_entry(self, row, expected_native, buy_rate):
        live_price = 120.0
        position, _ = _portfolio_summary_position(row, live_price)
        fx = LIVE_FX if row["market"] == "US" else 1.0
        derived_native = live_price - position["pnl"] * fx / SHARES
        assert derived_native == pytest.approx(expected_native, abs=0.01)

    @pytest.mark.parametrize("row,expected_native,buy_rate", CASES, ids=IDS)
    def test_portfolio_summary_stale_price_falls_back_to_the_native_entry(self, row, expected_native, buy_rate):
        # No live price and no stored price: current price is the native entry.
        position, _ = _portfolio_summary_position(row, None)
        fx = LIVE_FX if row["market"] == "US" else 1.0
        assert position["price_is_stale"] is True
        assert position["current_price"] == pytest.approx(round(expected_native / fx, 2))

    @pytest.mark.parametrize("row,expected_native,buy_rate", _with_marks({"US-nofill-nofx"}, _HARDCODED_127))
    def test_sector_exposure_values_a_priceless_position_at_its_native_entry(self, row, expected_native, buy_rate):
        uk_anchor = {**_row("UK", None, 1.0, 100.0), "ticker": "BP.L", "current_price": 100.0}
        sectors = {"MU": "Technology", "VOD.L": "Telecom", "BP.L": "Energy"}
        result = portfolio_risk.compute_sector_exposure([row, uk_anchor], sectors, LIVE_FX)
        fx = LIVE_FX if row["market"] == "US" else 1.0
        value = expected_native / fx * SHARES
        expected_pct = round(value / (value + 1000.0) * 100, 1)
        sector = sectors[row["ticker"]]
        actual = next(s["exposure_pct"] for s in result["sectors"] if s["sector_name"] == sector)
        assert actual == expected_pct


class TestPositionRiskAgreesOnEveryPath:
    """Position risk = (native entry - initial stop) x shares, converted at the
    rate the position was bought at (metrics_definitions.md §Position Risk)."""

    @pytest.mark.parametrize("row,expected_native,buy_rate", CASES, ids=IDS)
    def test_portfolio_summary_position_risk(self, row, expected_native, buy_rate):
        _, risk = _portfolio_summary_position(row, 120.0)
        assert risk == pytest.approx(_expected_risk_gbp(expected_native, buy_rate), abs=0.01)

    @pytest.mark.parametrize("row,expected_native,buy_rate",
                             _with_marks({"US-fill-nofx", "US-nofill-nofx"}, _HARDCODED_127))
    def test_risk_page_position_risk(self, row, expected_native, buy_rate):
        with patch("utils.pricing.get_live_fx_rate", return_value=LIVE_FX), \
             patch.object(portfolio_risk, "get_db", _fake_db), \
             patch.object(portfolio_risk, "get_portfolio", return_value={"id": "pf-1", "cash": 1000.0}), \
             patch.object(portfolio_risk, "get_positions", return_value=[row]), \
             patch.object(portfolio_risk, "_get_ticker_sector_map", return_value={}):
            _, _, positions, *_ = portfolio_risk._get_portfolio_heat_and_positions()
        assert positions[0]["position_risk_gbp"] == pytest.approx(
            _expected_risk_gbp(expected_native, buy_rate), abs=0.01)


class TestNetRMultiple:
    """Net R = (P&L - costs) / initial risk in GBP. US risk is native, so it
    must be converted at the entry rate; with no entry rate it is unknown."""

    def _net_r(self, market, entry_fx_rate):
        return _compute_net_r(pnl=100.0, commission_gbp=5.0, spread_cost_gbp=5.0,
                              entry_price=100.0, stop_price_at_entry=90.0, shares=SHARES,
                              market=market, entry_fx_rate=entry_fx_rate)

    def test_uk_risk_is_already_gbp(self):
        assert self._net_r("UK", None) == pytest.approx(90.0 / 100.0, abs=0.001)

    def test_us_risk_is_converted_at_the_entry_rate(self):
        assert self._net_r("US", 1.25) == pytest.approx(90.0 / (100.0 / 1.25), abs=0.001)

    @pytest.mark.xfail(strict=True, reason="BLG-BE-209: _compute_net_r treats a NULL US entry_fx_rate as 1.0")
    def test_us_with_no_entry_rate_is_unknown_not_computed_at_1(self):
        # replay_service and reports_service already treat a NULL rate as unavailable.
        assert self._net_r("US", None) is None


# Each entry is (file, number of inline copies). BLG-BE-208 replaces them with
# one function; when a copy is removed, lower its count here.
KNOWN_INLINE_NATIVE_ENTRY_COPIES = {
    "backend/services/portfolio_service.py": 2,
    "backend/routers/portfolio_risk.py": 2,
}
_INLINE_PATTERN = re.compile(
    r"fill_price['\"]\)?\s*or\s*\(?\s*(?:[a-z_]+(?:\[|\.get\()['\"])?entry_price"
)


def test_no_new_inline_native_entry_fallback():
    """A new inline copy of the fill_price-or-entry_price fallback must not be
    added: call position_service.native_entry_price() instead (BLG-BE-208)."""
    found = {}
    for path in (REPO_ROOT / "backend").rglob("*.py"):
        if ".venv" in path.parts or "site-packages" in path.parts:
            continue
        count = len(_INLINE_PATTERN.findall(path.read_text(encoding="utf-8")))
        if count:
            found[str(path.relative_to(REPO_ROOT))] = count
    assert found == KNOWN_INLINE_NATIVE_ENTRY_COPIES, (
        "Inline native-entry fallbacks changed. Use position_service.native_entry_price() "
        "rather than adding a copy; if you removed one, lower its count here."
    )
