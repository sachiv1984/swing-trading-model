from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
import yfinance as yf
from datetime import timedelta
import time

from database import (
    get_portfolio,
    update_portfolio_cash,
    get_positions,
    create_position,
    update_position,
    delete_position,
    get_trade_history,
    create_trade_history
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

# Request models
class AddPositionRequest(BaseModel):
    ticker: str
    entry_date: str
    shares: int
    fill_price: float
    fill_currency: str
    fx_rate: Optional[float] = None
    atr: float
    custom_stop: Optional[float] = None


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
    """Fetch current price from yfinance with improved error handling"""
    try:
        # Add a small delay to avoid rate limiting
        time.sleep(0.1)
        
        stock = yf.Ticker(ticker)
        
        # Method 1: Recent history (most reliable)
        hist = stock.history(period="5d")
        if not hist.empty and 'Close' in hist.columns:
            price = float(hist['Close'].iloc[-1])
            print(f"✓ {ticker}: ${price:.2f} (from history)")
            return price
        
        # Method 2: Info dict
        try:
            info = stock.info
            if 'currentPrice' in info and info['currentPrice']:
                price = float(info['currentPrice'])
                print(f"✓ {ticker}: ${price:.2f} (from currentPrice)")
                return price
            
            if 'regularMarketPrice' in info and info['regularMarketPrice']:
                price = float(info['regularMarketPrice'])
                print(f"✓ {ticker}: ${price:.2f} (from regularMarketPrice)")
                return price
        except:
            pass
        
        print(f"⚠️  {ticker}: No price found")
        return None
        
    except Exception as e:
        print(f"❌ {ticker}: Error - {str(e)}")
        return None


def check_market_regime():
    """Check SPY and FTSE for risk on/off"""
    try:
        spy = yf.Ticker("SPY")
        ftse = yf.Ticker("^FTSE")
        
        spy_hist = spy.history(period="1y")
        ftse_hist = ftse.history(period="1y")
        
        if spy_hist.empty or ftse_hist.empty:
            return {
                'spy_risk_on': True,
                'ftse_risk_on': True,
                'spy_price': 0,
                'spy_ma200': 0,
                'ftse_price': 0,
                'ftse_ma200': 0
            }
        
        spy_current = float(spy_hist['Close'].iloc[-1])
        spy_ma200 = float(spy_hist['Close'].rolling(200).mean().iloc[-1])
        
        ftse_current = float(ftse_hist['Close'].iloc[-1])
        ftse_ma200 = float(ftse_hist['Close'].rolling(200).mean().iloc[-1])
        
        return {
            'spy_risk_on': spy_current > spy_ma200,
            'ftse_risk_on': ftse_current > ftse_ma200,
            'spy_price': spy_current,
            'spy_ma200': spy_ma200,
            'ftse_price': ftse_current,
            'ftse_ma200': ftse_ma200
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


@app.get("/positions")
def get_positions_endpoint():
    """Get open positions in the format the frontend expects"""
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        positions = get_positions(portfolio_id, status='open')
        
        positions_list = []
        
        for pos in positions:
            pos = decimal_to_float(pos)
            current_price = pos.get('current_price', pos['entry_price'])
            current_value = current_price * pos['shares']
            pnl = pos.get('pnl', 0)
            pnl_pct = pos.get('pnl_pct', 0)
            
            # Calculate holding days correctly
            entry_date = datetime.strptime(str(pos['entry_date']), '%Y-%m-%d')
            holding_days = (datetime.now() - entry_date).days
            
            if holding_days < 10:
                display_status = "GRACE"
            elif pnl > 0:
                display_status = "PROFITABLE"
            else:
                display_status = "LOSING"
            
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
                "stop_price": round(pos.get('current_stop', 0), 2),  # Changed from current_stop
                "pnl": round(pnl, 2),
                "pnl_percent": round(pnl_pct, 2),  # Changed from pnl_pct
                "holding_days": holding_days,
                "status": "open",  # Frontend expects "open" for all open positions
                "display_status": display_status,  # Keep GRACE/PROFITABLE/LOSING as separate field
                "atr_value": pos.get('atr', 0),
                "fx_rate": pos.get('fx_rate', 1.0)
            })
        
        return positions_list
        
    except Exception as e:
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
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = str(portfolio['id'])
        
        # Calculate fees and costs
        is_uk = request.fill_currency == "GBP"
        
        # Auto-append .L for UK stocks
        ticker = request.ticker.upper().strip()
        if is_uk and not ticker.endswith('.L'):
            ticker = f"{ticker}.L"
            print(f"✓ Auto-appended .L to UK ticker: {ticker}")
        
        if is_uk:
            stamp_duty_rate = 0.005
            gross_cost = request.shares * request.fill_price
            fees_paid = gross_cost * stamp_duty_rate
            total_cost = gross_cost + fees_paid
            entry_price = total_cost / request.shares
            market = "UK"
        else:
            trading_fee_rate = 0.0015
            fx_rate = request.fx_rate or 1.28
            fill_price_gbp = request.fill_price / fx_rate
            gross_cost = request.shares * fill_price_gbp
            fees_paid = gross_cost * trading_fee_rate
            total_cost = gross_cost + fees_paid
            entry_price = total_cost / request.shares
            market = "US"
        
        # Calculate initial stop
        initial_stop = request.custom_stop if request.custom_stop else (entry_price - (5 * request.atr))
        
        # Create position with the modified ticker
        position_data = {
            'ticker': ticker,  # This now has .L for UK stocks
            'market': market,
            'entry_date': request.entry_date,
            'entry_price': round(entry_price, 4),
            'fill_price': request.fill_price,
            'fill_currency': request.fill_currency,
            'fx_rate': request.fx_rate,
            'shares': request.shares,
            'total_cost': round(total_cost, 2),
            'fees_paid': round(fees_paid, 2),
            'fee_type': 'stamp_duty' if is_uk else 'trading_fee',
            'initial_stop': round(initial_stop, 2),
            'current_stop': round(initial_stop, 2),
            'current_price': round(entry_price, 4),
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
                "fees_paid": round(fees_paid, 2),
                "entry_price": round(entry_price, 4),
                "initial_stop": round(initial_stop, 2),
                "remaining_cash": round(new_cash, 2)
            }
        }
    except Exception as e:
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
