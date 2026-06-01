"""
Endpoint Testing Router - Comprehensive test suite
Tests all API endpoints to verify system health
"""

from fastapi import APIRouter, HTTPException, Request
import httpx
import time
import os

router = APIRouter(prefix="/test", tags=["Testing"])


@router.post("/endpoints")
async def test_all_endpoints(request: Request):
    """
    Test all API endpoints and return results.

    Tests include:
    - Core endpoints (root, health)
    - Data endpoints (settings, positions, portfolio, trades, cash, signals)
    - Market data (market status, portfolio history)
    - Feature endpoints (tags)
    - Analytics endpoints
    - Alerts, notifications, digest endpoints
    - Validation endpoints

    Returns:
        dict: Test results with pass/fail status for each endpoint

    Note:
        - Forwards X-API-Key from incoming request to all downstream calls
        - API key forwarding (not middleware bypass) per ST-01 security constraint
    """

    # Auto-detect the base URL from the incoming request
    # This works both locally and on Render
    base_url = str(request.base_url).rstrip('/')

    # If API_BASE_URL is explicitly set, use that instead
    if os.getenv("API_BASE_URL"):
        base_url = os.getenv("API_BASE_URL").rstrip('/')

    # Extract API key from incoming request and forward to all downstream calls
    # This ensures auth-protected endpoints are tested with a valid key (ST-01)
    api_key = request.headers.get("X-API-Key", "")
    
    # Endpoint test list — source of truth: docs/reference/openapi.yaml (ST-02)
    # All parameterless GET endpoints plus key POST endpoints included.
    # When openapi.yaml is updated with new routes, add them here.
    test_cases = [
        # Core Endpoints
        {"name": "GET /", "method": "GET", "url": f"{base_url}/", "critical": True},
        {"name": "GET /health", "method": "GET", "url": f"{base_url}/health", "critical": True},
        {"name": "GET /health/detailed", "method": "GET", "url": f"{base_url}/health/detailed", "critical": True},

        # Settings & Configuration
        {"name": "GET /settings", "method": "GET", "url": f"{base_url}/settings", "critical": True},

        # Position & Portfolio Management
        {"name": "GET /positions", "method": "GET", "url": f"{base_url}/positions", "critical": True},
        {"name": "GET /positions/tags", "method": "GET", "url": f"{base_url}/positions/tags", "critical": False},
        {"name": "GET /positions/compliance", "method": "GET", "url": f"{base_url}/positions/compliance", "critical": False},
        {"name": "GET /portfolio", "method": "GET", "url": f"{base_url}/portfolio", "critical": True},
        {"name": "GET /portfolio/history", "method": "GET", "url": f"{base_url}/portfolio/history?days=30", "critical": True},

        # Trade History
        {"name": "GET /trades", "method": "GET", "url": f"{base_url}/trades", "critical": True},

        # Cash Management
        {"name": "GET /cash/transactions", "method": "GET", "url": f"{base_url}/cash/transactions", "critical": True},
        {"name": "GET /cash/summary", "method": "GET", "url": f"{base_url}/cash/summary", "critical": True},

        # Signals & Market
        {"name": "GET /signals", "method": "GET", "url": f"{base_url}/signals", "critical": False},
        {"name": "PATCH /signals/{id} (watchlisted)", "method": "PATCH", "url": f"{base_url}/signals/00000000-0000-0000-0000-000000000000", "body": {"status": "watchlisted"}, "critical": False},
        {"name": "GET /market/status", "method": "GET", "url": f"{base_url}/market/status", "critical": True},

        # Alerts (v2.3+)
        {"name": "GET /alerts/rules", "method": "GET", "url": f"{base_url}/alerts/rules", "critical": False},
        {"name": "GET /alerts/history", "method": "GET", "url": f"{base_url}/alerts/history", "critical": False},

        # Notifications (v2.3+)
        {"name": "GET /notifications", "method": "GET", "url": f"{base_url}/notifications", "critical": False},
        {"name": "GET /notifications/preferences", "method": "GET", "url": f"{base_url}/notifications/preferences", "critical": False},

        # Digest (v2.3+)
        {"name": "GET /digest/weekly", "method": "GET", "url": f"{base_url}/digest/weekly", "critical": False},

        # Analytics
        {"name": "GET /analytics/metrics (all_time)", "method": "GET", "url": f"{base_url}/analytics/metrics?period=all_time", "critical": True},
        {"name": "GET /analytics/metrics (last_7_days)", "method": "GET", "url": f"{base_url}/analytics/metrics?period=last_7_days", "critical": False},
        {"name": "GET /analytics/metrics (ytd)", "method": "GET", "url": f"{base_url}/analytics/metrics?period=ytd", "critical": False},
        {"name": "GET /analytics/cohort", "method": "GET", "url": f"{base_url}/analytics/cohort?period=month", "critical": False},
        {"name": "GET /analytics/r-multiple-distribution", "method": "GET", "url": f"{base_url}/analytics/r-multiple-distribution", "critical": False},
        {"name": "GET /analytics/compliance-metrics", "method": "GET", "url": f"{base_url}/analytics/compliance-metrics", "critical": False},

        # AI Journal
        {"name": "POST /ai/journal-summary", "method": "POST", "url": f"{base_url}/ai/journal-summary", "body": {"date_from": "2020-01-01"}, "critical": False},
        {"name": "GET /ai/journal-summary/history", "method": "GET", "url": f"{base_url}/ai/journal-summary/history", "critical": False},

        # News
        {"name": "GET /news/AAPL", "method": "GET", "url": f"{base_url}/news/AAPL", "critical": False},

        # Analytics (extended)
        {"name": "GET /analytics/market-correlation", "method": "GET", "url": f"{base_url}/analytics/market-correlation", "critical": False},

        # Arc 5 Compliance Metrics (v4.0 / ST-01)
        {"name": "GET /analytics/arc5-compliance", "method": "GET", "url": f"{base_url}/analytics/arc5-compliance", "critical": False},

        # Ticker Universe (v3.0 / ST-01)
        {"name": "GET /ticker-universe", "method": "GET", "url": f"{base_url}/ticker-universe", "critical": False},
        {"name": "POST /ticker-universe", "method": "POST", "url": f"{base_url}/ticker-universe", "body": {"ticker": "AAPL", "market": "US"}, "critical": False},
        {"name": "DELETE /ticker-universe/AAPL", "method": "DELETE", "url": f"{base_url}/ticker-universe/AAPL", "critical": False},

        # Screener (v3.0 / ST-04)
        {"name": "GET /screener/results", "method": "GET", "url": f"{base_url}/screener/results", "critical": False},
        {"name": "POST /screener/run", "method": "POST", "url": f"{base_url}/screener/run", "body": {}, "critical": False},

        # Trade Plans (v3.1 / ST-02)
        {"name": "GET /trade-plans", "method": "GET", "url": f"{base_url}/trade-plans", "critical": False},
        {"name": "POST /trade-plans", "method": "POST", "url": f"{base_url}/trade-plans", "body": {"ticker": "AAPL", "market": "US"}, "critical": False},
        {"name": "GET /trade-plans/by-position/00000000-0000-0000-0000-000000000000", "method": "GET", "url": f"{base_url}/trade-plans/by-position/00000000-0000-0000-0000-000000000000", "critical": False},
        {"name": "GET /trade-plans/00000000-0000-0000-0000-000000000001", "method": "GET", "url": f"{base_url}/trade-plans/00000000-0000-0000-0000-000000000001", "critical": False},
        {"name": "PUT /trade-plans/00000000-0000-0000-0000-000000000001", "method": "PUT", "url": f"{base_url}/trade-plans/00000000-0000-0000-0000-000000000001", "body": {"status": "active"}, "critical": False},
        {"name": "DELETE /trade-plans/00000000-0000-0000-0000-000000000001", "method": "DELETE", "url": f"{base_url}/trade-plans/00000000-0000-0000-0000-000000000001", "critical": False},
        {"name": "POST /trade-plans/{id}/generate-thesis", "method": "POST", "url": f"{base_url}/trade-plans/00000000-0000-0000-0000-000000000001/generate-thesis", "critical": False},

        # Earnings (v3.1 / ST-07)
        {"name": "GET /earnings/AAPL", "method": "GET", "url": f"{base_url}/earnings/AAPL", "critical": False},

        # Reports (v3.1 / ST-11)
        {"name": "GET /reports/monthly-pnl", "method": "GET", "url": f"{base_url}/reports/monthly-pnl", "critical": False},

        # Pre-Trade Research (v3.1 / ST-05)
        {"name": "GET /research/AAPL", "method": "GET", "url": f"{base_url}/research/AAPL?market=US", "critical": False},

        # Position Lifecycle (v3.3 / EPIC-01 ST-02)
        {"name": "GET /positions/00000000-0000-0000-0000-000000000000", "method": "GET", "url": f"{base_url}/positions/00000000-0000-0000-0000-000000000000", "critical": False},
        {"name": "POST /positions/00000000-0000-0000-0000-000000000000/refresh-state", "method": "POST", "url": f"{base_url}/positions/00000000-0000-0000-0000-000000000000/refresh-state", "critical": False},
        # Position Lifecycle Decision Support (v3.3 / EPIC-02)
        {"name": "GET /positions/grace-period-alerts", "method": "GET", "url": f"{base_url}/positions/grace-period-alerts", "critical": True},
        {"name": "GET /positions/{id}/stop-trail", "method": "GET", "url": f"{base_url}/positions/00000000-0000-0000-0000-000000000000/stop-trail", "critical": False},

        # Portfolio Risk (v3.4 / EPIC-02)
        {"name": "GET /portfolio/drawdown-status", "method": "GET", "url": f"{base_url}/portfolio/drawdown-status", "critical": False},
        {"name": "GET /portfolio/concentration-status", "method": "GET", "url": f"{base_url}/portfolio/concentration-status", "critical": False},

        # Paper Trading (v3.5 / EPIC-01 ST-02)
        {"name": "GET /portfolio/paper-positions", "method": "GET", "url": f"{base_url}/portfolio/paper-positions", "critical": False},

        # Pre-Entry Validation (v3.8 / EPIC-01 ST-02)
        {"name": "GET /portfolio/pre-entry-validation", "method": "GET", "url": f"{base_url}/portfolio/pre-entry-validation?ticker=AAPL&quantity=10&market=US", "critical": False},

        # Red Flag Journal (v3.9 / EPIC-03 ST-07)
        {"name": "GET /portfolio/red-flag-journal", "method": "GET", "url": f"{base_url}/portfolio/red-flag-journal", "critical": False},

        # Plan vs Reality (v3.5 / EPIC-02 ST-05)
        {"name": "GET /trades/{id}/plan-vs-reality", "method": "GET", "url": f"{base_url}/trades/00000000-0000-0000-0000-000000000000/plan-vs-reality", "critical": False},

        # Validation
        {"name": "POST /validate/calculations", "method": "POST", "url": f"{base_url}/validate/calculations", "critical": True},

        # AI Cost Monitoring (v4.1 / ST-09)
        {"name": "POST /ai/check-daily-cost", "method": "POST", "url": f"{base_url}/ai/check-daily-cost", "critical": False},

        # Claude API Audit Trail (v4.2 / ST-07)
        {"name": "GET /ai/claude-audit-log", "method": "GET", "url": f"{base_url}/ai/claude-audit-log", "critical": False},

        # SI-02 Behavioural Drift Detection (v4.6 / ST-04)
        {"name": "GET /analytics/behavioural-drift", "method": "GET", "url": f"{base_url}/analytics/behavioural-drift", "critical": False},
    ]
    
    results = []
    passed = 0
    failed = 0
    errors = 0
    
    # Build forwarded headers — include API key if present (ST-01)
    forward_headers = {}
    if api_key:
        forward_headers["X-API-Key"] = api_key

    async with httpx.AsyncClient(timeout=30.0) as client:
        for test in test_cases:
            result = {
                "endpoint": test["name"],
                "critical": test["critical"],
                "status": "unknown",
                "status_code": None,
                "response_time_ms": None,
                "error": None
            }

            try:
                start_time = time.time()

                if test["method"] == "GET":
                    response = await client.get(test["url"], headers=forward_headers)
                elif test["method"] == "POST":
                    response = await client.post(test["url"], json=test.get("body", {}), headers=forward_headers)
                elif test["method"] == "DELETE":
                    response = await client.delete(test["url"], headers=forward_headers)
                else:
                    raise ValueError(f"Unsupported method: {test['method']}")
                
                end_time = time.time()
                response_time_ms = (end_time - start_time) * 1000
                
                result["status_code"] = response.status_code
                result["response_time_ms"] = round(response_time_ms, 2)
                
                # Check if response is successful
                if 200 <= response.status_code < 300:
                    result["status"] = "pass"
                    passed += 1
                else:
                    result["status"] = "fail"
                    result["error"] = f"HTTP {response.status_code}: {response.text[:100]}"
                    failed += 1
                    
            except httpx.TimeoutException:
                result["status"] = "error"
                result["error"] = "Request timeout (>30s)"
                errors += 1
                
            except httpx.ConnectError as e:
                result["status"] = "error"
                result["error"] = f"Connection failed: {str(e)[:100]}"
                errors += 1
                
            except Exception as e:
                result["status"] = "error"
                result["error"] = f"Unexpected error: {str(e)[:100]}"
                errors += 1
            
            results.append(result)
    
    # Calculate success rate
    total = len(results)
    success_rate = (passed / total * 100) if total > 0 else 0
    
    return {
        "status": "ok",
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "success_rate": round(success_rate, 1)
        },
        "results": results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }


