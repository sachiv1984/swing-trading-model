"""
Trade Service

Business logic for trade history and statistics.

All functions are independent of FastAPI for maximum testability.
"""

import csv
import io

from typing import Dict, List, Optional
from database import (
    get_portfolio, get_trade_history, get_trade_reflection, upsert_trade_reflection,
    get_trade_history_with_stops, update_trade_costs,
)
from utils.formatting import decimal_to_float


def _compute_net_r(pnl: float, commission_gbp: Optional[float], spread_cost_gbp: Optional[float],
                   entry_price: float, stop_price_at_entry: Optional[float],
                   shares: float, market: str, entry_fx_rate: Optional[float]) -> Optional[float]:
    """Compute net-of-costs R-multiple. Returns None when inputs are insufficient.

    ST-03 (EPIC-02, v6.0) — BLG-FEAT-20.
    net_r = (pnl - commission_gbp - spread_cost_gbp) / initial_risk_gbp
    initial_risk_gbp: (entry_price - stop_price_at_entry) * shares, then /fx_rate for US stocks.
    """
    total_costs = (commission_gbp or 0.0) + (spread_cost_gbp or 0.0)
    if total_costs == 0.0:
        return None
    if stop_price_at_entry is None or stop_price_at_entry <= 0:
        return None
    if entry_price <= stop_price_at_entry:
        return None
    risk_native = (entry_price - stop_price_at_entry) * shares
    if risk_native <= 0:
        return None
    if market == "US":
        fx = entry_fx_rate or 1.0
        risk_gbp = risk_native / fx if fx > 0 else risk_native
    else:
        risk_gbp = risk_native
    if risk_gbp <= 0:
        return None
    net_pnl = pnl - total_costs
    return round(net_pnl / risk_gbp, 3)


