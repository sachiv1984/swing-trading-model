"""
ST-15 (BLG-OPS-217, EPIC-06, v9.17): causes of on-demand Yahoo failures.

1. UK positions stored without ".L" (e.g. "BARC") were priced as US tickers:
   an Alpaca miss, then Yahoo chart/BARC, which returns 404, so GET /positions,
   GET /portfolio and pre-entry validation fell back to the stored price. Staging
   api_call_log, 7 days to 2026-11-13: chart/BARC and chart/LGEN failed 31 of 31.
2. GET /earnings/{ticker} read Yahoo's earningsTimestamp, which keeps the past
   report after it happens; the next report is in earningsTimestampStart/End.
3. Funds have no earnings; their calendar fallback cost two 404 quoteSummary
   calls per lookup.

The fc.yahoo.com cookie 404 is covered in tests/test_api_call_attribution.py.
No network and no database.
"""
from datetime import date, datetime, timezone
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

import services.earnings_service as earnings_service
import services.position_service as position_service
import utils.pricing as pricing


# ---------------------------------------------------------------------------
# 1. UK tickers stored without .L
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ticker,market,expected", [
    ("BARC", "UK", "BARC.L"),
    ("BARC.L", "UK", "BARC.L"),
    ("barc", "uk", "barc.L"),
    ("AAPL", "US", "AAPL"),
    ("AAPL", None, "AAPL"),
    ("BARC.L", None, "BARC.L"),
])
def test_market_symbol(ticker, market, expected):
    assert pricing.market_symbol(ticker, market) == expected


def test_uk_ticker_without_suffix_is_priced_from_yahoo_with_suffix():
    with patch.object(pricing, "_yahoo_get_current_price", return_value=185.5) as yahoo, \
         patch("services.alpaca_service.get_latest_close") as alpaca:
        assert pricing.get_current_price("BARC", "UK") == 185.5
    yahoo.assert_called_once_with("BARC.L")
    alpaca.assert_not_called()


def test_us_ticker_still_tries_alpaca_first():
    with patch.object(pricing, "_yahoo_get_current_price") as yahoo, \
         patch("services.alpaca_service.get_latest_close", return_value=200.0) as alpaca:
        assert pricing.get_current_price("AAPL", "US") == 200.0
    alpaca.assert_called_once_with("AAPL")
    yahoo.assert_not_called()


def test_positions_pass_each_rows_market_to_the_price_lookup():
    row = {
        "id": "pos-1", "portfolio_id": "pf-1", "ticker": "BARC", "market": "UK",
        "entry_date": "2026-10-01", "entry_price": 1.80, "fill_price": 1.80, "fx_rate": None,
        "shares": 100, "current_price": 1.85, "current_stop": 1.70, "initial_stop": 1.60,
        "holding_days": 40, "total_cost": 180.0, "atr": 0.05, "status": "open",
    }
    calls = []

    def fake_price(ticker, market=None):
        calls.append((ticker, market))
        return 190.0

    with patch.object(position_service, "get_portfolio", return_value={"id": "pf-1"}), \
         patch.object(position_service, "get_positions", return_value=[row]), \
         patch.object(position_service, "get_live_fx_rate", return_value=1.30), \
         patch.object(position_service, "get_current_price", side_effect=fake_price), \
         patch.object(position_service, "get_sector_and_industry", return_value=(None, None)):
        out = position_service.get_positions_with_prices()
    assert calls == [("BARC", "UK")]
    assert out[0]["price_is_stale"] is False


# ---------------------------------------------------------------------------
# 2 and 3. Next earnings date
# ---------------------------------------------------------------------------

def _ts(y, m, d, hour_utc=21):
    return int(datetime(y, m, d, hour_utc, 0, tzinfo=timezone.utc).timestamp())


