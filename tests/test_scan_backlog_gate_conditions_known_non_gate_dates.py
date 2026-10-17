"""
ST-36 (BLG-GOV-373, EPIC-06, v9.13) — scripts/scan_backlog_gate_conditions.py
keeps an allow-list of known non-gate dates (each with a reason and a review
date), ignores those dates when deciding whether a gate has lapsed, and
reports the entries separately as "known non-gate dates".

The 2026-10-16 scan's date-lapsed list is empty, so these tests use a
fixture built from the 2026-10-06 gate text of BLG-OPS-53 and BLG-FEAT-92,
which three rebalances excluded by hand.
"""
import datetime
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "scan_backlog_gate_conditions.py"
_spec = importlib.util.spec_from_file_location("sbgc_non_gate", SCRIPT)
sbgc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sbgc)

AS_OF = datetime.date(2026, 10, 6)

OPS_53_GATE = (
    "claude_audit_log table 6+ months old (~Nov 2026, since v4.0 ship 2026-05-22). "
    "BLG-OPS-31 (Render log retention policy) shipped v4.7."
)
FEAT_92_GATE = (
    "Inherits `BLG-FEAT-30`'s gate (screener live ≥60 days AND ≥60 closed trades with attribution). "
    "Reconciled at the Product Owner's `2026-09-03__release-v9.1` decision (reaffirmed "
    "`decisions--2026-09-07__release-v9.2.md`); this field added `2026-09-09`."
)


def _item(item_id, gate):
    return f"### {item_id} — Title {item_id}\n**Priority:** P3\n**Gate criteria:** {gate}\n\n---\n\n"


FIXTURE = (
    _item("BLG-OPS-53", OPS_53_GATE)
    + _item("BLG-FEAT-92", FEAT_92_GATE)
    + _item("BLG-FEAT-62", "≥20 closed trades captured post-PT-04 (2026-06-23).")  # real lapse, not allow-listed
)


def _results(text, allow_list=sbgc.KNOWN_NON_GATE_DATES, as_of=AS_OF):
    return {r["id"]: r for r in (sbgc.classify_item(i, t, b, as_of, allow_list) for i, t, b in sbgc.parse_items(text))}


def test_allow_list_entries_carry_reason_and_review_date():
    ids = {e["id"] for e in sbgc.KNOWN_NON_GATE_DATES}
    assert {"BLG-OPS-53", "BLG-FEAT-92"} <= ids
    for e in sbgc.KNOWN_NON_GATE_DATES:
        assert e["reason"].strip()
        datetime.date.fromisoformat(e["review_by"])
        assert e["date"] is None or datetime.date.fromisoformat(e["date"])


def test_counting_start_and_provenance_dates_are_not_date_lapsed():
    results = _results(FIXTURE)
    assert results["BLG-OPS-53"]["date_lapsed"] is None
    assert results["BLG-FEAT-92"]["date_lapsed"] is None
    # still gated: the allow-list only affects date-lapse, never the gate itself
    assert results["BLG-OPS-53"]["gated"] and results["BLG-FEAT-92"]["gated"]


def test_without_the_allow_list_both_would_be_flagged():
    results = _results(FIXTURE, allow_list=[])
    assert results["BLG-OPS-53"]["date_lapsed"] == datetime.date(2026, 5, 22)
    assert results["BLG-FEAT-92"]["date_lapsed"] is not None


def test_non_allow_listed_item_still_lapses():
    assert _results(FIXTURE)["BLG-FEAT-62"]["date_lapsed"] == datetime.date(2026, 6, 23)


def test_date_scoped_entry_keeps_the_items_other_dates():
    """BLG-OPS-53's entry ignores only the ship date; its real clears-date still lapses."""
    gate = "claude_audit_log table 6+ months old — clears 2026-11-22 (6 months after the v4.0 ship 2026-05-22)."
    results = _results(_item("BLG-OPS-53", gate), as_of=datetime.date(2026, 11, 23))
    assert results["BLG-OPS-53"]["date_lapsed"] == datetime.date(2026, 11, 22)
    assert _results(_item("BLG-OPS-53", gate), as_of=datetime.date(2026, 10, 16))["BLG-OPS-53"]["date_lapsed"] is None


def test_known_non_gate_dates_rows_flag_presence_and_review_due():
    allow = [
        {"id": "BLG-OPS-53", "date": "2026-05-22", "reason": "ship date", "review_by": "2026-10-01"},
        {"id": "BLG-FEAT-92", "date": None, "reason": "provenance", "review_by": "2027-01-16"},
        {"id": "BLG-GOV-9", "date": "2026-01-01", "reason": "gone", "review_by": "2027-01-16"},
    ]
    results = list(_results(FIXTURE, allow_list=allow).values())
    rows = {r["id"]: r for r in sbgc.known_non_gate_dates(results, AS_OF, allow)}
    assert rows["BLG-OPS-53"]["present"] and rows["BLG-OPS-53"]["review_due"]
    assert rows["BLG-FEAT-92"]["present"] and not rows["BLG-FEAT-92"]["review_due"]
    assert not rows["BLG-GOV-9"]["present"]


def test_cli_reports_known_non_gate_dates_separately(tmp_path):
    backlog = tmp_path / "backlog.md"
    backlog.write_text(FIXTURE)
    text = subprocess.run([sys.executable, str(SCRIPT), "--backlog", str(backlog), "--as-of", "2026-10-06"],
                          capture_output=True, text=True, check=True).stdout
    lapsed = text.split("lapsed gate date", 1)[1].split("\n\n", 1)[0]
    assert "BLG-FEAT-62" in lapsed
    assert "BLG-OPS-53" not in lapsed and "BLG-FEAT-92" not in lapsed
    known = text.split("known non-gate date(s)", 1)[1].split("\n\n", 1)[0]
    assert "BLG-OPS-53" in known and "BLG-FEAT-92" in known and "review by" in known
    data = json.loads(subprocess.run([sys.executable, str(SCRIPT), "--backlog", str(backlog), "--json", "--as-of", "2026-10-06"],
                                     capture_output=True, text=True, check=True).stdout)
    assert [r["id"] for r in data["date_lapsed"]] == ["BLG-FEAT-62"]
    assert {r["id"] for r in data["known_non_gate_dates"]} >= {"BLG-OPS-53", "BLG-FEAT-92"}
