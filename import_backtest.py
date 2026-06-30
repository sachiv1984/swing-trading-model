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
    """Parse all_trades_*.csv into the request body 'trades' array."""
    trades = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
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

    print("Parsing yearly performance…")
    yearly = parse_yearly_csv(yearly_csv)
    print(f"  {len(yearly)} yearly records parsed")

    # POST to import endpoint
    endpoint = f"{api_url}/strategy/benchmark/import"
    print(f"Importing to {endpoint}…")

    resp = requests.post(
        endpoint,
        headers={"X-API-Key": api_key, "Content-Type": "application/json"},
        data=json.dumps({"trades": trades, "yearly_performance": yearly}),
        timeout=60,
    )

    if resp.status_code != 200:
        print(f"Error: server returned {resp.status_code}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    print("Import complete:")
    print(f"  trades_imported:  {result['trades_imported']}")
    print(f"  years_imported:   {result['years_imported']}")
    print(f"  imported_at:      {result['imported_at']}")


if __name__ == "__main__":
    main()
