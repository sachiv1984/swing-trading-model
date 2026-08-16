"""
ST-03 (BLG-BE-76, EPIC-01, v7.10): Idempotency-key pattern applied to the
trade-entry (POST /portfolio/position) and trade-plan-creation
(POST /trade-plans) endpoints.

Covers, at the endpoint level:
- RISK-02: omitting idempotency_key from the request body is byte-for-byte
  the same code path as before this story — two requests without a key
  create two distinct resources, exactly as pre-ST-03.
- Supplying the same idempotency_key on a retried request returns the
  original response and does not create a second resource.

CI-safe: no live DB or network connections — the underlying create/DB calls
are mocked; only the idempotency dedup wiring is under test.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402
import routers.trade_plans as trade_plans_router  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)


class _FakeIdempotencyStore:
    """In-memory stand-in for the idempotency_keys table — exercises the
    real store/retrieve round trip through utils.idempotency.replay_or_create
    rather than just asserting call counts."""

    def __init__(self):
        self._data = {}

    def ensure(self):
        pass

    def get(self, portfolio_id, endpoint, key):
        return self._data.get((portfolio_id, endpoint, key))

    def create(self, portfolio_id, endpoint, key, body):
        self._data.setdefault((portfolio_id, endpoint, key), body)


def _patch_idempotency_store(store: _FakeIdempotencyStore):
    return (
        patch("database.ensure_idempotency_keys_table", side_effect=store.ensure),
        patch("database.get_idempotency_record", side_effect=store.get),
        patch("database.create_idempotency_record", side_effect=store.create),
    )


class TestTradePlanCreationIdempotency:
    def _install_common_mocks(self):
        patches = [
            patch.object(trade_plans_router, "get_portfolio", return_value={"id": "portfolio-1", "cash": 100000.0}),
            patch.object(trade_plans_router, "ensure_trade_plans_table"),
            patch.object(trade_plans_router, "ensure_si02_trade_plans_columns"),
            patch.object(trade_plans_router, "ensure_strategy_version_at_entry_columns"),
            patch.object(trade_plans_router, "ensure_triggered_by_price_alert_id_column"),  # ST-09, BLG-BE-84, EPIC-02, v8.8
            patch.object(trade_plans_router, "get_latest_snapshot", return_value=None),
            patch.object(trade_plans_router, "get_settings", return_value=[]),
        ]
        for p in patches:
            p.start()
        return patches

    def _stop(self, patches):
        for p in patches:
            p.stop()

    def test_no_idempotency_key_creates_two_distinct_plans(self):
        common = self._install_common_mocks()
        created_ids = iter(["plan-a", "plan-b"])
        mock_create = patch.object(
            trade_plans_router, "create_trade_plan",
            side_effect=lambda portfolio_id, data: {"id": next(created_ids), "ticker": data["ticker"], "market": data["market"], "checklist_items": []},
        )
        mock_create.start()
        try:
            body = {"ticker": "AAPL", "market": "US"}
            r1 = CLIENT.post("/trade-plans", json=body)
            r2 = CLIENT.post("/trade-plans", json=body)
            assert r1.status_code == 201 and r2.status_code == 201
            assert r1.json()["data"]["id"] != r2.json()["data"]["id"]
        finally:
            mock_create.stop()
            self._stop(common)

    def test_same_idempotency_key_returns_cached_response_no_duplicate_plan(self):
        common = self._install_common_mocks()
        store = _FakeIdempotencyStore()
        idem_patches = _patch_idempotency_store(store)
        for p in idem_patches:
            p.start()

        call_count = {"n": 0}

        def _fake_create_trade_plan(portfolio_id, data):
            call_count["n"] += 1
            return {"id": f"plan-{call_count['n']}", "ticker": data["ticker"], "market": data["market"], "checklist_items": []}

        mock_create = patch.object(trade_plans_router, "create_trade_plan", side_effect=_fake_create_trade_plan)
        mock_create.start()
        try:
            body = {"ticker": "TSLA", "market": "US", "idempotency_key": "retry-key-1"}
            r1 = CLIENT.post("/trade-plans", json=body)
            r2 = CLIENT.post("/trade-plans", json=body)

            assert r1.status_code == 201
            assert r1.json() == r2.json()
            assert call_count["n"] == 1, "create_trade_plan must only run once for a retried idempotency key"
        finally:
            mock_create.stop()
            for p in idem_patches:
                p.stop()
            self._stop(common)


class TestAddPositionIdempotency:
    def test_no_idempotency_key_creates_two_distinct_positions(self):
        with patch("main.get_portfolio", return_value={"id": "portfolio-1", "cash": 100000.0}):
            created_ids = iter(["pos-a", "pos-b"])
            with patch("main.add_position", side_effect=lambda **kw: {"position_id": next(created_ids), "ticker": kw["ticker"]}):
                body = {"ticker": "AAPL", "market": "US", "entry_date": "2026-07-29", "shares": 1, "entry_price": 100.0}
                r1 = CLIENT.post("/portfolio/position", json=body)
                r2 = CLIENT.post("/portfolio/position", json=body)
                assert r1.status_code == 200 and r2.status_code == 200
                assert r1.json()["data"]["position_id"] != r2.json()["data"]["position_id"]

    def test_same_idempotency_key_returns_cached_response_no_duplicate_position(self):
        store = _FakeIdempotencyStore()
        idem_patches = _patch_idempotency_store(store)
        for p in idem_patches:
            p.start()

        call_count = {"n": 0}

        def _fake_add_position(**kw):
            call_count["n"] += 1
            return {"position_id": f"pos-{call_count['n']}", "ticker": kw["ticker"]}

        try:
            with patch("main.get_portfolio", return_value={"id": "portfolio-1", "cash": 100000.0}), \
                 patch("main.add_position", side_effect=_fake_add_position):
                body = {
                    "ticker": "NVDA", "market": "US", "entry_date": "2026-07-29",
                    "shares": 1, "entry_price": 100.0, "idempotency_key": "retry-key-pos-1",
                }
                r1 = CLIENT.post("/portfolio/position", json=body)
                r2 = CLIENT.post("/portfolio/position", json=body)

                assert r1.status_code == 200
                assert r1.json() == r2.json()
                assert call_count["n"] == 1, "add_position must only run once for a retried idempotency key"
        finally:
            for p in idem_patches:
                p.stop()
