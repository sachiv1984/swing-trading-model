"""ST-13 (BLG-FE-320, EPIC-02, v9.18): rules followed / broken per closed trade.

metrics_definitions.md §Rules Followed (per closed trade). Expected values are
written from the definition's worked examples A–H, not from the code.
Revised by ESC-EXEC-20261126-02: the evidence date is the position row's
created_at (position_created_at), not the user-entered entry_date.
"""
from datetime import date, datetime
from unittest.mock import patch

import pytest

from services.rules_followed import CHECKS_ON_EVERY_ROUTE_FROM, classify_rules
import services.trade_service as trade_service

EV = {
    "pos-a": {"events": set(), "override_acknowledged": False, "has_snapshot": True},
    "pos-b": {"events": {"pre_entry_override"}, "override_acknowledged": False, "has_snapshot": False},
    "pos-c": {"events": set(), "override_acknowledged": True, "has_snapshot": True},
    # G: checklist_skipped comes from the plan's saved checklist (checklist_incomplete), not events.
    "pos-g": {"events": {"stop_prompt_dismissed"}, "override_acknowledged": False, "has_snapshot": True, "checklist_incomplete": True},
}


@pytest.mark.parametrize("label, trade, expected", [
    ("A plan snapshot, nothing broken", {"position_id": "pos-a", "position_created_at": "2026-09-01", "exit_reason": "Stop Loss Hit"}, (True, [])),
    ("B override event on the position", {"position_id": "pos-b", "position_created_at": "2026-11-20"}, (False, ["pre_entry_override"])),
    ("C plan-time override acknowledged", {"position_id": "pos-c", "position_created_at": "2026-09-01"}, (False, ["pre_entry_override"])),
    ("D no position link", {"position_id": None, "position_created_at": "2026-11-20"}, (None, [])),
    ("E unlinked, before checks ran", {"position_id": "pos-e", "position_created_at": "2026-10-01"}, (None, [])),
    ("F no evidence, after 2026-11-04", {"position_id": "pos-f", "position_created_at": "2026-11-10"}, (True, [])),
    ("G two event types, sorted", {"position_id": "pos-g", "position_created_at": "2026-09-01"}, (False, ["checklist_skipped", "stop_prompt_dismissed"])),
    ("H manual exit is not broken", {"position_id": "pos-h", "position_created_at": "2026-11-05", "exit_reason": "Manual Exit"}, (True, [])),
])
def test_worked_examples(label, trade, expected):
    assert classify_rules(trade, EV) == expected


@pytest.mark.parametrize("entry, expected", [
    ("2026-11-03", None),          # the day before: no evidence the checks ran
    ("2026-11-04", True),          # on the date: on or after
    (date(2026, 11, 4), True),
    (datetime(2026, 11, 4, 23, 59), True),
    ("2026-11-04T00:00:00", True),
    (None, None),
    ("not a date", None),
])
def test_evidence_date_boundary(entry, expected):
    assert CHECKS_ON_EVERY_ROUTE_FROM == date(2026, 11, 4)
    assert classify_rules({"position_id": "pos-x", "position_created_at": entry}, {})[0] is expected


def test_the_user_entered_entry_date_is_not_the_evidence_date():
    # Back-dated entry made in the app after 2026-11-04: created_at decides.
    t = {"position_id": "pos-x", "entry_date": "2026-10-01", "position_created_at": "2026-11-10T08:00:00"}
    assert classify_rules(t, {}) == (True, [])
    # Forward-dated entry, but the position row predates the checks.
    t = {"position_id": "pos-x", "entry_date": "2026-11-20", "position_created_at": "2026-10-15T08:00:00"}
    assert classify_rules(t, {}) == (None, [])


def test_broken_wins_over_the_date():
    assert classify_rules({"position_id": "pos-b", "position_created_at": "2026-11-25"}, EV) == (False, ["pre_entry_override"])


def test_override_from_both_sources_is_listed_once():
    ev = {"p": {"events": {"pre_entry_override"}, "override_acknowledged": True, "has_snapshot": False}}
    assert classify_rules({"position_id": "p", "position_created_at": "2026-09-01"}, ev) == (False, ["pre_entry_override"])


def test_a_past_checklist_skipped_event_alone_does_not_break():
    # ESC-EXEC-20261126-03: a draft saved with an unticked item and completed
    # later, or a pre-v9.18 event that counted the old system ticks.
    ev = {"p": {"events": {"checklist_skipped"}, "override_acknowledged": False, "has_snapshot": True, "checklist_incomplete": False}}
    assert classify_rules({"position_id": "p", "position_created_at": "2026-09-01"}, ev) == (True, [])


def test_a_plan_still_incomplete_is_broken():
    ev = {"p": {"events": set(), "override_acknowledged": False, "has_snapshot": True, "checklist_incomplete": True}}
    assert classify_rules({"position_id": "p", "position_created_at": "2026-09-01"}, ev) == (False, ["checklist_skipped"])


def test_unknown_event_types_are_ignored():
    ev = {"p": {"events": {"compliance_recheck"}, "override_acknowledged": False, "has_snapshot": True}}
    assert classify_rules({"position_id": "p", "position_created_at": "2026-09-01"}, ev) == (True, [])


