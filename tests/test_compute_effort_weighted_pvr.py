"""
ST-48 (BLG-SPEC-191, EPIC-07, v9.14) — scripts/compute_effort_weighted_pvr.py
parse_effort_weight() weights exactly the values docs/specs/metrics_definitions.md
Appendix F's effort normalisation table lists, one example per table row.
"""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("pvr", ROOT / "scripts" / "compute_effort_weighted_pvr.py")
pvr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pvr)


@pytest.mark.parametrize("effort, weight", [
    # Direct numeric with unit
    ("8.00d", 8.0),
    ("4.0 days", 4.0),
    # Numeric with band annotation
    ("0.5 (XS)", 0.5),
    ("9.0 (S+S+S+M+M+M+S)", 9.0),
    # Bare numeric
    ("0.75", 0.75),
    # Band with a day range at the start of its parenthetical
    ("S (~0.5-1d)", 0.75),
    ("M (~1–2 days)", 1.5),
    ("S (~0.5–1d, pending root cause)", 0.75),
    # Band with a single day quantity
    ("S (~0.5d)", 0.5),
    ("S (~1 day)", 1.0),
    ("M (~2 days, 3 small sub-items)", 2.0),
    # Hour- or minute-scale quantity, or "<"
    ("XS (<1h)", 0.15),
    ("XS (<1 hour)", 0.15),
    ("XS (~0.5 hr)", 0.15),
    ("S (~4 hrs)", 0.15),
    ("XS (~15min)", 0.15),
    ("XS (<1h, plus a live measurement re-run)", 0.15),
    # Parenthetical that does not start with a quantity -> band midpoint
    ("M (Product Owner-confirmed scope, 2026-08-14 — see below)", 1.75),
    ("XS (confirmation only, once DB access is available)", 0.4),
    # Band alone
    ("XS", 0.4), ("S", 0.75), ("M", 1.75), ("L", 3.5), ("VL", 3.5), ("VH", 12.0),
])
def test_table_rows_are_weighted(effort, weight):
    assert pvr.parse_effort_weight(effort) == pytest.approx(weight)


@pytest.mark.parametrize("effort", ["S–M (~1–2d)", "VS", "VS (~0.1-0.2d)", "TBD"])
def test_values_outside_the_table_are_not_weighted(effort):
    assert pvr.parse_effort_weight(effort) is None
