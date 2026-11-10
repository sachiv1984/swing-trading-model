"""Tests for scripts/arc_velocity_report.py (ST-29, EPIC-07, v9.16, BLG-GOV-26)."""
import importlib.util
import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "arc_velocity_report.py")
REPORT = os.path.join(ROOT, "docs", "governance", "arc_velocity_report_arc2.md")

spec = importlib.util.spec_from_file_location("arc_velocity_report", SCRIPT)
avr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(avr)

VELOCITY_MD = """
| Cycle | Planned | Completed | Velocity | Notes |
|-------|---------|-----------|----------|-------|
| v1.1  | 10      | 10        | 1.00     | ok |
| v1.2  | 4       | 2         | 0.50     | gate |
| v1.10 | 6       | 6         | 1.00     | ok |
| v2.0  | 5       | 5         | 1.00     | outside range |
"""


def _cycle(tmp_path, name, epics):
    d = tmp_path / name
    d.mkdir()
    (d / "execution_state.json").write_text(json.dumps({"epics": epics}))


@pytest.fixture
def fixture_dirs(tmp_path):
    vel = tmp_path / "velocity_metrics.md"
    vel.write_text(VELOCITY_MD)
    cycles = tmp_path / "cycles"
    cycles.mkdir()
    _cycle(cycles, "2026-01-01__release-v1.1", {"EPIC-01": {"status": "merged"}, "EPIC-02": {"status": "done"}})
    _cycle(cycles, "2026-01-02__release-v1.2", {
        "EPIC-01": {"status": "merged"},
        "EPIC-02": {"status": "returned_to_backlog"},
        "EPIC-03": {"status": "deferred_at_planning"},
    })
    _cycle(cycles, "2026-01-03__release-v1.10", {"EPIC-01": {"status": "merged"}})
    return vel, cycles


def test_parse_velocity_table_reads_rows():
    rows = avr.parse_velocity_table(VELOCITY_MD)
    assert rows["v1.2"] == {"planned": 4, "completed": 2, "velocity": 0.5}
    assert set(rows) == {"v1.1", "v1.2", "v1.10", "v2.0"}


def test_select_range_orders_numerically():
    assert avr.select_range({"v1.10", "v1.2", "v1.1", "v2.0"}, "v1.1", "v1.10") == ["v1.1", "v1.2", "v1.10"]


def test_epic_counts_excludes_deferred_at_planning():
    c = avr.epic_counts({"epics": {
        "EPIC-01": {"status": "merged"},
        "EPIC-02": {"status": "returned_to_backlog"},
        "EPIC-03": {"status": "deferred_at_planning"},
    }})
    assert c == {"in_scope": 2, "completed": 1, "deferred_at_planning": 1,
                 "not_completed": ["EPIC-02: returned_to_backlog"]}


def test_summary_measures(fixture_dirs):
    vel, cycles = fixture_dirs
    velocity = avr.parse_velocity_table(vel.read_text())
    rows, missing = avr.build_rows(velocity, avr.find_cycle_dirs(str(cycles)), "v1.1", "v1.10")
    assert [r["version"] for r in rows] == ["v1.1", "v1.2", "v1.10"]
    assert missing == []
    s = avr.summarise(rows, window=2)
    assert (s["planned"], s["completed"]) == (20, 18)
    assert s["arc_velocity"] == pytest.approx(0.9)
    assert (s["epics_completed"], s["epics_in_scope"]) == (4, 5)
    assert s["epics_deferred_at_planning"] == 1
    assert s["rolling"] == [("v1.2", 0.75), ("v1.10", 0.75)]
    assert [r["version"] for r in s["below_full"]] == ["v1.2"]


def test_missing_inputs_reported(fixture_dirs):
    vel, cycles = fixture_dirs
    velocity = avr.parse_velocity_table(vel.read_text())
    _cycle(cycles, "2026-01-04__release-v1.3", {"EPIC-01": {"status": "merged"}})
    rows, missing = avr.build_rows(velocity, avr.find_cycle_dirs(str(cycles)), "v1.1", "v1.10")
    assert "v1.3" not in [r["version"] for r in rows]
    assert missing == ["v1.3: no velocity_metrics.md row"]


def test_out_replaces_only_between_markers(fixture_dirs, tmp_path):
    vel, cycles = fixture_dirs
    report = tmp_path / "report.md"
    report.write_text(f"# Head\n{avr.BEGIN}\nstale\n{avr.END}\n## Tail\n")
    rc = avr.main(["--arc", "Arc X", "--from", "v1.1", "--to", "v1.10", "--velocity-file", str(vel),
                   "--cycles-dir", str(cycles), "--window", "2", "--out", str(report)])
    assert rc == 0
    text = report.read_text()
    assert text.startswith("# Head\n") and text.endswith("## Tail\n")
    assert "stale" not in text
    assert "| EPIC completion rate | 4 / 5 = 0.800 |" in text


def test_arc2_report_matches_generator_output():
    """The committed Arc 2 report's data section is the generator's current output."""
    out = subprocess.run(
        [sys.executable, SCRIPT, "--arc", "Arc 2", "--from", "v3.1", "--to", "v6.1"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    text = open(REPORT, encoding="utf-8").read()
    section = text.split(avr.BEGIN + "\n", 1)[1].split(avr.END, 1)[0]
    assert section == out
