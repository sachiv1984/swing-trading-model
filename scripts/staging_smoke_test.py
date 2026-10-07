#!/usr/bin/env python3
"""
Staging environment smoke test suite.

ST-13 (BLG-OPS-25, EPIC-03, v9.0). Exercises a minimum set of critical,
read-only endpoints against the staging API to confirm the service is
actually up and correctly serving real responses after a deploy — not
just that Render's deploy hook accepted the trigger
(`.github/workflows/staging-deploy.yml` only confirms that much today).

Endpoints covered (4, above the story's minimum of 3), chosen to exercise
distinct subsystems so a failure narrows down where the problem is:
- GET /health          — basic process liveness, no auth, no DB
- GET /positions       — DB-backed read (Supabase connectivity)
- GET /market/status   — external market-data dependent read
- GET /portfolio       — core financial calculation read

All four are read-only GETs — this suite never writes to staging data,
safe to run on every deploy and on an independent schedule
(.github/workflows/staging-smoke-test.yml) without side effects.

Optionally, when EXPECTED_COMMIT_SHA is set, also runs a stale-deploy check
(ST-17, BLG-OPS-169, EPIC-04, v9.8): confirms GET /health/detailed's
deployed_commit_sha matches it, catching a merge to main that should have
redeployed staging but did not. See check_deployed_commit()'s docstring for
this check's documented known limits.

ST-18 (BLG-OPS-171, EPIC-04, v9.10): the comparison target is the latest
commit at or before EXPECTED_COMMIT_SHA that touches a staging-deploy path
(staging-deploy.yml's on.push.paths), not main's tip. A commit outside those
paths never redeploys staging, so comparing against the tip reported every
governance-only commit as a stale deploy. Staging running a descendant of
the target (e.g. after a manual staging-deploy.yml dispatch) also counts as
current.

Exit code: 0 if all checks pass, 1 if any fails (same convention as
scripts/check_api_performance_baseline_drift.py /
scripts/check_deploy_path_filter_drift.py).
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

# Render free-tier services spin down after inactivity and take ~30-60s to
# cold-start on the next request (same constraint class as
# daily-snapshot.yml's "Wake up API" step, which this mirrors). A fresh
# deploy is a colder start than an idle-spin-down wake, and this workflow
# has no Render deploy-status API access to poll for "deploy actually
# finished" — WAKE_UP_TIMEOUT_S is a generous fixed budget for both effects
# combined, not a precise wait. Documented tradeoff, not an oversight.
WAKE_UP_TIMEOUT_S = 90
WAKE_UP_RETRY_INTERVAL_S = 10

CHECKS = [
    {"method": "GET", "path": "/health", "requires_auth": False, "critical": True},
    {"method": "GET", "path": "/positions", "requires_auth": True, "critical": True},
    {"method": "GET", "path": "/market/status", "requires_auth": True, "critical": True},
    {"method": "GET", "path": "/portfolio", "requires_auth": True, "critical": True},
]


def _request(url: str, api_key: str = None, timeout: int = 30):
    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
        return resp.status, body


def _wake_up(base_url: str) -> bool:
    """Best-effort wake-up ping against /health (no auth required), same
    idiom as daily-snapshot.yml's 'Wake up API' step. Never raises —
    a failed wake-up ping isn't itself a smoke-test failure, the real
    checks below are."""
    deadline = time.time() + WAKE_UP_TIMEOUT_S
    while time.time() < deadline:
        try:
            status, _ = _request(f"{base_url}/health", timeout=15)
            if status == 200:
                return True
        except (urllib.error.URLError, OSError, TimeoutError):
            pass
        time.sleep(WAKE_UP_RETRY_INTERVAL_S)
    return False


def run_checks(base_url: str, api_key: str) -> list:
    """Returns a list of failure description strings — empty if all checks pass."""
    failures = []
    for check in CHECKS:
        url = f"{base_url}{check['path']}"
        key = api_key if check["requires_auth"] else None
        try:
            status, body = _request(url, api_key=key, timeout=30)
        except urllib.error.HTTPError as e:
            failures.append(f"{check['method']} {check['path']}: HTTP {e.code} — {e.read()[:200]}")
            continue
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            failures.append(f"{check['method']} {check['path']}: request failed — {e}")
            continue

        if status != 200:
            failures.append(f"{check['method']} {check['path']}: expected HTTP 200, got {status}")
            continue

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            failures.append(f"{check['method']} {check['path']}: response is not valid JSON")
            continue

        # Minimal shape check — every endpoint in this app returns either a
        # bare list/dict, the {"status": "ok", "data": ...} envelope
        # (backend_engineering_patterns_owner.md §7), or — for /health
        # specifically — its own domain-specific {"status": "ok"|"error",
        # "db": ..., ...} summary (a different, coincidentally-same-named
        # field, not the generic error envelope). Both cases mean the same
        # thing for a smoke test's purposes: parsed["status"] == "error"
        # is a genuine failure either way (a real API error, or /health
        # correctly reporting a broken subsystem such as an unreachable
        # DB) — dry-run verified against a real locally-running instance
        # with a genuinely broken DB schema, where /health correctly
        # returned {"status": "error", "db": "error", ...}.
        if isinstance(parsed, dict) and parsed.get("status") == "error":
            detail = parsed.get("message") or {k: v for k, v in parsed.items() if k != "status"}
            failures.append(f"{check['method']} {check['path']}: HTTP 200 but status=error — {detail}")

    return failures


def _git(*args: str):
    """Run a git command; return (returncode, stdout), or (None, "") if git
    itself can't run (no git binary, not a checkout)."""
    try:
        r = subprocess.run(["git", *args], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None, ""
    return r.returncode, r.stdout.strip()


def latest_deploy_commit(ref: str) -> str:
    """Return the latest commit at or before `ref` that touches a
    staging-deploy path, or `ref` itself if that can't be worked out
    (no git history, unparseable workflow). Falling back to `ref` keeps the
    old, stricter behaviour rather than silently skipping the check."""
    try:
        from check_deploy_path_filter_drift import _parse_staging_filter_paths
        paths = _parse_staging_filter_paths()
    except Exception:  # noqa: BLE001 -- any failure means "fall back to ref"
        return ref
    if not paths:
        return ref
    rc, out = _git("log", "-1", "--format=%H", ref, "--", *paths)
    return out if rc == 0 and out else ref


def _is_ancestor(ancestor: str, descendant: str):
    """True/False from `git merge-base --is-ancestor`; None if git can't tell
    (e.g. the deployed commit isn't in this checkout's history)."""
    rc, _ = _git("merge-base", "--is-ancestor", ancestor, descendant)
    return {0: True, 1: False}.get(rc)


def check_deployed_commit(base_url: str, api_key: str, expected_sha: str) -> str:
    """Compare GET /health/detailed's deployed_commit_sha (ST-17, BLG-OPS-169,
    EPIC-04, v9.8) against expected_sha (the merged commit on `main` this run
    checked out). Returns a failure description string, or "" if the deploy
    is current or the comparison can't be made (see known limits below).

    This is a *stale-staging* check, not a smoke check: it doesn't test
    whether staging is healthy, only whether it is running what was merged.
    It intentionally treats any divergence the same way regardless of
    whether the missed commit changed a startup-applied schema or not --
    the check has no way to inspect *which* commits changed schema, so it
    can't narrow the alert to schema-bearing changes specifically. This is
    the documented, known limit of what's verifiable from the repo alone
    (see docs/ops/staging_deploy_notes.md #7): treating every divergence as
    worth alerting on is the conservative choice, and by construction it
    always covers the schema-bearing case too.

    A missing/null deployed_commit_sha (e.g. an older staging deploy that
    predates this field) is reported as a warning-shaped message prefixed
    "known limit:" rather than a stale-deploy failure -- can't tell staleness
    apart from "field not populated yet" without more information than this
    check has.
    """
    try:
        status, body = _request(f"{base_url}/health/detailed", api_key=api_key, timeout=30)
    except (urllib.error.HTTPError, urllib.error.URLError, OSError, TimeoutError) as e:
        return f"GET /health/detailed: could not check deployed commit — request failed: {e}"

    if status != 200:
        return f"GET /health/detailed: could not check deployed commit — expected HTTP 200, got {status}"

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return "GET /health/detailed: could not check deployed commit — response is not valid JSON"

    deployed_sha = parsed.get("deployed_commit_sha")
    if not deployed_sha:
        return (
            "known limit: GET /health/detailed did not report a deployed_commit_sha "
            "(null/missing) -- cannot confirm staging is running the merged commit"
        )

    if deployed_sha != expected_sha and not _is_ancestor(expected_sha, deployed_sha):
        return (
            f"STALE STAGING DEPLOY: staging is running commit {deployed_sha!r} but "
            f"the latest staging-deploying commit is {expected_sha!r} -- a merge did not "
            f"redeploy staging (or the deploy has not completed yet)"
        )

    return ""


def main() -> int:
    base_url = os.environ.get("STAGING_API_URL", "").rstrip("/")
    api_key = os.environ.get("STAGING_API_KEY", "")
    expected_commit_sha = os.environ.get("EXPECTED_COMMIT_SHA", "").strip()

    if not base_url:
        print("::error::STAGING_API_URL environment variable is not set.")
        return 1

    print(f"Waking up {base_url} ...")
    awake = _wake_up(base_url)
    if not awake:
        print(f"::warning::{base_url}/health did not respond within {WAKE_UP_TIMEOUT_S}s — proceeding to the real checks anyway (they have their own timeout/retry).")

    print(f"Running {len(CHECKS)} smoke checks against {base_url} ...")
    failures = run_checks(base_url, api_key)

    if expected_commit_sha:
        main_tip = expected_commit_sha
        expected_commit_sha = latest_deploy_commit(main_tip)
        if expected_commit_sha != main_tip:
            print(f"{main_tip} does not touch a staging-deploy path; "
                  f"comparing against the latest commit before it that does.")
        print(f"Checking staging's deployed commit against {expected_commit_sha} ...")
        deploy_check_result = check_deployed_commit(base_url, api_key, expected_commit_sha)
        if deploy_check_result:
            if deploy_check_result.startswith("known limit:"):
                print(f"::warning::{deploy_check_result}")
            else:
                failures.append(deploy_check_result)
        else:
            print(f"  ✓ staging is running the latest merged commit ({expected_commit_sha})")

    if failures:
        print("::error::Staging smoke test FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1

    for check in CHECKS:
        print(f"  ✓ {check['method']} {check['path']}")
    print(f"\nAll {len(CHECKS)} staging smoke checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
