"""
ST-04 (BLG-BE-182, EPIC-01, v9.13): checklist_skipped events and Red Flag
Journal writer coverage.

- Saving a trade plan (create or update) with a non-empty, incomplete checklist
  writes exactly one non-blocking checklist_skipped event: ticker, plan id,
  unchecked item count and total (red_flag_journal.md v1.1.0).
- A complete or empty checklist, or an update that does not save the
  checklist, writes nothing. A failing write never blocks the save.
- Writer coverage: every event type declared in database._VALID_EVENT_TYPES
  has a create_red_flag_event writer in backend/, or a dated allow-list entry
  below, never both. The frontend's RECORDED_EVENT_TYPES
  (src/pages/RedFlagJournal.js) must equal the set of written types, so that
  adding a writer means editing one list on each side.
"""
import re
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

ROOT = Path(__file__).parent.parent
BACKEND = ROOT / "backend"

# Declared types that have no writer yet. Each entry is dated; remove it in
# the same change that adds the writer (the test fails while both exist).
UNWRITTEN_ALLOW_LIST = {
    "stop_prompt_dismissed": "2026-10-16 — no stop-prompt dismissal UI records it yet (BLG-BE-182, v9.13 ST-04)",
    "drawdown_prompt_dismissed": "2026-10-16 — the drawdown prompt's session dismissal is not recorded yet (BLG-BE-182, v9.13 ST-04)",
}

WRITER_RE = re.compile(r'create_red_flag_event\(\s*event_type\s*=\s*"(\w+)"')


def declared_event_types() -> set:
    source = (BACKEND / "database.py").read_text(encoding="utf-8")
    block = re.search(r"_VALID_EVENT_TYPES\s*=\s*frozenset\(\{(.*?)\}\)", source, re.S).group(1)
    return set(re.findall(r'"(\w+)"', block))


def written_event_types(sources) -> set:
    found = set()
    for text in sources:
        found.update(WRITER_RE.findall(text))
    return found


def backend_sources():
    for path in BACKEND.rglob("*.py"):
        if ".venv" in path.parts or "site-packages" in path.parts:
            continue
        yield path.read_text(encoding="utf-8")


def coverage_gaps(declared, written, allow_list) -> dict:
    return {
        "no_writer": sorted(t for t in declared if t not in written and t not in allow_list),
        "allow_listed_but_written": sorted(t for t in allow_list if t in written),
        "allow_list_not_declared": sorted(t for t in allow_list if t not in declared),
    }


def frontend_recorded_types() -> set:
    source = (ROOT / "src" / "pages" / "RedFlagJournal.js").read_text(encoding="utf-8")
    block = re.search(r"RECORDED_EVENT_TYPES\s*=\s*\[(.*?)\]", source, re.S).group(1)
    return set(re.findall(r'"(\w+)"', block))


class TestWriterCoverage:
    def test_every_declared_type_has_a_writer_or_a_dated_allow_list_entry(self):
        declared = declared_event_types()
        assert declared == {"pre_entry_override", "checklist_skipped", "stop_prompt_dismissed", "drawdown_prompt_dismissed"}
        written = written_event_types(backend_sources())
        assert coverage_gaps(declared, written, UNWRITTEN_ALLOW_LIST) == {
            "no_writer": [], "allow_listed_but_written": [], "allow_list_not_declared": [],
        }
        for reason in UNWRITTEN_ALLOW_LIST.values():
            assert re.match(r"\d{4}-\d{2}-\d{2} — ", reason)

    def test_check_fails_when_a_declared_type_loses_its_writer(self):
        declared = declared_event_types()
        sources = [s.replace('event_type="checklist_skipped"', 'event_type=EVENT') for s in backend_sources()]
        gaps = coverage_gaps(declared, written_event_types(sources), UNWRITTEN_ALLOW_LIST)
        assert gaps["no_writer"] == ["checklist_skipped"]

    def test_frontend_recorded_types_match_the_written_set(self):
        written = written_event_types(backend_sources())
        assert frontend_recorded_types() == written == {"pre_entry_override", "checklist_skipped"}


def _items(checked):
    return [{"id": f"item-{i}", "label": f"Item {i}", "checked": c} for i, c in enumerate(checked)]


PLAN = {
    "id": "plan-42", "ticker": "AAPL", "market": "US", "position_id": None,
    "checklist_items": "[]", "status": "draft", "created_at": None, "updated_at": None,
}


@pytest.fixture()
def tp():
    import routers.trade_plans as tp_mod
    app = FastAPI()
    app.include_router(tp_mod.router)
    patches = [
        patch.object(tp_mod, name)
        for name in (
            "ensure_trade_plans_table", "ensure_si02_trade_plans_columns",
            "ensure_strategy_version_at_entry_columns", "ensure_triggered_by_price_alert_id_column",
            "ensure_red_flag_events_table", "get_latest_snapshot", "get_settings",
        )
    ]
    patches += [
        patch.object(tp_mod, "get_portfolio", return_value={"id": "port-1"}),
        patch.object(tp_mod, "create_trade_plan", return_value=dict(PLAN)),
        patch.object(tp_mod, "update_trade_plan", return_value=dict(PLAN)),
    ]
    for p in patches:
        p.start()
    write = patch.object(tp_mod, "create_red_flag_event").start()
    yield TestClient(app), write
    patch.stopall()


def _checklist_calls(write):
    return [c for c in write.call_args_list if c.kwargs.get("event_type") == "checklist_skipped"]


class TestChecklistSkippedWriter:
    def test_create_with_incomplete_checklist_writes_one_event(self, tp):
        client, write = tp
        resp = client.post("/trade-plans", json={
            "ticker": "AAPL", "market": "US", "checklist_items": _items([True, False, False, True, False]),
        })
        assert resp.status_code == 201
        calls = _checklist_calls(write)
        assert len(calls) == 1
        assert calls[0].kwargs == {
            "event_type": "checklist_skipped",
            "ticker": "AAPL",
            "position_id": None,
            "context": {"source": "trade_plan", "plan_id": "plan-42", "unchecked_items": 3, "total_items": 5},
        }

    @pytest.mark.parametrize("items", [_items([True, True, True]), []])
    def test_complete_or_empty_checklist_writes_nothing(self, tp, items):
        client, write = tp
        resp = client.post("/trade-plans", json={"ticker": "AAPL", "market": "US", "checklist_items": items})
        assert resp.status_code == 201
        assert _checklist_calls(write) == []

    def test_failed_write_does_not_block_the_save(self, tp):
        client, write = tp
        write.side_effect = RuntimeError("red_flag_events unavailable")
        resp = client.post("/trade-plans", json={"ticker": "AAPL", "market": "US", "checklist_items": _items([False])})
        assert resp.status_code == 201
        assert resp.json()["data"]["id"] == "plan-42"

    def test_update_saving_incomplete_checklist_writes_one_event(self, tp):
        client, write = tp
        resp = client.put("/trade-plans/plan-42", json={"checklist_items": _items([True, False])})
        assert resp.status_code == 200
        calls = _checklist_calls(write)
        assert len(calls) == 1
        assert calls[0].kwargs["context"] == {
            "source": "trade_plan", "plan_id": "plan-42", "unchecked_items": 1, "total_items": 2,
        }

    def test_update_without_checklist_writes_nothing(self, tp):
        client, write = tp
        resp = client.put("/trade-plans/plan-42", json={"setup_thesis": "Breakout above the 50-day high"})
        assert resp.status_code == 200
        assert _checklist_calls(write) == []
