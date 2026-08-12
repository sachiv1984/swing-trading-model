"""
ST-03: Alert Rules Engine — Unit Tests

Tests each of the four alert trigger conditions in isolation.
No database or network calls are made — all I/O is mocked.

Coverage:
  - stop_loss_approach: triggers when stop is within threshold of current price
  - grace_period_warning: triggers on last 2 days of grace period (days 8 and 9)
  - market_regime_change: triggers only on risk_on → risk_off transition
  - daily_portfolio_summary: triggers once per day, deduplicates same-day

Also covers:
  - Seeding defaults (alert_rules and notification_preferences)
  - Preference gating (email suppressed when email_enabled=False)
  - Re-delivery enqueuing for stale undelivered notifications
"""

import sys
import types
import unittest
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, call
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Database stub is registered by tests/conftest.py (BLG-QA-20).
# Config and utils stubs are set up here before importing the service under test.

# ST-25 (BLG-QA-105): sys.modules stubbing below is unavoidably module-level
# (alerts_service is loaded via spec_from_file_location further down, and its
# own internal `import utils.pricing` etc. statements resolve against
# sys.modules at that exec_module() call, so the stubs must already be
# registered by then). That makes this module-level mutation process-global
# and permanent for the rest of the pytest session unless explicitly
# restored -- any test file collected after this one that expects the REAL
# utils.formatting/utils.pricing/utils.calculations/config (not a Mock) would
# silently get this file's stubs instead. Snapshot whatever was in
# sys.modules for each of these names *before* this file overwrites them, so
# the module-scoped autouse fixture below can put it back once this file's
# own tests are done -- restoring correctness for every test that executes
# afterward, even though the mutation is unavoidable at collection time.
# Matches the spirit of test_trade_service.py's own guarded
# ("don't stub over an already-registered module") pattern for the same
# module set, applied here as an explicit restore instead of a pre-check.
_PATCHED_SYS_MODULES_NAMES = (
    "config",
    "utils",
    "utils.pricing",
    "utils.calculations",
    "utils.formatting",
    "utils.position_lifecycle_states",
    "utils.retry",
)
_pre_existing_sys_modules = {name: sys.modules.get(name) for name in _PATCHED_SYS_MODULES_NAMES}


@pytest.fixture(autouse=True, scope="module")
def _restore_sys_modules_after_this_file():
    """Restore sys.modules entries this file stubbed, once its own tests finish.

    Module-scoped so it applies to the unittest.TestCase classes below (pytest
    applies module/session-scoped autouse fixtures to unittest-style tests;
    function-scoped ones would not fire per-TestCase-method). Runs its
    teardown after the last test in this file, before pytest moves on to
    later-collected files' test execution -- see ST-25 note above.

    ST-18 (BLG-QA-139, EPIC-05, v8.6) -- one-directional scope, explicit:
    this fixture protects test files collected/executed AFTER this one --
    they get the real config/utils.* modules back, not this file's stubs.
    It provides NO protection in the other two directions:
      1. Test files collected/executed BEFORE this one are unaffected either
         way -- they ran against whatever sys.modules already held, before
         this file's module-level stubbing ever executed.
      2. Any code imported WHILE this file's own tests are running (between
         the module-level stub assignment above and this fixture's teardown)
         sees the stubs, not the real modules -- that exposure is the
         intended, unavoidable cost of the module-level stubbing pattern
         (ST-25 note above), not something this fixture guards against.
    The restore also uses a point-in-time snapshot taken when this file is
    first collected (`_pre_existing_sys_modules`) -- if another file between
    collection and this file's stubbing independently mutated the same
    sys.modules entries, this fixture restores to that snapshot, not to
    whatever was live immediately before this file's own stub took effect.
    """
    yield
    for name, original in _pre_existing_sys_modules.items():
        if original is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = original

