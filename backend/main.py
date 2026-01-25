from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json
import os

# Set up paths
BASE_DIR = os.path.dirname(__file__)
PORTFOLIO_FILE = os.path.join(BASE_DIR, "current_portfolio.json")

app = FastAPI(title="Trading Assistant API")

# CORS - allow your GitHub Pages site
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sachiv1984.github.io",
        "http://localhost:3000"  # for local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        # Create default portfolio
        default = {
            "cash": 20000.0,
            "positions": {},
            "trade_history": [],
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_portfolio(default)
        return default
    
    with open(PORTFOLIO_FILE, 'r') as f:
        return json.load(f)

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=2)

# Endpoints
@app.get("/")
def root():
    return {"status": "ok", "message": "Trading Assistant API v1.0"}

@app.get("/portfolio")
def get_portfolio():
    try:
        portfolio = load_portfolio()
        
        positions_list = []
        for ticker, pos in portfolio['positions'].items():
            current_price = pos.get('current_price', pos['entry_price'])
            current_value = current_price * pos['shares']
            pnl = pos.get('pnl', 0)
            pnl_pct = pos.get('pnl_pct', 0)
            holding_days = pos.get('holding_days', 0)
            
            # Determine status
            if holding_days < 10:
                status = "GRACE"
            elif pnl > 0:
                status = "PROFITABLE"
            else:
                status = "LOSING"
            
            positions_list.append({
                "ticker": ticker,
                "market": pos.get('market', 'UK' if ticker.endswith('.L') else 'US'),
                "entry_date": pos['entry_date'],
                "entry_price": round(pos['entry_price'], 2),
                "shares": pos['shares'],
                "current_price": round(current_price, 2),
                "current_value": round(current_value, 2),
                "pnl": round(pnl, 2),
                "pnl_pct": round(pnl_pct, 2),
                "current_stop": round(pos.get('current_stop', 0), 2),
                "holding_days": holding_days,
                "status": status
            })
        
        return {
            "status": "ok",
            "data": {
                "cash": round(portfolio['cash'], 2),
                "last_updated": portfolio.get('last_updated', ''),
                "positions": positions_list
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/trades")
def get_trades():
    try:
        portfolio = load_portfolio()
        trades = portfolio.get('trade_history', [])
        
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
        
        return {
            "status": "ok",
            "data": {
                "total_trades": len(trades),
                "win_rate": round(win_rate, 1),
                "total_pnl": round(total_pnl, 2),
                "trades": trades
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)