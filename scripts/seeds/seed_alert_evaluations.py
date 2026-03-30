"""
Seed script: insert sample alert_evaluations rows for SC-ANB-VIS-01 testing.

Usage:
    DATABASE_URL=<your-db-url> python scripts/seeds/seed_alert_evaluations.py
    DATABASE_URL=<your-db-url> python scripts/seeds/seed_alert_evaluations.py --count 5
    DATABASE_URL=<your-db-url> python scripts/seeds/seed_alert_evaluations.py --clear

Options:
    --count N   Number of evaluation rows to insert (default: 5)
    --clear     Delete all existing alert_evaluations rows for the portfolio, then exit

Purpose:
    Inserts alert_evaluations rows directly so the nav badge (ST-10) is visible
    without needing open positions or triggered alert rules. Useful for:
      - SC-ANB-VIS-01: badge appearance (red circle, count, top-right of icon)
      - SC-ANB-VIS-03: "99+" display (use --count 101)
      - SC-ANB-VIS-04: collapsed Tools group header badge

    After running, clear your browser's sessionStorage key 'alerts-last-visit'
    (DevTools → Application → Session Storage → delete the key) to ensure the
    badge counts all inserted rows.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta

import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set.", file=sys.stderr)
    sys.exit(1)

RULE_TYPES = [
    "stop_loss_approach",
    "grace_period_warning",
    "market_regime_change",
    "daily_portfolio_summary",
]

SAMPLE_VALUES = {
    "stop_loss_approach": {
        "stop_price": 42.10,
        "current_price": 43.50,
        "gap_pct": 3.3,
        "threshold_pct": 5.0,
    },
    "grace_period_warning": {
        "days_remaining": 2,
        "grace_period_days": 7,
    },
    "market_regime_change": {
        "regime": "bearish",
        "previous_regime": "neutral",
    },
    "daily_portfolio_summary": {
        "positions_count": 3,
        "total_pnl": -120.50,
    },
}

SYMBOLS = {
    "stop_loss_approach": "AAPL",
    "grace_period_warning": "TSLA",
    "market_regime_change": None,
    "daily_portfolio_summary": None,
}


def get_portfolio_id(conn) -> str:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM portfolios LIMIT 1")
        row = cur.fetchone()
        if not row:
            print("ERROR: No portfolio found in database. Create a portfolio first.", file=sys.stderr)
            sys.exit(1)
        return str(row["id"])


def clear_evaluations(conn, portfolio_id: str) -> int:
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM alert_evaluations WHERE portfolio_id = %s",
            (portfolio_id,),
        )
        return cur.rowcount


def insert_evaluations(conn, portfolio_id: str, count: int) -> list:
    """
    Insert `count` evaluation rows spread over the last 48 hours.
    Rows are evenly spaced so that setting alerts-last-visit to different
    times lets you test varying badge counts.
    """
    now = datetime.now(timezone.utc)
    span_hours = min(48, count * 2)  # spread rows across up to 48 hours
    interval = timedelta(hours=span_hours) / max(count, 1)

    inserted = []
    with conn.cursor() as cur:
        for i in range(count):
            rule_type = RULE_TYPES[i % len(RULE_TYPES)]
            ts = now - timedelta(hours=span_hours) + interval * i
            cur.execute(
                """
                INSERT INTO alert_evaluations
                    (portfolio_id, evaluation_timestamp, rule_type, symbol,
                     triggered, notification_sent, values_compared)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, evaluation_timestamp
                """,
                (
                    portfolio_id,
                    ts,
                    rule_type,
                    SYMBOLS[rule_type],
                    True,
                    True,
                    json.dumps(SAMPLE_VALUES[rule_type]),
                ),
            )
            row = cur.fetchone()
            inserted.append((str(row["id"]), str(row["evaluation_timestamp"]), rule_type))
    return inserted


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--count", type=int, default=5, help="Number of rows to insert (default: 5)")
    parser.add_argument("--clear", action="store_true", help="Delete all existing rows for the portfolio, then exit")
    args = parser.parse_args()

    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        portfolio_id = get_portfolio_id(conn)
        print(f"Portfolio: {portfolio_id}")

        if args.clear:
            deleted = clear_evaluations(conn, portfolio_id)
            conn.commit()
            print(f"Deleted {deleted} alert_evaluations row(s).")
            print("Tip: also clear 'alerts-last-visit' from sessionStorage in your browser.")
            return

        rows = insert_evaluations(conn, portfolio_id, args.count)
        conn.commit()

        print(f"\nInserted {len(rows)} alert_evaluations row(s):\n")
        for rid, ts, rule in rows:
            print(f"  {ts}  {rule:<30}  id={rid}")

        print(f"""
Next steps for SC-ANB-VIS-01:
  1. Open the app in your browser
  2. Open DevTools → Application → Session Storage → delete 'alerts-last-visit' (if present)
  3. Navigate to any non-Alerts page (e.g. /Watchlist)
  4. Expand the Tools group — badge should show "{len(rows)}" on the Alerts item

To test SC-ANB-VIS-03 (99+ display): re-run with --count 101
To reset:                              re-run with --clear
""")
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
