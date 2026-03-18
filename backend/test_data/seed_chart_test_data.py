"""
seed_chart_test_data.py
=======================
Seeds the staging / PR preview database with 12 closed trades designed to
satisfy every precondition in docs/testing/chart_interactivity_scenarios.md
(ST-11 / SC-CHART-IX-*).

Usage:
    python seed_chart_test_data.py [BASE_URL]

    BASE_URL — root URL of the API, no trailing slash.
    Default: https://trading-assistant-staging.onrender.com

Examples:
    python seed_chart_test_data.py
    python seed_chart_test_data.py https://trading-assistant-api-pr-42.onrender.com

What it creates
---------------
  Jan 2026 — 4 trades   (AZN, SHEL, ULVR, BP.)
  Feb 2026 — 6 trades   (HSBA, VOD, GSK, RIO, LGEN, BT.A)
  Mar 2026 — 2 trades   (MKS, BATS)
  Apr 2026 — 0 trades   [zero-tile for SC-CHART-IX-01c]

R-multiple distribution — all 7 buckets populated:
  3R+        : GSK  (+3.0R)
  2R to 3R   : AZN  (+2.0R)  ULVR (+2.0R)  MKS (+2.0R)
  1R to 2R   : HSBA (+1.5R)
  0R to 1R   : LGEN (+0.5R)
  -1R to 0R  : BP.  (-1.0R)  VOD  (-0.5R)  RIO (-1.0R)
  -2R to -1R : SHEL (-1.5R)
  -3R+       : BT.A (-2.5R)  BATS (-3.0R)

  Total: 12 trades | Winners: 6 | Losers: 6 | Win rate: 50%

Scenario preconditions satisfied:
  SC-CHART-IX-01a : ≥1 closed trade in at least one calendar month  ✓
  SC-CHART-IX-01c : a tile with 0 trades (Apr 2026)                 ✓
  SC-CHART-IX-01d : known trade count per month (4 / 6 / 2)         ✓
  SC-CHART-IX-02  : > 4 closed trades total                         ✓
  SC-CHART-IX-04  : ≥ 3 trades                                      ✓
  SC-CHART-IX-05  : ≥ 10 trades with stop_price                     ✓ (all 12)

Notes for SC-CHART-IX-01d (data integrity verification):
  After seeding, open the heatmap and click each month tile.
  Count rows in the modal and note the displayed total P&L.
  The modal row count must match the trade count above (4 / 6 / 2).
  The modal total P&L must match the tile P&L exactly.
  (Exact GBP amounts depend on backend fee calculations — read from the UI.)
"""

import sys
import time
import requests

BASE_URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://trading-assistant-staging.onrender.com"

