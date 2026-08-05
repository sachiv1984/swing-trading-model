#!/usr/bin/env python3
"""
Staging Deploy Drift Check (ST-07, BLG-OPS-128, EPIC-02, v8.2).

Compares each staging Render service's most recently live-deployed commit
SHA against origin/main's current HEAD. Exits non-zero if any service's
deployed commit differs from HEAD and a grace period since the last push
to main has already elapsed (a very recent push should not immediately
alert while the deploy is still in flight).

Background: this check exists because the staging frontend static site's
Render `branch` config was found pointed at a stale, long-merged exec
branch (fixed 2026-08-04) -- every deploy hook call silently redeployed
the same frozen commit for weeks with no error, no failed CI job, and no
visible signal anywhere. Separately, the staging backend's GitHub<->Render
auto-deploy integration silently stopped delivering new-commit triggers
for ~7 weeks (2026-06-17 to 2026-08-03), self-recovering only when someone
happened to notice and manually re-triggered a deploy. Neither failure
mode produced a CI failure, a log entry, or an alert of any kind -- this
script exists to make that class of silent staleness detectable going
forward instead of only discoverable by chance.

Usage:
    RENDER_PLATFORM_API_KEY=... python3 scripts/check_staging_deploy_drift.py
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError
from urllib.request import Request, urlopen

RENDER_API_BASE = "https://api.render.com/v1"

# Render service IDs for the two staging services (confirmed 2026-08-04 via
# GET https://api.render.com/v1/services against this repo's Render account).
STAGING_SERVICES = {
    "trading-assistant-api-staging": "srv-d6rtdg94tr6s73ce2j6g",
    "trading-assistant-staging": "srv-d6rtdg94tr6s73ce2j60",
}

DEFAULT_GRACE_PERIOD_MINUTES = 15


def get_render_api_key():
    key = os.getenv("RENDER_PLATFORM_API_KEY")
    if not key:
        raise SystemExit(
            "RENDER_PLATFORM_API_KEY not set. This must be a Render platform "
            "management API key (from Render dashboard -> Account Settings -> "
            "API Keys), not the application X-API-Key."
        )
    return key


def get_latest_live_commit(service_id, api_key):
    """Return (commit_sha, commit_created_at_iso) for the most recent live deploy."""
    req = Request(
        f"{RENDER_API_BASE}/services/{service_id}/deploys?limit=5",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    try:
        with urlopen(req, timeout=15) as resp:
            deploys = json.loads(resp.read())
    except HTTPError as e:
        raise RuntimeError(f"Render API error for service {service_id}: HTTP {e.code}") from e

    for item in deploys:
        d = item["deploy"]
        if d.get("status") == "live":
            return d["commit"]["id"], d["commit"]["createdAt"]
    if deploys:
        d = deploys[0]["deploy"]
        return d["commit"]["id"], d["commit"]["createdAt"]
    raise RuntimeError(f"No deploys found for service {service_id}")


def get_main_head(repo_root=None):
    out = subprocess.run(
        ["git", "rev-parse", "origin/main"],
        capture_output=True, text=True, check=True, cwd=repo_root,
    )
    return out.stdout.strip()


def get_main_head_pushed_at(repo_root=None):
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "origin/main"],
        capture_output=True, text=True, check=True, cwd=repo_root,
    )
    return datetime.fromisoformat(out.stdout.strip())


def check_drift(deployed_sha, main_sha, main_pushed_at, grace_period_minutes, now=None):
    """Pure comparison logic, no I/O -- kept separate from the network/git
    calls above so it can be unit tested directly without mocking HTTP or git.

    Returns (drifted: bool, reason: str).
    """
    if deployed_sha == main_sha:
        return False, "up to date"
    now = now or datetime.now(timezone.utc)
    grace_deadline = main_pushed_at + timedelta(minutes=grace_period_minutes)
    if now < grace_deadline:
        return False, (
            f"deployed commit {deployed_sha[:10]} differs from origin/main HEAD "
            f"{main_sha[:10]}, but grace period has not yet elapsed "
            f"(deploy may still be in flight, grace ends {grace_deadline.isoformat()})"
        )
    return True, (
        f"deployed commit {deployed_sha[:10]} does not match origin/main HEAD "
        f"{main_sha[:10]}, and the {grace_period_minutes}-minute grace period "
        f"since the last push to main ({main_pushed_at.isoformat()}) has elapsed"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--grace-period-minutes", type=int, default=DEFAULT_GRACE_PERIOD_MINUTES)
    parser.add_argument("--repo-root", default=None)
    args = parser.parse_args()

    api_key = get_render_api_key()
    main_sha = get_main_head(args.repo_root)
    main_pushed_at = get_main_head_pushed_at(args.repo_root)

    any_drift = False
    for name, service_id in STAGING_SERVICES.items():
        deployed_sha, _deployed_at = get_latest_live_commit(service_id, api_key)
        drifted, reason = check_drift(deployed_sha, main_sha, main_pushed_at, args.grace_period_minutes)
        status = "DRIFT" if drifted else "OK"
        print(f"[{status}] {name}: {reason}")
        if drifted:
            any_drift = True

    if any_drift:
        print("\nStaging deploy drift detected -- see above.")
        sys.exit(1)
    print("\nAll staging services match origin/main HEAD (or are within grace period).")
    sys.exit(0)


if __name__ == "__main__":
    main()
