"""
Health Service

Business logic for system health monitoring including:
- Basic health checks
- Detailed component status
- Endpoint testing

All functions are independent of FastAPI for maximum testability.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta
import time
import requests
import collections
import math

import os
import urllib.parse
import urllib.request
import json

from database import get_portfolio, get_settings, get_database_size_bytes
from utils.pricing import get_live_fx_rate


# Module-level tracking (in-memory; resets on process restart)
_health_state: Dict = {
    "last_market_status_check": None,
    "last_alert_evaluation": None,
}

# External API rolling window — keeps last 100 call outcomes per API (ST-08)
_ROLLING_WINDOW = 100
_ext_api_state: Dict = {
    "alpaca": {
        "last_successful_call": None,
        "calls": collections.deque(maxlen=_ROLLING_WINDOW),
    },
    "yahoo_finance": {
        "last_successful_call": None,
        "calls": collections.deque(maxlen=_ROLLING_WINDOW),
    },
}

# Render free tier PostgreSQL limit (256 MB)
_RENDER_DB_LIMIT_BYTES: int = 268_435_456

# Rate-limit: suppress duplicate DB size alerts within this window (seconds)
_DB_ALERT_COOLDOWN_SECONDS: int = 3600

# Last DB size alert timestamp (module-level; resets on process restart)
_last_db_size_alert_utc: Optional[datetime] = None

# Nightly job last-run status (ST-13, BLG-OPS-79).
# Updated by each nightly computation endpoint on completion.
# Resets on process restart (Render spins up a fresh process on each deploy).
_NIGHTLY_JOB_NAMES = ("trailing_stop", "rebalance_exit", "inv_vol_sizing", "custom_price_alerts", "screener_refresh", "risk_off_alerts")
_nightly_job_status: Dict = {
    job: {
        "last_run_utc": None,
        "last_status": "never_run",
        "last_error": None,
        "detail": None,
    }
    for job in _NIGHTLY_JOB_NAMES
}


def record_external_api_call(api_name: str, success: bool, latency_ms: float) -> None:
    """Record the outcome of an external API call for health monitoring (ST-08)."""
    if api_name not in _ext_api_state:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    _ext_api_state[api_name]["calls"].append({
        "success": success,
        "latency_ms": latency_ms,
        "ts": now_iso,
    })
    if success:
        _ext_api_state[api_name]["last_successful_call"] = now_iso


def get_external_api_health() -> Dict:
    """Return external_apis health section for GET /health (ST-08)."""
    result = {}
    for api_name, state in _ext_api_state.items():
        calls = list(state["calls"])
        if not calls:
            result[api_name] = {
                "last_successful_call": None,
                "error_rate": 0.0,
                "p95_latency_ms": None,
            }
        else:
            error_count = sum(1 for c in calls if not c["success"])
            error_rate = round(error_count / len(calls), 4)
            latencies = sorted(c["latency_ms"] for c in calls if c["success"])
            p95 = None
            if latencies:
                idx = math.ceil(0.95 * len(latencies)) - 1
                p95 = int(latencies[max(0, idx)])
            result[api_name] = {
                "last_successful_call": state["last_successful_call"],
                "error_rate": error_rate,
                "p95_latency_ms": p95,
            }
    return result


def get_ai_journal_health() -> Dict:
    """Return ai_journal health section for GET /health (ST-09)."""
    try:
        from database import get_db
        now = datetime.utcnow()
        seven_days_ago = now - timedelta(days=7)
        one_day_ago = now - timedelta(days=1)

        with get_db() as conn:
            with conn.cursor() as cur:
                # usage_rate: summaries produced in last 7 days / 7
                cur.execute(
                    "SELECT COUNT(*) FROM ai_audit_log WHERE invoked_at >= %s",
                    (seven_days_ago,),
                )
                row = cur.fetchone()
                count_7d = row[0] if row else 0

                # error_rate: failed runs in last 24h / total last 24h
                cur.execute(
                    "SELECT COUNT(*), SUM(CASE WHEN summary_produced=FALSE THEN 1 ELSE 0 END) "
                    "FROM ai_audit_log WHERE invoked_at >= %s",
                    (one_day_ago,),
                )
                row = cur.fetchone()
                total_24h = row[0] if row else 0
                failed_24h = row[1] if row and row[1] else 0

                # p95_latency_ms from duration_ms (column may not exist yet)
                p95 = None
                try:
                    cur.execute(
                        "SELECT duration_ms FROM ai_audit_log "
                        "WHERE invoked_at >= %s AND duration_ms IS NOT NULL "
                        "ORDER BY duration_ms",
                        (one_day_ago,),
                    )
                    durations = [r[0] for r in cur.fetchall()]
                    if durations:
                        idx = math.ceil(0.95 * len(durations)) - 1
                        p95 = int(durations[max(0, idx)])
                except Exception:
                    pass  # column absent on older deploys

        if count_7d == 0 and total_24h == 0:
            return {"status": "unavailable"}

        usage_rate = round(count_7d / 7.0, 4)
        error_rate = round(failed_24h / total_24h, 4) if total_24h > 0 else 0.0
        return {
            "usage_rate": usage_rate,
            "error_rate": error_rate,
            "p95_latency_ms": p95,
        }
    except Exception:
        return {"status": "unavailable"}


def record_market_status_check() -> None:
    """Record the timestamp of the most recent market status check."""
    _health_state["last_market_status_check"] = datetime.now(timezone.utc).isoformat()


def record_alert_evaluation() -> None:
    """Record the timestamp of the most recent alert evaluation."""
    _health_state["last_alert_evaluation"] = datetime.now(timezone.utc).isoformat()


def get_operational_health() -> Dict:
    """
    Operational health check per ST-08 AC (v2.2).

    Returns:
        Dictionary with:
            - status: "ok" | "error"
            - db: "connected" | "error"
            - last_market_status_check: ISO-8601 string or null
            - last_alert_evaluation: ISO-8601 string or null
    """
    try:
        get_portfolio()
        db_status = "connected"
        overall = "ok"
    except Exception:
        db_status = "error"
        overall = "error"

    return {
        "status": overall,
        "db": db_status,
        "last_market_status_check": _health_state["last_market_status_check"],
        "last_alert_evaluation": _health_state["last_alert_evaluation"],
        "external_apis": get_external_api_health(),
        "ai_journal": get_ai_journal_health(),
    }


def get_basic_health() -> Dict:
    """
    Basic health check - fast response for load balancers
    
    Returns:
        Dictionary with:
            - status: "healthy"
            - timestamp: Current timestamp
            - version: Application version
    
    Note:
        - Fast response (<10ms)
        - Use for load balancer health checks
        - Returns 200 OK if system is running
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.4.0"
    }


