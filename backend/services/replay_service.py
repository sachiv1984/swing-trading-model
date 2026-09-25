"""
Replay Service — ST-01b (EPIC-01, v9.7, BLG-FEAT-74, PO-05 Lightweight Replay Mode)

Implements docs/product/decisions/po05_replay_scope_confirmation.md (rev 3) D1-D6:
replays each of the user's own closed trades, independently, through the current
`strategy_engine` exit rules (stop / risk-off), in a "ratio space" anchored at the
trade's own recorded entry price -- never comparing a recorded price against a raw
yfinance value directly (dividend adjustment, splits and UK pence make the two bases
incompatible; see the scope note D1 "Price basis").

§13 compliance (po05_section13_preassessment.md, Binding Condition 5, satisfied by
construction): this module makes NO Alpaca call and reads/writes no Alpaca data --
it is a pure in-process simulation over `trade_history` (own-data only) and
`yfinance` price history. It is also read-only: no table is created, no row is
written anywhere (Binding Condition 1).

Router -> service -> database layering: backend/routers/replay.py does request-shape
validation and error-envelope translation only; this module does everything else
(trade resolution, bounds, price/regime fetch, the day-by-day simulation, and
response assembly).
"""
import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import yfinance as yf

from database import get_portfolio, get_trade_history_by_date_range, get_trade_history_by_ids
from utils.upstream_call import get_timeout
from services.strategy_engine import (
    LIVE_PARAMS,
    compute_active_atr_mult,
    compute_atr,
    compute_initial_stop,
    compute_risk_on,
    is_risk_on,
    transaction_fee,
)

# Binding Condition 2 (po05_section13_preassessment.md) -- verbatim wording approved in
# docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md §2.3. A
# backend test (test_replay_service.py) asserts this constant equals that approved
# string exactly; the frontend keeps an identical hard-coded fallback literal so a
# missing/renamed field here can never silently drop the banner (D4).
RETROSPECTIVE_NOTICE = (
    "Retrospective result — shows what the current rules would have produced over "
    "this past period. Not a prediction of future performance."
)

MAX_TRADES = 100
MAX_TICKERS = 25
FETCH_LOOKBACK_DAYS = 420  # D6: min(entry_date) - 420 calendar days
ATR_MIN_ROWS_BEFORE_ENTRY = 14  # D6 -- deliberately one row more than compute_atr's own
                                 # rolling(14) minimum (first valid at position 13), so
                                 # ATR(entry) is never the artefact-bearing first valid row.
REGIME_MIN_ROWS_BEFORE_ENTRY = 200  # matches compute_risk_on's rolling(200) window


class ReplayValidationError(Exception):
    """Raised for a request-shape problem the router did not already catch (e.g. a
    resolved-but-nonsensical combination). Router maps this to 400 validation_error."""


class ReplayScopeTooLargeError(Exception):
    """Raised when resolved trades or distinct tickers exceed the D2 bounds (100
    trades / 25 tickers). Router maps this to 400 replay_scope_too_large."""


class ReplayPriceDataUnavailableError(Exception):
    """Raised when the price provider returned nothing usable for every requested
    ticker, or for a regime series this run requires. Router maps this to 500
    price_data_unavailable. Distinct from a per-trade `skipped` entry with the same
    reason string, which covers one trade's own individually-missing data."""


def _to_float(value) -> Optional[float]:
    """psycopg2/RealDictCursor returns NUMERIC columns as decimal.Decimal (or None)."""
    return None if value is None else float(value)


def _today_utc() -> date:
    """D6 "Today": evaluated in UTC, the repository precedent (BLG-BE-125,
    database.py's month-closure clock-source rule)."""
    return datetime.now(timezone.utc).date()


