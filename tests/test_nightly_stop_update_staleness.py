"""
ST-14 (BLG-OPS-166, EPIC-04, v9.6): Nightly trailing-stop update
dead-man's-switch.

Tests the pure comparison logic in
scripts/check_nightly_stop_update_staleness.py directly (no live API call
needed -- is_nightly_stop_update_overdue() takes plain values). This is the
"simulated missed run" AC-01 evidence: a deliberately-stale case exercises
the exact alert path without ever calling the real
POST /positions/nightly-stop-update endpoint, so live stops are never
disturbed (RISK-04). AC-02 ("a successful run clears it") is the mirror
case: a recent, "ok"-status run is not overdue.
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_nightly_stop_update_staleness import (  # noqa: E402
    is_nightly_stop_update_overdue,
    DEFAULT_THRESHOLD_HOURS,
)


def test_recent_successful_run_is_not_overdue():
    """AC-02: a successful run within the window clears the switch."""
    now = datetime.now(timezone.utc)
    overdue, reason = is_nightly_stop_update_overdue(
        last_run_utc=now - timedelta(hours=2),
        last_status="ok",
        now=now,
    )
    assert overdue is False
    assert "within the" in reason


def test_never_run_is_overdue():
    """No trailing_stop run recorded at all (e.g. a genuinely missed run,
    or process just restarted) -- must alert, not silently pass."""
    now = datetime.now(timezone.utc)
    overdue, reason = is_nightly_stop_update_overdue(
        last_run_utc=None, last_status="never_run", now=now
    )
    assert overdue is True
    assert "no trailing_stop run has been recorded" in reason


def test_deliberately_stale_missed_run_is_detected():
    """AC-01: genuinely exercises the failure path this story exists to
    catch -- a run frozen well beyond the 26h window."""
    now = datetime.now(timezone.utc)
    last_run_utc = now - timedelta(hours=50)
    overdue, reason = is_nightly_stop_update_overdue(
        last_run_utc=last_run_utc, last_status="ok", now=now
    )
    assert overdue is True
    assert last_run_utc.isoformat() in reason


def test_most_recent_run_errored_is_overdue_even_within_window():
    """A run that happened recently but failed is "not succeeded" --
    alert immediately, don't wait out the rest of the 26h window."""
    now = datetime.now(timezone.utc)
    overdue, reason = is_nightly_stop_update_overdue(
        last_run_utc=now - timedelta(hours=1), last_status="error", now=now
    )
    assert overdue is True
    assert "did not succeed" in reason
    assert "error" in reason


def test_threshold_boundary_is_inclusive_of_overdue():
    """Exactly at the deadline: overdue (>= comparison, not >)."""
    now = datetime.now(timezone.utc)
    last_run_utc = now - timedelta(hours=DEFAULT_THRESHOLD_HOURS)
    overdue, _ = is_nightly_stop_update_overdue(
        last_run_utc=last_run_utc, last_status="ok", now=now
    )
    assert overdue is True


def test_one_second_before_boundary_is_not_overdue():
    now = datetime.now(timezone.utc)
    last_run_utc = now - timedelta(hours=DEFAULT_THRESHOLD_HOURS) + timedelta(seconds=1)
    overdue, _ = is_nightly_stop_update_overdue(
        last_run_utc=last_run_utc, last_status="ok", now=now
    )
    assert overdue is False


def test_custom_threshold_is_respected():
    now = datetime.now(timezone.utc)
    overdue, _ = is_nightly_stop_update_overdue(
        last_run_utc=now - timedelta(hours=30),
        last_status="ok",
        now=now,
        threshold_hours=24,
    )
    assert overdue is True
