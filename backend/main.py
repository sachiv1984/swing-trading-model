from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from datetime import timedelta
import time
import os
import requests
from config import API_TITLE
from config import ALLOWED_ORIGINS
from utils.calculations import calculate_initial_stop
from utils.formatting import decimal_to_float
from pydantic import BaseModel
from routers import validation, analytics, test, portfolio_size, trades_export, prospective_heat, alerts
from routers import watchlist as watchlist_router
from routers import digest as digest_router
from routers import ai as ai_router
from routers import news as news_router
from routers import ticker_universe as ticker_universe_router
from routers import screener as screener_router
from routers import trade_plans as trade_plans_router
from routers import earnings as earnings_router
from routers import research as research_router
from services.watchlist_service import ensure_watchlist_table
from services.ai_audit_service import ensure_ai_audit_table
from services.ticker_universe_service import ensure_ticker_universe_table, seed_default_tickers, sync_from_tickers_table
from services.screener_batch_service import ensure_screener_results_table



from database import (
    get_portfolio,
    get_positions,
    update_position,
    create_position,
    update_portfolio_cash,
    get_settings,
    create_settings,
    update_settings,
    create_trade_history,
    update_position_note,
    update_position_tags,
    get_all_tags,
    search_positions_by_tags
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

from services.alerts_service import ensure_alerts_tables
from services.compliance_service import get_position_compliance
from services.position_lifecycle_service import (
    get_lifecycle_fields_for_position,
    refresh_position_lifecycle,
    compute_days_in_state,
)
from database import get_position_by_id

from services import (
    # Position service
    get_positions_with_prices,
    analyze_positions,
    add_position,
    exit_position,
    update_note,
    update_tags,
    get_available_tags,
    filter_by_tags,
    # Portfolio service
    get_portfolio_summary,
    create_daily_snapshot,
    get_performance_history,
    # Trade service
    get_trade_history_with_stats,
    get_reflection,
    save_reflection,
    # Cash service
    create_transaction,
    get_transaction_history,
    get_cash_summary,
    # Signal service
    generate_momentum_signals,
    get_signals,
    update_signal_status,
    delete_signal,
    # Health service
    get_basic_health,
    get_detailed_health,
    get_operational_health,
    record_market_status_check,
    test_all_endpoints,
    get_db_size_info,
    send_db_size_alert_if_needed,
    # Reports service
    get_tax_year_report,
    build_tax_year_pdf,
    build_tax_year_csv,
    get_monthly_pnl_report,
)
app = FastAPI(title=API_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    api_key = os.environ.get("API_KEY")
    if not api_key:
        # API_KEY not set — skip auth (local dev)
        return await call_next(request)
    # Exempt OPTIONS (CORS preflight) and GET /health
    if request.method == "OPTIONS":
        return await call_next(request)
    if request.method == "GET" and request.url.path == "/health":
        return await call_next(request)
    # Validate X-API-Key header
    provided_key = request.headers.get("X-API-Key")
    if not provided_key or provided_key != api_key:
        return JSONResponse(
            status_code=401,
            content={"status": "error", "message": "Unauthorized"},
        )
    return await call_next(request)


app.include_router(validation.router)
app.include_router(analytics.router)
app.include_router(test.router)
app.include_router(portfolio_size.router)
app.include_router(prospective_heat.router)
app.include_router(trades_export.router)
app.include_router(alerts.router)
app.include_router(watchlist_router.router)
app.include_router(digest_router.router)
app.include_router(ai_router.router)
app.include_router(news_router.router)
app.include_router(ticker_universe_router.router)
app.include_router(screener_router.router)
app.include_router(trade_plans_router.router)
app.include_router(earnings_router.router)
app.include_router(research_router.router)


@app.on_event("startup")
def on_startup():
    """Bootstrap tables after the ASGI app is ready (idempotent CREATE IF NOT EXISTS)."""
    import logging as _logging
    _log = _logging.getLogger(__name__)
    try:
        ensure_alerts_tables()
        _log.info("ensure_alerts_tables: OK")
    except Exception as _e:
        _log.error("ensure_alerts_tables FAILED at startup — alert endpoints will return 500 until fixed: %s", _e)
    try:
        ensure_watchlist_table()
        _log.info("ensure_watchlist_table: OK")
    except Exception as _e:
        _log.error("ensure_watchlist_table FAILED at startup: %s", _e)
    try:
        ensure_ai_audit_table()
        _log.info("ensure_ai_audit_table: OK")
    except Exception as _e:
        _log.error("ensure_ai_audit_table FAILED at startup: %s", _e)
    try:
        ensure_ticker_universe_table()
        seeded = seed_default_tickers()
        _log.info("ensure_ticker_universe_table: OK (seeded %d default tickers)", seeded)
    except Exception as _e:
        _log.error("ensure_ticker_universe_table FAILED at startup: %s", _e)
    try:
        synced = sync_from_tickers_table()
        _log.info("sync_from_tickers_table: OK (%d tickers synced from public.tickers)", synced)
    except Exception as _e:
        _log.warning("sync_from_tickers_table skipped (public.tickers may not exist): %s", _e)
    try:
        ensure_screener_results_table()
        _log.info("ensure_screener_results_table: OK")
    except Exception as _e:
        _log.error("ensure_screener_results_table FAILED at startup: %s", _e)
    try:
        from utils.feature_flags import log_flag_states
        log_flag_states()
    except Exception as _e:
        _log.warning("feature_flags startup log failed: %s", _e)


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
    """Get open positions with live prices and lifecycle state."""
    try:
        positions = get_positions_with_prices()
        for pos in positions:
            lifecycle = get_lifecycle_fields_for_position(pos)
            pos.update(lifecycle)
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
    result = exit_position(
        position_id=position_id,
        exit_price=request.exit_price,
        shares=request.shares,
        exit_date=request.exit_date,
        exit_reason=request.exit_reason,
        exit_fx_rate=request.exit_fx_rate,
        exit_note=request.exit_note  # ✅ NEW
    )
    return {"status": "ok", "data": result}

@app.post("/portfolio/position")
def add_position_endpoint(request: AddPositionRequest):
    """Add a new position to the portfolio"""
    try:
        result = add_position(
            ticker=request.ticker,
            market=request.market,
            entry_date=request.entry_date,
            shares=request.shares,
            entry_price=request.entry_price,
            fill_price=request.fill_price,
            fx_rate=request.fx_rate,
            atr_value=request.atr_value,
            stop_price=request.stop_price,
            entry_note=request.entry_note,
            tags=request.tags
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


# ---------------------------------------------------------------------------
# Reports endpoints — ST-04, EPIC-02, v2.0 / ST-12 PDF export, EPIC-05, v2.1
# Spec: docs/specs/api_contracts/reports_endpoints.md v0.3
# ---------------------------------------------------------------------------

@app.get("/reports/tax-year")
def get_tax_year_report_endpoint(year: Optional[int] = None, format: Optional[str] = None):
    """
    GET /reports/tax-year?year=YYYY[&format=pdf|csv]

    Returns a UK tax-year P&L statement for all closed trades whose
    exit_date falls within the specified tax year (6 April to 5 April).
    When format=pdf, returns a PDF file download instead of JSON.
    When format=csv, returns a CSV file download instead of JSON.
    Spec: reports_endpoints.md v0.3
    """
    from fastapi.responses import JSONResponse, Response
    if year is None:
        return JSONResponse(status_code=400,
            content={"status": "error", "message": "year parameter is required"})
    if year < 1000 or year > 9999:
        return JSONResponse(status_code=400,
            content={"status": "error", "message": "year must be a valid four-digit integer"})
    if format is not None and format not in ("pdf", "csv"):
        return JSONResponse(status_code=400,
            content={"status": "error", "message": "format must be one of: pdf, csv"})
    try:
        data = get_tax_year_report(year)
        if format == "pdf":
            pdf_bytes = build_tax_year_pdf(data)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'attachment; filename="tax-year-{year}-pnl.pdf"'
                },
            )
        if format == "csv":
            csv_text = build_tax_year_csv(data)
            return Response(
                content=csv_text.encode("utf-8"),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f'attachment; filename="tax-year-{year}-pnl.csv"'
                },
            )
        return {"status": "ok", "data": data}
    except ValueError as e:
        msg = str(e)
        if "not started yet" in msg:
            return JSONResponse(status_code=400,
                content={"status": "error", "message": "tax year has not started yet"})
        return JSONResponse(status_code=404,
            content={"status": "error", "message": msg})
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/reports/monthly-pnl")
def get_monthly_pnl_endpoint():
    """
    GET /reports/monthly-pnl

    Returns month-by-month realised P&L for the current and prior calendar year.
    Response is an array sorted descending by year then month.
    Spec: reports_endpoints.md §GET /reports/monthly-pnl (v3.1)
    """
    try:
        data = get_monthly_pnl_report()
        return {"status": "ok", "data": data}
    except Exception as e:
        return JSONResponse(status_code=500,
            content={"status": "error", "message": str(e)})


