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
from services.drawdown_service import get_drawdown_fields

from database import (
    get_db,
    get_portfolio,
    get_positions,
    create_portfolio_snapshot,
    get_portfolio_snapshots,
    get_total_deposits_withdrawals,
    create_sector_regime_snapshot,
)

from utils.pricing import get_current_price, get_live_fx_rate, check_market_regime
from services.grace_service import compute_grace_days_remaining
from utils.formatting import decimal_to_float
from utils.position_lifecycle_states import GRACE, PROFITABLE, LOSING


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
    with get_db() as conn:
        portfolio = get_portfolio(conn=conn)
        if not portfolio:
            raise ValueError("Portfolio not found")

        portfolio_id = str(portfolio['id'])
        positions = get_positions(portfolio_id, status='open', conn=conn)

        cash = float(portfolio['cash'])

        if not positions:
            live_fx_rate = get_live_fx_rate()
            cash_summary = get_total_deposits_withdrawals(portfolio_id, conn=conn)
            net_cash_flow = cash_summary['net_cash_flow']
            drawdown_fields = get_drawdown_fields(
                portfolio_id=portfolio_id,
                current_total_value=cash,
                conn=conn,
            )
            return {
                "cash": cash,
                "cash_balance": cash,
                "total_value": cash,
                "open_positions_value": 0,
                "total_pnl": 0,
                "initial_value": net_cash_flow,
                "net_deposits": net_cash_flow,
                "last_updated": str(portfolio['last_updated']),
                "live_fx_rate": live_fx_rate,
                "current_drawdown_percent": drawdown_fields["current_drawdown_percent"],
                "peak_portfolio_value": drawdown_fields["peak_portfolio_value"],
                "portfolio_heat_percent": 0.0,
                "position_risks": [],
                "positions": [],
            }

        # Get live FX rate
        live_fx_rate = get_live_fx_rate()
        print(f"\n📊 /portfolio endpoint - fetching live prices for Dashboard")

        positions_list = []
        position_risks = []
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

            # Convert entry_price and current_stop to GBP for display
            # Spec: risk_dashboard.md §6.2 — all price columns in GBP
            if market == 'US':
                entry_price_gbp = round(entry_price / stored_fx_rate, 2)
                current_stop_gbp = round(pos.get("current_stop", 0) / stored_fx_rate, 2)
            else:
                entry_price_gbp = round(entry_price, 2)
                current_stop_gbp = round(pos.get("current_stop", 0), 2)

            holding_days = pos.get('holding_days', 0)

            if holding_days < 10:
                display_status = GRACE
            elif pnl_gbp > 0:
                display_status = PROFITABLE
            else:
                display_status = LOSING

            grace_period = holding_days < 10
            grace_days_remaining = compute_grace_days_remaining(
                grace_period=grace_period,
                holding_days=holding_days,
            )

            # Calculate Position Risk per metrics_definitions.md §Position Risk (TASK-06 — v1.7)
            # Uses initial_stop (entry stop), not trailing current_stop
            # Formula: (entry_price_native - initial_stop_native) * shares * fx_adjustment
            # fx_adjustment = 1/fx_rate for US (USD→GBP), 1.0 for UK
            initial_stop = pos.get("initial_stop")
            if initial_stop is not None and float(initial_stop) > 0:
                initial_stop = float(initial_stop)
                risk_native = max(0.0, entry_price - initial_stop)
                if market == 'US':
                    fx_adj = 1.0 / stored_fx_rate if stored_fx_rate else 1.0 / live_fx_rate
                else:
                    fx_adj = 1.0
                position_risk_gbp = round(risk_native * shares * fx_adj, 2)
            else:
                position_risk_gbp = 0.0

            position_risks.append({
                "ticker": pos["ticker"],
                "position_risk_gbp": position_risk_gbp,
            })

            positions_list.append({
                "id": str(pos["id"]),
                "ticker": pos["ticker"],
                "market": market,
                "entry_date": str(pos["entry_date"]),
                "entry_price": entry_price_gbp,
                "shares": shares,
                "current_price": round(current_price_gbp, 2),
                "current_value": round(current_value_gbp, 2),
                "pnl": round(pnl_gbp, 2),
                "pnl_pct": round(pnl_pct, 2),
                "current_stop": current_stop_gbp,
                "holding_days": holding_days,
                "status": "open",
                "display_status": display_status,
                "fx_rate": stored_fx_rate,
                "grace_period": grace_period,
                "grace_days_remaining": grace_days_remaining,
                "live_fx_rate": live_fx_rate,
            })

        total_value = cash + total_positions_value_gbp

        # Calculate Portfolio Heat per metrics_definitions.md §Portfolio Heat (TASK-07 — v1.7)
        # Formula: Sum(Position_Risk_GBP) / Portfolio_Value_GBP * 100
        total_risk_gbp = sum(r["position_risk_gbp"] for r in position_risks)
        portfolio_heat_percent = round(total_risk_gbp / total_value * 100, 2) if total_value > 0 else 0.0

        # Calculate TRUE portfolio P&L accounting for deposits/withdrawals
        # Single connection: reuse conn established at top of function
        cash_summary = get_total_deposits_withdrawals(portfolio_id, conn=conn)
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

        # B1 — Current drawdown fields (QWB BLG-FEAT-01)
        # Spec: portfolio_endpoints.md v1.8.2, metrics_definitions.md v1.5.8
        drawdown_fields = get_drawdown_fields(
            portfolio_id=portfolio_id,
            current_total_value=total_value,
            conn=conn,
        )

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
            "current_drawdown_percent": drawdown_fields["current_drawdown_percent"],
            "peak_portfolio_value": drawdown_fields["peak_portfolio_value"],
            "portfolio_heat_percent": portfolio_heat_percent,
            "position_risks": position_risks,
            "positions": positions_list,
        }


