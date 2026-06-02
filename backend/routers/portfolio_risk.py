"""
Portfolio Risk Router

Implements:
  GET /portfolio/drawdown-status  — drawdown threshold check (IT-04)
  GET /portfolio/concentration-status — position/sector concentration limits (IT-05)

Contracts: docs/specs/api_contracts/portfolio_endpoints.md
"""

from fastapi import APIRouter
from database import get_db, get_portfolio, get_positions, get_portfolio_snapshots
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
        sector = pos.get("sector")

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
