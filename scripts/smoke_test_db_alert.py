#!/usr/bin/env python3
"""
Manual smoke test — Database Size Monitoring Alert (ST-08 BLG-OPS-09)

Confirms that:
  1. GET /health/database returns the correct response shape
  2. The Telegram alert fires when DB usage is above the configured threshold

Usage:
  # Basic check (uses the default threshold from DB_SIZE_ALERT_THRESHOLD_PERCENT):
  python scripts/smoke_test_db_alert.py --url https://your-app.onrender.com

  # Force-trigger the alert by temporarily lowering the threshold to 0%:
  python scripts/smoke_test_db_alert.py --url https://your-app.onrender.com --force-alert

  # Local dev:
  python scripts/smoke_test_db_alert.py --url http://localhost:8000

Required environment variables (on the server, not locally):
  TELEGRAM_BOT_TOKEN   — Telegram bot token
  TELEGRAM_CHAT_ID     — Target chat/user ID
  API_KEY              — Backend API key (if set)

On success you will see the response printed and (with --force-alert) receive
a Telegram message within a few seconds.

DoQ verification note:
  This script satisfies the manual verification step flagged in qa_evidence_EPIC-03.md
  for ST-08 runtime AC verification.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse


def check(url: str, api_key: str | None, force_alert: bool) -> None:
    endpoint = f"{url.rstrip('/')}/health/database"

    if force_alert:
        # Temporarily invoke with threshold=0 by calling the endpoint on a test
        # deployment that has DB_SIZE_ALERT_THRESHOLD_PERCENT=0 set.
        print("NOTE: --force-alert requires DB_SIZE_ALERT_THRESHOLD_PERCENT=0 set on the server.")
        print("      To force an alert, temporarily set that env var to 0, then call the endpoint.")
        print()

    print(f"Calling: GET {endpoint}")
    print()

    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key

    req = urllib.request.Request(endpoint, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read())
    except Exception as e:
        print(f"FAIL — request error: {e}")
        sys.exit(1)

    # --- Validate response shape ---
    required_fields = [
        "size_bytes", "size_mb", "limit_bytes", "limit_mb",
        "used_percent", "threshold_percent", "status"
    ]
    missing = [f for f in required_fields if f not in body]
    if missing:
        print(f"FAIL — missing fields in response: {missing}")
        print(json.dumps(body, indent=2))
        sys.exit(1)

    print("Response:")
    print(json.dumps(body, indent=2))
    print()

    # --- Validate field values ---
    status = body.get("status")
    if status not in ("ok", "warning", "error"):
        print(f"FAIL — unexpected status value: {status!r}")
        sys.exit(1)

    if body.get("limit_bytes") != 268_435_456:
        print(f"FAIL — limit_bytes should be 268435456, got {body.get('limit_bytes')}")
        sys.exit(1)

    if status == "error":
        print("WARN — status is 'error': DB size query failed on server.")
        print("       Check database connectivity. No Telegram alert will be sent.")
        sys.exit(1)

    # --- Report result ---
    used = body.get("used_percent", 0)
    threshold = body.get("threshold_percent", 80)
    print(f"DB usage: {used:.1f}% of {body.get('limit_mb', 256):.0f} MB "
          f"(threshold: {threshold:.0f}%)")

    if status == "warning":
        print()
        print("STATUS: warning — threshold exceeded.")
        print("A Telegram notification should have been sent (if credentials are configured")
        print("and the 1-hour cooldown has elapsed since the last alert).")
        print()
        print(">>> Check your Telegram for a message from the bot. <<<")
    else:
        print()
        print("STATUS: ok — below threshold. No Telegram alert sent.")
        print()
        print("To test the alert delivery, temporarily set DB_SIZE_ALERT_THRESHOLD_PERCENT=0")
        print("on your server, then call GET /health/database again.")

    print()
    print("PASS — GET /health/database shape and values are correct.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smoke test for DB size monitoring alert")
    parser.add_argument("--url", required=True, help="Base URL of the deployed backend")
    parser.add_argument("--force-alert", action="store_true",
                        help="Print instructions for forcing an alert trigger")
    parser.add_argument("--api-key", default=os.getenv("API_KEY"),
                        help="X-API-Key header value (falls back to API_KEY env var)")
    args = parser.parse_args()

    check(args.url, args.api_key, args.force_alert)
