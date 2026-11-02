"""
ST-36 (BLG-QA-218, EPIC-05, v9.14): no test file may put backend/services/ on
sys.path, and tests/conftest.py enforces it.

The guard itself is exercised in a subprocess: a probe test file outside tests/
is run with tests/conftest.py loaded as a plugin (-p tests.conftest), so the
probe's sys.path change never touches this session.
"""
import ast
import os
import subprocess
import sys
from pathlib import Path

from tests.conftest import backend_services_path_entries

REPO_ROOT = Path(__file__).parent.parent
TESTS_DIR = Path(__file__).parent
SERVICES = REPO_ROOT / "backend" / "services"


def _run_probe(tmp_path, source):
    probe = tmp_path / "test_probe.py"
    probe.write_text(source)
    env = dict(os.environ, DATABASE_URL="postgresql://stub:stub@localhost:5432/stub")
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "tests.conftest", "-p", "no:cacheprovider",
         "-q", "--rootdir", str(tmp_path), str(probe)],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120, env=env,
    )


def test_no_backend_services_entry_on_sys_path_now():
    assert backend_services_path_entries() == []


def test_entry_detection_matches_every_spelling():
    spellings = [
        str(SERVICES),
        str(SERVICES) + os.sep,
        os.path.join(str(TESTS_DIR), "..", "backend", "services"),
    ]
    assert backend_services_path_entries(spellings + [str(REPO_ROOT / "backend"), ""]) == spellings


def test_module_level_insert_fails_collection_naming_the_file(tmp_path):
    result = _run_probe(tmp_path, (
        "import sys\n"
        f"sys.path.insert(0, {str(SERVICES)!r})\n"
        "def test_ok():\n    pass\n"
    ))
    assert result.returncode != 0, result.stdout
    assert "test_probe.py: importing this test file added backend/services/ to sys.path" in result.stdout


def test_insert_inside_a_test_fails_that_test(tmp_path):
    result = _run_probe(tmp_path, (
        "import sys\n"
        "def test_adds_path():\n"
        f"    sys.path.append({str(SERVICES)!r})\n"
        "def test_after():\n"
        "    assert not any(p.rstrip('/').endswith('backend/services') for p in sys.path)\n"
    ))
    assert "test_probe.py::test_adds_path added backend/services/ to sys.path" in result.stdout
    # The failure is raised in test_adds_path's teardown (pytest counts it as
    # passed plus an error); test_after then sees sys.path cleaned and passes.
    assert result.returncode != 0
    assert "2 passed, 1 error" in result.stdout, result.stdout


def test_clean_probe_passes(tmp_path):
    result = _run_probe(tmp_path, "def test_ok():\n    pass\n")
    assert result.returncode == 0, result.stdout + result.stderr


def test_no_test_file_names_backend_services_in_a_sys_path_call():
    """Static backstop: a sys.path call whose arguments spell out a services
    directory, in any tests/ file."""
    offenders = []
    for path in TESTS_DIR.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            target = node.func.value
            if not (isinstance(target, ast.Attribute) and target.attr == "path"
                    and isinstance(target.value, ast.Name) and target.value.id == "sys"):
                continue
            literals = [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
            if any(lit.strip("/\\").endswith("services") for lit in literals) and path != Path(__file__):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}")
    assert not offenders, offenders
