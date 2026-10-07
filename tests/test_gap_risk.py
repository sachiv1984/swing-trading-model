"""
Gap Risk Flag Unit Tests — ST-02 (BLG-FEAT-65, v6.9)

Verifies GET /positions/{position_id}/gap-risk flags a US position whose
earnings fall after today and on or before its next trading day, with
historical gap statistics — no gap direction or magnitude prediction (§13,
AC-04). v9.10 (ST-13 ruling, ST-14, BLG-GOV-365/BLG-BE-136): UK positions are
never flagged, day 0 is not flagged, a Friday view flags Monday earnings, and
the standalone weekend_hold trigger is removed.

CI-safe: earnings_service and yfinance history calls are mocked; no live
network or database connections.

Spec: docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk
"""

import sys
from datetime import date
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
    earnings = {**NO_EARNINGS, "days_until_earnings": days_until}
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
