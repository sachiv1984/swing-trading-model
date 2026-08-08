"""
API Contract Tests — test_api_contracts.py

FastAPI TestClient tests for all application routes, organised by tag group
matching docs/reference/openapi.yaml.

Coverage goal: every GET endpoint (and key POST/PUT/DELETE routes) must
return the expected HTTP status code and, where applicable, the standard
{"status": "ok", "data": ...} response envelope.

CI-safe: all database calls, external HTTP calls (yfinance, Alpaca), and
live pricing are mocked via unittest.mock.patch. No live DB or network
connections are made.

Patch target rule (Python import binding): patch at the import site, not the
definition site. If a module does `from database import X`, patch `module.X`.

Spec source: docs/reference/openapi.yaml + docs/specs/api_contracts/
"""

import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Earlier test files (e.g. test_service_coverage.py) inject a stub into
# sys.modules["database"] that predates EPIC-01 and lacks trade_plan functions.
# Evict it here so Python loads the real backend/database.py instead.
sys.modules.pop("database", None)

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)

# ---------------------------------------------------------------------------
# Shared mock data
# ---------------------------------------------------------------------------

MOCK_PORTFOLIO = {
    "id": "portfolio-test-001",
    "cash": 10000.0,
    "initial_value": 50000.0,
    "last_updated": "2026-04-30T00:00:00",
}

MOCK_SETTINGS = {
    "id": "settings-001",
    "portfolio_id": "portfolio-test-001",
    "risk_per_trade": 1.0,
    "max_portfolio_heat": 10.0,
    "default_market": "UK",
}

MOCK_SIGNAL = {
    "id": "sig-001",
    "portfolio_id": "portfolio-test-001",
    "ticker": "NVDA",
    "market": "US",
    "direction": "long",
    "signal_date": date(2026, 4, 28),
    "status": "active",
    "rank": 1,
    "atr": 12.5,
    "entry_price": 450.0,
    "stop_price": 425.0,
    "r_target": 2.5,
}

MOCK_REGIME = {
    "spy_risk_on": True,
    "ftse_risk_on": True,
    "spy_price": 520.0,
    "spy_ma200": 490.0,
    "ftse_price": 8100.0,
    "ftse_ma200": 7800.0,
}

MOCK_CASH_SUMMARY = {
    "total_deposits": 50000.0,
    "total_withdrawals": 0.0,
    "net_deposits": 50000.0,
    "current_cash": 10000.0,
}

MOCK_PORTFOLIO_SUMMARY = {
    "total_value": 52000.0,
    "cash": 10000.0,
    "positions": [],
    "position_risks": [],
    "open_positions_count": 0,
    "portfolio_heat": 0.0,
    "drawdown": {},
    "net_deposits": 50000.0,
    "initial_value": 50000.0,
}

MOCK_TRADE_PLAN = {
    "id": "plan-001",
    "portfolio_id": "portfolio-test-001",
    "ticker": "AAPL",
    "market": "US",
    "status": "draft",
    "setup_thesis": "Breakout above resistance",
    "entry_rationale": "Volume confirmed",
    "checklist_completed": False,
    "checklist_items": [],
    "created_at": "2026-04-30T00:00:00",
    "updated_at": "2026-04-30T00:00:00",
    "r_target": 2.5,
    "regime_context_at_entry": None,
    "early_exit_conditions": None,
    "confirmation_criteria": None,
    "position_id": None,
}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _ok(r, status_code=200):
    """Assert HTTP status and standard envelope."""
    assert r.status_code == status_code, (
        f"Expected {status_code}, got {r.status_code}: {r.text[:300]}"
    )
    body = r.json()
    assert body.get("status") == "ok", f"Expected status=ok, got: {body}"
    return body


def _mock_conn():
    """Return a mock psycopg2 connection/cursor for raw-SQL endpoints."""
    cur = MagicMock()
    cur.fetchall.return_value = []
    cur.fetchone.return_value = None
    cur.__enter__ = lambda s: s
    cur.__exit__ = MagicMock(return_value=False)
    conn = MagicMock()
    conn.cursor.return_value = cur
    conn.__enter__ = lambda s: s
    conn.__exit__ = MagicMock(return_value=False)
    return conn


# ---------------------------------------------------------------------------
# 1. Core / Health
# ---------------------------------------------------------------------------

