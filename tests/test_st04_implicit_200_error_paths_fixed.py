"""
ST-04 (BLG-SEC-25, EPIC-02, v8.0): Raw exception text leaked in 16(+1)
implicit-HTTP-200 error paths in backend/main.py.

Covers: 17 call sites in backend/main.py where an `except Exception` block
previously returned a plain dict (implicit HTTP 200) instead of raising or
returning an explicit error status. Each is now fixed to return HTTP 500
(via JSONResponse) with the full exception logged server-side
(traceback.print_exc()) and only a generic message reaching the client.

Distinct from tests/test_main_500_no_raw_exception_text.py (ST-08, BLG-SEC-13,
v7.10), which covered a different, already-fixed set of paths that were
already returning explicit 500s but leaking raw exception text in the
message. This story's bug is the missing status code itself (implicit 200),
not the message content of an already-explicit 500.

Two endpoints (`/health`, `/health/detailed`) are exempt from the canonical
`{status, message}` error envelope per
`docs/specs/api_contracts/conventions.md` §11/§13.3 — they still must return
HTTP 500 (not implicit 200) and must not leak raw exception text, but their
response shape may differ from the standard envelope. `/test/endpoints` was
originally covered here too, but that coverage exercised a dead-code
duplicate handler in `main.py` that was shadowed by (and behaviourally
identical in intent to) `backend/routers/test.py`'s own route; the duplicate
was removed in ST-24 (BLG-BE-81, EPIC-05, v8.2) and this test removed with it.

CI-safe: no live DB or network connections — TestClient(app) with the
session-scoped database stub; underlying service functions are mocked to
raise directly.
"""

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)

_SENSITIVE_DETAIL = "psycopg2.OperationalError: password authentication failed for user 'admin' at /secret/internal/path.py"


class TestCanonicalEnvelopeErrorPaths:
    """Endpoints that must return the standard {status, message} 500 envelope."""

    def test_get_settings_500_returns_generic_message(self):
        with patch("main.get_settings", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/settings")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_get_portfolio_500_returns_generic_message(self):
        with patch("main.get_portfolio_summary", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/portfolio")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_positions_analyze_500_returns_generic_message(self):
        with patch("main.analyze_positions", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/positions/analyze")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_nightly_stop_update_500_returns_generic_message(self):
        with patch("main.run_nightly_trailing_stop_update", side_effect=RuntimeError(_SENSITIVE_DETAIL)), \
             patch("main.record_nightly_job"):
            resp = CLIENT.post("/positions/nightly-stop-update")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_risk_off_alerts_500_returns_generic_message(self):
        with patch("main.run_nightly_risk_off_alerts", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.post("/positions/risk-off-alerts")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_rebalance_exit_500_returns_generic_message(self):
        with patch("main.generate_rebalance_exit_signals", side_effect=RuntimeError(_SENSITIVE_DETAIL)), \
             patch("main.record_nightly_job"):
            resp = CLIENT.post("/signals/rebalance-exit")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_portfolio_history_500_returns_generic_message(self):
        with patch("main.get_performance_history", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/portfolio/history")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_cash_transactions_500_returns_generic_message(self):
        with patch("main.get_transaction_history", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/cash/transactions")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_cash_summary_500_returns_generic_message(self):
        with patch("main.get_cash_summary", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/cash/summary")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_trades_500_returns_generic_message(self):
        with patch("main.get_trade_history_with_stats", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/trades")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_reports_tax_year_500_returns_generic_message(self):
        with patch("main.get_tax_year_report", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/reports/tax-year", params={"year": 2026})
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_market_status_500_returns_generic_message(self):
        with patch("main.check_market_regime", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/market/status")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_health_database_500_returns_generic_message(self):
        with patch("main.get_db_size_info", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/health/database")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}

    def test_health_scheduler_500_returns_generic_message(self):
        with patch("main.get_scheduler_health", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/health/scheduler")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}


class TestHealthExemptEnvelopeErrorPaths:
    """
    /health, /health/detailed are exempt from the standard {status, message}
    envelope (conventions.md §11/§13.3), but must still return HTTP 500
    (not implicit 200) with no raw exception text leaked.
    """

    def test_health_500_returns_custom_shape_no_leak(self):
        with patch("main.get_operational_health", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/health")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {
            "status": "error",
            "db": "error",
            "last_market_status_check": None,
            "last_alert_evaluation": None,
        }

    def test_health_detailed_500_returns_generic_message(self):
        with patch("main.get_detailed_health", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/health/detailed")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body == {"status": "error", "message": "Internal server error"}


class TestExistingSuccessAndValueErrorPathsUnchanged:
    """Confirm the fix did not disturb existing 200 success shapes or 4xx ValueError paths."""

    def test_get_settings_success_path_unchanged(self):
        with patch("main.get_settings", return_value=[]):
            resp = CLIENT.get("/settings")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok", "data": []}

    def test_get_portfolio_value_error_still_returns_404(self):
        with patch("main.get_portfolio_summary", side_effect=ValueError("Portfolio not found")):
            resp = CLIENT.get("/portfolio")
        assert resp.status_code == 404
        assert resp.json().get("detail") == "Portfolio not found"


if __name__ == "__main__":
    import unittest
    unittest.main()
