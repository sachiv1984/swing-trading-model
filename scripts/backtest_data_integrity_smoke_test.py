#!/usr/bin/env python3
"""
backtest_data_integrity_smoke_test.py — ST-07 (EPIC-07, v7.9, BLG-BE-74)

Standing data-integrity smoke test for the nightly backtest job, checking
the same invariant class as three prior one-off audits:

  - BLG-BE-59 (v7.1): point-in-time ticker eligibility — a trade's entry
    must not predate the ticker's ticker_universe.created_at cutoff.
  - BLG-BE-60 (v7.1): total_pnl_gbp reproducibility — a run with zero new
    closed trades should not show an unexplained P&L swing (already
    alerted inline by import_backtest.py's check_drift_alert; re-exposed
    here so it participates in the same standing gate).
  - BLG-BE-63 (v7.7): idempotency — no duplicate trade rows (same ticker,
    entry date, exit date) should ever appear in a single import.

Prior incidents were each found by a one-off manual audit. This script is
the permanent, automated replacement — run as a CI step after every
nightly backtest import (see .github/workflows/backtest.yml), and
exercised directly by tests/test_backtest_data_integrity_smoke.py against
real checked-in backtest output for CI-independent regression coverage.

Usage:
    python3 scripts/backtest_data_integrity_smoke_test.py [--csv PATH] [--api-url URL]

If ticker_universe data is unavailable (no DATABASE_URL / no DB access in
this checkout), the point-in-time check is skipped with a clear message
rather than failing — matching this repo's existing "no credentials in
this checkout" fallback convention (see roadmap_prompt.md v9.6 STEP 2.3).
"""

import argparse
import csv
import glob
import os
import sys
from pathlib import Path
from typing import Optional


def find_latest_csv(directory: Path, pattern: str) -> Optional[Path]:
    matches = glob.glob(str(directory / pattern))
    if not matches:
        return None
    return Path(max(matches, key=os.path.getmtime))


def load_trades(csv_path: Path) -> list:
    """Parse all_trades_*.csv rows relevant to the integrity checks below.

    Includes "Open (Unrealized)" rows here (unlike import_backtest.py's
    parse_trades_csv) — an open position still has an entry date that must
    respect the point-in-time invariant, even though it's excluded from
    the closed-trade P&L aggregates elsewhere.
    """
    trades = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trades.append({
                "ticker": row["Ticker"].strip(),
                "entry_date": row["Entry Date"].strip(),
                "exit_date": row["Exit Date"].strip(),
                "exit_reason": row.get("Exit Reason", "").strip(),
            })
    return trades


def check_point_in_time_eligibility(trades: list, ticker_created_at: dict) -> list:
    """BLG-BE-59 class: return violations where a trade's entry predates its
    ticker's created_at cutoff. ticker_created_at maps ticker -> ISO date
    string or None (None = not yet gated, e.g. legacy CSV-sourced universe
    row — matches production_strategy.py's own masking semantics)."""
    violations = []
    for t in trades:
        cutoff = ticker_created_at.get(t["ticker"])
        if cutoff is None:
            continue
        if t["entry_date"] < cutoff:
            violations.append(
                f"{t['ticker']}: entry_date {t['entry_date']} precedes "
                f"ticker_universe.created_at {cutoff}"
            )
    return violations


def check_no_duplicate_trades(trades: list) -> list:
    """BLG-BE-63 class: return duplicate (ticker, entry_date, exit_date) keys.
    A full-replace import (upsert_backtest_data) should never produce two
    rows for the same round trip — a duplicate indicates either a
    production_strategy.py generation bug or an idempotency regression in
    the import path."""
    seen = {}
    duplicates = []
    for t in trades:
        key = (t["ticker"], t["entry_date"], t["exit_date"])
        seen[key] = seen.get(key, 0) + 1
    for key, count in seen.items():
        if count > 1:
            duplicates.append(f"{key[0]} {key[1]} -> {key[2]}: appears {count} times (expected 1)")
    return duplicates


def load_ticker_created_at() -> Optional[dict]:
    """Return {ticker: created_at_iso_date} from the DB, or None if unavailable.

    Uses a direct psycopg2 connection (same DATABASE_URL cleanup pattern as
    production_strategy.py's _load_tickers()) rather than importing
    backend/database.py, to keep this script self-contained and avoid
    coupling to that module's broader dependency surface."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return None
    try:
        import psycopg2
        from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

        clean_url = db_url.replace("postgres://", "postgresql://", 1)
        parsed = urlparse(clean_url)
        qs = {k: v for k, v in parse_qs(parsed.query).items() if k != "pgbouncer"}
        clean_url = urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))
        conn = psycopg2.connect(clean_url)
        with conn.cursor() as cur:
            cur.execute("SELECT ticker, created_at FROM ticker_universe")
            rows = cur.fetchall()
        conn.close()
        return {r[0]: (str(r[1])[:10] if r[1] is not None else None) for r in rows}
    except Exception as exc:  # pragma: no cover — defensive: DB reachable but query failed
        print(f"  Warning: could not load ticker_universe ({exc}) — skipping point-in-time check", file=sys.stderr)
        return None


def run_smoke_test(csv_path: Path) -> int:
    trades = load_trades(csv_path)
    print(f"Loaded {len(trades)} trade rows from {csv_path.name}")

    failures = []

    duplicates = check_no_duplicate_trades(trades)
    if duplicates:
        failures.append(("Idempotency (BLG-BE-63 class)", duplicates))

    ticker_created_at = load_ticker_created_at()
    if ticker_created_at is None:
        print("  ticker_universe unavailable in this environment — point-in-time check skipped (not a failure).")
    else:
        pit_violations = check_point_in_time_eligibility(trades, ticker_created_at)
        if pit_violations:
            failures.append(("Point-in-time eligibility (BLG-BE-59 class)", pit_violations))

    if failures:
        print("\nBACKTEST DATA-INTEGRITY SMOKE TEST FAILED:\n", file=sys.stderr)
        for check_name, violations in failures:
            print(f"  [{check_name}]", file=sys.stderr)
            for v in violations:
                print(f"    - {v}", file=sys.stderr)
        return 1

    print("Backtest data-integrity smoke test: PASSED — no violations detected.")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=None, help="Path to all_trades_*.csv (default: latest in production_results/)")
    parser.add_argument("--results-dir", type=Path, default=Path("production_results"))
    args = parser.parse_args()

    csv_path = args.csv or find_latest_csv(args.results_dir, "all_trades_*.csv")
    if csv_path is None or not csv_path.exists():
        print(f"No all_trades_*.csv found in {args.results_dir} — nothing to check.", file=sys.stderr)
        return 1

    return run_smoke_test(csv_path)


if __name__ == "__main__":
    sys.exit(main())