class TestCoreEndpoints(unittest.TestCase):

    def test_root_returns_ok(self):
        r = CLIENT.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    @patch("services.health_service.get_basic_health",
           return_value={"status": "healthy"})
    def test_health_returns_200(self, _):
        r = CLIENT.get("/health")
        assert r.status_code == 200

    @patch("services.health_service.get_detailed_health",
           return_value={"overall": "healthy", "checks": []})
    def test_health_detailed_returns_200(self, _):
        r = CLIENT.get("/health/detailed")
        assert r.status_code == 200


# ---------------------------------------------------------------------------
# 2. Settings  (main.py imports get_settings from database)
# ---------------------------------------------------------------------------

class TestSettingsEndpoints(unittest.TestCase):

    @patch("main.get_settings", return_value=[MOCK_SETTINGS])
    def test_get_settings_returns_ok(self, _):
        body = _ok(CLIENT.get("/settings"))
        assert isinstance(body["data"], list)
        assert len(body["data"]) == 1

    @patch("main.get_settings", return_value=[])
    def test_get_settings_empty_returns_ok(self, _):
        body = _ok(CLIENT.get("/settings"))
        assert body["data"] == []


# ---------------------------------------------------------------------------
# 3. Portfolio  (main.py uses services.get_portfolio_summary)
# ---------------------------------------------------------------------------

