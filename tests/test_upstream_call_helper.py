"""
Shared upstream-call helper tests (ST-13, EPIC-03, v9.6, BLG-BE-122).

Covers:
  - utils.upstream_call's per-provider timeout/retry-budget config
  - bounded_upstream_call() decorator: succeeds first try, retries then
    succeeds, exhausts and re-raises, non-retryable exception propagates
    immediately (no retry)
  - anthropic_retryable_exceptions() resolves the expected SDK classes
  - The two real, previously-unretried nightly-stop-update-path call sites
    this story fixes: utils.pricing.get_live_fx_rate (via its new
    _yahoo_fetch_fx_rate helper) now retries transient failures instead of
    falling straight back to DEFAULT_FX_RATE on the first blip; and a
    representative Anthropic call site (services.ai_service.ai_chat)
    gains the same retry/timeout coverage already proven for
    gemini_service.py/debrief_service.py.

CI-safe: no live network calls; requests.get / anthropic client mocked.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
# ai_service.py's success path does a bare `from ai_output_sampling_service
# import maybe_sample_output` (backend/services/ai_output_sampling_service.py),
# which only resolves if backend/services itself is on sys.path -- same
# setup already used by tests/test_plan_vs_reality.py and
# tests/test_position_lifecycle.py for the same reason.
sys.path.insert(0, str(Path(__file__).parent.parent / "backend" / "services"))

from utils.upstream_call import (  # noqa: E402
    UPSTREAM_RETRY_BUDGETS,
    UPSTREAM_TIMEOUTS,
    anthropic_retryable_exceptions,
    bounded_upstream_call,
    get_retry_budget,
    get_timeout,
)


# ---------------------------------------------------------------------------
# Config lookups
# ---------------------------------------------------------------------------

class TestUpstreamConfig:
    @pytest.mark.parametrize("provider", ["yfinance", "yfinance_history", "alpaca", "anthropic"])
    def test_get_timeout_known_provider(self, provider):
        assert get_timeout(provider) == UPSTREAM_TIMEOUTS[provider]
        assert get_timeout(provider) > 0

    def test_get_timeout_unknown_provider_raises(self):
        with pytest.raises(KeyError):
            get_timeout("not_a_real_provider")

    @pytest.mark.parametrize("provider", ["yfinance", "alpaca", "anthropic"])
    def test_get_retry_budget_known_provider(self, provider):
        budget = get_retry_budget(provider)
        assert budget == UPSTREAM_RETRY_BUDGETS[provider]
        assert budget["max_attempts"] >= 1
        assert budget["base_delay"] > 0

    def test_anthropic_retry_budget_is_conservative(self):
        """AC note (sprint_backlog.md ST-13): a retry budget on Anthropic
        calls re-issues paid inference -- must stay within existing AI
        cost gating. Confirmed here as a concrete, checkable bound rather
        than just a comment: not larger than yfinance/Alpaca's budget."""
        anthropic_budget = get_retry_budget("anthropic")
        yfinance_budget = get_retry_budget("yfinance")
        assert anthropic_budget["max_attempts"] <= yfinance_budget["max_attempts"]


# ---------------------------------------------------------------------------
# bounded_upstream_call() decorator
# ---------------------------------------------------------------------------

class TestBoundedUpstreamCallDecorator:
    def test_succeeds_first_try_no_retry(self):
        calls = {"n": 0}

        @bounded_upstream_call("yfinance", retryable_exceptions=(ValueError,))
        def fn():
            calls["n"] += 1
            return "ok"

        assert fn() == "ok"
        assert calls["n"] == 1

    def test_retries_then_succeeds(self):
        calls = {"n": 0}

        @bounded_upstream_call("yfinance", retryable_exceptions=(ValueError,))
        def fn():
            calls["n"] += 1
            if calls["n"] < 3:
                raise ValueError("transient")
            return "ok"

        with patch("utils.retry.time.sleep", lambda *_: None):
            assert fn() == "ok"
        assert calls["n"] == 3  # yfinance budget: max_attempts=3

    def test_exhausts_retry_budget_and_reraises(self):
        calls = {"n": 0}

        @bounded_upstream_call("anthropic", retryable_exceptions=(ValueError,))
        def fn():
            calls["n"] += 1
            raise ValueError("always fails")

        with patch("utils.retry.time.sleep", lambda *_: None):
            with pytest.raises(ValueError, match="always fails"):
                fn()
        assert calls["n"] == get_retry_budget("anthropic")["max_attempts"]

    def test_non_retryable_exception_propagates_immediately(self):
        calls = {"n": 0}

        @bounded_upstream_call("yfinance", retryable_exceptions=(ConnectionError,))
        def fn():
            calls["n"] += 1
            raise ValueError("not in the retryable set")

        with pytest.raises(ValueError):
            fn()
        assert calls["n"] == 1  # no retry attempted


# ---------------------------------------------------------------------------
# anthropic_retryable_exceptions()
# ---------------------------------------------------------------------------