@router.get("/quick-health")
async def quick_health_check(request: Request):
    """
    Quick health check - tests only critical endpoints.
    Faster than full test suite.
    """
    # Auto-detect the base URL from the incoming request
    base_url = str(request.base_url).rstrip('/')
    
    # If API_BASE_URL is explicitly set, use that instead
    if os.getenv("API_BASE_URL"):
        base_url = os.getenv("API_BASE_URL").rstrip('/')
    
    critical_tests = [
        {"name": "Health", "url": f"{base_url}/health"},
        {"name": "Settings", "url": f"{base_url}/settings"},
        {"name": "Portfolio", "url": f"{base_url}/portfolio"},
    ]
    
    results = []
    all_healthy = True
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for test in critical_tests:
            try:
                start = time.time()
                response = await client.get(test["url"])
                duration = (time.time() - start) * 1000
                
                healthy = 200 <= response.status_code < 300
                all_healthy = all_healthy and healthy
                
                results.append({
                    "name": test["name"],
                    "healthy": healthy,
                    "response_time_ms": round(duration, 2),
                    "status_code": response.status_code
                })
                
            except Exception as e:
                all_healthy = False
                results.append({
                    "name": test["name"],
                    "healthy": False,
                    "error": str(e)[:100]
                })
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": results
    }
