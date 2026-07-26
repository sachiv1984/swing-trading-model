"""
Unit tests for the changelog digest service (ST-02, EPIC-02, v7.8, BLG-FEAT-84).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

import services.changelog_digest_service as digest  # noqa: E402


SAMPLE_CHANGELOG = """# Product Changelog

## v7.8 — Release Visibility & Engineering Hardening — 2026-08-01
Cycle: 2026-07-24__release-v7.8

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | In-app what's new panel | docs/specs/frontend/pages/dashboard.md |
| EPIC-02 | Telegram changelog digest | claude/system/post_ship_closure.md |

### Deviations accepted
None.

## v7.7 — Strategy Intelligence Surfacing & Notification UX — 2026-07-24
Cycle: 2026-07-21__release-v7.7

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-04 strategy-version performance comparison view | docs/specs/frontend/pages/strategy_benchmark.md |
"""


def test_extract_most_recent_version_when_version_omitted():
    result = digest.extract_changes_shipped(SAMPLE_CHANGELOG)
    assert result is not None
    assert result["heading"].startswith("v7.8")
    assert result["rows"] == [
        ("EPIC-01", "In-app what's new panel"),
        ("EPIC-02", "Telegram changelog digest"),
    ]


def test_extract_specific_version_by_prefix():
    result = digest.extract_changes_shipped(SAMPLE_CHANGELOG, version="v7.7")
    assert result is not None
    assert result["heading"].startswith("v7.7")
    assert result["rows"] == [("EPIC-01", "SI-04 strategy-version performance comparison view")]


def test_extract_returns_none_for_unknown_version():
    assert digest.extract_changes_shipped(SAMPLE_CHANGELOG, version="v9.9") is None


def test_extract_returns_none_for_empty_changelog():
    assert digest.extract_changes_shipped("# Product Changelog\n\nNo versions yet.\n") is None


def test_format_changelog_digest_escapes_markdown_v2():
    message = digest.format_changelog_digest("v7.8 — Test.Release!", [("EPIC-01", "Fix (bug) in [module]")])
    assert "Release shipped" in message
    assert "\\." in message  # period escaped
    assert "\\!" in message  # exclamation escaped
    assert "\\(bug\\)" in message
    assert "\\[module\\]" in message


def test_send_changelog_digest_no_credentials_configured(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.setattr(digest, "CHANGELOG_PATH", digest.CHANGELOG_PATH)  # real file, unaffected
    result = digest.send_changelog_digest()
    assert result["sent"] is False
    assert "credentials" in result["error"]


def test_send_changelog_digest_sends_successfully(monkeypatch, tmp_path):
    changelog_file = tmp_path / "changelog.md"
    changelog_file.write_text(SAMPLE_CHANGELOG)
    monkeypatch.setattr(digest, "CHANGELOG_PATH", changelog_file)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "fake-chat-id")

    sent_calls = []
    monkeypatch.setattr(digest, "_send_telegram_request", lambda url, payload, sleep_fn=None: sent_calls.append(payload))

    result = digest.send_changelog_digest()
    assert result["sent"] is True
    assert result["entry_count"] == 2
    assert len(sent_calls) == 1
    assert sent_calls[0]["parse_mode"] == "MarkdownV2"


def test_send_changelog_digest_failure_does_not_raise(monkeypatch, tmp_path):
    # Post-Ship Closure must never be blocked by a Telegram send failure.
    changelog_file = tmp_path / "changelog.md"
    changelog_file.write_text(SAMPLE_CHANGELOG)
    monkeypatch.setattr(digest, "CHANGELOG_PATH", changelog_file)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "fake-chat-id")

    def _raise(*args, **kwargs):
        raise RuntimeError("Telegram API unreachable")

    monkeypatch.setattr(digest, "_send_telegram_request", _raise)

    result = digest.send_changelog_digest()  # must not raise
    assert result["sent"] is False
    assert "Telegram API unreachable" in result["error"]


def test_send_changelog_digest_missing_changelog_file(monkeypatch, tmp_path):
    monkeypatch.setattr(digest, "CHANGELOG_PATH", tmp_path / "does_not_exist.md")
    result = digest.send_changelog_digest()
    assert result["sent"] is False
    assert "not found" in result["error"]


def test_real_changelog_has_at_least_one_extractable_version():
    # Integration sanity check against the actual repo changelog.
    text = digest.CHANGELOG_PATH.read_text()
    result = digest.extract_changes_shipped(text)
    assert result is not None
    assert len(result["rows"]) > 0
