"""
Portfolio Risk Router

Implements:
  GET /portfolio/drawdown-status  — drawdown threshold check (IT-04)
  GET /portfolio/concentration-status — position/sector concentration limits (IT-05)
  GET /portfolio/gate-metrics  — trade count gate progress (ST-04, v5.5)

Contracts: docs/specs/api_contracts/portfolio_endpoints.md
"""

from fastapi import APIRouter
from database import get_db, get_portfolio, get_positions, get_portfolio_snapshots, get_gate_metrics
from utils.formatting import decimal_to_float

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

_DEFAULT_DRAWDOWN_THRESHOLD = 10.0
_DEFAULT_POSITION_CONCENTRATION_THRESHOLD = 15.0
_DEFAULT_SECTOR_CONCENTRATION_THRESHOLD = 30.0


def _get_settings_value(key: str, default):
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM settings ORDER BY created_at DESC LIMIT 1")
                row = cur.fetchone()
                if row and key in row.keys():
                    val = row[key]
                    if val is not None:
                        return float(val)
    except Exception:
        pass
    return default


def _get_ticker_sector_map(conn) -> dict:
    """Ticker -> sector lookup from ticker_universe. Pure DB read — no yfinance
    live-call added to the hot path (ST-12/AC-04). Positions never carry their
    own `sector` column; sector data only lives in `ticker_universe`.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT ticker, sector FROM ticker_universe WHERE sector IS NOT NULL")
        rows = cur.fetchall()
    return {row["ticker"]: row["sector"] for row in rows}


def _lookup_sector(ticker_sector_map: dict, ticker: str, market: str):
    """Resolve a position's sector via ticker_universe, matching the .L suffix
    convention UK tickers use there (same mapping as watchlist_service.py's join).
    Returns None if the ticker has no sector recorded in ticker_universe.
    """
    if not ticker:
        return None
    ticker = ticker.upper()
    if market == "UK" and not ticker.endswith(".L"):
        key = f"{ticker}.L"
    else:
        key = ticker
    return ticker_sector_map.get(key) or ticker_sector_map.get(ticker)


def _get_portfolio_heat_and_positions():
    """Return (total_value, portfolio_heat_pct, positions_list, portfolio_id, live_fx_rate)."""
    from utils.pricing import get_live_fx_rate
    live_fx_rate = get_live_fx_rate()

    with get_db() as conn:
        portfolio = get_portfolio(conn=conn)
        if not portfolio:
            raise ValueError("Portfolio not found")
        portfolio_id = str(portfolio["id"])
        cash = float(portfolio["cash"])
        positions = get_positions(portfolio_id, status="open", conn=conn)
        ticker_sector_map = _get_ticker_sector_map(conn)

    total_positions_value = 0.0
    position_risks = []
    positions_with_risk = []

    for pos in positions:
        pos = decimal_to_float(dict(pos))
        shares = float(pos.get("shares", 0))
        entry_price = float(pos.get("entry_price", 0))
        market = pos.get("market", "UK")
        fx_rate = float(pos.get("fx_rate") or 1.27)
        initial_stop = pos.get("initial_stop")
        sector = _lookup_sector(ticker_sector_map, pos.get("ticker"), market)

        if market == "US":
            # fill_price is USD native; entry_price is GBP-converted
            entry_price_native = float(pos.get("fill_price") or (entry_price * fx_rate))
            current_price_native = float(pos.get("current_price") or entry_price_native)
            current_price_gbp = current_price_native / live_fx_rate
        else:
            entry_price_native = entry_price
            current_price_gbp = float(pos.get("current_price") or entry_price_native)

        current_value_gbp = current_price_gbp * shares
        total_positions_value += current_value_gbp

        if initial_stop is not None and float(initial_stop) > 0:
            initial_stop = float(initial_stop)
            # Both entry_price_native and initial_stop are stored in native currency
            risk_native = max(0.0, entry_price_native - initial_stop)
            fx_adj = 1.0 / fx_rate if market == "US" else 1.0
            position_risk_gbp = round(risk_native * shares * fx_adj, 2)
        else:
            position_risk_gbp = 0.0

        position_risks.append(position_risk_gbp)
        positions_with_risk.append({
            "id": str(pos["id"]),
            "ticker": pos["ticker"],
            "market": market,
            "sector": sector,
            "position_state": pos.get("position_state"),
            "position_risk_gbp": position_risk_gbp,
        })

    total_value = cash + total_positions_value
    total_risk_gbp = sum(position_risks)
    portfolio_heat_pct = round(total_risk_gbp / total_value * 100, 2) if total_value > 0 else 0.0

    return total_value, portfolio_heat_pct, positions_with_risk, portfolio_id, live_fx_rate, cash, total_positions_value


def _get_30d_peak(portfolio_id: str) -> float:
    """Return portfolio peak total_value over the last 30 trading days. 0.0 if no history."""
    try:
        snapshots = get_portfolio_snapshots(portfolio_id, days=30)
        if not snapshots:
            return 0.0
        return max(float(s["total_value"]) for s in snapshots)
    except Exception:
        return 0.0


def _get_regime_label() -> str:
    try:
        from position_manager import check_market_regime
        r = check_market_regime()
        spy_on = r.get("spy_risk_on", False)
        ftse_on = r.get("ftse_risk_on", False)
        if spy_on and ftse_on:
            return "Bullish"
        elif not spy_on and not ftse_on:
            return "Bearish"
        else:
            return "Neutral"
    except Exception:
        return None


def _get_lifecycle_state_counts(portfolio_id: str) -> dict:
    """Return counts of open positions by position_state."""
    counts = {"GRACE": 0, "PROFITABLE": 0, "LOSING": 0, "EXIT ZONE": 0, "UNKNOWN": 0}
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT position_state, COUNT(*) AS cnt
                    FROM positions
                    WHERE portfolio_id = %s AND status = 'open'
                    GROUP BY position_state
                    """,
                    (portfolio_id,),
                )
                rows = cur.fetchall()
                for row in rows:
                    state = row["position_state"] or "UNKNOWN"
                    counts[state] = counts.get(state, 0) + int(row["cnt"])
    except Exception:
        pass
    return counts


