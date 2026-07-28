"""
Watchlist Service

Business logic for the pre-position ticker monitoring list.

Signal status is derived at read time via LEFT JOIN LATERAL on the signals table
(join-on-read architecture). No signal_status column is stored in the watchlist table.

Signal status mapping (from most recent signals record for the ticker):
  signals.status = 'new'                    → 'active'
  signals.status IN ('dismissed','expired') → 'watch'
  no record / 'entered' / 'already_held'   → 'no_signal'

Sort order for list: active first, then watch, then no_signal; alphabetically
by ticker within each group.

Contract: docs/specs/api_contracts/watchlist_endpoints.md v0.1
Data model: docs/specs/data_model.md §11 (watchlist table, migration v2.0→v2.1)
"""

import logging
import re
from datetime import date
from typing import Dict, List, Optional
import yfinance as yf

from database import get_db, get_portfolio

logger = logging.getLogger(__name__)

# Tag rules — journal_components.md §3/§4 pattern, reused for watchlist.tags
# (ST-03, BLG-FE-117, EPIC-03, v7.5). Watchlist entries have no pre-existing
# tags concept; this bulk-tag feature introduces the column.
_TAG_MAX_LENGTH = 20
_TAG_MAX_COUNT = 10
_TAG_PATTERN = re.compile(r"^[a-z0-9-]+$")
_BULK_MAX_IDS = 100


def _validate_tags(tags: Optional[List[str]]) -> List[str]:
    """Lowercase, alphanumeric+hyphen, max 20 chars, max 10 tags, deduped."""
    if not tags:
        return []
    validated: List[str] = []
    for tag in tags:
        clean = (tag or "").strip().lower()
        if clean and len(clean) <= _TAG_MAX_LENGTH and _TAG_PATTERN.match(clean) and clean not in validated:
            validated.append(clean)
    return validated[:_TAG_MAX_COUNT]


