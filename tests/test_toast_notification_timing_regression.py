"""
Regression coverage for the 9 toast call sites fixed in ST-42 (Toast
Notification Timing standard) -- ST-11, BLG-QA-180, EPIC-03, v9.8.

docs/specs/frontend/design_system.md's Toast Notification Timing standard:
an Error-row toast (no required next action) gets `duration: 8000` (8s or
manual dismiss); the Cmd+K info toast, at ~62 chars (under the 80-char
floor for an extended duration), gets sonner's plain 4s info default with
no override. ST-42 (EPIC-06, v9.5, BLG-FE-175) brought all 9 non-conforming
sites into line. No test asserted on any of the 9 exact call sites
(confirmed via grep at ST-42 time) -- a future edit could silently drop the
duration override (or reintroduce an incorrect one) with nothing failing.

Static source-level checks, consistent with this repo's established
convention for design-system/timing regressions (see sibling
tests/test_motion_timing_500ms_ceiling_regression.py, ST-12): each
assertion locates the exact toast call site by its message text and
confirms the duration option ST-42 put there is still present. A live
Playwright assertion on an 8-second dismiss timer is impractical here (9
sites x 8s+ real wall-clock waits per run) and is not what these
call-site-level regressions need — see this file's own commit for the
disclosure of this choice.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SRC_DIR = REPO_ROOT / "src"


def _read(rel_path: str) -> str:
    return (SRC_DIR / rel_path).read_text()


class TestLayoutCmdKInfoToastHasNoDurationOverride:
    def test_info_toast_has_no_explicit_duration(self):
        source = _read("Layout.js")
        match = re.search(
            r'toast\.info\(\s*"Press ⌘K.*?"\s*,\s*\{([^}]*)\}',
            source,
            re.DOTALL,
        )
        assert match, "Layout.js: Cmd+K info toast call site not found"
        assert "duration" not in match.group(1), (
            "Layout.js: Cmd+K info toast regained a `duration` override -- "
            "at ~62 chars (under the 80-char floor) it must use sonner's plain 4s info default"
        )


class TestErrorToastsCarryDuration8000:
    CASES = [
        ("components/positions/PositionCard.js", "Failed to mark position as reviewed. Please try again."),
        ("hooks/useWatchlistModal.js", "Failed to keep"),
        ("pages/Positions.js", "Failed to update stop. Please try again."),
        ("pages/Positions.js", "Failed to mark position as reviewed. Please try again."),
        ("pages/Settings.js", "Please fix the errors below before saving"),
        ("pages/Settings.js", "Failed to save settings"),
        ("pages/Signals.js", "Failed to add to watchlist"),
        ("pages/Signals.js", "Added to watchlist but failed to update signal status"),
    ]

    def test_all_8_error_toast_sites_have_duration_8000(self):
        missing = []
        for rel_path, needle in self.CASES:
            source = _read(rel_path)
            idx = source.find(needle)
            assert idx != -1, f"{rel_path}: expected error-toast message containing {needle!r} not found"
            # duration: 8000 must appear within the same toast.error(...) call --
            # look within a bounded window after the message text.
            window = source[idx: idx + 200]
            if "duration: 8000" not in window and "duration:8000" not in window:
                missing.append(f"{rel_path}: {needle!r}")
        assert not missing, "Error toast(s) missing `duration: 8000`:\n" + "\n".join(missing)

    def test_each_message_identifies_exactly_one_toast_error_call(self):
        # ST-40 (BLG-QA-200, v9.11): replaces two tautological count tests
        # (len() of this list against a literal). This one reads the source:
        # each message must sit inside exactly one toast.error(...) call, so the
        # duration check above cannot be satisfied by some other call that
        # happens to contain the same text.
        problems = []
        for rel_path, needle in self.CASES:
            source = _read(rel_path)
            calls = [m.start() for m in re.finditer(r"toast\.error\(", source)
                     if needle in source[m.start(): m.start() + 200]]
            if len(calls) != 1:
                problems.append(f"{rel_path}: {needle!r} found in {len(calls)} toast.error() calls")
        assert not problems, "\n".join(problems)
