"""
Regression tests for scripts/check_deploy_path_filter_drift.py
(ST-14, BLG-OPS-90, EPIC-03, v9.0).

Covers both confirmed incident shapes the script exists to catch:
1. Missing-deploy (BLG-OPS-82): a known runtime-read file not covered by
   either deploy path filter.
2. Dashboard-only build-path filter drift (this item's own gate-clearing
   incident): the production filter snapshot is the checked-in artifact
   that makes the previously dashboard-only fact comparable at all.

CI-safe: no live DB, no network, no live Render access. Reads the real
repo files (staging-deploy.yml, the production filter snapshot) since
those are exactly what the script itself reads in production use — the
tests that matter here are about the *matching logic*, not about
mocking the script's own inputs away.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import check_deploy_path_filter_drift as drift_check  # noqa: E402


class TestParseStagingFilterPaths:
    def test_parses_real_staging_workflow(self):
        """Sanity check against the real repo file — must find at least
        the paths documented in docs/ops/render_build_deploy_path_filter_audit.md."""
        paths = drift_check._parse_staging_filter_paths()
        assert "src/**" in paths
        assert "backend/**" in paths
        assert "public/**" in paths
        assert "docs/product/changelog.md" in paths


class TestCoveredByStaging:
    def test_exact_match(self):
        assert drift_check._covered_by_staging("docs/product/changelog.md", ["docs/product/changelog.md"]) is True

    def test_double_star_prefix_match(self):
        assert drift_check._covered_by_staging("backend/services/foo.py", ["backend/**"]) is True
        assert drift_check._covered_by_staging("backend/tickers_full_list.csv", ["backend/**"]) is True

    def test_not_covered(self):
        assert drift_check._covered_by_staging("docs/some_new_config.json", ["src/**", "backend/**"]) is False


class TestCoveredByProduction:
    def test_root_directory_default_scope_covers_nested_file(self):
        snapshot = {"root_directory": "backend", "root_directory_is_implicit_default_scope": True, "included_paths": []}
        assert drift_check._covered_by_production("backend/tickers_full_list.csv", snapshot) is True

    def test_included_paths_exact_match(self):
        snapshot = {"root_directory": "backend", "root_directory_is_implicit_default_scope": True, "included_paths": ["docs/product/changelog.md"]}
        assert drift_check._covered_by_production("docs/product/changelog.md", snapshot) is True

    def test_file_outside_root_directory_and_included_paths_not_covered(self):
        """This is exactly the BLG-OPS-82/BLG-OPS-90 drift shape: a file
        outside the Root Directory default scope and not in Included Paths."""
        snapshot = {"root_directory": "backend", "root_directory_is_implicit_default_scope": True, "included_paths": ["docs/product/changelog.md"]}
        assert drift_check._covered_by_production("docs/some_new_config.json", snapshot) is False


class TestMainIntegration:
    def test_real_repo_state_has_no_drift(self):
        """All of KNOWN_RUNTIME_READ_FILES must be covered by at least one
        real filter today — this is the actual CI gate behaviour."""
        assert drift_check.main() == 0

    def test_uncovered_known_file_fails(self, monkeypatch):
        """Simulates incident shape 1 (missing-deploy): a known
        runtime-read file covered by neither filter must hard-fail."""
        monkeypatch.setattr(
            drift_check,
            "KNOWN_RUNTIME_READ_FILES",
            drift_check.KNOWN_RUNTIME_READ_FILES + [{"path": "docs/not_covered_anywhere.json", "optional": False}],
        )
        assert drift_check.main() == 1

    def test_optional_file_absent_from_repo_does_not_fail(self, monkeypatch):
        """feature_flags.json-class entries: optional, and skipped entirely
        while the file doesn't exist yet (matches the audit doc's own
        'flagged, no action needed until that file is actually added')."""
        monkeypatch.setattr(
            drift_check,
            "KNOWN_RUNTIME_READ_FILES",
            [{"path": "docs/does_not_exist_and_never_will.json", "optional": True}],
        )
        assert drift_check.main() == 0
