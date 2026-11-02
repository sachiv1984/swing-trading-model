"""
ST-32 (BLG-QA-93, EPIC-05, v9.14): the AST scan in tests/conftest.py that builds
the session `database` stub must find every name backend/ imports from
`database`, in every subpackage.

The coverage test compares the scan's result with an independent regex scan of
the git-tracked backend files (git ls-files skips virtualenvs and vendored
code by construction), so a missed subpackage, a missed file or a missed
import form fails here rather than as an AttributeError in an unrelated test.
"""
import re
import subprocess
from pathlib import Path

from tests.conftest import _DB_STUB_FUNCTIONS, _discover_database_stub_functions

REPO_ROOT = Path(__file__).parent.parent

_FROM_IMPORT_RE = re.compile(r"^[ \t]*from[ \t]+database[ \t]+import[ \t]+(\([^)]*\)|[^\n]*)", re.MULTILINE)
_IMPORT_MODULE_RE = re.compile(r"^[ \t]*import[ \t]+database[ \t]*(?:#.*)?$", re.MULTILINE)
_ATTRIBUTE_RE = re.compile(r"\bdatabase\.([A-Za-z_][A-Za-z0-9_]*)")


def _tracked_backend_files():
    out = subprocess.run(
        ["git", "ls-files", "backend/*.py", "backend/**/*.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [REPO_ROOT / line for line in out.splitlines() if line]


def _names_from_text(text):
    names = set()
    for match in _FROM_IMPORT_RE.finditer(text):
        body = re.sub(r"#[^\n]*", "", match.group(1)).strip("() \t\n")
        for part in body.split(","):
            name = part.split(" as ")[0].strip()
            if name:
                names.add(name)
    if _IMPORT_MODULE_RE.search(text):
        names.update(_ATTRIBUTE_RE.findall(text))
    return names


def _expected_by_file():
    expected = {}
    for path in _tracked_backend_files():
        names = _names_from_text(path.read_text())
        if names:
            expected[path.relative_to(REPO_ROOT)] = names
    return expected


def test_scan_finds_every_database_import_in_backend():
    expected = _expected_by_file()
    assert expected, "independent scan found no database imports; the regexes are broken"
    missing = {
        str(path): sorted(names - set(_DB_STUB_FUNCTIONS))
        for path, names in expected.items()
        if names - set(_DB_STUB_FUNCTIONS)
    }
    assert not missing, f"conftest AST scan missed these database imports: {missing}"


def test_scan_reaches_every_backend_subpackage_with_a_database_import():
    expected = _expected_by_file()
    subpackages = {path.parts[1] for path in expected if len(path.parts) > 2}
    # Every subpackage known on 2026-11-02 still has a database import, so a
    # rename or move that empties one is noticed here.
    assert {"routers", "services"} <= subpackages
    for subpackage in subpackages:
        names = set().union(*(n for p, n in expected.items() if len(p.parts) > 2 and p.parts[1] == subpackage))
        assert names <= set(_DB_STUB_FUNCTIONS), subpackage


def test_import_database_attribute_form_is_covered():
    """routers/strategy_benchmark.py uses `import database` then `database.<fn>`."""
    for name in ("ensure_backtest_tables", "get_backtest_summary", "upsert_backtest_data"):
        assert name in _DB_STUB_FUNCTIONS


def test_scan_handles_nested_packages_and_skips_vendored_paths(tmp_path):
    backend = tmp_path / "backend"
    (backend / "pkg" / "sub").mkdir(parents=True)
    (backend / "pkg" / "sub" / "mod.py").write_text(
        "from database import (\n    alpha,  # comment\n    beta as b,\n)\n"
    )
    (backend / "other.py").write_text("import database\n\ndef f():\n    return database.gamma()\n")
    (backend / "aliased.py").write_text("import database as db\n\ndef g():\n    return db.not_counted()\n")
    (backend / ".venv" / "lib").mkdir(parents=True)
    (backend / ".venv" / "lib" / "vendored.py").write_text("from database import vendored\n")
    (backend / "broken.py").write_text("from database import (\n")

    assert _discover_database_stub_functions(backend) == ["alpha", "beta", "gamma"]
