from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
from decimal import Decimal
from datetime import timedelta
import time
import requests
from config import API_TITLE
from config import ALLOWED_ORIGINS
from utils.calculations import calculate_initial_stop

from database import (
    get_portfolio,
    update_portfolio_cash,
    get_positions,
    create_position,
    update_position,
    delete_position,
    get_trade_history,
    create_trade_history,
    get_settings,
    create_settings,
    update_settings,
    create_portfolio_snapshot,
    get_portfolio_snapshots,
    create_cash_transaction,
    get_cash_transactions,
    get_total_deposits_withdrawals,
    create_signal,
    get_signals,
    update_signal,
    delete_signal,
    get_all_tickers,
    download_ticker_data,
    compute_atr_simple
)

from utils.pricing import (
    get_current_price,
    get_live_fx_rate,
    check_market_regime,
    calculate_atr
)

from models import (
         AddPositionRequest,
         SettingsRequest,
         CashTransactionRequest,
         ExitPositionRequest
     )

from utils.formatting import decimal_to_float
from config import (
    API_TITLE,
    ALLOWED_ORIGINS,
    DEFAULT_FX_RATE
)

from utils.calculations import (
    # Fee calculations
    calculate_uk_entry_fees,
    calculate_us_entry_fees,
    calculate_uk_exit_fees,
    calculate_us_exit_fees,
    # P&L calculations
    calculate_position_pnl,
    calculate_exit_proceeds,
    calculate_realized_pnl,
    # Stop loss calculations
    calculate_trailing_stop,
    should_exit_position,
    calculate_holding_days
)

