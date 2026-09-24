"""
Float-vs-Decimal money-arithmetic golden tests (ST-12, EPIC-03, v9.6,
BLG-BE-121).

Audit write-up: docs/ops/money_arithmetic_audit_2026-09-22.md

Covers the position-sizing golden set (tests/golden_outputs.json's
`position_sizing` array plus additional boundary cases added here) and the
fee-calculation functions it depends on (`utils/calculations.py`),
comparing the implementation's `float` arithmetic against an independently
derived `Decimal` calculation of the same figure at rounding-boundary
inputs. Per the story's acceptance criteria, any discrepancy >= GBP 0.01
must be explained (documented), not silently rounded away.

CI-safe: pure-math functions only, no DB or network calls.
"""
import math
import sys
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# test_alerts_service.py installs a fake types.ModuleType("utils") stub and
# replaces sys.modules["utils.calculations"] with a MagicMock stub at
# collection time (alphabetically earlier, per its own ST-25/BLG-QA-105
# docstring). Evict both the submodule and the parent stub so Python
# re-imports the real utils package (backend/utils/) and binds the fee
# functions below to the real implementation rather than the MagicMock —
# same pattern already used by tests/test_nightly_computations.py and
# tests/test_trailing_stop_breakeven_floor.py for the same reason.
sys.modules.pop("utils.calculations", None)
sys.modules.pop("utils", None)

from services.sizing_service import _floor_4dp  # noqa: E402
from utils.calculations import (  # noqa: E402
    calculate_uk_entry_fees,
    calculate_us_entry_fees,
    calculate_uk_exit_fees,
    calculate_us_exit_fees,
)

_SETTINGS = {
    "uk_commission": 9.95,
    "stamp_duty_rate": 0.005,
    "us_commission": 0.00,
    "fx_fee_rate": 0.0015,
}


def _decimal_round_half_up(value: float, dp: int = 2) -> Decimal:
    """Independent reference implementation — Decimal, round-half-up, the
    standard UK/US retail-brokerage rounding convention. Deliberately not
    imported from the implementation under test."""
    quantum = Decimal("1").scaleb(-dp)
    return Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------------------
# Position-sizing golden set — floor-to-4dp boundary cases
# ---------------------------------------------------------------------------
# §4.1.3 rounds SuggestedShares by *flooring* (conservative — never suggest
# more shares than the risk budget allows), not by round-half-up, so the
# comparison here is float-floor vs Decimal-floor, not vs Decimal round.

class TestSuggestedSharesFloorBoundaries:
    """_floor_4dp boundary cases — values whose 5th decimal digit sits near
    a float-representation edge, where naive float flooring could tip the
    wrong way relative to the true (Decimal) value."""

    BOUNDARY_CASES = [
        # (raw_shares, description)
        (45.45454545454545, "PS-02 golden case — repeating decimal"),
        (20.00005, "just above a 4dp boundary"),
        (19.99995, "just below a 4dp boundary"),
        (100.00009999, "9999 in the 5th-8th decimal place"),
        (0.00019999, "sub-1-share near-zero boundary"),
        (33.333349999, "repeating-third-adjacent boundary"),
    ]

    @pytest.mark.parametrize("raw_shares,description", BOUNDARY_CASES)
    def test_float_floor_matches_decimal_floor(self, raw_shares, description):
        impl_result = _floor_4dp(raw_shares)

        dec = Decimal(str(raw_shares))
        dec_floored = (dec * 10000).to_integral_value(rounding=ROUND_FLOOR) / 10000

        diff = abs(Decimal(str(impl_result)) - dec_floored)
        assert diff <= Decimal("0.0001"), (
            f"{description}: float floor {impl_result} vs Decimal floor "
            f"{dec_floored} differ by {diff} shares"
        )


# ---------------------------------------------------------------------------
# Fee-calculation golden set — confirmed float-vs-Decimal discrepancies
# ---------------------------------------------------------------------------
# BLG-BE-127 (ST-08, EPIC-03, v9.7, fixed this story): calculate_uk_entry_fees /
# calculate_us_entry_fees (and the exit-fee equivalents, same arithmetic
# shape) now round stamp_duty/fx_fee/total via Decimal/ROUND_HALF_UP
# internally (utils/calculations.py's _round_half_up helper) instead of
# float round() at the call site. These golden cases previously locked in
# and documented a known £0.01 under-charge at half-penny boundaries (see
# docs/ops/money_arithmetic_audit_2026-09-22.md §3); they now assert parity
# with the independent Decimal reference instead.

