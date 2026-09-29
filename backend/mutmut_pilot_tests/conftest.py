"""
Standalone conftest for the ST-15 (BLG-QA-184) mutation-testing pilot.

Deliberately NOT the repo's main tests/conftest.py: mutmut 3.x derives its
mutant "keys" from each mutated file's path relative to the process cwd
(mutmut/utils/format_utils.py::get_mutant_name), stripping only a literal
"src." prefix. This repo's real tests/conftest.py puts backend/ itself on
sys.path (so application code imports as `services.X`/`utils.X`), which
only lines up with mutmut's key format if mutmut is *also* run with cwd set
to backend/ (see docs/testing/mutation_testing_pilot_sizing_and_stop_ratchet.md,
BLG-QA-198, for the full root-cause writeup and why the main conftest.py
can't be reused unmodified once tests/ is copied to a different relative
depth than mutmut's own mutants/ copy).

`Path(__file__).parent.parent` here resolves to `backend/` when this file
runs directly (cwd=backend/, e.g. `pytest mutmut_pilot_tests/`), and to
`backend/mutants/` when it runs *inside* a mutmut run (mutmut copies this
whole directory, since it lives under backend/, as part of
`source_paths=["."]` with cwd=backend/, and mutmut's process runs with
cwd=mutants/) -- in both cases the parent-of-parent is the correct root
for `services.*`/`utils.*`/bare `database` imports.
"""
import ast
import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

_BACKEND_ROOT = Path(__file__).parent.parent

sys.path.insert(0, str(_BACKEND_ROOT))

os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test_stub")


def _discover_database_stub_functions(backend_dir: Path) -> list:
    """Same approach as the repo's main tests/conftest.py (BLG-QA-73): AST-scan
    for `from database import (...)` so every module `services/__init__.py`
    pulls in transitively (not just sizing_service.py's own 3 names) resolves
    to a MagicMock rather than a real DB connection."""
    names = set()
    exclude = {".venv", "venv", "__pycache__"}
    for py_file in backend_dir.rglob("*.py"):
        if any(part in exclude for part in py_file.parts):
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


_database_stub = types.ModuleType("database")
for _fn in _discover_database_stub_functions(_BACKEND_ROOT):
    setattr(_database_stub, _fn, MagicMock())
sys.modules["database"] = _database_stub
