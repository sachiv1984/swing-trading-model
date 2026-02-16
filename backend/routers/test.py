"""
Endpoint Testing Router - Comprehensive test suite
Tests all API endpoints to verify system health
"""

from fastapi import APIRouter, HTTPException
import httpx
import time
import os

router = APIRouter(prefix="/test", tags=["Testing"])


@router.post("/endpoints")
async def test_all_endpoints():
    """
    Test all API endpoints and return results.
    
    Tests include:
    - Core endpoints (root, health)
    - Data endpoints (settings, positions, portfolio, trades, cash, signals)
    - Market data (market status, portfolio history)
    - Feature endpoints (tags)
    - Analytics endpoints (NEW)
    - Validation endpoints (NEW)
    
    Returns:
        dict: Test results with pass/fail status for each endpoint
    """
    
    # Get the base URL (same server we're running on)
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    # Define all test cases
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
        {"name": "GET /portfolio", "method": "GET", "url": f"{base_url}/portfolio", "critical": True},
        {"name": "GET /portfolio/history", "method": "GET", "url": f"{base_url}/portfolio/history?days=30", "critical": True},
        
        # Trade History
        {"name": "GET /trades", "method": "GET", "url": f"{base_url}/trades", "critical": True},
        
        # Cash Management
        {"name": "GET /cash/transactions", "method": "GET", "url": f"{base_url}/cash/transactions", "critical": True},
        {"name": "GET /cash/summary", "method": "GET", "url": f"{base_url}/cash/summary", "critical": True},
        
        # Signals & Market
        {"name": "GET /signals", "method": "GET", "url": f"{base_url}/signals", "critical": False},
        {"name": "GET /market/status", "method": "GET", "url": f"{base_url}/market/status", "critical": True},
        
        # Analytics (NEW)
        {"name": "GET /analytics/metrics (all_time)", "method": "GET", "url": f"{base_url}/analytics/metrics?period=all_time", "critical": True},
        {"name": "GET /analytics/metrics (last_7_days)", "method": "GET", "url": f"{base_url}/analytics/metrics?period=last_7_days", "critical": False},
        {"name": "GET /analytics/metrics (ytd)", "method": "GET", "url": f"{base_url}/analytics/metrics?period=ytd", "critical": False},
        
        # Validation (NEW)
        {"name": "POST /validate/calculations", "method": "POST", "url": f"{base_url}/validate/calculations", "critical": True},
    ]
    
    results = []
    passed = 0
    failed = 0
    errors = 0
    
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
                    response = await client.get(test["url"])
                elif test["method"] == "POST":
                    response = await client.post(test["url"], json={})
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
async def quick_health_check():
    """
    Quick health check - tests only critical endpoints.
    Faster than full test suite.
    """
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    
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
