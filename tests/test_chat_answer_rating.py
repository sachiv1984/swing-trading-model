"""
ST-22 (BLG-FE-208), EPIC-03, v9.13 — useful / not-useful rating per AI chat
answer.

- POST /ai/chat returns answer_id (the claude_audit_log row id) for a model
  answer only; fixed messages carry none (decision record §2.1).
- POST /ai/chat/{answer_id}/rating stores one rating: 201; a second attempt is
  409 with the stored rating (not overwritten); an unknown answer is 404;
  a bad rating or id is 422.

CI-safe: the service's database call is patched; the database layer runs
against real Postgres in tests/test_chat_answer_rating_db.py.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    from fastapi.testclient import TestClient  # noqa: E402

    import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)
ANSWER = "3f2b7c1e-9a4d-4e21-8c55-0d6f1a2b3c4d"
STORED = {"answer_id": ANSWER, "rating": "useful", "rated_at": "2026-10-27T09:30:00+00:00"}


def _rate(body, result, answer=ANSWER):
    with patch("services.ai_service.rate_chat_answer", return_value=result) as svc:
        return CLIENT.post(f"/ai/chat/{answer}/rating", json=body), svc


class TestRatingRoute:
    def test_first_rating_stored_201(self):
        resp, svc = _rate({"rating": "useful"}, {**STORED, "created": True})
        assert resp.status_code == 201
        assert resp.json() == {"status": "ok", "data": STORED}
        svc.assert_called_once_with(ANSWER, "useful")

    def test_second_rating_409_returns_stored_value(self):
        resp, svc = _rate({"rating": "not_useful"}, {**STORED, "created": False})
        assert resp.status_code == 409
        body = resp.json()
        assert body["status"] == "error" and body["data"] == STORED
        assert "already been rated" in body["message"]

    def test_unknown_answer_404(self):
        resp, _ = _rate({"rating": "useful"}, None)
        assert resp.status_code == 404
        assert resp.json() == {"status": "error", "message": "Chat answer not found."}

    @pytest.mark.parametrize("body", [{}, {"rating": "great"}, {"rating": None}])
    def test_invalid_rating_422(self, body):
        resp, svc = _rate(body, None)
        assert resp.status_code == 422
        svc.assert_not_called()

    def test_non_uuid_answer_422(self):
        resp, svc = _rate({"rating": "useful"}, None, answer="not-a-uuid")
        assert resp.status_code == 422
        svc.assert_not_called()


def test_service_delegates_to_database(database_stub):
    from services import ai_service
    sys.modules["database"] = database_stub
    database_stub.create_chat_answer_rating.return_value = {**STORED, "created": True}
    assert ai_service.rate_chat_answer(ANSWER, "useful")["created"] is True
    database_stub.create_chat_answer_rating.assert_called_with(ANSWER, "useful")


@pytest.fixture
def db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = []
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.reset_mock()
    database_stub.create_claude_audit_entry.side_effect = None
    return database_stub


def _chat(text, audit_id):
    from services import ai_service
    resp = MagicMock()
    resp.content = [MagicMock(text=text)] if text else []
    resp.usage = MagicMock(input_tokens=1, output_tokens=1)
    with patch.object(ai_service, "_create_message", return_value=resp), \
         patch.object(ai_service, "sample_ai_output"), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        return ai_service.ai_chat("How am I doing?")


class TestChatAnswerId:
    def test_model_answer_carries_answer_id(self, db):
        db.create_claude_audit_entry.return_value = ANSWER
        assert _chat("All quiet today.", ANSWER)["answer_id"] == ANSWER

    def test_no_answer_id_when_audit_row_not_written(self, db):
        db.create_claude_audit_entry.return_value = None
        assert "answer_id" not in _chat("All quiet today.", None)

    def test_empty_model_content_fixed_message_has_no_answer_id(self, db):
        db.create_claude_audit_entry.return_value = ANSWER
        result = _chat(None, ANSWER)
        assert result["response"] == "I was unable to generate a response."
        assert "answer_id" not in result

    def test_failed_call_fallback_has_no_answer_id(self, db):
        from services import ai_service
        with patch.object(ai_service, "_create_message", side_effect=RuntimeError("down")), \
             patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
            result = ai_service.ai_chat("How am I doing?")
        assert result["response"].startswith("Unable to get a response")
        assert "answer_id" not in result

    def test_chat_route_passes_answer_id_through(self):
        payload = {"response": "All quiet.", "advisory": True, "model": "m", "answer_id": ANSWER}
        with patch("services.ai_service.ai_chat", return_value=payload):
            resp = CLIENT.post("/ai/chat", json={"question": "How am I doing?"})
        assert resp.status_code == 200
        assert resp.json()["answer_id"] == ANSWER
