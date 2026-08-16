"""
Regression tests for retry/backoff on the market-regime call sites (ST-09,
EPIC-02, v8.3, BLG-BE-79).

Prior to this story, `utils.pricing.check_market_regime`'s inner `get_ma200`
and `services.screener_batch_service._fetch_index_regime` each made a single,
unretried Yahoo Finance request and fell back to a default (risk-on / None)
on any failure — including transient network blips that a retry would have
recovered from. Both now wrap their network call in `retry_with_backoff`
(same shared decorator and pattern as `utils.pricing._yahoo_get_current_price`,
see `tests/test_retry_backoff.py`), while preserving the exact existing
fallback behaviour once attempts are exhausted.
"""
import requests

import utils.pricing as pricing
import services.screener_batch_service as screener_batch_service


class _FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


def _valid_chart_payload(price=520.0, ma_close=450.0, n_closes=250):
    return {
        "chart": {
            "result": [
                {
                    "meta": {"regularMarketPrice": price},
                    "indicators": {"quote": [{"close": [ma_close] * n_closes}]},
                }
            ]
        }
    }


# ---------------------------------------------------------------------------
# utils.pricing.check_market_regime / get_ma200 (via _yahoo_fetch_ma200_pair)
# ---------------------------------------------------------------------------

def test_ma200_succeeds_first_try(monkeypatch):
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        return _FakeResponse(_valid_chart_payload(price=520.0, ma_close=450.0))

    monkeypatch.setattr(pricing.requests, "get", fake_get)
    current, ma200 = pricing._yahoo_fetch_ma200_pair("SPY")
    assert current == 520.0
    assert ma200 == 450.0
    assert calls["n"] == 1


def test_ma200_retries_on_connection_error_then_succeeds(monkeypatch):
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] < 2:
            raise requests.exceptions.ConnectionError("network blip")
        return _FakeResponse(_valid_chart_payload(price=520.0, ma_close=450.0))

    monkeypatch.setattr(pricing.requests, "get", fake_get)
    current, ma200 = pricing._yahoo_fetch_ma200_pair("SPY")
    assert (current, ma200) == (520.0, 450.0)
    assert calls["n"] == 2  # one transient failure, then success — retry happened before result


def test_check_market_regime_defaults_to_risk_on_after_persistent_failures(monkeypatch):
    """End-to-end: check_market_regime() falls back exactly as before once retries
    (ST-09's decorator, 3 attempts per index) are exhausted."""
    # check_market_regime() now caches its result for 5 minutes (BLG-BE-25,
    # consolidated here BLG-BE-97 v8.8 ST-07) — clear any leftover cache
    # entry from an earlier test in this session before asserting a fresh
    # fetch happens.
    pricing._market_regime_cache.clear()
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        raise requests.exceptions.ConnectionError("still down")

    monkeypatch.setattr(pricing.requests, "get", fake_get)
    result = pricing.check_market_regime()
    assert result["spy_risk_on"] is True  # unchanged fallback behaviour
    assert result["ftse_risk_on"] is True
    # 2 indices (SPY, FTSE) x 3 attempts each = 6 — retry attempts occurred before fallback
    assert calls["n"] == 6


def test_ma200_no_chart_data_not_retried(monkeypatch):
    # See cache-clear note in test_check_market_regime_defaults_to_risk_on_after_persistent_failures.
    pricing._market_regime_cache.clear()
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        return _FakeResponse({"chart": {"result": []}})  # well-formed, no usable data

    monkeypatch.setattr(pricing.requests, "get", fake_get)
    result = pricing.check_market_regime()
    assert result["spy_risk_on"] is True  # falls back, unchanged behaviour
    assert calls["n"] == 2  # 1 attempt per index (SPY, FTSE) — no retry on ValueError


# ---------------------------------------------------------------------------
# services.screener_batch_service._fetch_index_regime (via _fetch_index_regime_raw)
# ---------------------------------------------------------------------------

def test_fetch_index_regime_retries_on_connection_error_then_succeeds(monkeypatch):
    monkeypatch.setattr(screener_batch_service.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] < 3:
            raise requests.exceptions.ConnectionError("network blip")
        return _FakeResponse(_valid_chart_payload(price=520.0, ma_close=450.0))

    monkeypatch.setattr(screener_batch_service.requests, "get", fake_get)
    result = screener_batch_service._fetch_index_regime("SPY")
    assert result is not None
    assert result["regime_status"] == "risk_on"
    assert calls["n"] == 3  # 2 transient failures, then success — retries happened before result


def test_fetch_index_regime_gives_up_after_persistent_failures_returns_none(monkeypatch):
    monkeypatch.setattr(screener_batch_service.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        raise requests.exceptions.ConnectionError("still down")

    monkeypatch.setattr(screener_batch_service.requests, "get", fake_get)
    result = screener_batch_service._fetch_index_regime("SPY")
    assert result is None  # unchanged fallback behaviour (caller treats None as risk_off)
    assert calls["n"] == 3  # decorator's max_attempts=3 — retry attempts occurred before fallback


def test_fetch_index_regime_http_error_not_retried(monkeypatch):
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        return _FakeResponse({}, status_code=500)

    monkeypatch.setattr(screener_batch_service.requests, "get", fake_get)
    result = screener_batch_service._fetch_index_regime("SPY")
    assert result is None
    assert calls["n"] == 1  # ValueError (non-200) is not retryable — matches pre-ST-09 behaviour
