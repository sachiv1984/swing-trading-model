#!/usr/bin/env python3
"""
CI check flagging merged .skip()/.only() Playwright specs (ST-15, BLG-QA-174,
EPIC-04, v9.7).

A Playwright spec left with a declaration-time `test.only(...)` or
`test.describe.only(...)` in a merged PR silently narrows a full CI run down
to that one test/suite; `test.skip('title', ...)` / `test.describe.skip(...)`
silently disables a test/suite entirely. This is distinct from the
already-legitimate runtime pattern `test.skip()` / `test.skip(condition,
reason)` called *inside* a test body (an environment-conditional early exit
-- see docs/testing/flaky_test_quarantine_process.md's own distinction, and
the existing usage in tests/e2e/keyboard-shortcuts.spec.js /
visual-snapshots.spec.js), which this check must not flag.

Heuristic: `test.only(` and `test.describe.only(`/`test.describe.skip(` have
no legitimate runtime form in Playwright -- always flagged. `test.skip(` is
flagged only when its first argument is a string literal (the
declaration-time `test.skip('title', fn)` form); the no-arg or
condition-first runtime forms are exempt.

Exception mechanism: a same-line trailing comment
`// ALLOW-SKIP-ONLY: <reason> — tracked in BLG-QA-<id>` suppresses a flag for
that line -- e.g. for a deliberate, reviewed, temporarily-disabled test with
a tracked follow-up. An allow-list entry with no BLG-* reference is itself a
violation (an untracked exception is not an exception).

Usage: python3 scripts/check_playwright_skip_only.py
Exit code 0 = no violations, 1 = violations found (prints each one).
"""
import re
import sys
from pathlib import Path

E2E_DIR = Path(__file__).parent.parent / "tests" / "e2e"

_ONLY_RE = re.compile(r"\btest\.only\(")
_DESCRIBE_ONLY_OR_SKIP_RE = re.compile(r"\btest\.describe\.(only|skip)\(")
# Declaration-time test.skip('title', fn) -- first arg is a quoted string.
_DECLARATION_SKIP_RE = re.compile(r"""\btest\.skip\(\s*['"]""")

_ALLOW_RE = re.compile(r"ALLOW-SKIP-ONLY:\s*(.*)")
_BACKLOG_REF_RE = re.compile(r"BLG-[A-Z]+-\d+")


def find_violations(text: str, filename: str = "<string>") -> list:
    """Return a list of violation message strings for one spec file's text."""
    violations = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        allow_match = _ALLOW_RE.search(line)
        matched = None
        if _ONLY_RE.search(line):
            matched = "test.only("
        elif _DESCRIBE_ONLY_OR_SKIP_RE.search(line):
            kind = _DESCRIBE_ONLY_OR_SKIP_RE.search(line).group(1)
            matched = f"test.describe.{kind}("
        elif _DECLARATION_SKIP_RE.search(line):
            matched = "test.skip('...', ...)"

        if matched is None:
            continue

        if allow_match:
            reason = allow_match.group(1)
            if not _BACKLOG_REF_RE.search(reason):
                violations.append(
                    f"{filename}:{lineno}: ALLOW-SKIP-ONLY exception missing a "
                    f"BLG-* backlog reference: {reason!r}"
                )
            continue  # correctly-formatted exception -- not a violation

        violations.append(
            f"{filename}:{lineno}: disallowed {matched} with no "
            f"ALLOW-SKIP-ONLY exception comment"
        )
    return violations


def main() -> int:
    total = 0
    for spec_file in sorted(E2E_DIR.glob("*.js")):
        for v in find_violations(spec_file.read_text(), str(spec_file)):
            print(v)
            total += 1
    if total:
        print(f"\n{total} violation(s) found.")
        return 1
    print("Playwright skip/only check: PASSED — no disallowed .only()/declaration-skip() found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
