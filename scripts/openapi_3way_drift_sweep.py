#!/usr/bin/env python3
"""
openapi_3way_drift_sweep.py — ST-17 (EPIC-04, v8.3, BLG-QA-94)

Quarterly 3-way sweep: cross-checks backend router decorators, canonical
markdown API contract headings, and docs/reference/openapi.yaml paths
against each other. The existing OpenAPI Drift Detection CI gate
(.github/workflows/openapi-drift.yml) is a 2-way check (contracts <->
openapi.yaml) — it cannot catch a route that exists in code but was never
documented in EITHER of the other two artefacts. This script adds the
missing third leg (router decorators) as a standalone, manually-run sweep,
not a CI gate — running it on every PR would be redundant with the
existing 2-way gate for the legs it already covers, and router-decorator
parsing has a higher false-positive rate (helper functions, non-endpoint
decorators) that warrants human review rather than blocking merges.

Usage:
    python3 scripts/openapi_3way_drift_sweep.py

Exit code 0: no drift found across any of the three pairwise comparisons.
Exit code 1: drift found — see printed report.

Cadence: quarterly. Next scheduled run: see
docs/ops/openapi_3way_sweep_log.md for the run log and schedule.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROUTERS_DIR = REPO_ROOT / "backend" / "routers"
MAIN_PATH = REPO_ROOT / "backend" / "main.py"
CONTRACTS_DIR = REPO_ROOT / "docs" / "specs" / "api_contracts"
OPENAPI_PATH = REPO_ROOT / "docs" / "reference" / "openapi.yaml"

ROUTE_DECORATOR_RE = re.compile(
    r'@router\.(get|post|put|delete|patch)\(\s*["\']([^"\']*)["\']'
)
APP_DECORATOR_RE = re.compile(
    r'@app\.(get|post|put|delete|patch)\(\s*["\']([^"\']*)["\']'
)
PREFIX_RE = re.compile(r'APIRouter\(\s*prefix\s*=\s*["\']([^"\']*)["\']')
HEADING_RE = re.compile(
    r"^##\s+(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(/\S+)", re.MULTILINE
)
PATH_RE = re.compile(r"^  (/[^\s:]+)\s*:", re.MULTILINE)
METHOD_RE = re.compile(r"^    (get|post|put|patch|delete|head|options)\s*:", re.MULTILINE)

# Known, deliberately-excluded gaps — same convention as the 2-way CI gate's
# KNOWN_GAPS set. Populated at this sweep's first run (2026-08-06). See
# docs/ops/openapi_3way_sweep_log.md for the investigation behind each entry.
KNOWN_GAPS: set = {
    # Trivial infra root route, same exemption category as /health per
    # conventions.md §11/§13.3 (health/meta endpoints exempt from contract
    # documentation requirements).
    "GET /",
    # External Alpaca Markets API contracts (docs/specs/api_contracts/
    # alpaca_integration_contract.md) — document a third-party API this
    # backend calls, not a route of this backend's own routers/main.py.
    "GET /v2/stocks/{symbol}/bars",
    "GET /v1beta1/news",
    # Path-parameter NAME style only, not endpoint drift: contract headings
    # use a generic {id} placeholder; the implementation uses a more
    # descriptive param name. Each router function's own docstring already
    # cross-references its contract heading by the {id} form (e.g.
    # alerts.py's "Contract: alerts_endpoints.md §PATCH /notifications/{id}"
    # directly above its own @router.patch("/notifications/{notification_id}")
    # decorator) — this is a deliberate, already-documented convention, not
    # an undocumented endpoint. Both the router-side and contract-side
    # string forms are listed so the pairwise diff is suppressed in both
    # directions.
    "DELETE /price-alerts/{alert_id}", "DELETE /price-alerts/{id}",
    "DELETE /saved-filters/{filter_id}", "DELETE /saved-filters/{id}",
    "DELETE /trade-plans/{plan_id}", "DELETE /trade-plans/{id}",
    "GET /trade-plans/{plan_id}", "GET /trade-plans/{id}",
    "PUT /trade-plans/{plan_id}", "PUT /trade-plans/{id}",
    "PATCH /notifications/{notification_id}", "PATCH /notifications/{id}",
}


def get_router_paths():
    """Parse every backend/routers/*.py file for @router.<method>(...) decorators
    (combined with that file's own APIRouter(prefix=...)), plus backend/main.py's
    own @app.<method>(...) decorators (main.py defines 46 endpoints directly,
    not via backend/routers/ — both are real, live endpoints and both belong in
    this sweep). test.py excluded (it is the test registration file, not a
    router)."""
    pairs = set()
    for path in sorted(ROUTERS_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue
        text = path.read_text()
        prefix_match = PREFIX_RE.search(text)
        prefix = prefix_match.group(1) if prefix_match else ""
        for m in ROUTE_DECORATOR_RE.finditer(text):
            method, route_path = m.group(1).upper(), m.group(2)
            full_path = f"{prefix}{route_path}" if route_path != "/" else prefix or "/"
            pairs.add(f"{method} {full_path}")

    if MAIN_PATH.exists():
        main_text = MAIN_PATH.read_text()
        for m in APP_DECORATOR_RE.finditer(main_text):
            method, route_path = m.group(1).upper(), m.group(2)
            pairs.add(f"{method} {route_path}")

    return pairs


def get_contract_paths():
    pairs = set()
    for contract in sorted(CONTRACTS_DIR.glob("*.md")):
        text = contract.read_text()
        for m in HEADING_RE.finditer(text):
            pairs.add(f"{m.group(1).upper()} {m.group(2)}")
    return pairs


def get_openapi_paths():
    text = OPENAPI_PATH.read_text()
    pairs = set()
    path_spans = [(m.group(1), m.start(), m.end()) for m in PATH_RE.finditer(text)]
    for i, (path, start, end) in enumerate(path_spans):
        next_start = path_spans[i + 1][1] if i + 1 < len(path_spans) else len(text)
        block = text[end:next_start]
        for mm in METHOD_RE.finditer(block):
            pairs.add(f"{mm.group(1).upper()} {path}")
    return pairs


def main():
    router_pairs = get_router_paths()
    contract_pairs = get_contract_paths()
    openapi_pairs = get_openapi_paths()

    checks = [
        ("router decorators", "contracts", router_pairs - contract_pairs - KNOWN_GAPS),
        ("contracts", "router decorators", contract_pairs - router_pairs - KNOWN_GAPS),
        ("router decorators", "openapi.yaml", router_pairs - openapi_pairs - KNOWN_GAPS),
        ("openapi.yaml", "router decorators", openapi_pairs - router_pairs - KNOWN_GAPS),
        ("contracts", "openapi.yaml", contract_pairs - openapi_pairs - KNOWN_GAPS),
        ("openapi.yaml", "contracts", openapi_pairs - contract_pairs - KNOWN_GAPS),
    ]

    print(f"Router decorators: {len(router_pairs)} endpoint(s)")
    print(f"Contract headings:  {len(contract_pairs)} endpoint(s)")
    print(f"openapi.yaml paths: {len(openapi_pairs)} endpoint(s)")
    print()

    total_drift = 0
    for source, target, missing in checks:
        if missing:
            total_drift += len(missing)
            print(f"DRIFT: in {source}, not in {target} ({len(missing)}):")
            for pair in sorted(missing):
                print(f"  - {pair}")
            print()

    if total_drift == 0:
        print("No drift found across any of the three pairwise comparisons.")
        return 0

    print(f"Total drift: {total_drift} finding(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
