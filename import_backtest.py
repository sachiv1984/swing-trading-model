#!/usr/bin/env python3
"""
import_backtest.py — Import production_strategy.py backtest results into the live system.

ST-11 (BLG-FEAT-53, EPIC-03, v6.3)

Usage:
    python import_backtest.py [--api-url URL] [--api-key KEY] [--results-dir PATH]

Reads the latest all_trades_*.csv and yearly_performance_*.csv from production_results/
and POSTs the parsed data to POST /strategy/benchmark/import.

Defaults:
    --api-url    http://localhost:8000  (or REACT_APP_API_BASE_URL env var)
    --api-key    (reads from RENDER_API_KEY env var or ~/.api_keys)
    --results-dir  production_results/
"""

import os
import sys
import glob
import json
import argparse
import requests
import csv
from pathlib import Path
from typing import Optional


# BLG-BE-60 / RISK-01 (v7.1 ST-02) — fix vehicle selected at execution kickoff
# by the Backend Engineering Patterns Owner: option (c), "wire the existing
# drift-check output into an actual alert/threshold". Options (a) persistent
# historical-price caching (only extend forward, never re-download/re-simulate
# the full 8-year window) and (b) an append-only trade ledger both fix the
# root cause more completely but require substantially more infrastructure
# (a price cache store, or ledger diffing against what's already in the DB);
# both remain open follow-on work. Option (c) is the scoped, testable minimum:
# a total_pnl_gbp swing this large with zero new closed trades in the same
# run is not explainable by genuine trading activity, so it is surfaced
# loudly (distinct process exit code + a fixed, greppable log line) instead
# of being silently logged as before. See qa_evidence_EPIC-01.md for the
# fuller fix-vehicle rationale.
DRIFT_ALERT_THRESHOLD_GBP = 50.0


def check_drift_alert(
    trades_imported: int,
    trades_deleted: int,
    delta: Optional[float],
    threshold_gbp: float = DRIFT_ALERT_THRESHOLD_GBP,
) -> Optional[str]:
    """Return an alert message if an unexplained total_pnl_gbp swing is
    detected on a run with zero new closed trades, else None.

    Pure function — no I/O — so it is directly unit-testable without mocking
    the HTTP import round-trip (tests/test_nightly_computations.py).
    """
    if delta is None:
        return None
    zero_new_exits = trades_imported == trades_deleted
    if zero_new_exits and abs(delta) > threshold_gbp:
        return (
            f"BACKTEST_DRIFT_ALERT: total_pnl_gbp shifted by £{delta:,.2f} with "
            f"zero new closed trades this run (trades_imported={trades_imported} "
            f"== trades_deleted={trades_deleted}). Threshold: £{threshold_gbp:,.2f}. "
            "Likely cause: a historical price revision (e.g. yfinance auto_adjust) "
            "globally rescaled the compounding cash trajectory. See BLG-BE-60 / "
            "RISK-01 for the known root cause and fix-vehicle options."
        )
    return None


def find_latest_csv(directory: Path, pattern: str) -> Path | None:
    """Return the most recently modified file matching the glob pattern."""
    matches = glob.glob(str(directory / pattern))
    if not matches:
        return None
    return Path(max(matches, key=os.path.getmtime))


