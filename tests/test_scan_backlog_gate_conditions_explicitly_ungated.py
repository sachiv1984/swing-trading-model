"""
ST-35 (BLG-GOV-390, EPIC-06, v9.13) — scripts/scan_backlog_gate_conditions.py
treats a gate field reading `None`, `N/A`, `-` or `—` (case-insensitive,
trimmed, optional trailing period) as ungated, and reports those items in a
separate informational "explicitly ungated" count.
"""
import datetime
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "scan_backlog_gate_conditions.py"
_spec = importlib.util.spec_from_file_location("sbgc_ungated", SCRIPT)
sbgc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sbgc)

AS_OF = datetime.date(2026, 10, 16)


def _classify(gate_line):
    body = f"### BLG-GOV-1 — Title\n**Priority:** P3\n{gate_line}\n**Problem**\nx\n"
    return sbgc.classify_item("BLG-GOV-1", "Title", body, AS_OF)


@pytest.mark.parametrize("value", ["None", "none", "NONE.", "  None  ", "N/A", "n/a.", "-", "—", "—."])
def test_explicit_no_gate_values_are_ungated(value):
    r = _classify(f"**Gate criteria:** {value}")
    assert r["gated"] is False
    assert r["gate_condition"] is None
    assert r["explicitly_ungated"] == f"Gate criteria: {value.strip()}"


@pytest.mark.parametrize("field", ["Gate", "Gate date"])
def test_short_gate_fields_also_honour_none(field):
    r = _classify(f"**{field}:** N/A")
    assert r["gated"] is False
    assert r["explicitly_ungated"] == f"{field}: N/A"


def test_real_gate_is_still_gated():
    r = _classify("**Gate criteria:** AI feature usage review due 2027-01-03. Not actionable before that date.")
    assert r["gated"] is True
    assert r["gate_source"] == "Gate criteria"
    assert r["explicitly_ungated"] is None


@pytest.mark.parametrize("value", ["None of the above until BLG-OPS-17 ships", "Not applicable until v10", "N/A pending review"])
def test_text_that_only_starts_with_none_is_still_a_gate(value):
    assert _classify(f"**Gate criteria:** {value}")["gated"] is True


def test_none_criteria_does_not_hide_a_real_short_gate_field():
    body = "### BLG-GOV-1 — Title\n**Gate criteria:** None\n**Gate:** BLG-OPS-17 complete.\n"
    r = sbgc.classify_item("BLG-GOV-1", "Title", body, AS_OF)
    assert r["gated"] is True
    assert r["gate_source"] == "Gate"


def test_cli_reports_explicitly_ungated_count_and_json_key(tmp_path):
    backlog = tmp_path / "backlog.md"
    backlog.write_text(
        "### BLG-GOV-1 — A\n**Gate criteria:** None\n\n---\n\n"
        "### BLG-GOV-2 — B\n**Gate criteria:** N/A.\n\n---\n\n"
        "### BLG-GOV-3 — C\n**Gate criteria:** BLG-OPS-17 complete.\n\n---\n\n"
    )
    text = subprocess.run([sys.executable, str(SCRIPT), "--backlog", str(backlog), "--as-of", "2026-10-16"],
                          capture_output=True, text=True, check=True).stdout
    assert "1 gated/conditional item(s)" in text
    assert "2 explicitly ungated item(s)" in text
    data = json.loads(subprocess.run([sys.executable, str(SCRIPT), "--backlog", str(backlog), "--json"],
                                     capture_output=True, text=True, check=True).stdout)
    assert [r["id"] for r in data["gated"]] == ["BLG-GOV-3"]
    assert [r["id"] for r in data["explicitly_ungated"]] == ["BLG-GOV-1", "BLG-GOV-2"]


LIVE_NONE_ITEMS = {
    "BLG-GOV-178", "BLG-GOV-184", "BLG-GOV-185", "BLG-GOV-186", "BLG-GOV-189", "BLG-GOV-191",
    "BLG-GOV-192", "BLG-GOV-193", "BLG-GOV-194", "BLG-GOV-195", "BLG-GOV-196", "BLG-GOV-198",
    "BLG-GOV-200", "BLG-GOV-201", "BLG-SPEC-77", "BLG-OPS-105", "BLG-QA-93",
}


def test_live_backlog_none_items_are_no_longer_gated():
    """The 17 items named in BLG-GOV-390 leave the gated list; BLG-GOV-382's real gate stays."""
    items = sbgc.parse_items((ROOT / "claude" / "backlog" / "backlog.md").read_text())
    results = {r["id"]: r for r in (sbgc.classify_item(i, t, b, AS_OF) for i, t, b in items)}
    still_present = LIVE_NONE_ITEMS & set(results)
    assert all(not results[i]["gated"] for i in still_present)
    if "BLG-GOV-382" in results:
        assert results["BLG-GOV-382"]["gated"] is True
