"""
ST-03 (BLG-OPS-131, EPIC-01, v8.3): Staging/production API key distinctness check.

Tests the pure comparison logic in scripts/check_api_key_cross_environment.py
directly (no HTTP mocking needed -- evaluate_environment() takes plain status
codes). The deliberately-cross-wired test simulates the exact failure mode
this story exists to catch: a future rotation accidentally re-syncing
staging and production to the same key value (the state ST-06/BLG-SEC-27
fixed and confirmed once, manually, at rotation time).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_api_key_cross_environment import evaluate_environment  # noqa: E402


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
