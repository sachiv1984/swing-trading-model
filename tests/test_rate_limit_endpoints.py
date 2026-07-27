"""
Rate-limit remediation tests — ST-08 (EPIC-08, v7.8, BLG-SEC-21).

Covers the 4 endpoints newly gated by an app-level rate limit as part of
this cycle's rate-limiting audit remediation:
  - GET  /health                          (public_limiter, 60/min/IP)
  - POST /ai/journal-summary               (_ai_limiter, 10/min/IP)
  - POST /trade-plans/generate-plan        (_ai_limiter, 10/min/IP)
  - POST /trade-plans/{plan_id}/generate-thesis (_ai_limiter, 10/min/IP)

Each test drives the limiter to its configured ceiling and confirms the
next request receives HTTP 429 with a Retry-After header. Business-logic
correctness of the underlying handlers is out of scope here (covered
elsewhere) — these tests only exercise the rate-limit gate itself, which
runs before any DB/external-API work in each handler.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402
from services.rate_limiter import _ai_limiter, _public_limiter  # noqa: E402
import routers.ai as ai_router  # noqa: E402
import routers.trade_plans as trade_plans_router  # noqa: E402
import main as main_module  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)

_TEST_IP = "testclient"  # FastAPI TestClient's default request.client.host


def _reset(key: str, public: bool = False):
    (_public_limiter if public else _ai_limiter).reset(key)


def test_health_rate_limit_returns_429_after_60_requests():
    key = f"health:{_TEST_IP}"
    _reset(key, public=True)
    try:
        for _ in range(main_module._HEALTH_LIMIT):
            resp = CLIENT.get("/health")
            assert resp.status_code != 429
        resp = CLIENT.get("/health")
        assert resp.status_code == 429
        assert "Retry-After" in resp.headers
    finally:
        _reset(key, public=True)


def test_journal_summary_rate_limit_returns_429_after_10_requests():
    key = f"journal-summary:{_TEST_IP}"
    _reset(key)
    try:
        body = {"trade_ids": [1]}
        for _ in range(ai_router._JOURNAL_SUMMARY_LIMIT):
            resp = CLIENT.post("/ai/journal-summary", json=body)
            assert resp.status_code != 429
        resp = CLIENT.post("/ai/journal-summary", json=body)
        assert resp.status_code == 429
        assert "Retry-After" in resp.headers
    finally:
        _reset(key)


def test_generate_plan_rate_limit_returns_429_after_10_requests():
    key = f"generate-plan:{_TEST_IP}"
    _reset(key)
    try:
        body = {"ticker": "AAPL", "market": "US"}
        for _ in range(trade_plans_router._GENERATE_PLAN_LIMIT):
            resp = CLIENT.post("/trade-plans/generate-plan", json=body)
            assert resp.status_code != 429
        resp = CLIENT.post("/trade-plans/generate-plan", json=body)
        assert resp.status_code == 429
        assert "Retry-After" in resp.headers
    finally:
        _reset(key)


def test_generate_thesis_rate_limit_returns_429_after_10_requests():
    key = f"generate-thesis:{_TEST_IP}"
    _reset(key)
    try:
        for _ in range(trade_plans_router._GENERATE_THESIS_LIMIT):
            resp = CLIENT.post("/trade-plans/some-plan-id/generate-thesis")
            assert resp.status_code != 429
        resp = CLIENT.post("/trade-plans/some-plan-id/generate-thesis")
        assert resp.status_code == 429
        assert "Retry-After" in resp.headers
    finally:
        _reset(key)


def test_ai_and_public_limiters_are_distinct_instances():
    # ST-08: the public limiter must not share state with the AI limiter —
    # otherwise unauthenticated /health traffic could starve AI endpoint quota.
    assert _ai_limiter is not _public_limiter