def _resolve_trades(portfolio_id: Optional[str], mode: str, date_from: Optional[date],
                     date_to: Optional[date], trade_ids: Optional[List[str]]):
    """Return (rows, requested_trade_count, skipped) for the D2 resolution step.
    `rows` are dicts as returned by the database layer (own-portfolio trade_history
    rows only). `skipped` here only ever carries `trade_not_found` entries -- the
    later today-boundary and price-data skips are appended by the caller."""
    if mode == "trade_set":
        # De-duplicate, preserving first occurrence -- D2: "duplicate ids are
        # de-duplicated and requested_trade_count is counted after de-duplication."
        seen = set()
        deduped_ids = []
        for tid in trade_ids:
            if tid not in seen:
                seen.add(tid)
                deduped_ids.append(tid)
        requested_trade_count = len(deduped_ids)
        if portfolio_id is None:
            # No portfolio at all -- nothing can possibly match (every trade_history
            # row belongs to some real portfolio_id), so every id is trade_not_found
            # without a DB round trip. SQL `portfolio_id = NULL` would also naturally
            # match zero rows if this branch were removed, but that is a fragile
            # implicit-NULL-semantics dependency, not a design choice worth relying on.
            return [], requested_trade_count, [
                {"trade_id": tid, "reason": "trade_not_found"} for tid in deduped_ids
            ]
        rows = get_trade_history_by_ids(portfolio_id, deduped_ids)
        found_ids = {str(r["id"]) for r in rows}
        skipped = [
            {"trade_id": tid, "reason": "trade_not_found"}
            for tid in deduped_ids if tid not in found_ids
        ]
        return rows, requested_trade_count, skipped

    # date_range mode: every row the query returns is both requested and resolved --
    # there is no "not found" concept for a range query (D2's own text: "there is no
    # 'not found' concept for a date range" is implicit in the AC; a range simply
    # returns however many trades exist in it).
    if portfolio_id is None:
        return [], 0, []
    rows = get_trade_history_by_date_range(portfolio_id, date_from, date_to)
    return rows, len(rows), []


def _regimes_required_for(ticker: str, risk_off_mode: str) -> set:
    """Mirrors is_risk_on's own branching (strategy_engine.py) so replay fetches only
    the regime series a request's tickers actually need (D6 "Fetch only when
    needed")."""
    if risk_off_mode == "single":
        return {"uk"} if ticker.endswith(".L") else {"us"}
    return {"us", "uk"}  # dual / dual_strict need both regardless of ticker


def _extract_close(data) -> pd.DataFrame:
    """yfinance returns MultiIndex columns (level 0 = field, level 1 = ticker) for both
    a single- and multi-ticker `download()` call in current versions; older versions
    collapsed a single ticker to a plain Series/single-level DataFrame. Handle both."""
    if data is None or len(data) == 0:
        return pd.DataFrame()
    if isinstance(data.columns, pd.MultiIndex):
        if "Close" not in data.columns.get_level_values(0):
            return pd.DataFrame()
        close = data["Close"]
    else:
        close = data["Close"] if "Close" in data.columns else pd.Series(dtype=float)
    if isinstance(close, pd.Series):
        close = close.to_frame(name=close.name or "value")
    return close


def _fetch_close_series(tickers: List[str], start: date, end_exclusive: date) -> Dict[str, pd.Series]:
    """One yfinance call for all tickers, then per-ticker NaN-drop (D6: "each ticker
    uses its own trading calendar"; "rows with a NaN close are dropped per ticker").
    Returns {ticker: Series} with each ticker's own clean, ascending date index."""
    data = yf.download(
        tickers, start=start.isoformat(), end=end_exclusive.isoformat(),
        auto_adjust=True, progress=False, timeout=get_timeout("yfinance_history"),
    )
    close = _extract_close(data)
    if len(close.columns) == 1 and close.columns[0] not in tickers and len(tickers) == 1:
        close = close.rename(columns={close.columns[0]: tickers[0]})
    # D6 "sorted" -- searchsorted() in _asof_position and the day-loop's forward walk
    # both assume ascending order; sort defensively rather than trust yfinance's
    # ordering, the same precedent backtest_rule_service.py's own fetch already sets.
    return {t: (close[t].dropna().sort_index() if t in close.columns else pd.Series(dtype=float)) for t in tickers}


