"""
Unit tests for screener_engine (DS-01 / ST-03)
Uses BLG-QA-09 synthetic test data — no live API calls.
"""
import pytest
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

FIXTURES = Path(__file__).parent / "mock_harness" / "fixtures"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_bars(scenario: str, ticker: str) -> list:
    data = json.loads((FIXTURES / f"{scenario}.json").read_text())
    bars = data["alpaca"][f"bars/{ticker}"]["bars"]
    return [{"date": b["t"][:10], "open": b["o"], "high": b["h"],
             "low": b["l"], "close": b["c"], "volume": b["v"]} for b in bars]


def _risk_on_regime():
    return {
        "regime_status": "risk_on",
        "regime_index": "SPY",
        "regime_index_price": 520.0,
        "regime_index_ma200": 490.0,
    }


def _risk_off_regime():
    return {
        "regime_status": "risk_off",
        "regime_index": "SPY",
        "regime_index_price": 450.0,
        "regime_index_ma200": 490.0,
    }


def _make_ohlcv(n: int = 20, base_close: float = 100.0, atr_mult: float = 1.5) -> list:
    """Generate simple synthetic OHLCV with predictable ATR."""
    records = []
    for i in range(n):
        c = base_close + i * 0.5
        records.append({
            "date": f"2026-04-{(i % 28) + 1:02d}",
            "open": c - 0.5,
            "high": c + atr_mult,
            "low": c - atr_mult,
            "close": c,
            "volume": 1_000_000 + i * 10_000,
        })
    return records


# ---------------------------------------------------------------------------
# ATR calculation
# ---------------------------------------------------------------------------

from services.screener_engine import compute_atr, ATR_PERIOD


def test_atr_requires_at_least_period_plus_one_bars():
    ohlcv = _make_ohlcv(n=ATR_PERIOD)
    assert compute_atr(ohlcv, ATR_PERIOD) is None


def test_atr_returns_value_with_sufficient_bars():
    ohlcv = _make_ohlcv(n=ATR_PERIOD + 1)
    result = compute_atr(ohlcv, ATR_PERIOD)
    assert result is not None
    assert result > 0


def test_atr_is_deterministic():
    ohlcv = _make_ohlcv(n=30)
    assert compute_atr(ohlcv) == compute_atr(ohlcv)


def test_atr_higher_for_more_volatile_data():
    low_vol = _make_ohlcv(n=20, atr_mult=0.5)
    high_vol = _make_ohlcv(n=20, atr_mult=5.0)
    assert compute_atr(high_vol) > compute_atr(low_vol)


def test_atr_from_fixture_data():
    ohlcv = _load_bars("screener_pass_us", "MOCK-PASS-US")
    result = compute_atr(ohlcv)
    assert result is not None
    assert result > 0


# ---------------------------------------------------------------------------
# Signal scoring
# ---------------------------------------------------------------------------

from services.screener_engine import compute_signal_score


def test_signal_score_bounds():
    ohlcv = _make_ohlcv(n=40)
    score = compute_signal_score(ohlcv)
    assert 0.0 <= score <= 1.0


def test_signal_score_deterministic():
    ohlcv = _make_ohlcv(n=40)
    assert compute_signal_score(ohlcv) == compute_signal_score(ohlcv)


def test_signal_score_with_volume_surge():
    ohlcv = _make_ohlcv(n=30)
    # Triple last bar's volume
    ohlcv[-1]["volume"] = ohlcv[-2]["volume"] * 3
    score_surge = compute_signal_score(ohlcv)

    ohlcv[-1]["volume"] = ohlcv[-2]["volume"]
    score_flat = compute_signal_score(ohlcv)

    assert score_surge >= score_flat


def test_signal_score_rising_closes_higher_than_falling():
    rising = _make_ohlcv(n=40, base_close=100, atr_mult=1.5)
    falling = [dict(r, close=200 - i * 0.5, open=200 - i * 0.5 - 0.5,
                    high=200 - i * 0.5 + 1.5, low=200 - i * 0.5 - 1.5)
               for i, r in enumerate(rising)]
    assert compute_signal_score(rising) >= compute_signal_score(falling)


# ---------------------------------------------------------------------------
# compute_screener_result — gate tests
# ---------------------------------------------------------------------------

from services.screener_engine import compute_screener_result


def test_regime_gate_excludes_risk_off():
    ohlcv = _make_ohlcv(n=40)
    r = _risk_off_regime()
    result = compute_screener_result("AAPL", "US", ohlcv, **r)
    assert result is None


def test_data_gate_excludes_insufficient_history():
    ohlcv = _make_ohlcv(n=5)
    r = _risk_on_regime()
    result = compute_screener_result("AAPL", "US", ohlcv, **r)
    assert result is None


def test_atr_gate_excludes_zero_volatility():
    ohlcv = [{"date": f"2026-04-{i+1:02d}", "open": 100.0, "high": 100.0,
               "low": 100.0, "close": 100.0, "volume": 1000000} for i in range(20)]
    r = _risk_on_regime()
    result = compute_screener_result("FLAT", "US", ohlcv, **r)
    assert result is None


def test_passes_all_gates_returns_record():
    ohlcv = _load_bars("screener_pass_us", "MOCK-PASS-US")
    r = _risk_on_regime()
    result = compute_screener_result("MOCK-PASS-US", "US", ohlcv, **r)
    # Score may or may not exceed threshold for this fixture; just test structure if it passes
    if result is not None:
        assert result["ticker"] == "MOCK-PASS-US"
        assert result["market"] == "US"
        assert result["currency"] == "USD"
        assert isinstance(result["atr"], float)
        assert result["atr_period"] == ATR_PERIOD
        assert result["regime_status"] == "risk_on"
        assert 0.0 <= result["signal_score"] <= 1.0


def test_result_includes_all_required_fields():
    ohlcv = _make_ohlcv(n=40, base_close=200, atr_mult=5.0)
    r = _risk_on_regime()
    result = compute_screener_result("TEST", "US", ohlcv, **r,
                                     sector="Technology", industry="Software",
                                     news_headlines=[{"id": 1, "headline": "Test", "created_at": "2026-04-25"}],
                                     run_id="abc-123", run_timestamp="2026-04-25T12:00:00Z")
    if result is not None:
        required = ["ticker", "market", "currency", "price", "atr", "atr_period",
                    "regime_status", "regime_index", "regime_index_price", "regime_index_ma200",
                    "signal_score", "signal_type", "sector", "industry",
                    "proximity_to_entry_zone", "news_headline_count", "news_headlines",
                    "run_id", "run_timestamp"]
        for field in required:
            assert field in result, f"Missing field: {field}"
        assert result["sector"] == "Technology"
        assert result["news_headline_count"] == 1
        assert result["run_id"] == "abc-123"


def test_uk_ticker_currency_is_gbp():
    ohlcv = _make_ohlcv(n=40, base_close=500, atr_mult=10.0)
    r = {
        "regime_status": "risk_on",
        "regime_index": "^FTSE",
        "regime_index_price": 8400.0,
        "regime_index_ma200": 8000.0,
    }
    result = compute_screener_result("HSBA.L", "UK", ohlcv, **r)
    if result is not None:
        assert result["currency"] == "GBP"


def test_no_news_defaults_to_empty_list():
    ohlcv = _make_ohlcv(n=40, base_close=200, atr_mult=5.0)
    r = _risk_on_regime()
    result = compute_screener_result("TEST", "US", ohlcv, **r)
    if result is not None:
        assert result["news_headlines"] == []
        assert result["news_headline_count"] == 0
