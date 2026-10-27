#!/usr/bin/env python3
"""
Wait for the staging backend service's live deploy to match a target commit.

ST-13 (BLG-OPS-25, EPIC-03, v9.0). staging-deploy.yml triggers a deploy via
Render's deploy hook, but the hook's 200/201 response only confirms Render
*accepted* the trigger — not that the build finished or the new commit is
actually live. This polls the same Render platform API endpoint
scripts/check_staging_deploy_drift.py already uses
(GET /v1/services/{id}/deploys), reusing its get_latest_live_commit()
helper, until the staging backend's most recent live deploy's commit
matches the target SHA — or a bounded timeout is reached.

Correction (post-review, ST-13): an earlier version of this workflow used
a fixed `sleep 120` here instead of an actual deploy-status poll, based on
an incorrect module-docstring assumption that no Render platform API
access existed in this repo. Agent-mediated Infrastructure & Operations
Owner review caught this — RENDER_PLATFORM_API_KEY is already provisioned
and used by check_staging_deploy_drift.py/staging-deploy-drift-check.yml
against the exact same two staging services. Fixed to poll for real
confirmation instead.

Exit code: 0 if the target commit is confirmed live within the timeout;
1 otherwise (timeout, or the Render API key is unset). A timeout is a
hard failure, not a soft warning-and-proceed — running the smoke test
suite against an unconfirmed deploy risks it silently passing against
the still-running *previous* deploy (a false "staging ready" signal),
which is exactly the failure class this story exists to prevent.

ST-29 (BLG-OPS-189, EPIC-05, v9.13): staging-deploy.yml now deploys both
staging services and waits on each, so the service is an argument
(--service, default the backend) and --deploy-id, the ID
scripts/trigger_staging_deploy.py got back from that service's hook, makes
the wait follow that exact deploy: it fails at once if the deploy ends in a
failed or cancelled state instead of running out the timeout.

Usage:
    RENDER_PLATFORM_API_KEY=... python3 scripts/wait_for_staging_deploy_live.py <target_sha> \
        [--service trading-assistant-api-staging|trading-assistant-staging] [--deploy-id dep-...]
"""
import argparse
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_staging_deploy_drift import RENDER_API_BASE, get_latest_live_commit, get_render_api_key, STAGING_SERVICES  # noqa: E402

POLL_INTERVAL_S = 15
TIMEOUT_S = 480  # 8 minutes — generous for a Render free-tier build+deploy

BACKEND_SERVICE_NAME = "trading-assistant-api-staging"
BACKEND_SERVICE_ID = STAGING_SERVICES[BACKEND_SERVICE_NAME]

# Render deploy statuses after which the deploy will never go live.
FAILED_STATUSES = {"build_failed", "update_failed", "pre_deploy_failed", "canceled", "deactivated"}


def get_deploy(service_id: str, deploy_id: str, api_key: str):
    """Return (status, commit_sha) for one deploy of one service."""
    req = Request(
        f"{RENDER_API_BASE}/services/{service_id}/deploys/{deploy_id}",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    try:
        with urlopen(req, timeout=15) as resp:
            d = json.loads(resp.read())
    except HTTPError as e:
        raise RuntimeError(f"Render API error for deploy {deploy_id} on {service_id}: HTTP {e.code}") from e
    d = d.get("deploy", d)
    return d.get("status"), (d.get("commit") or {}).get("id")


def wait_for_deploy(target_sha: str, api_key: str, service_id: str, deploy_id: str,
                    timeout_s: int = TIMEOUT_S, poll_interval_s: int = POLL_INTERVAL_S) -> bool:
    """Follow one deploy until it is live on target_sha (True), ends in a
    failed state or goes live on another commit (False), or times out (False)."""
    deadline = time.time() + timeout_s
    last_status = None
    while time.time() < deadline:
        try:
            status, commit_sha = get_deploy(service_id, deploy_id, api_key)
        except RuntimeError as e:
            print(f"  (Render API check failed, retrying: {e})")
            time.sleep(poll_interval_s)
            continue
        last_status = status
        if status == "live":
            if commit_sha == target_sha:
                print(f"Confirmed: {service_id} deploy {deploy_id} is live on {target_sha[:10]}.")
                return True
            print(f"::error::{service_id} deploy {deploy_id} went live on {str(commit_sha)[:10]}, not {target_sha[:10]}.")
            return False
        if status in FAILED_STATUSES:
            print(f"::error::{service_id} deploy {deploy_id} ended as {status}; it will not go live.")
            return False
        print(f"  {service_id} deploy {deploy_id} is {status}, waiting for live on {target_sha[:10]}...")
        time.sleep(poll_interval_s)
    print(f"::error::Timed out after {timeout_s}s waiting for {service_id} deploy {deploy_id} "
          f"(last status: {last_status or 'unknown'}).")
    return False


def wait_for_live(target_sha: str, api_key: str, timeout_s: int = TIMEOUT_S, poll_interval_s: int = POLL_INTERVAL_S,
                  service_id: str = BACKEND_SERVICE_ID) -> bool:
    deadline = time.time() + timeout_s
    last_seen_sha = None
    while time.time() < deadline:
        try:
            deployed_sha, _ = get_latest_live_commit(service_id, api_key)
        except RuntimeError as e:
            print(f"  (Render API check failed, retrying: {e})")
            time.sleep(poll_interval_s)
            continue
        last_seen_sha = deployed_sha
        if deployed_sha == target_sha:
            print(f"Confirmed: {service_id}'s live deploy matches target commit {target_sha[:10]}.")
            return True
        print(f"  Not yet live: {service_id}'s live deploy is {deployed_sha[:10]}, waiting for {target_sha[:10]}...")
        time.sleep(poll_interval_s)

    print(
        f"::error::Timed out after {timeout_s}s waiting for {service_id} to deploy "
        f"{target_sha[:10]} (last seen live commit: "
        f"{last_seen_sha[:10] if last_seen_sha else 'unknown'}). Not running the smoke "
        f"test suite against an unconfirmed deploy — see module docstring for why a "
        f"timeout here is a hard failure, not a soft proceed-anyway."
    )
    return False


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("target_sha")
    parser.add_argument("--service", choices=sorted(STAGING_SERVICES), default=BACKEND_SERVICE_NAME)
    parser.add_argument("--deploy-id", default="")
    try:
        args = parser.parse_args(sys.argv[1:])
    except SystemExit:
        print("Usage: wait_for_staging_deploy_live.py <target_sha> [--service NAME] [--deploy-id ID]", file=sys.stderr)
        return 2
    api_key = get_render_api_key()
    service_id = STAGING_SERVICES[args.service]
    if args.deploy_id:
        ok = wait_for_deploy(args.target_sha, api_key, service_id, args.deploy_id)
    else:
        ok = wait_for_live(args.target_sha, api_key, service_id=service_id)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
