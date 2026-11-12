"""
One test per transition in data_model.md §Position & Trade Plan Lifecycle
State Diagram.

Why this file exists (2026-11-12, quality review after v9.16): BLG-BE-211
shipped because every story's own acceptance criteria passed while the spec's
`active --> closed` transition had no code path at all. Story ACs are not the
spec. This file reads the two mermaid diagrams from data_model.md and fails if
any transition in them has no test here (or a test here names a transition
the spec no longer has). Change the diagram and this file in the same commit.

Each test is tagged with @covers(<diagram>, <from>, <to>). A transition the
code does not yet honour is xfail(strict=True) with the backlog item that
fixes it; when the fix lands the XPASS failure says to remove the marker.

No database or network: every collaborator is patched.
"""
import re
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

import services.position_service as position_service
from services.position_lifecycle_service import compute_position_state

DATA_MODEL = Path(__file__).resolve().parent.parent / "docs" / "specs" / "data_model.md"
PLAN = "trade_plan"
POSITION = "position"
PRE_ACTIVE = ["draft", "research_pending", "research_complete", "entry_conditions_set"]

_COVERED = set()


def covers(diagram, *edges):
    """Register the diagram transitions a test checks. edges: (from, to) pairs."""
    for edge in edges:
        _COVERED.add((diagram, edge[0], edge[1]))

    def decorator(fn):
        return fn
    return decorator


# ---------------------------------------------------------------------------
# Spec <-> test coverage
# ---------------------------------------------------------------------------

def _diagram_edges(heading):
    text = DATA_MODEL.read_text(encoding="utf-8")
    start = text.index(heading)
    block = re.search(r"```mermaid\n(.*?)```", text[start:], re.S).group(1)
    edges = set()
    for line in block.splitlines():
        m = re.match(r"\s*(\S+)\s*-->\s*([^:\s]+)", line)
        if m:
            edges.add(tuple(s.replace("EXIT_ZONE", "EXIT ZONE") for s in m.groups()))
    return edges


def test_every_spec_transition_has_a_test_and_no_test_covers_a_removed_one():
    spec = {(PLAN, a, b) for a, b in _diagram_edges("### Trade Plan Lifecycle")}
    spec |= {(POSITION, a, b) for a, b in _diagram_edges("### Position Lifecycle")}
    assert spec, "no transitions parsed from data_model.md; did the diagram heading change?"
    missing = sorted(spec - _COVERED)
    stale = sorted(_COVERED - spec)
    assert not missing, f"data_model.md transitions with no test in this file: {missing}"
    assert not stale, f"tests here cover transitions data_model.md no longer has: {stale}"


# ---------------------------------------------------------------------------
# Trade plan lifecycle (trade_plans.status)
# ---------------------------------------------------------------------------

class _RouterTest:
    def setup_method(self):
        from fastapi.testclient import TestClient
        import main as _main
        self.client = TestClient(_main.app, raise_server_exceptions=False)
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, target, **kwargs):
        p = patch(target, **kwargs)
        self._patches.append(p)
        return p.start()

    def _common(self, existing=None):
        for name in ("ensure_trade_plans_table", "ensure_si02_trade_plans_columns",
                     "ensure_strategy_version_at_entry_columns",
                     "ensure_triggered_by_price_alert_id_column"):
            self._patch(f"routers.trade_plans.{name}", return_value=None)
        self._patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("routers.trade_plans.get_trade_plan_by_id", return_value=existing)
        self._patch("database.get_positions", return_value=[])

    def _put(self, existing, body):
        self._common(existing)
        update = self._patch(
            "routers.trade_plans.update_trade_plan",
            side_effect=lambda pid, pf, data: {**existing, **data},
        )
        return self.client.put("/trade-plans/plan-1", json=body), update


