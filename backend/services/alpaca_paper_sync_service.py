"""
Alpaca Paper Trading Sync Service (IT-06)

§13 compliance: Paper trading integration is §13 compliant — positions created by human
action only via the primary system position-open workflow; no automated order execution.
This service mirrors user-initiated position open/close events to Alpaca paper account
for hypothetical P&L tracking. It does not generate signals or automate decisions.

Sync is best-effort: any failure is logged but never blocks the primary position operation.
"""
import os
import time
import logging
import requests
from datetime import date
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

ALPACA_PAPER_BASE_URL = "https://paper-api.alpaca.markets"
ALPACA_DATA_BASE_URL = "https://data.alpaca.markets"

ALPACA_PAPER_API_KEY = os.environ.get("ALPACA_PAPER_API_KEY", "")
ALPACA_PAPER_SECRET_KEY = os.environ.get("ALPACA_PAPER_SECRET_KEY", "")


def _credentials_configured() -> bool:
    return bool(ALPACA_PAPER_API_KEY and ALPACA_PAPER_SECRET_KEY)


def _paper_headers() -> Dict[str, str]:
    return {
        "APCA-API-KEY-ID": ALPACA_PAPER_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_PAPER_SECRET_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def sync_open_paper_position(ticker: str, shares: float) -> None:
    """
    Mirror a US position open to the Alpaca paper account via a market order.
    Best-effort — any error is logged and silently swallowed.
    """
    if not _credentials_configured():
        return

    url = f"{ALPACA_PAPER_BASE_URL}/v2/orders"
    payload = {
        "symbol": ticker,
        "qty": str(shares),
        "side": "buy",
        "type": "market",
        "time_in_force": "day",
    }
    try:
        resp = requests.post(url, json=payload, headers=_paper_headers(), timeout=10)
        if resp.status_code in (200, 201):
            logger.info("Paper sync: opened position for %s (%.4f shares)", ticker, shares)
        else:
            logger.warning(
                "Paper sync: open order failed for %s — HTTP %d: %s",
                ticker, resp.status_code, resp.text[:200],
            )
    except Exception as exc:
        logger.warning("Paper sync: open order exception for %s — %s", ticker, exc)


def sync_close_paper_position(ticker: str) -> None:
    """
    Close a paper position when the real position exits.
    Best-effort — any error is logged and silently swallowed.
    """
    if not _credentials_configured():
        return

    url = f"{ALPACA_PAPER_BASE_URL}/v2/positions/{ticker}"
    try:
        resp = requests.delete(url, headers=_paper_headers(), timeout=10)
        if resp.status_code in (200, 204):
            logger.info("Paper sync: closed position for %s", ticker)
        elif resp.status_code == 404:
            logger.info("Paper sync: no paper position found for %s — nothing to close", ticker)
        else:
            logger.warning(
                "Paper sync: close failed for %s — HTTP %d: %s",
                ticker, resp.status_code, resp.text[:200],
            )
    except Exception as exc:
        logger.warning("Paper sync: close exception for %s — %s", ticker, exc)


def get_paper_positions() -> Dict:
    """
    Fetch current Alpaca paper account positions with P&L.

    Returns {"paper_tracking_enabled": False} when credentials absent.
    Returns {"paper_tracking_enabled": True, "positions": [...]} otherwise.
    """
    if not _credentials_configured():
        return {"paper_tracking_enabled": False}

    url = f"{ALPACA_PAPER_BASE_URL}/v2/positions"
    try:
        resp = requests.get(url, headers=_paper_headers(), timeout=10)
    except Exception as exc:
        logger.warning("Paper sync: get_positions network error — %s", exc)
        raise

    if resp.status_code != 200:
        logger.warning("Paper sync: get_positions HTTP %d — %s", resp.status_code, resp.text[:200])
        resp.raise_for_status()

    raw = resp.json()
    positions = []
    for pos in raw:
        try:
            avg_entry = float(pos.get("avg_entry_price") or 0)
            current_price = float(pos.get("current_price") or 0)
            qty = float(pos.get("qty") or 0)
            unrealized_pl = float(pos.get("unrealized_pl") or 0)
            unrealized_plpc = float(pos.get("unrealized_plpc") or 0)

            positions.append({
                "ticker": pos.get("symbol", ""),
                "paper_entry_price": round(avg_entry, 2),
                "current_market_price": round(current_price, 2),
                "paper_pnl_usd": round(unrealized_pl, 2),
                "paper_pnl_pct": round(unrealized_plpc * 100, 2),
                "date_opened": _parse_alpaca_date(pos),
                "position_size": qty,
            })
        except (TypeError, ValueError) as exc:
            logger.warning("Paper sync: skipping malformed position %s — %s", pos.get("symbol"), exc)

    return {
        "paper_tracking_enabled": True,
        "positions": positions,
    }


def _parse_alpaca_date(pos: dict) -> Optional[str]:
    raw = pos.get("lastday_price")  # Alpaca doesn't expose open date directly
    # Use asset_marginable as a proxy check; date_opened is not in Alpaca positions API
    # Return None — frontend will omit if not present
    return None
