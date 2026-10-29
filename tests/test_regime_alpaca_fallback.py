"""
SPY market regime falls back to Alpaca bars when Yahoo Finance fails
(ST-02, EPIC-01, v9.14, BLG-BE-192).

`check_market_regime()` used Yahoo Finance only, so a Yahoo outage left the
US regime unmeasured. SPY now falls back to Alpaca daily bars, and the result
records which source produced each reading.
"""
import pytest

import utils.pricing as pricing
import services.alpaca_service as alpaca_service


def _bars(closes):
    return [{"t": f"2026-01-{i:02d}", "o": c, "h": c, "l": c, "c": c, "v": 1} for i, c in enumerate(closes, 1)]


@pytest.fixture(autouse=True)
def _fresh_cache(monkeypatch):
    pricing._market_regime_cache.clear()
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    yield
    pricing._market_regime_cache.clear()


def _yahoo_fails(monkeypatch):
    def fail(ticker):
        raise ValueError(f"No chart result in Yahoo Finance response for {ticker}")
    monkeypatch.setattr(pricing, "_yahoo_fetch_ma200_pair", fail)


def test_spy_regime_computed_from_alpaca_bars_when_yahoo_fails(monkeypatch):
    _yahoo_fails(monkeypatch)
    closes = [400.0] * 199 + [300.0]
    calls = []

    def fake_bars(symbol, limit=30, timeframe="1Day", start=None):
        calls.append((symbol, limit, start))
        return _bars(closes)

    monkeypatch.setattr(alpaca_service, "get_ohlcv_bars", fake_bars)

    result = pricing.check_market_regime()

    assert calls and calls[0][0] == "SPY"
    assert calls[0][2] is not None, "the 200-day MA needs a start date, not only the latest bars"
    assert result["spy_price"] == 300.0
    assert result["spy_ma200"] == pytest.approx((400.0 * 199 + 300.0) / 200)
    assert result["spy_risk_on"] is False, "computed from the Alpaca bars, not defaulted to risk-on"
    assert result["spy_source"] == "alpaca"


def test_alpaca_ma_uses_last_200_closes(monkeypatch):
    closes = [100.0] * 50 + [200.0] * 200
    monkeypatch.setattr(alpaca_service, "get_ohlcv_bars", lambda *a, **k: _bars(closes))
    price, ma200 = pricing._alpaca_fetch_ma200_pair("SPY")
    assert price == 200.0
    assert ma200 == 200.0


def test_regime_records_yahoo_source_when_yahoo_succeeds(monkeypatch):
    monkeypatch.setattr(pricing, "_yahoo_fetch_ma200_pair", lambda ticker: (520.0, 450.0))

    def must_not_call(*a, **k):
        raise AssertionError("Alpaca must not be called when Yahoo Finance succeeds")

    monkeypatch.setattr(alpaca_service, "get_ohlcv_bars", must_not_call)

    result = pricing.check_market_regime()

    assert result["spy_source"] == "yahoo_finance"
    assert result["ftse_source"] == "yahoo_finance"
    assert result["spy_risk_on"] is True


def test_ftse_has_no_alpaca_fallback(monkeypatch):
    def spy_only(ticker):
        if ticker == "SPY":
            return 520.0, 450.0
        raise ValueError("no FTSE data")

    monkeypatch.setattr(pricing, "_yahoo_fetch_ma200_pair", spy_only)
    requested = []
    monkeypatch.setattr(alpaca_service, "get_ohlcv_bars", lambda symbol, **k: requested.append(symbol) or None)

    result = pricing.check_market_regime()

    assert "^FTSE" not in requested
    assert result["ftse_source"] is None


def test_both_sources_failing_keeps_the_existing_fallback(monkeypatch):
    _yahoo_fails(monkeypatch)
    monkeypatch.setattr(alpaca_service, "get_ohlcv_bars", lambda *a, **k: None)

    result = pricing.check_market_regime()

    assert result["spy_source"] is None
    assert result["spy_risk_on"] is True
    assert result["spy_price"] == 0
