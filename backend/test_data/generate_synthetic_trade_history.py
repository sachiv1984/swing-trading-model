"""
generate_synthetic_trade_history.py
====================================
ST-12 (BLG-QA-121, EPIC-03, v8.0) — Synthetic trade-history data generator
for gated-feature testing.

*** TEST DATA ONLY. NEVER RUN AGAINST A PRODUCTION DATABASE. ***

Several features gate on trade-history volume (e.g. SI-02 Behavioural Drift
Detection requires >= 20 closed trades — see docs/qa/si02_playwright_predesign.md
"minimum_required": 20 — and PT-04 Setup Quality Score is parked pending
>= 20 closed trades — see docs/specs/data_model/trade_plan_schema_audit_v4.6.md
§5.2). This module produces realistic, clearly-synthetic closed trades to
exercise those gates in tests and staging/PR-preview environments, without
waiting on real trading history to accumulate.

Two ways to use it:

1. Import `generate_synthetic_trades()` directly in a pytest test or fixture —
   returns a list of plain trade dicts, no network access, fully deterministic
   (seeded RNG). This is the primary, safe usage path.

2. Run as a CLI script to seed a staging / PR-preview API over HTTP, following
   the same pattern as backend/test_data/seed_chart_test_data.py:

       python generate_synthetic_trade_history.py [BASE_URL] [--count N]

   BASE_URL defaults to the staging environment. The script refuses to run
   against any URL that looks like production (same heuristic as
   scripts/reset_staging_db.sh's guard) and tags every position's
   entry_note/exit_note with "[SYNTHETIC TEST DATA]" for traceability.

Gate thresholds satisfied by the default output (count=25, > the 20-trade
minimum for both SI-02 and PT-04):
  - trade_count >= 20  (SI-02 data_sufficient / PT-04 gate)
  - Win/loss R-multiple distribution spans multiple buckets (realistic, not
    all-winners or all-losers)
"""

import random
import sys

# ---------------------------------------------------------------------------
# Gate thresholds this generator is designed to satisfy.
# ---------------------------------------------------------------------------
SI02_MINIMUM_REQUIRED_TRADES = 20  # docs/qa/si02_playwright_predesign.md
SQS_GATE_MINIMUM_CLOSED_TRADES = 20  # docs/specs/data_model/trade_plan_schema_audit_v4.6.md §5.2
DEFAULT_TRADE_COUNT = 25  # comfortably above both thresholds above

# Real UK-listed tickers, reused from backend/test_data/seed_chart_test_data.py's
# convention (test fixtures in this repo use real market symbols with prices
# chosen for the test scenario — not live-traded amounts).
TICKER_POOL = [
    ("AZN", "UK"), ("SHEL", "UK"), ("ULVR", "UK"), ("BP.", "UK"),
    ("HSBA", "UK"), ("VOD", "UK"), ("GSK", "UK"), ("RIO", "UK"),
    ("LGEN", "UK"), ("BT.A", "UK"), ("MKS", "UK"), ("BATS", "UK"),
    ("BARC", "UK"), ("TSCO", "UK"), ("NG.", "UK"), ("PRU", "UK"),
]

# R-multiple targets to cycle through so the generated set spans winners,
# losers, and near-breakeven trades rather than a single outcome shape.
R_MULTIPLE_CYCLE = [2.0, -1.5, 1.0, -0.5, 3.0, -1.0, 0.5, -2.5, 1.5, -0.75]

SYNTHETIC_TAG = "[SYNTHETIC TEST DATA]"


