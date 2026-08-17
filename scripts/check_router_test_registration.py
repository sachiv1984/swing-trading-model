#!/usr/bin/env python3
"""
check_router_test_registration.py — ST-10 (EPIC-10, v7.9, BLG-QA-125)

Blocks a commit that adds a new @router.<method>(...) decorator in
backend/routers/*.py without a corresponding entry in
backend/routers/test.py's test_cases list, per CLAUDE.md's
"Every new backend route must be registered in the endpoint test suite
in the same commit" rule.

Usage (pre-commit hook, staged changes only):
    python3 scripts/check_router_test_registration.py

Exit code 0: all new routes are registered (or no new routes added).
Exit code 1: at least one new route has no matching test.py entry.
"""

import re
import subprocess
import sys
from pathlib import Path

ROUTE_DECORATOR_RE = re.compile(
    r'@router\.(get|post|put|delete|patch)\(\s*["\']([^"\']*)["\']'
)
# ST-21 (BLG-QA-146, v8.8): the path group was previously `+` (one-or-more),
# which silently failed to match a bare `@router.get("")`/`@router.post("")`
# decorator (an empty-string path, resolving to the router's own prefix
# root — e.g. ticker_universe.py's GET/POST "/ticker-universe"). A newly
# added route registered this way would go undetected by this gate with
# no error, no warning — `*` (zero-or-more) closes that gap.
PREFIX_RE = re.compile(r'APIRouter\(\s*prefix\s*=\s*["\']([^"\']*)["\']')
TEST_ENTRY_RE = re.compile(
    r'"name":\s*"(GET|POST|PUT|DELETE|PATCH)\s+([^"]+)"'
)


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def get_staged_router_files():
    """Return staged backend/routers/*.py files (added or modified), excluding test.py."""
    result = _run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"])
    files = result.stdout.splitlines()
    return [
        f for f in files
        if f.startswith("backend/routers/") and f.endswith(".py") and Path(f).name != "test.py"
    ]


def get_staged_added_lines(path):
    """Return only the added (+) lines for a staged file, via git diff --cached -U0."""
    result = _run(["git", "diff", "--cached", "-U0", "--", path])
    added = []
    for line in result.stdout.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    return added


def get_staged_file_content(path):
    """Return the full staged (about-to-be-committed) content of a file, or '' if not staged/absent."""
    result = _run(["git", "show", f":{path}"])
    if result.returncode != 0:
        # Not staged (e.g. test.py itself wasn't touched this commit) — fall back to working tree.
        p = Path(path)
        return p.read_text() if p.exists() else ""
    return result.stdout


def extract_new_routes(router_file_path):
    """Return [(method, full_path), ...] for routes newly added (in the staged diff) to this file."""
    added_lines = get_staged_added_lines(router_file_path)
    new_route_lines = [ln for ln in added_lines if ROUTE_DECORATOR_RE.search(ln)]
    if not new_route_lines:
        return []

    full_content = get_staged_file_content(router_file_path)
    prefix_match = PREFIX_RE.search(full_content)
    prefix = prefix_match.group(1) if prefix_match else ""

    routes = []
    for line in new_route_lines:
        m = ROUTE_DECORATOR_RE.search(line)
        method, path = m.group(1).upper(), m.group(2)
        full_path = (prefix.rstrip("/") + "/" + path.lstrip("/")).replace("//", "/")
        if not full_path.startswith("/"):
            full_path = "/" + full_path
        # ST-21 (BLG-QA-146, v8.8): an empty-string path (`@router.get("")`) joins
        # to a bare trailing slash (e.g. "/ticker-universe/") which path_pattern()'s
        # exact `^...$` anchor match would never match against a test.py entry
        # written without the trailing slash (e.g. "/ticker-universe") — a false
        # "unregistered" flag even when a correct entry exists. Strip it, except
        # for the bare root path itself.
        if full_path != "/":
            full_path = full_path.rstrip("/")
        routes.append((method, full_path))
    return routes


def _clean_entry_path(raw_path):
    """Strip a trailing human-readable parenthetical annotation from a "name" field's
    path portion, e.g. "/analytics/metrics (all_time)" -> "/analytics/metrics". Some
    test.py entries disambiguate multiple registrations of the same route (different
    query-string variants) this way; the annotation is not part of the actual path."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", raw_path).strip()


def parse_test_py_entries(test_py_content):
    """Return [(method, path), ...] for every registered entry in test.py's test_cases list."""
    return [
        (m.group(1), _clean_entry_path(m.group(2)))
        for m in TEST_ENTRY_RE.finditer(test_py_content)
    ]


def path_pattern(path):
    """Compile a path with {param} segments into a regex matching any concrete value there."""
    escaped = re.escape(path)
    # re.escape turns {param} into \{param\} — collapse any \{...\} back to a wildcard segment.
    escaped = re.sub(r"\\\{[^}]+\\\}", r"[^/]+", escaped)
    return re.compile(f"^{escaped}$")


def is_registered(method, path, test_entries):
    """True if (method, path) has a matching entry in test_entries, params-aware."""
    pattern = path_pattern(path)
    for entry_method, entry_path in test_entries:
        if entry_method != method:
            continue
        if pattern.match(entry_path) or path_pattern(entry_path).match(path):
            return True
    return False


def find_unregistered_routes(new_routes, test_entries):
    """Return the subset of new_routes with no matching test_entries registration."""
    return [(m, p) for (m, p) in new_routes if not is_registered(m, p, test_entries)]


def main():
    router_files = get_staged_router_files()
    if not router_files:
        return 0

    test_py_content = get_staged_file_content("backend/routers/test.py")
    test_entries = parse_test_py_entries(test_py_content)

    missing = []
    for router_file in router_files:
        new_routes = extract_new_routes(router_file)
        for method, path in find_unregistered_routes(new_routes, test_entries):
            missing.append((router_file, method, path))

    if missing:
        print("COMMIT BLOCKED — new route(s) missing from backend/routers/test.py:\n", file=sys.stderr)
        for router_file, method, path in missing:
            print(f"  {router_file}: {method} {path}", file=sys.stderr)
        print(
            "\nAdd a matching test_cases entry to backend/routers/test.py in this same commit "
            "(use a representative value for path params, e.g. {ticker} -> AAPL), per CLAUDE.md's "
            "endpoint test suite registration rule.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