def load_api_key_from_file() -> str | None:
    """Read RENDER_API_KEY from ~/.api_keys if present."""
    api_keys_path = Path.home() / ".api_keys"
    if not api_keys_path.exists():
        return None
    with open(api_keys_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("export RENDER_API_KEY=") or line.startswith("RENDER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def parse_trades_csv(path: Path) -> list:
    """Parse all_trades_*.csv into the request body 'trades' array.

    Rows with Exit Reason "Open (Unrealized)" describe positions still held when
    production_strategy.py's price data ended, not completed round trips. The
    Strategy Benchmark page's win-rate/PnL aggregates assume closed trades, so
    these are excluded here rather than silently changing that page's semantics.
    (They are captured separately by parse_open_positions_csv — ST-08, BLG-FEAT-54.)
    """
    trades = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Exit Reason", "").strip() == "Open (Unrealized)":
                continue
            try:
                entry_year = int(row.get("Entry Year", 0) or 0)
                pnl_pct_raw = row.get("PnL %", "0")
                pnl_gbp_raw = row.get("PnL (£)", "0")
                holding_raw = row.get("Holding Days", "0")
                trades.append({
                    "ticker": row["Ticker"].strip(),
                    "entry_date": row["Entry Date"].strip(),
                    "exit_date": row["Exit Date"].strip(),
                    "holding_days": int(float(holding_raw)) if holding_raw else None,
                    "entry_price": float(row["Entry"]) if row.get("Entry") else None,
                    "exit_price": float(row["Exit"]) if row.get("Exit") else None,
                    "pnl_gbp": float(pnl_gbp_raw) if pnl_gbp_raw else None,
                    "pnl_pct": float(pnl_pct_raw) if pnl_pct_raw else None,
                    "market": row.get("Market", "US").strip() or "US",
                    "exit_reason": row.get("Exit Reason", "").strip() or None,
                    "was_profitable": row.get("Was Profitable", "").strip().lower() == "true",
                    "entry_year": entry_year,
                })
            except (KeyError, ValueError) as exc:
                print(f"  Warning: skipping row {row} — {exc}", file=sys.stderr)
    return trades


def parse_open_positions_csv(path: Path) -> list:
    """Parse all_trades_*.csv rows with Exit Reason "Open (Unrealized)" into
    the request body 'open_positions' array (ST-08, BLG-FEAT-54, EPIC-03, v6.4).

    production_strategy.py reuses the "Exit" column to record the current mark
    price (not a real exit) for positions still held when its price data ended.
    """
    open_positions = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Exit Reason", "").strip() != "Open (Unrealized)":
                continue
            try:
                pnl_pct_raw = row.get("PnL %", "0")
                pnl_gbp_raw = row.get("PnL (£)", "0")
                open_positions.append({
                    "ticker": row["Ticker"].strip(),
                    "entry_date": row["Entry Date"].strip(),
                    "entry_price": float(row["Entry"]) if row.get("Entry") else None,
                    "current_price": float(row["Exit"]) if row.get("Exit") else None,
                    "unrealized_pnl_gbp": float(pnl_gbp_raw) if pnl_gbp_raw else None,
                    "unrealized_pnl_pct": float(pnl_pct_raw) if pnl_pct_raw else None,
                    "market": row.get("Market", "US").strip() or "US",
                })
            except (KeyError, ValueError) as exc:
                print(f"  Warning: skipping open position row {row} — {exc}", file=sys.stderr)
    return open_positions


def parse_yearly_csv(path: Path) -> list:
    """Parse yearly_performance_*.csv into the request body 'yearly_performance' array."""
    yearly = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                yearly.append({
                    "entry_year": int(row["Entry Year"]),
                    "num_trades": int(row["Num Trades"]) if row.get("Num Trades") else None,
                    "avg_pnl_gbp": float(row["Avg PnL (£)"]) if row.get("Avg PnL (£)") else None,
                    "total_pnl_gbp": float(row["Total PnL (£)"]) if row.get("Total PnL (£)") else None,
                    "avg_hold_days": float(row["Avg Hold Days"]) if row.get("Avg Hold Days") else None,
                    "win_rate_pct": float(row["Win Rate %"]) if row.get("Win Rate %") else None,
                })
            except (KeyError, ValueError) as exc:
                print(f"  Warning: skipping yearly row {row} — {exc}", file=sys.stderr)
    return yearly


def main():
    parser = argparse.ArgumentParser(description="Import backtest CSVs into the trading assistant API")
    parser.add_argument("--api-url", default=None, help="API base URL (default: http://localhost:8000)")
    parser.add_argument("--api-key", default=None, help="X-API-Key value")
    parser.add_argument("--results-dir", default=None, help="Path to production_results/ directory")
    args = parser.parse_args()

    # Resolve API URL
    api_url = (
        args.api_url
        or os.getenv("REACT_APP_API_BASE_URL")
        or "http://localhost:8000"
    ).rstrip("/")

    # Resolve API key
    api_key = (
        args.api_key
        or os.getenv("RENDER_API_KEY")
        or load_api_key_from_file()
    )
    if not api_key:
        print("Error: no API key found. Set RENDER_API_KEY or pass --api-key.", file=sys.stderr)
        sys.exit(1)

    # Resolve results directory
    script_dir = Path(__file__).parent
    results_dir = Path(args.results_dir) if args.results_dir else script_dir / "production_results"
    if not results_dir.exists():
        print(f"Error: results directory not found: {results_dir}", file=sys.stderr)
        sys.exit(1)

    # Find latest CSVs
    trades_csv = find_latest_csv(results_dir, "all_trades_*.csv")
    yearly_csv = find_latest_csv(results_dir, "yearly_performance_*.csv")

    if not trades_csv:
        print(f"Error: no all_trades_*.csv found in {results_dir}", file=sys.stderr)
        sys.exit(1)
    if not yearly_csv:
        print(f"Error: no yearly_performance_*.csv found in {results_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Using trades CSV:  {trades_csv.name}")
    print(f"Using yearly CSV:  {yearly_csv.name}")

    # Parse
    print("Parsing trades…")
    trades = parse_trades_csv(trades_csv)
    print(f"  {len(trades)} trade records parsed")

    print("Parsing open positions…")
    open_positions = parse_open_positions_csv(trades_csv)
    print(f"  {len(open_positions)} open position records parsed")

    print("Parsing yearly performance…")
    yearly = parse_yearly_csv(yearly_csv)
    print(f"  {len(yearly)} yearly records parsed")

    # POST to import endpoint
    endpoint = f"{api_url}/strategy/benchmark/import"
    print(f"Importing to {endpoint}…")

    resp = requests.post(
        endpoint,
        headers={"X-API-Key": api_key, "Content-Type": "application/json"},
        data=json.dumps({"trades": trades, "yearly_performance": yearly, "open_positions": open_positions}),
        timeout=300,
    )

    if resp.status_code != 200:
        print(f"Error: server returned {resp.status_code}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    print("Import complete:")
    print(f"  trades_deleted:          {result.get('trades_deleted', 'n/a')}")
    print(f"  trades_imported:         {result['trades_imported']}")
    print(f"  open_positions_deleted:  {result.get('open_positions_deleted', 'n/a')}")
    print(f"  open_positions_imported: {result.get('open_positions_imported', 'n/a')}")
    print(f"  years_deleted:           {result.get('years_deleted', 'n/a')}")
    print(f"  years_imported:          {result['years_imported']}")
    print(f"  imported_at:      {result['imported_at']}")

    prev_total = result.get("previous_total_pnl_gbp")
    delta = result.get("total_pnl_gbp_delta")
    prev_unrealized = result.get("previous_total_unrealized_pnl_gbp")
    if prev_total is not None:
        print("\nTotal P&L drift check (vs previous import):")
        print(f"  previous total_pnl_gbp:            £{prev_total:,.2f}")
        print(f"  delta this import:                 £{delta:,.2f}")
        print(f"  previous total_unrealized_pnl_gbp: "
              f"{'£' + format(prev_unrealized, ',.2f') if prev_unrealized is not None else 'n/a'}")
        print("  (delta should track previous unrealized P&L, less any exit fees, "
              "if only positions closed — a larger swing warrants a closer look)")

        alert = check_drift_alert(result["trades_imported"], result["trades_deleted"], delta)
        if alert:
            print(f"\n{alert}", file=sys.stderr)
            # Distinct from exit code 1 (hard failure, nothing was imported):
            # the import already succeeded and committed, this exit code only
            # flags that the imported totals warrant a closer look.
            sys.exit(2)


if __name__ == "__main__":
    main()
