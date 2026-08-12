"""
Unit tests for scripts/check_dependency_vuln_rescan.py (ST-17, BLG-QA-138,
EPIC-05, v8.6).

Covers the script's core parsing/dedup logic directly (pure functions,
no subprocess) plus an end-to-end run of main() against temp files for the
full pipeline, per the story's AC: baseline-hit, new-finding, and
malformed/error-shaped input scenarios (at least 3; this file covers more).
"""
import importlib.util
import json
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "check_dependency_vuln_rescan.py"

spec = importlib.util.spec_from_file_location("check_dependency_vuln_rescan", SCRIPT_PATH)
rescan = importlib.util.module_from_spec(spec)
sys.modules["check_dependency_vuln_rescan"] = rescan
spec.loader.exec_module(rescan)


# ---------------------------------------------------------------------------
# load_json — malformed/error-shaped input scenario
# ---------------------------------------------------------------------------

def test_load_json_returns_none_for_missing_file(tmp_path):
    result = rescan.load_json(str(tmp_path / "does_not_exist.json"))
    assert result is None


def test_load_json_returns_none_for_malformed_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not valid json {{{")
    result = rescan.load_json(str(bad))
    assert result is None


def test_load_json_returns_parsed_data_for_valid_json(tmp_path):
    good = tmp_path / "good.json"
    good.write_text(json.dumps({"a": 1}))
    result = rescan.load_json(str(good))
    assert result == {"a": 1}


# ---------------------------------------------------------------------------
# pip_audit_findings
# ---------------------------------------------------------------------------

def test_pip_audit_findings_returns_empty_list_for_none():
    assert rescan.pip_audit_findings(None) == []


def test_pip_audit_findings_extracts_package_version_advisory():
    data = {
        "dependencies": [
            {"name": "requests", "version": "2.28.0", "vulns": [{"id": "PYSEC-2023-1"}]},
            {"name": "safe-pkg", "version": "1.0.0", "vulns": []},
        ]
    }
    findings = rescan.pip_audit_findings(data)
    assert findings == [("requests", "2.28.0", "PYSEC-2023-1")]


def test_pip_audit_findings_handles_list_shaped_data():
    data = [{"name": "urllib3", "version": "1.26.0", "vulns": [{"id": "PYSEC-2024-1"}]}]
    findings = rescan.pip_audit_findings(data)
    assert findings == [("urllib3", "1.26.0", "PYSEC-2024-1")]


def test_pip_audit_findings_defaults_advisory_id_to_unknown():
    data = {"dependencies": [{"name": "pkg", "version": "1.0", "vulns": [{}]}]}
    findings = rescan.pip_audit_findings(data)
    assert findings == [("pkg", "1.0", "UNKNOWN")]


# ---------------------------------------------------------------------------
# npm_audit_findings
# ---------------------------------------------------------------------------

def test_npm_audit_findings_returns_empty_list_for_none():
    assert rescan.npm_audit_findings(None) == []


def test_npm_audit_findings_filters_to_high_critical_only():
    data = {
        "vulnerabilities": {
            "low-pkg": {"severity": "low", "via": [{"url": "https://x/GHSA-aaaa", "title": "t"}]},
            "high-pkg": {"severity": "high", "via": [{"url": "https://x/GHSA-bbbb", "title": "t"}]},
        }
    }
    findings = rescan.npm_audit_findings(data)
    assert [f[0] for f in findings] == ["high-pkg"]
    assert findings[0][2] == ["GHSA-bbbb"]


def test_npm_audit_findings_labels_inherited_via_string_entries():
    data = {
        "vulnerabilities": {
            "leaf-pkg": {"severity": "critical", "via": ["parent-pkg"]},
        }
    }
    findings = rescan.npm_audit_findings(data)
    assert findings == [("leaf-pkg", "critical", ["(no own advisory — inherited via parent-pkg)"])]


def test_npm_audit_findings_labels_no_via_at_all():
    data = {"vulnerabilities": {"orphan-pkg": {"severity": "high", "via": []}}}
    findings = rescan.npm_audit_findings(data)
    assert findings == [("orphan-pkg", "high", ["(no own advisory)"])]


# ---------------------------------------------------------------------------
# main() end-to-end — baseline-hit and new-finding scenarios
# ---------------------------------------------------------------------------

def _run_main(tmp_path, pip_data, npm_data, baseline_data):
    pip_path = tmp_path / "pip.json"
    npm_path = tmp_path / "npm.json"
    baseline_path = tmp_path / "baseline.json"
    summary_path = tmp_path / "summary.md"
    github_output_path = tmp_path / "gh_output.txt"

    pip_path.write_text(json.dumps(pip_data) if pip_data is not None else "not json {{{")
    npm_path.write_text(json.dumps(npm_data) if npm_data is not None else "not json {{{")
    baseline_path.write_text(json.dumps(baseline_data))
    github_output_path.write_text("")

    old_argv = sys.argv
    sys.argv = [
        "check_dependency_vuln_rescan.py",
        "--pip-audit-json", str(pip_path),
        "--npm-audit-json", str(npm_path),
        "--baseline", str(baseline_path),
        "--summary-out", str(summary_path),
        "--github-output", str(github_output_path),
    ]
    try:
        exit_code = rescan.main()
    finally:
        sys.argv = old_argv

    summary = summary_path.read_text()
    outputs = {}
    for line in github_output_path.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            outputs[k] = v
    return exit_code, summary, outputs


def test_baseline_hit_scenario_no_new_findings(tmp_path):
    """A finding that IS in the baseline is not reported as new."""
    pip_data = {"dependencies": [{"name": "known-pkg", "version": "1.0", "vulns": [{"id": "PYSEC-KNOWN-1"}]}]}
    npm_data = {"vulnerabilities": {}}
    baseline_data = {"pip_audit": {"advisory_ids": ["PYSEC-KNOWN-1"]}, "npm_audit": {"advisory_ids": []}}

    exit_code, summary, outputs = _run_main(tmp_path, pip_data, npm_data, baseline_data)

    assert exit_code == 0
    assert outputs["new_finding_count"] == "0"
    assert outputs["pip_finding_count"] == "1"
    assert "no issue filed" in summary.lower()


def test_new_finding_scenario_flags_as_new(tmp_path):
    """A finding NOT in the baseline is counted as new and flagged for triage."""
    pip_data = {"dependencies": [{"name": "vulnerable-pkg", "version": "2.0", "vulns": [{"id": "PYSEC-NEW-1"}]}]}
    npm_data = {"vulnerabilities": {}}
    baseline_data = {"pip_audit": {"advisory_ids": []}, "npm_audit": {"advisory_ids": []}}

    exit_code, summary, outputs = _run_main(tmp_path, pip_data, npm_data, baseline_data)

    assert exit_code == 0
    assert outputs["new_finding_count"] == "1"
    assert "PYSEC-NEW-1" in summary
    assert "issue has been filed" in summary.lower()


def test_malformed_input_scenario_treated_as_zero_findings_not_crash(tmp_path):
    """Malformed JSON must not crash the script -- load_json() returns None,
    findings functions treat that as an empty list (current script contract;
    see BLG-SEC-29/ST-14 for the separate story making this distinguishable
    from a genuine 0-finding result via pip_audit_status/npm_audit_status)."""
    baseline_data = {"pip_audit": {"advisory_ids": []}, "npm_audit": {"advisory_ids": []}}

    exit_code, summary, outputs = _run_main(tmp_path, pip_data=None, npm_data={"vulnerabilities": {}}, baseline_data=baseline_data)

    assert exit_code == 0
    assert outputs["new_finding_count"] == "0"
    assert outputs["pip_finding_count"] == "0"
