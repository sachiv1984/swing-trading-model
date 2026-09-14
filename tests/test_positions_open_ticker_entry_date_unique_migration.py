"""
Synthetic/staging-shaped verification for DS-17 (ST-01, EPIC-01, v9.4, BLG-BE-115)
— DB-level unique constraint on (portfolio_id, ticker, entry_date) for open
positions.

RISK-01: no DATABASE_URL / live Postgres is available in this execution
environment (tests/conftest.py only provides a dummy DATABASE_URL to satisfy
import-time checks — it is not a live connection). This file therefore
verifies the constraint's *logic* against a minimal, positions-shaped SQLite
table rather than against production or staging Postgres directly.

SQLite supports partial unique indexes (`CREATE UNIQUE INDEX ... WHERE ...`)
with the same semantics relevant here (only rows matching the WHERE
predicate participate in the uniqueness check), so this is a faithful proxy
for the real migration's mechanism — not merely a restatement of it. It is
explicitly NOT a run of the actual DS-17 PL/pgSQL migration against
production-shaped Postgres data; that live step remains disclosed as
pending per RISK-01 and ST-01's staging-only AC-03 until a session with
DATABASE_URL access can perform it.
"""
import sqlite3

import pytest


def _fresh_db():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id TEXT NOT NULL,
            ticker TEXT NOT NULL,
            entry_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('open', 'closed'))
        )
        """
    )
    return conn


def _duplicate_open_groups(conn):
    """Mirrors the DS-17 migration's pre-check query (RISK-01): groups of
    (portfolio_id, ticker, entry_date) among OPEN positions with >1 row."""
    cur = conn.execute(
        """
        SELECT portfolio_id, ticker, entry_date, COUNT(*) AS cnt
        FROM positions
        WHERE status = 'open'
        GROUP BY portfolio_id, ticker, entry_date
        HAVING COUNT(*) > 1
        """
    )
    return cur.fetchall()


def _create_unique_index(conn):
    conn.execute(
        """
        CREATE UNIQUE INDEX idx_positions_open_ticker_entry_date_unique
        ON positions (portfolio_id, ticker, entry_date)
        WHERE status = 'open'
        """
    )


class TestPreCheckDetectsExistingDuplicates:
    def test_flags_duplicate_open_positions_same_portfolio(self):
        conn = _fresh_db()
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'open')"
        )
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'open')"
        )
        dups = _duplicate_open_groups(conn)
        assert dups == [("p1", "AAPL", "2026-09-01", 2)]

    def test_no_false_positive_when_no_duplicates(self):
        conn = _fresh_db()
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'open')"
        )
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'MSFT', '2026-09-01', 'open')"
        )
        assert _duplicate_open_groups(conn) == []


class TestUniqueIndexEnforcement:
    def test_rejects_duplicate_open_position_after_index_created(self):
        conn = _fresh_db()
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'open')"
        )
        _create_unique_index(conn)

        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
                "('p1', 'AAPL', '2026-09-01', 'open')"
            )

    def test_allows_closed_duplicate_of_an_open_position(self):
        """Partial index only covers status='open' — a closed position with
        the same (portfolio_id, ticker, entry_date) as an open one (e.g. a
        prior closed trade re-entered on the same date) must not be blocked."""
        conn = _fresh_db()
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'open')"
        )
        _create_unique_index(conn)

        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'closed')"
        )  # must not raise
        rows = conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
        assert rows == 2

    def test_allows_same_ticker_entry_date_across_different_portfolios(self):
        """Head of Engineering decision (DS-17, ST-01/v9.4): the index is
        scoped per-portfolio, not globally, since the schema supports
        multiple portfolios and a global scope would incorrectly reject a
        second, independent portfolio's legitimate position."""
        conn = _fresh_db()
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'open')"
        )
        _create_unique_index(conn)

        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p2', 'AAPL', '2026-09-01', 'open')"
        )  # must not raise — different portfolio
        rows = conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
        assert rows == 2

    def test_index_creation_itself_fails_over_existing_duplicates(self):
        """Sanity check on migration ordering: if the pre-check were skipped
        and duplicates already exist, index creation itself also fails —
        defense in depth alongside the explicit pre-check's clearer error
        report."""
        conn = _fresh_db()
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'open')"
        )
        conn.execute(
            "INSERT INTO positions (portfolio_id, ticker, entry_date, status) VALUES "
            "('p1', 'AAPL', '2026-09-01', 'open')"
        )
        with pytest.raises(sqlite3.IntegrityError):
            _create_unique_index(conn)
