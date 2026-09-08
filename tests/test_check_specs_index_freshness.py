"""
Unit tests for scripts/check_specs_index_freshness.py (ST-11, BLG-QA-161,
EPIC-03, v9.2).

Covers both detection paths (additions, removals), at least one exclusion
rule (docs/specs/qa/**), and explicitly confirms a legitimate non-docs/specs/
cross-reference (e.g. strategy_rules.md) is not flagged as a removal --
the AC's named false-positive guard.

REPO_ROOT/SPECS_DIR/INDEX_FILE are module-level constants derived from
__file__ at import time; each test that needs a sandboxed tree monkeypatches
those three attributes to point at a temp fixture instead of the real repo,
so this file never reads or depends on the real docs/specs/ tree.
"""
import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "check_specs_index_freshness.py"

spec = importlib.util.spec_from_file_location("check_specs_index_freshness", SCRIPT_PATH)
csif = importlib.util.module_from_spec(spec)
sys.modules["check_specs_index_freshness"] = csif
spec.loader.exec_module(csif)


# ---------------------------------------------------------------------------
# find_indexed_references -- pure function, no fixture needed
# ---------------------------------------------------------------------------

def test_find_indexed_references_extracts_full_docs_specs_paths():
    text = "See docs/specs/api_contracts/positions_endpoints.md for details."
    basenames, paths = csif.find_indexed_references(text)
    assert paths == {"api_contracts/positions_endpoints.md"}
    assert basenames == set()


def test_find_indexed_references_extracts_bare_backtick_basenames():
    text = "Canonical: `trade_endpoints.md`, cross-ref `strategy_rules.md`."
    basenames, paths = csif.find_indexed_references(text)
    assert basenames == {"trade_endpoints.md", "strategy_rules.md"}
    assert paths == set()


def test_find_indexed_references_treats_backtick_subpaths_as_paths():
    text = "See `api_contracts/positions_endpoints.md` for the envelope shape."
    basenames, paths = csif.find_indexed_references(text)
    assert paths == {"api_contracts/positions_endpoints.md"}
    assert basenames == set()


# ---------------------------------------------------------------------------
# main() end-to-end against a sandboxed fixture tree
# ---------------------------------------------------------------------------

def _build_fixture(tmp_path, index_text, specs_files=(), other_repo_files=()):
    """specs_files: iterable of (relative_path_under_docs_specs, content).
    other_repo_files: iterable of (relative_path_under_repo_root, content) --
    for exercising REPO_ROOT.rglob('*.md') cross-reference matching."""
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "Specs_Index.md").write_text(index_text)
    for rel, content in specs_files:
        p = specs_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    for rel, content in other_repo_files:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    return specs_dir


def _run_main(monkeypatch, tmp_path, index_text, specs_files=(), other_repo_files=()):
    specs_dir = _build_fixture(tmp_path, index_text, specs_files, other_repo_files)
    monkeypatch.setattr(csif, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(csif, "SPECS_DIR", specs_dir)
    monkeypatch.setattr(csif, "INDEX_FILE", specs_dir / "Specs_Index.md")
    return csif.main()


def test_addition_detected_for_unreferenced_live_file(monkeypatch, tmp_path, capsys):
    """A live docs/specs/ file mentioned nowhere in Specs_Index.md is
    reported as an ADDITION and the script exits 1."""
    exit_code = _run_main(
        monkeypatch, tmp_path,
        index_text="Nothing indexed here.",
        specs_files=[("orphan_spec.md", "# Orphan")],
    )
    out = capsys.readouterr().out
    assert exit_code == 1
    assert "ADDITIONS" in out
    assert "orphan_spec.md" in out
    assert "REMOVALS" not in out


def test_removal_detected_for_stale_reference(monkeypatch, tmp_path, capsys):
    """A Specs_Index.md reference to a file that exists nowhere in the repo
    (docs/specs/ or otherwise) is reported as a REMOVAL."""
    exit_code = _run_main(
        monkeypatch, tmp_path,
        index_text="See docs/specs/deleted_spec.md for the old contract.",
        specs_files=[],
    )
    out = capsys.readouterr().out
    assert exit_code == 1
    assert "REMOVALS" in out
    assert "deleted_spec.md" in out
    assert "ADDITIONS" not in out


def test_exclusion_rule_qa_directory_not_flagged_as_addition(monkeypatch, tmp_path, capsys):
    """docs/specs/qa/** is excluded by design -- a live file there must not
    be reported as an addition even though nothing references it."""
    exit_code = _run_main(
        monkeypatch, tmp_path,
        index_text="Nothing indexed here.",
        specs_files=[("qa/some_scenario_doc.md", "# QA scenario")],
    )
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "some_scenario_doc.md" not in out


def test_legitimate_cross_reference_not_flagged_as_removal(monkeypatch, tmp_path, capsys):
    """Named false-positive guard (AC): a bare-filename cross-reference to a
    real, non-docs/specs/ canonical file (e.g. strategy_rules.md, living
    under claude/strategy/) must not be flagged as a removal just because it
    doesn't live under docs/specs/."""
    exit_code = _run_main(
        monkeypatch, tmp_path,
        index_text="Strategy boundaries are defined in `strategy_rules.md`.",
        specs_files=[],
        other_repo_files=[("claude/strategy/strategy_rules.md", "# Strategy Rules")],
    )
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "strategy_rules.md" not in out


def test_clean_index_passes_with_no_additions_or_removals(monkeypatch, tmp_path, capsys):
    exit_code = _run_main(
        monkeypatch, tmp_path,
        index_text="Tracked: docs/specs/tracked_spec.md.",
        specs_files=[("tracked_spec.md", "# Tracked")],
    )
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "PASSED" in out
