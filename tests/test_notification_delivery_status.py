"""
ST-03 (BLG-FE-318, EPIC-01, v9.18): notification delivery truth — backend unit tests

Design: docs/design/2026-11-18__release-v9.18/alert-delivery-truth/decision_record.md §2–§3
Contract: docs/specs/api_contracts/alerts_endpoints.md §GET /notifications (delivery_status,
delivery_reason)

Covers:
  - derive_delivery_status: every stored state in the decision record's §3.2 table, the
    legacy pre-v9.18 strings, and the 2026-11-19 rulings (delivery_reason; legacy
    delivered=TRUE/'email not configured' rows report sent).
  - deliver_notification with Telegram unconfigured: the row is stored NOT delivered with
    'Telegram not configured' (AC 2), and attempts are counted so re-delivery stops at 3.
  - get_notifications: each item carries delivery_status/delivery_reason derived from its
    stored columns and the per-type preference.

No database or network calls — all I/O is mocked.
"""

import importlib.util as _ilu
import sys
import types
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

_config_stub = types.ModuleType("config")
_config_stub.DEFAULT_MIN_HOLD_DAYS = 10
_config_stub.TELEGRAM_BOT_TOKEN = ""
_config_stub.TELEGRAM_CHAT_ID = ""
_pricing_stub = types.ModuleType("utils.pricing")
_pricing_stub.check_market_regime = MagicMock()
_pricing_stub.get_current_price = MagicMock()
from tests._scoped_utils_stubs import scoped_stub_modules, stub_utils_package  # noqa: E402
_utils_stub = stub_utils_package(pricing=_pricing_stub)

_spec = _ilu.spec_from_file_location(
    "alerts_service_st03_v918",
    Path(__file__).parent.parent / "backend" / "services" / "alerts_service.py",
)
alerts_service = _ilu.module_from_spec(_spec)
with scoped_stub_modules({"config": _config_stub, "utils": _utils_stub, "utils.pricing": _pricing_stub}):
    _spec.loader.exec_module(alerts_service)

derive = alerts_service.derive_delivery_status


def _mock_db(cursor):
    conn = MagicMock()
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    conn.cursor.return_value.__enter__ = MagicMock(return_value=cursor)
    conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    return MagicMock(return_value=conn)


class TestDeriveDeliveryStatus(unittest.TestCase):
    """Decision record §3.2, one row per stored state (worked examples)."""

    def test_delivered_without_error_is_sent(self):
        self.assertEqual(derive(True, 1, None, True), ("sent", None))

    def test_legacy_unconfigured_row_stored_delivered_is_sent(self):
        # Ruling 2026-11-19: pre-v9.18 rows (TRUE, 'email not configured') are not rewritten
        # and report sent, so no "Not sent" line shows for them.
        self.assertEqual(derive(True, 1, "email not configured", True), ("sent", None))

    def test_disabled_error_new_and_legacy_strings_are_not_requested(self):
        # The reflection reminder with its preference off is stored delivered = TRUE.
        self.assertEqual(derive(True, 0, "Telegram off for this alert type", False), ("not_requested", None))
        self.assertEqual(derive(True, 0, "email disabled", False), ("not_requested", None))

    def test_never_attempted_with_preference_off_is_not_requested(self):
        self.assertEqual(derive(False, 0, None, False), ("not_requested", None))

    def test_never_attempted_with_preference_on_is_pending(self):
        self.assertEqual(derive(False, 0, None, True), ("pending", None))

    def test_unconfigured_is_not_sent_from_the_first_attempt(self):
        for attempts in (1, 2, 3, 4):
            self.assertEqual(
                derive(False, attempts, "Telegram not configured", True),
                ("not_sent", "telegram_not_configured"),
                attempts,
            )

    def test_other_error_below_three_attempts_is_pending(self):
        self.assertEqual(derive(False, 1, "HTTP Error 502", True), ("pending", None))
        self.assertEqual(derive(False, 2, "HTTP Error 502", True), ("pending", None))

    def test_other_error_at_three_attempts_is_not_sent_delivery_failed(self):
        # Boundary: exactly MAX_DELIVERY_ATTEMPTS.
        self.assertEqual(derive(False, 3, "HTTP Error 502", True), ("not_sent", "delivery_failed"))
        self.assertEqual(derive(False, 5, "timed out", False), ("not_sent", "delivery_failed"))

    def test_failed_row_that_will_not_be_retried_is_not_sent(self):
        # Review finding (2026-11-19): evaluate_alerts retries only unread rows of an
        # enabled type, so a read row, or one whose preference is now off, never reaches
        # 3 attempts and must not stay pending forever.
        self.assertEqual(derive(False, 1, "HTTP Error 502", True, read=True), ("not_sent", "delivery_failed"))
        self.assertEqual(derive(False, 2, "HTTP Error 502", False), ("not_sent", "delivery_failed"))
        # A read or preference-off row never attempted is not a failure.
        self.assertEqual(derive(False, 0, None, False, read=True), ("not_requested", None))
        self.assertEqual(derive(False, 0, None, True, read=True), ("pending", None))

    def test_null_attempts_treated_as_zero(self):
        self.assertEqual(derive(False, None, None, True), ("pending", None))
        self.assertEqual(derive(None, None, None, False), ("not_requested", None))

    def test_reason_only_set_for_not_sent(self):
        for args in [(True, 1, None, True), (False, 0, None, False), (False, 1, "x", True)]:
            status, reason = derive(*args)
            self.assertNotEqual(status, "not_sent")
            self.assertIsNone(reason)


