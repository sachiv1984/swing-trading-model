"""
Correlation-ID propagation tests (ST-03, EPIC-01, v9.3, BLG-BE-48).

AC coverage:
- A request-scoped correlation ID (middleware-generated or accepted via
  header) is included in all log lines emitted during that request.
- Correlation ID present in logs for at least 2 representative multi-step
  endpoints (GET /health/detailed, GET /screener/history — both exercise the
  router -> service -> (mocked) database layering).
- Documented in backend_engineering_patterns.md (see that document's §12).
"""
import logging
import sys
import uuid
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
from utils.correlation_id import (  # noqa: E402
    get_correlation_id, set_correlation_id, reset_correlation_id,
    new_correlation_id, install_correlation_id_log_record_factory,
)

# main.py installs this at import time; ensure it's installed for this test
# module too (idempotent) in case tests run in isolation.
install_correlation_id_log_record_factory()

CLIENT = TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Unit tests — the context var and log filter in isolation
# ---------------------------------------------------------------------------

def test_get_correlation_id_defaults_to_dash_outside_a_request():
    assert get_correlation_id() == "-"


def test_set_and_reset_correlation_id():
    token = set_correlation_id("test-corr-id")
    try:
        assert get_correlation_id() == "test-corr-id"
    finally:
        reset_correlation_id(token)
    assert get_correlation_id() == "-"


def test_new_correlation_id_generates_a_valid_uuid():
    corr_id = new_correlation_id()
    uuid.UUID(corr_id)  # raises ValueError if not a valid UUID string


def test_log_record_factory_stamps_current_correlation_id_onto_new_records():
    token = set_correlation_id("factory-test-id")
    try:
        record = logging.getLogger("test").makeRecord(
            "test", logging.INFO, __file__, 1, "hello", (), None,
        )
        assert record.correlation_id == "factory-test-id"
    finally:
        reset_correlation_id(token)


# ---------------------------------------------------------------------------
# Integration tests — end-to-end through the FastAPI middleware stack
# ---------------------------------------------------------------------------

def test_response_carries_generated_correlation_id_header():
    with patch("main.get_detailed_health",
               return_value={"overall": "healthy", "checks": []}):
        r = CLIENT.get("/health/detailed")
    assert r.status_code == 200
    assert "X-Correlation-ID" in r.headers
    uuid.UUID(r.headers["X-Correlation-ID"])  # auto-generated — a valid UUID


def test_response_echoes_inbound_correlation_id_header():
    with patch("main.get_detailed_health",
               return_value={"overall": "healthy", "checks": []}):
        r = CLIENT.get("/health/detailed", headers={"X-Correlation-ID": "caller-supplied-id"})
    assert r.headers["X-Correlation-ID"] == "caller-supplied-id"


def test_log_lines_during_health_detailed_request_carry_the_response_correlation_id(caplog):
    """Representative multi-step endpoint 1/2: GET /health/detailed."""
    def _fake_get_detailed_health():
        logging.getLogger("services.health_service").info("computing detailed health")
        return {"overall": "healthy", "checks": []}

    with caplog.at_level(logging.INFO):
        with patch("main.get_detailed_health", side_effect=_fake_get_detailed_health):
            r = CLIENT.get("/health/detailed", headers={"X-Correlation-ID": "health-detailed-corr-id"})

    assert r.headers["X-Correlation-ID"] == "health-detailed-corr-id"
    matching = [rec for rec in caplog.records if rec.message == "computing detailed health"]
    assert matching, "expected the service-layer log line to have been captured"
    assert getattr(matching[0], "correlation_id", None) == "health-detailed-corr-id"


def test_log_lines_during_screener_history_request_carry_the_response_correlation_id(caplog):
    """Representative multi-step endpoint 2/2: GET /screener/history (ST-01)."""
    def _fake_get_screener_run_history(limit=50, offset=0):
        logging.getLogger("services.screener_batch_service").info("fetching screener run history")
        return {"runs": [], "total": 0, "limit": limit, "offset": offset}

    with caplog.at_level(logging.INFO):
        with patch("routers.screener.get_screener_run_history", side_effect=_fake_get_screener_run_history):
            r = CLIENT.get("/screener/history", headers={"X-Correlation-ID": "screener-history-corr-id"})

    assert r.status_code == 200
    assert r.headers["X-Correlation-ID"] == "screener-history-corr-id"
    matching = [rec for rec in caplog.records if rec.message == "fetching screener run history"]
    assert matching, "expected the service-layer log line to have been captured"
    assert getattr(matching[0], "correlation_id", None) == "screener-history-corr-id"


def test_correlation_id_present_even_on_401_rejection(monkeypatch):
    """correlation_id_middleware is registered so it wraps api_key_middleware
    (outermost) — the ID must be assigned even for a request api_key_middleware
    rejects (BLG-BE-48 — see main.py's middleware-ordering comment)."""
    monkeypatch.setenv("API_KEY", "real-key")
    try:
        r = CLIENT.get("/positions", headers={"X-API-Key": "wrong-key"})
        assert r.status_code == 401
        assert "X-Correlation-ID" in r.headers
        uuid.UUID(r.headers["X-Correlation-ID"])
    finally:
        monkeypatch.delenv("API_KEY", raising=False)
