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
