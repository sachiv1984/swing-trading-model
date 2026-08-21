"""
Tests for backend/services/debrief_service.py — ST-06, EPIC-02, v8.9, BLG-FEAT-90

Covers the §13 review's Condition 9 output-side enforcement (prescriptive-
language scan, numeric cross-check, regenerate-then-fallback sequencing),
the deterministic (never model-generated) summary text, and audit logging
of the compliance-check outcome.
"""
from unittest.mock import patch, MagicMock

import pytest

from services.debrief_service import (
    scan_prescriptive,
    numeric_cross_check,
    _build_summary_text,
    generate_trade_debrief,
    _FOCUS_AREA_SYSTEM,
)


# ─── Condition 1/9: prescriptive-language scan ────────────────────────────

class TestScanPrescriptive:
    def test_observational_sentence_passes(self):
        text = "Your exit was 3 days earlier than the 15-day median across your last 5 trades in this setup type."
        assert scan_prescriptive(text) is False

    @pytest.mark.parametrize("text", [
        "You should hold winners longer.",
        "Consider reducing position size on high-volatility setups.",
        "Next time, do X differently.",
        "Reduce your stop distance on similar setups.",
        "Make sure to check volume before entering.",
        "It's recommended to wait for confirmation.",
        "We recommend tightening your stop next time.",
    ])
    def test_prescriptive_phrasing_detected(self, text):
        assert scan_prescriptive(text) is True

    def test_empty_text_is_not_a_violation(self):
        assert scan_prescriptive("") is False
        assert scan_prescriptive(None) is False


# ─── Condition 2/9: numeric cross-check ───────────────────────────────────

class TestNumericCrossCheck:
    def test_numbers_matching_source_pass(self):
        source = {"entry_price": 100.0, "exit_price": 108.5, "pnl": 8.5}
        text = "Your exit at 108.5 was above your entry at 100."
        assert numeric_cross_check(text, source) is True

    def test_fabricated_number_fails(self):
        source = {"entry_price": 100.0, "exit_price": 108.5}
        text = "This trade returned 42% more than your average."
        assert numeric_cross_check(text, source) is False

    def test_no_numbers_in_text_passes_trivially(self):
        source = {"entry_price": 100.0}
        text = "Your exit aligned closely with your stated plan."
        assert numeric_cross_check(text, source) is True

    def test_rounded_number_within_tolerance_passes(self):
        # Source has 108.6 -- model may state the full value or its 0dp rounding (109) -- both allowed.
        source = {"exit_price": 108.6}
        assert numeric_cross_check("Exit was 108.6.", source) is True
        assert numeric_cross_check("Exit was 109.", source) is True

    def test_none_values_in_source_are_skipped_safely(self):
        source = {"entry_price": None, "exit_price": 100.0}
        assert numeric_cross_check("Exit at 100.", source) is True


# ─── Deterministic summary (never model-generated) ────────────────────────

class TestBuildSummaryText:
    def test_summary_contains_only_real_trade_values(self):
        trade = {
            "entry_price": 100.0, "exit_price": 108.5, "pnl": 8.5,
            "pnl_pct": 8.5, "exit_reason": "Target Reached", "holding_days": 12,
        }
        summary = _build_summary_text(trade, None)
        assert "100.0" in summary
        assert "108.5" in summary
        assert "Target Reached" in summary
        assert "No linked trade plan" in summary

    def test_summary_includes_plan_fields_when_plan_present(self):
        trade = {"entry_price": 100.0, "exit_price": 108.5, "pnl": 8.5, "pnl_pct": 8.5,
                  "exit_reason": "Target Reached", "holding_days": 12}
        plan = {"planned_entry_price": 99.0, "planned_stop_price": 95.0, "r_target": 2.0}
        summary = _build_summary_text(trade, plan)
        assert "99.0" in summary
        assert "95.0" in summary
        assert "2.0" in summary


# ─── ST-04 (BLG-TECH-17, v9.0) — prompt no longer encourages unverifiable
#     cross-trade pattern language ────────────────────────────────────────

