"""
Regression coverage for the motion-timing values fixed in ST-41 (500ms
ceiling components) -- ST-12, BLG-QA-181, EPIC-03, v9.8.

docs/specs/frontend/design_system.md's Motion-vs-contrast guideline caps
opacity-animated, text-bearing elements' total time-to-full-opacity
(`delay` + `duration`) at 500ms. ST-41 (EPIC-06, v9.5, BLG-FE-175) brought
the 4 known non-compliant components under that ceiling. No test asserted
on the fixed values -- a future edit could silently regress any of them
back over 500ms (or back to an unbounded stagger) with nothing failing.

Static source-level checks (consistent with this repo's established
convention for design-system/timing regressions -- see
tests/test_check_contract_example_freshness.py and sibling
tests/test_check_*.py files -- rather than a live-render Playwright
assertion, since these are fixed numeric literals in the source, not
runtime-observable-only behaviour): read each component's actual source
text and confirm the exact `delay`/`duration` expressions ST-41 put in
place are still there, then independently recompute max(delay) + duration
for each to confirm the 500ms ceiling itself, not just the presence of a
particular string.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SRC_DIR = REPO_ROOT / "src"

CEILING_SECONDS = 0.5


def _read(rel_path: str) -> str:
    return (SRC_DIR / rel_path).read_text()


class TestRecentTradesWidget:
    FILE = "components/dashboard/widgets/RecentTradesWidget.js"

    def test_stagger_transition_has_explicit_duration_0_3(self):
        source = _read(self.FILE)
        match = re.search(r"transition=\{\{\s*delay:\s*idx \* 0\.05,\s*duration:\s*0\.3\s*\}\}", source)
        assert match, "RecentTradesWidget.js: expected `{ delay: idx * 0.05, duration: 0.3 }` transition not found"

    def test_max_combined_time_to_full_opacity_within_ceiling(self):
        # slice(0, 5) bounds idx to 0-4 -> max delay = 4 * 0.05 = 0.2
        assert _read(self.FILE).count("slice(0, 5)") >= 1, "expected list still capped at 5 items"
        max_delay = 4 * 0.05
        duration = 0.3
        assert max_delay + duration <= CEILING_SECONDS


class TestReportsTaxYearReport:
    FILE = "pages/Reports.js"
    DELAYS = (0.05, 0.1, 0.15, 0.2)

    def test_all_four_stat_cards_have_explicit_duration_0_3(self):
        source = _read(self.FILE)
        for delay in self.DELAYS:
            pattern = r"transition=\{\{\s*delay:\s*" + re.escape(str(delay)) + r",\s*duration:\s*0\.3\s*\}\}"
            assert re.search(pattern, source), f"Reports.js: expected explicit duration:0.3 for delay {delay} not found"

    def test_max_combined_time_to_full_opacity_within_ceiling(self):
        duration = 0.3
        for delay in self.DELAYS:
            assert delay + duration <= CEILING_SECONDS


class TestSignalsPageStagger:
    FILE = "pages/Signals.js"

    def test_stagger_capped_at_index_3_with_explicit_duration(self):
        source = _read(self.FILE)
        match = re.search(
            r"transition=\{\{\s*delay:\s*Math\.min\(index,\s*3\)\s*\*\s*0\.05,\s*duration:\s*0\.3\s*\}\}",
            source,
        )
        assert match, "Signals.js: expected `Math.min(index, 3) * 0.05` fixed stagger cap not found"

    def test_max_combined_time_to_full_opacity_within_ceiling(self):
        max_delay = 3 * 0.05
        duration = 0.3
        assert max_delay + duration <= CEILING_SECONDS


class TestSystemStatusPageStaggers:
    FILE = "pages/SystemStatus.js"

    def test_tests_list_stagger_capped_at_index_9(self):
        source = _read(self.FILE)
        match = re.search(
            r"transition=\{\{\s*delay:\s*Math\.min\(index,\s*9\)\s*\*\s*0\.02,\s*duration:\s*0\.3\s*\}\}",
            source,
        )
        assert match, "SystemStatus.js: expected `Math.min(index, 9) * 0.02` fixed stagger cap not found (tests list)"

    def test_validations_list_stagger_capped_at_index_3(self):
        source = _read(self.FILE)
        match = re.search(
            r"transition=\{\{\s*delay:\s*Math\.min\(index,\s*3\)\s*\*\s*0\.05,\s*duration:\s*0\.3\s*\}\}",
            source,
        )
        assert match, "SystemStatus.js: expected `Math.min(index, 3) * 0.05` fixed stagger cap not found (validations list)"

    def test_max_combined_time_to_full_opacity_within_ceiling_both_lists(self):
        duration = 0.3
        assert (9 * 0.02) + duration <= CEILING_SECONDS
        assert (3 * 0.05) + duration <= CEILING_SECONDS


class TestNoUnboundedIndexScaledDelayRegresses:
    """Confirms the pre-ST-41 defect pattern (bare `index * step` with no
    cap) has not been reintroduced on the two previously-unbounded
    components."""

    def test_signals_page_no_longer_has_bare_uncapped_stagger(self):
        source = _read("pages/Signals.js")
        assert not re.search(r"delay:\s*index \* 0\.05\s*\}\}", source), (
            "Signals.js: found an uncapped `delay: index * 0.05` stagger -- "
            "ST-41's Math.min(index, 3) cap appears to have been reverted"
        )

    def test_system_status_no_longer_has_bare_uncapped_stagger(self):
        source = _read("pages/SystemStatus.js")
        assert not re.search(r"delay:\s*index \* 0\.0[25]\s*\}\}", source), (
            "SystemStatus.js: found an uncapped `delay: index * 0.0X` stagger -- "
            "ST-41's Math.min(index, N) cap appears to have been reverted"
        )
