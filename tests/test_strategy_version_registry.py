"""Tests for backend/strategy_version_registry.py (SI-04, ST-01, EPIC-01, v7.7, BLG-FEAT-75)."""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from strategy_version_registry import resolve_version_window, STRATEGY_VERSION_REGISTRY


def test_registry_matches_strategy_rules_change_log_count():
    # strategy_rules.md Change Log has 5 entries (1.0-1.4) as of v7.7.
    assert len(STRATEGY_VERSION_REGISTRY) == 5


def test_resolve_version_window_returns_none_for_unknown_version():
    assert resolve_version_window("9.9") is None


def test_resolve_version_window_open_ended_for_latest_version():
    start, end = resolve_version_window("1.4")
    assert start == date(2026, 5, 20)
    assert end is None


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
