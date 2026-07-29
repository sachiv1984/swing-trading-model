"""
ST-06 (BLG-SEC-09, EPIC-02, v7.10): AI rate-limit bypass test.

Covers both rate-limited AI endpoints (POST /ai/daily-briefing,
POST /ai/chat) against two named bypass techniques:

1. X-Forwarded-For header spoofing — varying the header per request while
   the real transport-level client stays the same. Confirms this has ZERO
   effect: routers/ai.py keys the limiter purely on `request.client.host`
   and never reads any X-Forwarded-For / X-Real-IP header, so a spoofed
   header cannot manufacture a fresh quota bucket.
2. Genuine IP rotation — the request's actual transport-level source
   address changes between requests. Confirms the limiter mechanism itself
   is sound (each distinct `request.client.host` correctly gets its own
   independent bucket) — this is the expected, accepted behaviour of any
   per-IP limiter, not a code defect. See
   docs/ops/ai_rate_limit_bypass_audit_2026-07-29.md for the one confirmed,
   filed finding (BLG-SEC-24): in the production Render deployment, uvicorn
   is not started with `--proxy-headers`, so `request.client.host` may not
   reflect the true per-client IP at all — collapsing the limiter to a
   single shared bucket. That finding is a deployment-configuration risk,
   not something a unit test against the ASGI-transport-level request
   object can exercise directly (it requires live Render verification).

CI-safe: no live DB, network, or Claude API calls — the underlying
generate_daily_briefing/ai_chat calls are mocked; only the rate-limiter
keying logic is under test.
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import routers.ai as ai_router  # noqa: E402
from routers.ai import daily_briefing, ai_chat_endpoint, ChatRequest  # noqa: E402
from services.rate_limiter import _ai_limiter  # noqa: E402


def _fake_request(ip: str, xff: str = None):
    headers = {"X-Forwarded-For": xff} if xff else {}
    return SimpleNamespace(client=SimpleNamespace(host=ip), headers=headers)


def _is_429(response) -> bool:
    return getattr(response, "status_code", None) == 429


class TestDailyBriefingXFFSpoofingDoesNotBypass:
    def setup_method(self):
        self._real_ip = "203.0.113.5"
        _ai_limiter.reset(f"daily-briefing:{self._real_ip}")

    def teardown_method(self):
        _ai_limiter.reset(f"daily-briefing:{self._real_ip}")

    def test_rotating_xff_header_does_not_reset_quota(self):
        with patch("services.ai_service.generate_daily_briefing", return_value={"summary": "ok", "actions": []}):
            for i in range(ai_router._DAILY_BRIEFING_LIMIT):
                # A different spoofed X-Forwarded-For value on every request —
                # simulating an attacker rotating the header to try to look
                # like a new client each time.
                resp = daily_briefing(_fake_request(self._real_ip, xff=f"10.0.0.{i}"))
                assert not _is_429(resp), f"request {i} unexpectedly rate-limited"

            # Limit now exhausted for the real transport IP. One more request
            # with yet another spoofed XFF value — if the header were trusted,
            # this would look like a brand-new client and be allowed.
            resp = daily_briefing(_fake_request(self._real_ip, xff="10.0.0.999"))
            assert _is_429(resp), "X-Forwarded-For spoofing must NOT bypass the rate limit"


class TestChatXFFSpoofingDoesNotBypass:
    def setup_method(self):
        self._real_ip = "203.0.113.6"
        _ai_limiter.reset(f"chat:{self._real_ip}")

    def teardown_method(self):
        _ai_limiter.reset(f"chat:{self._real_ip}")

    def test_rotating_xff_header_does_not_reset_quota(self):
        with patch("services.ai_service.ai_chat", return_value={"response": "ok", "advisory": True}):
            body = ChatRequest(question="test?")
            for i in range(ai_router._CHAT_LIMIT):
                resp = ai_chat_endpoint(body, _fake_request(self._real_ip, xff=f"172.16.0.{i}"))
                assert not _is_429(resp), f"request {i} unexpectedly rate-limited"

            resp = ai_chat_endpoint(body, _fake_request(self._real_ip, xff="172.16.0.999"))
            assert _is_429(resp), "X-Forwarded-For spoofing must NOT bypass the rate limit"


class TestGenuineIpRotationBehavesAsExpectedForPerIpLimiter:
    """Confirms the limiter mechanism itself is sound — a real change in
    request.client.host does get an independent bucket. This is the
    inherent, accepted trade-off of any per-IP limiter (real IP rotation via
    a botnet/proxy pool always defeats per-IP throttling to some degree);
    the actionable risk is whether request.client.host is trustworthy in
    production at all (BLG-SEC-24, see audit doc), not this counting logic."""

    def test_each_distinct_real_ip_gets_its_own_independent_bucket(self):
        ips = ["198.51.100.1", "198.51.100.2", "198.51.100.3"]
        for ip in ips:
            _ai_limiter.reset(f"daily-briefing:{ip}")
        try:
            with patch("services.ai_service.generate_daily_briefing", return_value={"summary": "ok", "actions": []}):
                for ip in ips:
                    for i in range(ai_router._DAILY_BRIEFING_LIMIT):
                        resp = daily_briefing(_fake_request(ip))
                        assert not _is_429(resp), f"ip={ip} request {i} unexpectedly rate-limited"
                    # this same real IP is now exhausted
                    resp = daily_briefing(_fake_request(ip))
                    assert _is_429(resp), f"ip={ip} should be rate-limited after exhausting its own quota"
        finally:
            for ip in ips:
                _ai_limiter.reset(f"daily-briefing:{ip}")


if __name__ == "__main__":
    import unittest
    unittest.main()
