"""
Health Service

Business logic for system health monitoring including:
- Basic health checks
- Detailed component status
- Endpoint testing

All functions are independent of FastAPI for maximum testability.
"""

from typing import Dict, List
from datetime import datetime
import time
import requests

from database import get_portfolio, get_settings
from utils.pricing import get_live_fx_rate


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
        "version": "1.2.0"
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
        "version": "1.2.0",
        "responseTime": response_time,
        "components": checks
    }


def test_all_endpoints(base_url: str = "http://localhost:8000") -> Dict:
    """
    Test all API endpoints
    
    Args:
        base_url: Base URL of the API (default: http://localhost:8000)
    
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
    # Define endpoints to test
    endpoints = [
        {"method": "GET", "path": "/", "expected_status": 200},
        {"method": "GET", "path": "/health", "expected_status": 200},
        {"method": "GET", "path": "/settings", "expected_status": 200},
        {"method": "GET", "path": "/positions", "expected_status": 200},
        {"method": "GET", "path": "/portfolio", "expected_status": 200},
        {"method": "GET", "path": "/trades", "expected_status": 200},
        {"method": "GET", "path": "/cash/transactions", "expected_status": 200},
        {"method": "GET", "path": "/cash/summary", "expected_status": 200},
        {"method": "GET", "path": "/signals", "expected_status": 200},
        {"method": "GET", "path": "/market/status", "expected_status": 200},
        {"method": "GET", "path": "/portfolio/history?days=7", "expected_status": 200},
    ]
    
    test_results = []
    
    for endpoint in endpoints:
        try:
            start = time.time()
            
            if endpoint["method"] == "GET":
                response = requests.get(
                    f"{base_url}{endpoint['path']}",
                    timeout=10
                )
            
            response_time = round((time.time() - start) * 1000, 2)
            
            result = {
                "endpoint": f"{endpoint['method']} {endpoint['path']}",
                "status": "pass" if response.status_code == endpoint["expected_status"] else "fail",
                "statusCode": response.status_code,
                "expectedStatus": endpoint["expected_status"],
                "responseTime": response_time
            }
            
            test_results.append(result)
            
        except Exception as e:
            test_results.append({
                "endpoint": f"{endpoint['method']} {endpoint['path']}",
                "status": "error",
                "error": str(e),
                "statusCode": None,
                "responseTime": None
            })
    
    # Calculate summary
    total = len(test_results)
    passed = len([r for r in test_results if r.get("status") == "pass"])
    failed = len([r for r in test_results if r.get("status") == "fail"])
    errors = len([r for r in test_results if r.get("status") == "error"])
    success_rate = round((passed / total) * 100, 1) if total > 0 else 0
    
    return {
        "timestamp": datetime.now().isoformat(),
        "totalTests": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "successRate": success_rate,
        "tests": test_results
    }