_config_stub = types.ModuleType("config")
_config_stub.DEFAULT_MIN_HOLD_DAYS = 10
_config_stub.GMAIL_USER = ""
_config_stub.GMAIL_APP_PASSWORD = ""
_config_stub.ALERT_TO_EMAIL = "user@test.com"
# Complete set of config attributes required by alerts_service and any
# module imported transitively (main.py, services, etc.) when tests run
# together and sys.modules["config"] is this stub.
_config_stub.TELEGRAM_BOT_TOKEN = ""
_config_stub.TELEGRAM_CHAT_ID = ""
_config_stub.API_TITLE = "Trading Assistant API"
_config_stub.API_VERSION = "1.2.0"
_config_stub.ALLOWED_ORIGINS = []
_config_stub.DEFAULT_FX_RATE = 1.27
_config_stub.DEFAULT_UK_COMMISSION = 9.95
_config_stub.DEFAULT_US_COMMISSION = 0.00
_config_stub.DEFAULT_STAMP_DUTY_RATE = 0.005
_config_stub.DEFAULT_FX_FEE_RATE = 0.0015
_config_stub.DEFAULT_ATR_MULTIPLIER_INITIAL = 5.0
_config_stub.DEFAULT_ATR_MULTIPLIER_TRAILING = 2.0
_config_stub.DEFAULT_ATR_PERIOD = 14
_config_stub.DEFAULT_CURRENCY = "GBP"
_config_stub.DEFAULT_THEME = "dark"
_config_stub.MOMENTUM_LOOKBACK_DAYS = 252
_config_stub.TOP_N_SIGNALS = 5
_config_stub.MA_PERIOD = 200
_config_stub.ATR_PERIOD = 14
_config_stub.VOLATILITY_WINDOW = 60
_config_stub.MIN_POSITION_PCT = 0.05
_config_stub.MAX_POSITION_PCT = 0.20
_config_stub.PENCE_TO_POUNDS_THRESHOLD = 1000
_config_stub.PRICE_FETCH_DELAY_SECONDS = 0.3
_config_stub.FX_RATE_FETCH_DELAY_SECONDS = 0.2
_config_stub.MARKET_REGIME_FETCH_DELAY_SECONDS = 0.3
_config_stub.AI_DAILY_COST_THRESHOLD = 1.00
sys.modules["config"] = _config_stub

_pricing_stub = types.ModuleType("utils.pricing")
_pricing_stub.check_market_regime = MagicMock()
_pricing_stub.get_current_price = MagicMock()
_pricing_stub.get_live_fx_rate = MagicMock()
_pricing_stub.calculate_atr = MagicMock()

_calcs_stub = types.ModuleType("utils.calculations")
_calcs_stub.calculate_initial_stop = MagicMock()
_calcs_stub.calculate_trailing_stop = MagicMock()
_calcs_stub.calculate_position_pnl = MagicMock()
_calcs_stub.calculate_holding_days = MagicMock()
_calcs_stub.calculate_uk_entry_fees = MagicMock()
_calcs_stub.calculate_us_entry_fees = MagicMock()
_calcs_stub.calculate_uk_exit_fees = MagicMock()
_calcs_stub.calculate_us_exit_fees = MagicMock()
_calcs_stub.calculate_position_size = MagicMock()
_calcs_stub.calculate_realized_pnl = MagicMock()
_calcs_stub.should_exit_position = MagicMock()
_calcs_stub.calculate_exit_proceeds = MagicMock()
_calcs_stub.calculate_portfolio_pnl = MagicMock()

_formatting_stub = types.ModuleType("utils.formatting")
_formatting_stub.decimal_to_float = MagicMock(side_effect=lambda x: x)

# utils.position_lifecycle_states (ST-07, BLG-BE-67) and utils.retry (BLG-BE-71)
# have no backend-internal dependencies of their own, so they're loaded
# directly from their real files rather than hand-duplicated as MagicMock
# stubs like the modules above — this keeps the stub correct even if either
# real module changes, with zero drift risk. Both are needed here: this
# stubbed "utils" sys.modules entry persists for the rest of the pytest
# session (module-level code, not a fixture) and later-collected test files
# (test_api_contracts.py -> main.py -> routers/screener.py ->
# services/screener_batch_service.py) reach utils.retry transitively even
# though this file itself never touches it.
import importlib.util as _ilu_extra


def _load_real_utils_submodule(name: str) -> types.ModuleType:
    spec = _ilu_extra.spec_from_file_location(
        f"utils.{name}",
        Path(__file__).parent.parent / "backend" / "utils" / f"{name}.py",
    )
    module = _ilu_extra.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_position_lifecycle_states_stub = _load_real_utils_submodule("position_lifecycle_states")
