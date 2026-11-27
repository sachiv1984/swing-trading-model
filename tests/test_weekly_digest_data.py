"""
GET /digest/weekly data — journal completion fields (ST-14, EPIC-03, v9.18,
BLG-SPEC-204).

- AC 1: no API field named "compliance" is the only carrier of the journal
  completion rate: `journal_completion_rate_current` / `_7d_ago` carry it, and
  the `compliance_score_*` names stay as deprecated aliases with the same values.
- AC 2 (with the contract and metrics_definitions.md): the digest uses the
  same predicate as GET /analytics/compliance-metrics.
- Ruling 2026-11-27 (Metrics Definitions & Analytics Owner / Product Owner):
  `closed_trades_total` and `closed_trades_total_7d_ago` let the page tell
  "no closed trades" from "no notes" (both rates are 0.0 then).
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    import database as real_database  # noqa: E402


def _conn(all_trades, before_window):
    """A connection whose cursor answers each digest query by its SQL.

    all_trades / before_window: (total, with_notes) for the two journal
    completion queries, as `COUNT(*)` / `COUNT(CASE ...)` would return them.
    """
    cur = MagicMock()
    state = {}

    def execute(sql, params=None):
        if "SUM(pnl)" in sql:
            state["row"] = {"realised_pnl_7d": 0}
        elif "FROM red_flag_events" in sql:
            state["row"] = {"red_flags": 2}
        elif "FROM notifications" in sql:
            state["row"] = {"fired": 0, "dismissed": 0}
        elif "with_notes" in sql and "exit_date <" in sql:
            state["row"] = {"total": before_window[0], "with_notes": before_window[1]}
        elif "with_notes" in sql:
            state["row"] = {"total": all_trades[0], "with_notes": all_trades[1]}
        else:  # portfolio_history snapshots: none yet
            state["row"] = None

    cur.execute.side_effect = execute
    cur.fetchone.side_effect = lambda: state["row"]
    conn = MagicMock()
    conn.cursor.return_value = cur
    return conn


@pytest.mark.parametrize(
    "all_trades, before, expected",
    [
        # (total, with_notes) for all / before-window → (rate_now, rate_7d, n, n_7d)
        ((0, 0), (0, 0), (0.0, 0.0, 0, 0)),          # no closed trades at all
        ((3, 0), (0, 0), (0.0, 0.0, 3, 0)),          # trades, no notes; none before the window
        ((3, 2), (0, 0), (66.7, 0.0, 3, 0)),         # every trade closed this week (ruling case)
        ((40, 29), (37, 26), (72.5, 70.3, 40, 37)),  # 70.27 rounds to 70.3
        ((1, 1), (1, 1), (100.0, 100.0, 1, 1)),
    ],
)
def test_journal_completion_fields(all_trades, before, expected):
    data = real_database.get_weekly_digest_data(conn=_conn(all_trades, before))
    rate_now, rate_7d, n, n_7d = expected
    assert data["journal_completion_rate_current"] == rate_now
    assert data["journal_completion_rate_7d_ago"] == rate_7d
    assert data["closed_trades_total"] == n
    assert data["closed_trades_total_7d_ago"] == n_7d
    # Deprecated aliases carry the same values.
    assert data["compliance_score_current"] == data["journal_completion_rate_current"]
    assert data["compliance_score_7d_ago"] == data["journal_completion_rate_7d_ago"]


def test_zero_rate_is_distinguishable_from_no_trades():
    no_trades = real_database.get_weekly_digest_data(conn=_conn((0, 0), (0, 0)))
    no_notes = real_database.get_weekly_digest_data(conn=_conn((3, 0), (3, 0)))
    assert no_trades["journal_completion_rate_current"] == no_notes["journal_completion_rate_current"] == 0.0
    assert no_trades["closed_trades_total"] == 0
    assert no_notes["closed_trades_total"] == 3


def test_failed_journal_query_is_null_not_zero():
    """A failed query must not read as "no closed trades" (contract: 0 means none)."""
    conn = _conn((40, 29), (37, 26))
    cur = conn.cursor.return_value
    answer = cur.execute.side_effect

    def execute(sql, params=None):
        if "with_notes" in sql and "exit_date <" not in sql:
            raise RuntimeError("connection reset")
        answer(sql, params)

    cur.execute.side_effect = execute
    data = real_database.get_weekly_digest_data(conn=conn)
    assert data["journal_completion_rate_current"] is None
    assert data["closed_trades_total"] is None
    # The other query still answers: a partial failure stays visible.
    assert data["journal_completion_rate_7d_ago"] == 70.3
    assert data["closed_trades_total_7d_ago"] == 37
    # Deprecated aliases keep their old never-null 0.0.
    assert data["compliance_score_current"] == 0.0
    assert data["compliance_score_7d_ago"] == 70.3
    # The aborted transaction is cleared so later queries can run.
    assert conn.rollback.called


# The predicate match with GET /analytics/compliance-metrics (AC 2) is checked
# against real Postgres in tests/test_weekly_digest_postgres.py.


def test_red_flags_7d_counts_the_rolling_window():
    """ST-16: red_flag_events created at or after now − 7 days (same window as alerts)."""
    conn = _conn((0, 0), (0, 0))
    cur = conn.cursor.return_value
    data = real_database.get_weekly_digest_data(conn=conn)
    assert data["red_flags_7d"] == 2
    flag_calls = [c for c in cur.execute.call_args_list if "FROM red_flag_events" in c.args[0]]
    alert_calls = [c for c in cur.execute.call_args_list if "FROM notifications" in c.args[0]]
    assert len(flag_calls) == 1
    assert "created_at >= %s" in flag_calls[0].args[0]
    assert flag_calls[0].args[1] == alert_calls[0].args[1]  # one shared cutoff


def test_red_flags_7d_null_on_failure():
    conn = _conn((0, 0), (0, 0))
    cur = conn.cursor.return_value
    answer = cur.execute.side_effect

    def execute(sql, params=None):
        if "FROM red_flag_events" in sql:
            raise RuntimeError("relation does not exist")
        answer(sql, params)

    cur.execute.side_effect = execute
    data = real_database.get_weekly_digest_data(conn=conn)
    assert data["red_flags_7d"] is None
    assert data["closed_trades_total"] == 0  # later queries still ran



# ---------------------------------------------------------------------------
# ST-17 (EPIC-03, v9.18, BLG-FEAT-103): this week's loop.
# ---------------------------------------------------------------------------
from datetime import datetime, timezone  # noqa: E402


@pytest.mark.parametrize(
    "now, monday",
    [
        (datetime(2026, 11, 27, 14, 15, tzinfo=timezone.utc), "2026-11-23"),  # Friday
        (datetime(2026, 11, 23, 0, 0, tzinfo=timezone.utc), "2026-11-23"),    # Monday 00:00
        (datetime(2026, 11, 22, 23, 59, 59, tzinfo=timezone.utc), "2026-11-16"),  # Sunday 23:59:59
        (datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc), "2025-12-29"),      # ISO week across a year
        # A non-UTC input is read in UTC: Mon 00:30 at +01:00 is Sun 23:30 UTC.
        (datetime.fromisoformat("2026-11-23T00:30:00+01:00"), "2026-11-16"),
    ],
)
def test_iso_week_start_utc(now, monday):
    start = real_database.iso_week_start_utc(now)
    assert start.isoformat() == f"{monday}T00:00:00+00:00"


def test_loop_counts_and_failure_isolation():
    conn = _conn((0, 0), (0, 0))
    cur = conn.cursor.return_value
    answer = cur.execute.side_effect
    counts = {"FROM signals": 3, "FROM trade_plans": 1, "FROM positions": 1, "FROM trade_reflections": 0}
    seen = []
    state = {}

    def execute(sql, params=None):
        seen.append((sql, params))
        if "FROM loop_events" in sql:
            raise RuntimeError('relation "loop_events" does not exist')
        for key, n in counts.items():
            if key in sql and "COUNT" in sql and "with_notes" not in sql:
                state["row"] = {"n": n}
                return
        answer(sql, params)
        state["row"] = None

    base_fetch = cur.fetchone.side_effect

    def fetchone():
        if state.get("row") is not None:
            row, state["row"] = state["row"], None
            return row
        return base_fetch()

    cur.execute.side_effect = execute
    cur.fetchone.side_effect = fetchone
    data = real_database.get_weekly_digest_data(conn=conn)
    loop = data["loop"]
    assert loop["signals"] == 3 and loop["plans"] == 1 and loop["entries"] == 1 and loop["reflections"] == 0
    assert loop["reviews"] is None  # table missing → null, not 0
    # The window comes from the same clock read as as_of_utc (no second now()).
    as_of = datetime.fromisoformat(data["as_of_utc"])
    assert loop["week_start"] == real_database.iso_week_start_utc(as_of).date().isoformat()
    assert conn.rollback.called
    # Signals count distinct (ticker, market) by signal_date (a date param).
    sig_sql, sig_params = next(x for x in seen if "FROM signals" in x[0])
    assert "COUNT(DISTINCT (ticker, market))" in sig_sql and "signal_date >= %s" in sig_sql
    assert type(sig_params[0]).__name__ == "date"
    # Naive TIMESTAMP columns get a naive UTC value, TIMESTAMPTZ an aware one.
    pos_params = next(x for x in seen if "FROM positions" in x[0])[1]
    plan_params = next(x for x in seen if "FROM trade_plans" in x[0])[1]
    assert pos_params[0].tzinfo is None
    assert plan_params[0].tzinfo is not None


def test_record_loop_event_rejects_unknown_type():
    with pytest.raises(ValueError):
        real_database.record_loop_event("page_view", conn=MagicMock())