def _fetch_regime_series(ticker_symbol: str, start: date, end_exclusive: date) -> pd.Series:
    data = yf.download(
        ticker_symbol, start=start.isoformat(), end=end_exclusive.isoformat(),
        auto_adjust=True, progress=False, timeout=get_timeout("yfinance_history"),
    )
    close = _extract_close(data)
    if close.empty:
        return pd.Series(dtype=float)
    return close.iloc[:, 0].dropna().sort_index()


def _asof_position(date_index: pd.DatetimeIndex, target: date):
    """Return (position, bar_timestamp) of the last bar in `date_index` on or before
    `target`, or (None, None) if none exists. `date_index` must be sorted ascending."""
    if len(date_index) == 0:
        return None, None
    pos = date_index.searchsorted(pd.Timestamp(target), side="right") - 1
    if pos < 0:
        return None, None
    return int(pos), date_index[pos]


def _replay_one_trade(row: Dict, close_by_ticker: Dict[str, pd.Series], atr_by_ticker: Dict[str, pd.Series],
                       regime_aligned_by_ticker: Dict[str, Dict[str, pd.Series]], rule_set: Dict) -> Dict:
    """Simulate one trade per D1. Returns either a replayed-trade dict (with
    `simulated_exit_*` fields) or a `{"skip": "<reason>"}` dict."""
    trade_id = str(row["id"])
    ticker = row["ticker"]
    market = "UK" if ticker.endswith(".L") else "US"
    currency = "GBP" if market == "UK" else "USD"
    entry_date: date = row["entry_date"]
    exit_date: date = row["exit_date"]
    entry_price = _to_float(row["entry_price"])
    shares = _to_float(row["shares"])

    ticker_dates = close_by_ticker[ticker].index
    entry_pos, entry_bar = _asof_position(ticker_dates, entry_date)
    exit_pos, exit_bar = _asof_position(ticker_dates, exit_date)
    if entry_pos is None or exit_pos is None or exit_bar < entry_bar:
        return {"trade_id": trade_id, "skip": "price_data_unavailable"}
    if entry_pos < ATR_MIN_ROWS_BEFORE_ENTRY:
        return {"trade_id": trade_id, "skip": "insufficient_history"}

    for regime_side in _regimes_required_for(ticker, rule_set["risk_off_mode"]):
        raw = regime_aligned_by_ticker[ticker].get(f"_raw_{regime_side}")
        if raw is None:
            return {"trade_id": trade_id, "skip": "insufficient_history"}
        pos, _ = _asof_position(raw.index, entry_date)
        if pos is None or pos < REGIME_MIN_ROWS_BEFORE_ENTRY:
            return {"trade_id": trade_id, "skip": "insufficient_history"}

    ref = float(close_by_ticker[ticker].loc[entry_bar])
    if not np.isfinite(ref) or ref <= 0:
        return {"trade_id": trade_id, "skip": "insufficient_history"}
    scale = entry_price / ref

    atr_series = atr_by_ticker[ticker]
    atr_at_entry = float(atr_series.loc[entry_bar]) * scale if entry_bar in atr_series.index else np.nan
    if not np.isfinite(atr_at_entry):
        return {"trade_id": trade_id, "skip": "insufficient_history"}

    initial_stop = compute_initial_stop(entry_price, atr_at_entry, rule_set["stop_loss_mode"],
                                         rule_set["atr_mult"], rule_set["initial_atr_mult"])
    if not np.isfinite(initial_stop):
        return {"trade_id": trade_id, "skip": "insufficient_history"}

    regime_us = regime_aligned_by_ticker[ticker]["us"]
    regime_uk = regime_aligned_by_ticker[ticker]["uk"]

    stop = initial_stop
    sim_exit_date = None
    sim_exit_price = None
    sim_exit_reason = None
    for bar in ticker_dates[(ticker_dates > pd.Timestamp(entry_date)) & (ticker_dates <= pd.Timestamp(exit_date))]:
        bar_date = bar.date()
        holding_days = (bar_date - entry_date).days
        sim_price = scale * float(close_by_ticker[ticker].loc[bar])

        if holding_days >= rule_set["min_hold_days"]:
            atr_val = float(atr_series.loc[bar]) * scale if bar in atr_series.index else np.nan
            if not np.isnan(atr_val):
                is_profitable = sim_price > entry_price
                active_mult = compute_active_atr_mult(
                    rule_set["stop_loss_mode"], holding_days, rule_set["min_hold_days"],
                    rule_set["atr_mult"], rule_set["initial_atr_mult"], rule_set["profit_atr_mult"],
                    is_profitable=is_profitable,
                )
                new_stop = sim_price - active_mult * atr_val
                stop = max(stop, new_stop)
                if sim_price <= stop:
                    sim_exit_date, sim_exit_price, sim_exit_reason = bar_date, sim_price, "Stop"
                    break

        if not is_risk_on(ticker, bar, regime_us, regime_uk, rule_set["risk_off_mode"]):
            sim_exit_date, sim_exit_price, sim_exit_reason = bar_date, sim_price, "Risk-Off"
            break

    if sim_exit_date is None:
        # No rule fired through the trade's own window -- D1: the simulated exit is
        # the actual exit date's own bar, reason "Actual Exit". Covers the 0-day
        # (entry_date == exit_date) case too, whose day-loop domain is empty.
        sim_exit_date = exit_bar.date()
        sim_exit_price = scale * float(close_by_ticker[ticker].loc[exit_bar])
        sim_exit_reason = "Actual Exit"

    sell_fee = transaction_fee(ticker, "sell")
    pnl_native = (sim_exit_price * (1 - sell_fee) - entry_price) * shares

    entry_fx_rate = _to_float(row.get("entry_fx_rate"))
    if market == "UK":
        fx_basis = "not_applicable_gbp"
        pnl_gbp = pnl_native
    elif entry_fx_rate is not None and entry_fx_rate > 0:
        fx_basis = "entry_fx_rate"
        pnl_gbp = pnl_native / entry_fx_rate
    else:
        fx_basis = "unavailable"
        pnl_gbp = None

    return {
        "trade_id": trade_id, "ticker": ticker, "market": market, "currency": currency,
        "entry_date": entry_date.isoformat(), "entry_price": round(entry_price, 4), "shares": shares,
        "initial_stop": round(initial_stop, 4),
        "simulated_exit_date": sim_exit_date.isoformat(), "simulated_exit_price": round(sim_exit_price, 4),
        "simulated_exit_reason": sim_exit_reason, "holding_days": (sim_exit_date - entry_date).days,
        "simulated_pnl_native": round(pnl_native, 2),
        "simulated_pnl_gbp": None if pnl_gbp is None else round(pnl_gbp, 2),
        "fx_basis": fx_basis,
        "_win": pnl_native > 0,  # unrounded-basis win flag (D4); stripped before the response is returned
        "_pnl_gbp_unrounded": pnl_gbp,
    }


