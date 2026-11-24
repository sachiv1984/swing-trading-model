"""
ST-35 / BLG-BE-234 (EPIC-06, v9.18): a UK watchlist row finds its signal.

The watchlist stores UK tickers bare (`LGEN`); signal_service writes signals
with the Yahoo symbol (`LGEN.L`). get_watchlist()'s signal lookup matched the
exact ticker only, so once the staging seed wrote `LGEN.L` signals (ST-35) the
UK watchlist rows showed `no_signal`. This runs the real query against real
Postgres, with minimal tables holding only the columns it reads.

Phase B only: skipped when DATABASE_URL is a stub or unreachable. Uses its own
schema, dropped afterwards.
"""
import os
import sys
import types
import uuid
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

psycopg2 = pytest.importorskip("psycopg2")
from psycopg2.extras import RealDictCursor  # noqa: E402

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))
DB_URL = os.environ.get("DATABASE_URL", "")
PORTFOLIO = "11111111-1111-1111-1111-111111111111"


def _connect():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor, connect_timeout=3)


def _db_available():
    if not DB_URL or "stub" in DB_URL:
        return False
    try:
        _connect().close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _db_available(), reason="needs a reachable Postgres (CI Phase B)")

# A private copy of watchlist_service.py; its `database` import is a stub
# scoped to the load, so sys.modules["database"] is never replaced.
from tests._scoped_utils_stubs import scoped_stub_modules  # noqa: E402
import importlib.util as _ilu  # noqa: E402

_db_stub = types.ModuleType("database")
_db_stub.get_db = MagicMock()
_db_stub.get_portfolio = MagicMock()
_spec = _ilu.spec_from_file_location("watchlist_service_st35_it", ROOT / "backend" / "services" / "watchlist_service.py")
watchlist_service = _ilu.module_from_spec(_spec)
with scoped_stub_modules({"database": _db_stub}):
    _spec.loader.exec_module(watchlist_service)


@pytest.fixture
def schema(monkeypatch):
    name = f"st35_{uuid.uuid4().hex[:8]}"
    admin = _connect()
    admin.autocommit = True
    with admin.cursor() as cur:
        cur.execute(f"CREATE SCHEMA {name}")
        cur.execute(f"SET search_path TO {name}")
        cur.execute("""
            CREATE TABLE watchlist (
                id SERIAL PRIMARY KEY, portfolio_id UUID, ticker TEXT, market TEXT,
                target_entry_price NUMERIC, initial_stop_price NUMERIC, current_stop_price NUMERIC,
                tags TEXT[], notes TEXT, created_at TIMESTAMP, updated_at TIMESTAMP);
            CREATE TABLE ticker_universe (ticker TEXT PRIMARY KEY, company_name TEXT);
            CREATE TABLE signals (portfolio_id UUID, ticker TEXT, market TEXT, signal_date DATE, status TEXT);
        """)

    @contextmanager
    def get_db():
        c = _connect()
        try:
            with c.cursor() as cur:
                cur.execute(f"SET search_path TO {name}")
            yield c
            c.commit()
        finally:
            c.close()

    monkeypatch.setattr(watchlist_service, "get_db", get_db)
    yield admin
    with admin.cursor() as cur:
        cur.execute(f"DROP SCHEMA {name} CASCADE")
    admin.close()


def _seed(admin, watch, signals):
    with admin.cursor() as cur:
        for ticker, market in watch:
            cur.execute(
                "INSERT INTO watchlist (portfolio_id, ticker, market, target_entry_price, initial_stop_price,"
                " current_stop_price, created_at, updated_at) VALUES (%s,%s,%s,2.45,2.15,2.20,%s,%s)",
                (PORTFOLIO, ticker, market, datetime(2026, 11, 1), datetime(2026, 11, 1)))
        for ticker, market, status in signals:
            cur.execute("INSERT INTO signals VALUES (%s,%s,%s,%s,%s)",
                        (PORTFOLIO, ticker, market, date(2026, 4, 10), status))
        cur.execute("INSERT INTO ticker_universe VALUES ('LGEN.L', 'Legal & General'), ('AAPL', 'Apple')")


def _status(rows):
    return {r["ticker"]: r["signal_status"] for r in rows}


def test_uk_row_matches_a_dot_l_signal(schema):
    _seed(schema, [("LGEN", "UK"), ("AAPL", "US")],
          [("LGEN.L", "UK", "new"), ("AAPL", "US", "dismissed")])
    rows = watchlist_service.get_watchlist(PORTFOLIO)
    assert _status(rows) == {"LGEN": "active", "AAPL": "watch"}
    assert {r["ticker"]: r.get("company_name") for r in rows}["LGEN"] == "Legal & General"


def test_uk_row_still_matches_a_legacy_bare_signal(schema):
    _seed(schema, [("BARC", "UK")], [("BARC", "UK", "new")])
    assert _status(watchlist_service.get_watchlist(PORTFOLIO)) == {"BARC": "active"}


def test_us_row_does_not_match_a_dot_l_signal(schema):
    """A US ticker is never mapped to a .L symbol."""
    _seed(schema, [("BP", "US")], [("BP.L", "UK", "new")])
    assert _status(watchlist_service.get_watchlist(PORTFOLIO)) == {"BP": "no_signal"}
