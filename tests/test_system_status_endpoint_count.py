"""
ST-22 (BLG-QA-126, EPIC-05, v8.2): SystemStatus.js hardcoded fallback count
vs. AST-derived registered endpoint test count.

Reuses the same AST-parsing logic as the CI-only "Endpoint Count Drift Check
(ST-11)" job in .github/workflows/quality_gate.yml, as an actual pytest test
that also runs locally (not just at CI merge-gate time).
"""
import ast
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
TEST_ROUTER_PATH = REPO_ROOT / "backend" / "routers" / "test.py"
SYSTEM_STATUS_PATH = REPO_ROOT / "src" / "pages" / "SystemStatus.js"
TEST_CASES_VAR = "test_cases"


def get_test_cases_count(test_router_path: Path) -> int:
    """AST-parse backend/routers/test.py's `test_cases = [...]` list length."""
    tree = ast.parse(test_router_path.read_text(), filename=str(test_router_path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == TEST_CASES_VAR:
                    if isinstance(node.value, ast.List):
                        return len(node.value.elts)
    raise ValueError(f"Could not find a `{TEST_CASES_VAR} = [...]` list assignment in {test_router_path}")


def get_fallback_count(system_status_path: Path) -> int:
    """Extract SystemStatus.js's `totalTests || 'N'` fallback constant."""
    text = system_status_path.read_text()
    match = re.search(r"totalTests\s*\|\|\s*'(\d+)'", text)
    if not match:
        raise ValueError(f"Could not find the totalTests fallback constant in {system_status_path}")
    return int(match.group(1))


def test_fallback_count_matches_registered_endpoint_tests():
    """The current repository state must have zero drift — this is the real gate."""
    registered_count = get_test_cases_count(TEST_ROUTER_PATH)
    fallback_count = get_fallback_count(SYSTEM_STATUS_PATH)
    assert fallback_count == registered_count, (
        f"SystemStatus.js's hardcoded fallback ('{fallback_count}') does not match "
        f"backend/routers/test.py's AST-derived test_cases count ({registered_count}). "
        f"Per CLAUDE.md §2, update the fallback in src/pages/SystemStatus.js and "
        f"tests/e2e/system-status.spec.js's SC-SS-01b in the same commit as any new "
        f"backend route registered in test.py."
    )


def test_deliberately_stale_fallback_is_detected(tmp_path):
    """Prove the check itself is sensitive to drift — a deliberately-stale fallback
    value must fail the comparison, not silently pass."""
    real_count = get_test_cases_count(TEST_ROUTER_PATH)

    stale_system_status = tmp_path / "SystemStatus.js"
    stale_system_status.write_text(f"Tests {{totalTests || '{real_count + 1}'}} endpoints")

    fallback_count = get_fallback_count(stale_system_status)
    assert fallback_count != real_count, "Test fixture setup error — stale value must differ from real count"

    with pytest.raises(AssertionError):
        assert fallback_count == real_count, "expected mismatch"
