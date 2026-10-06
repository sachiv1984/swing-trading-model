"""
ST-01 (BLG-BE-138, EPIC-01, v9.10): one source for the strategy_rules.md §11
stop parameters across the on-load and nightly stop paths.

Parameter-authority ruling (a), 2026-10-06 (ESC-EXEC-20261006-01): the §11
values are fixed, held in backend/strategy_parameters.py, and never read
from the editable settings row.

Covers:
  - Parity: for identical inputs, analyze_positions() and
    run_nightly_trailing_stop_update() store the same stop (profitable and
    losing cases).
  - Source sensitivity: give both paths a different parameter source and both
    stops move together. A path with its own copy of the multipliers would
    stay put and fail this test.
  - The settings row no longer influences the on-load stop (it used to).
  - Grace length, exit-decision default and calculation defaults all equal the
    source; the frontend display mirror (src/lib/strategyParameters.js)
    matches it.
  - Each path records stop_calculation_source ('on_load' / 'nightly', DS-26).
"""
import importlib.util
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parent.parent
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

_spec = importlib.util.spec_from_file_location("_real_calculations_st01", BACKEND / "utils" / "calculations.py")
real_calcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(real_calcs)

import services.position_service as position_service  # noqa: E402
import strategy_parameters as sp  # noqa: E402


def _position(**overrides):
    base = {
        "id": "pos-1", "portfolio_id": "portfolio-1", "ticker": "VOD.L", "market": "UK",
        "entry_date": date.today() - timedelta(days=30), "entry_price": 100.0, "fill_price": None,
        "fx_rate": 1.0, "shares": 10.0, "current_stop": 50.0, "initial_stop": 50.0, "atr": 4.0,
        "total_cost": 1000.0, "status": "open",
    }
    base.update(overrides)
    return base


class _Paths:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()

    def _common(self, position, price, settings_row=None):
        for name in ("calculate_trailing_stop", "calculate_holding_days", "calculate_position_pnl", "should_exit_position"):
            self._patch(name, new=getattr(real_calcs, name))
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[position])
        self._patch("get_settings", return_value=[settings_row] if settings_row else [])
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=price)
        self._patch("check_market_regime", return_value={"spy_risk_on": True, "ftse_risk_on": True})
        self._patch("calculate_atr", return_value=position["atr"])  # nightly fetches the same ATR

    def on_load_updates(self, position, price, settings_row=None):
        self._common(position, price, settings_row)
        mock_update = self._patch("update_position")
        position_service.analyze_positions()
        return mock_update.call_args.args[1]

    def nightly_updates(self, position, price):
        self._common(position, price)
        mock_update = self._patch("update_position")
        position_service.run_nightly_trailing_stop_update()
        return mock_update.call_args.args[1]


class TestOnLoadNightlyParity(_Paths):

    @pytest.mark.parametrize("price", [130.0, 90.0], ids=["profitable", "losing"])
    def test_same_stop_for_identical_inputs(self, price):
        on_load = self.on_load_updates(_position(), price)
        self.teardown_method(); self.setup_method()
        nightly = self.nightly_updates(_position(), price)
        assert on_load["current_stop"] == pytest.approx(nightly["current_stop"])
        assert on_load["active_atr_multiplier"] == pytest.approx(nightly["active_atr_multiplier"])

    def test_values_are_the_section_11_values(self):
        # Profitable: max(130 − 2×4, entry 100) = 122. Losing: 90 − 5×4 = 70.
        assert self.on_load_updates(_position(), 130.0)["current_stop"] == pytest.approx(122.0)
        self.teardown_method(); self.setup_method()
        assert self.nightly_updates(_position(), 90.0)["current_stop"] == pytest.approx(70.0)

    def test_both_paths_follow_a_changed_source(self):
        changed = {"atr_multiplier_initial": 3.0, "atr_multiplier_trailing": 1.0}
        self._patch("stop_multiplier_settings", return_value=changed)
        on_load = self.on_load_updates(_position(), 130.0)
        # The nightly path builds its settings inside the function call, so the
        # patch above is still active for it.
        nightly = self.nightly_updates(_position(), 130.0)
        assert on_load["current_stop"] == pytest.approx(126.0)  # 130 − 1×4
        assert nightly["current_stop"] == pytest.approx(126.0)


