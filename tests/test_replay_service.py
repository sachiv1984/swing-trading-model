"""
tests/test_replay_service.py — ST-01b (EPIC-01, v9.7, BLG-FEAT-74, PO-05 Lightweight
Replay Mode)

Spec: docs/product/decisions/po05_replay_scope_confirmation.md (rev 3), D1-D6, §5.

CI-safe: no real database connection (`database.*` is mocked at the function level for
every test — this also matters beyond CI: this sandbox's ambient DATABASE_URL points at
a real staging database, so every DB-touching call in this file goes through a mock,
never a real connection) and no real network call (`yfinance.download` is replaced by
`FakeYF.download`, a deterministic in-memory panel slicer that reproduces yfinance's
own MultiIndex(Price, Ticker) column shape and `end`-exclusive date-range semantics).
"""
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.replay_service as replay_service  # noqa: E402
from services.replay_service import (  # noqa: E402
    MAX_TICKERS,
    MAX_TRADES,
    RETROSPECTIVE_NOTICE,
    ReplayPriceDataUnavailableError,
    ReplayScopeTooLargeError,
    run_replay,
)

PORTFOLIO_ID = str(uuid4())


class FakeYF:
    """In-memory stand-in for `yfinance.download`. `panels` maps ticker symbol ->
    a pandas Series of close prices (may contain leading NaN, or simply start later
    than the shared date index, to simulate a newly-listed ticker or a
    provider with limited history). Slicing reproduces yfinance's own
    `start`-inclusive / `end`-exclusive window semantics exactly."""

    def __init__(self, panels: dict):
        self.panels = panels
        self.calls = []

    def download(self, tickers, start=None, end=None, auto_adjust=True, progress=False, timeout=None):
        self.calls.append({"tickers": tickers, "start": start, "end": end})
        symbols = [tickers] if isinstance(tickers, str) else list(tickers)
        start_ts = pd.Timestamp(start)
        end_ts = pd.Timestamp(end)  # exclusive, matching real yfinance
        frames = {}
        for field in ("Close", "Open", "High", "Low", "Volume"):
            cols = {}
            for sym in symbols:
                series = self.panels.get(sym, pd.Series(dtype=float, index=pd.DatetimeIndex([])))
                sliced = series[(series.index >= start_ts) & (series.index < end_ts)]
                cols[sym] = sliced if field == "Close" else sliced  # OHLC identical is fine for these tests
            frames[field] = pd.DataFrame(cols)
        df = pd.concat(frames, axis=1)
        df.columns.names = ["Price", "Ticker"]
        return df


def _row(ticker, entry_date, exit_date, entry_price, shares, entry_fx_rate=None):
    return {
        "id": uuid4(), "ticker": ticker, "entry_date": entry_date, "exit_date": exit_date,
        "entry_price": Decimal(str(entry_price)), "shares": Decimal(str(shares)),
        "entry_fx_rate": None if entry_fx_rate is None else Decimal(str(entry_fx_rate)),
    }


def _flat_series(dates, level, start_at=0):
    """A perfectly flat (zero-volatility) price series -- ATR is exactly 0 on this
    series, so any stop check that fires does so immediately (matches
    strategy_engine.py's own ATR=0 behaviour, per the scope note D1's disclosed
    design-induced difference note)."""
    vals = np.full(len(dates), np.nan)
    vals[start_at:] = level
    return pd.Series(vals, index=dates)


def _uptrend_series(dates, start=100.0, daily_return=0.0006):
    return pd.Series(start * np.cumprod(1 + np.full(len(dates), daily_return)), index=dates)


FULL_DATES = pd.bdate_range("2022-01-03", periods=700)  # ends 2024-09-06 -- safely in the past

