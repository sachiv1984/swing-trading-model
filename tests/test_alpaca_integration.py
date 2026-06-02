"""
Integration tests for Alpaca US Market Data Integration (DS-05 — ST-06)

Covers:
- Alpaca bars fetch and parse
- US ticker routing to Alpaca via get_current_price
- Fallback to Yahoo Finance when Alpaca fails
- UK tickers never sent to Alpaca (Yahoo Finance only)
- ATR calculation routes US tickers through Alpaca
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


class TestAlpacaService(unittest.TestCase):

    def _mock_response(self, status_code=200, json_data=None):
        mock = MagicMock()
        mock.status_code = status_code
        mock.json.return_value = json_data or {}
        return mock

    @patch('services.alpaca_service.requests.get')
    def test_get_ohlcv_bars_success(self, mock_get):
        bars = [{"t": "2026-04-23T00:00:00Z", "o": 100, "h": 105, "l": 98, "c": 103, "v": 1000000}]
        mock_get.return_value = self._mock_response(200, {"bars": bars})

        from services.alpaca_service import get_ohlcv_bars
        with patch.dict(os.environ, {"APCA_API_KEY_ID": "key", "APCA_API_SECRET_KEY": "secret"}):
            import importlib
            import services.alpaca_service as alpaca_mod
            alpaca_mod.ALPACA_API_KEY = "key"
            alpaca_mod.ALPACA_API_SECRET = "secret"
            result = get_ohlcv_bars("NVDA")

        self.assertIsNotNone(result)
        self.assertEqual(result[0]["c"], 103)

    @patch('services.alpaca_service.requests.get')
    def test_get_ohlcv_bars_returns_none_on_403(self, mock_get):
        mock_get.return_value = self._mock_response(403, {})
        from services.alpaca_service import get_ohlcv_bars
        import services.alpaca_service as alpaca_mod
        alpaca_mod.ALPACA_API_KEY = "key"
        alpaca_mod.ALPACA_API_SECRET = "secret"
        result = get_ohlcv_bars("NVDA")
        self.assertIsNone(result)

    @patch('services.alpaca_service.requests.get')
    def test_get_latest_close(self, mock_get):
        bars = [
            {"t": "2026-04-22T00:00:00Z", "c": 900.0},
            {"t": "2026-04-23T00:00:00Z", "c": 910.5},
        ]
        mock_get.return_value = self._mock_response(200, {"bars": bars})
        from services.alpaca_service import get_latest_close
        import services.alpaca_service as alpaca_mod
        alpaca_mod.ALPACA_API_KEY = "key"
        alpaca_mod.ALPACA_API_SECRET = "secret"
        price = get_latest_close("NVDA")
        self.assertEqual(price, 910.5)

    def test_no_credentials_returns_none(self):
        from services.alpaca_service import get_ohlcv_bars
        import services.alpaca_service as alpaca_mod
        alpaca_mod.ALPACA_API_KEY = ""
        alpaca_mod.ALPACA_API_SECRET = ""
        result = get_ohlcv_bars("NVDA")
        self.assertIsNone(result)


class TestPricingRouting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # test_alerts_service.py registers a utils.pricing stub in sys.modules at
        # import time. When the full test suite runs, this stub is present before
        # these tests and lacks private helpers like _yahoo_get_current_price,
        # causing @patch to raise AttributeError. Evict the stubs here so the
        # real backend/utils/pricing.py is loaded for these tests.
        for _key in ('utils', 'utils.pricing', 'utils.calculations', 'utils.formatting'):
            sys.modules.pop(_key, None)

    @patch('utils.pricing._yahoo_get_current_price')
    @patch('services.alpaca_service.get_latest_close')
    def test_us_ticker_uses_alpaca_first(self, mock_alpaca, mock_yahoo):
        mock_alpaca.return_value = 500.0
        mock_yahoo.return_value = 490.0
        from utils.pricing import get_current_price
        price = get_current_price("NVDA")
        self.assertEqual(price, 500.0)
        mock_yahoo.assert_not_called()

    @patch('utils.pricing._yahoo_get_current_price')
    @patch('services.alpaca_service.get_latest_close')
    def test_us_ticker_fallback_to_yahoo_when_alpaca_fails(self, mock_alpaca, mock_yahoo):
        mock_alpaca.return_value = None
        mock_yahoo.return_value = 490.0
        from utils.pricing import get_current_price
        price = get_current_price("NVDA")
        self.assertEqual(price, 490.0)
        mock_yahoo.assert_called_once_with("NVDA")

    @patch('utils.pricing._yahoo_get_current_price')
    def test_uk_ticker_never_uses_alpaca(self, mock_yahoo):
        mock_yahoo.return_value = 150.0
        from utils.pricing import get_current_price
        with patch('services.alpaca_service.get_latest_close') as mock_alpaca:
            price = get_current_price("AZN.L")
            mock_alpaca.assert_not_called()
        self.assertEqual(price, 150.0)

    @patch('utils.pricing._yahoo_get_current_price')
    @patch('services.alpaca_service.get_latest_close')
    def test_us_ticker_returns_none_when_both_fail(self, mock_alpaca, mock_yahoo):
        mock_alpaca.return_value = None
        mock_yahoo.return_value = None
        from utils.pricing import get_current_price
        price = get_current_price("FAIL")
        self.assertIsNone(price)


class TestATRRouting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Same stub-eviction as TestPricingRouting — ensure real utils.pricing
        # is in sys.modules before these tests patch its private attributes.
        for _key in ('utils', 'utils.pricing', 'utils.calculations', 'utils.formatting'):
            sys.modules.pop(_key, None)

    @patch('utils.pricing._alpaca_calculate_atr')
    def test_us_ticker_atr_uses_alpaca(self, mock_alpaca_atr):
        mock_alpaca_atr.return_value = 12.5
        from utils.pricing import calculate_atr
        atr = calculate_atr("NVDA")
        self.assertEqual(atr, 12.5)
        mock_alpaca_atr.assert_called_once()

    @patch('utils.pricing._yahoo_get_current_price')
    @patch('utils.pricing._alpaca_calculate_atr')
    @patch('requests.get')
    def test_uk_ticker_atr_uses_yahoo(self, mock_requests, mock_alpaca_atr, mock_yahoo):
        mock_alpaca_atr.return_value = None
        # Provide a Yahoo Finance response for ATR
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "chart": {"result": [{"indicators": {"quote": [
                {"high": [102]*20, "low": [98]*20, "close": [100]*20}
            ]}}]}
        }
        mock_requests.return_value = mock_resp
        from utils.pricing import calculate_atr
        # UK tickers skip Alpaca entirely
        atr = calculate_atr("AZN.L")
        mock_alpaca_atr.assert_not_called()


if __name__ == '__main__':
    unittest.main()