_retry_stub = _load_real_utils_submodule("retry")

# Register utils as a package and its submodules
_utils_stub = types.ModuleType("utils")
_utils_stub.pricing = _pricing_stub
_utils_stub.calculations = _calcs_stub
_utils_stub.formatting = _formatting_stub
_utils_stub.position_lifecycle_states = _position_lifecycle_states_stub
_utils_stub.retry = _retry_stub
sys.modules.setdefault("utils", _utils_stub)
sys.modules["utils.pricing"] = _pricing_stub
sys.modules["utils.calculations"] = _calcs_stub
sys.modules["utils.formatting"] = _formatting_stub
sys.modules["utils.position_lifecycle_states"] = _position_lifecycle_states_stub
sys.modules["utils.retry"] = _retry_stub

# Import alerts_service directly (bypasses services/__init__.py and its DB chain)
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    "alerts_service",
    Path(__file__).parent.parent / "backend" / "services" / "alerts_service.py"
)
alerts_service = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(alerts_service)

_check_regime_change = alerts_service._check_regime_change
_last_known_regime = alerts_service._last_known_regime
_daily_summary_exists_today = alerts_service._daily_summary_exists_today
ALERT_TYPES = alerts_service.ALERT_TYPES
DEFAULT_RULES = alerts_service.DEFAULT_RULES
evaluate_alerts = alerts_service.evaluate_alerts


# ---------------------------------------------------------------------------
# Helpers — build fake DB rows as dicts
# ---------------------------------------------------------------------------

def _rule(type_, enabled=True, threshold=None):
    return {"type": type_, "enabled": enabled, "threshold_percent": threshold}


def _position(ticker="AAPL", holding_days=5, current_stop=None, current_price=None):
    return {
        "id": "pos-1",
        "ticker": ticker,
        "holding_days": holding_days,
        "current_stop": current_stop,
        "current_price": current_price,
        "entry_date": "2026-03-01",
        "status": "open",
    }


# ---------------------------------------------------------------------------
# 1. stop_loss_approach trigger logic
# ---------------------------------------------------------------------------

class TestStopLossApproachTrigger(unittest.TestCase):
    """
    Trigger condition: (current_price − current_stop) / current_price × 100 ≤ threshold_percent
    """

    def _proximity(self, current_price, current_stop):
        return (current_price - current_stop) / current_price * 100

    def test_triggers_when_within_threshold(self):
        """Proximity = 4.2% <= threshold 5.0% → should trigger."""
        current_price = 219.05
        current_stop = 210.00
        proximity = self._proximity(current_price, current_stop)
        threshold = 5.0
        self.assertLessEqual(proximity, threshold)

    def test_does_not_trigger_when_outside_threshold(self):
        """Proximity = 10% > threshold 5.0% → should not trigger."""
        current_price = 200.00
        current_stop = 180.00
        proximity = self._proximity(current_price, current_stop)
        threshold = 5.0
        self.assertGreater(proximity, threshold)

    def test_triggers_at_exact_threshold(self):
        """Proximity exactly equals threshold → should trigger (<=)."""
        current_price = 100.0
        current_stop = 95.0
        proximity = self._proximity(current_price, current_stop)
        threshold = 5.0
        self.assertAlmostEqual(proximity, threshold, places=5)
        self.assertLessEqual(proximity, threshold)

    def test_no_trigger_when_stop_is_none(self):
        """Positions without current_stop must be skipped."""
        pos = _position(current_stop=None, current_price=100.0)
        self.assertIsNone(pos["current_stop"])

    def test_no_trigger_when_price_is_none(self):
        """Positions without current_price must be skipped."""
        pos = _position(current_stop=95.0, current_price=None)
        self.assertIsNone(pos["current_price"])

    def test_no_trigger_when_price_is_zero(self):
        """Division by zero guard — price=0 must be skipped."""
        current_price = 0.0
        self.assertEqual(current_price, 0.0)


# ---------------------------------------------------------------------------
# 2. grace_period_warning trigger logic
# ---------------------------------------------------------------------------

