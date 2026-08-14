"""
Unit tests for SI-05 Phase 1 strategy integrity digest service.

ST-01 AC-7: covers digest generation (data present), empty/zero data state,
Telegram message format compliance (section order, character limit).

ST-01 (EPIC-01, v5.1 cycle 2026-06-21__release-v5.1)
Spec: docs/product/decisions/si05-telegram-message-format-spec.md (BLG-GOV-86)
"""
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helpers — import from the service
# ---------------------------------------------------------------------------

def get_service():
    from services.si05_digest_service import (
        format_si05_section,
        _format_pass_rate,
        _format_override_rate,
        _format_top_rule_breach,
        _integrity_summary_line,
        _escape_mdv2,
        send_si05_digest,
        MAX_MESSAGE_LENGTH,
    )
    return (
        format_si05_section,
        _format_pass_rate,
        _format_override_rate,
        _format_top_rule_breach,
        _integrity_summary_line,
        _escape_mdv2,
        send_si05_digest,
        MAX_MESSAGE_LENGTH,
    )


# ---------------------------------------------------------------------------
# AC-7.1: Digest generation with data present
# ---------------------------------------------------------------------------

class TestFormatSi05SectionDataPresent:
    """Digest generation with realistic compliance data."""

    def test_section_contains_strategy_integrity_header(self):
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 1.0,
            "override_rate": 0.10,
            "top_rule_breach": "regime_gate",
        }
        section = format_si05_section(data)
        assert "*📋 Strategy Integrity*" in section

    def test_section_structure_order_matches_spec(self):
        """Section fields appear in order: pass_rate, red_flag, override, top_rule, summary."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 1.0,
            "override_rate": 0.10,
            "top_rule_breach": "regime_gate",
        }
        section = format_si05_section(data)
        idx_pass = section.index("pass rate")
        idx_red = section.index("Red flag")
        idx_override = section.index("Override rate")
        idx_top = section.index("Top rule breach")
        assert idx_pass < idx_red < idx_override < idx_top

    def test_pass_rate_formatted_as_percentage(self):
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "85\\.0%" in section

    def test_red_flag_count_multiplied_by_7(self):
        """events_per_week=1.0 → red_flag_count = round(1.0 * 7) = 7."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 1.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "7" in section  # red_flag_count = 7

    def test_top_rule_breach_title_cased(self):
        """regime_gate → Regime Gate."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.0,
            "override_rate": 0.05,
            "top_rule_breach": "regime_gate",
        }
        section = format_si05_section(data)
        assert "Regime Gate" in section

    def test_healthy_summary_line_when_all_clear(self):
        """All metrics healthy → summary: Strategy integrity healthy this week."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.90,  # >= 70% → no threshold warning
            "events_per_week": 0.5,         # 0.5 * 7 = 3 → <= 5 → no elevated activity
            "override_rate": 0.05,          # <= 30% → no high override
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "Strategy integrity healthy this week" in section

    def test_character_limit_under_4096(self):
        """Populated section is well under the 4,096-char Telegram limit."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.82,
            "events_per_week": 3.0,
            "override_rate": 0.12,
            "top_rule_breach": "sector_concentration",
        }
        section = format_si05_section(data)
        assert len(section) <= 4096


# ---------------------------------------------------------------------------
# AC-7.2: Empty / zero data state
# ---------------------------------------------------------------------------

class TestFormatSi05SectionEmptyData:
    """Digest generation with empty, null, or zero compliance data."""

    def test_null_pass_rate_shows_na(self):
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": None,
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "N/A" in section

    def test_null_pass_rate_triggers_no_data_summary(self):
        """Rule 1: pass_rate None → 'No pre-entry validation data available this week.'"""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": None,
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "No pre\\-entry validation data available this week" in section

    def test_zero_events_per_week_shows_zero_count(self):
        """events_per_week=0.0 → red_flag_count = 0."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.90,
            "events_per_week": 0.0,
            "override_rate": 0.0,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "🚨 Red flag events \\(7d\\): 0" in section

    def test_null_override_rate_shows_na(self):
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        # Override rate shows N/A
        assert "Override rate" in section
        assert "N/A" in section

    def test_null_top_rule_breach_shows_none_text(self):
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.0,
            "override_rate": 0.05,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "🔍 Top rule breach: None" in section


