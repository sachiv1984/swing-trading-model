"""
ST-17 (BLG-FR-06, EPIC-03, v9.11): new closed trades carry the strategy
parameters in force at exit -- active multiplier, ATR, grace length and
parameter source (data_model.md DS-29).

Runs the real exit_position() with only the DB layer mocked (same pattern as
tests/test_multi_currency_cost_basis_rounding_audit.py) and checks the
trade_history row it writes. A second check confirms create_trade_history()'s
INSERT names all four DS-29 columns and binds them from trade_data.
"""
import sys
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent))

import services.position_service as position_service  # noqa: E402
from strategy_parameters import GRACE_PERIOD_DAYS, INITIAL_ATR_MULTIPLIER  # noqa: E402
from strategy_version_registry import get_current_strategy_version  # noqa: E402
from _real_database import load_real_database  # noqa: E402

SNAPSHOT_FIELDS = ("active_atr_multiplier", "atr", "grace_period_days", "parameter_source")


def _position(days_held, **overrides):
    position = {
        "id": "pos-1",
        "ticker": "TEST.L",
        "market": "UK",
        "status": "open",
        "shares": 10,
        "total_cost": 1000.0,
        "fees_paid": 0.0,
        "entry_price": 100.0,
        "entry_date": (date(2026, 10, 9) - timedelta(days=days_held)).isoformat(),
        "atr": 3.25,
        "active_atr_multiplier": None,
    }
    position.update(overrides)
    return position


def _exit(position):
    writes = []
    with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 0.0}), \
         patch.object(position_service, "get_positions", return_value=[position]), \
         patch.object(position_service, "get_settings", return_value=[{"uk_commission": 0, "stamp_duty_rate": 0}]), \
         patch.object(position_service, "update_portfolio_cash"), \
         patch.object(position_service, "create_trade_history", side_effect=lambda pid, td: writes.append(td)), \
         patch.object(position_service, "update_position"), \
         patch.object(position_service, "get_trade_plans_by_position", return_value=[]), \
         patch.object(position_service, "ensure_planned_entry_price_column", return_value=None):
        position_service.exit_position(position_id="pos-1", exit_price=110.0, exit_date="2026-10-09")
    assert len(writes) == 1
    return writes[0]


class TestClosedTradeCarriesParameters:
    def test_post_grace_exit_copies_the_stamped_multiplier_and_atr(self):
        row = _exit(_position(20, active_atr_multiplier=2.0))
        assert row["active_atr_multiplier"] == 2.0
        assert row["atr"] == 3.25
        assert row["grace_period_days"] == GRACE_PERIOD_DAYS == 10
        assert row["parameter_source"] == f"strategy_rules_s11_v{get_current_strategy_version()}"

    def test_in_grace_exit_records_the_initial_multiplier(self):
        # Stop frozen at the §5 initial stop during grace (strategy_rules.md §6.3 v1.15).
        row = _exit(_position(3))
        assert row["active_atr_multiplier"] == INITIAL_ATR_MULTIPLIER == 5.0
        assert row["atr"] == 3.25

    def test_post_grace_exit_without_a_stamped_multiplier_stays_null(self):
        # Never recomputed since DS-22: the multiplier is unknown, so none is invented.
        row = _exit(_position(20))
        assert row["active_atr_multiplier"] is None
        assert row["grace_period_days"] == 10

    def test_missing_atr_stays_null(self):
        row = _exit(_position(20, atr=None, active_atr_multiplier=5.0))
        assert row["atr"] is None
        assert row["active_atr_multiplier"] == 5.0

    def test_partial_exit_also_carries_the_snapshot(self):
        position = _position(20, active_atr_multiplier=2.0)
        writes = []
        with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 0.0}), \
             patch.object(position_service, "get_positions", return_value=[position]), \
             patch.object(position_service, "get_settings", return_value=[{"uk_commission": 0, "stamp_duty_rate": 0}]), \
             patch.object(position_service, "update_portfolio_cash"), \
             patch.object(position_service, "create_trade_history", side_effect=lambda pid, td: writes.append(td)), \
             patch.object(position_service, "update_position"), \
             patch.object(position_service, "get_trade_plans_by_position", return_value=[]), \
             patch.object(position_service, "ensure_planned_entry_price_column", return_value=None):
            position_service.exit_position(position_id="pos-1", exit_price=110.0, shares=4, exit_date="2026-10-09")
        assert all(writes[0][f] is not None for f in SNAPSHOT_FIELDS)


class TestInsertPersistsTheSnapshot:
    def test_insert_names_and_binds_all_four_columns(self):
        cursor = MagicMock()
        conn = MagicMock()
        conn.__enter__.return_value = conn
        conn.cursor.return_value.__enter__.return_value = cursor
        trade = {f: f"value-{f}" for f in SNAPSHOT_FIELDS}
        database = load_real_database("database_real_for_trade_parameter_snapshot_test")
        with patch.object(database, "get_db", return_value=conn):
            database.create_trade_history("portfolio-1", trade)
        sql, params = cursor.execute.call_args[0]
        columns = sql.split("INSERT INTO trade_history (")[1].split(")")[0]
        column_names = [c.strip() for c in columns.split(",")]
        assert sql.count("%s") == len(column_names) == len(params)
        for field in SNAPSHOT_FIELDS:
            assert params[column_names.index(field)] == f"value-{field}"