@router.get("/drawdown-status")
def get_drawdown_status():
    """
    Returns current portfolio drawdown vs configurable threshold.

    Drawdown = (30-day portfolio peak − current value) / peak × 100.
    threshold_breached: true when drawdown % exceeds the configured threshold.
    When breached, also returns lifecycle state counts, portfolio heat %, regime.
    """
    try:
        total_value, portfolio_heat_pct, _, portfolio_id, _, cash, positions_value = _get_portfolio_heat_and_positions()
        peak = _get_30d_peak(portfolio_id)
        threshold = _get_settings_value("drawdown_threshold_pct", _DEFAULT_DRAWDOWN_THRESHOLD)

        if peak <= 0:
            current_drawdown_pct = 0.0
        else:
            current_drawdown_pct = round((peak - total_value) / peak * 100, 2)
            current_drawdown_pct = max(current_drawdown_pct, 0.0)

        threshold_breached = current_drawdown_pct >= threshold

        data = {
            "current_drawdown_pct": current_drawdown_pct,
            "threshold_pct": threshold,
            "threshold_breached": threshold_breached,
            "_debug": {
                "peak_value_gbp": round(peak, 2),
                "current_value_gbp": round(total_value, 2),
                "cash_gbp": round(cash, 2),
                "positions_value_gbp": round(positions_value, 2),
            },
        }

        if threshold_breached:
            state_counts = _get_lifecycle_state_counts(portfolio_id)
            regime = _get_regime_label()
            data["portfolio_heat_pct"] = portfolio_heat_pct
            data["regime_status"] = regime
            data["positions_by_state"] = state_counts

        return {"status": "ok", "data": data}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "ok", "data": {"threshold_breached": False, "error": str(e)}}


