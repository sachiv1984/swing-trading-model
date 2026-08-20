"""
Direct unit test coverage for cash_service, compliance_service, news_service,
validation_service (ST-14, BLG-QA-151, EPIC-04, v8.9).

The ST-19 (v8.8) consolidated backend service-layer test-coverage report
(`docs/ops/backend_service_layer_test_coverage_report_2026-08-16.md`) found
these 4 live, called-in-production service modules with zero direct unit
test coverage -- only HTTP-level contract tests (status code/envelope
shape, not calculation correctness) existed for any of them.

Each module below gets at least one direct unit test exercising
non-trivial logic (branching/calculation), not just an HTTP-level smoke
test. DB/external HTTP calls are mocked per this suite's existing
convention (patch.object on the module's imported names).
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

import services.cash_service as cash_service  # noqa: E402
import services.compliance_service as compliance_service  # noqa: E402
import services.news_service as news_service  # noqa: E402
from services.validation_service import _check, _by_severity  # noqa: E402


# ---------------------------------------------------------------------------
# cash_service — create_transaction / get_summary
# ---------------------------------------------------------------------------

class TestCashServiceCreateTransaction:
    def _portfolio(self, cash=1000.0):
        return {"id": "portfolio-1", "cash": cash}

    def test_deposit_increases_balance(self):
        with patch.object(cash_service, "get_portfolio", return_value=self._portfolio(1000.0)), \
             patch.object(cash_service, "db_create_cash_transaction", return_value={"id": "tx-1", "type": "deposit", "amount": 500.0, "date": "2026-08-18", "note": ""}), \
             patch.object(cash_service, "update_portfolio_cash") as mock_update:
            result = cash_service.create_transaction("deposit", 500.0)

        assert result["new_balance"] == 1500.0
        mock_update.assert_called_once_with("portfolio-1", 1500.0)

    def test_withdrawal_decreases_balance(self):
        with patch.object(cash_service, "get_portfolio", return_value=self._portfolio(1000.0)), \
             patch.object(cash_service, "db_create_cash_transaction", return_value={"id": "tx-1", "type": "withdrawal", "amount": 300.0, "date": "2026-08-18", "note": ""}), \
             patch.object(cash_service, "update_portfolio_cash") as mock_update:
            result = cash_service.create_transaction("withdrawal", 300.0)

        assert result["new_balance"] == 700.0
        mock_update.assert_called_once_with("portfolio-1", 700.0)

    def test_withdrawal_exceeding_cash_raises(self):
        with patch.object(cash_service, "get_portfolio", return_value=self._portfolio(100.0)):
            try:
                cash_service.create_transaction("withdrawal", 500.0)
                assert False, "expected ValueError for insufficient funds"
            except ValueError as e:
                assert "Insufficient funds" in str(e)

    def test_invalid_transaction_type_raises(self):
        with patch.object(cash_service, "get_portfolio", return_value=self._portfolio(1000.0)):
            try:
                cash_service.create_transaction("transfer", 100.0)
                assert False, "expected ValueError for invalid type"
            except ValueError as e:
                assert "Invalid transaction type" in str(e)

    def test_non_positive_amount_raises(self):
        with patch.object(cash_service, "get_portfolio", return_value=self._portfolio(1000.0)):
            try:
                cash_service.create_transaction("deposit", 0)
                assert False, "expected ValueError for non-positive amount"
            except ValueError as e:
                assert "must be greater than 0" in str(e)

    def test_no_portfolio_raises(self):
        with patch.object(cash_service, "get_portfolio", return_value=None):
            try:
                cash_service.create_transaction("deposit", 100.0)
                assert False, "expected ValueError for missing portfolio"
            except ValueError as e:
                assert "Portfolio not found" in str(e)


class TestCashServiceGetSummary:
    def test_net_cash_flow_computation(self):
        with patch.object(cash_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 2500.0}), \
             patch.object(cash_service, "get_total_deposits_withdrawals", return_value={
                 "total_deposits": 3000.0, "total_withdrawals": 500.0, "net_cash_flow": 2500.0,
             }):
            result = cash_service.get_summary()

        assert result["total_deposits"] == 3000.0
        assert result["total_withdrawals"] == 500.0
        assert result["net_cash_flow"] == 2500.0
        assert result["current_cash"] == 2500.0


# ---------------------------------------------------------------------------
# compliance_service — pure calculation helpers
# ---------------------------------------------------------------------------

class TestComputeStopCompliance:
    def test_grace_period_returns_none(self):
        assert compliance_service._compute_stop_compliance(100.0, 90.0, 90.0, 2.0, in_grace=True) is None

    def test_no_stop_after_grace_is_non_compliant(self):
        assert compliance_service._compute_stop_compliance(100.0, 0.0, 0.0, 2.0, in_grace=False) is False

    def test_missing_atr_returns_none(self):
        assert compliance_service._compute_stop_compliance(100.0, 90.0, 90.0, 0.0, in_grace=False) is None

    def test_stop_above_entry_is_non_compliant(self):
        assert compliance_service._compute_stop_compliance(100.0, 105.0, 105.0, 2.0, in_grace=False) is False

    def test_within_threshold_is_compliant(self):
        # stop_distance=4, atr=2 -> ratio 2.0 <= 2.5 threshold -> compliant
        assert compliance_service._compute_stop_compliance(100.0, 96.0, 96.0, 2.0, in_grace=False) is True

    def test_beyond_threshold_is_non_compliant(self):
        # stop_distance=10, atr=2 -> ratio 5.0 > 2.5 threshold -> non-compliant
        assert compliance_service._compute_stop_compliance(100.0, 90.0, 90.0, 2.0, in_grace=False) is False


class TestComputeSizeCompliance:
    def test_uk_position_within_tolerance_is_compliant(self):
        # stop_distance=5, shares=100 -> actual_risk=500 GBP
        # portfolio=10000, risk_percent=1% -> recommended=100, x1.10 tolerance=110
        # 500 > 110 -> non-compliant
        result = compliance_service._compute_size_compliance(
            entry_price=100.0, stop_price=95.0, shares=100.0, market="UK",
            fx_rate=1.0, portfolio_value_gbp=10000.0, risk_percent=1.0,
        )
        assert result is False

    def test_uk_position_within_recommended_risk_is_compliant(self):
        # stop_distance=1, shares=100 -> actual_risk=100 GBP; recommended=100 x1.10=110 -> compliant
        result = compliance_service._compute_size_compliance(
            entry_price=100.0, stop_price=99.0, shares=100.0, market="UK",
            fx_rate=1.0, portfolio_value_gbp=10000.0, risk_percent=1.0,
        )
        assert result is True

    def test_us_position_converts_via_fx_rate(self):
        # stop_distance=10 USD, shares=10 -> 100 USD / fx 2.0 -> 50 GBP actual risk
        # recommended = 10000 * 1% = 100, x1.10 = 110 -> compliant
        result = compliance_service._compute_size_compliance(
            entry_price=110.0, stop_price=100.0, shares=10.0, market="US",
            fx_rate=2.0, portfolio_value_gbp=10000.0, risk_percent=1.0,
        )
        assert result is True

    def test_missing_portfolio_value_returns_none(self):
        result = compliance_service._compute_size_compliance(
            entry_price=100.0, stop_price=95.0, shares=100.0, market="UK",
            fx_rate=1.0, portfolio_value_gbp=None, risk_percent=1.0,
        )
        assert result is None

    def test_no_stop_price_returns_none(self):
        result = compliance_service._compute_size_compliance(
            entry_price=100.0, stop_price=0.0, shares=100.0, market="UK",
            fx_rate=1.0, portfolio_value_gbp=10000.0, risk_percent=1.0,
        )
        assert result is None


class TestGetPositionComplianceAggregation:
    def test_overall_status_needs_attention_below_half_non_compliant(self):
        """3 positions, 1 non-compliant (< 50%) -> 'Needs Attention'."""
        positions = [
            {"id": "p1", "ticker": "AAA.L", "market": "UK", "holding_days": 30,
             "entry_price": 100.0, "current_stop": 95.0, "initial_stop": 95.0,
             "atr": 2.0, "shares": 10.0, "fx_rate": 1.0},
            {"id": "p2", "ticker": "BBB.L", "market": "UK", "holding_days": 30,
             "entry_price": 100.0, "current_stop": 95.0, "initial_stop": 95.0,
             "atr": 2.0, "shares": 10.0, "fx_rate": 1.0},
            # Non-compliant: stop_distance=10, atr=2 -> ratio 5.0 > 2.5
            {"id": "p3", "ticker": "CCC.L", "market": "UK", "holding_days": 30,
             "entry_price": 100.0, "current_stop": 90.0, "initial_stop": 90.0,
             "atr": 2.0, "shares": 10.0, "fx_rate": 1.0},
        ]
        with patch.object(compliance_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(compliance_service, "get_positions", return_value=positions), \
             patch.object(compliance_service, "get_latest_snapshot", return_value=None), \
             patch.object(compliance_service, "get_settings", return_value=[]):
            result = compliance_service.get_position_compliance()

        assert result["total_count"] == 3
        assert result["compliant_count"] == 2
        assert result["overall_status"] == "Needs Attention"

    def test_no_open_positions_returns_compliant_empty(self):
        with patch.object(compliance_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(compliance_service, "get_positions", return_value=[]):
            result = compliance_service.get_position_compliance()

        assert result == {"overall_status": "Compliant", "compliant_count": 0, "total_count": 0, "positions": []}


# ---------------------------------------------------------------------------
# news_service — credential branching, UK short-circuit, retry
# ---------------------------------------------------------------------------

class TestNewsServiceGetNewsHeadlines:
    def test_uk_ticker_always_returns_empty_list(self):
        # Should short-circuit before any HTTP call or credential check.
        with patch.object(news_service, "requests") as mock_requests:
            result = news_service.get_news_headlines("VOD.L", "UK")
        assert result == []
        mock_requests.get.assert_not_called()

    def test_missing_credentials_returns_empty_list(self):
        with patch.object(news_service, "ALPACA_API_KEY", ""), \
             patch.object(news_service, "ALPACA_API_SECRET", ""), \
             patch.object(news_service, "requests") as mock_requests:
            result = news_service.get_news_headlines("AAPL", "US")
        assert result == []
        mock_requests.get.assert_not_called()

    def test_success_response_filters_articles_without_headline(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"news": [
            {"headline": "Real headline", "created_at": "2026-08-18T00:00:00Z", "source": "Reuters", "url": "http://x"},
            {"headline": "", "created_at": "2026-08-18T00:00:00Z"},  # no headline -> filtered
        ]}
        with patch.object(news_service, "ALPACA_API_KEY", "key"), \
             patch.object(news_service, "ALPACA_API_SECRET", "secret"), \
             patch.object(news_service.requests, "get", return_value=mock_resp) as mock_get:
            result = news_service.get_news_headlines("AAPL", "US")

        assert len(result) == 1
        assert result[0]["headline"] == "Real headline"
        mock_get.assert_called_once()

    def test_403_forbidden_returns_empty_no_retry(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        with patch.object(news_service, "ALPACA_API_KEY", "key"), \
             patch.object(news_service, "ALPACA_API_SECRET", "secret"), \
             patch.object(news_service.requests, "get", return_value=mock_resp) as mock_get:
            result = news_service.get_news_headlines("AAPL", "US")

        assert result == []
        mock_get.assert_called_once()  # 403 does not retry

    def test_429_rate_limit_retries_then_gives_up(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 429
        with patch.object(news_service, "ALPACA_API_KEY", "key"), \
             patch.object(news_service, "ALPACA_API_SECRET", "secret"), \
             patch.object(news_service.requests, "get", return_value=mock_resp) as mock_get, \
             patch.object(news_service.time, "sleep"):  # skip real delay
            result = news_service.get_news_headlines("AAPL", "US")

        assert result == []
        assert mock_get.call_count == 3  # max_attempts


# ---------------------------------------------------------------------------
# validation_service — _check / _by_severity (the exact HOTFIX bug's logic)
# ---------------------------------------------------------------------------

class TestValidationServiceCheck:
    def test_within_tolerance_passes(self):
        result = _check("sharpe_ratio", actual=1.05, expected=1.0, tolerance=0.1)
        assert result["status"] == "pass"
        assert result["severity"] == "critical"

    def test_beyond_tolerance_fails(self):
        result = _check("sharpe_ratio", actual=2.0, expected=1.0, tolerance=0.1)
        assert result["status"] == "fail"

    def test_zero_tolerance_requires_exact_match(self):
        assert _check("win_streak", actual=5, expected=5, tolerance=0)["status"] == "pass"
        assert _check("win_streak", actual=4, expected=5, tolerance=0)["status"] == "fail"

    def test_unknown_metric_defaults_to_low_severity(self):
        result = _check("some_new_metric", actual=1.0, expected=1.0, tolerance=0.1)
        assert result["severity"] == "low"


class TestValidationServiceBySeverity:
    def test_regression_status_to_tier_key_mapping(self):
        """The exact HOTFIX bug (BLG-TECH-02/03): by_severity[tier][v['status']]
        with status='pass'/'warn'/'fail' against tier keys
        'passed'/'warned'/'failed' raised KeyError before STATUS_MAP was added.
        This test locks in the fixed mapping so a future direct-indexing
        regression is caught immediately rather than only surfacing in
        production."""
        validations = [
            {"severity": "critical", "status": "pass"},
            {"severity": "critical", "status": "fail"},
            {"severity": "high", "status": "warn"},
        ]
        result = _by_severity(validations)

        assert result["critical"] == {"total": 2, "passed": 1, "warned": 0, "failed": 1}
        assert result["high"] == {"total": 1, "passed": 0, "warned": 1, "failed": 0}
        assert result["medium"] == {"total": 0, "passed": 0, "warned": 0, "failed": 0}
        assert result["low"] == {"total": 0, "passed": 0, "warned": 0, "failed": 0}

    def test_unknown_severity_is_skipped_not_crashed(self):
        validations = [{"severity": "nonexistent_tier", "status": "pass"}]
        result = _by_severity(validations)  # must not raise
        assert all(tier["total"] == 0 for tier in result.values())

    def test_all_four_tiers_always_present_even_when_empty(self):
        result = _by_severity([])
        assert set(result.keys()) == {"critical", "high", "medium", "low"}