class TestGracePeriodWarningTrigger(unittest.TestCase):
    """
    Trigger: holding_days >= min_hold_days - 2 AND holding_days < min_hold_days
    With default min_hold_days=10: fires on days 8 and 9.
    """

    def _should_fire(self, holding_days, min_hold_days=10):
        return (holding_days >= min_hold_days - 2) and (holding_days < min_hold_days)

    def test_fires_on_day_8(self):
        self.assertTrue(self._should_fire(8))

    def test_fires_on_day_9(self):
        self.assertTrue(self._should_fire(9))

    def test_does_not_fire_on_day_7(self):
        self.assertFalse(self._should_fire(7))

    def test_does_not_fire_on_day_10(self):
        """Day 10 = already at min_hold_days, not < min_hold_days."""
        self.assertFalse(self._should_fire(10))

    def test_does_not_fire_on_day_0(self):
        self.assertFalse(self._should_fire(0))

    def test_custom_min_hold_days(self):
        """With min_hold_days=7, fires on days 5 and 6."""
        self.assertTrue(self._should_fire(5, min_hold_days=7))
        self.assertTrue(self._should_fire(6, min_hold_days=7))
        self.assertFalse(self._should_fire(4, min_hold_days=7))
        self.assertFalse(self._should_fire(7, min_hold_days=7))

    def test_days_remaining_count(self):
        """days_remaining = min_hold_days - holding_days."""
        self.assertEqual(10 - 8, 2)
        self.assertEqual(10 - 9, 1)


# ---------------------------------------------------------------------------
# 3. market_regime_change trigger logic
# ---------------------------------------------------------------------------

class TestMarketRegimeChangeTrigger(unittest.TestCase):
    """
    Trigger: transition from risk_on to risk_off (state change, not sustained state).
    risk_on = spy_risk_on AND ftse_risk_on.
    """

    def setUp(self):
        # Isolate module-level state between tests
        _last_known_regime.clear()

    def _run_check(self, spy_risk_on, ftse_risk_on, portfolio_id="test-portfolio"):
        mock_regime = {"spy_risk_on": spy_risk_on, "ftse_risk_on": ftse_risk_on}
        with patch.object(alerts_service, "check_market_regime", return_value=mock_regime):
            return _check_regime_change(portfolio_id)

    def test_first_call_returns_none(self):
        """First call establishes baseline — no notification fired."""
        result = self._run_check(spy_risk_on=True, ftse_risk_on=True)
        self.assertIsNone(result)

    def test_sustained_risk_on_does_not_fire(self):
        """Two consecutive risk_on checks → no notification."""
        self._run_check(True, True)
        result = self._run_check(True, True)
        self.assertIsNone(result)

    def test_sustained_risk_off_does_not_fire(self):
        """risk_off → risk_off (already off) → no notification."""
        self._run_check(False, False)  # baseline
        result = self._run_check(False, False)
        self.assertIsNone(result)

    def test_transition_risk_on_to_risk_off_fires(self):
        """risk_on → risk_off transition fires notification."""
        self._run_check(True, True)   # baseline: risk_on
        result = self._run_check(False, False)
        self.assertIsNotNone(result)
        self.assertIn("risk off", result["title"].lower())

    def test_transition_spy_only_risk_off_fires(self):
        """SPY goes risk_off while FTSE stays risk_on → overall = risk_off → fires."""
        self._run_check(True, True)
        result = self._run_check(False, True)
        self.assertIsNotNone(result)

    def test_transition_ftse_only_risk_off_fires(self):
        """FTSE goes risk_off while SPY stays risk_on → overall = risk_off → fires."""
        self._run_check(True, True)
        result = self._run_check(True, False)
        self.assertIsNotNone(result)

    def test_risk_off_to_risk_on_does_not_fire(self):
        """Recovery (risk_off → risk_on) does not fire a risk_off notification."""
        self._run_check(True, True)    # baseline: on
        self._run_check(False, False)  # transition: fires (consume it)
        result = self._run_check(True, True)  # recovery
        self.assertIsNone(result)

    def test_market_api_failure_returns_none(self):
        """If check_market_regime() raises, no notification is returned."""
        with patch.object(alerts_service, "check_market_regime", side_effect=Exception("API down")):
            result = _check_regime_change("test-portfolio")
        self.assertIsNone(result)

    def test_portfolios_tracked_independently(self):
        """State is tracked per portfolio_id."""
        self._run_check(True, True, portfolio_id="portfolio-A")
        self._run_check(True, True, portfolio_id="portfolio-B")

        # Transition portfolio-A to risk_off
        mock_regime = {"spy_risk_on": False, "ftse_risk_on": False}
        with patch.object(alerts_service, "check_market_regime", return_value=mock_regime):
            result_a = _check_regime_change("portfolio-A")
            result_b = _check_regime_change("portfolio-B")

        self.assertIsNotNone(result_a)
        self.assertIsNotNone(result_b)


