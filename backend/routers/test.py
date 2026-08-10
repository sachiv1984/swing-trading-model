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
        {"name": "GET /health/scheduler", "method": "GET", "url": f"{base_url}/health/scheduler", "critical": False},
        {"name": "GET /health/database", "method": "GET", "url": f"{base_url}/health/database", "critical": False},

        # Changelog (ST-01, EPIC-01, v7.8)
        {"name": "GET /changelog/latest", "method": "GET", "url": f"{base_url}/changelog/latest", "critical": False},

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
        {"name": "POST /signals/rebalance-exit", "method": "POST", "url": f"{base_url}/signals/rebalance-exit", "critical": False},
        {"name": "POST /positions/nightly-stop-update", "method": "POST", "url": f"{base_url}/positions/nightly-stop-update", "critical": False},
        {"name": "POST /positions/risk-off-alerts", "method": "POST", "url": f"{base_url}/positions/risk-off-alerts", "critical": False},
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

        # Watchlist (v5.3 / ST-07)
        {"name": "GET /watchlist", "method": "GET", "url": f"{base_url}/watchlist", "critical": False},
        {"name": "POST /watchlist", "method": "POST", "url": f"{base_url}/watchlist", "body": {"ticker": "TSLA", "market": "US"}, "critical": False},
        {"name": "DELETE /watchlist/test-entry-id", "method": "DELETE", "url": f"{base_url}/watchlist/test-entry-id", "critical": False},

        # Analytics (extended)
        {"name": "GET /analytics/market-correlation", "method": "GET", "url": f"{base_url}/analytics/market-correlation", "critical": False},

        # Arc 5 Compliance Metrics (v4.0 / ST-01)
        {"name": "GET /analytics/arc5-compliance", "method": "GET", "url": f"{base_url}/analytics/arc5-compliance", "critical": False},

        # SI-04 Strategy Version Comparison (v7.7 / EPIC-01 ST-01, BLG-FEAT-75)
        {"name": "GET /analytics/strategy-version-comparison", "method": "GET", "url": f"{base_url}/analytics/strategy-version-comparison?version_from=1.0&version_to=1.4", "critical": False},

        # Trade Plan Tag Performance (v6.8 / ST-05, BLG-FEAT-52)
        {"name": "GET /analytics/tag-performance", "method": "GET", "url": f"{base_url}/analytics/tag-performance?tags=momentum", "critical": False},

        # Ticker Universe (v3.0 / ST-01)
        {"name": "GET /ticker-universe", "method": "GET", "url": f"{base_url}/ticker-universe", "critical": False},
        {"name": "POST /ticker-universe", "method": "POST", "url": f"{base_url}/ticker-universe", "body": {"ticker": "AAPL", "market": "US"}, "critical": False},
        {"name": "DELETE /ticker-universe/AAPL", "method": "DELETE", "url": f"{base_url}/ticker-universe/AAPL", "critical": False},

        # Screener (v3.0 / ST-04)
        {"name": "GET /screener/results", "method": "GET", "url": f"{base_url}/screener/results", "critical": False},
        {"name": "POST /screener/run", "method": "POST", "url": f"{base_url}/screener/run", "body": {}, "critical": False},
        {"name": "GET /screener/regime-distribution", "method": "GET", "url": f"{base_url}/screener/regime-distribution", "critical": False},

        # Trade Plans (v3.1 / ST-02)
        {"name": "GET /trade-plans", "method": "GET", "url": f"{base_url}/trade-plans", "critical": False},
        {"name": "GET /trade-plans/tags", "method": "GET", "url": f"{base_url}/trade-plans/tags", "critical": False},
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

        # On-Demand Compliance Recheck / Gap Risk Flag (v6.9 / EPIC-01 ST-01, EPIC-02 ST-02)
        {"name": "GET /positions/{id}/compliance-recheck", "method": "GET", "url": f"{base_url}/positions/00000000-0000-0000-0000-000000000000/compliance-recheck", "critical": False},
        {"name": "GET /positions/{id}/gap-risk", "method": "GET", "url": f"{base_url}/positions/00000000-0000-0000-0000-000000000000/gap-risk", "critical": False},

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

        # Claude API Monthly Cost (v7.6 / EPIC-07 ST-07)
        {"name": "GET /ai/monthly-cost", "method": "GET", "url": f"{base_url}/ai/monthly-cost", "critical": False},
        {"name": "GET /ai/spend-trend", "method": "GET", "url": f"{base_url}/ai/spend-trend", "critical": False},

        # SI-02 Behavioural Drift Detection (v4.6 / ST-04)
        {"name": "GET /analytics/behavioural-drift", "method": "GET", "url": f"{base_url}/analytics/behavioural-drift", "critical": False},

        # Signal allocation_insufficient status (v5.0 / ST-06)
        {"name": "GET /signals?status=allocation_insufficient", "method": "GET", "url": f"{base_url}/signals?status=allocation_insufficient", "critical": False},

        # SI-05 Phase 1 strategy integrity digest (v5.1 / ST-01)
        {"name": "POST /digest/si05/send", "method": "POST", "url": f"{base_url}/digest/si05/send", "body": {}, "critical": False},

        # Trade count gate metrics (v5.5 / ST-04)
        {"name": "GET /portfolio/gate-metrics", "method": "GET", "url": f"{base_url}/portfolio/gate-metrics", "critical": False},

        # Net-of-costs trade cost update (v6.0 / EPIC-02 ST-03)
        {"name": "PATCH /trades/{id}/costs", "method": "PATCH", "url": f"{base_url}/trades/00000000-0000-0000-0000-000000000000/costs", "critical": False},

        # Sector concentration heat map (v6.1 / EPIC-03 ST-06)
        {"name": "GET /portfolio/sector-weights", "method": "GET", "url": f"{base_url}/portfolio/sector-weights", "critical": False},
        {"name": "GET /portfolio/sector-regime-trend", "method": "GET", "url": f"{base_url}/portfolio/sector-regime-trend", "critical": False},

        # Setup Quality Score (v6.1 / EPIC-04 ST-08)
        {"name": "GET /trade-plans/setup-quality-score", "method": "GET", "url": f"{base_url}/trade-plans/setup-quality-score?ticker=AAPL", "critical": False},

        # AI Daily Briefing (v6.2 / EPIC-02 ST-06)
        {"name": "POST /ai/daily-briefing", "method": "POST", "url": f"{base_url}/ai/daily-briefing", "critical": False},

        # AI Chat Advisor (v6.2 / EPIC-02 ST-08)
        {"name": "POST /ai/chat", "method": "POST", "url": f"{base_url}/ai/chat", "body": {"question": "How many positions do I have open?"}, "critical": False},

        # Strategy Benchmark (v6.3 / EPIC-03 ST-11)
        {"name": "GET /strategy/benchmark/summary", "method": "GET", "url": f"{base_url}/strategy/benchmark/summary", "critical": False},
        {"name": "GET /strategy/benchmark/trades", "method": "GET", "url": f"{base_url}/strategy/benchmark/trades", "critical": False},
        {"name": "POST /strategy/benchmark/import", "method": "POST", "url": f"{base_url}/strategy/benchmark/import", "body": {"trades": [], "yearly_performance": []}, "critical": False},

        # Strategy Benchmark Open Positions (v6.4 / EPIC-03 ST-08)
        {"name": "GET /strategy/benchmark/open-positions", "method": "GET", "url": f"{base_url}/strategy/benchmark/open-positions", "critical": False},

        # AI rate limit 429 scenario verification (v6.3 / EPIC-01 ST-03)
        {"name": "POST /test/rate-limit-scenarios", "method": "POST", "url": f"{base_url}/test/rate-limit-scenarios", "critical": False},

        # Custom Price Alerts (v7.5 / EPIC-02 ST-02, BLG-FE-116)
        {"name": "GET /price-alerts", "method": "GET", "url": f"{base_url}/price-alerts", "critical": False},
        {"name": "POST /price-alerts", "method": "POST", "url": f"{base_url}/price-alerts", "body": {"ticker": "AAPL", "condition": "above", "threshold_price": 1.0}, "critical": False},
        {"name": "DELETE /price-alerts/00000000-0000-0000-0000-000000000000", "method": "DELETE", "url": f"{base_url}/price-alerts/00000000-0000-0000-0000-000000000000", "critical": False},

        # Bulk Actions Toolbar — Watchlist (v7.5 / EPIC-03 ST-03, BLG-FE-117)
        {"name": "GET /watchlist/tags", "method": "GET", "url": f"{base_url}/watchlist/tags", "critical": False},
        {"name": "POST /watchlist/bulk-tag", "method": "POST", "url": f"{base_url}/watchlist/bulk-tag", "body": {"ids": [], "tags": ["momentum"]}, "critical": False},
        {"name": "DELETE /watchlist/bulk", "method": "DELETE", "url": f"{base_url}/watchlist/bulk", "body": {"ids": []}, "critical": False},

        # Bulk Actions Toolbar — Trade Plans (v7.5 / EPIC-03 ST-03, BLG-FE-117)
        {"name": "POST /trade-plans/bulk-tag", "method": "POST", "url": f"{base_url}/trade-plans/bulk-tag", "body": {"ids": [], "tags": ["momentum"]}, "critical": False},
        {"name": "PUT /trade-plans/bulk-archive", "method": "PUT", "url": f"{base_url}/trade-plans/bulk-archive", "body": {"ids": []}, "critical": False},
        {"name": "DELETE /trade-plans/bulk", "method": "DELETE", "url": f"{base_url}/trade-plans/bulk", "body": {"ids": []}, "critical": False},

        # Saved Filters & Daily P&L — Calendar View (v7.5 / EPIC-04 ST-04, BLG-FE-118)
        {"name": "GET /reports/daily-pnl", "method": "GET", "url": f"{base_url}/reports/daily-pnl?year=2026&month=7", "critical": False},
        {"name": "GET /saved-filters", "method": "GET", "url": f"{base_url}/saved-filters", "critical": False},
        {"name": "POST /saved-filters", "method": "POST", "url": f"{base_url}/saved-filters", "body": {"name": "__test__", "filter_state": {}}, "critical": False},
        {"name": "DELETE /saved-filters/00000000-0000-0000-0000-000000000000", "method": "DELETE", "url": f"{base_url}/saved-filters/00000000-0000-0000-0000-000000000000", "critical": False},

        # ST-11 (BLG-QA-133, EPIC-03, v7.10): coverage audit additions — all
        # confirmed read-only / no-side-effect (or side effects already
        # accepted for a sibling endpoint) before being added here.
        {"name": "GET /portfolio/prospective-heat", "method": "GET", "url": f"{base_url}/portfolio/prospective-heat?ticker=AAPL&shares=10&entry_price=100&stop_price=90", "critical": False},
        {"name": "GET /positions/search/tags", "method": "GET", "url": f"{base_url}/positions/search/tags?tags=momentum", "critical": False},
        {"name": "GET /reports/tax-year", "method": "GET", "url": f"{base_url}/reports/tax-year?year=2025", "critical": False},
        {"name": "GET /reports/reconciliation", "method": "GET", "url": f"{base_url}/reports/reconciliation?year=2025", "critical": False},
        {"name": "GET /trades/export/csv", "method": "GET", "url": f"{base_url}/trades/export/csv", "critical": False},
        {"name": "POST /portfolio/size", "method": "POST", "url": f"{base_url}/portfolio/size", "body": {"entry_price": 100.0, "stop_price": 90.0, "risk_percent": 1.0, "market": "US"}, "critical": False},
        {"name": "POST /trade-plans/generate-plan", "method": "POST", "url": f"{base_url}/trade-plans/generate-plan", "body": {"ticker": "AAPL", "market": "US"}, "critical": False},
    ]

    # ST-11 (BLG-QA-133) coverage-audit disposition — endpoints deliberately
    # NOT added above, with rationale (see docs/ops/endpoint_test_coverage_audit_2026-07-29.md
    # for the full audit):
    #   - Real-data-mutating endpoints (POST /cash/transaction, POST /portfolio/position,
    #     POST /portfolio/snapshot, POST/PATCH/DELETE /alerts/rules, POST /alerts/evaluate,
    #     POST/PATCH /settings, POST /signals/generate, POST /notifications/mark-all-read,
    #     PATCH /notifications/{id}, POST /positions/{id}/exit, PATCH /positions/{id}/mark-reviewed,
    #     PATCH /positions/{id}/note, PATCH /positions/{id}/tags, PATCH /watchlist/{id},
    #     DELETE /signals/{id}): would mutate the live single-portfolio production system's
    #     real financial/trading state every time this smoke test is run — correctly excluded,
    #     not an oversight.
    #   - GET /positions/analyze: despite the GET verb, updates trailing stops and position
    #     data in the database (see services/position_service.py::analyze_positions docstring)
    #     — same mutation-risk exclusion as above.
    #   - GET /trades/{trade_id}/reflection: always returns 404 for any placeholder trade_id
    #     (no reflection exists until explicitly saved) — unsuitable for this harness's
    #     2xx-only pass criterion; not a coverage gap in the sense of "never exercised",
    #     just not expressible in this test shape.
    #   - POST /test/endpoints: this endpoint itself — recursive self-call excluded.
    
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
                elif test["method"] == "PUT":
                    response = await client.put(test["url"], json=test.get("body", {}), headers=forward_headers)
                elif test["method"] == "PATCH":
                    response = await client.patch(test["url"], json=test.get("body", {}), headers=forward_headers)
                elif test["method"] == "DELETE":
                    response = await client.request(
                        "DELETE", test["url"], json=test.get("body", {}), headers=forward_headers
                    )
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


