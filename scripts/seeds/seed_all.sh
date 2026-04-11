#!/usr/bin/env bash
# scripts/seeds/seed_all.sh
# Run all three domain seed scripts in sequence against the staging database.
#
# Seeds applied (in order):
#   1. seed_portfolio_trades.sql — open positions, trade history, cash tx
#   2. seed_watchlist.sql        — watchlist entries
#   3. seed_alerts.sql           — alert rules, preferences, notifications
#   4. seed_analytics.sql        — 12 closed trades for analytics chart QA
#
# Prerequisites:
#   - psql installed and on $PATH
#   - STAGING_DATABASE_URL set to the staging PostgreSQL connection string
#   - reset_staging_db.sh run first (or since the last QA run)
#
# Usage:
#   export STAGING_DATABASE_URL="postgresql://user:pass@host:5432/db"
#   ./scripts/seeds/seed_all.sh
#
# Individual seed scripts can be run independently in any order after
# reset_staging_db.sh has established the portfolio baseline.
#
# The script intentionally uses STAGING_DATABASE_URL (not DATABASE_URL)
# to prevent accidental execution against the production database.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Guard: require explicit staging URL ──────────────────────────────────
if [[ -z "${STAGING_DATABASE_URL:-}" ]]; then
    echo "ERROR: STAGING_DATABASE_URL is not set." >&2
    echo "" >&2
    echo "Set it to your staging PostgreSQL connection string:" >&2
    echo "  export STAGING_DATABASE_URL=\"postgresql://user:pass@host:5432/db\"" >&2
    echo "  ./scripts/seeds/seed_all.sh" >&2
    echo "" >&2
    echo "This script does NOT accept DATABASE_URL to prevent accidental" >&2
    echo "execution against the production database." >&2
    exit 1
fi

# ── Guard: reject URLs that look like production ─────────────────────────
if [[ "$STAGING_DATABASE_URL" == *"production"* ]] || \
   [[ "$STAGING_DATABASE_URL" == *"/prod"* ]]; then
    echo "ERROR: STAGING_DATABASE_URL appears to point at a production database." >&2
    echo "Aborting to prevent data loss." >&2
    exit 1
fi

# ── Check psql is available ───────────────────────────────────────────────
if ! command -v psql &>/dev/null; then
    echo "ERROR: psql not found on PATH." >&2
    echo "Install PostgreSQL client tools and retry." >&2
    exit 1
fi

DB_HOST=$(echo "$STAGING_DATABASE_URL" | sed -E 's|.*@([^:/]+).*|\1|')
echo "Staging database host: $DB_HOST"
echo ""

# ── Run seeds in order ────────────────────────────────────────────────────
SEEDS=(
    "seed_portfolio_trades.sql"
    "seed_watchlist.sql"
    "seed_alerts.sql"
    "seed_analytics.sql"
    "seed_signals.sql"
)

for seed in "${SEEDS[@]}"; do
    echo "──────────────────────────────────────────────────────────"
    echo "Running: $seed"
    psql "$STAGING_DATABASE_URL" \
        --no-psqlrc \
        --single-transaction \
        -f "$SCRIPT_DIR/$seed"
    echo ""
done

echo "══════════════════════════════════════════════════════════"
echo "All seeds complete. Staging database ready for QA run."
echo ""
echo "State summary:"
echo "  portfolio/trades : 2 open positions (LGEN, BARC) + 2 closed trades"
echo "  signals          : 2 active (LGEN, BARC) + 1 dismissed (HSBA) + 1 converted (TSCO)"
echo "  watchlist        : 4 entries (AAPL, MSFT, LGEN, BARC)"
echo "  alerts           : 4 rules + 4 preferences + 2 unread notifications"
echo "  analytics        : 12 closed trades across Jan-Mar 2026 (analytics charts enabled)"
