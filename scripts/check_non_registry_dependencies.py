#!/usr/bin/env python3
"""
CI guard rejecting non-registry dependency specifiers (ST-29, BLG-SEC-38, EPIC-07,
v9.7).

A dependency pinned to a git ref (`git+ssh://`, `git+https://`, `git://`) or a local
path (`file:`) bypasses the package registry entirely -- no published, versioned,
checksummed artefact exists for it, so a supply-chain review (`pip-audit`, `npm
audit`, the dependency-vuln-rescan cadence) cannot see it, and the exact code that
ships is whatever the referenced ref/path happened to contain at install time, not a
reproducible, auditable release.

Scans both backend/requirements.txt (pip) and package.json (npm) for a dependency
specifier using one of these non-registry schemes.

Usage: python3 scripts/check_non_registry_dependencies.py
Exit code 0 = no violations, 1 = violations found (prints each one).
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REQUIREMENTS_TXT = REPO_ROOT / "backend" / "requirements.txt"
PACKAGE_JSON = REPO_ROOT / "package.json"

# pip: a requirement line containing one of these schemes anywhere (covers both the
# direct-reference form `name @ git+https://...` and the older `-e git+ssh://...`
# editable-install form).
_PIP_NON_REGISTRY_RE = re.compile(r"\b(git\+ssh|git\+https|git\+git|git://|file:)")

# npm: package.json dependency *values* using one of these non-registry protocols.
_NPM_NON_REGISTRY_RE = re.compile(r"^(git\+ssh|git\+https|git\+git|git://|file:|link:)")


def check_requirements_txt(text: str) -> list:
    violations = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if _PIP_NON_REGISTRY_RE.search(stripped):
            violations.append(
                f"backend/requirements.txt:{lineno}: non-registry dependency specifier: {stripped!r}"
            )
    return violations


def check_package_json(text: str) -> list:
    violations = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return [f"package.json: could not parse as JSON ({e}) -- cannot check for non-registry specifiers"]
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        for name, spec in data.get(section, {}).items():
            if isinstance(spec, str) and _NPM_NON_REGISTRY_RE.match(spec):
                violations.append(
                    f"package.json: {section}.{name} uses a non-registry specifier: {spec!r}"
                )
    return violations


def main() -> int:
    violations = []
    if REQUIREMENTS_TXT.exists():
        violations += check_requirements_txt(REQUIREMENTS_TXT.read_text())
    if PACKAGE_JSON.exists():
        violations += check_package_json(PACKAGE_JSON.read_text())

    if violations:
        for v in violations:
            print(v)
        print(f"\n{len(violations)} violation(s) found.")
        return 1
    print("Non-registry dependency check: PASSED — no git/file/link-scheme dependency specifiers found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
