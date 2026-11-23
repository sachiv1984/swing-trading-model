"""
Split Service — stock splits on open positions.

ST-27 (BLG-BE-223, EPIC-05, v9.18). Rule: strategy_rules.md §9.1 (v1.28).
Data: position_split_adjustments (data_model.md DS-42). Display: positions.md
§Split Detected State. Contract: position_endpoints.md
§POST /positions/{position_id}/split-adjustment/confirm.

- detect_position_splits(): the nightly run reads each open position's split
  history from the market-data provider and records any new split as pending.
- split_preview(): the Before → After figures the confirmation dialog shows.
- confirm_split(): applies the pending split. The entry fields stay stored as
  they were; quantity, entry and initial stop are adjusted on read
  (database.apply_split_adjustments). The live stop and ATR are rescaled here,
  so the §7.3 ratchet keeps working in the new units (a unit change, not a
  stop movement).

While a split is pending the position gets no stop-breach alert and no exit
recommendation, and its stop and ATR are not recalculated.
"""

import logging
import math
from datetime import date, datetime
from fractions import Fraction
from typing import Dict, Optional

from database import (
    confirm_split_adjustment,
    create_pending_split_adjustment,
    get_portfolio,
    get_position_by_id,
    get_positions,
)
from utils.formatting import decimal_to_float
from utils.pricing import get_live_fx_rate, get_split_history

logger = logging.getLogger(__name__)

SPLIT_SOURCE_YAHOO = "yahoo"
# A share count closer than this to a whole number is treated as whole.
_WHOLE_TOLERANCE = 1e-6


class SplitNotPendingError(ValueError):
    """The position has no unconfirmed split (HTTP 409)."""


class SplitSharesError(ValueError):
    """The post-split share count is missing or not allowed (HTTP 400)."""


def is_split_pending(position: Dict) -> bool:
    """True when the position has a detected, unconfirmed split (§9.1)."""
    return bool(position.get("split_pending"))


def ratio_label(ratio: float) -> str:
    """'2:1' for 2.0, '3:2' for 1.5, '1:10' for 0.1 (new shares : old shares)."""
    frac = Fraction(float(ratio)).limit_denominator(1000)
    return f"{frac.numerator}:{frac.denominator}"


def _entry_date(position: Dict) -> Optional[date]:
    raw = position.get("entry_date")
    if isinstance(raw, datetime):
        return raw.date()
    if isinstance(raw, date):
        return raw
    try:
        return date.fromisoformat(str(raw).split("T")[0].split(" ")[0])
    except (ValueError, TypeError):
        return None


def detect_position_splits() -> Dict:
    """Record new splits on open positions as pending (nightly run).

    A split counts when it is effective on or after the position's entry date
    (§9.1). A split already recorded for the position on that date (pending or
    confirmed) is not recorded again. A provider failure for one ticker is
    reported and skipped; it is never read as "no split". Never raises.
    """
    summary = {"checked": 0, "detected": 0, "failed": [], "pending": []}
    try:
        portfolio = get_portfolio()
        if not portfolio:
            return summary
        positions = get_positions(str(portfolio["id"]), status="open")
    except Exception:
        logger.warning("Split detection could not read open positions", exc_info=True)
        summary["error"] = "positions unavailable"
        return summary

    for pos in positions or []:
        entry = _entry_date(pos)
        if entry is None:
            continue
        summary["checked"] += 1
        history = get_split_history(pos["ticker"], pos.get("market"), entry)
        if history is None:
            summary["failed"].append(pos["ticker"])
            continue
        known = {
            str(a.get("effective_date"))
            for a in (pos.get("split_adjustments") or []) + ([pos["split_pending"]] if pos.get("split_pending") else [])
        }
        for event in history:
            if str(event["effective_date"]) in known:
                continue
            try:
                if create_pending_split_adjustment(
                    str(pos["id"]), event["ratio"], event["effective_date"], SPLIT_SOURCE_YAHOO
                ):
                    summary["detected"] += 1
                    summary["pending"].append({
                        "ticker": pos["ticker"],
                        "ratio": ratio_label(event["ratio"]),
                        "effective_date": str(event["effective_date"]),
                    })
            except Exception:
                logger.warning("Could not record split for %s", pos["ticker"], exc_info=True)
                summary["failed"].append(pos["ticker"])
    return summary


def _native_entry(position: Dict, live_fx_rate: Optional[float]) -> Optional[float]:
    from services.position_service import native_entry_price
    if position.get("entry_price") is None:
        return None
    rate = live_fx_rate
    if position.get("market") == "US" and not position.get("fill_price") and not position.get("fx_rate") and not rate:
        rate = get_live_fx_rate()
    return float(native_entry_price(position, rate))


