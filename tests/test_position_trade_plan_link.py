"""
BLG-BE-46 regression tests (ST-01, EPIC-01, v6.8).

trade_plans.position_id was never populated in production because the
pre-trade planning flow (TradePlan.js) and the position-entry flow
(TradeEntry.js) are separate pages with no hand-off between them.

add_position() now auto-links the most recent unlinked draft trade plan for
the same ticker/market to the newly created position (best-effort — a lookup
or update failure must not block position creation).

ST-01 (EPIC-01, v7.3) extends add_position() with an optional explicit
trade_plan_id parameter — the "Start Trade from Plan" action passes the exact
plan the user started from, which takes precedence over the ticker/market
best-effort match. See TestAddPositionExplicitTradePlanLink below.
"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.position_service as position_service  # noqa: E402


def _portfolio():
    return {"id": "portfolio-1", "cash": 100000.0}


def _settings():
    return [{
        "uk_commission": 9.95,
        "us_commission": 0,
        "stamp_duty_rate": 0.005,
        "fx_fee_rate": 0.0015,
    }]


class TestAddPositionTradePlanAutoLink:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()

    def _install_common_mocks(self):
        # NOTE: calculate_us_entry_fees / calculate_uk_entry_fees / calculate_initial_stop
        # are explicitly mocked here (not left to the real utils.calculations
        # implementation) because some other test modules in this suite globally
        # stub sys.modules["utils.calculations"] attributes without restoring them
        # (pre-existing test-isolation gap, unrelated to BLG-BE-46) — depending on
        # suite run order, position_service's module-level bindings for these names
        # may already be MagicMocks by the time this test runs. Mocking them here
        # makes this test hermetic regardless of execution order.
        self._patch("get_portfolio", return_value=_portfolio())
        self._patch("get_settings", return_value=_settings())
        self._patch("create_position", return_value={"id": "new-position-id"})
        self._patch("update_portfolio_cash")
        self._patch("calculate_atr", return_value=1.0)
        self._patch("get_live_fx_rate", return_value=1.27)
        self._patch("calculate_us_entry_fees", return_value={"commission": 0, "stamp_duty": 0, "fx_fee": 1.5, "total": 1.5})
        self._patch("calculate_uk_entry_fees", return_value={"commission": 9.95, "stamp_duty": 5.0, "total": 14.95})
        self._patch("calculate_initial_stop", return_value=90.0)

    def test_links_matching_unlinked_draft_plan(self):
        self._install_common_mocks()
        unlinked_plan = {"id": "plan-1", "ticker": "AAPL", "market": "US", "status": "draft"}
        mock_lookup = self._patch("get_unlinked_trade_plan_for_entry", return_value=unlinked_plan)
        mock_update = self._patch("update_trade_plan", return_value=None)

        result = position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-09",
            shares=10, entry_price=100.0, fx_rate=1.27,
        )

        assert result["position_id"] == "new-position-id"
        mock_lookup.assert_called_once_with("portfolio-1", "AAPL", "US")
        mock_update.assert_called_once_with(
            "plan-1", "portfolio-1",
            {"position_id": "new-position-id", "status": "active"},
        )

    def test_no_matching_plan_skips_update(self):
        self._install_common_mocks()
        self._patch("get_unlinked_trade_plan_for_entry", return_value=None)
        mock_update = self._patch("update_trade_plan", return_value=None)

        position_service.add_position(
            ticker="TSLA", market="US", entry_date="2026-07-09",
            shares=5, entry_price=200.0, fx_rate=1.27,
        )

        mock_update.assert_not_called()

    def test_link_lookup_failure_does_not_block_position_creation(self):
        self._install_common_mocks()
        self._patch("get_unlinked_trade_plan_for_entry", side_effect=Exception("db error"))
        mock_update = self._patch("update_trade_plan")

        result = position_service.add_position(
            ticker="MSFT", market="US", entry_date="2026-07-09",
            shares=3, entry_price=300.0, fx_rate=1.27,
        )

        assert result["position_id"] == "new-position-id"
        mock_update.assert_not_called()

    def test_link_update_failure_does_not_block_position_creation(self):
        self._install_common_mocks()
        unlinked_plan = {"id": "plan-2", "ticker": "NVDA", "market": "US", "status": "draft"}
        self._patch("get_unlinked_trade_plan_for_entry", return_value=unlinked_plan)
        self._patch("update_trade_plan", side_effect=Exception("update failed"))

        result = position_service.add_position(
            ticker="NVDA", market="US", entry_date="2026-07-09",
            shares=2, entry_price=400.0, fx_rate=1.27,
        )

        assert result["position_id"] == "new-position-id"


class TestAddPositionExplicitTradePlanLink:
    """ST-01 (EPIC-01, v7.3): explicit trade_plan_id passed by "Start Trade from Plan"."""

    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()

    def _install_common_mocks(self):
        self._patch("get_portfolio", return_value=_portfolio())
        self._patch("get_settings", return_value=_settings())
        self._patch("create_position", return_value={"id": "new-position-id"})
        self._patch("update_portfolio_cash")
        self._patch("calculate_atr", return_value=1.0)
        self._patch("get_live_fx_rate", return_value=1.27)
        self._patch("calculate_us_entry_fees", return_value={"commission": 0, "stamp_duty": 0, "fx_fee": 1.5, "total": 1.5})
        self._patch("calculate_uk_entry_fees", return_value={"commission": 9.95, "stamp_duty": 5.0, "total": 14.95})
        self._patch("calculate_initial_stop", return_value=90.0)

    def test_explicit_plan_id_links_that_exact_plan_not_ticker_match(self):
        self._install_common_mocks()
        exact_plan = {"id": "plan-exact", "ticker": "AAPL", "market": "US", "status": "research_complete", "position_id": None}
        mock_get_by_id = self._patch("get_trade_plan_by_id", return_value=exact_plan)
        mock_fuzzy_lookup = self._patch("get_unlinked_trade_plan_for_entry")
        mock_update = self._patch("update_trade_plan", return_value=None)

        result = position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-16",
            shares=10, entry_price=100.0, fx_rate=1.27,
            trade_plan_id="plan-exact",
        )

        assert result["position_id"] == "new-position-id"
        mock_get_by_id.assert_called_once_with("plan-exact", "portfolio-1")
        mock_fuzzy_lookup.assert_not_called()
        mock_update.assert_called_once_with(
            "plan-exact", "portfolio-1",
            {"position_id": "new-position-id", "status": "active"},
        )

    def test_explicit_plan_already_linked_skips_update(self):
        self._install_common_mocks()
        already_linked_plan = {"id": "plan-taken", "ticker": "AAPL", "market": "US", "status": "active", "position_id": "some-other-position"}
        self._patch("get_trade_plan_by_id", return_value=already_linked_plan)
        mock_update = self._patch("update_trade_plan", return_value=None)

        result = position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-16",
            shares=10, entry_price=100.0, fx_rate=1.27,
            trade_plan_id="plan-taken",
        )

        assert result["position_id"] == "new-position-id"
        mock_update.assert_not_called()

    def test_explicit_plan_lookup_failure_does_not_block_position_creation(self):
        self._install_common_mocks()
        self._patch("get_trade_plan_by_id", side_effect=Exception("db error"))
        mock_update = self._patch("update_trade_plan")

        result = position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-16",
            shares=10, entry_price=100.0, fx_rate=1.27,
            trade_plan_id="plan-missing",
        )

        assert result["position_id"] == "new-position-id"
        mock_update.assert_not_called()

    def test_explicit_plan_not_found_skips_update_cleanly(self):
        """Plan ID not found (or belongs to another portfolio) — get_trade_plan_by_id
        returns None rather than raising. Distinct from the exception-path test above."""
        self._install_common_mocks()
        self._patch("get_trade_plan_by_id", return_value=None)
        mock_update = self._patch("update_trade_plan")

        result = position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-16",
            shares=10, entry_price=100.0, fx_rate=1.27,
            trade_plan_id="plan-nonexistent",
        )

        assert result["position_id"] == "new-position-id"
        mock_update.assert_not_called()
