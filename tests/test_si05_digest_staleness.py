"""
ST-02 (BLG-OPS-130, EPIC-01, v8.3): SI-05 digest delivery-failure alerting.

Tests the pure comparison logic in scripts/check_si05_digest_staleness.py
directly (no database mocking needed -- is_digest_overdue() takes plain
values). The deliberately-stale test simulates the exact failure mode this
story exists to catch: a digest that stopped sending weeks ago with nothing
noticing until the next multi-week effectiveness review (BLG-OPS-129).
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_si05_digest_staleness import is_digest_overdue, DEFAULT_THRESHOLD_HOURS  # noqa: E402


def test_recent_send_is_not_overdue():
    now = datetime.now(timezone.utc)
    overdue, reason = is_digest_overdue(
        last_sent_at=now - timedelta(days=2),
        now=now,
    )
    assert overdue is False
    assert "within the" in reason


def test_never_sent_is_overdue():
    """No row in si05_digest_log at all -- must alert, not silently pass."""
    now = datetime.now(timezone.utc)
    overdue, reason = is_digest_overdue(last_sent_at=None, now=now)
    assert overdue is True
    assert "no successful SI-05 digest send" in reason


def test_deliberately_stale_send_is_detected():
    """Genuinely exercises the failure path this story exists to catch: a
    digest frozen at a send from weeks ago (matches the real ~7-week gap
    found live in BLG-OPS-129) while the threshold has long since elapsed."""
    now = datetime.now(timezone.utc)
    last_sent_at = now - timedelta(days=49)  # matches the real ~7-week gap
    overdue, reason = is_digest_overdue(last_sent_at=last_sent_at, now=now)
    assert overdue is True
    assert last_sent_at.isoformat() in reason


def test_threshold_boundary_is_inclusive_of_overdue():
    """Exactly at the deadline: overdue (>= comparison, not >)."""
    now = datetime.now(timezone.utc)
    last_sent_at = now - timedelta(hours=DEFAULT_THRESHOLD_HOURS)
    overdue, _ = is_digest_overdue(last_sent_at=last_sent_at, now=now)
    assert overdue is True


def test_one_second_before_boundary_is_not_overdue():
    now = datetime.now(timezone.utc)
    last_sent_at = now - timedelta(hours=DEFAULT_THRESHOLD_HOURS) + timedelta(seconds=1)
    overdue, _ = is_digest_overdue(last_sent_at=last_sent_at, now=now)
    assert overdue is False


def test_custom_threshold_is_respected():
    now = datetime.now(timezone.utc)
    overdue, _ = is_digest_overdue(
        last_sent_at=now - timedelta(hours=30),
        now=now,
        threshold_hours=24,
    )
    assert overdue is True
