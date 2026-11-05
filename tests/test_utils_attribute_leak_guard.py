"""
ST-41 (BLG-QA-222, EPIC-07, v9.15) — conftest's utils.* attribute leak guard.

The module-identity guard (ST-46, BLG-QA-209) only checks which object sits
under utils / utils.* in sys.modules. This guard also fails a test or file
that replaces a public callable on a real utils module without restoring it.
"""
import os
import subprocess
import sys
import textwrap
import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch

import tests.conftest as conftest

ROOT = Path(__file__).resolve().parent.parent


def _calculations():
    # Looked up at call time: another file may have re-imported the module.
    conftest.snapshot_real_utils_attributes()
    return sys.modules["utils.calculations"]


def test_real_utils_modules_are_snapshotted():
    calculations = _calculations()
    name, module, originals = conftest._UTILS_ATTR_SNAPSHOTS[id(calculations)]
    assert name == "utils.calculations" and module is calculations
    assert originals["calculate_trailing_stop"] is calculations.calculate_trailing_stop
    # backend/utils is imported at conftest load, so every module is covered.
    assert {"utils.pricing", "utils.formatting"} <= {n for n, _, _ in conftest._UTILS_ATTR_SNAPSHOTS.values()}


def test_replaced_attribute_is_reported_and_restored():
    calculations = _calculations()
    original = calculations.calculate_trailing_stop
    calculations.calculate_trailing_stop = MagicMock()
    try:
        assert conftest.replaced_utils_attributes() == ["utils.calculations.calculate_trailing_stop"]
        assert calculations.calculate_trailing_stop is original
    finally:
        calculations.calculate_trailing_stop = original


def test_deleted_attribute_is_reported_and_restored():
    calculations = _calculations()
    original = calculations.calculate_holding_days
    del calculations.calculate_holding_days
    try:
        assert conftest.replaced_utils_attributes() == ["utils.calculations.calculate_holding_days"]
        assert calculations.calculate_holding_days is original
    finally:
        calculations.calculate_holding_days = original


def test_scoped_patch_is_not_reported():
    calculations = _calculations()
    with patch.object(calculations, "calculate_trailing_stop"):
        pass
    with patch("utils.calculations.calculate_holding_days"):
        pass
    assert conftest.replaced_utils_attributes() == []


def _run_pytest_on(body):
    """Run pytest on a throwaway test file under tests/ so tests/conftest.py applies."""
    folder = ROOT / "tests" / f"_st41_guard_selftest_{uuid.uuid4().hex[:8]}"
    folder.mkdir()
    try:
        (folder / "test_leak.py").write_text(textwrap.dedent(body))
        env = {**os.environ, "DATABASE_URL": "postgresql://stub:stub@localhost:5432/stub"}
        return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(folder)],
                              cwd=ROOT, capture_output=True, text=True, env=env)
    finally:
        for f in folder.rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted(folder.rglob("*"), reverse=True):
            d.rmdir()
        folder.rmdir()


def test_guard_fails_a_test_that_leaves_an_attribute_replaced():
    result = _run_pytest_on("""
        from unittest.mock import MagicMock
        import utils.calculations

        def test_leaks():
            utils.calculations.calculate_trailing_stop = MagicMock()

        def test_after():
            assert not isinstance(utils.calculations.calculate_trailing_stop, MagicMock)
    """)
    out = result.stdout + result.stderr
    assert result.returncode != 0, out
    assert "test_leaks" in out and "utils.calculations.calculate_trailing_stop" in out and "ST-41" in out
    # The guard fails test_leaks at teardown (reported as an error on it), and
    # test_after sees the restored function.
    assert "ERROR tests/" in out and "test_leak.py::test_leaks" in out
    assert "test_after" not in out.split("short test summary info", 1)[-1]


def test_guard_fails_a_file_that_leaves_an_attribute_replaced_at_import():
    result = _run_pytest_on("""
        from unittest.mock import patch
        patch("utils.pricing.get_live_fx_rate").start()   # never stopped

        def test_anything():
            pass
    """)
    out = result.stdout + result.stderr
    assert result.returncode != 0, out
    assert "importing this test file" in out and "utils.pricing.get_live_fx_rate" in out


def test_guard_passes_a_test_that_restores_with_monkeypatch():
    result = _run_pytest_on("""
        import utils.calculations

        def test_monkeypatched(monkeypatch):
            monkeypatch.setattr(utils.calculations, "calculate_trailing_stop", lambda *a, **k: 0)
    """)
    assert result.returncode == 0, result.stdout + result.stderr
