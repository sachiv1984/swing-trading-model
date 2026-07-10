"""
Gap Risk Flag Service — ST-02 (BLG-FEAT-65, v6.9)

Computes overnight/weekend gap risk flags for open positions by combining:
  - Earnings proximity (DS-04 earnings calendar via earnings_service.get_earnings)
  - Weekend-hold detection (Friday close, server-computed day-of-week — frontend
    renders the flag as returned, no client-side day-of-week logic per ux_spec.md §5)
  - Historical overnight/weekend gap statistics from daily OHLCV (yfinance), matching
    the existing yfinance-direct pattern used by earnings_service.py / sector_service.py

Deterministic only — surfaces a known calendar event and a historical statistic;
does not predict gap direction or magnitude for the upcoming event (§13, AC-04).

Spec: docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk
      docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md
      docs/specs/frontend/pages/positions.md#Gap Risk Badge
"""
from datetime import date
from typing import Dict, Optional

import yfinance as yf

from services.earnings_service import get_earnings, _yf_ticker_symbol

# Minimum historical gap events required before a numeric average is shown.
# Backend-defined constant (N in ux_spec.md §4) — frontend renders whatever the
# API returns verbatim; no client-side threshold logic.
MIN_HISTORICAL_EVENTS = 10

_HISTORY_PERIOD = "2y"

# Earnings dates within this many days are treated as "before the position's
# next trading session" (AC-01). 0 = earnings today (commonly released after
# close, affecting tomorrow's session); 1 = earnings tomorrow. Deterministic
# calendar check only — no attempt to infer before/after-market timing, which
# yfinance does not reliably expose.
_EARNINGS_NEXT_SESSION_WINDOW_DAYS = 1


def _is_weekend_hold(today: Optional[date] = None) -> bool:
    """True when today is Friday — every open position is a weekend hold, flagged at Friday close."""
    d = today or date.today()
    return d.weekday() == 4  # Monday=0 ... Friday=4


def _compute_gap_stats(ticker: str, market: str, weekend: bool) -> Dict:
    """
    Historical average overnight or weekend gap magnitude for a ticker.

    overnight gap: |open[t] - close[t-1]| / close[t-1] for each trading-day pair
                   that is NOT a weekend gap.
    weekend gap:   |open[Monday] - close[Friday]| / close[Friday] (or after any
                   multi-day market closure > 3 days, e.g. holiday weekends).

    Returns {"avg_gap_pct": float|None, "event_count": int, "insufficient_history": bool}
    """
    yf_symbol = _yf_ticker_symbol(ticker, market)
    try:
        hist = yf.Ticker(yf_symbol).history(period=_HISTORY_PERIOD, auto_adjust=True)
        if hist is None or hist.empty or len(hist) < 2:
            return {"avg_gap_pct": None, "event_count": 0, "insufficient_history": True}

        closes = hist["Close"]
        opens = hist["Open"]
        idx = hist.index

        gaps = []
        for i in range(1, len(hist)):
            prev_date = idx[i - 1]
            cur_date = idx[i]
            is_weekend_gap = (cur_date - prev_date).days > 3

            if weekend and not is_weekend_gap:
                continue
            if not weekend and is_weekend_gap:
                continue

            prev_close = float(closes.iloc[i - 1])
            cur_open = float(opens.iloc[i])
            if prev_close <= 0:
                continue
            gaps.append(abs(cur_open - prev_close) / prev_close * 100)

        event_count = len(gaps)
        if event_count < MIN_HISTORICAL_EVENTS:
            return {"avg_gap_pct": None, "event_count": event_count, "insufficient_history": True}

        return {
            "avg_gap_pct": round(sum(gaps) / event_count, 2),
            "event_count": event_count,
            "insufficient_history": False,
        }
    except Exception:
        return {"avg_gap_pct": None, "event_count": 0, "insufficient_history": True}


def get_gap_risk(ticker: str, market: str) -> Dict:
    """
    Compute the gap_risk object for a single position.

    Returns:
      {
        "flagged": bool,
        "reasons": [...] subset of ["earnings", "weekend_hold"], in that order,
        "avg_gap_pct": float | None,
        "event_count": int,
        "insufficient_history": bool
      }
    """
    reasons = []

    earnings = get_earnings(ticker, market)
    days_until = earnings.get("days_until_earnings")
    if days_until is not None and 0 <= days_until <= _EARNINGS_NEXT_SESSION_WINDOW_DAYS:
        reasons.append("earnings")

    weekend_hold = _is_weekend_hold()
    if weekend_hold:
        reasons.append("weekend_hold")

    if not reasons:
        return {
            "flagged": False,
            "reasons": [],
            "avg_gap_pct": None,
            "event_count": 0,
            "insufficient_history": False,
        }

    # When both reasons apply, the weekend gap is the rarer/larger event and is
    # shown per ux_spec.md §4's combined example (Friday close + Monday earnings).
    stats = _compute_gap_stats(ticker, market, weekend=weekend_hold)

    return {
        "flagged": True,
        "reasons": reasons,
        "avg_gap_pct": stats["avg_gap_pct"],
        "event_count": stats["event_count"],
        "insufficient_history": stats["insufficient_history"],
    }
