#!/usr/bin/env python3
"""
SI-05 Digest Delivery-Failure Alerting (ST-02, BLG-OPS-130, EPIC-01, v8.3).

Checks the most recent successful send recorded in `si05_digest_log` and
alerts if the digest is overdue beyond the expected weekly cadence plus a
grace period. Exists because the SI-05 digest silently stopped sending for
several weeks (BLG-OPS-129) with no mechanism to catch a similar gap before
the next multi-week effectiveness review -- see
docs/ops/si05_digest_delivery_root_cause_2026-08-05.md.

Follows the same pure-comparison-logic pattern as
scripts/check_staging_deploy_drift.py (BLG-OPS-128, v8.2): the staleness
decision itself (`is_digest_overdue`) takes plain values and does no I/O, so
it can be unit-tested directly with a deliberately-stale case, without
mocking the database.

Usage:
    DATABASE_URL=... python3 scripts/check_si05_digest_staleness.py
"""
import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

import psycopg2

DEFAULT_THRESHOLD_HOURS = 192  # 8 days: weekly cadence (168h) + 24h grace


def _clean_db_url(url: str) -> str:
    """Strip Supabase-specific params not supported by libpq (matches the
    identical helper in backend/services/si05_digest_service.py)."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    params.pop("pgbouncer", None)
    new_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=new_query))


def get_database_url():
    url = os.getenv("DATABASE_URL") or os.getenv("PROD_DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL or PROD_DATABASE_URL must be set.")
    return url


def get_last_sent_at(database_url):
    """Return the UTC timestamp of the most recent successful digest send,
    or None if `si05_digest_log` has no `sent` rows (or does not exist)."""
    conn = psycopg2.connect(_clean_db_url(database_url))
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT MAX(sent_at) FROM si05_digest_log WHERE status = 'sent'"
            )
            row = cur.fetchone()
            return row[0] if row else None
    finally:
        conn.close()


def is_digest_overdue(last_sent_at, now, threshold_hours=DEFAULT_THRESHOLD_HOURS):
    """Pure comparison logic -- no I/O.

    Returns (overdue: bool, reason: str).

    `last_sent_at` of None (no successful send ever recorded) is always
    overdue -- there is no baseline to be within threshold of.
    """
    if last_sent_at is None:
        return True, "no successful SI-05 digest send has ever been recorded"

    deadline = last_sent_at + timedelta(hours=threshold_hours)
    if now >= deadline:
        return True, (
            f"last successful send was {last_sent_at.isoformat()}, "
            f"which exceeds the {threshold_hours}-hour threshold "
            f"(deadline was {deadline.isoformat()})"
        )
    return False, (
        f"last successful send was {last_sent_at.isoformat()}, "
        f"within the {threshold_hours}-hour threshold "
        f"(deadline {deadline.isoformat()})"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--threshold-hours", type=int, default=DEFAULT_THRESHOLD_HOURS)
    args = parser.parse_args()

    database_url = get_database_url()
    last_sent_at = get_last_sent_at(database_url)
    now = datetime.now(timezone.utc)
    overdue, reason = is_digest_overdue(last_sent_at, now, args.threshold_hours)

    status = "OVERDUE" if overdue else "OK"
    print(f"[{status}] SI-05 digest: {reason}")

    if overdue:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
