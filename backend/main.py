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
    update_settings,
    create_portfolio_snapshot,
    get_portfolio_snapshots,
    create_cash_transaction,
    get_cash_transactions,
    get_total_deposits_withdrawals
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
    atr_multiplier_trailing: Optional[float] = 2
    atr_period: Optional[int] = 14
    default_currency: Optional[str] = "GBP"
    theme: Optional[str] = "dark"
    uk_commission: Optional[float] = 9.95
    us_commission: Optional[float] = 0
    stamp_duty_rate: Optional[float] = 0.005
    fx_fee_rate: Optional[float] = 0.0015


class CashTransactionRequest(BaseModel):
    type: str  # "deposit" or "withdrawal"
    amount: float
    date: Optional[str] = None
    note: Optional[str] = ""


# Helper to convert Decimal to float
def decimal_to_float(obj):
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj


def calculate_atr(ticker: str, period: int = 14) -> float:
    """Calculate ATR for a ticker if not stored in database"""
    try:
        # Fetch historical data
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "1mo"  # Need enough data for ATR calculation
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            if "indicators" in result and "quote" in result["indicators"]:
                quote = result["indicators"]["quote"][0]
                
                # Get high, low, close
                highs = [h for h in quote.get("high", []) if h is not None]
                lows = [l for l in quote.get("low", []) if l is not None]
                closes = [c for c in quote.get("close", []) if c is not None]
                
                if len(highs) >= period and len(lows) >= period and len(closes) >= period:
                    # Calculate True Range
                    true_ranges = []
                    for i in range(1, len(closes)):
                        high_low = highs[i] - lows[i]
                        high_close = abs(highs[i] - closes[i-1])
                        low_close = abs(lows[i] - closes[i-1])
                        true_range = max(high_low, high_close, low_close)
                        true_ranges.append(true_range)
                    
                    # Calculate ATR (simple moving average of TR)
                    if len(true_ranges) >= period:
                        atr = sum(true_ranges[-period:]) / period
                        
                        # Fix UK stocks: Yahoo returns pence, need to convert to pounds
                        if ticker.endswith('.L') and atr > 100:
                            atr = atr / 100
                            print(f"   📊 Calculated ATR for {ticker}: {atr:.2f} (converted from pence)")
                        else:
                            print(f"   📊 Calculated ATR for {ticker}: {atr:.2f}")
                        
                        return atr
        
        print(f"   ⚠️  Could not calculate ATR for {ticker}")
        return None
        
    except Exception as e:
        print(f"   ❌ ATR calculation error for {ticker}: {e}")
        return None


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


