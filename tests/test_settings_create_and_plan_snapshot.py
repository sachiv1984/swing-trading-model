"""
ST-16 (BLG-BE-144, EPIC-02, v9.12): first-time Settings saves keep the strategy
column defaults, and trade-plan snapshots record the strategy_rules.md §11 values.

Since the v9.10 parameter-authority ruling (ESC-EXEC-20261006-01, outcome (a)),
the Settings page no longer sends min_hold_days, atr_period,
atr_multiplier_initial or atr_multiplier_trailing. The first-time create path
(POST /settings) inserted SettingsRequest.dict()'s None for them, writing NULL
over the column defaults. create_plan() copied those row values into
effective_settings_snapshot, which no stop path reads.

The create path runs through the real backend/database.py create_settings() with
a fake connection that records the SQL. No database or network is touched.
"""
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    from fastapi.testclient import TestClient  # noqa: E402
    import main  # noqa: E402
    import routers.trade_plans as trade_plans_router  # noqa: E402

from strategy_parameters import GRACE_PERIOD_DAYS, INITIAL_ATR_MULTIPLIER, PROFIT_ATR_MULTIPLIER  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)

STRATEGY_COLUMNS = ("min_hold_days", "atr_period", "atr_multiplier_initial", "atr_multiplier_trailing")

# What the Settings page sends on a first save since v9.10 (no strategy fields).
SETTINGS_PAGE_BODY = {
    "default_currency": "GBP", "theme": "dark", "uk_commission": 9.95, "us_commission": 0,
    "stamp_duty_rate": 0.005, "fx_fee_rate": 0.0015, "default_risk_percent": 1.0,
}


class _RecordingDb:
    def __init__(self):
        self.executed = []

    @contextmanager
    def __call__(self):
        conn = MagicMock()
        cur = MagicMock()
        cur.execute.side_effect = lambda sql, params=None: self.executed.append((sql, params))
        cur.fetchone.return_value = {"id": "settings-1"}
        conn.cursor.return_value.__enter__.return_value = cur
        yield conn


def _post_settings(body):
    db = _RecordingDb()
    with patch.dict(main.create_settings.__globals__, {"get_db": db}):
        response = CLIENT.post("/settings", json=body)
    return response, db.executed


class TestFirstTimeSettingsSave:

    def test_create_path_leaves_strategy_columns_to_their_defaults(self):
        """ST-16 AC 1: none of the four columns appears in the INSERT, so each keeps its default."""
        response, executed = _post_settings(SETTINGS_PAGE_BODY)
        assert response.status_code == 200
        (sql, params), = executed
        assert sql.startswith("INSERT INTO settings (")
        columns = sql.split("(", 1)[1].split(")", 1)[0].split(", ")
        for column in STRATEGY_COLUMNS:
            assert column not in columns
        assert None not in params
        assert set(columns) == set(SETTINGS_PAGE_BODY)

    def test_supplied_values_are_still_inserted(self):
        response, executed = _post_settings({**SETTINGS_PAGE_BODY, "min_hold_days": 10})
        assert response.status_code == 200
        sql, params = executed[0]
        assert "min_hold_days" in sql and 10 in params

    def test_empty_body_inserts_defaults_only(self):
        response, executed = _post_settings({})
        assert response.status_code == 200
        assert executed[0][0] == "INSERT INTO settings DEFAULT VALUES RETURNING *"


class TestTradePlanSnapshot:

    def _create_plan(self, settings_row):
        captured = {}

        def _capture(portfolio_id, plan_data):
            captured.update(plan_data)
            return {"id": "plan-1", **plan_data}

        names = ("ensure_trade_plans_table", "ensure_si02_trade_plans_columns",
                 "ensure_strategy_version_at_entry_columns", "ensure_triggered_by_price_alert_id_column")
        with patch.multiple(trade_plans_router, **{n: MagicMock() for n in names}), \
             patch.object(trade_plans_router, "_get_portfolio_id", return_value="pf-1"), \
             patch.object(trade_plans_router, "get_latest_snapshot", return_value={"total_value": 10000}), \
             patch.object(trade_plans_router, "get_settings", return_value=[settings_row]), \
             patch.object(trade_plans_router, "create_trade_plan", side_effect=_capture):
            response = CLIENT.post("/trade-plans", json={"ticker": "AAPL", "market": "US"})
        assert response.status_code == 201, response.text
        return captured["effective_settings_snapshot"]

    def test_snapshot_carries_section_11_values_not_the_settings_row(self):
        """ST-16 AC 2: a row that disagrees with §11 (or is NULL) does not reach the snapshot."""
        snapshot = self._create_plan({
            "default_risk_percent": 1.5, "atr_multiplier_initial": 2, "atr_multiplier_trailing": 1, "min_hold_days": 3,
        })
        assert snapshot["atr_multiplier_initial"] == INITIAL_ATR_MULTIPLIER == 5.0
        assert snapshot["atr_multiplier_trailing"] == PROFIT_ATR_MULTIPLIER == 2.0
        assert snapshot["min_hold_days"] == GRACE_PERIOD_DAYS == 10
        assert snapshot["default_risk_percent"] == 1.5
        assert snapshot["captured_at"]

    def test_null_strategy_columns_still_give_section_11_values(self):
        snapshot = self._create_plan({
            "default_risk_percent": 1.0, "atr_multiplier_initial": None, "atr_multiplier_trailing": None, "min_hold_days": None,
        })
        assert (snapshot["atr_multiplier_initial"], snapshot["atr_multiplier_trailing"], snapshot["min_hold_days"]) == (5.0, 2.0, 10)
