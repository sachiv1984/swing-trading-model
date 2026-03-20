"""
Reports Service

Business logic for the tax-year P&L report.

Spec: docs/specs/api_contracts/reports_endpoints.md v0.3
Data model: docs/specs/data_model.md §3 (trade_history), §2 (positions)

Schema note: trade_history stores exit value as net_proceeds (exit proceeds
after fees), not exit_proceeds as named in data_model.md. The report field
exit_proceeds_gbp maps to net_proceeds. fees are deductible for tax purposes,
so net_proceeds is the correct value.
"""

import csv
import io
from datetime import date, datetime, timezone
from io import BytesIO
from typing import Dict

from database import (
    get_portfolio,
    get_positions,
    get_trade_history_by_tax_year,
)
from utils.formatting import decimal_to_float


UNREALISED_NOTE = (
    "Reflects current open positions at time of report generation, "
    "not positions open during the specified tax year. "
    "Indicative only — not a tax liability."
)


def get_tax_year_report(year: int) -> Dict:
    """
    Build a UK tax-year P&L report for the given start year.

    Args:
        year: The start year of the UK tax year (e.g. 2025 for 2025/26).

    Returns:
        Dict matching the data schema in reports_endpoints.md §Response.

    Raises:
        ValueError: "tax year has not started yet" if year is in the future.
        ValueError: "Portfolio not found" if no portfolio exists.
    """
    tax_year_start = date(year, 4, 6)
    if tax_year_start > date.today():
        raise ValueError("tax year has not started yet")

    tax_year_end = date(year + 1, 4, 5)

    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    portfolio_id = str(portfolio['id'])

    # --- Closed trades for this tax year ---
    raw_trades = get_trade_history_by_tax_year(portfolio_id, tax_year_start, tax_year_end)
    trades = [decimal_to_float(t) for t in raw_trades]

    trades_out = []
    for t in trades:
        realised_pnl = round(float(t.get('pnl', 0)), 2)
        total_cost = round(float(t.get('total_cost', 0)), 2)
        # exit_proceeds_gbp = net_proceeds (after exit fees — deductible for tax)
        exit_proceeds = round(float(t.get('net_proceeds', 0)), 2)
        pnl_pct = round(realised_pnl / total_cost * 100, 2) if total_cost else 0.0
        market = t['market']
        trades_out.append({
            "id": str(t['id']),
            "ticker": t['ticker'],
            "market": market,
            "entry_date": str(t['entry_date']),
            "exit_date": str(t['exit_date']),
            "holding_days": int(t.get('holding_days', 0)),
            "entry_price_native": round(float(t.get('entry_price', 0)), 4),
            "exit_price_native": round(float(t.get('exit_price', 0)), 4),
            "entry_fx_rate": float(t['entry_fx_rate']) if t.get('entry_fx_rate') else None,
            "exit_fx_rate": float(t['exit_fx_rate']) if t.get('exit_fx_rate') else None,
            "shares": float(t.get('shares', 0)),
            "total_cost_gbp": total_cost,
            "exit_proceeds_gbp": exit_proceeds,
            "realised_pnl_gbp": realised_pnl,
            "pnl_pct": pnl_pct,
            "currency": "USD" if market == "US" else "GBP",
            "tags": t.get('tags') or [],
        })

    # --- Summary ---
    total_count = len(trades_out)
    total_pnl = round(sum(t['realised_pnl_gbp'] for t in trades_out), 2)
    gross_profit = round(sum(t['realised_pnl_gbp'] for t in trades_out if t['realised_pnl_gbp'] > 0), 2)
    gross_loss = round(sum(t['realised_pnl_gbp'] for t in trades_out if t['realised_pnl_gbp'] <= 0), 2)
    win_count = sum(1 for t in trades_out if t['realised_pnl_gbp'] > 0)
    loss_count = total_count - win_count
    win_rate = round(win_count / total_count * 100, 1) if total_count else 0.0

    # --- Estimated unrealised P&L from currently open positions ---
    open_positions = get_positions(portfolio_id, status='open')
    estimated_unrealised_pnl = round(
        sum(float(p.get('pnl', 0) or 0) for p in open_positions), 2
    )

    return {
        "tax_year_start": str(tax_year_start),
        "tax_year_end": str(tax_year_end),
        "tax_year_label": f"{year}/{str(year + 1)[2:]}",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": {
            "total_closed_trades": total_count,
            "total_realised_pnl": total_pnl,
            "total_gross_profit": gross_profit,
            "total_gross_loss": gross_loss,
            "win_count": win_count,
            "loss_count": loss_count,
            "win_rate": win_rate,
            "estimated_unrealised_pnl": estimated_unrealised_pnl,
            "unrealised_note": UNREALISED_NOTE,
        },
        "trades": trades_out,
    }


