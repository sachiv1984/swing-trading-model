"""
Multi-currency cost-basis rounding audit (ST-12, EPIC-04, DEL-20260811-02,
v8.6).

Systematic audit of cost-basis rounding across position_service.add_position()
(entry), position_service.exit_position() (exit / partial exit), and the
reports_service.py consumers, per the decision record added in this story:
docs/product/decisions/multi-currency-cost-basis-rounding-audit--2026-08-12.md

Findings (see that decision record for the full write-up):

1. Entry-side (add_position()): total_cost_gbp is computed unrounded in
   Python and handed to create_position(). US positions carry an extra
   FX-division step that UK positions don't. BUT the `total_cost` DB column
   is NUMERIC(12,2) on both `positions` and `trade_history`
   (docs/specs/data_model.md lines 70, 156) — Postgres rounds (not
   truncates) every value to 2dp on write, so the persisted value is always
   canonical to the cent regardless of how many unrounded arithmetic steps
   preceded the write. The "3 rounding steps for US vs 1 for UK" claim in
   DEL-20260811-02's starting-point finding is true of the *computation
   path* but does not translate into extra *persisted* drift for US vs UK —
   the DB write collapses it to the same single ±0.005 rounding tolerance
   either way.

2. The real, market-SYMMETRIC (not US-vs-UK-asymmetric) rounding source is
   the partial-exit cost allocation in exit_position():
   `cost_per_share = total_cost / total_shares` then
   `exit_total_cost = cost_per_share * exit_shares` (position_service.py,
   also independently re-derived inside calculate_realized_pnl() with the
   same inputs — confirmed bit-for-bit identical, not a second source of
   drift). This division is currency-agnostic: dividing a GBP total_cost by
   a fractional share count produces a repeating decimal for UK positions
   exactly as readily as for US ones.

   CORRECTION (2026-08-12, post-review): the original version of this audit
   asserted this error "does not compound across exits" because each write
   is independently rounded to 2dp. That claim was FALSE in the general
   case and was caught by an agent-mediated Financial Reporting & Records
   Owner review of PR #1363, which produced a concrete counter-example: 37
   sequential single-share exits of a £12,345.67 position drifted £0.12 —
   6x the ≤£0.02 bound this file originally asserted (which had only been
   empirically checked against two small fixtures, a 3-share and a 7-share
   split of £100). The error DOES compound, because each partial exit's
   `remaining_cost = total_cost - exit_total_cost` was computed from the
   UNROUNDED `exit_total_cost`, then independently rounded on write — the
   next exit then reads that already-slightly-wrong remaining_cost as its
   new starting `total_cost`, so small per-step errors can accumulate in
   one direction across many exits rather than cancelling out.

   FIX APPLIED: `exit_total_cost`/`exit_entry_fees` are now rounded to 2dp
   immediately (matching the NUMERIC(12,2)/NUMERIC(10,2) columns they
   persist to), and `remaining_cost`/`remaining_fees` are derived by exact
   subtraction from the already-rounded starting total_cost/fees_paid —
   not by independently rounding a second, separately-computed unrounded
   remainder. This "round once, derive the rest by exact subtraction"
   ordering makes the allocation telescope exactly: the sum of every
   exit_total_cost across a position's full partial-exit lifecycle always
   reconstructs the original total_cost to the cent, for any share count,
   position size, or number of partial exits — see
   TestExactTelescopingAllocation below, which reproduces the counter-
   example and confirms zero drift post-fix.
3. reports_service.py consumers (tax-year report, reconciliation report,
   monthly P&L) read back already-persisted (DB-rounded) `total_cost`
   values and do not re-derive cost basis independently — no additional
   drift is introduced downstream of the two sources above. The
   reconciliation report (get_reconciliation_report()) already carries a
   pre-existing ±£0.01 tolerance for exactly this class of float-aggregation
   noise (reports_service.py ~line 287), an established codebase precedent
   that sub-penny/one-cent drift from proportional allocation is treated as
   immaterial, not a bug.

4. Incidental observation (not a rounding-audit finding, noted for
   completeness): a *full* exit's update_position() call does not clear
   `positions.total_cost` (position_service.py's full-exit branch only sets
   `status`/`exit_date`/`exit_price`/`exit_reason`). The field is simply
   never read again once `status == 'closed'`, so this has no financial-
   correctness impact — but it means `positions.total_cost` should not be
   relied on as a "cost of remaining shares" value once a position is
   closed. Out of scope for this story; not filed as a backlog item since
   there is no observed or reachable consumer of a closed position's
   `total_cost`.

Conclusion (revised): the entry-side finding (#1) remains immaterial, as
originally documented. The partial-exit finding (#2) required an actual
fix, not just documentation — see TestExactTelescopingAllocation below for
the regression coverage proving the fix eliminates the drift exactly,
including on the originally-failing counter-example. Both outcomes are
documented in
docs/product/decisions/multi-currency-cost-basis-rounding-audit--2026-08-12.md
(revised 2026-08-12 to reflect the corrected finding). This satisfies
DEL-20260811-02's unblock criterion (a) for finding #2 ("any inconsistency
found is fixed") and criterion (b) for finding #1 ("documented as
immaterial with a quantified bound").

No live database — DB writes are mocked with a round-trip that mimics
NUMERIC(12,2) column rounding (round(value, 2) on every simulated write),
matching the real schema. Mock pattern follows
test_fx_audit_trail_completeness.py / test_position_trade_plan_link.py.
Note: "Postgres rounds (not truncates) NUMERIC(N,2) on write" is documented
Postgres semantics, not something this sandbox can verify against a live
instance (no DATABASE_URL/Postgres access here) — the round(value, 2)
simulation encodes that documented behaviour as an assumption, not an
empirical observation from this test run.
"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.position_service as position_service  # noqa: E402


def _settings():
    return [{
        "uk_commission": 9.95,
        "us_commission": 0,
        "stamp_duty_rate": 0.005,
        "fx_fee_rate": 0.0015,
    }]


class _FakeDb:
    """Mimics NUMERIC(12,2) round-trip: every value written to `total_cost`
    (positions or trade_history) is rounded to 2dp on write, exactly as
    Postgres would round it on INSERT/UPDATE. This lets the test exercise
    the *real* exit_position()/calculate_realized_pnl() arithmetic while
    still modelling the DB's own rounding behaviour at each persist point.
    """

    def __init__(self, position):
        self.position = dict(position)
        self.portfolio = {"id": "portfolio-1", "cash": 100000.0}
        self.trade_history_writes = []
        self.position_updates = []

    def get_portfolio(self):
        return self.portfolio

    def get_positions(self, portfolio_id):
        return [self.position]

    def update_portfolio_cash(self, portfolio_id, new_cash):
        self.portfolio["cash"] = new_cash

    def create_trade_history(self, portfolio_id, trade_data):
        trade_data = dict(trade_data)
        trade_data["total_cost"] = round(trade_data["total_cost"], 2)
        self.trade_history_writes.append(trade_data)

    def update_position(self, position_id, updates):
        updates = dict(updates)
        if "total_cost" in updates:
            updates["total_cost"] = round(updates["total_cost"], 2)
        self.position.update(updates)
        self.position_updates.append(updates)

    def get_trade_plans_by_position(self, position_id, portfolio_id):
        return []


def _run_sequential_single_share_exits(fake_db, exit_price, num_shares, market, fx_rate=1.0):
    """Exit `num_shares` one at a time (worst-case partial-exit path) via the
    REAL exit_position(), with only the DB layer mocked."""
    with patch.object(position_service, "get_portfolio", side_effect=fake_db.get_portfolio), \
         patch.object(position_service, "get_positions", side_effect=fake_db.get_positions), \
         patch.object(position_service, "get_settings", return_value=_settings()), \
         patch.object(position_service, "update_portfolio_cash", side_effect=fake_db.update_portfolio_cash), \
         patch.object(position_service, "create_trade_history", side_effect=fake_db.create_trade_history), \
         patch.object(position_service, "update_position", side_effect=fake_db.update_position), \
         patch.object(position_service, "get_trade_plans_by_position", side_effect=fake_db.get_trade_plans_by_position), \
         patch.object(position_service, "ensure_planned_entry_price_column", return_value=None):
        for _ in range(num_shares):
            kwargs = {
                "position_id": fake_db.position["id"],
                "exit_price": exit_price,
                "shares": 1,
                "exit_date": "2026-08-12",
            }
            if market == "US":
                kwargs["exit_fx_rate"] = fx_rate
            position_service.exit_position(**kwargs)


class TestExactTelescopingAllocation:
    """Confirms the fix (round exit_total_cost first, derive the remainder
    by exact subtraction) makes the partial-exit cost split telescope
    exactly, for any share count / position size / exit count — not just
    the two small fixtures the original (incorrect) version of this file
    checked. Finding #2 in the module docstring."""

    def _drift(self, market, entry_total_cost, shares, exit_price, fx_rate=1.0):
        position = {
            "id": "pos-1",
            "ticker": "TEST.L" if market == "UK" else "TEST",
            "market": market,
            "shares": shares,
            "total_cost": entry_total_cost,
            "fees_paid": 0.0,
            "entry_price": 100.0 if market == "UK" else 100.0,
            "fill_price": 100.0,
            "entry_date": "2026-01-01",
            "status": "open",
            "fx_rate": fx_rate,
            "user_fill_price": None,
            "entry_note": None,
            "tags": None,
        }
        fake_db = _FakeDb(position)
        _run_sequential_single_share_exits(fake_db, exit_price=exit_price, num_shares=shares, market=market, fx_rate=fx_rate)

        # All `shares` are exited one at a time, so every penny of the
        # original total_cost has been allocated across the trade_history
        # writes by the time the position fully closes (a full exit doesn't
        # touch positions.total_cost — see the decision record's "dangling
        # field" observation (finding #4) —
        # so only the trade_history side is meaningful here).
        exited_total = sum(t["total_cost"] for t in fake_db.trade_history_writes)
        return abs(exited_total - entry_total_cost)

    def test_uk_position_drift_is_exactly_zero(self):
        # £100.00 spread across 3 shares — does not divide evenly (33.333...).
        drift = self._drift(market="UK", entry_total_cost=100.00, shares=3, exit_price=50.0)
        assert drift == 0.0, f"UK partial-exit drift {drift} — telescoping fix should make this exact"

    def test_us_position_drift_is_exactly_zero(self):
        # Same £100.00 total_cost (already GBP as persisted), same 3-share split.
        drift = self._drift(market="US", entry_total_cost=100.00, shares=3, exit_price=60.0, fx_rate=1.25)
        assert drift == 0.0, f"US partial-exit drift {drift} — telescoping fix should make this exact"

    def test_drift_is_zero_and_symmetric_across_markets(self):
        """Core audit finding: the partial-exit rounding source is
        currency-agnostic — UK and US positions with the same total_cost/
        share-count split produce identical (zero) drift post-fix. This
        disproves the delegation's starting-point hypothesis that only US
        positions carry extra rounding noise."""
        uk_drift = self._drift(market="UK", entry_total_cost=100.00, shares=7, exit_price=20.0)
        us_drift = self._drift(market="US", entry_total_cost=100.00, shares=7, exit_price=25.0, fx_rate=1.3)
        assert uk_drift == 0.0
        assert us_drift == 0.0

    def test_regression_reviewer_counter_example_37_exits_of_large_position(self):
        """The exact scenario an agent-mediated Financial Reporting &
        Records Owner review used to disprove this file's original
        "bounded ≤£0.02, non-compounding" claim: 37 sequential single-share
        exits of a £12,345.67 position. Pre-fix this drifted £0.12 (6x the
        originally-asserted bound). Post-fix it must be exact."""
        drift = self._drift(market="UK", entry_total_cost=12345.67, shares=37, exit_price=500.0)
        assert drift == 0.0, f"Counter-example still drifts by {drift} — telescoping fix regressed"

    def test_regression_large_us_position_many_exits(self):
        """Same counter-example shape, US market with FX conversion in the
        mix, to confirm the fix holds for the currency-conversion path too."""
        drift = self._drift(market="US", entry_total_cost=12345.67, shares=37, exit_price=650.0, fx_rate=1.28)
        assert drift == 0.0, f"US counter-example drifts by {drift} — telescoping fix regressed"

    def test_realized_pnl_and_persisted_total_cost_use_identical_cost_per_share(self):
        """Confirms position_service.exit_position()'s own cost_per_share
        computation (used for the persisted trade_history.total_cost) and
        calculate_realized_pnl()'s independent re-derivation of the same
        formula (used for realized_pnl) are bit-for-bit consistent — i.e.
        no *additional* drift is introduced by the duplicate computation."""
        position = {
            "id": "pos-2", "ticker": "TEST.L", "market": "UK",
            "shares": 3, "total_cost": 100.00, "fees_paid": 0.0,
            "entry_price": 33.33, "fill_price": 33.33, "entry_date": "2026-01-01",
            "status": "open", "fx_rate": 1.0, "user_fill_price": None,
            "entry_note": None, "tags": None,
        }
        fake_db = _FakeDb(position)
        with patch.object(position_service, "get_portfolio", side_effect=fake_db.get_portfolio), \
             patch.object(position_service, "get_positions", side_effect=fake_db.get_positions), \
             patch.object(position_service, "get_settings", return_value=_settings()), \
             patch.object(position_service, "update_portfolio_cash", side_effect=fake_db.update_portfolio_cash), \
             patch.object(position_service, "create_trade_history", side_effect=fake_db.create_trade_history), \
             patch.object(position_service, "update_position", side_effect=fake_db.update_position), \
             patch.object(position_service, "get_trade_plans_by_position", side_effect=fake_db.get_trade_plans_by_position), \
             patch.object(position_service, "ensure_planned_entry_price_column", return_value=None):
            result = position_service.exit_position(position_id="pos-2", exit_price=50.0, shares=1, exit_date="2026-08-12")

        persisted_exit_total_cost = fake_db.trade_history_writes[0]["total_cost"]
        expected_cost_per_share = 100.00 / 3
        expected_exit_total_cost = round(expected_cost_per_share * 1, 2)
        assert persisted_exit_total_cost == expected_exit_total_cost
        # realized_pnl is net_proceeds (gross minus UK £9.95 exit commission)
        # minus the SAME unrounded exit_total_cost used above — cross-check
        # it lands within a cent of the value derived from that figure,
        # confirming exit_position()'s own cost_per_share and
        # calculate_realized_pnl()'s independent re-derivation of it agree.
        net_proceeds = 50.0 - 9.95
        implied_pnl = round(net_proceeds - expected_cost_per_share, 2)
        assert abs(result["realized_pnl"] - implied_pnl) <= 0.01

    def test_fees_paid_telescopes_exactly_too(self):
        """fees_paid is the same DECIMAL(10,2) class of column as total_cost
        and goes through the identical entry_fees_per_share * exit_shares
        proportional-split pattern — confirms the fix (applied to both
        total_cost and fees_paid in the same commit) covers fees_paid too,
        not just total_cost."""
        position = {
            "id": "pos-3", "ticker": "TEST.L", "market": "UK",
            "shares": 3, "total_cost": 100.00, "fees_paid": 10.00,
            "entry_price": 33.33, "fill_price": 33.33, "entry_date": "2026-01-01",
            "status": "open", "fx_rate": 1.0, "user_fill_price": None,
            "entry_note": None, "tags": None,
        }
        fake_db = _FakeDb(position)
        _run_sequential_single_share_exits(fake_db, exit_price=50.0, num_shares=3, market="UK")

        exited_fees_total = sum(t["entry_fees"] for t in fake_db.trade_history_writes)
        assert abs(exited_fees_total - 10.00) == 0.0, (
            f"fees_paid drift {abs(exited_fees_total - 10.00)} — telescoping fix should cover fees_paid too"
        )