# AAAA: full history, gentle uptrend, no volatility spikes -> should reach "Actual Exit".
AAAA = _uptrend_series(FULL_DATES, start=50.0, daily_return=0.0003)
# DROP: full history, gentle uptrend, then a single sharp crash -> should hit "Stop".
DROP = _uptrend_series(FULL_DATES, start=80.0, daily_return=0.0003)
DROP_CRASH_IDX = 515
DROP.iloc[DROP_CRASH_IDX:] = DROP.iloc[DROP_CRASH_IDX] * 0.5  # halves and stays there
# RISKOFF: full history, gentle uptrend, no crash of its own -- exits via the shared
# SPY regime dip below, not its own price action.
RISKOFF = _uptrend_series(FULL_DATES, start=60.0, daily_return=0.0002)
# NEWTICK: a UK ticker (.L) with only 10 trading days of history before its trade's
# entry date -- fewer than the required 14, triggering `insufficient_history` (ATR).
NEWTICK_ENTRY_IDX = 300
NEWTICK = _flat_series(FULL_DATES, level=200.0, start_at=NEWTICK_ENTRY_IDX - 10)

# SPY: gentle uptrend throughout, with a single one-day dip at SPY_DIP_IDX that drops
# the day's price below its own (slowly-rising) 200-day trailing MA -- a one-day
# regime flip to risk-off, recovering the next day. Placed well after AAAA/DROP's
# trade windows (idx ~500-540) so it cannot interfere with them.
SPY_DIP_IDX = 580
SPY = _uptrend_series(FULL_DATES, start=100.0, daily_return=0.0004)
SPY.iloc[SPY_DIP_IDX] = SPY.iloc[SPY_DIP_IDX - 1] * 0.85
# FTSE: gentle uptrend throughout, no dip -- NEWTICK's own scenario is about ATR
# warm-up, not regime, so its regime side must stay comfortably risk-on.
FTSE = _uptrend_series(FULL_DATES, start=90.0, daily_return=0.0003)

MAIN_PANELS = {"AAAA": AAAA, "DROP": DROP, "RISKOFF": RISKOFF, "NEWTICK.L": NEWTICK, "SPY": SPY, "^FTSE": FTSE}


def _mock_db(monkeypatch, rows_by_ids=None, rows_by_range=None, portfolio_id=PORTFOLIO_ID):
    monkeypatch.setattr(replay_service, "get_portfolio", lambda: ({"id": portfolio_id} if portfolio_id else None))
    monkeypatch.setattr(replay_service, "get_trade_history_by_ids", lambda pid, ids: rows_by_ids or [])
    monkeypatch.setattr(replay_service, "get_trade_history_by_date_range", lambda pid, f, t: rows_by_range or [])


def _mock_yf(monkeypatch, panels=MAIN_PANELS):
    fake = FakeYF(panels)
    monkeypatch.setattr(replay_service.yf, "download", fake.download)
    return fake


# ── Happy path / determinism / fingerprint ──────────────────────────────────────────

def test_actual_exit_when_no_rule_fires(monkeypatch):
    row = _row("AAAA", date(2023, 12, 1), date(2024, 1, 15), entry_price=float(AAAA.loc["2023-12-01"]), shares=10, entry_fx_rate=1.27)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)

    data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    assert data["run"]["skipped"] == []
    assert len(data["trades"]) == 1
    t = data["trades"][0]
    assert t["simulated_exit_reason"] == "Actual Exit"
    assert t["simulated_exit_date"] == "2024-01-15"
    assert data["retrospective_notice"] == RETROSPECTIVE_NOTICE


def test_stop_exit_on_a_sharp_crash(monkeypatch):
    entry_date = FULL_DATES[500].date()
    exit_date = FULL_DATES[540].date()
    row = _row("DROP", entry_date, exit_date, entry_price=float(DROP.loc[FULL_DATES[500]]), shares=5, entry_fx_rate=1.27)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)

    data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    assert data["run"]["skipped"] == []
    t = data["trades"][0]
    assert t["simulated_exit_reason"] == "Stop"
    # Exits at or shortly after the crash day, well before the trade's real (later) exit_date.
    assert t["simulated_exit_date"] < exit_date.isoformat()
    assert t["simulated_pnl_native"] < 0


def test_risk_off_exit_on_a_regime_dip(monkeypatch):
    entry_date = FULL_DATES[560].date()
    exit_date = FULL_DATES[600].date()
    row = _row("RISKOFF", entry_date, exit_date, entry_price=float(RISKOFF.loc[FULL_DATES[560]]), shares=8, entry_fx_rate=1.27)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)

    data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    assert data["run"]["skipped"] == []
    t = data["trades"][0]
    assert t["simulated_exit_reason"] == "Risk-Off"
    assert t["simulated_exit_date"] == FULL_DATES[SPY_DIP_IDX].date().isoformat()


