#!/usr/bin/env python3
"""
Classify a CI run's changed files as code or governance/docs-only.

ST-31 (EPIC-05, v9.15, BLG-OPS-191; Product Owner ruling ESC-EXEC-20261105-05).
Reads changed file paths, one per line, on stdin. Prints `true` if the run
must run the code-test suites, `false` if every path is under `claude/` or
`docs/`.

Fails safe towards running the suites: an empty list (the file list could not
be read) prints `true`.

Usage: <file list> | python3 scripts/ci_code_changes.py
"""
import sys

GOVERNANCE_OR_DOCS_PREFIXES = ("claude/", "docs/")


def needs_code_suites(paths) -> bool:
    paths = [p.strip() for p in paths if p.strip()]
    if not paths:
        return True
    return any(not p.startswith(GOVERNANCE_OR_DOCS_PREFIXES) for p in paths)


if __name__ == "__main__":
    print("true" if needs_code_suites(sys.stdin.read().splitlines()) else "false")
