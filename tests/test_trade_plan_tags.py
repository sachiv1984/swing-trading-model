"""
Trade Plan Tags regression tests (ST-05, BLG-FEAT-52, EPIC-02, v6.8).

Trade-plan tags (`trade_plans.trade_tags`) are a new, data-independent field —
no dependency on trade_annotations/PO-02 (AC-04). Tag validation reuses the
journal_components.md §3/§4 rules (lowercase, alphanumeric+hyphen, max 20
chars, max 10 tags, dedup) already applied to positions.tags.

AC coverage:
    AC-01: user can add/remove tags on any trade plan — validation helper
           tested directly (pure function, no DB required)
    AC-02: GET /analytics/tag-performance win-rate/avg-R computation — tested
           against a mocked get_db() connection (no live database calls)

No live database calls — database.get_tag_performance / get_all_trade_plan_tags
are exercised against a mocked get_db() connection, following the same pattern
as test_signal_write_sanitization.py.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# conftest.py registers a MagicMock stub at sys.modules["database"] (BLG-QA-20).
# Evict it so Python loads the real backend/database.py for the functions under test.
sys.modules.pop("database", None)
import database  # noqa: E402

from routers.trade_plans import _validate_trade_tags  # noqa: E402


# ---------------------------------------------------------------------------
# _validate_trade_tags — pure validation unit tests
# ---------------------------------------------------------------------------

def test_lowercases_and_strips():
    assert _validate_trade_tags(["  Breakout  "]) == ["breakout"]


def test_rejects_disallowed_characters():
    assert _validate_trade_tags(["bad tag!", "ok-tag"]) == ["ok-tag"]


def test_allows_hyphen_and_digits():
    assert _validate_trade_tags(["earnings-play-2"]) == ["earnings-play-2"]


def test_max_20_chars_drops_overlong_tag():
    overlong = "a" * 21
    assert _validate_trade_tags([overlong, "momentum"]) == ["momentum"]


def test_exactly_20_chars_kept():
    exact = "a" * 20
    assert _validate_trade_tags([exact]) == [exact]


def test_dedup_preserves_first_occurrence():
    assert _validate_trade_tags(["momentum", "Momentum", "momentum"]) == ["momentum"]


def test_max_10_tags_truncates():
    tags = [f"tag{i}" for i in range(15)]
    result = _validate_trade_tags(tags)
    assert len(result) == 10
    assert result == [f"tag{i}" for i in range(10)]


def test_empty_input_returns_empty_list():
    assert _validate_trade_tags(None) == []
    assert _validate_trade_tags([]) == []


def test_blank_and_none_entries_dropped():
    assert _validate_trade_tags(["", "  ", "momentum"]) == ["momentum"]


# ---------------------------------------------------------------------------
# database.get_tag_performance — win rate / avg R-multiple aggregation
# ---------------------------------------------------------------------------

def _mock_conn(rows):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = rows
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def test_get_tag_performance_computes_win_rate_and_avg_r():
    rows = [
        # winner: entry 100, exit 110, stop 90 -> R = (110-100)/(100-90) = 1.0
        {"trade_tags": ["breakout"], "pnl": 500.0, "entry_price": 100.0, "exit_price": 110.0, "initial_stop": 90.0},
        # loser: entry 100, exit 95, stop 90 -> R = (95-100)/(100-90) = -0.5
        {"trade_tags": ["breakout"], "pnl": -250.0, "entry_price": 100.0, "exit_price": 95.0, "initial_stop": 90.0},
    ]
    mock_conn, _ = _mock_conn(rows)
    with patch.object(database, "get_db", return_value=mock_conn):
        result = database.get_tag_performance("portfolio-1", ["breakout"])

    assert len(result) == 1
    entry = result[0]
    assert entry["tag"] == "breakout"
    assert entry["trade_count"] == 2
    assert entry["win_rate"] == 50.0
    assert entry["avg_r_multiple"] == 0.25  # mean(1.0, -0.5)


def test_get_tag_performance_no_matching_trades_returns_zeroed_entry():
    mock_conn, _ = _mock_conn([])
    with patch.object(database, "get_db", return_value=mock_conn):
        result = database.get_tag_performance("portfolio-1", ["nonexistent"])

    assert result == [{"tag": "nonexistent", "win_rate": 0.0, "avg_r_multiple": None, "trade_count": 0}]


def test_get_tag_performance_missing_stop_excluded_from_avg_r_but_counted():
    rows = [
        {"trade_tags": ["momentum"], "pnl": 100.0, "entry_price": 100.0, "exit_price": 105.0, "initial_stop": None},
    ]
    mock_conn, _ = _mock_conn(rows)
    with patch.object(database, "get_db", return_value=mock_conn):
        result = database.get_tag_performance("portfolio-1", ["momentum"])

    entry = result[0]
    assert entry["trade_count"] == 1
    assert entry["win_rate"] == 100.0
    assert entry["avg_r_multiple"] is None


def test_get_tag_performance_multi_tag_rows_credited_to_each_matching_tag():
    rows = [
        {"trade_tags": ["breakout", "momentum"], "pnl": 200.0, "entry_price": 50.0, "exit_price": 55.0, "initial_stop": 45.0},
    ]
    mock_conn, _ = _mock_conn(rows)
    with patch.object(database, "get_db", return_value=mock_conn):
        result = database.get_tag_performance("portfolio-1", ["breakout", "momentum"])

    assert {r["tag"]: r["trade_count"] for r in result} == {"breakout": 1, "momentum": 1}


# ---------------------------------------------------------------------------
# database.get_all_trade_plan_tags — autocomplete source
# ---------------------------------------------------------------------------

def test_get_all_trade_plan_tags_returns_distinct_tags():
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"tag": "breakout"}, {"tag": "momentum"}]
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)

    with patch.object(database, "get_db", return_value=mock_conn):
        result = database.get_all_trade_plan_tags("portfolio-1")

    assert result == ["breakout", "momentum"]
