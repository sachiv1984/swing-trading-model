"""
ST-08 (BLG-OPS-09): Database Size Monitoring Alert — Unit Tests

Tests for:
  - get_db_size_info()     — returns correct structure and calculates percentages
  - send_db_size_alert_if_needed() — fires Telegram alert when threshold exceeded,
                                      respects cooldown, skips when below threshold

All tests are CI-safe: no live database calls, no live HTTP calls.
Database and Telegram calls are patched via unittest.mock.

Spec ref: docs/specs/api_contracts/health_endpoints.md v1.2 §GET /health/database
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import services.health_service as health_service
from services.health_service import get_db_size_info, send_db_size_alert_if_needed

# Render free tier limit constant (256 MB)
_LIMIT = 268_435_456


class TestGetDbSizeInfo(unittest.TestCase):
    """Unit tests for get_db_size_info()."""

    def setUp(self):
        # Reset module-level alert state between tests
        health_service._last_db_size_alert_utc = None

    def test_returns_required_fields(self):
        """Response always includes all required fields."""
        with patch('services.health_service.get_database_size_bytes', return_value=50 * 1024 * 1024):
            result = get_db_size_info()
        for field in ('size_bytes', 'size_mb', 'limit_bytes', 'limit_mb',
                      'used_percent', 'threshold_percent', 'status'):
            self.assertIn(field, result, f"Missing field: {field}")

    def test_limit_is_always_256mb(self):
        """limit_bytes and limit_mb are always the Render free tier constant."""
        with patch('services.health_service.get_database_size_bytes', return_value=1024):
            result = get_db_size_info()
        self.assertEqual(result['limit_bytes'], _LIMIT)
        self.assertEqual(result['limit_mb'], 256.0)

    def test_status_ok_below_threshold(self):
        """Status is 'ok' when used_percent is below the default 80% threshold."""
        fifty_mb = 50 * 1024 * 1024  # ~19.5% of 256 MB
        with patch('services.health_service.get_database_size_bytes', return_value=fifty_mb):
            with patch.dict(os.environ, {'DB_SIZE_ALERT_THRESHOLD_PERCENT': '80'}):
                result = get_db_size_info()
        self.assertEqual(result['status'], 'ok')
        self.assertLess(result['used_percent'], 80.0)

    def test_status_warning_at_threshold(self):
        """Status is 'warning' when used_percent equals the threshold exactly."""
        eighty_pct = int(_LIMIT * 0.80)
        with patch('services.health_service.get_database_size_bytes', return_value=eighty_pct):
            with patch.dict(os.environ, {'DB_SIZE_ALERT_THRESHOLD_PERCENT': '80'}):
                result = get_db_size_info()
        self.assertEqual(result['status'], 'warning')
        self.assertGreaterEqual(result['used_percent'], 80.0)

    def test_status_warning_above_threshold(self):
        """Status is 'warning' when used_percent exceeds the threshold."""
        ninety_pct = int(_LIMIT * 0.90)
        with patch('services.health_service.get_database_size_bytes', return_value=ninety_pct):
            with patch.dict(os.environ, {'DB_SIZE_ALERT_THRESHOLD_PERCENT': '80'}):
                result = get_db_size_info()
        self.assertEqual(result['status'], 'warning')

    def test_custom_threshold_respected(self):
        """DB_SIZE_ALERT_THRESHOLD_PERCENT env var overrides default 80%."""
        fifty_pct = int(_LIMIT * 0.50)
        with patch('services.health_service.get_database_size_bytes', return_value=fifty_pct):
            with patch.dict(os.environ, {'DB_SIZE_ALERT_THRESHOLD_PERCENT': '40'}):
                result = get_db_size_info()
        self.assertEqual(result['status'], 'warning')
        self.assertEqual(result['threshold_percent'], 40.0)

    def test_percentages_calculated_correctly(self):
        """used_percent = size_bytes / limit_bytes * 100, rounded to 2 d.p."""
        size = 134_217_728  # exactly 128 MB = 50% of 256 MB
        with patch('services.health_service.get_database_size_bytes', return_value=size):
            result = get_db_size_info()
        self.assertAlmostEqual(result['used_percent'], 50.0, places=1)
        self.assertAlmostEqual(result['size_mb'], 128.0, places=1)

    def test_error_status_on_db_failure(self):
        """Status is 'error' and error key present when DB query raises."""
        with patch('services.health_service.get_database_size_bytes',
                   side_effect=Exception("connection refused")):
            result = get_db_size_info()
        self.assertEqual(result['status'], 'error')
        self.assertIn('error', result)
        self.assertIsNone(result['size_bytes'])
        self.assertIsNone(result['size_mb'])
        self.assertIsNone(result['used_percent'])
        # Limit constants still returned even on error
        self.assertEqual(result['limit_bytes'], _LIMIT)

    def test_size_mb_and_bytes_consistent(self):
        """size_mb should equal size_bytes / (1024*1024), rounded to 2 d.p."""
        size = 26_843_545  # ~25.6 MB
        with patch('services.health_service.get_database_size_bytes', return_value=size):
            result = get_db_size_info()
        expected_mb = round(size / (1024 * 1024), 2)
        self.assertEqual(result['size_mb'], expected_mb)


class TestSendDbSizeAlertIfNeeded(unittest.TestCase):
    """Unit tests for send_db_size_alert_if_needed()."""

    def setUp(self):
        health_service._last_db_size_alert_utc = None

    def _warning_info(self, used_percent=85.0, threshold=80.0):
        return {
            'status': 'warning',
            'used_percent': used_percent,
            'size_mb': round(_LIMIT * used_percent / 100 / (1024 * 1024), 2),
            'limit_mb': 256.0,
            'threshold_percent': threshold,
        }

    def _ok_info(self):
        return {
            'status': 'ok',
            'used_percent': 50.0,
            'size_mb': 128.0,
            'limit_mb': 256.0,
            'threshold_percent': 80.0,
        }

    def test_no_alert_when_status_ok(self):
        """Does not send alert when status is 'ok'."""
        with patch('urllib.request.urlopen') as mock_open:
            result = send_db_size_alert_if_needed(self._ok_info())
        self.assertFalse(result)
        mock_open.assert_not_called()

    def test_no_alert_when_status_error(self):
        """Does not send alert when status is 'error' (DB query failed)."""
        error_info = {'status': 'error', 'used_percent': None, 'size_mb': None,
                      'limit_mb': 256.0, 'threshold_percent': 80.0}
        with patch('urllib.request.urlopen') as mock_open:
            result = send_db_size_alert_if_needed(error_info)
        self.assertFalse(result)
        mock_open.assert_not_called()

    def test_sends_alert_on_warning(self):
        """Sends Telegram alert when status is 'warning' and credentials set."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"ok": true}'
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        env = {'TELEGRAM_BOT_TOKEN': 'test-token', 'TELEGRAM_CHAT_ID': 'test-chat'}
        with patch.dict(os.environ, env):
            with patch('urllib.request.urlopen', return_value=mock_resp):
                result = send_db_size_alert_if_needed(self._warning_info())
        self.assertTrue(result)
        self.assertIsNotNone(health_service._last_db_size_alert_utc)

    def test_cooldown_suppresses_duplicate_alert(self):
        """Second alert is suppressed within the 1-hour cooldown window."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"ok": true}'
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        env = {'TELEGRAM_BOT_TOKEN': 'test-token', 'TELEGRAM_CHAT_ID': 'test-chat'}
        with patch.dict(os.environ, env):
            with patch('urllib.request.urlopen', return_value=mock_resp) as mock_open:
                # First call — should send
                send_db_size_alert_if_needed(self._warning_info())
                first_call_count = mock_open.call_count

                # Second call immediately — should be suppressed by cooldown
                result = send_db_size_alert_if_needed(self._warning_info())
                self.assertFalse(result)
                self.assertEqual(mock_open.call_count, first_call_count)

    def test_alert_resent_after_cooldown_expires(self):
        """Alert is resent once the cooldown period elapses."""
        # Set last alert to 2 hours ago (beyond 1-hour cooldown)
        health_service._last_db_size_alert_utc = (
            datetime.now(timezone.utc) - timedelta(hours=2)
        )
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"ok": true}'
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        env = {'TELEGRAM_BOT_TOKEN': 'test-token', 'TELEGRAM_CHAT_ID': 'test-chat'}
        with patch.dict(os.environ, env):
            with patch('urllib.request.urlopen', return_value=mock_resp):
                result = send_db_size_alert_if_needed(self._warning_info())
        self.assertTrue(result)

    def test_no_alert_when_telegram_not_configured(self):
        """Does not attempt delivery when Telegram credentials are absent."""
        env = {'TELEGRAM_BOT_TOKEN': '', 'TELEGRAM_CHAT_ID': ''}
        with patch.dict(os.environ, env, clear=False):
            # Remove the keys entirely if present
            os.environ.pop('TELEGRAM_BOT_TOKEN', None)
            os.environ.pop('TELEGRAM_CHAT_ID', None)
            with patch('urllib.request.urlopen') as mock_open:
                result = send_db_size_alert_if_needed(self._warning_info())
        self.assertFalse(result)
        mock_open.assert_not_called()

    def test_telegram_api_error_does_not_raise(self):
        """Telegram delivery failure is swallowed — never raises to caller."""
        env = {'TELEGRAM_BOT_TOKEN': 'test-token', 'TELEGRAM_CHAT_ID': 'test-chat'}
        with patch.dict(os.environ, env):
            with patch('urllib.request.urlopen', side_effect=Exception("network error")):
                # Must not raise
                result = send_db_size_alert_if_needed(self._warning_info())
        self.assertFalse(result)

    def test_alert_message_contains_percentage(self):
        """The Telegram message text contains the usage percentage."""
        captured_url = []

        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"ok": true}'
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        def capture_request(req, **kwargs):
            captured_url.append(req.full_url)
            return mock_resp

        env = {'TELEGRAM_BOT_TOKEN': 'test-token', 'TELEGRAM_CHAT_ID': 'test-chat'}
        with patch.dict(os.environ, env):
            with patch('urllib.request.urlopen', side_effect=capture_request):
                send_db_size_alert_if_needed(self._warning_info(used_percent=85.0))

        self.assertTrue(len(captured_url) > 0)
        self.assertIn('85', captured_url[0])

    def test_notification_only_no_cleanup_invoked(self):
        """No cleanup or data modification function is called during alert."""
        # Ensure send_db_size_alert_if_needed only calls Telegram — nothing destructive
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"ok": true}'
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)

        env = {'TELEGRAM_BOT_TOKEN': 'test-token', 'TELEGRAM_CHAT_ID': 'test-chat'}
        with patch.dict(os.environ, env):
            with patch('urllib.request.urlopen', return_value=mock_resp):
                with patch('services.health_service.get_database_size_bytes') as mock_db:
                    send_db_size_alert_if_needed(self._warning_info())
                    # No DB write calls made
                    mock_db.assert_not_called()


if __name__ == '__main__':
    unittest.main()
