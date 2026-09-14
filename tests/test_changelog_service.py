"""
Unit tests for the changelog service (ST-01, EPIC-01, v7.8, BLG-FE-128;
User Impact sourcing added ST-13, EPIC-03, v8.8, BLG-FE-161).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

import services.changelog_service as changelog_service  # noqa: E402


SAMPLE_CHANGELOG = """# Product Changelog

## v8.8 — Live Data-Integrity, Backend Hardening & Debt Closure — 2026-08-20
Cycle: 2026-08-14__release-v8.8

### Changes shipped
| EPIC | Description | User Impact | Spec sections updated |
|------|-------------|-------------|----------------------|
| EPIC-01 | In-app what's new panel | Release notes now show what's new for you, not raw engineering copy. | docs/specs/frontend/pages/dashboard.md |
| EPIC-02 | Telegram changelog digest | — | claude/system/post_ship_closure.md |

### Deviations accepted
None.

## v7.7 — Strategy Intelligence Surfacing & Notification UX — 2026-07-24
Cycle: 2026-07-21__release-v7.7

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-04 strategy-version performance comparison view | docs/specs/frontend/pages/strategy_benchmark.md |
"""


def test_get_latest_returns_most_recent_version(monkeypatch, tmp_path):
    changelog_file = tmp_path / "changelog.md"
    changelog_file.write_text(SAMPLE_CHANGELOG)
    monkeypatch.setattr(changelog_service, "CHANGELOG_PATH", changelog_file)

    result = changelog_service.get_latest_changelog_entry()
    assert result is not None
    assert result["version"] == "v8.8"
    assert result["changes"] == ["Release notes now show what's new for you, not raw engineering copy."]


def test_get_latest_returns_none_for_pre_v8_8_table_with_no_user_impact_column(monkeypatch, tmp_path):
    # A 3-column table (Description only, no User Impact) predates ST-13
    # (v8.8) and does not match the 4-cell row pattern -- degrades to
    # "no changes" rather than falling back to Description.
    changelog_file = tmp_path / "changelog.md"
    changelog_file.write_text("""# Product Changelog

## v7.8 — Release Visibility & Engineering Hardening — 2026-08-01
Cycle: 2026-07-24__release-v7.8

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | In-app what's new panel | docs/specs/frontend/pages/dashboard.md |
""")
    monkeypatch.setattr(changelog_service, "CHANGELOG_PATH", changelog_file)
    assert changelog_service.get_latest_changelog_entry() is None


def test_get_latest_returns_none_for_missing_file(monkeypatch, tmp_path):
    monkeypatch.setattr(changelog_service, "CHANGELOG_PATH", tmp_path / "does_not_exist.md")
    assert changelog_service.get_latest_changelog_entry() is None


def test_get_latest_returns_none_for_no_version_headings(monkeypatch, tmp_path):
    changelog_file = tmp_path / "changelog.md"
    changelog_file.write_text("# Product Changelog\n\nNo versions yet.\n")
    monkeypatch.setattr(changelog_service, "CHANGELOG_PATH", changelog_file)
    assert changelog_service.get_latest_changelog_entry() is None


def test_get_latest_returns_none_when_no_changes_shipped_table(monkeypatch, tmp_path):
    changelog_file = tmp_path / "changelog.md"
    changelog_file.write_text("## v1.0 — Initial — 2026-01-01\n\nNo changes-shipped table here.\n")
    monkeypatch.setattr(changelog_service, "CHANGELOG_PATH", changelog_file)
    assert changelog_service.get_latest_changelog_entry() is None


def test_real_changelog_is_parseable():
    # Integration sanity check against the actual repo changelog: confirms
    # the real file has at least one structurally parseable "## vX.Y — ..."
    # version heading. Does NOT assert the latest release has any
    # user-facing changes -- a pure engineering-debt release (every EPIC row
    # marked "-"/"—" User Impact) legitimately produces changes == [], and
    # get_latest_changelog_entry() correctly returns None in that case (see
    # dashboard.md §6A's own defined "Empty" state -- "Nothing to show" --
    # for exactly this scenario). Asserting non-empty content here made this
    # test break every time the latest real release happened to be
    # debt-only (confirmed live: v9.3, "Full-Capacity Debt Clearance", all 5
    # EPIC rows are "-"), which is an expected, not exceptional, state --
    # not a parser regression. BLG-BE-117.
    text = changelog_service.CHANGELOG_PATH.read_text()
    assert re.search(r"^## v\S+ — .+$", text, re.MULTILINE), (
        "real changelog.md has no parseable '## vX.Y — ...' heading"
    )

    result = changelog_service.get_latest_changelog_entry()
    if result is not None:
        assert result["version"]
        assert len(result["changes"]) > 0
    # else: latest release legitimately has 0 user-facing changes -- valid,
    # not a failure.
