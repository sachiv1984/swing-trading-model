"""
Router error-envelope conformance tests (ST-08, EPIC-02, v8.3, BLG-BE-69).

Spot-checks a representative error path in each of the 17 routers named in
BLG-BE-69's acceptance criteria, confirming each now returns the canonical
`{"status": "error", "message": "..."}` envelope (docs/specs/api_contracts/
conventions.md §13) at the correct HTTP status code, instead of FastAPI's
default `{"detail": "..."}` shape. Does not re-verify every one of the ~90
individual `raise HTTPException` call sites touched by this story — the fix
is a single mechanical pattern (translate at the router boundary rather than
let HTTPException reach FastAPI's default handler) applied identically
everywhere; see docs/specs/api_contracts/backend_engineering_patterns.md
§Error-response envelope conformance for the full audit this story resolves.

Success-path shapes are explicitly NOT covered here — out of this story's
scope (some routers, e.g. screener.py/news.py, use a pre-existing `{"ok": ...}`
success shape; this story only touches error paths).

CI-safe: no live DB or network connections — TestClient(app) with per-test
mocks; database stub evicted so the real database.py module loads (same
pattern as test_api_contracts.py), individual functions patched per test.
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)


def _assert_canonical_error(resp, status_code):
    assert resp.status_code == status_code
    body = resp.json()
    assert body.get("status") == "error"
    assert isinstance(body.get("message"), str) and body["message"]
    assert "detail" not in body


class TestAlertsEnvelope:
    @patch("routers.alerts.get_portfolio", return_value=None)
    def test_alert_rules_500_when_no_portfolio(self, _):
        resp = CLIENT.get("/alerts/rules")
        _assert_canonical_error(resp, 500)


class TestAnalyticsEnvelope:
    def test_tag_performance_400_when_no_tags(self):
        resp = CLIENT.get("/analytics/tag-performance", params={"tags": "  , ,"})
        _assert_canonical_error(resp, 400)


class TestDigestEnvelope:
    def test_si05_send_401_when_unauthorized(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "test-secret")
        resp = CLIENT.post("/digest/si05/send")
        _assert_canonical_error(resp, 401)
        monkeypatch.delenv("API_KEY", raising=False)


class TestAiEnvelope:
    def test_journal_summary_422_when_no_selector(self):
        resp = CLIENT.post("/ai/journal-summary", json={})
        _assert_canonical_error(resp, 422)


class TestPaperTradingEnvelope:
    @patch("routers.paper_trading.get_paper_positions", side_effect=RuntimeError("Alpaca unavailable"))
    def test_paper_positions_500_on_exception(self, _):
        resp = CLIENT.get("/portfolio/paper-positions")
        _assert_canonical_error(resp, 500)


class TestPlanVsRealityEnvelope:
    @patch(
        "routers.plan_vs_reality.get_plan_vs_reality_for_trade",
        side_effect=ValueError("No trade plan found for trade x"),
    )
    def test_plan_vs_reality_404_when_no_plan(self, _):
        resp = CLIENT.get("/trades/some-id/plan-vs-reality")
        _assert_canonical_error(resp, 404)


class TestPortfolioSizeEnvelope:
    @patch("routers.portfolio_size.size_position", side_effect=ValueError("bad input"))
    def test_size_400_on_value_error(self, _):
        resp = CLIENT.post(
            "/portfolio/size",
            json={"entry_price": 10, "stop_price": 9, "risk_percent": 1, "market": "UK"},
        )
        _assert_canonical_error(resp, 400)


class TestRedFlagJournalEnvelope:
    @patch("routers.red_flag_journal._ensure_schema_once", return_value=None)
    @patch("routers.red_flag_journal.get_red_flag_events", side_effect=RuntimeError("db down"))
    def test_red_flag_journal_500_on_exception(self, _mock_get, _mock_schema):
        resp = CLIENT.get("/portfolio/red-flag-journal")
        _assert_canonical_error(resp, 500)


class TestSavedFiltersEnvelope:
    @patch("routers.saved_filters.get_portfolio", return_value=None)
    def test_saved_filters_500_when_no_portfolio(self, _):
        resp = CLIENT.get("/saved-filters")
        _assert_canonical_error(resp, 500)


class TestScreenerEnvelope:
    def test_screener_results_400_on_limit_too_high(self):
        resp = CLIENT.get("/screener/results", params={"limit": 500})
        _assert_canonical_error(resp, 400)


class TestStrategyBenchmarkEnvelope:
    @patch("routers.strategy_benchmark.database.ensure_backtest_tables", side_effect=RuntimeError("db down"))
    def test_benchmark_summary_500_on_exception(self, _):
        resp = CLIENT.get("/strategy/benchmark/summary")
        _assert_canonical_error(resp, 500)


class TestTickerUniverseEnvelope:
    def test_list_tickers_400_on_bad_market(self):
        resp = CLIENT.get("/ticker-universe", params={"market": "XX"})
        _assert_canonical_error(resp, 400)


class TestTradePlansEnvelope:
    @patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
    @patch("routers.trade_plans.get_trade_plan_by_id", return_value=None)
    @patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"})
    def test_get_plan_404_when_not_found(self, _get_p, _get_plan, _ensure):
        resp = CLIENT.get("/trade-plans/missing-id")
        _assert_canonical_error(resp, 404)


class TestTradesExportEnvelope:
    @patch("routers.trades_export.get_portfolio", return_value=None)
    def test_export_csv_500_when_no_portfolio(self, _):
        resp = CLIENT.get("/trades/export/csv")
        _assert_canonical_error(resp, 500)


class TestValidationEnvelope:
    @patch("routers.validation.ValidationService")
    def test_validate_calculations_500_on_exception(self, mock_service_cls):
        mock_service_cls.return_value.validate_all.side_effect = RuntimeError("boom")
        resp = CLIENT.post("/validate/calculations")
        _assert_canonical_error(resp, 500)


class TestWatchlistEnvelope:
    @patch("routers.watchlist.get_portfolio", return_value=None)
    def test_watchlist_500_when_no_portfolio(self, _):
        resp = CLIENT.get("/watchlist")
        _assert_canonical_error(resp, 500)


class TestEarningsEnvelope:
    @patch("routers.earnings.get_earnings", side_effect=RuntimeError("yfinance down"))
    def test_earnings_500_on_exception(self, _):
        resp = CLIENT.get("/earnings/AAPL")
        _assert_canonical_error(resp, 500)


class TestNewsEnvelope:
    @patch("routers.news.get_news_headlines", side_effect=RuntimeError("alpaca down"))
    def test_news_500_on_exception(self, _):
        resp = CLIENT.get("/news/AAPL")
        _assert_canonical_error(resp, 500)
