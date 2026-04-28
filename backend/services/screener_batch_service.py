"""
Screener Batch Service (DS-01 / ST-04)

Orchestrates screener runs: fetches regime, iterates ticker universe,
runs the computation engine, and persists results.

Run lifecycle: synchronous (runs in-process).
Idempotency: rejects new run while one is in progress.
"""
import json
import logging
import threading
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict

import requests

from database import get_db
from services.ticker_universe_service import get_all_tickers
from services.screener_data_service import fetch_ohlcv
from services.screener_engine import compute_screener_result

logger = logging.getLogger(__name__)

_YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
_YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

_run_lock = threading.Lock()
_run_in_progress = False


# ---------------------------------------------------------------------------
# Table bootstrap
# ---------------------------------------------------------------------------

def ensure_screener_results_table() -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS screener_runs (
                    run_id UUID PRIMARY KEY,
                    run_timestamp TIMESTAMP NOT NULL,
                    tickers_evaluated INTEGER DEFAULT 0,
                    tickers_passed INTEGER DEFAULT 0,
                    regime_us VARCHAR(10),
                    regime_uk VARCHAR(10)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_screener_runs_ts
                ON screener_runs (run_timestamp DESC)
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS screener_results (
                    id SERIAL PRIMARY KEY,
                    run_id UUID NOT NULL,
                    run_timestamp TIMESTAMP NOT NULL,
                    ticker VARCHAR(20) NOT NULL,
                    market VARCHAR(2) NOT NULL,
                    currency VARCHAR(3) NOT NULL,
                    price NUMERIC,
                    atr NUMERIC,
                    atr_pct NUMERIC,
                    atr_period INTEGER DEFAULT 14,
                    regime_status VARCHAR(10),
                    regime_index VARCHAR(10),
                    regime_index_price NUMERIC,
                    regime_index_ma200 NUMERIC,
                    signal_score NUMERIC,
                    signal_type VARCHAR(50),
                    sector VARCHAR(100),
                    industry VARCHAR(100),
                    proximity_to_entry_zone NUMERIC,
                    news_headline_count INTEGER DEFAULT 0,
                    news_headlines JSONB DEFAULT '[]'
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_screener_results_run_id
                ON screener_results (run_id)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_screener_results_run_ts
                ON screener_results (run_timestamp DESC)
            """)
        conn.commit()


# ---------------------------------------------------------------------------
# Regime helpers
# ---------------------------------------------------------------------------

def _fetch_index_regime(index_ticker: str) -> Optional[Dict]:
    """
    Fetch current price and 200-day MA for a market index via Yahoo Finance.
    Returns {regime_status, regime_index, regime_index_price, regime_index_ma200}
    or None on failure (defaults to risk_off to be conservative).
    """
    try:
        resp = requests.get(
            _YAHOO_URL.format(ticker=index_ticker),
            params={"interval": "1d", "range": "1y"},
            headers=_YAHOO_HEADERS,
            timeout=15,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        result = data["chart"]["result"][0]
        price = float(result["meta"]["regularMarketPrice"])
        closes = [c for c in result["indicators"]["quote"][0]["close"] if c is not None]
        ma200 = sum(closes[-200:]) / min(len(closes), 200) if closes else None
        if ma200 is None:
            return None
        regime_status = "risk_on" if price > ma200 else "risk_off"
        return {
            "regime_status": regime_status,
            "regime_index": index_ticker,
            "regime_index_price": price,
            "regime_index_ma200": ma200,
        }
    except Exception as exc:
        logger.warning("Regime fetch failed for %s: %s", index_ticker, exc)
        return None


# ---------------------------------------------------------------------------
# Result persistence
# ---------------------------------------------------------------------------

def _persist_run(run_id: str, run_timestamp: str, tickers_evaluated: int,
                 tickers_passed: int, regime_us: str, regime_uk: str) -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO screener_runs
                  (run_id, run_timestamp, tickers_evaluated, tickers_passed, regime_us, regime_uk)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (run_id) DO NOTHING
                """,
                (run_id, run_timestamp, tickers_evaluated, tickers_passed, regime_us, regime_uk),
            )
        conn.commit()


def _persist_results(results: List[Dict]) -> None:
    if not results:
        return
    with get_db() as conn:
        with conn.cursor() as cur:
            for r in results:
                cur.execute(
                    """
                    INSERT INTO screener_results
                      (run_id, run_timestamp, ticker, market, currency, price,
                       atr, atr_pct, atr_period,
                       regime_status, regime_index, regime_index_price, regime_index_ma200,
                       signal_score, signal_type, sector, industry,
                       proximity_to_entry_zone, news_headline_count, news_headlines)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        r["run_id"], r["run_timestamp"],
                        r["ticker"], r["market"], r["currency"], r["price"],
                        r["atr"],
                        r["atr"] / r["price"] if r["price"] else None,
                        r["atr_period"],
                        r["regime_status"], r["regime_index"],
                        r["regime_index_price"], r["regime_index_ma200"],
                        r["signal_score"], r.get("signal_type"),
                        r.get("sector"), r.get("industry"),
                        r.get("proximity_to_entry_zone"),
                        r.get("news_headline_count", 0),
                        json.dumps(r.get("news_headlines", [])),
                    ),
                )
        conn.commit()


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def run_screener(ticker_universe: Optional[List[str]] = None) -> Dict:
    """
    Execute a screener run.

    If ticker_universe is None, uses all active tickers from the DB.
    Returns {run_id, status, count, tickers_evaluated, tickers_passed}.
    Raises RuntimeError if a run is already in progress.
    """
    global _run_in_progress
    with _run_lock:
        if _run_in_progress:
            raise RuntimeError("RUN_IN_PROGRESS")
        _run_in_progress = True

    try:
        run_id = str(uuid.uuid4())
        run_timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Resolve ticker list
        if ticker_universe is None:
            rows = get_all_tickers(active_only=True)
            ticker_universe = [r["ticker"] for r in rows]

        # Fetch regime data (once per market)
        us_regime = _fetch_index_regime("SPY")
        uk_regime = _fetch_index_regime("^FTSE")

        if us_regime is None:
            us_regime = {"regime_status": "risk_off", "regime_index": "SPY",
                         "regime_index_price": 0.0, "regime_index_ma200": 0.0}
        if uk_regime is None:
            uk_regime = {"regime_status": "risk_off", "regime_index": "^FTSE",
                         "regime_index_price": 0.0, "regime_index_ma200": 0.0}

        results = []
        tickers_evaluated = 0

        for ticker in ticker_universe:
            market = "UK" if ticker.upper().endswith(".L") else "US"
            regime = uk_regime if market == "UK" else us_regime

            ohlcv = fetch_ohlcv(ticker, market, days=30)
            if not ohlcv:
                continue

            tickers_evaluated += 1
            record = compute_screener_result(
                ticker=ticker,
                market=market,
                ohlcv_data=ohlcv,
                run_id=run_id,
                run_timestamp=run_timestamp,
                **regime,
            )
            if record is not None:
                results.append(record)

        regime_us_status = us_regime.get("regime_status", "risk_off")
        regime_uk_status = uk_regime.get("regime_status", "risk_off")
        _persist_run(run_id, run_timestamp, tickers_evaluated, len(results),
                     regime_us_status, regime_uk_status)
        _persist_results(results)

        return {
            "run_id": run_id,
            "status": "completed",
            "count": len(results),
            "tickers_evaluated": tickers_evaluated,
            "tickers_passed": len(results),
            "regime_us": regime_us_status,
            "regime_uk": regime_uk_status,
        }
    finally:
        with _run_lock:
            _run_in_progress = False


def get_screener_results(
    market: Optional[str] = None,
    run_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Dict:
    """
    Fetch screener results for the latest run (or a specific run_id).
    Returns {results, run_id, run_timestamp, total, limit, offset}.
    Raises ValueError if no runs have been completed yet.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            if run_id is None:
                cur.execute(
                    "SELECT run_id, run_timestamp, tickers_evaluated, tickers_passed, regime_us, regime_uk "
                    "FROM screener_runs ORDER BY run_timestamp DESC LIMIT 1"
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError("NO_RESULTS")
                run_id = str(row["run_id"])
                run_ts = row["run_timestamp"]
                run_meta = dict(row)
            else:
                cur.execute(
                    "SELECT run_id, run_timestamp, tickers_evaluated, tickers_passed, regime_us, regime_uk "
                    "FROM screener_runs WHERE run_id = %s LIMIT 1",
                    (run_id,),
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError("NO_RESULTS")
                run_ts = row["run_timestamp"]
                run_meta = dict(row)

            filters = ["run_id = %s"]
            params = [run_id]
            if market and market != "all":
                filters.append("market = %s")
                params.append(market)

            where = "WHERE " + " AND ".join(filters)

            cur.execute(f"SELECT COUNT(*) AS cnt FROM screener_results {where}", params)
            total = cur.fetchone()["cnt"]

            cur.execute(
                f"""
                SELECT ticker, market, currency, price, atr, atr_pct, atr_period,
                       regime_status, regime_index, regime_index_price, regime_index_ma200,
                       signal_score, signal_type, sector, industry,
                       proximity_to_entry_zone, news_headline_count, news_headlines,
                       run_id::text AS run_id, run_timestamp
                FROM screener_results {where}
                ORDER BY signal_score DESC
                LIMIT %s OFFSET %s
                """,
                params + [limit, offset],
            )
            rows = cur.fetchall()

    results = []
    for r in rows:
        rec = dict(r)
        if isinstance(rec.get("news_headlines"), str):
            rec["news_headlines"] = json.loads(rec["news_headlines"])
        if rec.get("run_timestamp"):
            rec["run_timestamp"] = rec["run_timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ")
        results.append(rec)

    run_ts_str = run_ts.strftime("%Y-%m-%dT%H:%M:%SZ") if hasattr(run_ts, "strftime") else str(run_ts)

    return {
        "results": results,
        "run_id": run_id,
        "run_timestamp": run_ts_str,
        "total": total,
        "limit": limit,
        "offset": offset,
        "tickers_evaluated": run_meta.get("tickers_evaluated", 0),
        "tickers_passed": run_meta.get("tickers_passed", 0),
        "regime_us": run_meta.get("regime_us"),
        "regime_uk": run_meta.get("regime_uk"),
    }