app = FastAPI(title=API_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
      
@app.get("/")
def root():
    return {"status": "ok", "message": "Trading Assistant API v1.0"}


@app.get("/settings")
def get_settings_endpoint():
    """Get user settings"""
    try:
        settings = get_settings()
        if not settings:
            # Return default settings if none exist
            return {
                "status": "ok",
                "data": []
            }
        
        settings_list = [decimal_to_float(s) for s in settings]
        return {
            "status": "ok",
            "data": settings_list
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/settings")
def create_settings_endpoint(request: SettingsRequest):
    """Create new settings"""
    try:
        settings_data = request.dict()
        new_settings = create_settings(settings_data)
        return {
            "status": "ok",
            "data": decimal_to_float(new_settings)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/settings/{settings_id}")
def update_settings_endpoint(settings_id: str, request: SettingsRequest):
    """Update existing settings"""
    try:
        settings_data = {k: v for k, v in request.dict().items() if v is not None}
        updated_settings = update_settings(settings_id, settings_data)
        return {
            "status": "ok",
            "data": decimal_to_float(updated_settings)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/positions")
def get_positions_endpoint():
    """Get open positions with live prices - always fetches fresh data"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        positions = get_positions(portfolio_id, status='open')
        
        if not positions:
            return []
        
        # Get live FX rate for conversions
        live_fx_rate = get_live_fx_rate()
        
        print(f"\n📊 /positions endpoint - fetching live prices for {len(positions)} position(s)")
        
        positions_list = []
        
        for pos in positions:
            pos = decimal_to_float(pos)
            
            # ALWAYS fetch live price - don't rely on analysis
            print(f"   Fetching {pos['ticker']}...")
            live_price = get_current_price(pos['ticker'])
            
            if live_price:
                # Fix UK stocks: Yahoo returns pence
                if pos['market'] == 'UK' and live_price > 1000:
                    live_price = live_price / 100
                current_price_native = live_price
                print(f"   ✓ Live: {current_price_native:.2f}")
            else:
                # Fallback to stored
                print(f"   ⚠️  Using stored price")
                current_price_native = pos.get('current_price', pos['entry_price'])
            
            # Calculate P&L using utility function
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
            
           # Calculate holding days using utility function
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
            
            # Display ticker without .L suffix
            display_ticker = pos['ticker'].replace('.L', '') if pos['market'] == 'UK' else pos['ticker']
            
            # Determine status
            if grace_period:
                display_status = "GRACE"
            elif pnl_gbp > 0:
                display_status = "PROFITABLE"
            else:
                display_status = "LOSING"
            
            # FIXED: Return total_cost field
            positions_list.append({
                "id": str(pos['id']),
                "ticker": display_ticker,
                "market": pos['market'],
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
                "stop_reason": f"Grace period ({holding_days}/10 days)" if grace_period else "Active",
                "atr_value": pos.get('atr', 0),
                "fx_rate": pos.get('fx_rate', 1.0),
                "live_fx_rate": live_fx_rate,
                "total_cost": round(pos.get('total_cost', 0), 2)  # FIXED: Added total_cost
            })
        
        print(f"✓ Returned {len(positions_list)} positions with live prices\n")
        
        return positions_list
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/portfolio")
def get_portfolio_endpoint():
    """Returns portfolio with live prices - current_price in GBP for Dashboard calculations"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        positions = get_positions(portfolio_id, status='open')
        
        if not positions:
            cash = float(portfolio['cash'])
            return {
                "status": "ok",
                "data": {
                    "cash": cash,
                    "cash_balance": cash,
                    "total_value": cash,
                    "open_positions_value": 0,
                    "total_pnl": 0,
                    "last_updated": str(portfolio['last_updated']),
                    "live_fx_rate": 1.27,
                    "positions": []
                }
            }
        
        # Get live FX rate
        live_fx_rate = get_live_fx_rate()
        print(f"\n📊 /portfolio endpoint - fetching live prices for Dashboard")
        
        positions_list = []
        total_positions_value_gbp = 0
        
        for pos in positions:
            pos = decimal_to_float(pos)
            
            # FETCH LIVE PRICE - don't use stale database value
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
                # Fallback to stored price if live fetch fails
                print(f"   ⚠️  Using stored price for {pos['ticker']}")
                # Check if stored price is already converted (< 500 suggests GBP for US stock)
                stored_price = pos.get('current_price', pos['entry_price'])
                if pos['market'] == 'US' and stored_price < 500:
                    # This looks like it's already in GBP, convert back to USD estimate
                    current_price_native = stored_price * 1.38  # Rough estimate
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
                "current_price": round(current_price_gbp, 2),  # GBP for Dashboard
                "current_value": round(current_value_gbp, 2),
                "pnl": round(pnl_gbp, 2),
                "pnl_pct": round(pnl_pct, 2),
                "current_stop": round(pos.get('current_stop', 0), 2),
                "holding_days": holding_days,
                "status": display_status,
                "fx_rate": stored_fx_rate,
                "live_fx_rate": live_fx_rate
            })
        
        cash = float(portfolio['cash'])
        total_value = cash + total_positions_value_gbp
        
        # Calculate TRUE portfolio P&L accounting for deposits/withdrawals
        # P&L = Current Value - Initial Investment
        # Initial Investment = Net Deposits/Withdrawals
        
        # Get cash transaction summary
        cash_summary = get_total_deposits_withdrawals(portfolio_id)
        net_cash_flow = cash_summary['net_cash_flow']  # deposits - withdrawals
        
        # Calculate total cost of all positions (what we paid including fees)
        total_cost_of_positions = sum(float(pos.get('total_cost', 0)) for pos in positions)
        
        # Initial portfolio value = net deposits/withdrawals
        # This is the money you put in (minus what you took out)
        initial_portfolio_value = net_cash_flow
        
        # True P&L = Current Value - Initial Investment
        # Current value = cash + positions
        # Initial investment = net cash flow (deposits - withdrawals)
        true_total_pnl = total_value - initial_portfolio_value
        
        print(f"\n✓ Portfolio calculated:")
        print(f"   Total positions value: £{total_positions_value_gbp:.2f}")
        print(f"   Total cost of positions: £{total_cost_of_positions:.2f}")
        print(f"   Cash: £{cash:.2f}")
        print(f"   Total value: £{total_value:.2f}")
        print(f"   Net cash flow (deposits-withdrawals): £{net_cash_flow:.2f}")
        print(f"   Initial portfolio value: £{initial_portfolio_value:.2f}")
        print(f"   True total P&L: £{true_total_pnl:+.2f}\n")
        
        return {
            "status": "ok",
            "data": {
                "cash": cash,
                "cash_balance": cash,
                "total_value": total_value,
                "open_positions_value": total_positions_value_gbp,
                "total_pnl": true_total_pnl,  # TRUE portfolio P&L
                "initial_value": initial_portfolio_value,  # For reference
                "net_deposits": net_cash_flow,  # Total deposits - withdrawals
                "last_updated": str(portfolio['last_updated']),
                "live_fx_rate": live_fx_rate,
                "positions": positions_list
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.post("/positions/{position_id}/exit")
def exit_position_endpoint(position_id: str, request: ExitPositionRequest):
    """Exit a position (full or partial) and record in trade history
    
    v1.2 Updates:
    - Accepts user-provided exit price (REQUIRED)
    - Supports partial exits via shares parameter
    - Accepts custom exit date for backdating
    - Requires FX rate for US stocks (from broker statement)
    - Returns detailed fee breakdown
    """
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        
        # Get the position
        positions = get_positions(portfolio_id)
        position = None
        for pos in positions:
            if str(pos['id']) == position_id:
                position = pos
                break
        
        if not position:
            raise HTTPException(status_code=404, detail="Position not found")
        
        if position['status'] == 'closed':
            raise HTTPException(status_code=400, detail="Position already closed")
        
        # Validate exit price
        if request.exit_price <= 0:
            raise HTTPException(status_code=400, detail="Exit price must be greater than 0")
        
        # Validate shares for partial exit
        total_shares = float(position['shares'])
        exit_shares = float(request.shares) if request.shares else total_shares
        
        if exit_shares <= 0:
            raise HTTPException(status_code=400, detail="Shares to exit must be greater than 0")
        
        if exit_shares > total_shares:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient shares. Position has {total_shares} shares, exit requested {exit_shares}"
            )
        
        # FIXED: Use user-provided FX rate for US stocks
        if position['market'] == 'US':
            if request.exit_fx_rate and request.exit_fx_rate > 0:
                exit_fx_rate = request.exit_fx_rate
                print(f"✓ Exit FX rate: {exit_fx_rate:.4f} (user-provided from broker)")
            else:
                raise HTTPException(
                    status_code=400,
                    detail="FX rate is required for US stock exits. Please provide the GBP/USD rate from your broker statement."
                )
        else:
            exit_fx_rate = 1.0
        
        print(f"\n📤 Exiting position: {position['ticker']}")
        print(f"   Shares to exit: {exit_shares} of {total_shares}")
        print(f"   Exit price: {request.exit_price:.2f} (user-provided)")
        
        # Get settings for commission rates
        settings_list = get_settings()
        settings = settings_list[0] if settings_list else None
        
        uk_commission = float(settings.get('uk_commission', 9.95)) if settings else 9.95
        us_commission = float(settings.get('us_commission', 0.00)) if settings else 0.00
        fx_fee_rate = float(settings.get('fx_fee_rate', 0.0015)) if settings else 0.0015
        
        exit_price_native = request.exit_price
        market = position['market']
        
        # Calculate exit proceeds in native currency
        gross_proceeds_native = exit_price_native * exit_shares
        
        # Calculate exit proceeds using utility function
proceeds = calculate_exit_proceeds(
    exit_price=exit_price_native,
    shares=exit_shares,
    market=market,
    exit_fx_rate=exit_fx_rate,
    settings=settings or {}
)

gross_proceeds_native = proceeds['gross_proceeds_native']
gross_proceeds_gbp = proceeds['gross_proceeds_gbp']
exit_fees_native = proceeds['exit_fees_native']
exit_fees_gbp = proceeds['exit_fees_gbp']
net_proceeds_native = proceeds['net_proceeds_native']
net_proceeds_gbp = proceeds['net_proceeds_gbp']
fee_breakdown = proceeds['fee_breakdown']

commission = fee_breakdown['commission']
stamp_duty = fee_breakdown['stamp_duty']
fx_fee = fee_breakdown['fx_fee']

if market == 'UK':
    print(f"   UK exit fees: £{commission:.2f} commission")
else:
    print(f"   US exit fees: ${fx_fee:.2f} ({float(settings.get('fx_fee_rate', 0.0015))*100:.2f}% FX fee)")
    print(f"   💱 FX conversion: ${net_proceeds_native:.2f} / {exit_fx_rate:.4f} = £{net_proceeds_gbp:.2f}")
        
        # Calculate realized P&L using utility function
total_cost = float(position['total_cost'])
realized_pnl_gbp, realized_pnl_pct = calculate_realized_pnl(
    net_proceeds_gbp=net_proceeds_gbp,
    total_cost=total_cost,
    shares_exited=exit_shares,
    total_shares=total_shares
)

# Calculate proportional costs for partial exit tracking
cost_per_share = total_cost / total_shares
exit_total_cost = cost_per_share * exit_shares

entry_fees = float(position.get('fees_paid', 0))
entry_fees_per_share = entry_fees / total_shares
exit_entry_fees = entry_fees_per_share * exit_shares
        
        # Calculate holding period using utility function
exit_date_str = request.exit_date or datetime.now().strftime('%Y-%m-%d')
holding_days = calculate_holding_days(
    entry_date=str(position['entry_date']),
    exit_date=exit_date_str
)

if request.exit_date:
    print(f"   📅 Exit date: {exit_date_str} (user-provided)")
else:
    print(f"   📅 Exit date: {exit_date_str} (today)")
        
        print(f"   Shares: {exit_shares}")
        print(f"   Gross proceeds: £{gross_proceeds_gbp:.2f}")
        print(f"   Exit fees: £{exit_fees_gbp:.2f}")
        print(f"   Net proceeds: £{net_proceeds_gbp:.2f}")
        print(f"   Cost of exited shares: £{exit_total_cost:.2f}")
        print(f"   Realized P&L: £{realized_pnl_gbp:+.2f} ({realized_pnl_pct:+.2f}%)")
        
        # FIXED: Get exit reason from request
        exit_reason = request.exit_reason if request.exit_reason else 'Manual Exit'
        
        # Create trade history record with CORRECT FX rate and date
        trade_data = {
            'ticker': position['ticker'],
            'market': market,
            'entry_date': position['entry_date'],
            'exit_date': exit_date_str,  # FIXED: User-provided date
            'shares': exit_shares,
            'entry_price': entry_price,
            'exit_price': exit_price_native,
            'total_cost': exit_total_cost,
            'gross_proceeds': gross_proceeds_gbp,
            'net_proceeds': net_proceeds_gbp,
            'entry_fees': exit_entry_fees,
            'exit_fees': exit_fees_gbp,
            'pnl': realized_pnl_gbp,
            'pnl_pct': realized_pnl_pct,
            'holding_days': holding_days,
            'exit_reason': exit_reason,  # FIXED: From request
            'entry_fx_rate': float(position.get('fx_rate', 1.0)),
            'exit_fx_rate': exit_fx_rate  # FIXED: User-provided rate
        }
        
        print(f"   💾 Creating trade history record...")
        print(f"      Exit FX rate for history: {exit_fx_rate:.4f}")
        print(f"      Exit date for history: {exit_date_str}")
        print(f"      Exit reason: {exit_reason}")
        
        create_trade_history(portfolio_id, trade_data)
        print(f"   ✓ Trade history created")
        
        # Determine if this is a partial or full exit
        is_partial_exit = exit_shares < total_shares
        
        if is_partial_exit:
            # Partial exit - update position to reduce shares
            remaining_shares = total_shares - exit_shares
            remaining_cost = total_cost - exit_total_cost
            
            print(f"   📝 Partial exit: {remaining_shares} shares remaining")
            
            updated_position = update_position(position_id, {
                'shares': remaining_shares,
                'total_cost': remaining_cost,
                'fees_paid': entry_fees - exit_entry_fees
            })
            
            print(f"   ✓ Position updated: {remaining_shares} shares remaining")
        else:
            # Full exit - close the position
            print(f"   💾 Full exit: closing position...")
            
            try:
                updated_position = update_position(position_id, {
                    'status': 'closed',
                    'exit_date': exit_date_str,
                    'exit_price': exit_price_native,
                    'exit_reason': exit_reason
                })
            except Exception as e:
                if 'exit_date' in str(e) or 'UndefinedColumn' in str(e):
                    print(f"   ⚠️  Exit columns don't exist, updating status only")
                    updated_position = update_position(position_id, {
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
            "status": "ok",
            "data": {
                "ticker": position['ticker'],
                "market": market,
                "exit_price": round(exit_price_native, 2),
                "shares": exit_shares,
                "gross_proceeds": round(gross_proceeds_gbp, 2),
                "exit_fees": round(exit_fees_gbp, 2),
                "fee_breakdown": fee_breakdown,
                "net_proceeds": round(net_proceeds_gbp, 2),
                "realized_pnl": round(realized_pnl_gbp, 2),
                "realized_pnl_pct": round(realized_pnl_pct, 2),
                "new_cash_balance": round(new_cash, 2),
                "exit_fx_rate": exit_fx_rate,  # Return the FX rate used
                "exit_date": exit_date_str,    # Return the date used
                "is_partial_exit": is_partial_exit,
                "remaining_shares": round(total_shares - exit_shares, 4) if is_partial_exit else 0
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/portfolio/position")
def add_position_endpoint(request: AddPositionRequest):
    """Add a new position to the portfolio"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        
        print(f"\n📝 Adding new position: {request.ticker}")
        
        # Validate market
        if request.market not in ['US', 'UK']:
            raise HTTPException(status_code=400, detail="Market must be 'US' or 'UK'")
        
        # Auto-detect market from ticker if not provided correctly
        if request.ticker.endswith('.L') and request.market == 'US':
            request.market = 'UK'
            print(f"   Auto-detected UK market from .L suffix")
        
        # Add .L suffix for UK stocks if missing
        ticker = request.ticker
        if request.market == 'UK' and not ticker.endswith('.L'):
            ticker = f"{ticker}.L"
            print(f"   Added .L suffix: {ticker}")
        
        # Get settings for fees
        settings_list = get_settings()
        settings = settings_list[0] if settings_list else None
        
        uk_commission = float(settings.get('uk_commission', 9.95)) if settings else 9.95
        us_commission = float(settings.get('us_commission', 0.00)) if settings else 0.00
        stamp_duty_rate = float(settings.get('stamp_duty_rate', 0.005)) if settings else 0.005
        fx_fee_rate = float(settings.get('fx_fee_rate', 0.0015)) if settings else 0.0015
        
        # Calculate entry details
        shares = request.shares
        entry_price_native = request.entry_price  # In native currency (USD or GBP)
        
        # Get or validate FX rate for US stocks
        if request.market == 'US':
            if request.fx_rate and request.fx_rate > 0:
                fx_rate = request.fx_rate
                print(f"   Using provided FX rate: {fx_rate:.4f}")
            else:
                # Fetch live FX rate if not provided
                fx_rate = get_live_fx_rate()
                print(f"   Using live FX rate: {fx_rate:.4f}")
        else:
            fx_rate = 1.0
        
        # Calculate gross cost in native currency
        gross_cost_native = entry_price_native * shares
        
        # Calculate fees using utility function
if request.market == 'UK':
    fee_breakdown = calculate_uk_entry_fees(gross_cost_native, settings or {})
    fee_type = 'stamp_duty'
    print(f"   UK fees: £{fee_breakdown['commission']:.2f} commission + £{fee_breakdown['stamp_duty']:.2f} stamp duty = £{fee_breakdown['total']:.2f}")
else:
    fee_breakdown = calculate_us_entry_fees(gross_cost_native, settings or {})
    fee_type = 'fx_fee'
    print(f"   US fees: ${fee_breakdown['fx_fee']:.2f} FX fee")

total_fees_native = fee_breakdown['total']
commission = fee_breakdown['commission']
        
        # Total cost in native currency
        total_cost_native = gross_cost_native + total_fees_native
        
        # Convert to GBP for portfolio tracking
        if request.market == 'US':
            entry_price_gbp = entry_price_native / fx_rate
            total_cost_gbp = total_cost_native / fx_rate
            fees_paid_gbp = total_fees_native / fx_rate
            print(f"   💱 Total cost: ${total_cost_native:.2f} / {fx_rate:.4f} = £{total_cost_gbp:.2f}")
        else:
            entry_price_gbp = entry_price_native
            total_cost_gbp = total_cost_native
            fees_paid_gbp = total_fees_native
        
        # Check if enough cash
        current_cash = float(portfolio['cash'])
        if total_cost_gbp > current_cash:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient funds. Need £{total_cost_gbp:.2f}, have £{current_cash:.2f}"
            )
        
        # Get or calculate ATR
        atr_value = request.atr_value
        if not atr_value or atr_value == 0:
            print(f"   Calculating ATR for {ticker}...")
            atr_value = calculate_atr(ticker)
            if not atr_value:
                # Use default 2% of entry price if can't calculate
                atr_value = entry_price_native * 0.02
                print(f"   ⚠️  Using default ATR (2% of entry): {atr_value:.2f}")
        
        # Calculate initial stop using utility function

initial_stop_native = calculate_initial_stop(entry_price_native, atr_value, multiplier=5.0)
        
        print(f"   Entry price: {entry_price_native:.2f}")
        print(f"   ATR: {atr_value:.2f}")
        print(f"   Initial stop: {initial_stop_native:.2f}")
        
        # Create position record
        position_data = {
            'ticker': ticker,
            'market': request.market,
            'entry_date': request.entry_date,
            'entry_price': entry_price_gbp,  # GBP for portfolio
            'fill_price': entry_price_native,  # Native for display
            'fill_currency': 'USD' if request.market == 'US' else 'GBP',
            'fx_rate': fx_rate,
            'shares': shares,
            'total_cost': total_cost_gbp,
            'fees_paid': fees_paid_gbp,
            'fee_type': fee_type,
            'initial_stop': initial_stop_native,  # Native currency
            'current_stop': initial_stop_native,  # Native currency
            'current_price': entry_price_native,  # Native currency
            'atr': atr_value,
            'holding_days': 0,
            'pnl': 0,
            'pnl_pct': 0,
            'status': 'open'
        }
        
        # Create position in database
        new_position = create_position(portfolio_id, position_data)
        
        # Update portfolio cash
        new_cash = current_cash - total_cost_gbp
        update_portfolio_cash(portfolio_id, new_cash)
        
        print(f"   ✓ Position created")
        print(f"   Cash: £{current_cash:.2f} → £{new_cash:.2f}\n")
        
        # Return response
        display_ticker = ticker.replace('.L', '') if request.market == 'UK' else ticker
        
        return {
            "status": "ok",
            "data": {
                "ticker": display_ticker,
                "total_cost": round(total_cost_gbp, 2),
                "fees_paid": round(fees_paid_gbp, 2),
                "entry_price": round(entry_price_native, 2),
                "initial_stop": round(initial_stop_native, 2),
                "remaining_cash": round(new_cash, 2),
                "position_id": str(new_position['id'])
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/positions/analyze")
def analyze_positions_endpoint():
    """Run daily position analysis with live prices and market regime using LIVE FX rate"""
    try:
        print("\n" + "="*70)
        print("🔍 STARTING POSITION ANALYSIS")
        print("="*70)
        
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        positions = get_positions(portfolio_id, status='open')
        
        if not positions:
            print("✓ No open positions to analyze")
            return {
                "status": "ok",
                "data": {
                    "analysis_date": datetime.now().strftime('%Y-%m-%d'),
                    "summary": {
                        "total_value": 0,
                        "total_pnl": 0,
                        "exit_count": 0
                    },
                    "actions": []
                }
            }
        
        # Get live FX rate for current valuations
        live_fx_rate = get_live_fx_rate()
        
        # Get market regime
        print("\n📊 Checking market regime...")
        market_regime = check_market_regime()
        print(f"   SPY: {'🟢 Risk On' if market_regime['spy_risk_on'] else '🔴 Risk Off'}")
        print(f"   FTSE: {'🟢 Risk On' if market_regime['ftse_risk_on'] else '🔴 Risk Off'}")
        
        actions = []
        total_value_gbp = 0  # Track in GBP
        total_pnl_gbp = 0    # Track in GBP
        
        print(f"\n💼 Analyzing {len(positions)} position(s)...")
        
        for pos in positions:
            pos = decimal_to_float(pos)
            
            print(f"\n{'='*70}")
            print(f"📈 Analyzing: {pos['ticker']} ({pos['market']})")
            print(f"{'='*70}")
            
            # Get live price with detailed logging
            print(f"   🔍 Fetching live price from Yahoo Finance...")
            live_price = get_current_price(pos['ticker'])
            
            # For US stocks, use fill_price (USD). For UK stocks, use entry_price (GBP)
            entry_price = pos.get('fill_price', pos['entry_price']) if pos['market'] == 'US' else pos['entry_price']
            stored_fx_rate = pos.get('fx_rate', 1.27)  # FX rate at purchase time
            
            if live_price:
                # Fix UK stocks: Yahoo returns pence, convert to pounds
                if pos['market'] == 'UK' and live_price > 1000:
                    live_price = live_price / 100
                    print(f"   ✓ Converted from pence to pounds")
                
                print(f"   ✓ Live price: ${live_price:.2f}")
                print(f"   Entry price: ${entry_price:.2f}")
                print(f"   Change: {((live_price - entry_price) / entry_price * 100):+.2f}%")
                current_price = live_price
            else:
                print(f"   ⚠️  Failed to fetch live price")
                print(f"   Using stored price: ${pos.get('current_price', entry_price):.2f}")
                current_price = pos.get('current_price', entry_price)
            
            # Calculate metrics
            shares = pos['shares']
            
            # Calculate value in native currency then convert to GBP using LIVE FX rate
            current_value_native = current_price * shares
            if pos['market'] == 'US':
                current_value_gbp = current_value_native / live_fx_rate
                print(f"   💱 Converting USD to GBP (LIVE rate): ${current_value_native:.2f} / {live_fx_rate:.4f} = £{current_value_gbp:.2f}")
            else:
                current_value_gbp = current_value_native
            
            # Calculate P&L using utility function
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
            entry_date = datetime.strptime(str(pos['entry_date']), '%Y-%m-%d')
            holding_days = (datetime.now() - entry_date).days
            
            print(f"   Holdings: {shares} shares = £{current_value_gbp:.2f} (GBP)")
            print(f"   P&L: £{pnl_gbp:+.2f} ({pnl_pct:+.2f}%)")
            print(f"   Days held: {holding_days}")
            
            # Get current stop from database (stored in NATIVE currency)
            current_stop_native = pos.get('current_stop', pos.get('initial_stop', 0))
            
            # Check grace period
            grace_period = holding_days < 10
            
            # Calculate new trailing stop based on strategy (ALL IN NATIVE CURRENCY)
            if grace_period:
                # During grace period, keep initial stop but don't display it
                trailing_stop_native = current_stop_native
                display_stop_native = 0  # Show 0 to indicate no active stop during grace period
                stop_reason = f"Grace period ({holding_days}/10 days)"
                print(f"   🆕 Grace period active - no stop loss")
            else:
                # After grace period, calculate trailing stop
                # Get settings for ATR multipliers
                settings_list = get_settings()
                settings = settings_list[0] if settings_list else None
                
                if pnl_native > 0:
                    # Profitable: tight 2x ATR stop
                    atr_mult = float(settings.get('atr_multiplier_trailing', 2)) if settings else 2
                    stop_reason = f"Profitable (tight {atr_mult}x ATR)"
                else:
                    # At loss: wide 5x ATR stop
                    atr_mult = float(settings.get('atr_multiplier_initial', 5)) if settings else 5
                    stop_reason = f"At loss (wide {atr_mult}x ATR)"
                
                # Get ATR value (stored in position or calculate it)
                atr_value = pos.get('atr')
                
                if not atr_value or atr_value == 0:
                    print(f"   ⚠️  No ATR in database, calculating...")
                    atr_value = calculate_atr(pos['ticker'])
                    
                    # Store calculated ATR in database for future use
                    if atr_value and atr_value > 0:
                        update_position(str(pos['id']), {'atr': round(atr_value, 4)})
                        print(f"   💾 Stored calculated ATR: {atr_value:.2f}")
                
                if atr_value and atr_value > 0:
                    # Calculate new stop in NATIVE currency: current_price - (multiplier * ATR)
                    # Both current_price and atr_value are in native currency
                    new_stop_native = current_price - (atr_mult * atr_value)
                    
                    # Get entry price in native currency
                    entry_price_native = pos.get('fill_price', entry_price) if pos['market'] == 'US' else entry_price
                    
                    # Trailing stop logic depends on profitability:
                    # - Profitable (tight 2×ATR): Never go below entry (protect gains)
                    # - Losing (wide 5×ATR): Can go below entry (room to recover)
                    if pnl_native > 0:
                        # Profitable: enforce entry-level minimum
                        trailing_stop_native = max(current_stop_native, new_stop_native, entry_price_native)
                    else:
                        # Losing: allow wide stop below entry
                        trailing_stop_native = max(current_stop_native, new_stop_native)
                    
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
                    print(f"   ⚠️  No ATR value available, stop at entry level")
            
            # Determine action
            action = "HOLD"
            exit_reason = None
            
            if not grace_period:
                # Check market regime
                is_uk = pos['market'] == 'UK'
                market_risk_on = market_regime['ftse_risk_on'] if is_uk else market_regime['spy_risk_on']
                
                if not market_risk_on:
                    action = "EXIT"
                    exit_reason = "Risk-Off Signal"
                    stop_reason = "Market risk-off"
                    print(f"   🔴 EXIT: Market risk-off")
                elif current_price <= trailing_stop_native:
                    action = "EXIT"
                    exit_reason = "Stop Loss Hit"
                    stop_reason = "Stop triggered"
                    currency_symbol = "$" if pos['market'] == 'US' else "£"
                    print(f"   🔴 EXIT: Stop loss hit ({currency_symbol}{trailing_stop_native:.2f})")
                else:
                    print(f"   ✅ HOLD: {stop_reason}")
            
            # Update position in database with new prices AND stop (all in native currency)
            if live_price:
                print(f"   💾 Updating position in database...")
                
                # Store current price in native currency
                # (It's converted to GBP in /positions endpoint for portfolio aggregation)
                update_position(str(pos['id']), {
                    'current_price': round(current_price, 4),  # Native currency
                    'current_stop': round(trailing_stop_native, 2),  # Native currency
                    'holding_days': holding_days,
                    'pnl': round(pnl_gbp, 2),  # Store P&L in GBP for portfolio total
                    'pnl_pct': round(pnl_pct, 2)
                })
            
            actions.append({
                "ticker": pos['ticker'],
                "market": pos['market'],
                "action": action,
                "exit_reason": exit_reason,
                "entry_price": round(entry_price, 2),
                "current_price": round(current_price, 2),
                "shares": shares,
                "pnl": round(pnl_gbp, 2),  # P&L in GBP
                "pnl_pct": round(pnl_pct, 2),
                "current_stop": round(display_stop_native, 2),  # Use native currency stop
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
            "status": "ok",
            "data": {
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
        }
    except Exception as e:
        print(f"\n❌ ANALYSIS FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.post("/portfolio/snapshot")
def create_snapshot_endpoint():
    """Create a daily snapshot of portfolio performance"""
    try:
        print("\n📸 Creating portfolio snapshot...")
        
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        # Get current portfolio data
        portfolio_data = get_portfolio_endpoint()
        
        if portfolio_data.get('status') == 'error':
            raise HTTPException(status_code=500, detail=portfolio_data.get('message'))
        
        data = portfolio_data['data']
        
        # Count open positions
        portfolio_id = str(portfolio['id'])
        positions = get_positions(portfolio_id, status='open')
        position_count = len(positions) if positions else 0
        
        # Create snapshot
        snapshot_data = {
            'portfolio_id': portfolio_id,
            'snapshot_date': datetime.now().date(),
            'total_value': round(data['total_value'], 2),
            'cash_balance': round(data['cash'], 2),
            'positions_value': round(data['open_positions_value'], 2),
            'total_pnl': round(data['total_pnl'], 2),
            'position_count': position_count
        }
        
        snapshot = create_portfolio_snapshot(snapshot_data)
        
        print(f"✓ Snapshot created:")
        print(f"   Date: {snapshot_data['snapshot_date']}")
        print(f"   Total Value: £{snapshot_data['total_value']:,.2f}")
        print(f"   P&L: £{snapshot_data['total_pnl']:+,.2f}")
        print(f"   Positions: {position_count}\n")
        
        return {
            "status": "ok",
            "data": decimal_to_float(snapshot)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/portfolio/history")
def get_history_endpoint(days: int = 30):
    """Get portfolio performance history for the last N days"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        snapshots = get_portfolio_snapshots(portfolio_id, days)
        
        if not snapshots:
            # No historical data yet - return empty array
            print(f"⚠️  No portfolio history found (create snapshots with POST /portfolio/snapshot)")
            return {
                "status": "ok",
                "data": []
            }
        
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
        
        return {
            "status": "ok",
            "data": history
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.post("/cash/transaction")
def create_cash_transaction_endpoint(request: CashTransactionRequest):
    """Create a cash transaction (deposit or withdrawal)"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        
        # Validate transaction type
        if request.type not in ['deposit', 'withdrawal']:
            raise HTTPException(status_code=400, detail="Invalid transaction type. Must be 'deposit' or 'withdrawal'")
        
        # Validate amount
        if request.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        # For withdrawals, check if there's enough cash
        current_cash = float(portfolio['cash'])
        if request.type == 'withdrawal' and request.amount > current_cash:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient funds. Available cash: £{current_cash:.2f}"
            )
        
        # Create transaction record
        transaction_data = {
            'type': request.type,
            'amount': request.amount,
            'date': request.date or datetime.now().strftime('%Y-%m-%d'),
            'note': request.note or ''
        }
        
        transaction = create_cash_transaction(portfolio_id, transaction_data)
        
        # Update portfolio cash balance
        if request.type == 'deposit':
            new_cash = current_cash + request.amount
        else:  # withdrawal
            new_cash = current_cash - request.amount
        
        update_portfolio_cash(portfolio_id, new_cash)
        
        print(f"✓ Cash transaction created:")
        print(f"   Type: {request.type.upper()}")
        print(f"   Amount: £{request.amount:,.2f}")
        print(f"   New balance: £{new_cash:,.2f}")
        
        return {
            "status": "ok",
            "data": {
                "transaction": decimal_to_float(transaction),
                "new_balance": new_cash
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cash/transactions")
def get_cash_transactions_endpoint(order: str = "DESC"):
    """Get all cash transactions"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        
        # Validate order parameter
        if order.upper() not in ['ASC', 'DESC']:
            order = 'DESC'
        
        transactions = get_cash_transactions(portfolio_id, order.upper())
        
        # Format for frontend
        formatted = []
        for tx in transactions:
            formatted.append({
                'id': str(tx['id']),
                'type': tx['type'],
                'amount': float(tx['amount']),
                'date': str(tx['date']),
                'note': tx['note'] or '',
                'created_at': str(tx['created_at'])
            })
        
        return {
            "status": "ok",
            "data": formatted
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.get("/cash/summary")
def get_cash_summary_endpoint():
    """Get summary of all deposits and withdrawals"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        summary = get_total_deposits_withdrawals(portfolio_id)
        
        return {
            "status": "ok",
            "data": {
                "total_deposits": round(summary['total_deposits'], 2),
                "total_withdrawals": round(summary['total_withdrawals'], 2),
                "net_cash_flow": round(summary['net_cash_flow'], 2),
                "current_cash": float(portfolio['cash'])
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
        
@app.get("/trades")
def get_trades_endpoint():
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        trades = get_trade_history(portfolio_id)
        trades = [decimal_to_float(t) for t in trades]
        
        if not trades:
            return {
                "status": "ok",
                "data": {
                    "total_trades": 0,
                    "win_rate": 0,
                    "total_pnl": 0,
                    "trades": []
                }
            }
        
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        wins = len([t for t in trades if t.get('pnl', 0) > 0])
        win_rate = (wins / len(trades)) * 100
        
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
            "status": "ok",
            "data": {
                "total_trades": len(trades),
                "win_rate": round(win_rate, 1),
                "total_pnl": round(total_pnl, 2),
                "trades": formatted_trades
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/signals/generate")
def generate_signals_endpoint():
    """Generate momentum signals based on current portfolio state"""
    try:
        print("\n" + "="*70)
        print("🎯 GENERATING MOMENTUM SIGNALS")
        print("="*70)
        
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        available_cash = float(portfolio['cash'])
        
        # Get open positions to check for already-held stocks
        open_positions = get_positions(portfolio_id, status='open')
        held_tickers = set([pos['ticker'] for pos in open_positions])
        
        print(f"Portfolio cash: £{available_cash:,.2f}")
        print(f"Open positions: {len(open_positions)}")
        print(f"Held tickers: {held_tickers}\n")
        
        # Get settings
        settings_list = get_settings()
        settings = settings_list[0] if settings_list else None
        
        lookback_days = 252
        top_n = 5
        ma_period = 200
        atr_period = 14
        volatility_window = 60
        min_position_pct = 0.05
        max_position_pct = 0.20
        
        # Load universe
        import pandas as pd
        tickers = get_all_tickers()
        
        print(f"Universe: {len(tickers)} tickers")
        
        # Calculate dates
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days + 300)
        
        signal_date_str = end_date.strftime('%Y-%m-%d')
        
        # Download prices for all tickers
        print("Downloading price data...\n")
        
        prices_dict = {}
        failed = []
        
        for ticker in tickers:
            df_price = download_ticker_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            if df_price is not None and len(df_price) >= lookback_days:
                prices_dict[ticker] = df_price['close']
            else:
                failed.append(ticker)
        
        if not prices_dict:
            raise HTTPException(status_code=500, detail="Failed to download price data")
        
        prices = pd.DataFrame(prices_dict)
        prices = prices.ffill(limit=5)
        
        print(f"✓ Downloaded {len(prices.columns)} tickers")
        if failed:
            print(f"⚠️  Failed: {len(failed)} tickers\n")
        
        # Get live FX rate
        live_fx_rate = get_live_fx_rate()
        
        # Download market indices
        print("Checking market regime...")
        spy_data = download_ticker_data("SPY", start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        ftse_data = download_ticker_data("^FTSE", start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        if spy_data is None or ftse_data is None:
            print("⚠️  Market data unavailable, assuming risk-on\n")
            spy_risk_on = True
            ftse_risk_on = True
        else:
            spy_close = spy_data['close']
            ftse_close = ftse_data['close']
            
            spy_ma200 = spy_close.rolling(ma_period).mean()
            ftse_ma200 = ftse_close.rolling(ma_period).mean()
            
            spy_risk_on = spy_close.iloc[-1] > spy_ma200.iloc[-1]
            ftse_risk_on = ftse_close.iloc[-1] > ftse_ma200.iloc[-1]
        
        print(f"SPY: {'🟢 Risk On' if spy_risk_on else '🔴 Risk Off'}")
        print(f"FTSE: {'🟢 Risk On' if ftse_risk_on else '🔴 Risk Off'}\n")
        
        # Calculate momentum
        print("Calculating momentum...")
        momentum = prices.pct_change(lookback_days, fill_method=None)
        
        # Calculate MA200 trend
        ma200 = prices.rolling(ma_period).mean()
        trend = prices > ma200
        
        # Get latest values
        latest_momentum = momentum.iloc[-1]
        latest_trend = trend.iloc[-1]
        latest_prices = prices.iloc[-1]
        
        # Calculate ATR for all tickers
        print("Calculating ATR...")
        atr_dict = {}
        for ticker in prices.columns:
            atr = compute_atr_simple(prices[ticker], atr_period)
            if len(atr) > 0 and not pd.isna(atr.iloc[-1]):
                atr_dict[ticker] = atr.iloc[-1]
        
        # Calculate volatility
        print("Calculating volatility...")
        volatility_dict = {}
        for ticker in prices.columns:
            returns = prices[ticker].pct_change()
            vol = returns.rolling(volatility_window).std()
            if len(vol) > 0 and not pd.isna(vol.iloc[-1]):
                volatility_dict[ticker] = vol.iloc[-1]
        
        # Rank stocks by momentum
        ranks = latest_momentum.rank(ascending=False, method='first')
        
        # Generate signals
        print("\nGenerating signals...\n")
        signals = []
        
        for ticker in prices.columns:
            # Check trend and rank
            if pd.isna(latest_trend[ticker]) or not latest_trend[ticker]:
                continue
            
            if pd.isna(ranks[ticker]) or ranks[ticker] > top_n:
                continue
            
            # Check market regime
            is_uk = ticker.endswith('.L')
            market_risk_on = ftse_risk_on if is_uk else spy_risk_on
            
            if not market_risk_on:
                continue
            
            # Get price and ATR
            native_price = latest_prices[ticker]
            native_atr = atr_dict.get(ticker)
            
            if pd.isna(native_atr) or native_atr == 0:
                continue
            
            # Convert to GBP
            if is_uk:
                # UK prices in pence, convert to pounds
                price_gbp = native_price / 100
                atr_gbp = native_atr / 100
                price_display = price_gbp
                currency = "GBP"
                market = "UK"
            else:
                # US prices in USD
                price_gbp = native_price / live_fx_rate
                atr_gbp = native_atr / live_fx_rate
                price_display = native_price
                currency = "USD"
                market = "US"
            
            # Get volatility
            vol = volatility_dict.get(ticker, 0)
            if pd.isna(vol) or vol == 0:
                continue
            
            # Check if already held
            status = 'already_held' if ticker in held_tickers else 'new'
            
            signals.append({
                'ticker': ticker,
                'market': market,
                'rank': int(ranks[ticker]),
                'momentum_percent': round(latest_momentum[ticker] * 100, 2),
                'current_price': round(price_display, 2),
                'price_gbp': round(price_gbp, 2),
                'atr_value': round(atr_gbp, 4),
                'volatility': round(vol, 6),
                'initial_stop': round(price_display - (5 * (atr_gbp if currency == 'GBP' else native_atr)), 2),
                'status': status
            })
        
        if not signals:
            print("⚠️  No qualifying signals found\n")
            return {
                "status": "ok",
                "data": {
                    "signals_generated": 0,
                    "signal_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "fx_rate": live_fx_rate,
                    "signals": []
                }
            }
        
        # Sort by rank
        signals_sorted = sorted(signals, key=lambda x: x['rank'])
        
        # Calculate position sizing (equal weight)
        available_for_new = available_cash
        new_signals = [s for s in signals_sorted if s['status'] == 'new']
        
        if new_signals:
            allocation_per_stock = available_for_new / len(new_signals)
            
            # Clamp to min/max
            min_allocation = available_for_new * min_position_pct
            max_allocation = available_for_new * max_position_pct
            allocation_per_stock = max(min_allocation, min(max_allocation, allocation_per_stock))
        
        # Add position sizing to signals
        for signal in signals_sorted:
            if signal['status'] == 'new':
                signal['allocation_gbp'] = round(allocation_per_stock, 2)
                signal['suggested_shares'] = int(allocation_per_stock / signal['price_gbp'])  # ← FIND THIS LINE
                
                # Calculate fees
                if signal['market'] == 'UK':
                    fee_rate = 0.005  # 0.5% stamp duty
                else:
                    fee_rate = 0.0015  # 0.15% FX fee
                
                gross_cost = signal['suggested_shares'] * signal['price_gbp']
                fees = gross_cost * fee_rate
                signal['total_cost'] = round(gross_cost + fees, 2)
            else:
                # Already held - no allocation
                signal['allocation_gbp'] = 0
                signal['suggested_shares'] = 0
                signal['total_cost'] = 0
        
        # Save to database
        print(f"Saving {len(signals_sorted)} signals to database...")
        
        for signal_data in signals_sorted:
            signal_data['portfolio_id'] = portfolio_id
            signal_data['signal_date'] = signal_date_str
            create_signal(portfolio_id, signal_data)
        
        print(f"✓ Saved {len(signals_sorted)} signals\n")
        print("="*70 + "\n")
        
        return {
            "status": "ok",
            "data": {
                "signals_generated": len(signals_sorted),
                "new_signals": len(new_signals),
                "already_held": len([s for s in signals_sorted if s['status'] == 'already_held']),
                "signal_date": signal_date_str,
                "fx_rate": live_fx_rate,
                "available_cash": available_cash,
                "market_regime": {
                    "spy_risk_on": spy_risk_on,
                    "ftse_risk_on": ftse_risk_on
                },
                "signals": [decimal_to_float(s) for s in signals_sorted]
            }
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/status")
def get_market_status():
    """
    Get current market regime (SPY and FTSE vs 200-day MA)
    Returns live FX rate as well
    
    This endpoint provides real-time market status for the Signals page
    """
    try:
        print("\n📊 Fetching market status...")
        
        # Reuse existing check_market_regime() function
        market_regime = check_market_regime()
        
        # Get live FX rate
        fx_rate = get_live_fx_rate()
        
        print(f"✓ Market status retrieved:")
        print(f"   SPY: {'🟢 Risk On' if market_regime['spy_risk_on'] else '🔴 Risk Off'}")
        print(f"   FTSE: {'🟢 Risk On' if market_regime['ftse_risk_on'] else '🔴 Risk Off'}")
        print(f"   FX Rate: {fx_rate:.4f}\n")
        
        return {
            "status": "ok",
            "data": {
                "spy": {
                    "price": round(market_regime['spy_price'], 2),
                    "ma200": round(market_regime['spy_ma200'], 2),
                    "is_risk_on": market_regime['spy_risk_on']
                },
                "ftse": {
                    "price": round(market_regime['ftse_price'], 2),
                    "ma200": round(market_regime['ftse_ma200'], 2),
                    "is_risk_on": market_regime['ftse_risk_on']
                },
                "fx_rate": round(fx_rate, 4),
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Failed to fetch market status: {str(e)}"
        }


@app.get("/signals")
def get_signals_endpoint(status: str = None):
    """Get all signals, optionally filtered by status"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        signals = get_signals(portfolio_id, status)
        
        return [decimal_to_float(s) for s in signals]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/signals/{signal_id}")
def update_signal_endpoint(signal_id: str, updates: dict):
    """Update a signal (e.g., change status)"""
    try:
        updated = update_signal(signal_id, updates)
        return {
            "status": "ok",
            "data": decimal_to_float(updated)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/signals/{signal_id}")
def delete_signal_endpoint(signal_id: str):
    """Delete a signal"""
    try:
        delete_signal(signal_id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
