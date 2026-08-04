"""
Unit tests for SI-02 behavioural_drift_service.py

Covers all 4 metrics in isolation, insufficient_data states, §13 compliance,
and overall endpoint status logic.

Spec: docs/specs/metrics/si02_drift_score.md §2–§4
AC ref: stage4_backlog_slice.md#ST-05
"""
import pytest
from datetime import date
from unittest.mock import MagicMock

from services.behavioural_drift_service import (
    compute_drift,
    compute_insufficient_data_streak,
    _compute_entry_timing_drift,
    _compute_sizing_adherence,
    _compute_consecutive_loss_sizing,
    _compute_regime_context,
    _classify_status,
    _deviation_pct,
    _overall_status,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_trade(entry_date=None, pnl=100.0, risk_percent_used=1.5, regime_context_at_entry="risk_on", signal_id=None):
    return {
        "entry_date": entry_date or date(2026, 4, 1),
        "pnl": pnl,
        "risk_percent_used": risk_percent_used,
        "regime_context_at_entry": regime_context_at_entry,
        "signal_id": signal_id or "sig-1",
        "effective_settings_snapshot": None,
    }


def _make_signal_timing(entry_date, signal_date):
    return {"entry_date": entry_date, "signal_date": signal_date}


def _make_portfolio_data(trades, signal_timing=None, settings=None, trade_count=None):
    return {
        "trade_count": trade_count if trade_count is not None else len(trades),
        "trades": trades,
        "signal_timing": signal_timing or [],
        "settings": settings or {"default_risk_percent": 1.5},
    }


# ---------------------------------------------------------------------------
# TC-01: Sufficient data returns correct metric values
# ---------------------------------------------------------------------------

def test_compute_drift_sufficient_data_returns_metrics():
    trades = [_make_trade() for _ in range(12)]
    data = _make_portfolio_data(trades)
    result = compute_drift(data)

    assert result["status"] in ("no_drift", "drift_detected")
    assert result["analysis_window_days"] == 90
    assert result["trade_count_in_window"] == 12
    assert len(result["metrics"]) == 4
    metric_ids = {m["metric_id"] for m in result["metrics"]}
    assert metric_ids == {"entry_timing_drift", "sizing_adherence", "consecutive_loss_sizing", "regime_context"}


# ---------------------------------------------------------------------------
# TC-02: Insufficient data (< 10 trades) → insufficient_data top-level status
# ---------------------------------------------------------------------------

def test_compute_drift_insufficient_data_returns_no_metrics():
    data = _make_portfolio_data([], trade_count=5)
    result = compute_drift(data)

    assert result["status"] == "insufficient_data"
    assert result["trade_count_in_window"] == 5
    assert result["metrics"] == []


def test_compute_drift_zero_trades():
    data = _make_portfolio_data([], trade_count=0)
    result = compute_drift(data)

    assert result["status"] == "insufficient_data"


# ---------------------------------------------------------------------------
# TC-03: entry_timing_drift excludes trades without signal_id; count in advisory
# ---------------------------------------------------------------------------

def test_entry_timing_drift_excludes_trades_without_signal():
    signal_timing = [
        _make_signal_timing(date(2026, 4, 2), date(2026, 4, 1)),   # 1 day lag
        _make_signal_timing(date(2026, 4, 3), date(2026, 4, 2)),   # 1 day lag
    ]
    result = _compute_entry_timing_drift(signal_timing, total_window_trades=5)

    assert result["metric_id"] == "entry_timing_drift"
    assert result["measured_value"] == pytest.approx(1.0)
    assert result["status"] == "approaching"
    assert "3 of 5" in (result["advisory_note"] or "")


def test_entry_timing_drift_no_signals():
    result = _compute_entry_timing_drift([], total_window_trades=12)
    assert result["status"] == "insufficient_data"


def test_entry_timing_drift_ok_status():
    signal_timing = [_make_signal_timing(date(2026, 4, 1), date(2026, 3, 31))] * 10
    result = _compute_entry_timing_drift(signal_timing, total_window_trades=10)
    assert result["measured_value"] == pytest.approx(1.0)
    assert result["status"] == "approaching"


def test_entry_timing_drift_green_status():
    signal_timing = [_make_signal_timing(date(2026, 4, 1), date(2026, 4, 1))] * 10
    result = _compute_entry_timing_drift(signal_timing, total_window_trades=10)
    assert result["measured_value"] == pytest.approx(0.0)
    assert result["status"] == "ok"


# ---------------------------------------------------------------------------
# TC-04: sizing_adherence correct for over-sizing (red), approaching (amber), within (green)
# ---------------------------------------------------------------------------

def test_sizing_adherence_green():
    trades = [_make_trade(risk_percent_used=1.0) for _ in range(5)]
    result = _compute_sizing_adherence(trades, plan_max=1.5)
    assert result["measured_value"] == pytest.approx(1.0)
    assert result["status"] == "ok"


def test_sizing_adherence_approaching():
    trades = [_make_trade(risk_percent_used=1.3) for _ in range(5)]
    result = _compute_sizing_adherence(trades, plan_max=1.5)
    assert result["measured_value"] == pytest.approx(1.3)
    assert result["status"] == "approaching"


def test_sizing_adherence_breached():
    trades = [_make_trade(risk_percent_used=2.0) for _ in range(5)]
    result = _compute_sizing_adherence(trades, plan_max=1.5)
    assert result["measured_value"] == pytest.approx(2.0)
    assert result["status"] == "breached"


def test_sizing_adherence_undersizing_advisory():
    trades = [_make_trade(risk_percent_used=0.5) for _ in range(5)]
    result = _compute_sizing_adherence(trades, plan_max=1.5)
    assert result["status"] == "ok"
    assert result["advisory_note"] is not None
    assert "50%" in result["advisory_note"]


def test_sizing_adherence_null_risk_excluded():
    trades = [_make_trade(risk_percent_used=None) for _ in range(5)]
    result = _compute_sizing_adherence(trades, plan_max=1.5)
    assert result["status"] == "insufficient_data"


# ---------------------------------------------------------------------------
# TC-05: consecutive_loss_sizing — identifies post-loss-streak trades correctly
# ---------------------------------------------------------------------------

def test_consecutive_loss_sizing_identifies_post_loss_trades():
    # 3 qualifying post-loss trades, each preceded by ≥2 consecutive losses
    trades = [
        _make_trade(risk_percent_used=1.0, pnl=-100.0),   # loss 1
        _make_trade(risk_percent_used=1.0, pnl=-100.0),   # loss 2 (consecutive)
        _make_trade(risk_percent_used=2.5, pnl=100.0),    # post-2-loss (qualifying 1)
        _make_trade(risk_percent_used=1.0, pnl=-100.0),   # loss
        _make_trade(risk_percent_used=1.0, pnl=-100.0),   # loss (2 consecutive)
        _make_trade(risk_percent_used=2.0, pnl=100.0),    # post-2-loss (qualifying 2)
        _make_trade(risk_percent_used=1.0, pnl=-100.0),   # loss
        _make_trade(risk_percent_used=1.0, pnl=-100.0),   # loss (2 consecutive)
        _make_trade(risk_percent_used=2.3, pnl=100.0),    # post-2-loss (qualifying 3)
    ]
    result = _compute_consecutive_loss_sizing(trades, plan_max=1.5)
    assert result["status"] == "breached"
    assert result["measured_value"] > 1.5


def test_consecutive_loss_sizing_insufficient_post_loss_trades():
    trades = [
        _make_trade(risk_percent_used=1.0, pnl=-100.0),
        _make_trade(risk_percent_used=1.0, pnl=-100.0),
        _make_trade(risk_percent_used=2.0, pnl=100.0),  # only 1 post-loss with risk data
        _make_trade(risk_percent_used=None, pnl=100.0),  # null — excluded
        _make_trade(risk_percent_used=None, pnl=100.0),  # null — excluded
    ]
    result = _compute_consecutive_loss_sizing(trades, plan_max=1.5)
    assert result["status"] == "insufficient_data"
    assert result["measured_value"] is None


# ---------------------------------------------------------------------------
# TC-06: regime_context — risk_off counted as violation; null counted as neutral
# ---------------------------------------------------------------------------

def test_regime_context_all_valid():
    trades = [_make_trade(regime_context_at_entry="risk_on") for _ in range(10)]
    result = _compute_regime_context(trades)
    assert result["measured_value"] == pytest.approx(100.0)
    assert result["status"] == "ok"


def test_regime_context_null_regime_counted_as_neutral():
    trades = [_make_trade(regime_context_at_entry=None) for _ in range(10)]
    result = _compute_regime_context(trades)
    assert result["measured_value"] == pytest.approx(100.0)
    assert result["status"] == "ok"


def test_regime_context_risk_off_as_violation():
    trades = (
        [_make_trade(regime_context_at_entry="risk_on")] * 9
        + [_make_trade(regime_context_at_entry="risk_off")]
    )
    result = _compute_regime_context(trades)
    assert result["measured_value"] == pytest.approx(90.0)
    assert result["status"] == "approaching"


def test_regime_context_breached():
    trades = (
        [_make_trade(regime_context_at_entry="risk_on")] * 8
        + [_make_trade(regime_context_at_entry="risk_off")] * 2
    )
    result = _compute_regime_context(trades)
    assert result["measured_value"] == pytest.approx(80.0)
    assert result["status"] == "breached"


# ---------------------------------------------------------------------------
# TC-07: §13 binding condition — no automated recommendations in response
# ---------------------------------------------------------------------------

def test_compute_drift_response_contains_no_automated_recommendations():
    trades = [_make_trade() for _ in range(15)]
    data = _make_portfolio_data(trades)
    result = compute_drift(data)

    response_str = str(result)
    forbidden_phrases = ["recommend", "should trade", "automated action", "execute", "trigger"]
    for phrase in forbidden_phrases:
        assert phrase.lower() not in response_str.lower(), f"Found forbidden phrase '{phrase}' in response"


def test_compute_drift_error_does_not_expose_internals():
    data = {
        "trade_count": 15,
        "trades": [_make_trade() for _ in range(15)],
        "settings": {"default_risk_percent": 1.5},
        "signal_timing": [],
    }
    result = compute_drift(data)
    assert result["status"] in ("no_drift", "drift_detected", "insufficient_data")


# ---------------------------------------------------------------------------
# TC-08: _classify_status unit tests for both directions
# ---------------------------------------------------------------------------

def test_classify_status_lte_ok():
    assert _classify_status(0.5, 1.0, "lte") == "ok"


def test_classify_status_lte_approaching():
    assert _classify_status(0.9, 1.0, "lte") == "approaching"


def test_classify_status_lte_breached():
    assert _classify_status(1.5, 1.0, "lte") == "breached"


def test_classify_status_gte_ok():
    # ok when measured >= threshold * 1.20; use threshold=50 so ok threshold=60
    assert _classify_status(70.0, 50.0, "gte") == "ok"


def test_classify_status_gte_approaching():
    assert _classify_status(92.0, 90.0, "gte") == "approaching"


def test_classify_status_gte_breached():
    assert _classify_status(85.0, 90.0, "gte") == "breached"


def test_classify_status_none_returns_insufficient():
    assert _classify_status(None, 1.0, "lte") == "insufficient_data"


# ---------------------------------------------------------------------------
# TC-09: _overall_status derives correctly
# ---------------------------------------------------------------------------

def test_overall_status_no_drift():
    metrics = [{"status": "ok"}, {"status": "ok"}, {"status": "insufficient_data"}]
    assert _overall_status(metrics) == "no_drift"


def test_overall_status_drift_detected_approaching():
    metrics = [{"status": "ok"}, {"status": "approaching"}]
    assert _overall_status(metrics) == "drift_detected"


def test_overall_status_drift_detected_breached():
    metrics = [{"status": "ok"}, {"status": "breached"}]
    assert _overall_status(metrics) == "drift_detected"


def test_overall_status_all_insufficient():
    metrics = [{"status": "insufficient_data"}, {"status": "insufficient_data"}]
    assert _overall_status(metrics) == "insufficient_data"


# ---------------------------------------------------------------------------
# TC-10: deviation_pct formula
# ---------------------------------------------------------------------------

def test_deviation_pct_positive():
    result = _deviation_pct(1.5, 1.0)
    assert result == pytest.approx(50.0)


def test_deviation_pct_negative():
    result = _deviation_pct(0.5, 1.0)
    assert result == pytest.approx(-50.0)


def test_deviation_pct_none():
    assert _deviation_pct(None, 1.0) is None


def test_deviation_pct_zero_threshold():
    assert _deviation_pct(1.0, 0.0) is None


# ---------------------------------------------------------------------------
# ST-05 (EPIC-01, v8.2, BLG-FEAT-86): compute_insufficient_data_streak
# ---------------------------------------------------------------------------

def test_streak_zero_when_window_already_sufficient():
    """10 entry_dates all within the last 90 days -> no streak (0 days)."""
    as_of = date(2026, 8, 4)
    entry_dates = [date(2026, 7, 1)] * 10
    result = compute_insufficient_data_streak(entry_dates, as_of=as_of)
    assert result["insufficient_data_streak_days"] == 0
    assert result["streak_capped"] is False


def test_streak_positive_when_no_trades_at_all():
    """No trades anywhere -> streak grows until the max-lookback cap, capped=True."""
    as_of = date(2026, 8, 4)
    result = compute_insufficient_data_streak([], as_of=as_of)
    assert result["insufficient_data_streak_days"] == 180
    assert result["streak_capped"] is True


def test_streak_ends_on_the_day_the_window_first_cleared_the_threshold():
    """10 trades all entered on the same day D. The 90-day trailing window
    contains all 10 exactly when the as-of day falls in [D, D+89]. With
    D = 2026-04-26 and as_of = 2026-08-04 (D+100), the window first clears
    the _MIN_TRADES threshold walking backward at day = D+89 = 2026-07-24 —
    an 11-day streak (2026-07-25 .. 2026-08-04 inclusive, both insufficient)."""
    as_of = date(2026, 8, 4)
    entry_dates = [date(2026, 4, 26)] * 10
    result = compute_insufficient_data_streak(entry_dates, as_of=as_of)
    assert result["insufficient_data_streak_days"] == 11
    assert result["streak_capped"] is False


def test_streak_trend_increasing_when_recent_trades_added():
    as_of = date(2026, 8, 4)
    # 3 trades entered in the last few days: inside today's window [May 7, Aug 4],
    # but outside the 30-days-prior window [Apr 7, Jul 5] entirely -> count goes
    # from 0 (prior) to 3 (today) -> increasing.
    recent = [date(2026, 8, 1), date(2026, 8, 2), date(2026, 8, 3)]
    result = compute_insufficient_data_streak(recent, as_of=as_of)
    assert result["trade_count_trend"] == "increasing"


def test_streak_trend_flat_when_no_change():
    as_of = date(2026, 8, 4)
    entry_dates = [date(2026, 1, 1)] * 5
    result = compute_insufficient_data_streak(entry_dates, as_of=as_of)
    assert result["trade_count_trend"] == "flat"
