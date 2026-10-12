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
particular string. From v9.11 (ST-40, BLG-QA-200) the ceiling tests read
every delay, cap, list bound and duration from the source; before that they
restated them as literals.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SRC_DIR = REPO_ROOT / "src"

CEILING_SECONDS = 0.5

# ST-40 (BLG-QA-200, EPIC-06, v9.11): the ceiling tests below used to restate
# the delay/duration values as Python literals, so they passed whatever the
# component said. They now read every number from the source.
_NUM = r"(\d+(?:\.\d+)?)"


def _read(rel_path: str) -> str:
    return (SRC_DIR / rel_path).read_text()


def _transitions(source: str):
    """Every `transition={{ delay: <expr>, duration: <n> }}` in the source, as
    (delay_expression, duration_seconds)."""
    return [
        (m.group(1).strip(), float(m.group(2)))
        for m in re.finditer(r"transition=\{\{\s*delay:\s*((?:[^,(){}]|\([^)]*\))+?),\s*duration:\s*" + _NUM + r"\s*\}\}", source)
    ]


def _max_delay(expr: str, index_bound: int = None) -> float:
    """Largest value a stagger delay expression can take: a literal, a capped
    `Math.min(index, K) * step`, or `idx * step` with the list bounded to
    `index_bound` items (the caller reads that bound from the source)."""
    m = re.fullmatch(_NUM, expr)
    if m:
        return float(m.group(1))
    m = re.fullmatch(r"Math\.min\(\s*\w+,\s*(\d+)\s*\)\s*\*\s*" + _NUM, expr)
    if m:
        return int(m.group(1)) * float(m.group(2))
    m = re.fullmatch(r"\w+\s*\*\s*" + _NUM, expr)
    if m and index_bound is not None:
        return (index_bound - 1) * float(m.group(1))
    raise AssertionError(f"unbounded or unrecognised delay expression: {expr!r}")


class TestRecentTradesWidget:
    FILE = "components/dashboard/widgets/RecentTradesWidget.js"

    def test_stagger_transition_has_explicit_duration_0_3(self):
        source = _read(self.FILE)
        match = re.search(r"transition=\{\{\s*delay:\s*idx \* 0\.05,\s*duration:\s*0\.3\s*\}\}", source)
        assert match, "RecentTradesWidget.js: expected `{ delay: idx * 0.05, duration: 0.3 }` transition not found"

    def test_max_combined_time_to_full_opacity_within_ceiling(self):
        source = _read(self.FILE)
        bound = re.search(r"\.slice\(0,\s*(\d+)\)", source)
        assert bound, "expected the trades list to be capped by .slice(0, N)"
        transitions = [t for t in _transitions(source) if "idx" in t[0]]
        assert transitions, "stagger transition not found"
        for expr, duration in transitions:
            assert _max_delay(expr, int(bound.group(1))) + duration <= CEILING_SECONDS


class TestReportsTaxYearReport:
    FILE = "pages/Reports.js"
    DELAYS = (0.05, 0.1, 0.15, 0.2)

    def test_all_four_stat_cards_have_explicit_duration_0_3(self):
        source = _read(self.FILE)
        for delay in self.DELAYS:
            pattern = r"transition=\{\{\s*delay:\s*" + re.escape(str(delay)) + r",\s*duration:\s*0\.3\s*\}\}"
            assert re.search(pattern, source), f"Reports.js: expected explicit duration:0.3 for delay {delay} not found"

    def test_max_combined_time_to_full_opacity_within_ceiling(self):
        transitions = [t for t in _transitions(_read(self.FILE)) if re.fullmatch(_NUM, t[0])]
        assert len(transitions) >= len(self.DELAYS), "stat-card transitions not found"
        for expr, duration in transitions:
            assert _max_delay(expr) + duration <= CEILING_SECONDS, f"Reports.js: delay {expr} + {duration} > 0.5s"


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
        transitions = [t for t in _transitions(_read(self.FILE)) if "index" in t[0]]
        assert transitions, "Signals.js: stagger transition not found"
        for expr, duration in transitions:
            assert _max_delay(expr) + duration <= CEILING_SECONDS, f"Signals.js: {expr} + {duration} > 0.5s"


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
        transitions = [t for t in _transitions(_read(self.FILE)) if "index" in t[0]]
        assert len(transitions) >= 2, "SystemStatus.js: both stagger transitions expected"
        for expr, duration in transitions:
            assert _max_delay(expr) + duration <= CEILING_SECONDS, f"SystemStatus.js: {expr} + {duration} > 0.5s"


class TestCeilingHelpers:
    """The helpers the ceiling tests rely on reject the defect shapes."""

    def test_uncapped_index_stagger_is_rejected(self):
        import pytest
        with pytest.raises(AssertionError, match="unbounded"):
            _max_delay("index * 0.05")

    def test_values_are_read_not_assumed(self):
        assert _transitions("transition={{ delay: Math.min(index, 3) * 0.05, duration: 0.45 }}") == [
            ("Math.min(index, 3) * 0.05", 0.45)
        ]
        assert _max_delay("Math.min(index, 3) * 0.05") + 0.45 > CEILING_SECONDS


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