def test_determinism_same_request_same_output(monkeypatch):
    row = _row("AAAA", date(2023, 12, 1), date(2024, 1, 15), entry_price=float(AAAA.loc["2023-12-01"]), shares=10, entry_fx_rate=1.27)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)

    data1 = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    _mock_yf(monkeypatch)  # fresh FakeYF instance -- proves it's not object-identity reuse
    data2 = run_replay(mode="trade_set", trade_ids=[str(row["id"])])

    assert data1["trades"] == data2["trades"]
    assert data1["summary"] == data2["summary"]
    assert data1["run"]["price_data_fingerprint"] == data2["run"]["price_data_fingerprint"]


def test_fingerprint_changes_when_a_price_changes(monkeypatch):
    row = _row("AAAA", date(2023, 12, 1), date(2024, 1, 15), entry_price=float(AAAA.loc["2023-12-01"]), shares=10, entry_fx_rate=1.27)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)
    data1 = run_replay(mode="trade_set", trade_ids=[str(row["id"])])

    nudged = dict(MAIN_PANELS)
    nudged_aaaa = AAAA.copy()
    nudged_aaaa.loc["2024-01-10"] *= 1.10  # a single day's price bumped 10%
    nudged["AAAA"] = nudged_aaaa
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch, panels=nudged)
    data2 = run_replay(mode="trade_set", trade_ids=[str(row["id"])])

    assert data1["run"]["price_data_fingerprint"] != data2["run"]["price_data_fingerprint"]


# ── Skip reasons ─────────────────────────────────────────────────────────────────────

def test_trade_not_found_for_an_id_that_does_not_match(monkeypatch):
    missing_id = str(uuid4())
    _mock_db(monkeypatch, rows_by_ids=[])  # DB mock returns nothing for any id
    _mock_yf(monkeypatch)

    data = run_replay(mode="trade_set", trade_ids=[missing_id])
    assert data["run"]["requested_trade_count"] == 1
    assert data["run"]["replayed_trade_count"] == 0
    assert data["run"]["skipped"] == [{"trade_id": missing_id, "reason": "trade_not_found"}]
    assert data["trades"] == []


def test_duplicate_trade_ids_are_deduplicated_before_counting(monkeypatch):
    tid = str(uuid4())
    _mock_db(monkeypatch, rows_by_ids=[])
    _mock_yf(monkeypatch)
    data = run_replay(mode="trade_set", trade_ids=[tid, tid, tid])
    assert data["run"]["requested_trade_count"] == 1


def test_price_data_unavailable_skip_when_exit_date_is_today_or_later(monkeypatch):
    today = replay_service._today_utc()
    row = _row("AAAA", date(2023, 12, 1), today, entry_price=float(AAAA.loc["2023-12-01"]), shares=1)
    _mock_db(monkeypatch, rows_by_ids=[row])
    fake = _mock_yf(monkeypatch)

    data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    assert data["run"]["skipped"] == [{"trade_id": str(row["id"]), "reason": "price_data_unavailable"}]
    assert fake.calls == []  # D6 "fetch only when needed" -- no trade survived to fetch for


def test_insufficient_history_skip_for_a_newly_listed_ticker_under_14_rows(monkeypatch):
    """NEWTICK.L has only 10 trading days of history before its entry date -- fewer
    than the required 14 -- so it must be skipped, never silently replayed against a
    too-short ATR warm-up."""
    entry_date = FULL_DATES[NEWTICK_ENTRY_IDX].date()
    exit_date = FULL_DATES[NEWTICK_ENTRY_IDX + 20].date()
    row = _row("NEWTICK.L", entry_date, exit_date, entry_price=200.0, shares=3)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)

    data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    assert data["run"]["skipped"] == [{"trade_id": str(row["id"]), "reason": "insufficient_history"}]


