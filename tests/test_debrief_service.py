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
    _journal_context_for_trade,
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
        # ST-01 (v9.11): the target is stated as an R multiple.
        assert "2R target" in summary


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


# ─── ST-03 (BLG-BE-108, v9.0) — journal context sources both entry/exit
#     notes and Red Flag Journal events, per Product Owner decision
#     (ESC-EXEC-20260821-01) ───────────────────────────────────────────────

class TestJournalContextForTrade:
    """BLG-BE-108: 'linked journal entries' in ST-06's own AC draws on BOTH
    the trade's entry_note/exit_note (the fields the UI itself labels
    "Trade Journal") and Red Flag Journal events -- not one or the other."""

    def test_includes_entry_and_exit_notes_when_present(self):
        trade = {"ticker": "AAPL", "entry_note": "Broke out on volume.", "exit_note": "Hit target."}
        with patch("services.debrief_service.get_red_flag_events", return_value={"items": []}):
            ctx = _journal_context_for_trade(trade)
        assert "Broke out on volume." in ctx
        assert "Hit target." in ctx

    def test_includes_red_flag_events_when_present(self):
        trade = {"ticker": "AAPL", "entry_note": None, "exit_note": None}
        events = {"items": [{"event_type": "pre_entry_override"}]}
        with patch("services.debrief_service.get_red_flag_events", return_value=events):
            ctx = _journal_context_for_trade(trade)
        assert "pre_entry_override" in ctx
        assert "1 recent flag" in ctx

    def test_includes_both_sources_together_when_both_present(self):
        trade = {"ticker": "AAPL", "entry_note": "Broke out on volume.", "exit_note": None}
        events = {"items": [{"event_type": "pre_entry_override"}]}
        with patch("services.debrief_service.get_red_flag_events", return_value=events):
            ctx = _journal_context_for_trade(trade)
        assert "Broke out on volume." in ctx
        assert "pre_entry_override" in ctx

    def test_blank_or_whitespace_only_notes_are_treated_as_absent(self):
        trade = {"ticker": "AAPL", "entry_note": "   ", "exit_note": ""}
        with patch("services.debrief_service.get_red_flag_events", return_value={"items": []}):
            ctx = _journal_context_for_trade(trade)
        assert ctx == "None"

    def test_no_ticker_and_no_notes_returns_none(self):
        trade = {"ticker": None, "entry_note": None, "exit_note": None}
        assert _journal_context_for_trade(trade) == "None"

    def test_red_flag_lookup_failure_does_not_drop_notes(self):
        trade = {"ticker": "AAPL", "entry_note": "Broke out on volume.", "exit_note": None}
        with patch("services.debrief_service.get_red_flag_events", side_effect=Exception("db down")):
            ctx = _journal_context_for_trade(trade)
        assert "Broke out on volume." in ctx


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


# ─── ST-01 (BLG-BE-152, v9.11) — derived figures: R achieved, stop at exit,
#     entry slippage. Condition 2 ruling (AI Compliance & Governance Officer,
#     agent-mediated, 2026-10-08) binding conditions 1-8. ─────────────────

from services.debrief_service import derive_trade_figures, r_value_check  # noqa: E402

# The three 2026-10-07 production examples (BLG-BE-152 Problem section).
_EX1_TRADE = {
    "id": "t-ex1", "portfolio_id": "pf-1", "position_id": "pos-ex1", "ticker": "MU",
    "market": "US", "entry_price": 926.80, "exit_price": 1058.60, "pnl": 217.56,
    "pnl_pct": 15.80, "exit_reason": "Stop Loss Hit", "holding_days": 16,
}
_EX1_PLAN = {"planned_entry_price": 926.80, "planned_stop_price": 868.00, "r_target": 2.2, "status": "completed"}
_EX1_POSITION = {"initial_stop": 868.00, "current_stop": 1055.00}

