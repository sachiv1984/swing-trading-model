"""ST-06 (BLG-QA-271, EPIC-01, v9.18): scripts/perf/check_bundle_size.py.

The checker reports gzipped JS against performance_budget.md §3.3. Each
over-budget form it claims to catch has a deliberately bad sample here (main
bundle, a chunk, the total), plus the inputs that must not pass silently
(no build directory; a directory with only .map files).
"""

import importlib.util
import os
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "check_bundle_size", Path(__file__).parent.parent / "scripts" / "perf" / "check_bundle_size.py"
)
cbs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cbs)

KB = 1024


def _write_js(js_dir: Path, name: str, gzip_target_kb: float):
    """Write incompressible bytes so gzip size ~= the target (random data barely compresses)."""
    js_dir.mkdir(parents=True, exist_ok=True)
    (js_dir / name).write_bytes(os.urandom(int(gzip_target_kb * KB)))


def _build(tmp_path, files):
    js = tmp_path / "build" / "static" / "js"
    for name, kb in files:
        _write_js(js, name, kb)
    return tmp_path / "build"


def test_within_budget_reports_no_overage(tmp_path, capsys):
    build = _build(tmp_path, [("main.abc.js", 150), ("12.def.chunk.js", 40)])
    assert cbs.main([str(build)]) == 0
    out = capsys.readouterr().out
    assert "::warning" not in out
    assert "| main.abc.js | main |" in out
    assert "| 12.def.chunk.js | chunk |" in out


def test_main_over_budget_is_reported_not_failed_by_default(tmp_path, capsys):
    build = _build(tmp_path, [("main.abc.js", 210)])
    assert cbs.main([str(build)]) == 0
    out = capsys.readouterr().out
    assert "::warning title=Bundle over budget::main.abc.js" in out
    assert "(main budget)" in out


def test_chunk_over_budget_is_reported(tmp_path, capsys):
    build = _build(tmp_path, [("main.abc.js", 50), ("7.x.chunk.js", 85)])
    cbs.main([str(build)])
    out = capsys.readouterr().out
    assert "7.x.chunk.js" in out and "(chunk budget)" in out


def test_total_over_budget_is_reported_even_when_each_file_is_within(tmp_path, capsys):
    build = _build(tmp_path, [("main.abc.js", 190)] + [(f"{i}.c.chunk.js", 70) for i in range(5)])
    cbs.main([str(build)])
    out = capsys.readouterr().out
    assert "total JS:" in out
    assert "(chunk budget)" not in out and "(main budget)" not in out


def test_enforce_fails_on_any_overage(tmp_path):
    build = _build(tmp_path, [("main.abc.js", 210)])
    assert cbs.main([str(build), "--enforce"]) == 1
    ok = _build(tmp_path / "ok", [("main.abc.js", 10)])
    assert cbs.main([str(ok), "--enforce"]) == 0


def test_missing_build_dir_exits_2(tmp_path):
    assert cbs.main([str(tmp_path / "nope")]) == 2


def test_only_map_files_exits_2(tmp_path):
    js = tmp_path / "build" / "static" / "js"
    js.mkdir(parents=True)
    (js / "main.abc.js.map").write_text("{}")
    (js / "main.abc.js.LICENSE.txt").write_text("MIT")
    assert cbs.main([str(tmp_path / "build")]) == 2


def test_summary_and_json_outputs(tmp_path):
    build = _build(tmp_path, [("main.abc.js", 210)])
    summary = tmp_path / "summary.md"
    js_out = tmp_path / "bundle.json"
    summary.write_text("existing\n")
    cbs.main([str(build), "--summary", str(summary), "--json", str(js_out)])
    text = summary.read_text()
    assert text.startswith("existing\n")  # appended, not overwritten
    assert "### JS bundle size" in text and "**Total**" in text
    import json
    data = json.loads(js_out.read_text())
    assert data["files"][0]["over"] is True
    assert data["total_gzip"] > 200 * KB