class TestAnthropicRetryableExceptions:
    def test_includes_expected_transient_classes(self):
        import anthropic

        classes = anthropic_retryable_exceptions()
        assert anthropic.APITimeoutError in classes
        assert anthropic.APIConnectionError in classes
        assert anthropic.RateLimitError in classes
        assert anthropic.InternalServerError in classes

    def test_excludes_4xx_client_error_classes(self):
        import anthropic

        classes = anthropic_retryable_exceptions()
        assert anthropic.BadRequestError not in classes
        assert anthropic.AuthenticationError not in classes


# ---------------------------------------------------------------------------
# Real call site: utils.pricing.get_live_fx_rate (nightly stop-update path)
# ---------------------------------------------------------------------------

class TestGetLiveFxRateRetry:
    """Prior to ST-13, get_live_fx_rate() made a single, unretried request
    and fell straight back to DEFAULT_FX_RATE on any failure, including a
    transient network blip a retry would have recovered from."""

    def _reset_cache(self):
        import utils.pricing as pricing
        pricing._fx_cache["rate"] = None
        pricing._fx_cache["expires_at"] = 0.0

    def _chart_response(self, rate: float):
        resp = MagicMock()
        resp.json.return_value = {
            "chart": {"result": [{"meta": {"regularMarketPrice": rate}}]}
        }
        return resp

    def test_retries_on_transient_failure_then_succeeds(self):
        import requests
        import utils.pricing as pricing

        self._reset_cache()
        calls = {"n": 0}

        def fake_get(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] < 2:
                raise requests.exceptions.ConnectionError("transient blip")
            return self._chart_response(1.4321)

        with patch.object(pricing.requests, "get", side_effect=fake_get), \
             patch("utils.retry.time.sleep", lambda *_: None):
            rate = pricing.get_live_fx_rate()

        assert rate == 1.4321
        assert calls["n"] == 2  # one transient failure, then success

    def test_exhausts_retries_then_falls_back_to_default(self):
        import requests
        import utils.pricing as pricing

        self._reset_cache()
        calls = {"n": 0}

        def fake_get(*args, **kwargs):
            calls["n"] += 1
            raise requests.exceptions.ConnectionError("persistent failure")

        with patch.object(pricing.requests, "get", side_effect=fake_get), \
             patch("utils.retry.time.sleep", lambda *_: None):
            rate = pricing.get_live_fx_rate()

        assert rate == pricing.DEFAULT_FX_RATE
        assert calls["n"] == get_retry_budget("yfinance")["max_attempts"]

    def test_yahoo_fetch_fx_rate_uses_configured_timeout(self):
        import utils.pricing as pricing

        self._reset_cache()
        with patch.object(pricing.requests, "get", return_value=self._chart_response(1.5)) as mock_get, \
             patch("utils.retry.time.sleep", lambda *_: None):
            pricing.get_live_fx_rate()

        assert mock_get.call_args.kwargs["timeout"] == get_timeout("yfinance")


# ---------------------------------------------------------------------------
# Real call site: services.ai_service.ai_chat (Anthropic, previously
# entirely unretried)
# ---------------------------------------------------------------------------

class TestAiChatRetryAndTimeout:
    def _mock_response(self, text="ok"):
        content_block = MagicMock()
        content_block.text = text
        usage = MagicMock(input_tokens=10, output_tokens=5)
        resp = MagicMock()
        resp.content = [content_block]
        resp.usage = usage
        return resp

    def test_retries_on_rate_limit_then_succeeds(self, database_stub):
        import anthropic
        import httpx
        import sys as _sys

        _sys.modules["database"] = database_stub
        database_stub.get_portfolio.return_value = {"id": "p-1", "cash": 1000, "initial_cash": 1000}
        database_stub.get_positions.return_value = []
        database_stub.get_signals.return_value = []
        database_stub.create_claude_audit_entry.return_value = None

        rate_limit_error = anthropic.RateLimitError(
            "rate limited",
            response=httpx.Response(429, request=httpx.Request("POST", "https://api.anthropic.com/v1/messages")),
            body=None,
        )
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [rate_limit_error, self._mock_response("You have 0 open positions.")]

        with patch("services.ai_service.anthropic") as mock_anthropic, \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}), \
             patch("utils.retry.time.sleep", lambda *_: None):
            mock_anthropic.Anthropic.return_value = mock_client
            from services.ai_service import ai_chat
            result = ai_chat("How am I doing?")

        assert result["response"] == "You have 0 open positions."
        assert mock_client.messages.create.call_count == 2

    def test_client_constructed_with_configured_timeout(self, database_stub):
        import sys as _sys

        _sys.modules["database"] = database_stub
        database_stub.get_portfolio.return_value = {"id": "p-1", "cash": 1000, "initial_cash": 1000}
        database_stub.get_positions.return_value = []
        database_stub.get_signals.return_value = []
        database_stub.create_claude_audit_entry.return_value = None

        mock_client = MagicMock()
        mock_client.messages.create.return_value = self._mock_response("ok")

        with patch("services.ai_service.anthropic") as mock_anthropic, \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            mock_anthropic.Anthropic.return_value = mock_client
            from services.ai_service import ai_chat
            ai_chat("How am I doing?")

            mock_anthropic.Anthropic.assert_called_once_with(
                api_key="test-key", timeout=get_timeout("anthropic")
            )