def get_live_fx_rate():
    """Fetch live GBP/USD exchange rate from Yahoo Finance"""
    try:
        time.sleep(0.2)
        
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GBPUSD=X"
        params = {
            "interval": "1d",
            "range": "1d"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            # Try meta.regularMarketPrice first
            if "meta" in result and "regularMarketPrice" in result["meta"]:
                fx_rate = float(result["meta"]["regularMarketPrice"])
                if fx_rate > 0:
                    print(f"✓ Live FX rate (GBP/USD): {fx_rate:.4f}")
                    return fx_rate
            
            # Try latest close price
            if "indicators" in result and "quote" in result["indicators"]:
                quotes = result["indicators"]["quote"]
                if len(quotes) > 0 and "close" in quotes[0]:
                    closes = [c for c in quotes[0]["close"] if c is not None]
                    if closes:
                        fx_rate = float(closes[-1])
                        if fx_rate > 0:
                            print(f"✓ Live FX rate (GBP/USD): {fx_rate:.4f}")
                            return fx_rate
        
        print("⚠️  Could not fetch live FX rate, using default 1.27")
        return 1.27
        
    except Exception as e:
        print(f"⚠️  FX rate fetch error: {e}, using default 1.27")
        return 1.27


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
            
            # Calculate P&L correctly
            # For US stocks: entry_price is in GBP (stored), but we need USD for comparison
            # So use fill_price (USD) for US stocks, entry_price (GBP) for UK stocks
            if pos['market'] == 'US':
                # US stock: Compare USD to USD
                entry_price_usd = pos.get('fill_price', pos['entry_price'] * (pos.get('fx_rate', 1.27)))
                pnl_usd = (current_price_native - entry_price_usd) * pos['shares']
                pnl_gbp = pnl_usd / live_fx_rate
                entry_price_display = entry_price_usd
            else:
                # UK stock: Already in GBP
                entry_price_display = pos['entry_price']
                pnl_gbp = (current_price_native - entry_price_display) * pos['shares']
            
            pnl_pct = ((current_price_native - entry_price_display) / entry_price_display) * 100 if entry_price_display > 0 else 0
            
            # Convert to GBP for Dashboard calculations
            if pos['market'] == 'US':
                current_price_gbp = current_price_native / live_fx_rate
                print(f"   💱 ${current_price_native:.2f} → £{current_price_gbp:.2f}")
            else:
                current_price_gbp = current_price_native
            
            # Calculate holding days
            entry_date = datetime.strptime(str(pos['entry_date']), '%Y-%m-%d')
            holding_days = (datetime.now() - entry_date).days
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
            
            # Return both GBP and native prices
            positions_list.append({
                "id": str(pos['id']),
                "ticker": display_ticker,
                "market": pos['market'],
                "entry_date": str(pos['entry_date']),
                "entry_price": round(entry_price_display, 2),  # Native currency for display
                "shares": pos['shares'],
                "current_price": round(current_price_gbp, 2),  # GBP for Dashboard
                "current_price_native": round(current_price_native, 2),  # Native for display
                "stop_price": round(stop_price_gbp, 2),  # GBP (0 during grace)
                "stop_price_native": round(stop_price_native, 2),  # Native (0 during grace) - STABLE!
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
                "live_fx_rate": live_fx_rate
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
            initial_stop_native = entry_price_for_display - (atr_multiplier * atr)
        else:
            initial_stop_native = request.stop_price or entry_price_for_display
        
        # Store stop in NATIVE currency (USD for US, GBP for UK)
        # This prevents FX fluctuations from affecting displayed stop prices
        initial_stop = initial_stop_native
        
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
            'initial_stop': round(initial_stop, 2),  # Native currency
            'current_stop': round(initial_stop, 2),  # Native currency
            'current_price': round(entry_price_for_display, 4),  # Initialize with fill price
            'atr': round(atr, 4) if atr > 0 else None,  # Store ATR for trailing stop calculations
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
                "initial_stop": round(initial_stop_native, 2),  # Return native currency for display
                "remaining_cash": round(new_cash, 2)
            }
        }
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
            
            # Calculate P&L in native currency then convert to GBP using LIVE FX rate
            pnl_native = (current_price - entry_price) * shares
            if pos['market'] == 'US':
                pnl_gbp = pnl_native / live_fx_rate
                print(f"   💰 P&L in GBP (LIVE rate): ${pnl_native:.2f} / {live_fx_rate:.4f} = £{pnl_gbp:.2f}")
            else:
                pnl_gbp = pnl_native
            
            pnl_pct = ((current_price - entry_price) / entry_price) * 100
            
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


@app.post("/positions/{position_id}/exit")
def exit_position_endpoint(position_id: str):
    """Exit a position and record in trade history"""
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
        
        # Get current live price for exit
        print(f"\n📤 Exiting position: {position['ticker']}")
        
        live_price = get_current_price(position['ticker'])
        if not live_price:
            raise HTTPException(status_code=500, detail="Could not fetch current price for exit")
        
        # Fix UK stocks (Yahoo returns pence)
        if position['market'] == 'UK' and live_price > 1000:
            live_price = live_price / 100
        
        exit_price_native = live_price
        print(f"   Exit price: {exit_price_native:.2f}")
        
        # Get live FX rate
        live_fx_rate = get_live_fx_rate()
        
        # Calculate exit proceeds
        shares = float(position['shares'])
        market = position['market']
        
        # Calculate in native currency first
        gross_proceeds_native = exit_price_native * shares
        
        # Calculate exit fees
        if market == 'UK':
            exit_fee_rate = 0.0  # No stamp duty on sale, only commission
            commission = 9.95  # From settings
            exit_fees = commission
        else:
            exit_fee_rate = 0.0015  # FX fee
            commission = 0.0
            exit_fees = gross_proceeds_native * exit_fee_rate
        
        # Net proceeds in native currency
        net_proceeds_native = gross_proceeds_native - exit_fees
        
        # Convert to GBP if US stock
        if market == 'US':
            gross_proceeds_gbp = gross_proceeds_native / live_fx_rate
            net_proceeds_gbp = net_proceeds_native / live_fx_rate
            exit_fees_gbp = exit_fees / live_fx_rate
        else:
            gross_proceeds_gbp = gross_proceeds_native
            net_proceeds_gbp = net_proceeds_native
            exit_fees_gbp = exit_fees
        
        # Calculate P&L
        entry_price = float(position.get('fill_price', position['entry_price'])) if market == 'US' else float(position['entry_price'])
        entry_fees = float(position.get('fees_paid', 0))
        total_cost = float(position['total_cost'])
        
        # P&L = net proceeds - total cost
        realized_pnl_gbp = net_proceeds_gbp - total_cost
        realized_pnl_pct = (realized_pnl_gbp / total_cost) * 100
        
        # Calculate holding period
        entry_date = datetime.strptime(str(position['entry_date']), '%Y-%m-%d')
        exit_date = datetime.now()
        holding_days = (exit_date - entry_date).days
        
        print(f"   Shares: {shares}")
        print(f"   Gross proceeds: £{gross_proceeds_gbp:.2f}")
        print(f"   Exit fees: £{exit_fees_gbp:.2f}")
        print(f"   Net proceeds: £{net_proceeds_gbp:.2f}")
        print(f"   Total cost: £{total_cost:.2f}")
        print(f"   Realized P&L: £{realized_pnl_gbp:+.2f} ({realized_pnl_pct:+.2f}%)")
        
        # Create trade history record
        trade_data = {
            'ticker': position['ticker'],
            'market': market,
            'entry_date': position['entry_date'],
            'exit_date': exit_date.strftime('%Y-%m-%d'),
            'shares': shares,
            'entry_price': entry_price,
            'exit_price': exit_price_native,
            'total_cost': total_cost,
            'gross_proceeds': gross_proceeds_gbp,
            'net_proceeds': net_proceeds_gbp,
            'entry_fees': entry_fees,
            'exit_fees': exit_fees_gbp,
            'pnl': realized_pnl_gbp,
            'pnl_pct': realized_pnl_pct,
            'holding_days': holding_days,
            'exit_reason': 'Manual Exit',
            'entry_fx_rate': float(position.get('fx_rate', 1.0)),
            'exit_fx_rate': live_fx_rate if market == 'US' else 1.0
        }
        
        print(f"   💾 Creating trade history record...")
        create_trade_history(portfolio_id, trade_data)
        print(f"   ✓ Trade history created")
        
        # Update position to closed
        # NOTE: If exit_date, exit_price, exit_reason columns don't exist in positions table,
        # just update status. The real data is in trade_history anyway.
        print(f"   💾 Updating position status to closed...")
        
        try:
            # Try updating with all exit fields (requires migration to add columns)
            updated_position = update_position(position_id, {
                'status': 'closed',
                'exit_date': exit_date.strftime('%Y-%m-%d'),
                'exit_price': exit_price_native,
                'exit_reason': 'Manual Exit'
            })
        except Exception as e:
            # If columns don't exist, just update status
            if 'exit_date' in str(e) or 'UndefinedColumn' in str(e):
                print(f"   ⚠️  Exit columns don't exist in positions table, updating status only")
                print(f"   ⚠️  Run migration: add_exit_columns_to_positions.sql")
                updated_position = update_position(position_id, {
                    'status': 'closed'
                })
            else:
                raise
        
        if updated_position:
            print(f"   ✓ Position status updated to: {updated_position.get('status', 'unknown')}")
        else:
            print(f"   ⚠️  Warning: update_position returned None")
        
        # Update portfolio cash
        current_cash = float(portfolio['cash'])
        new_cash = current_cash + net_proceeds_gbp
        update_portfolio_cash(portfolio_id, new_cash)
        
        print(f"   ✓ Position closed")
        print(f"   New cash balance: £{new_cash:.2f}\n")
        
        return {
            "status": "ok",
            "data": {
                "ticker": position['ticker'],
                "exit_price": round(exit_price_native, 2),
                "shares": shares,
                "gross_proceeds": round(gross_proceeds_gbp, 2),
                "exit_fees": round(exit_fees_gbp, 2),
                "net_proceeds": round(net_proceeds_gbp, 2),
                "realized_pnl": round(realized_pnl_gbp, 2),
                "realized_pnl_pct": round(realized_pnl_pct, 2),
                "new_cash_balance": round(new_cash, 2)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


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
