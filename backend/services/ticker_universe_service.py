"""
Ticker Universe Service (DS-01 / ST-01)

Manages the set of tickers eligible for screener runs.
Supports UK (.L suffix) and US tickers.
"""
import csv
import logging
import os
from typing import Dict, List, Optional
from database import get_db

_log = logging.getLogger(__name__)


def _yfinance_company_name(ticker: str) -> Optional[str]:
    """Return company name from yfinance, or None on failure."""
    try:
        import yfinance as yf
        info = yf.Ticker(ticker).info
        return info.get("longName") or info.get("shortName") or None
    except Exception:
        return None


def backfill_company_names() -> int:
    """Fetch company names from yfinance for any ticker_universe rows where company_name IS NULL.

    Called at startup to recover tickers added before the yfinance lookup was wired in.
    Returns the number of rows updated.
    """
    updated = 0
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT ticker, market FROM ticker_universe WHERE company_name IS NULL AND active = TRUE")
                rows = cur.fetchall()
        for row in rows:
            name = _yfinance_company_name(row["ticker"])
            if name:
                with get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "UPDATE ticker_universe SET company_name = %s WHERE ticker = %s AND company_name IS NULL",
                            (name, row["ticker"]),
                        )
                        if cur.rowcount:
                            updated += 1
                    conn.commit()
    except Exception as exc:
        _log.warning("backfill_company_names failed: %s", exc)
    return updated

_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "tickers_full_list.csv")


def _load_company_names() -> Dict[str, str]:
    """Return {ticker: company_name} from tickers_full_list.csv."""
    mapping: Dict[str, str] = {}
    try:
        with open(_CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                ticker = (row.get("Ticker") or "").strip().upper()
                name = (row.get("Name") or "").strip()
                if ticker and name:
                    mapping[ticker] = name
    except FileNotFoundError:
        pass
    return mapping


def _load_csv_tickers() -> set:
    """Return the set of tickers in tickers_full_list.csv — the pre-DB
    tracked universe, in place long before ticker_universe existed."""
    tickers = set()
    try:
        with open(_CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                t = (row.get("Ticker") or "").strip().upper()
                if t:
                    tickers.add(t)
    except FileNotFoundError:
        pass
    return tickers


# BLG-BE-59 fallout: the one-time migration that first populated
# ticker_universe (sync_from_tickers_table(), run 2026-04-27/28) stamped
# every row's created_at with the insertion timestamp, not the date each
# ticker was actually added to the tracked universe. compute_signals()'s
# eligibility gate (production_strategy.py, added 2026-07-14) reads
# created_at as "date this ticker became eligible" and masks all signal
# history before it — so 599 legacy tickers (already in
# tickers_full_list.csv pre-migration) lost virtually their entire
# 2018-2026 backtest history. This sentinel predates the backtest's own
# price-download start date (2018-01-01), so tickers stamped with it are
# always-eligible, matching pre-migration behaviour.
LEGACY_TICKER_CREATED_AT_SENTINEL = "2018-01-01 00:00:00"


def backfill_legacy_ticker_created_at() -> int:
    """Reset created_at to the legacy sentinel for every ticker_universe row
    whose ticker also appears in tickers_full_list.csv (i.e. predates the DB
    table). Idempotent — only touches rows still later than the sentinel, so
    re-running after the first successful pass is a no-op. Returns the
    number of rows updated.
    """
    legacy_tickers = _load_csv_tickers()
    if not legacy_tickers:
        return 0
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE ticker_universe
                SET created_at = %s
                WHERE ticker = ANY(%s) AND created_at > %s
                """,
                (LEGACY_TICKER_CREATED_AT_SENTINEL, list(legacy_tickers), LEGACY_TICKER_CREATED_AT_SENTINEL),
            )
            updated = cur.rowcount
        conn.commit()
    return updated


VALID_MARKETS = {"UK", "US"}

DEFAULT_TICKERS = [
    # US tickers
    {"ticker": "AAPL", "market": "US", "sector": "Technology", "industry": "Consumer Electronics"},
    {"ticker": "MSFT", "market": "US", "sector": "Technology", "industry": "Software"},
    {"ticker": "NVDA", "market": "US", "sector": "Technology", "industry": "Semiconductors"},
    {"ticker": "AMZN", "market": "US", "sector": "Consumer Discretionary", "industry": "Internet Retail"},
    {"ticker": "GOOGL", "market": "US", "sector": "Communication Services", "industry": "Internet Content"},
    # UK tickers
    {"ticker": "HSBA.L", "market": "UK", "sector": "Financials", "industry": "Banks"},
    {"ticker": "BP.L", "market": "UK", "sector": "Energy", "industry": "Oil & Gas"},
    {"ticker": "SHEL.L", "market": "UK", "sector": "Energy", "industry": "Oil & Gas"},
    {"ticker": "AZN.L", "market": "UK", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    {"ticker": "ULVR.L", "market": "UK", "sector": "Consumer Staples", "industry": "Household Products"},
]


def ensure_ticker_universe_table() -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ticker_universe (
                    ticker VARCHAR(20) PRIMARY KEY,
                    market VARCHAR(2) NOT NULL CHECK (market IN ('UK', 'US')),
                    active BOOLEAN NOT NULL DEFAULT TRUE,
                    sector VARCHAR(100),
                    industry VARCHAR(100),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_ticker_universe_market
                ON ticker_universe (market)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_ticker_universe_active
                ON ticker_universe (active)
            """)
        conn.commit()


def ensure_company_name_column() -> None:
    """Add company_name TEXT column to ticker_universe and backfill from CSV."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                ALTER TABLE ticker_universe
                ADD COLUMN IF NOT EXISTS company_name TEXT
            """)
        conn.commit()
    names = _load_company_names()
    if not names:
        return
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ticker FROM ticker_universe WHERE company_name IS NULL")
            rows = cur.fetchall()
        with conn.cursor() as cur:
            for row in rows:
                ticker = row["ticker"]
                company_name = names.get(ticker)
                if company_name:
                    cur.execute(
                        "UPDATE ticker_universe SET company_name = %s WHERE ticker = %s",
                        (company_name, ticker),
                    )
        conn.commit()


