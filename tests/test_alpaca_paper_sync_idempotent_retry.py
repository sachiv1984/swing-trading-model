"""
Regression tests for idempotent retry on the Alpaca paper-trading order-open
sync (ST-10, EPIC-02, v8.3, BLG-BE-80).

Prior to this story, `sync_open_paper_position` made a single, unretried POST
to Alpaca's paper API with no `client_order_id` — a retry was unsafe (would
risk a duplicate paper order) and so was correctly never attempted, silently
dropping the paper-sync mirror on any transient failure. It now derives a
deterministic `client_order_id` from the internal position id and applies
`retry_with_backoff`, so a retried call is safe: Alpaca either creates the
order once or rejects the re-submission as a duplicate — either way, exactly
one paper order results.
"""
import requests

import services.alpaca_paper_sync_service as paper_sync


class _FakeResponse:
    def __init__(self, status_code, text="", json_body=None):
        self.status_code = status_code
        self.text = text
        self._json_body = json_body or {}

    def json(self):
        return self._json_body


def _configure_credentials(monkeypatch):
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_API_KEY", "test-key")
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_SECRET_KEY", "test-secret")


def test_client_order_id_deterministic_from_position_id():
    assert paper_sync._client_order_id_for_open("pos-123") == paper_sync._client_order_id_for_open("pos-123")
    assert paper_sync._client_order_id_for_open("pos-123") != paper_sync._client_order_id_for_open("pos-456")


def test_open_succeeds_first_try_includes_client_order_id(monkeypatch):
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    captured = {}

    def fake_post(url, json, headers, timeout):
        captured["payload"] = json
        return _FakeResponse(200)

    monkeypatch.setattr(paper_sync.requests, "post", fake_post)
    paper_sync.sync_open_paper_position("AAPL", 10, "pos-123")
    assert captured["payload"]["client_order_id"] == "paper-open-pos-123"


def test_open_retries_on_connection_error_then_succeeds_no_duplicate(monkeypatch):
    """A retried call with the same client_order_id results in exactly one
    order-creating POST attempt succeeding — no duplicate order (mocked)."""
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}
    client_order_ids_seen = []

    def fake_post(url, json, headers, timeout):
        calls["n"] += 1
        client_order_ids_seen.append(json["client_order_id"])
        if calls["n"] < 2:
            raise requests.exceptions.ConnectionError("network blip")
        return _FakeResponse(200)

    monkeypatch.setattr(paper_sync.requests, "post", fake_post)
    paper_sync.sync_open_paper_position("AAPL", 10, "pos-123")
    assert calls["n"] == 2  # one transient failure, then success — retry happened
    # Every attempt (including the retried one) used the same client_order_id —
    # this is what makes the retry safe against duplicate orders.
    assert client_order_ids_seen == ["paper-open-pos-123", "paper-open-pos-123"]


def test_open_retry_hitting_alpaca_duplicate_rejection_is_not_a_failure(monkeypatch):
    """Simulates the real-world case: the first attempt's order actually landed at
    Alpaca despite the client seeing a network error, so the retry's re-submission
    is rejected by Alpaca as a duplicate client_order_id (422). This must be
    treated as success, not an error — exactly one order exists at Alpaca."""
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_post(url, json, headers, timeout):
        calls["n"] += 1
        if calls["n"] < 2:
            raise requests.exceptions.ConnectionError("client never saw the response")
        return _FakeResponse(422, text='{"code":40010001,"message":"client_order_id must be unique"}')

    monkeypatch.setattr(paper_sync.requests, "post", fake_post)
    # No exception propagates — best-effort contract preserved, and the 422
    # duplicate-rejection is recognised as a safe no-op, not retried further.
    paper_sync.sync_open_paper_position("AAPL", 10, "pos-123")
    assert calls["n"] == 2


def test_open_gives_up_after_persistent_failures_swallows_error(monkeypatch):
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(paper_sync.time, "sleep", lambda *_: None)
    calls = {"n": 0}

    def fake_post(url, json, headers, timeout):
        calls["n"] += 1
        raise requests.exceptions.ConnectionError("still down")

    monkeypatch.setattr(paper_sync.requests, "post", fake_post)
    # Best-effort contract unchanged: never raises to the caller.
    paper_sync.sync_open_paper_position("AAPL", 10, "pos-123")
    assert calls["n"] == 3  # decorator's max_attempts=3 — retries occurred before giving up


def test_open_no_credentials_skips_entirely(monkeypatch):
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_API_KEY", "")
    monkeypatch.setattr(paper_sync, "ALPACA_PAPER_SECRET_KEY", "")
    calls = {"n": 0}

    def fake_post(*args, **kwargs):
        calls["n"] += 1
        return _FakeResponse(200)

    monkeypatch.setattr(paper_sync.requests, "post", fake_post)
    paper_sync.sync_open_paper_position("AAPL", 10, "pos-123")
    assert calls["n"] == 0