def split_preview(position: Dict, live_fx_rate: Optional[float] = None) -> Optional[Dict]:
    """Before → After figures for the position's pending split, or None.

    `position` is a row as read (confirmed splits already applied). Figures
    are native currency. `shares_after` is None when quantity × ratio is not
    whole: the user enters the count (§9.1).
    """
    pending = position.get("split_pending")
    if not pending:
        return None
    pos = decimal_to_float(dict(position))
    ratio = float(pending["ratio"])
    shares_before = float(pos.get("shares") or 0)
    raw_after = shares_before * ratio
    whole = abs(raw_after - round(raw_after)) < _WHOLE_TOLERANCE
    entry_before = _native_entry(pos, live_fx_rate)
    entry_after = entry_before / ratio if entry_before is not None else None
    stop_before = pos.get("current_stop") or pos.get("initial_stop")
    stop_before = float(stop_before) if stop_before is not None else None
    stop_after = stop_before / ratio if stop_before is not None else None
    cost_before = shares_before * entry_before if entry_before is not None else None
    shares_after = float(round(raw_after)) if whole else None
    cost_after = shares_after * entry_after if (shares_after is not None and entry_after is not None) else None
    return {
        "id": str(pending["id"]),
        "ratio": ratio,
        "ratio_label": ratio_label(ratio),
        "effective_date": str(pending["effective_date"]),
        "source": pending.get("source"),
        "detected_at": pending["detected_at"].isoformat() if hasattr(pending.get("detected_at"), "isoformat") else pending.get("detected_at"),
        "shares_before": round(shares_before, 4),
        "shares_after": shares_after,
        "shares_after_exact": round(raw_after, 4),
        "shares_after_is_whole": whole,
        "entry_before": round(entry_before, 4) if entry_before is not None else None,
        "entry_after": round(entry_after, 4) if entry_after is not None else None,
        "stop_before": round(stop_before, 4) if stop_before is not None else None,
        "stop_after": round(stop_after, 4) if stop_after is not None else None,
        "cost_before": round(cost_before, 2) if cost_before is not None else None,
        "cost_after": round(cost_after, 2) if cost_after is not None else None,
    }


def _validate_shares_after(raw_after: float, shares: Optional[float]) -> float:
    whole = abs(raw_after - round(raw_after)) < _WHOLE_TOLERANCE
    if shares is None:
        if not whole:
            raise SplitSharesError(
                f"Quantity × ratio is {raw_after:g}, not a whole number: enter the post-split share count "
                "your broker shows (strategy_rules.md §9.1)."
            )
        return float(round(raw_after))
    try:
        shares = float(shares)
    except (TypeError, ValueError):
        raise SplitSharesError("shares must be a number")
    if not math.isfinite(shares) or shares <= 0:
        raise SplitSharesError("shares must be greater than 0")
    if whole and abs(shares - round(raw_after)) > _WHOLE_TOLERANCE:
        raise SplitSharesError(
            f"Quantity × ratio is {round(raw_after):g}; a different share count is only accepted "
            "when the result is not a whole number."
        )
    if abs(shares - raw_after) >= 1:
        raise SplitSharesError(
            f"The post-split share count must be within 1 share of {raw_after:g} (quantity × ratio)."
        )
    return shares


def confirm_split(position_id: str, shares: Optional[float] = None) -> Dict:
    """Apply the position's pending split (§9.1).

    Writes the adjustment row's confirmation and the shares before and after,
    and rescales the live stop fields and ATR in the same transaction. The
    stored entry fields (shares, entry price, fill price, initial stop,
    total cost) are not edited. Raises SplitNotPendingError when nothing is
    pending, SplitSharesError for a missing or out-of-range share count.
    """
    position = get_position_by_id(position_id)
    if not position or position.get("status") != "open":
        raise SplitNotPendingError("Position not found or not open")
    pending = position.get("split_pending")
    if not pending:
        raise SplitNotPendingError("This position has no split to confirm")
    pos = decimal_to_float(dict(position))
    ratio = float(pending["ratio"])
    shares_before = float(pos.get("shares") or 0)
    if shares_before <= 0:
        raise SplitSharesError("The position has no shares to adjust")
    shares_after = _validate_shares_after(shares_before * ratio, shares)

    updates = {}
    for field in ("current_stop", "previous_stop", "atr"):
        if pos.get(field) is not None:
            updates[field] = round(float(pos[field]) / ratio, 4)
    if not confirm_split_adjustment(str(pending["id"]), position_id, shares_before, shares_after, updates):
        raise SplitNotPendingError("This split was already confirmed")

    confirmed = decimal_to_float(dict(get_position_by_id(position_id) or {}))
    return {
        "position_id": position_id,
        "ticker": pos.get("ticker"),
        "ratio": ratio,
        "ratio_label": ratio_label(ratio),
        "effective_date": str(pending["effective_date"]),
        "shares_before": round(shares_before, 4),
        "shares_after": round(shares_after, 4),
        # Native entry after the split (entry_price is stored in GBP for US rows).
        "entry_price": round(_native_entry(confirmed, None), 4) if confirmed.get("entry_price") is not None else None,
        "initial_stop": round(float(confirmed["initial_stop"]), 4) if confirmed.get("initial_stop") is not None else None,
        "current_stop": round(float(confirmed["current_stop"]), 4) if confirmed.get("current_stop") is not None else None,
    }
