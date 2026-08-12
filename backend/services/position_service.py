"""
Position Service

Business logic for position management including:
- Position retrieval with live prices
- Daily position analysis with stop loss updates
- Position entry with fee calculation and validation
- Position exit with trade history recording

All functions are independent of FastAPI for maximum testability.
"""
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from decimal import Decimal
from services.grace_service import compute_grace_days_remaining
from services.sector_service import get_sector_and_industry
from utils.position_lifecycle_states import GRACE, PROFITABLE, LOSING


from database import (
    get_portfolio,
    get_positions,
    update_position,
    create_position,
    update_portfolio_cash,
    get_settings,
    create_trade_history,
    update_position_note,
    update_position_tags,
    get_all_tags,
    search_positions_by_tags,
    get_trade_plans_by_position,
    get_unlinked_trade_plan_for_entry,
    get_trade_plan_by_id,
    update_trade_plan,
    get_signals,
    ensure_planned_entry_price_column,
    mark_position_reviewed as db_mark_position_reviewed,
    create_position_audit_log_entry,
)
from strategy_version_registry import get_current_strategy_version

from utils.pricing import (
    get_current_price,
    get_live_fx_rate,
    check_market_regime,
    calculate_atr
)

from utils.calculations import (
    calculate_position_pnl,
    calculate_holding_days,
    calculate_trailing_stop,
    should_exit_position,
    calculate_uk_entry_fees,
    calculate_us_entry_fees,
    calculate_exit_proceeds,
    calculate_realized_pnl,
    calculate_initial_stop
)

from utils.formatting import decimal_to_float


# ============================================================================
# GET POSITIONS
# ============================================================================

