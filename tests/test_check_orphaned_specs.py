"""
Unit tests for scripts/check_orphaned_specs.py (ST-17, BLG-SPEC-70, EPIC-04,
v9.3).

Uses a fully sandboxed temp tree (specs dir + repo root + backlog files) via
monkeypatch — never reads the real repo, so it stays fast and independent of
the real docs/specs/ tree's actual (changing) contents. Deliberately proves
detection works (a genuinely-unreferenced file IS flagged), not just that it
never trips — mirrors the precedent already used by
test_lint_api_contract_headings.py / test_pilot_contract_schemas.py's own
"prove the check catches drift, not just that it passes" convention.
"""
import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "check_orphaned_specs.py"

spec = importlib.util.spec_from_file_location("check_orphaned_specs", SCRIPT_PATH)
cos = importlib.util.module_from_spec(spec)
sys.modules["check_orphaned_specs"] = cos
spec.loader.exec_module(cos)


def _make_tree(tmp_path):
    """Build a minimal sandboxed repo tree: docs/specs/, claude/backlog/,
    and a source file, returning (specs_dir, repo_root, backlog_files)."""
    specs_dir = tmp_path / "docs" / "specs"
    specs_dir.mkdir(parents=True)
    backlog_dir = tmp_path / "claude" / "backlog"
    backlog_dir.mkdir(parents=True)
    backlog = backlog_dir / "backlog.md"
    backlog.write_text("")
    archive = backlog_dir / "backlog_archive.md"
    archive.write_text("")
    return specs_dir, tmp_path, [backlog, archive]


def test_referenced_in_backlog_is_not_orphaned(tmp_path):
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "referenced_endpoint.md").write_text("# Some spec")
    backlog_files[0].write_text("See `referenced_endpoint.md` for the contract.")

    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, backlog_files)
    assert orphaned == []


def test_referenced_in_code_comment_is_not_orphaned(tmp_path):
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "referenced_endpoint.md").write_text("# Some spec")
    src = repo_root / "backend"
    src.mkdir()
    (src / "routers.py").write_text("# Spec: docs/specs/referenced_endpoint.md\n")

    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, backlog_files)
    assert orphaned == []


def test_referenced_only_by_sibling_spec_is_not_orphaned(tmp_path):
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "referenced_endpoint.md").write_text("# Some spec")
    (specs_dir / "index.md").write_text("See referenced_endpoint.md for details.")
    # index.md itself needs its own reference too, so this test isolates
    # exactly one fact (a sibling-spec mention suffices to clear a file) —
    # without this, index.md would legitimately be its own orphan finding.
    backlog_files[0].write_text("See index.md for the spec index.")

    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, backlog_files)
    assert orphaned == []


def test_genuinely_unreferenced_file_is_flagged(tmp_path):
    """Proves the detector actually catches drift, not just that it passes
    on well-referenced fixtures."""
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "orphaned_endpoint.md").write_text("# A spec nobody mentions anywhere else")
    # Referenced fixture alongside it, to prove the orphan isn't a false
    # positive from an empty/broken scan.
    (specs_dir / "referenced_endpoint.md").write_text("# Some spec")
    backlog_files[0].write_text("See `referenced_endpoint.md`.")

    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, backlog_files)
    assert orphaned == ["docs/specs/orphaned_endpoint.md"]


def test_self_mention_does_not_count_as_a_reference(tmp_path):
    """A file's own filename appearing inside itself (e.g. in its own
    header/title) must not count as a reference — that would make every
    file trivially non-orphaned."""
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "self_referencing.md").write_text(
        "# self_referencing.md\n\nThis document is self_referencing.md, see self_referencing.md for details."
    )

    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, backlog_files)
    assert orphaned == ["docs/specs/self_referencing.md"]


def test_vendored_directories_excluded_from_scan(tmp_path):
    """A reference sitting only inside an excluded directory (e.g.
    node_modules) must not count — vendored files are not real cross-refs."""
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "orphaned_endpoint.md").write_text("# A spec")
    vendored = repo_root / "node_modules" / "somepkg"
    vendored.mkdir(parents=True)
    (vendored / "readme.md").write_text("mentions orphaned_endpoint.md incidentally")

    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, backlog_files)
    assert orphaned == ["docs/specs/orphaned_endpoint.md"]


def test_multiple_orphans_all_reported(tmp_path):
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "orphan_a.md").write_text("# A")
    (specs_dir / "orphan_b.md").write_text("# B")
    (specs_dir / "referenced.md").write_text("# C")
    backlog_files[0].write_text("See referenced.md.")

    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, backlog_files)
    assert orphaned == ["docs/specs/orphan_a.md", "docs/specs/orphan_b.md"]


def test_nested_subdirectory_specs_are_scanned(tmp_path):
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    nested = specs_dir / "api_contracts"
    nested.mkdir()
    (nested / "orphaned_nested.md").write_text("# Nested orphan")

    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, backlog_files)
    assert orphaned == ["docs/specs/api_contracts/orphaned_nested.md"]


def test_missing_backlog_file_does_not_crash(tmp_path):
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "some_spec.md").write_text("# A spec")
    missing = [tmp_path / "does_not_exist.md"]

    # Must not raise even though the "backlog file" doesn't exist.
    orphaned = cos.find_orphaned_specs(specs_dir, repo_root, missing)
    assert orphaned == ["docs/specs/some_spec.md"]


def test_main_json_output(tmp_path, monkeypatch, capsys):
    specs_dir, repo_root, backlog_files = _make_tree(tmp_path)
    (specs_dir / "orphan.md").write_text("# orphan")
    monkeypatch.setattr(cos, "SPECS_DIR", specs_dir)
    monkeypatch.setattr(cos, "REPO_ROOT", repo_root)
    monkeypatch.setattr(cos, "BACKLOG_FILES", backlog_files)
    monkeypatch.setattr(sys, "argv", ["check_orphaned_specs.py", "--json"])

    rc = cos.main()

    assert rc == 0
    captured = capsys.readouterr()
    assert "orphan.md" in captured.out
    assert '"count": 1' in captured.out
