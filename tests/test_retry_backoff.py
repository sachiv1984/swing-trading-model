"""
Unit tests for the shared retry/backoff decorator (ST-09, EPIC-09, v7.8, BLG-BE-71).

Covers the decorator itself (backend/utils/retry.py) and its application to
the highest-traffic external call site, `utils.pricing._yahoo_get_current_price`
(proof-of-pattern migration, RISK-02).
"""
import requests
import pytest

from utils.retry import retry_with_backoff
import utils.pricing as pricing


# ---------------------------------------------------------------------------
# retry_with_backoff decorator
# ---------------------------------------------------------------------------

def test_succeeds_on_first_attempt_no_retry():
    sleeps = []
    calls = {"n": 0}

    @retry_with_backoff(max_attempts=3, base_delay=1.0, sleep_fn=sleeps.append)
    def fn():
        calls["n"] += 1
        return "ok"

    assert fn() == "ok"
    assert calls["n"] == 1
    assert sleeps == []  # no retry needed, no sleep called


def test_retries_then_succeeds():
    sleeps = []
    calls = {"n": 0}

    @retry_with_backoff(max_attempts=3, base_delay=1.0, sleep_fn=sleeps.append)
    def fn():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("transient")
        return "ok"

    assert fn() == "ok"
    assert calls["n"] == 3
    assert sleeps == [1.0, 2.0]  # exponential backoff, one sleep per failed attempt


def test_exhausts_attempts_and_reraises():
    sleeps = []
    calls = {"n": 0}

    @retry_with_backoff(max_attempts=3, base_delay=1.0, sleep_fn=sleeps.append)
    def fn():
        calls["n"] += 1
        raise ValueError("always fails")

    with pytest.raises(ValueError, match="always fails"):
        fn()
    assert calls["n"] == 3
    assert sleeps == [1.0, 2.0]  # no sleep after the final failed attempt


def test_delay_caps_at_max_delay():
    sleeps = []
    calls = {"n": 0}

    @retry_with_backoff(max_attempts=5, base_delay=10.0, max_delay=15.0, sleep_fn=sleeps.append)
    def fn():
        calls["n"] += 1
        raise ValueError("fails")

    with pytest.raises(ValueError):
        fn()
    # 5 attempts -> 4 sleeps (none after the final attempt):
    # 10.0, min(20.0,15.0)=15.0, min(30.0,15.0)=15.0, min(30.0,15.0)=15.0
    assert sleeps == [10.0, 15.0, 15.0, 15.0]


def test_non_retryable_exception_propagates_immediately():
    sleeps = []
    calls = {"n": 0}

    @retry_with_backoff(max_attempts=3, base_delay=1.0, sleep_fn=sleeps.append,
                         retryable_exceptions=(requests.exceptions.RequestException,))
    def fn():
        calls["n"] += 1
        raise ValueError("not a retryable type")

    with pytest.raises(ValueError):
        fn()
    assert calls["n"] == 1  # no retry — ValueError isn't in retryable_exceptions
    assert sleeps == []


# ---------------------------------------------------------------------------
# Proof-of-pattern migration: utils.pricing._yahoo_get_current_price
# ---------------------------------------------------------------------------

class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def _valid_payload(price=123.45):
    return {"chart": {"result": [{"meta": {"regularMarketPrice": price}}]}}


def test_yahoo_price_succeeds_first_try(monkeypatch):
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        return _FakeResponse(_valid_payload(200.0))

    monkeypatch.setattr(pricing.requests, "get", fake_get)
    assert pricing._yahoo_get_current_price("AAPL") == 200.0
    assert calls["n"] == 1


def test_yahoo_price_retries_on_connection_error_then_succeeds(monkeypatch):
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] < 2:
            raise requests.exceptions.ConnectionError("network blip")
        return _FakeResponse(_valid_payload(150.0))

    monkeypatch.setattr(pricing.requests, "get", fake_get)
    assert pricing._yahoo_get_current_price("MSFT") == 150.0
    assert calls["n"] == 2  # one transient failure, then success


def test_yahoo_price_gives_up_after_persistent_connection_errors(monkeypatch):
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        raise requests.exceptions.ConnectionError("still down")

    monkeypatch.setattr(pricing.requests, "get", fake_get)
    # Caller-facing contract unchanged: returns None on failure, never raises.
    assert pricing._yahoo_get_current_price("TSLA") is None
    assert calls["n"] == 3  # decorator's max_attempts=3 for this call site


def test_yahoo_price_no_data_in_response_not_retried(monkeypatch):
    monkeypatch.setattr(pricing.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        return _FakeResponse({"chart": {"result": []}})  # well-formed, no usable price

    monkeypatch.setattr(pricing.requests, "get", fake_get)
    assert pricing._yahoo_get_current_price("DELISTED") is None
    assert calls["n"] == 1  # ValueError is not in retryable_exceptions — no retry
