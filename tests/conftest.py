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
#
# ST-14 (BLG-QA-188, EPIC-04, v9.7): the guard used to read "if not already
# set, use a stub" -- so an ambient DATABASE_URL already pointing at a real
# database (e.g. a developer's sandbox configured with real, if read-only,
# credentials for unrelated interactive use) passed straight through
# unmodified into every test, including tests that load a private, isolated
# copy of backend/database.py via importlib (bypassing the sys.modules
# stub below entirely) and then execute real SQL. Confirmed live: with a
# real-looking DATABASE_URL set, tests/test_schema_rollback_verification.py
# attempted (and got InsufficientPrivilege from) a real Postgres connection.
#
# Fixed: outside CI, DATABASE_URL is now always forced to the safe stub,
# regardless of what is already set, unless PYTEST_ALLOW_REAL_DB=1 is
# explicitly set (a deliberate, local opt-in for a developer who has spun up
# their own throwaway Postgres and wants to run integration-style tests
# against it). Inside CI (GitHub Actions sets CI=true automatically for
# every workflow, including Phase A and Phase B here), the workflow's own
# deliberately-configured DATABASE_URL passes through unchanged -- no
# workflow file needs to change for this fix, since Phase A's
# postgresql://ci:ci@localhost:5432/ci_stub and Phase B's
# postgresql://ci:ci@localhost:5432/ci_test are already each workflow's own
# explicit, already-opted-in configuration.
_RUNNING_IN_CI = os.getenv("CI", "").lower() in ("1", "true")
_REAL_DB_OPT_IN = os.getenv("PYTEST_ALLOW_REAL_DB") == "1"
if (_RUNNING_IN_CI or _REAL_DB_OPT_IN) and os.getenv("DATABASE_URL"):
    pass  # deliberately configured (CI workflow env, or explicit local opt-in) -- leave as-is
else:
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
# Test files that need the real database.py (e.g. test_api_contracts.py) import it
# via tests/_real_database.py, which never leaves this stub replaced -- enforced by
# the leak guard below (ST-14, BLG-QA-190).
# ---------------------------------------------------------------------------

import ast  # noqa: E402

_DB_STUB_SCAN_EXCLUDE_DIRS = {".venv", "venv", "site-packages", "node_modules", "__pycache__", "build", "dist"}


def _discover_database_stub_functions(backend_dir: Path) -> list:
    """AST-scan backend/ for `from database import (...)` and return the
    sorted union of imported names, excluding vendored/virtualenv paths.

    Also covers the `import database` form: in a module that binds the name
    `database` that way, every `database.<name>` attribute access counts as
    an imported name.

    Coverage confirmed 2026-11-02 (ST-32, BLG-QA-93, EPIC-05, v9.14) against
    every backend/ subpackage with a database import (routers, services,
    utils, mutmut_pilot_tests, plus backend/*.py). rglob already reached
    every subpackage. The gap was the `import database` form:
    routers/strategy_benchmark.py's 6 `database.<fn>` names were missing
    from the stub. tests/test_conftest_database_stub_scan.py asserts this
    coverage against an independent text scan of the tracked backend files.
    """
    names = set()
    for py_file in backend_dir.rglob("*.py"):
        if any(part in _DB_STUB_SCAN_EXCLUDE_DIRS for part in py_file.parts):
            continue
        try:
            tree = ast.parse(py_file.read_text(), filename=str(py_file))
        except SyntaxError:
            continue
        imports_module = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "database":
                for alias in node.names:
                    names.add(alias.name)
            elif isinstance(node, ast.Import):
                imports_module = imports_module or any(
                    alias.name == "database" and alias.asname is None for alias in node.names
                )
        if imports_module:
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Attribute)
                    and isinstance(node.value, ast.Name)
                    and node.value.id == "database"
                ):
                    names.add(node.attr)
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


# ---------------------------------------------------------------------------
# sys.modules["database"] leak guard (ST-14, BLG-QA-190, EPIC-03, v9.9)
#
# A test file that swaps the stub for the real backend/database.py and never puts
# it back changes what every later file sees, so results silently depend on
# collection order. Files that need the real module use tests/_real_database.py
# (a private copy, or a scoped swap that restores the stub). These two checks
# turn any new unrestored swap into a failure attributed to the file or test
# that caused it, instead of a confusing failure somewhere else.
#
# Not covered (ST-27, BLG-QA-211, v9.13): the guard checks sys.modules["database"]
# only. Modules first imported inside a real_database_imports() block (main,
# routers, services) stay cached for the session with their module-level
# `from database import` names bound to the real module (modules already cached
# stub-bound stay stub-bound), and a later file importing them gets that copy.
# This is accepted and documented in tests/_real_database.py ("Known limit"),
# with the rule that keeps tests independent of it: patch at the service level.
# ---------------------------------------------------------------------------

