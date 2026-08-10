"""
Screener Batch Service (DS-01 / ST-04)

Orchestrates screener runs: fetches regime, iterates ticker universe,
runs the computation engine, and persists results.

Run lifecycle: synchronous (runs in-process).
Idempotency: rejects new run while one is in progress.
"""
import json
import logging
import os
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import List, Optional, Dict

import requests

from database import get_db
from services.ticker_universe_service import get_all_tickers
from services.screener_data_service import fetch_ohlcv
from services.screener_engine import compute_screener_result
from utils.retry import retry_with_backoff

YF_MAX_CONCURRENT = int(os.environ.get("YF_MAX_CONCURRENT", "5"))

logger = logging.getLogger(__name__)

_YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
_YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
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
                    regime_uk VARCHAR(10),
                    degraded_run BOOLEAN NOT NULL DEFAULT FALSE,
                    failure_rate NUMERIC
                )
            """)
            # Add columns to existing tables that may predate this schema
            cur.execute("""
                ALTER TABLE screener_runs
                    ADD COLUMN IF NOT EXISTS degraded_run BOOLEAN NOT NULL DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS failure_rate NUMERIC,
                    ADD COLUMN IF NOT EXISTS tickers_requested INTEGER DEFAULT 0,
                    ADD COLUMN IF NOT EXISTS failed_tickers JSONB DEFAULT '[]'
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

@retry_with_backoff(
    max_attempts=3,
    base_delay=0.5,
    retryable_exceptions=(requests.exceptions.RequestException,),
)
def _fetch_index_regime_raw(index_ticker: str) -> Dict:
    """
    Fetch current price and 200-day MA for a market index via Yahoo Finance (internal).
    Raises on any transient/network failure (retried by the decorator, ST-09) or a
    `ValueError` when the response is well-formed but carries no usable MA200 data
    (not retried — retrying won't produce data that isn't there).
    """
    resp = requests.get(
        _YAHOO_URL.format(ticker=index_ticker),
        params={"interval": "1d", "range": "1y"},
        headers=_YAHOO_HEADERS,
        timeout=15,
    )
    if resp.status_code != 200:
        raise ValueError(f"Yahoo Finance returned HTTP {resp.status_code} for {index_ticker}")
    data = resp.json()
    result = data["chart"]["result"][0]
    price = float(result["meta"]["regularMarketPrice"])
    closes = [c for c in result["indicators"]["quote"][0]["close"] if c is not None]
    ma200 = sum(closes[-200:]) / min(len(closes), 200) if closes else None
    if ma200 is None:
        raise ValueError(f"No MA200 data available for {index_ticker}")
    regime_status = "risk_on" if price > ma200 else "risk_off"
    return {
        "regime_status": regime_status,
        "regime_index": index_ticker,
        "regime_index_price": price,
        "regime_index_ma200": ma200,
    }


def _fetch_index_regime(index_ticker: str) -> Optional[Dict]:
    """
    Fetch current price and 200-day MA for a market index via Yahoo Finance,
    retrying transient failures (ST-09, ~3 attempts).
    Returns {regime_status, regime_index, regime_index_price, regime_index_ma200}
    or None on failure (defaults to risk_off to be conservative).
    """
    try:
        return _fetch_index_regime_raw(index_ticker)
    except Exception as exc:
        logger.warning("Regime fetch failed for %s: %s", index_ticker, exc)
        return None


# ---------------------------------------------------------------------------
# Result persistence
# ---------------------------------------------------------------------------