_DISCLAIMER = (
    "Disclaimer: The tax-year P&L report is provided for user reference only. "
    "It is not a substitute for qualified tax advice. Users are responsible for "
    "verifying the figures against their broker records and obtaining appropriate "
    "professional advice before submitting any tax return."
)


def build_tax_year_pdf(report_data: dict) -> bytes:
    """
    Render a tax-year P&L report dict as a PDF document (bytes).

    Args:
        report_data: Dict returned by get_tax_year_report().

    Returns:
        Raw PDF bytes suitable for streaming as application/pdf.
    """
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )
    styles = getSampleStyleSheet()
    story = []

    # --- Title ---
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Heading1"], fontSize=16, spaceAfter=4
    )
    story.append(
        Paragraph(f"Tax Year P&L — {report_data['tax_year_label']}", title_style)
    )
    sub_style = ParagraphStyle(
        "ReportSub", parent=styles["Normal"], fontSize=9, textColor=colors.grey
    )
    story.append(
        Paragraph(f"Generated: {report_data['generated_at']} (UTC)", sub_style)
    )
    story.append(Spacer(1, 6 * mm))

    # --- Summary bar ---
    summary = report_data["summary"]
    _DARK = colors.HexColor("#1e293b")
    _LIGHT = colors.HexColor("#f8fafc")

    summary_data = [
        ["Total Realised P&L", "Gross Profit", "Gross Loss", "Win Rate", "Total Trades"],
        [
            f"£{summary['total_realised_pnl']:,.2f}",
            f"£{summary['total_gross_profit']:,.2f}",
            f"£{summary['total_gross_loss']:,.2f}",
            f"{summary['win_rate']}%",
            str(summary["total_closed_trades"]),
        ],
    ]
    col_w = 52 * mm
    summary_table = Table(summary_data, colWidths=[col_w] * 5)
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _DARK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, 1), 12),
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, 1), _LIGHT),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 6 * mm))

    # --- Trades table ---
    trades = report_data.get("trades", [])
    if trades:
        headers = [
            "Ticker", "Mkt", "Entry Date", "Exit Date", "Days",
            "Entry Price", "Exit Price", "Shares",
            "Cost GBP", "Proceeds GBP", "P&L GBP", "P&L %",
            "FX In", "FX Out", "CCY", "Tags",
        ]
        rows = [headers]
        for t in trades:
            tags = ", ".join(t.get("tags") or [])
            fx_in = f"{t['entry_fx_rate']:.4f}" if t.get("entry_fx_rate") else "—"
            fx_out = f"{t['exit_fx_rate']:.4f}" if t.get("exit_fx_rate") else "—"
            rows.append(
                [
                    t["ticker"],
                    t["market"],
                    t["entry_date"],
                    t["exit_date"],
                    str(t["holding_days"]),
                    f"{t['entry_price_native']:,.4f}",
                    f"{t['exit_price_native']:,.4f}",
                    f"{t['shares']:.2f}",
                    f"£{t['total_cost_gbp']:,.2f}",
                    f"£{t['exit_proceeds_gbp']:,.2f}",
                    f"£{t['realised_pnl_gbp']:,.2f}",
                    f"{t['pnl_pct']:.2f}%",
                    fx_in,
                    fx_out,
                    t["currency"],
                    tags,
                ]
            )

        # Landscape A4 usable width ≈ 267mm
        col_widths = [
            16, 8, 20, 20, 10,   # ticker, mkt, entry_date, exit_date, days
            22, 22, 14,           # entry_price, exit_price, shares
            24, 26, 22, 14,       # cost, proceeds, pnl, pnl%
            14, 14, 10, 21,       # fx_in, fx_out, ccy, tags
        ]
        col_widths = [w * mm for w in col_widths]

        trade_table = Table(rows, colWidths=col_widths, repeatRows=1)
        pnl_col_idx = 10  # "P&L GBP" column (0-indexed)
        cell_style = [
            ("BACKGROUND", (0, 0), (-1, 0), _DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, _LIGHT]),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]
        for i, t in enumerate(trades, start=1):
            pnl = t["realised_pnl_gbp"]
            if pnl > 0:
                cell_style.append(
                    ("TEXTCOLOR", (pnl_col_idx, i), (pnl_col_idx, i), colors.HexColor("#16a34a"))
                )
            elif pnl < 0:
                cell_style.append(
                    ("TEXTCOLOR", (pnl_col_idx, i), (pnl_col_idx, i), colors.HexColor("#dc2626"))
                )
        trade_table.setStyle(TableStyle(cell_style))
        story.append(trade_table)
    else:
        story.append(Paragraph("No trades recorded in this tax year.", styles["Normal"]))

    story.append(Spacer(1, 6 * mm))

    # --- Disclaimer ---
    disclaimer_style = ParagraphStyle(
        "Disclaimer", parent=styles["Normal"], fontSize=7, textColor=colors.grey
    )
    story.append(Paragraph(_DISCLAIMER, disclaimer_style))

    doc.build(story)
    return buffer.getvalue()


