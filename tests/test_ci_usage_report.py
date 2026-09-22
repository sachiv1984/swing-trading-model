"""
ST-17 (BLG-OPS-165, EPIC-04, v9.6): CI minutes and artifact-storage
visibility.

Tests the pure logic in scripts/generate_ci_usage_report.py directly (no
`gh api` calls needed -- estimate_workflow_minutes(), workflow_for_artifact_name(),
aggregate_artifact_storage(), and previous_month_window() all take/return
plain values).
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_ci_usage_report import (  # noqa: E402
    aggregate_artifact_storage,
    artifact_undercount_caveat,
    estimate_workflow_minutes,
    previous_month_window,
    render_markdown,
    workflow_for_artifact_name,
)


def test_estimate_workflow_minutes_averages_sample_and_scales_by_exact_count():
    # sample: 2 min, 4 min -> avg 3 min/run; 100 actual runs -> 300 est. minutes
    avg_minutes, estimated_total, sample_size = estimate_workflow_minutes(
        sample_duration_ms=[120_000, 240_000], total_run_count=100
    )
    assert avg_minutes == 3.0
    assert estimated_total == 300.0
    assert sample_size == 2


def test_estimate_workflow_minutes_empty_sample_is_zero_not_a_crash():
    avg_minutes, estimated_total, sample_size = estimate_workflow_minutes(
        sample_duration_ms=[], total_run_count=50
    )
    assert avg_minutes == 0.0
    assert estimated_total == 0.0
    assert sample_size == 0


def test_workflow_for_artifact_name_matches_known_prefixes():
    assert workflow_for_artifact_name("playwright-report-shard-2") == "Playwright E2E Acceptance Tests"
    assert workflow_for_artifact_name("visual-snapshot-report") == "Playwright E2E Acceptance Tests"
    assert workflow_for_artifact_name("visual-regression-report") == "Playwright E2E Acceptance Tests"
    assert workflow_for_artifact_name("smoke-test-report") == "Critical-Path Smoke Tests (Playwright)"
    assert workflow_for_artifact_name("db-backup-123456") == "Production Database Backup"
    assert workflow_for_artifact_name("updated-visual-snapshots") == "Update Visual Snapshot Baselines"


def test_workflow_for_artifact_name_unrecognized_is_none_not_fabricated():
    """An artifact name that matches no known upload step must not be
    silently attributed to some guessed workflow -- the caller groups it
    under "(unmapped artifact)" instead."""
    assert workflow_for_artifact_name("some-future-artifact-nobody-documented") is None


def test_aggregate_artifact_storage_sums_by_workflow_and_groups_unmapped():
    artifacts = [
        {"name": "playwright-report-shard-1", "size_in_bytes": 10 * 1024 * 1024},
        {"name": "playwright-report-shard-2", "size_in_bytes": 5 * 1024 * 1024},
        {"name": "db-backup-999", "size_in_bytes": 2 * 1024 * 1024},
        {"name": "mystery-artifact", "size_in_bytes": 1024 * 1024},
    ]
    result = aggregate_artifact_storage(artifacts)
    assert result["Playwright E2E Acceptance Tests"] == 15.0
    assert result["Production Database Backup"] == 2.0
    assert result["(unmapped artifact)"] == 1.0


def test_previous_month_window_handles_january_year_rollover():
    now = datetime(2026, 1, 15, tzinfo=timezone.utc)
    start, end, label = previous_month_window(now)
    assert start == "2025-12-01"
    assert end == "2025-12-31"
    assert label == "2025-12"


def test_previous_month_window_handles_ordinary_month():
    now = datetime(2026, 9, 22, tzinfo=timezone.utc)
    start, end, label = previous_month_window(now)
    assert start == "2026-08-01"
    assert end == "2026-08-31"
    assert label == "2026-08"


def test_previous_month_window_handles_leap_february():
    now = datetime(2028, 3, 5, tzinfo=timezone.utc)  # 2028 is a leap year
    start, end, label = previous_month_window(now)
    assert start == "2028-02-01"
    assert end == "2028-02-29"
    assert label == "2028-02"


def test_render_markdown_sorts_by_minutes_descending_and_includes_totals():
    report = {
        "Small Workflow": {"run_count": 1, "estimated_minutes": 0.5, "sample_size": 1},
        "Big Workflow": {"run_count": 5, "estimated_minutes": 42.0, "sample_size": 5},
    }
    md = render_markdown(report, {}, "2026-08", sample_size=5)
    big_idx = md.index("Big Workflow")
    small_idx = md.index("Small Workflow")
    assert big_idx < small_idx
    assert "42.5" in md  # total minutes: 42.0 + 0.5
    assert "2026-08" in md


def test_render_markdown_includes_artifact_only_workflow_row():
    """A workflow with artifact storage but no runs counted this window
    (edge case) must still appear, with run_count 0, not be dropped."""
    md = render_markdown({}, {"Production Database Backup": 90.0}, "2026-08", sample_size=5)
    assert "Production Database Backup" in md
    assert "90.0" in md


def test_artifact_undercount_caveat_empty_for_recent_window():
    """A window closed only 2 days ago is within every known artifact
    type's retention -- no caveat needed."""
    assert artifact_undercount_caveat(days_since_window_end=2) == ""


def test_artifact_undercount_caveat_none_when_not_computed():
    assert artifact_undercount_caveat(days_since_window_end=None) == ""


def test_artifact_undercount_caveat_flags_only_expired_categories():
    """21 days since window close: the 7d and 14d retention workflows are
    stale (expired), the 30d and 90d ones are not -- both must be named
    correctly, not lumped together."""
    caveat = artifact_undercount_caveat(days_since_window_end=21)
    assert "Update Visual Snapshot Baselines" in caveat  # 7d retention
    assert "Playwright E2E Acceptance Tests" in caveat  # 14d retention (also covers 30d prefixes)
    assert "Critical-Path Smoke Tests (Playwright)" in caveat  # 14d retention
    assert "Production Database Backup" not in caveat  # 90d retention, not yet stale


def test_artifact_undercount_caveat_flags_all_categories_when_very_stale():
    caveat = artifact_undercount_caveat(days_since_window_end=100)
    assert "Production Database Backup" in caveat  # even the 90d retention is now stale
