"""
BLG-BE-94 regression tests (ST-12, EPIC-02, v8.8).

Pre-Trade Research View query-latency budget review: routers/research.py's
_get_signal() previously fetched every signal ever generated for the
portfolio (services.signal_service.get_signals(), unbounded, no LIMIT) and
filtered to one ticker in Python on every research page load — a query
cost that grows unbounded with the signals table's history. Replaced with
a targeted database.get_signals_for_ticker(portfolio_id, ticker) query
(uses idx_signals_portfolio for the portfolio predicate and the new
functional index idx_signals_ticker_upper for the UPPER(ticker) predicate
— see database.ensure_signals_ticker_upper_index(), added after an
agent-mediated Head of Engineering review caught that the pre-existing
plain idx_signals_ticker cannot serve a UPPER()-wrapped predicate), with
an identical selection tie-break in Python afterward — same result, less
I/O and a real index path instead of a scan.
"""
import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import routers.research as research  # noqa: E402
import services.signal_service as signal_service  # noqa: E402

# conftest.py replaces sys.modules["database"] (session-wide, process-global)
# with an auto-derived stub whose function bodies are bare MagicMocks — see
# tests/test_position_audit_log.py's identical convention. Loading a private,
# independent copy of the real module via importlib exercises the real
# get_signals_for_ticker() query shape rather than a MagicMock stand-in.
_db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
_spec = importlib.util.spec_from_file_location('database_real_for_research_signal_lookup_test', _db_path)
_real_database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real_database)


def _signal_row(ticker="AAPL", signal_date="2026-08-01", status="new", rank=1,
                 current_price=150.0, initial_stop=140.0):
    return {
        "id": f"sig-{ticker}-{signal_date}",
        "ticker": ticker,
        "signal_date": signal_date,
        "status": status,
        "rank": rank,
        "direction": "long",
        "current_price": current_price,
        "initial_stop": initial_stop,
        "atr_value": 3.0,
    }


class TestSignalServiceGetSignalsForTicker:
    def test_calls_db_function_with_portfolio_id_and_ticker(self):
        with patch.object(signal_service, "get_portfolio", return_value={"id": "pf-1"}), \
             patch.object(signal_service, "db_get_signals_for_ticker", return_value=[_signal_row()]) as mock_db:
            result = signal_service.get_signals_for_ticker("AAPL")

        mock_db.assert_called_once_with("pf-1", "AAPL")
        assert len(result) == 1
        assert result[0]["ticker"] == "AAPL"

    def test_raises_when_no_portfolio(self):
        with patch.object(signal_service, "get_portfolio", return_value=None):
            try:
                signal_service.get_signals_for_ticker("AAPL")
                assert False, "expected ValueError"
            except ValueError:
                pass


class TestResearchGetSignalUsesTargetedLookup:
    def test_calls_get_signals_for_ticker_not_full_get_signals(self):
        with patch.object(research, "get_signals_for_ticker", return_value=[_signal_row()]) as mock_lookup:
            result = research._get_signal("AAPL", "pf-1")

        mock_lookup.assert_called_once_with("AAPL")
        assert result["signal_id"] == "sig-AAPL-2026-08-01"

    def test_selects_most_recent_signal_by_date(self):
        """Same tie-break behaviour as before this story: highest signal_date wins."""
        rows = [
            _signal_row(signal_date="2026-07-01", status="new"),
            _signal_row(signal_date="2026-08-01", status="dismissed"),
        ]
        with patch.object(research, "get_signals_for_ticker", return_value=rows):
            result = research._get_signal("AAPL", "pf-1")

        assert result["signal_date"] == "2026-08-01"

    def test_no_signals_returns_none(self):
        with patch.object(research, "get_signals_for_ticker", return_value=[]):
            result = research._get_signal("AAPL", "pf-1")

        assert result is None

    def test_lookup_exception_returns_none_not_raises(self):
        with patch.object(research, "get_signals_for_ticker", side_effect=Exception("db down")):
            result = research._get_signal("AAPL", "pf-1")

        assert result is None


class TestDatabaseGetSignalsForTicker:
    """Exercises the real database.py query shape (loaded independently of
    the process-global stub — see module docstring above)."""

    def test_query_filters_by_portfolio_and_ticker(self):
        cur = MagicMock()
        cur.fetchall.return_value = [_signal_row()]
        cur_ctx = MagicMock()
        cur_ctx.__enter__ = MagicMock(return_value=cur)
        cur_ctx.__exit__ = MagicMock(return_value=False)
        conn = MagicMock()
        conn.cursor.return_value = cur_ctx
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)

        with patch.object(_real_database, "get_db", return_value=conn):
            result = _real_database.get_signals_for_ticker("pf-1", "AAPL")

        query, params = cur.execute.call_args.args
        assert "WHERE portfolio_id = %s AND UPPER(ticker) = UPPER(%s)" in query
        assert "signals" in query
        assert params == ("pf-1", "AAPL")
        assert result == [_signal_row()]

    def test_ensure_signals_ticker_upper_index_creates_functional_index(self):
        """Head-of-Engineering-review correction (§5.3 retry 1, ST-12): the
        UPPER(ticker) predicate above requires a matching functional index —
        a plain index on ticker cannot serve it."""
        cur = MagicMock()
        cur_ctx = MagicMock()
        cur_ctx.__enter__ = MagicMock(return_value=cur)
        cur_ctx.__exit__ = MagicMock(return_value=False)
        conn = MagicMock()
        conn.cursor.return_value = cur_ctx
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)

        with patch.object(_real_database, "get_db", return_value=conn):
            _real_database.ensure_signals_ticker_upper_index()

        (query,) = cur.execute.call_args.args
        assert "CREATE INDEX IF NOT EXISTS idx_signals_ticker_upper" in query
        assert "UPPER(ticker)" in query