class TestSettingsRowIgnored(_Paths):

    def test_divergent_settings_row_does_not_change_the_on_load_stop(self):
        # The Settings form used to seed 2× initial / 3× trailing.
        row = {"atr_multiplier_initial": 2, "atr_multiplier_trailing": 3, "min_hold_days": 5}
        updates = self.on_load_updates(_position(), 130.0, settings_row=row)
        assert updates["current_stop"] == pytest.approx(122.0)
        assert updates["active_atr_multiplier"] == pytest.approx(sp.PROFIT_ATR_MULTIPLIER)

    def test_settings_row_min_hold_days_does_not_shorten_grace(self):
        row = {"min_hold_days": 5}
        updates = self.on_load_updates(_position(entry_date=date.today() - timedelta(days=7)), 130.0, settings_row=row)
        assert "stop_calculated_at" not in updates  # still in the 10-day grace period


class TestStopCalculationSource(_Paths):

    def test_on_load_records_on_load(self):
        assert self.on_load_updates(_position(), 130.0)["stop_calculation_source"] == "on_load"

    def test_nightly_records_nightly(self):
        assert self.nightly_updates(_position(), 130.0)["stop_calculation_source"] == "nightly"

    def test_in_grace_on_load_does_not_claim_a_recalculation(self):
        updates = self.on_load_updates(_position(entry_date=date.today() - timedelta(days=2)), 130.0)
        assert "stop_calculation_source" not in updates


class TestEveryPathUsesTheSource:

    def test_section_11_values(self):
        assert (sp.GRACE_PERIOD_DAYS, sp.INITIAL_ATR_MULTIPLIER, sp.PROFIT_ATR_MULTIPLIER, sp.ATR_PERIOD_DAYS) == (10, 5.0, 2.0, 14)

    def test_nightly_constants_alias_the_source(self):
        assert position_service._INITIAL_ATR_MULT == sp.INITIAL_ATR_MULTIPLIER
        assert position_service._PROFIT_ATR_MULT == sp.PROFIT_ATR_MULTIPLIER
        assert position_service._ATR_PERIOD == sp.ATR_PERIOD_DAYS

    def test_calculation_defaults(self):
        assert real_calcs.calculate_initial_stop(100, 4) == pytest.approx(100 - sp.INITIAL_ATR_MULTIPLIER * 4)
        assert real_calcs.should_exit_position(1, 100, sp.GRACE_PERIOD_DAYS - 1, True) == (False, None)
        assert real_calcs.should_exit_position(1, 100, sp.GRACE_PERIOD_DAYS, True)[0] is True

    def test_grace_service(self):
        spec = importlib.util.spec_from_file_location("_real_grace_st01", BACKEND / "services" / "grace_service.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert mod.compute_grace_days_remaining(True, 0) == sp.GRACE_PERIOD_DAYS

    def test_compliance_and_alerts_import_the_source(self):
        for rel in ("services/compliance_service.py", "services/alerts_service.py"):
            text = (BACKEND / rel).read_text()
            assert "from strategy_parameters import GRACE_PERIOD_DAYS" in text, rel
            assert not re.search(r"GRACE_PERIOD_DAYS\s*=\s*\d", text), rel
        assert "min_hold_days = GRACE_PERIOD_DAYS" in (BACKEND / "services/alerts_service.py").read_text()


class TestFrontendMirror:

    def test_mirror_matches_the_backend_source(self):
        text = (ROOT / "src" / "lib" / "strategyParameters.js").read_text()
        values = {k: float(v) for k, v in re.findall(r"export const (\w+) = ([\d.]+);", text)}
        assert values == {
            "GRACE_PERIOD_DAYS": sp.GRACE_PERIOD_DAYS,
            "ATR_PERIOD_DAYS": sp.ATR_PERIOD_DAYS,
            "INITIAL_ATR_MULTIPLIER": sp.INITIAL_ATR_MULTIPLIER,
            "PROFIT_ATR_MULTIPLIER": sp.PROFIT_ATR_MULTIPLIER,
        }
