from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import (
    get_portfolio,
    update_portfolio_cash,
    get_positions,
    create_position,
    update_position,
    delete_position,
    get_trade_history,
    create_trade_history,
)

app = FastAPI(title="Trading Assistant API")


# -----------------------------------------------------------------------------
# CORS configuration
# -----------------------------------------------------------------------------
# Note: When listing origins, each entry must be separated by a comma.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sachiv1984.github.io",
        "https://trading-assistant-api-c0f9.onrender.com",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Request models
# -----------------------------------------------------------------------------
class AddPositionRequest(BaseModel):
    ticker: str
    entry_date: str
    shares: int
    fill_price: float
    fill_currency: str
    fx_rate: Optional[float] = None
    atr: float
    custom_stop: Optional[float] = None


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------
def decimal_to_float(value):
    """
    Recursively converts Decimal values to float to ensure objects are JSON serialisable.
    """
    if isinstance(value, dict):
        return {k: decimal_to_float(v) for k, v in value.items()}
    if isinstance(value, list):
        return [decimal_to_float(item) for item in value]
    if isinstance(value, Decimal):
        return float(value)
    return value


# -----------------------------------------------------------------------------
# API endpoints
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "Trading Assistant API v1.0"}


@app.get("/portfolio")
def get_portfolio_endpoint():
    """
    Returns the current portfolio summary, including open positions.
    """
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        portfolio_id = str(portfolio["id"])
        positions = get_positions(portfolio_id, status="open")

        positions_list = []
        for pos in positions:
            pos = decimal_to_float(pos)

            current_price = pos.get("current_price", pos["entry_price"])
            current_value = current_price * pos["shares"]

            pnl = pos.get("pnl", 0)
            pnl_pct = pos.get("pnl_pct", 0)
            holding_days = pos.get("holding_days", 0)

            if holding_days < 10:
                position_status = "GRACE"
            elif pnl > 0:
                position_status = "PROFITABLE"
            else:
                position_status = "LOSING"

            positions_list.append(
                {
                    "id": str(pos["id"]),
                    "ticker": pos["ticker"],
                    "market": pos["market"],
                    "entry_date": str(pos["entry_date"]),
                    "entry_price": round(pos["entry_price"], 2),
                    "shares": pos["shares"],
                    "current_price": round(current_price, 2),
                    "current_value": round(current_value, 2),
                    "pnl": round(pnl, 2),
                    "pnl_pct": round(pnl_pct, 2),
                    "current_stop": round(pos.get("current_stop", 0), 2),
                    "holding_days": holding_days,
                    "status": position_status,
                }
            )

        return {
            "status": "ok",
            "data": {
                "cash": float(portfolio["cash"]),
                "last_updated": str(portfolio["last_updated"]),
                "positions": positions_list,
            },
        }

    except Exception as exc:
        return {"status": "error", "message": str(exc)}


@app.post("/portfolio/position")
def add_position_endpoint(request: AddPositionRequest):
    """
    Creates a new position and updates the portfolio cash balance.
    """
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        portfolio_id = str(portfolio["id"])

        # Calculate fees and total entry cost.
        is_uk_trade = request.fill_currency == "GBP"

        if is_uk_trade:
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

        # Calculate the initial stop.
        initial_stop = (
            request.custom_stop if request.custom_stop else (entry_price - (5 * request.atr))
        )

        position_data = {
            "ticker": request.ticker,
            "market": market,
            "entry_date": request.entry_date,
            "entry_price": round(entry_price, 4),
            "fill_price": request.fill_price,
            "fill_currency": request.fill_currency,
            "fx_rate": request.fx_rate,
            "shares": request.shares,
            "total_cost": round(total_cost, 2),
            "fees_paid": round(fees_paid, 2),
            "fee_type": "stamp_duty" if is_uk_trade else "trading_fee",
            "initial_stop": round(initial_stop, 2),
            "current_stop": round(initial_stop, 2),
            "current_price": round(entry_price, 4),
            "holding_days": 0,
            "pnl": 0.0,
            "pnl_pct": 0.0,
            "status": "open",
        }

        create_position(portfolio_id, position_data)

        # Update portfolio cash.
        new_cash = float(portfolio["cash"]) - total_cost
        update_portfolio_cash(portfolio_id, new_cash)

        return {
            "status": "ok",
            "data": {
                "ticker": request.ticker,
                "total_cost": round(total_cost, 2),
                "fees_paid": round(fees_paid, 2),
                "entry_price": round(entry_price, 4),
                "initial_stop": round(initial_stop, 2),
                "remaining_cash": round(new_cash, 2),
            },
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/trades")
def get_trades_endpoint():
    """
    Returns trade history and headline performance metrics.
    """
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        portfolio_id = str(portfolio["id"])
        trades = get_trade_history(portfolio_id)
        trades = [decimal_to_float(t) for t in trades]

        if not trades:
            return {
                "status": "ok",
                "data": {"total_trades": 0, "win_rate": 0, "total_pnl": 0, "trades": []},
            }

        total_pnl = sum(t.get("pnl", 0) for t in trades)
        wins = len([t for t in trades if t.get("pnl", 0) > 0])
        win_rate = (wins / len(trades)) * 100

        formatted_trades = [
            {
                "ticker": t["ticker"],
                "entry_date": str(t["entry_date"]),
                "exit_date": str(t["exit_date"]),
                "pnl": round(t.get("pnl", 0), 2),
                "pnl_pct": round(t.get("pnl_pct", 0), 2),
                "exit_reason": t.get("exit_reason", "Unknown"),
            }
            for t in trades
        ]

        return {
            "status": "ok",
            "data": {
                "total_trades": len(trades),
                "win_rate": round(win_rate, 1),
                "total_pnl": round(total_pnl, 2),
                "trades": formatted_trades,
            },
        }

    except Exception as exc:
        return {"status": "error", "message": str(exc)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