def _earnings(info, today, calendar=None):
    ticker = MagicMock()
    ticker.info = info
    calendar_prop = PropertyMock(return_value=calendar)
    type(ticker).calendar = calendar_prop
    with patch.object(earnings_service.yf, "Ticker", return_value=ticker), \
         patch.object(earnings_service, "us_market_date", return_value=today):
        out = earnings_service.get_earnings("AAPL", "US")
    return out, calendar_prop


def test_next_report_is_read_after_the_past_one():
    """AAPL as Yahoo served it on 2026-11-13: earningsTimestamp is the 2026-11-02
    report, earningsTimestampStart/End the next one on 2027-01-28."""
    info = {
        "earningsTimestamp": _ts(2026, 11, 2),
        "earningsTimestampStart": _ts(2027, 1, 28),
        "earningsTimestampEnd": _ts(2027, 1, 28),
        "quoteType": "EQUITY",
    }
    out, _ = _earnings(info, date(2026, 11, 13))
    assert out["next_earnings_date"] == "2027-01-28"
    assert out["days_until_earnings"] == 76


def test_earliest_upcoming_candidate_wins():
    info = {"earningsTimestampStart": _ts(2026, 11, 20), "earningsTimestampEnd": _ts(2026, 11, 24),
            "earningsTimestamp": _ts(2026, 11, 24)}
    out, _ = _earnings(info, date(2026, 11, 13))
    assert out["next_earnings_date"] == "2026-11-20"
    assert out["days_until_earnings"] == 7


def test_release_today_is_kept_with_zero_days():
    # 21:00 EST on 5 Nov is 02:00 UTC on 6 Nov; viewed on ET 5 Nov.
    info = {"earningsTimestamp": int(datetime(2026, 11, 6, 2, 0, tzinfo=timezone.utc).timestamp())}
    out, _ = _earnings(info, date(2026, 11, 5))
    assert out["next_earnings_date"] == "2026-11-05"
    assert out["days_until_earnings"] == 0


def test_only_past_dates_give_null_without_the_calendar_call():
    """VOD.L as served on 2026-11-13: every field holds the 2026-11-10 report."""
    info = {"earningsTimestamp": _ts(2026, 11, 10, 10), "earningsTimestampStart": _ts(2026, 11, 10, 10)}
    out, calendar_prop = _earnings(info, date(2026, 11, 13))
    assert out["next_earnings_date"] is None
    assert out["days_until_earnings"] is None
    calendar_prop.assert_not_called()


def test_fund_skips_the_calendar_lookup():
    out, calendar_prop = _earnings({"quoteType": "ETF"}, date(2026, 11, 13))
    assert out["next_earnings_date"] is None
    calendar_prop.assert_not_called()


def test_equity_without_info_dates_still_uses_the_calendar():
    import pandas as pd
    cal = pd.DataFrame({"Earnings Date": [pd.Timestamp("2026-12-01")]})
    out, calendar_prop = _earnings({"quoteType": "EQUITY"}, date(2026, 11, 13), calendar=cal)
    assert out["next_earnings_date"] == "2026-12-01"
    assert calendar_prop.called


def test_past_calendar_date_is_not_returned():
    import pandas as pd
    cal = pd.DataFrame({"Earnings Date": [pd.Timestamp("2026-10-22")]})
    out, _ = _earnings({"quoteType": "EQUITY"}, date(2026, 11, 13), calendar=cal)
    assert out["next_earnings_date"] is None


def test_earnings_date_list_and_bare_date_values():
    info = {"earningsDate": [date(2026, 10, 1), date(2026, 12, 2)]}
    out, _ = _earnings(info, date(2026, 11, 13))
    assert out["next_earnings_date"] == "2026-12-02"


def test_non_date_values_are_ignored():
    info = {"earningsTimestamp": True, "earningsTimestampStart": "soon", "earningsTimestampEnd": None}
    out, _ = _earnings(info, date(2026, 11, 13), calendar=None)
    assert out["next_earnings_date"] is None


# ---------------------------------------------------------------------------
# 4. Bursts: shared Ticker.info cache and concurrency cap
#    Production 2026-11-09 15:37-15:38: 471 calls, 418 failed (86% of the
#    week's on-demand failures) when a page fired one earnings lookup per row.
# ---------------------------------------------------------------------------

