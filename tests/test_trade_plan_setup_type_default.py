"""
setup_type server-side default regression test (ST-13, BLG-QA-150, EPIC-04,
v8.9).

`POST /trade-plans` previously accepted `setup_type` as an optional,
client-supplied field with no server-side default. Only the linked-
watchlisted-signal creation path in `TradePlan.js` pre-populated it
("Momentum Continuation") -- every other creation path (manual entry,
Ticker Universe, Research CTA with no matching signal, direct API use)
saved `setup_type: null`, undercounting Arc 6/SI-02's future
`win_rate_by_setup_type` analysis (a null value doesn't group into any of
the 6 canonical `setup_type` enum values).

Product Owner decision (agent-mediated, §5.3): normalize null/absent
`setup_type` to the existing canonical value "Other" server-side, in
`create_plan()`'s `_create()` closure -- covers every creation path
(frontend and direct API) at the single choke point through which all
writes flow, with no new UI or enum value (`Other` already exists in both
`SETUP_TYPE_OPTIONS` and the frontend `SETUP_TYPES` dropdown).

No live database calls -- TestClient(app) with database.create_trade_plan
and the other _create() dependencies (get_latest_snapshot, get_settings,
get_portfolio) mocked directly, following the same TestClient(app) pattern
as tests/test_st04_implicit_200_error_paths_fixed.py.
"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)

_MINIMAL_BODY = {"ticker": "AAPL", "market": "US"}


def _patched_create(**overrides):
    """Common patch set for POST /trade-plans's _create() closure dependencies."""
    patches = {
        "routers.trade_plans.ensure_trade_plans_table": patch("routers.trade_plans.ensure_trade_plans_table"),
        "routers.trade_plans.ensure_si02_trade_plans_columns": patch("routers.trade_plans.ensure_si02_trade_plans_columns"),
        "routers.trade_plans.ensure_strategy_version_at_entry_columns": patch("routers.trade_plans.ensure_strategy_version_at_entry_columns"),
        "routers.trade_plans.ensure_triggered_by_price_alert_id_column": patch("routers.trade_plans.ensure_triggered_by_price_alert_id_column"),
        "routers.trade_plans.get_portfolio": patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"}),
        "routers.trade_plans.get_current_strategy_version": patch("routers.trade_plans.get_current_strategy_version", return_value="v1"),
        "routers.trade_plans.get_latest_snapshot": patch("routers.trade_plans.get_latest_snapshot", return_value=None),
        "routers.trade_plans.get_settings": patch("routers.trade_plans.get_settings", return_value=[]),
    }
    started = {name: p.start() for name, p in patches.items()}
    return started, patches


class TestSetupTypeServerSideDefault:
    def test_omitted_setup_type_defaults_to_other(self):
        started, patches = _patched_create()
        try:
            with patch("routers.trade_plans.create_trade_plan", return_value={"id": "plan-1", **_MINIMAL_BODY, "setup_type": "Other"}) as mock_create:
                resp = CLIENT.post("/trade-plans", json=_MINIMAL_BODY)
            assert resp.status_code == 201
            mock_create.assert_called_once()
            _, plan_data = mock_create.call_args.args
            assert plan_data["setup_type"] == "Other"
        finally:
            for p in patches.values():
                p.stop()

    def test_explicit_null_setup_type_defaults_to_other(self):
        started, patches = _patched_create()
        try:
            body = {**_MINIMAL_BODY, "setup_type": None}
            with patch("routers.trade_plans.create_trade_plan", return_value={"id": "plan-1", **body, "setup_type": "Other"}) as mock_create:
                resp = CLIENT.post("/trade-plans", json=body)
            assert resp.status_code == 201
            _, plan_data = mock_create.call_args.args
            assert plan_data["setup_type"] == "Other"
        finally:
            for p in patches.values():
                p.stop()

    def test_explicit_value_is_preserved_not_overridden(self):
        started, patches = _patched_create()
        try:
            body = {**_MINIMAL_BODY, "setup_type": "Breakout"}
            with patch("routers.trade_plans.create_trade_plan", return_value={"id": "plan-1", **body}) as mock_create:
                resp = CLIENT.post("/trade-plans", json=body)
            assert resp.status_code == 201
            _, plan_data = mock_create.call_args.args
            assert plan_data["setup_type"] == "Breakout"
        finally:
            for p in patches.values():
                p.stop()

    def test_empty_string_setup_type_defaults_to_other(self):
        """Guards against a client sending "" (e.g. an unselected <select> that
        posts an empty string rather than omitting the key) -- `or` treats ""
        as falsy the same as None, so this also normalizes to "Other"."""
        started, patches = _patched_create()
        try:
            body = {**_MINIMAL_BODY, "setup_type": ""}
            with patch("routers.trade_plans.create_trade_plan", return_value={"id": "plan-1", **body, "setup_type": "Other"}) as mock_create:
                resp = CLIENT.post("/trade-plans", json=body)
            assert resp.status_code == 201
            _, plan_data = mock_create.call_args.args
            assert plan_data["setup_type"] == "Other"
        finally:
            for p in patches.values():
                p.stop()
