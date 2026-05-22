"""
Ticker Universe Service (DS-01 / ST-01)

Manages the set of tickers eligible for screener runs.
Supports UK (.L suffix) and US tickers.
"""
from typing import List, Optional
from database import get_db


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
                f"SELECT ticker, market, active, sector, industry, created_at FROM ticker_universe {where} ORDER BY market, ticker",
                params,
            )
            return [dict(r) for r in cur.fetchall()]


def add_ticker(ticker: str, market: str, sector: Optional[str] = None, industry: Optional[str] = None) -> dict:
    if not ticker or not ticker.strip():
        raise ValueError("ticker must not be empty")
    if market not in VALID_MARKETS:
        raise ValueError(f"market must be one of: {', '.join(sorted(VALID_MARKETS))}")
    ticker = ticker.strip().upper()
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ticker_universe (ticker, market, active, sector, industry)
                VALUES (%s, %s, TRUE, %s, %s)
                ON CONFLICT (ticker) DO UPDATE
                    SET active = TRUE, market = EXCLUDED.market,
                        sector = EXCLUDED.sector, industry = EXCLUDED.industry
                RETURNING ticker, market, active, sector, industry, created_at
                """,
                (ticker, market, sector, industry),
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
                cur.execute(
                    """
                    INSERT INTO ticker_universe (ticker, market, active)
                    VALUES (%s, %s, TRUE)
                    ON CONFLICT (ticker) DO UPDATE SET active = TRUE, market = EXCLUDED.market
                    """,
                    (ticker, market),
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
