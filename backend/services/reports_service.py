"""
Reports Service

Business logic for the tax-year P&L report.

Spec: docs/specs/api_contracts/reports_endpoints.md v0.1
Data model: docs/specs/data_model.md §3 (trade_history), §2 (positions)

Schema note: trade_history stores exit value as net_proceeds (exit proceeds
after fees), not exit_proceeds as named in data_model.md. The report field
exit_proceeds_gbp maps to net_proceeds. fees are deductible for tax purposes,
so net_proceeds is the correct value.
"""

from datetime import date, datetime, timezone
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