def get_detailed_health() -> Dict:
    """
    Comprehensive system status check
    
    Checks:
        - Database connectivity
        - External services (Yahoo Finance)
        - Service layer health
        - Configuration validity
    
    Returns:
        Dictionary with:
            - status: Overall status ("healthy", "degraded", "unhealthy")
            - timestamp: Check timestamp
            - version: Application version
            - responseTime: Response time in milliseconds
            - components: Component-level health checks
    
    Note:
        - Checks all critical system components
        - Returns "degraded" if any component unhealthy
        - Use for post-deployment verification
    """
    start_time = time.time()
    
    checks = {
        "database": {"status": "unknown", "details": None},
        "yahooFinance": {"status": "unknown", "details": None},
        "services": {"status": "unknown", "details": None},
        "config": {"status": "unknown", "details": None}
    }
    
    # 1. Database check
    try:
        portfolio = get_portfolio()
        checks["database"]["status"] = "healthy"
        checks["database"]["details"] = {
            "connected": True,
            "portfolio_exists": portfolio is not None
        }
    except Exception as e:
        checks["database"]["status"] = "unhealthy"
        checks["database"]["details"] = {"error": str(e)}
    
    # 2. Yahoo Finance check
    try:
        fx_rate = get_live_fx_rate()
        checks["yahooFinance"]["status"] = "healthy"
        checks["yahooFinance"]["details"] = {
            "gbp_usd_rate": fx_rate,
            "accessible": True
        }
    except Exception as e:
        checks["yahooFinance"]["status"] = "unhealthy"
        checks["yahooFinance"]["details"] = {"error": str(e)}
    
    # 3. Service layer check (verify imports work)
    try:
        from services import (
            get_positions_with_prices,
            get_portfolio_summary,
            get_cash_summary
        )
        checks["services"]["status"] = "healthy"
        checks["services"]["details"] = {
            "position_service": "available",
            "portfolio_service": "available",
            "cash_service": "available",
            "trade_service": "available",
            "signal_service": "available"
        }
    except Exception as e:
        checks["services"]["status"] = "unhealthy"
        checks["services"]["details"] = {"error": str(e)}
    
    # 4. Config check
    try:
        settings = get_settings()
        checks["config"]["status"] = "healthy"
        checks["config"]["details"] = {
            "settings_loaded": len(settings) > 0 if settings else False
        }
    except Exception as e:
        checks["config"]["status"] = "unhealthy"
        checks["config"]["details"] = {"error": str(e)}
    
    # Overall status
    all_healthy = all(c["status"] == "healthy" for c in checks.values())
    overall_status = "healthy" if all_healthy else "degraded"
    
    response_time = round((time.time() - start_time) * 1000, 2)
    
    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "version": "1.4.0",
        "response_time_ms": response_time,
        "checks": checks
    }