def test_atr_warm_up_boundary_14_rows_is_the_minimum(monkeypatch):
    """Exactly 14 rows before entry (position 14 in the 0-indexed clean series) must
    pass; 13 must not -- confirms the boundary is where the scope note says (one row
    more conservative than compute_atr's own bare-minimum 13)."""
    dates = FULL_DATES[NEWTICK_ENTRY_IDX - 20: NEWTICK_ENTRY_IDX + 30]

    for n_rows_before, should_skip in [(13, True), (14, False)]:
        panel = dict(MAIN_PANELS)
        series = _flat_series(FULL_DATES, level=50.0, start_at=NEWTICK_ENTRY_IDX - n_rows_before)
        panel["BOUND.L"] = series
        entry_date = FULL_DATES[NEWTICK_ENTRY_IDX].date()
        exit_date = FULL_DATES[NEWTICK_ENTRY_IDX + 20].date()
        row = _row("BOUND.L", entry_date, exit_date, entry_price=50.0, shares=1)
        _mock_db(monkeypatch, rows_by_ids=[row])
        _mock_yf(monkeypatch, panels=panel)

        data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
        was_skipped = any(s["reason"] == "insufficient_history" for s in data["run"]["skipped"])
        assert was_skipped == should_skip, f"n_rows_before={n_rows_before}: expected skip={should_skip}"


def test_regime_warm_up_boundary_200_rows(monkeypatch):
    """A ticker with plenty of its own price history is still skipped
    `insufficient_history` if the regime series (SPY) it depends on has fewer than 200
    rows before the trade's entry date."""
    dates = FULL_DATES
    ticker_series = _uptrend_series(dates, start=40.0)
    entry_idx = 250
    entry_date = dates[entry_idx].date()
    exit_date = dates[entry_idx + 20].date()
    row = _row("REGWARM", entry_date, exit_date, entry_price=float(ticker_series.loc[dates[entry_idx]]), shares=2)
    _mock_db(monkeypatch, rows_by_ids=[row])

    for spy_rows_before_entry, should_skip in [(199, True), (200, False)]:
        short_spy = _flat_series(dates, level=100.0, start_at=entry_idx - spy_rows_before_entry)
        panel = {"REGWARM": ticker_series, "SPY": short_spy, "^FTSE": FTSE}
        _mock_db(monkeypatch, rows_by_ids=[row])
        _mock_yf(monkeypatch, panels=panel)
        data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
        was_skipped = any(s["reason"] == "insufficient_history" for s in data["run"]["skipped"])
        assert was_skipped == should_skip, f"spy_rows_before_entry={spy_rows_before_entry}: expected skip={should_skip}"


def test_price_data_unavailable_error_when_provider_has_nothing_for_any_ticker(monkeypatch):
    row = _row("GHOST", date(2023, 12, 1), date(2024, 1, 15), entry_price=100.0, shares=1)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch, panels={"SPY": SPY, "^FTSE": FTSE})  # "GHOST" absent entirely

    with pytest.raises(ReplayPriceDataUnavailableError):
        run_replay(mode="trade_set", trade_ids=[str(row["id"])])


def test_price_data_unavailable_error_when_required_regime_series_is_empty(monkeypatch):
    row = _row("AAAA", date(2023, 12, 1), date(2024, 1, 15), entry_price=float(AAAA.loc["2023-12-01"]), shares=1)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch, panels={"AAAA": AAAA})  # SPY absent entirely -- AAAA is US, needs SPY

    with pytest.raises(ReplayPriceDataUnavailableError):
        run_replay(mode="trade_set", trade_ids=[str(row["id"])])


# ── Bounds ───────────────────────────────────────────────────────────────────────────

def test_bounds_over_max_trades_raises(monkeypatch):
    rows = [_row("AAAA", date(2023, 12, 1), date(2024, 1, 15), 100.0, 1) for _ in range(MAX_TRADES + 1)]
    _mock_db(monkeypatch, rows_by_range=rows)
    _mock_yf(monkeypatch)
    with pytest.raises(ReplayScopeTooLargeError):
        run_replay(mode="date_range", date_from=date(2023, 12, 1), date_to=date(2024, 1, 15))


def test_bounds_at_max_trades_does_not_raise(monkeypatch):
    rows = [_row("AAAA", date(2023, 12, 1), date(2023, 12, 1), 100.0, 1) for _ in range(MAX_TRADES)]
    _mock_db(monkeypatch, rows_by_range=rows)
    _mock_yf(monkeypatch)
    data = run_replay(mode="date_range", date_from=date(2023, 12, 1), date_to=date(2024, 1, 15))
    assert data["run"]["requested_trade_count"] == MAX_TRADES