class TestPortfolioEndpoints(unittest.TestCase):

    @patch("main.get_portfolio_summary", return_value=MOCK_PORTFOLIO_SUMMARY)
    def test_get_portfolio_returns_ok(self, _):
        body = _ok(CLIENT.get("/portfolio"))
        assert "data" in body

    # ST-25 (BLG-QA-135): the endpoint calls services.portfolio_service.get_performance_history(),
    # which internally calls get_portfolio() and get_portfolio_snapshots() bound in that module's
    # own namespace (from database import ...) — patching main.get_portfolio / database.get_portfolio_snapshots
    # (the definition/re-export sites) does not intercept those calls per this file's own "Patch
    # target rule" above. Fixed to patch at the actual import site.
    @patch("services.portfolio_service.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("services.portfolio_service.get_portfolio_snapshots", return_value=[])
    def test_get_portfolio_history_returns_ok(self, *_):
        r = CLIENT.get("/portfolio/history?days=30")
        assert r.status_code == 200

    @patch("routers.prospective_heat.get_portfolio_summary",
           return_value={"total_value": 52000.0, "position_risks": []})
    @patch("routers.prospective_heat.get_live_fx_rate", return_value=1.27)
    def test_prospective_heat_valid_inputs(self, *_):
        body = _ok(CLIENT.get(
            "/portfolio/prospective-heat"
            "?ticker=AAPL&shares=10&entry_price=180&stop_price=170&market=US&fx_rate=1.27"
        ))
        assert body["data"]["valid"] is True

    @patch("routers.prospective_heat.get_portfolio_summary",
           return_value={"total_value": 52000.0, "position_risks": []})
    def test_prospective_heat_stop_above_entry_invalid(self, _):
        body = _ok(CLIENT.get(
            "/portfolio/prospective-heat"
            "?ticker=AAPL&shares=10&entry_price=160&stop_price=180&market=US&fx_rate=1.27"
        ))
        assert body["data"]["valid"] is False


# ---------------------------------------------------------------------------
# 4. Positions  (main.py uses main.get_positions_with_prices)
# ---------------------------------------------------------------------------

class TestPositionEndpoints(unittest.TestCase):

    @patch("main.get_positions_with_prices", return_value=[])
    def test_get_positions_returns_ok(self, _):
        # /positions returns a raw list, not a {"status":"ok"} envelope
        r = CLIENT.get("/positions")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    @patch("main.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("main.get_available_tags", return_value=["momentum", "breakout"])
    def test_get_position_tags_returns_ok(self, *_):
        body = _ok(CLIENT.get("/positions/tags"))
        assert isinstance(body["data"], list)

    @patch("main.get_position_compliance", return_value=[])
    @patch("main.get_positions_with_prices", return_value=[])
    def test_get_positions_compliance_returns_ok(self, *_):
        r = CLIENT.get("/positions/compliance")
        assert r.status_code == 200

    @patch("main.mark_position_reviewed", return_value={"id": "pos-1", "last_reviewed_at": None})
    def test_mark_position_reviewed_returns_ok(self, _):
        # ST-04 (BLG-BE-61, v7.1) — endpoint now calls services.position_service
        # .mark_position_reviewed() (module-level import into main.py's
        # namespace), not database.mark_position_reviewed directly, so it
        # performs the same portfolio-ownership check as note/tags.
        body = _ok(CLIENT.patch("/positions/pos-1/mark-reviewed"))
        assert body["data"]["id"] == "pos-1"

    @patch("main.mark_position_reviewed", side_effect=ValueError("Position nonexistent-id not found"))
    def test_mark_position_reviewed_404_when_not_found(self, _):
        r = CLIENT.patch("/positions/nonexistent-id/mark-reviewed")
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# 5. Trades  (main.py uses main.get_trade_history_with_stats)
# ---------------------------------------------------------------------------

class TestTradeEndpoints(unittest.TestCase):

    @patch("main.get_trade_history_with_stats",
           return_value={"trades": [], "stats": {}})
    def test_get_trades_returns_ok(self, _):
        body = _ok(CLIENT.get("/trades"))
        assert "data" in body


# ---------------------------------------------------------------------------
# 6. Cash  (main.py uses main.get_transaction_history / main.get_cash_summary)
# ---------------------------------------------------------------------------

class TestCashEndpoints(unittest.TestCase):

    @patch("main.get_transaction_history", return_value=[])
    def test_get_cash_transactions_returns_ok(self, _):
        body = _ok(CLIENT.get("/cash/transactions"))
        assert isinstance(body["data"], list)

    @patch("main.get_cash_summary", return_value=MOCK_CASH_SUMMARY)
    def test_get_cash_summary_returns_ok(self, _):
        body = _ok(CLIENT.get("/cash/summary"))
        assert "net_deposits" in body["data"]


# ---------------------------------------------------------------------------
# 7. Signals & Market
# ---------------------------------------------------------------------------

class TestSignalAndMarketEndpoints(unittest.TestCase):

    @patch("main.get_signals", return_value=[MOCK_SIGNAL])
    def test_get_signals_returns_ok(self, _):
        # /signals returns a raw list, not a {"status":"ok"} envelope
        r = CLIENT.get("/signals")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    @patch("main.get_live_fx_rate", return_value=1.27)
    @patch("utils.pricing.check_market_regime", return_value=MOCK_REGIME)
    def test_market_status_returns_ok(self, _, __):
        body = _ok(CLIENT.get("/market/status"))
        assert "data" in body


# ---------------------------------------------------------------------------
# 8. Analytics  (router calls psycopg2 directly — patch at router level)
# ---------------------------------------------------------------------------

class TestAnalyticsEndpoints(unittest.TestCase):

    @patch("routers.analytics.psycopg2.connect")
    @patch("database.get_portfolio", return_value=MOCK_PORTFOLIO)
    def test_analytics_metrics_all_time(self, _, mock_connect):
        mock_connect.return_value = _mock_conn()
        assert CLIENT.get("/analytics/metrics?period=all_time").status_code == 200

    @patch("routers.analytics.psycopg2.connect")
    @patch("database.get_portfolio", return_value=MOCK_PORTFOLIO)
    def test_analytics_metrics_last_7_days(self, _, mock_connect):
        mock_connect.return_value = _mock_conn()
        assert CLIENT.get("/analytics/metrics?period=last_7_days").status_code == 200

    @patch("routers.analytics.psycopg2.connect")
    @patch("database.get_portfolio", return_value=MOCK_PORTFOLIO)
    def test_analytics_cohort(self, _, mock_connect):
        mock_connect.return_value = _mock_conn()
        assert CLIENT.get("/analytics/cohort?period=month").status_code == 200

    @patch("routers.analytics.psycopg2.connect")
    @patch("database.get_portfolio", return_value=MOCK_PORTFOLIO)
    def test_analytics_r_multiple_distribution(self, _, mock_connect):
        mock_connect.return_value = _mock_conn()
        assert CLIENT.get("/analytics/r-multiple-distribution").status_code == 200

    @patch("routers.analytics.psycopg2.connect")
    @patch("database.get_portfolio", return_value=MOCK_PORTFOLIO)
    def test_analytics_compliance_metrics(self, _, mock_connect):
        mock_connect.return_value = _mock_conn()
        assert CLIENT.get("/analytics/compliance-metrics").status_code == 200

    @patch("routers.analytics.psycopg2.connect")
    @patch("database.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("utils.pricing.get_current_price", return_value=None)
    def test_analytics_market_correlation(self, _, __, mock_connect):
        mock_connect.return_value = _mock_conn()
        assert CLIENT.get("/analytics/market-correlation").status_code == 200


# ---------------------------------------------------------------------------
# 9. Alerts & Notifications
#    router imports: from database import get_portfolio
#                    from services.alerts_service import get_alert_rules, ...
# ---------------------------------------------------------------------------

class TestAlertsEndpoints(unittest.TestCase):

    @patch("routers.alerts.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.alerts.get_alert_rules", return_value=[])
    def test_get_alert_rules_returns_ok(self, *_):
        assert CLIENT.get("/alerts/rules").status_code == 200

    @patch("routers.alerts.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.alerts.get_alert_history", return_value=[])
    def test_get_alert_history_returns_ok(self, *_):
        assert CLIENT.get("/alerts/history").status_code == 200

    @patch("routers.alerts.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.alerts.get_notifications",
           return_value={"notifications": [], "total": 0})
    def test_get_notifications_returns_ok(self, *_):
        assert CLIENT.get("/notifications").status_code == 200

    @patch("routers.alerts.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.alerts.get_notifications",
           return_value={"notifications": [], "total": 0})
    def test_get_notifications_forwards_since_days_and_read(self, mock_get_notifications, *_):
        # ST-02 (EPIC-02, v7.7, BLG-FE-114): since_days/read filter params
        resp = CLIENT.get("/notifications?since_days=7&read=true")
        assert resp.status_code == 200
        _, kwargs = mock_get_notifications.call_args
        assert kwargs.get("since_days") == 7
        assert kwargs.get("read") is True

    @patch("routers.alerts.get_portfolio", return_value=MOCK_PORTFOLIO)
    def test_get_notifications_rejects_non_positive_since_days(self, *_):
        assert CLIENT.get("/notifications?since_days=0").status_code == 400

    @patch("routers.alerts.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.alerts.get_preferences", return_value={})
    def test_get_notification_preferences_returns_ok(self, *_):
        assert CLIENT.get("/notifications/preferences").status_code == 200


# ---------------------------------------------------------------------------
# 10. Digest  (router calls psycopg2 directly)
# ---------------------------------------------------------------------------

class TestDigestEndpoints(unittest.TestCase):

    @patch("routers.digest.psycopg2.connect")
    @patch("database.get_portfolio", return_value=MOCK_PORTFOLIO)
    def test_get_digest_weekly_returns_200(self, _, mock_connect):
        mock_connect.return_value = _mock_conn()
        assert CLIENT.get("/digest/weekly").status_code == 200

    def test_post_digest_si05_send_returns_401_without_api_key(self):
        """ST-08 (BLG-BE-35): unauthenticated POST /digest/si05/send returns 401."""
        import os
        with patch.dict(os.environ, {"API_KEY": "test-secret"}):
            resp = CLIENT.post("/digest/si05/send")
        assert resp.status_code == 401

    @patch("routers.digest.send_si05_digest", return_value={"sent": True, "message_length": 100, "error": None})
    def test_post_digest_si05_send_returns_200_with_api_key(self, _):
        """ST-08 (BLG-BE-35): authenticated POST /digest/si05/send returns 200."""
        import os
        with patch.dict(os.environ, {"API_KEY": "test-secret"}):
            resp = CLIENT.post("/digest/si05/send", headers={"X-API-Key": "test-secret"})
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# 11. Ticker Universe
#     router imports: from services.ticker_universe_service import get_all_tickers, ...
# ---------------------------------------------------------------------------

class TestTickerUniverseEndpoints(unittest.TestCase):

    @patch("routers.ticker_universe.get_all_tickers",
           return_value=[{"ticker": "AAPL", "market": "US", "active": True}])
    def test_get_ticker_universe_returns_ok(self, _):
        body = _ok(CLIENT.get("/ticker-universe"))
        assert isinstance(body["data"], list)

    @patch("routers.ticker_universe._validate_ticker_yfinance", return_value=None)
    @patch("routers.ticker_universe.add_ticker",
           return_value={"ticker": "TSLA", "market": "US", "active": True})
    def test_post_ticker_universe_returns_ok(self, _add, _validate):
        # POST /ticker-universe returns 201
        assert CLIENT.post("/ticker-universe", json={"ticker": "TSLA", "market": "US"}).status_code == 201

    @patch("routers.ticker_universe.soft_delete_ticker", return_value=True)
    def test_delete_ticker_universe_returns_ok(self, _):
        assert CLIENT.delete("/ticker-universe/AAPL").status_code == 200


# ---------------------------------------------------------------------------
# 12. Screener
#     router imports: from services.screener_batch_service import run_screener, get_screener_results
# ---------------------------------------------------------------------------

class TestScreenerEndpoints(unittest.TestCase):

    @patch("routers.screener.get_screener_results",
           return_value={"results": [], "count": 0, "last_run_timestamp": None})
    def test_get_screener_results_returns_ok(self, _):
        assert CLIENT.get("/screener/results").status_code == 200

    @patch("routers.screener.run_screener",
           return_value={"run_id": "run-001", "status": "accepted"})
    def test_post_screener_run_accepts(self, _):
        assert CLIENT.post("/screener/run", json={}).status_code in (200, 202)


# ---------------------------------------------------------------------------
# 13. Reports
# ---------------------------------------------------------------------------

class TestReportsEndpoints(unittest.TestCase):

    @patch("services.reports_service.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("services.reports_service.get_positions", return_value=[])
    @patch("services.reports_service.get_trade_history_by_tax_year", return_value=[])
    def test_get_tax_year_report_returns_ok(self, *_):
        body = _ok(CLIENT.get("/reports/tax-year?year=2025"))
        assert "data" in body

    @patch("services.reports_service.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("services.reports_service.get_positions", return_value=[])
    @patch("services.reports_service.get_trade_history_by_tax_year", return_value=[])
    def test_get_tax_year_missing_param_returns_400(self, *_):
        assert CLIENT.get("/reports/tax-year").status_code == 400

    @patch("main.get_monthly_pnl_report", return_value={"months": [], "estimated_unrealised_pnl": None, "unrealised_note": "note"})
    @patch("main.get_arc5_compliance_summary", return_value=None)
    def test_get_monthly_pnl_returns_ok(self, *_):
        body = _ok(CLIENT.get("/reports/monthly-pnl"))
        assert "data" in body

    @patch("main.get_monthly_pnl_report", return_value={
        "months": [{"year": 2026, "month": 5, "realised_pnl_gbp": 100.0, "trade_count": 2}],
        "estimated_unrealised_pnl": 340.0,
        "unrealised_note": "note",
    })
    @patch("main.get_arc5_compliance_summary", return_value={
        "period_days": 30,
        "validation_pass_rate": 0.85,
        "override_count": 1,
        "red_flag_events_count": 3,
        "most_frequent_rule_breach": "sector_concentration",
    })
    def test_monthly_pnl_compliance_summary_present_when_data_available(self, *_):
        # AC-01/AC-02: compliance_summary section present with correct fields (ST-03, v4.7)
        body = _ok(CLIENT.get("/reports/monthly-pnl"))
        assert "compliance_summary" in body
        cs = body["compliance_summary"]
        assert cs["validation_pass_rate"] == 0.85
        assert cs["override_count"] == 1
        assert cs["red_flag_events_count"] == 3
        assert cs["most_frequent_rule_breach"] == "sector_concentration"

    @patch("main.get_monthly_pnl_report", return_value={"months": [], "estimated_unrealised_pnl": None, "unrealised_note": "note"})
    @patch("main.get_arc5_compliance_summary", return_value=None)
    def test_monthly_pnl_compliance_summary_absent_when_data_unavailable(self, *_):
        # AC-04: compliance_summary null when Arc 5 data unavailable (ST-03, v4.7)
        body = _ok(CLIENT.get("/reports/monthly-pnl"))
        assert body.get("compliance_summary") is None

    @patch("main.get_monthly_pnl_report", return_value={
        "months": [{"year": 2026, "month": 5, "realised_pnl_gbp": 100.0, "trade_count": 2}],
        "estimated_unrealised_pnl": 340.0,
        "unrealised_note": "Reflects current open positions at time of report generation.",
    })
    @patch("main.get_arc5_compliance_summary", return_value=None)
    def test_monthly_pnl_estimated_unrealised_pnl_present(self, *_):
        # ST-14 (BLG-FEAT-70, v7.0): estimated_unrealised_pnl/unrealised_note top-level, data unchanged
        body = _ok(CLIENT.get("/reports/monthly-pnl"))
        assert body["estimated_unrealised_pnl"] == 340.0
        assert "unrealised_note" in body
        assert body["data"] == [{"year": 2026, "month": 5, "realised_pnl_gbp": 100.0, "trade_count": 2}]

    @patch("main.get_monthly_pnl_report", return_value={
        "months": [{"year": 2026, "month": 5, "realised_pnl_gbp": 100.0, "trade_count": 2}],
        "estimated_unrealised_pnl": 340.0,
        "unrealised_note": "note",
    })
    def test_monthly_pnl_csv_format_returns_csv_download(self, *_):
        # ST-05 (EPIC-05, v7.8, BLG-FEAT-81): format=csv returns a CSV file download
        response = CLIENT.get("/reports/monthly-pnl?format=csv")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/csv")
        assert 'attachment; filename="monthly-pnl.csv"' in response.headers["content-disposition"]
        assert "Year,Month,Realised P&L (GBP),Trades" in response.text
        assert "2026,5,100.0,2" in response.text

    def test_monthly_pnl_invalid_format_returns_400(self):
        assert CLIENT.get("/reports/monthly-pnl?format=xml").status_code == 400


# ---------------------------------------------------------------------------
# 14. Trade Plans  (EPIC-01 — available after EPIC-01 merges into main)
#     router imports: from database import get_portfolio, create_trade_plan, ...
# ---------------------------------------------------------------------------

_TRADE_PLANS_AVAILABLE = CLIENT.get("/trade-plans").status_code != 404


@unittest.skipUnless(_TRADE_PLANS_AVAILABLE, "trade-plans route not yet on this branch (EPIC-01)")
class TestTradePlanEndpoints(unittest.TestCase):

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.get_trade_plans", return_value=[MOCK_TRADE_PLAN])
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    def test_list_trade_plans_returns_ok(self, *_):
        body = _ok(CLIENT.get("/trade-plans"))
        assert isinstance(body["data"], list)

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.get_trade_plans", return_value=[])
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    def test_list_trade_plans_status_filter(self, *_):
        body = _ok(CLIENT.get("/trade-plans?status=draft"))
        assert isinstance(body["data"], list)

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.create_trade_plan", return_value=MOCK_TRADE_PLAN)
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    @patch("routers.trade_plans.ensure_si02_trade_plans_columns", return_value=None)
    @patch("routers.trade_plans.ensure_strategy_version_at_entry_columns", return_value=None)
    @patch("routers.trade_plans.get_latest_snapshot", return_value={"total_value": 10000.00})
    @patch("routers.trade_plans.get_settings", return_value=[{"default_risk_percent": 1.5, "atr_multiplier_initial": 5.0, "atr_multiplier_trailing": 2.0, "min_hold_days": 10}])
    def test_create_trade_plan_returns_201(self, *_):
        r = CLIENT.post("/trade-plans", json={"ticker": "AAPL", "market": "US"})
        assert r.status_code == 201
        assert r.json()["status"] == "ok"

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.get_trade_plan_by_id", return_value=MOCK_TRADE_PLAN)
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    def test_get_trade_plan_by_id_returns_ok(self, *_):
        body = _ok(CLIENT.get("/trade-plans/plan-001"))
        assert body["data"]["id"] == "plan-001"

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.get_trade_plan_by_id", return_value=None)
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    def test_get_trade_plan_not_found_returns_404(self, *_):
        assert CLIENT.get("/trade-plans/nonexistent-id").status_code == 404

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.update_trade_plan",
           return_value={**MOCK_TRADE_PLAN, "status": "active"})
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    def test_update_trade_plan_returns_ok(self, *_):
        body = _ok(CLIENT.put("/trade-plans/plan-001", json={"status": "active"}))
        assert body["data"]["status"] == "active"

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.delete_trade_plan", return_value=True)
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    def test_delete_trade_plan_returns_ok(self, *_):
        body = _ok(CLIENT.delete("/trade-plans/plan-001"))
        assert body["message"] == "Trade plan deleted"

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.delete_trade_plan", return_value=False)
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    def test_delete_trade_plan_not_found_returns_404(self, *_):
        assert CLIENT.delete("/trade-plans/nonexistent-id").status_code == 404

    @patch("routers.trade_plans.get_portfolio", return_value=MOCK_PORTFOLIO)
    @patch("routers.trade_plans.get_trade_plans_by_position", return_value=[])
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    def test_list_plans_by_position_returns_ok(self, *_):
        body = _ok(CLIENT.get(
            "/trade-plans/by-position/00000000-0000-0000-0000-000000000000"
        ))
        assert isinstance(body["data"], list)


# ---------------------------------------------------------------------------
# 15. Validation
# ---------------------------------------------------------------------------

class TestValidationEndpoints(unittest.TestCase):

    def test_post_validate_calculations_returns_ok(self):
        r = CLIENT.post("/validate/calculations")
        assert r.status_code == 200


if __name__ == "__main__":
    unittest.main()
