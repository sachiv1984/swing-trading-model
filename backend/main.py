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
            
            if holding_days < 10:
                status = "GRACE"
            elif pnl > 0:
                status = "PROFITABLE"
            else:
                status = "LOSING"
            
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

    # 👇 NEW fields for frontend compatibility
    "stop_price": round(pos.get('current_stop', 0), 2),
    "pnl_percent": round(pnl_pct, 2),

    "current_stop": round(pos.get('current_stop', 0), 2),
    "holding_days": holding_days,
    "status": status
})
        
        cash = float(portfolio['cash'])
        total_value = cash + total_positions_value
        
        return {
            "status": "ok",
            "data": {
                "cash": cash,
                "cash_balance": cash,  # Add for compatibility
                "total_value": total_value,  # Add this
                "open_positions_value": total_positions_value,  # Add this
                "total_pnl": sum(p['pnl'] for p in positions_list),  # Add this
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

        # Market is sent from frontend
        is_uk = request.market == "UK"

        # Fees are sent from frontend
        fees_paid = round(request.fees or 0, 2)

        # Total cost based on entry price + fees
        total_cost = round((request.entry_price * request.shares) + fees_paid, 2)

        # Stop price from frontend
        initial_stop = request.stop_price if request.stop_price else None

        position_data = {
    "ticker": request.ticker,
    "market": request.market,
    "entry_date": request.entry_date,
    "entry_price": round(request.entry_price, 4),

    "shares": request.shares,
    "current_price": round(request.current_price or request.entry_price, 4),

    "fx_rate": request.fx_rate,
    "atr_value": request.atr_value,

    "stop_price": request.stop_price,
    "current_stop": request.stop_price,   # <-- Correctly set current stop

    "fees_paid": round(request.fees or 0, 2),

    # BONUS FIX: total_cost should be based on entry_price already provided by frontend
    "total_cost": round((request.fees or 0) + (request.entry_price * request.shares), 2),

    "fee_type": "manual",
    "status": request.status or "open",
    "holding_days": 0,
    "pnl": 0,
    "pnl_pct": 0
}

        new_position = create_position(portfolio_id, position_data)

        # Update cash
        new_cash = float(portfolio["cash"]) - total_cost
        update_portfolio_cash(portfolio_id, new_cash)

        return {
            "status": "ok",
            "data": {
                "ticker": request.ticker,
                "total_cost": total_cost,
                "fees_paid": fees_paid,
                "entry_price": round(request.entry_price, 4),
                "initial_stop": initial_stop,
                "remaining_cash": round(new_cash, 2),
            },
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
        
        # Format trades for response
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
