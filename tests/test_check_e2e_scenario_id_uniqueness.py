"""
ST-42 (BLG-QA-224, EPIC-07, v9.15) — scripts/check_e2e_scenario_id_uniqueness.py:
no Playwright scenario ID is used in more than one file under tests/e2e
(beyond the shrink-only KNOWN_DUPLICATES list, BLG-QA-250), and SC-TS-* is
unique after the epic01-v62-stops-alerts.spec.js rename to SC-TSC-*.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("ckids", ROOT / "scripts" / "check_e2e_scenario_id_uniqueness.py")
ckids = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ckids)


def _write(root, name, *titles):
    body = "".join(f"test('{t}: does a thing', async ({{ page }}) => {{}});\n" for t in titles)
    (root / name).write_text(body)


def test_live_tree_has_no_new_cross_file_duplicates():
    ids = ckids.scenario_ids(ROOT / "tests" / "e2e")
    assert ckids.check(ids) == []


def test_sc_ts_ids_are_unique_across_files():
    ids = ckids.scenario_ids(ROOT / "tests" / "e2e")
    sc_ts = {sid: files for sid, files in ids.items() if sid.startswith("SC-TS-")}
    assert sc_ts and all(len(files) == 1 for files in sc_ts.values()), sc_ts
    assert not any(sid.startswith("SC-TS-") for sid in ckids.KNOWN_DUPLICATES)
    assert all(files == {"epic01-v62-stops-alerts.spec.js"}
               for sid, files in ids.items() if sid.startswith("SC-TSC-"))


def test_duplicate_across_two_files_fails(tmp_path):
    _write(tmp_path, "a.spec.js", "SC-AA-01", "SC-AA-02")
    _write(tmp_path, "b.spec.js", "SC-AA-02")
    problems = ckids.check(ckids.scenario_ids(tmp_path), known={})
    assert problems == ["SC-AA-02: used in 2 files: a.spec.js, b.spec.js"]


def test_repeat_within_one_file_and_longer_prefix_are_not_duplicates(tmp_path):
    _write(tmp_path, "a.spec.js", "SC-TS-01", "SC-TS-01")
    _write(tmp_path, "b.spec.js", "SC-TSC-01", "SC-TS-01a")
    assert ckids.check(ckids.scenario_ids(tmp_path), known={}) == []


def test_known_duplicate_passes_but_a_stale_entry_fails(tmp_path):
    _write(tmp_path, "a.spec.js", "SC-AA-01")
    _write(tmp_path, "b.spec.js", "SC-AA-01")
    known = {"SC-AA-01": ("a.spec.js", "b.spec.js")}
    assert ckids.check(ckids.scenario_ids(tmp_path), known=known) == []
    _write(tmp_path, "b.spec.js", "SC-BB-01")      # duplicate fixed, entry left behind
    assert any("no longer matches" in p for p in ckids.check(ckids.scenario_ids(tmp_path), known=known))


def test_cli_exit_codes(tmp_path, capsys):
    _write(tmp_path, "a.spec.js", "SC-AA-01")
    _write(tmp_path, "b.spec.js", "SC-AA-01")
    assert ckids.main(["--root", str(tmp_path)]) == 1   # also reports every KNOWN_DUPLICATES entry stale
    assert "SC-AA-01: used in 2 files" in capsys.readouterr().out
    assert ckids.main(["--root", str(tmp_path / "missing")]) == 2
    assert ckids.main(["--root", str(ROOT / "tests" / "e2e")]) == 0
