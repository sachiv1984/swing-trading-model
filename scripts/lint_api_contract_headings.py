#!/usr/bin/env python3
"""
API Contract Heading-Level Compliance Lint (ST-12, EPIC-12, v7.8, BLG-OPS-117).

Catches the documented "###-level silent-fail" case from CLAUDE.md §2:
"OpenAPI Drift Detection (.github/workflows/openapi-drift.yml) scans contract
files for `## METHOD /path` at exactly the `##` level. Using `###` causes the
endpoint to be invisible to the gate, reporting it as missing from the
contract even if documented."

This lint runs ahead of / alongside that drift-detection gate: rather than
silently ignoring a miscoded heading (as the drift regex does, since it only
matches literal `## `), this script actively scans for any heading that
*looks like* an endpoint declaration (an HTTP method + a path, at any `#`
depth) and fails if it is not at exactly the canonical `##` level.

Usage:
    python3 scripts/lint_api_contract_headings.py [contracts_dir]

Exit code 0: no violations. Exit code 1: one or more heading-level violations
found (printed to stdout, one per line).
"""
import re
import sys
from pathlib import Path

DEFAULT_CONTRACTS_DIR = Path("docs/specs/api_contracts")
HTTP_METHODS = "GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS"

# Files in docs/specs/api_contracts/ that are NOT themselves a canonical
# contract declaration source, so a METHOD+PATH-shaped heading inside them
# at a non-`##` depth is a legitimate nested subsection, not a silent-fail
# bug. Confirmed by manual review (v7.8, ST-12, BLG-OPS-117) — this is the
# only file in the directory that produces this pattern; verify by re-running
# this script whenever a new file is added.
NON_CANONICAL_FILES = {
    # A checklist TEMPLATE (per its own "## Purpose" section) whose completed
    # instances are nested as depth-3 subsections under a depth-2
    # "Retroactive Application" section header — legitimate Markdown
    # structure, not an orphaned/miscoded top-level contract declaration.
    # The actual canonical contract for these endpoints lives in
    # ai_endpoints.md.
    "ai_advisory_contract_checklist.md",
}

# Matches a heading of ANY depth (1-6 '#' chars) followed by an HTTP method
# and a path — this is deliberately broader than the drift detector's
# `^##\s+` regex so it can catch the miscoded (wrong-depth) case instead of
# silently missing it.
_ENDPOINT_HEADING_RE = re.compile(
    rf"^(#{{1,6}})\s+({HTTP_METHODS})\s+(/\S+)", re.MULTILINE
)

CANONICAL_DEPTH = 2  # "## METHOD /path"


def find_heading_level_violations(text: str) -> list[str]:
    """
    Return a list of human-readable violation strings for any endpoint-shaped
    heading not at the canonical `##` (depth-2) level. Correctly-leveled
    headings produce no entry.
    """
    violations = []
    for match in _ENDPOINT_HEADING_RE.finditer(text):
        hashes, method, path = match.groups()
        depth = len(hashes)
        if depth != CANONICAL_DEPTH:
            violations.append(
                f"'{hashes} {method} {path}' is at heading level {depth} "
                f"(expected level {CANONICAL_DEPTH}, i.e. '## {method} {path}') "
                f"— invisible to the OpenAPI Drift Detection gate at this depth."
            )
    return violations


def lint_directory(contracts_dir: Path) -> int:
    """Scan all .md files in contracts_dir. Returns violation count."""
    total = 0
    for contract_file in sorted(contracts_dir.glob("*.md")):
        if contract_file.name in NON_CANONICAL_FILES:
            continue
        text = contract_file.read_text()
        for violation in find_heading_level_violations(text):
            print(f"{contract_file}: {violation}")
            total += 1
    return total


if __name__ == "__main__":
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CONTRACTS_DIR
    if not target_dir.is_dir():
        print(f"ERROR: contracts directory not found: {target_dir}")
        sys.exit(1)

    count = lint_directory(target_dir)
    if count == 0:
        print(f"API Contract Heading-Level Compliance Lint: PASSED (scanned {target_dir})")
        sys.exit(0)
    else:
        print(f"\nAPI Contract Heading-Level Compliance Lint: FAILED — {count} violation(s) found.")
        sys.exit(1)
