#!/usr/bin/env python3
"""
check_openapi_drift.py — ST-08 (EPIC-02, v1.8, CLAUDE.md's OpenAPI Drift
Detection gate), extracted as its own importable module by ST-20
(BLG-QA-173, EPIC-05, v9.6).

This is the exact 2-way drift check .github/workflows/openapi-drift.yml
has run as an inline Python heredoc since v1.8: cross-checks
docs/reference/openapi.yaml against the canonical markdown API contracts
in docs/specs/api_contracts/. Extracted into this standalone module for
ST-20's own purpose -- a hard, PR-blocking gate had no test of its own
confirming it actually still fires when it should; an inline heredoc
embedded in a YAML workflow file cannot be imported by pytest, so there
was no way to write a genuine regression test against it without either
duplicating the logic (which would silently drift from the real gate) or
extracting it (this module). The workflow's own "Detect drift" step now
calls this script instead of carrying the logic inline -- same behaviour,
now regression-tested (tests/test_openapi_drift_gate.py).

Approach: regex-based path/method extraction and cross-check (no YAML
parser for structure -- PyYAML is used only to detect syntax errors).
Regex is used deliberately: the YAML parser cannot handle malformed
openapi.yaml files -- and a malformed file IS a form of drift we want to
surface, not crash on.
  1. Parse markdown contracts for "## METHOD /path" section headings.
  2. Parse openapi.yaml for "  /path:" blocks and their "    method:" keys.
  3. Flag: any contract-declared METHOD+PATH missing from openapi.yaml.
  4. Flag: any openapi.yaml METHOD+PATH missing from all contracts.
  5. Flag: YAML parse errors in openapi.yaml as a blocking issue.

Canonical truth: markdown contracts take precedence over openapi.yaml.

Usage (CI / local, matches the original inline step exactly):
    python3 scripts/check_openapi_drift.py
Writes drift_report.md and (if $GITHUB_OUTPUT is set) a drift_count line.
Exit code 0: no drift. Exit code 1: drift found (or a YAML syntax error).
"""
import os
import re
import sys
from pathlib import Path

HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}

PATH_RE = re.compile(r"^  (/[^\s:]+)\s*:", re.MULTILINE)
METHOD_RE = re.compile(r"^    (get|post|put|patch|delete|head|options)\s*:", re.MULTILINE)
HEADING_RE = re.compile(
    r"^##\s+(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(/\S+)",
    re.MULTILINE,
)

# Known gaps during transition periods (METHOD PATH strings). Same set the
# inline heredoc carried before extraction.
KNOWN_GAPS: set = {"GET /market/status"}


def get_yaml_parse_error(openapi_text: str):
    """Returns the error string if openapi_text has a YAML syntax error,
    else None. PyYAML is optional at import time (mirrors the original
    inline step's own `try: import yaml` guard)."""
    try:
        import yaml
        yaml.safe_load(openapi_text)
        return None
    except Exception as e:
        return str(e)


def get_openapi_pairs(openapi_text: str) -> set:
    pairs = set()
    path_spans = [(m.group(1), m.start(), m.end()) for m in PATH_RE.finditer(openapi_text)]
    for i, (path, start, end) in enumerate(path_spans):
        next_start = path_spans[i + 1][1] if i + 1 < len(path_spans) else len(openapi_text)
        block = openapi_text[end:next_start]
        for mm in METHOD_RE.finditer(block):
            pairs.add(f"{mm.group(1).upper()} {path}")
    return pairs


def get_contract_pairs(contract_files) -> set:
    """contract_files: iterable of Path objects (already-read markdown contract files)."""
    pairs = set()
    for contract in contract_files:
        text = contract.read_text()
        for m in HEADING_RE.finditer(text):
            pairs.add(f"{m.group(1).upper()} {m.group(2)}")
    return pairs


def compute_drift(contract_pairs: set, openapi_pairs: set, known_gaps: frozenset = frozenset()):
    """Pure -- no I/O. Returns (in_contracts_not_openapi, in_openapi_not_contracts)."""
    in_contracts_not_openapi = contract_pairs - openapi_pairs - known_gaps
    in_openapi_not_contracts = openapi_pairs - contract_pairs - known_gaps
    return in_contracts_not_openapi, in_openapi_not_contracts


