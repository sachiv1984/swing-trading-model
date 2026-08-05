"""
ST-07 (BLG-OPS-128, EPIC-02, v8.2): Staging deploy drift detection.

Tests the pure comparison logic in scripts/check_staging_deploy_drift.py
directly (no network/git mocking needed -- check_drift() takes plain
values). The deliberately-stale test simulates the exact failure mode
found live during this story: a deployed commit that stopped advancing
weeks ago while origin/main kept moving.
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_staging_deploy_drift import check_drift  # noqa: E402

MAIN_SHA = "bfe43e959af9ec041a5ac287448bfc791afc4ded"
STALE_SHA = "3d6d7d7babaa32b9278a1e20a8b24944352e0833"


def test_matching_sha_is_not_drift():
    drifted, reason = check_drift(
        deployed_sha=MAIN_SHA,
        main_sha=MAIN_SHA,
        main_pushed_at=datetime.now(timezone.utc) - timedelta(minutes=5),
        grace_period_minutes=15,
    )
    assert drifted is False
    assert reason == "up to date"


def test_recent_mismatch_within_grace_period_is_not_drift():
    """A deploy that hasn't caught up yet, seconds after a push, should not
    alert -- the drift check must distinguish 'still deploying' from
    'silently stuck'."""
    now = datetime.now(timezone.utc)
    drifted, reason = check_drift(
        deployed_sha=STALE_SHA,
        main_sha=MAIN_SHA,
        main_pushed_at=now - timedelta(minutes=2),
        grace_period_minutes=15,
        now=now,
    )
    assert drifted is False
    assert "grace period" in reason


def test_deliberately_stale_deploy_is_detected():
    """Genuinely exercises the failure path this story exists to catch:
    a deploy frozen at an old commit (the real trading-assistant-staging
    static site was found stuck on this exact commit, 3d6d7d7b, for
    weeks -- see scripts/check_staging_deploy_drift.py's module docstring)
    while origin/main has long since moved past the grace period."""
    now = datetime.now(timezone.utc)
    main_pushed_at = now - timedelta(days=49)  # matches the real ~7-week gap found live
    drifted, reason = check_drift(
        deployed_sha=STALE_SHA,
        main_sha=MAIN_SHA,
        main_pushed_at=main_pushed_at,
        grace_period_minutes=15,
        now=now,
    )
    assert drifted is True
    assert STALE_SHA[:10] in reason
    assert MAIN_SHA[:10] in reason


def test_grace_period_boundary_is_exclusive_of_drift():
    """One second before the grace deadline: not yet drift."""
    now = datetime.now(timezone.utc)
    main_pushed_at = now - timedelta(minutes=15) + timedelta(seconds=1)
    drifted, _ = check_drift(
        deployed_sha=STALE_SHA,
        main_sha=MAIN_SHA,
        main_pushed_at=main_pushed_at,
        grace_period_minutes=15,
        now=now,
    )
    assert drifted is False


def test_grace_period_boundary_is_inclusive_of_drift_after_deadline():
    """One second after the grace deadline: now flagged as drift."""
    now = datetime.now(timezone.utc)
    main_pushed_at = now - timedelta(minutes=15) - timedelta(seconds=1)
    drifted, _ = check_drift(
        deployed_sha=STALE_SHA,
        main_sha=MAIN_SHA,
        main_pushed_at=main_pushed_at,
        grace_period_minutes=15,
        now=now,
    )
    assert drifted is True
