"""
Gap Risk Flag Unit Tests — ST-02 (BLG-FEAT-65, v6.9)

Verifies GET /positions/{position_id}/gap-risk flags a US position whose
earnings fall after today and on or before its next trading day, with
historical gap statistics — no gap direction or magnitude prediction (§13,
AC-04). v9.10 (ST-13 ruling, ST-14, BLG-GOV-365/BLG-BE-136): UK positions are
never flagged, day 0 is not flagged, a Friday view flags Monday earnings, and
the standalone weekend_hold trigger is removed. v9.12 (ST-14, BLG-BE-148,
Revised Ruling 3): the next session comes from the NYSE calendar and "today" is
the US market date; days_until is computed from next_earnings_date.

CI-safe: earnings_service and yfinance history calls are mocked; no live
network or database connections.

Spec: docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk
"""

import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi.testclient import TestClient
from main import app
from services.gap_risk_service import get_gap_risk, MIN_HISTORICAL_EVENTS, _days_to_next_trading_day

CLIENT = TestClient(app, raise_server_exceptions=False)

OPEN_POSITION = {
    "id": "pos-001",
    "ticker": "AAPL",
    "market": "US",
    "status": "open",
}

NO_EARNINGS = {"ticker": "AAPL", "next_earnings_date": None, "days_until_earnings": None}

# Fixed view dates (2026-10-05 is a Monday).
MONDAY = date(2026, 10, 5)
THURSDAY = date(2026, 10, 8)
FRIDAY = date(2026, 10, 9)
SATURDAY = date(2026, 10, 10)
SUNDAY = date(2026, 10, 11)

STATS = {"avg_gap_pct": 2.3, "event_count": 14, "insufficient_history": False}


def _run(days_until, today, market="US", stats=STATS):
    # v9.12: the service computes days_until from next_earnings_date and today.
    # days_until_earnings is deliberately set to a misleading value to prove the
    # service no longer reads it.
    next_date = None if days_until is None else (today + timedelta(days=days_until)).isoformat()
    earnings = {**NO_EARNINGS, "next_earnings_date": next_date, "days_until_earnings": 99}
    with (
        patch("services.gap_risk_service.get_earnings", return_value=earnings) as m_earn,
        patch("services.gap_risk_service._compute_gap_stats", return_value=stats) as m_stats,
    ):
        result = get_gap_risk("AAPL" if market == "US" else "VOD", market, today=today)
    return result, m_earn, m_stats


def test_404_when_position_not_found():
    with patch("main.get_position_by_id", return_value=None):
        resp = CLIENT.get("/positions/does-not-exist/gap-risk")
    assert resp.status_code == 404


def test_not_flagged_when_no_earnings():
    result, _, _ = _run(None, THURSDAY)
    assert result["flagged"] is False
    assert result["reasons"] == []
    assert result["avg_gap_pct"] is None


def test_flagged_for_earnings_tomorrow():
    result, _, m_stats = _run(1, THURSDAY)
    assert result["flagged"] is True
    assert result["reasons"] == ["earnings"]
    assert result["avg_gap_pct"] == 2.3
    assert result["event_count"] == 14
    m_stats.assert_called_once_with("AAPL", "US", weekend=False)


def test_not_flagged_when_earnings_too_far_out():
    result, _, _ = _run(10, THURSDAY)
    assert result["flagged"] is False


# --- ST-13 ruling: day 0 ---

def test_day_0_not_flagged():
    """ST-13: earnings today are not flagged (a before-open release has already gapped)."""
    for today in (MONDAY, THURSDAY, FRIDAY):
        result, _, _ = _run(0, today)
        assert result["flagged"] is False, today
        assert result["reasons"] == []


def test_past_earnings_not_flagged():
    result, _, _ = _run(-1, THURSDAY)
    assert result["flagged"] is False


# --- ST-14 AC 2: trading-session window ---

def test_friday_view_flags_monday_earnings():
    """ST-14 AC 2: a Friday view with Monday earnings (3 days) is flagged 'earnings'."""
    result, _, m_stats = _run(3, FRIDAY)
    assert result["flagged"] is True
    assert result["reasons"] == ["earnings"]
    m_stats.assert_called_once_with("AAPL", "US", weekend=True)


def test_friday_view_does_not_flag_tuesday_earnings():
    result, _, _ = _run(4, FRIDAY)
    assert result["flagged"] is False


def test_thursday_view_does_not_flag_monday_earnings():
    """Monday is not Thursday's next trading day (Friday is)."""
    result, _, _ = _run(4, THURSDAY)
    assert result["flagged"] is False
    result, _, _ = _run(2, THURSDAY)
    assert result["flagged"] is False


