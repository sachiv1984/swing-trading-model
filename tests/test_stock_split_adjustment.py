"""ST-27 (BLG-BE-223, EPIC-05, v9.18): a stock split on an open position.

Rule: strategy_rules.md §9.1 (v1.28). Data: data_model.md DS-42. Contract:
position_endpoints.md v2.23.0. Fixture: the design record's worked example
(docs/design/2026-11-18__release-v9.18/position-data-states/decision_record.md
§2.2): 10 shares at 200.00 USD, stop 180.00, 2:1 split on day D, price 104.00.

Slice ACs covered here:
  AC 2  a 2:1 split on day D raises no stop breach and no exit recommendation
        on day D (analyze, nightly, stop alert, risk-off, month-end paths)
  AC 3  after confirmation quantity x adjusted entry equals the original cost,
        and the stop is the original stop / ratio
  AC 4  the adjustment row records ratio, effective date and source; the
        original entry fields are unchanged
  AC 5  detection, suppression and the arithmetic, including a UK (.L) ticker
"""
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

BACKEND = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(BACKEND))

import utils.calculations as real_calcs  # noqa: E402
import services.position_service as position_service  # noqa: E402
import services.split_service as split_service  # noqa: E402
import services.signal_service as signal_service  # noqa: E402
from utils.pricing import parse_split_events  # noqa: E402
from utils.split_adjustments import (  # noqa: E402
    adjust_position_for_splits,
    split_factors,
    stored_units_for_split,
)

DAY_D = date.today()
CONFIRMED_AT = datetime(2026, 11, 23, 10, 0, tzinfo=timezone.utc)


def _us_position(**overrides):
    """MU: entry_price is stored in GBP (data_model_positions_dictionary.md v0.4),
    fill_price is the native entry, stops are native."""
    base = {
        "id": "pos-mu", "portfolio_id": "portfolio-1", "ticker": "MU", "market": "US",
        "entry_date": DAY_D - timedelta(days=30),
        "entry_price": 160.0, "fill_price": 200.0, "user_fill_price": None, "fx_rate": 1.25,
        "shares": 10.0, "initial_stop": 180.0, "current_stop": 180.0, "previous_stop": None,
        "atr": 4.0, "total_cost": 1601.2, "fees_paid": 1.2, "status": "open",
        "holding_days": 30, "current_price": 104.0, "risk_off_exit": False,
    }
    base.update(overrides)
    return base


def _uk_position(**overrides):
    base = {
        "id": "pos-vod", "portfolio_id": "portfolio-1", "ticker": "VOD.L", "market": "UK",
        "entry_date": DAY_D - timedelta(days=30),
        "entry_price": 2.00, "fill_price": 2.00, "user_fill_price": None, "fx_rate": 1.0,
        "shares": 1000.0, "initial_stop": 1.80, "current_stop": 1.80, "previous_stop": None,
        "atr": 0.04, "total_cost": 2019.95, "fees_paid": 19.95, "status": "open",
        "holding_days": 30, "current_price": 1.04, "risk_off_exit": False,
    }
    base.update(overrides)
    return base


def _pending(position_id="pos-mu", ratio=2.0, effective=DAY_D):
    return {"id": "split-1", "position_id": position_id, "ratio": ratio, "effective_date": effective,
            "source": "yahoo", "detected_at": datetime(2026, 11, 23, 22, 30, tzinfo=timezone.utc),
            "confirmed_at": None, "shares_before": None, "shares_after": None}


def _confirmed(position_id="pos-mu", ratio=2.0, before=10.0, after=20.0, effective=DAY_D):
    row = _pending(position_id, ratio, effective)
    row.update(confirmed_at=CONFIRMED_AT, shares_before=before, shares_after=after)
    return row


def _with_pending(position, ratio=2.0):
    return adjust_position_for_splits(position, [_pending(position["id"], ratio)])


