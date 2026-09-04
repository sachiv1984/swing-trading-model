"""
Sector Concentration Service (ST-04, BLG-BE-104, EPIC-02, v8.9)

Shared sector-exposure calculation used by the Position Sizing Calculator's
concentration-aware size adjustment (sizing_service.py, POST /portfolio/size).

Canonical threshold: strategy_rules.md §4.2.2 defines the 30% sector
concentration advisory limit for the existing pre-entry check
(GET /portfolio/pre-entry-validation). SECTOR_CONCENTRATION_PCT below reuses
that same canonical number — it is not a new threshold. This module does not
redefine or override §4.2.2; it applies the existing threshold to a second
consumer (the sizing calculator) per the ST-04 design record.

Design record: docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md
§13: deterministic, rule-based over the user's own open positions — advisory
only. The suggested share count remains user-editable (design record §3).

DB-first sector lookup (no live yfinance call) — safe for the sizing
endpoint's 300ms-debounced call pattern (strategy_rules.md §4.1.7).

Consolidation (ST-10, BLG-TECH-13, v9.1): this module is now the canonical
home for both sector-lookup shapes used across the codebase — the
single-ticker `get_ticker_sector()` (DB then open-position fallback) and the
bulk `get_ticker_sector_map()` (DB-only, all tickers with a recorded sector,
for callers that need exposure across many positions in one query).
`routers/pre_entry_validation.py` and `routers/portfolio_risk.py` import and
delegate to these rather than carrying their own copies;
`services/compliance_recheck_service.py` delegates transitively via its
existing import from `pre_entry_validation`. No behaviour change — same SQL,
same fallback order, same return shapes as the pre-consolidation copies.
"""

from typing import Dict, Optional

from database import get_portfolio, get_positions
from utils.pricing import get_live_fx_rate
from utils.formatting import decimal_to_float

# strategy_rules.md §4.2.2 — canonical, shared with GET /portfolio/concentration-status
# and GET /portfolio/pre-entry-validation. Do not redefine this number elsewhere.
SECTOR_CONCENTRATION_PCT = 30.0


def get_ticker_sector(ticker: str) -> Optional[str]:
    """
    Look up sector for a ticker from ticker_universe, falling back to the
    user's own open positions. DB-only — no live network call.
    """
    try:
        from database import get_db
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT sector FROM ticker_universe WHERE ticker = %s LIMIT 1",
                    (ticker,),
                )
                row = cur.fetchone()
                if row and row["sector"]:
                    return row["sector"]
    except Exception:
        pass
    try:
        portfolio = get_portfolio()
        if portfolio:
            for pos in get_positions(str(portfolio["id"]), status="open"):
                if pos.get("ticker") == ticker and pos.get("sector"):
                    return pos["sector"]
    except Exception:
        pass
    return None


def get_ticker_sector_map(conn) -> Dict[str, str]:
    """
    Bulk ticker -> sector map from ticker_universe (ST-10, BLG-TECH-13).

    Pure DB read via an already-open `conn` — no yfinance call, no
    open-position fallback (unlike get_ticker_sector() above, this is for
    callers computing exposure across many positions in one query and
    reusing a connection across several queries in the same request).
    Canonical implementation for routers/portfolio_risk.py's sector-weights
    and concentration-status endpoints.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT ticker, sector FROM ticker_universe WHERE sector IS NOT NULL")
        rows = cur.fetchall()
    return {row["ticker"]: row["sector"] for row in rows}


def get_sector_exposure(sector: str) -> Optional[Dict]:
    """
    Compute current (pre-new-position) sector exposure across the user's
    open positions.

    Returns:
        {
            "sector_value_gbp": float,            # current GBP value of open positions in this sector
            "total_portfolio_value_gbp": float,    # cash + all open position values, GBP
            "position_count": int,                 # count of open positions in this sector
            "fx_rate": float,
        }
        None if portfolio/position data is unavailable.
    """
    try:
        portfolio = get_portfolio()
        if not portfolio:
            return None

        cash = float(portfolio["cash"])
        positions = get_positions(str(portfolio["id"]), status="open")
        live_fx_rate = get_live_fx_rate()
        fx = float(live_fx_rate) if live_fx_rate and live_fx_rate > 0 else 1.27

        total_pos_value = 0.0
        sector_value = 0.0
        position_count = 0

        for pos in positions:
            pos = decimal_to_float(dict(pos))
            shares = float(pos.get("shares", 0))
            price = float(pos.get("current_price") or pos.get("entry_price") or 0)
            pos_market = pos.get("market", "UK")
            value_gbp = price * shares / fx if pos_market == "US" else price * shares
            total_pos_value += value_gbp
            if pos.get("sector") and pos["sector"].lower() == sector.lower():
                sector_value += value_gbp
                position_count += 1

        return {
            "sector_value_gbp": sector_value,
            "total_portfolio_value_gbp": cash + total_pos_value,
            "position_count": position_count,
            "fx_rate": fx,
        }
    except Exception:
        return None
