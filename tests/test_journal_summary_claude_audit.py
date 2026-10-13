"""
ST-06 (BLG-OPS-183, EPIC-01, v9.12) — the journal summary logs its Claude
calls to claude_audit_log.

ST-06 moved the daily cost alert to claude_audit_log on the premise that
every Claude call writes it. The agent-mediated Director of Quality review
found that summarise_journal_notes() did not: it wrote only ai_audit_log,
which has no cost column, so journal-summary spend was still invisible to
the alert. Each journal-summary model call now writes one claude_audit_log
row (Haiku cost, tokens, prompt hash, latency); a failed call writes a
'model_call_failed' row; an audit failure never affects the summary.
"""
import logging
import sys
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.create_claude_audit_entry.reset_mock()
    database_stub.create_claude_audit_entry.side_effect = None
    return database_stub


def _summarise(text="Patient entries; stops respected.", raises=None):
    from services import ai_service
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    resp.usage = MagicMock(input_tokens=2000, output_tokens=400)
    kw = {"side_effect": raises} if raises else {"return_value": resp}
    with patch.object(ai_service, "_create_message", **kw), \
         patch.object(ai_service, "sample_ai_output"), \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        return ai_service.summarise_journal_notes(["Entered on breakout", "Stopped out"])


def test_successful_call_writes_one_costed_row(db):
    result = _summarise()
    assert result["summary"] == "Patient entries; stops respected."
    db.create_claude_audit_entry.assert_called_once()
    kw = db.create_claude_audit_entry.call_args.kwargs
    assert kw["endpoint"] == "POST /ai/journal-summary"
    assert kw["model_id"] == "claude-haiku-4-5-20251001"
    assert kw["prompt_version"] == "v1.0"
    assert (kw["input_tokens"], kw["output_tokens"]) == (2000, 400)
    # Haiku 4.5: $1/M input, $5/M output -> 2000*1e-6 + 400*5e-6 = 0.004
    assert kw["cost_usd"] == pytest.approx(0.004)
    assert len(kw["prompt_hash"]) == 16
    assert kw["response_length"] == len("Patient entries; stops respected.")
    assert kw["compliance_check_result"] is None


def test_failed_call_writes_model_call_failed_row(db):
    result = _summarise(raises=RuntimeError("upstream down"))
    assert result["summary"] is None and "unavailable" in result["message"]
    kw = db.create_claude_audit_entry.call_args.kwargs
    assert kw["compliance_check_result"] == "model_call_failed"
    assert kw["cost_usd"] is None and kw["endpoint"] == "POST /ai/journal-summary"


def test_audit_failure_never_affects_the_summary(db, caplog):
    db.create_claude_audit_entry.side_effect = Exception("audit table unavailable")
    with caplog.at_level(logging.WARNING, logger="services.ai_service"):
        result = _summarise()
    assert result["summary"] == "Patient entries; stops respected."
    assert any("journal-summary audit row not written" in r.getMessage() for r in caplog.records)


def test_no_model_call_no_row(db):
    from services import ai_service
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        assert ai_service.summarise_journal_notes([])["summary"] is None
    db.create_claude_audit_entry.assert_not_called()
