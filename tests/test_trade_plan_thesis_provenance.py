"""
trade_plans thesis provenance regression tests (ST-12, BLG-BE-70, EPIC-03, v8.4).

Stored AI-generated thesis/summary text (trade_plans.setup_thesis /
entry_rationale / etc.) previously had no field recording which model+version
produced it -- gemini_service.py's generate_full_plan()/generate_setup_thesis()
already returned model_version/prompt_version to the caller and logged them
to gemini_audit_log keyed by plan_id, but the *stored* trade_plans row itself
carried no provenance, so retroactive audit required a fragile join via
plan_id (often null at generate-plan time, before a plan exists).

create_trade_plan()/update_trade_plan() now accept and persist
thesis_model_version/thesis_prompt_version -- frontend-passed, nullable, no
backfill of existing rows. No live database required -- verifies the exact
SQL/params via a mocked get_db() connection.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# conftest.py registers a MagicMock stub at sys.modules["database"] (BLG-QA-20).
# Evict it so Python loads the real backend/database.py for the functions under test.
sys.modules.pop("database", None)
import database  # noqa: E402


def _mock_conn(fetchone_row=None):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = fetchone_row
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def test_ensure_thesis_provenance_columns_adds_both_nullable_columns():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.ensure_thesis_provenance_columns()

    sql_statements = [call.args[0] for call in mock_cursor.execute.call_args_list if call.args]
    assert any("thesis_model_version" in s and "ADD COLUMN IF NOT EXISTS" in s for s in sql_statements)
    assert any("thesis_prompt_version" in s and "ADD COLUMN IF NOT EXISTS" in s for s in sql_statements)


def test_create_trade_plan_persists_thesis_provenance_when_provided():
    """AI-generated plan saved as-received: provenance fields populated."""
    fake_row = {"id": "plan-1", "thesis_model_version": "claude-haiku-4-5", "thesis_prompt_version": "v3.0"}
    mock_conn, mock_cursor = _mock_conn(fetchone_row=fake_row)
    data = {
        "ticker": "NVDA",
        "market": "US",
        "setup_thesis": "Momentum breakout above resistance.",
        "thesis_model_version": "claude-haiku-4-5",
        "thesis_prompt_version": "v3.0",
    }
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_trade_plan("portfolio-1", data)

    call = mock_cursor.execute.call_args_list[0]
    sql, params = call.args[0], call.args[1]
    assert "thesis_model_version" in sql and "thesis_prompt_version" in sql
    assert "claude-haiku-4-5" in params
    assert "v3.0" in params


def test_create_trade_plan_leaves_thesis_provenance_null_when_absent():
    """Manually-typed thesis (no AI generation involved): provenance stays null --
    existing pre-ST-12 records are unaffected, and this confirms new manually-authored
    records are not falsely attributed to AI generation either."""
    fake_row = {"id": "plan-2", "thesis_model_version": None, "thesis_prompt_version": None}
    mock_conn, mock_cursor = _mock_conn(fetchone_row=fake_row)
    data = {"ticker": "AAPL", "market": "US", "setup_thesis": "Manually written thesis."}
    with patch.object(database, "get_db", return_value=mock_conn):
        database.create_trade_plan("portfolio-1", data)

    call = mock_cursor.execute.call_args_list[0]
    params = call.args[1]
    # thesis_model_version/thesis_prompt_version are the last two positional params
    assert params[-2] is None
    assert params[-1] is None


def test_update_trade_plan_accepts_thesis_provenance_fields():
    fake_row = {"id": "plan-1", "thesis_model_version": "claude-haiku-4-5", "thesis_prompt_version": "v3.0"}
    mock_conn, mock_cursor = _mock_conn(fetchone_row=fake_row)
    # ST-13 (EPIC-03, v8.4) added a before-state pre-fetch via
    # get_trade_plan_by_id() inside update_trade_plan() for audit-trail
    # purposes -- stub it so this test only exercises the UPDATE itself.
    with patch.object(database, "get_db", return_value=mock_conn), \
         patch.object(database, "get_trade_plan_by_id", return_value=None):
        database.update_trade_plan(
            "plan-1", "portfolio-1",
            {"thesis_model_version": "claude-haiku-4-5", "thesis_prompt_version": "v3.0"},
        )

    update_calls = [c for c in mock_cursor.execute.call_args_list if c.args and "UPDATE trade_plans" in c.args[0]]
    assert len(update_calls) == 1
    sql = update_calls[0].args[0]
    assert "thesis_model_version" in sql
    assert "thesis_prompt_version" in sql