def test_all_endpoints(base_url: str = None, api_key: str = None) -> Dict:
    """
    Test all API endpoints

    Args:
        base_url: Base URL of the API (if None, uses localhost:8000)
        api_key: X-API-Key value to forward to auth-protected endpoints (ST-01)

    Returns:
        Dictionary with:
            - timestamp: Test timestamp
            - summary: Summary statistics (total, passed, failed, errors, success_rate)
            - results: List of test results for each endpoint

    Note:
        - Tests all GET endpoints that don't require parameters
        - Returns pass/fail status for each
        - Includes response times
        - Use for post-deployment smoke tests
        - Can take 10-30 seconds to complete
    """
    # If no base_url provided, use localhost (for local testing)
    if base_url is None:
        base_url = "http://localhost:8000"

    # Remove trailing slash if present
    base_url = base_url.rstrip('/')

    # Build forwarded headers — include API key if present (ST-01)
    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key

    # Endpoint list — source of truth: docs/reference/openapi.yaml (ST-02)
    # All parameterless GET endpoints included. Update when openapi.yaml adds new routes.
    endpoints = [
        {"method": "GET", "path": "/", "expected_status": 200},
        {"method": "GET", "path": "/health", "expected_status": 200},
        {"method": "GET", "path": "/health/detailed", "expected_status": 200},
        {"method": "GET", "path": "/settings", "expected_status": 200},
        {"method": "GET", "path": "/positions", "expected_status": 200},
        {"method": "GET", "path": "/positions/tags", "expected_status": 200},
        {"method": "GET", "path": "/positions/compliance", "expected_status": 200},
        {"method": "GET", "path": "/portfolio", "expected_status": 200},
        {"method": "GET", "path": "/trades", "expected_status": 200},
        {"method": "GET", "path": "/cash/transactions", "expected_status": 200},
        {"method": "GET", "path": "/cash/summary", "expected_status": 200},
        {"method": "GET", "path": "/signals", "expected_status": 200},
        {"method": "GET", "path": "/market/status", "expected_status": 200},
        {"method": "GET", "path": "/portfolio/history?days=7", "expected_status": 200},
        {"method": "GET", "path": "/alerts/rules", "expected_status": 200},
        {"method": "GET", "path": "/alerts/history", "expected_status": 200},
        {"method": "GET", "path": "/notifications", "expected_status": 200},
        {"method": "GET", "path": "/notifications/preferences", "expected_status": 200},
        {"method": "GET", "path": "/digest/weekly", "expected_status": 200},
        {"method": "GET", "path": "/analytics/cohort?period=month", "expected_status": 200},
        {"method": "GET", "path": "/analytics/r-multiple-distribution", "expected_status": 200},
        {"method": "GET", "path": "/analytics/compliance-metrics", "expected_status": 200},
    ]

    test_results = []

    for endpoint in endpoints:
        try:
            start = time.time()

            if endpoint["method"] == "GET":
                response = requests.get(
                    f"{base_url}{endpoint['path']}",
                    headers=headers,
                    timeout=10
                )
            
            response_time = round((time.time() - start) * 1000, 2)
            
            result = {
                "endpoint": f"{endpoint['method']} {endpoint['path']}",
                "status": "pass" if response.status_code == endpoint["expected_status"] else "fail",
                "status_code": response.status_code,
                "expected_status": endpoint["expected_status"],
                "response_time_ms": response_time
            }
            
            test_results.append(result)
            
        except Exception as e:
            test_results.append({
                "endpoint": f"{endpoint['method']} {endpoint['path']}",
                "status": "error",
                "error": str(e),
                "status_code": None,
                "response_time_ms": None
             })
    
    # Calculate summary
    total = len(test_results)
    passed = len([r for r in test_results if r.get("status") == "pass"])
    failed = len([r for r in test_results if r.get("status") == "fail"])
    errors = len([r for r in test_results if r.get("status") == "error"])
    success_rate = round((passed / total) * 100, 1) if total > 0 else 0
    
    return {
    "timestamp": datetime.now().isoformat(),
    "summary": {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "success_rate": success_rate
    },
    "results": test_results
}


