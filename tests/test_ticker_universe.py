"""
Unit tests for ticker_universe_service (DS-01 / ST-01)
"""
import pytest
from unittest.mock import MagicMock, patch, call


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(ticker="AAPL", market="US", active=True, sector=None, industry=None, created_at=None):
    row = {
        "ticker": ticker,
        "market": market,
        "active": active,
        "sector": sector,
        "industry": industry,
        "created_at": created_at,
    }
    mock = MagicMock()
    mock.__iter__ = lambda s: iter(row.items())
    mock.keys = lambda: row.keys()
    mock.__getitem__ = lambda s, k: row[k]
    # dict(row) works via keys + __getitem__
    mock._row = row
    return mock


def _patch_db(rows=None, rowcount=1):
    """Return a context-manager mock for get_db()."""
    cur = MagicMock()
    cur.fetchall.return_value = rows or []
    cur.fetchone.return_value = _make_row() if rows is None else (rows[0] if rows else None)
    cur.rowcount = rowcount
    conn = MagicMock()
    conn.__enter__ = lambda s: conn
    conn.__exit__ = MagicMock(return_value=False)
    conn.cursor.return_value.__enter__ = lambda s: cur
    conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    return conn, cur


# ---------------------------------------------------------------------------
# ensure_ticker_universe_table
# ---------------------------------------------------------------------------

def test_ensure_table_creates_table_and_indexes():
    conn, cur = _patch_db()
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import ensure_ticker_universe_table
        ensure_ticker_universe_table()
    assert cur.execute.call_count == 3
    first_sql = cur.execute.call_args_list[0][0][0]
    assert "CREATE TABLE IF NOT EXISTS ticker_universe" in first_sql


# ---------------------------------------------------------------------------
# get_all_tickers
# ---------------------------------------------------------------------------

def test_get_all_tickers_returns_list():
    row = _make_row("AAPL", "US")
    conn, cur = _patch_db(rows=[row])
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import get_all_tickers
        result = get_all_tickers()
    assert isinstance(result, list)


def test_get_all_tickers_filters_by_market():
    row = _make_row("HSBA.L", "UK")
    conn, cur = _patch_db(rows=[row])
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import get_all_tickers
        get_all_tickers(market="UK")
    sql = cur.execute.call_args[0][0]
    assert "market = %s" in sql


def test_get_all_tickers_includes_inactive_when_flag_false():
    conn, cur = _patch_db(rows=[])
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import get_all_tickers
        get_all_tickers(active_only=False)
    sql = cur.execute.call_args[0][0]
    assert "active = TRUE" not in sql


# ---------------------------------------------------------------------------
# add_ticker
# ---------------------------------------------------------------------------

def test_add_ticker_invalid_market_raises():
    from services.ticker_universe_service import add_ticker
    with pytest.raises(ValueError, match="market must be one of"):
        add_ticker("AAPL", "INVALID")


def test_add_ticker_empty_ticker_raises():
    from services.ticker_universe_service import add_ticker
    with pytest.raises(ValueError, match="ticker must not be empty"):
        add_ticker("  ", "US")


def test_add_ticker_upserts_row():
    row = _make_row("NVDA", "US", sector="Technology")
    conn, cur = _patch_db(rows=[row])
    cur.fetchone.return_value = row
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import add_ticker
        result = add_ticker("nvda", "US", sector="Technology")
    sql = cur.execute.call_args[0][0]
    assert "ON CONFLICT" in sql


def test_add_ticker_normalises_to_uppercase():
    row = _make_row("AAPL", "US")
    conn, cur = _patch_db(rows=[row])
    cur.fetchone.return_value = row
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import add_ticker
        add_ticker("aapl", "US")
    params = cur.execute.call_args[0][1]
    assert params[0] == "AAPL"


# ---------------------------------------------------------------------------
# soft_delete_ticker
# ---------------------------------------------------------------------------

def test_soft_delete_returns_true_on_success():
    conn, cur = _patch_db(rowcount=1)
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import soft_delete_ticker
        result = soft_delete_ticker("AAPL")
    assert result is True


def test_soft_delete_returns_false_when_not_found():
    conn, cur = _patch_db(rowcount=0)
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import soft_delete_ticker
        result = soft_delete_ticker("UNKNOWN")
    assert result is False


def test_soft_delete_normalises_to_uppercase():
    conn, cur = _patch_db(rowcount=1)
    with patch("services.ticker_universe_service.get_db", return_value=conn):
        from services.ticker_universe_service import soft_delete_ticker
        soft_delete_ticker("aapl")
    params = cur.execute.call_args[0][1]
    assert params[0] == "AAPL"
