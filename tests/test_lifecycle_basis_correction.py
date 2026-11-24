"""ST-28 (BLG-BE-179, EPIC-05, v9.18): lifecycle transitions caused by the v9.12
currency correction are identifiable.

The v9.12 fix (ST-13, PR #2025, merged 2026-10-13T19:04:30Z) made a US
position's badge compare native with native. On the first recompute after it, an
affected position changed state with no market move. The convention
(data_model.md §Lifecycle Transition Reasons) tags that position's first
post-cut-off transition as "basis_correction", for US positions entered before
the cut-off, unless either side is GRACE (price is ignored in grace) or UNKNOWN.
"""

import pytest

from services.position_lifecycle_service import (
    BASIS_CORRECTION_CUTOFF_UTC,
    REASON_BASIS_CORRECTION,
    basis_correction_history_row_id,
    tag_basis_correction_transitions,
)

BEFORE = "2026-10-12T22:30:00"
AT_CUTOFF = "2026-10-13T19:04:30"
JUST_BEFORE_CUTOFF = "2026-10-13T19:04:29"
AFTER = "2026-10-13T20:15:00"
LATER = "2026-10-20T09:00:00"


def _position(market="US", entry_date="2026-09-15", history=None):
    return {"id": "pos-1", "market": market, "entry_date": entry_date, "state_history": history or []}


def _reasons(history):
    return [h.get("reason") for h in history]


def test_cutoff_is_the_pr_2025_merge_time():
    assert BASIS_CORRECTION_CUTOFF_UTC.isoformat() == "2026-10-13T19:04:30"


# (id, market, entry_date, history, expected reasons per entry)
CASES = [
    ("us-profitable-to-losing-after-cutoff-tagged", "US", "2026-09-15",
     [("GRACE", "2026-09-15T10:00:00"), ("PROFITABLE", "2026-09-25T10:00:00"), ("LOSING", AFTER)],
     [None, None, REASON_BASIS_CORRECTION]),
    ("us-exactly-at-cutoff-tagged", "US", "2026-09-15",
     [("GRACE", "2026-09-15T10:00:00"), ("PROFITABLE", "2026-09-25T10:00:00"), ("EXIT ZONE", AT_CUTOFF)],
     [None, None, REASON_BASIS_CORRECTION]),
    ("us-one-second-before-cutoff-not-tagged", "US", "2026-09-15",
     [("GRACE", "2026-09-15T10:00:00"), ("PROFITABLE", "2026-09-25T10:00:00"), ("LOSING", JUST_BEFORE_CUTOFF)],
     [None, None, None]),
    ("us-only-first-post-cutoff-transition-tagged", "US", "2026-09-15",
     [("GRACE", "2026-09-15T10:00:00"), ("PROFITABLE", BEFORE), ("LOSING", AFTER), ("PROFITABLE", LATER)],
     [None, None, REASON_BASIS_CORRECTION, None]),
    ("uk-never-tagged", "UK", "2026-09-15",
     [("GRACE", "2026-09-15T10:00:00"), ("PROFITABLE", "2026-09-25T10:00:00"), ("LOSING", AFTER)],
     [None, None, None]),
    ("us-entered-on-cutoff-day-not-tagged", "US", "2026-10-13",
     [("GRACE", "2026-10-13T08:00:00"), ("PROFITABLE", AFTER)],
     [None, None]),
    ("us-grace-ending-after-cutoff-not-tagged", "US", "2026-10-05",
     [("GRACE", "2026-10-05T10:00:00"), ("LOSING", "2026-10-15T09:00:00"), ("PROFITABLE", LATER)],
     [None, None, None]),
    ("us-to-unknown-after-cutoff-not-tagged", "US", "2026-09-15",
     [("GRACE", "2026-09-15T10:00:00"), ("PROFITABLE", "2026-09-25T10:00:00"), ("UNKNOWN", AFTER), ("LOSING", LATER)],
     [None, None, None, None]),
    ("us-seed-only-after-cutoff-not-tagged", "US", "2026-09-15",
     [("LOSING", AFTER)],
     [None]),
    ("us-empty-history", "US", "2026-09-15", [], []),
    ("us-tz-aware-string-tagged", "US", "2026-09-15",
     [("GRACE", "2026-09-15T10:00:00+00:00"), ("PROFITABLE", "2026-09-25T10:00:00+00:00"), ("LOSING", "2026-10-13T20:15:00+01:00")],
     [None, None, REASON_BASIS_CORRECTION]),
    ("us-tz-aware-string-before-cutoff-in-utc-not-tagged", "US", "2026-09-15",
     [("GRACE", "2026-09-15T10:00:00+00:00"), ("PROFITABLE", "2026-09-25T10:00:00+00:00"), ("LOSING", "2026-10-13T20:00:00+01:00")],
     [None, None, None]),
    ("us-missing-entry-date-not-tagged", "US", None,
     [("GRACE", "2026-09-15T10:00:00"), ("PROFITABLE", "2026-09-25T10:00:00"), ("LOSING", AFTER)],
     [None, None, None]),
]


@pytest.mark.parametrize("market,entry_date,history,expected",
                         [c[1:] for c in CASES], ids=[c[0] for c in CASES])
def test_state_history_tagging(market, entry_date, history, expected):
    position = _position(market, entry_date, [{"state": s, "entered_at": t} for s, t in history])
    tagged = tag_basis_correction_transitions(position)
    assert _reasons(tagged) == expected
    # A copy: the stored history is not changed.
    assert all("reason" not in h for h in position["state_history"])


def test_state_history_stored_as_json_text():
    import json
    history = [{"state": "GRACE", "entered_at": "2026-09-15T10:00:00"},
               {"state": "PROFITABLE", "entered_at": "2026-09-25T10:00:00"},
               {"state": "LOSING", "entered_at": AFTER}]
    position = _position(history=json.dumps(history))
    assert _reasons(tag_basis_correction_transitions(position)) == [None, None, REASON_BASIS_CORRECTION]


def test_position_state_history_rows_in_any_order():
    position = _position()
    rows = [
        {"id": "r3", "from_state": "LOSING", "to_state": "PROFITABLE", "entered_at": LATER},
        {"id": "r1", "from_state": None, "to_state": "GRACE", "entered_at": "2026-09-15T10:00:00"},
        {"id": "r2", "from_state": "PROFITABLE", "to_state": "LOSING", "entered_at": AFTER},
        {"id": "r0", "from_state": "GRACE", "to_state": "PROFITABLE", "entered_at": "2026-09-25T10:00:00"},
    ]
    assert basis_correction_history_row_id(position, rows) == "r2"


def test_position_state_history_first_seen_row_after_cutoff_is_not_a_transition():
    # A position first recorded in the table after the cut-off (from_state NULL).
    rows = [{"id": "r1", "from_state": None, "to_state": "LOSING", "entered_at": AFTER},
            {"id": "r2", "from_state": "LOSING", "to_state": "PROFITABLE", "entered_at": LATER}]
    assert basis_correction_history_row_id(_position(), rows) is None


def test_position_state_history_uk_rows_none():
    rows = [{"id": "r2", "from_state": "PROFITABLE", "to_state": "LOSING", "entered_at": AFTER}]
    assert basis_correction_history_row_id(_position(market="UK"), rows) is None
