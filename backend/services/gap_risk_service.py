"""
Gap Risk Flag Service — ST-02 (BLG-FEAT-65, v6.9)

Governed by the §13 review record
docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md
(CONDITIONAL, Binding Conditions 1-9) and its v9.10 addendum (ST-13, BLG-GOV-365).

Flags an open position when one known, dated event specific to its ticker falls
before its next trading session. The only such event is a scheduled earnings
date (strategy_rules.md §4.2.3, §13.3). Shown with a historical overnight or
weekend gap statistic from daily OHLCV (yfinance), matching the yfinance-direct
pattern used by earnings_service.py / sector_service.py.

Trigger rules (Strategy Rules & System Intent Owner ruling, v9.10 ST-13):
  - US positions only, as §4.2.3 is US-only. A UK position is never flagged.
  - The earnings date is after today and on or before the next trading day
    (weekday calendar). A Friday view flags Monday earnings. Earnings today
    (day 0) are not flagged: a before-open release has already gapped, which
    §13.3 and Binding Condition 3 exclude, and yfinance cannot tell before-open
    from after-close. The previous session's view already flagged that date.

The standalone weekend-hold trigger, which flagged every position each Friday,
was removed in v9.10 (ST-14, BLG-BE-136) under Binding Condition 6.

Display-only and computed on request (Binding Conditions 1-2). Surfaces a known
calendar event and a historical statistic; does not predict gap direction or
magnitude for the upcoming event (§13, AC-04).

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

# Markets whose earnings dates are a canonical gap-risk event (strategy_rules.md
# §4.2.3 is US-only; ST-13 ruling, v9.10).
_EARNINGS_TRIGGER_MARKETS = ("US",)


def _days_to_next_trading_day(today: date) -> int:
    """Calendar days from today to the next weekday (Fri -> 3, Sat -> 2, else 1).

    Weekday calendar only: exchange holidays are not modelled, so the day after a
    holiday-shortened week is treated as the next session.
    """
    weekday = today.weekday()  # Monday=0 ... Sunday=6
    if weekday == 4:
        return 3
    if weekday == 5:
        return 2
    return 1


def _earnings_before_next_session(days_until: Optional[int], today: date) -> bool:
    """True when earnings fall after today and on or before the next trading day (no day 0)."""
    if days_until is None:
        return False
    return 1 <= days_until <= _days_to_next_trading_day(today)


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


def get_gap_risk(ticker: str, market: str, today: Optional[date] = None) -> Dict:
    """
    Compute the gap_risk object for a single position.

    Returns:
      {
        "flagged": bool,
        "reasons": [] or ["earnings"],
        "avg_gap_pct": float | None,
        "event_count": int,
        "insufficient_history": bool
      }
    """
    today = today or date.today()
    reasons = []

    if market in _EARNINGS_TRIGGER_MARKETS:
        earnings = get_earnings(ticker, market)
        if _earnings_before_next_session(earnings.get("days_until_earnings"), today):
            reasons.append("earnings")

    if not reasons:
        return {
            "flagged": False,
            "reasons": [],
            "avg_gap_pct": None,
            "event_count": 0,
            "insufficient_history": False,
        }

    # From Friday to Sunday the gap ahead is the Friday-close to Monday-open
    # weekend gap, so show the weekend statistic then.
    stats = _compute_gap_stats(ticker, market, weekend=today.weekday() >= 4)

    return {
        "flagged": True,
        "reasons": reasons,
        "avg_gap_pct": stats["avg_gap_pct"],
        "event_count": stats["event_count"],
        "insufficient_history": stats["insufficient_history"],
    }