def get_positions_with_prices() -> List[Dict]:
    """
    Get all open positions with live prices and P&L calculations
    
    Returns:
        List of position dictionaries with:
            - Live current prices (native and GBP)
            - P&L calculations (amount and percentage)
            - Stop prices (considering grace period)
            - Holding days and grace period status
            - Display status (GRACE/PROFITABLE/LOSING)
    
    Raises:
        ValueError: If portfolio not found
        
    Note:
        - Always fetches live prices from Yahoo Finance
        - Converts prices to GBP for portfolio aggregation
        - Grace period = first 10 days (no active stop)
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    positions = get_positions(portfolio_id, status='open')
    
    if not positions:
        return []
    
    # Get live FX rate for USD/GBP conversions
    live_fx_rate = get_live_fx_rate()
    
    print(f"\n📊 Fetching live prices for {len(positions)} position(s)")
    
    positions_list = []
    
    for pos in positions:
        pos = decimal_to_float(pos)
        
        # ALWAYS fetch live price
        print(f"   Fetching {pos['ticker']}...")
        live_price = get_current_price(pos['ticker'])
        
        if live_price:
            # Fix UK stocks: Yahoo returns pence
            if pos['market'] == 'UK' and live_price > 1000:
                live_price = live_price / 100
            current_price_native = live_price
            print(f"   ✓ Live: {current_price_native:.2f}")
        else:
            # Fallback to stored price
            print(f"   ⚠️  Using stored price")
            current_price_native = pos.get('current_price', pos['entry_price'])
        
        # Calculate P&L
        if pos['market'] == 'US':
            entry_price_display = pos.get('fill_price', pos['entry_price'] * (pos.get('fx_rate', 1.27)))
        else:
            entry_price_display = pos['entry_price']
        
        pnl_native, pnl_gbp, pnl_pct = calculate_position_pnl(
            entry_price=entry_price_display,
            current_price=current_price_native,
            shares=pos['shares'],
            market=pos['market'],
            live_fx_rate=live_fx_rate
        )
        
        # Convert to GBP for Dashboard calculations
        if pos['market'] == 'US':
            current_price_gbp = current_price_native / live_fx_rate
            print(f"   💱 ${current_price_native:.2f} → £{current_price_gbp:.2f}")
        else:
            current_price_gbp = current_price_native
        
        # Calculate holding days and grace period
        holding_days = calculate_holding_days(str(pos['entry_date']))
        grace_period = holding_days < 10
        
        # Stop price handling
        if grace_period:
            # During grace period: No stop shown
            stop_price_native = 0
            print(f"   🆕 Grace period: {holding_days}/10 days - No stop active")
        else:
            # After grace period: Show stop from database (already in native currency)
            stop_price_native = pos.get('current_stop', pos.get('initial_stop', 0))
        
        # Convert stop to GBP for portfolio aggregation
        if pos['market'] == 'US':
            stop_price_gbp = stop_price_native / live_fx_rate if stop_price_native > 0 else 0
        else:
            stop_price_gbp = stop_price_native
        
        # Fetch sector/industry from Yahoo Finance (DS-03)
        sector, industry = get_sector_and_industry(pos['ticker'], pos['market'])

        # Display ticker without .L suffix
        display_ticker = pos['ticker'].replace('.L', '') if pos['market'] == 'UK' else pos['ticker']
        
        # Determine status
        if grace_period:
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

        
        initial_stop = pos.get("initial_stop")

        # Fallbacks if your DB uses different column names
        if initial_stop is None:
            initial_stop = pos.get("initial_stop_price", pos.get("stop_price"))

        # ST-01 (BLG-FEAT-46): current_trailing_stop — always the computed stop value,
        # non-zero even during grace period (informational; stop_price is 0 during grace)
        current_trailing_stop_native = pos.get('current_stop', 0) or 0
        if pos['market'] == 'US':
            current_trailing_stop_gbp = current_trailing_stop_native / live_fx_rate if current_trailing_stop_native > 0 else 0
        else:
            current_trailing_stop_gbp = current_trailing_stop_native

        # risk_off_exit — per-position alert flag, set by nightly risk-off job (ST-05)
        risk_off_exit = bool(pos.get('risk_off_exit', False))

        # last_reviewed_at — position review cadence nudge (ST-15, BLG-FEAT-68, v7.0)
        last_reviewed_at = pos.get('last_reviewed_at')
        last_reviewed_at = last_reviewed_at.isoformat() if last_reviewed_at else None

        # Build position dict
        positions_list.append({
            "id": str(pos['id']),
            "ticker": display_ticker,
            "market": pos['market'],
            "initial_stop": round(initial_stop, 2) if initial_stop is not None else None,
            "current_trailing_stop": round(current_trailing_stop_gbp, 2),
            "risk_off_exit": risk_off_exit,
            "entry_date": str(pos['entry_date']),
            "entry_price": round(entry_price_display, 2),
            "shares": pos['shares'],
            "current_price": round(current_price_gbp, 2),
            "current_price_native": round(current_price_native, 2),
            "stop_price": round(stop_price_gbp, 2),
            "stop_price_native": round(stop_price_native, 2),
            "pnl": round(pnl_gbp, 2),
            "pnl_percent": round(pnl_pct, 2),
            "holding_days": holding_days,
            "status": "open",
            "display_status": display_status,
            "exit_reason": None,
            "grace_period": grace_period,
            "grace_days_remaining": grace_days_remaining,
            "stop_reason": f"Grace period ({holding_days}/10 days)" if grace_period else "Active",
            "atr_value": pos.get('atr', 0),
            "fx_rate": pos.get('fx_rate', 1.0),
            "live_fx_rate": live_fx_rate,
            "total_cost": round(pos.get('total_cost', 0), 2),
            "entry_note": pos.get('entry_note'),
            "exit_note": pos.get('exit_note'),
            "tags": pos.get('tags', []),
            "sector": sector,
            "industry": industry,
            "last_reviewed_at": last_reviewed_at,
        })
    
    print(f"✓ Returned {len(positions_list)} positions with live prices\n")
    
    return positions_list


# ============================================================================
# ANALYZE POSITIONS (Daily Analysis)
# ============================================================================

def analyze_positions() -> Dict:
    """
    Run daily position analysis with live prices and market regime
    
    Performs:
        - Fetches live prices for all open positions
        - Calculates P&L using current FX rates
        - Updates trailing stops based on profitability
        - Checks market regime (SPY/FTSE vs 200-day MA)
        - Determines EXIT or HOLD for each position
        - Updates position data in database
    
    Returns:
        Dictionary with:
            - analysis_date: Date of analysis
            - market_regime: SPY and FTSE risk status
            - live_fx_rate: Current GBP/USD rate
            - summary: Portfolio totals and exit count
            - actions: List of position actions (HOLD/EXIT)
    
    Raises:
        ValueError: If portfolio not found
    """
    print("\n" + "="*70)
    print("🔍 STARTING POSITION ANALYSIS")
    print("="*70)
    
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    positions = get_positions(portfolio_id, status='open')
    
    if not positions:
        print("✓ No open positions to analyze")
        return {
            "analysis_date": datetime.now().strftime('%Y-%m-%d'),
            "summary": {
                "total_value": 0,
                "total_pnl": 0,
                "exit_count": 0
            },
            "actions": []
        }
    
    # Get live FX rate
    live_fx_rate = get_live_fx_rate()
    
    # Get market regime
    print("\n📊 Checking market regime...")
    market_regime = check_market_regime()
    print(f"   SPY: {'🟢 Risk On' if market_regime['spy_risk_on'] else '🔴 Risk Off'}")
    print(f"   FTSE: {'🟢 Risk On' if market_regime['ftse_risk_on'] else '🔴 Risk Off'}")
    
    # Get settings for stop calculations
    settings_list = get_settings()
    settings_dict = settings_list[0] if settings_list else {}
    
    actions = []
    total_value_gbp = 0
    total_pnl_gbp = 0
    
    print(f"\n💼 Analyzing {len(positions)} position(s)...")
    
    for pos in positions:
        pos = decimal_to_float(pos)
        
        print(f"\n{'='*70}")
        print(f"📈 Analyzing: {pos['ticker']} ({pos['market']})")
        print(f"{'='*70}")
        
        # Get live price
        print(f"   🔍 Fetching live price from Yahoo Finance...")
        live_price = get_current_price(pos['ticker'])
        
        # Determine entry price
        entry_price = pos.get('fill_price', pos['entry_price']) if pos['market'] == 'US' else pos['entry_price']
        
        if live_price:
            # Fix UK stocks: Yahoo returns pence
            if pos['market'] == 'UK' and live_price > 1000:
                live_price = live_price / 100
                print(f"   ✓ Converted from pence to pounds")
            
            print(f"   ✓ Live price: {live_price:.2f}")
            print(f"   Entry price: {entry_price:.2f}")
            print(f"   Change: {((live_price - entry_price) / entry_price * 100):+.2f}%")
            current_price = live_price
        else:
            print(f"   ⚠️  Failed to fetch live price")
            print(f"   Using stored price: {pos.get('current_price', entry_price):.2f}")
            current_price = pos.get('current_price', entry_price)
        
        # Calculate metrics
        shares = pos['shares']
        
        # Calculate value and P&L
        current_value_native = current_price * shares
        if pos['market'] == 'US':
            current_value_gbp = current_value_native / live_fx_rate
            print(f"   💱 Converting USD to GBP (LIVE rate): ${current_value_native:.2f} / {live_fx_rate:.4f} = £{current_value_gbp:.2f}")
        else:
            current_value_gbp = current_value_native
        
        pnl_native, pnl_gbp, pnl_pct = calculate_position_pnl(
            entry_price=entry_price,
            current_price=current_price,
            shares=shares,
            market=pos['market'],
            live_fx_rate=live_fx_rate
        )
        
        if pos['market'] == 'US':
            print(f"   💰 P&L in GBP (LIVE rate): ${pnl_native:.2f} / {live_fx_rate:.4f} = £{pnl_gbp:.2f}")
        
        total_value_gbp += current_value_gbp
        total_pnl_gbp += pnl_gbp
        
        # Calculate holding days
        holding_days = calculate_holding_days(str(pos['entry_date']))
        
        print(f"   Holdings: {shares} shares = £{current_value_gbp:.2f} (GBP)")
        print(f"   P&L: £{pnl_gbp:+.2f} ({pnl_pct:+.2f}%)")
        print(f"   Days held: {holding_days}")
        
        # Get current stop from database (stored in NATIVE currency)
        current_stop_native = pos.get('current_stop', pos.get('initial_stop', 0))
        
        # Check grace period
        grace_period = holding_days < 10
        
        # Calculate trailing stop
        if grace_period:
            trailing_stop_native = current_stop_native
            display_stop_native = 0
            stop_reason = f"Grace period ({holding_days}/10 days)"
            atr_mult = 0
            print(f"   🆕 Grace period active - no stop loss")
        else:
            # Get ATR value
            atr_value = pos.get('atr')
            if not atr_value or atr_value == 0:
                print(f"   ⚠️  No ATR in database, calculating...")
                atr_value = calculate_atr(pos['ticker'])
                
                if atr_value and atr_value > 0:
                    update_position(str(pos['id']), {'atr': round(atr_value, 4)})
                    print(f"   💾 Stored calculated ATR: {atr_value:.2f}")
            
            if atr_value and atr_value > 0:
                # Get entry price in native currency
                entry_price_native = pos.get('fill_price', entry_price) if pos['market'] == 'US' else entry_price
                
                # Calculate trailing stop
                trailing_stop_native, stop_reason, atr_mult = calculate_trailing_stop(
                    current_price=current_price,
                    atr=atr_value,
                    is_profitable=(pnl_native > 0),
                    current_stop=current_stop_native,
                    entry_price=entry_price_native,
                    settings=settings_dict
                )
                
                display_stop_native = trailing_stop_native
                
                currency_symbol = "$" if pos['market'] == 'US' else "£"
                if trailing_stop_native > current_stop_native:
                    print(f"   📈 Stop moved up: {currency_symbol}{current_stop_native:.2f} → {currency_symbol}{trailing_stop_native:.2f}")
                else:
                    print(f"   📊 Stop unchanged: {currency_symbol}{trailing_stop_native:.2f}")
            else:
                # No ATR available, use entry price as stop
                entry_price_native = pos.get('fill_price', entry_price) if pos['market'] == 'US' else entry_price
                trailing_stop_native = max(current_stop_native, entry_price_native)
                display_stop_native = trailing_stop_native
                stop_reason = "No ATR - stop at entry"
                atr_mult = 0
                print(f"   ⚠️  No ATR value available, stop at entry level")
        
        # Determine action
        is_uk = pos['market'] == 'UK'
        market_risk_on = market_regime['ftse_risk_on'] if is_uk else market_regime['spy_risk_on']
        
        should_exit, exit_reason = should_exit_position(
            current_price=current_price,
            stop_price=trailing_stop_native,
            holding_days=holding_days,
            market_risk_on=market_risk_on,
            grace_period_days=10
        )
        
        if should_exit:
            action = "EXIT"
            if exit_reason == "Risk-Off Signal":
                stop_reason = "Market risk-off"
                print(f"   🔴 EXIT: Market risk-off")
            else:
                stop_reason = "Stop triggered"
                currency_symbol = "$" if pos['market'] == 'US' else "£"
                print(f"   🔴 EXIT: Stop loss hit ({currency_symbol}{trailing_stop_native:.2f})")
        else:
            action = "HOLD"
            print(f"   ✅ HOLD: {stop_reason}")
        
        # Update position in database
        if live_price:
            print(f"   💾 Updating position in database...")
            update_position(str(pos['id']), {
                'current_price': round(current_price, 4),
                'current_stop': round(trailing_stop_native, 2),
                'holding_days': holding_days,
                'pnl': round(pnl_gbp, 2),
                'pnl_pct': round(pnl_pct, 2)
            })
        
        # Add to actions
        actions.append({
            "ticker": pos['ticker'],
            "market": pos['market'],
            "action": action,
            "exit_reason": exit_reason,
            "entry_price": round(entry_price, 2),
            "current_price": round(current_price, 2),
            "shares": shares,
            "pnl": round(pnl_gbp, 2),
            "pnl_pct": round(pnl_pct, 2),
            "current_stop": round(display_stop_native, 2),
            "holding_days": holding_days,
            "stop_reason": stop_reason,
            "grace_period": grace_period
        })
    
    exit_count = len([a for a in actions if a['action'] == 'EXIT'])
    
    print(f"\n{'='*70}")
    print(f"📊 ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"Total Value: £{total_value_gbp:.2f} (GBP)")
    print(f"Total P&L: £{total_pnl_gbp:+.2f} (GBP)")
    print(f"Live FX Rate: {live_fx_rate:.4f}")
    print(f"Exit Signals: {exit_count}")
    print("="*70 + "\n")
    
    return {
        "analysis_date": datetime.now().strftime('%Y-%m-%d'),
        "market_regime": market_regime,
        "live_fx_rate": live_fx_rate,
        "summary": {
            "total_value": round(total_value_gbp, 2),
            "total_pnl": round(total_pnl_gbp, 2),
            "exit_count": exit_count
        },
        "actions": actions
    }


# ============================================================================
# NIGHTLY TRAILING STOP UPDATE (ST-01 / BLG-FEAT-46)
# ============================================================================

# Production strategy constants — must match production_strategy.py exactly
_INITIAL_ATR_MULT = 5.0   # Wide stop when position not in profit
_PROFIT_ATR_MULT = 2.0    # Tight stop when position in profit
_ATR_PERIOD = 14          # 14-day ATR


def run_nightly_trailing_stop_update() -> Dict:
    """
    Nightly job: recompute trailing stop for every open position and store result.

    Strategy (production_strategy.py profit-lock logic):
      - In profit: new_stop = current_price − (PROFIT_ATR_MULT × ATR)
      - Not in profit: new_stop = entry_price − (INITIAL_ATR_MULT × ATR)
      - Ratchet: stored stop only ever moves up — max(current_stop, new_stop)

    Constants:
      INITIAL_ATR_MULT=5, PROFIT_ATR_MULT=2, ATR_PERIOD=14

    Returns summary dict with per-position results.
    """
    _SETTINGS = {
        'atr_multiplier_trailing': _PROFIT_ATR_MULT,
        'atr_multiplier_initial': _INITIAL_ATR_MULT,
    }

    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")

    portfolio_id = str(portfolio['id'])
    positions = get_positions(portfolio_id, status='open')
    live_fx_rate = get_live_fx_rate()

    results = []
    for pos in positions:
        pos = decimal_to_float(pos)
        position_id = str(pos['id'])

        live_price = get_current_price(pos['ticker'])
        if not live_price:
            results.append({"ticker": pos['ticker'], "status": "skipped", "reason": "price unavailable"})
            continue

        if pos['market'] == 'UK' and live_price > 1000:
            live_price = live_price / 100

        entry_price = pos.get('fill_price', pos['entry_price']) if pos['market'] == 'US' else pos['entry_price']

        # Recalculate ATR at _ATR_PERIOD to ensure freshness
        atr_value = calculate_atr(pos['ticker'], period=_ATR_PERIOD)
        if not atr_value or atr_value == 0:
            atr_value = pos.get('atr', 0)
        if not atr_value or atr_value == 0:
            results.append({"ticker": pos['ticker'], "status": "skipped", "reason": "ATR unavailable"})
            continue

        if pos['market'] == 'UK' and atr_value > 100:
            atr_value = atr_value / 100

        current_stop_native = pos.get('current_stop', pos.get('initial_stop', 0)) or 0
        holding_days = calculate_holding_days(str(pos['entry_date']))

        if pos['market'] == 'US':
            pnl_native = (live_price - entry_price) * pos['shares']
        else:
            pnl_native = (live_price - entry_price) * pos['shares']

        new_stop_native, stop_reason, atr_mult = calculate_trailing_stop(
            current_price=live_price,
            atr=atr_value,
            is_profitable=(pnl_native > 0),
            current_stop=current_stop_native,
            entry_price=entry_price,
            settings=_SETTINGS,
        )

        update_position(position_id, {
            'current_stop': round(new_stop_native, 2),
            'current_price': round(live_price, 4),
            'atr': round(atr_value, 4),
            'holding_days': holding_days,
        })

        results.append({
            "ticker": pos['ticker'],
            "market": pos['market'],
            "status": "updated",
            "previous_stop": round(current_stop_native, 2),
            "new_stop": round(new_stop_native, 2),
            "stop_moved": new_stop_native > current_stop_native,
            "atr_mult": atr_mult,
            "reason": stop_reason,
        })

    updated = sum(1 for r in results if r['status'] == 'updated')
    skipped = sum(1 for r in results if r['status'] == 'skipped')
    return {
        "run_date": datetime.now().strftime('%Y-%m-%d'),
        "positions_processed": len(positions),
        "updated": updated,
        "skipped": skipped,
        "results": results,
    }


# ============================================================================
# NIGHTLY RISK-OFF EXIT ALERTS (ST-05 / BLG-FEAT-49)
# ============================================================================

def run_nightly_risk_off_alerts() -> Dict:
    """
    Nightly job: flag open positions with risk_off_exit alert based on market regime.

    Logic:
      - If SPY < MA200: set risk_off_exit=True for all open US positions
      - If FTSE < MA200: set risk_off_exit=True for all open UK positions
      - Clear (risk_off_exit=False) when the relevant index recovers above MA200

    Market isolation: US risk-off does NOT affect UK positions and vice versa.
    """
    from database import update_positions_risk_off_exit

    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")

    portfolio_id = str(portfolio['id'])
    positions = get_positions(portfolio_id, status='open')
    market_regime = check_market_regime()

    spy_risk_on = market_regime.get('spy_risk_on', True)
    ftse_risk_on = market_regime.get('ftse_risk_on', True)

    us_risk_off = not spy_risk_on
    uk_risk_off = not ftse_risk_on

    flagged_us = 0
    cleared_us = 0
    flagged_uk = 0
    cleared_uk = 0

    for pos in positions:
        pos = decimal_to_float(pos)
        position_id = str(pos['id'])
        market = pos['market']

        if market == 'US':
            new_flag = us_risk_off
            if new_flag:
                flagged_us += 1
            else:
                cleared_us += 1
        else:
            new_flag = uk_risk_off
            if new_flag:
                flagged_uk += 1
            else:
                cleared_uk += 1

        update_positions_risk_off_exit(position_id, new_flag)

    return {
        "run_date": datetime.now().strftime('%Y-%m-%d'),
        "market_regime": {
            "spy_risk_on": spy_risk_on,
            "ftse_risk_on": ftse_risk_on,
        },
        "us_risk_off": us_risk_off,
        "uk_risk_off": uk_risk_off,
        "us_positions_flagged": flagged_us,
        "us_positions_cleared": cleared_us,
        "uk_positions_flagged": flagged_uk,
        "uk_positions_cleared": cleared_uk,
    }


# ============================================================================
# ADD POSITION
# ============================================================================

def add_position(
    ticker: str,
    market: str,
    entry_date: str,
    shares: float,
    entry_price: float,
    fx_rate: Optional[float] = None,
    atr_value: Optional[float] = None,
    stop_price: Optional[float] = None,
    entry_note: Optional[str] = None,
    tags: Optional[List[str]] = None,
    fill_price: Optional[float] = None,
    trade_plan_id: Optional[str] = None
) -> Dict:
    """
    Add a new position to the portfolio with automatic fee calculation
    
    Args:
        ticker: Stock symbol (e.g., "NVDA", "FRES")
        market: "US" or "UK"
        entry_date: Entry date (YYYY-MM-DD)
        shares: Number of shares (fractional supported)
        entry_price: Entry price in native currency
        fx_rate: Optional GBP/USD rate (auto-fetched if not provided for US)
        atr_value: Optional ATR value (auto-calculated if not provided)
        stop_price: Optional custom stop (auto-calculated if not provided)
    
    Returns:
        Dictionary with:
            - ticker: Display ticker
            - total_cost: Total cost in GBP
            - fees_paid: Fees paid in GBP
            - entry_price: Entry price in native currency
            - initial_stop: Initial stop level
            - remaining_cash: Cash balance after entry
            - position_id: UUID of created position
    
    Raises:
        ValueError: If portfolio not found, invalid market, or insufficient funds
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    
    print(f"\n📝 Adding new position: {ticker}")
    
    # Validate market
    if market not in ['US', 'UK']:
        raise ValueError("Market must be 'US' or 'UK'")
    
    # Auto-detect market from ticker if needed
    if ticker.endswith('.L') and market == 'US':
        market = 'UK'
        print(f"   Auto-detected UK market from .L suffix")
    
    # Add .L suffix for UK stocks if missing
    if market == 'UK' and not ticker.endswith('.L'):
        ticker = f"{ticker}.L"
        print(f"   Added .L suffix: {ticker}")
    
    # Get settings for fees
    settings_list = get_settings()
    settings = settings_list[0] if settings_list else None
    
    # Calculate entry details
    entry_price_native = entry_price
    
    # Get or validate FX rate for US stocks
    if market == 'US':
        if fx_rate and fx_rate > 0:
            fx_rate_to_use = fx_rate
            print(f"   Using provided FX rate: {fx_rate_to_use:.4f}")
        else:
            fx_rate_to_use = get_live_fx_rate()
            print(f"   Using live FX rate: {fx_rate_to_use:.4f}")
    else:
        fx_rate_to_use = 1.0
    
    # Calculate gross cost in native currency
    gross_cost_native = entry_price_native * shares
    
    # Calculate fees
    if market == 'UK':
        fee_breakdown = calculate_uk_entry_fees(gross_cost_native, settings or {})
        fee_type = 'stamp_duty'
        print(f"   UK fees: £{fee_breakdown['commission']:.2f} commission + £{fee_breakdown['stamp_duty']:.2f} stamp duty = £{fee_breakdown['total']:.2f}")
    else:
        fee_breakdown = calculate_us_entry_fees(gross_cost_native, settings or {})
        fee_type = 'fx_fee'
        print(f"   US fees: ${fee_breakdown['fx_fee']:.2f} FX fee")
    
    total_fees_native = fee_breakdown['total']
    
    # Total cost in native currency
    total_cost_native = gross_cost_native + total_fees_native
    
    # Convert to GBP for portfolio tracking
    if market == 'US':
        entry_price_gbp = entry_price_native / fx_rate_to_use
        total_cost_gbp = total_cost_native / fx_rate_to_use
        fees_paid_gbp = total_fees_native / fx_rate_to_use
        print(f"   💱 Total cost: ${total_cost_native:.2f} / {fx_rate_to_use:.4f} = £{total_cost_gbp:.2f}")
    else:
        entry_price_gbp = entry_price_native
        total_cost_gbp = total_cost_native
        fees_paid_gbp = total_fees_native
    
    # Check if enough cash
    current_cash = float(portfolio['cash'])
    if total_cost_gbp > current_cash:
        raise ValueError(
            f"Insufficient funds. Need £{total_cost_gbp:.2f}, have £{current_cash:.2f}"
        )
    
    # Get or calculate ATR
    if not atr_value or atr_value == 0:
        print(f"   Calculating ATR for {ticker}...")
        atr_value = calculate_atr(ticker)
        if not atr_value:
            # Use default 2% of entry price if can't calculate
            atr_value = entry_price_native * 0.02
            print(f"   ⚠️  Using default ATR (2% of entry): {atr_value:.2f}")
    
    # Calculate initial stop
    initial_stop_native = calculate_initial_stop(entry_price_native, atr_value, multiplier=5.0)
    
    print(f"   Entry price: {entry_price_native:.2f}")
    print(f"   ATR: {atr_value:.2f}")
    print(f"   Initial stop: {initial_stop_native:.2f}")
    
    # Create position record
    position_data = {
        'ticker': ticker,
        'market': market,
        'entry_date': entry_date,
        'entry_price': entry_price_gbp,
        'fill_price': entry_price_native,
        'fill_currency': 'USD' if market == 'US' else 'GBP',
        'fx_rate': fx_rate_to_use,
        'shares': shares,
        'total_cost': total_cost_gbp,
        'fees_paid': fees_paid_gbp,
        'fee_type': fee_type,
        'initial_stop': initial_stop_native,
        'current_stop': initial_stop_native,
        'current_price': entry_price_native,
        'atr': atr_value,
        'holding_days': 0,
        'pnl': 0,
        'pnl_pct': 0,
        'status': 'open',
        'entry_note': entry_note,
        'tags': tags,
        'user_fill_price': fill_price,
        # ST-01 (EPIC-01, v8.0): stamp the active strategy version at entry,
        # forward-only — no backfill of existing rows.
        'strategy_version_at_entry': get_current_strategy_version(),
    }

    # Create position in database
    new_position = create_position(portfolio_id, position_data)

    # Update portfolio cash
    new_cash = current_cash - total_cost_gbp
    update_portfolio_cash(portfolio_id, new_cash)

    # BLG-BE-46: auto-link this new position to the most recent unlinked draft
    # trade plan for the same ticker/market, if one exists. The pre-trade
    # planning flow (TradePlan.js) and position-entry flow (TradeEntry.js) are
    # separate pages with no explicit hand-off between them, which left
    # trade_plans.position_id permanently NULL in production. Best-effort —
    # a lookup/link failure must not block position creation.
    #
    # ST-01 (EPIC-01, v7.3): when the caller passes an explicit trade_plan_id
    # (the "Start Trade from Plan" action), link that exact plan instead of the
    # ticker/market best-effort match — deterministic, no reliance on there
    # being exactly one unlinked plan per ticker.
    #
    # ST-03 (BLG-BE-91, EPIC-02, v8.6): trade-plan linkage is the enforced
    # DEFAULT path, not silently optional -- track and surface the outcome
    # (trade_plan_linked / trade_plan_id) in the response instead of only a
    # server-side print(), so the entry flow (and any test/staging check) can
    # observe when a position was created with no trade plan behind it, per
    # trade_plan.md §10's "Start Trade from Plan" default-path intent.
    trade_plan_linked = False
    linked_trade_plan_id = None
    try:
        plan_to_link = (
            get_trade_plan_by_id(trade_plan_id, portfolio_id)
            if trade_plan_id
            else get_unlinked_trade_plan_for_entry(portfolio_id, ticker, market)
        )
        if plan_to_link and not plan_to_link.get("position_id"):
            update_trade_plan(str(plan_to_link["id"]), portfolio_id, {
                "position_id": str(new_position["id"]),
                "status": "active",
            })
            trade_plan_linked = True
            linked_trade_plan_id = str(plan_to_link["id"])
            print(f"   ✓ Linked trade plan {plan_to_link['id']} to new position")
        elif not plan_to_link:
            print(f"   ⚠️  No trade plan linked — position created without a pre-trade plan")
    except Exception as e:
        print(f"   ⚠️  Trade plan auto-link skipped: {e}")

    print(f"   ✓ Position created")
    print(f"   Cash: £{current_cash:.2f} → £{new_cash:.2f}\n")

    # Return response
    display_ticker = ticker.replace('.L', '') if market == 'UK' else ticker

    return {
        "ticker": display_ticker,
        "total_cost": round(total_cost_gbp, 2),
        "fees_paid": round(fees_paid_gbp, 2),
        "entry_price": round(entry_price_native, 2),
        "trade_plan_linked": trade_plan_linked,
        "trade_plan_id": linked_trade_plan_id,
        "initial_stop": round(initial_stop_native, 2),
        "remaining_cash": round(new_cash, 2),
        "position_id": str(new_position['id']),
        # ST-03 (EPIC-01, v8.0): §4.1.5 requires the FX rate used be returned
        # for auditability — was already persisted to positions.fx_rate but
        # never surfaced in this response.
        "fx_rate_used": round(fx_rate_to_use, 4),
    }


