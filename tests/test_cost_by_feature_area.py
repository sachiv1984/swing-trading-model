"""
ST-39 (BLG-OPS-85, EPIC-06, v9.14) — cost by feature area.

scripts/cost_by_feature_area.py partitions a month's cost into AI endpoints,
screener and core CRUD from claude_audit_log and api_call_log, and allocates
the shared Render dyno charge by work-unit share
(docs/ops/cost_by_feature_area.md). AC 1 (the report and its allocation
method) is checked here; AC 2 (populated with a complete month of
production data) is post-merge, tracked by BLG-OPS-201.
"""
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "cost_by_feature_area.py"
spec = importlib.util.spec_from_file_location("cost_by_feature_area", SCRIPT)
cbfa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cbfa)


@pytest.mark.parametrize("feature,area", [
    ("POST /ai/daily-briefing", "ai"),
    ("GET /ai/journal-summary/history", "ai"),
    ("POST /trade-plans/generate-plan", "ai"),
    ("POST /trade-plans/{plan_id}/generate-thesis", "ai"),
    ("POST /reports/monthly-pnl/narrative", "ai"),
    ("POST /trades/{trade_id}/debrief", "ai"),
    ("POST /screener/run", "screener"),
    ("GET /screener/results", "screener"),
    ("PUT /ticker-universe/{ticker}", "screener"),
    ("GET /positions", "core"),
    ("GET /reports/monthly-pnl", "core"),
    ("GET /trade-plans/{plan_id}", "core"),
    ("GET /screenerish", "core"),
    ("unattributed", "unattributed"),
    (None, "unattributed"),
])
def test_classify(feature, area):
    assert cbfa.classify(feature) == area


def test_month_bounds_cover_the_whole_month_including_december():
    assert [d.isoformat() for d in cbfa.month_bounds("2026-11")] == ["2026-11-01", "2026-12-01"]
    assert [d.isoformat() for d in cbfa.month_bounds("2026-12")] == ["2026-12-01", "2027-01-01"]


def test_partition_direct_costs_and_dyno_allocation():
    claude = [("POST /ai/chat", 30, 0.06, 90000), ("POST /trade-plans/generate-plan", 10, 0.02, 30000)]
    market = [
        ("POST /screener/run", "alpaca_data", 500, 4),
        ("POST /screener/run", "yahoo", 300, 10),
        ("GET /positions", "yahoo", 120, 0),
        ("POST /ai/daily-briefing", "yahoo", 10, 0),
        ("unattributed", "yahoo", 40, 1),
    ]
    out = cbfa.partition(claude, market, {"yahoo": 0.0, "alpaca_data": 0.001}, 10.0)
    assert out["ai"]["claude_calls"] == 40 and round(out["ai"]["claude_cost_usd"], 6) == 0.08
    assert out["ai"]["claude_latency_s"] == 120.0
    assert out["ai"]["market_calls"] == 10
    assert out["screener"]["market_calls"] == 800 and out["screener"]["market_failures"] == 14
    assert round(out["screener"]["market_cost_usd"], 6) == 0.5
    assert out["core"]["market_calls"] == 120 and out["unattributed"]["market_calls"] == 40
    # 50 + 800 + 120 + 40 = 1010 work units share the $10 dyno charge.
    assert out["screener"]["work_units"] == 800
    assert round(out["screener"]["render_share_usd"], 4) == round(10 * 800 / 1010, 4)
    assert round(sum(v["render_share_usd"] for v in out.values()), 9) == 10.0
    assert round(out["screener"]["total_usd"], 4) == round(0.5 + 10 * 800 / 1010, 4)


def test_empty_month_has_no_division_by_zero():
    out = cbfa.partition([], [], {}, 7.0)
    assert all(v["work_unit_share"] == 0.0 and v["render_share_usd"] == 0.0 for v in out.values())


def test_markdown_has_a_row_per_area_and_a_total():
    out = cbfa.partition([("POST /ai/chat", 2, 0.004, 1000)], [("GET /positions", "yahoo", 2, 0)], {}, None)
    md = cbfa.render_markdown("2026-11", out, None, "2026-12-02")
    assert md.startswith("### 2026-11\n")
    for label in cbfa.AREA_LABELS.values():
        assert f"| {label} |" in md
    assert "| **Total** | 2 | $0.0040 | 2 (0) |" in md
    assert "not given" in md


def test_queries_are_bounded_reads_of_the_two_tables():
    assert "FROM claude_audit_log" in cbfa.CLAUDE_SQL and "generated_at < %s" in cbfa.CLAUDE_SQL
    assert "FROM api_call_log" in cbfa.MARKET_SQL and "called_at < %s" in cbfa.MARKET_SQL
    src = SCRIPT.read_text()
    assert "SET TRANSACTION READ ONLY" in src
    for verb in ("INSERT", "UPDATE ", "DELETE", "DROP"):
        assert verb not in cbfa.CLAUDE_SQL + cbfa.MARKET_SQL


def test_month_argument_is_validated():
    with pytest.raises(SystemExit):
        cbfa.main(["--month", "2026-13"])
