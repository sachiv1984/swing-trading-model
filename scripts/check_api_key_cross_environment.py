#!/usr/bin/env python3
"""
Staging/Production API Key Distinctness Check (ST-03, BLG-OPS-131, EPIC-01, v8.3).

Confirms staging's `API_KEY` is rejected by production and vice versa, using
a lightweight authenticated GET (`/health/detailed`, requires `X-API-Key` per
`api_key_middleware` in backend/main.py) against both live services.

Background: ST-06 (BLG-SEC-27, v8.2) rotated staging and production to
distinct values and confirmed this live via a one-time manual check at
rotation time. There was no ongoing, automated signal if a future rotation
accidentally re-syncs the two environments -- this script makes that
recurring, following the same pure-comparison-logic pattern as
scripts/check_staging_deploy_drift.py (BLG-OPS-128, v8.2): the cross-wiring
decision itself (`evaluate_environment`) takes plain HTTP status codes and
does no I/O, so it can be unit-tested directly with a deliberately-cross-
wired case, without mocking HTTP calls.

Usage:
    PROD_API_URL=... PROD_API_KEY=... \\
    STAGING_API_URL=... STAGING_API_KEY=... \\
    python3 scripts/check_api_key_cross_environment.py
"""
import os
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

CHECK_PATH = "/health/detailed"


def get_env_config():
    required = [
        "PROD_API_URL", "PROD_API_KEY",
        "STAGING_API_URL", "STAGING_API_KEY",
    ]
    values = {k: os.getenv(k) for k in required}
    missing = [k for k, v in values.items() if not v]
    if missing:
        raise SystemExit(f"Missing required environment variable(s): {', '.join(missing)}")
    return values


def probe(base_url, api_key):
    """Return the HTTP status code from a GET request with the given key.

    Any non-2xx response surfaces as its actual status code (via HTTPError),
    not an exception -- both 200 and 401 are expected, meaningful outcomes
    here, not failures of the probe itself.
    """
    req = Request(
        f"{base_url.rstrip('/')}{CHECK_PATH}",
        headers={"X-API-Key": api_key},
        method="GET",
    )
    try:
        with urlopen(req, timeout=15) as resp:
            return resp.status
    except HTTPError as e:
        return e.code


def evaluate_environment(name, own_key_status, other_key_status):
    """Pure comparison logic -- no I/O.

    Returns (ok: bool, reason: str). An environment is healthy only if its
    own key succeeds (200) AND the other environment's key is rejected
    (401) -- either failing independently is worth distinguishing in the
    reason text for triage.
    """
    if own_key_status != 200:
        return False, (
            f"{name}: own key did not authenticate (HTTP {own_key_status}) — "
            "service may be down, or its own key was rotated without this "
            "check's credentials being updated"
        )
    if other_key_status == 200:
        return False, (
            f"{name}: the OTHER environment's key was ALSO accepted (HTTP 200) — "
            "keys are not distinct (cross-wired)"
        )
    if other_key_status != 401:
        return False, (
            f"{name}: other-environment key check returned unexpected HTTP "
            f"{other_key_status} (expected 401)"
        )
    return True, f"{name}: own key succeeds, other environment's key correctly rejected (401)"


def main():
    config = get_env_config()

    prod_with_prod_key = probe(config["PROD_API_URL"], config["PROD_API_KEY"])
    prod_with_staging_key = probe(config["PROD_API_URL"], config["STAGING_API_KEY"])
    staging_with_staging_key = probe(config["STAGING_API_URL"], config["STAGING_API_KEY"])
    staging_with_prod_key = probe(config["STAGING_API_URL"], config["PROD_API_KEY"])

    prod_ok, prod_reason = evaluate_environment("production", prod_with_prod_key, prod_with_staging_key)
    staging_ok, staging_reason = evaluate_environment("staging", staging_with_staging_key, staging_with_prod_key)

    any_failure = not (prod_ok and staging_ok)
    print(f"[{'OK' if prod_ok else 'CROSS-WIRED'}] {prod_reason}")
    print(f"[{'OK' if staging_ok else 'CROSS-WIRED'}] {staging_reason}")

    if any_failure:
        print("\nAPI key cross-environment check FAILED -- see above.")
        sys.exit(1)
    print("\nBoth environments' keys are confirmed distinct.")
    sys.exit(0)


if __name__ == "__main__":
    main()
