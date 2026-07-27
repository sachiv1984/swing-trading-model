#!/usr/bin/env python3
"""
API Performance Baseline Drift Check (ST-12, EPIC-03; enforced pre-PR step
added v3.60, OA-2 post-ship closure 2026-07-24__release-v7.8).

Flags endpoints present in docs/reference/openapi.yaml that are not yet
reflected in docs/ops/api_performance_baseline.md. This is the same check
CI runs at PR-open time as the "API Performance Baseline Drift Detection
(ST-12)" job in .github/workflows/quality_gate.yml — this script is the
canonical implementation; the workflow calls it directly rather than
duplicating the logic inline.

Why this exists as a script and not a prose instruction: execution_prompt.md
§3.2.B previously told the agent to run an ad hoc `grep -c` per new endpoint
before opening a PR. That prose advisory failed to prevent the same class of
miss twice (v7.6/EPIC-07, v7.8/EPIC-06) — a manual grep is easy to skip or
get the pattern wrong on under multi-file endpoint-addition load. A single
script with a hard pass/fail exit code removes that judgment call.

Path parameters are normalised to {id} before comparison (openapi.yaml uses
semantic names like {position_id}/{trade_id}; the baseline doc uses a
generic {id} placeholder throughout) to avoid false positives.

KNOWN_GAPS grandfathers pre-existing endpoints that predate the v6.8 gate.
New entries must not be added to this list; they must be measured and added
to api_performance_baseline.md instead (BLG-OPS-61 tracks closing the
pre-existing gap list itself).

Usage:
    python3 scripts/check_api_performance_baseline_drift.py

Exit code 0: no drift. Exit code 1: one or more endpoints in openapi.yaml
are missing from the performance baseline doc (printed to stdout).
"""
import re
import sys
from pathlib import Path

import yaml

OPENAPI_PATH = Path("docs/reference/openapi.yaml")
BASELINE_PATH = Path("docs/ops/api_performance_baseline.md")
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}

# Pre-existing gaps as of v6.8 (ST-12) — grandfathered, not to be added to
# going forward. Tracked for closure under BLG-OPS-61.
KNOWN_GAPS = {
    "DELETE /watchlist/{id}",
    "GET /analytics/market-correlation",
    "GET /analytics/metrics",
    "GET /analytics/tag-performance",
    "GET /news/{id}",
    "GET /positions/analyze",
    "GET /positions/grace-period-alerts",
    "GET /positions/tags",
    "GET /positions/{id}",
    "GET /positions/{id}/stop-trail",
    "PATCH /watchlist/{id}",
    "POST /alerts/rules",
    "POST /positions/nightly-stop-update",
    "POST /positions/risk-off-alerts",
    "POST /positions/{id}/refresh-state",
    "POST /settings",
    "POST /signals/rebalance-exit",
}


def find_missing_endpoints(openapi_path: Path, baseline_path: Path) -> list[str]:
    spec = yaml.safe_load(openapi_path.read_text())
    paths = spec.get("paths", {}) or {}

    endpoints = set()
    for path, methods in paths.items():
        norm_path = re.sub(r"\{[^}]+\}", "{id}", path)
        for method in methods or {}:
            if method.lower() in HTTP_METHODS:
                endpoints.add(f"{method.upper()} {norm_path}")

    baseline_text = baseline_path.read_text()
    return sorted(e for e in endpoints if e not in baseline_text and e not in KNOWN_GAPS)


if __name__ == "__main__":
    if not OPENAPI_PATH.is_file():
        print(f"ERROR: {OPENAPI_PATH} not found.")
        sys.exit(1)
    if not BASELINE_PATH.is_file():
        print(f"ERROR: {BASELINE_PATH} not found.")
        sys.exit(1)

    missing = find_missing_endpoints(OPENAPI_PATH, BASELINE_PATH)

    if missing:
        print("MERGE BLOCKED: endpoint(s) in openapi.yaml not reflected in "
              "docs/ops/api_performance_baseline.md:")
        for m in missing:
            print(f"  - {m}")
        print("")
        print("Add a baseline measurement row (or an 'Endpoints Not Measured' "
              "/ 'Pending Baseline Measurement' entry) for each endpoint "
              "above, following the most recent '## N. vX.Y Endpoint "
              "Registration' section's pattern, before opening the PR.")
        sys.exit(1)

    print("API Performance Baseline Drift Check: PASSED — no new drift detected.")
    sys.exit(0)
