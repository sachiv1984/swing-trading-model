"""
Regression coverage for the "inverse" OpenAPI drift case
(ST-03, EPIC-01, v9.4, BLG-API-02).

BLG-API-02 was filed on the premise that the OpenAPI Drift Detection gate
(.github/workflows/openapi-drift.yml) only caught one direction of drift
(a contract heading with no openapi.yaml entry) and not the inverse (an
openapi.yaml path with no matching contract heading).

Direct inspection of openapi-drift.yml's "Detect drift" step at v9.4 shows
this premise is stale: the gate already computes BOTH
`in_contracts_not_openapi` and `in_openapi_not_contracts`, sums them into
one `drift_count`, and blocks the merge if either is non-empty (see that
workflow's own step-1..4 header comment). The same inverse check is also
covered by scripts/openapi_3way_drift_sweep.py (run locally pre-commit via
check_local_openapi_contract_completeness.py) via its
`("openapi.yaml", "router decorators", ...)`-style pairwise comparisons,
which include an explicit `openapi_pairs - contract_pairs - KNOWN_GAPS`
("openapi.yaml", "contracts") direction.

No new CI check is added here — duplicating a check that already runs (and
already blocks the merge gate) would be redundant CI surface, not new
coverage. What was actually missing was a *unit-level* regression guard
proving the inverse-direction logic in openapi_3way_drift_sweep.py keeps
firing on synthetic, minimal fixtures — the existing test file
(test_check_local_openapi_contract_completeness.py) only exercises the
real, current, already-clean repo tree end-to-end, which would not catch a
future code change that silently narrowed the sweep back down to one
direction. This file adds that guard.

Live-repo finding at time of writing: 0 pairwise drift across all 6
directions (see scripts/openapi_3way_drift_sweep.py's own output, run via
the pre-commit hook) — there is no pre-existing inverse-drift gap to file
as a BLG-SPEC-* item.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import openapi_3way_drift_sweep as sweep  # noqa: E402


def _write_fixture(tmp_path, monkeypatch, *, routers=None, contracts=None, openapi_paths=""):
    """Point the sweep module's module-level path constants at a synthetic
    fixture tree under tmp_path, so main()'s three get_*_paths() functions
    read fixture content instead of the real repo."""
    routers_dir = tmp_path / "routers"
    routers_dir.mkdir()
    contracts_dir = tmp_path / "contracts"
    contracts_dir.mkdir()
    main_path = tmp_path / "main.py"
    main_path.write_text("")
    openapi_path = tmp_path / "openapi.yaml"

    for name, text in (routers or {}).items():
        (routers_dir / name).write_text(text)
    for name, text in (contracts or {}).items():
        (contracts_dir / name).write_text(text)
    openapi_path.write_text(openapi_paths)

    monkeypatch.setattr(sweep, "ROUTERS_DIR", routers_dir)
    monkeypatch.setattr(sweep, "MAIN_PATH", main_path)
    monkeypatch.setattr(sweep, "CONTRACTS_DIR", contracts_dir)
    monkeypatch.setattr(sweep, "OPENAPI_PATH", openapi_path)
    monkeypatch.setattr(sweep, "KNOWN_GAPS", set())


class TestInverseDirectionDetection:
    """The specific case BLG-API-02 was filed against: a path present in
    openapi.yaml with no matching contract heading."""

    def test_openapi_path_missing_from_contracts_is_flagged(self, tmp_path, monkeypatch):
        _write_fixture(
            tmp_path,
            monkeypatch,
            routers={
                "widgets.py": (
                    'from fastapi import APIRouter\n'
                    'router = APIRouter(prefix="/widgets")\n'
                    '@router.get("/{id}")\n'
                    'def get_widget(id: str):\n'
                    '    ...\n'
                ),
            },
            contracts={},  # no contract file at all — nothing documents /widgets/{id}
            openapi_paths=(
                "paths:\n"
                "  /widgets/{id}:\n"
                "    get:\n"
                "      summary: Get a widget\n"
            ),
        )

        openapi_pairs = sweep.get_openapi_paths()
        contract_pairs = sweep.get_contract_paths()

        assert "GET /widgets/{id}" in openapi_pairs
        assert openapi_pairs - contract_pairs == {"GET /widgets/{id}"}

    def test_main_exits_nonzero_when_only_inverse_direction_drifts(self, tmp_path, monkeypatch, capsys):
        _write_fixture(
            tmp_path,
            monkeypatch,
            routers={},
            contracts={},
            openapi_paths=(
                "paths:\n"
                "  /orphaned:\n"
                "    post:\n"
                "      summary: Documented in openapi.yaml only\n"
            ),
        )

        rc = sweep.main()
        out = capsys.readouterr().out

        assert rc == 1
        assert "openapi.yaml" in out
        assert "POST /orphaned" in out

    def test_main_exits_zero_when_all_three_sources_agree(self, tmp_path, monkeypatch):
        _write_fixture(
            tmp_path,
            monkeypatch,
            routers={
                "widgets.py": (
                    'from fastapi import APIRouter\n'
                    'router = APIRouter(prefix="/widgets")\n'
                    '@router.get("/{id}")\n'
                    'def get_widget(id: str):\n'
                    '    ...\n'
                ),
            },
            contracts={
                "widgets_endpoints.md": "## GET /widgets/{id}\n\nGet a widget.\n",
            },
            openapi_paths=(
                "paths:\n"
                "  /widgets/{id}:\n"
                "    get:\n"
                "      summary: Get a widget\n"
            ),
        )

        rc = sweep.main()
        assert rc == 0


class TestLiveRepoBaseline:
    """Sanity check against the real repo tree — mirrors the pre-commit
    hook's own invocation. Confirms the AC's required baseline run (no
    pre-existing inverse-drift gap) at the time this story shipped."""

    def test_real_repo_has_no_openapi_to_contract_drift(self):
        openapi_pairs = sweep.get_openapi_paths()
        contract_pairs = sweep.get_contract_paths()
        drift = openapi_pairs - contract_pairs - sweep.KNOWN_GAPS
        assert drift == set(), f"Unexpected inverse drift found: {sorted(drift)}"