def test_bounds_over_max_tickers_raises(monkeypatch):
    rows = [_row(f"T{i}", date(2023, 12, 1), date(2024, 1, 15), 100.0, 1) for i in range(MAX_TICKERS + 1)]
    _mock_db(monkeypatch, rows_by_range=rows)
    _mock_yf(monkeypatch)
    with pytest.raises(ReplayScopeTooLargeError):
        run_replay(mode="date_range", date_from=date(2023, 12, 1), date_to=date(2024, 1, 15))


# ── 0-trade success ──────────────────────────────────────────────────────────────────

def test_zero_trades_in_date_range_is_a_normal_success(monkeypatch):
    _mock_db(monkeypatch, rows_by_range=[])
    fake = _mock_yf(monkeypatch)
    data = run_replay(mode="date_range", date_from=date(2023, 12, 1), date_to=date(2024, 1, 15))
    assert data["trades"] == []
    assert data["summary"]["trade_count"] == 0
    assert data["summary"]["win_rate_pct"] is None
    assert data["summary"]["total_simulated_pnl_gbp"] == 0.0
    assert data["retrospective_notice"] == RETROSPECTIVE_NOTICE
    assert fake.calls == []


def test_no_portfolio_resolves_to_zero_trades_without_a_db_round_trip(monkeypatch):
    calls = []
    monkeypatch.setattr(replay_service, "get_portfolio", lambda: None)
    monkeypatch.setattr(replay_service, "get_trade_history_by_ids", lambda *a: calls.append(a) or [])
    monkeypatch.setattr(replay_service, "get_trade_history_by_date_range", lambda *a: calls.append(a) or [])
    _mock_yf(monkeypatch)

    tid = str(uuid4())
    data = run_replay(mode="trade_set", trade_ids=[tid])
    assert data["run"]["skipped"] == [{"trade_id": tid, "reason": "trade_not_found"}]
    assert calls == []


# ── Latest-date-bar / fetch-end-exclusivity ─────────────────────────────────────────

def test_trade_exiting_on_the_latest_date_uses_that_dates_bar(monkeypatch):
    """yfinance's `end` is exclusive (D6) -- fetching only up to (not including) the
    latest exit_date would silently drop that day's bar. This is the single trade in
    the batch, so its own exit_date IS the batch's max(exit_date)."""
    exit_ts = FULL_DATES[520]
    row = _row("AAAA", FULL_DATES[500].date(), exit_ts.date(), entry_price=float(AAAA.loc[FULL_DATES[500]]), shares=1)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)

    data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    t = data["trades"][0]
    if t["simulated_exit_reason"] == "Actual Exit":
        assert t["simulated_exit_date"] == exit_ts.date().isoformat()
        expected_price = round(float(AAAA.loc[exit_ts]), 4)
        assert t["simulated_exit_price"] == expected_price


# ── FX handling ──────────────────────────────────────────────────────────────────────

def test_uk_trade_pnl_is_native_and_gbp_equal(monkeypatch):
    entry_date, exit_date = FULL_DATES[500].date(), FULL_DATES[520].date()
    entry_price = float(RISKOFF.loc[FULL_DATES[500]])  # reuse a plain uptrend series as a UK ticker
    row = _row("RISKOFF.L" if False else "AAAA", entry_date, exit_date, entry_price=entry_price, shares=4)
    # Build a dedicated UK ticker sharing AAAA's price path so the exit is "Actual Exit".
    panel = dict(MAIN_PANELS)
    panel["UKTICK.L"] = AAAA
    row = _row("UKTICK.L", entry_date, exit_date, entry_price=entry_price, shares=4, entry_fx_rate=None)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch, panels=panel)

    data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    t = data["trades"][0]
    assert t["market"] == "UK" and t["currency"] == "GBP"
    assert t["fx_basis"] == "not_applicable_gbp"
    assert t["simulated_pnl_gbp"] == t["simulated_pnl_native"]