def _fetch_and_store_company_name(ticker: str, market: str) -> None:
    """Look up company name via yfinance and upsert into ticker_universe if missing."""
    try:
        yf_symbol = ticker + ".L" if market == "UK" and not ticker.endswith(".L") else ticker
        info = yf.Ticker(yf_symbol).info
        name = info.get("longName") or info.get("shortName")
        if not name:
            return
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO ticker_universe (ticker, market, active, company_name)
                    VALUES (%s, %s, true, %s)
                    ON CONFLICT (ticker, market)
                    DO UPDATE SET company_name = EXCLUDED.company_name
                    WHERE ticker_universe.company_name IS NULL
                """, (ticker, market, name))
    except Exception:
        logger.debug("company name lookup failed for %s/%s", ticker, market)

# ---------------------------------------------------------------------------
# Table bootstrap
# ---------------------------------------------------------------------------

def ensure_watchlist_table() -> None:
    """Create the watchlist table if it does not yet exist (idempotent)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS watchlist (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL,
                    ticker VARCHAR(20) NOT NULL,
                    market VARCHAR(5) NOT NULL
                        CHECK (market IN ('US', 'UK')),
                    target_entry_price DECIMAL(10, 4),
                    initial_stop_price DECIMAL(10, 4),
                    current_stop_price DECIMAL(10, 4),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT watchlist_portfolio_ticker_key
                        UNIQUE (portfolio_id, ticker),
                    CONSTRAINT watchlist_portfolio_fkey
                        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
                        ON DELETE CASCADE
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_watchlist_portfolio
                    ON watchlist (portfolio_id)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_watchlist_ticker
                    ON watchlist (ticker)
            """)
            # ST-03 (BLG-FE-117, v7.5): tags column for the new Bulk Tag action
            # (data_model.md v2.13->v2.14). No single-item tag UI is added —
            # only bulk-tag, per the locked bulk-actions-toolbar/ux_spec.md.
            cur.execute("""
                ALTER TABLE watchlist ADD COLUMN IF NOT EXISTS tags TEXT[] NOT NULL DEFAULT '{}'
            """)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SIGNAL_STATUS_SORT = {"active": 1, "watch": 2, "no_signal": 3}


def _compute_days_on_watchlist(added_at) -> int:
    """Days between `added_at` (the watchlist table's `created_at` column --
    see STALENESS_THRESHOLD_DAYS docstring below) and today.

    Legacy rows with no added_at (pre-dating this feature) are treated as
    added today (ux_spec.md §5) -- never mass-flagged as stale on ship day.
    """
    if added_at is None:
        return 0
    added_date = added_at.date() if hasattr(added_at, "date") else added_at
    return max((date.today() - added_date).days, 0)


# Staleness threshold (ST-01, EPIC-01, v7.9, BLG-FEAT-66): fixed, server-side
# constant this cycle -- not user-editable, per ux_spec.md §2/§7.
STALENESS_THRESHOLD_DAYS = 30


def _row_to_dict(row) -> Dict:
    """Convert a DB row to a JSON-serialisable dict."""
    added_at = row["created_at"]
    days_on_watchlist = _compute_days_on_watchlist(added_at)
    return {
        "id": str(row["id"]),
        "ticker": row["ticker"],
        "market": row["market"],
        "company_name": row.get("company_name") or None,
        "signal_status": row["signal_status"],
        "tags": list(row["tags"]) if row.get("tags") is not None else [],
        "target_entry_price": float(row["target_entry_price"]) if row["target_entry_price"] is not None else None,
        "initial_stop_price": float(row["initial_stop_price"]) if row["initial_stop_price"] is not None else None,
        "current_stop_price": float(row["current_stop_price"]) if row["current_stop_price"] is not None else None,
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
        # ST-01 (EPIC-01, v7.9, BLG-FEAT-66): `added_at` is an API-level alias
        # for the existing `created_at` column -- the ux_spec.md's "no backend
        # schema change required" premise holds once the field is exposed
        # under its spec'd name at the serialisation boundary rather than
        # requiring an actual new `added_at` column.
        "added_at": row["created_at"].isoformat() if row["created_at"] else None,
        "days_on_watchlist": days_on_watchlist,
        "is_stale": days_on_watchlist >= STALENESS_THRESHOLD_DAYS,
    }


# ---------------------------------------------------------------------------
# Service functions
# ---------------------------------------------------------------------------

def get_watchlist(portfolio_id: str) -> List[Dict]:
    """
    Return all watchlist entries with computed signal_status.

    signal_status is derived via LEFT JOIN LATERAL on signals (join-on-read).
    Sort: active → watch → no_signal, then alphabetically by ticker.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    w.id,
                    w.ticker,
                    w.market,
                    w.target_entry_price,
                    w.initial_stop_price,
                    w.current_stop_price,
                    w.tags,
                    w.created_at,
                    w.updated_at,
                    tu.company_name,
                    CASE
                        WHEN s.status = 'new'                     THEN 'active'
                        WHEN s.status IN ('dismissed', 'expired') THEN 'watch'
                        ELSE                                           'no_signal'
                    END AS signal_status
                FROM watchlist w
                LEFT JOIN ticker_universe tu
                    ON tu.ticker = CASE
                        WHEN w.market = 'UK' THEN w.ticker || '.L'
                        ELSE w.ticker
                    END
                LEFT JOIN LATERAL (
                    SELECT status
                    FROM signals
                    WHERE portfolio_id = w.portfolio_id
                      AND ticker = w.ticker
                    ORDER BY signal_date DESC
                    LIMIT 1
                ) s ON true
                WHERE w.portfolio_id = %s
                ORDER BY
                    CASE
                        WHEN s.status = 'new'                     THEN 1
                        WHEN s.status IN ('dismissed', 'expired') THEN 2
                        ELSE                                           3
                    END,
                    w.ticker ASC
            """, (portfolio_id,))
            rows = cur.fetchall()
    return [_row_to_dict(r) for r in rows]


def create_watchlist_entry(portfolio_id: str, data: Dict) -> Dict:
    """
    Add a ticker to the watchlist.

    Raises:
        ValueError: ticker/market validation failures or positive-price checks.
        LookupError: ticker already exists on the watchlist (409).
    """
    ticker = data.get("ticker", "").strip().upper()
    market = data.get("market", "")
    target = data.get("target_entry_price")
    initial = data.get("initial_stop_price")
    current = data.get("current_stop_price")

    if not ticker:
        raise ValueError("ticker is required")
    if len(ticker) > 10 or not ticker.isalnum():
        raise ValueError("ticker must be alphanumeric and 1–10 characters")
    if market not in ("UK", "US"):
        raise ValueError("market must be 'UK' or 'US'")
    for label, val in [("target_entry_price", target), ("initial_stop_price", initial), ("current_stop_price", current)]:
        if val is not None and val <= 0:
            raise ValueError(f"{label} must be a positive decimal")

    with get_db() as conn:
        with conn.cursor() as cur:
            # Duplicate check
            cur.execute(
                "SELECT id FROM watchlist WHERE portfolio_id = %s AND ticker = %s",
                (portfolio_id, ticker),
            )
            if cur.fetchone():
                raise LookupError(f"ticker '{ticker}' is already on the watchlist")

    # Ensure company name is in ticker_universe before fetching back (best-effort)
    _fetch_and_store_company_name(ticker, market)

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO watchlist
                    (portfolio_id, ticker, market,
                     target_entry_price, initial_stop_price, current_stop_price)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (portfolio_id, ticker, market, target, initial, current))
            new_id = str(cur.fetchone()["id"])

    # Fetch back with computed signal_status
    entries = get_watchlist(portfolio_id)
    for entry in entries:
        if entry["id"] == new_id:
            return entry
    raise RuntimeError("Watchlist entry created but could not be retrieved")


def update_watchlist_entry(portfolio_id: str, entry_id: str, data: Dict) -> Dict:
    """
    Update price fields on an existing watchlist entry, or reset its
    staleness clock via `added_at` (ST-01, EPIC-01, v7.9, BLG-FEAT-66 --
    the "Keep" action).

    ticker and market are not updatable.

    Raises:
        LookupError: entry not found.
        ValueError: no updatable fields, or non-positive price value.

    Security/integrity note: `added_at` is treated as a reset *trigger*,
    not a client-supplied timestamp -- presence of the key (any value)
    resets the underlying `created_at` column to the server's CURRENT_TIMESTAMP.
    A client can never backdate or postdate its own staleness clock; this
    matches the server-authoritative pattern already used by
    mark_position_reviewed() elsewhere in this app.
    """
    price_fields = {"target_entry_price", "initial_stop_price", "current_stop_price"}
    fields = {k: v for k, v in data.items() if k in price_fields}
    reset_added_at = "added_at" in data and data["added_at"] is not None

    if not fields and not reset_added_at:
        raise ValueError(
            "At least one of target_entry_price, initial_stop_price, current_stop_price, or added_at must be supplied"
        )

    for key, val in fields.items():
        if val is not None and val <= 0:
            raise ValueError(f"{key} must be a positive decimal")

    set_clauses = [f"{k} = %s" for k in fields]
    values = list(fields.values())
    if reset_added_at:
        set_clauses.append("created_at = CURRENT_TIMESTAMP")
    set_sql = ", ".join(set_clauses)

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE watchlist
                SET {set_sql}, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND portfolio_id = %s
                RETURNING id
                """,
                values + [entry_id, portfolio_id],
            )
            if cur.fetchone() is None:
                raise LookupError(f"Watchlist entry '{entry_id}' not found")

    entries = get_watchlist(portfolio_id)
    for entry in entries:
        if entry["id"] == entry_id:
            return entry
    raise RuntimeError("Watchlist entry updated but could not be retrieved")


