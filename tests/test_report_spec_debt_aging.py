"""
ST-54 (BLG-GOV-191, EPIC-07, v9.14) — scripts/report_spec_debt_aging.py ages
open BLG-SPEC items by release cycles without a story (release_planning_prompt.md
§1.1), resets on a seated cycle, flags gated items and skips undated ones.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("aging", ROOT / "scripts" / "report_spec_debt_aging.py")
aging = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aging)

BACKLOG = """# Backlog

### BLG-SPEC-10 — Old item
**Source:** idea intake — 2026-09-01
**Gate criteria:** None

**Problem**
x

---

### BLG-SPEC-11 — Seated once
**Source:** ST-02, cycle 2026-09-10 — 2026-09-10

**Problem**
x

---

### BLG-SPEC-12 — Gated item
**Source:** review — 2026-09-01
**Gate criteria:** BLG-FEAT-99 shipped

**Problem**
x

---

### BLG-SPEC-13 — No date
**Source:** user request

**Problem**
x

---

### BLG-SPEC-14 — ✅ COMPLETE (v9.1) Done item
**Source:** review — 2026-09-01

---

### BLG-FE-15 — Not spec debt
**Source:** review — 2026-09-01

---
"""


def _cycles(tmp_path):
    for name, sources in [("2026-08-20__release-v9.0", []),
                          ("2026-09-05__release-v9.1", []),
                          ("2026-09-12__release-v9.2", ["BLG-SPEC-11"]),
                          ("2026-09-20__release-v9.3", []),
                          ("2026-09-25__scheduled", ["BLG-SPEC-10"])]:
        d = tmp_path / name
        d.mkdir()
        (d / "stage4_backlog_slice.md").write_text(
            "\n".join(f"### ST-0{n}\n**Source:** {s}\n" for n, s in enumerate(sources, 1)))
    return aging.release_cycles(tmp_path)


def _aged(tmp_path):
    items = aging.age_items(aging.open_spec_items(BACKLOG), _cycles(tmp_path))
    return {i["id"]: i for i in items}


def test_only_open_spec_items_are_listed(tmp_path):
    assert set(_aged(tmp_path)) == {"BLG-SPEC-10", "BLG-SPEC-11", "BLG-SPEC-12", "BLG-SPEC-13"}


def test_counts_release_cycles_since_filing_without_a_story(tmp_path):
    item = _aged(tmp_path)["BLG-SPEC-10"]
    # v9.0 predates filing; v9.1, v9.2, v9.3 count; the non-release folder is ignored
    assert item["cycles_unseated"] == 3
    assert item["last_seated"] is None


def test_a_seated_cycle_resets_the_count(tmp_path):
    item = _aged(tmp_path)["BLG-SPEC-11"]
    assert item["last_seated"] == "v9.2"
    assert item["cycles_unseated"] == 1


def test_gated_and_undated_items(tmp_path):
    aged = _aged(tmp_path)
    assert aged["BLG-SPEC-12"]["gated"] is True and aged["BLG-SPEC-10"]["gated"] is False
    assert aged["BLG-SPEC-13"]["cycles_unseated"] is None


def test_render_flags_only_ungated_items_at_threshold(tmp_path):
    out = aging.render(list(_aged(tmp_path).values()), threshold=2)
    assert "| BLG-SPEC-10 | 3 ⚠ |" in out
    assert "| BLG-SPEC-12 | 3 |" in out  # gated: not flagged
    assert "| BLG-SPEC-11 | 1 |" in out
    assert "Ungated items at or over it: 1." in out
    assert "Undated (no date on the **Source:** line, not aged): BLG-SPEC-13" in out
    assert out.index("BLG-SPEC-10") < out.index("BLG-SPEC-11")
