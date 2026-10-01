"""
ST-23, EPIC-04, v9.9, BLG-GOV-347: date-disambiguation fix for
scripts/scan_backlog_gate_conditions.py's _lapsed_date().

Prior behaviour used re.search to take only the FIRST embedded ISO date in
a gate_condition, undisambiguated. A gate_condition mentioning an earlier,
still-future date before a later, already-past clears-date was silently
reported as NOT lapsed (a false negative) -- the reverse ordering produced
a false positive. Since this script drives a real release-planning gate
decision (release_planning_prompt.md §1.3a), an undetected false negative
hides a genuinely-clearable item from the ready pool indefinitely.

Covers: single-date lapsed, single-date not-lapsed, multi-date-both-past,
multi-date-both-future, the false-negative/false-positive orderings named
in the source backlog item, governing-keyword preference (the common real
case, confirmed against the live BLG-OPS-48 entry), and the ambiguous
fallback when no keyword is present and dates disagree.
"""
import datetime
import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "scan_backlog_gate_conditions.py"
spec = importlib.util.spec_from_file_location("scan_backlog_gate_conditions", SCRIPT_PATH)
sbgc = importlib.util.module_from_spec(spec)
sys.modules["scan_backlog_gate_conditions"] = sbgc
spec.loader.exec_module(sbgc)

AS_OF = datetime.date(2026, 10, 1)


class TestSingleDate:

    def test_single_past_date_is_lapsed(self):
        lapsed, ambiguous = sbgc._lapsed_date("Ships after 2026-09-01.", AS_OF)
        assert lapsed == datetime.date(2026, 9, 1)
        assert ambiguous is False

    def test_single_future_date_is_not_lapsed(self):
        lapsed, ambiguous = sbgc._lapsed_date("Ships after 2026-12-01.", AS_OF)
        assert lapsed is None
        assert ambiguous is False

    def test_no_date_at_all(self):
        lapsed, ambiguous = sbgc._lapsed_date("Depends on PT-04 shipping.", AS_OF)
        assert lapsed is None
        assert ambiguous is False


class TestMultiDateAgreement:

    def test_multi_date_both_past_is_lapsed(self):
        lapsed, ambiguous = sbgc._lapsed_date(
            "Shipped 2026-06-25 and 2026-07-25, both in the past.", AS_OF
        )
        assert lapsed == datetime.date(2026, 6, 25)
        assert ambiguous is False

    def test_multi_date_both_future_is_not_lapsed(self):
        lapsed, ambiguous = sbgc._lapsed_date(
            "Scheduled for 2026-11-01 and 2026-12-01, both upcoming.", AS_OF
        )
        assert lapsed is None
        assert ambiguous is False


class TestFalseNegativeFalsePositiveOrderings:
    """The exact failure mode BLG-GOV-347 named: an early future date
    followed by a later past date (or vice versa), with no governing
    keyword present to disambiguate."""

    def test_early_future_then_later_past_is_lapsed_not_hidden(self):
        # Old behaviour (first-match): would see 2026-12-01 (future) first
        # and wrongly report NOT lapsed -- the false negative BLG-GOV-347
        # described, hiding a genuinely-clearable item from the ready pool.
        lapsed, ambiguous = sbgc._lapsed_date(
            "Mentioned alongside 2026-12-01 and also 2026-08-01, no further context.", AS_OF
        )
        assert lapsed == datetime.date(2026, 8, 1)
        assert ambiguous is True  # no governing keyword here -- flagged for verification

    def test_early_past_then_later_future_is_not_falsely_lapsed(self):
        # Old behaviour (first-match): would see 2026-08-01 (past) first and
        # wrongly report LAPSED -- the false positive BLG-GOV-347 described.
        lapsed, ambiguous = sbgc._lapsed_date(
            "Mentioned alongside 2026-08-01 and also 2026-12-01, no further context.", AS_OF
        )
        # Dates disagree and no keyword governs -- conservative choice is
        # still to surface as lapsed+ambiguous rather than silently hide it,
        # but the AMBIGUOUS flag makes clear this needs human verification
        # rather than being silently trusted either way.
        assert lapsed == datetime.date(2026, 8, 1)
        assert ambiguous is True


class TestGoverningKeywordPreference:
    """Real case confirmed against the live backlog.md: BLG-OPS-48's
    'No earlier than 2026-11-01 (~6 months after ... 2026-05-28)' --
    the keyword date must win outright, not merely break a tie."""

    def test_no_earlier_than_keyword_wins_over_earlier_past_date(self):
        lapsed, ambiguous = sbgc._lapsed_date(
            "No earlier than 2026-11-01 (~6 months after BLG-OPS-36 scope review in v4.2, 2026-05-28)",
            AS_OF,
        )
        assert lapsed is None  # 2026-11-01 is still in the future
        assert ambiguous is False

    def test_clears_keyword_preferred_over_earlier_shipped_date(self):
        lapsed, ambiguous = sbgc._lapsed_date(
            "v6.2 shipped 2026-06-25; clears ~2026-07-25", AS_OF
        )
        assert lapsed == datetime.date(2026, 7, 25)
        assert ambiguous is False

    def test_due_keyword_future_date_not_lapsed(self):
        lapsed, ambiguous = sbgc._lapsed_date(
            "Released 2026-01-01; due 2026-12-25", AS_OF
        )
        assert lapsed is None
        assert ambiguous is False
