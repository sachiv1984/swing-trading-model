"""
Trade Plan Completion Rate regression tests (ST-01, BLG-FEAT-32, EPIC-01, v8.6).

database.get_trade_plan_completion_rate() computes plans_created,
plans_completed, plans_abandoned, and completion_rate for the Performance
Analytics page §21. No live database calls — the single aggregate query is
exercised against a mocked get_db() connection, following the same pattern
as test_trade_plan_tags.py's database.get_tag_performance() tests.

Design source: docs/design/2026-08-11__release-v8.6/trade-plan-completion-rate-metric/decision_record.md
Spec: docs/specs/frontend/pages/analytics.md §21
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# conftest.py registers a MagicMock stub at sys.modules["database"] (BLG-QA-20).
# Evict it so Python loads the real backend/database.py for the function under test.
sys.modules.pop("database", None)
import database  # noqa: E402


def _mock_conn(row):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = row
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn


def test_computes_completion_rate_from_mixed_plans():
    row = {"plans_created": 24, "plans_abandoned": 4, "plans_completed": 15}
    with patch.object(database, "get_db", return_value=_mock_conn(row)):
        result = database.get_trade_plan_completion_rate("portfolio-1")

    assert result == {
        "plans_created": 24,
        "plans_completed": 15,
        "plans_abandoned": 4,
        "completion_rate": 62.5,
    }


def test_zero_plans_created_returns_null_completion_rate_not_zero_percent():
    row = {"plans_created": 0, "plans_abandoned": 0, "plans_completed": 0}
    with patch.object(database, "get_db", return_value=_mock_conn(row)):
        result = database.get_trade_plan_completion_rate("portfolio-1")

    # Per decision_record.md §4: a null rate signals "no plans yet" so the
    # frontend can render its empty state rather than a misleading 0%.
    assert result["plans_created"] == 0
    assert result["completion_rate"] is None


def test_all_plans_abandoned_zero_completion_rate():
    row = {"plans_created": 5, "plans_abandoned": 5, "plans_completed": 0}
    with patch.object(database, "get_db", return_value=_mock_conn(row)):
        result = database.get_trade_plan_completion_rate("portfolio-1")

    assert result["completion_rate"] == 0.0
    assert result["plans_abandoned"] == 5


def test_all_plans_completed_full_completion_rate():
    row = {"plans_created": 8, "plans_abandoned": 0, "plans_completed": 8}
    with patch.object(database, "get_db", return_value=_mock_conn(row)):
        result = database.get_trade_plan_completion_rate("portfolio-1")

    assert result["completion_rate"] == 100.0


def test_null_row_counts_treated_as_zero():
    # FILTER(...) aggregates return NULL (not 0) when no source rows exist
    # at all for the portfolio -- guard against that mapping to a TypeError.
    row = {"plans_created": None, "plans_abandoned": None, "plans_completed": None}
    with patch.object(database, "get_db", return_value=_mock_conn(row)):
        result = database.get_trade_plan_completion_rate("portfolio-1")

    assert result == {
        "plans_created": 0,
        "plans_completed": 0,
        "plans_abandoned": 0,
        "completion_rate": None,
    }