def _persist_run(run_id: str, run_timestamp: str, tickers_evaluated: int,
                 tickers_passed: int, regime_us: str, regime_uk: str,
                 degraded_run: bool = False, failure_rate: Optional[float] = None,
                 tickers_requested: int = 0,
                 failed_tickers: Optional[List[str]] = None) -> None:
    import json as _json
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO screener_runs
                  (run_id, run_timestamp, tickers_evaluated, tickers_passed,
                   regime_us, regime_uk, degraded_run, failure_rate,
                   tickers_requested, failed_tickers)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (run_id) DO NOTHING
                """,
                (run_id, run_timestamp, tickers_evaluated, tickers_passed,
                 regime_us, regime_uk, degraded_run, failure_rate,
                 tickers_requested, _json.dumps(failed_tickers or [])),
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

def run_screener(ticker_universe: Optional[List[str]] = None,
                 run_id: Optional[str] = None) -> Dict:
    """
    Execute a screener run.

    If ticker_universe is None, uses all active tickers from the DB.
    If run_id is provided, uses it (allows callers to pre-generate and return the ID before execution).
    Returns {run_id, status, count, tickers_evaluated, tickers_passed, degraded_run, failure_rate}.
    Raises RuntimeError if a run is already in progress.
    """
    global _run_in_progress
    with _run_lock:
        if _run_in_progress:
            raise RuntimeError("RUN_IN_PROGRESS")
        _run_in_progress = True

    try:
        if run_id is None:
            run_id = str(uuid.uuid4())
        run_timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Resolve ticker list — keep full row dicts to preserve sector/industry
        if ticker_universe is None:
            ticker_rows = get_all_tickers(active_only=True)
        else:
            ticker_rows = [{"ticker": t, "market": "UK" if t.upper().endswith(".L") else "US",
                            "sector": None, "industry": None}
                           for t in ticker_universe]

        total_tickers = len(ticker_rows)

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
        ohlcv_failures = 0
        failed_ticker_list: List[str] = []

        def _process_row_tracked(row: Dict) -> tuple:
            """Returns (result_or_None, had_ohlcv)."""
            ticker = row["ticker"]
            market = row.get("market") or ("UK" if ticker.upper().endswith(".L") else "US")
            sector = row.get("sector")
            industry = row.get("industry")
            regime = uk_regime if market == "UK" else us_regime
            ohlcv = fetch_ohlcv(ticker, market, days=30)
            if not ohlcv:
                return None, False, ticker
            record = compute_screener_result(
                ticker=ticker,
                market=market,
                ohlcv_data=ohlcv,
                run_id=run_id,
                run_timestamp=run_timestamp,
                sector=sector,
                industry=industry,
                **regime,
            )
            return record, True, ticker

        # Split UK and US so we can use different fetch strategies.
        # UK: sequential with inter-request delay — Yahoo Finance rate-limits hard
        #     under concurrent load; 0.3s spacing keeps it under the threshold.
        # US: concurrent thread pool — Alpaca handles concurrency fine.
        def _is_uk(row: Dict) -> bool:
            m = row.get("market") or ("UK" if row["ticker"].upper().endswith(".L") else "US")
            return m == "UK"

        uk_rows = [r for r in ticker_rows if _is_uk(r)]
        us_rows = [r for r in ticker_rows if not _is_uk(r)]

        for row in uk_rows:
            time.sleep(0.3)
            try:
                record, had_ohlcv, ticker = _process_row_tracked(row)
                if not had_ohlcv:
                    ohlcv_failures += 1
                    failed_ticker_list.append(ticker)
                else:
                    tickers_evaluated += 1
                    if record is not None:
                        results.append(record)
            except Exception as exc:
                logger.warning("Screener batch error for %s: %s", row.get("ticker"), exc)
                ohlcv_failures += 1
                failed_ticker_list.append(row.get("ticker", "unknown"))

        with ThreadPoolExecutor(max_workers=YF_MAX_CONCURRENT) as executor:
            futures = {executor.submit(_process_row_tracked, row): row for row in us_rows}
            for future in as_completed(futures):
                row = futures[future]
                try:
                    record, had_ohlcv, ticker = future.result()
                    if not had_ohlcv:
                        ohlcv_failures += 1
                        failed_ticker_list.append(ticker)
                    else:
                        tickers_evaluated += 1
                        if record is not None:
                            results.append(record)
                except Exception as exc:
                    logger.warning("Screener batch error for %s: %s", row.get("ticker"), exc)
                    ohlcv_failures += 1
                    failed_ticker_list.append(row.get("ticker", "unknown"))

        failure_rate = ohlcv_failures / total_tickers if total_tickers > 0 else 0.0
        degraded_run = failure_rate > 0.20

        regime_us_status = us_regime.get("regime_status", "risk_off")
        regime_uk_status = uk_regime.get("regime_status", "risk_off")
        _persist_run(run_id, run_timestamp, tickers_evaluated, len(results),
                     regime_us_status, regime_uk_status, degraded_run, failure_rate,
                     tickers_requested=total_tickers,
                     failed_tickers=failed_ticker_list)
        _persist_results(results)

        return {
            "run_id": run_id,
            "status": "completed",
            "count": len(results),
            "tickers_evaluated": tickers_evaluated,
            "tickers_passed": len(results),
            "regime_us": regime_us_status,
            "regime_uk": regime_uk_status,
            "degraded_run": degraded_run,
            "failure_rate": failure_rate,
            "tickers_requested": total_tickers,
            "tickers_loaded": tickers_evaluated,
            "tickers_failed": failed_ticker_list,
        }
    finally:
        with _run_lock:
            _run_in_progress = False


def is_run_in_progress() -> bool:
    with _run_lock:
        return _run_in_progress


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
            _run_cols = ("run_id, run_timestamp, tickers_evaluated, tickers_passed, "
                         "regime_us, regime_uk, degraded_run, failure_rate, "
                         "tickers_requested, failed_tickers")
            if run_id is None:
                cur.execute(
                    f"SELECT {_run_cols} FROM screener_runs ORDER BY run_timestamp DESC LIMIT 1"
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError("NO_RESULTS")
                run_id = str(row["run_id"])
                run_ts = row["run_timestamp"]
                run_meta = dict(row)
            else:
                cur.execute(
                    f"SELECT {_run_cols} FROM screener_runs WHERE run_id = %s LIMIT 1",
                    (run_id,),
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError("NO_RESULTS")
                run_ts = row["run_timestamp"]
                run_meta = dict(row)

            # last_full_run_utc — most recent run with degraded_run = false
            cur.execute(
                "SELECT run_timestamp FROM screener_runs WHERE degraded_run = false "
                "ORDER BY run_timestamp DESC LIMIT 1"
            )
            lfr_row = cur.fetchone()
            last_full_run_ts = lfr_row["run_timestamp"] if lfr_row else None

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

    failure_rate_val = run_meta.get("failure_rate")
    failure_rate_f = float(failure_rate_val) if failure_rate_val is not None else 0.0
    tickers_req = run_meta.get("tickers_requested") or 0
    tickers_loaded = run_meta.get("tickers_evaluated") or 0

    # Derive run_quality
    if tickers_req == 0 or tickers_loaded == 0:
        run_quality = "FAILED"
    elif run_meta.get("degraded_run"):
        run_quality = "DEGRADED"
    else:
        run_quality = "FULL"

    # Deserialise failed_tickers from JSONB (may arrive as str, list, or None)
    import json as _json
    raw_failed = run_meta.get("failed_tickers")
    if isinstance(raw_failed, str):
        try:
            failed_tickers_list = _json.loads(raw_failed)
        except Exception:
            failed_tickers_list = []
    elif isinstance(raw_failed, list):
        failed_tickers_list = raw_failed
    else:
        failed_tickers_list = []

    last_full_run_utc = (
        last_full_run_ts.strftime("%Y-%m-%dT%H:%M:%SZ")
        if hasattr(last_full_run_ts, "strftime") else (str(last_full_run_ts) if last_full_run_ts else None)
    )

    return {
        "results": results,
        "run_id": run_id,
        "run_timestamp": run_ts_str,
        "total": total,
        "limit": limit,
        "offset": offset,
        "tickers_evaluated": tickers_loaded,
        "tickers_passed": run_meta.get("tickers_passed", 0),
        "regime_us": run_meta.get("regime_us"),
        "regime_uk": run_meta.get("regime_uk"),
        "degraded_run": bool(run_meta.get("degraded_run", False)),
        "failure_rate": failure_rate_f,
        "tickers_requested": tickers_req,
        "tickers_loaded": tickers_loaded,
        "tickers_failed": failed_tickers_list,
        "run_quality": run_quality,
        "last_full_run_utc": last_full_run_utc,
    }


_REGIME_WINDOW_DAYS = {"30d": 30, "60d": 60}


def get_regime_distribution(window: str = "30d") -> Dict:
    """
    ST-21 (BLG-FEAT-29): aggregate market regime distribution over screener
    run history. Contract: screener_api_contract.md.

    Source: screener_runs.regime_us / regime_uk (one row per run, not
    screener_results — that table is one row per *ticker*, which would
    weight the distribution by how many tickers happened to be evaluated in
    each market rather than by how often each market has actually been in
    each regime). Each run contributes one observation per market (US, UK)
    that has a non-null regime value for that run, so a run where a market's
    regime failed to resolve (regime_us/regime_uk NULL, e.g. an index price
    fetch failure) is excluded from that market's count rather than
    miscounted as a fabricated regime.

    window: "30d", "60d", or "all". Raises ValueError on any other value.
    """
    if window not in ("30d", "60d", "all"):
        raise ValueError(f"INVALID_PARAMS: window must be 30d, 60d, or all (got {window!r})")

    with get_db() as conn:
        with conn.cursor() as cur:
            params = []
            where = ""
            if window in _REGIME_WINDOW_DAYS:
                where = "WHERE run_timestamp >= NOW() - (%s || ' days')::interval"
                params.append(_REGIME_WINDOW_DAYS[window])

            cur.execute(
                f"""
                SELECT
                    COUNT(*) FILTER (WHERE regime_us = 'risk_on') AS us_risk_on,
                    COUNT(*) FILTER (WHERE regime_us = 'risk_off') AS us_risk_off,
                    COUNT(*) FILTER (WHERE regime_uk = 'risk_on') AS uk_risk_on,
                    COUNT(*) FILTER (WHERE regime_uk = 'risk_off') AS uk_risk_off,
                    COUNT(*) AS run_count
                FROM screener_runs
                {where}
                """,
                params,
            )
            row = cur.fetchone()

    us_risk_on = row["us_risk_on"] or 0
    us_risk_off = row["us_risk_off"] or 0
    uk_risk_on = row["uk_risk_on"] or 0
    uk_risk_off = row["uk_risk_off"] or 0
    risk_on = us_risk_on + uk_risk_on
    risk_off = us_risk_off + uk_risk_off
    total_observations = risk_on + risk_off

    if total_observations == 0:
        return {
            "window": window,
            "run_count": row["run_count"] or 0,
            "total_observations": 0,
            "risk_on_count": 0,
            "risk_off_count": 0,
            "risk_on_pct": None,
            "risk_off_pct": None,
        }

    return {
        "window": window,
        "run_count": row["run_count"] or 0,
        "total_observations": total_observations,
        "risk_on_count": risk_on,
        "risk_off_count": risk_off,
        "risk_on_pct": round(risk_on / total_observations * 100, 1),
        "risk_off_pct": round(risk_off / total_observations * 100, 1),
    }