# ---------------------------------------------------------------------------
# AC-7.3: Telegram message format compliance
# ---------------------------------------------------------------------------

class TestMessageFormatCompliance:
    """Telegram MarkdownV2 format compliance per BLG-GOV-86."""

    def test_section_divider_present(self):
        """Section starts with MarkdownV2-escaped --- divider per spec §4."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": "momentum_gate",
        }
        section = format_si05_section(data)
        assert section.startswith("\\-\\-\\-")

    def test_emojis_present_for_each_metric(self):
        """Each metric line uses its designated emoji per spec §4."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": "momentum_gate",
        }
        section = format_si05_section(data)
        assert "✅" in section   # pass rate
        assert "🚨" in section   # red flags
        assert "⚠️" in section   # override rate
        assert "🔍" in section   # top rule breach

    def test_low_pass_rate_triggers_threshold_warning(self):
        """Rule 2: pass_rate < 70% → threshold warning summary."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.65,  # 65% < 70%
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "Pass rate below threshold" in section

    def test_high_red_flags_triggers_elevated_activity(self):
        """Rule 3: red_flag_count > 5 → elevated activity warning."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 1.0,  # 1.0 * 7 = 7 > 5
            "override_rate": 0.05,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "Elevated red flag activity" in section

    def test_high_override_rate_triggers_warning(self):
        """Rule 4: override_rate > 30% → high override rate warning."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.3,  # 0.3 * 7 = 2.1 ≤ 5 → no rule 3
            "override_rate": 0.35,    # 35% > 30%
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "High override rate" in section

    def test_rules_evaluated_in_order_rule1_wins(self):
        """Rule 1 (pass_rate None) fires even when red_flag_count > 5."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": None,  # Rule 1 fires first
            "events_per_week": 2.0,         # Would trigger rule 3 (14 events)
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "No pre\\-entry validation data available" in section
        assert "Elevated red flag activity" not in section


# ---------------------------------------------------------------------------
# send_si05_digest: no Telegram credentials
# ---------------------------------------------------------------------------

class TestSendSi05Digest:
    """send_si05_digest() behaviour under various conditions."""

    def test_returns_error_without_telegram_credentials(self):
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "", "TELEGRAM_CHAT_ID": ""}):
            result = send_si05_digest()
        assert result["sent"] is False
        assert "credentials" in result["error"].lower()

    def test_returns_error_when_data_unavailable(self):
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=None):
                result = send_si05_digest()
        assert result["sent"] is False
        assert result["error"] is not None

    def test_returns_sent_true_on_success(self):
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("urllib.request.urlopen") as mock_urlopen:
                    mock_urlopen.return_value = MagicMock()
                    result = send_si05_digest()
        assert result["sent"] is True
        assert result["message_length"] > 0
        assert result["error"] is None

    def test_telegram_api_connection_failure_logs_error(self):
        """ST-05 AC-05: Telegram API failure logged at ERROR level; returns sent=False."""
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        no_sleep = lambda _: None  # suppress 30s/60s retry delays in CI
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
                    with patch("services.si05_digest_service.logger") as mock_logger:
                        result = send_si05_digest(_sleep_fn=no_sleep)
        assert result["sent"] is False
        assert result["error"] is not None
        mock_logger.error.assert_called()

    def test_retry_succeeds_on_second_attempt(self):
        """ST-05 AC-03: retry fires on transient failure; succeeds on second attempt."""
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        call_count = {"n": 0}

        def _flaky_urlopen(_url, timeout=10):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise OSError("transient error")
            return MagicMock()

        no_sleep = lambda _: None
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("urllib.request.urlopen", side_effect=_flaky_urlopen):
                    result = send_si05_digest(_sleep_fn=no_sleep)
        assert result["sent"] is True
        assert call_count["n"] == 2  # failed once, succeeded on retry

    def test_message_truncation_at_character_limit(self):
        """Edge case (c): Message exceeding MAX_MESSAGE_LENGTH is truncated before send."""
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, MAX_MESSAGE_LENGTH
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        huge_section = "x" * (MAX_MESSAGE_LENGTH + 500)
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("services.si05_digest_service.format_si05_section", return_value=huge_section):
                    with patch("urllib.request.urlopen") as mock_urlopen:
                        mock_urlopen.return_value = MagicMock()
                        result = send_si05_digest()
        assert result["sent"] is True
        assert result["message_length"] <= MAX_MESSAGE_LENGTH


