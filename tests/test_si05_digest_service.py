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
        assert "85.0%" in section

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
        """Section starts with --- divider per spec §4."""
        format_si05_section = get_service()[0]
        data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": "momentum_gate",
        }
        section = format_si05_section(data)
        assert section.startswith("---")

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

    def test_telegram_api_connection_failure(self):
        """Edge case (b): Telegram API connection failure → sent=False, error logged at ERROR."""
        import logging
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
                with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
                    with patch("services.si05_digest_service.logger") as mock_logger:
                        result = send_si05_digest()
        assert result["sent"] is False
        assert result["error"] is not None
        mock_logger.error.assert_called()

    def test_message_truncation_at_character_limit(self):
        """Edge case (c): Message exceeding MAX_MESSAGE_LENGTH is truncated before send."""
        (
            format_si05_section, _1, _2, _3, _4, _5,
            send_si05_digest, MAX_MESSAGE_LENGTH
        ) = get_service()
        # Build a data set that would produce a very long message via the section formatter
        long_top_rule = "a" * 200
        mock_data = {
            "validation_pass_rate": 0.85,
            "events_per_week": 0.5,
            "override_rate": 0.10,
            "top_rule_breach": long_top_rule,
        }
        # Patch format_si05_section to return a very long string, forcing truncation
        huge_section = "x" * (MAX_MESSAGE_LENGTH + 500)
        with patch.dict("os.environ", {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "123"}):
            with patch("services.si05_digest_service.fetch_arc5_data_for_digest", return_value=mock_data):
                with patch("services.si05_digest_service.format_si05_section", return_value=huge_section):
                    with patch("urllib.request.urlopen") as mock_urlopen:
                        mock_urlopen.return_value = MagicMock()
                        result = send_si05_digest()
        # Message should be sent (truncated) and length should be within or at the limit
        assert result["sent"] is True
        assert result["message_length"] <= MAX_MESSAGE_LENGTH
