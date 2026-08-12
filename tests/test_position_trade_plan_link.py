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
        # ST-03 (BLG-BE-91, EPIC-02, v8.6): the linkage outcome must be
        # surfaced in the response, not just a server-side print().
        assert result["trade_plan_linked"] is True
        assert result["trade_plan_id"] == "plan-1"

    def test_no_matching_plan_skips_update(self):
        self._install_common_mocks()
        self._patch("get_unlinked_trade_plan_for_entry", return_value=None)
        mock_update = self._patch("update_trade_plan", return_value=None)

        result = position_service.add_position(
            ticker="TSLA", market="US", entry_date="2026-07-09",
            shares=5, entry_price=200.0, fx_rate=1.27,
        )

        mock_update.assert_not_called()
        # ST-03 (BLG-BE-91, EPIC-02, v8.6): a position genuinely created with
        # no trade plan must surface that fact, not stay silent.
        assert result["trade_plan_linked"] is False
        assert result["trade_plan_id"] is None

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
        # A lookup failure is also a "not linked" outcome, not a hidden one.
        assert result["trade_plan_linked"] is False
        assert result["trade_plan_id"] is None

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
        assert result["trade_plan_linked"] is True
        assert result["trade_plan_id"] == "plan-exact"

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


# ---------------------------------------------------------------------------
# ST-03 (BLG-BE-91, EPIC-02, v8.6): DB-level safeguard against new orphaned
# trade_plans rows — router-level guard on PUT /trade-plans/{id} (primary
# defense) and the paired DB CHECK constraint (defense-in-depth).
# ---------------------------------------------------------------------------

class TestUpdatePlanActiveStatusRequiresPosition:
    """routers/trade_plans.py::update_plan() -- status='active' with no
    position_id (on the existing row or this same update) must 400, not
    silently persist an orphaned "active" plan."""

    def setup_method(self):
        # Deliberately do NOT sys.modules.pop("main", None) here: doing so
        # replaces the shared `main` module object in sys.modules with a
        # fresh one, which silently breaks @patch("main.X", ...) /
        # @patch("routers.trade_plans.X", ...) string-path patches used by
        # OTHER test files collected in the same pytest session -- those
        # patches resolve against sys.modules at call time, not a captured
        # reference, so a later re-import here left them patching an
        # orphaned module object with zero effect on the actually-running
        # app. Reuse whatever `main` is already in sys.modules (imported
        # once per session, same as every other test file in this suite).
        from fastapi.testclient import TestClient
        import main as _main
        self._main = _main
        self.client = TestClient(_main.app, raise_server_exceptions=False)
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, target, **kwargs):
        p = patch(target, **kwargs)
        self._patches.append(p)
        return p.start()

    def _install_common_mocks(self):
        self._patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)

    def test_active_status_with_no_position_id_anywhere_returns_400(self):
        self._install_common_mocks()
        self._patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(
            "routers.trade_plans.get_trade_plan_by_id",
            return_value={"id": "plan-1", "position_id": None, "status": "draft"},
        )
        mock_update = self._patch("routers.trade_plans.update_trade_plan")

        resp = self.client.put("/trade-plans/plan-1", json={"status": "active"})

        assert resp.status_code == 400
        assert "position_id" in resp.json()["message"]
        mock_update.assert_not_called()

    def test_active_status_with_position_id_in_same_update_succeeds(self):
        self._install_common_mocks()
        self._patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(
            "routers.trade_plans.get_trade_plan_by_id",
            return_value={"id": "plan-1", "position_id": None, "status": "draft"},
        )
        self._patch(
            "routers.trade_plans.update_trade_plan",
            return_value={"id": "plan-1", "position_id": "pos-1", "status": "active"},
        )

        resp = self.client.put(
            "/trade-plans/plan-1",
            json={"status": "active", "position_id": "pos-1"},
        )

        assert resp.status_code == 200

    def test_active_status_with_position_id_already_on_existing_plan_succeeds(self):
        self._install_common_mocks()
        self._patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(
            "routers.trade_plans.get_trade_plan_by_id",
            return_value={"id": "plan-1", "position_id": "pos-existing", "status": "research_complete"},
        )
        self._patch(
            "routers.trade_plans.update_trade_plan",
            return_value={"id": "plan-1", "position_id": "pos-existing", "status": "active"},
        )

        resp = self.client.put("/trade-plans/plan-1", json={"status": "active"})

        assert resp.status_code == 200

    def test_active_status_for_nonexistent_plan_returns_404_not_400(self):
        self._install_common_mocks()
        self._patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("routers.trade_plans.get_trade_plan_by_id", return_value=None)
        mock_update = self._patch("routers.trade_plans.update_trade_plan")

        resp = self.client.put("/trade-plans/plan-missing", json={"status": "active"})

        assert resp.status_code == 404
        mock_update.assert_not_called()

    def test_non_active_status_update_unaffected_by_this_guard(self):
        """Regression guard: this story's check must not fire for any status
        other than 'active' (e.g. a plain field edit with no status change)."""
        self._install_common_mocks()
        self._patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(
            "routers.trade_plans.get_trade_plan_by_id",
            return_value={"id": "plan-1", "position_id": None, "status": "draft"},
        )
        self._patch(
            "routers.trade_plans.update_trade_plan",
            return_value={"id": "plan-1", "position_id": None, "status": "draft", "setup_thesis": "updated"},
        )

        resp = self.client.put("/trade-plans/plan-1", json={"setup_thesis": "updated"})

        assert resp.status_code == 200


