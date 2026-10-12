"""Tests for backend/strategy_version_registry.py (SI-04, ST-01, EPIC-01, v7.7, BLG-FEAT-75).

ST-05 (BLG-BE-137, EPIC-01, v9.10): the hard-coded `len == 5` check is
replaced by checks derived from strategy_rules.md's own Change Log, under the
2026-10-06 coverage rule (register only behaviour/parameter-changing versions).
A new Change Log row that is neither registered nor classified as
documentation-only fails the build.
"""
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from strategy_version_registry import (  # noqa: E402
    DOCUMENTATION_ONLY_VERSIONS,
    STRATEGY_VERSION_REGISTRY,
    get_current_strategy_version,
    resolve_version_window,
)

GRANDFATHERED_NON_BEHAVIOURAL = {"1.1"}


def _change_log():
    """{version: effective_date} parsed from strategy_rules.md's Change Log table."""
    text = (ROOT / "claude" / "strategy" / "strategy_rules.md").read_text()
    rows = {}
    for version, when in re.findall(r"^\| (\d+\.\d+) \| ([^|]+?) \|", text, re.M):
        when = when.strip()
        try:
            rows[version] = datetime.strptime(when, "%d %B %Y").date()
        except ValueError:
            # "February 2026": no day given; the registry uses the 1st for ordering.
            rows[version] = datetime.strptime(when, "%B %Y").date().replace(day=1)
    return rows


def _key(v):
    return tuple(int(p) for p in v.split("."))


def test_change_log_parses():
    log = _change_log()
    assert "1.0" in log and "1.4" in log and len(log) >= 15


def test_every_change_log_row_is_parsed():
    # A row in an unexpected format (e.g. "1.15.1" or "v1.15") must fail here
    # rather than be skipped silently by _change_log()'s version regex.
    text = (ROOT / "claude" / "strategy" / "strategy_rules.md").read_text()
    table = text[text.index("| Version | Date | Summary |"):]
    table = table[: table.index("\n\n")]
    data_rows = [l for l in table.splitlines()[2:] if l.startswith("|")]
    assert len(data_rows) == len(_change_log())


def test_every_change_log_version_is_registered_or_documentation_only():
    registered = {e["version"] for e in STRATEGY_VERSION_REGISTRY}
    unclassified = sorted(set(_change_log()) - registered - DOCUMENTATION_ONLY_VERSIONS, key=_key)
    assert not unclassified, (
        f"strategy_rules.md Change Log versions {unclassified} are neither in "
        "STRATEGY_VERSION_REGISTRY nor DOCUMENTATION_ONLY_VERSIONS. A behavioural/"
        "parameter change must be registered in the same commit; a documentation-"
        "only change must be listed as such (2026-10-06 coverage rule)."
    )


def test_no_version_is_both_registered_and_documentation_only():
    registered = {e["version"] for e in STRATEGY_VERSION_REGISTRY}
    assert not registered & DOCUMENTATION_ONLY_VERSIONS


def test_registry_and_classification_only_name_real_change_log_versions():
    log = _change_log()
    registered = {e["version"] for e in STRATEGY_VERSION_REGISTRY}
    assert registered <= set(log)
    assert DOCUMENTATION_ONLY_VERSIONS <= set(log)


def test_registered_effective_dates_match_change_log():
    log = _change_log()
    for entry in STRATEGY_VERSION_REGISTRY:
        assert entry["effective_date"] == log[entry["version"]], entry["version"]


def test_registry_is_in_version_order():
    versions = [e["version"] for e in STRATEGY_VERSION_REGISTRY]
    assert versions == sorted(versions, key=_key)


def test_current_version_is_the_latest_behavioural_version():
    log = _change_log()
    behavioural = [v for v in log if v not in DOCUMENTATION_ONLY_VERSIONS]
    assert get_current_strategy_version() == max(behavioural, key=_key)


def test_only_grandfathered_entries_are_non_behavioural_registrations():
    text = (ROOT / "claude" / "strategy" / "strategy_rules.md").read_text()
    for entry in STRATEGY_VERSION_REGISTRY:
        row = re.search(rf"^\| {re.escape(entry['version'])} \|.*$", text, re.M).group(0)
        if "No behavioural rules changed" in row:
            assert entry["version"] in GRANDFATHERED_NON_BEHAVIOURAL, entry["version"]


def test_resolve_version_window_returns_none_for_unknown_version():
    assert resolve_version_window("9.9") is None


def test_resolve_version_window_open_ended_for_latest_version():
    start, end = resolve_version_window("1.15")
    assert start == date(2026, 10, 9)
    assert end is None


def test_resolve_version_window_1_4_closed_by_1_15():
    # ST-16 (v9.11): 1.4's window, open-ended until then, now ends where 1.15 starts.
    start, end = resolve_version_window("1.4")
    assert start == date(2026, 5, 20)
    assert end == date(2026, 10, 9)


def test_resolve_version_window_bounded_for_middle_version():
    start, end = resolve_version_window("1.3")
    assert start == date(2026, 2, 19)
    assert end == date(2026, 5, 20)


def test_resolve_version_window_zero_width_for_same_day_superseded_version():
    # 1.1 and 1.2 share an effective date (2026-02-18) — 1.1 was superseded same-day.
    start, end = resolve_version_window("1.1")
    assert start == date(2026, 2, 18)
    assert end == date(2026, 2, 18)
    assert start == end
