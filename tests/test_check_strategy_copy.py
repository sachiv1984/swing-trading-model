"""
ST-21 (BLG-GOV-369, EPIC-03, v9.12) — scripts/check_strategy_copy.py, the CI
strategy-copy lint.

AC 1: no strategy-number literals in TradeEntry.js, Settings.js, Positions.js
or SignalContextPanel.js outside src/constants/strategy.js.
AC 2: the lint reports zero contradictions on the current tree.
Also pins how the lint reads strategy_rules.md §11 and which text it flags.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_strategy_copy", ROOT / "scripts" / "check_strategy_copy.py")
lint = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = lint  # dataclasses resolve annotations through sys.modules
_spec.loader.exec_module(lint)

PARAMS = lint.Params(grace_days=10, initial_mult=5, profit_mult=2, atr_period=14)


class TestCurrentTree:
    def test_zero_contradictions_and_zero_literals(self):
        params = lint.parse_section_11(lint.RULES.read_text(encoding="utf-8"))
        findings = lint.run(params)
        assert [f.render() for f in findings] == []

    def test_named_pages_exist(self):
        for page in lint.LITERAL_PAGES:
            assert page.exists(), page

    def test_strict_mode_exits_zero_on_clean_tree(self):
        assert lint.main(["--strict"]) == 0


class TestSection11Parsing:
    def test_reads_the_rules_document(self):
        params = lint.parse_section_11(lint.RULES.read_text(encoding="utf-8"))
        assert params == lint.Params(grace_days=10, initial_mult=5, profit_mult=2, atr_period=14)

    def test_follows_a_changed_rule(self):
        text = (
            "## 11. Current production parameters\n\n"
            "- Grace period: 7 days\n- Initial / losing stop multiplier: 4 × ATR\n"
            "- Profitable stop multiplier: 1.5 × ATR\n- ATR period: 20 days\n\n## 12. Parameter governance\n"
        )
        assert lint.parse_section_11(text) == lint.Params(7, 4, 1.5, 20)

    def test_missing_section_fails_loudly(self):
        with pytest.raises(SystemExit):
            lint.parse_section_11("## 10. Something\n## 12. Else\n")


class TestContradictions:
    @pytest.mark.parametrize("line", [
        '"Stop = entry − 3×ATR"',
        '"ATR × 2.5 trailing"',
        "const stop = price - 3 * signal.atr_value;",
        '"20-day ATR"',
        '"ATR (20-day, £)"',
        '"ATR period: 21 days"',
        '"ATR (20d)"',
        '"20d ATR"',
        '"the grace period ends (7 calendar days)"',
        '"a 5-day grace window"',
        "Day {n} of 7",
        '"e.g., 2 = High − 2×ATR"',
    ])
    def test_flags_text_that_disagrees_with_the_rules(self, line):
        assert lint.scan_line(line, PARAMS), line

    @pytest.mark.parametrize("line", [
        '"Stop = price − 5×ATR for new and losing positions (§5, §7.2)."',
        '"ATR × 2.0"',
        "const stop = price - 5 * signal.atr_value;",
        '"14-day ATR"',
        '"ATR (14d)"',
        '"grace period ends (10 calendar days, §6)"',
        "Day {n} of 10",
        "formatPercent(atrPct * 100)",
        '"Price above 200-day MA"',
    ])
    def test_does_not_flag_text_that_matches(self, line):
        assert lint.scan_line(line, PARAMS) == [], line


class TestLiterals:
    @pytest.mark.parametrize("line", [
        '<p>entry − 5×ATR</p>',
        '"ATR (14-day)"',
        '<p>ATR (14d)</p>',
        "Day {dayNumber} of 10",
        "price - 5 * signal.atr_value",
    ])
    def test_literal_strategy_numbers_are_flagged(self, line):
        assert lint.literal_line(lint.INTERPOLATED.sub("", line))

    @pytest.mark.parametrize("line", [
        "<p>entry − {INITIAL_ATR_MULTIPLIER}×ATR</p>",
        "`ATR (${ATR_PERIOD_DAYS}-day)`",
        "<p>ATR ({ATR_PERIOD_DAYS}d)</p>",
        "Day {dayNumber} of {GRACE_PERIOD_DAYS}",
        '"vs 200-day MA"',
    ])
    def test_constants_are_not_flagged(self, line):
        assert not lint.literal_line(lint.INTERPOLATED.sub("", line))


class TestCommentsIgnored:
    def test_line_and_block_comments_are_stripped(self):
        src = 'const a = 1; // entry − 3×ATR\n/* 7-day grace\n still comment */\nconst url = "http://x/3×ATR";\n'
        stripped = lint.strip_comments(src)
        lines = stripped.splitlines()
        assert len(lines) == 4  # line numbers kept
        assert "3×ATR" not in lines[0]
        assert "grace" not in stripped
        assert "http://x/3×ATR" in lines[3]  # a URL in a string is not a comment
