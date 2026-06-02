"""Unit tests for daily Claude API cost threshold alert logic (ST-09, BLG-OPS-34)."""
import pytest
from unittest.mock import patch, MagicMock


def test_threshold_not_exceeded_no_alert():
    """When daily cost is below threshold, no alert is sent."""
    from services.gemini_service import check_and_alert_daily_cost
    with patch("database.get_daily_ai_cost", return_value={"total_cost_usd": 0.50, "request_count": 5}):
        with patch("config.TELEGRAM_BOT_TOKEN", "test_token"):
            with patch("config.TELEGRAM_CHAT_ID", "123"):
                result = check_and_alert_daily_cost(threshold_usd=1.00)
    assert result["threshold_exceeded"] is False
    assert result["alert_sent"] is False
    assert result["total_cost_usd"] == 0.50


def test_threshold_exceeded_sends_alert():
    """When daily cost meets threshold, Telegram alert is triggered."""
    from services.gemini_service import check_and_alert_daily_cost
    with patch("database.get_daily_ai_cost", return_value={"total_cost_usd": 1.50, "request_count": 12}):
        with patch("config.TELEGRAM_BOT_TOKEN", "test_token"):
            with patch("config.TELEGRAM_CHAT_ID", "123"):
                with patch("urllib.request.urlopen") as mock_urlopen:
                    mock_urlopen.return_value = MagicMock()
                    result = check_and_alert_daily_cost(threshold_usd=1.00)
    assert result["threshold_exceeded"] is True
    assert result["alert_sent"] is True
    assert mock_urlopen.called


def test_threshold_at_exact_boundary():
    """When daily cost equals threshold exactly, alert fires."""
    from services.gemini_service import check_and_alert_daily_cost
    with patch("database.get_daily_ai_cost", return_value={"total_cost_usd": 1.00, "request_count": 8}):
        with patch("config.TELEGRAM_BOT_TOKEN", "test_token"):
            with patch("config.TELEGRAM_CHAT_ID", "123"):
                with patch("urllib.request.urlopen") as mock_urlopen:
                    mock_urlopen.return_value = MagicMock()
                    result = check_and_alert_daily_cost(threshold_usd=1.00)
    assert result["threshold_exceeded"] is True


def test_no_alert_without_telegram_credentials():
    """When Telegram credentials are absent, alert is not sent even if threshold exceeded."""
    from services.gemini_service import check_and_alert_daily_cost
    with patch("database.get_daily_ai_cost", return_value={"total_cost_usd": 2.00, "request_count": 20}):
        with patch("config.TELEGRAM_BOT_TOKEN", ""):
            with patch("config.TELEGRAM_CHAT_ID", ""):
                result = check_and_alert_daily_cost(threshold_usd=1.00)
    assert result["threshold_exceeded"] is True
    assert result["alert_sent"] is False


def test_custom_threshold():
    """Threshold is configurable."""
    from services.gemini_service import check_and_alert_daily_cost
    with patch("database.get_daily_ai_cost", return_value={"total_cost_usd": 0.30, "request_count": 3}):
        with patch("config.TELEGRAM_BOT_TOKEN", ""):
            with patch("config.TELEGRAM_CHAT_ID", ""):
                result = check_and_alert_daily_cost(threshold_usd=0.25)
    assert result["threshold_exceeded"] is True
    assert result["threshold_usd"] == 0.25