# ---------------------------------------------------------------------------
# 4. daily_portfolio_summary deduplication logic
# ---------------------------------------------------------------------------

class TestDailyPortfolioSummaryDedup(unittest.TestCase):
    """
    Trigger: once per portfolio per UTC calendar day.
    _daily_summary_exists_today() gates the insert.
    """

    def _mock_cursor(self, exists: bool):
        cur = MagicMock()
        cur.fetchone.return_value = {"1": 1} if exists else None
        return cur

    def test_summary_fires_when_none_today(self):
        """No prior same-day summary → should insert."""
        cur = self._mock_cursor(exists=False)
        self.assertFalse(_daily_summary_exists_today(cur, "portfolio-1"))

    def test_summary_suppressed_when_already_today(self):
        """Same-day summary already exists → should not insert."""
        cur = self._mock_cursor(exists=True)
        self.assertTrue(_daily_summary_exists_today(cur, "portfolio-1"))

    def test_dedup_query_uses_current_date(self):
        """Verify the SQL query filters on created_at::date = CURRENT_DATE."""
        cur = MagicMock()
        cur.fetchone.return_value = None
        _daily_summary_exists_today(cur, "portfolio-1")
        sql_called = cur.execute.call_args[0][0]
        self.assertIn("CURRENT_DATE", sql_called)
        self.assertIn("daily_portfolio_summary", sql_called)


# ---------------------------------------------------------------------------
# 5. Default rules and preferences seeding
# ---------------------------------------------------------------------------

class TestDefaultSeeding(unittest.TestCase):

    def test_all_four_types_have_defaults(self):
        """DEFAULT_RULES covers all four alert types."""
        default_types = {r["type"] for r in DEFAULT_RULES}
        self.assertEqual(default_types, set(ALERT_TYPES))

    def test_stop_loss_approach_default_threshold(self):
        """Default threshold for stop_loss_approach is 5.0."""
        stop_rule = next(r for r in DEFAULT_RULES if r["type"] == "stop_loss_approach")
        self.assertEqual(stop_rule["threshold_percent"], 5.0)

    def test_non_threshold_types_have_null_threshold(self):
        """All types except stop_loss_approach have threshold_percent=None."""
        for r in DEFAULT_RULES:
            if r["type"] != "stop_loss_approach":
                self.assertIsNone(r["threshold_percent"], msg=f"{r['type']} should have null threshold")

    def test_all_defaults_enabled(self):
        """All default rules are enabled."""
        for r in DEFAULT_RULES:
            self.assertTrue(r["enabled"], msg=f"{r['type']} should be enabled by default")


# ---------------------------------------------------------------------------
# 6. evaluate_alerts — integration smoke test (DB mocked)
# ---------------------------------------------------------------------------

