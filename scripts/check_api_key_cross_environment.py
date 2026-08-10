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
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

CHECK_PATH = "/health/detailed"

# Exit codes -- distinct on purpose (ST-02, BLG-OPS-134, v8.5). A live run's
# log (2026-08-09 scheduled run) showed the daily job genuinely executing
# (secrets ARE configured -- the missing-secrets skip-guard is not silently
# masking this), but a PROD_API_URL read timeout inside probe() propagated
# as an unhandled exception. The workflow's alert step only checked
# exit_code == 1 (the same code used for a genuine cross-wired-keys
# finding), so the crash's implicit exit code produced a false-positive
# "API key cross-environment check FAILED" Telegram alert with no
# [CROSS-WIRED] finding to back it up -- a transient network timeout was
# indistinguishable, at the alert layer, from an actual security incident.
EXIT_OK = 0
EXIT_CROSS_WIRED = 1
EXIT_ERROR = 2  # probe/config failure -- inconclusive, NOT a cross-wiring finding


def get_env_config():
    required = [
        "PROD_API_URL", "PROD_API_KEY",
        "STAGING_API_URL", "STAGING_API_KEY",
    ]
    values = {k: os.getenv(k) for k in required}
    missing = [k for k, v in values.items() if not v]
    if missing:
        print(f"[ERROR] Missing required environment variable(s): {', '.join(missing)}")
        sys.exit(EXIT_ERROR)
    return values


def probe(base_url, api_key):
    """Return the HTTP status code from a GET request with the given key,
    or None if the probe itself failed (network/timeout/TLS/DNS error)
    rather than producing a meaningful HTTP status.

    Any non-2xx HTTP response surfaces as its actual status code (via
    HTTPError), not an exception -- both 200 and 401 are expected,
    meaningful outcomes here, not failures of the probe itself. A
    network-level failure is different in kind from either: it says
    nothing about whether the keys are cross-wired, so it must not be
    conflated with a genuine finding (previously it crashed the script
    entirely -- see EXIT_ERROR comment above).
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
    except (URLError, OSError) as e:
        print(f"[ERROR] probe of {base_url.rstrip('/')}{CHECK_PATH} failed: {e}")
        return None


def evaluate_environment(name, own_key_status, other_key_status):
    """Pure comparison logic -- no I/O.

    Returns (ok: bool | None, reason: str). `ok` is None when a probe
    errored (own_key_status or other_key_status is None) -- distinct from
    both True (confirmed distinct) and False (confirmed cross-wired or
    otherwise unhealthy), so the caller can report and exit differently
    for "inconclusive" than for "genuine finding".
    """
    if own_key_status is None or other_key_status is None:
        return None, (
            f"{name}: probe error -- could not determine key status "
            "(network/timeout failure; see [ERROR] output above). This is "
            "NOT a cross-wiring finding."
        )
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


def _label(ok):
    if ok is None:
        return "ERROR"
    return "OK" if ok else "CROSS-WIRED"


def main():
    config = get_env_config()

    prod_with_prod_key = probe(config["PROD_API_URL"], config["PROD_API_KEY"])
    prod_with_staging_key = probe(config["PROD_API_URL"], config["STAGING_API_KEY"])
    staging_with_staging_key = probe(config["STAGING_API_URL"], config["STAGING_API_KEY"])
    staging_with_prod_key = probe(config["STAGING_API_URL"], config["PROD_API_KEY"])

    prod_ok, prod_reason = evaluate_environment("production", prod_with_prod_key, prod_with_staging_key)
    staging_ok, staging_reason = evaluate_environment("staging", staging_with_staging_key, staging_with_prod_key)

    print(f"[{_label(prod_ok)}] {prod_reason}")
    print(f"[{_label(staging_ok)}] {staging_reason}")

    if prod_ok is None or staging_ok is None:
        print("\nAPI key cross-environment check could not complete (probe error) -- inconclusive, not a security finding.")
        sys.exit(EXIT_ERROR)
    if not (prod_ok and staging_ok):
        print("\nAPI key cross-environment check FAILED -- see above.")
        sys.exit(EXIT_CROSS_WIRED)
    print("\nBoth environments' keys are confirmed distinct.")
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