# ---------------------------------------------------------------------------
# Trade definitions.
# All UK stocks — prices in pence, no fx_rate needed.
# R = (exit_price - entry_price) / abs(entry_price - stop_price)
# stop_price must be < entry_price (long-only).
#
# _r      : expected R-multiple (for display only)
# _bucket : R-multiple histogram bucket (for display only)
# _month  : calendar month (for display only)
# ---------------------------------------------------------------------------
TRADES = [
    # ── January 2026 ── 4 trades ─────────────────────────────────────────
    {
        "ticker": "AZN", "market": "UK",
        "entry_date": "2026-01-06", "shares": 10,
        "entry_price": 11500, "stop_price": 11000,  # risk = 500p
        "exit_date": "2026-01-20", "exit_price": 12500, "exit_reason": "target",
        # R = (12500-11500)/500 = +2.0R
        "_r": "+2.0R", "_bucket": "2R to 3R", "_month": "Jan 2026",
    },
    {
        "ticker": "SHEL", "market": "UK",
        "entry_date": "2026-01-07", "shares": 10,
        "entry_price": 2600, "stop_price": 2400,  # risk = 200p
        "exit_date": "2026-01-21", "exit_price": 2300, "exit_reason": "stop_hit",
        # R = (2300-2600)/200 = -1.5R
        "_r": "-1.5R", "_bucket": "-2R to -1R", "_month": "Jan 2026",
    },
    {
        "ticker": "ULVR", "market": "UK",
        "entry_date": "2026-01-08", "shares": 25,
        "entry_price": 4200, "stop_price": 4000,  # risk = 200p
        "exit_date": "2026-01-22", "exit_price": 4600, "exit_reason": "target",
        # R = (4600-4200)/200 = +2.0R
        "_r": "+2.0R", "_bucket": "2R to 3R", "_month": "Jan 2026",
    },
    {
        "ticker": "BP.", "market": "UK",
        "entry_date": "2026-01-09", "shares": 100,
        "entry_price": 430, "stop_price": 400,  # risk = 30p
        "exit_date": "2026-01-23", "exit_price": 400, "exit_reason": "stop_hit",
        # R = (400-430)/30 = -1.0R
        "_r": "-1.0R", "_bucket": "-1R to 0R", "_month": "Jan 2026",
    },

    # ── February 2026 ── 6 trades ─────────────────────────────────────────
    {
        "ticker": "HSBA", "market": "UK",
        "entry_date": "2026-02-03", "shares": 200,
        "entry_price": 700, "stop_price": 650,  # risk = 50p
        "exit_date": "2026-02-17", "exit_price": 775, "exit_reason": "manual",
        # R = (775-700)/50 = +1.5R
        "_r": "+1.5R", "_bucket": "1R to 2R", "_month": "Feb 2026",
    },
    {
        "ticker": "VOD", "market": "UK",
        "entry_date": "2026-02-04", "shares": 500,
        "entry_price": 75, "stop_price": 65,  # risk = 10p
        "exit_date": "2026-02-18", "exit_price": 70, "exit_reason": "manual",
        # R = (70-75)/10 = -0.5R
        "_r": "-0.5R", "_bucket": "-1R to 0R", "_month": "Feb 2026",
    },
    {
        "ticker": "GSK", "market": "UK",
        "entry_date": "2026-02-05", "shares": 50,
        "entry_price": 1700, "stop_price": 1600,  # risk = 100p
        "exit_date": "2026-02-19", "exit_price": 2000, "exit_reason": "target",
        # R = (2000-1700)/100 = +3.0R
        "_r": "+3.0R", "_bucket": "3R+", "_month": "Feb 2026",
    },
    {
        "ticker": "RIO", "market": "UK",
        "entry_date": "2026-02-06", "shares": 10,
        "entry_price": 5200, "stop_price": 4900,  # risk = 300p
        "exit_date": "2026-02-20", "exit_price": 4900, "exit_reason": "stop_hit",
        # R = (4900-5200)/300 = -1.0R
        "_r": "-1.0R", "_bucket": "-1R to 0R", "_month": "Feb 2026",
    },
    {
        "ticker": "LGEN", "market": "UK",
        "entry_date": "2026-02-07", "shares": 500,
        "entry_price": 240, "stop_price": 220,  # risk = 20p
        "exit_date": "2026-02-21", "exit_price": 250, "exit_reason": "manual",
        # R = (250-240)/20 = +0.5R
        "_r": "+0.5R", "_bucket": "0R to 1R", "_month": "Feb 2026",
    },
    {
        "ticker": "BT.A", "market": "UK",
        "entry_date": "2026-02-10", "shares": 200,
        "entry_price": 140, "stop_price": 120,  # risk = 20p
        "exit_date": "2026-02-24", "exit_price": 90, "exit_reason": "stop_hit",
        # R = (90-140)/20 = -2.5R
        "_r": "-2.5R", "_bucket": "-3R+", "_month": "Feb 2026",
    },

    # ── March 2026 ── 2 trades ────────────────────────────────────────────
    {
        "ticker": "MKS", "market": "UK",
        "entry_date": "2026-03-03", "shares": 125,
        "entry_price": 380, "stop_price": 340,  # risk = 40p
        "exit_date": "2026-03-17", "exit_price": 460, "exit_reason": "target",
        # R = (460-380)/40 = +2.0R
        "_r": "+2.0R", "_bucket": "2R to 3R", "_month": "Mar 2026",
    },
    {
        "ticker": "BATS", "market": "UK",
        "entry_date": "2026-03-04", "shares": 40,
        "entry_price": 2700, "stop_price": 2600,  # risk = 100p
        "exit_date": "2026-03-18", "exit_price": 2400, "exit_reason": "stop_hit",
        # R = (2400-2700)/100 = -3.0R
        "_r": "-3.0R", "_bucket": "-3R+", "_month": "Mar 2026",
    },
]


