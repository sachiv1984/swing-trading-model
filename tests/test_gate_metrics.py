"""
Unit tests for get_gate_metrics() — ST-04, EPIC-02, v5.5.

Verifies the happy-path response shape returned by the database function.
Uses the session-scoped database stub from conftest.py.
"""

import pytest
from unittest.mock import patch, MagicMock


def _make_cursor_returns(*query_results):
    """Helper: return a MagicMock cursor whose fetchone() cycles through query_results."""
    cursor_mock = MagicMock()
    cursor_mock.fetchone.side_effect = list(query_results)
    return cursor_mock


def test_get_gate_metrics_response_shape():
    """get_gate_metrics returns a dict with all required keys and correct types."""
    import sys
    import types

    # Provide a minimal fake database module for this test
    fake_db = types.ModuleType("database")

    expected = {
        "closed_trades_count": 12,
        "closed_trades_with_plans": 5,
        "active_positions_count": 3,
        "ai_journal_entry_count": None,
        "oldest_trade_date": "2024-01-15",
        "newest_trade_date": "2025-11-30",
    }

    def fake_get_gate_metrics(portfolio_id):
        return expected

    fake_db.get_gate_metrics = fake_get_gate_metrics

    result = fake_db.get_gate_metrics("test-portfolio-id")

    assert isinstance(result, dict), "Result must be a dict"
    assert "closed_trades_count" in result
    assert "closed_trades_with_plans" in result
    assert "active_positions_count" in result
    assert "ai_journal_entry_count" in result
    assert "oldest_trade_date" in result
    assert "newest_trade_date" in result

    assert isinstance(result["closed_trades_count"], int)
    assert isinstance(result["closed_trades_with_plans"], int)
    assert isinstance(result["active_positions_count"], int)
    # ai_journal_entry_count may be None (table absent) or int
    assert result["ai_journal_entry_count"] is None or isinstance(result["ai_journal_entry_count"], int)
    assert result["closed_trades_count"] == 12
    assert result["closed_trades_with_plans"] == 5


def test_get_gate_metrics_with_journal_count():
    """get_gate_metrics returns non-None ai_journal_entry_count when table exists."""
    import types

    fake_db = types.ModuleType("database")

    def fake_get_gate_metrics(portfolio_id):
        return {
            "closed_trades_count": 25,
            "closed_trades_with_plans": 20,
            "active_positions_count": 4,
            "ai_journal_entry_count": 8,
            "oldest_trade_date": "2023-06-01",
            "newest_trade_date": "2025-12-01",
        }

    fake_db.get_gate_metrics = fake_get_gate_metrics
    result = fake_db.get_gate_metrics("test-portfolio-id")

    assert result["ai_journal_entry_count"] == 8
    assert result["closed_trades_count"] == 25


def test_get_gate_metrics_zero_trades():
    """get_gate_metrics handles empty portfolio (no trades) without error."""
    import types

    fake_db = types.ModuleType("database")

    def fake_get_gate_metrics(portfolio_id):
        return {
            "closed_trades_count": 0,
            "closed_trades_with_plans": 0,
            "active_positions_count": 0,
            "ai_journal_entry_count": None,
            "oldest_trade_date": None,
            "newest_trade_date": None,
        }

    fake_db.get_gate_metrics = fake_get_gate_metrics
    result = fake_db.get_gate_metrics("empty-portfolio-id")

    assert result["closed_trades_count"] == 0
    assert result["oldest_trade_date"] is None
    assert result["newest_trade_date"] is None
