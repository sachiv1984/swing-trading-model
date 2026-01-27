from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from datetime import timedelta
import time
import requests

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
    update_settings
)

app = FastAPI(title="Trading Assistant API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sachiv1984.github.io",
        "https://trading-assistant-api-c0f9.onrender.com",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models - FIXED to match frontend
class AddPositionRequest(BaseModel):
    ticker: str
    market: str
    entry_date: str
    shares: float  # Changed from int to allow fractional shares
    entry_price: float  # Frontend sends this instead of fill_price
    current_price: Optional[float] = None
    fx_rate: Optional[float] = None
    atr_value: Optional[float] = None  # Frontend sends this
    stop_price: Optional[float] = None
    fees: Optional[float] = None
    status: Optional[str] = "open"


class SettingsRequest(BaseModel):
    min_hold_days: Optional[int] = 5
    atr_multiplier_initial: Optional[float] = 2
    atr_multiplier_trailing: Optional[float] = 3
    atr_period: Optional[int] = 14
    default_currency: Optional[str] = "GBP"
    theme: Optional[str] = "dark"
    uk_commission: Optional[float] = 9.95
    us_commission: Optional[float] = 0
    stamp_duty_rate: Optional[float] = 0.005
    fx_fee_rate: Optional[float] = 0.0015


# Helper to convert Decimal to float
def decimal_to_float(obj):
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj


def get_current_price(ticker: str) -> float:
    """Fetch current price directly from Yahoo Finance API (bypassing yfinance library)"""
    try:
        # Add delay to avoid rate limiting
        time.sleep(0.3)
        
        # Direct Yahoo Finance API call
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "1d"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️  {ticker}: HTTP {response.status_code}")
            return None
        
        data = response.json()
        
        # Extract price from response
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            # Try meta.regularMarketPrice first
            if "meta" in result and "regularMarketPrice" in result["meta"]:
                price = float(result["meta"]["regularMarketPrice"])
                if price > 0:
                    print(f"✓ {ticker}: ${price:.2f} (Yahoo API)")
                    return price
            
            # Try latest close price from indicators
            if "indicators" in result and "quote" in result["indicators"]:
                quotes = result["indicators"]["quote"]
                if len(quotes) > 0 and "close" in quotes[0]:
                    closes = [c for c in quotes[0]["close"] if c is not None]
                    if closes:
                        price = float(closes[-1])
                        if price > 0:
                            print(f"✓ {ticker}: ${price:.2f} (Yahoo API - close)")
                            return price
        
        print(f"⚠️  {ticker}: No price in API response")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"❌ {ticker}: Network error - {str(e)}")
        return None
    except Exception as e:
        print(f"❌ {ticker}: Error - {str(e)}")
        return None


