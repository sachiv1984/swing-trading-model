#!/usr/bin/env bash
# scripts/reset_staging_db.sh
# Reset the staging database to a known, reproducible baseline state.
#
# What it does:
#   1. Clears all application data (TRUNCATE + CASCADE)
#   2. Re-inserts a baseline portfolio (£20,000 cash)
#   3. Re-inserts default settings
#
# Idempotent: safe to run multiple times before each QA run.
#
# Prerequisites:
#   - psql installed and on $PATH
#   - STAGING_DATABASE_URL set to the staging PostgreSQL connection string
#
# Usage:
#   export STAGING_DATABASE_URL="postgresql://user:pass@host:5432/db"
#   ./scripts/reset_staging_db.sh
#
# The script intentionally uses STAGING_DATABASE_URL (not DATABASE_URL)
# to prevent accidental execution against the production database.
# Passing the production DATABASE_URL will cause the script to abort.
#
# Example connection string (Supabase / Render):
#   postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_FILE="$SCRIPT_DIR/reset_staging_db.sql"

# ── Guard: require explicit staging URL ──────────────────────────────────
if [[ -z "${STAGING_DATABASE_URL:-}" ]]; then
    echo "ERROR: STAGING_DATABASE_URL is not set." >&2
    echo "" >&2
    echo "Set it to your staging PostgreSQL connection string:" >&2
    echo "  export STAGING_DATABASE_URL=\"postgresql://user:pass@host:5432/db\"" >&2
    echo "  ./scripts/reset_staging_db.sh" >&2
    echo "" >&2
    echo "This script does NOT accept DATABASE_URL to prevent accidental" >&2
    echo "execution against the production database." >&2
    exit 1
fi

# ── Guard: reject if URL looks like it might be production ───────────────
# Heuristic: production Supabase URLs typically contain the production
# project ref. If your staging URL accidentally contains "prod" or
# the script is pointed at a non-staging host, abort.
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

# ── Run the reset ─────────────────────────────────────────────────────────
# Log the host portion only — never log credentials.
DB_HOST=$(echo "$STAGING_DATABASE_URL" | sed -E 's|.*@([^:/]+).*|\1|')
echo "Connecting to staging database host: $DB_HOST"
echo "Executing: $SQL_FILE"
echo ""

psql "$STAGING_DATABASE_URL" \
    --no-psqlrc \
    --single-transaction \
    -f "$SQL_FILE"

echo ""
echo "Staging DB reset complete. Ready for QA run."