def generate_synthetic_trades(count=DEFAULT_TRADE_COUNT, seed=20260730, start_date="2026-01-05", spacing_days=3):
    """
    Return a list of `count` synthetic CLOSED trade dicts.

    Deterministic given the same (count, seed, start_date, spacing_days) —
    no network access, no randomness leakage across calls. Safe to call
    directly from pytest tests/fixtures.

    Each dict has the shape expected by POST /portfolio/position and
    POST /positions/{id}/exit (backend/main.py):
        ticker, market, entry_date, shares, entry_price, stop_price,
        entry_note, exit_date, exit_price, exit_reason, exit_note

    Every entry_note/exit_note is tagged with SYNTHETIC_TAG so these rows are
    always identifiable and greppable — never mistake them for real trades.
    """
    if count < 1:
        raise ValueError("count must be >= 1")

    rng = random.Random(seed)
    from datetime import date, timedelta

    y, m, d = (int(p) for p in start_date.split("-"))
    cursor = date(y, m, d)

    trades = []
    for i in range(count):
        ticker, market = TICKER_POOL[i % len(TICKER_POOL)]
        target_r = R_MULTIPLE_CYCLE[i % len(R_MULTIPLE_CYCLE)]

        entry_price = rng.randint(200, 5000)  # pence, matches seed_chart_test_data.py convention
        risk_per_share = max(1, round(entry_price * rng.uniform(0.03, 0.10)))
        stop_price = entry_price - risk_per_share
        exit_price = round(entry_price + target_r * risk_per_share)
        shares = rng.choice([10, 20, 25, 50, 100])

        entry_date = cursor
        exit_date = cursor + timedelta(days=rng.randint(5, 21))
        cursor = cursor + timedelta(days=spacing_days)

        exit_reason = "target" if target_r > 0 else ("stop_hit" if target_r <= -1.0 else "manual")

        trades.append({
            "ticker": ticker,
            "market": market,
            "entry_date": entry_date.isoformat(),
            "shares": shares,
            "entry_price": entry_price,
            "stop_price": stop_price,
            "entry_note": f"{SYNTHETIC_TAG} ST-12 generator — trade {i + 1}/{count}",
            "exit_date": exit_date.isoformat(),
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "exit_note": f"{SYNTHETIC_TAG} target R={target_r:+.1f}",
        })

    return trades


# ---------------------------------------------------------------------------
# CLI mode — seed a staging / PR-preview API over HTTP.
# Mirrors backend/test_data/seed_chart_test_data.py's create_and_close flow.
# ---------------------------------------------------------------------------

def _looks_like_production(base_url):
    """Same heuristic as scripts/reset_staging_db.sh's production guard."""
    lowered = base_url.lower()
    return "production" in lowered or "/prod" in lowered


def _create_and_close(base_url, trade, requests_module):
    post = requests_module.post
    pos_resp = post(f"{base_url}/portfolio/position", json={
        "ticker": trade["ticker"],
        "market": trade["market"],
        "entry_date": trade["entry_date"],
        "shares": trade["shares"],
        "entry_price": trade["entry_price"],
        "stop_price": trade["stop_price"],
        "entry_note": trade["entry_note"],
    }, timeout=30)
    if not pos_resp.ok or pos_resp.json().get("status") != "ok":
        raise RuntimeError(f"Create failed for {trade['ticker']}: {pos_resp.status_code} {pos_resp.text[:200]}")

    position_id = pos_resp.json()["data"]["id"]

    exit_resp = post(f"{base_url}/positions/{position_id}/exit", json={
        "exit_price": trade["exit_price"],
        "exit_date": trade["exit_date"],
        "exit_reason": trade["exit_reason"],
        "exit_note": trade["exit_note"],
    }, timeout=30)
    if not exit_resp.ok or exit_resp.json().get("status") != "ok":
        raise RuntimeError(f"Exit failed for {trade['ticker']}: {exit_resp.status_code} {exit_resp.text[:200]}")

    return position_id


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    count = DEFAULT_TRADE_COUNT
    if "--count" in sys.argv:
        count = int(sys.argv[sys.argv.index("--count") + 1])

    base_url = (args[0].rstrip("/") if args else
                "https://trading-assistant-staging.onrender.com")

    if _looks_like_production(base_url):
        print(f"ERROR: '{base_url}' looks like a production URL. Aborting.", file=sys.stderr)
        print("This generator produces synthetic test data and must never run against production.", file=sys.stderr)
        raise SystemExit(1)

    import requests  # local import: only needed for CLI mode, not the pure-function path

    trades = generate_synthetic_trades(count=count)

    print(f"\n{'=' * 65}")
    print(f"  Seeding {len(trades)} synthetic trades (SYNTHETIC TEST DATA ONLY)")
    print(f"  Target: {base_url}")
    print(f"  Gate thresholds satisfied: SI-02 (>= {SI02_MINIMUM_REQUIRED_TRADES}), "
          f"Setup Quality Score (>= {SQS_GATE_MINIMUM_CLOSED_TRADES})")
    print(f"{'=' * 65}\n")

    created = 0
    for i, trade in enumerate(trades, 1):
        label = f"{trade['ticker']:<5} entry={trade['entry_price']}p exit={trade['exit_price']}p"
        print(f"  [{i:02d}/{len(trades)}] {label} ... ", end="", flush=True)
        try:
            _create_and_close(base_url, trade, requests)
            print("OK")
            created += 1
        except Exception as exc:
            print(f"FAILED — {exc}")

    print(f"\n  Result: {created}/{len(trades)} synthetic trades created\n")


if __name__ == "__main__":
    main()
