"""
POST /digest/events (ST-17, EPIC-03, v9.18, BLG-FEAT-103; digest_endpoints.md v0.8).

- The two event types are written; anything else is a 400 and writes nothing.
- dry_run validates and writes nothing (the System Status endpoint test).
- A failed write is a 500 with the error envelope.
- The table is ensured once per process, before the first write.
"""
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

import routers.digest as digest
from main import app

CLIENT = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_table_flag():
    digest._loop_events_table_ready = False
    yield
    digest._loop_events_table_ready = False


@pytest.mark.parametrize("event_type", ["weekly_digest_opened", "due_today_action"])
def test_writes_each_event_type(event_type):
    with patch.object(digest, "ensure_loop_events_table") as ensure, patch.object(digest, "record_loop_event") as record:
        resp = CLIENT.post("/digest/events", json={"event_type": event_type})
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "data": {"event_type": event_type, "written": True}}
    record.assert_called_once_with(event_type)
    ensure.assert_called_once()


def test_table_is_ensured_once_per_process():
    with patch.object(digest, "ensure_loop_events_table") as ensure, patch.object(digest, "record_loop_event"):
        CLIENT.post("/digest/events", json={"event_type": "weekly_digest_opened"})
        CLIENT.post("/digest/events", json={"event_type": "due_today_action"})
    ensure.assert_called_once()


@pytest.mark.parametrize("event_type", ["page_view", "", "WEEKLY_DIGEST_OPENED"])
def test_unknown_event_type_is_400_and_writes_nothing(event_type):
    with patch.object(digest, "record_loop_event") as record:
        resp = CLIENT.post("/digest/events", json={"event_type": event_type})
    assert resp.status_code == 400
    assert resp.json()["status"] == "error"
    record.assert_not_called()


def test_dry_run_writes_nothing():
    with patch.object(digest, "ensure_loop_events_table") as ensure, patch.object(digest, "record_loop_event") as record:
        resp = CLIENT.post("/digest/events", json={"event_type": "weekly_digest_opened", "dry_run": True})
    assert resp.status_code == 200
    assert resp.json()["data"] == {"event_type": "weekly_digest_opened", "written": False}
    record.assert_not_called()
    ensure.assert_not_called()


def test_missing_body_is_422():
    assert CLIENT.post("/digest/events").status_code == 422


def test_failed_write_is_500():
    with patch.object(digest, "ensure_loop_events_table"), \
         patch.object(digest, "record_loop_event", side_effect=RuntimeError("db down")):
        resp = CLIENT.post("/digest/events", json={"event_type": "weekly_digest_opened"})
    assert resp.status_code == 500
    assert resp.json() == {"status": "error", "message": "Failed to record event"}


def test_endpoint_test_entry_uses_dry_run():
    """The System Status test entry must never write a real event (it would count as a review)."""
    import inspect
    import routers.test as endpoint_tests

    src = inspect.getsource(endpoint_tests)
    line = next(l for l in src.splitlines() if '"POST /digest/events"' in l)
    assert '"dry_run": True' in line


def test_router_event_types_match_database():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
    from tests._real_database import real_database_imports

    with real_database_imports():
        import database as real_database
    assert digest.LOOP_EVENT_TYPES == real_database.LOOP_EVENT_TYPES



# ---------------------------------------------------------------------------
# System Status test runs leave no loop data behind (ST-17 review finding).
# ---------------------------------------------------------------------------
import asyncio  # noqa: E402
from unittest.mock import AsyncMock, MagicMock  # noqa: E402

import routers.test as endpoint_tests  # noqa: E402


def _response(body):
    resp = MagicMock()
    resp.json.return_value = body
    return resp


def test_created_trade_plan_is_deleted_after_the_test_call():
    client = MagicMock()
    client.request = AsyncMock()
    entry = {"name": "POST /trade-plans", "cleanup_delete": "http://api/trade-plans/{id}"}
    asyncio.run(endpoint_tests._cleanup_created_row(client, entry, _response({"status": "ok", "data": {"id": "p-1"}}), {"X-API-Key": "k"}))
    client.request.assert_awaited_once_with("DELETE", "http://api/trade-plans/p-1", headers={"X-API-Key": "k"})


def test_cleanup_is_skipped_without_an_id_or_a_template_and_never_raises():
    client = MagicMock()
    client.request = AsyncMock(side_effect=RuntimeError("network"))
    asyncio.run(endpoint_tests._cleanup_created_row(client, {"name": "x"}, _response({"data": {"id": "p"}}), {}))
    asyncio.run(endpoint_tests._cleanup_created_row(client, {"name": "x", "cleanup_delete": "u/{id}"}, _response({"data": None}), {}))
    client.request.assert_not_awaited()
    # A failing DELETE is swallowed.
    asyncio.run(endpoint_tests._cleanup_created_row(client, {"name": "x", "cleanup_delete": "u/{id}"}, _response({"data": {"id": "p"}}), {}))


def test_post_trade_plans_entry_has_cleanup():
    import inspect
    src = inspect.getsource(endpoint_tests)
    line = next(l for l in src.splitlines() if '"POST /trade-plans"' in l)
    assert '"cleanup_delete": f"{base_url}/trade-plans/{{id}}"' in line


def test_concurrent_first_calls_create_the_table_once():
    import threading as _t
    import time as _time

    calls = []

    def slow_ensure():
        calls.append(1)
        _time.sleep(0.05)

    with patch.object(digest, "ensure_loop_events_table", side_effect=slow_ensure), patch.object(digest, "record_loop_event"):
        threads = [_t.Thread(target=lambda: CLIENT.post("/digest/events", json={"event_type": "weekly_digest_opened"})) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    assert len(calls) == 1
