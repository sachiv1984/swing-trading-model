"""
ST-02 (BLG-FE-116, EPIC-02, v7.5): Custom Price Alerts — Unit Tests

Tests the price_alerts CRUD and evaluation logic in isolation.
No database or network calls are made — all I/O is mocked.

Coverage:
  - create_price_alert: ticker/condition/threshold validation, active-alert cap
  - delete_price_alert: not-found handling
  - _evaluate_price_alerts: above/below trigger logic, price-fetch failure handling
  - _price_alert_row: serialisation
"""

import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Database stub is registered by tests/conftest.py (BLG-QA-20).
# Config and utils stubs mirror tests/test_alerts_service.py.

_config_stub = types.ModuleType("config")
_config_stub.DEFAULT_MIN_HOLD_DAYS = 10
_config_stub.TELEGRAM_BOT_TOKEN = ""
_config_stub.TELEGRAM_CHAT_ID = ""
sys.modules["config"] = _config_stub

_pricing_stub = types.ModuleType("utils.pricing")
_pricing_stub.check_market_regime = MagicMock()
_pricing_stub.get_current_price = MagicMock()

_utils_stub = types.ModuleType("utils")
_utils_stub.pricing = _pricing_stub
sys.modules.setdefault("utils", _utils_stub)
sys.modules["utils.pricing"] = _pricing_stub

_health_stub = types.ModuleType("services.health_service")
_health_stub.record_nightly_job = MagicMock()
# Scoped via patch.dict(sys.modules, ...) per-test below (not a bare global
# assignment) — a global sys.modules["services.health_service"] entry would
# leak into other test files sharing this pytest process (e.g.
# test_health_extensions.py, which imports the real module by the same name).

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    "alerts_service",
    Path(__file__).parent.parent / "backend" / "services" / "alerts_service.py"
)
alerts_service = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(alerts_service)

create_price_alert = alerts_service.create_price_alert
delete_price_alert = alerts_service.delete_price_alert
_evaluate_price_alerts = alerts_service._evaluate_price_alerts
_price_alert_row = alerts_service._price_alert_row
PRICE_ALERT_CAP = alerts_service.PRICE_ALERT_CAP


def _pa_row(id_="pa-1", ticker="AAPL", condition="above", threshold=150.0):
    return {"id": id_, "ticker": ticker, "condition": condition, "threshold_price": threshold}


# ---------------------------------------------------------------------------
# 1. create_price_alert — validation
# ---------------------------------------------------------------------------

class TestCreatePriceAlertValidation(unittest.TestCase):

    def test_rejects_missing_ticker(self):
        with self.assertRaises(ValueError):
            create_price_alert("portfolio-1", {"ticker": "", "condition": "above", "threshold_price": 1.0})

    def test_rejects_invalid_ticker_format(self):
        with self.assertRaises(ValueError):
            create_price_alert("portfolio-1", {"ticker": "TOO-LONG!", "condition": "above", "threshold_price": 1.0})

    def test_rejects_invalid_condition(self):
        with self.assertRaises(ValueError):
            create_price_alert("portfolio-1", {"ticker": "AAPL", "condition": "sideways", "threshold_price": 1.0})

    def test_rejects_zero_threshold(self):
        with self.assertRaises(ValueError):
            create_price_alert("portfolio-1", {"ticker": "AAPL", "condition": "above", "threshold_price": 0})

    def test_rejects_negative_threshold(self):
        with self.assertRaises(ValueError):
            create_price_alert("portfolio-1", {"ticker": "AAPL", "condition": "above", "threshold_price": -5})

    def test_rejects_missing_threshold(self):
        with self.assertRaises(ValueError):
            create_price_alert("portfolio-1", {"ticker": "AAPL", "condition": "above", "threshold_price": None})

    def test_ticker_is_uppercased(self):
        with patch.object(alerts_service, "get_db") as mock_db:
            mock_conn = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_conn
            cur = MagicMock()
            cur.fetchone.side_effect = [
                {"cnt": 0},
                {"id": "pa-1", "ticker": "AAPL", "condition": "above", "threshold_price": Decimal("150.0"),
                 "active": True, "triggered_at": None, "created_at": "2026-07-17T10:00:00Z",
                 "updated_at": "2026-07-17T10:00:00Z"},
            ]
            mock_conn.cursor.return_value.__enter__.return_value = cur

            result = create_price_alert("portfolio-1", {"ticker": "aapl", "condition": "above", "threshold_price": 150.0})

            insert_call = cur.execute.call_args_list[-1]
            self.assertEqual(insert_call[0][1][1], "AAPL")
            self.assertEqual(result["ticker"], "AAPL")


