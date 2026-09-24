"""
ST-11 (BLG-BE-125, EPIC-03, v9.7): Month-closure check and Monthly P&L's own
SQL window must use the same (year, month) clock source.

Prior to this fix, database.get_monthly_pnl()'s 1-year window bound used bare
`CURRENT_DATE`, which resolves against the Postgres session's configured
timezone (not necessarily UTC), while reports_service._is_closed_month()
derives "today" from Python's `datetime.now(timezone.utc).date()`. Near a
month/year boundary, a non-UTC session timezone could disagree with UTC on
the current (year, month) tuple.

No live DB or network connections are made -- SQL text is inspected
structurally, following the pattern already used by
test_null_fee_trade_audit.py::test_get_monthly_pnl_sql_filters_on_either_fee_leg_null.
"""
import importlib.util as _ilu
import inspect
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# tests/conftest.py replaces sys.modules["database"] with a session-scoped MagicMock stub
# (BLG-QA-20/retired BLG-QA-73), so `from database import get_monthly_pnl` here would yield
# a MagicMock, and inspect.getsource() on a MagicMock raises TypeError (confirmed: the
# pre-existing test_null_fee_trade_audit.py::test_get_monthly_pnl_sql_filters_on_either_fee_leg_null
# has this same failure mode). Load a private, isolated copy of the real backend/database.py
# instead -- same pattern as tests/test_reflection_reminder.py / test_monthly_pnl_snapshot.py
# (shared_standards.md §18): never touches sys.modules["database"].
_DATABASE_PY = Path(__file__).parent.parent / "backend" / "database.py"
_spec = _ilu.spec_from_file_location("database_real_for_clock_source_test", _DATABASE_PY)
_real_database = _ilu.module_from_spec(_spec)
with patch.dict("os.environ", {"DATABASE_URL": "postgresql://user:pw@localhost:5432/dummy"}):
    _spec.loader.exec_module(_real_database)


def test_get_monthly_pnl_sql_derives_today_from_utc_not_bare_current_date():
    source = inspect.getsource(_real_database.get_monthly_pnl)
    assert "(NOW() AT TIME ZONE 'UTC')::date" in source, (
        "get_monthly_pnl's window bound must derive 'today' from an explicit "
        "UTC clock, not bare CURRENT_DATE, so it can never disagree with "
        "reports_service._is_closed_month's UTC-based 'today' regardless of "
        "the Postgres session's configured timezone."
    )
    assert "CURRENT_DATE" not in source, (
        "bare CURRENT_DATE resolves against the session timezone, not UTC -- "
        "must not reappear in this query."
    )


def test_is_closed_month_uses_utc_clock():
    """reports_service.get_monthly_pnl_report derives 'today' via
    datetime.now(timezone.utc).date() -- the same UTC clock source the SQL
    window now uses -- not a bare, timezone-naive datetime.now()."""
    import services.reports_service as reports_service
    source = inspect.getsource(reports_service.get_monthly_pnl_report)
    assert "datetime.now(timezone.utc)" in source, (
        "get_monthly_pnl_report must derive 'today' from the UTC clock to "
        "agree with database.get_monthly_pnl's window bound."
    )