def post(path, body):
    url = BASE_URL + path
    resp = requests.post(url, json=body, timeout=30)
    if not resp.ok:
        raise RuntimeError(f"HTTP {resp.status_code} — {resp.text[:300]}")
    return resp.json()


def preflight():
    """Check the environment is ready before seeding."""
    print(f"  Preflight checks...")
    # Portfolio must exist
    r = requests.get(BASE_URL + "/portfolio", timeout=15)
    if not r.ok:
        print(f"  ✗ GET /portfolio → HTTP {r.status_code}: {r.text[:200]}")
        print(f"  The environment may not be fully configured. Set up the app first.")
        raise SystemExit(1)
    print(f"  ✓ Portfolio exists")
    # Settings must exist
    r = requests.get(BASE_URL + "/settings", timeout=15)
    if not r.ok:
        print(f"  ✗ GET /settings → HTTP {r.status_code}: {r.text[:200]}")
        raise SystemExit(1)
    print(f"  ✓ Settings exist")
    print()


def create_and_close(trade):
    """Create an open position then immediately close it."""
    # 1. Open position
    pos_resp = post("/portfolio/position", {
        "ticker": trade["ticker"],
        "market": trade["market"],
        "entry_date": trade["entry_date"],
        "shares": trade["shares"],
        "entry_price": trade["entry_price"],
        "stop_price": trade["stop_price"],
        "entry_note": "[SEED] ST-11 chart interactivity test data",
    })
    if pos_resp.get("status") != "ok":
        raise RuntimeError(f"Create failed: {pos_resp}")

    position_id = pos_resp["data"]["id"]
    time.sleep(0.3)  # avoid DB race on fast inserts

    # 2. Close position
    exit_resp = post(f"/positions/{position_id}/exit", {
        "exit_price": trade["exit_price"],
        "exit_date": trade["exit_date"],
        "exit_reason": trade["exit_reason"],
        "exit_note": f"[SEED] {trade['_r']}",
    })
    if exit_resp.get("status") != "ok":
        raise RuntimeError(f"Exit failed: {exit_resp}")

    return position_id


def main():
    print(f"\n{'='*65}")
    print(f"  Seeding chart test data")
    print(f"  Target: {BASE_URL}")
    print(f"{'='*65}\n")

    preflight()
    created = []
    for i, trade in enumerate(TRADES, 1):
        label = f"{trade['ticker']:<5}  {trade['_month']}  {trade['_r']:>7}  [{trade['_bucket']}]"
        print(f"  [{i:02d}/12] {label} ... ", end="", flush=True)
        try:
            pid = create_and_close(trade)
            print(f"OK")
            created.append(trade)
        except Exception as exc:
            print(f"FAILED — {exc}")

    print(f"\n{'='*65}")
    print(f"  Result: {len(created)}/12 trades created\n")

    if created:
        print(f"  Monthly trade counts (verify in heatmap modal):")
        for month in ["Jan 2026", "Feb 2026", "Mar 2026"]:
            count = sum(1 for t in created if t["_month"] == month)
            print(f"    {month}: {count} trade{'s' if count != 1 else ''}")
        print(f"    Apr 2026: 0 trades  ← zero-tile for SC-CHART-IX-01c")

        print(f"\n  R-multiple buckets populated:")
        buckets_order = ["3R+", "2R to 3R", "1R to 2R", "0R to 1R", "-1R to 0R", "-2R to -1R", "-3R+"]
        from collections import defaultdict
        by_bucket = defaultdict(list)
        for t in created:
            by_bucket[t["_bucket"]].append(f"{t['ticker']}({t['_r']})")
        for b in buckets_order:
            items = by_bucket.get(b, [])
            status = "  ".join(items) if items else "— empty"
            print(f"    {b:<15}: {status}")

        wins = sum(1 for t in created if float(t["_r"].replace("R", "")) > 0)
        print(f"\n  Win rate: {wins}/{len(created)} = {wins/len(created)*100:.0f}%")

    print(f"\n{'='*65}")
    if len(created) == 12:
        print("  ✓ All 12 trades seeded. Open Analytics and run SC-CHART-IX tests.\n")
    else:
        print(f"  ⚠ Only {len(created)}/12 created — fix errors before testing.\n")


if __name__ == "__main__":
    main()