class TestDeliverNotificationUnconfigured(unittest.TestCase):
    """AC 2: with Telegram unconfigured, a new notification is stored as not delivered."""

    def test_unconfigured_records_not_delivered_with_telegram_error(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"id": "n1", "alert_type": "stop_loss_approach", "title": "t", "message": "m"}
        with patch.object(alerts_service, "get_db", _mock_db(cur)), \
             patch.object(alerts_service, "TELEGRAM_BOT_TOKEN", ""), \
             patch.object(alerts_service, "TELEGRAM_CHAT_ID", ""), \
             patch.object(alerts_service, "_send_via_telegram") as send:
            alerts_service.deliver_notification("n1")
        send.assert_not_called()
        sql, params = cur.execute.call_args_list[-1].args
        self.assertIn("delivered = FALSE", sql)
        self.assertNotIn("delivered = TRUE", sql)
        self.assertIn("delivery_attempts = delivery_attempts + 1", sql)
        self.assertEqual(params, ("Telegram not configured", "n1"))

    def test_configured_success_still_records_delivered(self):
        cur = MagicMock()
        cur.fetchone.return_value = {"id": "n2", "alert_type": "stop_loss_approach", "title": "t", "message": "m"}
        with patch.object(alerts_service, "get_db", _mock_db(cur)), \
             patch.object(alerts_service, "TELEGRAM_BOT_TOKEN", "tok"), \
             patch.object(alerts_service, "TELEGRAM_CHAT_ID", "chat"), \
             patch.object(alerts_service, "_send_via_telegram") as send:
            alerts_service.deliver_notification("n2")
        send.assert_called_once()
        sql, _ = cur.execute.call_args_list[-1].args
        self.assertIn("delivered = TRUE", sql)
        self.assertIn("delivery_error = NULL", sql)


class TestGetNotificationsDeliveryFields(unittest.TestCase):

    def test_items_carry_derived_delivery_status_and_reason(self):
        created = datetime(2026, 11, 19, 9, 0, tzinfo=timezone.utc)

        def row(i, alert_type, delivered, attempts, error):
            return {"id": i, "alert_type": alert_type, "title": "t", "message": "m", "read": False,
                    "created_at": created, "context": None, "delivered": delivered,
                    "delivery_attempts": attempts, "delivery_error": error}

        rows = [
            row("a", "stop_loss_approach", False, 1, "Telegram not configured"),
            row("b", "stop_loss_approach", False, 3, "HTTP Error 502"),
            row("c", "stop_loss_approach", True, 1, None),
            row("d", "grace_period_warning", False, 0, None),       # preference off
            row("e", "reflection_reminder", True, 0, "Telegram off for this alert type"),
            row("f", "custom_price_alert", False, 0, None),         # no preference row -> on
            row("g", "stop_loss_approach", True, 1, "email not configured"),  # legacy
        ]
        cur = MagicMock()
        cur.fetchone.return_value = {"cnt": len(rows)}
        cur.fetchall.side_effect = [
            rows,
            [{"alert_type": "stop_loss_approach", "email_enabled": True},
             {"alert_type": "grace_period_warning", "email_enabled": False},
             {"alert_type": "reflection_reminder", "email_enabled": False}],
        ]
        with patch.object(alerts_service, "get_db", _mock_db(cur)):
            result = alerts_service.get_notifications("portfolio-1")

        got = {n["id"]: (n["delivery_status"], n["delivery_reason"]) for n in result["notifications"]}
        self.assertEqual(got, {
            "a": ("not_sent", "telegram_not_configured"),
            "b": ("not_sent", "delivery_failed"),
            "c": ("sent", None),
            "d": ("not_requested", None),
            "e": ("not_requested", None),
            "f": ("pending", None),
            "g": ("sent", None),
        })
        # Raw delivery columns stay server-side (ruling 2026-11-19).
        for n in result["notifications"]:
            self.assertNotIn("delivery_error", n)
            self.assertNotIn("delivered", n)
            self.assertNotIn("delivery_attempts", n)
        select_sql = cur.execute.call_args_list[1].args[0]
        self.assertIn("delivered, delivery_attempts, delivery_error", select_sql)


class TestMarkReadReturnsDeliveryFields(unittest.TestCase):

    def test_patch_item_has_the_same_delivery_fields_as_the_feed(self):
        cur = MagicMock()
        cur.fetchone.return_value = {
            "id": "n1", "alert_type": "stop_loss_approach", "title": "t", "message": "m", "read": True,
            "created_at": datetime(2026, 11, 19, tzinfo=timezone.utc), "context": None,
            "delivered": False, "delivery_attempts": 1, "delivery_error": "Telegram not configured",
        }
        cur.fetchall.return_value = [{"alert_type": "stop_loss_approach", "email_enabled": True}]
        with patch.object(alerts_service, "get_db", _mock_db(cur)):
            item = alerts_service.mark_notification_read("portfolio-1", "n1")
        self.assertEqual((item["delivery_status"], item["delivery_reason"]), ("not_sent", "telegram_not_configured"))
        self.assertIn("delivered, delivery_attempts, delivery_error", cur.execute.call_args_list[0].args[0])


if __name__ == "__main__":
    unittest.main()