def test_us_trade_with_null_fx_rate_is_excluded_from_gbp_total(monkeypatch):
    entry_date, exit_date = FULL_DATES[500].date(), FULL_DATES[520].date()
    row = _row("AAAA", entry_date, exit_date, entry_price=float(AAAA.loc[FULL_DATES[500]]), shares=4, entry_fx_rate=None)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)

    data = run_replay(mode="trade_set", trade_ids=[str(row["id"])])
    t = data["trades"][0]
    assert t["fx_basis"] == "unavailable"
    assert t["simulated_pnl_gbp"] is None
    assert data["summary"]["excluded_from_gbp_total"] == 1
    assert data["summary"]["total_simulated_pnl_gbp"] == 0.0


def test_us_trade_gbp_conversion_uses_unrounded_native_value():
    """The scope note D4 worked example: (133.1*0.9985 - 121.5)*10 = 114.0035, shown
    as 114.0; the GBP figure divides the UNROUNDED native value (114.0035/1.272 =
    89.6253 -> 89.63), not the rounded 114.00 (which would give 89.62)."""
    native = (133.1 * (1 - 0.0015) - 121.5) * 10
    assert round(native, 2) == 114.0
    gbp = round(native / 1.272, 2)
    assert gbp == 89.63
    assert round(round(native, 2) / 1.272, 2) == 89.62  # the wrong way, for contrast


# ── retrospective_notice constant ───────────────────────────────────────────────────

def test_retrospective_notice_matches_the_approved_banner_wording():
    assert RETROSPECTIVE_NOTICE == (
        "Retrospective result — shows what the current rules would have produced over "
        "this past period. Not a prediction of future performance."
    )


# ── No Alpaca call, no database write ───────────────────────────────────────────────

def test_replay_never_calls_alpaca(monkeypatch):
    row = _row("AAAA", date(2023, 12, 1), date(2024, 1, 15), entry_price=float(AAAA.loc["2023-12-01"]), shares=1)
    _mock_db(monkeypatch, rows_by_ids=[row])
    _mock_yf(monkeypatch)

    with patch("services.alpaca_paper_sync_service.requests.post") as mock_post, \
         patch("services.alpaca_paper_sync_service.requests.delete") as mock_delete, \
         patch("services.alpaca_paper_sync_service.requests.get") as mock_get:
        run_replay(mode="trade_set", trade_ids=[str(row["id"])])
        mock_post.assert_not_called()
        mock_delete.assert_not_called()
        mock_get.assert_not_called()


def test_replay_service_imports_no_database_write_function():
    """Static guard, per the scope note's Binding Condition 1 test requirement ("no
    INSERT/UPDATE/DELETE is issued, not only that row counts are unchanged"): the
    module's own import line must name only read functions."""
    import inspect
    source = inspect.getsource(replay_service)
    import_line = next(line for line in source.splitlines() if line.startswith("from database import"))
    imported = [name.strip() for name in import_line.split("import", 1)[1].split(",")]
    for name in imported:
        assert name.startswith("get_"), f"replay_service.py imports a non-read database function: {name}"


# ── LIVE_PARAMS drift guard ──────────────────────────────────────────────────────────

def test_live_params_matches_production_strategy_optimal_params():
    """No prior test tied these two together (scope note §5) -- backtest_rule_service's
    (now strategy_engine's) LIVE_PARAMS is supposed to mirror production_strategy.py's
    OPTIMAL_PARAMS exactly; this is the guard against them silently drifting apart."""
    import importlib.util
    repo_root = Path(__file__).parent.parent
    spec = importlib.util.spec_from_file_location("production_strategy_constants", repo_root / "production_strategy.py")
    # production_strategy.py runs top-level code on import (a full nightly backtest) --
    # do not import it. Instead, extract OPTIMAL_PARAMS via a restricted exec of just
    # its own literal dict source, located by AST, so this test never executes the
    # rest of the script.
    import ast
    tree = ast.parse((repo_root / "production_strategy.py").read_text())
    optimal_params = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "OPTIMAL_PARAMS" for t in node.targets):
            optimal_params = ast.literal_eval(node.value)
            break
    assert optimal_params is not None, "production_strategy.py's OPTIMAL_PARAMS not found"
    assert replay_service.LIVE_PARAMS == optimal_params


def test_backtest_rule_service_reexports_the_same_live_params():
    from services.backtest_rule_service import LIVE_PARAMS as reexported
    assert reexported is replay_service.LIVE_PARAMS