def record_nightly_job(job_name: str, status: str, detail: Optional[Dict] = None, error: Optional[str] = None) -> None:
    """Record completion of a nightly computation job (ST-13, BLG-OPS-79)."""
    if job_name not in _nightly_job_status:
        return
    _nightly_job_status[job_name]["last_run_utc"] = datetime.now(timezone.utc).isoformat()
    _nightly_job_status[job_name]["last_status"] = status
    _nightly_job_status[job_name]["last_error"] = error
    _nightly_job_status[job_name]["detail"] = detail


def get_scheduler_health() -> Dict:
    """Return last-run status for all nightly computation jobs (ST-13, BLG-OPS-79).

    Trigger mechanism: GitHub Actions external cron (not an in-process scheduler).
    Jobs: trailing_stop (POST /positions/nightly-stop-update),
          rebalance_exit (POST /signals/rebalance-exit),
          inv_vol_sizing (co-invoked by rebalance-exit or manual trigger),
          custom_price_alerts (co-invoked by POST /alerts/evaluate, ST-02/BLG-FE-116),
          screener_refresh (POST /screener/run, ST-01/BLG-OPS-144, v8.8),
          risk_off_alerts (POST /positions/risk-off-alerts, ST-02/BLG-OPS-145, v8.8).
    Status resets on process restart — Render spins up a fresh process on each deploy.
    """
    jobs = {}
    for job_name, state in _nightly_job_status.items():
        jobs[job_name] = {
            "last_run_utc": state["last_run_utc"],
            "last_status": state["last_status"],
            "last_error": state["last_error"],
            "detail": state["detail"],
        }
    all_ok = all(s["last_status"] in ("ok", "never_run") for s in _nightly_job_status.values())
    return {
        "scheduler_type": "github_actions_external_cron",
        "trigger_endpoints": {
            "trailing_stop": "POST /positions/nightly-stop-update",
            "rebalance_exit": "POST /signals/rebalance-exit",
            "inv_vol_sizing": "co-invoked by rebalance-exit",
            "custom_price_alerts": "co-invoked by POST /alerts/evaluate",
            "screener_refresh": "POST /screener/run",
            "risk_off_alerts": "POST /positions/risk-off-alerts",
        },
        "overall_status": "ok" if all_ok else "degraded",
        "jobs": jobs,
        "note": "Status resets on process restart. A never_run status after a recent deploy is normal.",
    }


