"""
services/drawdown_service.py — QWB Quick Wins Bundle (v1.6.1)
=============================================================
New service file. Place at: backend/services/drawdown_service.py
Export get_drawdown_fields from backend/services/__init__.py

Canonical spec: portfolio_endpoints.md v1.8.2
               metrics_definitions.md v1.5.8 §Current Drawdown
"""

from typing import Dict
from database import get_peak_portfolio_value


def get_drawdown_fields(portfolio_id: str, current_total_value: float, conn=None) -> Dict:
    """
    Compute current_drawdown_percent and peak_portfolio_value for
    inclusion in the GET /portfolio response.

    Formula (canonical — metrics_definitions.md v1.5.8):
        peak_portfolio_value  = MAX(portfolio_history.total_value)  [all-time]
        current_drawdown_percent =
            (current_total_value - peak_portfolio_value)
            / peak_portfolio_value * 100

    Result contract:
        - current_drawdown_percent is always <= 0.0
        - Both fields default to 0.0 when no portfolio_history exists
        - Both fields are always present — never None

    Args:
        portfolio_id:        Portfolio UUID string.
        current_total_value: The portfolio's current total_value
                             (cash + open positions), already computed
                             by the calling portfolio service.
        conn:                Optional DB connection to reuse (for single-connection
                             request paths). If None, a new connection is opened.

    Returns:
        Dict with keys:
            current_drawdown_percent (float): Drawdown %, <= 0.0
            peak_portfolio_value     (float): All-time peak in GBP
    """
    peak = get_peak_portfolio_value(portfolio_id, conn=conn)

    if peak == 0.0:
        # No portfolio_history records exist — Establishing Peak state.
        # Both fields return 0.0 per spec failure behaviour.
        return {
            "current_drawdown_percent": 0.0,
            "peak_portfolio_value": 0.0,
        }

    current_drawdown_percent = (
        (current_total_value - peak) / peak * 100
    )

    # Result must be <= 0.0 by definition (current can only equal or
    # be below peak when peak is the all-time max). Guard against
    # floating-point edge cases where current_total_value > peak
    # due to snapshot timing (e.g. intraday price rise not yet snapped).
    current_drawdown_percent = min(current_drawdown_percent, 0.0)

    return {
        "current_drawdown_percent": round(current_drawdown_percent, 4),
        "peak_portfolio_value": round(peak, 2),
    }
