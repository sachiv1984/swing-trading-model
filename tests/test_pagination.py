"""
Cursor pagination utility tests (ST-17, EPIC-06, v8.1, BLG-BE-47).

Pure-function tests for backend/utils/pagination.py — no DB required.
Reference migration (GET /trade-plans) is covered indirectly: these tests
exercise the exact functions that endpoint calls (cursor_where_clause,
paginate_results), so a regression in the shared helper is caught here
rather than only via a live-DB integration test.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from utils.pagination import (  # noqa: E402
    cursor_where_clause,
    decode_cursor,
    encode_cursor,
    paginate_results,
)


def test_encode_decode_cursor_roundtrip():
    ts = datetime(2026, 8, 1, 12, 30, 0, tzinfo=timezone.utc)
    cursor = encode_cursor(ts, "abc-123")
    decoded_ts, decoded_id = decode_cursor(cursor)
    assert decoded_ts == ts
    assert decoded_id == "abc-123"


def test_decode_cursor_malformed_raises_value_error():
    import pytest

    with pytest.raises(Exception):
        decode_cursor("not-a-valid-cursor!!!")


def test_cursor_where_clause_none_is_noop():
    sql, params = cursor_where_clause(None)
    assert sql == ""
    assert params == []


def test_cursor_where_clause_with_cursor():
    ts = datetime(2026, 8, 1, tzinfo=timezone.utc)
    cursor = encode_cursor(ts, "row-1")
    sql, params = cursor_where_clause(cursor)
    assert sql == "(created_at, id) < (%s, %s)"
    assert params == [ts, "row-1"]


def test_cursor_where_clause_custom_field_names():
    ts = datetime(2026, 8, 1, tzinfo=timezone.utc)
    cursor = encode_cursor(ts, "row-1")
    sql, _ = cursor_where_clause(cursor, created_field="updated_at", id_field="uuid")
    assert sql == "(updated_at, uuid) < (%s, %s)"


def test_paginate_results_no_more_pages():
    ts = datetime(2026, 8, 1, tzinfo=timezone.utc)
    rows = [{"id": str(i), "created_at": ts} for i in range(3)]
    page, next_cursor = paginate_results(rows, limit=5)
    assert len(page) == 3
    assert next_cursor is None


def test_paginate_results_has_more_pages():
    ts = datetime(2026, 8, 1, tzinfo=timezone.utc)
    # limit=2, fetch limit+1=3 rows (caller convention) -> has_more True
    rows = [{"id": str(i), "created_at": ts} for i in range(3)]
    page, next_cursor = paginate_results(rows, limit=2)
    assert len(page) == 2
    assert next_cursor is not None
    decoded_ts, decoded_id = decode_cursor(next_cursor)
    assert decoded_id == "1"  # last item in the trimmed page (0-indexed: rows[1])


def test_paginate_results_empty():
    page, next_cursor = paginate_results([], limit=10)
    assert page == []
    assert next_cursor is None
