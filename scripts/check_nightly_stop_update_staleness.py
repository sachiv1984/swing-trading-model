#!/usr/bin/env python3
"""
Nightly Trailing-Stop Update Dead-Man's-Switch (ST-14, BLG-OPS-166, EPIC-04, v9.6).

Alerts when the nightly trailing-stop update job (the `trailing_stop` entry
in `GET /health/scheduler`) has not succeeded within a threshold window
(default 26 hours -- the job runs once daily at 22:30 UTC per
.github/workflows/nightly-stop-update.yml; 26h gives a ~3.5h grace period
over the 24h cadence). Read-only: this script only ever queries
GET /health/scheduler, it never calls POST /positions/nightly-stop-update
itself, so it cannot disturb live stops (RISK-04).

Follows the same pure-comparison-logic pattern as
scripts/check_si05_digest_staleness.py (BLG-OPS-130, v8.3): the staleness
decision itself (`is_nightly_stop_update_overdue`) takes plain values and
does no I/O, so ST-14's AC-01 ("a simulated missed run raises the alert
within the window") is satisfied by a deliberately-stale unit test case
(tests/test_nightly_stop_update_staleness.py), not by exercising the live
workflow or disturbing a real position's stop.

Known limitation (disclosed, not solved -- inherited from
GET /health/scheduler's own documented caveat, see
docs/specs/api_contracts/health_endpoints.md #GET /health/scheduler): job
status is tracked in-memory and resets on process restart. A
`last_status: "never_run"` shortly after a Render deploy is expected, not a
genuine missed run, and this script has no deploy-timestamp signal to tell
the two cases apart -- it will alert in that window. Accepted for this
S-effort story; a persisted per-run log (the si05_digest_log pattern) would
resolve this but is out of scope here.

Usage:
    API_URL=... API_KEY=... python3 scripts/check_nightly_stop_update_staleness.py
"""
import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

import requests

DEFAULT_THRESHOLD_HOURS = 26  # daily job (22:30 UTC) + ~3.5h grace over the 24h cadence


def get_scheduler_health(api_url, api_key, timeout=30):
    """Fetch GET /health/scheduler from the live API. Read-only -- never
    calls the trailing-stop update endpoint itself (RISK-04)."""
    resp = requests.get(
        f"{api_url.rstrip('/')}/health/scheduler",
        headers={"X-API-Key": api_key},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def is_nightly_stop_update_overdue(last_run_utc, last_status, now, threshold_hours=DEFAULT_THRESHOLD_HOURS):
    """Pure comparison logic -- no I/O.

    Returns (overdue: bool, reason: str).

    `last_run_utc` of None (no run recorded since the last deploy/restart --
    this also covers a genuinely missed run) is always overdue -- there is
    no baseline to be within threshold of.

    A most-recent run whose own status is not "ok" counts as "not
    succeeded" immediately, even if within the threshold window: the last
    recorded attempt is the only success signal this endpoint tracks, so a
    failed attempt means no success is currently on record.
    """
    if last_run_utc is None:
        return True, "no trailing_stop run has been recorded since the last deploy/restart"

    if last_status != "ok":
        return True, (
            f"most recent trailing_stop run ({last_run_utc.isoformat()}) did not succeed "
            f"(last_status={last_status!r})"
        )

    deadline = last_run_utc + timedelta(hours=threshold_hours)
    if now >= deadline:
        return True, (
            f"last successful trailing_stop run was {last_run_utc.isoformat()}, "
            f"which exceeds the {threshold_hours}-hour threshold (deadline was {deadline.isoformat()})"
        )
    return False, (
        f"last successful trailing_stop run was {last_run_utc.isoformat()}, "
        f"within the {threshold_hours}-hour threshold (deadline {deadline.isoformat()})"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--threshold-hours", type=int, default=DEFAULT_THRESHOLD_HOURS)
    args = parser.parse_args()

    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")
    if not api_url or not api_key:
        raise SystemExit("API_URL and API_KEY must be set.")

    health = get_scheduler_health(api_url, api_key)
    job = health.get("jobs", {}).get("trailing_stop", {})
    last_run_raw = job.get("last_run_utc")
    last_status = job.get("last_status", "never_run")
    last_run_utc = datetime.fromisoformat(last_run_raw) if last_run_raw else None
    now = datetime.now(timezone.utc)

    overdue, reason = is_nightly_stop_update_overdue(last_run_utc, last_status, now, args.threshold_hours)

    status = "OVERDUE" if overdue else "OK"
    print(f"[{status}] nightly trailing_stop update: {reason}")

    if overdue:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