def _fingerprint(rule_set: Dict, replayed_rows: List[Dict], close_by_ticker: Dict[str, pd.Series],
                  regime_raw: Dict[str, pd.Series]) -> str:
    """D6: SHA-256 of one canonical JSON document covering the rule set, every
    replayed trade's own identifying fields, and the full fetched close/regime series
    actually used this run."""
    payload = {
        "rule_set": rule_set,
        "trades": sorted([
            {
                "trade_id": str(r["id"]), "ticker": r["ticker"],
                "entry_date": r["entry_date"].isoformat(), "exit_date": r["exit_date"].isoformat(),
                "entry_price": _to_float(r["entry_price"]), "shares": _to_float(r["shares"]),
                "entry_fx_rate": _to_float(r.get("entry_fx_rate")),
            }
            for r in replayed_rows
        ], key=lambda x: x["trade_id"]),
        "close_series": {
            ticker: [[d.date().isoformat(), repr(float(v))] for d, v in series.items()]
            for ticker, series in sorted(close_by_ticker.items())
        },
        "regime_series": {
            side: [[d.date().isoformat(), repr(bool(v))] for d, v in series.items()]
            for side, series in sorted(regime_raw.items())
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def run_replay(mode: str, date_from: Optional[date] = None, date_to: Optional[date] = None,
               trade_ids: Optional[List[str]] = None) -> Dict:
    """Entry point called by backend/routers/replay.py once the request body has
    passed its own structural validation. Returns the full `data` object of D4's
    success envelope. Raises ReplayScopeTooLargeError / ReplayPriceDataUnavailableError
    for the D5 error cases that originate in this layer."""
    portfolio = get_portfolio()
    portfolio_id = str(portfolio["id"]) if portfolio else None

    rows, requested_trade_count, skipped = _resolve_trades(portfolio_id, mode, date_from, date_to, trade_ids)

    # D2 bounds: evaluated on resolved trades, before the today-boundary skip below.
    if len(rows) > MAX_TRADES:
        raise ReplayScopeTooLargeError(f"Resolved {len(rows)} trades; at most {MAX_TRADES} may be replayed in one run.")
    distinct_tickers = {r["ticker"] for r in rows}
    if len(distinct_tickers) > MAX_TICKERS:
        raise ReplayScopeTooLargeError(f"Resolved trades span {len(distinct_tickers)} tickers; at most {MAX_TICKERS} may be replayed in one run.")

    today = _today_utc()
    surviving_rows = []
    for r in rows:
        if r["exit_date"] >= today:
            skipped.append({"trade_id": str(r["id"]), "reason": "price_data_unavailable"})
        else:
            surviving_rows.append(r)

    rule_set = {k: LIVE_PARAMS[k] for k in (
        "stop_loss_mode", "atr_mult", "initial_atr_mult", "profit_atr_mult", "min_hold_days", "risk_off_mode",
    )}

    if not surviving_rows:
        # D6 "Fetch only when needed": nothing to replay, so no network call at all.
        return _build_response(mode, date_from, date_to, requested_trade_count, [], skipped, rule_set, {}, {})

    tickers = sorted({r["ticker"] for r in surviving_rows})
    needed_regimes = set()
    for r in surviving_rows:
        needed_regimes |= _regimes_required_for(r["ticker"], rule_set["risk_off_mode"])

    fetch_start = min(r["entry_date"] for r in surviving_rows) - timedelta(days=FETCH_LOOKBACK_DAYS)
    fetch_end_exclusive = max(r["exit_date"] for r in surviving_rows) + timedelta(days=1)  # yfinance `end` is exclusive

    close_by_ticker = _fetch_close_series(tickers, fetch_start, fetch_end_exclusive)
    if all(len(s) == 0 for s in close_by_ticker.values()):
        raise ReplayPriceDataUnavailableError("The price provider returned no usable data for any requested ticker.")

    regime_raw = {}
    if "us" in needed_regimes:
        regime_raw["us"] = _fetch_regime_series("SPY", fetch_start, fetch_end_exclusive)
        if len(regime_raw["us"]) == 0:
            raise ReplayPriceDataUnavailableError("The price provider returned no usable data for the SPY regime series.")
    if "uk" in needed_regimes:
        regime_raw["uk"] = _fetch_regime_series("^FTSE", fetch_start, fetch_end_exclusive)
        if len(regime_raw["uk"]) == 0:
            raise ReplayPriceDataUnavailableError("The price provider returned no usable data for the ^FTSE regime series.")

    regime_bool = {side: compute_risk_on(series) for side, series in regime_raw.items()}

    atr_by_ticker = {t: compute_atr(close_by_ticker[t].to_frame(name=t))[t] for t in tickers if len(close_by_ticker[t]) > 0}

    # Align each required regime side onto each ticker's OWN calendar (D6: "each ticker
    # uses its own trading calendar... a regime value for a ticker's date is the last
    # regime bar on or before it (forward-fill only)") so the unmodified engine
    # is_risk_on() can do an exact `.at[date]` lookup, per strategy_engine.py's own
    # docstring for that function.
    regime_aligned_by_ticker = {}
    for t in tickers:
        idx = close_by_ticker[t].index
        aligned = {}
        for side in ("us", "uk"):
            if side in regime_bool:
                aligned[side] = regime_bool[side].reindex(idx, method="ffill").fillna(False)
                aligned[f"_raw_{side}"] = regime_raw[side]
            else:
                aligned[side] = pd.Series(False, index=idx)
        regime_aligned_by_ticker[t] = aligned

    replayed = []
    for row in surviving_rows:
        ticker = row["ticker"]
        if len(close_by_ticker.get(ticker, [])) == 0:
            skipped.append({"trade_id": str(row["id"]), "reason": "price_data_unavailable"})
            continue
        result = _replay_one_trade(row, close_by_ticker, atr_by_ticker, regime_aligned_by_ticker, rule_set)
        if "skip" in result:
            skipped.append({"trade_id": result["trade_id"], "reason": result["skip"]})
        else:
            replayed.append(result)

    replayed_rows_for_fingerprint = [r for r in surviving_rows if str(r["id"]) in {t["trade_id"] for t in replayed}]
    fingerprint = _fingerprint(rule_set, replayed_rows_for_fingerprint, close_by_ticker, regime_raw)

    return _build_response(mode, date_from, date_to, requested_trade_count, replayed, skipped, rule_set,
                            close_by_ticker, regime_raw, fingerprint)


def _build_response(mode, date_from, date_to, requested_trade_count, replayed, skipped, rule_set,
                     close_by_ticker, regime_raw, fingerprint=None) -> Dict:
    replayed_sorted = sorted(replayed, key=lambda t: (t["simulated_exit_date"], t["trade_id"]))

    trade_count = len(replayed_sorted)
    win_count = sum(1 for t in replayed_sorted if t["_win"])
    win_rate_pct = round(100.0 * win_count / trade_count, 2) if trade_count > 0 else None

    gbp_values = [t["_pnl_gbp_unrounded"] for t in replayed_sorted if t["_pnl_gbp_unrounded"] is not None]
    excluded_from_gbp_total = sum(1 for t in replayed_sorted if t["fx_basis"] == "unavailable")
    total_simulated_pnl_gbp = round(sum(gbp_values), 2) if gbp_values else 0.0

    trades_out = [
        {k: v for k, v in t.items() if not k.startswith("_")}
        for t in replayed_sorted
    ]

    return {
        "retrospective_notice": RETROSPECTIVE_NOTICE,
        "run": {
            "mode": mode,
            "date_from": date_from.isoformat() if date_from else None,
            "date_to": date_to.isoformat() if date_to else None,
            "requested_trade_count": requested_trade_count,
            "replayed_trade_count": trade_count,
            "skipped": skipped,
            "rule_set": rule_set,
            "price_data_source": "yfinance",
            "price_data_fingerprint": fingerprint,
        },
        "summary": {
            "trade_count": trade_count,
            "win_count": win_count,
            "win_rate_pct": win_rate_pct,
            "total_simulated_pnl_gbp": total_simulated_pnl_gbp,
            "excluded_from_gbp_total": excluded_from_gbp_total,
        },
        "trades": trades_out,
    }
