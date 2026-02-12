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