def test_weekend_views_flag_monday_earnings():
    result, _, _ = _run(2, SATURDAY)
    assert result["reasons"] == ["earnings"]
    result, _, m_stats = _run(1, SUNDAY)
    assert result["reasons"] == ["earnings"]
    m_stats.assert_called_once_with("AAPL", "US", weekend=True)


def test_days_to_next_trading_day():
    assert _days_to_next_trading_day(MONDAY) == 1
    assert _days_to_next_trading_day(THURSDAY) == 1
    assert _days_to_next_trading_day(FRIDAY) == 3
    assert _days_to_next_trading_day(SATURDAY) == 2
    assert _days_to_next_trading_day(SUNDAY) == 1


# --- ST-13 ruling: UK tickers ---

def test_uk_position_never_flagged_and_earnings_not_fetched():
    """ST-13: §4.2.3 is US-only, so a UK position's earnings never trigger the flag."""
    for days_until, today in ((1, THURSDAY), (3, FRIDAY), (0, MONDAY)):
        result, m_earn, _ = _run(days_until, today, market="UK")
        assert result["flagged"] is False
        assert result["reasons"] == []
        m_earn.assert_not_called()


# --- ST-14 AC 1: no uniform trigger (Binding Condition 6) ---

def test_friday_without_earnings_not_flagged():
    """ST-14: the standalone weekend_hold trigger is removed; Friday alone flags nothing."""
    for market in ("US", "UK"):
        result, _, _ = _run(None, FRIDAY, market=market)
        assert result["flagged"] is False
        assert result["reasons"] == []


def test_no_trigger_flags_every_position_identically():
    """Binding Condition 6: on any day, positions without an event are never flagged."""
    for today in (MONDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY):
        for market in ("US", "UK"):
            result, _, _ = _run(None, today, market=market)
            assert result["flagged"] is False, (today, market)


def test_reasons_only_ever_earnings():
    for days_until in range(-2, 8):
        for today in (MONDAY, FRIDAY, SATURDAY):
            result, _, _ = _run(days_until, today)
            assert set(result["reasons"]) <= {"earnings"}


def test_module_docstring_cites_section13_review_record():
    """Binding Condition 8."""
    from services import gap_risk_service
    assert "decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md" in gap_risk_service.__doc__


def test_insufficient_history_flag_still_shown():
    """Insufficient history does not suppress the flag — badge still shown per ux_spec.md §6."""
    result, _, _ = _run(1, THURSDAY, stats={"avg_gap_pct": None, "event_count": 3, "insufficient_history": True})
    assert result["flagged"] is True
    assert result["insufficient_history"] is True
    assert result["avg_gap_pct"] is None


def test_compute_gap_stats_insufficient_below_threshold():
    """Directly exercises _compute_gap_stats' history-length gate against a mocked yfinance frame."""
    import pandas as pd
    from services import gap_risk_service

    # Only 3 daily bars — fewer than MIN_HISTORICAL_EVENTS overnight gaps possible.
    idx = pd.date_range("2026-06-01", periods=3, freq="B")
    hist = pd.DataFrame({"Open": [100.0, 101.0, 102.0], "Close": [100.5, 101.5, 102.5]}, index=idx)

    mock_ticker = MagicMock()
    mock_ticker.history.return_value = hist
    with patch("services.gap_risk_service.yf.Ticker", return_value=mock_ticker):
        stats = gap_risk_service._compute_gap_stats("AAPL", "US", weekend=False)

    assert stats["insufficient_history"] is True
    assert stats["event_count"] < MIN_HISTORICAL_EVENTS
    assert stats["avg_gap_pct"] is None


def test_endpoint_returns_gap_risk_object():
    with (
        patch("main.get_position_by_id", return_value=OPEN_POSITION),
        patch("main.get_gap_risk", return_value={
            "flagged": True,
            "reasons": ["earnings"],
            "avg_gap_pct": 2.3,
            "event_count": 14,
            "insufficient_history": False,
        }) as m_gap,
    ):
        resp = CLIENT.get("/positions/pos-001/gap-risk")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["flagged"] is True
    assert data["reasons"] == ["earnings"]
    m_gap.assert_called_once_with("AAPL", "US")


# --- v9.12 ST-14 (BLG-BE-148): NYSE calendar and US market date ---

from services import us_market_calendar as cal  # noqa: E402