def check_market_regime():
    """Check SPY and FTSE for risk on/off using direct Yahoo Finance API"""
    try:
        time.sleep(0.3)
        
        def get_ma200(ticker: str):
            """Get current price and 200-day MA"""
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                params = {
                    "interval": "1d",
                    "range": "1y"
                }
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=15)
                data = response.json()
                
                if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
                    result = data["chart"]["result"][0]
                    
                    # Get current price
                    current = None
                    if "meta" in result and "regularMarketPrice" in result["meta"]:
                        current = float(result["meta"]["regularMarketPrice"])
                    
                    # Get historical closes for MA200
                    ma200 = None
                    if "indicators" in result and "quote" in result["indicators"]:
                        quotes = result["indicators"]["quote"]
                        if len(quotes) > 0 and "close" in quotes[0]:
                            closes = [c for c in quotes[0]["close"] if c is not None]
                            if len(closes) >= 200:
                                # Calculate 200-day moving average
                                ma200 = sum(closes[-200:]) / 200
                            elif len(closes) > 0:
                                # Use available data if less than 200 days
                                ma200 = sum(closes) / len(closes)
                    
                    return current, ma200
                
                return None, None
            except Exception as e:
                print(f"Error getting MA200 for {ticker}: {e}")
                return None, None
        
        # Get SPY data
        spy_price, spy_ma200 = get_ma200("SPY")
        
        # Get FTSE data
        ftse_price, ftse_ma200 = get_ma200("^FTSE")
        
        # Default to risk-on if we can't fetch data
        if spy_price is None or spy_ma200 is None:
            print("⚠️  Could not fetch SPY data, defaulting to risk-on")
            spy_risk_on = True
            spy_price = 0
            spy_ma200 = 0
        else:
            spy_risk_on = spy_price > spy_ma200
        
        if ftse_price is None or ftse_ma200 is None:
            print("⚠️  Could not fetch FTSE data, defaulting to risk-on")
            ftse_risk_on = True
            ftse_price = 0
            ftse_ma200 = 0
        else:
            ftse_risk_on = ftse_price > ftse_ma200
        
        return {
            'spy_risk_on': spy_risk_on,
            'ftse_risk_on': ftse_risk_on,
            'spy_price': spy_price or 0,
            'spy_ma200': spy_ma200 or 0,
            'ftse_price': ftse_price or 0,
            'ftse_ma200': ftse_ma200 or 0
        }
    except Exception as e:
        print(f"❌ Market regime check failed: {e}")
        return {
            'spy_risk_on': True,
            'ftse_risk_on': True,
            'spy_price': 0,
            'spy_ma200': 0,
            'ftse_price': 0,
            'ftse_ma200': 0
        }


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
    """Get open positions with live prices and calculated stops"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        positions = get_positions(portfolio_id, status='open')
        
        if not positions:
            return []
        
        # Get analysis data (live prices, stops, signals)
        try:
            print(f"\n📊 Running live analysis for {len(positions)} positions...")
            analysis_response = analyze_positions_endpoint()
            
            # Handle response format
            if isinstance(analysis_response, dict):
                if 'status' in analysis_response and analysis_response['status'] == 'ok':
                    analysis_data = analysis_response.get('data', {})
                else:
                    analysis_data = analysis_response
            else:
                analysis_data = {}
            
            actions = analysis_data.get('actions', [])
            market_regime = analysis_data.get('market_regime', {})
            
            print(f"✓ Analysis complete: {len(actions)} position(s) analyzed")
            
        except Exception as e:
            print(f"⚠️  Analysis failed: {e}")
            import traceback
            traceback.print_exc()
            actions = []
            market_regime = {}
        
        positions_list = []
        
        for pos in positions:
            pos = decimal_to_float(pos)
            
            # Find analysis data for this position (match with full ticker including .L)
            analysis = next((a for a in actions if a['ticker'] == pos['ticker']), None)
            
            if analysis:
                # Use live analyzed data
                current_price = analysis['current_price']
                current_stop = analysis['current_stop']
                pnl = analysis['pnl']
                pnl_pct = analysis['pnl_pct']
                holding_days = analysis['holding_days']
                grace_period = analysis['grace_period']
                stop_reason = analysis['stop_reason']
                
                # Determine display status
                if analysis['action'] == 'EXIT':
                    display_status = "EXIT"
                    exit_reason = analysis['exit_reason']
                elif grace_period:
                    display_status = "GRACE"
                    exit_reason = None
                elif pnl > 0:
                    display_status = "PROFITABLE"
                    exit_reason = None
                else:
                    display_status = "LOSING"
                    exit_reason = None
            else:
                # Fallback to stored data
                print(f"⚠️  No analysis found for {pos['ticker']}, using stored data")
                current_price = pos.get('current_price', pos['entry_price'])
                current_stop = pos.get('current_stop', 0)
                pnl = pos.get('pnl', 0)
                pnl_pct = pos.get('pnl_pct', 0)
                
                entry_date = datetime.strptime(str(pos['entry_date']), '%Y-%m-%d')
                holding_days = (datetime.now() - entry_date).days
                
                grace_period = holding_days < 10
                stop_reason = f"Grace period ({holding_days}/10 days)" if grace_period else "No live data"
                
                if grace_period:
                    display_status = "GRACE"
                elif pnl > 0:
                    display_status = "PROFITABLE"
                else:
                    display_status = "LOSING"
                exit_reason = None
            
            current_value = current_price * pos['shares']
            
            # Display ticker without .L suffix for UK stocks
            display_ticker = pos['ticker'].replace('.L', '') if pos['market'] == 'UK' else pos['ticker']
            
            # Map backend fields to frontend field names
            positions_list.append({
                "id": str(pos['id']),
                "ticker": display_ticker,
                "market": pos['market'],
                "entry_date": str(pos['entry_date']),
                "entry_price": round(pos['entry_price'], 2),
                "shares": pos['shares'],
                "current_price": round(current_price, 2),
                "stop_price": round(current_stop, 2),
                "pnl": round(pnl, 2),
                "pnl_percent": round(pnl_pct, 2),
                "holding_days": holding_days,
                "status": "open",
                "display_status": display_status,
                "exit_reason": exit_reason,
                "grace_period": grace_period,
                "stop_reason": stop_reason,
                "atr_value": pos.get('atr', 0),
                "fx_rate": pos.get('fx_rate', 1.0)
            })
        
        return positions_list
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/portfolio")
def get_portfolio_endpoint():
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        positions = get_positions(portfolio_id, status='open')
        
        positions_list = []
        total_positions_value = 0
        
        for pos in positions:
            pos = decimal_to_float(pos)
            current_price = pos.get('current_price', pos['entry_price'])
            current_value = current_price * pos['shares']
            pnl = pos.get('pnl', 0)
            pnl_pct = pos.get('pnl_pct', 0)
            holding_days = pos.get('holding_days', 0)
            
            total_positions_value += current_value
            
            if holding_days < 10:
                display_status = "GRACE"
            elif pnl > 0:
                display_status = "PROFITABLE"
            else:
                display_status = "LOSING"
            
            positions_list.append({
                "id": str(pos['id']),
                "ticker": pos['ticker'],
                "market": pos['market'],
                "entry_date": str(pos['entry_date']),
                "entry_price": round(pos['entry_price'], 2),
                "shares": pos['shares'],
                "current_price": round(current_price, 2),
                "current_value": round(current_value, 2),
                "pnl": round(pnl, 2),
                "pnl_pct": round(pnl_pct, 2),
                "current_stop": round(pos.get('current_stop', 0), 2),
                "holding_days": holding_days,
                "status": display_status
            })
        
        cash = float(portfolio['cash'])
        total_value = cash + total_positions_value
        
        return {
            "status": "ok",
            "data": {
                "cash": cash,
                "cash_balance": cash,
                "total_value": total_value,
                "open_positions_value": total_positions_value,
                "total_pnl": sum(p['pnl'] for p in positions_list),
                "last_updated": str(portfolio['last_updated']),
                "positions": positions_list
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/portfolio/position")
def add_position_endpoint(request: AddPositionRequest):
    """FIXED: Now accepts frontend format with fractional shares"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        
        # Get settings for commission and fee rates
        settings_list = get_settings()
        settings = settings_list[0] if settings_list else None
        
        # Use settings or defaults
        uk_commission = float(settings.get('uk_commission', 9.95)) if settings else 9.95
        us_commission = float(settings.get('us_commission', 0)) if settings else 0
        stamp_duty_rate = float(settings.get('stamp_duty_rate', 0.005)) if settings else 0.005
        fx_fee_rate = float(settings.get('fx_fee_rate', 0.0015)) if settings else 0.0015
        
        # Calculate fees and costs
        is_uk = request.market == "UK"
        
        # Auto-append .L for UK stocks
        ticker = request.ticker.upper().strip()
        if is_uk and not ticker.endswith('.L'):
            ticker = f"{ticker}.L"
            print(f"✓ Auto-appended .L to UK ticker: {ticker}")
        
        # Use entry_price from frontend as fill_price
        fill_price = request.entry_price
        shares = request.shares
        fx_rate = request.fx_rate or (1.0 if is_uk else 1.27)
        
        if is_uk:
            gross_cost = shares * fill_price
            stamp_duty = gross_cost * stamp_duty_rate
            commission = uk_commission
            total_fees = stamp_duty + commission
            total_cost = gross_cost + total_fees
            # Entry price for display is the actual fill price, not adjusted for fees
            entry_price_for_display = fill_price
        else:
            # US position - costs calculated in GBP for portfolio tracking
            fill_price_gbp = fill_price / fx_rate
            gross_cost = shares * fill_price_gbp
            
            fx_fee = gross_cost * fx_fee_rate
            commission = us_commission
            
            total_fees = fx_fee + commission
            total_cost = gross_cost + total_fees
            # Entry price for display is the actual USD fill price
            entry_price_for_display = fill_price
        
        # Calculate initial stop based on the fill price, not fee-adjusted price
        atr = request.atr_value or 0
        atr_multiplier = float(settings.get('atr_multiplier_initial', 2)) if settings else 2
        
        if atr > 0 and request.stop_price is None:
            initial_stop = entry_price_for_display - (atr_multiplier * atr)
        else:
            initial_stop = request.stop_price or entry_price_for_display
        
        # Create position with the modified ticker
        position_data = {
            'ticker': ticker,
            'market': request.market,
            'entry_date': request.entry_date,
            'entry_price': round(entry_price_for_display, 4),  # Store actual fill price for display
            'fill_price': fill_price,
            'fill_currency': 'GBP' if is_uk else 'USD',
            'fx_rate': fx_rate,
            'shares': shares,
            'total_cost': round(total_cost, 2),
            'fees_paid': round(total_fees, 2),
            'fees': round(total_fees, 2),
            'fee_type': 'stamp_duty' if is_uk else 'fx_fee',
            'initial_stop': round(initial_stop, 2),
            'current_stop': round(initial_stop, 2),
            'current_price': round(entry_price_for_display, 4),  # Initialize with fill price
            'holding_days': 0,
            'pnl': 0.0,
            'pnl_pct': 0.0,
            'status': 'open'
        }
        
        new_position = create_position(portfolio_id, position_data)
        
        # Update cash
        new_cash = float(portfolio['cash']) - total_cost
        update_portfolio_cash(portfolio_id, new_cash)
        
        return {
            "status": "ok",
            "data": {
                "ticker": ticker,
                "total_cost": round(total_cost, 2),
                "fees_paid": round(total_fees, 2),
                "entry_price": round(entry_price_for_display, 4),  # Return actual fill price
                "initial_stop": round(initial_stop, 2),
                "remaining_cash": round(new_cash, 2)
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/positions/analyze")
def analyze_positions_endpoint():
    """Run daily position analysis with live prices and market regime"""
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
        
        # Get market regime
        print("\n📊 Checking market regime...")
        market_regime = check_market_regime()
        print(f"   SPY: {'🟢 Risk On' if market_regime['spy_risk_on'] else '🔴 Risk Off'}")
        print(f"   FTSE: {'🟢 Risk On' if market_regime['ftse_risk_on'] else '🔴 Risk Off'}")
        
        actions = []
        total_value = 0
        total_pnl = 0
        
        print(f"\n💼 Analyzing {len(positions)} position(s)...")
        
        for pos in positions:
            pos = decimal_to_float(pos)
            
            print(f"\n{'='*70}")
            print(f"📈 Analyzing: {pos['ticker']} ({pos['market']})")
            print(f"{'='*70}")
            
            # Get live price with detailed logging
            print(f"   🔍 Fetching live price from yfinance...")
            live_price = get_current_price(pos['ticker'])
            
            entry_price = pos['entry_price']
            
            if live_price:
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
            current_value = current_price * shares
            pnl = (current_price - entry_price) * shares
            pnl_pct = ((current_price - entry_price) / entry_price) * 100
            
            total_value += current_value
            total_pnl += pnl
            
            # Calculate holding days
            entry_date = datetime.strptime(str(pos['entry_date']), '%Y-%m-%d')
            holding_days = (datetime.now() - entry_date).days
            
            print(f"   Holdings: {shares} shares = ${current_value:.2f}")
            print(f"   P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
            print(f"   Days held: {holding_days}")
            
            # Determine action
            action = "HOLD"
            exit_reason = None
            stop_reason = ""
            current_stop = pos.get('current_stop', pos.get('initial_stop', 0))
            
            # Check grace period
            grace_period = holding_days < 10
            
            if grace_period:
                stop_reason = f"Grace period ({holding_days}/10 days)"
                print(f"   🆕 Grace period active - no stop loss")
            else:
                # Check market regime
                is_uk = pos['market'] == 'UK'
                market_risk_on = market_regime['ftse_risk_on'] if is_uk else market_regime['spy_risk_on']
                
                if not market_risk_on:
                    action = "EXIT"
                    exit_reason = "Risk-Off Signal"
                    stop_reason = "Market risk-off"
                    print(f"   🔴 EXIT: Market risk-off")
                elif current_price <= current_stop:
                    action = "EXIT"
                    exit_reason = "Stop Loss Hit"
                    stop_reason = "Stop triggered"
                    print(f"   🔴 EXIT: Stop loss hit (${current_stop:.2f})")
                elif pnl > 0:
                    stop_reason = "Profitable (tight 2x ATR)"
                    print(f"   ✅ HOLD: Profitable, tight stop")
                else:
                    stop_reason = "At loss (wide 5x ATR)"
                    print(f"   ✅ HOLD: At loss, wide stop")
            
            # Update position in database if we have new price
            if live_price and live_price != pos.get('current_price'):
                print(f"   💾 Updating position with new price...")
                update_position(str(pos['id']), {
                    'current_price': round(current_price, 4),
                    'holding_days': holding_days,
                    'pnl': round(pnl, 2),
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
                "pnl": round(pnl, 2),
                "pnl_pct": round(pnl_pct, 2),
                "current_stop": round(current_stop, 2),
                "holding_days": holding_days,
                "stop_reason": stop_reason,
                "grace_period": grace_period
            })
        
        exit_count = len([a for a in actions if a['action'] == 'EXIT'])
        
        print(f"\n{'='*70}")
        print(f"📊 ANALYSIS COMPLETE")
        print(f"{'='*70}")
        print(f"Total Value: ${total_value:.2f}")
        print(f"Total P&L: ${total_pnl:+.2f}")
        print(f"Exit Signals: {exit_count}")
        print("="*70 + "\n")
        
        return {
            "status": "ok",
            "data": {
                "analysis_date": datetime.now().strftime('%Y-%m-%d'),
                "market_regime": market_regime,
                "summary": {
                    "total_value": round(total_value, 2),
                    "total_pnl": round(total_pnl, 2),
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
                "ticker": t['ticker'],
                "entry_date": str(t['entry_date']),
                "exit_date": str(t['exit_date']),
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
