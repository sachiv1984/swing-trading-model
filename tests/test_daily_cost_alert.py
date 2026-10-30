"""Unit tests for daily Claude API cost threshold alert logic (ST-09, BLG-OPS-34)."""
import pytest
from datetime import datetime, timezone
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


def test_second_call_same_day_does_not_resend(monkeypatch):
    """ST-07 (BLG-OPS-172, EPIC-02, v9.9): a second call on the same UTC day,
    with the threshold still exceeded and an alert already sent today, does
    not send a second Telegram message."""
    from services.gemini_service import check_and_alert_daily_cost
    import database

    today = datetime.now(timezone.utc).date().isoformat()
    monkeypatch.setattr(database, "get_last_alert_fingerprint", lambda key: today)
    recorded = []
    monkeypatch.setattr(database, "record_alert_fingerprint", lambda key, fp: recorded.append((key, fp)))
    monkeypatch.setattr(database, "ensure_scheduled_alert_dedup_table", lambda: None)

    with patch("database.get_daily_ai_cost", return_value={"total_cost_usd": 1.50, "request_count": 12}):
        with patch("config.TELEGRAM_BOT_TOKEN", "test_token"):
            with patch("config.TELEGRAM_CHAT_ID", "123"):
                with patch("urllib.request.urlopen") as mock_urlopen:
                    result = check_and_alert_daily_cost(threshold_usd=1.00)

    assert result["threshold_exceeded"] is True
    assert result["alert_sent"] is False
    assert not mock_urlopen.called
    assert recorded == []


def test_new_day_resends_even_though_still_exceeded(monkeypatch):
    """A new UTC day's fingerprint differs from yesterday's stored one, so
    the alert sends fresh regardless of yesterday's alert.

    ST-41 (BLG-OPS-186, EPIC-06, v9.14): the check also reads the previous
    day, so only today's spend is over the threshold here."""
    from services.gemini_service import check_and_alert_daily_cost
    import database

    monkeypatch.setattr(database, "get_last_alert_fingerprint", lambda key: "2020-01-01")
    recorded = []
    monkeypatch.setattr(database, "record_alert_fingerprint", lambda key, fp: recorded.append((key, fp)))
    monkeypatch.setattr(database, "ensure_scheduled_alert_dedup_table", lambda: None)

    today = datetime.now(timezone.utc).date().isoformat()
    spend = lambda day=None: ({"total_cost_usd": 1.50, "request_count": 12} if day == today
                              else {"total_cost_usd": 0.10, "request_count": 1})
    with patch("database.get_daily_ai_cost", side_effect=spend):
        with patch("config.TELEGRAM_BOT_TOKEN", "test_token"):
            with patch("config.TELEGRAM_CHAT_ID", "123"):
                with patch("urllib.request.urlopen") as mock_urlopen:
                    mock_urlopen.return_value = MagicMock()
                    result = check_and_alert_daily_cost(threshold_usd=1.00)

    assert result["alert_sent"] is True
    assert mock_urlopen.called
    assert recorded == [("daily_cost_alert", today)]


def test_custom_threshold():
    """Threshold is configurable."""
    from services.gemini_service import check_and_alert_daily_cost
    with patch("database.get_daily_ai_cost", return_value={"total_cost_usd": 0.30, "request_count": 3}):
        with patch("config.TELEGRAM_BOT_TOKEN", ""):
            with patch("config.TELEGRAM_CHAT_ID", ""):
                result = check_and_alert_daily_cost(threshold_usd=0.25)
    assert result["threshold_exceeded"] is True
    assert result["threshold_usd"] == 0.25