class TestCreatePlanActiveStatusRequiresPosition:
    """routers/trade_plans.py::create_plan() -- same active-status-requires-
    position rule as update_plan(), applied at creation time (found during
    agent-mediated Data Model Owner review of ST-03: the original delegation
    only covered the PUT path, but POST /trade-plans accepted status='active'
    with no position_id just as readily)."""

    def setup_method(self):
        from fastapi.testclient import TestClient
        import main as _main
        self.client = TestClient(_main.app, raise_server_exceptions=False)
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, target, **kwargs):
        p = patch(target, **kwargs)
        self._patches.append(p)
        return p.start()

    def _install_common_mocks(self):
        self._patch("routers.trade_plans.ensure_trade_plans_table", return_value=None)
        self._patch("routers.trade_plans.ensure_si02_trade_plans_columns", return_value=None)
        self._patch("routers.trade_plans.ensure_strategy_version_at_entry_columns", return_value=None)
        self._patch("routers.trade_plans.get_portfolio", return_value={"id": "portfolio-1"})

    def test_create_with_active_status_and_no_position_id_returns_400(self):
        self._install_common_mocks()
        mock_create = self._patch("routers.trade_plans.create_trade_plan")

        resp = self.client.post(
            "/trade-plans",
            json={"ticker": "AAPL", "market": "US", "status": "active"},
        )

        assert resp.status_code == 400
        assert "position_id" in resp.json()["message"]
        mock_create.assert_not_called()

    def test_create_with_active_status_and_position_id_succeeds(self):
        self._install_common_mocks()
        self._patch(
            "routers.trade_plans.create_trade_plan",
            return_value={"id": "plan-new", "status": "active", "position_id": "pos-1", "ticker": "AAPL", "market": "US"},
        )

        resp = self.client.post(
            "/trade-plans",
            json={"ticker": "AAPL", "market": "US", "status": "active", "position_id": "pos-1"},
        )

        assert resp.status_code == 201

    def test_create_with_default_draft_status_unaffected(self):
        """Regression guard: the default status='draft' path (no status
        supplied at all) must be entirely unaffected by this guard."""
        self._install_common_mocks()
        self._patch(
            "routers.trade_plans.create_trade_plan",
            return_value={"id": "plan-new", "status": "draft", "position_id": None, "ticker": "AAPL", "market": "US"},
        )

        resp = self.client.post("/trade-plans", json={"ticker": "AAPL", "market": "US"})

        assert resp.status_code == 201


class TestEnsureTradePlansActiveRequiresPositionConstraint:
    """backend/database.py::ensure_trade_plans_active_requires_position_constraint()
    -- the paired DB-level CHECK constraint (defense-in-depth)."""

    def test_issues_idempotent_drop_then_add_constraint_not_valid(self):
        sys.modules.pop("database", None)
        import database

        mock_cursor = __import__("unittest.mock", fromlist=["MagicMock"]).MagicMock()
        mock_cursor.__enter__ = lambda s: mock_cursor
        mock_cursor.__exit__ = lambda s, *a: False
        mock_conn = __import__("unittest.mock", fromlist=["MagicMock"]).MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = lambda s: mock_conn
        mock_conn.__exit__ = lambda s, *a: False

        with patch.object(database, "get_db", return_value=mock_conn):
            database.ensure_trade_plans_active_requires_position_constraint()

        executed = [c.args[0] for c in mock_cursor.execute.call_args_list]
        assert any("DROP CONSTRAINT IF EXISTS trade_plans_active_requires_position_check" in s for s in executed)
        add_stmt = next(s for s in executed if "ADD CONSTRAINT trade_plans_active_requires_position_check" in s)
        assert "CHECK (status != 'active' OR position_id IS NOT NULL)" in add_stmt
        assert "NOT VALID" in add_stmt
        mock_conn.commit.assert_called_once()
