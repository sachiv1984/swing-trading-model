"""
ST-13 (BLG-QA-182, EPIC-03, v9.8): confirms the escaped-defect/follow-on
ratio tracker's v9.5 baseline row is present, internally consistent, and
matches the source cycle's own recorded execution/closure data -- so a
future edit to the tracker (or a stale copy-paste of the wrong cycle's
numbers into a new row) is caught rather than silently trusted.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TRACKER = REPO_ROOT / "docs" / "testing" / "escaped_defect_and_follow_on_ratio_tracker.md"
V95_EXECUTION_STATE = REPO_ROOT / "claude/cycles/2026-09-15__release-v9.5/execution_state.json"
V95_CLOSURE_RECORD = REPO_ROOT / "claude/cycles/2026-09-15__release-v9.5/closure_record.md"


def _table_row(cycle_id: str) -> list:
    text = TRACKER.read_text()
    for line in text.splitlines():
        if line.startswith("|") and cycle_id in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            return cells
    raise AssertionError(f"No table row found for {cycle_id!r} in {TRACKER}")


class TestTrackerFileStructure:
    def test_tracker_file_exists(self):
        assert TRACKER.exists()

    def test_table_has_expected_columns(self):
        text = TRACKER.read_text()
        assert "| Cycle | Shipped Stories | Follow-on Items Filed | Follow-on Ratio | Escaped Defects | Notes |" in text


class TestV95Baseline:
    def test_shipped_story_count_matches_execution_state(self):
        data = json.loads(V95_EXECUTION_STATE.read_text())
        done_count = sum(
            1
            for epic in data.get("epics", {}).values()
            for story in epic.get("stories", {}).values()
            if story.get("status") in ("done", "merged")
        )
        row = _table_row("2026-09-15__release-v9.5")
        assert int(row[1]) == done_count == 43

    def test_follow_on_count_matches_closure_record(self):
        closure_text = V95_CLOSURE_RECORD.read_text()
        match = re.search(r"(\d+)\s+Phase 4 follow-on items", closure_text)
        assert match, "closure_record.md: expected a 'N Phase 4 follow-on items' count not found"
        row = _table_row("2026-09-15__release-v9.5")
        assert int(row[2]) == int(match.group(1)) == 21

    def test_follow_on_ratio_is_correctly_computed(self):
        row = _table_row("2026-09-15__release-v9.5")
        shipped, filed, ratio = int(row[1]), int(row[2]), float(row[3])
        assert round(filed / shipped, 2) == ratio == 0.49

    def test_escaped_defect_count_matches_zero_dev_deviations(self):
        closure_text = V95_CLOSURE_RECORD.read_text()
        assert "0 formal `DEV-*` deviations filed this cycle" in closure_text
        row = _table_row("2026-09-15__release-v9.5")
        assert int(row[4]) == 0