class TestCreatePriceAlertCap(unittest.TestCase):

    def test_rejects_when_cap_exceeded(self):
        with patch.object(alerts_service, "get_db") as mock_db:
            mock_conn = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_conn
            cur = MagicMock()
            cur.fetchone.return_value = {"cnt": PRICE_ALERT_CAP}
            mock_conn.cursor.return_value.__enter__.return_value = cur

            with self.assertRaises(ValueError) as ctx:
                create_price_alert("portfolio-1", {"ticker": "AAPL", "condition": "above", "threshold_price": 1.0})
            self.assertIn("maximum number", str(ctx.exception))

    def test_allows_when_under_cap(self):
        with patch.object(alerts_service, "get_db") as mock_db:
            mock_conn = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_conn
            cur = MagicMock()
            cur.fetchone.side_effect = [
                {"cnt": PRICE_ALERT_CAP - 1},
                {"id": "pa-1", "ticker": "AAPL", "condition": "above", "threshold_price": Decimal("150.0"),
                 "active": True, "triggered_at": None, "created_at": "2026-07-17T10:00:00Z",
                 "updated_at": "2026-07-17T10:00:00Z"},
            ]
            mock_conn.cursor.return_value.__enter__.return_value = cur

            result = create_price_alert("portfolio-1", {"ticker": "AAPL", "condition": "above", "threshold_price": 150.0})
            self.assertEqual(result["ticker"], "AAPL")


# ---------------------------------------------------------------------------
# 2. delete_price_alert
# ---------------------------------------------------------------------------

class TestDeletePriceAlert(unittest.TestCase):

    def test_raises_lookup_error_when_not_found(self):
        with patch.object(alerts_service, "get_db") as mock_db:
            mock_conn = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_conn
            cur = MagicMock()
            cur.fetchone.return_value = None
            mock_conn.cursor.return_value.__enter__.return_value = cur

            with self.assertRaises(LookupError):
                delete_price_alert("portfolio-1", "missing-id")

    def test_returns_deleted_true_on_success(self):
        with patch.object(alerts_service, "get_db") as mock_db:
            mock_conn = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_conn
            cur = MagicMock()
            cur.fetchone.return_value = {"id": "pa-1"}
            mock_conn.cursor.return_value.__enter__.return_value = cur

            result = delete_price_alert("portfolio-1", "pa-1")
            self.assertEqual(result, {"deleted": True, "id": "pa-1"})


# ---------------------------------------------------------------------------
# 3. _evaluate_price_alerts — trigger logic
# ---------------------------------------------------------------------------

class TestEvaluatePriceAlerts(unittest.TestCase):
    """
    _evaluate_price_alerts does a local `from services.health_service import
    record_nightly_job` — sys.modules is patched per-test (not globally) so
    the stub never leaks into other test files sharing this pytest process.
    """

    def setUp(self):
        self._sys_modules_patch = patch.dict(sys.modules, {"services.health_service": _health_stub})
        self._sys_modules_patch.start()
        self.addCleanup(self._sys_modules_patch.stop)

    def test_above_condition_triggers_when_price_exceeds_threshold(self):
        cur = MagicMock()
        cur.fetchall.return_value = [_pa_row(condition="above", threshold=150.0)]
        enqueued = []

        with patch.object(alerts_service, "get_current_price", return_value=160.0):
            summary = _evaluate_price_alerts(cur, "portfolio-1", lambda nid: enqueued.append(nid))

        self.assertEqual(summary["triggered"], 1)
        self.assertEqual(summary["errors"], 0)
        self.assertEqual(len(enqueued), 1)

    def test_above_condition_does_not_trigger_when_price_below_threshold(self):
        cur = MagicMock()
        cur.fetchall.return_value = [_pa_row(condition="above", threshold=150.0)]

        with patch.object(alerts_service, "get_current_price", return_value=140.0):
            summary = _evaluate_price_alerts(cur, "portfolio-1", lambda nid: None)

        self.assertEqual(summary["triggered"], 0)

    def test_below_condition_triggers_when_price_under_threshold(self):
        cur = MagicMock()
        cur.fetchall.return_value = [_pa_row(condition="below", threshold=42.10)]

        with patch.object(alerts_service, "get_current_price", return_value=40.0):
            summary = _evaluate_price_alerts(cur, "portfolio-1", lambda nid: None)

        self.assertEqual(summary["triggered"], 1)

    def test_below_condition_does_not_trigger_when_price_above_threshold(self):
        cur = MagicMock()
        cur.fetchall.return_value = [_pa_row(condition="below", threshold=42.10)]

        with patch.object(alerts_service, "get_current_price", return_value=50.0):
            summary = _evaluate_price_alerts(cur, "portfolio-1", lambda nid: None)

        self.assertEqual(summary["triggered"], 0)

    def test_price_fetch_failure_counted_as_error_not_crash(self):
        cur = MagicMock()
        cur.fetchall.return_value = [_pa_row()]

        with patch.object(alerts_service, "get_current_price", side_effect=Exception("network down")):
            summary = _evaluate_price_alerts(cur, "portfolio-1", lambda nid: None)

        self.assertEqual(summary["errors"], 1)
        self.assertEqual(summary["triggered"], 0)

    def test_none_price_counted_as_error(self):
        cur = MagicMock()
        cur.fetchall.return_value = [_pa_row()]

        with patch.object(alerts_service, "get_current_price", return_value=None):
            summary = _evaluate_price_alerts(cur, "portfolio-1", lambda nid: None)

        self.assertEqual(summary["errors"], 1)

    def test_no_active_alerts_returns_zero_summary(self):
        cur = MagicMock()
        cur.fetchall.return_value = []

        summary = _evaluate_price_alerts(cur, "portfolio-1", lambda nid: None)

        self.assertEqual(summary["evaluated"], 0)
        self.assertEqual(summary["triggered"], 0)

    def test_calls_record_nightly_job(self):
        cur = MagicMock()
        cur.fetchall.return_value = []
        _health_stub.record_nightly_job.reset_mock()

        _evaluate_price_alerts(cur, "portfolio-1", lambda nid: None)

        _health_stub.record_nightly_job.assert_called_once()
        self.assertEqual(_health_stub.record_nightly_job.call_args[0][0], "custom_price_alerts")

    def test_triggered_notification_context_includes_price_alert_id(self):
        """ST-09 (BLG-BE-84, EPIC-02, v8.8): the fired notification's context
        must carry the triggering price_alerts row's id, so the frontend can
        pass it through when creating a trade plan from the alert."""
        import json
        cur = MagicMock()
        cur.fetchall.return_value = [_pa_row(id_="pa-42", ticker="TSLA", condition="above", threshold=150.0)]
        cur.fetchone.return_value = {"id": "notif-1"}

        with patch.object(alerts_service, "get_current_price", return_value=160.0):
            _evaluate_price_alerts(cur, "portfolio-1", lambda nid: None)

        insert_calls = [
            c for c in cur.execute.call_args_list
            if "INSERT INTO notifications" in c.args[0]
        ]
        self.assertEqual(len(insert_calls), 1)
        params = insert_calls[0].args[1]
        context = json.loads(params[4])  # (portfolio_id, alert_type, title, message, context)
        self.assertEqual(context["price_alert_id"], "pa-42")
        self.assertEqual(context["ticker"], "TSLA")


