"""
Unit tests for the canonical position_state / lifecycle_state registry
(ST-07, EPIC-02, v8.3, BLG-BE-67).
"""
from utils.position_lifecycle_states import (
    EXIT_ZONE, PROFITABLE, LOSING, GRACE, UNKNOWN,
    POSITION_LIFECYCLE_STATES,
)


def test_registry_contains_exactly_the_five_known_states():
    assert set(POSITION_LIFECYCLE_STATES) == {"EXIT ZONE", "PROFITABLE", "LOSING", "GRACE", "UNKNOWN"}


def test_named_constants_match_registry_values():
    assert EXIT_ZONE == "EXIT ZONE"
    assert PROFITABLE == "PROFITABLE"
    assert LOSING == "LOSING"
    assert GRACE == "GRACE"
    assert UNKNOWN == "UNKNOWN"
    assert set(POSITION_LIFECYCLE_STATES) == {EXIT_ZONE, PROFITABLE, LOSING, GRACE, UNKNOWN}


def test_no_duplicate_values():
    assert len(POSITION_LIFECYCLE_STATES) == len(set(POSITION_LIFECYCLE_STATES))


def test_compute_position_state_only_ever_returns_registry_values():
    """Cross-check: services.position_lifecycle_service.compute_position_state
    (the canonical state-machine implementation) never returns a value outside
    this registry, across every branch of its logic."""
    from services.position_lifecycle_service import compute_position_state

    base = {"entry_price": 100.0, "current_price": 100.0, "atr": 2.0, "entry_date": "2020-01-01"}

    cases = [
        {},  # missing fields -> UNKNOWN
        {**base, "atr": None},  # no ATR -> UNKNOWN
        {**base, "current_price": 130.0, "initial_stop": 90.0},  # EXIT ZONE
        {**base, "current_price": 105.0},  # PROFITABLE
        {**base, "current_price": 95.0},  # LOSING
        {**base, "current_price": 100.0, "entry_date": "2099-01-01"},  # GRACE (today <= entry)
    ]
    for case in cases:
        assert compute_position_state(case) in POSITION_LIFECYCLE_STATES
