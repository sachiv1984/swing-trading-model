"""
Unit tests for scripts/check_local_openapi_contract_completeness.py (ST-23,
BLG-GOV-179, EPIC-05, v9.3).

This script is a thin orchestration wrapper around 2 pre-existing checks
(scripts/lint_api_contract_headings.py, scripts/openapi_3way_drift_sweep.py)
— the wrapper's own logic (run both, aggregate exit codes, run all even if
one fails) is what these tests cover, using fake check scripts rather than
re-validating the pre-existing scripts' own detection correctness (already
exercised elsewhere: lint_api_contract_headings.py is an established CI
script; openapi_3way_drift_sweep.py has been run repeatedly this session
against the real repo).

Also includes one end-to-end smoke test against the real current repo
state, proving the wrapper's actual configured CHECKS list runs cleanly
today (catches a real wiring mistake, e.g. a wrong script path).
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "check_local_openapi_contract_completeness.py"

spec = importlib.util.spec_from_file_location("check_local_openapi_contract_completeness", SCRIPT_PATH)
checker = importlib.util.module_from_spec(spec)
sys.modules["check_local_openapi_contract_completeness"] = checker
spec.loader.exec_module(checker)


def _write_fake_check(tmp_path, name, exit_code):
    script = tmp_path / name
    script.write_text(f"import sys\nsys.exit({exit_code})\n")
    return script


def test_all_checks_pass_returns_zero(tmp_path):
    check_a = _write_fake_check(tmp_path, "check_a.py", 0)
    check_b = _write_fake_check(tmp_path, "check_b.py", 0)
    rc = checker.run_checks(checks=[check_a, check_b])
    assert rc == 0


def test_one_check_failing_returns_nonzero(tmp_path):
    check_a = _write_fake_check(tmp_path, "check_a.py", 0)
    check_b = _write_fake_check(tmp_path, "check_b.py", 1)
    rc = checker.run_checks(checks=[check_a, check_b])
    assert rc == 1


def test_both_checks_failing_returns_nonzero(tmp_path):
    check_a = _write_fake_check(tmp_path, "check_a.py", 1)
    check_b = _write_fake_check(tmp_path, "check_b.py", 1)
    rc = checker.run_checks(checks=[check_a, check_b])
    assert rc == 1


def test_all_checks_run_even_when_an_earlier_one_fails(tmp_path, monkeypatch):
    """A single hook run should surface every issue, not stop at the first
    failure — write a marker file from the second check to prove it ran."""
    marker = tmp_path / "second_check_ran.txt"
    check_a = _write_fake_check(tmp_path, "check_a.py", 1)
    check_b = tmp_path / "check_b.py"
    check_b.write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('ran')\n")

    checker.run_checks(checks=[check_a, check_b])

    assert marker.exists()


def test_main_returns_nonzero_and_prints_message_on_failure(tmp_path, monkeypatch, capsys):
    check_a = _write_fake_check(tmp_path, "check_a.py", 1)
    monkeypatch.setattr(checker, "CHECKS", [check_a])

    rc = checker.main()

    assert rc == 1
    captured = capsys.readouterr()
    assert "MERGE BLOCKED locally" in captured.err


def test_main_returns_zero_on_success(tmp_path, monkeypatch):
    check_a = _write_fake_check(tmp_path, "check_a.py", 0)
    monkeypatch.setattr(checker, "CHECKS", [check_a])

    rc = checker.main()

    assert rc == 0


def test_real_configured_checks_pass_against_current_repo():
    """End-to-end smoke test: the wrapper's actual CHECKS list (the 2 real
    scripts) runs cleanly against the current repo state — catches a wiring
    mistake (e.g. a wrong path) that fake-script unit tests above cannot."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        capture_output=True, text=True, cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