class TestFocusAreaPromptExcludesCrossTradeLanguage:
    """BLG-TECH-17: the prompt previously framed the focus area as "a
    pattern in this trade's own plan-vs-reality data", which -- combined
    with the multi-trade journal_context passed as prompt context -- could
    invite the model toward frequency/count claims across trades ("this is
    the Nth time...") that numeric_cross_check() cannot reliably catch (a
    fabricated count either fails the check outright, losing the feature's
    value, or coincidentally matches an unrelated approved number and passes
    despite being an ungrounded guess). Fixed by removing the "pattern"
    framing and explicitly prohibiting cross-trade count/frequency/
    comparison claims in the prompt itself (option (a) from the backlog
    item's two proposed directions)."""

    def test_prompt_does_not_use_pattern_framing(self):
        assert "a pattern in this trade" not in _FOCUS_AREA_SYSTEM

    def test_prompt_explicitly_prohibits_cross_trade_claims(self):
        lowered = _FOCUS_AREA_SYSTEM.lower()
        assert "nth time" in lowered
        assert "across multiple trades" in lowered or "aggregate data" in lowered

    def test_prompt_still_scopes_to_single_trade(self):
        assert "THIS trade only" in _FOCUS_AREA_SYSTEM


class TestNumericCrossCheckCatchesUngroundedFrequencyClaim:
    """Defense in depth (BLG-TECH-17): even if a cross-trade count claim
    slipped past the prompt-level prohibition, numeric_cross_check() must
    still reject a count number that isn't one of the trade's own source
    values."""

    def test_ungrounded_count_not_matching_any_source_value_fails(self):
        source = {"entry_price": 100.0, "exit_price": 108.5, "holding_days": 12}
        text = "This is the 7th time this setup has stopped out early."
        assert numeric_cross_check(text, source) is False


# ─── Regenerate-then-fallback sequencing (Condition 9) ────────────────────

