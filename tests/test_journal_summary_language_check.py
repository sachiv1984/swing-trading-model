"""
ST-18 (BLG-AI-15), EPIC-03, v9.13 — POST /ai/journal-summary output-language
check.

The first working staging summary ended "...or if stop placements need
adjustment", which neither scan_prescriptive nor scan_prediction flags. AI
Compliance & Governance Officer ruling ESC-EXEC-20261027-03 (A): a summary
fails on the debrief's prescriptive scan or on wording suggesting a change to
stops, sizing or setups; it is regenerated once, then replaced by a
code-written message (summary null). Each model call writes one
claude_audit_log row with its result: pass, pass_on_regenerate,
fail_regenerate:<cats>, fail_fallback:<cats>. Prompt tightened,
JOURNAL_SUMMARY_PROMPT_VERSION v1.0 -> v1.1. Model call mocked.

These tests re-check the ruling's own sentence classification rather than
relying on it (LL-v8.6-P3-01).
"""
import logging
import sys
from unittest.mock import MagicMock, patch

import pytest

from services.ai_service import JOURNAL_SUMMARY_WITHHELD_MESSAGE, journal_summary_language_failures

STAGING = ("Entries cluster around breakouts, though few notes record why a trade was closed, "
           "which limits visibility into whether setups are working, or if stop placements need adjustment.")
PRESCRIPTIVE = "You should reduce your position size after two losses."
DESCRIPTIVE = "Entries were patient and mostly on breakouts. Stops were hit on 3 trades."


@pytest.mark.parametrize("text", [
    STAGING,
    "Position sizing should be reviewed.",
    "Setups may need refining.",
    "The stop level requires tightening on volatile names.",
    "Your stops need to be widened.",
])
def test_trading_change_wording_caught(text):
    assert "trading_change" in journal_summary_language_failures(text)


@pytest.mark.parametrize("text", [
    "Consider tightening stops on volatile names.",
    "It may be worth revisiting position sizing.",
    "Stops could be tightened.",
    "Tighter stops could help.",
    "Reducing position size after losses would be prudent.",
    "A review of setups is warranted.",
    "Stop placement is something to revisit.",
])
def test_advisory_phrasings_caught(text):
    # ST-15 (BLG-AI-20, EPIC-03, v9.14; ruling ESC-EXEC-20261030-02): the
    # seven sentences in BLG-AI-20's Problem, each [] at c8fd54e7.
    assert "trading_change" in journal_summary_language_failures(text)


def test_staging_sentence_missed_by_prescriptive_scan_alone():
    from services.debrief_service import scan_prescriptive
    assert not scan_prescriptive(STAGING)
    assert journal_summary_language_failures(STAGING) == ["trading_change"]


def test_plainly_prescriptive_caught():
    assert "prescriptive" in journal_summary_language_failures(PRESCRIPTIVE)


@pytest.mark.parametrize("text", [
    DESCRIPTIVE,
    "Stops were moved to breakeven twice after strong days.",
    "The trader reduced position size after two losses.",
    "Notes say the stop needed adjusting once, in March.",
    "Setups were mostly breakouts; sizing was consistent.",
    "A stop was hit. Review of the notes shows patience.",
    # ST-15 (v9.14): past-tense and descriptive forms of the new phrasings.
    "Stops were tightened after the loss.",
    "Tightening stops in March helped.",
    "The trader considered tightening stops but kept them.",
    "Reviewing setups each weekend was part of the routine.",
    "A review of setups was done in April.",
    "Position size was reduced after losses, which the notes call prudent.",
])
def test_descriptive_wording_passes(text):
    assert journal_summary_language_failures(text) == []


@pytest.fixture
def db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.create_claude_audit_entry.reset_mock()
    database_stub.create_claude_audit_entry.side_effect = None
    return database_stub


def _summarise(*texts):
    from services import ai_service
    responses = []
    for t in texts:
        r = MagicMock()
        r.content = [MagicMock(text=t)]
        r.usage = MagicMock(input_tokens=100, output_tokens=50)
        responses.append(r)
    with patch.object(ai_service, "_create_message", side_effect=responses) as create, \
         patch.object(ai_service, "sample_ai_output") as sample, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        result = ai_service.summarise_journal_notes(["Entered on breakout", "Stopped out"])
    return result, create, sample


def _results(db):
    return [c.kwargs["compliance_check_result"] for c in db.create_claude_audit_entry.call_args_list]


def test_descriptive_summary_passes_unchanged(db):
    result, create, _ = _summarise(DESCRIPTIVE)
    assert result == {"summary": DESCRIPTIVE, "model": "claude-haiku-4-5-20251001", "message": None}
    assert create.call_count == 1
    assert _results(db) == ["pass"]


def test_staging_sentence_regenerated_and_passes(db):
    result, create, sample = _summarise(STAGING, DESCRIPTIVE)
    assert result["summary"] == DESCRIPTIVE
    assert create.call_count == 2
    assert _results(db) == ["fail_regenerate:trading_change", "pass_on_regenerate"]
    assert [c.args[1] for c in sample.call_args_list] == [STAGING, DESCRIPTIVE]


def test_two_failures_return_the_fallback(db, caplog):
    with caplog.at_level(logging.WARNING, logger="services.ai_service"):
        result, create, _ = _summarise(PRESCRIPTIVE, STAGING)
    assert result == {"summary": None, "model": None, "message": JOURNAL_SUMMARY_WITHHELD_MESSAGE}
    assert create.call_count == 2
    assert _results(db) == ["fail_regenerate:prescriptive", "fail_fallback:trading_change"]
    logged = " ".join(r.getMessage() for r in caplog.records)
    assert "categories=prescriptive" in logged and "categories=trading_change" in logged
    assert "stop placements" not in logged and "reduce your position" not in logged


def test_each_attempt_row_is_costed(db):
    _summarise(STAGING, DESCRIPTIVE)
    for call in db.create_claude_audit_entry.call_args_list:
        assert call.kwargs["prompt_version"] == "v1.1"
        assert call.kwargs["cost_usd"] is not None


def test_prompt_tightened_and_version_bumped(db):
    from services import ai_service
    assert ai_service.JOURNAL_SUMMARY_PROMPT_VERSION == "v1.1"
    _, create, _ = _summarise(DESCRIPTIVE)
    prompt = create.call_args.kwargs["messages"][0]["content"]
    assert "do not suggest changing stops, position sizing or setups" in prompt