# ---------------------------------------------------------------------------
# BLG-BE-85 (ST-10, EPIC-02, v8.8): telegram_message_id population
# ---------------------------------------------------------------------------

class TestTelegramMessageIdPopulation:
    def _mock_urlopen_response(self, message_id=987654321):
        """A urlopen() return value shaped like the real Telegram API's
        successful response: usable as a context manager, .read() returns
        the JSON body bytes."""
        import json as _json
        resp = MagicMock()
        resp.read.return_value = _json.dumps(
            {"ok": True, "result": {"message_id": message_id, "date": 1}}
        ).encode("utf-8")
        resp.__enter__.return_value = resp
        resp.__exit__.return_value = False
        return resp

    def test_successful_send_populates_real_telegram_message_id(self):
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("urllib.request.urlopen", return_value=self._mock_urlopen_response()):
                    with patch("services.si05_digest_service._write_delivery_log") as mock_log:
                        result = send_si05_digest()

        assert result["sent"] is True
        mock_log.assert_called_once_with("sent", 4, "987654321", None)  # 0.5/wk * 7 = 3.5 -> round() = 4

    def test_failure_path_still_logs_null_message_id(self):
        """AC: failure-path logging unchanged — no message_id on a failed send."""
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        no_sleep = lambda _: None
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
                    with patch("services.si05_digest_service._write_delivery_log") as mock_log:
                        result = send_si05_digest(_sleep_fn=no_sleep)

        assert result["sent"] is False
        mock_log.assert_called_once()
        assert mock_log.call_args.args[0] == "failed"
        assert mock_log.call_args.args[2] is None  # telegram_message_id still NULL on failure

    def test_malformed_response_falls_back_to_null_message_id(self):
        """A response that doesn't parse as expected must not fail the send
        (message_id logged as NULL, same as before this story)."""
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("urllib.request.urlopen") as mock_urlopen:
                    mock_urlopen.return_value = MagicMock()
                    with patch("services.si05_digest_service._write_delivery_log") as mock_log:
                        result = send_si05_digest()

        assert result["sent"] is True
        assert mock_log.call_args.args[2] is None


# ---------------------------------------------------------------------------
# BLG-BE-87 (ST-11, EPIC-02, v8.8): duration logging around the Telegram send
# ---------------------------------------------------------------------------

class TestTelegramSendDurationLogging:
    def test_success_log_line_includes_elapsed_time(self):
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("urllib.request.urlopen") as mock_urlopen:
                    mock_urlopen.return_value = MagicMock()
                    with patch("services.si05_digest_service.logger") as mock_logger:
                        result = send_si05_digest()

        assert result["sent"] is True
        info_calls = [c for c in mock_logger.info.call_args_list if "SI-05 digest sent" in c.args[0]]
        assert len(info_calls) == 1
        # Format string: "SI-05 digest sent (%d chars) in %.2fs" -> args[2] is elapsed seconds
        assert info_calls[0].args[2] >= 0

    def test_failure_log_line_includes_elapsed_time(self):
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, _7
        ) = get_service()
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        no_sleep = lambda _: None
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
                    with patch("services.si05_digest_service.logger") as mock_logger:
                        result = send_si05_digest(_sleep_fn=no_sleep)

        assert result["sent"] is False
        error_calls = [c for c in mock_logger.error.call_args_list if c.args[0] == "SI-05 Telegram send failed after %.2fs: %s"]
        assert len(error_calls) == 1
        # Format string: "SI-05 Telegram send failed after %.2fs: %s" -> args[1] is elapsed seconds
        assert error_calls[0].args[1] >= 0


