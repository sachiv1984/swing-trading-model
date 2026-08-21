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

Usage:
    RENDER_PLATFORM_API_KEY=... python3 scripts/wait_for_staging_deploy_live.py <target_sha>
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_staging_deploy_drift import get_latest_live_commit, get_render_api_key, STAGING_SERVICES  # noqa: E402

POLL_INTERVAL_S = 15
TIMEOUT_S = 480  # 8 minutes — generous for a Render free-tier build+deploy

BACKEND_SERVICE_ID = STAGING_SERVICES["trading-assistant-api-staging"]


def wait_for_live(target_sha: str, api_key: str, timeout_s: int = TIMEOUT_S, poll_interval_s: int = POLL_INTERVAL_S) -> bool:
    deadline = time.time() + timeout_s
    last_seen_sha = None
    while time.time() < deadline:
        try:
            deployed_sha, _ = get_latest_live_commit(BACKEND_SERVICE_ID, api_key)
        except RuntimeError as e:
            print(f"  (Render API check failed, retrying: {e})")
            time.sleep(poll_interval_s)
            continue
        last_seen_sha = deployed_sha
        if deployed_sha == target_sha:
            print(f"Confirmed: staging backend's live deploy matches target commit {target_sha[:10]}.")
            return True
        print(f"  Not yet live: staging backend's live deploy is {deployed_sha[:10]}, waiting for {target_sha[:10]}...")
        time.sleep(poll_interval_s)

    print(
        f"::error::Timed out after {timeout_s}s waiting for staging backend to deploy "
        f"{target_sha[:10]} (last seen live commit: "
        f"{last_seen_sha[:10] if last_seen_sha else 'unknown'}). Not running the smoke "
        f"test suite against an unconfirmed deploy — see module docstring for why a "
        f"timeout here is a hard failure, not a soft proceed-anyway."
    )
    return False


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: wait_for_staging_deploy_live.py <target_sha>", file=sys.stderr)
        return 2
    target_sha = sys.argv[1]
    api_key = get_render_api_key()
    return 0 if wait_for_live(target_sha, api_key) else 1


if __name__ == "__main__":
    sys.exit(main())