@router.post("/rate-limit-scenarios")
async def rate_limit_scenarios():
    """
    Verify rate limiting logic for POST /ai/daily-briefing (limit=10) and
    POST /ai/chat (limit=30). Uses isolated test keys so live traffic is not
    affected. AC-05 for ST-03 (BLG-OPS-81, EPIC-01, v6.3).
    """
    from services.rate_limiter import _ai_limiter

    results = []

    for endpoint, key, limit in [
        ("POST /ai/daily-briefing", "daily-briefing:__test__", 10),
        ("POST /ai/chat", "chat:__test__", 30),
    ]:
        _ai_limiter.reset(key)
        try:
            # Drain the window
            for _ in range(limit):
                allowed, _ = _ai_limiter.is_allowed(key, limit=limit)
                if not allowed:
                    results.append({
                        "endpoint": endpoint,
                        "status": "fail",
                        "error": f"Rate limiter rejected before {limit} requests were consumed",
                    })
                    _ai_limiter.reset(key)
                    break
            else:
                # One more call must be rejected (429 territory)
                allowed, retry_after = _ai_limiter.is_allowed(key, limit=limit)
                if allowed:
                    results.append({
                        "endpoint": endpoint,
                        "status": "fail",
                        "error": f"Expected rejection after {limit} requests but was still allowed",
                    })
                else:
                    results.append({
                        "endpoint": endpoint,
                        "status": "pass",
                        "limit": limit,
                        "retry_after_secs": retry_after,
                    })
                _ai_limiter.reset(key)
        except Exception as exc:
            results.append({"endpoint": endpoint, "status": "error", "error": str(exc)[:200]})
            _ai_limiter.reset(key)

    all_pass = all(r["status"] == "pass" for r in results)
    return {"status": "ok" if all_pass else "fail", "scenarios": results}
