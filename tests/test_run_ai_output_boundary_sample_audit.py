"""
Unit tests for scripts/run_ai_output_boundary_sample_audit.py (ST-22,
BLG-GOV-178, EPIC-05, v9.3).

Proves the scanner catches real violations, not just that it passes on
compliant text — mirrors this codebase's established
"deliberately-miscoded-fixture" test convention.
"""
import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "run_ai_output_boundary_sample_audit.py"

spec = importlib.util.spec_from_file_location("run_ai_output_boundary_sample_audit", SCRIPT_PATH)
audit = importlib.util.module_from_spec(spec)
sys.modules["run_ai_output_boundary_sample_audit"] = audit
spec.loader.exec_module(audit)


def test_scan_prescriptive_catches_directive_language():
    assert audit.scan_prescriptive("You should reduce your position size here.") is True
    assert audit.scan_prescriptive("We recommend cutting the position by half.") is True
    assert audit.scan_prescriptive("Buy now before the breakout continues.") is True


def test_scan_prescriptive_clean_text_not_flagged():
    assert audit.scan_prescriptive("NVDA is 2.8% above its trailing stop.") is False
    assert audit.scan_prescriptive("") is False
    assert audit.scan_prescriptive(None) is False


def test_scan_prediction_catches_forecast_language():
    assert audit.scan_prediction("AAPL will rise sharply in the coming days.") is True
    assert audit.scan_prediction("The price is expected to reach £200 soon.") is True
    assert audit.scan_prediction("This setup should climb further.") is True


def test_scan_prediction_clean_text_not_flagged():
    assert audit.scan_prediction("Price is currently holding above the 200 SMA.") is False
    assert audit.scan_prediction("") is False
    assert audit.scan_prediction(None) is False


def test_run_audit_on_deliberately_violating_sample():
    """Deliberately-violating fixture, proving the audit's overall pipeline
    (not just the individual scan functions) surfaces real violations."""
    sample = [
        ("test-source-clean", "Momentum remains positive above the 50-day average."),
        ("test-source-prescriptive", "You must exit this position immediately."),
        ("test-source-prediction", "This stock will surge past resistance next week."),
    ]
    results = audit.run_audit(sample)
    by_source = {r["source"]: r for r in results}
    assert by_source["test-source-clean"]["prescriptive_violation"] is False
    assert by_source["test-source-clean"]["prediction_violation"] is False
    assert by_source["test-source-prescriptive"]["prescriptive_violation"] is True
    assert by_source["test-source-prediction"]["prediction_violation"] is True


def test_default_sample_all_clean():
    """The real ST-22 sample (10 documented example outputs) — confirms the
    committed audit result (0 violations) is reproducible."""
    results = audit.run_audit()
    assert len(results) == 10
    assert all(not r["prescriptive_violation"] and not r["prediction_violation"] for r in results)


def test_main_returns_zero_when_clean(capsys):
    rc = audit.main()
    assert rc == 0
    captured = capsys.readouterr()
    assert "Violations found: 0" in captured.out
