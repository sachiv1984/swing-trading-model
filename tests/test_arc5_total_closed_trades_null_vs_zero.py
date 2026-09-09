"""
Arc5 compliance total_closed_trades null-vs-zero regression tests
(ST-04, EPIC-01, v9.3, BLG-BE-111).

database.get_arc5_trade_plan_adherence_rate() previously returned
{"total_trades": 0} both for a genuine zero-trades portfolio and for a
missing/broken `trade_history` table (UndefinedColumn/UndefinedTable) —
indistinguishable to any caller. It must now return `total_trades: None` for
the schema-error case, reserving `0` for the genuine empty-portfolio case.

AC coverage:
- A missing/broken trade_history table no longer produces a total_closed_trades
  value indistinguishable from a genuine zero-trades portfolio (null on error
  vs. 0 on genuine empty).
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import psycopg2.errors
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

sys.modules.pop("database", None)
import database


def _mock_conn_with_cursor(cursor: MagicMock):
    cursor.__enter__ = MagicMock(return_value=cursor)
    cursor.__exit__ = MagicMock(return_value=False)
    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn


def test_genuine_zero_trades_returns_zero_not_none():
    cursor = MagicMock()
    cursor.fetchone.return_value = {"total": 0}
    conn = _mock_conn_with_cursor(cursor)

    result = database.get_arc5_trade_plan_adherence_rate(conn=conn)

    assert result == {"rate": None, "total_trades": 0}
    assert result["total_trades"] is not None


def test_missing_trade_history_table_returns_none_not_zero():
    cursor = MagicMock()
    cursor.execute.side_effect = psycopg2.errors.UndefinedTable("relation \"trade_history\" does not exist")
    conn = _mock_conn_with_cursor(cursor)
    conn.rollback = MagicMock()

    result = database.get_arc5_trade_plan_adherence_rate(conn=conn)

    assert result["total_trades"] is None
    assert result["rate"] is None
    conn.rollback.assert_called_once()


def test_broken_column_returns_none_not_zero():
    cursor = MagicMock()
    cursor.execute.side_effect = psycopg2.errors.UndefinedColumn("column \"position_id\" does not exist")
    conn = _mock_conn_with_cursor(cursor)
    conn.rollback = MagicMock()

    result = database.get_arc5_trade_plan_adherence_rate(conn=conn)

    assert result["total_trades"] is None


def test_trades_with_plans_computes_rate_and_real_count():
    cursor = MagicMock()
    cursor.fetchone.side_effect = [{"total": 10}, {"with_plan": 4}]
    conn = _mock_conn_with_cursor(cursor)

    result = database.get_arc5_trade_plan_adherence_rate(conn=conn)

    assert result == {"rate": 0.4, "total_trades": 10}


def test_endpoint_returns_json_null_not_zero_on_schema_error():
    """Integration: GET /analytics/arc5-compliance must surface total_closed_trades
    as JSON null (not 0) when the underlying table is missing/broken."""
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    from routers.analytics import router

    app = FastAPI()
    app.include_router(router)
    client = TestClient(app, raise_server_exceptions=False)

    with patch("routers.analytics.get_arc5_validation_pass_rate_by_rule", return_value=[]), \
         patch("routers.analytics.get_arc5_top_rule_breach", return_value=None), \
         patch("routers.analytics.get_arc5_events_per_week", return_value=0), \
         patch("routers.analytics.get_arc5_override_rate", return_value=None), \
         patch("routers.analytics.get_arc5_trade_plan_adherence_rate",
               return_value={"rate": None, "total_trades": None}), \
         patch("routers.analytics.get_db"):
        resp = client.get("/analytics/arc5-compliance")

    assert resp.status_code == 200
    body = resp.json()
    assert body["data"]["total_closed_trades"] is None


def test_endpoint_returns_zero_for_genuine_empty_portfolio():
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    from routers.analytics import router

    app = FastAPI()
    app.include_router(router)
    client = TestClient(app, raise_server_exceptions=False)

    with patch("routers.analytics.get_arc5_validation_pass_rate_by_rule", return_value=[]), \
         patch("routers.analytics.get_arc5_top_rule_breach", return_value=None), \
         patch("routers.analytics.get_arc5_events_per_week", return_value=0), \
         patch("routers.analytics.get_arc5_override_rate", return_value=None), \
         patch("routers.analytics.get_arc5_trade_plan_adherence_rate",
               return_value={"rate": None, "total_trades": 0}), \
         patch("routers.analytics.get_db"):
        resp = client.get("/analytics/arc5-compliance")

    assert resp.status_code == 200
    body = resp.json()
    assert body["data"]["total_closed_trades"] == 0