def calculate_prospective_heat(
    entry_price: float,
    stop_price: float,
    shares: float,
    market: str = "UK",
    fx_rate: float = None,
) -> Dict:
    """
    Calculate portfolio heat percentage if a prospective position were added.

    Shared calculation used by GET /portfolio/prospective-heat
    (routers/prospective_heat.py) and POST /portfolio/size's
    heat_impact_percent field (ST-05, BLG-FEAT-91, services/sizing_service.py)
    — extracted here (ST-05) so both call sites use one implementation
    rather than duplicating the risk-basis math.

    Calculation rules: docs/specs/metrics_definitions.md §Portfolio Heat

    Returns:
        {"valid": False, "error": <str>} for invalid inputs or unusable
        portfolio state, or:
        {
            "valid": True,
            "current_heat_percent": float,
            "prospective_heat_percent": float,
            "incremental_heat_percent": float,
            "prospective_risk_gbp": float,
            "portfolio_value_gbp": float,
            "fx_rate_used": float,
        }
    """
    if stop_price >= entry_price:
        return {"valid": False, "error": "stop_price must be less than entry_price"}
    if shares <= 0:
        return {"valid": False, "error": "shares must be greater than 0"}
    if entry_price <= 0 or stop_price <= 0:
        return {"valid": False, "error": "entry_price and stop_price must be greater than 0"}

    market = (market or "UK").upper()
    if market == "US":
        fx_rate_used = float(fx_rate) if fx_rate else get_live_fx_rate()
    else:
        fx_rate_used = 1.0

    portfolio = get_portfolio_summary()
    portfolio_value_gbp = portfolio.get("total_value", 0.0)

    if portfolio_value_gbp <= 0:
        return {"valid": False, "error": "portfolio value is zero; cannot calculate heat"}

    position_risks = portfolio.get("position_risks", [])
    current_risk_gbp = sum(r.get("position_risk_gbp", 0.0) for r in position_risks)

    prospective_risk_gbp = round((entry_price - stop_price) * shares / fx_rate_used, 2)

    current_heat_percent = round(current_risk_gbp / portfolio_value_gbp * 100, 2)
    total_risk_gbp = current_risk_gbp + prospective_risk_gbp
    prospective_heat_percent = round(total_risk_gbp / portfolio_value_gbp * 100, 2)
    incremental_heat_percent = round(prospective_heat_percent - current_heat_percent, 2)

    return {
        "valid": True,
        "current_heat_percent": current_heat_percent,
        "prospective_heat_percent": prospective_heat_percent,
        "incremental_heat_percent": incremental_heat_percent,
        "prospective_risk_gbp": prospective_risk_gbp,
        "portfolio_value_gbp": round(portfolio_value_gbp, 2),
        "fx_rate_used": round(fx_rate_used, 4),
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

    _snapshot_sector_regime(portfolio_id, snapshot_data['snapshot_date'], positions)

    print(f"✓ Snapshot created:")
    print(f"   Date: {snapshot_data['snapshot_date']}")
    print(f"   Total Value: £{snapshot_data['total_value']:,.2f}")
    print(f"   P&L: £{snapshot_data['total_pnl']:+,.2f}")
    print(f"   Positions: {position_count}\n")

    return decimal_to_float(snapshot)


def _snapshot_sector_regime(portfolio_id: str, snapshot_date, positions: list) -> None:
    """Best-effort daily capture for the sector/regime exposure trend (ST-02,
    EPIC-02, v7.9, BLG-FEAT-67). Failure here must never break the main
    portfolio snapshot it's called from — same fail-open convention as
    create_position_audit_log_entry / create_claude_audit_entry.

    Layering note: reuses compute_sector_exposure/_get_ticker_sector_map from
    routers.portfolio_risk (pure functions, no FastAPI dependency) rather than
    duplicating the sector-computation logic a second time.
    """
    try:
        from routers.portfolio_risk import compute_sector_exposure, _get_ticker_sector_map

        with get_db() as conn:
            ticker_sector_map = _get_ticker_sector_map(conn)
        live_fx_rate = get_live_fx_rate()
        exposure = compute_sector_exposure(positions, ticker_sector_map, live_fx_rate)

        regime = check_market_regime()
        create_sector_regime_snapshot(
            portfolio_id,
            snapshot_date,
            exposure["sectors"],
            regime.get("spy_risk_on"),
            regime.get("ftse_risk_on"),
        )
    except Exception as exc:
        print(f"  Warning: sector/regime snapshot failed ({exc}) — main portfolio snapshot unaffected")


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
