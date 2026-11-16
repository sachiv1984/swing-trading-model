"""
GET /analytics/metrics summary below the minimum-trades threshold.

BLG-FE-300 (ST-06, EPIC-02, v9.17): when the period has fewer closed trades
than min_trades, summary.win_rate and summary.total_pnl are the period's real
figures (a percentage and a sum, analytics_endpoints.md §summary), not 0.0.
Only executive_metrics and advanced_metrics stay empty. The Performance page
shows Total P&L, Win Rate and Total Trades in that state (performance.md §6).
"""

import pytest


@pytest.fixture
def svc():
    from backend.services.analytics_service import AnalyticsService
    return AnalyticsService.__new__(AnalyticsService)


def _trade(pnl, exit_date="2026-11-10"):
    # Shape of a trade_history row as the service reads it (ticker is read by
    # the enough-data branch's market/top-performer builders).
    return {"ticker": "AAPL", "pnl": pnl, "pnl_pct": 1.0, "exit_date": exit_date, "entry_date": "2026-11-01",
            "market": "US", "exit_reason": "Stop Loss", "holding_days": 9, "shares": 10, "entry_price": 100.0,
            "exit_price": 101.0, "total_cost": 1000.0}


def _summary(svc, trades, min_trades=10):
    return svc.calculate_metrics_from_data(trades=trades, portfolio_history=[], period="all_time", min_trades=min_trades)


def test_below_minimum_reports_real_win_rate_and_total_pnl(svc):
    # 3 trades, 2 winners; 55.12 + 28.35 - 39.37 = 44.10 (not exact in binary floating point)
    result = _summary(svc, [_trade(55.12), _trade(28.35), _trade(-39.37)])
    s = result["summary"]
    assert s["has_enough_data"] is False
    assert s["total_trades"] == 3
    assert s["min_required"] == 10
    assert s["win_rate"] == 66.7
    assert s["total_pnl"] == 44.1
    assert result["executive_metrics"] == {}
    assert result["advanced_metrics"] == {}


def test_below_minimum_with_no_trades_is_zero_not_an_error(svc):
    s = _summary(svc, [])["summary"]
    assert s == {"total_trades": 0, "win_rate": 0.0, "total_pnl": 0.0, "has_enough_data": False, "min_required": 10}


def test_below_minimum_all_losses_and_break_even(svc):
    # A break-even trade is not a win (pnl > 0), matching the enough-data branch.
    s = _summary(svc, [_trade(-10.0), _trade(0.0)])["summary"]
    assert s["win_rate"] == 0.0
    assert s["total_pnl"] == -10.0


def test_below_minimum_matches_the_enough_data_formula(svc):
    trades = [_trade(p) for p in (12.5, -4.25, 7.0, -1.1, 3.33)]
    below = _summary(svc, trades, min_trades=10)["summary"]
    enough = _summary(svc, trades, min_trades=5)["summary"]
    assert enough["has_enough_data"] is True
    assert below["win_rate"] == enough["win_rate"]
    assert below["total_pnl"] == enough["total_pnl"]
