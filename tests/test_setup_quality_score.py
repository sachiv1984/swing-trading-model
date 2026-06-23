"""
Unit tests for GET /trade-plans/setup-quality-score — ST-08, EPIC-04, v6.1.

AC-06: covers gate_not_met case, gate_met with mixed history, perfect-history case.

Uses unittest.mock to isolate the endpoint from the database.
"""

import sys
import types
import pytest
from unittest.mock import patch, MagicMock


def _make_portfolio():
    p = MagicMock()
    p.__getitem__ = lambda self, k: "test-portfolio-id" if k == "id" else None
    p.get = lambda k, default=None: "test-portfolio-id" if k == "id" else default
    return p


def _make_trades(count, win_pct=0.6, avg_pnl_pct=10.0):
    """Generate `count` synthetic closed trades with given win rate and avg pnl_pct."""
    trades = []
    win_count = int(count * win_pct)
    for i in range(count):
        pnl = 100.0 if i < win_count else -50.0
        pnl_pct = avg_pnl_pct if i < win_count else -avg_pnl_pct / 2
        trades.append({"pnl": pnl, "pnl_pct": pnl_pct, "ticker": "AAPL"})
    return trades


class TestSetupQualityScoreGateNotMet:
    """AC-03: Returns gate_not_met when fewer than 20 closed trades exist."""

    def test_gate_not_met_with_zero_trades(self):
        with patch("backend.routers.trade_plans.get_portfolio", return_value=_make_portfolio()), \
             patch("backend.routers.trade_plans.get_trade_history", return_value=[]):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="AAPL")
            data = result["data"]
            assert data["gate_not_met"] is True
            assert data["min_trades_required"] == 20
            assert data["current_trades"] == 0

    def test_gate_not_met_with_15_trades(self):
        trades = _make_trades(15)
        with patch("backend.routers.trade_plans.get_portfolio", return_value=_make_portfolio()), \
             patch("backend.routers.trade_plans.get_trade_history", return_value=trades):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="AAPL")
            data = result["data"]
            assert data["gate_not_met"] is True
            assert data["current_trades"] == 15
            assert data["min_trades_required"] == 20

    def test_gate_not_met_excludes_trades_without_pnl(self):
        trades = _make_trades(25)
        # Make 10 of them open positions (pnl=None)
        for i in range(10):
            trades[i] = {"pnl": None, "pnl_pct": None, "ticker": "AAPL"}
        with patch("backend.routers.trade_plans.get_portfolio", return_value=_make_portfolio()), \
             patch("backend.routers.trade_plans.get_trade_history", return_value=trades):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="AAPL")
            data = result["data"]
            assert data["gate_not_met"] is True
            assert data["current_trades"] == 15


class TestSetupQualityScoreGateMet:
    """AC-01, AC-02, AC-04: Returns score response when gate is met (≥20 closed trades)."""

    def test_gate_met_response_shape(self):
        trades = _make_trades(20, win_pct=0.6, avg_pnl_pct=10.0)
        with patch("backend.routers.trade_plans.get_portfolio", return_value=_make_portfolio()), \
             patch("backend.routers.trade_plans.get_trade_history", return_value=trades):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="AAPL")
            data = result["data"]
            assert data["gate_not_met"] is False
            assert "score" in data
            assert "matching_trades" in data
            assert "win_rate" in data
            assert "average_pnl_pct" in data
            assert "score_explanation" in data

    def test_gate_met_with_mixed_history(self):
        trades = _make_trades(20, win_pct=0.5, avg_pnl_pct=5.0)
        with patch("backend.routers.trade_plans.get_portfolio", return_value=_make_portfolio()), \
             patch("backend.routers.trade_plans.get_trade_history", return_value=trades):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="AAPL")
            data = result["data"]
            assert data["gate_not_met"] is False
            assert data["matching_trades"] == 20
            assert data["win_rate"] == 50.0
            assert 0 <= data["score"] <= 100

    def test_gate_met_score_in_range(self):
        trades = _make_trades(30, win_pct=0.7, avg_pnl_pct=15.0)
        with patch("backend.routers.trade_plans.get_portfolio", return_value=_make_portfolio()), \
             patch("backend.routers.trade_plans.get_trade_history", return_value=trades):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="AAPL")
            data = result["data"]
            assert 0 <= data["score"] <= 100

    def test_perfect_history_yields_high_score(self):
        """100% win rate with positive avg_pnl_pct should produce a high score."""
        trades = _make_trades(20, win_pct=1.0, avg_pnl_pct=25.0)
        with patch("backend.routers.trade_plans.get_portfolio", return_value=_make_portfolio()), \
             patch("backend.routers.trade_plans.get_trade_history", return_value=trades):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="AAPL")
            data = result["data"]
            assert data["gate_not_met"] is False
            assert data["score"] >= 60, f"Expected high score for perfect history, got {data['score']}"
            assert data["win_rate"] == 100.0

    def test_ticker_echoed_uppercase(self):
        trades = _make_trades(20)
        with patch("backend.routers.trade_plans.get_portfolio", return_value=_make_portfolio()), \
             patch("backend.routers.trade_plans.get_trade_history", return_value=trades):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="aapl")
            assert result["data"]["ticker"] == "AAPL"


class TestSetupQualityScoreNoPortfolio:
    """Returns gate_not_met when portfolio is not found."""

    def test_no_portfolio(self):
        with patch("backend.routers.trade_plans.get_portfolio", return_value=None):
            from backend.routers.trade_plans import get_setup_quality_score
            result = get_setup_quality_score(ticker="AAPL")
            data = result["data"]
            assert data["gate_not_met"] is True
            assert data["current_trades"] == 0
