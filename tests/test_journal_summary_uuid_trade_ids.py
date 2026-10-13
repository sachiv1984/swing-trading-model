"""
ST-01 (BLG-BE-162, EPIC-01, v9.12): POST /ai/journal-summary accepts the
UUID trade IDs that Trade History sends, end to end.

`trade_history.id` is a UUID, but `trade_ids` was typed `list[int]`, so
every request from Trade History failed with HTTP 422 before reaching the
AI. These tests post real UUIDs through the router and check that they
reach `fetch_journal_notes()` and the `ai_audit_log` write as UUID strings,
that integer IDs are now the ones rejected with 422, that the
`GET /ai/journal-summary/history?trade_id=` filter takes a UUID, and that
the DS-31 column migration is in `ensure_ai_audit_table()`.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    from fastapi.testclient import TestClient  # noqa: E402

    from main import app  # noqa: E402
    import database as real_database  # noqa: E402
    import routers.ai as ai_router  # noqa: E402
    from services.rate_limiter import _ai_limiter  # noqa: E402

CLIENT = TestClient(app)

_UUID_A = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
_UUID_B = "9b2e7c1d-0a4f-4e6b-8d3c-5f1a2b3c4d5e"

_SUMMARY = {"summary": "Recurring theme: patient entries.", "model": "m", "message": None}


def _reset_limiter():
    _ai_limiter.reset("journal-summary:testclient")


def _post(body):
    _reset_limiter()
    return CLIENT.post("/ai/journal-summary", json=body)


def test_uuid_trade_ids_reach_notes_query_and_audit_log():
    rows = [{"entry_note": "Entered on breakout", "exit_note": "Stopped out"}]
    with patch.object(ai_router, "fetch_journal_notes", return_value=rows) as fetch, \
         patch.object(ai_router, "summarise_journal_notes", return_value=_SUMMARY) as summarise, \
         patch.object(ai_router, "log_ai_summary_run") as log_run:
        resp = _post({"trade_ids": [_UUID_A, _UUID_B]})

    assert resp.status_code == 200
    body = resp.json()
    assert body["summary"] == _SUMMARY["summary"]
    assert body["trade_count"] == 1
    assert fetch.call_args.kwargs["trade_ids"] == [_UUID_A, _UUID_B]
    summarise.assert_called_once_with(["Entered on breakout", "Stopped out"])
    assert log_run.call_args.kwargs["trade_ids"] == [_UUID_A, _UUID_B]
    assert log_run.call_args.kwargs["trade_count"] == 1


def test_integer_trade_ids_rejected_with_422():
    with patch.object(ai_router, "fetch_journal_notes") as fetch:
        resp = _post({"trade_ids": [1, 2, 3]})
    assert resp.status_code == 422
    fetch.assert_not_called()


def test_non_uuid_string_rejected_with_422():
    with patch.object(ai_router, "fetch_journal_notes") as fetch:
        resp = _post({"trade_ids": ["not-a-uuid"]})
    assert resp.status_code == 422
    fetch.assert_not_called()


def test_date_range_request_still_logs_null_trade_ids():
    with patch.object(ai_router, "fetch_journal_notes", return_value=[]) as fetch, \
         patch.object(ai_router, "summarise_journal_notes", return_value=_SUMMARY), \
         patch.object(ai_router, "log_ai_summary_run") as log_run:
        resp = _post({"date_from": "2026-01-01"})
    assert resp.status_code == 200
    assert fetch.call_args.kwargs["trade_ids"] is None
    assert log_run.call_args.kwargs["trade_ids"] is None


def test_fetch_journal_notes_casts_trade_ids_to_uuid_array():
    database = real_database
    cur = MagicMock()
    cur.fetchall.return_value = []
    cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
    conn = MagicMock(__enter__=MagicMock(), __exit__=MagicMock(return_value=False))
    conn.__enter__.return_value = conn
    conn.cursor.return_value = cur_ctx
    with patch.object(database, "get_db", return_value=conn):
        database.fetch_journal_notes(trade_ids=[_UUID_A])
    sql, params = cur.execute.call_args[0]
    assert "ANY(%s::uuid[])" in sql
    assert params == ([_UUID_A],)


def test_history_filter_accepts_uuid_and_rejects_integer():
    with patch.object(ai_router, "query_audit_log", return_value=[]) as query:
        ok = CLIENT.get(f"/ai/journal-summary/history?trade_id={_UUID_A}")
        bad = CLIENT.get("/ai/journal-summary/history?trade_id=42")
    assert ok.status_code == 200
    assert query.call_args.kwargs["trade_id"] == _UUID_A
    assert bad.status_code == 422


def test_ensure_table_creates_uuid_column_and_migrates_integer_column():
    from services import ai_audit_service
    cur = MagicMock()
    cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
    conn = MagicMock(__exit__=MagicMock(return_value=False))
    conn.__enter__ = MagicMock(return_value=conn)
    conn.cursor.return_value = cur_ctx
    with patch.object(ai_audit_service, "get_db", return_value=conn):
        ai_audit_service.ensure_ai_audit_table()
    executed = " ".join(str(c.args[0]) for c in cur.execute.call_args_list)
    assert "trade_ids UUID[]" in executed
    assert "udt_name = '_int4'" in executed
    assert "ALTER COLUMN trade_ids TYPE UUID[] USING NULL" in executed


def test_audit_insert_casts_trade_ids_to_uuid_array():
    from services import ai_audit_service
    cur = MagicMock()
    cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
    conn = MagicMock(__exit__=MagicMock(return_value=False))
    conn.__enter__ = MagicMock(return_value=conn)
    conn.cursor.return_value = cur_ctx
    with patch.object(ai_audit_service, "get_db", return_value=conn):
        ai_audit_service.log_ai_summary_run([_UUID_A], None, None, 1, "m", "text")
    sql, params = cur.execute.call_args[0]
    assert "%s::uuid[]" in sql
    assert params[2] == [_UUID_A]
