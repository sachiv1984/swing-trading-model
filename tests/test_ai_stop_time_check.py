"""
ST-04 (BLG-AI-10, EPIC-01, v9.12) — post-generation stop-time check for the
daily briefing and chat.

AI Compliance & Governance Officer ruling (ESC-EXEC-20261013-01, 2026-10-13):
when a response cites a position's stop without its recalculation time, code
appends "(<TICKER> <_stop_recalculated_label()>)" after the model's text in
that field, and every miss is logged and counted in
claude_audit_log.compliance_check_result. Model text is never edited; the
sampling hook receives the raw output; the check fails open. Model call mocked.
"""
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import run_ai_output_boundary_sample_audit as audit  # noqa: E402

_POSITIONS = [
    {"ticker": "NVDA", "market": "US", "current_price": 470.0, "current_stop": 450.0, "pnl_pct": 4.0,
     "pnl": 40.0, "holding_days": 14, "risk_off_exit": False,
     "stop_calculated_at": datetime(2026, 10, 12, 21, 5, tzinfo=timezone.utc)},
    {"ticker": "WDC", "market": "US", "current_price": 50.0, "current_stop": 51.0, "pnl_pct": -2.0,
     "pnl": -20.0, "holding_days": 3, "risk_off_exit": False, "stop_calculated_at": None},
]
NVDA_NOTE = "(NVDA stop last recalculated 2026-10-12 21:05 UTC)"
WDC_NOTE = "(WDC stop not recalculated since entry)"


@pytest.fixture
def db(database_stub):
    sys.modules["database"] = database_stub
    database_stub.get_portfolio.return_value = {"id": "p-001", "cash": 5000, "initial_cash": 10000}
    database_stub.get_positions.return_value = [dict(p) for p in _POSITIONS]
    database_stub.get_signals.return_value = []
    database_stub.create_claude_audit_entry.reset_mock()
    return database_stub


def _run(func, *args, text):
    from services import ai_service
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    resp.usage = MagicMock(input_tokens=1, output_tokens=1)
    with patch.object(ai_service, "_create_message", return_value=resp), \
         patch.object(ai_service, "_get_regime_data", return_value=None), \
         patch.object(ai_service, "sample_ai_output") as sample, \
         patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}):
        result = getattr(ai_service, func)(*args)
    return result, sample


def _audit_result(db):
    return db.create_claude_audit_entry.call_args.kwargs["compliance_check_result"]


# ─── Detection (AC 1) ─────────────────────────────────────────────────────

def _check(text, own_ticker=None):
    from services.ai_service import _append_missing_stop_times
    return _append_missing_stop_times(text, _POSITIONS, "POST /ai/chat", "response", "v1.1", own_ticker)


class TestDetection:
    def test_stop_without_time_is_caught(self):
        text = "NVDA is near its trailing stop."
        assert _check(text) == (f"{text} {NVDA_NOTE}", "appended")

    def test_stop_with_full_label_passes(self):
        text = "NVDA's stop (last recalculated 2026-10-12 21:05 UTC) is close."
        assert _check(text) == (text, None)

    def test_stop_with_date_only_passes(self):
        text = "NVDA's stop of £450.00, set on 2026-10-12, is close."
        assert _check(text) == (text, None)

    def test_null_stop_phrase_passes(self):
        text = "WDC is below its stop, which has not recalculated since entry."
        assert _check(text) == (text, None)

    def test_null_stop_without_phrase_is_caught(self):
        text = "WDC breached its stop."
        assert _check(text) == (f"{text} {WDC_NOTE}", "appended")

    def test_text_without_stop_is_not_flagged(self):
        assert _check("NVDA is up 4% today.") == ("NVDA is up 4% today.", None)

    def test_ticker_not_an_open_position_is_ignored(self):
        assert _check("TSLA hit its stop yesterday.") == ("TSLA hit its stop yesterday.", "unattributed")

    def test_no_ticker_logs_unattributed_and_appends_nothing(self, caplog):
        text = "Two positions are near their stops."
        with caplog.at_level(logging.WARNING, logger="services.ai_service"):
            assert _check(text) == (text, "unattributed")
        assert any("ticker=unattributed action=unattributed_no_append" in r.getMessage() for r in caplog.records)

    def test_ticker_matched_as_whole_word_only(self):
        assert _check("NVDAX is near its stop.") == ("NVDAX is near its stop.", "unattributed")

    def test_each_ticker_appended_once_in_order(self):
        text = "WDC breached its stop. NVDA is near its stop. NVDA's stop is tight."
        out, outcome = _check(text)
        assert out == f"{text} {WDC_NOTE} {NVDA_NOTE}"
        assert out.count(NVDA_NOTE) == 1 and outcome == "appended"

    def test_action_own_ticker_attributed(self):
        out, outcome = _check("Within 3% of trailing stop — watch closely.", own_ticker="NVDA")
        assert out.endswith(f" {NVDA_NOTE}") and outcome == "appended"

    def test_fails_open(self, caplog):
        from services import ai_service
        with patch.object(ai_service, "_stop_time_present", side_effect=RuntimeError("boom")), \
             caplog.at_level(logging.ERROR, logger="services.ai_service"):
            assert _check("NVDA is near its stop.") == ("NVDA is near its stop.", "error")
        assert any("stop-time check failed" in r.getMessage() for r in caplog.records)


# ─── Failure action applied for briefing and chat (AC 2) ──────────────────

