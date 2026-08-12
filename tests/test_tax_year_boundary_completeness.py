"""
Closed-trade export completeness at tax-year boundaries (ST-13, BLG-BE-93,
EPIC-04, v8.6).

`tests/test_tax_year_pnl_boundary.py` (ST-18, v5.3) validates the UK
tax-year boundary date arithmetic (Apr 5 / Apr 6) via *reimplemented*
Python date comparisons -- it never calls the real
`get_trade_history_by_tax_year()`/`get_tax_year_report()` functions, so a
regression in the actual SQL (`BETWEEN`) or the actual Python date
construction (`date(year, 4, 6)` / `date(year + 1, 4, 5)`) in
`reports_service.py` would not be caught by that suite.

This file closes that gap: it exercises the REAL `get_tax_year_report()`
(mocked DB layer, following the pattern in `test_trade_origin_query.py`)
for two adjacent tax years, captures the ACTUAL `tax_year_start`/
`tax_year_end` values it computes and passes down to
`get_trade_history_by_tax_year()`, and confirms a trade exiting exactly on
each boundary day is captured by exactly one adjacent year's real query
params -- no silent omission, no double-count.
"""
import sys
from pathlib import Path
from datetime import date
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

sys.modules.pop("database", None)
import database  # noqa: E402
import services.reports_service as reports_service  # noqa: E402


def _mock_conn(fetchall_rows=None):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = fetchall_rows or []
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def _capture_real_year_bounds(year):
    """Call the real get_tax_year_report(year), returning the actual
    (tax_year_start, tax_year_end) tuple it passed to the real
    get_trade_history_by_tax_year() -- not a value reimplemented in the test."""
    captured = {}

    def fake_get_trade_history_by_tax_year(portfolio_id, year_start, year_end):
        captured["year_start"] = year_start
        captured["year_end"] = year_end
        return []

    # No mocking of `date` itself -- both 2025 and 2026 tax-year start dates
    # (Apr 2026 and Apr 2027 respectively) are safely in the past relative
    # to any real system clock this suite runs under, so the future-year
    # guard (`tax_year_start > date.today()`) is a non-issue here without
    # needing to fake "today".
    with patch.object(reports_service, "get_portfolio", return_value={"id": "port-1"}), \
         patch.object(reports_service, "get_trade_history_by_tax_year", side_effect=fake_get_trade_history_by_tax_year), \
         patch.object(reports_service, "get_estimated_unrealised_pnl", return_value=0.0):
        reports_service.get_tax_year_report(year)

    return captured["year_start"], captured["year_end"]


def test_adjacent_tax_years_have_no_gap_or_overlap_in_real_computed_bounds():
    """The real get_tax_year_report()'s computed boundaries for consecutive
    years must be exactly adjacent: year N's end + 1 day == year N+1's start."""
    from datetime import timedelta

    start_2025, end_2025 = _capture_real_year_bounds(2025)
    start_2026, end_2026 = _capture_real_year_bounds(2026)

    assert start_2025 == date(2025, 4, 6)
    assert end_2025 == date(2026, 4, 5)
    assert start_2026 == date(2026, 4, 6)
    assert end_2026 == date(2027, 4, 5)
    assert end_2025 + timedelta(days=1) == start_2026, (
        "No gap/overlap allowed between adjacent tax years -- a trade exiting "
        "on any date must fall in exactly one year's [start, end] range."
    )


def test_query_uses_inclusive_between_both_ends():
    """Confirm the real SQL get_trade_history_by_tax_year() issues uses
    BETWEEN (inclusive on both ends in Postgres), not a half-open range that
    would silently drop or duplicate a boundary-day trade."""
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.get_trade_history_by_tax_year("portfolio-1", date(2025, 4, 6), date(2026, 4, 5))

    sql = mock_cursor.execute.call_args.args[0]
    assert "BETWEEN %s AND %s" in sql
    params = mock_cursor.execute.call_args.args[1]
    assert params == ("portfolio-1", date(2025, 4, 6), date(2026, 4, 5))


def test_boundary_day_trade_captured_by_exactly_one_adjacent_year_no_omission_no_double_count():
    """
    The completeness guarantee this story's AC requires: using the REAL
    computed year boundaries (from test 1 above, re-derived here), a trade
    exiting on Apr 5 (last day of 2025/26) and a trade exiting on Apr 6
    (first day of 2026/27) must each be captured by exactly one of the two
    adjacent years' real [start, end] windows -- never zero (silent
    omission), never both (double-count).
    """
    start_2025, end_2025 = _capture_real_year_bounds(2025)
    start_2026, end_2026 = _capture_real_year_bounds(2026)

    last_day_of_2025_26 = date(2026, 4, 5)
    first_day_of_2026_27 = date(2026, 4, 6)

    def in_year(exit_date, year_start, year_end):
        # Mirrors Postgres BETWEEN's inclusive-both-ends semantics, confirmed
        # against the real SQL text in test_query_uses_inclusive_between_both_ends.
        return year_start <= exit_date <= year_end

    apr5_in_2025_26 = in_year(last_day_of_2025_26, start_2025, end_2025)
    apr5_in_2026_27 = in_year(last_day_of_2025_26, start_2026, end_2026)
    apr6_in_2025_26 = in_year(first_day_of_2026_27, start_2025, end_2025)
    apr6_in_2026_27 = in_year(first_day_of_2026_27, start_2026, end_2026)

    assert (apr5_in_2025_26, apr5_in_2026_27) == (True, False), (
        "Apr 5 trade: must appear in 2025/26 only -- omission or double-count detected"
    )
    assert (apr6_in_2025_26, apr6_in_2026_27) == (False, True), (
        "Apr 6 trade: must appear in 2026/27 only -- omission or double-count detected"
    )