class TestTradePlanTransitions(_RouterTest):

    @covers(PLAN, ("[*]", "draft"))
    def test_post_creates_a_draft(self):
        self._common()
        create = self._patch(
            "routers.trade_plans.create_trade_plan",
            side_effect=lambda pf, data: {"id": "plan-new", **data},
        )
        resp = self.client.post("/trade-plans", json={"ticker": "AAPL", "market": "US"})
        assert resp.status_code == 201
        assert create.call_args[0][1]["status"] == "draft"

    @covers(PLAN, ("draft", "research_pending"), ("research_pending", "research_complete"),
            ("research_complete", "entry_conditions_set"))
    @pytest.mark.parametrize("before,after", [
        ("draft", "research_pending"),
        ("research_pending", "research_complete"),
        ("research_complete", "entry_conditions_set"),
    ])
    def test_research_workflow_steps(self, before, after):
        resp, update = self._put({"id": "plan-1", "status": before, "position_id": None},
                                 {"status": after})
        assert resp.status_code == 200, resp.text
        assert update.call_args[0][2]["status"] == after

    @covers(PLAN, *[(s, "abandoned") for s in PRE_ACTIVE])
    @pytest.mark.parametrize("before", PRE_ACTIVE)
    def test_pre_active_plan_can_be_abandoned_with_a_reason(self, before):
        resp, update = self._put({"id": "plan-1", "status": before, "position_id": None},
                                 {"status": "abandoned", "abandonment_reason": "setup failed"})
        assert resp.status_code == 200, resp.text
        assert update.call_args[0][2]["status"] == "abandoned"

    @pytest.mark.parametrize("before", PRE_ACTIVE)
    def test_abandoning_without_a_reason_is_rejected(self, before):
        resp, update = self._put({"id": "plan-1", "status": before, "position_id": None},
                                 {"status": "abandoned"})
        assert resp.status_code == 400
        update.assert_not_called()

    @covers(PLAN, ("abandoned", "[*]"), ("closed", "[*]"))
    @pytest.mark.xfail(strict=True, reason="BLG-BE-214: PUT /trade-plans/{id} lets a closed or abandoned plan change status")
    @pytest.mark.parametrize("terminal", ["abandoned", "closed"])
    @pytest.mark.parametrize("target", ["draft", "entry_conditions_set"])
    def test_terminal_plan_status_cannot_change(self, terminal, target):
        existing = {"id": "plan-1", "status": terminal, "position_id": "pos-1",
                    "abandonment_reason": "x" if terminal == "abandoned" else None}
        resp, update = self._put(existing, {"status": target})
        assert resp.status_code == 400
        update.assert_not_called()


# add_position() auto-link: the only code path that sets 'active'.

def _add_position(plan_lookup_name, plan, trade_plan_id=None):
    with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 100000.0}), \
         patch.object(position_service, "get_settings", return_value=[{
             "uk_commission": 9.95, "us_commission": 0, "stamp_duty_rate": 0.005, "fx_fee_rate": 0.0015}]), \
         patch.object(position_service, "create_position", return_value={"id": "new-position-id"}) as create, \
         patch.object(position_service, "update_portfolio_cash"), \
         patch.object(position_service, "calculate_atr", return_value=1.0), \
         patch.object(position_service, "get_live_fx_rate", return_value=1.27), \
         patch.object(position_service, plan_lookup_name, return_value=plan), \
         patch.object(position_service, "update_trade_plan", return_value=None) as update:
        position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-09",
            shares=10, entry_price=100.0, fx_rate=1.27, trade_plan_id=trade_plan_id,
        )
    return create, update


class TestTradePlanActivation:

    @covers(PLAN, *[(s, "active") for s in PRE_ACTIVE])
    @pytest.mark.parametrize("before", PRE_ACTIVE)
    def test_entering_a_position_activates_the_pre_active_plan(self, before):
        plan = {"id": "plan-1", "ticker": "AAPL", "market": "US", "status": before, "position_id": None}
        _, update = _add_position("get_unlinked_trade_plan_for_entry", plan)
        update.assert_called_once_with(
            "plan-1", "portfolio-1", {"position_id": "new-position-id", "status": "active"})

    @pytest.mark.xfail(strict=True, reason="BLG-BE-214: add_position links an explicit trade_plan_id without checking it is not abandoned")
    def test_an_abandoned_plan_is_not_activated_by_an_explicit_trade_plan_id(self):
        plan = {"id": "plan-1", "ticker": "AAPL", "market": "US", "status": "abandoned", "position_id": None}
        _, update = _add_position("get_trade_plan_by_id", plan, trade_plan_id="plan-1")
        update.assert_not_called()


# ---------------------------------------------------------------------------
# Position lifecycle (positions.status + positions.position_state)
# ---------------------------------------------------------------------------