@router.get("/concentration-status")
def get_concentration_status():
    """
    Returns positions and sectors that breach configurable concentration thresholds.

    Single-position threshold (default 15%): position_risk_gbp / total_risk_gbp × 100.
    Sector threshold (default 30%): sum(sector_risk_gbp) / total_risk_gbp × 100.
    Graceful degradation: positions without sector data excluded from sector calculation.
    """
    try:
        _, _, positions_with_risk, _, _, _, _ = _get_portfolio_heat_and_positions()

        pos_threshold = _get_settings_value(
            "concentration_position_threshold_pct", _DEFAULT_POSITION_CONCENTRATION_THRESHOLD
        )
        sector_threshold = _get_settings_value(
            "concentration_sector_threshold_pct", _DEFAULT_SECTOR_CONCENTRATION_THRESHOLD
        )

        total_risk_gbp = sum(p["position_risk_gbp"] for p in positions_with_risk)

        breaching_positions = []
        sector_risk = {}

        for pos in positions_with_risk:
            risk = pos["position_risk_gbp"]
            if total_risk_gbp > 0:
                pct = round(risk / total_risk_gbp * 100, 2)
            else:
                pct = 0.0

            if pct >= pos_threshold:
                breaching_positions.append({
                    "ticker": pos["ticker"],
                    "heat_pct": pct,
                    "limit_pct": pos_threshold,
                })

            sector = pos.get("sector")
            if sector and total_risk_gbp > 0:
                sector_risk[sector] = sector_risk.get(sector, 0.0) + risk

        breaching_sectors = []
        for sector, risk in sector_risk.items():
            pct = round(risk / total_risk_gbp * 100, 2) if total_risk_gbp > 0 else 0.0
            if pct >= sector_threshold:
                breaching_sectors.append({
                    "sector": sector,
                    "concentration_pct": pct,
                    "limit_pct": sector_threshold,
                })

        any_breach = bool(breaching_positions or breaching_sectors)

        return {
            "status": "ok",
            "data": {
                "any_breach": any_breach,
                "position_threshold_pct": pos_threshold,
                "sector_threshold_pct": sector_threshold,
                "breaching_positions": breaching_positions,
                "breaching_sectors": breaching_sectors,
            },
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "ok", "data": {"any_breach": False, "error": str(e)}}


# ST-06, EPIC-03, v6.1
@router.get("/sector-weights")
def get_sector_weights():
    """
    GET /portfolio/sector-weights

    Return open-position sector breakdown: exposure % by market value,
    position count per sector, and a concentration alert flag (≥40% in one sector).

    Spec: stage4_backlog_slice.md#ST-06
    """
    try:
        from utils.pricing import get_live_fx_rate
        live_fx_rate = get_live_fx_rate()

        with get_db() as conn:
            portfolio = get_portfolio(conn=conn)
            if not portfolio:
                return {"status": "ok", "data": {"sectors": [], "total_positions": 0, "concentration_alert": False}}
            portfolio_id = str(portfolio["id"])
            raw_positions = get_positions(portfolio_id, status="open", conn=conn)
            ticker_sector_map = _get_ticker_sector_map(conn)

        sector_values: dict = {}
        sector_counts: dict = {}
        total_market_value = 0.0

        for pos in raw_positions:
            pos = decimal_to_float(dict(pos))
            shares = float(pos.get("shares", 0))
            market = pos.get("market", "UK")
            sector = _lookup_sector(ticker_sector_map, pos.get("ticker"), market) or "Unclassified"
            entry_price = float(pos.get("entry_price", 0))
            fx_rate = float(pos.get("fx_rate") or 1.27)

            if market == "US":
                entry_price_native = float(pos.get("fill_price") or (entry_price * fx_rate))
                current_price_native = float(pos.get("current_price") or entry_price_native)
                current_value_gbp = (current_price_native / live_fx_rate) * shares
            else:
                current_price_gbp = float(pos.get("current_price") or entry_price)
                current_value_gbp = current_price_gbp * shares

            sector_values[sector] = sector_values.get(sector, 0.0) + current_value_gbp
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
            total_market_value += current_value_gbp

        sectors = []
        concentration_alert = False

        for sector, value in sorted(sector_values.items(), key=lambda x: x[1], reverse=True):
            exposure_pct = round(value / total_market_value * 100, 1) if total_market_value > 0 else 0.0
            if exposure_pct >= 40.0:
                concentration_alert = True
            sectors.append({
                "sector_name": sector,
                "position_count": sector_counts[sector],
                "exposure_pct": exposure_pct,
            })

        return {
            "status": "ok",
            "data": {
                "sectors": sectors,
                "total_positions": sum(sector_counts.values()),
                "concentration_alert": concentration_alert,
            },
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "ok", "data": {"sectors": [], "total_positions": 0, "concentration_alert": False, "error": str(e)}}


# ST-04, EPIC-02, v5.5
@router.get("/gate-metrics")
def get_gate_metrics_endpoint():
    """
    GET /portfolio/gate-metrics

    Return trade count and data density gate progress metrics.
    Used by the System Status page and SI-05 digest to surface progress
    toward the 20/50/100 closed-trade gates.

    Spec: stage4_backlog_slice.md#ST-04
    """
    try:
        portfolio = get_portfolio()
        if not portfolio:
            return {"status": "ok", "data": {
                "closed_trades_count": 0,
                "closed_trades_with_plans": 0,
                "active_positions_count": 0,
                "ai_journal_entry_count": None,
                "oldest_trade_date": None,
                "newest_trade_date": None,
            }}
        metrics = get_gate_metrics(portfolio["id"])
        return {"status": "ok", "data": metrics}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}
