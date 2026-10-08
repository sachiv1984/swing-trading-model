"""
ST-04 (BLG-QA-217, EPIC-01, v9.11) — every backend module imports with only
backend/ on the path, the way production runs.

`tests/test_backend_service_import_paths.py` (PR #1921) catches one class of
bug: a bare import of a backend/services module. It cannot catch a bare
import of anything else that only resolves through a test-only `sys.path`
entry, because several test files add backend/services/ and similar
directories to `sys.path` for the whole pytest run.

This test therefore runs in a clean subprocess (`python -I`: no
PYTHONPATH, no user site, no script or working directory on `sys.path`)
with only backend/ added, and:

1. imports every backend module (module-level imports), and
2. resolves every import statement in backend/, including function-level
   (lazy) imports, with `importlib.util.find_spec`. A lazy import only runs
   when a request reaches it, so importing the module does not exercise it.
   That is how the PR #1921 defect reached production.

Imports inside a `try` with an explicit ImportError/ModuleNotFoundError
handler are optional dependencies by design and are skipped by the static
check. A broad `except Exception:` does not exempt an import.

Regression: reintroducing `from ai_output_sampling_service import ...`
inside any backend function makes test 2 fail.
"""
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent / "backend"
EXCLUDED_DIRS = {".venv", "venv", "site-packages", "__pycache__", "node_modules",
                 # Test code and fixture generators, not part of the running app.
                 "mutmut_pilot_tests", "test_data"}


def _backend_sources():
    for path in sorted(BACKEND.rglob("*.py")):
        if EXCLUDED_DIRS.intersection(path.relative_to(BACKEND).parts):
            continue
        yield path


def _module_name(path: Path) -> str:
    rel = path.relative_to(BACKEND).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _handles_import_error(handler: ast.ExceptHandler) -> bool:
    """Only an explicit ImportError/ModuleNotFoundError handler marks an
    optional dependency. A bare `except:` or `except Exception:` does not:
    that is exactly how a broken import gets hidden (the sampling call
    sites before ST-03, and utils/ai_sampling.py's own guard)."""
    if handler.type is None:
        return False
    names = handler.type.elts if isinstance(handler.type, ast.Tuple) else [handler.type]
    return any(isinstance(n, ast.Name) and n.id in {"ImportError", "ModuleNotFoundError"}
               for n in names)


def _optional_import_nodes(tree: ast.AST) -> set:
    optional = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Try) and any(_handles_import_error(h) for h in node.handlers):
            for stmt in node.body:
                for inner in ast.walk(stmt):
                    if isinstance(inner, (ast.Import, ast.ImportFrom)):
                        optional.add(id(inner))
    return optional


def _collect_imports(path: Path):
    """(lineno, module name) for every absolute import in `path`, except
    optional imports guarded by an ImportError handler."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    optional = _optional_import_nodes(tree)
    found = []
    for node in ast.walk(tree):
        if id(node) in optional:
            continue
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            found.append((node.lineno, node.module))
        elif isinstance(node, ast.Import):
            found.extend((node.lineno, alias.name) for alias in node.names)
    return found


_CHILD = r"""
import importlib, importlib.util, json, sys
backend, payload = sys.argv[1], json.loads(sys.argv[2])
sys.path.insert(0, backend)
out = {"import_failures": [], "unresolved": []}
for mod in payload["modules"]:
    try:
        importlib.import_module(mod)
    except Exception as exc:
        out["import_failures"].append(f"{mod}: {type(exc).__name__}: {exc}")
for where, name in payload["imports"]:
    try:
        spec = importlib.util.find_spec(name)
    except Exception as exc:
        spec = None
    if spec is None:
        out["unresolved"].append(f"{where} imports '{name}'")
print("@@RESULT@@" + json.dumps(out))
"""


def _run_child(modules, imports):
    env = {k: v for k, v in os.environ.items() if k not in {"PYTHONPATH", "PYTHONHOME"}}
    env.setdefault("DATABASE_URL", "postgresql://stub:stub@localhost:5432/stub")
    payload = json.dumps({"modules": modules, "imports": imports})
    proc = subprocess.run(
        [sys.executable, "-I", "-c", _CHILD, str(BACKEND), payload],
        capture_output=True, text=True, env=env, cwd="/", timeout=300,
    )
    marker = [line for line in proc.stdout.splitlines() if line.startswith("@@RESULT@@")]
    assert marker, f"child process failed (rc={proc.returncode}):\n{proc.stderr[-3000:]}"
    return json.loads(marker[-1][len("@@RESULT@@"):])


def _all_imports():
    imports = []
    for path in _backend_sources():
        rel = path.relative_to(BACKEND.parent)
        imports.extend([f"{rel}:{line}", name] for line, name in _collect_imports(path))
    return imports


def test_every_backend_module_imports_with_only_backend_on_path():
    modules = [_module_name(p) for p in _backend_sources()]
    result = _run_child(modules, [])
    assert not result["import_failures"], (
        "Backend modules that fail to import with only backend/ on sys.path:\n"
        + "\n".join(result["import_failures"])
    )


def test_every_import_statement_resolves_with_only_backend_on_path():
    result = _run_child([], _all_imports())
    assert not result["unresolved"], (
        "Imports (including function-level ones) that do not resolve with only "
        "backend/ on sys.path -- they would raise ModuleNotFoundError in production:\n"
        + "\n".join(result["unresolved"])
    )


def test_bare_sampling_import_is_detected(tmp_path):
    """The PR #1921 shape: a function-level bare import resolves only when
    backend/services/ is on sys.path."""
    src = tmp_path / "probe.py"
    src.write_text("def f():\n    from ai_output_sampling_service import maybe_sample_output\n")
    imports = [[f"probe.py:{line}", name] for line, name in _collect_imports(src)]
    result = _run_child([], imports)
    assert result["unresolved"] == ["probe.py:2 imports 'ai_output_sampling_service'"]


def test_optional_import_guarded_by_import_error_is_skipped(tmp_path):
    src = tmp_path / "probe.py"
    src.write_text("try:\n    import not_installed_pkg\nexcept ImportError:\n    pass\n")
    assert _collect_imports(src) == []


def test_import_hidden_by_broad_except_is_still_checked(tmp_path):
    src = tmp_path / "probe.py"
    src.write_text("try:\n    from ai_output_sampling_service import x\nexcept Exception:\n    pass\n")
    assert _collect_imports(src) == [(2, "ai_output_sampling_service")]
