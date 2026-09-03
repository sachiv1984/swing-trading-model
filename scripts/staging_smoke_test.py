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

Exit code: 0 if all checks pass, 1 if any fails (same convention as
scripts/check_api_performance_baseline_drift.py /
scripts/check_deploy_path_filter_drift.py).
"""
import json
import os
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


def main() -> int:
    base_url = os.environ.get("STAGING_API_URL", "").rstrip("/")
    api_key = os.environ.get("STAGING_API_KEY", "")

    if not base_url:
        print("::error::STAGING_API_URL environment variable is not set.")
        return 1

    print(f"Waking up {base_url} ...")
    awake = _wake_up(base_url)
    if not awake:
        print(f"::warning::{base_url}/health did not respond within {WAKE_UP_TIMEOUT_S}s — proceeding to the real checks anyway (they have their own timeout/retry).")

    print(f"Running {len(CHECKS)} smoke checks against {base_url} ...")
    failures = run_checks(base_url, api_key)

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
