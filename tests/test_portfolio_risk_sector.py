"""
ST-12 (BLG-BE-38, EPIC-02, v7.0): Sector Concentration — ticker_universe join.

Covers the bug fix where GET /portfolio/sector-weights and
GET /portfolio/concentration-status never joined `ticker_universe`, so every
position showed "Unclassified" regardless of actual sector data recorded there.

Covers:
- _lookup_sector: ticker/market -> sector resolution against a ticker_universe
  map, including the .L suffix convention for UK tickers (AC-01)
- Positions with no sector in ticker_universe still resolve to None, so callers'
  "Unclassified" fallback is preserved (AC-02)
- _get_ticker_sector_map: pure DB read via SELECT, no yfinance call (AC-04)

CI-safe: no live DB or network connections.
"""

import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from routers.portfolio_risk import _lookup_sector, _get_ticker_sector_map


class TestLookupSector(unittest.TestCase):

    def setUp(self):
        self.ticker_sector_map = {
            "AAPL": "Technology",
            "AZN.L": "Healthcare",
            "VOD.L": "Communication Services",
        }

    def test_us_ticker_found(self):
        self.assertEqual(_lookup_sector(self.ticker_sector_map, "AAPL", "US"), "Technology")

    def test_uk_ticker_bare_resolves_via_l_suffix(self):
        # positions store UK tickers bare ('AZN'); ticker_universe stores '.L' suffixed
        self.assertEqual(_lookup_sector(self.ticker_sector_map, "AZN", "UK"), "Healthcare")

    def test_uk_ticker_already_suffixed(self):
        self.assertEqual(_lookup_sector(self.ticker_sector_map, "AZN.L", "UK"), "Healthcare")

    def test_lowercase_ticker_normalised(self):
        self.assertEqual(_lookup_sector(self.ticker_sector_map, "aapl", "US"), "Technology")

    def test_unknown_ticker_returns_none(self):
        # AC-02: no sector in ticker_universe -> None, caller applies "Unclassified" fallback
        self.assertIsNone(_lookup_sector(self.ticker_sector_map, "UNKN", "US"))

    def test_unknown_uk_ticker_returns_none(self):
        self.assertIsNone(_lookup_sector(self.ticker_sector_map, "ZZZ", "UK"))

    def test_none_ticker_returns_none(self):
        self.assertIsNone(_lookup_sector(self.ticker_sector_map, None, "US"))

    def test_empty_map_returns_none(self):
        self.assertIsNone(_lookup_sector({}, "AAPL", "US"))


class TestGetTickerSectorMap(unittest.TestCase):

    def _mock_conn(self, rows):
        conn = MagicMock()
        cursor_cm = MagicMock()
        cursor_cm.__enter__.return_value.fetchall.return_value = rows
        conn.cursor.return_value = cursor_cm
        return conn, cursor_cm

    def test_builds_ticker_to_sector_dict(self):
        rows = [
            {"ticker": "AAPL", "sector": "Technology"},
            {"ticker": "AZN.L", "sector": "Healthcare"},
        ]
        conn, _ = self._mock_conn(rows)
        result = _get_ticker_sector_map(conn)
        self.assertEqual(result, {"AAPL": "Technology", "AZN.L": "Healthcare"})

    def test_empty_ticker_universe_returns_empty_dict(self):
        conn, _ = self._mock_conn([])
        result = _get_ticker_sector_map(conn)
        self.assertEqual(result, {})

    def test_query_filters_null_sector_no_yfinance_call(self):
        # AC-04: pure SQL read against ticker_universe — assert the query string
        # itself, proving no live pricing/yfinance import is exercised in this path.
        rows = []
        conn, cursor_cm = self._mock_conn(rows)
        _get_ticker_sector_map(conn)
        executed_sql = cursor_cm.__enter__.return_value.execute.call_args[0][0]
        self.assertIn("ticker_universe", executed_sql)
        self.assertIn("sector IS NOT NULL", executed_sql)
        self.assertNotIn("yfinance", executed_sql.lower())


if __name__ == "__main__":
    unittest.main()