# ---------------------------------------------------------------------------
# Detection source: Yahoo chart split events
# ---------------------------------------------------------------------------

def _ts(d):
    return int(datetime(d.year, d.month, d.day, 14, 30, tzinfo=timezone.utc).timestamp())


class TestParseSplitEvents:
    def test_forward_reverse_and_odd_ratios(self):
        since = date(2026, 1, 1)
        events = {
            "a": {"date": _ts(date(2026, 6, 10)), "numerator": 2, "denominator": 1},
            "b": {"date": _ts(date(2026, 3, 2)), "numerator": 1, "denominator": 10},
            "c": {"date": _ts(date(2026, 9, 1)), "numerator": 3, "denominator": 2},
        }
        out = parse_split_events(events, since)
        assert [(e["effective_date"], e["ratio"]) for e in out] == [
            (date(2026, 3, 2), 0.1), (date(2026, 6, 10), 2.0), (date(2026, 9, 1), 1.5),
        ]

    def test_only_splits_after_the_entry_date_count(self):
        # §9.1 (ruling 2026-11-23): a position bought on the ex-date is already
        # post-split, so a split effective on the entry date is ignored.
        since = date(2026, 6, 10)
        events = {"old": {"date": _ts(date(2026, 6, 9)), "numerator": 2, "denominator": 1},
                  "same": {"date": _ts(date(2026, 6, 10)), "numerator": 4, "denominator": 1},
                  "next": {"date": _ts(date(2026, 6, 11)), "numerator": 3, "denominator": 1}}
        assert [e["ratio"] for e in parse_split_events(events, since)] == [3.0]

    @pytest.mark.parametrize("bad", [
        {"date": None, "numerator": 2, "denominator": 1},
        {"date": 1, "numerator": 0, "denominator": 1},
        {"date": 1, "numerator": 2, "denominator": 0},
        {"date": 1, "numerator": 1, "denominator": 1},
        {"date": 1, "numerator": "x", "denominator": 1},
    ])
    def test_unusable_entries_are_skipped(self, bad):
        assert parse_split_events({"e": bad}, date(1969, 12, 31)) == []

    def test_empty(self):
        assert parse_split_events({}, date(2026, 1, 1)) == []


