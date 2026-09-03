"""
R-multiple calculation regression test (ST-19, BLG-QA-89, EPIC-04, v9.0).

Locks the behaviour of AnalyticsService.calculate_r_multiple_distribution
against a small set of known trade fixtures, per
docs/specs/metrics_definitions.md's "R-Multiple (Canonical Server-Side)"
section and its "Cross-Currency Normalization" (BLG-SPEC-59) subsection.

Canonical formula: R = (exit_price - entry_price) / (entry_price - stop_price)

Qualifying conditions: stop_price is non-null; entry_price > stop_price
(denominator > 0); exit_price is non-null.

Cross-currency invariant (BLG-SPEC-59, v6.8): R-multiple is dimensionless
by construction — a trade's three prices (entry/exit/stop) are always the
same native currency, so the currency unit cancels algebraically. No
fx_rate/fx_adjustment may be applied to R-multiple inputs or outputs.
metrics_definitions.md's own "Validation" note prescribes the exact test
shape used below: a mixed USD/GBP fixture set with deliberately different
fx_rate values attached (fx_rate is passed in the fixture dicts but is
never read by calculate_r_multiple_distribution — its signature has no
fx_rate parameter at all, confirming the spec's "no FX conversion at any
step" requirement structurally, not just by output value).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.analytics_service import AnalyticsService  # noqa: E402


def _trade(entry_price, stop_price, exit_price, fx_rate=1.0):
    """fx_rate is deliberately accepted and stored on the fixture dict but
    is NOT one of the three fields calculate_r_multiple_distribution reads
    (entry_price/stop_price/exit_price only) — included here purely to
    prove its presence/value has no effect (BLG-SPEC-59 validation)."""
    return {"entry_price": entry_price, "stop_price": stop_price, "exit_price": exit_price, "fx_rate": fx_rate}


class TestRMultipleKnownFixtures:
    """A small, hand-computed fixture set — each trade's expected R value
    verified by the formula directly, not derived from the code under test."""

    def setup_method(self):
        self.service = AnalyticsService()

    def test_five_known_trades_produce_expected_distribution(self):
        # R values (by hand): 1.0, -1.0, 2.0, 0.5, -0.5
        trades = [
            _trade(entry_price=100, stop_price=90, exit_price=110),   # R = (110-100)/(100-90) = 1.0
            _trade(entry_price=100, stop_price=90, exit_price=90),    # R = (90-100)/(100-90) = -1.0
            _trade(entry_price=50, stop_price=40, exit_price=70),     # R = (70-50)/(50-40) = 2.0
            _trade(entry_price=200, stop_price=180, exit_price=210),  # R = (210-200)/(200-180) = 0.5
            _trade(entry_price=200, stop_price=180, exit_price=190),  # R = (190-200)/(200-180) = -0.5
        ]
        result = self.service.calculate_r_multiple_distribution(trades)

        assert result["has_enough_data"] is True
        assert result["total_qualifying_trades"] == 5
        # sorted: [-1.0, -0.5, 0.5, 1.0, 2.0] -> median (odd n=5) is the middle value
        assert result["median_r"] == 0.5
        assert result["avg_winner_r"] == round((1.0 + 2.0 + 0.5) / 3, 2)
        assert result["avg_loser_r"] == round((-1.0 + -0.5) / 2, 2)
        assert result["pct_above_1r"] == round(1 / 5 * 100, 1)  # only the R=2.0 trade

    def test_bucket_counts_match_hand_computed_ranges(self):
        trades = [
            _trade(entry_price=100, stop_price=90, exit_price=65),    # R = -3.5 -> "< -2R"
            _trade(entry_price=100, stop_price=90, exit_price=75),    # R = -2.5 -> "< -2R"
            _trade(entry_price=100, stop_price=90, exit_price=85),    # R = -1.5 -> "-2R to -1R"
            _trade(entry_price=100, stop_price=90, exit_price=95),    # R = -0.5 -> "-1R to 0R"
            _trade(entry_price=100, stop_price=90, exit_price=105),   # R = 0.5 -> "0R to 1R"
        ]
        result = self.service.calculate_r_multiple_distribution(trades)
        counts = {b["range"]: b["count"] for b in result["buckets"]}
        assert counts["< -2R"] == 2
        assert counts["-2R to -1R"] == 1
        assert counts["-1R to 0R"] == 1
        assert counts["0R to 1R"] == 1
        assert counts["1R to 2R"] == 0
        assert counts["2R to 3R"] == 0
        assert counts["> 3R"] == 0


class TestQualifyingConditions:
    def setup_method(self):
        self.service = AnalyticsService()

    def test_null_stop_price_excludes_trade(self):
        trades = [_trade(100, None, 110)] + [_trade(100, 90, 105)] * 4
        result = self.service.calculate_r_multiple_distribution(trades)
        assert result["total_qualifying_trades"] == 4

    def test_entry_at_or_below_stop_excludes_trade(self):
        """entry_price > stop_price is required (denominator > 0) --
        short-side and lock-in stops above entry are excluded per spec."""
        trades = [_trade(entry_price=100, stop_price=100, exit_price=110)] + [_trade(100, 90, 105)] * 4
        result = self.service.calculate_r_multiple_distribution(trades)
        assert result["total_qualifying_trades"] == 4

    def test_stop_above_entry_excludes_trade(self):
        trades = [_trade(entry_price=100, stop_price=110, exit_price=95)] + [_trade(100, 90, 105)] * 4
        result = self.service.calculate_r_multiple_distribution(trades)
        assert result["total_qualifying_trades"] == 4

    def test_fewer_than_five_qualifying_trades_reports_insufficient_data(self):
        trades = [_trade(100, 90, 105)] * 4
        result = self.service.calculate_r_multiple_distribution(trades)
        assert result["has_enough_data"] is False
        assert result["total_qualifying_trades"] == 4
        assert result["median_r"] is None
        assert result["buckets"] == []


class TestCrossCurrencyNormalization:
    """BLG-SPEC-59 (v6.8): R-multiple is dimensionless by construction --
    no FX conversion applies at any step. Validation shape prescribed
    directly by metrics_definitions.md's own 'Validation' note: a mixed
    USD/GBP fixture with deliberately different fx_rate values, confirming
    aggregate R metrics are unaffected by the FX rate difference."""

    def setup_method(self):
        self.service = AnalyticsService()

    def test_mixed_usd_gbp_trades_with_different_fx_rates_unaffected(self):
        # Two economically-identical trades (same R = 1.0) but attached to
        # wildly different fx_rate values, simulating a USD trade and a
        # GBP trade with different live FX rates at the time.
        usd_trade = _trade(entry_price=100.0, stop_price=90.0, exit_price=110.0, fx_rate=1.27)
        gbp_trade = _trade(entry_price=50.0, stop_price=45.0, exit_price=55.0, fx_rate=1.0)
        filler = [_trade(100, 90, 95)] * 3  # 3 more qualifying trades, R = -0.5 each, to clear the 5-trade minimum

        trades_a = [usd_trade, gbp_trade] + filler
        result_a = self.service.calculate_r_multiple_distribution(trades_a)

        # Now flip the fx_rate values (same three native prices, different
        # fx_rate attached) -- if fx_rate were incorrectly read, this would
        # change the result. It must not.
        usd_trade_different_fx = dict(usd_trade, fx_rate=99.0)
        gbp_trade_different_fx = dict(gbp_trade, fx_rate=0.01)
        trades_b = [usd_trade_different_fx, gbp_trade_different_fx] + filler
        result_b = self.service.calculate_r_multiple_distribution(trades_b)

        assert result_a == result_b, (
            "R-multiple aggregates must be identical regardless of fx_rate "
            "value attached to each trade -- R is dimensionless by "
            "construction (BLG-SPEC-59) and must never be FX-adjusted."
        )
        assert result_a["median_r"] is not None  # sanity: the comparison above isn't vacuously true on an empty/None result

    def test_function_signature_has_no_fx_parameter(self):
        """Structural confirmation of the 'no FX conversion at any step'
        requirement -- calculate_r_multiple_distribution takes only the
        trades list, no fx_rate/fx_adjustment parameter exists to pass."""
        import inspect
        sig = inspect.signature(self.service.calculate_r_multiple_distribution)
        param_names = list(sig.parameters.keys())
        assert "fx_rate" not in param_names
        assert "fx_adjustment" not in param_names