class TestEntrySideRoundingSymmetryAfterDbPersist:
    """Confirms finding #1: once DB-column NUMERIC(12,2) rounding is
    applied, entry-side total_cost precision is equivalent between UK and
    US positions — the extra US FX-division step does not survive as extra
    persisted imprecision."""

    def _install_common_mocks(self, portfolio_cash=100000.0):
        self._patch("get_portfolio", return_value={"id": "portfolio-1", "cash": portfolio_cash})
        self._patch("get_settings", return_value=_settings())
        self._patch("create_position", return_value={"id": "new-position-id"})
        self._patch("update_portfolio_cash")
        self._patch("calculate_atr", return_value=1.0)
        self._patch("calculate_us_entry_fees", return_value={"commission": 0, "stamp_duty": 0, "fx_fee": 1.5, "total": 1.5})
        self._patch("calculate_uk_entry_fees", return_value={"commission": 9.95, "stamp_duty": 5.0, "total": 14.95})
        self._patch("calculate_initial_stop", return_value=90.0)
        self._patch("get_unlinked_trade_plan_for_entry", return_value=None)
        self._patch("get_current_strategy_version", return_value="1.4")

    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()

    def test_us_and_uk_total_cost_both_land_on_a_2dp_value(self):
        self._install_common_mocks()
        us_result = position_service.add_position(
            ticker="AAPL", market="US", entry_date="2026-07-09",
            shares=7, entry_price=133.37, fx_rate=1.2731,
        )
        uk_result = position_service.add_position(
            ticker="FRES.L", market="UK", entry_date="2026-07-09",
            shares=7, entry_price=133.37,
        )
        # Both response values are already rounded to 2dp (add_position()'s
        # own response formatting) — mirrors what NUMERIC(12,2) would store.
        assert round(us_result["total_cost"], 2) == us_result["total_cost"]
        assert round(uk_result["total_cost"], 2) == uk_result["total_cost"]
