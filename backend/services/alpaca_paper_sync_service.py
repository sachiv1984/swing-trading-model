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

from utils.retry import retry_with_backoff

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


def _client_order_id_for_open(position_id: str) -> str:
    """Derive a deterministic Alpaca client_order_id from the internal position id
    (ST-10, BLG-BE-80). A retried open call for the same position always submits
    the same client_order_id, so Alpaca rejects the duplicate as a no-op instead
    of creating a second paper order."""
    return f"paper-open-{position_id}"


@retry_with_backoff(
    max_attempts=3,
    base_delay=0.5,
    retryable_exceptions=(requests.exceptions.RequestException,),
)
def _sync_open_paper_position_raw(ticker: str, shares: float, client_order_id: str) -> None:
    """POST the paper open order (internal). Raises on network failure (retried by
    the decorator) or a non-2xx response that isn't the expected duplicate-order
    outcome for a retried client_order_id (not retried — see caller)."""
    url = f"{ALPACA_PAPER_BASE_URL}/v2/orders"
    payload = {
        "symbol": ticker,
        "qty": str(shares),
        "side": "buy",
        "type": "market",
        "time_in_force": "day",
        "client_order_id": client_order_id,
    }
    resp = requests.post(url, json=payload, headers=_paper_headers(), timeout=10)
    if resp.status_code in (200, 201):
        logger.info("Paper sync: opened position for %s (%.4f shares)", ticker, shares)
        return
    if resp.status_code == 422 and "client_order_id" in resp.text:
        # Alpaca rejects a re-submitted client_order_id as a duplicate — this is
        # the expected, safe outcome of a retry, not a failure.
        logger.info(
            "Paper sync: open order for %s already submitted (client_order_id=%s) — no duplicate created",
            ticker, client_order_id,
        )
        return
    logger.warning(
        "Paper sync: open order failed for %s — HTTP %d: %s",
        ticker, resp.status_code, resp.text[:200],
    )
    raise requests.exceptions.RequestException(f"Alpaca open order HTTP {resp.status_code}")


def sync_open_paper_position(ticker: str, shares: float, position_id: str) -> None:
    """
    Mirror a US position open to the Alpaca paper account via a market order.
    Retries transient failures (ST-09-pattern, ~3 attempts) using a deterministic
    client_order_id derived from position_id, so a retried call cannot create a
    duplicate order. Best-effort — any error is logged and silently swallowed.
    """
    if not _credentials_configured():
        return

    client_order_id = _client_order_id_for_open(position_id)
    try:
        _sync_open_paper_position_raw(ticker, shares, client_order_id)
    except Exception as exc:
        logger.warning("Paper sync: open order exception for %s — %s", ticker, exc)


@retry_with_backoff(
    max_attempts=3,
    base_delay=0.5,
    retryable_exceptions=(requests.exceptions.RequestException,),
)
def _sync_close_paper_position_raw(ticker: str) -> str:
    """DELETE the paper position (internal). Raises on network failure or a
    non-(200, 204, 404) response — retried by the decorator (ST-11,
    BLG-BE-83). Returns a disposition string for the caller to log; 404
    ("nothing to close") is a legitimate outcome, not a failure."""
    url = f"{ALPACA_PAPER_BASE_URL}/v2/positions/{ticker}"
    resp = requests.delete(url, headers=_paper_headers(), timeout=10)
    if resp.status_code in (200, 204):
        return "closed"
    if resp.status_code == 404:
        return "not_found"
    logger.warning(
        "Paper sync: close failed for %s — HTTP %d: %s",
        ticker, resp.status_code, resp.text[:200],
    )
    raise requests.exceptions.RequestException(f"Alpaca close position HTTP {resp.status_code}")


def sync_close_paper_position(ticker: str) -> None:
    """
    Close a paper position when the real position exits.
    Retries transient/429 failures (ST-11, BLG-BE-83, ~3 attempts) via the
    shared retry_with_backoff decorator before giving up. Best-effort — any
    error (including retries exhausted) is logged and silently swallowed;
    never raises to the caller. Unchanged from the pre-ST-11 behaviour.
    """
    if not _credentials_configured():
        return

    try:
        disposition = _sync_close_paper_position_raw(ticker)
        if disposition == "closed":
            logger.info("Paper sync: closed position for %s", ticker)
        else:
            logger.info("Paper sync: no paper position found for %s — nothing to close", ticker)
    except Exception as exc:
        logger.warning("Paper sync: close exception for %s — %s", ticker, exc)


@retry_with_backoff(
    max_attempts=3,
    base_delay=0.5,
    retryable_exceptions=(requests.exceptions.RequestException,),
)
def _get_paper_positions_raw() -> list:
    """GET current Alpaca paper positions (internal). Raises on network
    failure or a non-200 response — retried by the decorator (ST-11,
    BLG-BE-83)."""
    url = f"{ALPACA_PAPER_BASE_URL}/v2/positions"
    resp = requests.get(url, headers=_paper_headers(), timeout=10)
    if resp.status_code != 200:
        logger.warning("Paper sync: get_positions HTTP %d — %s", resp.status_code, resp.text[:200])
        resp.raise_for_status()
    return resp.json()


def get_paper_positions() -> Dict:
    """
    Fetch current Alpaca paper account positions with P&L.

    Retries transient/429 failures (ST-11, BLG-BE-83, ~3 attempts) via the
    shared retry_with_backoff decorator before giving up. Returns
    {"paper_tracking_enabled": False} when credentials absent. Returns
    {"paper_tracking_enabled": True, "positions": [...]} otherwise. Still
    raises to the caller if every retry attempt fails — unchanged from the
    pre-ST-11 behaviour (the router's caller converts this to a 500).
    """
    if not _credentials_configured():
        return {"paper_tracking_enabled": False}

    try:
        raw = _get_paper_positions_raw()
    except requests.exceptions.RequestException as exc:
        logger.warning("Paper sync: get_positions failed after retries — %s", exc)
        raise
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