def delete_watchlist_entry(portfolio_id: str, entry_id: str) -> Dict:
    """
    Remove a watchlist entry.

    Raises:
        LookupError: entry not found (404 / non-idempotent per spec).
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM watchlist WHERE id = %s AND portfolio_id = %s RETURNING id",
                (entry_id, portfolio_id),
            )
            if cur.fetchone() is None:
                raise LookupError(f"Watchlist entry '{entry_id}' not found")

    return {"id": entry_id, "deleted": True}


# ---------------------------------------------------------------------------
# Bulk actions (ST-03, BLG-FE-117, EPIC-03, v7.5)
# ---------------------------------------------------------------------------

def get_all_watchlist_tags(portfolio_id: str) -> List[str]:
    """Unique tags across all watchlist entries, for autocomplete (mirrors GET /trade-plans/tags)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT unnest(tags) AS tag FROM watchlist WHERE portfolio_id = %s ORDER BY tag",
                (portfolio_id,),
            )
            return [r["tag"] for r in cur.fetchall()]


def bulk_tag_watchlist(portfolio_id: str, ids: List[str], tags: List[str]) -> Dict:
    """
    Add tags to each selected watchlist entry's existing tag set (union, not replace).
    Returns {succeeded: [ids], failed: [{id, reason}]} per readiness-pass AC-01 shape.
    """
    if not ids:
        raise ValueError("ids must be a non-empty array")
    if len(ids) > _BULK_MAX_IDS:
        raise ValueError(f"ids exceeds the maximum batch size ({_BULK_MAX_IDS})")
    validated_tags = _validate_tags(tags)

    succeeded, failed = [], []
    with get_db() as conn:
        with conn.cursor() as cur:
            for entry_id in ids:
                cur.execute(
                    "SELECT tags FROM watchlist WHERE id = %s AND portfolio_id = %s",
                    (entry_id, portfolio_id),
                )
                row = cur.fetchone()
                if not row:
                    failed.append({"id": entry_id, "reason": "not_found"})
                    continue
                existing = list(row["tags"]) if row.get("tags") else []
                merged = existing[:]
                for t in validated_tags:
                    if t not in merged:
                        merged.append(t)
                merged = merged[:_TAG_MAX_COUNT]
                cur.execute(
                    "UPDATE watchlist SET tags = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s AND portfolio_id = %s",
                    (merged, entry_id, portfolio_id),
                )
                succeeded.append(entry_id)

    return {"succeeded": succeeded, "failed": failed}


def bulk_delete_watchlist(portfolio_id: str, ids: List[str]) -> Dict:
    """Remove each selected watchlist entry. Returns {succeeded, failed} per-row."""
    if not ids:
        raise ValueError("ids must be a non-empty array")
    if len(ids) > _BULK_MAX_IDS:
        raise ValueError(f"ids exceeds the maximum batch size ({_BULK_MAX_IDS})")

    succeeded, failed = [], []
    with get_db() as conn:
        with conn.cursor() as cur:
            for entry_id in ids:
                cur.execute(
                    "DELETE FROM watchlist WHERE id = %s AND portfolio_id = %s RETURNING id",
                    (entry_id, portfolio_id),
                )
                if cur.fetchone() is None:
                    failed.append({"id": entry_id, "reason": "not_found"})
                else:
                    succeeded.append(entry_id)

    return {"succeeded": succeeded, "failed": failed}