_EX2_TRADE = {
    "id": "t-ex2", "portfolio_id": "pf-1", "position_id": "pos-ex2", "ticker": "WDC",
    "market": "US", "entry_price": 100.00, "exit_price": 108.64, "pnl": 64.10,
    "pnl_pct": 8.64, "exit_reason": "Stop Loss Hit", "holding_days": 14,
}
_EX2_PLAN = {"planned_entry_price": 100.00, "planned_stop_price": 90.00, "r_target": 2.2, "status": "completed"}
_EX2_POSITION = {"initial_stop": 90.00, "current_stop": 108.00}


class TestDeriveTradeFigures:
    def test_example_1_r_achieved_and_trailing_stop(self):
        f = derive_trade_figures(_EX1_TRADE, _EX1_PLAN, _EX1_POSITION)
        assert f["r_achieved"] == 2.24
        assert f["r_vs_target"] == 0.04
        assert f["stop_at_exit"] == 1055.00
        assert f["trailing_stop_exit"] is True
        assert f["entry_slippage_pct"] == 0.0

    def test_example_2_r_achieved_below_target(self):
        f = derive_trade_figures(_EX2_TRADE, _EX2_PLAN, _EX2_POSITION)
        assert f["r_achieved"] == 0.86
        assert f["r_vs_target"] == -1.34

    def test_missing_initial_stop_leaves_r_not_computed(self):
        # Binding condition 2: no R when entry - initial_stop is unavailable.
        f = derive_trade_figures(_EX1_TRADE, _EX1_PLAN, None)
        assert f["r_achieved"] is None and f["r_vs_target"] is None

    def test_stop_at_or_above_entry_as_initial_stop_leaves_r_not_computed(self):
        f = derive_trade_figures(_EX1_TRADE, _EX1_PLAN, {"initial_stop": 926.80, "current_stop": 1000.0})
        assert f["r_achieved"] is None

    def test_losing_stop_out_is_not_a_trailing_stop(self):
        trade = dict(_EX2_TRADE, exit_price=90.0, pnl=-100.0, pnl_pct=-10.0)
        f = derive_trade_figures(trade, _EX2_PLAN, {"initial_stop": 90.0, "current_stop": 90.0})
        assert f["trailing_stop_exit"] is False
        assert f["r_achieved"] == -1.0

    def test_entry_slippage_against_plan(self):
        trade = dict(_EX2_TRADE, entry_price=101.0)
        f = derive_trade_figures(trade, _EX2_PLAN, _EX2_POSITION)
        assert f["entry_slippage_pct"] == 1.0


class TestSummaryStatesRAndStopAtExit:
    def test_example_1_states_r_vs_target_and_trailing_stop(self):
        f = derive_trade_figures(_EX1_TRADE, _EX1_PLAN, _EX1_POSITION)
        summary = _build_summary_text(_EX1_TRADE, _EX1_PLAN, f)
        assert "+2.24R against a 2.2R target" in summary
        assert "trailing stop (raised from $868.00 to $1,055.00) was hit" in summary
        assert "Entered at the planned $926.80" in summary
        # The entry price is not repeated when it matched the plan.
        assert summary.count("926.80") == 1
        assert "+£217.56" in summary and "+15.80%" in summary
        assert "after 16 days" in summary

    def test_example_2_states_r_below_target(self):
        f = derive_trade_figures(_EX2_TRADE, _EX2_PLAN, _EX2_POSITION)
        summary = _build_summary_text(_EX2_TRADE, _EX2_PLAN, f)
        assert "+0.86R against a 2.2R target" in summary
        assert "trailing stop" in summary

    def test_example_3_profitable_stop_loss_hit_is_described_as_trailing_stop(self):
        f = derive_trade_figures(_EX1_TRADE, _EX1_PLAN, _EX1_POSITION)
        summary = _build_summary_text(_EX1_TRADE, _EX1_PLAN, f)
        assert "trailing stop" in summary
        assert "contradict" not in summary.lower()

    def test_r_not_recorded_is_stated_when_initial_stop_missing(self):
        f = derive_trade_figures(_EX1_TRADE, _EX1_PLAN, None)
        summary = _build_summary_text(_EX1_TRADE, _EX1_PLAN, f)
        assert "R achieved is not recorded" in summary
        assert "R against" not in summary