class TestDetection:
    def _run(self, positions, history):
        create = MagicMock(return_value=True)
        with patch.object(split_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(split_service, "get_positions", return_value=positions), \
             patch.object(split_service, "get_split_history", side_effect=history), \
             patch.object(split_service, "create_pending_split_adjustment", create):
            return split_service.detect_position_splits(), create

    def test_new_split_is_recorded_as_pending_with_ratio_date_and_source(self):
        summary, create = self._run([_us_position()], lambda t, m, since: [{"effective_date": DAY_D, "ratio": 2.0}])
        create.assert_called_once_with("pos-mu", 2.0, DAY_D, "yahoo")
        assert summary["detected"] == 1
        assert summary["pending"] == [{"ticker": "MU", "ratio": "2:1", "effective_date": str(DAY_D)}]

    def test_history_is_read_from_the_entry_date_with_the_market(self):
        seen = []
        self._run([_uk_position()], lambda t, m, since: seen.append((t, m, since)) or [])
        assert seen == [("VOD.L", "UK", DAY_D - timedelta(days=30))]

    def test_a_split_already_recorded_is_not_recorded_again(self):
        for row in (_pending("pos-mu"), _confirmed("pos-mu")):
            pos = adjust_position_for_splits(_us_position(), [row])
            _, create = self._run([pos], lambda t, m, since: [{"effective_date": DAY_D, "ratio": 2.0}])
            create.assert_not_called()

    def test_a_failed_lookup_is_reported_not_read_as_no_split(self):
        summary, create = self._run([_us_position()], lambda t, m, since: None)
        assert summary["failed"] == ["MU"] and summary["detected"] == 0
        create.assert_not_called()

    def test_never_raises_when_positions_cannot_be_read(self):
        with patch.object(split_service, "get_portfolio", side_effect=RuntimeError("db down")):
            assert split_service.detect_position_splits()["error"] == "positions unavailable"


# ---------------------------------------------------------------------------
# Arithmetic (AC 3, AC 4)
# ---------------------------------------------------------------------------

class TestConfirmedAdjustmentOnRead:
    @pytest.mark.parametrize("make,native_entry_field", [(_us_position, "fill_price"), (_uk_position, "entry_price")])
    def test_quantity_times_adjusted_entry_is_the_original_cost_and_stop_is_halved(self, make, native_entry_field):
        stored = make()
        before = stored["shares"]
        adjusted = adjust_position_for_splits(stored, [_confirmed(stored["id"], 2.0, before, before * 2)])
        assert adjusted["shares"] == before * 2
        assert adjusted["shares"] * adjusted[native_entry_field] == pytest.approx(before * stored[native_entry_field])
        assert adjusted["initial_stop"] == pytest.approx(stored["initial_stop"] / 2)
        assert adjusted["total_cost"] == stored["total_cost"]  # cost unchanged for a whole count

    def test_original_entry_fields_are_unchanged_and_kept(self):
        stored = _us_position()
        snapshot = dict(stored)
        adjusted = adjust_position_for_splits(stored, [_confirmed()])
        assert stored == snapshot  # the input row is not modified
        assert adjusted["split_original"]["fill_price"] == 200.0
        assert adjusted["split_original"]["shares"] == 10.0
        assert adjusted["split_original"]["initial_stop"] == 180.0
        assert adjusted["split_adjustments"][0]["ratio"] == 2.0
        assert adjusted["split_adjustments"][0]["source"] == "yahoo"
        assert adjusted["split_adjustments"][0]["effective_date"] == DAY_D

    def test_pending_rows_are_not_applied(self):
        adjusted = _with_pending(_us_position())
        assert adjusted["shares"] == 10.0 and adjusted["fill_price"] == 200.0
        assert adjusted["split_pending"]["id"] == "split-1"
        assert "split_factors" not in adjusted

    def test_two_splits_compound(self):
        f = split_factors([_confirmed(ratio=2.0, before=10, after=20, effective=date(2026, 1, 1)),
                           _confirmed(ratio=3.0, before=20, after=60, effective=date(2026, 6, 1))])
        assert f == {"price_factor": 6.0, "shares_factor": 6.0, "cost_factor": 1.0}

    def test_reverse_split(self):
        adjusted = adjust_position_for_splits(_us_position(shares=100.0), [_confirmed(ratio=0.1, before=100, after=10)])
        assert adjusted["shares"] == 10.0
        assert adjusted["fill_price"] == pytest.approx(2000.0)
        assert adjusted["initial_stop"] == pytest.approx(1800.0)

    def test_odd_lot_entry_divides_by_ratio_and_cost_moves(self):
        # 3:2 on 7 shares = 10.5; the user enters 10 (0.5 paid as cash in lieu).
        stored = _uk_position(shares=7.0, entry_price=3.0, fill_price=3.0, total_cost=31.0, fees_paid=10.0, initial_stop=2.7)
        adjusted = adjust_position_for_splits(stored, [_confirmed("pos-vod", 1.5, 7.0, 10.0)])
        assert adjusted["shares"] == 10.0
        assert adjusted["entry_price"] == pytest.approx(2.0)
        assert adjusted["initial_stop"] == pytest.approx(1.8)
        # share cost 21.00 x (10 / 10.5) + fees 10.00
        assert adjusted["total_cost"] == pytest.approx(21.0 * 10 / 10.5 + 10.0, abs=0.01)

    def test_partial_exit_writes_back_in_stored_units(self):
        adjusted = adjust_position_for_splits(_us_position(), [_confirmed()])
        assert stored_units_for_split(adjusted, {"shares": 15.0, "total_cost": 1200.0, "fees_paid": 0.9}) == \
            {"shares": 7.5, "total_cost": 1200.0, "fees_paid": 0.9}

    def test_no_adjustment_no_conversion(self):
        assert stored_units_for_split(_us_position(), {"shares": 4}) == {"shares": 4}


class TestPreviewMatchesTheWorkedExample:
    def test_us_preview(self):
        p = split_service.split_preview(_with_pending(_us_position()), live_fx_rate=1.3)
        assert p["ratio_label"] == "2:1" and p["shares_after_is_whole"] is True
        assert (p["shares_before"], p["shares_after"]) == (10.0, 20.0)
        assert (p["entry_before"], p["entry_after"]) == (200.0, 100.0)
        assert (p["stop_before"], p["stop_after"]) == (180.0, 90.0)
        assert p["cost_before"] == p["cost_after"] == 2000.0

    def test_uk_preview(self):
        p = split_service.split_preview(_with_pending(_uk_position()))
        assert (p["entry_before"], p["entry_after"]) == (2.0, 1.0)
        assert (p["stop_before"], p["stop_after"]) == (1.8, 0.9)
        assert p["cost_before"] == p["cost_after"] == 2000.0

    def test_non_whole_leaves_shares_after_for_the_user(self):
        p = split_service.split_preview(_with_pending(_uk_position(shares=7.0), ratio=1.5))
        assert p["ratio_label"] == "3:2"
        assert p["shares_after"] is None and p["shares_after_exact"] == 10.5 and p["cost_after"] is None

    def test_no_pending_no_preview(self):
        assert split_service.split_preview(_us_position()) is None


# ---------------------------------------------------------------------------
# Confirmation
# ---------------------------------------------------------------------------

class TestConfirm:
    def _confirm(self, position, shares=None, ok=True):
        confirm_db = MagicMock(return_value=ok)
        reread = adjust_position_for_splits(position, [_confirmed(position["id"], float(position["split_pending"]["ratio"]),
                                                                    position["shares"], position["shares"] * float(position["split_pending"]["ratio"]))])
        with patch.object(split_service, "get_position_by_id", side_effect=[position, reread]), \
             patch.object(split_service, "confirm_split_adjustment", confirm_db):
            result = split_service.confirm_split(position["id"], shares=shares)
        return result, confirm_db

    def test_rescales_live_stop_and_atr_and_records_share_counts(self):
        result, confirm_db = self._confirm(_with_pending(_us_position(previous_stop=175.0)))
        adj_id, pos_id, before, after, updates = confirm_db.call_args.args
        assert (adj_id, pos_id, before, after) == ("split-1", "pos-mu", 10.0, 20.0)
        # current_price moves with the stop: nothing wrote it while pending.
        assert updates == {"current_stop": 90.0, "previous_stop": 87.5, "atr": 2.0, "current_price": 52.0}
        assert result["shares_after"] == 20.0
        assert result["entry_price"] == pytest.approx(100.0)
        assert result["initial_stop"] == pytest.approx(90.0)

    def test_partial_exit_remainder_snaps_back_to_whole_shares(self):
        # 10 stored, 3:1 confirmed (30 shown); sell 10 -> 20 written as 6.6667
        # (DECIMAL(10,4)); re-read must be 20, not 20.0001.
        stored = _uk_position(shares=10.0)
        adjusted = adjust_position_for_splits(stored, [_confirmed("pos-vod", 3.0, 10.0, 30.0)])
        written = round(stored_units_for_split(adjusted, {"shares": 20.0})["shares"], 4)
        assert written == 6.6667
        reread = adjust_position_for_splits(dict(stored, shares=written), [_confirmed("pos-vod", 3.0, 10.0, 30.0)])
        assert reread["shares"] == 20.0

    def test_fractional_holdings_are_not_snapped(self):
        adjusted = adjust_position_for_splits(_uk_position(shares=5.125), [_confirmed("pos-vod", 2.0, 5.125, 10.25)])
        assert adjusted["shares"] == 10.25

    def test_entry_fields_are_not_in_the_update(self):
        _, confirm_db = self._confirm(_with_pending(_uk_position()))
        updates = confirm_db.call_args.args[4]
        assert not ({"shares", "entry_price", "fill_price", "initial_stop", "total_cost"} & set(updates))

    def test_non_whole_needs_the_count(self):
        with pytest.raises(split_service.SplitSharesError, match="not a whole number"):
            self._confirm(_with_pending(_uk_position(shares=7.0), ratio=1.5))
        _, confirm_db = self._confirm(_with_pending(_uk_position(shares=7.0), ratio=1.5), shares=10)
        assert confirm_db.call_args.args[3] == 10.0

    @pytest.mark.parametrize("shares", [0, -1, 12, "x"])
    def test_out_of_range_counts_are_refused(self, shares):
        with pytest.raises(split_service.SplitSharesError):
            self._confirm(_with_pending(_uk_position(shares=7.0), ratio=1.5), shares=shares)

    def test_whole_result_refuses_a_different_count(self):
        with pytest.raises(split_service.SplitSharesError, match="only accepted"):
            self._confirm(_with_pending(_us_position()), shares=19)
        _, confirm_db = self._confirm(_with_pending(_us_position()), shares=20)
        assert confirm_db.call_args.args[3] == 20.0

    def test_nothing_pending_is_a_conflict(self):
        with patch.object(split_service, "get_position_by_id", return_value=_us_position()):
            with pytest.raises(split_service.SplitNotPendingError):
                split_service.confirm_split("pos-mu")

    def test_already_confirmed_race_is_a_conflict(self):
        with pytest.raises(split_service.SplitNotPendingError):
            self._confirm(_with_pending(_us_position()), ok=False)


# ---------------------------------------------------------------------------
# Suppression on day D (AC 2)
# ---------------------------------------------------------------------------

def _settings():
    return [{"uk_commission": 9.95, "us_commission": 0, "stamp_duty_rate": 0.005, "fx_fee_rate": 0.0015}]


class _Patcher:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, target, name, **kwargs):
        p = patch.object(target, name, **kwargs)
        self._patches.append(p)
        return p.start()


