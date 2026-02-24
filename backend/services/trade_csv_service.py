"""
services/trade_csv_service.py — QWB Quick Wins Bundle (v1.6.1)
===============================================================
New service file. Place at: backend/services/trade_csv_service.py
Export build_trade_history_csv from backend/services/__init__.py

Canonical spec: trade_endpoints.md v1.8.4 §GET /trades/export/csv
"""

import csv
import io
from typing import List, Dict


# Canonical column order — trade_endpoints.md v1.8.4 §CSV columns table.
# Do not reorder. Do not rename. Frontend and QA test scenarios
# verify exact column order and exact column names (B-09).
CSV_COLUMNS = [
    "ticker",
    "market",
    "entry_date",
    "exit_date",
    "shares",
    "entry_price",
    "exit_price",
    "pnl",
    "pnl_pct",
    "holding_days",
    "exit_reason",
    "tags",
    "entry_note",
    "exit_note",
]


def _serialise_field(column: str, value) -> str:
    """
    Serialise a single field value to its CSV string representation.

    Rules (canonical — trade_endpoints.md v1.8.4 §null handling and
    §tags serialisation):
        - None / null -> empty string (never the string "null" or "None")
        - tags (list) -> semicolon-separated string, e.g. "momentum;breakout"
        - tags empty list -> empty string
        - dates -> string as-is (already YYYY-MM-DD from PostgreSQL)
        - all other values -> str(value)
    """
    if column == "tags":
        if not value:
            return ""
        if isinstance(value, list):
            return ";".join(str(tag) for tag in value)
        # Defensive: if stored as string already, return as-is
        return str(value)

    if value is None:
        return ""

    return str(value)


def build_trade_history_csv(trades: List[Dict]) -> str:
    """
    Build the complete CSV string for the trade history export.

    Includes the header row followed by one data row per trade.
    When trades is empty, returns the header row only (not an empty
    string) — per trade_endpoints.md v1.8.4 §empty export (B-12).

    Args:
        trades: List of trade dicts from get_all_closed_trades_for_csv_export().
                Each dict must contain the 14 canonical columns.

    Returns:
        str: UTF-8 CSV content. Header row always present.
    """
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")

    # Header row — exact column names, canonical order
    writer.writerow(CSV_COLUMNS)

    # Data rows
    for trade in trades:
        writer.writerow(
            [_serialise_field(col, trade.get(col)) for col in CSV_COLUMNS]
        )

    return output.getvalue()
