"""
BLG-BE-84 regression tests (ST-09, EPIC-02, v8.8).

Real alert-to-trade provenance: POST /trade-plans now accepts an optional
triggered_by_price_alert_id, persisted to a new nullable trade_plans column
(data_model.md DS-15). Set only via the alert-notification-to-trade-plan UI
path; null for plans created any other way.
"""
import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import routers.trade_plans as trade_plans_router  # noqa: E402

# conftest.py replaces sys.modules["database"] (session-wide, process-global)
# with an auto-derived stub — loading a private, independent copy of the real
# module via importlib exercises the real create_trade_plan() INSERT shape
# rather than a MagicMock stand-in (same convention as
# test_position_audit_log.py / test_position_state_history.py).
_db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
_spec = importlib.util.spec_from_file_location('database_real_for_price_alert_trade_plan_linkage_test', _db_path)
_real_database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real_database)


class TestCreatePlanRouterAcceptsField:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(trade_plans_router, name, **kwargs)
        self._patches.append(p)
        return p.start()

    def _install_common_mocks(self, create_return):
        self._patch("ensure_trade_plans_table")
        self._patch("ensure_si02_trade_plans_columns")
        self._patch("ensure_strategy_version_at_entry_columns")
        self._patch("ensure_triggered_by_price_alert_id_column")
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_latest_snapshot", return_value=None)
        self._patch("get_settings", return_value=[])
        return self._patch("create_trade_plan", return_value=create_return)

    def test_triggered_by_price_alert_id_passed_through_to_create_trade_plan(self):
        mock_create = self._install_common_mocks(
            {"id": "plan-1", "ticker": "TSLA", "market": "US", "triggered_by_price_alert_id": "pa-42"}
        )
        body = trade_plans_router.TradePlanCreate(
            ticker="TSLA", market="US", triggered_by_price_alert_id="pa-42"
        )
        trade_plans_router.create_plan(body)

        mock_create.assert_called_once()
        _, plan_data = mock_create.call_args.args
        assert plan_data["triggered_by_price_alert_id"] == "pa-42"

    def test_field_omitted_defaults_to_none(self):
        mock_create = self._install_common_mocks(
            {"id": "plan-2", "ticker": "AAPL", "market": "US", "triggered_by_price_alert_id": None}
        )
        body = trade_plans_router.TradePlanCreate(ticker="AAPL", market="US")
        trade_plans_router.create_plan(body)

        _, plan_data = mock_create.call_args.args
        assert plan_data["triggered_by_price_alert_id"] is None


def _make_conn_cur():
    cur = MagicMock()
    cur_ctx = MagicMock()
    cur_ctx.__enter__ = MagicMock(return_value=cur)
    cur_ctx.__exit__ = MagicMock(return_value=False)
    conn = MagicMock()
    conn.cursor.return_value = cur_ctx
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn, cur


class TestDatabaseCreateTradePlanIncludesColumn:
    """Exercises the real database.py INSERT shape (loaded independently of
    the process-global stub — see module docstring above)."""

    def test_insert_includes_triggered_by_price_alert_id_param(self):
        conn, cur = _make_conn_cur()
        cur.fetchone.return_value = {"id": "plan-1"}

        with patch.object(_real_database, "get_db", return_value=conn):
            _real_database.create_trade_plan(
                "portfolio-1",
                {"ticker": "TSLA", "market": "US", "triggered_by_price_alert_id": "pa-42"},
            )

        insert_call = [c for c in cur.execute.call_args_list if "INSERT INTO trade_plans" in c.args[0]]
        assert len(insert_call) == 1
        query, params = insert_call[0].args
        assert "triggered_by_price_alert_id" in query
        assert params[-1] == "pa-42"

    def test_insert_defaults_to_none_when_absent(self):
        conn, cur = _make_conn_cur()
        cur.fetchone.return_value = {"id": "plan-2"}

        with patch.object(_real_database, "get_db", return_value=conn):
            _real_database.create_trade_plan("portfolio-1", {"ticker": "AAPL", "market": "US"})

        insert_call = [c for c in cur.execute.call_args_list if "INSERT INTO trade_plans" in c.args[0]]
        _, params = insert_call[0].args
        assert params[-1] is None

    def test_ensure_triggered_by_price_alert_id_column_adds_nullable_uuid(self):
        conn, cur = _make_conn_cur()
        with patch.object(_real_database, "get_db", return_value=conn):
            _real_database.ensure_triggered_by_price_alert_id_column()

        (query,) = cur.execute.call_args.args
        assert "ADD COLUMN IF NOT EXISTS triggered_by_price_alert_id UUID" in query