class TestGenerateTradeDebriefSequencing:
    _TRADE = {
        "id": "trade-1", "portfolio_id": "pf-1", "position_id": None,
        "ticker": "AAPL", "entry_price": 100.0, "exit_price": 108.5,
        "pnl": 8.5, "pnl_pct": 8.5, "exit_reason": "Target Reached",
        "holding_days": 12,
    }

    @patch("services.debrief_service.create_claude_audit_entry")
    @patch("services.debrief_service.create_trade_debrief")
    @patch("services.debrief_service.get_red_flag_events", return_value={"items": []})
    @patch("services.debrief_service.get_trade_plans_by_position", return_value=[])
    @patch("services.debrief_service.get_trade_by_id")
    @patch("services.debrief_service.ANTHROPIC_API_KEY", "fake-key")
    def test_compliant_first_attempt_generates_status_ok(
        self, mock_get_trade, mock_get_plans, mock_red_flags, mock_create_debrief, mock_audit
    ):
        mock_get_trade.return_value = dict(self._TRADE)
        mock_usage = MagicMock(input_tokens=50, output_tokens=20)
        mock_create_debrief.return_value = {
            "summary_text": "x", "focus_area_text": "Your exit at 108.5 matched your plan.",
            "generation_status": "ok", "model_version": "claude-haiku-4-5",
            "prompt_version": "v1.0", "generated_at": None,
        }
        with patch("services.debrief_service._call_claude",
                   return_value=("Your exit at 108.5 matched your plan.", mock_usage)):
            result = generate_trade_debrief("trade-1")

        assert result["generation_status"] == "ok"
        # Compliance outcome must be logged, per Condition 9's third bullet.
        assert mock_audit.call_count == 1
        assert mock_audit.call_args.kwargs["compliance_check_result"] == "pass"

    @patch("services.debrief_service.create_claude_audit_entry")
    @patch("services.debrief_service.create_trade_debrief")
    @patch("services.debrief_service.get_red_flag_events", return_value={"items": []})
    @patch("services.debrief_service.get_trade_plans_by_position", return_value=[])
    @patch("services.debrief_service.get_trade_by_id")
    @patch("services.debrief_service.ANTHROPIC_API_KEY", "fake-key")
    def test_prescriptive_first_attempt_regenerates_then_passes(
        self, mock_get_trade, mock_get_plans, mock_red_flags, mock_create_debrief, mock_audit
    ):
        mock_get_trade.return_value = dict(self._TRADE)
        mock_usage = MagicMock(input_tokens=50, output_tokens=20)
        mock_create_debrief.return_value = {
            "summary_text": "x", "focus_area_text": "Your exit at 108.5 matched your plan.",
            "generation_status": "ok", "model_version": "claude-haiku-4-5",
            "prompt_version": "v1.0", "generated_at": None,
        }
        responses = iter([
            ("You should hold winners longer.", mock_usage),          # attempt 1: violation
            ("Your exit at 108.5 matched your plan.", mock_usage),     # attempt 2: compliant
        ])
        with patch("services.debrief_service._call_claude", side_effect=lambda *a, **k: next(responses)):
            result = generate_trade_debrief("trade-1")

        assert result["generation_status"] == "ok"
        assert mock_audit.call_args.kwargs["compliance_check_result"] == "pass_on_regenerate"

    @patch("services.debrief_service.create_claude_audit_entry")
    @patch("services.debrief_service.create_trade_debrief")
    @patch("services.debrief_service.get_red_flag_events", return_value={"items": []})
    @patch("services.debrief_service.get_trade_plans_by_position", return_value=[])
    @patch("services.debrief_service.get_trade_by_id")
    @patch("services.debrief_service.ANTHROPIC_API_KEY", "fake-key")
    def test_two_consecutive_failures_fall_back_never_persist_bad_text(
        self, mock_get_trade, mock_get_plans, mock_red_flags, mock_create_debrief, mock_audit
    ):
        mock_get_trade.return_value = dict(self._TRADE)
        mock_usage = MagicMock(input_tokens=50, output_tokens=20)
        mock_create_debrief.return_value = {
            "summary_text": "x", "focus_area_text": None,
            "generation_status": "fallback_no_focus_area", "model_version": "claude-haiku-4-5",
            "prompt_version": "v1.0", "generated_at": None,
        }
        responses = iter([
            ("You should hold winners longer.", mock_usage),    # attempt 1: violation
            ("Increase your position size next time.", mock_usage),  # attempt 2 (regenerated): violation again
        ])
        with patch("services.debrief_service._call_claude", side_effect=lambda *a, **k: next(responses)):
            result = generate_trade_debrief("trade-1")

        assert result["generation_status"] == "fallback_no_focus_area"
        assert result["focus_area_text"] is None
        # Never persisted with the non-compliant text on either attempt.
        persisted_kwargs = mock_create_debrief.call_args[0][2]
        assert persisted_kwargs["focus_area_text"] is None
        assert "prescriptive_language_detected" in persisted_kwargs["focus_area_omitted_reason"]
        assert mock_audit.call_args.kwargs["compliance_check_result"].startswith("fail_fallback")
        # Exactly one regeneration -- _call_claude invoked exactly twice, not more.
        assert mock_get_trade.call_count == 1

    @patch("services.debrief_service.create_trade_debrief")
    @patch("services.debrief_service.get_trade_plans_by_position", return_value=[])
    @patch("services.debrief_service.get_trade_by_id")
    @patch("services.debrief_service.ANTHROPIC_API_KEY", "")
    def test_no_api_key_falls_back_to_summary_only(self, mock_get_trade, mock_get_plans, mock_create_debrief):
        mock_get_trade.return_value = dict(self._TRADE)
        mock_create_debrief.return_value = {
            "summary_text": "x", "focus_area_text": None,
            "generation_status": "ai_unavailable", "model_version": "claude-haiku-4-5",
            "prompt_version": "v1.0", "generated_at": None,
        }
        result = generate_trade_debrief("trade-1")
        assert result["generation_status"] == "ai_unavailable"
        assert result["focus_area_text"] is None

    @patch("services.debrief_service.get_trade_by_id", return_value=None)
    def test_unknown_trade_raises_value_error(self, mock_get_trade):
        with pytest.raises(ValueError):
            generate_trade_debrief("does-not-exist")
