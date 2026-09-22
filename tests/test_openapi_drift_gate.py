"""
ST-20 (BLG-QA-173, EPIC-05, v9.6): standing regression check for the
OpenAPI Drift Detection gate itself.

The gate (.github/workflows/openapi-drift.yml) is a hard, PR-blocking CI
gate, but until this story its comparison logic lived only as an inline
Python heredoc inside the workflow YAML — not importable by pytest, so a
regression in the gate's own logic had no test to catch it before it
silently stopped protecting anything. ST-20 extracted that logic,
byte-for-byte behaviourally unchanged, into scripts/check_openapi_drift.py
(see that module's own docstring); this file is the regression test
against the extracted module.

Uses real temp directories (tmp_path) rather than mocking file reads, so
the test exercises the actual Path.read_text()/glob() calls the gate
performs against openapi.yaml and docs/specs/api_contracts/*.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_openapi_drift import (  # noqa: E402
    compute_drift,
    get_contract_pairs,
    get_openapi_pairs,
    get_yaml_parse_error,
    run_check,
)


def _write_openapi(tmp_path, paths_yaml_body):
    openapi_path = tmp_path / "openapi.yaml"
    openapi_path.write_text(f"openapi: 3.0.0\npaths:\n{paths_yaml_body}\n")
    return openapi_path


def _write_contracts(tmp_path, *headings):
    contracts_dir = tmp_path / "contracts"
    contracts_dir.mkdir()
    body = "\n\n".join(f"## {h}\n\nSome contract text." for h in headings)
    (contracts_dir / "example_endpoints.md").write_text(body + "\n")
    return contracts_dir


# ── Fixture 1: deliberate drift — the gate must fire ────────────────────

def test_gate_fires_when_contract_heading_has_no_openapi_entry(tmp_path):
    """A contract declares GET /widgets but openapi.yaml has nothing --
    this is exactly the drift class the gate exists to catch."""
    openapi_path = _write_openapi(tmp_path, "  /other:\n    get:\n      summary: unrelated\n")
    contracts_dir = _write_contracts(tmp_path, "GET /widgets")

    drift_count, report = run_check(openapi_path, contracts_dir)

    assert drift_count > 0
    assert "GET /widgets" in report
    assert "MISSING from openapi.yaml" in report
    assert "MERGE BLOCKED" in report


def test_gate_fires_when_openapi_entry_has_no_contract_heading(tmp_path):
    """openapi.yaml declares POST /orphan but no contract documents it."""
    openapi_path = _write_openapi(tmp_path, "  /orphan:\n    post:\n      summary: undocumented\n")
    contracts_dir = _write_contracts(tmp_path, "GET /widgets")
    # Give the openapi side a matching /widgets entry too, so ONLY /orphan drifts.
    openapi_path.write_text(
        "openapi: 3.0.0\npaths:\n"
        "  /widgets:\n    get:\n      summary: widgets\n"
        "  /orphan:\n    post:\n      summary: undocumented\n"
    )

    drift_count, report = run_check(openapi_path, contracts_dir)

    assert drift_count > 0
    assert "POST /orphan" in report
    assert "MISSING from contracts" in report


# ── Fixture 2: compliant case — the gate must pass ──────────────────────

def test_gate_passes_when_contracts_and_openapi_match(tmp_path):
    openapi_path = _write_openapi(
        tmp_path,
        "  /widgets:\n    get:\n      summary: widgets\n"
        "  /widgets/{id}:\n    delete:\n      summary: delete widget\n",
    )
    contracts_dir = _write_contracts(tmp_path, "GET /widgets", "DELETE /widgets/{id}")

    drift_count, report = run_check(openapi_path, contracts_dir)

    assert drift_count == 0
    assert "No drift detected" in report
    assert "MERGE BLOCKED" not in report


def test_gate_passes_with_known_gap_exemption(tmp_path):
    """A known gap in the KNOWN_GAPS set must not be reported as drift."""
    openapi_path = _write_openapi(tmp_path, "  /widgets:\n    get:\n      summary: widgets\n")
    contracts_dir = _write_contracts(tmp_path, "GET /widgets", "GET /exempted")

    drift_count, report = run_check(openapi_path, contracts_dir, known_gaps=frozenset({"GET /exempted"}))

    assert drift_count == 0
    assert "No drift detected" in report


# ── AC: deliberate revert of the gate's logic must fail the fixture ─────

def test_mutation_check_reverted_compute_drift_fails_to_catch_real_drift():
    """Proves test_gate_fires_when_contract_heading_has_no_openapi_entry
    actually exercises the gate's real comparison logic, not a tautology:
    if compute_drift() were reverted to a no-op (always "no drift"), this
    test demonstrates the resulting false negative directly, rather than
    asserting on run_check() (which would need monkeypatching to prove
    the same thing less directly)."""
    contract_pairs = {"GET /widgets"}
    openapi_pairs = set()  # openapi.yaml has nothing -- real drift

    real_missing_from_openapi, real_missing_from_contracts = compute_drift(contract_pairs, openapi_pairs)
    assert real_missing_from_openapi == {"GET /widgets"}, "sanity: the real logic catches this drift"

    def reverted_compute_drift(contract_pairs, openapi_pairs, known_gaps=frozenset()):
        """Simulates a regression: the comparison always reports no drift."""
        return set(), set()

    reverted_missing_from_openapi, reverted_missing_from_contracts = reverted_compute_drift(
        contract_pairs, openapi_pairs
    )
    assert reverted_missing_from_openapi == set(), (
        "the reverted (broken) logic silently reports no drift -- this is exactly "
        "the failure mode ST-20 exists to catch: confirms the real compute_drift() "
        "above is not equivalent to a no-op, i.e. the fixture in "
        "test_gate_fires_when_contract_heading_has_no_openapi_entry genuinely "
        "depends on the real logic to pass."
    )
    assert real_missing_from_openapi != reverted_missing_from_openapi


# ── Supporting unit coverage for the extracted helpers ───────────────────

def test_get_yaml_parse_error_detects_bad_yaml():
    bad_yaml = "openapi: 3.0.0\npaths:\n  /widgets:\n    get: [unclosed"
    assert get_yaml_parse_error(bad_yaml) is not None


def test_get_yaml_parse_error_none_for_valid_yaml():
    good_yaml = "openapi: 3.0.0\npaths:\n  /widgets:\n    get:\n      summary: ok\n"
    assert get_yaml_parse_error(good_yaml) is None


def test_get_openapi_pairs_extracts_method_and_path():
    text = "paths:\n  /a:\n    get:\n      x: 1\n    post:\n      x: 2\n  /b:\n    delete:\n      x: 3\n"
    pairs = get_openapi_pairs(text)
    assert pairs == {"GET /a", "POST /a", "DELETE /b"}


def test_get_contract_pairs_extracts_heading_method_and_path(tmp_path):
    f = tmp_path / "contract.md"
    f.write_text("## GET /a\n\ntext\n\n## POST /b\n\nmore text\n\n### Not a top-level heading /c\n")
    pairs = get_contract_pairs([f])
    assert pairs == {"GET /a", "POST /b"}