def get_all_tickers(market: Optional[str] = None, active_only: bool = True) -> List[dict]:
    filters = []
    params = []
    if active_only:
        filters.append("active = TRUE")
    if market is not None:
        filters.append("market = %s")
        params.append(market)
    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT ticker, market, active, sector, industry, company_name, created_at FROM ticker_universe {where} ORDER BY market, ticker",
                params,
            )
            return [dict(r) for r in cur.fetchall()]


def add_ticker(ticker: str, market: str, sector: Optional[str] = None, industry: Optional[str] = None) -> dict:
    if not ticker or not ticker.strip():
        raise ValueError("ticker must not be empty")
    if market not in VALID_MARKETS:
        raise ValueError(f"market must be one of: {', '.join(sorted(VALID_MARKETS))}")
    ticker = ticker.strip().upper()
    company_name = _load_company_names().get(ticker) or _yfinance_company_name(ticker)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ticker_universe (ticker, market, active, sector, industry, company_name)
                VALUES (%s, %s, TRUE, %s, %s, %s)
                ON CONFLICT (ticker) DO UPDATE
                    SET active = TRUE, market = EXCLUDED.market,
                        sector = EXCLUDED.sector, industry = EXCLUDED.industry,
                        company_name = COALESCE(EXCLUDED.company_name, ticker_universe.company_name)
                RETURNING ticker, market, active, sector, industry, company_name, created_at
                """,
                (ticker, market, sector, industry, company_name),
            )
            row = cur.fetchone()
        conn.commit()
    return dict(row)


def soft_delete_ticker(ticker: str) -> bool:
    ticker = ticker.strip().upper()
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE ticker_universe SET active = FALSE WHERE ticker = %s AND active = TRUE",
                (ticker,),
            )
            affected = cur.rowcount
        conn.commit()
    return affected > 0


def sync_from_tickers_table() -> int:
    """
    Upsert all rows from public.tickers into ticker_universe.
    exchange='LSE' → market='UK' (ticker gets .L suffix if missing).
    All other exchanges → market='US'.
    Returns count of rows inserted/updated.
    """
    names = _load_company_names()
    legacy_tickers = _load_csv_tickers()
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT ticker, exchange FROM tickers")
            rows = cur.fetchall()

        count = 0
        with conn.cursor() as cur:
            for row in rows:
                raw_ticker = row["ticker"].strip().upper()
                exchange = (row["exchange"] or "").strip().upper()
                if exchange == "LSE":
                    market = "UK"
                    ticker = raw_ticker if raw_ticker.endswith(".L") else raw_ticker + ".L"
                else:
                    market = "US"
                    ticker = raw_ticker
                company_name = names.get(ticker)
                if ticker in legacy_tickers:
                    # Already part of the pre-DB tracked universe (BLG-BE-59
                    # fallout) — stamp with the legacy sentinel, not NOW(),
                    # so a (re-)sync never re-triggers the created_at gate
                    # bug for tickers that aren't actually new.
                    cur.execute(
                        """
                        INSERT INTO ticker_universe (ticker, market, active, company_name, created_at)
                        VALUES (%s, %s, TRUE, %s, %s)
                        ON CONFLICT (ticker) DO UPDATE SET active = TRUE, market = EXCLUDED.market,
                            company_name = COALESCE(EXCLUDED.company_name, ticker_universe.company_name)
                        """,
                        (ticker, market, company_name, LEGACY_TICKER_CREATED_AT_SENTINEL),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO ticker_universe (ticker, market, active, company_name)
                        VALUES (%s, %s, TRUE, %s)
                        ON CONFLICT (ticker) DO UPDATE SET active = TRUE, market = EXCLUDED.market,
                            company_name = COALESCE(EXCLUDED.company_name, ticker_universe.company_name)
                        """,
                        (ticker, market, company_name),
                    )
                count += cur.rowcount
        conn.commit()
    return count


INVALID_TICKERS = ["DAY"]


def deactivate_invalid_tickers() -> int:
    """Deactivate known-invalid tickers (e.g. DAY consistently returns 404 on YF)."""
    count = 0
    for ticker in INVALID_TICKERS:
        count += 1 if soft_delete_ticker(ticker) else 0
    return count


def seed_default_tickers() -> int:
    count = 0
    for t in DEFAULT_TICKERS:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO ticker_universe (ticker, market, active, sector, industry)
                    VALUES (%s, %s, TRUE, %s, %s)
                    ON CONFLICT (ticker) DO NOTHING
                    """,
                    (t["ticker"], t["market"], t.get("sector"), t.get("industry")),
                )
                count += cur.rowcount
            conn.commit()
    return count