def build_tax_year_csv(report_data: dict) -> str:
    """
    Render a tax-year P&L report dict as a CSV string.

    Structure per spec reports_endpoints.md v0.3:
      - Section 1: 5-row metadata block (key/value pairs)
      - Row 6: blank
      - Row 7: column header row (17 columns)
      - Rows 8+: trade data rows

    Args:
        report_data: Dict returned by get_tax_year_report().

    Returns:
        UTF-8 CSV string.
    """
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")

    summary = report_data["summary"]

    # Section 1 — Metadata (5 rows)
    writer.writerow(["Tax Year", report_data["tax_year_label"]])
    writer.writerow(["Generated At", report_data["generated_at"]])
    writer.writerow(["Total Realised P&L (GBP)", summary["total_realised_pnl"]])
    writer.writerow(["Total Closed Trades", summary["total_closed_trades"]])
    writer.writerow(["Win Rate (%)", summary["win_rate"]])

    # Blank row
    writer.writerow([])

    # Section 2 — Trades table
    headers = [
        "Trade ID", "Ticker", "Market", "Entry Date", "Exit Date",
        "Holding Days", "Entry Price (Native)", "Exit Price (Native)",
        "Entry FX Rate (GBP/USD)", "Exit FX Rate (GBP/USD)", "Shares",
        "Total Cost (GBP)", "Exit Proceeds (GBP)", "Realised P&L (GBP)",
        "P&L %", "Currency", "Tags",
    ]
    writer.writerow(headers)

    for t in report_data.get("trades", []):
        tags = "; ".join(t.get("tags") or [])
        writer.writerow([
            t["id"],
            t["ticker"],
            t["market"],
            t["entry_date"],
            t["exit_date"],
            t["holding_days"],
            t["entry_price_native"],
            t["exit_price_native"],
            t["entry_fx_rate"] if t.get("entry_fx_rate") is not None else "",
            t["exit_fx_rate"] if t.get("exit_fx_rate") is not None else "",
            t["shares"],
            t["total_cost_gbp"],
            t["exit_proceeds_gbp"],
            t["realised_pnl_gbp"],
            t["pnl_pct"],
            t["currency"],
            tags,
        ])

    return output.getvalue()