def get_trade_history_with_stats() -> Dict:
    """
    Get complete trade history with performance statistics
    
    Returns:
        Dictionary with:
            - total_trades: Total number of closed trades
            - win_rate: Percentage of profitable trades
            - total_pnl: Total realized P&L across all trades
            - trades: List of trade dictionaries (NOW INCLUDING NOTES AND TAGS!)
    
    Raises:
        ValueError: If portfolio not found
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")

    portfolio_id = str(portfolio['id'])
    trades = get_trade_history_with_stops(portfolio_id)
    trades = [decimal_to_float(t) for t in trades]
    
    if not trades:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "avg_slippage_pct": None,
            "avg_fee_drag_pct": None,
            "trades": []
        }
    
    # Calculate statistics
    total_pnl = sum(t.get('pnl', 0) for t in trades)
    wins = len([t for t in trades if t.get('pnl', 0) > 0])
    win_rate = (wins / len(trades)) * 100
    
    # Format trades for frontend
    formatted_trades = []
    for t in trades:
        fill_price = t.get('fill_price')
        entry_price_val = float(t.get('entry_price', 0))
        if fill_price is not None and entry_price_val != 0:
            slippage_pct = round((float(fill_price) - entry_price_val) / entry_price_val * 100, 2)
        else:
            slippage_pct = None

        exit_fees = t.get('exit_fees')
        gross_proceeds = t.get('gross_proceeds')
        if exit_fees is not None and gross_proceeds is not None and float(gross_proceeds) > 0:
            fee_drag_pct = round(float(exit_fees) / float(gross_proceeds) * 100, 2)
        else:
            fee_drag_pct = None

        commission_gbp = t.get('commission_gbp')
        spread_cost_gbp = t.get('spread_cost_gbp')
        net_r_multiple = _compute_net_r(
            pnl=t.get('pnl', 0),
            commission_gbp=float(commission_gbp) if commission_gbp is not None else None,
            spread_cost_gbp=float(spread_cost_gbp) if spread_cost_gbp is not None else None,
            entry_price=float(t.get('entry_price', 0)),
            stop_price_at_entry=float(t['stop_price_at_entry']) if t.get('stop_price_at_entry') is not None else None,
            shares=float(t.get('shares', 0)),
            market=t.get('market', 'UK'),
            entry_fx_rate=float(t['entry_fx_rate']) if t.get('entry_fx_rate') is not None else None,
        )

        formatted_trades.append({
            "id": str(t.get('id', '')),
            "ticker": t['ticker'],
            "market": t['market'],
            "entry_date": str(t['entry_date']),
            "exit_date": str(t['exit_date']),
            "shares": float(t.get('shares', 0)),
            "entry_price": round(float(t.get('entry_price', 0)), 2),
            "exit_price": round(float(t.get('exit_price', 0)), 2),
            "pnl": round(t.get('pnl', 0), 2),
            "pnl_pct": round(t.get('pnl_pct', 0), 2),
            "pnl_percent": round(t.get('pnl_pct', 0), 2),
            "holding_days": t.get('holding_days'),
            "exit_reason": t.get('exit_reason', 'Unknown'),
            "entry_note": t.get('entry_note'),
            "exit_note": t.get('exit_note'),
            "tags": t.get('tags', []),
            "fill_price": float(fill_price) if fill_price is not None else None,
            "slippage_pct": slippage_pct,
            "fee_drag_pct": fee_drag_pct,
            "commission_gbp": float(commission_gbp) if commission_gbp is not None else None,
            "spread_cost_gbp": float(spread_cost_gbp) if spread_cost_gbp is not None else None,
            "net_r_multiple": net_r_multiple,
        })

    slippage_values = [t['slippage_pct'] for t in formatted_trades if t['slippage_pct'] is not None]
    avg_slippage_pct = round(sum(slippage_values) / len(slippage_values), 2) if slippage_values else None

    fee_drag_values = [t['fee_drag_pct'] for t in formatted_trades if t['fee_drag_pct'] is not None]
    avg_fee_drag_pct = round(sum(fee_drag_values) / len(fee_drag_values), 2) if fee_drag_values else None

    return {
        "total_trades": len(trades),
        "win_rate": round(win_rate, 1),
        "total_pnl": round(total_pnl, 2),
        "avg_slippage_pct": avg_slippage_pct,
        "avg_fee_drag_pct": avg_fee_drag_pct,
        "trades": formatted_trades
    }

def build_trade_history_csv(portfolio_id: str) -> str:
    """
    Build a UTF-8 CSV string of all closed trades for the given portfolio.

    Implements trade_endpoints.md v1.8.4 §GET /trades/export/csv.

    Column order (14 columns):
        ticker, market, entry_date, exit_date, shares, entry_price,
        exit_price, pnl, pnl_pct, holding_days, exit_reason, tags,
        entry_note, exit_note

    Null serialisation: all nullable fields (exit_reason, tags,
        entry_note, exit_note) are serialised as empty string — never
        as "null" or "None".

    Tags serialisation: list serialised as semicolon-separated string.
        Empty list or null becomes empty string.

    Returns:
        str: complete CSV content including header row.
             If no trades exist, returns header row only.
    """
    from database import get_all_closed_trades_for_csv_export

    COLUMNS = [
        "ticker", "market", "entry_date", "exit_date", "shares",
        "entry_price", "exit_price", "pnl", "pnl_pct", "holding_days",
        "exit_reason", "tags", "entry_note", "exit_note",
    ]

    rows = get_all_closed_trades_for_csv_export(portfolio_id)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=COLUMNS, extrasaction="ignore")
    writer.writeheader()

    for row in rows:
        # Serialise tags: list → semicolon-separated string, None → ""
        tags_raw = row.get("tags")
        if tags_raw and isinstance(tags_raw, list):
            row["tags"] = ";".join(tags_raw)
        else:
            row["tags"] = ""

        # Serialise nullable string fields: None → ""
        for field in ("exit_reason", "entry_note", "exit_note"):
            if row.get(field) is None:
                row[field] = ""

        # Serialise dates to YYYY-MM-DD string (psycopg2 may return date objects)
        for field in ("entry_date", "exit_date"):
            val = row.get(field)
            if val is not None and not isinstance(val, str):
                row[field] = str(val)

        writer.writerow(row)

    return output.getvalue()


# ---------------------------------------------------------------------------
# Trade reflection service — ST-02, EPIC-01, v1.9
# Spec: docs/specs/frontend/pages/trade_reflection.md §7
# ---------------------------------------------------------------------------

MAX_REFLECTION_FIELD_LENGTH = 500  # per trade_reflection.md §5


def _validate_reflection_fields(data: Dict) -> None:
    """Raise ValueError if any reflection text field exceeds the 500-char limit."""
    fields = ("trade_rationale", "what_worked", "what_didnt_work",
              "discipline_assessment", "key_takeaway")
    for field in fields:
        value = data.get(field)
        if value and len(value) > MAX_REFLECTION_FIELD_LENGTH:
            raise ValueError(
                f"Field '{field}' exceeds {MAX_REFLECTION_FIELD_LENGTH} characters "
                f"({len(value)} provided)."
            )


def _serialise_reflection(row: Dict) -> Dict:
    """Convert DB row to API-safe dict (stringify UUIDs and datetimes)."""
    return {
        "id": str(row["id"]),
        "trade_id": str(row["trade_id"]),
        "trade_rationale": row.get("trade_rationale"),
        "what_worked": row.get("what_worked"),
        "what_didnt_work": row.get("what_didnt_work"),
        "discipline_assessment": row.get("discipline_assessment"),
        "key_takeaway": row.get("key_takeaway"),
        "created_at": str(row["created_at"]) if row.get("created_at") else None,
        "updated_at": str(row["updated_at"]) if row.get("updated_at") else None,
    }


def get_reflection(trade_id: str) -> Optional[Dict]:
    """
    Return the saved reflection for a trade, or None if none exists.

    Raises:
        ValueError: never — absence of a reflection is not an error at this layer.
    """
    row = get_trade_reflection(trade_id)
    return _serialise_reflection(row) if row else None


def save_reflection(trade_id: str, data: Dict) -> Dict:
    """
    Create or update the reflection for a closed trade (upsert).

    Args:
        trade_id: UUID of the trade_history record.
        data: dict with any subset of the five reflection text fields.

    Returns:
        Serialised reflection dict.

    Raises:
        ValueError: if trade not found, or a field exceeds 500 chars.
    """
    _validate_reflection_fields(data)
    row = upsert_trade_reflection(trade_id, data)
    return _serialise_reflection(row)
