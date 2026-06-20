"""
Pytest configuration for the swing trading model test suite.

Sets up sys.path to include backend/ and provides a dummy DATABASE_URL
environment variable to prevent database.py from raising a ValueError at
import time. Tests that require a real database use their own mocking strategy.
"""
import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock
import pytest

# Add backend to sys.path so all test files can import backend modules directly
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Provide a dummy DATABASE_URL before any test module imports database.py.
# This prevents the "DATABASE_URL environment variable not set" ValueError
# that would otherwise fire at collection time for any test importing the
# backend database module (directly or via services/__init__.py).
# Tests that need a real DB use their own mock/stub strategy.
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test_stub"

# ---------------------------------------------------------------------------
# Session-scoped database stub (BLG-QA-20 / ST-09)
#
# Registered at conftest load time (before any test file is collected) so that
# import-time `from database import <fn>` bindings in service modules resolve
# to MagicMock instances rather than a real DB connection.
#
# test_api_contracts.py intentionally evicts this stub (sys.modules.pop) to
# load the real database.py — that is the correct behaviour for contract tests.
# ---------------------------------------------------------------------------

_DB_STUB_FUNCTIONS = [
    "get_db", "get_portfolio", "get_positions", "update_position",
    "create_position", "update_portfolio_cash", "get_settings",
    "create_trade_history", "update_position_note", "update_position_tags",
    "get_all_tags", "search_positions_by_tags", "get_trade_history",
    "get_trade_history_by_tax_year", "create_cash_transaction",
    "get_cash_transactions", "get_total_deposits_withdrawals",
    "create_portfolio_snapshot", "get_portfolio_snapshots", "get_latest_snapshot",
    "create_signal", "get_signals", "update_signal", "delete_signal",
    "get_all_tickers", "get_peak_portfolio_value",
    "get_all_closed_trades_for_csv_export",
    "get_trade_reflection", "upsert_trade_reflection",
    "get_database_size_bytes", "delete_position",
    "download_ticker_data", "compute_atr_simple", "create_settings", "update_settings",
    "get_trade_plans_by_position", "ensure_planned_entry_price_column",
    "get_monthly_pnl",
    "create_trade_plan", "update_trade_plan", "get_trade_plans", "get_trade_plan_by_id",
    "delete_trade_plan", "ensure_setup_type_column", "ensure_override_acknowledged_column", "ensure_trade_plans_table",
    "get_trade_by_id", "get_position_by_id", "update_position_lifecycle_state",
    "ensure_plan_vs_reality_columns", "ensure_signals_watchlisted_status",
    "ensure_red_flag_events_table", "create_red_flag_event", "get_red_flag_events",
    "ensure_pre_entry_validation_log_table", "log_pre_entry_validation_results",
    "ensure_gemini_audit_log_table", "create_gemini_audit_entry", "purge_gemini_audit_log_older_than_90_days",
    "get_daily_ai_cost",
    "ensure_claude_audit_log_table", "create_claude_audit_entry", "query_claude_audit_log",
    "ensure_si02_trade_plans_columns", "ensure_si02_trade_history_indexes", "get_behavioural_drift_data",
    "ensure_red_flag_events_severity_column",
    "ensure_positions_user_fill_price_column", "ensure_trade_history_fill_price_column",
    "get_gate_metrics",
    "ensure_trade_cost_columns", "update_trade_costs", "get_trade_history_with_stops",
]

_database_stub = types.ModuleType("database")
for _fn in _DB_STUB_FUNCTIONS:
    setattr(_database_stub, _fn, MagicMock())
sys.modules["database"] = _database_stub


@pytest.fixture(scope="session", autouse=True)
def database_stub():
    """Exposes the session-scoped database stub registered at conftest load time."""
    yield _database_stub


# Import mock harness fixtures (BLG-QA-08 / ST-09)
from tests.mock_harness.conftest_extension import (  # noqa: F401, E402
    alpaca_mock_harness,
    yahoo_mock_harness,
    screener_mocks,
    scenario_mocks,
)
