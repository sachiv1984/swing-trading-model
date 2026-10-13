"""
ST-46 (BLG-QA-209, EPIC-06, v9.12) — tests/conftest.py's utils.* leak guard
fails a test file (at collection) or a test (at teardown) that leaves a
stand-in utils / utils.* module in sys.modules, and
tests/_scoped_utils_stubs.py's scoped_stub_modules() leaves nothing behind.
"""
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from tests import conftest  # noqa: E402
from tests._scoped_utils_stubs import scoped_stub_modules, stub_utils_package  # noqa: E402


def _run_with_repo_conftest(tmp_path, source):
    test_file = tmp_path / "test_leaker.py"
    test_file.write_text(source)
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "tests.conftest", "-p", "no:cacheprovider", "-q",
         "--rootdir", str(tmp_path), str(test_file)],
        cwd=ROOT, capture_output=True, text=True,
        env={"DATABASE_URL": "postgresql://stub:stub@localhost/stub", "PATH": "/usr/bin:/bin",
             "PYTHONPATH": str(ROOT)},
    )


def test_file_leaving_a_module_level_utils_stub_fails_collection(tmp_path):
    result = _run_with_repo_conftest(tmp_path, (
        "import sys, types\n"
        "sys.modules['utils.pricing'] = types.ModuleType('utils.pricing')\n"
        "def test_ok():\n    assert True\n"
    ))
    assert result.returncode != 0
    assert "left a stand-in utils / utils.* module" in result.stdout
    assert "utils.pricing" in result.stdout


def test_test_leaving_a_utils_stub_fails_at_teardown(tmp_path):
    result = _run_with_repo_conftest(tmp_path, (
        "import sys\nfrom unittest.mock import MagicMock\n"
        "def test_leaks():\n    sys.modules['utils.calculations'] = MagicMock()\n"
    ))
    assert result.returncode != 0
    assert "test_leaks" in result.stdout and "utils.calculations" in result.stdout


def test_scoped_stub_file_passes_the_guard(tmp_path):
    result = _run_with_repo_conftest(tmp_path, (
        "import types\n"
        "from tests._scoped_utils_stubs import scoped_stub_modules, stub_utils_package\n"
        "_fmt = types.ModuleType('utils.formatting')\n"
        "with scoped_stub_modules({'utils': stub_utils_package(formatting=_fmt), 'utils.formatting': _fmt}):\n"
        "    import utils.formatting as f\n"
        "assert f is _fmt\n"
        "def test_ok():\n    assert True\n"
    ))
    assert result.returncode == 0, result.stdout + result.stderr


def test_scoped_stub_modules_restores_and_evicts():
    before_utils = sys.modules.get("utils")
    fmt = types.ModuleType("utils.formatting")
    with scoped_stub_modules({"utils": stub_utils_package(formatting=fmt), "utils.formatting": fmt}):
        import utils.formatting
        assert utils.formatting is fmt
    assert sys.modules.get("utils") is before_utils
    assert conftest.leaked_utils_stubs() == []


def test_real_utils_modules_are_not_flagged():
    import utils.calculations  # noqa: F401
    assert conftest.leaked_utils_stubs() == []
