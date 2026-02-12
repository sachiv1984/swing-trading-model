"""
Portfolio Service

Business logic for portfolio management including:
- Portfolio summary with P&L calculation
- Daily snapshot creation
- Performance history retrieval

All functions are independent of FastAPI for maximum testability.
"""

from typing import Dict, List
from datetime import datetime

from database import (
    get_portfolio,
    get_positions,
    create_portfolio_snapshot,
    get_portfolio_snapshots,
    get_total_deposits_withdrawals
)

from utils.pricing import get_current_price, get_live_fx_rate
from utils.formatting import decimal_to_float


def get_portfolio_summary() -> Dict:
    """
    Get comprehensive portfolio summary with live prices
    
    Returns:
        Dictionary with:
            - cash: Current cash balance (GBP)
            - cash_balance: Same as cash
            - total_value: Total portfolio value (cash + positions)
            - open_positions_value: Total value of open positions
            - total_pnl: True portfolio P&L (accounts for deposits/withdrawals)
            - initial_value: Initial portfolio value
            - net_deposits: Total deposits - withdrawals
            - last_updated: Last update timestamp
            - live_fx_rate: Current GBP/USD rate
            - positions: List of position summaries
    
    Raises:
        ValueError: If portfolio not found
    
    Note:
        - Always fetches live prices for positions
        - Calculates true P&L using net cash flow
        - Converts all values to GBP for consistency
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    positions = get_positions(portfolio_id, status='open')
    
    cash = float(portfolio['cash'])
    
    if not positions:
        return {
            "cash": cash,
            "cash_balance": cash,
            "total_value": cash,
            "open_positions_value": 0,
            "total_pnl": 0,
            "last_updated": str(portfolio['last_updated']),
            "live_fx_rate": 1.27,
            "positions": []
        }
    
    # Get live FX rate
    live_fx_rate = get_live_fx_rate()
    print(f"\n📊 /portfolio endpoint - fetching live prices for Dashboard")
    
    positions_list = []
    total_positions_value_gbp = 0
    
    for pos in positions:
        pos = decimal_to_float(pos)
        
        # FETCH LIVE PRICE
        print(f"   Fetching live price for {pos['ticker']}...")
        live_price = get_current_price(pos['ticker'])
        
        if live_price:
            # Fix UK stocks: Yahoo returns pence
            if pos['market'] == 'UK' and live_price > 1000:
                live_price = live_price / 100
                print(f"   ✓ Converted {pos['ticker']} from pence to pounds: {live_price}")
            current_price_native = live_price
            print(f"   ✓ Live price: {current_price_native:.2f}")
        else:
            # Fallback to stored price
            print(f"   ⚠️  Using stored price for {pos['ticker']}")
            stored_price = pos.get('current_price', pos['entry_price'])
            if pos['market'] == 'US' and stored_price < 500:
                # Appears to be GBP, convert back to USD estimate
                current_price_native = stored_price * 1.38
                print(f"   ⚠️  Stored price appears to be GBP, estimated USD: {current_price_native:.2f}")
            else:
                current_price_native = stored_price
        
        shares = pos['shares']
        market = pos['market']
        stored_fx_rate = pos.get('fx_rate', 1.27)
        
        # Convert to GBP for Dashboard
        if market == 'US':
            current_price_gbp = current_price_native / live_fx_rate
            print(f"   💱 ${current_price_native:.2f} → £{current_price_gbp:.2f}")
        else:
            current_price_gbp = current_price_native
        
        current_value_gbp = current_price_gbp * shares
        total_positions_value_gbp += current_value_gbp
        
        # Calculate P&L
        entry_price = pos.get('fill_price', pos['entry_price']) if market == 'US' else pos['entry_price']
        pnl_native = (current_price_native - entry_price) * shares
        
        if market == 'US':
            pnl_gbp = pnl_native / live_fx_rate
        else:
            pnl_gbp = pnl_native
        
        pnl_pct = ((current_price_native - entry_price) / entry_price) * 100 if entry_price > 0 else 0
        holding_days = pos.get('holding_days', 0)
        
        if holding_days < 10:
            display_status = "GRACE"
        elif pnl_gbp > 0:
            display_status = "PROFITABLE"
        else:
            display_status = "LOSING"
        
        positions_list.append({
            "id": str(pos['id']),
            "ticker": pos['ticker'],
            "market": market,
            "entry_date": str(pos['entry_date']),
            "entry_price": round(entry_price, 2),
            "shares": shares,
            "current_price": round(current_price_gbp, 2),
            "current_value": round(current_value_gbp, 2),
            "pnl": round(pnl_gbp, 2),
            "pnl_pct": round(pnl_pct, 2),
            "current_stop": round(pos.get('current_stop', 0), 2),
            "holding_days": holding_days,
            "status": display_status,
            "fx_rate": stored_fx_rate,
            "live_fx_rate": live_fx_rate
        })
    
    total_value = cash + total_positions_value_gbp
    
    # Calculate TRUE portfolio P&L accounting for deposits/withdrawals
    cash_summary = get_total_deposits_withdrawals(portfolio_id)
    net_cash_flow = cash_summary['net_cash_flow']
    
    # Total cost of all positions
    total_cost_of_positions = sum(float(pos.get('total_cost', 0)) for pos in positions)
    
    # True P&L = Current Value - Net Cash Flow
    true_total_pnl = total_value - net_cash_flow
    
    print(f"\n✓ Portfolio calculated:")
    print(f"   Total positions value: £{total_positions_value_gbp:.2f}")
    print(f"   Total cost of positions: £{total_cost_of_positions:.2f}")
    print(f"   Cash: £{cash:.2f}")
    print(f"   Total value: £{total_value:.2f}")
    print(f"   Net cash flow (deposits-withdrawals): £{net_cash_flow:.2f}")
    print(f"   True total P&L: £{true_total_pnl:+.2f}\n")
    
    return {
        "cash": cash,
        "cash_balance": cash,
        "total_value": total_value,
        "open_positions_value": total_positions_value_gbp,
        "total_pnl": true_total_pnl,
        "initial_value": net_cash_flow,
        "net_deposits": net_cash_flow,
        "last_updated": str(portfolio['last_updated']),
        "live_fx_rate": live_fx_rate,
        "positions": positions_list
    }


def create_daily_snapshot() -> Dict:
    """
    Create a daily snapshot of portfolio performance
    
    Returns:
        Dictionary with snapshot data:
            - portfolio_id: Portfolio UUID
            - snapshot_date: Date of snapshot
            - total_value: Total portfolio value
            - cash_balance: Cash balance
            - positions_value: Value of positions
            - total_pnl: Total P&L
            - position_count: Number of open positions
    
    Raises:
        ValueError: If portfolio not found
        
    Note:
        - Uses UPSERT logic (updates if snapshot exists for today)
        - Should be run daily (automated via cron)
        - Recommended time: 4 PM UTC on weekdays
    """
    print("\n📸 Creating portfolio snapshot...")
    
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    # Get current portfolio data
    portfolio_data = get_portfolio_summary()
    
    # Count open positions
    portfolio_id = str(portfolio['id'])
    positions = get_positions(portfolio_id, status='open')
    position_count = len(positions) if positions else 0
    
    # Create snapshot
    snapshot_data = {
        'portfolio_id': portfolio_id,
        'snapshot_date': datetime.now().date(),
        'total_value': round(portfolio_data['total_value'], 2),
        'cash_balance': round(portfolio_data['cash'], 2),
        'positions_value': round(portfolio_data['open_positions_value'], 2),
        'total_pnl': round(portfolio_data['total_pnl'], 2),
        'position_count': position_count
    }
    
    snapshot = create_portfolio_snapshot(snapshot_data)
    
    print(f"✓ Snapshot created:")
    print(f"   Date: {snapshot_data['snapshot_date']}")
    print(f"   Total Value: £{snapshot_data['total_value']:,.2f}")
    print(f"   P&L: £{snapshot_data['total_pnl']:+,.2f}")
    print(f"   Positions: {position_count}\n")
    
    return decimal_to_float(snapshot)


def get_performance_history(days: int = 30) -> List[Dict]:
    """
    Get portfolio performance history for charts
    
    Args:
        days: Number of days of history to retrieve (default 30)
    
    Returns:
        List of snapshot dictionaries with:
            - date: Snapshot date (YYYY-MM-DD)
            - total_value: Total portfolio value
            - cash_balance: Cash balance
            - positions_value: Value of positions
            - total_pnl: Total P&L
            - position_count: Number of positions
    
    Raises:
        ValueError: If portfolio not found
        
    Note:
        - Returns empty list if no snapshots exist
        - Sorted by date (most recent first)
        - Used for performance charts in frontend
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    snapshots = get_portfolio_snapshots(portfolio_id, days)
    
    if not snapshots:
        print(f"⚠️  No portfolio history found (create snapshots with POST /portfolio/snapshot)")
        return []
    
    # Format for frontend
    history = []
    for snap in snapshots:
        history.append({
            'date': str(snap['snapshot_date']),
            'total_value': float(snap['total_value']),
            'cash_balance': float(snap['cash_balance']),
            'positions_value': float(snap['positions_value']),
            'total_pnl': float(snap['total_pnl']),
            'position_count': snap.get('position_count', 0)
        })
    
    print(f"✓ Retrieved {len(history)} snapshots from last {days} days")
    
    return history