def get_db_size_info() -> Dict:
    """
    Query current database size and return monitoring data.

    Returns:
        Dictionary with:
            - size_bytes: raw database size in bytes
            - size_mb: size in megabytes (2 d.p.)
            - limit_bytes: Render free tier limit (268,435,456 = 256 MB)
            - limit_mb: limit in megabytes
            - used_percent: percentage of limit used (2 d.p.)
            - threshold_percent: alert threshold (from DB_SIZE_ALERT_THRESHOLD_PERCENT env var, default 80)
            - status: "ok" | "warning" | "error"
                  "ok"      — below threshold
                  "warning" — at or above threshold
                  "error"   — could not query size

    Implements BLG-OPS-09. Alert is notification-only per §3 compliance.
    """
    threshold_percent = float(os.getenv("DB_SIZE_ALERT_THRESHOLD_PERCENT", "80"))
    try:
        size_bytes = get_database_size_bytes()
        size_mb = round(size_bytes / (1024 * 1024), 2)
        limit_mb = round(_RENDER_DB_LIMIT_BYTES / (1024 * 1024), 2)
        used_percent = round(size_bytes / _RENDER_DB_LIMIT_BYTES * 100, 2)
        status = "warning" if used_percent >= threshold_percent else "ok"
        return {
            "size_bytes": size_bytes,
            "size_mb": size_mb,
            "limit_bytes": _RENDER_DB_LIMIT_BYTES,
            "limit_mb": limit_mb,
            "used_percent": used_percent,
            "threshold_percent": threshold_percent,
            "status": status,
        }
    except Exception as e:
        return {
            "size_bytes": None,
            "size_mb": None,
            "limit_bytes": _RENDER_DB_LIMIT_BYTES,
            "limit_mb": round(_RENDER_DB_LIMIT_BYTES / (1024 * 1024), 2),
            "used_percent": None,
            "threshold_percent": threshold_percent,
            "status": "error",
            "error": str(e),
        }


def send_db_size_alert_if_needed(db_info: Dict) -> bool:
    """
    Send a Telegram alert if DB usage is at or above the configured threshold.

    Rate-limited: suppresses duplicate alerts within _DB_ALERT_COOLDOWN_SECONDS.
    Alert is notification-only — no automated cleanup (§3 compliance).

    Args:
        db_info: Dictionary returned by get_db_size_info()

    Returns:
        True if an alert was sent, False otherwise.
    """
    global _last_db_size_alert_utc

    if db_info.get("status") != "warning":
        return False

    now = datetime.now(timezone.utc)
    if _last_db_size_alert_utc is not None:
        elapsed = (now - _last_db_size_alert_utc).total_seconds()
        if elapsed < _DB_ALERT_COOLDOWN_SECONDS:
            return False

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not telegram_token or not telegram_chat_id:
        return False

    used_pct = db_info.get("used_percent", 0)
    size_mb = db_info.get("size_mb", 0)
    limit_mb = db_info.get("limit_mb", 256)
    threshold_pct = db_info.get("threshold_percent", 80)

    title = "⚠️ Database Size Warning"
    message = (
        f"Database is {used_pct:.1f}% full "
        f"({size_mb:.1f} MB of {limit_mb:.0f} MB used). "
        f"Alert threshold: {threshold_pct:.0f}%. "
        f"No automated action taken — manual review recommended."
    )
    text = f"*{title}*\n{message}"

    try:
        params = urllib.parse.urlencode({
            "chat_id": telegram_chat_id,
            "text": text,
            "parse_mode": "Markdown",
        })
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?{params}"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
            if not body.get("ok"):
                raise RuntimeError(f"Telegram API error: {body}")
        _last_db_size_alert_utc = now
        return True
    except Exception as e:
        # Log and suppress — never raise from a monitoring side-effect
        import logging
        logging.getLogger(__name__).error("send_db_size_alert_if_needed failed: %s", e)
        return False
