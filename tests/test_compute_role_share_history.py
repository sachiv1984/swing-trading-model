"""
ST-45 (BLG-QA-212, EPIC-06, v9.12) — unit tests for
scripts/compute_role_share_history.py, which roadmap_prompt.md §7.2 depends on.
Covers simple and compound Owner strings, a story with no Owner line (reported,
not silently dropped), the --json shape, and the v9.8 regression pin.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "compute_role_share_history.py"
_spec = importlib.util.spec_from_file_location("role_share", SCRIPT)
role_share = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(role_share)

FIXTURE = """# Sprint Backlog — fixture

### EPIC-01 — Example
**Owner:** Head of Specs Team; PMO Lead

#### ST-01 — Simple owner
**Owner:** Head of Specs Team
**Delegation class:** autonomous

---

#### ST-02 — Compound owner
**Owner:** Head of Engineering; Head of UX & Design

---

#### ST-03 — Same simple owner again
**Owner:** Head of Specs Team

---

#### ST-04 — No owner line
**Delegation class:** autonomous

---
"""


def _run(path, *extra):
    return subprocess.run([sys.executable, str(SCRIPT), str(path), *extra], capture_output=True, text=True)


def _write(tmp_path, text, cycle="2026-01-01__release-v0.1"):
    d = tmp_path / cycle
    d.mkdir()
    p = d / "sprint_backlog.md"
    p.write_text(text)
    return p


def test_simple_and_compound_owners_tallied_verbatim():
    a = role_share.analyse(FIXTURE)
    assert a["counts"] == {"Head of Specs Team": 2, "Head of Engineering; Head of UX & Design": 1}
    # the EPIC-level Owner line is not a story and is not counted
    assert "Head of Specs Team; PMO Lead" not in a["counts"]


def test_story_with_no_owner_line_is_reported_not_dropped(tmp_path):
    a = role_share.analyse(FIXTURE)
    assert a["unattributed"] == ["ST-04"]
    assert a["st_headings"] == 4 and sum(a["counts"].values()) == 3
    result = _run(_write(tmp_path, FIXTURE))
    assert result.returncode == 0
    assert "WARNING" in result.stderr and "ST-04" in result.stderr and "difference 1" in result.stderr


def test_st_heading_at_another_level_is_reported(tmp_path):
    text = FIXTURE + "\n### ST-05 — Wrong heading level\n**Owner:** PMO Lead\n"
    a = role_share.analyse(text)
    assert a["other_level_headings"] == ["ST-05"]
    assert a["st_headings"] == 5
    assert "ST-05" in _run(_write(tmp_path, text)).stderr


def test_total_equals_st_headings_when_every_story_has_an_owner(tmp_path):
    text = FIXTURE.replace("#### ST-04 — No owner line\n", "#### ST-04 — Now owned\n**Owner:** PMO Lead\n")
    result = _run(_write(tmp_path, text), "--json")
    data = json.loads(result.stdout)["2026-01-01__release-v0.1"]
    assert data["total"] == data["st_headings"] == 4
    assert result.stderr == ""


def test_json_output_shape(tmp_path):
    data = json.loads(_run(_write(tmp_path, FIXTURE), "--json").stdout)
    cycle = data["2026-01-01__release-v0.1"]
    assert set(cycle) >= {"total", "by_role", "st_headings", "unattributed", "other_level_headings"}
    assert cycle["total"] == 3
    assert list(cycle["by_role"].items())[0] == ("Head of Specs Team", 2)


def test_v9_8_regression_pin():
    path = ROOT / "claude" / "cycles" / "2026-09-28__release-v9.8" / "sprint_backlog.md"
    a = role_share.analyse(path.read_text())
    assert sum(a["counts"].values()) == 39 == a["st_headings"]
    assert a["counts"]["Head of Specs Team"] == 12
    assert a["unattributed"] == [] and a["other_level_headings"] == []
