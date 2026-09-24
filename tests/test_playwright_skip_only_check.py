"""
Playwright .skip()/.only() lint enforcement — ST-15 (EPIC-04, v9.7, BLG-QA-174).

Unit tests for scripts/check_playwright_skip_only.py's detection logic, plus a
regression guard confirming the real tests/e2e/ suite has zero violations today.
Mirrors the existing test_flaky_quarantine_format.py convention for this class
of grep-based CI lint.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_playwright_skip_only import find_violations  # noqa: E402

E2E_DIR = Path(__file__).parent.parent / "tests" / "e2e"


def test_test_only_is_flagged():
    text = "test.only('some test', async ({ page }) => {\n  await page.goto('/');\n});\n"
    violations = find_violations(text)
    assert len(violations) == 1
    assert "test.only(" in violations[0]


def test_describe_only_is_flagged():
    text = "test.describe.only('a suite', () => {\n  test('x', async () => {});\n});\n"
    violations = find_violations(text)
    assert len(violations) == 1
    assert "test.describe.only(" in violations[0]


def test_describe_skip_is_flagged():
    text = "test.describe.skip('a suite', () => {\n  test('x', async () => {});\n});\n"
    violations = find_violations(text)
    assert len(violations) == 1
    assert "test.describe.skip(" in violations[0]


def test_declaration_time_test_skip_with_string_title_is_flagged():
    text = "test.skip('a disabled test', async ({ page }) => {\n  await page.goto('/');\n});\n"
    violations = find_violations(text)
    assert len(violations) == 1
    assert "test.skip(" in violations[0]


def test_runtime_unconditional_skip_inside_test_body_is_not_flagged():
    """Existing legitimate pattern (tests/e2e/keyboard-shortcuts.spec.js) -- an
    environment-conditional early exit inside the test body, not a declaration-time
    disable."""
    text = "test('some test', async ({ page }) => {\n  test.skip();\n});\n"
    assert find_violations(text) == []


def test_runtime_conditional_skip_with_reason_is_not_flagged():
    """Existing legitimate pattern (tests/e2e/visual-snapshots.spec.js)."""
    text = (
        "test('some test', async ({ page }) => {\n"
        "  test.skip(true, 'Skeleton not visible — response too fast in this environment');\n"
        "});\n"
    )
    assert find_violations(text) == []


def test_allow_list_exception_with_backlog_reference_suppresses_the_flag():
    text = (
        "test.only('debugging', async () => {}); "
        "// ALLOW-SKIP-ONLY: deliberate, reviewed — tracked in BLG-QA-999\n"
    )
    assert find_violations(text) == []


def test_allow_list_exception_missing_backlog_reference_is_itself_a_violation():
    text = "test.only('debugging', async () => {}); // ALLOW-SKIP-ONLY: temporary\n"
    violations = find_violations(text)
    assert len(violations) == 1
    assert "backlog reference" in violations[0]


def test_clean_file_produces_no_violations():
    text = "test('a normal test', async ({ page }) => {\n  await page.goto('/');\n});\n"
    assert find_violations(text) == []


def test_real_e2e_directory_has_no_violations_today():
    """Regression guard, per this story's own AC: 'first run completed'. Any future
    .only()/declaration-skip() introduced into tests/e2e/ must be caught here."""
    total_violations = 0
    for spec_file in sorted(E2E_DIR.glob("*.js")):
        total_violations += len(find_violations(spec_file.read_text(), str(spec_file)))
    assert total_violations == 0