# NYSE's published full-closure holidays (checked 2026-10-13).
NYSE_PUBLISHED = {
    2026: {date(2026, 1, 1), date(2026, 1, 19), date(2026, 2, 16), date(2026, 4, 3), date(2026, 5, 25),
           date(2026, 6, 19), date(2026, 7, 3), date(2026, 9, 7), date(2026, 11, 26), date(2026, 12, 25)},
    2027: {date(2027, 1, 1), date(2027, 1, 18), date(2027, 2, 15), date(2027, 3, 26), date(2027, 5, 31),
           date(2027, 6, 18), date(2027, 7, 5), date(2027, 9, 6), date(2027, 11, 25), date(2027, 12, 24)},
}


def test_holiday_rules_match_published_nyse_schedule():
    for year, published in NYSE_PUBLISHED.items():
        assert cal.nyse_holidays(year) == published, year


def test_friday_before_monday_holiday_flags_tuesday_earnings():
    """ST-14 AC 1: Friday 2026-09-04, Labor Day Monday 09-07; Tuesday earnings are 4 days out."""
    friday = date(2026, 9, 4)
    assert _days_to_next_trading_day(friday) == 4
    result, _, _ = _run(4, friday)
    assert result["reasons"] == ["earnings"]
    result, _, _ = _run(5, friday)
    assert result["flagged"] is False


def test_0200_utc_view_uses_us_market_date():
    """ST-14 AC 2: 02:00 UTC on Tuesday 2026-10-13 is still Monday 10-12 in New York."""
    now = datetime(2026, 10, 13, 2, 0, tzinfo=timezone.utc)
    assert cal.us_market_date(now) == date(2026, 10, 12)
    # Earnings on Tuesday 10-13: 1 day from the US date (flagged); 0 from the UTC date (not).
    earnings = {**NO_EARNINGS, "next_earnings_date": "2026-10-13", "days_until_earnings": 0}
    with patch("services.gap_risk_service.get_earnings", return_value=earnings), \
         patch("services.gap_risk_service._compute_gap_stats", return_value=STATS):
        result = get_gap_risk("AAPL", "US", now=now)
    assert result["reasons"] == ["earnings"]


def test_us_market_date_rejects_naive_datetime():
    import pytest
    with pytest.raises(ValueError):
        cal.us_market_date(datetime(2026, 10, 13, 2, 0))


def test_thursday_before_good_friday_flags_monday_earnings():
    thursday = date(2026, 4, 2)  # Good Friday 2026-04-03
    assert _days_to_next_trading_day(thursday) == 4
    result, _, _ = _run(4, thursday)
    assert result["reasons"] == ["earnings"]


def test_saturday_new_year_not_observed_on_friday():
    assert date(2022, 1, 1).weekday() == 5
    assert cal.is_nyse_session(date(2021, 12, 31))
    assert date(2021, 12, 31) not in cal.nyse_holidays(2021)


def test_juneteenth_only_from_2022():
    assert date(2021, 6, 18) not in cal.nyse_holidays(2021)  # would be the Friday observance
    assert date(2022, 6, 20) in cal.nyse_holidays(2022)      # Sunday 19th observed Monday


def test_early_close_day_is_a_session():
    """Wednesday before Thanksgiving: next session is the Friday early close (d=2)."""
    wednesday = date(2026, 11, 25)
    assert _days_to_next_trading_day(wednesday) == 2
    assert _run(2, wednesday)[0]["reasons"] == ["earnings"]   # Friday
    assert _run(5, wednesday)[0]["flagged"] is False          # Monday


def test_view_on_a_holiday():
    """On Labor Day itself the next session is Tuesday."""
    assert _days_to_next_trading_day(date(2026, 9, 7)) == 1
    assert _run(1, date(2026, 9, 7))[0]["reasons"] == ["earnings"]


def test_one_off_closures_are_not_sessions():
    assert not cal.is_nyse_session(date(2025, 1, 9))
    assert _days_to_next_trading_day(date(2025, 1, 8)) == 2


def test_calendar_is_deterministic_with_no_network():
    """Binding Condition 1: no socket, yfinance or price-history access in the calendar."""
    import socket
    with patch.object(socket, "socket", side_effect=AssertionError("network used")), \
         patch("services.gap_risk_service.yf", side_effect=AssertionError("yfinance used")):
        first = [cal.days_to_next_nyse_session(date(2026, 1, 1) + timedelta(days=i)) for i in range(800)]
        cal.nyse_holidays.cache_clear()
        second = [cal.days_to_next_nyse_session(date(2026, 1, 1) + timedelta(days=i)) for i in range(800)]
    assert first == second
    assert max(first) <= 5


def test_module_docstrings_cite_v912_addendum():
    """Binding Condition 8 (extended at v9.12)."""
    from services import gap_risk_service
    assert "v9.12 addendum" in gap_risk_service.__doc__
    assert "ESC-EXEC-20261013-07" in cal.__doc__
