"""
Static guard: backend code must import service modules as `services.<name>`.

The app runs with backend/ (not backend/services/) on sys.path, so a bare
`from ai_output_sampling_service import ...` raises ModuleNotFoundError in
production. Several test files put backend/services/ on sys.path to load
modules directly, and that entry persists for the whole pytest run, so a
runtime import test cannot catch this. Scanning the source can.

Regression for the post-trade debrief failure ("No module named
'ai_output_sampling_service'", 2026-10-07).
"""

import ast
from pathlib import Path

BACKEND = Path(__file__).parent.parent / "backend"
SERVICES = BACKEND / "services"
EXCLUDED_DIRS = {".venv", "venv", "site-packages", "__pycache__", "node_modules"}

SERVICE_MODULES = {p.stem for p in SERVICES.glob("*.py") if p.stem != "__init__"}


def _backend_sources():
    for path in BACKEND.rglob("*.py"):
        if EXCLUDED_DIRS.intersection(path.relative_to(BACKEND).parts):
            continue
        yield path


def test_no_bare_service_module_imports():
    violations = []
    for path in _backend_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            elif isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            else:
                continue
            for name in names:
                if name.split(".")[0] in SERVICE_MODULES:
                    rel = path.relative_to(BACKEND.parent)
                    violations.append(f"{rel}:{node.lineno} imports '{name}' (use 'services.{name}')")
    assert not violations, "Bare service-module imports found:\n" + "\n".join(violations)
