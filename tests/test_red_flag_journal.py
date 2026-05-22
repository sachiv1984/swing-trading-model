"""
Unit tests for Red Flag Journal backend (SI-03 / ST-07, EPIC-03, v3.9)

Tests the GET /portfolio/red-flag-journal endpoint via the router.
Database functions are stubbed via conftest.py BLG-QA-08 harness.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from fastapi import FastAPI
    from routers.red_flag_journal import router
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def _empty_result(page=1, page_size=20):
    return {"total": 0, "page": page, "page_size": page_size, "items": []}


def _make_event(event_type="pre_entry_override", ticker="AAPL"):
    return {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "event_type": event_type,
        "ticker": ticker,
        "position_id": None,
        "context": {"source": "trade_plan", "override_acknowledged": True},
        "created_at": "2026-05-22T10:00:00+00:00",
    }


class TestEmptyJournal:
    def test_empty_journal_returns_empty_items(self, client):
        with (
            patch("routers.red_flag_journal.ensure_red_flag_events_table"),
            patch("routers.red_flag_journal.get_red_flag_events", return_value=_empty_result()) as mock_get,
        ):
            resp = client.get("/portfolio/red-flag-journal")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["data"]["total"] == 0
        assert data["data"]["items"] == []
        mock_get.assert_called_once_with(page=1, page_size=20, event_type=None, ticker=None, since=None)


class TestPagination:
    def test_pagination_params_forwarded(self, client):
        result = {"total": 50, "page": 3, "page_size": 10, "items": [_make_event()]}
        with (
            patch("routers.red_flag_journal.ensure_red_flag_events_table"),
            patch("routers.red_flag_journal.get_red_flag_events", return_value=result) as mock_get,
        ):
            resp = client.get("/portfolio/red-flag-journal?page=3&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        assert data["data"]["page"] == 3
        assert data["data"]["page_size"] == 10
        assert data["data"]["total"] == 50
        mock_get.assert_called_once_with(page=3, page_size=10, event_type=None, ticker=None, since=None)


class TestFilterByEventType:
    def test_filter_event_type_forwarded(self, client):
        result = {"total": 2, "page": 1, "page_size": 20, "items": [_make_event("pre_entry_override")]}
        with (
            patch("routers.red_flag_journal.ensure_red_flag_events_table"),
            patch("routers.red_flag_journal.get_red_flag_events", return_value=result) as mock_get,
        ):
            resp = client.get("/portfolio/red-flag-journal?event_type=pre_entry_override")
        assert resp.status_code == 200
        mock_get.assert_called_once_with(
            page=1, page_size=20, event_type="pre_entry_override", ticker=None, since=None
        )
        items = resp.json()["data"]["items"]
        assert len(items) == 1
        assert items[0]["event_type"] == "pre_entry_override"


class TestFilterByTicker:
    def test_filter_ticker_forwarded(self, client):
        result = {"total": 1, "page": 1, "page_size": 20, "items": [_make_event(ticker="NVDA")]}
        with (
            patch("routers.red_flag_journal.ensure_red_flag_events_table"),
            patch("routers.red_flag_journal.get_red_flag_events", return_value=result) as mock_get,
        ):
            resp = client.get("/portfolio/red-flag-journal?ticker=NVDA")
        assert resp.status_code == 200
        mock_get.assert_called_once_with(
            page=1, page_size=20, event_type=None, ticker="NVDA", since=None
        )
        items = resp.json()["data"]["items"]
        assert items[0]["ticker"] == "NVDA"


class TestSI01OverrideEventWrite:
    def test_create_plan_with_override_writes_event(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        import routers.trade_plans as tp_mod

        app = FastAPI()
        from routers.trade_plans import router as tp_router
        app.include_router(tp_router)
        c = TestClient(app)

        mock_plan = {
            "id": "plan-1", "ticker": "AAPL", "market": "US",
            "position_id": None, "setup_type": None, "setup_thesis": None,
            "entry_rationale": None, "regime_context_at_entry": None,
            "r_target": None, "early_exit_conditions": None,
            "confirmation_criteria": None, "checklist_completed": False,
            "checklist_items": "[]", "status": "draft",
            "pre_entry_override_acknowledged": True,
            "created_at": None, "updated_at": None, "abandonment_reason": None,
        }
        with (
            patch.object(tp_mod, "ensure_trade_plans_table"),
            patch.object(tp_mod, "get_portfolio", return_value={"id": "port-1"}),
            patch.object(tp_mod, "create_trade_plan", return_value=mock_plan),
            patch.object(tp_mod, "ensure_red_flag_events_table"),
            patch.object(tp_mod, "create_red_flag_event") as mock_write,
        ):
            resp = c.post("/trade-plans", json={
                "ticker": "AAPL",
                "market": "US",
                "pre_entry_override_acknowledged": True,
            })
        assert resp.status_code == 201
        mock_write.assert_called_once()
        call_kwargs = mock_write.call_args
        assert call_kwargs.kwargs.get("event_type") == "pre_entry_override" or \
               call_kwargs.args[0] == "pre_entry_override"
