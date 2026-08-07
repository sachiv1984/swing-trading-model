"""
Regression tests for 429/backoff handling on the Alpaca paper-trading
close and positions-fetch sync call sites (ST-11, EPIC-03, v8.4, BLG-BE-83).

Prior to this story, `sync_close_paper_position` and `get_paper_positions`
made a single, unretried HTTP call each -- any transient/429 failure was
either silently dropped (close) or immediately raised to the caller
(positions). Both now retry via the shared `retry_with_backoff` decorator
(same 3-attempt pattern already used by `sync_open_paper_position`, ST-10
BLG-BE-80, v8.3) before falling back to their existing behaviour:
`sync_close_paper_position` still logs-and-swallows (best-effort, never
raises); `get_paper_positions` still raises after retries are exhausted
(the router's caller converts this to a 500) -- neither disposition changed.
"""
import requests

import services.alpaca_paper_sync_service as paper_sync


class _FakeResponse:
    def __init__(self, status_code, text="", json_body=None):
        self.status_code = status_code
        self.text = text
        self._json_body = json_body if json_body is not None else []

    def json(self):
        return self._json_body

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")


def _configure_credentials(monkeypatch):
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_API_KEY", "test-key")
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_SECRET_KEY", "test-secret")


# ---------------------------------------------------------------------------
# sync_close_paper_position — retry before best-effort swallow
# ---------------------------------------------------------------------------

def test_close_succeeds_first_try(monkeypatch):
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_delete(url, headers, timeout):
        calls["n"] += 1
        return _FakeResponse(200)

    monkeypatch.setattr(paper_sync.requests, "delete", fake_delete)
    paper_sync.sync_close_paper_position("AAPL")
    assert calls["n"] == 1


def test_close_retries_on_429_then_succeeds(monkeypatch):
    """Retry attempts occur before the close call gives up -- AC-03."""
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_delete(url, headers, timeout):
        calls["n"] += 1
        if calls["n"] < 2:
            return _FakeResponse(429, text="rate limited")
        return _FakeResponse(200)

    monkeypatch.setattr(paper_sync.requests, "delete", fake_delete)
    paper_sync.sync_close_paper_position("AAPL")
    assert calls["n"] == 2  # one 429, then success -- retry happened before fallback


def test_close_treats_404_as_success_not_a_retryable_failure(monkeypatch):
    """No paper position to close is a legitimate outcome -- must not retry."""
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_delete(url, headers, timeout):
        calls["n"] += 1
        return _FakeResponse(404)

    monkeypatch.setattr(paper_sync.requests, "delete", fake_delete)
    paper_sync.sync_close_paper_position("AAPL")
    assert calls["n"] == 1  # 404 is not retried


def test_close_gives_up_after_persistent_failures_swallows_error(monkeypatch):
    """Best-effort contract unchanged: never raises to the caller, even after
    retries are exhausted."""
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_delete(url, headers, timeout):
        calls["n"] += 1
        raise requests.exceptions.ConnectionError("still down")

    monkeypatch.setattr(paper_sync.requests, "delete", fake_delete)
    paper_sync.sync_close_paper_position("AAPL")  # must not raise
    assert calls["n"] == 3  # decorator's max_attempts=3 -- retries before giving up


def test_close_no_credentials_skips_entirely(monkeypatch):
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_API_KEY", "")
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_SECRET_KEY", "")
    calls = {"n": 0}

    def fake_delete(*args, **kwargs):
        calls["n"] += 1
        return _FakeResponse(200)

    monkeypatch.setattr(paper_sync.requests, "delete", fake_delete)
    paper_sync.sync_close_paper_position("AAPL")
    assert calls["n"] == 0


# ---------------------------------------------------------------------------
# get_paper_positions — retry before existing raise-to-caller behaviour
# ---------------------------------------------------------------------------

def test_positions_succeeds_first_try(monkeypatch):
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(url, headers, timeout):
        calls["n"] += 1
        return _FakeResponse(200, json_body=[])

    monkeypatch.setattr(paper_sync.requests, "get", fake_get)
    result = paper_sync.get_paper_positions()
    assert calls["n"] == 1
    assert result == {"paper_tracking_enabled": True, "positions": []}


def test_positions_retries_on_429_then_succeeds(monkeypatch):
    """Retry attempts occur before the positions fetch gives up -- AC-03."""
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(url, headers, timeout):
        calls["n"] += 1
        if calls["n"] < 2:
            return _FakeResponse(429, text="rate limited")
        return _FakeResponse(200, json_body=[])

    monkeypatch.setattr(paper_sync.requests, "get", fake_get)
    result = paper_sync.get_paper_positions()
    assert calls["n"] == 2  # one 429, then success -- retry happened before fallback
    assert result["paper_tracking_enabled"] is True


def test_positions_gives_up_after_persistent_failures_still_raises(monkeypatch):
    """Existing raise-to-caller behaviour unchanged -- the router converts
    this to a 500. Retries occur before the final raise."""
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_get(url, headers, timeout):
        calls["n"] += 1
        raise requests.exceptions.ConnectionError("still down")

    monkeypatch.setattr(paper_sync.requests, "get", fake_get)
    try:
        paper_sync.get_paper_positions()
        assert False, "expected an exception to propagate"
    except requests.exceptions.RequestException:
        pass
    assert calls["n"] == 3  # decorator's max_attempts=3 -- retries before giving up


def test_positions_no_credentials_skips_entirely(monkeypatch):
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_API_KEY", "")
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_SECRET_KEY", "")
    calls = {"n": 0}

    def fake_get(*args, **kwargs):
        calls["n"] += 1
        return _FakeResponse(200, json_body=[])

    monkeypatch.setattr(paper_sync.requests, "get", fake_get)
    result = paper_sync.get_paper_positions()
    assert calls["n"] == 0
    assert result == {"paper_tracking_enabled": False}
