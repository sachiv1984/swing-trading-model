"""
Last good GBP/USD rate and its source (ST-04/ST-05, EPIC-01, v9.14,
BLG-BE-194/BLG-BE-169).

get_live_fx_rate() used the constant 1.27 whenever Yahoo Finance failed. It
now uses the last good rate (kept in memory and in fx_rate_last_good, so it
survives a restart) and falls back to the constant only when none was ever
stored. get_fx_rate_info() reports the source, and GET /portfolio,
GET /positions and GET /market/status carry it.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
import utils.pricing as pricing  # noqa: E402

FETCHED_AT = datetime(2026, 10, 27, 15, 30, tzinfo=timezone.utc)


def _payload(rate):
    return {"chart": {"result": [{"meta": {"regularMarketPrice": rate}}]}}


@pytest.fixture(autouse=True)
def _fresh_fx_state(monkeypatch):
    monkeypatch.setitem(pricing._fx_cache, "rate", None)
    monkeypatch.setitem(pricing._fx_cache, "expires_at", 0.0)
    for key in ("rate", "source", "as_of"):
        monkeypatch.setitem(pricing._fx_state, key, None)
    for key in ("rate", "as_of"):
        monkeypatch.setitem(pricing._fx_last_good, key, None)
    stored = {}
    monkeypatch.setattr("database.upsert_last_good_fx_rate",
                        lambda pair, rate, fetched_at: stored.update({pair: {"rate": rate, "fetched_at": fetched_at}}),
                        raising=False)
    monkeypatch.setattr("database.get_last_good_fx_rate", lambda pair: stored.get(pair), raising=False)
    return stored


def _yahoo_fails(monkeypatch):
    def fail():
        raise ConnectionError("Yahoo Finance down")
    monkeypatch.setattr(pricing, "_yahoo_fetch_fx_rate", fail)


def test_live_fetch_is_reported_live_and_stored(monkeypatch, _fresh_fx_state):
    monkeypatch.setattr(pricing, "_yahoo_fetch_fx_rate", lambda: _payload(1.3412))

    info = pricing.get_fx_rate_info()

    assert info["fx_rate"] == 1.3412
    assert info["fx_rate_source"] == "live"
    assert info["fx_rate_as_of"] is not None
    assert _fresh_fx_state["GBPUSD"]["rate"] == 1.3412


def test_failed_fetch_uses_the_last_good_rate_not_the_constant(monkeypatch):
    monkeypatch.setattr(pricing, "_yahoo_fetch_fx_rate", lambda: _payload(1.3412))
    pricing.get_live_fx_rate()
    monkeypatch.setitem(pricing._fx_cache, "expires_at", 0.0)
    _yahoo_fails(monkeypatch)

    rate = pricing.get_live_fx_rate()
    info = pricing.get_fx_rate_info(rate)

    assert rate == 1.3412
    assert rate != pricing.DEFAULT_FX_RATE
    assert info["fx_rate_source"] == "last_known"
    assert info["fx_rate_as_of"] is not None


def test_stored_rate_survives_a_restart(monkeypatch, _fresh_fx_state):
    _fresh_fx_state["GBPUSD"] = {"rate": 1.3301, "fetched_at": FETCHED_AT}
    _yahoo_fails(monkeypatch)

    info = pricing.get_fx_rate_info()

    assert info == {"fx_rate": 1.3301, "fx_rate_source": "last_known", "fx_rate_as_of": FETCHED_AT.isoformat()}


def test_constant_only_when_no_rate_was_ever_stored(monkeypatch):
    _yahoo_fails(monkeypatch)

    info = pricing.get_fx_rate_info()

    assert info == {"fx_rate": pricing.DEFAULT_FX_RATE, "fx_rate_source": "constant", "fx_rate_as_of": None}


def test_constant_is_never_reported_live(monkeypatch):
    monkeypatch.setattr(pricing, "_yahoo_fetch_fx_rate", lambda: {"chart": {"result": []}})

    info = pricing.get_fx_rate_info()

    assert info["fx_rate"] == pricing.DEFAULT_FX_RATE
    assert info["fx_rate_source"] != "live"


def test_storage_failure_still_falls_back_to_the_constant(monkeypatch):
    def broken(pair):
        raise RuntimeError("database unavailable")
    monkeypatch.setattr("database.get_last_good_fx_rate", broken, raising=False)
    _yahoo_fails(monkeypatch)

    assert pricing.get_fx_rate_info()["fx_rate_source"] == "constant"


def test_market_status_carries_the_fx_source():
    from fastapi.testclient import TestClient
    import main

    regime = {"spy_risk_on": True, "ftse_risk_on": True, "spy_price": 500.0, "spy_ma200": 450.0,
              "ftse_price": 8000.0, "ftse_ma200": 7900.0, "date": FETCHED_AT}
    with patch.object(main, "check_market_regime", return_value=regime), \
         patch.object(main, "get_live_fx_rate", return_value=1.3301), \
         patch.object(main, "get_fx_rate_info", return_value={
             "fx_rate": 1.3301, "fx_rate_source": "last_known", "fx_rate_as_of": FETCHED_AT.isoformat()}), \
         patch.object(main, "record_market_status_check"):
        resp = TestClient(main.app).get("/market/status")

    data = resp.json()["data"]
    assert data["fx_rate"] == 1.3301
    assert data["fx_rate_source"] == "last_known"
    assert data["fx_rate_as_of"] == FETCHED_AT.isoformat()


def test_mismatched_constant_fails_closed(monkeypatch):
    # Another request moved the shared state to a live rate after this one got the constant.
    monkeypatch.setitem(pricing._fx_state, "rate", 1.3412)
    monkeypatch.setitem(pricing._fx_state, "source", "live")
    monkeypatch.setitem(pricing._fx_cache, "rate", 1.3412)

    info = pricing.get_fx_rate_info(pricing.DEFAULT_FX_RATE)

    assert info["fx_rate_source"] == "constant"
    assert info["fx_rate_as_of"] is None


def test_mismatched_last_known_rate_is_not_reported_live(monkeypatch):
    monkeypatch.setitem(pricing._fx_state, "rate", 1.3412)
    monkeypatch.setitem(pricing._fx_state, "source", "live")
    monkeypatch.setitem(pricing._fx_cache, "rate", 1.3412)
    monkeypatch.setitem(pricing._fx_last_good, "rate", 1.3301)
    monkeypatch.setitem(pricing._fx_last_good, "as_of", FETCHED_AT)

    info = pricing.get_fx_rate_info(1.3301)

    assert info["fx_rate_source"] == "last_known"
    assert info["fx_rate_as_of"] == FETCHED_AT.isoformat()