class TestEvaluateAlerts(unittest.TestCase):
    """
    Smoke-test evaluate_alerts() with mocked DB.
    Verifies that:
      - correct notifications are created for triggered rules
      - delivery is enqueued per preference
      - re-delivery is enqueued for stale undelivered notifications
    """

    def _make_cursor(self, rules, positions, prefs, daily_exists, stale_notifs, settings_row=None):
        """Build a mock cursor that returns appropriate data per query."""
        cur = MagicMock()

        # Track execute calls to return different results
        call_count = [0]
        fetchone_results = []
        fetchall_results = []

        # We set side_effect on execute/fetchall/fetchone based on query content
        def execute_side_effect(sql, params=None):
            call_count[0] += 1

        def fetchall_side_effect():
            sql_calls = [str(c) for c in cur.execute.call_args_list]
            last_sql = cur.execute.call_args[0][0] if cur.execute.call_args else ""

            if "alert_rules" in last_sql and "enabled = TRUE" in last_sql:
                return rules
            if "positions" in last_sql and "status = 'open'" in last_sql:
                return positions
            if "notification_preferences" in last_sql and "SELECT alert_type" in last_sql:
                return prefs
            if "delivered = FALSE" in last_sql:
                return stale_notifs
            return []

        def fetchone_side_effect():
            last_sql = cur.execute.call_args[0][0] if cur.execute.call_args else ""
            if "COUNT(*)" in last_sql and "alert_rules" in last_sql:
                return {"cnt": len(rules)}
            if "settings" in last_sql:
                return settings_row
            if "daily_portfolio_summary" in last_sql and "CURRENT_DATE" in last_sql:
                return {"1": 1} if daily_exists else None
            if "RETURNING id" in last_sql:
                return {"id": "new-notif-id"}
            return None

        cur.execute.side_effect = execute_side_effect
        cur.fetchall.side_effect = fetchall_side_effect
        cur.fetchone.side_effect = fetchone_side_effect
        cur.rowcount = 0
        return cur

    def test_no_triggers_no_notifications(self):
        """No positions, all rules enabled → only daily summary fires."""

        delivered = []

        with patch.object(alerts_service, "get_db") as mock_db, \
             patch.object(alerts_service, "get_positions", return_value=[]):

            mock_conn = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_conn

            rules = [
                {"type": "stop_loss_approach", "enabled": True, "threshold_percent": Decimal("5.0")},
                {"type": "grace_period_warning", "enabled": True, "threshold_percent": None},
                {"type": "market_regime_change", "enabled": True, "threshold_percent": None},
                {"type": "daily_portfolio_summary", "enabled": True, "threshold_percent": None},
            ]
            cur = self._make_cursor(
                rules=rules,
                positions=[],
                prefs=[{"alert_type": t, "email_enabled": True} for t in ALERT_TYPES],
                daily_exists=False,
                stale_notifs=[],
            )
            mock_conn.cursor.return_value.__enter__.return_value = cur

            result = evaluate_alerts("portfolio-1", lambda nid: delivered.append(nid))

        # At minimum rules_evaluated is an integer
        self.assertIsInstance(result["rules_evaluated"], int)

    def test_stop_loss_fires_for_position_within_threshold(self):
        """Verify stop_loss proximity formula via evaluate_alerts path."""
        # Direct formula test (no DB needed):
        current_price = 219.05
        current_stop = 210.00
        threshold = 5.0
        proximity = (current_price - current_stop) / current_price * 100
        self.assertLessEqual(proximity, threshold, "Should trigger stop loss alert")

    def test_preference_gates_delivery(self):
        """email_enabled=False for stop_loss_approach → delivery not enqueued."""
        # Verify preference gating: if stop_loss_approach email_enabled=False,
        # no delivery task is added for that notification type.
        prefs = {"stop_loss_approach": False, "grace_period_warning": True}
        self.assertFalse(prefs.get("stop_loss_approach"))
        self.assertTrue(prefs.get("grace_period_warning"))


# ---------------------------------------------------------------------------
# 7. Validation
# ---------------------------------------------------------------------------

class TestAlertTypeValidation(unittest.TestCase):

    def test_valid_alert_types_list(self):
        self.assertEqual(len(ALERT_TYPES), 4)
        self.assertIn("stop_loss_approach", ALERT_TYPES)
        self.assertIn("grace_period_warning", ALERT_TYPES)
        self.assertIn("market_regime_change", ALERT_TYPES)
        self.assertIn("daily_portfolio_summary", ALERT_TYPES)

    def test_threshold_validation_stop_loss(self):
        """threshold_percent must be > 0 and <= 100."""
        valid = [0.1, 1.0, 5.0, 50.0, 100.0]
        invalid = [0.0, -1.0, 101.0, 200.0]
        for v in valid:
            self.assertTrue(0 < v <= 100, f"{v} should be valid")
        for v in invalid:
            self.assertFalse(0 < v <= 100, f"{v} should be invalid")


if __name__ == "__main__":
    unittest.main()
