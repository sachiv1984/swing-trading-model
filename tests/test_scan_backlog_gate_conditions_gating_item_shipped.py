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


# ST-37 (BLG-GOV-404, EPIC-07, v9.15): a gate naming a roadmap feature ID
# (PT-xx, SI-xx, PO-xx) is listed once the roadmap marks that feature shipped.

ROADMAP = (
    "|ID   |Feature            |Effort|Status|\n"
    "|PT-04|Setup Quality Score|M     |Deterministic score. Gate: 20+ closed trades|\n"   # older table, no marker
    "|Setup Quality Score|PT-04|M|✅ Shipped v6.1 (2026-06-23)|\n"                      # shipped row
    "|PO-01|Plan vs Reality|H|✅ Shipped v3.5–v3.6 — **Arc 4 PO-01 fully complete**|\n"
    "|SI-02|Behavioural Drift Detection|H|Rolling analysis of entries|\n"                 # unshipped
    "> **Arc 2 ✅ Fully Complete:** SI-05 and PO-02 mentioned in prose only.\n"          # prose ignored
)

FEATURE_FIXTURE = (
    _item("BLG-OPS-17")
    + _item("BLG-FE-39", gate="PT-04 (Setup Quality Score) shipped.")
    + _item("BLG-FEAT-70", gate="SI-02 (Behavioural Drift Detection) shipped.")
    + _item("BLG-FEAT-71", gate="PO-02 shipped.")                                 # prose mention only → unshipped
    + _item("BLG-QA-9", gate="PT-04 shipped and BLG-OPS-17 complete.")            # BLG still active → not listed
    + _item("BLG-QA-10", gate="PO-01 shipped and BLG-OPS-99 complete.")           # both shipped → listed
)


def _shipped_with_roadmap(text, roadmap=ROADMAP):
    items = sbgc.parse_items(text)
    results = [sbgc.classify_item(i, t, b, AS_OF) for i, t, b in items]
    features = sbgc.shipped_feature_ids([roadmap])
    return {r["id"]: refs for r, refs in sbgc.gating_item_shipped(results, items, features)}


def test_shipped_feature_ids_reads_table_rows_only():
    assert sbgc.shipped_feature_ids([ROADMAP]) == {"PT-04", "PO-01"}


def test_gate_on_shipped_feature_id_is_listed():
    assert _shipped_with_roadmap(FEATURE_FIXTURE)["BLG-FE-39"] == ["PT-04"]


def test_gate_on_unshipped_feature_id_is_not_listed():
    shipped = _shipped_with_roadmap(FEATURE_FIXTURE)
    assert "BLG-FEAT-70" not in shipped
    assert "BLG-FEAT-71" not in shipped


def test_mixed_feature_and_blg_gate_needs_both_shipped():
    shipped = _shipped_with_roadmap(FEATURE_FIXTURE)
    assert "BLG-QA-9" not in shipped
    assert shipped["BLG-QA-10"] == ["BLG-OPS-99", "PO-01"]
    assert set(shipped) == {"BLG-FE-39", "BLG-QA-10"}


def test_feature_gate_not_listed_without_roadmap_input():
    items = sbgc.parse_items(FEATURE_FIXTURE)
    results = [sbgc.classify_item(i, t, b, AS_OF) for i, t, b in items]
    assert "BLG-FE-39" not in {r["id"] for r, _ in sbgc.gating_item_shipped(results, items)}


def test_cli_reads_roadmap_argument(tmp_path):
    backlog = tmp_path / "backlog.md"
    backlog.write_text(FEATURE_FIXTURE)
    roadmap = tmp_path / "current_roadmap.md"
    roadmap.write_text(ROADMAP)
    data = json.loads(subprocess.run(
        [sys.executable, str(SCRIPT), "--backlog", str(backlog), "--roadmap", str(roadmap), "--json"],
        capture_output=True, text=True, check=True).stdout)
    assert [r["id"] for r in data["gating_item_shipped"]] == ["BLG-FE-39", "BLG-QA-10"]


def test_live_backlog_lists_the_six_pt04_gated_items():
    """AC 3: the six items named in BLG-GOV-404's Problem appear on the live
    backlog while their gate still names PT-04.

    release_planning_prompt.md §1.3a clears such a gate in place (the Gate
    field goes, the item stays), and an item may later be archived. Either
    way it drops out of this check, rather than failing CI on the very edit
    ST-37 enables (BLG-QA-251). The fixture tests above stay as the permanent
    AC 1 / AC 2 coverage."""
    import pytest
    six = {"BLG-FE-39", "BLG-QA-21", "BLG-QA-22", "BLG-QA-23", "BLG-GOV-26", "BLG-FEAT-26"}
    backlog = (ROOT / "claude" / "backlog" / "backlog.md").read_text()
    items = sbgc.parse_items(backlog)
    results = [sbgc.classify_item(i, t, b, AS_OF) for i, t, b in items]
    still_gated = {r["id"] for r in results
                   if r["id"] in six and r["gated"] and "PT-04" in r["gate_condition"]}
    if not still_gated:
        pytest.skip("none of the six items is still gated on PT-04 (cleared in place or archived)")
    features = sbgc.shipped_feature_ids((ROOT / p).read_text() for p in sbgc.ROADMAP_PATHS)
    listed = {r["id"] for r, _ in sbgc.gating_item_shipped(results, items, features)}
    assert still_gated <= listed, sorted(still_gated - listed)
