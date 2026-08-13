"""
Regression tests for retry/backoff on the Claude ("Gemini") thesis-generation
call site (ST-10, EPIC-04, v8.7, BLG-BE-89).

Prior to this story, `services.gemini_service._call_claude()` — the single
call site both `generate_full_plan()` and `generate_setup_thesis()` route
through — made a single, unretried Anthropic API call. It now wraps that
call in the same shared `retry_with_backoff` decorator used by the other
BLG-BE-57 pattern call sites (see `tests/test_regime_retry_backoff.py`,
`tests/test_retry_backoff.py`), retrying on timeout, connection error,
rate-limit, and transient 5xx (`InternalServerError`) — the three failure
modes this story's AC names — while NOT retrying 4xx client errors
(`BadRequestError`, `AuthenticationError`, etc.), where a retry cannot
produce a different outcome.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import httpx
import anthropic

import services.gemini_service as gemini_service  # noqa: E402


def _request():
    return httpx.Request("POST", "https://api.anthropic.com/v1/messages")


def _rate_limit_error():
    return anthropic.RateLimitError(
        "rate limited", response=httpx.Response(429, request=_request()), body=None
    )


def _timeout_error():
    return anthropic.APITimeoutError(request=_request())


def _connection_error():
    return anthropic.APIConnectionError(request=_request())


def _server_error():
    return anthropic.InternalServerError(
        "server error", response=httpx.Response(500, request=_request()), body=None
    )


def _bad_request_error():
    return anthropic.BadRequestError(
        "bad request", response=httpx.Response(400, request=_request()), body=None
    )


def _mock_anthropic_client(responses):
    """responses: list of return values or exceptions to raise, one per call,
    in order. The real anthropic.Anthropic().messages.create(...) call is
    what gets replaced."""
    mock_client = MagicMock()
    mock_client.messages.create.side_effect = responses
    return mock_client


def _usage_response(text="thesis text"):
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    resp.usage = MagicMock(input_tokens=10, output_tokens=5)
    return resp


class TestCallClaudeRetryBackoff:
    def test_succeeds_first_try_no_retry(self):
        # No failure injected -- succeeds on the first attempt, so
        # retry_with_backoff never sleeps; no need to patch time.sleep.
        mock_client = _mock_anthropic_client([_usage_response("hello")])
        with patch.object(anthropic, "Anthropic", return_value=mock_client):
            text, usage = gemini_service._call_claude("prompt")
        assert text == "hello"
        assert mock_client.messages.create.call_count == 1

    def test_retries_on_timeout_then_succeeds(self):
        mock_client = _mock_anthropic_client([_timeout_error(), _usage_response("hello")])
        with patch.object(anthropic, "Anthropic", return_value=mock_client), \
             patch("utils.retry.time.sleep", lambda *_: None):
            text, usage = gemini_service._call_claude("prompt")
        assert text == "hello"
        assert mock_client.messages.create.call_count == 2

    def test_retries_on_rate_limit_then_succeeds(self):
        mock_client = _mock_anthropic_client([_rate_limit_error(), _usage_response("hello")])
        with patch.object(anthropic, "Anthropic", return_value=mock_client), \
             patch("utils.retry.time.sleep", lambda *_: None):
            text, usage = gemini_service._call_claude("prompt")
        assert text == "hello"
        assert mock_client.messages.create.call_count == 2

    def test_retries_on_transient_5xx_then_succeeds(self):
        mock_client = _mock_anthropic_client([_server_error(), _server_error(), _usage_response("hello")])
        with patch.object(anthropic, "Anthropic", return_value=mock_client), \
             patch("utils.retry.time.sleep", lambda *_: None):
            text, usage = gemini_service._call_claude("prompt")
        assert text == "hello"
        assert mock_client.messages.create.call_count == 3  # max_attempts=3, succeeds on the last

    def test_retries_on_connection_error_then_succeeds(self):
        mock_client = _mock_anthropic_client([_connection_error(), _usage_response("hello")])
        with patch.object(anthropic, "Anthropic", return_value=mock_client), \
             patch("utils.retry.time.sleep", lambda *_: None):
            text, usage = gemini_service._call_claude("prompt")
        assert text == "hello"
        assert mock_client.messages.create.call_count == 2

    def test_gives_up_after_persistent_transient_failures_and_raises(self):
        mock_client = _mock_anthropic_client([_server_error(), _server_error(), _server_error()])
        with patch.object(anthropic, "Anthropic", return_value=mock_client), \
             patch("utils.retry.time.sleep", lambda *_: None):
            try:
                gemini_service._call_claude("prompt")
                assert False, "expected InternalServerError to propagate after exhausting retries"
            except anthropic.InternalServerError:
                pass
        assert mock_client.messages.create.call_count == 3  # max_attempts=3, all exhausted

    def test_bad_request_error_not_retried(self):
        """A 4xx client error (malformed request) is not in the retryable set
        -- retrying it 3x would just repeat the same failure with added
        latency, per this story's own AC framing (only timeout/rate-limit/
        transient 5xx are retried)."""
        mock_client = _mock_anthropic_client([_bad_request_error()])
        with patch.object(anthropic, "Anthropic", return_value=mock_client):
            try:
                gemini_service._call_claude("prompt")
                assert False, "expected BadRequestError to propagate immediately"
            except anthropic.BadRequestError:
                pass
        assert mock_client.messages.create.call_count == 1  # no retry attempted


def test_generate_setup_thesis_surfaces_graceful_error_after_retries_exhausted(monkeypatch):
    """End-to-end: generate_setup_thesis() already catches _call_claude()'s
    final raised exception and returns {"available": False, "error": ...}
    (unchanged pre-existing behaviour) -- confirms the retry decorator
    doesn't break that graceful-degradation contract once attempts are
    exhausted."""
    monkeypatch.setattr(gemini_service, "ANTHROPIC_API_KEY", "test-key")
    mock_client = _mock_anthropic_client([_server_error(), _server_error(), _server_error()])
    with patch.object(anthropic, "Anthropic", return_value=mock_client), \
         patch("utils.retry.time.sleep", lambda *_: None):
        result = gemini_service.generate_setup_thesis(ticker="AAPL", market="US")
    assert result["available"] is False
    assert "Claude API error" in result["error"]
    assert mock_client.messages.create.call_count == 3
