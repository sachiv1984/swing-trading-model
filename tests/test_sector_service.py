"""
Unit tests for sector_service (DS-03 — BLG-SPEC-22)

Covers:
- Sector/industry fetch for US and UK tickers
- Null handling when Yahoo Finance returns no classification
- Exception handling (network errors, missing fields)
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.sector_service import get_sector_and_industry, enrich_positions_with_sector


class TestGetSectorAndIndustry(unittest.TestCase):

    def _mock_ticker(self, info_dict):
        mock = MagicMock()
        mock.info = info_dict
        return mock

    @patch('services.sector_service.yf.Ticker')
    def test_us_ticker_returns_sector_and_industry(self, mock_ticker_cls):
        mock_ticker_cls.return_value = self._mock_ticker({
            'sector': 'Technology',
            'industry': 'Semiconductors',
        })
        sector, industry = get_sector_and_industry('NVDA', 'US')
        self.assertEqual(sector, 'Technology')
        self.assertEqual(industry, 'Semiconductors')
        mock_ticker_cls.assert_called_once_with('NVDA')

    @patch('services.sector_service.yf.Ticker')
    def test_uk_ticker_appends_l_suffix(self, mock_ticker_cls):
        mock_ticker_cls.return_value = self._mock_ticker({
            'sector': 'Consumer Defensive',
            'industry': 'Beverages—Non-Alcoholic',
        })
        sector, industry = get_sector_and_industry('AZN', 'UK')
        mock_ticker_cls.assert_called_once_with('AZN.L')
        self.assertEqual(sector, 'Consumer Defensive')

    @patch('services.sector_service.yf.Ticker')
    def test_uk_ticker_already_has_l_suffix(self, mock_ticker_cls):
        mock_ticker_cls.return_value = self._mock_ticker({'sector': 'Healthcare', 'industry': 'Drug Manufacturers'})
        sector, industry = get_sector_and_industry('AZN.L', 'UK')
        mock_ticker_cls.assert_called_once_with('AZN.L')

    @patch('services.sector_service.yf.Ticker')
    def test_returns_none_when_sector_absent(self, mock_ticker_cls):
        mock_ticker_cls.return_value = self._mock_ticker({})
        sector, industry = get_sector_and_industry('UNKN', 'US')
        self.assertIsNone(sector)
        self.assertIsNone(industry)

    @patch('services.sector_service.yf.Ticker')
    def test_returns_none_on_exception(self, mock_ticker_cls):
        mock_ticker_cls.side_effect = Exception("network error")
        sector, industry = get_sector_and_industry('FAIL', 'US')
        self.assertIsNone(sector)
        self.assertIsNone(industry)

    @patch('services.sector_service.yf.Ticker')
    def test_returns_none_when_sector_is_empty_string(self, mock_ticker_cls):
        mock_ticker_cls.return_value = self._mock_ticker({'sector': '', 'industry': ''})
        sector, industry = get_sector_and_industry('XYZ', 'US')
        self.assertIsNone(sector)
        self.assertIsNone(industry)


class TestEnrichPositionsWithSector(unittest.TestCase):

    @patch('services.sector_service.get_sector_and_industry')
    def test_enriches_all_positions(self, mock_fetch):
        mock_fetch.side_effect = [
            ('Technology', 'Semiconductors'),
            ('Healthcare', 'Drug Manufacturers'),
        ]
        positions = [
            {'ticker': 'NVDA', 'market': 'US', 'entry_price': 100},
            {'ticker': 'AZN', 'market': 'UK', 'entry_price': 50},
        ]
        result = enrich_positions_with_sector(positions)
        self.assertEqual(result[0]['sector'], 'Technology')
        self.assertEqual(result[0]['industry'], 'Semiconductors')
        self.assertEqual(result[1]['sector'], 'Healthcare')
        self.assertIsNone(result[1].get('entry_note'))

    @patch('services.sector_service.get_sector_and_industry')
    def test_null_sector_when_unavailable(self, mock_fetch):
        mock_fetch.return_value = (None, None)
        positions = [{'ticker': 'UNKN', 'market': 'US'}]
        result = enrich_positions_with_sector(positions)
        self.assertIsNone(result[0]['sector'])
        self.assertIsNone(result[0]['industry'])

    @patch('services.sector_service.get_sector_and_industry')
    def test_original_position_fields_preserved(self, mock_fetch):
        mock_fetch.return_value = ('Technology', 'Cloud Computing')
        positions = [{'ticker': 'MSFT', 'market': 'US', 'entry_price': 300.0, 'tags': ['growth']}]
        result = enrich_positions_with_sector(positions)
        self.assertEqual(result[0]['entry_price'], 300.0)
        self.assertEqual(result[0]['tags'], ['growth'])


if __name__ == '__main__':
    unittest.main()
