#!/usr/bin/env python3
"""
PII Field-Name Pattern Scan (ST-08, EPIC-03, BLG-GOV-241, cycle 2026-08-03__release-v8.1).

Scans lines *added* to docs/reference/openapi.yaml (relative to a base ref,
default origin/main) for field names matching common PII naming patterns
(email, phone, SSN, date of birth, home address, full legal name, payment
card, government ID, etc.) and flags them for manual review.

This is a lightweight, name-pattern-only heuristic — it does not parse the
OpenAPI schema structurally or inspect actual data. It exists to catch the
common case (a new/changed response schema field is obviously PII-shaped by
name) cheaply, at PR-open time, before a human reviewer has to notice it
themselves. It is not a substitute for a real data-classification review.

Usage:
    python3 scripts/check_pii_field_patterns.py [--base-ref REF]

Exit code 0: no PII-shaped field names found in the diff.
Exit code 1: one or more PII-shaped field names found (printed to stdout) —
             flagged for manual review, does not imply the field is
             necessarily wrong, only that it warrants a human look.
"""
import argparse
import re
import subprocess
import sys

# Common PII field-name patterns (case-insensitive, word-boundary aware).
# Deliberately conservative and name-based only — false positives are
# expected and acceptable for a "flag for manual review" gate; false
# negatives (a PII field slipping through unnoticed) are the failure mode
# this check exists to reduce.
PII_PATTERNS = [
    r"e[-_]?mail",
    r"phone(_?number)?",
    r"ssn",
    r"social[-_]?security",
    r"date[-_]?of[-_]?birth",
    r"\bdob\b",
    r"(home|street|mailing)[-_]?address",
    r"full[-_]?(legal[-_]?)?name",
    r"first[-_]?name",
    r"last[-_]?name",
    r"surname",
    r"passport",
    r"national[-_]?id",
    r"tax[-_]?id",
    r"driver[s]?[-_]?licen[sc]e",
    r"credit[-_]?card",
    r"card[-_]?number",
    r"cvv",
    r"bank[-_]?account",
    r"\biban\b",
    r"\bsort[-_]?code\b",
]

_COMBINED = re.compile("(" + "|".join(PII_PATTERNS) + ")", re.IGNORECASE)

# Matches a YAML mapping key line, e.g. "      full_name:" or "  - email:"
_YAML_KEY = re.compile(r"^\+\s*[-]?\s*([A-Za-z_][A-Za-z0-9_]*)\s*:")

OPENAPI_PATH = "docs/reference/openapi.yaml"


def get_added_field_lines(base_ref: str):
    """Return (field_name, full_line) pairs for every added YAML key line
    in the diff of OPENAPI_PATH against base_ref."""
    result = subprocess.run(
        ["git", "diff", "--unified=0", base_ref, "--", OPENAPI_PATH],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode not in (0, 1):
        print(f"git diff failed: {result.stderr}", file=sys.stderr)
        sys.exit(2)

    matches = []
    for line in result.stdout.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        m = _YAML_KEY.match(line)
        if m:
            matches.append((m.group(1), line.strip()))
    return matches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default="origin/main")
    args = parser.parse_args()

    added = get_added_field_lines(args.base_ref)
    flagged = [(name, line) for name, line in added if _COMBINED.search(name)]

    if not flagged:
        print("No PII-shaped field names found in added/changed openapi.yaml lines.")
        return 0

    print("PII-shaped field name(s) flagged for manual review:")
    for name, line in flagged:
        print(f"  - {name}   ({line})")
    print(
        "\nThis is a name-pattern heuristic, not a data-classification review. "
        "If these fields are genuinely new PII surface, confirm handling/retention "
        "policy is documented before merging. If a false positive, note why in the PR."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