def build_report(contract_files_count, contract_pairs, openapi_pairs,
                  in_contracts_not_openapi, in_openapi_not_contracts,
                  yaml_parse_error, drift_count):
    lines = [
        "## OpenAPI Drift Detection Report",
        "",
        "**Spec:** `docs/reference/openapi.yaml`  |  "
        "**Contracts:** `docs/specs/api_contracts/*.md`",
        "**Cycle:** `2026-03-04__release-v1.8`  |  **Gate:** `[EPIC-02][ST-08]`",
        "",
        f"Scanned {contract_files_count} contract file(s).  "
        f"Contracts: {len(contract_pairs)} endpoint(s).  "
        f"OpenAPI: {len(openapi_pairs)} endpoint(s).",
        "",
    ]

    if yaml_parse_error:
        lines += [
            "### YAML Syntax Error in openapi.yaml",
            "",
            "```",
            yaml_parse_error,
            "```",
            "",
            "Fix the YAML syntax error before drift check can be fully reliable.",
            "",
        ]

    if drift_count == 0:
        lines += [
            "### No drift detected",
            "",
            "All contract-declared endpoints are present in openapi.yaml "
            "and vice versa. Merge gate: PASSED.",
        ]
    else:
        if in_contracts_not_openapi:
            lines += [
                "### In contracts but MISSING from openapi.yaml",
                "",
                "Declared as canonical in markdown but absent from "
                "`docs/reference/openapi.yaml`. Update openapi.yaml.",
                "",
                "| Method + Path |",
                "|--------------|",
            ]
            for pair in sorted(in_contracts_not_openapi):
                lines.append(f"| `{pair}` |")
            lines.append("")

        if in_openapi_not_contracts:
            lines += [
                "### In openapi.yaml but MISSING from contracts",
                "",
                "Present in `docs/reference/openapi.yaml` but has no matching "
                "`## METHOD /path` heading in any markdown contract. "
                "Add the canonical contract section or remove from openapi.yaml.",
                "",
                "| Method + Path |",
                "|--------------|",
            ]
            for pair in sorted(in_openapi_not_contracts):
                lines.append(f"| `{pair}` |")
            lines.append("")

        lines += [
            f"### MERGE BLOCKED — {drift_count} issue(s) detected.",
            "",
            "Resolve drift before merging: update openapi.yaml (ST-10 pattern) "
            "or update the relevant markdown contract.",
        ]

    return "\n".join(lines)


def run_check(openapi_path: Path, contracts_dir: Path, known_gaps: frozenset = frozenset(KNOWN_GAPS)):
    """Runs the full check against real files. Returns (drift_count, report_text).
    Raises SystemExit(1) with a stderr message if no contract files are found
    (matches the original inline step's own hard-fail behaviour)."""
    openapi_text = openapi_path.read_text()
    yaml_parse_error = get_yaml_parse_error(openapi_text)
    openapi_pairs = get_openapi_pairs(openapi_text)

    contract_files = sorted(contracts_dir.glob("*.md"))
    if not contract_files:
        print(f"ERROR: No markdown contracts found in {contracts_dir}", file=sys.stderr)
        sys.exit(1)
    contract_pairs = get_contract_pairs(contract_files)

    in_contracts_not_openapi, in_openapi_not_contracts = compute_drift(
        contract_pairs, openapi_pairs, known_gaps
    )

    drift_count = len(in_contracts_not_openapi) + len(in_openapi_not_contracts)
    if yaml_parse_error:
        drift_count += 1

    report = build_report(
        len(contract_files), contract_pairs, openapi_pairs,
        in_contracts_not_openapi, in_openapi_not_contracts,
        yaml_parse_error, drift_count,
    )
    return drift_count, report


def main():
    repo_root = Path(__file__).resolve().parent.parent
    drift_count, report = run_check(
        repo_root / "docs" / "reference" / "openapi.yaml",
        repo_root / "docs" / "specs" / "api_contracts",
    )

    print(report)

    with open("drift_report.md", "w") as fh:
        fh.write(report)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as fh:
            fh.write(f"drift_count={drift_count}\n")

    return 1 if drift_count != 0 else 0


if __name__ == "__main__":
    sys.exit(main())
