"""
N+1 query audit — GET /positions lifecycle refresh (ST-11, BLG-BE-90,
EPIC-04, v8.7).

Before this story: get_lifecycle_fields_for_position() (called once per
position by GET /positions' loop, see main.py) always called
refresh_position_lifecycle(position_id), which unconditionally re-fetched
the full row via get_position_by_id() -- even though the caller already had
the exact same row in hand (get_positions_with_prices() already did the
bulk SELECT). For a list of N positions, this meant 1 list query + N
redundant single-row re-fetches (a clearly-attributable N+1).

Fix: refresh_position_lifecycle() accepts an optional prefetched_position
dict and skips the re-fetch when given one; get_lifecycle_fields_for_position()
now always passes the position dict it already received.

These tests confirm the fix at both layers:
  1. refresh_position_lifecycle() with prefetched_position never calls
     get_position_by_id().
  2. get_lifecycle_fields_for_position() (the actual per-position call site
     in the /positions loop) results in zero get_position_by_id() calls.
  3. Without prefetched_position, behaviour is unchanged (still fetches).
"""
import sys
from pathlib import Path
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.position_lifecycle_service as lifecycle_service  # noqa: E402


def _raw_position_row(position_id="pos-1", position_state="PROFITABLE", atr=2.0):
    """A SELECT *-shaped row, same fields refresh_position_lifecycle() reads,
    tuned so compute_position_state() returns the same state already stored
    (no transition -> the "state unchanged" branch, the simplest path)."""
    entry_date = (date.today() - timedelta(days=30)).isoformat()
    return {
        "id": position_id,
        "entry_price": 100.0,
        "current_price_native": 103.0,  # > entry + 0.5*atr(2.0)=101 -> PROFITABLE
        "atr": atr,
        "entry_date": entry_date,
        "initial_stop": 90.0,
        "position_state": position_state,
        "state_history": [{"state": position_state, "entered_at": "2026-01-01T00:00:00"}],
        "state_entered_at": "2026-01-01T00:00:00",
    }


class TestRefreshPositionLifecyclePrefetch:
    def test_prefetched_position_skips_get_position_by_id(self):
        row = _raw_position_row()
        with patch.object(lifecycle_service, "get_position_by_id") as mock_get, \
             patch.object(lifecycle_service, "update_position_lifecycle_state") as mock_update:
            result = lifecycle_service.refresh_position_lifecycle("pos-1", prefetched_position=row)

        mock_get.assert_not_called()
        # State unchanged (PROFITABLE -> PROFITABLE) and state_entered_at
        # already set -> no UPDATE needed either, matching pre-fix behaviour
        # for this same state-unchanged case.
        mock_update.assert_not_called()
        assert result["position_state"] == "PROFITABLE"

    def test_without_prefetch_still_fetches_unchanged_behaviour(self):
        row = _raw_position_row()
        with patch.object(lifecycle_service, "get_position_by_id", return_value=row) as mock_get, \
             patch.object(lifecycle_service, "update_position_lifecycle_state") as mock_update:
            result = lifecycle_service.refresh_position_lifecycle("pos-1")

        mock_get.assert_called_once_with("pos-1")
        assert result["position_state"] == "PROFITABLE"

    def test_prefetch_state_transition_still_persists_via_update(self):
        """The prefetch optimisation only skips the redundant SELECT -- a
        genuine state transition still triggers the real UPDATE call
        (legitimate work, not N+1 waste)."""
        row = _raw_position_row(position_state="LOSING")  # stored=LOSING, computed=PROFITABLE -> transition
        with patch.object(lifecycle_service, "get_position_by_id") as mock_get, \
             patch.object(lifecycle_service, "update_position_lifecycle_state", return_value={"position_state": "PROFITABLE"}) as mock_update:
            lifecycle_service.refresh_position_lifecycle("pos-1", prefetched_position=row)

        mock_get.assert_not_called()
        mock_update.assert_called_once()
        args = mock_update.call_args.args
        assert args[0] == "pos-1"
        assert args[1] == "PROFITABLE"


class TestGetLifecycleFieldsForPositionNoLongerRefetches:
    def test_zero_get_position_by_id_calls_for_a_list_of_positions(self):
        """End-to-end simulation of the GET /positions loop: N positions,
        each already carrying position_state/state_history/state_entered_at
        (as get_positions_with_prices() now includes) -> zero additional
        get_position_by_id() calls across the whole list (was N before this
        fix)."""
        positions = [_raw_position_row(position_id=f"pos-{i}") for i in range(5)]

        with patch.object(lifecycle_service, "get_position_by_id") as mock_get, \
             patch.object(lifecycle_service, "update_position_lifecycle_state") as mock_update:
            for pos in positions:
                lifecycle = lifecycle_service.get_lifecycle_fields_for_position(pos)
                assert lifecycle["position_state"] == "PROFITABLE"

        mock_get.assert_not_called()  # was called once per position (5x) before this fix
        mock_update.assert_not_called()  # no state transitions in this fixture