# ============================================================================
# EXIT POSITION
# ============================================================================

def exit_position(
    position_id: str,
    exit_price: float,
    shares: Optional[float] = None,
    exit_date: Optional[str] = None,
    exit_reason: Optional[str] = None,
    exit_fx_rate: Optional[float] = None,
    exit_note: Optional[str] = None
) -> Dict:
    """
    Exit a position (full or partial) and record in trade history
    
    Args:
        position_id: UUID of position to exit
        exit_price: Exit price in native currency (REQUIRED - from broker)
        shares: Number of shares to exit (None = all shares)
        exit_date: Exit date YYYY-MM-DD (None = today)
        exit_reason: Reason for exit (default "Manual Exit")
        exit_fx_rate: GBP/USD rate from broker (REQUIRED for US stocks)
    
    Returns:
        Dictionary with:
            - ticker: Stock symbol
            - market: US or UK
            - exit_price: Exit price in native currency
            - shares: Shares exited
            - gross_proceeds: Gross proceeds in GBP
            - exit_fees: Total fees in GBP
            - fee_breakdown: Commission, stamp duty, FX fee
            - net_proceeds: Net proceeds in GBP
            - realized_pnl: Realized P&L in GBP
            - realized_pnl_pct: Realized P&L percentage
            - new_cash_balance: Portfolio cash after exit
            - exit_fx_rate: FX rate used
            - exit_date: Exit date used
            - is_partial_exit: True if shares remain
            - remaining_shares: Shares remaining (0 if full exit)
    
    Raises:
        ValueError: If position not found, already closed, invalid shares,
                   or missing FX rate for US stocks
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    
    # Get the position
    positions = get_positions(portfolio_id)
    position = None
    for pos in positions:
        if str(pos['id']) == position_id:
            position = pos
            break
    
    if not position:
        raise ValueError("Position not found")
    
    if position['status'] == 'closed':
        raise ValueError("Position already closed")
    
    # Validate exit price
    if exit_price <= 0:
        raise ValueError("Exit price must be greater than 0")
    
    # Validate shares
    total_shares = float(position['shares'])
    exit_shares = float(shares) if shares else total_shares
    
    if exit_shares <= 0:
        raise ValueError("Shares to exit must be greater than 0")
    
    if exit_shares > total_shares:
        raise ValueError(
            f"Insufficient shares. Position has {total_shares} shares, exit requested {exit_shares}"
        )
    
    # Validate FX rate for US stocks
    if position['market'] == 'US':
        if exit_fx_rate and exit_fx_rate > 0:
            fx_rate_to_use = exit_fx_rate
            print(f"✓ Exit FX rate: {fx_rate_to_use:.4f} (user-provided from broker)")
        else:
            raise ValueError(
                "FX rate is required for US stock exits. Please provide the GBP/USD rate from your broker statement."
            )
    else:
        fx_rate_to_use = 1.0
    
    print(f"\n📤 Exiting position: {position['ticker']}")
    print(f"   Shares to exit: {exit_shares} of {total_shares}")
    print(f"   Exit price: {exit_price:.2f} (user-provided)")
    
    # Get settings
    settings_list = get_settings()
    settings = settings_list[0] if settings_list else None
    
    market = position['market']
    entry_price = position.get('fill_price', position['entry_price']) if market == 'US' else position['entry_price']
    
    # Calculate exit proceeds
    proceeds = calculate_exit_proceeds(
        exit_price=exit_price,
        shares=exit_shares,
        market=market,
        exit_fx_rate=fx_rate_to_use,
        settings=settings or {}
    )
    
    gross_proceeds_gbp = proceeds['gross_proceeds_gbp']
    exit_fees_gbp = proceeds['exit_fees_gbp']
    net_proceeds_gbp = proceeds['net_proceeds_gbp']
    fee_breakdown = proceeds['fee_breakdown']
    
    if market == 'UK':
        print(f"   UK exit fees: £{fee_breakdown['commission']:.2f} commission")
    else:
        print(f"   US exit fees: ${fee_breakdown['fx_fee']:.2f} FX fee")
        print(f"   💱 FX conversion: ${proceeds['net_proceeds_native']:.2f} / {fx_rate_to_use:.4f} = £{net_proceeds_gbp:.2f}")
    
    # Calculate realized P&L
    total_cost = float(position['total_cost'])
    realized_pnl_gbp, realized_pnl_pct = calculate_realized_pnl(
        net_proceeds_gbp=net_proceeds_gbp,
        total_cost=total_cost,
        shares_exited=exit_shares,
        total_shares=total_shares
    )
    
    # Calculate proportional costs
    cost_per_share = total_cost / total_shares
    exit_total_cost = cost_per_share * exit_shares
    
    entry_fees = float(position.get('fees_paid', 0))
    entry_fees_per_share = entry_fees / total_shares
    exit_entry_fees = entry_fees_per_share * exit_shares
    
    # Calculate holding period
    exit_date_str = exit_date or datetime.now().strftime('%Y-%m-%d')
    holding_days = calculate_holding_days(
        entry_date=str(position['entry_date']),
        exit_date=exit_date_str
    )
    
    if exit_date:
        print(f"   📅 Exit date: {exit_date_str} (user-provided)")
    else:
        print(f"   📅 Exit date: {exit_date_str} (today)")
    
    print(f"   Gross proceeds: £{gross_proceeds_gbp:.2f}")
    print(f"   Exit fees: £{exit_fees_gbp:.2f}")
    print(f"   Net proceeds: £{net_proceeds_gbp:.2f}")
    print(f"   Cost of exited shares: £{exit_total_cost:.2f}")
    print(f"   Realized P&L: £{realized_pnl_gbp:+.2f} ({realized_pnl_pct:+.2f}%)")
    
    # Get exit reason
    reason = exit_reason if exit_reason else 'Manual Exit'

    # Snapshot planned_entry_price from linked signal when a trade plan exists (Arc 4 PO-01).
    planned_entry_price = None
    try:
        ensure_planned_entry_price_column()
        plans = get_trade_plans_by_position(position_id, portfolio_id)
        if plans:
            signals = get_signals(portfolio_id)
            ticker_upper = position['ticker'].upper()
            signal = next(
                (s for s in signals if (s.get('ticker') or '').upper() == ticker_upper),
                None,
            )
            if signal:
                planned_entry_price = float(signal['current_price']) if signal.get('current_price') else None
    except Exception:
        pass  # best-effort; null is acceptable for pre-arc4 trades

    # Create trade history record
    trade_data = {
        'position_id': position_id,  # BLG-TECH-07: FK enables stop_price JOIN for R-multiple
        'ticker': position['ticker'],
        'market': market,
        'entry_date': position['entry_date'],
        'exit_date': exit_date_str,
        'shares': exit_shares,
        'entry_price': entry_price,
        'exit_price': exit_price,
        'total_cost': exit_total_cost,
        'gross_proceeds': gross_proceeds_gbp,
        'net_proceeds': net_proceeds_gbp,
        'entry_fees': exit_entry_fees,
        'exit_fees': exit_fees_gbp,
        'pnl': realized_pnl_gbp,
        'pnl_pct': realized_pnl_pct,
        'holding_days': holding_days,
        'exit_reason': reason,
        'entry_fx_rate': float(position.get('fx_rate', 1.0)),
        'exit_fx_rate': fx_rate_to_use,
        'entry_note': position.get('entry_note'),
        'exit_note': exit_note,
        'tags': position.get('tags'),
        'fill_price': position.get('user_fill_price'),
        'planned_entry_price': planned_entry_price,
    }
    
    print(f"   💾 Creating trade history record...")
    create_trade_history(portfolio_id, trade_data)
    print(f"   ✓ Trade history created")
    
    # Determine if partial or full exit
    is_partial_exit = exit_shares < total_shares
    
    if is_partial_exit:
        # Partial exit - update position to reduce shares
        remaining_shares = total_shares - exit_shares
        remaining_cost = total_cost - exit_total_cost
        
        print(f"   📝 Partial exit: {remaining_shares} shares remaining")
        
        update_position(position_id, {
            'shares': remaining_shares,
            'total_cost': remaining_cost,
            'fees_paid': entry_fees - exit_entry_fees
        })
        
        print(f"   ✓ Position updated: {remaining_shares} shares remaining")
    else:
        # Full exit - close the position
        print(f"   💾 Full exit: closing position...")
        
        try:
            update_position(position_id, {
                'status': 'closed',
                'exit_date': exit_date_str,
                'exit_price': exit_price,
                'exit_reason': reason
            })
        except Exception as e:
            if 'exit_date' in str(e) or 'UndefinedColumn' in str(e):
                print(f"   ⚠️  Exit columns don't exist, updating status only")
                update_position(position_id, {
                    'status': 'closed'
                })
            else:
                raise
        
        print(f"   ✓ Position closed")
    
    # Update portfolio cash
    current_cash = float(portfolio['cash'])
    new_cash = current_cash + net_proceeds_gbp
    update_portfolio_cash(portfolio_id, new_cash)
    
    print(f"   ✓ Cash updated: £{current_cash:.2f} → £{new_cash:.2f}\n")
    
    return {
        "ticker": position['ticker'],
        "market": market,
        "exit_price": round(exit_price, 2),
        "shares": exit_shares,
        "gross_proceeds": round(gross_proceeds_gbp, 2),
        "exit_fees": round(exit_fees_gbp, 2),
        "fee_breakdown": fee_breakdown,
        "net_proceeds": round(net_proceeds_gbp, 2),
        "realized_pnl": round(realized_pnl_gbp, 2),
        "realized_pnl_pct": round(realized_pnl_pct, 2),
        "new_cash_balance": round(new_cash, 2),
        "exit_fx_rate": fx_rate_to_use,
        "exit_date": exit_date_str,
        "is_partial_exit": is_partial_exit,
        "remaining_shares": round(total_shares - exit_shares, 4) if is_partial_exit else 0
    }

def update_note(position_id: str, entry_note: str) -> Dict:
    """
    Update entry note for a position.
    
    Args:
        position_id: UUID of position
        entry_note: Note text (can be empty to clear)
    
    Returns:
        Updated position with note
    """
    if not position_id:
        raise ValueError("Position ID is required")
    
    # Validate position exists
    position = get_position(position_id)
    if not position:
        raise ValueError(f"Position {position_id} not found")
    
    # Update note in database
    before_note = position.get('entry_note')
    result = update_position_note(position_id, entry_note)

    # Audit trail (ST-06, EPIC-06, v7.9, BLG-BE-73) — manual override outside
    # the automated trade lifecycle.
    create_position_audit_log_entry(position_id, "note", "entry_note", before_note, entry_note)

    return result


def mark_position_reviewed(position_id: str) -> Dict:
    """
    Set last_reviewed_at = NOW() for the given position (ST-15, BLG-FEAT-68, v7.0).

    Portfolio-ownership check (ST-04, BLG-BE-61, v7.1): routes through
    get_position() first, matching update_note()/update_tags() above — the
    prior direct database.mark_position_reviewed(position_id) call had no
    ownership check at all (raw UPDATE ... WHERE id = %s, no portfolio_id
    filter), unlike every other position-mutating endpoint in this file.

    Args:
        position_id: UUID of position

    Returns:
        Updated position dict with id and last_reviewed_at
    """
    if not position_id:
        raise ValueError("Position ID is required")

    # Validate position exists and belongs to the active portfolio
    position = get_position(position_id)
    if not position:
        raise ValueError(f"Position {position_id} not found")

    before_reviewed_at = position.get('last_reviewed_at')
    result = db_mark_position_reviewed(position_id)
    if result is None:
        raise ValueError(f"Position {position_id} not found")

    # Audit trail (ST-06, EPIC-06, v7.9, BLG-BE-73) — manual override outside
    # the automated trade lifecycle.
    create_position_audit_log_entry(
        position_id, "mark-reviewed", "last_reviewed_at",
        before_reviewed_at, result.get('last_reviewed_at'),
    )

    return result


def update_tags(position_id: str, tags: List[str]) -> Dict:
    """
    Update tags for a position.
    
    Args:
        position_id: UUID of position
        tags: List of tag strings (e.g., ["momentum", "breakout"])
    
    Returns:
        Updated position with tags
    """
    if not position_id:
        raise ValueError("Position ID is required")
    
    # Validate position exists
    position = get_position(position_id)
    if not position:
        raise ValueError(f"Position {position_id} not found")
    
    # Validate tags (lowercase, no special chars except hyphen)
    validated_tags = []
    for tag in tags:
        clean_tag = tag.strip().lower()
        if clean_tag and re.match(r'^[a-z0-9-]+$', clean_tag):
            validated_tags.append(clean_tag)
    
    # Update tags in database
    before_tags = position.get('tags')
    result = update_position_tags(position_id, validated_tags)

    # Audit trail (ST-06, EPIC-06, v7.9, BLG-BE-73) — manual override outside
    # the automated trade lifecycle.
    create_position_audit_log_entry(position_id, "tags", "tags", before_tags, validated_tags)

    return result


def get_available_tags(portfolio_id: str) -> List[str]:
    """Get all unique tags used in portfolio"""
    return get_all_tags(portfolio_id)


def filter_by_tags(portfolio_id: str, tags: List[str]) -> List[Dict]:
    """Search positions by tags"""
    if not tags:
        raise ValueError("At least one tag is required")
    
    return search_positions_by_tags(portfolio_id, tags)

def get_position(position_id: str) -> Optional[Dict]:
    """Get a single position by ID"""
    portfolio = get_portfolio()
    if not portfolio:
        return None
    
    portfolio_id = str(portfolio['id'])
    positions = get_positions(portfolio_id)
    
    for pos in positions:
        if str(pos['id']) == position_id:
            return decimal_to_float(pos)
    
    return None