_LEAK_HINT = (
    "replaced sys.modules['database'] (conftest's stub) without restoring it -- use "
    "tests/_real_database.py: load_real_database(), real_database_imports() or the "
    "restore_database_module fixture (ST-14, BLG-QA-190)"
)


# ---------------------------------------------------------------------------
# backend/services/ sys.path guard (ST-36, BLG-QA-218, EPIC-05, v9.14)
#
# The app runs with backend/ on sys.path, never backend/services/. A test file
# that adds backend/services/ (to load a service by bare name without running
# services/__init__.py) leaves it there for the whole pytest process, so code
# under test can resolve a bare `from x_service import ...` that raises
# ModuleNotFoundError in production. That is how BLG-BE-150 passed CI. Load
# such a module by file path (importlib.util.spec_from_file_location) or as
# services.<name> instead. The collect-report hook below fails the file that
# added the entry; the fixture after it fails a test that adds it at run time.
# Both remove the entry so later files are unaffected.
# ---------------------------------------------------------------------------

_BACKEND_SERVICES_DIR = (Path(__file__).parent.parent / "backend" / "services").resolve()
_SERVICES_PATH_HINT = (
    "added backend/services/ to sys.path -- load the module with "
    "importlib.util.spec_from_file_location or import it as services.<name> (ST-36, BLG-QA-218)"
)


def backend_services_path_entries(entries=None) -> list:
    """sys.path entries (or the given entries) that resolve to backend/services/."""
    found = []
    for entry in sys.path if entries is None else entries:
        try:
            if Path(entry or ".").resolve() == _BACKEND_SERVICES_DIR:
                found.append(entry)
        except (OSError, RuntimeError, TypeError, ValueError):
            continue
    return found


def _remove_backend_services_path_entries(entries) -> None:
    for entry in entries:
        while entry in sys.path:
            sys.path.remove(entry)


# ---------------------------------------------------------------------------
# --docs-coupled-only (ST-31, EPIC-05, v9.15, BLG-OPS-191): governance-only and
# docs-only CI runs collect only the test files that may read claude/ or docs/.
# Selection rule: tests/docs_coupled.py.
# ---------------------------------------------------------------------------

def pytest_addoption(parser):
    parser.addoption(
        "--docs-coupled-only",
        action="store_true",
        default=False,
        help="Collect only test files that may read claude/ or docs/ (tests/docs_coupled.py).",
    )


def pytest_ignore_collect(collection_path, config):
    if not config.getoption("--docs-coupled-only", default=False):
        return None
    if collection_path.suffix != ".py" or not collection_path.name.startswith("test_"):
        return None
    from tests.docs_coupled import is_docs_coupled
    return None if is_docs_coupled(collection_path) else True


@pytest.hookimpl(hookwrapper=True)
def pytest_make_collect_report(collector):
    # One hook for every leak guard: a second module-level function with this
    # name would silently replace this one (PR #2023 review, ST-46).
    outcome = yield
    if not isinstance(collector, pytest.Module):
        return
    problems = []
    services_entries = backend_services_path_entries()
    if services_entries:
        _remove_backend_services_path_entries(services_entries)
        problems.append(_SERVICES_PATH_HINT)
    if sys.modules.get("database") is not _database_stub:
        sys.modules["database"] = _database_stub
        problems.append(_LEAK_HINT)
    leaked = leaked_utils_stubs()
    if leaked:
        _evict(leaked)
        problems.append(f"{_UTILS_LEAK_HINT}: {leaked}")
    replaced = replaced_utils_attributes()
    if replaced:
        problems.append(f"{_UTILS_ATTR_HINT}: {replaced}")
    if problems:
        report = outcome.get_result()
        report.outcome = "failed"
        report.longrepr = f"{collector.nodeid}: importing this test file " + "; and ".join(problems)


@pytest.fixture(autouse=True)
def _backend_services_not_on_sys_path(request):
    yield
    services_entries = backend_services_path_entries()
    if services_entries:
        _remove_backend_services_path_entries(services_entries)
        pytest.fail(f"{request.node.nodeid} {_SERVICES_PATH_HINT}", pytrace=False)


@pytest.fixture(autouse=True)
def _database_stub_not_leaked(request):
    yield
    if sys.modules.get("database") is not _database_stub:
        sys.modules["database"] = _database_stub
        pytest.fail(f"{request.node.nodeid} {_LEAK_HINT}", pytrace=False)


# ---------------------------------------------------------------------------
# sys.modules["utils.*"] leak guard (ST-46, BLG-QA-209, EPIC-06, v9.12)
#
# The same leak shape for the utils package: a file that leaves a stand-in
# `utils` / `utils.<name>` in sys.modules (a types.ModuleType or MagicMock,
# not the real file under backend/utils/) changes what every later file
# imports. Reversed file order once failed 32 tests and a collection this
# way. Every utils entry must be a real module loaded from backend/utils/.
# Stub only inside tests/_scoped_utils_stubs.py's scoped_stub_modules().
# ---------------------------------------------------------------------------

