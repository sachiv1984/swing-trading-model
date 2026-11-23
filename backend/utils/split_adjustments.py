"""
Split adjustment arithmetic (ST-27, BLG-BE-223, EPIC-05, v9.18).

strategy_rules.md §9.1: a confirmed split adjusts quantity, entry and stops on
read; the stored entry fields are never edited (data_model.md DS-42). Pure
functions, no database access: database.apply_split_adjustments() reads the
rows and calls adjust_position_for_splits(); a partial exit after a confirmed
split converts its write back with stored_units_for_split().
"""

from typing import Dict

# Entry fields a confirmed split adjusts on read (strategy_rules.md §9.1).
_SPLIT_PRICE_FIELDS = ("entry_price", "fill_price", "user_fill_price", "initial_stop")


def split_factors(adjustments) -> Dict:
    """Cumulative factors for a position's confirmed adjustments, oldest first.

    price_factor: product of the ratios; prices and stops are ÷ it.
    shares_factor: product of shares_after / shares_before per adjustment, so
    a user-entered odd-lot count is honoured (equals price_factor when every
    count was whole). cost_factor = shares_factor / price_factor: 1 for whole
    counts; otherwise the share cost moves by the cash-in-lieu difference.
    """
    price_factor = 1.0
    shares_factor = 1.0
    for a in adjustments:
        if a.get("confirmed_at") is None:
            continue
        ratio = float(a["ratio"])
        before = a.get("shares_before")
        after = a.get("shares_after")
        price_factor *= ratio
        if before and after:
            shares_factor *= float(after) / float(before)
        else:
            shares_factor *= ratio
    return {
        "price_factor": price_factor,
        "shares_factor": shares_factor,
        "cost_factor": shares_factor / price_factor,
    }


def adjust_position_for_splits(row: Dict, adjustments) -> Dict:
    """The row with confirmed splits applied (a copy). Adds `split_pending`
    (the unconfirmed row or None), `split_adjustments` (confirmed rows) and,
    when adjusted, `split_original` (the stored entry fields) and
    `split_factors`. Rows with no adjustments are returned unchanged apart
    from split_pending/split_adjustments."""
    out = dict(row)
    ordered = sorted(adjustments, key=lambda a: str(a.get("effective_date")))
    confirmed = [dict(a) for a in ordered if a.get("confirmed_at") is not None]
    pending = [dict(a) for a in ordered if a.get("confirmed_at") is None]
    out["split_pending"] = pending[0] if pending else None
    out["split_adjustments"] = confirmed
    if not confirmed:
        return out
    f = split_factors(confirmed)
    original = {k: row.get(k) for k in ("shares", "total_cost", "fees_paid") + _SPLIT_PRICE_FIELDS}
    out["split_original"] = original
    out["split_factors"] = f
    for k in _SPLIT_PRICE_FIELDS:
        if row.get(k) is not None:
            out[k] = float(row[k]) / f["price_factor"]
    if row.get("shares") is not None:
        out["shares"] = round(float(row["shares"]) * f["shares_factor"], 4)
    if row.get("total_cost") is not None and f["cost_factor"] != 1.0:
        fees = float(row.get("fees_paid") or 0)
        out["total_cost"] = round((float(row["total_cost"]) - fees) * f["cost_factor"] + fees, 2)
    return out


def stored_units_for_split(position: Dict, updates: Dict) -> Dict:
    """Convert `shares` / `total_cost` in an update computed from an adjusted
    row back to the stored (pre-split) units, so a partial exit after a
    confirmed split writes the right remainder. Other keys pass through."""
    f = position.get("split_factors")
    if not f:
        return updates
    out = dict(updates)
    if out.get("shares") is not None:
        out["shares"] = float(out["shares"]) / f["shares_factor"]
    if out.get("total_cost") is not None and f["cost_factor"] != 1.0:
        fees = float(out.get("fees_paid", position.get("fees_paid")) or 0)
        out["total_cost"] = round((float(out["total_cost"]) - fees) / f["cost_factor"] + fees, 2)
    return out