class TestNoExitOnDayD(_Patcher):
    def _analyze(self, position, risk_on=True):
        ps = position_service
        self._patch(ps, "get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(ps, "get_positions", return_value=[position])
        self._patch(ps, "get_settings", return_value=_settings())
        self._patch(ps, "get_live_fx_rate", return_value=1.3)
        self._patch(ps, "get_current_price", return_value=104.0)
        self._patch(ps, "calculate_atr", return_value=2.0)
        self._patch(ps, "check_market_regime", return_value={"spy_risk_on": risk_on, "ftse_risk_on": risk_on})
        update = self._patch(ps, "update_position")
        return ps.analyze_positions(), update

    def test_control_without_the_split_state_104_against_180_is_an_exit(self):
        result, _ = self._analyze(_us_position())
        assert result["actions"][0]["action"] == "EXIT"
        assert result["actions"][0]["exit_reason"] == "Stop Loss Hit"

    @pytest.mark.parametrize("risk_on", [True, False])
    def test_pending_split_holds_and_writes_nothing(self, risk_on):
        result, update = self._analyze(_with_pending(_us_position()), risk_on=risk_on)
        action = result["actions"][0]
        assert action["action"] == "HOLD" and action["exit_reason"] is None
        assert action["split_pending"] is True
        assert result["summary"]["exit_count"] == 0
        update.assert_not_called()

    def test_uk_pending_split_holds(self):
        position = _with_pending(_uk_position())
        ps = position_service
        self._patch(ps, "get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(ps, "get_positions", return_value=[position])
        self._patch(ps, "get_settings", return_value=_settings())
        self._patch(ps, "get_live_fx_rate", return_value=1.3)
        self._patch(ps, "get_current_price", return_value=1.04)
        self._patch(ps, "calculate_atr", return_value=0.02)
        self._patch(ps, "check_market_regime", return_value={"spy_risk_on": True, "ftse_risk_on": True})
        self._patch(ps, "update_position")
        assert ps.analyze_positions()["actions"][0]["action"] == "HOLD"

    def test_nightly_skips_the_recompute(self):
        ps = position_service
        self._patch(ps, "get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(ps, "get_positions", return_value=[_with_pending(_us_position())])
        self._patch(ps, "get_live_fx_rate", return_value=1.3)
        price = self._patch(ps, "get_current_price", return_value=104.0)
        atr = self._patch(ps, "calculate_atr", return_value=2.0)
        update = self._patch(ps, "update_position")
        result = ps.run_nightly_trailing_stop_update()
        assert result["results"] == [{"ticker": "MU", "market": "US", "status": "skipped", "reason": "split to confirm"}]
        update.assert_not_called()
        price.assert_not_called()
        atr.assert_not_called()

    def test_risk_off_flag_is_cleared_while_pending(self):
        ps = position_service
        self._patch(ps, "get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(ps, "get_positions", return_value=[_with_pending(_us_position()), _us_position(id="pos-2")])
        self._patch(ps, "check_market_regime", return_value={"spy_risk_on": False, "ftse_risk_on": True})
        flag = MagicMock()
        with patch("database.update_positions_risk_off_exit", flag):
            result = ps.run_nightly_risk_off_alerts()
        assert sorted(c.args for c in flag.call_args_list) == [("pos-2", True), ("pos-mu", False)]
        assert result["us_positions_flagged"] == 1
        assert result["us_positions_cleared"] == 1

    def test_exit_is_refused_while_pending(self):
        ps = position_service
        self._patch(ps, "get_portfolio", return_value={"id": "portfolio-1", "cash": 1000.0})
        self._patch(ps, "get_positions", return_value=[_with_pending(_us_position())])
        trade = self._patch(ps, "create_trade_history")
        with pytest.raises(ValueError, match="waiting for confirmation"):
            ps.exit_position("pos-mu", exit_price=104.0, exit_fx_rate=1.3)
        trade.assert_not_called()


class TestMonthEndSkipsPending(_Patcher):
    def test_rebalance_exit_not_generated_for_a_pending_split(self):
        src = Path(signal_service.__file__).read_text()
        start = src.index("def generate_rebalance_exit_signals")
        body = src[start:start + 6000]
        assert "if pos.get('split_pending'):" in body
        assert body.index("if pos.get('split_pending'):") < body.index("create_rebalance_exit_signal(")


class TestStopAlertSkipsPending:
    def test_pending_ids_lookup_fails_open(self):
        from services import alerts_service
        with patch("database.get_pending_split_position_ids", side_effect=RuntimeError("no table")):
            assert alerts_service._pending_split_ids("portfolio-1", conn=None) == set()

    def test_stop_loss_approach_loop_skips_pending_ids(self):
        from services import alerts_service
        src = Path(alerts_service.__file__).read_text()
        loop = src[src.index("# --- stop_loss_approach ---"):src.index("# --- grace_period_warning ---")]
        assert 'if str(pos["id"]) in split_pending_ids:' in loop


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

from fastapi.testclient import TestClient  # noqa: E402
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)
CONFIRM_URL = "/positions/00000000-0000-0000-0000-000000000000/split-adjustment/confirm"


class TestConfirmEndpoint:
    def test_200_with_the_confirmed_figures(self):
        data = {"position_id": "p", "ratio": 2.0, "ratio_label": "2:1", "shares_after": 20.0}
        with patch.object(main, "confirm_split", return_value=data) as confirm:
            r = CLIENT.post(CONFIRM_URL)
        assert r.status_code == 200 and r.json() == {"status": "ok", "data": data}
        assert confirm.call_args.kwargs == {"shares": None}

    def test_shares_are_passed_through(self):
        with patch.object(main, "confirm_split", return_value={}) as confirm:
            CLIENT.post(CONFIRM_URL, json={"shares": 10})
        assert confirm.call_args.kwargs == {"shares": 10.0}

    def test_409_when_nothing_is_pending(self):
        with patch.object(main, "confirm_split", side_effect=split_service.SplitNotPendingError("This position has no split to confirm")):
            r = CLIENT.post(CONFIRM_URL)
        assert r.status_code == 409 and r.json()["detail"] == "This position has no split to confirm"

    def test_400_for_a_bad_share_count(self):
        with patch.object(main, "confirm_split", side_effect=split_service.SplitSharesError("shares must be greater than 0")):
            r = CLIENT.post(CONFIRM_URL, json={"shares": 0})
        assert r.status_code == 400

    def test_exit_while_pending_is_409(self):
        with patch.object(main, "exit_position", side_effect=ValueError(position_service.SPLIT_PENDING_EXIT_ERROR)):
            r = CLIENT.post("/positions/00000000-0000-0000-0000-000000000000/exit", json={"exit_price": 104.0, "exit_fx_rate": 1.3})
        assert r.status_code == 409

    def test_nightly_run_detects_splits_before_the_recompute(self):
        order = []
        with patch.object(main, "detect_position_splits", side_effect=lambda: order.append("detect") or {"detected": 1}), \
             patch.object(main, "run_nightly_trailing_stop_update", side_effect=lambda: order.append("recompute") or {"results": []}), \
             patch.object(main, "record_nightly_job"):
            r = CLIENT.post("/positions/nightly-stop-update")
        assert r.status_code == 200 and order == ["detect", "recompute"]
        assert r.json()["data"]["splits"] == {"detected": 1}


class TestReviewFollowUps(_Patcher):
    """High code review of ST-27 (2026-11-23)."""

    def test_analyze_detects_a_split_before_comparing_prices(self):
        # Ex-date load before the nightly run: the first read has no pending
        # split; detection records one and the path re-reads.
        ps = position_service
        reads = [[_us_position()], [_with_pending(_us_position())]]
        self._patch(ps, "get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(ps, "get_positions", side_effect=lambda *a, **k: reads.pop(0))
        detect = self._patch(ps, "ensure_splits_detected", return_value=True)
        self._patch(ps, "get_settings", return_value=_settings())
        self._patch(ps, "get_live_fx_rate", return_value=1.3)
        self._patch(ps, "get_current_price", return_value=104.0)
        self._patch(ps, "calculate_atr", return_value=2.0)
        self._patch(ps, "check_market_regime", return_value={"spy_risk_on": True, "ftse_risk_on": True})
        update = self._patch(ps, "update_position")
        result = ps.analyze_positions()
        detect.assert_called_once()
        assert result["actions"][0]["action"] == "HOLD"
        update.assert_not_called()

    def test_pending_position_is_valued_in_pre_split_units(self):
        # UK: 1000 shares at 2.00, 2:1 pending, live 1.04 -> pre-split 2.08:
        # P&L (2.08 - 2.00) x 1000 = 80, not (1.04 - 2.00) x 1000 = -960.
        ps = position_service
        self._patch(ps, "get_portfolio", return_value={"id": "portfolio-1"})
        self._patch(ps, "get_positions", return_value=[_with_pending(_uk_position())])
        self._patch(ps, "ensure_splits_detected", return_value=False)
        self._patch(ps, "get_settings", return_value=_settings())
        self._patch(ps, "get_live_fx_rate", return_value=1.3)
        self._patch(ps, "get_current_price", return_value=1.04)
        self._patch(ps, "calculate_atr", return_value=0.02)
        self._patch(ps, "check_market_regime", return_value={"spy_risk_on": True, "ftse_risk_on": True})
        self._patch(ps, "update_position")
        action = ps.analyze_positions()["actions"][0]
        assert action["pnl"] == pytest.approx(80.0)

    def test_valuation_price(self):
        from utils.split_adjustments import valuation_price
        assert valuation_price(_us_position(), 104.0) == 104.0
        assert valuation_price(_with_pending(_us_position()), 104.0) == 208.0
        assert valuation_price(_with_pending(_us_position(), ratio=0.1), 50.0) == pytest.approx(5.0)
        assert valuation_price(_with_pending(_us_position()), None) is None

    def test_lifecycle_is_not_recomputed_while_pending(self):
        from services import position_lifecycle_service as lc
        refresh = self._patch(lc, "refresh_position_lifecycle")
        pos = dict(_with_pending(_us_position()), position_state="PROFITABLE",
                   state_entered_at="2026-11-01T00:00:00")
        fields = lc.get_lifecycle_fields_for_position(pos)
        refresh.assert_not_called()
        assert fields["position_state"] == "PROFITABLE"
        assert fields["state_entered_at"] == "2026-11-01T00:00:00"


class _FakeCursor:
    def __init__(self, row):
        self.row = row
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False
    def execute(self, *a, **k):
        pass
    def fetchone(self):
        return self.row


class _FakeConn:
    def __init__(self, row):
        self.row = row
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False
    def cursor(self):
        return _FakeCursor(self.row)


class TestStopTrail:
    def _get(self, row, live=180.0, fx=1.25):
        import database as real_db
        with patch.object(main, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(real_db, "get_db", lambda: _FakeConn(row)), \
             patch.object(main, "apply_split_adjustments", side_effect=lambda cur, rows: rows), \
             patch.object(main, "get_current_price", return_value=live), \
             patch.object(main, "get_live_fx_rate", return_value=fx), \
             patch("database.log_trailing_stop_recommendation"):
            return CLIENT.get("/positions/pos-mu/stop-trail")

    def test_409_while_a_split_is_pending(self):
        row = dict(_with_pending(_us_position()), trade_plan_id=None, r_target=None)
        r = self._get(row)
        assert r.status_code == 409 and "waiting for confirmation" in r.json()["detail"]

    def test_us_trail_uses_the_native_entry(self):
        # BLG-BE-229: fill_price 200 (native), entry_price 160 (GBP), live 180:
        # the trade is losing in USD, so the initial multiplier applies and R uses 200 - 180 = 20.
        row = dict(_us_position(current_stop=150.0, initial_stop=180.0 - 0.0), trade_plan_id=None, r_target=None)
        row["initial_stop"] = 170.0
        r = self._get(row, live=180.0)
        assert r.status_code == 200, r.text
        data = r.json()["data"] if "data" in r.json() else r.json()
        expected, _, _ = real_calcs.calculate_trailing_stop(
            current_price=180.0, atr=4.0, is_profitable=False, current_stop=float("-inf"),
            entry_price=200.0, settings=__import__("strategy_parameters").stop_multiplier_settings())
        assert data["atr_trail_stop"] == pytest.approx(round(expected, 4))
        assert data["trail_r_terms"] == pytest.approx(round((round(expected, 4) - 150.0) / (200.0 - 170.0), 2))

    def test_uk_trail_is_unchanged(self):
        # BLG-BE-229 AC 2: UK entry_price is already native.
        row = dict(_uk_position(current_stop=1.70, initial_stop=1.60), trade_plan_id=None, r_target=None)
        r = self._get(row, live=2.20, fx=1.3)
        assert r.status_code == 200, r.text
        data = r.json()["data"] if "data" in r.json() else r.json()
        expected, _, _ = real_calcs.calculate_trailing_stop(
            current_price=2.20, atr=0.04, is_profitable=True, current_stop=float("-inf"),
            entry_price=2.00, settings=__import__("strategy_parameters").stop_multiplier_settings())
        assert data["atr_trail_stop"] == pytest.approx(round(expected, 4))
