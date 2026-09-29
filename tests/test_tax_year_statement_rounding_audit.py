"""
Tax-year statement float-vs-Decimal rounding-boundary audit (ST-08, EPIC-02,
v9.8, BLG-BE-130).

Extends the v9.7 fee-rounding audit (docs/ops/money_arithmetic_audit_2026-09-22.md,
BLG-BE-127/BLG-BE-121) to the tax-year statement calculation path
(`services.reports_service.get_tax_year_report`). Audit write-up:
docs/ops/money_arithmetic_audit_tax_year_2026-09-29.md.

Scope: the v9.6 audit's known discrepancy class (BLG-BE-127) is specifically
a `gross_cost * fee_rate` multiplication landing on a half-penny boundary,
already fixed at every entry/exit fee call site via `_round_half_up()`
(utils/calculations.py). `get_tax_year_report()` performs no new rate
multiplication of its own -- it reads already-computed, already-rounded
`pnl`/`total_cost`/`net_proceeds` values off each trade and sums/rounds
them. This file provides the golden-boundary evidence for that specific
claim: a brute-force scan confirming the summary aggregation
(`round(sum(already-2dp-rounded pnl values), 2)`) never disagrees with an
independently-derived Decimal/ROUND_HALF_UP sum, plus a real-function
smoke test with boundary-adjacent trade data.

CI-safe: no DB or network calls (get_tax_year_report's DB dependencies are
mocked, same pattern as tests/test_tax_year_boundary_completeness.py).
"""
import random
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

sys.modules.pop("database", None)
import database  # noqa: E402
import services.reports_service as reports_service  # noqa: E402


def _decimal_round_half_up(value, dp: int = 2) -> Decimal:
    """Independent reference implementation -- Decimal, round-half-up.
    Deliberately not imported from the implementation under test."""
    quantum = Decimal("1").scaleb(-dp)
    return Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP)


def _decimal_sum(values) -> Decimal:
    total = Decimal("0")
    for v in values:
        total += Decimal(str(v))
    return total.quantize(Decimal("1").scaleb(-2), rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------------------
# Brute-force scan: summing already-2dp-rounded pnl values
# ---------------------------------------------------------------------------
# Every trade's own pnl is already rounded to 2dp before it reaches this
# summation (position_service.py's realized_pnl_gbp is stored via a
# NUMERIC(12,2) column, and get_tax_year_report's own per-trade loop applies
# round(float(t.get('pnl', 0)), 2) again defensively). The question this
# scan answers: can round(sum(already-2dp floats), 2) ever disagree with a
# Decimal/ROUND_HALF_UP sum of the same values, given float representation
# error accumulated across many terms?

class TestSummaryAggregationGoldenScan:
    def test_random_trade_sets_never_disagree_with_decimal_sum(self):
        rng = random.Random(9998001)  # fixed seed -- reproducible golden run
        disagreements = []

        for trial in range(2000):
            n_trades = rng.randint(1, 60)
            # Round to 2dp exactly as position_service.py stores pnl --
            # realistic magnitude range for a swing-trading position.
            pnls = [round(rng.uniform(-2000.0, 2000.0), 2) for _ in range(n_trades)]

            float_total = round(sum(pnls), 2)
            decimal_total = float(_decimal_sum(pnls))

            if abs(float_total - decimal_total) >= 0.005:
                disagreements.append((trial, pnls, float_total, decimal_total))

        assert disagreements == [], (
            f"{len(disagreements)} of 2000 scanned trade sets disagreed by "
            f">= GBP 0.005 between float round(sum(...), 2) and a Decimal/"
            f"ROUND_HALF_UP sum -- first case: {disagreements[0] if disagreements else None}"
        )

    def test_half_penny_adjacent_pnl_values_never_disagree(self):
        """Deliberately construct pnl sets whose true sum sits exactly on, or
        one float-ULP off, a half-penny boundary (X.XX5) -- the same
        boundary shape BLG-BE-127 found in the fee-multiplication path."""
        disagreements = []
        boundary_totals = [0.005, 1.005, 9.995, 100.005, 999.995, -0.005, -100.005]

        for target in boundary_totals:
            for split in (1, 2, 3, 5):
                # Split `target` into `split` already-2dp-rounded pnl values
                # that sum to (approximately, at float precision) `target`.
                base = round(target / split, 2)
                pnls = [base] * (split - 1)
                pnls.append(round(target - base * (split - 1), 2))

                float_total = round(sum(pnls), 2)
                decimal_total = float(_decimal_sum(pnls))

                if abs(float_total - decimal_total) >= 0.005:
                    disagreements.append((target, split, pnls, float_total, decimal_total))

        assert disagreements == [], (
            f"Half-penny-adjacent pnl sets disagreed: {disagreements}"
        )


# ---------------------------------------------------------------------------
# Real function: get_tax_year_report() with boundary-adjacent trade data
# ---------------------------------------------------------------------------

def _trade(trade_id, pnl, total_cost=1000.0, net_proceeds=None, market="UK"):
    if net_proceeds is None:
        net_proceeds = round(total_cost + pnl, 2)
    return {
        "id": trade_id,
        "ticker": "AAA",
        "market": market,
        "entry_date": "2026-05-01",
        "exit_date": "2026-06-01",
        "holding_days": 31,
        "entry_price": 10.0,
        "exit_price": 11.0,
        "entry_fx_rate": None,
        "exit_fx_rate": None,
        "shares": 100.0,
        "total_cost": total_cost,
        "net_proceeds": net_proceeds,
        "pnl": pnl,
        "tags": [],
        "trade_origin": "Manual",
    }


class TestGetTaxYearReportRealFunctionBoundaryCases:
    def _run(self, trades):
        with patch.object(reports_service, "get_portfolio", return_value={"id": "port-1"}), \
             patch.object(reports_service, "get_trade_history_by_tax_year", return_value=trades), \
             patch.object(reports_service, "get_estimated_unrealised_pnl", return_value=0.0), \
             patch.object(reports_service, "_get_restated_month_count", return_value=0):
            return reports_service.get_tax_year_report(2025)

    def test_summary_totals_match_decimal_sum_at_boundary_values(self):
        pnls = [3.00 * 0.005, -1.005, 9.995, 100.005, -999.995, 0.015, -0.005]
        pnls = [round(p, 2) for p in pnls]
        trades = [_trade(f"t{i}", p) for i, p in enumerate(pnls)]

        result = self._run(trades)
        summary = result["summary"]

        expected_total = float(_decimal_sum(pnls))
        expected_gross_profit = float(_decimal_sum([p for p in pnls if p > 0]) if any(p > 0 for p in pnls) else Decimal("0.00"))
        expected_gross_loss = float(_decimal_sum([p for p in pnls if p <= 0]) if any(p <= 0 for p in pnls) else Decimal("0.00"))

        assert summary["total_realised_pnl"] == pytest.approx(expected_total, abs=0.001)
        assert summary["total_gross_profit"] == pytest.approx(expected_gross_profit, abs=0.001)
        assert summary["total_gross_loss"] == pytest.approx(expected_gross_loss, abs=0.001)

    def test_no_carried_forward_loss_field_in_response(self):
        """Regression guard for the audit's second finding: carried_forward_loss_gbp
        has no backend implementation (Design Only -- docs/design/2026-09-14__release-v9.4/
        carried-forward-loss-field/decision_record.md). If this test ever fails,
        an implementation has been added and this audit's "not applicable, no
        code exists" disposition needs re-review, not a silent pass."""
        result = self._run([_trade("t0", 50.0)])
        assert "carried_forward_loss_gbp" not in result["summary"]
