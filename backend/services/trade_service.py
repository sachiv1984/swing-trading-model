"""
Trade Service

Business logic for trade history and statistics.

All functions are independent of FastAPI for maximum testability.
"""

import csv
import io

from typing import Dict, List
from database import get_portfolio, get_trade_history
from utils.formatting import decimal_to_float


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
    trades = get_trade_history(portfolio_id)
    trades = [decimal_to_float(t) for t in trades]
    
    if not trades:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "trades": []
        }
    
    # Calculate statistics
    total_pnl = sum(t.get('pnl', 0) for t in trades)
    wins = len([t for t in trades if t.get('pnl', 0) > 0])
    win_rate = (wins / len(trades)) * 100
    
    # Format trades for frontend
    formatted_trades = []
    for t in trades:
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
            "tags": t.get('tags', [])
        })
    
    return {
        "total_trades": len(trades),
        "win_rate": round(win_rate, 1),
        "total_pnl": round(total_pnl, 2),
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
    from database import get_all_trade_history

    COLUMNS = [
        "ticker", "market", "entry_date", "exit_date", "shares",
        "entry_price", "exit_price", "pnl", "pnl_pct", "holding_days",
        "exit_reason", "tags", "entry_note", "exit_note",
    ]

    rows = get_all_trade_history(portfolio_id)

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