def test_uuid_position_ids_match_string_keys():
    import uuid
    pid = uuid.UUID("00000000-0000-0000-0000-0000000000b0")
    ev = {str(pid): {"events": {"pre_entry_override"}, "override_acknowledged": False, "has_snapshot": False}}
    assert classify_rules({"position_id": pid, "position_created_at": "2026-09-01"}, ev) == (False, ["pre_entry_override"])


def test_empty_string_position_id_is_not_known():
    assert classify_rules({"position_id": "", "position_created_at": "2026-11-20"}, {}) == (None, [])


# ---------------------------------------------------------------------------
# GET /trades service: fields on every trade; a failed evidence query → null
# ---------------------------------------------------------------------------

PORTFOLIO = {"id": "port-1"}


def _row(**kw):
    base = {
        "id": "t1", "ticker": "AAPL", "market": "US", "entry_date": "2026-11-10", "exit_date": "2026-11-20",
        "shares": 10, "entry_price": 100, "exit_price": 110, "pnl": 100, "pnl_pct": 10, "holding_days": 10,
        "exit_reason": "Manual Exit", "tags": [], "position_id": "pos-f",
        "position_created_at": "2026-11-10T09:00:00",
    }
    base.update(kw)
    return base


def test_service_adds_the_fields_to_every_trade():
    rows = [_row(id="t1", position_id="pos-b"), _row(id="t2", position_id=None), _row(id="t3", position_id="pos-f")]
    with patch.object(trade_service, "get_portfolio", return_value=PORTFOLIO), \
         patch.object(trade_service, "get_trade_history_with_stops", return_value=rows), \
         patch.object(trade_service, "get_rules_followed_evidence", return_value=EV) as ev:
        out = trade_service.get_trade_history_with_stats()
    # Only the trades' own positions are asked for (none for t2, no position).
    ev.assert_called_once_with("port-1", ["pos-b", "pos-f"])
    got = [(t["id"], t["rules_followed"], t["rules_broken"]) for t in out["trades"]]
    assert got == [("t1", False, ["pre_entry_override"]), ("t2", None, []), ("t3", True, [])]


def test_no_trades_makes_no_evidence_query():
    with patch.object(trade_service, "get_portfolio", return_value=PORTFOLIO), \
         patch.object(trade_service, "get_trade_history_with_stops", return_value=[]), \
         patch.object(trade_service, "get_rules_followed_evidence") as ev:
        out = trade_service.get_trade_history_with_stats()
    ev.assert_not_called()
    assert out["trades"] == []


@pytest.mark.parametrize("failure", [RuntimeError("db down"), None])
def test_failed_or_missing_evidence_marks_every_trade_not_known(failure):
    kwargs = {"side_effect": failure} if isinstance(failure, Exception) else {"return_value": failure}
    with patch.object(trade_service, "get_portfolio", return_value=PORTFOLIO), \
         patch.object(trade_service, "get_trade_history_with_stops", return_value=[_row(position_id="pos-b")]), \
         patch.object(trade_service, "get_rules_followed_evidence", **kwargs):
        out = trade_service.get_trade_history_with_stats()
    assert out["trades"][0]["rules_followed"] is None
    assert out["trades"][0]["rules_broken"] == []
    assert out["total_trades"] == 1


# ---------------------------------------------------------------------------
# The plan's saved checklist (database._checklist_has_unticked_judgement_item)
# ---------------------------------------------------------------------------

def _real_database_module():
    import importlib.util
    from pathlib import Path
    path = Path(__file__).parent.parent / "backend" / "database.py"
    spec = importlib.util.spec_from_file_location("database_real_st13_unit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


J = [{"id": "signal_confirmed", "checked": True}, {"id": "research_reviewed", "checked": True}]


@pytest.mark.parametrize("label, items, expected", [
    ("both judgement items ticked", J, False),
    ("one judgement item unticked", [J[0], {"id": "research_reviewed", "checked": False}], True),
    ("legacy: only the old heat tick unticked (no auto key)", J + [{"id": "heat_limit_checked", "checked": False}], False),
    ("legacy: stop tick unticked", J + [{"id": "stop_defined", "checked": False}], False),
    ("v9.18 system items saved auto and unticked", J + [{"id": "heat_limit_checked", "checked": False, "auto": True}], False),
    ("an unknown item without auto counts as judgement", J + [{"id": "custom", "checked": False}], True),
    ("checked must be a real true", [{"id": "signal_confirmed", "checked": "true"}], True),
    ("empty checklist", [], False),
    ("missing checklist", None, False),
    ("JSON string", '[{"id": "signal_confirmed", "checked": false}]', True),
    ("bad JSON string", "not json", False),
    ("non-dict entries count as unticked, as the event writer counts them", ["x", 3], True),
])
def test_plan_checklist_judgement(label, items, expected):
    assert _real_database_module()._checklist_has_unticked_judgement_item(items) is expected


def test_the_writer_and_the_evidence_use_one_rule():
    # routers/trade_plans._unchecked_count and the evidence helper agree.
    from utils.checklist import count_unchecked_judgement_items
    legacy = J + [{"id": "heat_limit_checked", "checked": False}, {"id": "stop_defined", "checked": False}]
    assert count_unchecked_judgement_items(legacy) == (0, 2)
    assert count_unchecked_judgement_items([J[0], {"id": "research_reviewed", "checked": False}, "x"]) == (2, 3)
    assert count_unchecked_judgement_items("not json") == (0, 0)
    assert count_unchecked_judgement_items({"id": "a"}) == (0, 0)