class TestBriefing:
    def test_summary_and_action_description_get_notes(self, db, caplog):
        body = json.dumps({"summary": "NVDA is near its trailing stop.", "actions": [
            {"type": "MONITOR", "ticker": "NVDA", "description": "Within 3% of trailing stop."},
            {"type": "EXIT", "ticker": "WDC", "description": "Stop breached (stop not recalculated since entry)."},
        ]})
        with caplog.at_level(logging.WARNING, logger="services.ai_service"):
            result, sample = _run("generate_daily_briefing", text=body)
        assert result["summary"] == f"NVDA is near its trailing stop. {NVDA_NOTE}"
        assert result["actions"][0]["description"] == f"Within 3% of trailing stop. {NVDA_NOTE}"
        assert result["actions"][1]["description"] == "Stop breached (stop not recalculated since entry)."
        assert result["actions"][0]["type"] == "MONITOR" and result["actions"][0]["ticker"] == "NVDA"
        assert _audit_result(db) == "stop_time_missing_appended"
        warnings = [r.getMessage() for r in caplog.records if "stop-time check" in r.getMessage()]
        assert any("field=summary ticker=NVDA action=appended prompt_version=v1.3" in w for w in warnings)
        assert any("field=actions[0].description ticker=NVDA action=appended" in w for w in warnings)
        assert not any("actions[1]" in w for w in warnings)
        # Condition 2: the sampling hook gets the raw model output.
        assert sample.call_args[0][1] == body

    def test_clean_briefing_records_pass(self, db):
        body = json.dumps({"summary": "All quiet.", "actions": []})
        result, _ = _run("generate_daily_briefing", text=body)
        assert result["summary"] == "All quiet."
        assert _audit_result(db) == "pass"

    def test_unattributed_only_records_unattributed(self, db):
        body = json.dumps({"summary": "Two positions are near their stops.", "actions": []})
        result, _ = _run("generate_daily_briefing", text=body)
        assert result["summary"] == "Two positions are near their stops."
        assert _audit_result(db) == "stop_time_missing_unattributed"

    def test_unparseable_response_still_audited_then_falls_back(self, db):
        result, _ = _run("generate_daily_briefing", text="not json")
        assert result["summary"] is None and result["error"]
        db.create_claude_audit_entry.assert_called_once()
        assert _audit_result(db) is None


class TestChat:
    def test_response_gets_note_and_raw_text_is_sampled(self, db, caplog):
        raw = "NVDA is closest to its trailing stop, 2.8% above £450.00."
        with caplog.at_level(logging.WARNING, logger="services.ai_service"):
            result, sample = _run("ai_chat", "Which stop is closest?", text=raw)
        assert result["response"] == f"{raw} {NVDA_NOTE}"
        assert result["response"].count(NVDA_NOTE) == 1
        assert _audit_result(db) == "stop_time_missing_appended"
        assert any("endpoint=POST /ai/chat field=response ticker=NVDA action=appended prompt_version=v1.1"
                   in r.getMessage() for r in caplog.records)
        assert sample.call_args[0][1] == raw

    def test_response_with_time_unchanged(self, db):
        raw = "NVDA's stop was last recalculated 2026-10-12 21:05 UTC."
        result, _ = _run("ai_chat", "q", text=raw)
        assert result["response"] == raw
        assert _audit_result(db) == "pass"

    def test_check_failure_returns_model_text(self, db):
        from services import ai_service
        raw = "NVDA is near its stop."
        with patch.object(ai_service, "_stop_time_present", side_effect=RuntimeError("boom")):
            result, _ = _run("ai_chat", "q", text=raw)
        assert result["response"] == raw
        assert _audit_result(db) == "stop_time_check_error"


def test_prompt_versions_unchanged_by_st04():
    from services import ai_service
    assert ai_service.CHAT_PROMPT_VERSION == "v1.1"


# ─── Boundary-sample audit scores the check (AC 3) ────────────────────────

class TestBoundarySampleAudit:
    def test_scan_flags_stop_without_time(self):
        assert audit.scan_stop_time_missing("NVDA is near its trailing stop.")

    @pytest.mark.parametrize("text", [
        "NVDA's stop (last recalculated 2026-10-12 21:05 UTC) is close.",
        "WDC's stop has not recalculated since entry.",
        "NVDA is up 4% today.",
        "",
    ])
    def test_scan_passes_text_with_time_or_without_stop(self, text):
        assert not audit.scan_stop_time_missing(text)

    def test_illustrative_nvda_rows_are_flagged(self):
        rows = {source: r for (source, _), r in zip(audit.SAMPLE, audit.run_audit())}
        assert rows["daily-briefing summary (POST /ai/daily-briefing)"]["stop_time_missing"]
        assert rows["chat response (POST /ai/chat)"]["stop_time_missing"]

    def test_only_briefing_and_chat_sources_are_scored(self):
        results = audit.run_audit([
            ("debrief summary_text (POST /trades/{id}/debrief)", "planned stop 95.0"),
            ("chat (POST /ai/chat) [real sample, 2026-10-13]", "NVDA is near its stop."),
        ])
        assert [r["stop_time_missing"] for r in results] == [False, True]

    def test_metric_reported_separately_and_exit_code_unaffected(self, capsys, monkeypatch):
        monkeypatch.setattr(audit, "load_real_samples_from_store", lambda limit=10: [])
        assert audit.main() == 0
        out = capsys.readouterr().out
        assert "Violations found: 0" in out
        assert "Stop-time missing (correctness metric" in out
        assert "[STOP-TIME-MISSING] chat response (POST /ai/chat)" in out
