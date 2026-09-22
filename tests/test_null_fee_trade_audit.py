"""
ST-07 (BLG-FR-04, EPIC-02, v9.6): Audit whether closed-trade P&L is net of
fees_paid; flag closed trades with NULL entry_fees/exit_fees in Monthly P&L.

Tests get_monthly_pnl_report() in isolation (database layer mocked) -- same
convention as test_reports_integration.py / test_monthly_pnl_cost_basis.py.
No live DB or network connections are made.
"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.reports_service import get_monthly_pnl_report  # noqa: E402

MOCK_PORTFOLIO = {"id": "portfolio-test-001"}

PATCH_GET_PORTFOLIO = "services.reports_service.get_portfolio"
PATCH_GET_MONTHLY_PNL = "services.reports_service.get_monthly_pnl"
PATCH_GET_POSITIONS = "services.reports_service.get_positions"


@patch(PATCH_GET_POSITIONS, return_value=[])
@patch(PATCH_GET_MONTHLY_PNL, return_value=[
    {"year": 2026, "month": 5, "realised_pnl_gbp": 100.0, "trade_count": 2, "null_fee_trade_count": 1},
    {"year": 2026, "month": 4, "realised_pnl_gbp": 50.0, "trade_count": 1, "null_fee_trade_count": 0},
])
@patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
def test_null_fee_trade_count_passed_through_per_month(*_):
    report = get_monthly_pnl_report()
    months = report["months"]
    assert months[0]["null_fee_trade_count"] == 1
    assert months[1]["null_fee_trade_count"] == 0


@patch(PATCH_GET_POSITIONS, return_value=[])
@patch(PATCH_GET_MONTHLY_PNL, return_value=[
    {"year": 2026, "month": 5, "realised_pnl_gbp": 100.0, "trade_count": 2},
])
@patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
def test_null_fee_trade_count_defaults_to_zero_for_legacy_row_shape(*_):
    """A row shape predating this field (e.g. an older fixture) must not
    raise -- defaults to 0 rather than surfacing a KeyError."""
    report = get_monthly_pnl_report()
    assert report["months"][0]["null_fee_trade_count"] == 0


@patch(PATCH_GET_POSITIONS, return_value=[])
@patch(PATCH_GET_MONTHLY_PNL, return_value=[
    {"year": 2026, "month": 5, "realised_pnl_gbp": 100.0, "trade_count": 3, "null_fee_trade_count": 3},
])
@patch(PATCH_GET_PORTFOLIO, return_value=MOCK_PORTFOLIO)
def test_null_fee_trade_count_can_equal_trade_count(*_):
    """Every closed trade in the month missing a fee leg is a valid state
    (not clamped or silently dropped)."""
    report = get_monthly_pnl_report()
    month = report["months"][0]
    assert month["null_fee_trade_count"] == month["trade_count"] == 3


def test_get_monthly_pnl_sql_filters_on_either_fee_leg_null():
    """Mutation check on the SQL: the FILTER clause must use OR, not AND --
    a trade missing only one of entry_fees/exit_fees still has an unrecorded
    fee leg and must be counted (RISK-02: do not under-count)."""
    import inspect
    from database import get_monthly_pnl
    source = inspect.getsource(get_monthly_pnl)
    assert "null_fee_trade_count" in source
    assert "entry_fees IS NULL OR exit_fees IS NULL" in source
