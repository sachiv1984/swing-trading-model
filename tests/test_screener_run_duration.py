"""
ST-32 (BLG-OPS-23, EPIC-05, v9.13) — benchmark the full screener run.

The p50/p95 of a full-universe run is computed from run history, so each run
now records its duration: run_screener() times the run, _persist_run()
stores screener_runs.duration_seconds (DS-36), and GET /screener/history
returns it (null for runs before v9.13). scripts/screener_run_benchmark.py
turns that history into the p50/p95 and the >1.5x regression check.

The live measurement on a deployed environment is a staging/production
delegation; this file covers the recording and the computation.
"""
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import screener_run_benchmark as bench  # noqa: E402


def _db():
    cur = MagicMock()
    cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
    conn = MagicMock(__exit__=MagicMock(return_value=False))
    conn.__enter__ = MagicMock(return_value=conn)
    conn.cursor.return_value = cur_ctx
    return conn, cur


class TestRecording:
    def test_ensure_adds_duration_column(self):
        from services.screener_batch_service import ensure_screener_results_table
        conn, cur = _db()
        with patch("services.screener_batch_service.get_db", return_value=conn):
            ensure_screener_results_table()
        sql = " ".join(c[0][0] for c in cur.execute.call_args_list)
        assert "ADD COLUMN IF NOT EXISTS duration_seconds NUMERIC" in sql

    def test_persist_run_writes_duration(self):
        from services.screener_batch_service import _persist_run
        conn, cur = _db()
        with patch("services.screener_batch_service.get_db", return_value=conn):
            _persist_run("r1", "2026-10-27T22:00:00Z", 10, 2, "risk_on", "risk_on", duration_seconds=412.6)
        sql, params = cur.execute.call_args[0]
        assert "duration_seconds" in sql
        assert params[-1] == 412.6

    @pytest.mark.parametrize("stored,returned", [(412.6, 412.6), (None, None)])
    def test_history_returns_duration(self, stored, returned):
        from services.screener_batch_service import get_screener_run_history
        conn, cur = _db()
        cur.fetchone.return_value = {"cnt": 1}
        cur.fetchall.return_value = [{
            "run_id": "r1", "run_timestamp": datetime(2026, 10, 27, 22, 0), "tickers_requested": 520,
            "tickers_passed": 12, "regime_us": "risk_on", "regime_uk": "risk_off",
            "degraded_run": False, "failure_rate": 0.02, "duration_seconds": stored,
        }]
        with patch("services.screener_batch_service.get_db", return_value=conn):
            run = get_screener_run_history()["runs"][0]
        assert run["duration_seconds"] == returned
        assert "duration_seconds" in cur.execute.call_args_list[-1][0][0]


def _run(duration, degraded=False, total=520):
    return {"run_id": "r", "run_timestamp": "2026-10-27T22:00:00Z", "total_tickers": total,
            "degraded_run": degraded, "duration_seconds": duration}


class TestBenchmark:
    def test_percentiles_nearest_rank(self):
        assert bench.percentile([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 50) == 50
        assert bench.percentile([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 95) == 100
        assert bench.percentile([7.0], 95) == 7.0

    def test_only_full_timed_runs_count(self):
        runs = [_run(400), _run(None), _run(900, degraded=True), _run(30, total=5), _run(420)]
        assert [r["duration_seconds"] for r in bench.eligible_runs(runs, min_tickers=500)] == [400, 420]

    def test_summary_and_threshold(self):
        runs = [_run(d) for d in [400, 410, 420, 430, 440, 450, 460, 470, 480, 600]]
        summary = bench.summarise(runs, min_tickers=500)
        assert summary["runs"] == 10
        assert (summary["p50_seconds"], summary["p95_seconds"]) == (440, 600)
        assert summary["regression_threshold_seconds"] == 660.0

    def test_too_few_runs_is_reported_not_guessed(self):
        summary = bench.summarise([_run(400)] * 3, min_tickers=500, min_runs=10)
        assert summary["sufficient"] is False and summary["runs"] == 3

    def test_default_min_tickers_is_90_percent_of_the_largest_run(self):
        runs = [_run(400, total=520), _run(410, total=470), _run(50, total=100)]
        assert bench.default_min_tickers(runs) == 468
        assert bench.summarise(runs, min_runs=1)["runs"] == 2

    def test_regression_check(self):
        assert bench.is_regression(661, p50=440) is True
        assert bench.is_regression(660, p50=440) is False
