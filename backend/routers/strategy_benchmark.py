"""
Strategy Benchmark router — compare live trades against backtest results.

ST-11 (BLG-FEAT-53, EPIC-03, v6.3)

Endpoints:
  POST /strategy/benchmark/import   — upsert backtest data from production_strategy.py CSVs
  GET  /strategy/benchmark/summary  — Panel 1 stats + Panel 2 yearly breakdown
  GET  /strategy/benchmark/trades   — Panel 3 trade log (backtest + live)
"""

from fastapi import APIRouter, Request, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import database

router = APIRouter()


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class BacktestTradeRecord(BaseModel):
    ticker: str
    entry_date: str
    exit_date: str
    holding_days: Optional[int] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    pnl_gbp: Optional[float] = None
    pnl_pct: Optional[float] = None
    market: str = "US"
    exit_reason: Optional[str] = None
    was_profitable: Optional[bool] = None
    entry_year: int


class BacktestYearlyRecord(BaseModel):
    entry_year: int
    num_trades: Optional[int] = None
    avg_pnl_gbp: Optional[float] = None
    total_pnl_gbp: Optional[float] = None
    avg_hold_days: Optional[float] = None
    win_rate_pct: Optional[float] = None


class BacktestImportRequest(BaseModel):
    trades: List[BacktestTradeRecord]
    yearly_performance: List[BacktestYearlyRecord]


# ---------------------------------------------------------------------------
# POST /strategy/benchmark/import
# ---------------------------------------------------------------------------

@router.post("/strategy/benchmark/import")
async def import_backtest(request: Request, body: BacktestImportRequest):
    """Upsert backtest trade records and yearly performance data.

    Called by import_backtest.py after parsing production_strategy.py CSV outputs.
    Returns the count of records imported and the import timestamp.
    """
    database.ensure_backtest_tables()
    result = database.upsert_backtest_data(
        trades=[t.dict() for t in body.trades],
        yearly_performance=[y.dict() for y in body.yearly_performance],
    )
    return {
        "status": "ok",
        "trades_imported": result["trades_imported"],
        "years_imported": result["years_imported"],
        "imported_at": result["imported_at"],
    }


# ---------------------------------------------------------------------------
# GET /strategy/benchmark/summary
# ---------------------------------------------------------------------------

@router.get("/strategy/benchmark/summary")
async def get_benchmark_summary(
    request: Request,
    year: Optional[int] = Query(None, description="Filter to a specific entry year; omit for all years"),
    market: Optional[str] = Query(None, description="Filter by market (US, UK, ALL); omit for all"),
):
    """Return Panel 1 stats and Panel 2 yearly breakdown for the Strategy Benchmark page.

    backtest_stats: aggregated stats from imported backtest data.
    actual_stats: aggregated stats from live trade_history (null if no matching trades — frontend shows '—').
    yearly_breakdown: per-year rows for Panel 2 table.
    available_years: distinct years present in backtest data (for year filter dropdown).
    last_imported_at: timestamp of most recent import run.
    """
    database.ensure_backtest_tables()

    portfolio = database.get_portfolio()
    portfolio_id = portfolio["id"] if portfolio else None

    summary = database.get_backtest_summary(
        year_filter=year,
        market_filter=market,
    )
    actual_stats = None
    if portfolio_id:
        actual_stats = database.get_actual_stats_for_benchmark(
            portfolio_id=portfolio_id,
            year_filter=year,
            market_filter=market,
        )

    return {
        "filters": {"year": year, "market": market or "ALL"},
        "last_imported_at": summary["last_imported_at"],
        "available_years": summary["available_years"],
        "backtest_stats": summary["backtest_stats"],
        "actual_stats": actual_stats,
        "yearly_breakdown": summary["yearly_breakdown"],
    }


# ---------------------------------------------------------------------------
# GET /strategy/benchmark/trades
# ---------------------------------------------------------------------------

@router.get("/strategy/benchmark/trades")
async def get_benchmark_trades(
    request: Request,
    year: Optional[int] = Query(None, description="Filter to a specific entry year"),
    market: Optional[str] = Query(None, description="Filter by market (US, UK, ALL)"),
):
    """Return Panel 3 trade log data for the Strategy Benchmark page.

    Returns backtest_trades and actual_trades separately so the frontend can
    display the appropriate subset based on the selected toggle mode:
      - backtest only: render backtest_trades
      - actual only: render actual_trades
      - side-by-side: render both lists together
    """
    database.ensure_backtest_tables()

    backtest_trades = database.get_backtest_trades(
        year_filter=year,
        market_filter=market,
    )

    portfolio = database.get_portfolio()
    portfolio_id = portfolio["id"] if portfolio else None
    actual_trades: list = []
    if portfolio_id:
        from database import get_trade_history
        raw = get_trade_history(portfolio_id)
        for t in raw:
            entry_year = None
            if t.get("entry_date"):
                try:
                    entry_year = int(str(t["entry_date"])[:4])
                except (ValueError, TypeError):
                    pass
            if year is not None and entry_year != year:
                continue
            if market and market.upper() != "ALL":
                if (t.get("market") or "").upper() != market.upper():
                    continue
            actual_trades.append({
                "ticker": t.get("ticker"),
                "entry_date": str(t["entry_date"]) if t.get("entry_date") else None,
                "exit_date": str(t["exit_date"]) if t.get("exit_date") else None,
                "holding_days": t.get("holding_days"),
                "entry_price": float(t["entry_price"]) if t.get("entry_price") else None,
                "exit_price": float(t["exit_price"]) if t.get("exit_price") else None,
                "pnl_gbp": float(t["pnl"]) if t.get("pnl") else None,
                "pnl_pct": float(t["pnl_pct"]) if t.get("pnl_pct") else None,
                "market": t.get("market", "US"),
                "exit_reason": t.get("exit_reason"),
                "was_profitable": (float(t["pnl"]) > 0) if t.get("pnl") else None,
                "entry_year": entry_year,
            })

    return {
        "filters": {"year": year, "market": market or "ALL"},
        "backtest_trades": [
            {**t, "entry_date": str(t["entry_date"]), "exit_date": str(t["exit_date"])}
            for t in backtest_trades
        ],
        "actual_trades": actual_trades,
    }
