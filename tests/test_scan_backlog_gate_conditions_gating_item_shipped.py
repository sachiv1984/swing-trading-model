"""
ST-40 (BLG-GOV-386, EPIC-06, v9.12) — scripts/scan_backlog_gate_conditions.py
lists gated items whose gate names only BLG-* items that have shipped
(archived out of the active backlog, or bannered ✅ COMPLETE) under a
"gating item shipped — verify" heading, read by release_planning_prompt.md
§1.3a.
"""
import datetime
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "scan_backlog_gate_conditions.py"
_spec = importlib.util.spec_from_file_location("sbgc_shipped", SCRIPT)
sbgc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sbgc)

AS_OF = datetime.date(2026, 10, 13)


def _item(item_id, gate=None, extra=""):
    gate_line = f"**Gate criteria:** {gate}\n" if gate else ""
    return f"### {item_id} — Title {item_id}\n**Priority:** P3\n{gate_line}{extra}\n**Problem**\nx\n\n---\n\n"


FIXTURE = (
    _item("BLG-OPS-17")                                                 # active, open
    + _item("BLG-FE-56", extra="> ✅ COMPLETE — shipped v5.0\n")         # active but bannered complete
    + _item("BLG-OPS-18", gate="BLG-OPS-99 complete.")                  # BLG-OPS-99 archived → listed
    + _item("BLG-OPS-19", gate="BLG-OPS-17 complete.")                  # gating item still active → not listed
    + _item("BLG-OPS-21", gate="BLG-OPS-99 and BLG-OPS-17 complete.")  # one still active → not listed
    + _item("BLG-FE-62", gate="BLG-FE-56 shipped.")                     # ✅ COMPLETE counts as shipped → listed
    + _item("BLG-QA-1", gate="20+ closed trades confirmed.")           # no BLG reference → not listed
    + _item("BLG-GOV-5", gate="BLG-GOV-5 itself reviewed annually.")   # only its own ID → not listed
)


def _shipped(text):
    items = sbgc.parse_items(text)
    results = [sbgc.classify_item(i, t, b, AS_OF) for i, t, b in items]
    return {r["id"]: refs for r, refs in sbgc.gating_item_shipped(results, items)}


def test_gate_naming_only_an_archived_item_is_listed():
    assert _shipped(FIXTURE)["BLG-OPS-18"] == ["BLG-OPS-99"]


def test_complete_banner_counts_as_shipped():
    assert _shipped(FIXTURE)["BLG-FE-62"] == ["BLG-FE-56"]


def test_gate_naming_a_still_active_item_is_not_listed():
    shipped = _shipped(FIXTURE)
    assert "BLG-OPS-19" not in shipped
    assert "BLG-OPS-21" not in shipped


def test_gate_with_no_blg_reference_or_only_own_id_is_not_listed():
    shipped = _shipped(FIXTURE)
    assert "BLG-QA-1" not in shipped
    assert "BLG-GOV-5" not in shipped
    assert set(shipped) == {"BLG-OPS-18", "BLG-FE-62"}


def test_cli_prints_new_heading_and_json_key(tmp_path):
    backlog = tmp_path / "backlog.md"
    backlog.write_text(FIXTURE)
    text = subprocess.run([sys.executable, str(SCRIPT), "--backlog", str(backlog), "--as-of", "2026-10-13"],
                          capture_output=True, text=True, check=True).stdout
    assert "gating item shipped — verify" in text
    section = text.split("gating item shipped — verify", 1)[1]
    assert "BLG-OPS-18" in section and "BLG-OPS-19" not in section
    data = json.loads(subprocess.run([sys.executable, str(SCRIPT), "--backlog", str(backlog), "--json"],
                                     capture_output=True, text=True, check=True).stdout)
    assert [r["id"] for r in data["gating_item_shipped"]] == ["BLG-OPS-18", "BLG-FE-62"]
    assert data["gating_item_shipped"][0]["shipped_gating_items"] == ["BLG-OPS-99"]
    assert all(r["gated"] for r in data["gating_item_shipped"])  # still gated: never auto-cleared