import threading  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ThreadPoolExecutor  # noqa: E402

import services.sector_service as sector_service  # noqa: E402
from utils import yahoo_info  # noqa: E402

_EQUITY_INFO = {"quoteType": "EQUITY", "sector": "Technology", "industry": "Semis",
                "earningsTimestampStart": _ts(2027, 1, 28), "marketCap": 1}


class _CountingTicker:
    """A yf.Ticker stand-in that counts .info fetches and the peak number
    running at once."""

    def __init__(self, info=None, delay=0.0, fail=False):
        self.info_value = dict(_EQUITY_INFO if info is None else info)
        self.delay = delay
        self.fail = fail
        self.fetches = 0
        self.running = 0
        self.peak = 0
        self.lock = threading.Lock()

    def __call__(self, symbol):
        outer = self

        class _T:
            @property
            def info(self_inner):
                with outer.lock:
                    outer.fetches += 1
                    outer.running += 1
                    outer.peak = max(outer.peak, outer.running)
                try:
                    time.sleep(outer.delay)
                    if outer.fail:
                        raise RuntimeError("401 Invalid Crumb")
                    return dict(outer.info_value)
                finally:
                    with outer.lock:
                        outer.running -= 1

            calendar = None
        return _T()


def _with_fake(fake, fn):
    with patch.object(earnings_service.yf, "Ticker", side_effect=fake), \
         patch.object(sector_service.yf, "Ticker", side_effect=fake), \
         patch.object(earnings_service, "us_market_date", return_value=date(2026, 11, 13)):
        return fn()


def test_burst_of_100_tickers_never_runs_more_than_4_lookups_at_once():
    fake = _CountingTicker(delay=0.02)
    tickers = [f"T{i}" for i in range(100)]

    def burst():
        with ThreadPoolExecutor(max_workers=40) as pool:
            return list(pool.map(lambda t: earnings_service.get_earnings(t, "US"), tickers))

    results = _with_fake(fake, burst)
    assert fake.peak <= yahoo_info.MAX_CONCURRENT_LOOKUPS
    assert fake.peak >= 2  # the cap is the limit, not a serial queue
    assert fake.fetches == 100
    assert all(r["next_earnings_date"] == "2027-01-28" for r in results)


def test_reload_of_the_same_page_costs_no_yahoo_call():
    fake = _CountingTicker()
    tickers = [f"T{i}" for i in range(20)]

    def two_loads():
        first = [earnings_service.get_earnings(t, "US") for t in tickers]
        second = [earnings_service.get_earnings(t, "US") for t in tickers]
        return first, second

    first, second = _with_fake(fake, two_loads)
    assert fake.fetches == 20
    assert first == second


def test_sector_earnings_and_market_cap_share_one_lookup_per_symbol():
    """Research looked up Ticker.info three times per symbol; GET /positions once
    per position per load."""
    fake = _CountingTicker()

    def research_like():
        sector = sector_service.get_sector_and_industry("AAPL", "US")
        earnings = earnings_service.get_earnings("AAPL", "US")
        cap = yahoo_info.get_info("AAPL", lambda: fake("AAPL").info)["marketCap"]
        return sector, earnings, cap

    sector, earnings, cap = _with_fake(fake, research_like)
    assert sector == ("Technology", "Semis")
    assert earnings["next_earnings_date"] == "2027-01-28"
    assert cap == 1
    assert fake.fetches == 1


def test_failed_lookup_is_not_cached():
    fake = _CountingTicker(fail=True)

    def twice():
        a = earnings_service.get_earnings("AAPL", "US")
        b = sector_service.get_sector_and_industry("AAPL", "US")
        return a, b

    a, b = _with_fake(fake, twice)
    assert a["next_earnings_date"] is None and b == (None, None)
    assert fake.fetches == 2
    fake.fail = False
    a2 = _with_fake(fake, lambda: earnings_service.get_earnings("AAPL", "US"))
    assert a2["next_earnings_date"] == "2027-01-28"
    assert fake.fetches == 3


