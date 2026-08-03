#!/usr/bin/env python3
"""
Recurring Endpoint Test Coverage Audit (ST-11, EPIC-04, BLG-QA-113,
cycle 2026-08-03__release-v8.1).

Full-repo backstop audit: compares EVERY @router.get/post/put/delete
decorator across all of backend/routers/*.py against backend/routers/test.py's
registered entries, regardless of when each route was added.

This complements — it does not replace — scripts/check_router_test_registration.py
(the pre-commit hook), which only checks routes newly staged in the current
diff. That check has been in place since v7.9 (ST-10, EPIC-10) and prevents
*new* gaps at commit time; it cannot catch a gap that predates the hook, or
one introduced by a commit that bypassed the hook. This script is a periodic
(recommended: pre-sprint-planning) full-state audit intended to catch that
residual class of gap.

Usage:
    python3 scripts/audit_endpoint_test_coverage.py

Exit code 0: every route in backend/routers/*.py has a matching test.py entry.
Exit code 1: one or more routes have no matching entry (printed to stdout).
"""
import re
import sys
from pathlib import Path

ROUTE_DECORATOR_RE = re.compile(
    r'@router\.(get|post|put|delete|patch)\(\s*["\']([^"\']+)["\']'
)
PREFIX_RE = re.compile(r'APIRouter\(\s*prefix\s*=\s*["\']([^"\']*)["\']')
TEST_ENTRY_RE = re.compile(
    r'"name":\s*"(GET|POST|PUT|DELETE|PATCH)\s+([^"]+)"'
)

ROUTERS_DIR = Path("backend/routers")
TEST_PY = ROUTERS_DIR / "test.py"

# Deliberate, documented exclusions — grandfathered per the disposition comment
# block in backend/routers/test.py (ST-11, BLG-QA-133, v7.10) and
# docs/ops/endpoint_test_coverage_audit_2026-07-29.md. These are real-data-mutating
# endpoints (would mutate the live single-portfolio production system's actual
# financial/trading state on every smoke-test run) or otherwise unsuitable for
# this harness's 2xx-only pass criterion — not oversights. New entries must not
# be added here without an equivalent documented rationale in test.py itself.
KNOWN_GAPS = {
    ("POST", "/cash/transaction"),
    ("POST", "/portfolio/position"),
    ("POST", "/portfolio/snapshot"),
    ("POST", "/alerts/rules"),
    ("PATCH", "/alerts/rules/{rule_id}"),
    ("DELETE", "/alerts/rules/{rule_id}"),
    ("POST", "/alerts/evaluate"),
    ("POST", "/settings"),
    ("PATCH", "/settings"),
    ("POST", "/signals/generate"),
    ("POST", "/notifications/mark-all-read"),
    ("PATCH", "/notifications/{notification_id}"),
    ("POST", "/positions/{id}/exit"),
    ("PATCH", "/positions/{id}/mark-reviewed"),
    ("PATCH", "/positions/{id}/note"),
    ("PATCH", "/positions/{id}/tags"),
    ("PATCH", "/watchlist/{entry_id}"),
    ("DELETE", "/signals/{id}"),
    ("GET", "/positions/analyze"),
    ("GET", "/trades/{trade_id}/reflection"),
    ("POST", "/test/endpoints"),
}


def _clean_entry_path(raw_path):
    """Strip a trailing human-readable parenthetical annotation, e.g.
    "/analytics/metrics (all_time)" -> "/analytics/metrics"."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", raw_path).strip()


def parse_test_py_entries(test_py_content):
    return [
        (m.group(1), _clean_entry_path(m.group(2)))
        for m in TEST_ENTRY_RE.finditer(test_py_content)
    ]


def path_pattern(path):
    escaped = re.escape(path)
    escaped = re.sub(r"\\\{[^}]+\\\}", r"[^/]+", escaped)
    return re.compile(f"^{escaped}$")


def is_registered(method, path, test_entries):
    pattern = path_pattern(path)
    for entry_method, entry_path in test_entries:
        if entry_method != method:
            continue
        if pattern.match(entry_path) or path_pattern(entry_path).match(path):
            return True
    return False


def is_known_gap(method, path):
    for gap_method, gap_path in KNOWN_GAPS:
        if gap_method != method:
            continue
        if path_pattern(gap_path).match(path) or path_pattern(path).match(gap_path):
            return True
    return False


def all_router_files():
    return sorted(
        f for f in ROUTERS_DIR.glob("*.py")
        if f.name != "test.py" and f.name != "__init__.py"
    )


def extract_all_routes(router_file_path: Path):
    content = router_file_path.read_text()
    prefix_match = PREFIX_RE.search(content)
    prefix = prefix_match.group(1) if prefix_match else ""

    routes = []
    for line in content.splitlines():
        m = ROUTE_DECORATOR_RE.search(line)
        if not m:
            continue
        method, path = m.group(1).upper(), m.group(2)
        full_path = (prefix.rstrip("/") + "/" + path.lstrip("/")).replace("//", "/")
        if not full_path.startswith("/"):
            full_path = "/" + full_path
        routes.append((method, full_path))
    return routes


def main():
    if not TEST_PY.exists():
        print(f"{TEST_PY} not found", file=sys.stderr)
        return 2

    test_entries = parse_test_py_entries(TEST_PY.read_text())

    missing = []
    known = []
    total = 0
    for router_file in all_router_files():
        for method, path in extract_all_routes(router_file):
            total += 1
            if is_registered(method, path, test_entries):
                continue
            if is_known_gap(method, path):
                known.append((router_file.name, method, path))
            else:
                missing.append((router_file.name, method, path))

    print(f"Scanned {total} route decorator(s) across {len(all_router_files())} router file(s).")
    print(f"{len(known)} route(s) are documented KNOWN_GAPS (deliberate exclusions, see test.py disposition comment).")

    if not missing:
        print("No undocumented gaps — every route is either registered or a documented, deliberate exclusion.")
        return 0

    print(f"{len(missing)} undocumented route(s) with no matching test.py entry and no KNOWN_GAPS exclusion:")
    for fname, method, path in missing:
        print(f"  - {fname}: {method} {path}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
