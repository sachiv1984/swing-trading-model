"""
Gap Risk Flag Unit Tests — ST-02 (BLG-FEAT-65, v6.9)

Verifies GET /positions/{position_id}/gap-risk combines earnings proximity
(DS-04 calendar) and Friday-close weekend-hold detection into a deterministic,
informational flag with historical gap statistics — no gap direction or
magnitude prediction (§13, AC-04).

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
from services.gap_risk_service import get_gap_risk, MIN_HISTORICAL_EVENTS

CLIENT = TestClient(app, raise_server_exceptions=False)

OPEN_POSITION = {
    "id": "pos-001",
    "ticker": "AAPL",
    "market": "US",
    "status": "open",
}

NO_EARNINGS = {"ticker": "AAPL", "next_earnings_date": None, "days_until_earnings": None}


def test_404_when_position_not_found():
    with patch("main.get_position_by_id", return_value=None):
        resp = CLIENT.get("/positions/does-not-exist/gap-risk")
    assert resp.status_code == 404


def test_not_flagged_when_no_earnings_and_not_friday():
    with (
        patch("services.gap_risk_service.get_earnings", return_value=NO_EARNINGS),
        patch("services.gap_risk_service._is_weekend_hold", return_value=False),
    ):
        result = get_gap_risk("AAPL", "US")
    assert result["flagged"] is False
    assert result["reasons"] == []
    assert result["avg_gap_pct"] is None


def test_flagged_for_earnings_before_next_session():
    earnings = {**NO_EARNINGS, "days_until_earnings": 1, "next_earnings_date": "2026-07-14"}
    with (
        patch("services.gap_risk_service.get_earnings", return_value=earnings),
        patch("services.gap_risk_service._is_weekend_hold", return_value=False),
        patch("services.gap_risk_service._compute_gap_stats", return_value={"avg_gap_pct": 2.3, "event_count": 14, "insufficient_history": False}),
    ):
        result = get_gap_risk("AAPL", "US")
    assert result["flagged"] is True
    assert result["reasons"] == ["earnings"]
    assert result["avg_gap_pct"] == 2.3
    assert result["event_count"] == 14


def test_not_flagged_when_earnings_too_far_out():
    earnings = {**NO_EARNINGS, "days_until_earnings": 10, "next_earnings_date": "2026-07-23"}
    with (
        patch("services.gap_risk_service.get_earnings", return_value=earnings),
        patch("services.gap_risk_service._is_weekend_hold", return_value=False),
    ):
        result = get_gap_risk("AAPL", "US")
    assert result["flagged"] is False


def test_flagged_for_weekend_hold_on_friday():
    with (
        patch("services.gap_risk_service.get_earnings", return_value=NO_EARNINGS),
        patch("services.gap_risk_service._is_weekend_hold", return_value=True),
        patch("services.gap_risk_service._compute_gap_stats", return_value={"avg_gap_pct": 1.1, "event_count": 31, "insufficient_history": False}),
    ):
        result = get_gap_risk("AAPL", "US")
    assert result["flagged"] is True
    assert result["reasons"] == ["weekend_hold"]
    assert result["avg_gap_pct"] == 1.1


def test_both_reasons_stack_when_earnings_and_weekend_coincide():
    earnings = {**NO_EARNINGS, "days_until_earnings": 0, "next_earnings_date": "2026-07-10"}
    with (
        patch("services.gap_risk_service.get_earnings", return_value=earnings),
        patch("services.gap_risk_service._is_weekend_hold", return_value=True),
        patch("services.gap_risk_service._compute_gap_stats", return_value={"avg_gap_pct": 3.0, "event_count": 20, "insufficient_history": False}),
    ):
        result = get_gap_risk("AAPL", "US")
    assert result["flagged"] is True
    assert result["reasons"] == ["earnings", "weekend_hold"]


def test_insufficient_history_flag_still_shown():
    """Insufficient history does not suppress the flag — badge still shown per ux_spec.md §6."""
    earnings = {**NO_EARNINGS, "days_until_earnings": 1, "next_earnings_date": "2026-07-14"}
    with (
        patch("services.gap_risk_service.get_earnings", return_value=earnings),
        patch("services.gap_risk_service._is_weekend_hold", return_value=False),
        patch("services.gap_risk_service._compute_gap_stats", return_value={"avg_gap_pct": None, "event_count": 3, "insufficient_history": True}),
    ):
        result = get_gap_risk("AAPL", "US")
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
            "reasons": ["weekend_hold"],
            "avg_gap_pct": 1.1,
            "event_count": 31,
            "insufficient_history": False,
        }),
    ):
        resp = CLIENT.get("/positions/pos-001/gap-risk")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["flagged"] is True
    assert data["reasons"] == ["weekend_hold"]