def test_throttled_empty_answer_is_not_cached_as_no_earnings():
    """A throttled lookup can return a dict without quoteType; it must not be
    kept for 12 hours as "no earnings"."""
    fake = _CountingTicker(info={})
    out = _with_fake(fake, lambda: earnings_service.get_earnings("AAPL", "US"))
    assert out["next_earnings_date"] is None
    fake.info_value = dict(_EQUITY_INFO)
    out = _with_fake(fake, lambda: earnings_service.get_earnings("AAPL", "US"))
    assert out["next_earnings_date"] == "2027-01-28"
    assert fake.fetches == 2


def test_cached_date_that_has_passed_is_looked_up_again():
    fake = _CountingTicker(info={"quoteType": "EQUITY", "earningsTimestampStart": _ts(2026, 11, 14)})
    first = _with_fake(fake, lambda: earnings_service.get_earnings("AAPL", "US"))
    assert first["days_until_earnings"] == 1
    with patch.object(earnings_service.yf, "Ticker", side_effect=fake), \
         patch.object(earnings_service, "us_market_date", return_value=date(2026, 11, 15)):
        later = earnings_service.get_earnings("AAPL", "US")
    assert later["next_earnings_date"] is None
    assert fake.fetches == 1  # the Ticker.info answer is reused; only the result is re-derived


def test_days_until_is_counted_on_each_call_from_a_cached_date():
    fake = _CountingTicker()
    _with_fake(fake, lambda: earnings_service.get_earnings("AAPL", "US"))
    with patch.object(earnings_service.yf, "Ticker", side_effect=fake), \
         patch.object(earnings_service, "us_market_date", return_value=date(2026, 11, 20)):
        out = earnings_service.get_earnings("AAPL", "US")
    assert out["days_until_earnings"] == 69
    assert fake.fetches == 1


def test_no_free_slot_within_the_wait_is_a_failed_lookup_not_a_hang():
    with patch.object(yahoo_info, "SLOT_WAIT_SECONDS", 0.05):
        for _ in range(yahoo_info.MAX_CONCURRENT_LOOKUPS):
            assert yahoo_info._slots.acquire(timeout=1)
        try:
            with pytest.raises(yahoo_info.YahooInfoBusy):
                yahoo_info.get_info("AAPL", lambda: dict(_EQUITY_INFO))
            fake = _CountingTicker()
            out = _with_fake(fake, lambda: earnings_service.get_earnings("AAPL", "US"))
            assert out["next_earnings_date"] is None
            assert fake.fetches == 0
        finally:
            for _ in range(yahoo_info.MAX_CONCURRENT_LOOKUPS):
                yahoo_info._slots.release()


def test_ttl_cache_expiry():
    cache = yahoo_info.TTLCache()
    cache.set("k", "v", 10, now=100.0)
    assert cache.get("k", now=109.9) == "v"
    assert cache.get("k", "gone", now=110.0) == "gone"
    assert len(cache) == 0


# ---------------------------------------------------------------------------
# 5. UK prices in pence (EPIC-06 DoQ review round 1, P2)
#    Yahoo chart meta.currency on 2026-11-13: VOD.L GBp 116.0, AZN.L GBp
#    13962.0, BARC.L GBp 430.25, VUSA.L GBP 109.3125. Callers guessed "UK and
#    above 1000 means pence", so VOD at 116p read as GBP 116; pre-entry
#    validation and the compliance recheck did not convert at all.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("price,currency,expected", [
    (116.0, "GBp", 1.16),
    (13962.0, "GBp", 139.62),
    (430.25, "GBX", 4.3025),
    (109.3125, "GBP", 109.3125),
    (1200.0, "GBP", 1200.0),
    (354.88, "USD", 354.88),
    (354.88, None, 354.88),
])
def test_to_major_currency_units(price, currency, expected):
    assert pricing.to_major_currency_units(price, currency) == pytest.approx(expected)


