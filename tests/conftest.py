"""
Pytest configuration for the swing trading model test suite.

Sets up sys.path to include backend/ and provides a dummy DATABASE_URL
environment variable to prevent database.py from raising a ValueError at
import time. Tests that require a real database use their own mocking strategy.
"""
import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock
import pytest

# Add backend to sys.path so all test files can import backend modules directly
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Provide a dummy DATABASE_URL before any test module imports database.py.
# This prevents the "DATABASE_URL environment variable not set" ValueError
# that would otherwise fire at collection time for any test importing the
# backend database module (directly or via services/__init__.py).
# Tests that need a real DB use their own mock/stub strategy.
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test_stub"

# ---------------------------------------------------------------------------
# Session-scoped database stub (BLG-QA-20 / ST-09; auto-derived per BLG-QA-73)
#
# Registered at conftest load time (before any test file is collected) so that
# import-time `from database import <fn>` bindings in service modules resolve
# to MagicMock instances rather than a real DB connection.
#
# The stub's function list is derived automatically by an AST scan of backend/
# for `from database import (...)` statements, rather than hand-maintained.
# This removes the manual-sync requirement that previously lived in CLAUDE.md
# (adding a new `database` import no longer requires a matching conftest.py
# edit — see claude/backlog resolution for BLG-QA-73).
#
# test_api_contracts.py intentionally evicts this stub (sys.modules.pop) to
# load the real database.py — that is the correct behaviour for contract tests.
# ---------------------------------------------------------------------------

import ast  # noqa: E402

_DB_STUB_SCAN_EXCLUDE_DIRS = {".venv", "venv", "site-packages", "node_modules", "__pycache__", "build", "dist"}


def _discover_database_stub_functions(backend_dir: Path) -> list:
    """AST-scan backend/ for `from database import (...)` and return the
    sorted union of imported names, excluding vendored/virtualenv paths."""
    names = set()
    for py_file in backend_dir.rglob("*.py"):
        if any(part in _DB_STUB_SCAN_EXCLUDE_DIRS for part in py_file.parts):
            continue
        try:
            tree = ast.parse(py_file.read_text(), filename=str(py_file))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "database":
                for alias in node.names:
                    names.add(alias.name)
    return sorted(names)


_DB_STUB_FUNCTIONS = _discover_database_stub_functions(Path(__file__).parent.parent / "backend")

_database_stub = types.ModuleType("database")
for _fn in _DB_STUB_FUNCTIONS:
    setattr(_database_stub, _fn, MagicMock())
sys.modules["database"] = _database_stub


@pytest.fixture(scope="session", autouse=True)
def database_stub():
    """Exposes the session-scoped database stub registered at conftest load time."""
    yield _database_stub


# Import mock harness fixtures (BLG-QA-08 / ST-09)
from tests.mock_harness.conftest_extension import (  # noqa: F401, E402
    alpaca_mock_harness,
    yahoo_mock_harness,
    screener_mocks,
    scenario_mocks,
)
