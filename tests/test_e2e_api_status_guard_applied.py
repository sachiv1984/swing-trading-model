"""
Static check that the ST-24 API status guard is applied suite-wide
(ST-24, EPIC-04, v9.13, BLG-QA-227).

tests/e2e/fixtures/api-status-guard.js fails a Playwright test on any
404/405 from the app's API origin, but only for specs that take `test`
from it. A new spec that imports from '@playwright/test' directly would
silently skip the guard, so this test fails on one.
"""
import re
from pathlib import Path

E2E_DIR = Path(__file__).parent / "e2e"
GUARD_IMPORT = re.compile(r"""(require\(\s*|from\s+)(['"])\./fixtures/api-status-guard\2""")
DIRECT_IMPORT = re.compile(r"""(require\(\s*|from\s+)(['"])@playwright/test\2""")


def _spec_files():
    return sorted(p for p in E2E_DIR.rglob("*.spec.js") if p.is_file())


def test_suite_has_specs():
    assert len(_spec_files()) > 100


def test_no_spec_imports_playwright_test_directly():
    offenders = [p.relative_to(E2E_DIR).as_posix() for p in _spec_files() if DIRECT_IMPORT.search(p.read_text())]
    assert offenders == [], (
        "Import test/expect from './fixtures/api-status-guard', not '@playwright/test': " + ", ".join(offenders)
    )


def test_every_spec_uses_the_guard_module():
    missing = [p.relative_to(E2E_DIR).as_posix() for p in _spec_files() if not GUARD_IMPORT.search(p.read_text())]
    assert missing == [], "Spec(s) not using fixtures/api-status-guard: " + ", ".join(missing)