class _ChartResponse:
    def __init__(self, price, currency):
        self.payload = {"chart": {"result": [{"meta": {"regularMarketPrice": price, "currency": currency}}]}}

    def json(self):
        return self.payload


@pytest.mark.parametrize("symbol,price,currency,expected", [
    ("VOD.L", 116.0, "GBp", 1.16),
    ("AZN.L", 13962.0, "GBp", 139.62),
    ("VUSA.L", 109.3125, "GBP", 109.3125),
    ("AAPL", 354.88, "USD", 354.88),
])
def test_yahoo_price_is_returned_in_pounds_for_pence_quotes(monkeypatch, symbol, price, currency, expected):
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    monkeypatch.setattr(pricing.requests, "get", lambda *a, **k: _ChartResponse(price, currency))
    assert pricing._yahoo_get_current_price(symbol) == pytest.approx(expected)


def _uk_row(ticker, entry, stored):
    return {
        "id": f"pos-{ticker}", "portfolio_id": "pf-1", "ticker": ticker, "market": "UK",
        "entry_date": "2026-10-01", "entry_price": entry, "fill_price": entry, "fx_rate": None,
        "shares": 100, "current_price": stored, "current_stop": entry * 0.9, "initial_stop": entry * 0.85,
        "holding_days": 40, "total_cost": entry * 100, "atr": entry * 0.03, "status": "open",
    }


@pytest.mark.parametrize("live_pounds", [1.16, 139.62, 1200.0])
def test_positions_use_the_pounds_price_as_is(live_pounds):
    """No caller re-divides: 1.16 stays 1.16 (was read as 116 when Yahoo gave
    116p), and a pounds price above 1000 is not divided again."""
    row = _uk_row("VOD.L", entry=1.10, stored=1.12)
    with patch.object(position_service, "get_portfolio", return_value={"id": "pf-1"}), \
         patch.object(position_service, "get_positions", return_value=[row]), \
         patch.object(position_service, "get_live_fx_rate", return_value=1.30), \
         patch.object(position_service, "get_current_price", return_value=live_pounds), \
         patch.object(position_service, "get_sector_and_industry", return_value=(None, None)):
        out = position_service.get_positions_with_prices()
    assert out[0]["current_price_native"] == pytest.approx(live_pounds)


def test_pre_entry_uk_cash_check_uses_pounds():
    """BARC typed without .L, 1,000 shares at 430.25p = GBP 4,302.50, within GBP 10,000."""
    from routers import pre_entry_validation

    def fake_get(*a, **k):
        assert a[0].endswith("/BARC.L")
        return _ChartResponse(430.25, "GBp")

    with patch("database.get_portfolio", return_value={"id": "pf-1", "cash": 10_000.0}), \
         patch.object(pricing.requests, "get", side_effect=fake_get), \
         patch.object(pricing.time, "sleep", lambda *_: None):
        result = pre_entry_validation._check_cash_constraint("BARC", "UK", 1000)
    assert result["status"] == "pass"
    assert result["estimated_cost_gbp"] == pytest.approx(4302.50)


class _OkChart(_ChartResponse):
    ok = True


@pytest.mark.parametrize("symbol,price,currency,expected", [
    ("VOD.L", 116.0, "GBp", 1.16),
    ("VUSA.L", 109.3125, "GBP", 109.3125),
    ("VOD.L", 116.0, None, 1.16),  # no currency given: pence, as before
])
def test_research_price_uses_the_quote_currency(symbol, price, currency, expected):
    from routers import research
    payload = _OkChart(price, currency)
    if currency is None:
        del payload.payload["chart"]["result"][0]["meta"]["currency"]
    with patch.object(research.requests, "get", return_value=payload), \
         patch.object(research.time, "sleep", lambda *_: None):
        out = research._get_price_data(symbol, "UK")
    assert out["price"] == pytest.approx(expected)
