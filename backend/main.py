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
from utils.formatting import decimal_to_float

from database import (
    get_portfolio,
    delete_position,
    get_trade_history,
    get_settings,
    create_settings,
    update_settings,
    create_cash_transaction,
    get_cash_transactions,
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

from services import (
    # Position service
    get_positions_with_prices,
    analyze_positions,
    add_position as add_position_service,
    exit_position as exit_position_service,
    # Portfolio service
    get_portfolio_summary,
    create_daily_snapshot,
    get_performance_history,
    # Trade service
    get_trade_history_with_stats,
    # Cash service
    create_transaction,
    get_transaction_history,
    get_cash_summary,
    # Signal service
    generate_momentum_signals,
    get_signals,
    update_signal_status,
    delete_signal
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
    """Get open positions with live prices"""
    try:
        positions = get_positions_with_prices()
        return positions
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/portfolio")
def get_portfolio_endpoint():
    """Returns portfolio with live prices"""
    try:
        portfolio_data = get_portfolio_summary()
        return {
            "status": "ok",
            "data": portfolio_data
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.post("/positions/{position_id}/exit")
def exit_position_endpoint(position_id: str, request: ExitPositionRequest):
    """Exit a position (full or partial) and record in trade history"""
    try:
        result = exit_position_service(
            position_id=position_id,
            exit_price=request.exit_price,
            shares=request.shares,
            exit_date=request.exit_date,
            exit_reason=request.exit_reason,
            exit_fx_rate=request.exit_fx_rate
        )
        
        return {
            "status": "ok",
            "data": result
        }
    except ValueError as e:
        # ValueError from service = business logic error (400)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/portfolio/position")
def add_position_endpoint(request: AddPositionRequest):
    """Add a new position to the portfolio"""
    try:
        result = add_position_service(
            ticker=request.ticker,
            market=request.market,
            entry_date=request.entry_date,
            shares=request.shares,
            entry_price=request.entry_price,
            fx_rate=request.fx_rate,
            atr_value=request.atr_value,
            stop_price=request.stop_price
        )
        
        return {
            "status": "ok",
            "data": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/positions/analyze")
def analyze_positions_endpoint():
    """Run daily position analysis with live prices and market regime"""
    try:
        result = analyze_positions()
        return {
            "status": "ok",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"\n❌ ANALYSIS FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.post("/portfolio/snapshot")
def create_snapshot_endpoint():
    """Create a daily snapshot of portfolio performance"""
    try:
        snapshot = create_daily_snapshot()
        return {
            "status": "ok",
            "data": snapshot
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/portfolio/history")
def get_history_endpoint(days: int = 30):
    """Get portfolio performance history for the last N days"""
    try:
        history = get_performance_history(days)
        return {
            "status": "ok",
            "data": history
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.post("/cash/transaction")
def create_cash_transaction_endpoint(request: CashTransactionRequest):
    """Create a cash transaction (deposit or withdrawal)"""
    try:
        result = create_transaction(
            transaction_type=request.type,
            amount=request.amount,
            date=request.date,
            note=request.note
        )
        
        return {
            "status": "ok",
            "data": result
        }
    except ValueError as e:
        # ValueError from service = business logic error (400)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cash/transactions")
def get_cash_transactions_endpoint(order: str = "DESC"):
    """Get all cash transactions"""
    try:
        transactions = get_transaction_history(order)
        return {
            "status": "ok",
            "data": transactions
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.get("/cash/summary")
def get_cash_summary_endpoint():
    """Get summary of all deposits and withdrawals"""
    try:
        summary = get_cash_summary()
        return {
            "status": "ok",
            "data": summary
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
        
@app.get("/trades")
def get_trades_endpoint():
    """Get trade history with statistics"""
    try:
        trade_data = get_trade_history_with_stats()
        return {
            "status": "ok",
            "data": trade_data
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/signals/generate")
def generate_signals_endpoint(
    lookback_days: int = 252,
    top_n: int = 5
):
    """Generate momentum signals"""
    try:
        result = generate_momentum_signals(
            lookback_days=lookback_days,
            top_n=top_n,
            ma_period=200,
            atr_period=14,
            volatility_window=60,
            min_position_pct=0.05,
            max_position_pct=0.20
        )
        
        return {
            "status": "ok",
            "data": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
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
        signals = get_signals(status)
        return signals
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
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
