"""
System Status Yahoo Finance check detects an outage (ST-06, EPIC-01, v9.14,
BLG-OPS-194).

get_live_fx_rate() never raises: it returns a fallback rate. So the check
that called it and reported "healthy" whenever a number came back passed
during a Yahoo outage. It now reads the FX source (ST-04/ST-05) and the
regime sources (ST-02/ST-03) and gives the reason in `details`.
"""
from unittest.mock import patch

import services.health_service as health_service

LIVE_FX = {"fx_rate": 1.3412, "fx_rate_source": "live", "fx_rate_as_of": "2026-10-29T09:00:00+00:00"}
LAST_KNOWN_FX = {"fx_rate": 1.3301, "fx_rate_source": "last_known", "fx_rate_as_of": "2026-10-27T15:30:00+00:00"}
CONSTANT_FX = {"fx_rate": 1.27, "fx_rate_source": "constant", "fx_rate_as_of": None}
YAHOO_REGIME = {"spy_source": "yahoo_finance", "ftse_source": "yahoo_finance"}
FAILED_REGIME = {"spy_source": None, "ftse_source": None}


def _check(fx, regime):
    with patch.object(health_service, "get_live_fx_rate", return_value=fx["fx_rate"]), \
         patch.object(health_service, "get_fx_rate_info", return_value=fx), \
         patch.object(health_service, "check_market_regime", return_value=regime):
        return health_service._yahoo_finance_check()


def test_fx_fetch_failure_is_not_healthy():
    result = _check(LAST_KNOWN_FX, YAHOO_REGIME)
    assert result["status"] == "degraded"
    assert "GBP/USD fetch failed" in result["details"]["reason"]
    assert "1.3301" in result["details"]["reason"]


def test_fx_constant_fallback_is_not_healthy():
    result = _check(CONSTANT_FX, YAHOO_REGIME)
    assert result["status"] == "degraded"
    assert "fixed fallback 1.2700" in result["details"]["reason"]


def test_successful_fetch_is_healthy_with_the_live_rate():
    result = _check(LIVE_FX, YAHOO_REGIME)
    assert result["status"] == "healthy"
    assert result["details"]["gbp_usd_rate"] == 1.3412
    assert result["details"]["fx_rate_source"] == "live"
    assert "reason" not in result["details"]


def test_regime_fetch_failure_is_not_healthy():
    result = _check(LIVE_FX, FAILED_REGIME)
    assert result["status"] != "healthy"
    assert "SPY regime data unavailable; regime unknown" in result["details"]["reason"]
    assert "FTSE regime data unavailable" in result["details"]["reason"]


def test_spy_regime_from_alpaca_is_degraded():
    result = _check(LIVE_FX, {"spy_source": "alpaca", "ftse_source": "yahoo_finance"})
    assert result["status"] == "degraded"
    assert "computed from alpaca" in result["details"]["reason"]


def test_both_failing_is_unhealthy():
    result = _check(CONSTANT_FX, FAILED_REGIME)
    assert result["status"] == "unhealthy"
    assert result["details"]["accessible"] is False


def test_detailed_health_carries_the_yahoo_check():
    with patch.object(health_service, "_yahoo_finance_check",
                      return_value={"status": "degraded", "details": {"reason": "x"}}), \
         patch.object(health_service, "get_portfolio", return_value={"id": 1}), \
         patch.object(health_service, "get_settings", return_value=[{"k": 1}]):
        result = health_service.get_detailed_health()
    assert result["checks"]["yahooFinance"] == {"status": "degraded", "details": {"reason": "x"}}
    assert result["status"] == "degraded"
