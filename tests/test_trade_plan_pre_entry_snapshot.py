"""
ST-05 (EPIC-02, v9.16, BLG-FE-271): the Trade Plan form saves a dated
pre-entry snapshot (trade_plan.md v1.22 §5e), and Trade Entry re-runs the
checks for a plan-linked entry whose snapshot is stale or holds an
unacknowledged WARN/FAIL (position_form.md v1.14 §Pre-Entry Checks).

Backend side:
- PUT /trade-plans/{id} stores pre_entry_validation_snapshot as JSONB, so an
  edited plan's snapshot is replaced (database.update_trade_plan).
- A snapshot change is structural, so it is not written to the post-entry
  audit log.
- Saving the plan-linked entry with the acknowledgement writes one
  pre_entry_override event with source "trade_entry" (ST-05 AC 2).

No live database: get_db() and the event writer are mocked.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

_db_path = os.path.join(os.path.dirname(__file__), "..", "backend", "database.py")
_spec = importlib.util.spec_from_file_location("database_real_for_pre_entry_snapshot_test", _db_path)
database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(database)

_SNAPSHOT = {
    "captured_at": "2026-11-09T10:00:00.000Z",
    "advisory_status": "warn",
    "checks": [{"rule": "earnings_proximity", "status": "warn", "detail": "Earnings in 3 days"}],
    "inputs": {"quantity": 50, "entry_price": 150.0, "stop_price": 142.0},
}


def _mock_conn():
    mock_cursor = MagicMock()
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


class TestUpdateStoresSnapshot:
    def test_snapshot_is_written_as_jsonb(self):
        mock_conn, mock_cursor = _mock_conn()
        mock_cursor.fetchone.return_value = {"id": "plan-1", "position_id": None}
        with patch.object(database, "get_db", return_value=mock_conn), \
             patch.object(database, "get_trade_plan_by_id", return_value={"id": "plan-1", "position_id": None}):
            database.update_trade_plan("plan-1", "portfolio-1", {"pre_entry_validation_snapshot": _SNAPSHOT})
        sql, values = mock_cursor.execute.call_args.args
        assert "pre_entry_validation_snapshot = %s::jsonb" in sql
        assert json.loads(values[0]) == _SNAPSHOT

    def test_snapshot_change_is_not_audit_logged_post_entry(self):
        before = {"id": "plan-1", "position_id": "pos-1", "pre_entry_validation_snapshot": None}
        after = {"id": "plan-1", "position_id": "pos-1", "pre_entry_validation_snapshot": _SNAPSHOT}
        mock_conn, mock_cursor = _mock_conn()
        mock_cursor.fetchone.return_value = after
        calls = []
        with patch.object(database, "get_db", return_value=mock_conn), \
             patch.object(database, "get_trade_plan_by_id", return_value=before), \
             patch.object(database, "create_trade_plan_audit_log_entry", side_effect=lambda *a: calls.append(a)):
            database.update_trade_plan("plan-1", "portfolio-1", {"pre_entry_validation_snapshot": _SNAPSHOT})
        assert calls == []


class TestUpdateRouterAcceptsSnapshot:
    def test_put_passes_snapshot_to_update(self):
        from tests._real_database import real_database_imports
        with real_database_imports():
            from fastapi.testclient import TestClient
            import main
            from routers import trade_plans
        client = TestClient(main.app, raise_server_exceptions=False)
        existing = {"id": "11111111-1111-1111-1111-111111111111", "position_id": None, "status": "draft"}
        with patch.object(trade_plans, "ensure_trade_plans_table"), \
             patch.object(trade_plans, "_get_portfolio_id", return_value="portfolio-1"), \
             patch.object(trade_plans, "get_trade_plan_by_id", return_value=existing), \
             patch.object(trade_plans, "update_trade_plan", return_value=existing) as mock_update:
            response = client.put(
                f"/trade-plans/{existing['id']}",
                json={"pre_entry_validation_snapshot": _SNAPSHOT},
            )
        assert response.status_code == 200, response.text
        assert mock_update.call_args.args[2]["pre_entry_validation_snapshot"] == _SNAPSHOT


class TestPlanLinkedEntryOverrideEvent:
    def test_plan_linked_acknowledged_entry_writes_one_trade_entry_event(self):
        from tests._real_database import real_database_imports
        with real_database_imports():
            from fastapi.testclient import TestClient
            import main
        import database as db
        client = TestClient(main.app, raise_server_exceptions=False)
        body = {
            "ticker": "AAPL", "market": "US", "entry_date": "2026-11-09",
            "shares": 10, "entry_price": 100.0, "fx_rate": 1.3,
            "trade_plan_id": "11111111-1111-1111-1111-111111111111",
            "pre_entry_override_acknowledged": True,
        }
        result = {"position_id": "pos-1", "ticker": "AAPL", "initial_stop": 90.0}
        with patch.object(main, "add_position", return_value=result) as mock_add, \
             patch.object(db, "ensure_red_flag_events_table"), \
             patch.object(db, "create_red_flag_event") as mock_event, \
             patch("services.alpaca_paper_sync_service.sync_open_paper_position", create=True):
            response = client.post("/portfolio/position", json=body)
        assert response.status_code == 200, response.text
        assert mock_add.call_args.kwargs["trade_plan_id"] == body["trade_plan_id"]
        mock_event.assert_called_once_with(
            event_type="pre_entry_override",
            ticker="AAPL",
            position_id="pos-1",
            context={"source": "trade_entry", "override_acknowledged": True},
        )
