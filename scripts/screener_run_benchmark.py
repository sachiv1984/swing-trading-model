#!/usr/bin/env python3
"""
Full screener run benchmark: p50/p95 duration from run history.

ST-32 (BLG-OPS-23, EPIC-05, v9.13). Each screener run records
duration_seconds (DS-36), returned by GET /screener/history. This script
reads that history from a deployed environment and reports the p50 and p95
of full-universe runs, and the regression threshold: a run slower than
1.5 x the baseline p50 is a regression (docs/ops/api_performance_baseline.md).

A run counts when it has a duration, is not degraded (more than 20% of
tickers without data), and covered at least --min-tickers tickers, so a
partial universe or a broken data source does not skew the baseline. By
default --min-tickers is 90% of the largest run in the history, i.e. the
full universe as it stands.
Percentiles use the nearest-rank method.

Usage:
    API_URL=... API_KEY=... python3 scripts/screener_run_benchmark.py [--min-tickers N] [--min-runs 10] [--limit 200]

Exit code: 0 with a sufficient sample; 1 if fewer than --min-runs runs
qualify or the history cannot be read.
"""
import argparse
import json
import math
import os
import sys
from urllib.request import Request, urlopen

REGRESSION_MULTIPLIER = 1.5
FULL_UNIVERSE_FRACTION = 0.9


def percentile(values, pct):
    ordered = sorted(values)
    rank = max(1, math.ceil(pct / 100 * len(ordered)))
    return ordered[rank - 1]


def eligible_runs(runs, min_tickers):
    return [
        r for r in runs
        if r.get("duration_seconds") is not None
        and not r.get("degraded_run")
        and (r.get("total_tickers") or 0) >= min_tickers
    ]


def default_min_tickers(runs):
    largest = max((r.get("total_tickers") or 0 for r in runs), default=0)
    return math.ceil(largest * FULL_UNIVERSE_FRACTION)


def summarise(runs, min_tickers=None, min_runs=10):
    if min_tickers is None:
        min_tickers = default_min_tickers(runs)
    eligible = eligible_runs(runs, min_tickers)
    durations = [float(r["duration_seconds"]) for r in eligible]
    summary = {"runs": len(durations), "min_tickers": min_tickers, "sufficient": len(durations) >= min_runs}
    if durations:
        p50 = percentile(durations, 50)
        summary.update({
            "p50_seconds": p50,
            "p95_seconds": percentile(durations, 95),
            "regression_threshold_seconds": round(p50 * REGRESSION_MULTIPLIER, 1),
            "first_run": min(r["run_timestamp"] for r in eligible),
            "last_run": max(r["run_timestamp"] for r in eligible),
        })
    return summary


def is_regression(duration_seconds, p50):
    return duration_seconds > p50 * REGRESSION_MULTIPLIER


def fetch_history(api_url, api_key, limit):
    req = Request(f"{api_url.rstrip('/')}/screener/history?limit={limit}",
                  headers={"X-API-Key": api_key, "Accept": "application/json"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["data"]["runs"]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    parser.add_argument("--min-tickers", type=int, default=None)
    parser.add_argument("--min-runs", type=int, default=10)
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()
    api_url, api_key = os.getenv("API_URL", ""), os.getenv("API_KEY", "")
    if not api_url:
        print("API_URL is not set", file=sys.stderr)
        return 1
    try:
        runs = fetch_history(api_url, api_key, args.limit)
    except Exception as exc:
        print(f"Could not read screener history: {exc}", file=sys.stderr)
        return 1
    summary = summarise(runs, args.min_tickers, args.min_runs)
    print(json.dumps(summary, indent=2))
    if not summary["sufficient"]:
        print(f"Only {summary['runs']} qualifying runs; need {args.min_runs}.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
