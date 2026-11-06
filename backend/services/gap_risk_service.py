"""
Gap Risk Flag Service — ST-02 (BLG-FEAT-65, v6.9)

Governed by the §13 review record
docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md
(CONDITIONAL, Binding Conditions 1-9), its v9.10 addendum (ST-13, BLG-GOV-365)
and its v9.12 addendum (ST-14, BLG-BE-148, Revised Ruling 3, ESC-EXEC-20261013-07).

Flags an open position when one known, dated event specific to its ticker falls
before its next trading session. The only such event is a scheduled earnings
date (strategy_rules.md §4.2.3, §13.3). Shown with a historical overnight or
weekend gap statistic from daily OHLCV (yfinance), matching the yfinance-direct
pattern used by earnings_service.py / sector_service.py.

Trigger rules (Strategy Rules & System Intent Owner rulings: v9.10 ST-13; v9.12 ST-14):
  - US positions only, as §4.2.3 is US-only. A UK position is never flagged.
  - "Today" (T) is the current US market date (America/New_York), so a 02:00 UTC
    view uses the previous US day. days_until is the earnings date minus T,
    computed here, not earnings_service's server-date days_until_earnings.
  - Flagged when 1 <= days_until <= d, where d is the calendar days from T to the
    next NYSE session (services/us_market_calendar.py: weekends, NYSE full-closure
    holidays and dated one-off closures are not sessions; early closes are). A
    Friday view flags Monday earnings, or Tuesday's before a Monday holiday.
    Deterministic, with no network call; unannounced closures are not anticipated.
  - Earnings today (day 0) are not flagged: a before-open release has already
    gapped, which §13.3 and Binding Condition 3 exclude, and yfinance cannot tell
    before-open from after-close. The previous session's view already flagged it.

The standalone weekend-hold trigger, which flagged every position each Friday,
was removed in v9.10 (ST-14, BLG-BE-136) under Binding Condition 6.

Display-only and computed on request (Binding Conditions 1-2). Surfaces a known
calendar event and a historical statistic; does not predict gap direction or
magnitude for the upcoming event (§13, AC-04).

Spec: docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk
      docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md
      docs/specs/frontend/pages/positions.md#Gap Risk Badge
"""
from datetime import date, datetime, timedelta
from typing import Dict, Optional

import yfinance as yf

from services.earnings_service import get_earnings, _yf_ticker_symbol
from services.us_market_calendar import (
    days_to_next_nyse_session, is_nyse_session, next_nyse_session, us_market_date,
)

# Minimum historical gap events required before a numeric average is shown.
# Backend-defined constant (N in ux_spec.md §4) — frontend renders whatever the
# API returns verbatim; no client-side threshold logic.
MIN_HISTORICAL_EVENTS = 10

_HISTORY_PERIOD = "2y"

# Markets whose earnings dates are a canonical gap-risk event (strategy_rules.md
# §4.2.3 is US-only; ST-13 ruling, v9.10).
_EARNINGS_TRIGGER_MARKETS = ("US",)


def _days_to_next_trading_day(today: date) -> int:
    """Calendar days from the US market date to the next NYSE session (v9.12 Revised Ruling 3)."""
    return days_to_next_nyse_session(today)


def _days_until(next_earnings_date, today: date) -> Optional[int]:
    """Earnings date minus the US market date, or None when there is no date."""
    if not next_earnings_date:
        return None
    if isinstance(next_earnings_date, str):
        next_earnings_date = date.fromisoformat(next_earnings_date[:10])
    return (next_earnings_date - today).days


def _earnings_before_next_session(days_until: Optional[int], today: date) -> bool:
    """True when earnings fall after today and on or before the next trading day (no day 0)."""
    if days_until is None:
        return False
    return 1 <= days_until <= _days_to_next_trading_day(today)


def _spans_non_session_day(prev_day: date, cur_day: date, market: str) -> bool:
    """True when a non-session day lies between two consecutive bars (ST-22, BLG-BE-174).

    US bars use the NYSE calendar (ST-14), so Friday -> Monday, a holiday and a
    one-off closure all count. Other markets fall back to "more than one calendar
    day apart". The previous `> 3` days test missed every ordinary weekend
    (Friday -> Monday is 3 days), so those were counted as overnight gaps.
    """
    if market == "US":
        d = prev_day + timedelta(days=1)
        while d < cur_day:
            if not is_nyse_session(d):
                return True
            d += timedelta(days=1)
        return False
    return (cur_day - prev_day).days > 1


def _next_session_follows_non_session_day(today: date) -> bool:
    """Whether the gap ahead is a weekend/multi-day gap (ST-22, BLG-BE-174).

    True when the day before the next NYSE session is not a session: Friday to
    Sunday views, and a Thursday view before Good Friday. Uses the ST-14 calendar.
    """
    return not is_nyse_session(next_nyse_session(today) - timedelta(days=1))


def _compute_gap_stats(ticker: str, market: str, weekend: bool) -> Dict:
    """
    Historical average overnight or weekend gap magnitude for a ticker.

    overnight gap: |open[t] - close[t-1]| / close[t-1] for consecutive bars with
                   no non-session day between them.
    weekend gap:   the same, for consecutive bars with one or more non-session
                   days between them: Friday -> Monday, and any holiday or
                   closure (ST-22, BLG-BE-174, v9.15: the ST-14 NYSE calendar).

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
            is_weekend_gap = _spans_non_session_day(prev_date.date(), cur_date.date(), market)

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


def get_gap_risk(ticker: str, market: str, today: Optional[date] = None,
                 now: Optional[datetime] = None) -> Dict:
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
    # T: the US market date (injectable for tests as `today` or an aware `now`).
    today = today or us_market_date(now)
    reasons = []

    if market in _EARNINGS_TRIGGER_MARKETS:
        earnings = get_earnings(ticker, market)
        days_until = _days_until(earnings.get("next_earnings_date"), today)
        if _earnings_before_next_session(days_until, today):
            reasons.append("earnings")

    if not reasons:
        return {
            "flagged": False,
            "reasons": [],
            "avg_gap_pct": None,
            "event_count": 0,
            "insufficient_history": False,
        }

    # ST-22 (BLG-BE-174, v9.15): the weekend statistic when the next session
    # follows a non-session day (Friday to Sunday, or a Thursday before Good
    # Friday), by the ST-14 calendar; the overnight statistic otherwise.
    stats = _compute_gap_stats(ticker, market, weekend=_next_session_follows_non_session_day(today))

    return {
        "flagged": True,
        "reasons": reasons,
        "avg_gap_pct": stats["avg_gap_pct"],
        "event_count": stats["event_count"],
        "insufficient_history": stats["insufficient_history"],
    }
