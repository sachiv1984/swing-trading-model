"""
Endpoint-level regression test for GET /analytics/tag-performance's
ensure_trade_plans_table() call (ST-15, BLG-QA-136, EPIC-05, v8.6).

ST-01 (BLG-BE-86, v8.5) added an `ensure_trade_plans_table()` call to this
endpoint (`backend/routers/analytics.py::get_tag_performance_endpoint()`) so
a staging DB whose `trade_plans` table predates the `trade_tags` migration
doesn't 500 on "column trade_tags does not exist". That fix had no direct
regression test of its own — `tests/test_router_error_envelope_conformance.py`
covers this endpoint's 400 error path (which never reaches the
`ensure_trade_plans_table()` call), and `tests/test_trade_plan_tags.py`
covers `database.get_tag_performance()` in isolation, not the router's own
call sequence. This file closes that gap.

CI-safe: no live DB — TestClient(app) with `database.*` functions patched
(the router does a *local* import of `get_portfolio`/`get_tag_performance`/
`ensure_trade_plans_table` inside the function body, so patches must target
`database.<name>`, not `routers.analytics.<name>` -- same reasoning as
test_api_contracts.py's `routers.trade_plans.ensure_trade_plans_table`
patches use module-level-import targets for that router; analytics.py's
import is local, so the patch target differs accordingly).
"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)

_PORTFOLIO = {"id": "port-1"}


def test_tag_performance_calls_ensure_trade_plans_table_before_query():
    call_order = []

    with patch("database.get_portfolio", return_value=_PORTFOLIO), \
         patch("database.ensure_trade_plans_table", side_effect=lambda: call_order.append("ensure")), \
         patch("database.get_tag_performance", side_effect=lambda *a, **kw: call_order.append("query") or []):
        resp = CLIENT.get("/analytics/tag-performance", params={"tags": "breakout"})

    assert resp.status_code == 200
    assert call_order == ["ensure", "query"], (
        f"ensure_trade_plans_table() must be called before get_tag_performance() -- got order {call_order}"
    )


def test_tag_performance_does_not_query_if_ensure_table_fails():
    """If ensure_trade_plans_table() itself raises (e.g. a genuine DB error),
    the endpoint must not proceed to query trade_tags anyway -- confirms the
    call is not merely present but actually gates the query, not fired in
    parallel or ignored on failure."""
    call_order = []

    with patch("database.get_portfolio", return_value=_PORTFOLIO), \
         patch("database.ensure_trade_plans_table", side_effect=RuntimeError("DB unavailable")), \
         patch("database.get_tag_performance", side_effect=lambda *a, **kw: call_order.append("query") or []):
        resp = CLIENT.get("/analytics/tag-performance", params={"tags": "breakout"})

    assert resp.status_code == 500
    assert call_order == [], "get_tag_performance() must not run if ensure_trade_plans_table() failed"
