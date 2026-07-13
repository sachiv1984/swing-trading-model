"""
Tests for utils.formatting.decimal_to_float — Decimal and numpy scalar coercion.

Regression coverage for the 2026-06-23 numpy 2.x upgrade (282bda4f) breaking
signal_service's DB writes: under numpy>=2.0, repr(np.float64(x)) renders as
"np.float64(x)" instead of a bare number, and psycopg2 embeds that repr as
the literal SQL parameter text. Postgres then parses "np.float64(...)" as a
schema-qualified function call and fails with 'schema "np" does not exist'.
decimal_to_float must strip numpy scalar wrappers before values reach any
DB write, not just at the JSON-response boundary.
"""

import importlib.util
from decimal import Decimal
from pathlib import Path

import numpy as np

# Loaded directly from file rather than `from utils.formatting import decimal_to_float`:
# tests/test_alerts_service.py and tests/test_trade_service.py replace
# sys.modules["utils.formatting"] with a passthrough MagicMock stub at import
# time and never restore it, which leaks into every test collected afterward
# in the same pytest process. Bypassing sys.modules here keeps this file's
# assertions honest regardless of collection order (tracked separately as a
# test-isolation cleanup item).
_spec = importlib.util.spec_from_file_location(
    "_formatting_under_test",
    Path(__file__).parent.parent / "backend" / "utils" / "formatting.py",
)
_formatting = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_formatting)
decimal_to_float = _formatting.decimal_to_float


def test_numpy_float64_converted_to_native_float():
    result = decimal_to_float(np.float64(230.55))
    assert result == 230.55
    assert type(result) is float


def test_numpy_int64_converted_to_native_int():
    result = decimal_to_float(np.int64(3))
    assert result == 3
    assert type(result) is int


def test_decimal_still_converted():
    result = decimal_to_float(Decimal("100.50"))
    assert result == 100.5
    assert type(result) is float


def test_nested_dict_with_numpy_and_decimal_scalars():
    signal_data = {
        "ticker": "NBIS",
        "rank": np.int64(1),
        "momentum_percent": np.float64(230.55),
        "current_price": np.float64(219.98),
        "cash": Decimal("5202.80"),
        "status": "new",
    }
    result = decimal_to_float(signal_data)

    assert result["ticker"] == "NBIS"
    assert type(result["rank"]) is int
    assert type(result["momentum_percent"]) is float
    assert type(result["current_price"]) is float
    assert type(result["cash"]) is float
    assert result["status"] == "new"


def test_list_of_numpy_scalars():
    result = decimal_to_float([np.float64(1.1), np.float64(2.2)])
    assert result == [1.1, 2.2]
    assert all(type(v) is float for v in result)


def test_plain_values_unaffected():
    assert decimal_to_float(5) == 5
    assert decimal_to_float("US") == "US"
    assert decimal_to_float(None) is None
