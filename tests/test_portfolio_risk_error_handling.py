"""
ST-01 (BLG-BE-68, EPIC-01, v7.10): Errors masked as HTTP 200 in portfolio_risk.py.

Covers:
- GET /portfolio/drawdown-status, /concentration-status, /sector-weights,
  /gate-metrics all return HTTP 500 with the canonical {status, message}
  envelope when the underlying computation raises, instead of silently
  returning HTTP 200 with an embedded "error" field.
- Existing 200-path success shapes unchanged (spot-checked for gate-metrics'
  no-portfolio branch, which does not raise).

CI-safe: no live DB or network connections.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from routers import portfolio_risk


class TestPortfolioRiskErrorEnvelope(unittest.TestCase):

    def _assert_500_envelope(self, response, expected_message_substr=None):
        self.assertIsInstance(response, portfolio_risk.JSONResponse)
        self.assertEqual(response.status_code, 500)
        import json
        body = json.loads(response.body)
        self.assertEqual(body["status"], "error")
        self.assertIn("message", body)
        if expected_message_substr:
            self.assertIn(expected_message_substr, body["message"])

    def test_drawdown_status_returns_500_on_internal_error(self):
        with patch.object(
            portfolio_risk, "_get_portfolio_heat_and_positions",
            side_effect=RuntimeError("boom-drawdown"),
        ):
            response = portfolio_risk.get_drawdown_status()
        self._assert_500_envelope(response, "boom-drawdown")

    def test_concentration_status_returns_500_on_internal_error(self):
        with patch.object(
            portfolio_risk, "_get_portfolio_heat_and_positions",
            side_effect=RuntimeError("boom-concentration"),
        ):
            response = portfolio_risk.get_concentration_status()
        self._assert_500_envelope(response, "boom-concentration")

    def test_sector_weights_returns_500_on_internal_error(self):
        with patch.object(
            portfolio_risk, "get_portfolio",
            side_effect=RuntimeError("boom-sector-weights"),
        ):
            response = portfolio_risk.get_sector_weights()
        self._assert_500_envelope(response, "boom-sector-weights")

    def test_gate_metrics_returns_500_on_internal_error(self):
        with patch.object(
            portfolio_risk, "get_portfolio",
            side_effect=RuntimeError("boom-gate-metrics"),
        ):
            response = portfolio_risk.get_gate_metrics_endpoint()
        self._assert_500_envelope(response, "boom-gate-metrics")

    def test_gate_metrics_no_portfolio_success_path_unchanged(self):
        # Existing 200-path (no portfolio row) must still return the plain
        # dict success shape, not an error envelope.
        with patch.object(portfolio_risk, "get_portfolio", return_value=None):
            response = portfolio_risk.get_gate_metrics_endpoint()
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["data"]["closed_trades_count"], 0)


if __name__ == "__main__":
    unittest.main()