class TestNumericCheckAcceptsDerivedR:
    _SOURCE = {
        "entry_price": 926.80, "exit_price": 1058.60, "pnl": 217.56, "pnl_pct": 15.80,
        "holding_days": 16, "planned_entry_price": 926.80, "planned_stop_price": 868.00,
        "r_target": 2.2, "initial_stop": 868.00, "stop_at_exit": 1055.00,
        "r_achieved": 2.24, "r_vs_target": 0.04, "entry_slippage_pct": 0.0,
    }

    def test_focus_area_citing_r_achieved_passes(self):
        text = "This trade exited at 2.24R against a 2.2R target when the trailing stop at 1055.00 was hit."
        assert numeric_cross_check(text, self._SOURCE)
        assert r_value_check(text, self._SOURCE)

    def test_fabricated_r_value_still_fails(self):
        # Binding condition 4.
        text = "This trade exited at 2.5R."
        assert not (numeric_cross_check(text, self._SOURCE) and r_value_check(text, self._SOURCE))

    def test_coarse_rounding_of_r_fails_r_check(self):
        # Binding condition 8: "2R" would pass the value-only check via the
        # 0 dp rounding of 2.24, but an R multiple must match exactly.
        text = "This trade exited at 2R."
        assert numeric_cross_check(text, self._SOURCE)
        assert not r_value_check(text, self._SOURCE)

    def test_known_limitation_r_equal_to_target_value_passes(self):
        # Binding condition 8, recorded known limitation: the check compares
        # values, so "achieved 2.2R" passes because 2.2 is the target.
        assert r_value_check("This trade achieved 2.2R.", self._SOURCE)


class TestPromptIncludesTrailingStopContext:
    @patch("services.debrief_service.create_claude_audit_entry")
    @patch("services.debrief_service.create_trade_debrief")
    @patch("services.debrief_service.get_red_flag_events", return_value={"items": []})
    @patch("services.debrief_service.get_position_by_id")
    @patch("services.debrief_service.get_trade_plans_by_position")
    @patch("services.debrief_service.get_trade_by_id")
    @patch("services.debrief_service.ANTHROPIC_API_KEY", "fake-key")
    def test_profitable_stop_loss_hit_prompt_includes_trailing_stop_at_exit(
        self, mock_get_trade, mock_get_plans, mock_get_position, mock_red_flags, mock_create_debrief, mock_audit
    ):
        mock_get_trade.return_value = dict(_EX1_TRADE)
        mock_get_plans.return_value = [dict(_EX1_PLAN)]
        mock_get_position.return_value = dict(_EX1_POSITION)
        mock_create_debrief.return_value = {
            "summary_text": "x", "focus_area_text": "y", "generation_status": "ok",
            "model_version": "m", "prompt_version": "v1.1", "generated_at": None,
        }
        captured = {}

        def fake_call(system, user, *a, **k):
            captured["system"], captured["user"] = system, user
            return ("This trade exited at 2.24R when the trailing stop at 1055.00 was hit.",
                    MagicMock(input_tokens=1, output_tokens=1))

        with patch("services.debrief_service._call_claude", side_effect=fake_call):
            generate_trade_debrief("t-ex1")

        user = captured["user"]
        assert "Exit reason: Stop Loss Hit" in user
        assert "Stop at exit: 1055.0" in user
        assert "Initial stop: 868.0" in user
        assert "Exit was a trailing stop above entry (computed): yes" in user
        assert "R achieved (computed): 2.24" in user
        assert "Holding days: 16" in user
        assert "trailing stop that locked in a profit" in captured["system"]
        # The position read is read-only (binding condition 6) and the
        # derived R reaches the persisted debrief's compliance outcome.
        mock_get_position.assert_called_once_with("pos-ex1")
        assert mock_audit.call_args.kwargs["compliance_check_result"] == "pass"
        assert mock_audit.call_args.kwargs["prompt_version"] == "v1.1"
