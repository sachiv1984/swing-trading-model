"""
Regression coverage — numpy scalar handling in create_rebalance_exit_signal.

ST-08 (EPIC-08, v7.7, BLG-QA-104). Guards against recurrence of the PR #971
defect class: under numpy>=2.0, repr(np.float64(x)) renders as "np.float64(x)"
rather than a bare number, and psycopg2's parameter adapter embeds that repr
as literal SQL text — Postgres then fails with 'schema "np" does not exist'.

test_formatting.py already covers decimal_to_float() in isolation (unit-level
numpy/Decimal coercion). This file closes the gap one level up: it exercises
the REAL generate_rebalance_exit_signals() -> decimal_to_float() ->
create_rebalance_exit_signal() call chain end-to-end, with numpy-typed
position data (as would occur if get_positions()/pricing enrichment produced
numpy scalars, e.g. from a pandas/yfinance source) and a mocked get_db(),
asserting the values that actually reach psycopg2's cursor.execute() are
native Python types — not numpy scalars. Unlike test_nightly_computations.py's
RX-01..RX-05 suite (which mocks create_rebalance_exit_signal out entirely and
bypasses decimal_to_float via a passthrough side_effect specifically to
isolate signal-selection logic), this test intentionally uses the REAL
decimal_to_float and the REAL create_rebalance_exit_signal so a future
regression in either would be caught here.

No live database calls — get_db() is mocked to isolate the type-safety
property under test from actual SQL execution.

Test-isolation note: this file deliberately does NOT pop/reimport
sys.modules["services.signal_service"] — doing so creates a second, distinct
module object that diverges from the one other test files in the same pytest
session already hold a reference to (`from services.signal_service import
generate_rebalance_exit_signals` binds a function object from whichever
module object existed at that import time), which broke
test_nightly_computations.py's RX-02/03/05 when both files ran in the same
session. Instead, the real create_rebalance_exit_signal and decimal_to_float
are obtained via a fresh `database` import and a direct file-load of
utils/formatting.py (mirroring test_formatting.py's own technique) and
patched onto whatever `services.signal_service` module object is already
cached — this changes no module identities, only attribute values, and only
for the duration of each `with` block.
"""

import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Evict any stub sys.modules["database"] (conftest.py's MagicMock stub lacks
# the real create_rebalance_exit_signal implementation under test here) — same
# defensive pattern as test_signal_write_sanitization.py / test_api_contracts.py.
# services.signal_service is intentionally left untouched (see module docstring).
sys.modules.pop("database", None)

import database  # noqa: E402
import services.signal_service as signal_service  # noqa: E402

# Load the real decimal_to_float directly from file, bypassing sys.modules
# entirely (utils.pricing/utils.formatting may be stubbed by other test files
# still cached in this session) — same technique as test_formatting.py.
_spec = importlib.util.spec_from_file_location(
    "_formatting_under_test_rx08",
    Path(__file__).parent.parent / "backend" / "utils" / "formatting.py",
)
_formatting = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_formatting)
real_decimal_to_float = _formatting.decimal_to_float


def _mock_conn():
    """Build a mock get_db() context manager returning a mock cursor."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {"id": "sig-numpy-regression"}
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def test_create_rebalance_exit_signal_direct_call_binds_native_types_when_given_native_args():
    """Baseline: the real create_rebalance_exit_signal, called with the native
    types decimal_to_float is expected to produce, passes native types
    straight through to psycopg2 (sanity check the function itself doesn't
    reintroduce numpy anywhere internally, e.g. via arithmetic on its args)."""
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_rebalance_exit_signal(
            portfolio_id="p-001",
            ticker="TSLA",
            market="US",
            current_price=250.0,
            price_gbp=196.85,
            signal_date="2026-06-30",
            reason="test",
        )

    params = mock_cursor.execute.call_args[0][1]
    for value in params:
        assert not isinstance(value, (np.floating, np.integer)), (
            f"numpy scalar reached psycopg2 params: {value!r} ({type(value)})"
        )


def test_generate_rebalance_exit_signals_end_to_end_with_numpy_position_data():
    """End-to-end regression: get_positions() returns numpy-typed
    current_price/current_stop (simulating a pandas/yfinance-derived value
    leaking into the position dict, the exact PR #971 defect shape) — by the
    time create_rebalance_exit_signal's INSERT executes, every bound
    parameter must be a native Python type."""
    rebalance_day = datetime(2026, 6, 30)

    mock_conn, mock_cursor = _mock_conn()

    # get_live_fx_rate is left as a plain native float below (matching its real
    # implementation, utils/pricing.py, which parses a JSON HTTP response —
    # never a pandas/numpy value) — the numpy leak under test is specifically
    # the get_positions()-derived data path, matching the documented PR #971
    # defect shape. create_rebalance_exit_signal and decimal_to_float are
    # explicitly pointed at their REAL implementations (not whatever this
    # session's cached services.signal_service module happens to have bound
    # them to) so this test exercises the actual production code path.
    with patch.object(signal_service, "get_portfolio", return_value={"id": "portfolio-001"}), \
         patch.object(signal_service, "db_get_signals", return_value=[
             {"ticker": "AAPL", "signal_date": "2026-06-30", "status": "new"},
         ]), \
         patch.object(signal_service, "get_positions", return_value=[
             {
                 "ticker": "TSLA",  # NOT in top-5 ("AAPL")
                 "market": "US",
                 "current_price": np.float64(250.1234),
                 "current_stop": np.float64(200.5),
             }
         ]), \
         patch.object(signal_service, "get_live_fx_rate", return_value=1.27), \
         patch.object(signal_service, "decimal_to_float", real_decimal_to_float), \
         patch.object(signal_service, "create_rebalance_exit_signal", database.create_rebalance_exit_signal), \
         patch.object(database, "get_db", return_value=mock_conn), \
         patch("services.signal_service.datetime") as mock_dt:
        mock_dt.now.return_value = rebalance_day
        result = signal_service.generate_rebalance_exit_signals()

    assert result["is_last_trading_day"] is True
    assert result["signals_created"] == 1
    mock_cursor.execute.assert_called_once()

    params = mock_cursor.execute.call_args[0][1]
    for value in params:
        assert not isinstance(value, (np.floating, np.integer)), (
            f"numpy scalar reached psycopg2 params: {value!r} ({type(value)}) — "
            "decimal_to_float() upstream did not fully convert this value "
            "before it reached create_rebalance_exit_signal's INSERT (PR #971 "
            "defect class: repr(np.float64(x)) embeds as 'np.float64(x)' in "
            "the SQL text, and Postgres fails with 'schema \"np\" does not exist')."
        )

    # Also confirm the specific numeric fields resolved to the expected native
    # values. Param order matches create_rebalance_exit_signal's cur.execute()
    # call: (portfolio_id, ticker, market, signal_date, current_price, price_gbp, reason).
    inserted_current_price = params[4]
    inserted_price_gbp = params[5]
    assert inserted_current_price == pytest.approx(250.12)
    assert type(inserted_current_price) is float
    assert type(inserted_price_gbp) is float
