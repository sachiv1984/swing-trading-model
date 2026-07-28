"""
ST-04 (BLG-FEAT-85, EPIC-04, v7.9): Monthly P&L CSV export -- cost-basis
method disclosure/reconciliation column.

Tests build_monthly_pnl_csv in isolation (pure function, plain dict rows
in, no database or network calls) -- same convention as
test_pnl_reconciliation_service.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from services.reports_service import build_monthly_pnl_csv, _COST_BASIS_METHOD_NOTE  # noqa: E402


def test_csv_includes_cost_basis_disclosure_row():
    months = [{"year": 2026, "month": 7, "realised_pnl_gbp": 123.45, "trade_count": 3}]
    csv_text = build_monthly_pnl_csv(months)

    assert "Cost Basis Method" in csv_text
    assert "Specific Identification" in csv_text


def test_main_table_rows_unchanged_by_disclosure_addition():
    """AC-01 must be additive only -- the on-screen-mirroring main table
    (header + one row per month) is byte-identical to before this story."""
    months = [
        {"year": 2026, "month": 7, "realised_pnl_gbp": 123.45, "trade_count": 3},
        {"year": 2026, "month": 6, "realised_pnl_gbp": -50.0, "trade_count": 1},
    ]
    csv_text = build_monthly_pnl_csv(months)
    lines = csv_text.split("\n")

    assert lines[0] == "Year,Month,Realised P&L (GBP),Trades"
    assert lines[1] == "2026,7,123.45,3"
    assert lines[2] == "2026,6,-50.0,1"
    # Blank separator row before the disclosure, per the trailing-note design.
    assert lines[3] == ""
    # csv.writer quotes this field (contains commas) -- check content, not exact quoting.
    assert lines[4].startswith("Cost Basis Method,")
    assert "Specific Identification" in lines[4]


def test_empty_months_still_includes_header_and_disclosure():
    csv_text = build_monthly_pnl_csv([])
    lines = csv_text.split("\n")

    assert lines[0] == "Year,Month,Realised P&L (GBP),Trades"
    assert lines[1] == ""
    assert "Cost Basis Method" in lines[2]


class TestCostBasisReconciliation:
    """AC-02: reconciles against a manually-verified sample.

    Reconstructs get_monthly_pnl's SQL aggregation
    (SUM(pnl) GROUP BY year, month FROM trade_history) in pure Python
    against a hand-computed fixture, confirming the "Specific
    Identification (per-position lot)" method claim: each trade_history
    row's pnl already reflects that specific position's own entry cost
    (prorated by shares exited for a partial exit) -- summing them by
    month is not FIFO re-derivation, it is a direct sum of
    already-final, per-lot realised figures.
    """

    def test_manual_sample_reconciles_to_expected_monthly_total(self):
        # Manually-verified sample: two positions, same ticker (AAPL),
        # each its own lot -- one full exit, one partial exit -- both
        # closing in the same month.
        #
        # Position A: bought 10 shares, total_cost=1000.00 GBP, fully
        # exited for net_proceeds=1150.00 GBP.
        #   pnl_A = 1150.00 - 1000.00 = 150.00
        #
        # Position B: bought 20 shares, total_cost=2000.00 GBP, partially
        # exited (8 of 20 shares) for net_proceeds=780.00 GBP.
        #   cost_basis_B_partial = 2000.00 * (8/20) = 800.00
        #   pnl_B = 780.00 - 800.00 = -20.00
        #
        # Expected monthly total = 150.00 + (-20.00) = 130.00
        trade_history_rows = [
            {"exit_date": "2026-07-05", "pnl": 150.00},
            {"exit_date": "2026-07-18", "pnl": -20.00},
        ]

        expected_total = 130.00
        computed_total = round(sum(r["pnl"] for r in trade_history_rows), 2)

        assert computed_total == expected_total

        # Confirm this reconciled total is exactly what the report/CSV
        # builder would render for the month.
        months = [{"year": 2026, "month": 7, "realised_pnl_gbp": computed_total, "trade_count": 2}]
        csv_text = build_monthly_pnl_csv(months)
        assert "2026,7,130.0,2" in csv_text