# ---------------------------------------------------------------------------
# Trade reflection endpoints — ST-02, EPIC-01, v1.9
# Spec: docs/specs/frontend/pages/trade_reflection.md §7
# Data model: docs/specs/data_model.md §v1.8
# ---------------------------------------------------------------------------

class ReflectionRequest(BaseModel):
    trade_rationale: Optional[str] = None
    what_worked: Optional[str] = None
    what_didnt_work: Optional[str] = None
    discipline_assessment: Optional[str] = None
    key_takeaway: Optional[str] = None


@app.get("/trades/{trade_id}/reflection")
def get_trade_reflection_endpoint(trade_id: str):
    """
    GET /trades/{trade_id}/reflection

    Retrieve the saved reflection for a closed trade.
    Returns 404 if no reflection has been saved yet.
    Spec: trade_reflection.md §7
    """
    try:
        reflection = get_reflection(trade_id)
        if reflection is None:
            raise HTTPException(status_code=404, detail="No reflection found for this trade")
        return {"status": "ok", "data": reflection}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trades/{trade_id}/reflection")
def save_trade_reflection_endpoint(trade_id: str, request: ReflectionRequest):
    """
    POST /trades/{trade_id}/reflection

    Create or update (upsert) the reflection for a closed trade.
    All five fields are optional — any subset (including all null) is valid.
    Returns 404 if trade_id does not exist in trade_history.
    Spec: trade_reflection.md §7
    """
    try:
        data = request.model_dump()
        reflection = save_reflection(trade_id, data)
        return {"status": "ok", "data": reflection}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


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
        record_market_status_check()

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
        updated = update_signal_status(signal_id, updates)
        return {
            "status": "ok",
            "data": updated
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/signals/{signal_id}")
def delete_signal_endpoint(signal_id: str):
    """Delete a signal"""
    try:
        delete_signal(signal_id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """
    Operational health check (v2.2).

    Returns DB connectivity, and timestamps of last market status check
    and last alert evaluation. Schema per ST-08 / health_endpoints.md.
    """
    try:
        return get_operational_health()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "db": "error", "last_market_status_check": None, "last_alert_evaluation": None}


@app.get("/health/detailed")
def detailed_health_check():
    """
    Comprehensive system status check
    
    Checks:
    - Database connectivity
    - External services (Yahoo Finance)
    - Service layer health
    - Configuration validity
    """
    try:
        result = get_detailed_health()
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

@app.get("/health/database")
def database_size_check():
    """
    Database size monitoring endpoint (BLG-OPS-09).

    Returns current database size, percentage of Render free tier limit used,
    and configured alert threshold. Triggers a Telegram notification if usage
    is at or above the threshold (notification-only — no automated cleanup).

    Contract: docs/specs/api_contracts/health_endpoints.md v1.2
    """
    try:
        info = get_db_size_info()
        send_db_size_alert_if_needed(info)
        return info
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@app.post("/test/endpoints")
def test_endpoints(request: Request):
    """
    Test all API endpoints
    
    Returns:
        Test results for all endpoints
    
    Note:
        - Can take 10-30 seconds to complete
        - Tests all GET endpoints
        - Returns pass/fail status and response times
    """
    try:
        # Get the base URL from the request
        # This works for both localhost and production
        base_url = str(request.base_url).rstrip('/')
        
        # Pass the actual server URL to the test function
        result = test_all_endpoints(base_url)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

class UpdateNoteRequest(BaseModel):
    entry_note: str

class UpdateTagsRequest(BaseModel):
    tags: List[str]

@app.patch("/positions/{position_id}/note")
def update_position_note_endpoint(position_id: str, request: UpdateNoteRequest):
    """Update entry note for a position"""
    try:
        result = update_note(position_id, request.entry_note)  # ✅ Direct call
        return {"status": "ok", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

def get_portfolio_id() -> str:
    """Helper to get portfolio ID"""
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    return str(portfolio['id'])

@app.patch("/positions/{position_id}/tags")
def update_position_tags_endpoint(position_id: str, request: UpdateTagsRequest):
    """
    Update tags for a position.
    
    Tags help categorize trades by strategy, setup type, or other criteria.
    Examples: ["momentum", "breakout", "earnings-play"]
    """
    try:
        result = update_tags(position_id, request.tags)
        return {"status": "ok", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/positions/compliance")
def get_positions_compliance_endpoint():
    """
    GET /positions/compliance

    Returns ATR-based strategy compliance flags for all open positions.

    Per-position fields:
      - stop_compliant: bool | null — stop within 2.5× ATR of entry; null in grace period
      - stop_age_days: int | null — approximate days since stop was set; null in grace period
      - size_compliant: bool | null — risk amount within strategy limit; null if no snapshot

    Scope constraint §13.3: Display-only. No automated action generated.
    Spec: docs/specs/api_contracts/position_endpoints.md §GET /positions/compliance
    """
    try:
        result = get_position_compliance()
        return {"status": "ok", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/positions/tags")
def get_available_tags_endpoint():
    """
    Get all unique tags used across positions and trade history.
    
    Used for tag autocomplete and filtering.
    """
    try:
        portfolio_id = get_portfolio_id()  # Your existing helper
        tags = get_available_tags(portfolio_id)
        return {"status": "ok", "data": tags}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/positions/search/tags")
def search_positions_by_tags_endpoint(tags: str):
    """
    Search positions by tags.
    
    Query params:
        tags: Comma-separated list of tags (e.g., "momentum,breakout")
    
    Returns positions that match ANY of the provided tags.
    """
    try:
        portfolio_id = get_portfolio_id()
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        
        if not tag_list:
            raise ValueError("At least one tag is required")
        
        positions = filter_by_tags(portfolio_id, tag_list)
        return {"status": "ok", "data": positions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/positions/grace-period-alerts")
def get_grace_period_alerts_endpoint():
    """
    GET /positions/grace-period-alerts

    Returns positions in GRACE lifecycle state where days_in_state >= 8 (nearing end of grace
    period). Includes linked trade plan summary if available.

    Response fields per alert:
      - position_id, ticker, days_in_state
      - trade_plan_id (null if no linked plan)
      - trade_plan_summary: {setup_thesis excerpt, entry_rationale, stop_level, r_target} or null

    §13 display-only: system surfaces contextual information; human decides next action.
    Spec: docs/specs/api_contracts/grace_period_alert_endpoint.md
    """
    from datetime import datetime, timezone
    from database import get_db

    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise ValueError("Portfolio not found")
        portfolio_id = str(portfolio["id"])

        # Fetch open positions with lifecycle state columns (available post EPIC-01 migration)
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT p.id, p.ticker, p.market, p.position_state, p.state_entered_at,
                           p.entry_date, p.entry_price, p.atr, p.initial_stop,
                           tp.id AS trade_plan_id,
                           tp.setup_thesis, tp.entry_rationale, tp.stop_level, tp.r_target
                    FROM positions p
                    LEFT JOIN trade_plans tp ON tp.position_id = p.id
                    WHERE p.portfolio_id = %s AND p.status = 'open'
                      AND p.position_state = 'GRACE'
                    ORDER BY p.entry_date ASC
                    """,
                    (portfolio_id,),
                )
                rows = cur.fetchall()

        alerts = []
        for row in rows:
            state_entered_at = row.get("state_entered_at")
            if state_entered_at:
                if hasattr(state_entered_at, "tzinfo") and state_entered_at.tzinfo is None:
                    state_entered_at = state_entered_at.replace(tzinfo=timezone.utc)
                days_in_state = (datetime.now(timezone.utc) - state_entered_at).days
            else:
                # Fallback: count trading days from entry_date as days_in_state approximation
                from datetime import date
                entry = row.get("entry_date")
                if entry:
                    entry_d = date.fromisoformat(str(entry).split("T")[0].split(" ")[0]) if isinstance(entry, str) else entry
                    today = date.today()
                    count = 0
                    current = entry_d
                    while current < today:
                        current = date.fromordinal(current.toordinal() + 1)
                        if current.weekday() < 5:
                            count += 1
                    days_in_state = count
                else:
                    days_in_state = 0

            if days_in_state < 8:
                continue

            trade_plan_summary = None
            if row.get("trade_plan_id"):
                setup_thesis = row.get("setup_thesis") or ""
                trade_plan_summary = {
                    "setup_thesis": setup_thesis[:200] if setup_thesis else None,
                    "entry_rationale": row.get("entry_rationale"),
                    "stop_level": row.get("stop_level"),
                    "r_target": row.get("r_target"),
                }

            ticker = str(row.get("ticker") or "")
            if row.get("market") == "UK":
                ticker = ticker.replace(".L", "")

            alerts.append({
                "position_id": str(row["id"]),
                "ticker": ticker,
                "market": row.get("market"),
                "days_in_state": days_in_state,
                "trade_plan_id": str(row["trade_plan_id"]) if row.get("trade_plan_id") else None,
                "trade_plan_summary": trade_plan_summary,
            })

        return {"status": "ok", "data": alerts}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/positions/{position_id}")
def get_position_by_id_endpoint(position_id: str):
    """Get a single position by ID with live prices and lifecycle state."""
    from utils.formatting import decimal_to_float
    from utils.calculations import calculate_holding_days
    from utils.pricing import get_current_price, get_live_fx_rate
    from services.grace_service import compute_grace_days_remaining
    from services.sector_service import get_sector_and_industry
    from utils.calculations import calculate_position_pnl

    try:
        raw = get_position_by_id(position_id)
        if not raw:
            raise HTTPException(status_code=404, detail="Position not found")
        pos = decimal_to_float(dict(raw))
        if pos.get("status") != "open":
            lifecycle = get_lifecycle_fields_for_position(pos)
            pos.update(lifecycle)
            return pos

        live_fx_rate = get_live_fx_rate()
        live_price = get_current_price(pos["ticker"])
        if live_price:
            if pos["market"] == "UK" and live_price > 1000:
                live_price = live_price / 100
            current_price_native = live_price
        else:
            current_price_native = pos.get("current_price") or pos["entry_price"]

        if pos["market"] == "US":
            entry_price_display = pos.get("fill_price") or pos["entry_price"] * pos.get("fx_rate", 1.27)
            current_price_gbp = current_price_native / live_fx_rate
        else:
            entry_price_display = pos["entry_price"]
            current_price_gbp = current_price_native

        pnl_native, pnl_gbp, pnl_pct = calculate_position_pnl(
            entry_price=entry_price_display,
            current_price=current_price_native,
            shares=pos["shares"],
            market=pos["market"],
            live_fx_rate=live_fx_rate,
        )
        holding_days = calculate_holding_days(str(pos["entry_date"]))
        grace_period = holding_days < 10
        grace_days_remaining = compute_grace_days_remaining(
            grace_period=grace_period, holding_days=holding_days
        )
        stop_price_native = 0 if grace_period else (pos.get("current_stop") or pos.get("initial_stop") or 0)
        stop_price_gbp = stop_price_native / live_fx_rate if pos["market"] == "US" and stop_price_native else stop_price_native
        sector, industry = get_sector_and_industry(pos["ticker"], pos["market"])
        display_ticker = pos["ticker"].replace(".L", "") if pos["market"] == "UK" else pos["ticker"]

        result = {
            "id": str(pos["id"]),
            "ticker": display_ticker,
            "market": pos["market"],
            "initial_stop": round(pos["initial_stop"], 2) if pos.get("initial_stop") else None,
            "entry_date": str(pos["entry_date"]),
            "entry_price": round(entry_price_display, 2),
            "shares": pos["shares"],
            "current_price": round(current_price_gbp, 2),
            "current_price_native": round(current_price_native, 2),
            "stop_price": round(stop_price_gbp, 2),
            "stop_price_native": round(stop_price_native, 2),
            "pnl": round(pnl_gbp, 2),
            "pnl_percent": round(pnl_pct, 2),
            "holding_days": holding_days,
            "status": "open",
            "grace_period": grace_period,
            "grace_days_remaining": grace_days_remaining,
            "atr_value": pos.get("atr", 0),
            "fx_rate": pos.get("fx_rate", 1.0),
            "live_fx_rate": live_fx_rate,
            "total_cost": round(pos.get("total_cost", 0), 2),
            "entry_note": pos.get("entry_note"),
            "exit_note": pos.get("exit_note"),
            "tags": pos.get("tags", []),
            "sector": sector,
            "industry": industry,
        }
        lifecycle = get_lifecycle_fields_for_position({**pos, "current_price_native": current_price_native})
        result.update(lifecycle)
        return result
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/positions/{position_id}/refresh-state")
def refresh_position_state_endpoint(position_id: str):
    """Explicitly refresh lifecycle state for a position."""
    from utils.formatting import decimal_to_float

    try:
        raw = get_position_by_id(position_id)
        if not raw:
            raise HTTPException(status_code=404, detail="Position not found")
        updated = refresh_position_lifecycle(position_id)
        if not updated:
            raise HTTPException(status_code=404, detail="Position not found")
        updated = decimal_to_float(dict(updated))
        state_entered_at = updated.get("state_entered_at")
        return {
            "status": "ok",
            "data": {
                "position_id": position_id,
                "position_state": updated.get("position_state"),
                "state_entered_at": state_entered_at.isoformat() if hasattr(state_entered_at, "isoformat") else str(state_entered_at) if state_entered_at else None,
                "days_in_state": compute_days_in_state(state_entered_at),
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/positions/{position_id}/stop-trail")
def get_stop_trail_endpoint(position_id: str):
    """
    GET /positions/{position_id}/stop-trail

    Returns ATR-based trail stop recommendation for a position.

    Response fields:
      - current_stop: current stop price from position record (null if not set)
      - atr_trail_stop: current_price - (ATR × 2.0)
      - trail_difference: atr_trail_stop - current_stop (null if current_stop null)
      - trail_r_terms: trail_difference expressed as R-multiples (null if R unavailable)
      - recommendation: display string "Raise stop to {atr_trail_stop}" (§13 display-only)

    §13 display-only: recommendation is informational; human must confirm any stop change.
    Spec: docs/specs/api_contracts/stop_trail_endpoint.md
    """
    from database import get_db

    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise ValueError("Portfolio not found")
        portfolio_id = str(portfolio["id"])

        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT p.id, p.ticker, p.market, p.entry_price, p.initial_stop,
                           p.current_stop, p.atr,
                           tp.id AS trade_plan_id, tp.r_target
                    FROM positions p
                    LEFT JOIN trade_plans tp ON tp.position_id = p.id
                    WHERE p.id = %s AND p.portfolio_id = %s AND p.status = 'open'
                    """,
                    (position_id, portfolio_id),
                )
                row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail=f"Position {position_id} not found")

        ticker = str(row.get("ticker") or "")
        if row.get("market") == "UK":
            ticker = ticker.replace(".L", "")

        current_price = get_current_price(ticker if row.get("market") == "US" else row.get("ticker"))
        if current_price is None:
            raise HTTPException(status_code=503, detail="Live price unavailable")
        if row.get("market") == "UK" and current_price > 1000:
            current_price = current_price / 100

        atr = float(row.get("atr") or 0)
        if atr <= 0:
            raise HTTPException(status_code=422, detail="ATR not available for this position")

        trail_multiplier = 2.0
        atr_trail_stop = round(current_price - (atr * trail_multiplier), 4)

        current_stop = row.get("current_stop")
        if current_stop is not None:
            current_stop = float(current_stop)

        trail_difference = None
        if current_stop is not None:
            trail_difference = round(atr_trail_stop - current_stop, 4)

        # Express trail_difference in R-multiples if R is available
        trail_r_terms = None
        entry_price = float(row.get("entry_price") or 0)
        initial_stop = row.get("initial_stop")
        if initial_stop is not None and entry_price > 0 and trail_difference is not None:
            r_value = entry_price - float(initial_stop)
            if r_value > 0:
                trail_r_terms = round(trail_difference / r_value, 2)

        recommendation = f"Raise stop to {atr_trail_stop:.4f}" if (
            trail_difference is not None and trail_difference > 0
        ) else (
            "Trail stop is below current stop — no action required"
        )

        return {
            "status": "ok",
            "data": {
                "position_id": position_id,
                "ticker": ticker,
                "current_price": round(current_price, 4),
                "current_stop": current_stop,
                "atr_trail_stop": atr_trail_stop,
                "trail_difference": trail_difference,
                "trail_r_terms": trail_r_terms,
                "recommendation": recommendation,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