# ---------------------------------------------------------------------------
# BLG-FE-74 (ST-02): N/A reason clarification
# ---------------------------------------------------------------------------

class TestNaReasonClarification:
    """AC-01/AC-02: N/A values include parenthetical reason; no-events vs data-unavailable distinct."""

    def test_no_events_reason_shown_in_pass_rate(self):
        """validation_na_reason='no_events' → pass rate shows 'no validation events this week'."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": None,
            "validation_na_reason": "no_events",
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "no validation events this week" in section

    def test_data_unavailable_reason_shown_in_pass_rate(self):
        """validation_na_reason='data_unavailable' → pass rate shows 'data unavailable'."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": None,
            "validation_na_reason": "data_unavailable",
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "data unavailable" in section

    def test_no_events_and_data_unavailable_produce_distinct_messages(self):
        """AC-02: 'no events' and 'data unavailable' are not the same string."""
        format_si05_section = get_service()[0]
        no_events_data = {
            "validation_pass_rate": None,
            "validation_na_reason": "no_events",
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        unavailable_data = {
            "validation_pass_rate": None,
            "validation_na_reason": "data_unavailable",
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section_no_events = format_si05_section(no_events_data)
        section_unavailable = format_si05_section(unavailable_data)
        assert section_no_events != section_unavailable

    def test_no_events_summary_line_distinct_from_data_unavailable(self):
        """Summary line differs: 'No pre-entry validation events' vs 'data available'."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": None,
            "validation_na_reason": "no_events",
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "No pre\\-entry validation events this week" in section
        assert "data available" not in section

    def test_backward_compat_no_na_reason_still_shows_na(self):
        """Without na_reason key, N/A is still shown (backward compat)."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": None,
            "events_per_week": 0.0,
            "override_rate": None,
            "top_rule_breach": None,
        }
        section = format_si05_section(data)
        assert "N/A" in section


# ---------------------------------------------------------------------------
# BLG-FE-73 (ST-01): Deep links in SI-05 digest
# ---------------------------------------------------------------------------

class TestDeepLinks:
    """AC-01: Deep links present in digest when FRONTEND_URL is configured."""

    def test_deep_links_present_when_frontend_url_set(self):
        """With FRONTEND_URL set, digest includes Risk Dashboard and Red Flag Journal links."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        with patch.dict("os.environ", {"FRONTEND_URL": "https://app.example.com"}):
            section = format_si05_section(data)
        assert "Risk Dashboard" in section
        assert "Red Flag Journal" in section
        assert "https://app.example.com/#/RiskDashboard" in section
        assert "https://app.example.com/#/RedFlagJournal" in section

    def test_deep_links_absent_when_frontend_url_not_set(self):
        """Without FRONTEND_URL, no deep links in digest (graceful omission)."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        with patch.dict("os.environ", {}, clear=True):
            import os
            os.environ.pop("FRONTEND_URL", None)
            section = format_si05_section(data)
        # Deep link section is absent but core metrics still present
        assert "Risk Dashboard" not in section
        assert "*📋 Strategy Integrity*" in section

    def test_deep_links_url_construction_strips_trailing_slash(self):
        """FRONTEND_URL with trailing slash produces correct link without double slash."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": None,
        }
        with patch.dict("os.environ", {"FRONTEND_URL": "https://app.example.com/"}):
            section = format_si05_section(data)
        assert "https://app.example.com/#/RiskDashboard" in section
        assert "//RiskDashboard" not in section

    def test_character_limit_with_deep_links(self):
        """Section with deep links still under 4,096-char Telegram limit."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": "sector_concentration",
        }
        with patch.dict("os.environ", {"FRONTEND_URL": "https://app.swingtrading.io"}):
            section = format_si05_section(data)
        assert len(section) <= 4096