_UTILS_DIR = (Path(__file__).resolve().parent.parent / "backend" / "utils").resolve()
_UTILS_LEAK_HINT = (
    "left a stand-in utils / utils.* module in sys.modules -- install utils stubs only "
    "inside tests/_scoped_utils_stubs.py's scoped_stub_modules() (ST-46, BLG-QA-209)"
)


def _is_real_utils_module(module) -> bool:
    try:
        return Path(module.__file__).resolve().is_relative_to(_UTILS_DIR)
    except (AttributeError, TypeError, OSError, ValueError):
        return False


def leaked_utils_stubs() -> list:
    """Names of utils / utils.* sys.modules entries that are not real backend/utils files."""
    return sorted(
        name for name, module in list(sys.modules.items())
        if (name == "utils" or name.startswith("utils.")) and module is not None
        and not _is_real_utils_module(module)
    )


def _evict(names):
    for name in names:
        sys.modules.pop(name, None)


@pytest.fixture(autouse=True)
def _utils_stubs_not_leaked(request):
    yield
    leaked = leaked_utils_stubs()
    if leaked:
        _evict(leaked)
        pytest.fail(f"{request.node.nodeid} {_UTILS_LEAK_HINT}: {leaked}", pytrace=False)


# ---------------------------------------------------------------------------
# utils.* attribute leak guard (ST-41, BLG-QA-222, EPIC-07, v9.15)
#
# The guard above checks which module object sits under utils / utils.*. A
# test that instead replaces an attribute on the real module
# (`sys.modules["utils.calculations"].calculate_atr = MagicMock()`, or a
# patch(...).start() never stopped) and does not restore it leaks just as
# badly, and every later importer binds the replacement. Each real
# backend/utils module object's public callables are snapshotted when first
# seen (all of backend/utils is imported at conftest load, so normally at
# session start); after every test file is collected and every test runs, any
# snapshotted name that now holds a different object fails that file or test
# and is put back. A module re-imported as a new object is snapshotted too,
# and the older object stays checked, since modules imported earlier still
# call it.
# Restore with patch()/patch.object() as a context manager or decorator, or
# the monkeypatch fixture -- all of which undo before this check runs.
# ---------------------------------------------------------------------------

_UTILS_ATTR_HINT = (
    "replaced a public callable on a real utils module without restoring it -- use "
    "patch()/patch.object() as a context manager or decorator, or monkeypatch "
    "(ST-41, BLG-QA-222)"
)
# id(module) -> (name, module object, {attr: original}). Every real utils
# module object ever seen is kept: a file may evict and re-import a utils
# module, and services imported earlier still call the older object.
_UTILS_ATTR_SNAPSHOTS: dict = {}


def _public_callables(module) -> dict:
    return {name: value for name, value in list(vars(module).items())
            if not name.startswith("_") and callable(value) and not isinstance(value, type(sys))}


def snapshot_real_utils_attributes() -> None:
    """Record public callables of every real utils module object in
    sys.modules not yet snapshotted."""
    for name, module in list(sys.modules.items()):
        if (name == "utils" or name.startswith("utils.")) and module is not None \
                and _is_real_utils_module(module) and id(module) not in _UTILS_ATTR_SNAPSHOTS:
            _UTILS_ATTR_SNAPSHOTS[id(module)] = (name, module, _public_callables(module))


def replaced_utils_attributes(restore: bool = True) -> list:
    """`module.attr` names whose object differs from the snapshot, on any real
    utils module object seen so far; restored when `restore` is true. Then
    snapshots any newly seen module objects."""
    replaced = set()
    for name, module, originals in list(_UTILS_ATTR_SNAPSHOTS.values()):
        current = vars(module)
        for attr, original in originals.items():
            if current.get(attr, _MISSING) is not original:
                replaced.add(f"{name}.{attr}")
                if restore:
                    setattr(module, attr, original)
    snapshot_real_utils_attributes()
    return sorted(replaced)


_MISSING = object()


def _import_all_real_utils() -> None:
    import importlib
    import pkgutil
    for info in pkgutil.iter_modules([str(_UTILS_DIR)]):
        try:
            importlib.import_module(f"utils.{info.name}")
        except Exception:  # an import-time failure surfaces in the tests that use it
            pass


_import_all_real_utils()
snapshot_real_utils_attributes()


@pytest.fixture(autouse=True)
def _utils_attributes_not_leaked(request):
    yield
    replaced = replaced_utils_attributes()
    if replaced:
        pytest.fail(f"{request.node.nodeid} {_UTILS_ATTR_HINT}: {replaced}", pytrace=False)


# Import mock harness fixtures (BLG-QA-08 / ST-09)
from tests.mock_harness.conftest_extension import (  # noqa: F401, E402
    alpaca_mock_harness,
    yahoo_mock_harness,
    screener_mocks,
    scenario_mocks,
)
