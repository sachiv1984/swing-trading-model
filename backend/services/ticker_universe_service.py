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
