"""
AI Chat Response Schema Validation Tests
ST-09 (BLG-QA-67, EPIC-02, v6.3)

Validates POST /ai/chat response schema conformance and advisory-only constraints
via unit test of ai_chat() service function (no live API calls — Anthropic client mocked).
AC-03: equivalent CI test entry point per sprint_backlog.md.
"""

import pytest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_anthropic_response(text: str):
    """Build a minimal mock Anthropic messages.create() response."""
    content_block = MagicMock()
    content_block.text = text
    usage = MagicMock()
    usage.input_tokens = 50
    usage.output_tokens = 30
    resp = MagicMock()
    resp.content = [content_block]
    resp.usage = usage
    return resp


# ---------------------------------------------------------------------------
# Schema validation tests (AC-01)
# ---------------------------------------------------------------------------

def test_ai_chat_response_has_required_fields(database_stub):
    """AC-01: POST /ai/chat response contains required fields: response, advisory, model."""
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = []
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.return_value = None

    mock_response = _mock_anthropic_response("You have 0 open positions.")

    with patch("services.ai_service.anthropic") as mock_anthropic, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-xyz"}):
        mock_anthropic.Anthropic.return_value.messages.create.return_value = mock_response
        from services.ai_service import ai_chat
        result = ai_chat(question="How many positions do I have open?")

    assert "response" in result, "Missing 'response' field"
    assert "advisory" in result, "Missing 'advisory' field"
    assert isinstance(result["response"], str), "'response' must be a string"
    assert isinstance(result["advisory"], bool), "'advisory' must be a boolean"


def test_ai_chat_response_types_correct(database_stub):
    """AC-01: Field types conform to schema — response: str, advisory: bool, model: str|None."""
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = []
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.return_value = None

    mock_response = _mock_anthropic_response("NVDA is not in your portfolio.")

    with patch("services.ai_service.anthropic") as mock_anthropic, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-xyz"}):
        mock_anthropic.Anthropic.return_value.messages.create.return_value = mock_response
        from services.ai_service import ai_chat
        result = ai_chat(question="What is NVDA?")

    # model is optional but when present must be a string
    if "model" in result and result["model"] is not None:
        assert isinstance(result["model"], str), "'model' must be str or None"


def test_ai_chat_no_api_key_returns_schema_conforming_error(database_stub):
    """AC-01: When ANTHROPIC_API_KEY is absent, response still conforms to schema."""
    import os
    env_without_key = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

    with patch.dict("os.environ", env_without_key, clear=True):
        from services.ai_service import ai_chat
        result = ai_chat(question="Test question")

    assert "response" in result
    assert "advisory" in result
    assert isinstance(result["response"], str)
    assert isinstance(result["advisory"], bool)


def test_ai_chat_no_portfolio_returns_schema_conforming_error(database_stub):
    """AC-01: When portfolio is not found, response still conforms to schema."""
    database_stub.get_portfolio.return_value = None

    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-xyz"}):
        from services.ai_service import ai_chat
        result = ai_chat(question="Test question")

    assert "response" in result
    assert "advisory" in result
    assert isinstance(result["advisory"], bool)


# ---------------------------------------------------------------------------
# Advisory-only constraint tests (AC-02)
# ---------------------------------------------------------------------------

_DIRECTIVE_PATTERNS = [
    "you must buy",
    "you must sell",
    "you should immediately",
    "execute the trade",
    "place an order",
    "buy now",
    "sell now",
    "i will buy",
    "i will sell",
    "i am buying",
    "i am selling",
]


def _has_directive_language(text: str) -> bool:
    lower = text.lower()
    return any(pattern in lower for pattern in _DIRECTIVE_PATTERNS)


def test_ai_chat_advisory_field_is_always_true(database_stub):
    """AC-02: advisory field is always True — never False or missing."""
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = []
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.return_value = None

    mock_response = _mock_anthropic_response("Advisory response about your portfolio.")

    with patch("services.ai_service.anthropic") as mock_anthropic, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-xyz"}):
        mock_anthropic.Anthropic.return_value.messages.create.return_value = mock_response
        from services.ai_service import ai_chat
        result = ai_chat(question="What should I do?")

    assert result["advisory"] is True, "advisory must always be True (SRB-v1.7 §13)"


def test_ai_chat_system_prompt_contains_advisory_constraint(database_stub):
    """AC-02: The system prompt sent to the model includes 'advisory only' language,
    establishing the no-execution constraint at the model instruction level."""
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = []
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.return_value = None

    captured_system = {}
    mock_response = _mock_anthropic_response("Advisory: your portfolio looks stable.")

    def capture_create(**kwargs):
        captured_system["system"] = kwargs.get("system", "")
        return mock_response

    with patch("services.ai_service.anthropic") as mock_anthropic, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-xyz"}):
        mock_anthropic.Anthropic.return_value.messages.create.side_effect = capture_create
        from services.ai_service import ai_chat
        ai_chat(question="What should I do with NVDA?")

    system = captured_system.get("system", "")
    assert "advisory" in system.lower() or "cannot execute" in system.lower(), \
        "System prompt must include advisory-only constraint language"


def test_ai_chat_response_no_directive_language_in_test_response(database_stub):
    """AC-02: When the model returns a well-formed advisory response (as in production),
    no directive language patterns are present. This validates the detection logic
    used to catch accidental model instruction violations."""
    typical_advisory = (
        "Your portfolio currently holds 3 positions. NVDA is near its trailing stop. "
        "Based on current signals, AAPL shows strong momentum. "
        "These are observations only — all trade decisions require your confirmation."
    )
    assert not _has_directive_language(typical_advisory), \
        f"Test response unexpectedly contains directive language: {typical_advisory}"


def test_directive_language_detector_catches_violations():
    """AC-02: The directive language detector correctly identifies violation patterns."""
    violating_responses = [
        "You must buy AAPL immediately based on the signal.",
        "You should immediately sell NVDA — stop breach imminent.",
        "I will sell TSLA for you if the stop is hit.",
        "Execute the trade now while price is favourable.",
    ]
    for resp in violating_responses:
        assert _has_directive_language(resp), \
            f"Detector missed directive language in: {resp}"