# ---------------------------------------------------------------------------
# 4. _price_alert_row serialisation
# ---------------------------------------------------------------------------

class TestPriceAlertRowSerialisation(unittest.TestCase):

    def test_serialises_decimal_threshold_to_float(self):
        row = {
            "id": "pa-1", "ticker": "AAPL", "condition": "above",
            "threshold_price": Decimal("150.5000"), "active": True, "triggered_at": None,
            "created_at": "2026-07-17T10:00:00Z", "updated_at": "2026-07-17T10:00:00Z",
        }
        result = _price_alert_row(row)
        self.assertIsInstance(result["threshold_price"], float)
        self.assertEqual(result["threshold_price"], 150.5)

    def test_id_serialised_as_string(self):
        row = {
            "id": "pa-1", "ticker": "AAPL", "condition": "above",
            "threshold_price": Decimal("1"), "active": True, "triggered_at": None,
            "created_at": "2026-07-17T10:00:00Z", "updated_at": "2026-07-17T10:00:00Z",
        }
        result = _price_alert_row(row)
        self.assertEqual(result["id"], "pa-1")


# ---------------------------------------------------------------------------
# 5. _notif_row context exposure (ST-09, BLG-BE-84, EPIC-02, v8.8)
# ---------------------------------------------------------------------------

class TestNotifRowContextExposure(unittest.TestCase):
    """context (JSONB) was already stored but never returned to callers
    before this story — GET /notifications now exposes it so the frontend
    can read context.price_alert_id / context.ticker."""

    def test_context_included_in_output(self):
        row = {
            "id": "notif-1", "alert_type": "custom_price_alert",
            "title": "Price Alert — TSLA above 250.00", "message": "...",
            "read": False, "created_at": "2026-08-14T14:00:00Z",
            "context": {"ticker": "TSLA", "price_alert_id": "pa-42"},
        }
        result = alerts_service._notif_row(row)
        self.assertEqual(result["context"], {"ticker": "TSLA", "price_alert_id": "pa-42"})

    def test_null_context_passed_through(self):
        """Alert types other than custom_price_alert write no context."""
        row = {
            "id": "notif-2", "alert_type": "stop_loss_approach",
            "title": "...", "message": "...",
            "read": False, "created_at": "2026-08-14T14:00:00Z",
            "context": None,
        }
        result = alerts_service._notif_row(row)
        self.assertIsNone(result["context"])


if __name__ == "__main__":
    unittest.main()
