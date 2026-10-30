"""
ST-10 (BLG-BE-188, EPIC-02, v9.14): POST /positions/{position_id}/exit returns
its documented 404 or 400 with a `detail` string, not a 500.

position_endpoints.md §POST /positions/{position_id}/exit Errors. Each case
runs the real services.position_service.exit_position, with only its
portfolio and position reads mocked, so the ValueError is the one the service
actually raises. No write is reached.
"""
from unittest.mock import patch

import pytest

UK_OPEN = {"id": "pos-1", "ticker": "VOD.L", "market": "UK", "status": "open", "shares": 10}
US_OPEN = {"id": "pos-1", "ticker": "AAPL", "market": "US", "status": "open", "shares": 10}
BODY = {"shares": 10, "exit_price": 120.0, "exit_date": "2026-10-30"}


def _client():
    from tests._real_database import real_database_imports
    with real_database_imports():
        from fastapi.testclient import TestClient
        import main
        import services.position_service as position_service
    return TestClient(main.app, raise_server_exceptions=False), position_service


def _post(portfolio, positions, body):
    client, position_service = _client()
    with patch.object(position_service, "get_portfolio", return_value=portfolio), \
         patch.object(position_service, "get_positions", return_value=positions):
        return client.post("/positions/pos-1/exit", json=body)


def _assert_error(response, status_code, detail):
    assert response.status_code == status_code, response.text
    assert response.json()["detail"] == detail


PORTFOLIO = {"id": "p-1", "cash": 1000.0}


def test_missing_position_returns_404():
    _assert_error(_post(PORTFOLIO, [], BODY), 404, "Position not found")


def test_missing_portfolio_returns_404():
    _assert_error(_post(None, [], BODY), 404, "Portfolio not found")


def test_closed_position_returns_400():
    _assert_error(_post(PORTFOLIO, [{**UK_OPEN, "status": "closed"}], BODY), 400, "Position already closed")


@pytest.mark.parametrize("exit_price", [0, -1.0])
def test_nonpositive_exit_price_returns_400(exit_price):
    response = _post(PORTFOLIO, [UK_OPEN], {**BODY, "exit_price": exit_price})
    _assert_error(response, 400, "Exit price must be greater than 0")


def test_negative_shares_returns_400():
    response = _post(PORTFOLIO, [UK_OPEN], {**BODY, "shares": -1})
    _assert_error(response, 400, "Shares to exit must be greater than 0")


def test_shares_above_position_size_returns_400():
    response = _post(PORTFOLIO, [UK_OPEN], {**BODY, "shares": 11})
    _assert_error(response, 400, "Insufficient shares. Position has 10.0 shares, exit requested 11.0")


def test_us_exit_without_fx_rate_returns_400():
    response = _post(PORTFOLIO, [US_OPEN], BODY)
    _assert_error(
        response, 400,
        "FX rate is required for US stock exits. Please provide the GBP/USD rate from your broker statement.",
    )
