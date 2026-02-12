"""
Trade Service

Business logic for trade history and statistics.

All functions are independent of FastAPI for maximum testability.
"""

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
            - trades: List of trade dictionaries
    
    Raises:
        ValueError: If portfolio not found
        
    Note:
        - Only includes closed trades
        - Sorted by exit date (most recent first)
        - Calculates win rate and totals dynamically
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
            "exit_reason": t.get('exit_reason', 'Unknown')
        })
    
    return {
        "total_trades": len(trades),
        "win_rate": round(win_rate, 1),
        "total_pnl": round(total_pnl, 2),
        "trades": formatted_trades
    }
