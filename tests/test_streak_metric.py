"""
Unit tests for consecutive losing streak metric computation (ST-15 / BLG-FEAT-18).
Tests the _build_advanced_metrics streak logic in analytics_service.py.
No live DB required — trades are plain dicts.
"""
import pytest


def _make_trade(pnl, exit_date="2026-01-01", entry_date="2025-12-01", holding_days=5):
    return {
        "pnl": pnl,
        "exit_date": exit_date,
        "entry_date": entry_date,
        "holding_days": holding_days,
    }


@pytest.fixture
def svc():
    from backend.services.analytics_service import AnalyticsService
    return AnalyticsService.__new__(AnalyticsService)


def test_all_wins_streak_zero(svc):
    trades = [_make_trade(100), _make_trade(50), _make_trade(200)]
    result = svc._build_advanced_metrics(trades, [])
    assert result["loss_streak"] == 0
    assert result["win_streak"] == 3


def test_all_losses_streak_equals_count(svc):
    trades = [_make_trade(-10), _make_trade(-20), _make_trade(-5)]
    result = svc._build_advanced_metrics(trades, [])
    assert result["loss_streak"] == 3
    assert result["win_streak"] == 0


def test_alternating_streak_is_one(svc):
    trades = [_make_trade(50), _make_trade(-20), _make_trade(30), _make_trade(-10)]
    result = svc._build_advanced_metrics(trades, [])
    assert result["loss_streak"] == 1
    assert result["win_streak"] == 1


def test_consecutive_losses_correct_count(svc):
    trades = [
        _make_trade(50),
        _make_trade(-10),
        _make_trade(-20),
        _make_trade(-5),
        _make_trade(100),
    ]
    result = svc._build_advanced_metrics(trades, [])
    assert result["loss_streak"] == 3


def test_multiple_runs_max_streak_returned(svc):
    trades = [
        _make_trade(-5), _make_trade(-5),          # streak of 2
        _make_trade(10),
        _make_trade(-5), _make_trade(-5), _make_trade(-5),  # streak of 3
        _make_trade(10),
    ]
    result = svc._build_advanced_metrics(trades, [])
    assert result["loss_streak"] == 3


def test_empty_trades_returns_empty(svc):
    result = svc._build_advanced_metrics([], [])
    assert result == {}


def test_zero_pnl_counts_as_loss(svc):
    trades = [_make_trade(10), _make_trade(0), _make_trade(0)]
    result = svc._build_advanced_metrics(trades, [])
    assert result["loss_streak"] == 2
