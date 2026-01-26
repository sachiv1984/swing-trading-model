from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

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
    market: str
    entry_date: str
    shares: float
    entry_price: float

    current_price: Optional[float] = None
    fx_rate: Optional[float] = None
    atr_value: Optional[float] = None

    stop_price: Optional[float] = None
    fees: Optional[float] = None

    status: Optional[str] = "open"


# Helper to convert Decimal to float
def decimal_to_float(obj):
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

@app.get("/")
def root():
    return {"status": "ok", "message": "Trading Assistant API v1.0"}

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
            
            # 👇 IMPORTANT FIX:
            # Do NOT change the DB status.
            # Use display_status only for UI display.
            display_status = "GRACE" if holding_days < 10 else ("PROFITABLE" if pnl > 0 else "LOSING")
            
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

                # Keep DB status
                "status": pos.get("status", "open"),

                # UI status only
                "display_status": display_status
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
        is_uk = request.market == "UK"
        
        if is_uk:
            stamp_duty_rate = 0.005
            gross_cost = request.shares * request.entry_price
            fees_paid = gross_cost * stamp_duty_rate
            total_cost = gross_cost + fees_paid
            entry_price = total_cost / request.shares
        else:
            trading_fee_rate = 0.0015
            fx_rate = request.fx_rate or 1.28
            fill_price_gbp = request.entry_price / fx_rate
            gross_cost = request.shares * fill_price_gbp
            fees_paid = gross_cost * trading_fee_rate
            total_cost = gross_cost + fees_paid
            entry_price = total_cost / request.shares
        
        # Calculate initial stop
        initial_stop = request.stop_price if request.stop_price else entry_price - (5 * (request.atr_value or 0))
        
        # Create position
        position_data = {
            'ticker': request.ticker,
            'market': request.market,
            'entry_date': request.entry_date,
            'entry_price': round(entry_price, 4),

            'shares': request.shares,
            'current_price': round(request.current_price or entry_price, 4),

            'fx_rate': request.fx_rate,
            'atr_value': request.atr_value,
            'stop_price': request.stop_price,

            'fees_paid': round(fees_paid or 0, 2),
            'total_cost': round(total_cost, 2),
            'fee_type': 'manual',

            'status': request.status or 'open',
            'holding_days': 0,
            'pnl': 0,
            'pnl_pct': 0
        }
        
        new_position = create_position(portfolio_id, position_data)
        
        # Update cash
        new_cash = float(portfolio['cash']) - total_cost
        update_portfolio_cash(portfolio_id, new_cash)
        
        return {
            "status": "ok",
            "data": {
                "ticker": request.ticker,
                "total_cost": round(total_cost, 2),
                "fees_paid": round(fees_paid, 2),
                "entry_price": round(entry_price, 4),
                "initial_stop": round(initial_stop, 2),
                "remaining_cash": round(new_cash, 2)
            }
        }
    except Exception as e:
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
