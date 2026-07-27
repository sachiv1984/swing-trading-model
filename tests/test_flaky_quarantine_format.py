"""
Flaky-test quarantine format enforcement — ST-10 (EPIC-10, v7.8, BLG-QA-117).

Scans tests/e2e/*.js for `test.fixme(` calls and asserts every one carries
the required `FLAKY-QUARANTINE:` prefix and a `BLG-*` backlog reference, per
docs/testing/flaky_test_quarantine_process.md. This prevents an untracked
quarantine (a test.fixme added without a follow-up backlog item) from
silently accumulating.
"""
import re
from pathlib import Path

E2E_DIR = Path(__file__).parent.parent / "tests" / "e2e"

# Matches `test.fixme(<anything>, "..."` or `test.fixme(<anything>, '...'`
# across the call's first two arguments (condition, description).
_FIXME_CALL_RE = re.compile(r"test\.fixme\(\s*[^,]+,\s*(['\"])(.*?)\1", re.DOTALL)

_REQUIRED_PREFIX = "FLAKY-QUARANTINE:"
_BACKLOG_REF_RE = re.compile(r"BLG-[A-Z]+-\d+")


def find_fixme_calls(text: str) -> list[str]:
    """Return the description string of every `test.fixme(cond, "desc")` call found."""
    return [m.group(2) for m in _FIXME_CALL_RE.finditer(text)]


def find_format_violations(text: str) -> list[str]:
    """Return a violation message for every test.fixme call missing the required format."""
    violations = []
    for description in find_fixme_calls(text):
        if _REQUIRED_PREFIX not in description:
            violations.append(
                f"test.fixme description missing required '{_REQUIRED_PREFIX}' prefix: {description!r}"
            )
        elif not _BACKLOG_REF_RE.search(description):
            violations.append(
                f"test.fixme description missing a BLG-* backlog reference: {description!r}"
            )
    return violations


def test_correctly_formatted_quarantine_produces_no_violation():
    text = 'test.fixme(true, "FLAKY-QUARANTINE: timing-dependent — tracked in BLG-QA-999");\n'
    assert find_format_violations(text) == []


def test_quarantine_missing_prefix_is_caught():
    text = 'test.fixme(true, "flaky, will fix later, BLG-QA-999");\n'
    violations = find_format_violations(text)
    assert len(violations) == 1
    assert "FLAKY-QUARANTINE" in violations[0]


def test_quarantine_missing_backlog_reference_is_caught():
    text = 'test.fixme(true, "FLAKY-QUARANTINE: timing-dependent assertion");\n'
    violations = find_format_violations(text)
    assert len(violations) == 1
    assert "backlog reference" in violations[0]


def test_no_fixme_calls_produces_no_violations():
    assert find_format_violations("test.skip();\n") == []


def test_real_e2e_directory_has_no_format_violations():
    """
    Regression guard: no test.fixme call exists in the real suite today
    (per the process doc's "Currently-Known Flaky Tests: None" finding),
    and any future one must be correctly formatted.
    """
    total_violations = 0
    for spec_file in sorted(E2E_DIR.glob("*.js")):
        text = spec_file.read_text()
        total_violations += len(find_format_violations(text))
    assert total_violations == 0