def _exit_open_position(linked_plans):
    position = {
        "id": "pos-1", "ticker": "VOD.L", "market": "UK", "status": "open", "shares": 10,
        "total_cost": 1000.0, "fees_paid": 0.0, "entry_price": 100.0, "fx_rate": 1.0,
        "fill_price": None, "entry_date": "2026-10-01", "atr": None, "active_atr_multiplier": None,
    }
    trade_rows = []
    with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 0.0}), \
         patch.object(position_service, "get_positions", return_value=[position]), \
         patch.object(position_service, "get_settings", return_value=[{"fx_fee_rate": 0}]), \
         patch.object(position_service, "update_portfolio_cash"), \
         patch.object(position_service, "create_trade_history",
                      side_effect=lambda pid, td: trade_rows.append(td)), \
         patch.object(position_service, "update_position") as update_position, \
         patch.object(position_service, "get_trade_plans_by_position", return_value=linked_plans), \
         patch.object(position_service, "get_signals", return_value=[]), \
         patch.object(position_service, "ensure_planned_entry_price_column", return_value=None), \
         patch.object(position_service, "update_trade_plan", return_value=None) as update_plan:
        position_service.exit_position(position_id="pos-1", exit_price=110.0,
                                       exit_date="2026-11-10", exit_fx_rate=1.0)
    return trade_rows, update_position, update_plan


class TestPositionOpenAndClose:

    @covers(POSITION, ("[*]", "open"))
    def test_add_position_creates_an_open_position(self):
        create, _ = _add_position("get_unlinked_trade_plan_for_entry", None)
        position_data = create.call_args[0][1]
        assert position_data["status"] == "open"

    @covers(POSITION, ("open", "closed"), ("closed", "[*]"))
    def test_full_exit_closes_the_position_and_writes_trade_history(self):
        trade_rows, update_position, _ = _exit_open_position([])
        assert len(trade_rows) == 1
        assert update_position.call_args[0][1]["status"] == "closed"

    @covers(PLAN, ("active", "closed"))
    @pytest.mark.xfail(strict=True, reason="BLG-BE-211 (v9.17 ST-11): no code path moves a linked plan to closed")
    def test_full_exit_closes_the_linked_active_plan(self):
        plan = {"id": "plan-1", "status": "active", "position_id": "pos-1"}
        _, _, update_plan = _exit_open_position([plan])
        statuses = [c[0][2].get("status") for c in update_plan.call_args_list]
        assert "closed" in statuses


# position_state is recomputed from scratch on every GET /positions, so each
# transition A --> B holds when the conditions for A give A and the conditions
# for B give B. Entry 100, initial stop 90: R = 10, so EXIT ZONE is >= 120.

def _state(days_held, price, entry=100.0, initial_stop=90.0):
    return compute_position_state({
        "market": "UK", "entry_price": entry, "initial_stop": initial_stop,
        "current_price": price, "entry_date": str(date.today() - timedelta(days=days_held)),
    })


_CONDITIONS = {
    "GRACE": dict(days_held=3, price=80.0),
    "PROFITABLE": dict(days_held=20, price=110.0),
    "LOSING": dict(days_held=20, price=95.0),
    "EXIT ZONE": dict(days_held=20, price=125.0),
    "UNKNOWN": dict(days_held=20, price=None),
}

_STATE_EDGES = [
    ("GRACE", "PROFITABLE"), ("GRACE", "LOSING"), ("GRACE", "EXIT ZONE"),
    ("PROFITABLE", "EXIT ZONE"), ("EXIT ZONE", "PROFITABLE"),
    ("PROFITABLE", "LOSING"), ("LOSING", "PROFITABLE"), ("LOSING", "EXIT ZONE"),
    ("UNKNOWN", "GRACE"), ("UNKNOWN", "PROFITABLE"), ("UNKNOWN", "LOSING"),
]


class TestPositionStateTransitions:

    @covers(POSITION, ("[*]", "GRACE"))
    @pytest.mark.parametrize("price", [50.0, 100.0, 150.0])
    def test_new_position_is_grace_at_any_price(self, price):
        assert _state(0, price) == "GRACE"

    @covers(POSITION, *_STATE_EDGES)
    @pytest.mark.parametrize("before,after", _STATE_EDGES)
    def test_transition(self, before, after):
        assert _state(**_CONDITIONS[before]) == before
        assert _state(**_CONDITIONS[after]) == after

    @pytest.mark.parametrize("days_held,price,expected", [
        (9, 125.0, "GRACE"),          # day 9 is still grace (10 calendar days, 0-9)
        (10, 125.0, "EXIT ZONE"),     # grace elapsed
        (20, 100.0, "LOSING"),        # price == entry is LOSING, not PROFITABLE
        (20, 100.01, "PROFITABLE"),
        (20, 120.0, "EXIT ZONE"),     # exactly entry + 2R
        (20, 119.99, "PROFITABLE"),
    ])
    def test_boundaries(self, days_held, price, expected):
        assert _state(days_held, price) == expected
