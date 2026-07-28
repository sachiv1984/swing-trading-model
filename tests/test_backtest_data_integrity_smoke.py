"""
Tests for scripts/backtest_data_integrity_smoke_test.py — ST-07 (EPIC-07, v7.9, BLG-BE-74).

Exercises the detection logic against synthetic violation cases (proving
the checks actually catch the invariant class from BLG-BE-59/60/63), and
against the real, checked-in production_results/all_trades_*.csv to
confirm the smoke test passes on current data (AC-02).
"""

import glob
import importlib.util
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "backtest_data_integrity_smoke_test.py"
spec = importlib.util.spec_from_file_location("backtest_data_integrity_smoke_test", SCRIPT_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules["backtest_data_integrity_smoke_test"] = mod
spec.loader.exec_module(mod)


def test_no_duplicates_is_clean():
    trades = [
        {"ticker": "AAPL", "entry_date": "2026-01-01", "exit_date": "2026-01-05"},
        {"ticker": "AAPL", "entry_date": "2026-02-01", "exit_date": "2026-02-05"},
    ]
    assert mod.check_no_duplicate_trades(trades) == []


def test_duplicate_trade_is_flagged():
    """BLG-BE-63 class: a duplicate (ticker, entry_date, exit_date) round trip
    must be caught — this is exactly the shape of the idempotency defect the
    v7.7 audit checked for."""
    trades = [
        {"ticker": "AAPL", "entry_date": "2026-01-01", "exit_date": "2026-01-05"},
        {"ticker": "AAPL", "entry_date": "2026-01-01", "exit_date": "2026-01-05"},
    ]
    violations = mod.check_no_duplicate_trades(trades)
    assert len(violations) == 1
    assert "AAPL" in violations[0]


def test_point_in_time_violation_is_flagged():
    """BLG-BE-59 class: a trade entered before the ticker's created_at cutoff
    must be caught."""
    trades = [{"ticker": "NEWCO", "entry_date": "2026-01-01", "exit_date": "2026-01-05", "exit_reason": ""}]
    ticker_created_at = {"NEWCO": "2026-01-15"}
    violations = mod.check_point_in_time_eligibility(trades, ticker_created_at)
    assert len(violations) == 1
    assert "NEWCO" in violations[0]


def test_point_in_time_compliant_trade_passes():
    trades = [{"ticker": "NEWCO", "entry_date": "2026-02-01", "exit_date": "2026-02-05", "exit_reason": ""}]
    ticker_created_at = {"NEWCO": "2026-01-15"}
    assert mod.check_point_in_time_eligibility(trades, ticker_created_at) == []


def test_ungated_ticker_is_not_flagged():
    """A ticker with created_at=None (legacy CSV-sourced universe row) is not
    gated — matches production_strategy.py's own masking semantics."""
    trades = [{"ticker": "LEGACY", "entry_date": "2018-01-01", "exit_date": "2018-01-05", "exit_reason": ""}]
    ticker_created_at = {"LEGACY": None}
    assert mod.check_point_in_time_eligibility(trades, ticker_created_at) == []


def test_smoke_test_passes_on_real_checked_in_data():
    """AC-02: passes on current data — run against the actual, most recent
    production_results/all_trades_*.csv checked into this repo."""
    results_dir = REPO_ROOT / "production_results"
    matches = glob.glob(str(results_dir / "all_trades_*.csv"))
    assert matches, "expected at least one all_trades_*.csv in production_results/"
    latest = Path(max(matches, key=os.path.getmtime))

    trades = mod.load_trades(latest)
    assert len(trades) > 0

    duplicates = mod.check_no_duplicate_trades(trades)
    assert duplicates == [], f"real backtest data has duplicate trades: {duplicates}"


def test_run_smoke_test_returns_zero_on_real_data(capsys):
    results_dir = REPO_ROOT / "production_results"
    matches = glob.glob(str(results_dir / "all_trades_*.csv"))
    latest = Path(max(matches, key=os.path.getmtime))
    assert mod.run_smoke_test(latest) == 0


def test_run_smoke_test_returns_nonzero_on_injected_duplicate(tmp_path):
    """End-to-end: write a CSV with a deliberately duplicated trade row and
    confirm the smoke test fails on it (mirrors the deliberately-missing-case
    pattern used elsewhere this sprint for AC-02-style verification)."""
    csv_path = tmp_path / "all_trades_test.csv"
    header = "Ticker,Entry Date,Exit Date,Holding Days,Entry,Exit,PnL (£),PnL %,Market,Exit Reason,Was Profitable,Entry Year\n"
    row = "AAPL,2026-01-01,2026-01-05,4,100.0,105.0,50.0,5.0,US,Target Reached,True,2026\n"
    csv_path.write_text(header + row + row)  # same row twice — injected duplicate

    assert mod.run_smoke_test(csv_path) == 1
