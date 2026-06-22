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
from typing import Dict, List, Optional

import yfinance as yf

from database import get_db, get_portfolio

logger = logging.getLogger(__name__)


def _fetch_and_store_company_name(ticker: str, market: str) -> None:
    """Look up company name via yfinance and upsert into ticker_universe if missing.

    UK tickers are stored in ticker_universe with the .L suffix (e.g. BP → BP.L),
    while the watchlist stores them without it (backend isalnum() validation).
    """
    try:
        # ticker_universe key matches yfinance symbol: BP.L for UK, AAPL for US
        tu_ticker = ticker + ".L" if market == "UK" and not ticker.endswith(".L") else ticker
        info = yf.Ticker(tu_ticker).info
        name = info.get("longName") or info.get("shortName")
        if not name:
            return
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO ticker_universe (ticker, market, active, company_name)
                    VALUES (%s, %s, true, %s)
                    ON CONFLICT (ticker)
                    DO UPDATE SET company_name = EXCLUDED.company_name
                    WHERE ticker_universe.company_name IS NULL
                """, (tu_ticker, market, name))
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


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SIGNAL_STATUS_SORT = {"active": 1, "watch": 2, "no_signal": 3}


def _row_to_dict(row) -> Dict:
    """Convert a DB row to a JSON-serialisable dict."""
    return {
        "id": str(row["id"]),
        "ticker": row["ticker"],
        "market": row["market"],
        "company_name": row["company_name"] if row["company_name"] else None,
        "signal_status": row["signal_status"],
        "target_entry_price": float(row["target_entry_price"]) if row["target_entry_price"] is not None else None,
        "initial_stop_price": float(row["initial_stop_price"]) if row["initial_stop_price"] is not None else None,
        "current_stop_price": float(row["current_stop_price"]) if row["current_stop_price"] is not None else None,
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
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
    Update price fields on an existing watchlist entry.
    ticker and market are not updatable.

    Raises:
        LookupError: entry not found.
        ValueError: no updatable fields, or non-positive price value.
    """
    updatable = {"target_entry_price", "initial_stop_price", "current_stop_price"}
    fields = {k: v for k, v in data.items() if k in updatable}

    if not fields:
        raise ValueError("At least one of target_entry_price, initial_stop_price, current_stop_price must be supplied")

    for key, val in fields.items():
        if val is not None and val <= 0:
            raise ValueError(f"{key} must be a positive decimal")

    set_clauses = ", ".join(f"{k} = %s" for k in fields)
    values = list(fields.values())

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE watchlist
                SET {set_clauses}, updated_at = CURRENT_TIMESTAMP
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
