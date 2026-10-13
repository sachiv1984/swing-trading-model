"""
ST-39 (BLG-GOV-385, EPIC-06, v9.12) — scripts/check_backlog_item_integrity.py
fails on the backlog.md splice a clean CLAUDE.md §8 merge produced at
3237cb5e, and passes on the repaired file and on today's backlog.md.
"""
import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "backlog_item_integrity"
_spec = importlib.util.spec_from_file_location("integrity", ROOT / "scripts" / "check_backlog_item_integrity.py")
integrity = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(integrity)

GOOD_ITEM = """### BLG-QA-1 — Example
**Priority:** P3 (Low)
**Type:** QA
**Owner:** QA & Testing Owner
**Source:** test
**Effort:** S
**Provisional-Target:** TBD

**Problem**
Something.

**Scope**
- Do it

**Acceptance Criteria**
- Done

---
"""


def _git_show(ref):
    try:
        return subprocess.run(["git", "show", f"{ref}:claude/backlog/backlog.md"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip(f"{ref} not in this checkout (shallow clone)")


def test_well_formed_item_passes():
    assert integrity.check_text(GOOD_ITEM) == []


def test_legacy_formats_pass():
    compact = ("### BLG-BE-1 — Compact\n**Priority:** P3 | **Type:** Backend | **Owner:** X | **Source:** Y "
               "| **Effort:** S | **Provisional-Target:** TBD\n**Problem:** p\n**Scope:** s\n**Acceptance Criteria:** a\n")
    proposed = GOOD_ITEM.replace("**Scope**\n- Do it\n\n**Acceptance Criteria**\n- Done", "**Proposed solution**\nDo it")
    assert integrity.check_text(compact) == []
    assert integrity.check_text(proposed) == []


def test_spliced_fixture_fails_and_names_both_items():
    violations = integrity.check_text((FIXTURES / "spliced_3237cb5e.md").read_text())
    assert any("BLG-SPEC-190" in v and "Problem block found 0" in v for v in violations)
    assert any("BLG-BE-157" in v and "Scope block found 2" in v for v in violations)
    assert any("BLG-BE-157" in v and "Acceptance Criteria block found 2" in v for v in violations)


def test_repaired_fixture_passes():
    assert integrity.check_text((FIXTURES / "repaired_936181f7.md").read_text()) == []


@pytest.mark.parametrize("mutation, expected", [
    (lambda t: t + "\n" + t, "appears 2 times"),
    (lambda t: t.replace("**Owner:** QA & Testing Owner\n", ""), "**Owner:** found 0"),
    (lambda t: t.replace("**Effort:** S\n", "**Effort:** S\n**Effort:** S\n"), "**Effort:** found 2"),
    (lambda t: t.replace("**Problem**\nSomething.\n", ""), "Problem block found 0"),
    (lambda t: t.replace("**Acceptance Criteria**\n- Done\n", ""), "no Acceptance Criteria block"),
])
def test_each_structural_break_is_named(mutation, expected):
    violations = integrity.check_text(mutation(GOOD_ITEM))
    assert any(expected in v for v in violations), violations


def test_real_3237cb5e_fails_and_936181f7_passes():
    assert integrity.check_text(_git_show("3237cb5e"))
    assert integrity.check_text(_git_show("936181f7")) == []


def test_current_backlog_passes():
    assert integrity.main([str(ROOT / "claude" / "backlog" / "backlog.md")]) == 0
