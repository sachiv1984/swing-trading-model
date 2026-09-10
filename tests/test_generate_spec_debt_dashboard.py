"""
Unit tests for scripts/generate_spec_debt_dashboard.py (ST-16, BLG-SPEC-69,
EPIC-04, v9.3).

Covers: standard one-field-per-line parsing, the legacy condensed
multi-field-per-line format (BLG-SPEC-81's real shape in backlog.md), date
extraction including the "date immediately followed by underscore" edge case
that a naive \\b-bounded regex misses (e.g. "cycle 2026-05-22__scheduled"),
and priority-tier sort ordering.
"""
import importlib.util
import sys
from datetime import date
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "generate_spec_debt_dashboard.py"

spec = importlib.util.spec_from_file_location("generate_spec_debt_dashboard", SCRIPT_PATH)
gsdd = importlib.util.module_from_spec(spec)
sys.modules["generate_spec_debt_dashboard"] = gsdd
spec.loader.exec_module(gsdd)


# ---------------------------------------------------------------------------
# parse_backlog_items
# ---------------------------------------------------------------------------

def test_parse_standard_one_field_per_line_item():
    text = """
### BLG-SPEC-99 — Some spec debt title

**Priority:** P2 (Medium)
**Type:** Spec Debt
**Owner:** Head of Specs Team
**Source:** IDEA-x-20260101-01 — Promoted-Backlog cycle 2026-01-15__scheduled

**Problem**
Some problem text.

---

### BLG-GOV-1 — Unrelated governance item
**Priority:** P3 (Low)
"""
    items = gsdd.parse_backlog_items(text)
    assert len(items) == 1
    assert items[0] == {
        "id": "BLG-SPEC-99",
        "title": "Some spec debt title",
        "priority": "P2 (Medium)",
        "source": "IDEA-x-20260101-01 — Promoted-Backlog cycle 2026-01-15__scheduled",
    }


def test_parse_condensed_multi_field_per_line_item():
    """BLG-SPEC-81's real shape: all fields packed onto one line with ' | '
    separators instead of one field per line."""
    text = (
        "### BLG-SPEC-81 — Research view `signal_type` filter spec\n"
        "**Priority:** P3 (Low) | **Type:** Spec Debt | "
        "**Owner:** Frontend Specifications & UX Documentation Owner | "
        "**Source:** IDEA-frontend-specs-20260712-02 | **Effort:** S | "
        "**Provisional-Target:** Unscheduled\n"
        "**Gate criteria:** some gate\n"
    )
    items = gsdd.parse_backlog_items(text)
    assert len(items) == 1
    assert items[0]["title"] == "Research view `signal_type` filter spec"
    assert items[0]["priority"] == "P3 (Low)"
    assert items[0]["source"] == "IDEA-frontend-specs-20260712-02"


def test_parse_ignores_non_spec_items():
    text = "### BLG-GOV-5 — Not a spec item\n**Priority:** P1 (High)\n"
    items = gsdd.parse_backlog_items(text)
    assert items == []


def test_parse_multiple_items():
    text = (
        "### BLG-SPEC-1 — First\n**Priority:** P1 (High)\n**Source:** x 2026-01-01\n\n"
        "### BLG-SPEC-2 — Second\n**Priority:** P2 (Medium)\n**Source:** y 2026-02-02\n"
    )
    items = gsdd.parse_backlog_items(text)
    assert [i["id"] for i in items] == ["BLG-SPEC-1", "BLG-SPEC-2"]


# ---------------------------------------------------------------------------
# extract_filing_date
# ---------------------------------------------------------------------------

def test_extract_filing_date_finds_dash_date():
    assert gsdd.extract_filing_date("Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)") == date(2026, 5, 22)


def test_extract_filing_date_underscore_immediately_after_date():
    """The bug this test guards against: a naive \\b-bounded regex treats
    digit-then-underscore as NOT a word boundary (both are word characters),
    so it fails to match "2026-05-22__scheduled" at all without this fix."""
    assert gsdd.extract_filing_date("cycle 2026-05-22__scheduled") == date(2026, 5, 22)


def test_extract_filing_date_prefers_last_date_when_multiple_present():
    # e.g. an ID-embedded compact date (no dashes, doesn't match) plus a real one
    assert gsdd.extract_filing_date("IDEA-x-20260522-02 — cycle 2026-06-03__scheduled") == date(2026, 6, 3)


def test_extract_filing_date_no_date_returns_none():
    assert gsdd.extract_filing_date("No date here at all") is None


def test_extract_filing_date_none_source_returns_none():
    assert gsdd.extract_filing_date(None) is None


def test_extract_filing_date_does_not_overmatch_longer_digit_run():
    # "2026-05-223" should not be truncated-matched as "2026-05-22"
    assert gsdd.extract_filing_date("bogus 2026-05-223 not a real date") is None


# ---------------------------------------------------------------------------
# priority_sort_key
# ---------------------------------------------------------------------------

def test_priority_sort_key_orders_p0_first():
    assert gsdd.priority_sort_key("P0 (Critical)") < gsdd.priority_sort_key("P1 (High)")
    assert gsdd.priority_sort_key("P1 (High)") < gsdd.priority_sort_key("P2 (Medium)")
    assert gsdd.priority_sort_key("P2 (Medium)") < gsdd.priority_sort_key("P3 (Low)")


def test_priority_sort_key_unknown_or_none_sorts_last():
    assert gsdd.priority_sort_key("P4 (Trivial)") > gsdd.priority_sort_key("P3 (Low)")
    assert gsdd.priority_sort_key(None) > gsdd.priority_sort_key("P3 (Low)")


# ---------------------------------------------------------------------------
# main() — end-to-end against a fixture file
# ---------------------------------------------------------------------------

def test_main_writes_output_file(tmp_path, monkeypatch):
    backlog = tmp_path / "backlog.md"
    backlog.write_text(
        "### BLG-SPEC-1 — First item\n**Priority:** P1 (High)\n**Source:** x 2026-01-01\n\n"
        "### BLG-SPEC-2 — Second item\n**Priority:** P3 (Low)\n**Source:** y 2026-06-01\n"
    )
    output = tmp_path / "spec_debt_dashboard.md"
    monkeypatch.setattr(gsdd, "BACKLOG_PATH", backlog)
    monkeypatch.setattr(gsdd, "OUTPUT_PATH", output)

    rc = gsdd.main()

    assert rc == 0
    assert output.exists()
    content = output.read_text()
    assert "BLG-SPEC-1" in content
    assert "BLG-SPEC-2" in content
    assert "Total open BLG-SPEC-* items:** 2" in content


def test_main_missing_backlog_file_returns_error(tmp_path, monkeypatch):
    monkeypatch.setattr(gsdd, "BACKLOG_PATH", tmp_path / "does_not_exist.md")
    rc = gsdd.main()
    assert rc == 1
