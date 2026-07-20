"""
Standing regression suite — ticker/market input sanitisation.

ST-08 (BLG-QA-69, EPIC-08, v7.6). Consolidates the BLG-SEC-01/BLG-SEC-02
security-fix test cases (injection strings, trailing-newline bypass,
invalid ticker/market values) into one dedicated, clearly-named suite
covering all 4 previously-vulnerable write paths, so a regression in any
of them is caught under one obvious file name rather than requiring a
reader to already know these two fix commits exist.

This file intentionally does NOT duplicate the full behavioural coverage
already present in tests/test_signal_write_sanitization.py (BLG-SEC-02,
BLG-SEC-08) and tests/test_ai_chat_schema.py (BLG-SEC-01) — those remain
the source of truth for exhaustive unit coverage of each fix. This suite
is a focused regression guard: one high-signal assertion per attack class
per path, run together so "did any of the 4 paths regress" is one file
and one pytest invocation away.

The 4 previously-vulnerable paths (per stage4_backlog_slice.md#ST-08):
    1. database.create_signal            (BLG-SEC-02, v6.4 ST-03)
    2. database.create_rebalance_exit_signal (BLG-SEC-02, v6.4 ST-03)
    3. database.update_signal             (BLG-SEC-02, v6.4 ST-03)
    4. ai_service.ai_chat context_opts.ticker (BLG-SEC-01, v6.4 ST-02)

No live database or LLM calls — signal write paths are exercised against
a mocked get_db() connection; ai_chat's context_opts validation is
exercised directly via _validate_context_ticker (raises before any
network call is made).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# See tests/test_signal_write_sanitization.py for the rationale — conftest.py's
# database stub lacks the real implementations under test here.
sys.modules.pop("database", None)
import database  # noqa: E402

from services.ai_service import _validate_context_ticker  # noqa: E402


INJECTION_STRING = "AAPL<script>alert(1)</script>; DROP TABLE signals;--"
TRAILING_NEWLINE_TICKER = "AAPL\n"  # BLG-SEC-01's specific regression: a bare
# trailing newline with no content after it — Python's `$` anchor matches
# immediately before a trailing '\n', so a naive `re.match(r'^[...]+$')`
# would incorrectly accept this. Validation must use fullmatch (or an
# equivalent \Z-anchored pattern).
INVALID_MARKET = "US; DROP TABLE portfolios;--"


def _mock_conn():
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {"id": "sig-1"}
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


# ---------------------------------------------------------------------------
# Path 1 — database.create_signal
# ---------------------------------------------------------------------------

def test_create_signal_rejects_injection_string():
    mock_conn, mock_cursor = _mock_conn()
    signal_data = {
        "ticker": INJECTION_STRING, "market": INVALID_MARKET,
        "signal_date": "2026-07-20", "rank": 1, "momentum_percent": 10.0,
        "current_price": 100.0, "price_gbp": 80.0, "atr_value": 2.0,
        "volatility": 0.1, "initial_stop": 90.0, "suggested_shares": 5,
        "allocation_gbp": 400.0, "total_cost": 400.0,
    }
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_signal("p-001", signal_data)

    inserted_ticker, inserted_market = mock_cursor.execute.call_args[0][1][1:3]
    assert ";" not in inserted_ticker and "<" not in inserted_ticker
    assert len(inserted_ticker) <= 12
    assert ";" not in inserted_market and len(inserted_market) <= 12


# ---------------------------------------------------------------------------
# Path 2 — database.create_rebalance_exit_signal
# ---------------------------------------------------------------------------

def test_create_rebalance_exit_signal_rejects_injection_string():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_rebalance_exit_signal(
            portfolio_id="p-001", ticker=INJECTION_STRING, market=INVALID_MARKET,
            current_price=100.0, price_gbp=80.0, signal_date="2026-07-20", reason="test",
        )

    inserted_ticker = mock_cursor.execute.call_args[0][1][1]
    assert ";" not in inserted_ticker and "<" not in inserted_ticker
    assert len(inserted_ticker) <= 12


# ---------------------------------------------------------------------------
# Path 3 — database.update_signal
# ---------------------------------------------------------------------------

def test_update_signal_rejects_injection_string_in_ticker():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.update_signal("sig-1", {"ticker": INJECTION_STRING})

    updated_ticker = mock_cursor.execute.call_args[0][1][0]
    assert ";" not in updated_ticker and "<" not in updated_ticker
    assert len(updated_ticker) <= 12


def test_update_signal_rejects_unvalidated_column_key():
    """BLG-SEC-08: dict keys are spliced into the SQL UPDATE as column names —
    an unrecognised key must be rejected before any SQL is built."""
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        with pytest.raises(ValueError, match="Unrecognised signal field"):
            database.update_signal("sig-1", {"1=1; DROP TABLE signals;--": "x"})
    mock_cursor.execute.assert_not_called()


# ---------------------------------------------------------------------------
# Path 4 — ai_service.ai_chat context_opts.ticker
# ---------------------------------------------------------------------------

def test_context_ticker_rejects_injection_string():
    with pytest.raises(HTTPException) as exc_info:
        _validate_context_ticker({"ticker": INJECTION_STRING})
    assert exc_info.value.status_code == 422


def test_context_ticker_rejects_trailing_newline_bypass():
    """The specific BLG-SEC-01 regression: re.match(r'^[...]+$') incorrectly
    accepts a bare trailing newline because `$` matches before it. Must use
    fullmatch (or \\Z-anchored) validation to close this gap."""
    with pytest.raises(HTTPException) as exc_info:
        _validate_context_ticker({"ticker": TRAILING_NEWLINE_TICKER})
    assert exc_info.value.status_code == 422


def test_context_ticker_accepts_valid_value():
    """Regression guard for the inverse case — a legitimate ticker must not
    be rejected by an over-tightened fix."""
    _validate_context_ticker({"ticker": "VOD.L"})  # must not raise
