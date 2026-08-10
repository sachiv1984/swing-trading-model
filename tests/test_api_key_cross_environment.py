"""
ST-03 (BLG-OPS-131, EPIC-01, v8.3): Staging/production API key distinctness check.

Tests the pure comparison logic in scripts/check_api_key_cross_environment.py
directly (no HTTP mocking needed -- evaluate_environment() takes plain status
codes). The deliberately-cross-wired test simulates the exact failure mode
this story exists to catch: a future rotation accidentally re-syncing
staging and production to the same key value (the state ST-06/BLG-SEC-27
fixed and confirmed once, manually, at rotation time).

ST-02 (BLG-OPS-134, EPIC-01, v8.5): added probe-error (`None` status) cases.
A live 2026-08-09 scheduled run showed a PROD_API_URL read timeout crashing
the script with an unhandled exception, which the workflow's alert step
could not distinguish from a genuine cross-wired-keys finding -- both
produced a non-zero exit code, so a transient network timeout triggered a
false-positive "keys are cross-wired" Telegram alert. These tests cover the
fix: a probe error must report as a distinct `ok=None` outcome, never as
`ok=False` (which the caller maps to a cross-wiring finding).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_api_key_cross_environment import (  # noqa: E402
    EXIT_CROSS_WIRED,
    EXIT_ERROR,
    EXIT_OK,
    _label,
    evaluate_environment,
)


def test_distinct_keys_pass():
    ok, reason = evaluate_environment("production", own_key_status=200, other_key_status=401)
    assert ok is True
    assert "correctly rejected" in reason


def test_deliberately_cross_wired_keys_fail():
    """Genuinely exercises the failure path this story exists to catch: the
    other environment's key is accepted where it should be rejected."""
    ok, reason = evaluate_environment("production", own_key_status=200, other_key_status=200)
    assert ok is False
    assert "cross-wired" in reason


def test_own_key_rejected_is_a_distinct_failure_reason():
    """Own key failing (e.g. rotated without updating this check) must not
    be confused with a cross-wiring failure in the reported reason."""
    ok, reason = evaluate_environment("staging", own_key_status=401, other_key_status=401)
    assert ok is False
    assert "own key did not authenticate" in reason


def test_unexpected_other_key_status_is_flagged():
    ok, reason = evaluate_environment("production", own_key_status=200, other_key_status=500)
    assert ok is False
    assert "unexpected HTTP 500" in reason


def test_probe_error_on_own_key_is_inconclusive_not_cross_wired():
    """A network/timeout probe failure (None status) must report ok=None,
    never ok=False -- the caller maps False to a cross-wiring finding, and
    a probe error says nothing about whether the keys are cross-wired
    (this is exactly the 2026-08-09 false-positive alert's root cause)."""
    ok, reason = evaluate_environment("production", own_key_status=None, other_key_status=401)
    assert ok is None
    assert "probe error" in reason
    assert "NOT a cross-wiring finding" in reason


def test_probe_error_on_other_key_is_inconclusive_not_cross_wired():
    ok, reason = evaluate_environment("staging", own_key_status=200, other_key_status=None)
    assert ok is None
    assert "probe error" in reason


def test_label_maps_none_to_error_not_ok_or_cross_wired():
    assert _label(True) == "OK"
    assert _label(False) == "CROSS-WIRED"
    assert _label(None) == "ERROR"


def test_exit_codes_are_distinct():
    """The whole fix depends on these three staying distinct integers so the
    workflow's alert steps can route on `exit_code` without ambiguity."""
    assert len({EXIT_OK, EXIT_CROSS_WIRED, EXIT_ERROR}) == 3