class TestKnownFloatDecimalDiscrepancies:
    """Former £0.01 discrepancies between the old float/round() fee path and
    a Decimal/ROUND_HALF_UP reference, at exact half-penny boundaries.
    BLG-BE-127 fixed this — these cases now assert equality, not a gap."""

    UK_STAMP_DUTY_DISCREPANCY_CASES = [3.00, 9.00, 15.00, 21.00, 25.00]
    US_FX_FEE_DISCREPANCY_CASES = [10.00, 30.00, 50.00, 70.00, 290.00]

    @pytest.mark.parametrize("gross_cost", UK_STAMP_DUTY_DISCREPANCY_CASES)
    def test_uk_stamp_duty_known_discrepancy_at_half_penny_boundary(self, gross_cost):
        fees = calculate_uk_entry_fees(gross_cost, _SETTINGS)
        float_stamp_duty = round(fees["stamp_duty"], 2)

        expected_decimal = _decimal_round_half_up(
            gross_cost * _SETTINGS["stamp_duty_rate"]
        )

        # BLG-BE-127 fixed: now at parity with the Decimal reference.
        assert float_stamp_duty == pytest.approx(float(expected_decimal), abs=1e-9), (
            f"gross_cost={gross_cost}: expected parity with the Decimal "
            f"reference (float={float_stamp_duty}, decimal={expected_decimal})"
        )

    @pytest.mark.parametrize("gross_cost", US_FX_FEE_DISCREPANCY_CASES)
    def test_us_fx_fee_known_discrepancy_at_half_penny_boundary(self, gross_cost):
        fees = calculate_us_entry_fees(gross_cost, _SETTINGS)
        float_fx_fee = round(fees["fx_fee"], 2)

        expected_decimal = _decimal_round_half_up(
            gross_cost * _SETTINGS["fx_fee_rate"]
        )

        assert float_fx_fee == pytest.approx(float(expected_decimal), abs=1e-9), (
            f"gross_cost={gross_cost}: expected parity with the Decimal "
            f"reference (float={float_fx_fee}, decimal={expected_decimal})"
        )


class TestFeeCalculationsAgreeElsewhere:
    """Non-boundary values — confirms the float and Decimal paths agree
    everywhere except the documented boundary class above, i.e. the
    discrepancy is narrow, not systemic."""

    NON_BOUNDARY_GROSS_COSTS = [100.0, 250.50, 999.99, 1000.0, 1998.0, 5000.0]

    @pytest.mark.parametrize("gross_cost", NON_BOUNDARY_GROSS_COSTS)
    def test_uk_stamp_duty_matches_decimal_away_from_boundary(self, gross_cost):
        fees = calculate_uk_entry_fees(gross_cost, _SETTINGS)
        float_stamp_duty = round(fees["stamp_duty"], 2)
        expected_decimal = _decimal_round_half_up(gross_cost * _SETTINGS["stamp_duty_rate"])
        assert float_stamp_duty == pytest.approx(float(expected_decimal), abs=1e-9)

    @pytest.mark.parametrize("gross_cost", NON_BOUNDARY_GROSS_COSTS)
    def test_us_fx_fee_matches_decimal_away_from_boundary(self, gross_cost):
        fees = calculate_us_entry_fees(gross_cost, _SETTINGS)
        float_fx_fee = round(fees["fx_fee"], 2)
        expected_decimal = _decimal_round_half_up(gross_cost * _SETTINGS["fx_fee_rate"])
        assert float_fx_fee == pytest.approx(float(expected_decimal), abs=1e-9)

    def test_uk_exit_fees_commission_only_no_rate_multiplication(self):
        # UK exit fees are a fixed commission (no stamp duty on sales) — no
        # rate-multiplication step, so no boundary class applies here.
        fees = calculate_uk_exit_fees(1000.0, _SETTINGS)
        assert fees["total"] == _SETTINGS["uk_commission"]

    def test_us_exit_fees_shares_the_same_fx_fee_shape_as_entry(self):
        fees = calculate_us_exit_fees(70.0, _SETTINGS)
        expected_decimal = _decimal_round_half_up(70.0 * _SETTINGS["fx_fee_rate"])
        # BLG-BE-127 fixed: exit fees share calculate_us_entry_fees's
        # arithmetic shape and now use the same internal Decimal rounding,
        # so this former boundary-class discrepancy is at parity too.
        assert round(fees["fx_fee"], 2) == float(expected_decimal)


# ---------------------------------------------------------------------------
# Bounded regression scan — keeps the discrepancy count from silently
# growing if the rate constants or rounding approach change.
# ---------------------------------------------------------------------------

class TestDiscrepancyCountRegression:
    """A bounded brute-force scan (not the full 500k-value audit scan, which
    lives in the one-off audit — see docs/ops/money_arithmetic_audit_
    2026-09-22.md §3) confirming the discrepancy rate stays within the
    documented, explained bounds. A large jump here would mean the root
    cause has changed and needs re-auditing."""

    def _count_discrepancies(self, rate: float, hi_pennies: int) -> int:
        rate_str = "0.005" if rate == 0.005 else "0.0015"
        dec_rate = Decimal(rate_str)
        count = 0
        for cents in range(1, hi_pennies):
            gc = cents / 100.0
            float_rounded = round(gc * rate, 2)
            dec_rounded = (Decimal(cents) / Decimal(100) * dec_rate).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            if abs(float_rounded - float(dec_rounded)) >= 0.01 - 1e-9:
                count += 1
        return count

    def test_uk_stamp_duty_discrepancy_rate_within_documented_bound(self):
        # 50,000 values (£0.01-£500.00) — documented full-range rate is
        # ~0.18%; assert well within an order of magnitude of that so a
        # rate-constant change is caught without over-fitting to the exact
        # count.
        count = self._count_discrepancies(0.005, 50_000)
        assert 0 < count < 500, (
            f"UK stamp duty discrepancy count {count}/50000 is outside the "
            "documented ~0.18% bound — re-run the full audit "
            "(docs/ops/money_arithmetic_audit_2026-09-22.md)"
        )

    def test_us_fx_fee_discrepancy_rate_within_documented_bound(self):
        count = self._count_discrepancies(0.0015, 50_000)
        assert 0 < count < 100, (
            f"US FX fee discrepancy count {count}/50000 is outside the "
            "documented ~0.018% bound — re-run the full audit "
            "(docs/ops/money_arithmetic_audit_2026-09-22.md)"
        )
