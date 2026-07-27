"""
Unit tests for the AI spend trend service (ST-06, EPIC-06, v7.8, BLG-FEAT-82).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
# Note: deliberately NOT popping "database" from sys.modules here (unlike
# test_api_contracts.py's pattern) -- that pop is a process-global mutation
# that evicts conftest.py's session-scoped DB stub for every test file that
# runs afterward in the same pytest session, not just this one. This test
# only needs to monkeypatch the get_claude_spend_between attribute on
# whatever `database` module object is already resolved (stub or real),
# which works safely either way.

import services.ai_spend_trend_service as trend_service  # noqa: E402


SAMPLE_CHANGELOG = """# Product Changelog

## v7.8 — Release Visibility & Engineering Hardening — 2026-08-01
Cycle: 2026-07-24__release-v7.8

### Changes shipped
| EPIC | Description |
|------|-------------|
| EPIC-06 | AI spend trend chart |

## v7.7 — Strategy Intelligence Surfacing & Notification UX — 2026-07-24
Cycle: 2026-07-21__release-v7.7

## v7.6 — PDF / Print-Friendly Export — 2026-07-20
Cycle: 2026-07-20__release-v7.6

## v7.5 — UI Feature Expansion Continuation — 2026-07-20
Cycle: 2026-07-20__release-v7.5

## v7.4 — UI Feature Expansion Readiness Pass — 2026-07-17
Cycle: 2026-07-17__release-v7.4

## v7.3 — Dashboard/Trade-Plan/Navigation UX Continuation — 2026-07-16
Cycle: 2026-07-16__release-v7.3

## v7.2 — Dashboard & Trade-Plan UX Hardening — 2026-07-15
Cycle: 2026-07-15__release-v7.2
"""


def test_parse_changelog_cycles_sorted_ascending_by_date():
    cycles = trend_service._parse_changelog_cycles(SAMPLE_CHANGELOG)
    dates = [c["date"] for c in cycles]
    assert dates == sorted(dates)
    assert cycles[-1]["version"] == "v7.8"
    assert cycles[0]["version"] == "v7.2"


def test_parse_changelog_cycles_same_day_tie_resolves_in_document_order():
    # Real case: v7.5 and v7.6 both shipped 2026-07-20. changelog.md lists
    # v7.6 first (newest-first convention), so v7.6 is chronologically the
    # later of the two same-day releases -- ascending output must place
    # v7.5 before v7.6, not the reverse.
    versions = [c["version"] for c in trend_service._parse_changelog_cycles(SAMPLE_CHANGELOG)]
    assert versions.index("v7.5") < versions.index("v7.6")


def test_parse_changelog_cycles_empty_for_no_headings():
    assert trend_service._parse_changelog_cycles("# Product Changelog\n\nNothing here.\n") == []


def test_get_ai_spend_trend_takes_last_6_cycles_oldest_to_newest(monkeypatch, tmp_path):
    changelog_file = tmp_path / "changelog.md"
    changelog_file.write_text(SAMPLE_CHANGELOG)
    monkeypatch.setattr(trend_service, "CHANGELOG_PATH", changelog_file)

    calls = []

    def fake_spend_between(start, end):
        calls.append((start, end))
        return 10.0

    import database
    monkeypatch.setattr(database, "get_claude_spend_between", fake_spend_between, raising=False)

    trend = trend_service.get_ai_spend_trend()

    # 7 cycles exist (v7.2..v7.8); only the last 6 (v7.3..v7.8) should appear.
    versions = [t["version"] for t in trend]
    assert versions == ["v7.3", "v7.4", "v7.5", "v7.6", "v7.7", "v7.8"]
    assert all(t["spend_usd"] == 10.0 for t in trend)

    # Windows: each cycle's start is its own date; end is the next cycle's
    # date, except the last (open-ended, end=None).
    assert calls[0] == ("2026-07-16", "2026-07-17")  # v7.3 -> v7.4
    assert calls[-1] == ("2026-08-01", None)  # v7.8, open-ended


def test_get_ai_spend_trend_returns_fewer_than_6_when_history_shorter(monkeypatch, tmp_path):
    short_changelog = """## v7.8 — Test — 2026-08-01
## v7.7 — Test — 2026-07-24
"""
    changelog_file = tmp_path / "changelog.md"
    changelog_file.write_text(short_changelog)
    monkeypatch.setattr(trend_service, "CHANGELOG_PATH", changelog_file)

    import database
    monkeypatch.setattr(database, "get_claude_spend_between", lambda start, end: 5.0, raising=False)

    trend = trend_service.get_ai_spend_trend()
    assert [t["version"] for t in trend] == ["v7.7", "v7.8"]


def test_get_ai_spend_trend_empty_for_missing_changelog(monkeypatch, tmp_path):
    monkeypatch.setattr(trend_service, "CHANGELOG_PATH", tmp_path / "does_not_exist.md")
    assert trend_service.get_ai_spend_trend() == []


def test_real_changelog_produces_a_trend():
    # Integration sanity check against the actual repo changelog.
    trend = trend_service.get_ai_spend_trend()
    assert isinstance(trend, list)
    assert len(trend) <= 6
    if trend:
        assert all("version" in t and "spend_usd" in t for t in trend)


def test_spend_trend_endpoint_returns_ok_envelope(monkeypatch):
    from fastapi.testclient import TestClient
    from main import app

    monkeypatch.setattr(
        trend_service, "get_ai_spend_trend",
        lambda: [{"version": "v7.8", "spend_usd": 1.23}],
    )
    client = TestClient(app)
    response = client.get("/ai/spend-trend")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["data"] == [{"version": "v7.8", "spend_usd": 1.23}]
