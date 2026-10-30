#!/usr/bin/env python3
"""
Cost by feature area for one calendar month (ST-39, BLG-OPS-85, EPIC-06, v9.14).

Partitions the month's cost into three feature areas, AI endpoints, screener
and core CRUD, plus "unattributed" for calls made outside any request. The
method and its limits are in docs/ops/cost_by_feature_area.md; this script
produces that report's populated tables.

Sources (both production tables, read-only):
- claude_audit_log: one row per Claude call, with endpoint, cost_usd and
  latency_ms. Every row is in the AI area.
- api_call_log: one row per outbound market-data HTTP attempt, with service
  (provider) and feature ("<METHOD> <route template>" of the request that
  made it, or "unattributed"). Priced with UNIT_COST_USD from
  backend/utils/api_attribution.py, currently $0 for every provider.

Render's dyno is a fixed monthly charge shared by every feature. Render
reports no per-route usage, so the charge (passed as --render-monthly-usd,
from the Render invoice) is allocated by each area's share of work units:
one work unit per Claude call plus one per market-data call. See the doc
for why this proxy and what it misses.

Usage:
    DATABASE_URL=... python3 scripts/cost_by_feature_area.py --month 2026-11 \
        --render-monthly-usd 7.00
"""
import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

AREAS = ("ai", "screener", "core", "unattributed")
AREA_LABELS = {
    "ai": "AI endpoints",
    "screener": "Screener",
    "core": "Core CRUD",
    "unattributed": "Unattributed (outside a request)",
}

# Routes whose work is the AI feature, as written in api_call_log.feature
# ("<METHOD> <route template>"). Their Claude calls are in claude_audit_log;
# any market-data calls they make (e.g. the daily briefing's prices) count
# here too.
AI_ROUTE_PATTERNS = (
    r"^[A-Z]+ /ai/",
    r"^POST /trade-plans/generate-plan$",
    r"^POST /trade-plans/\{plan_id\}/generate-thesis$",
    r"^[A-Z]+ /reports/monthly-pnl/narrative$",
    r"^[A-Z]+ /trades/\{trade_id\}/debrief$",
)
SCREENER_ROUTE_PATTERNS = (
    r"^[A-Z]+ /screener(/|$)",
    r"^[A-Z]+ /ticker-universe(/|$)",
)


def classify(feature):
    """Feature area for an api_call_log.feature value."""
    if not feature or feature == "unattributed":
        return "unattributed"
    if any(re.search(p, feature) for p in AI_ROUTE_PATTERNS):
        return "ai"
    if any(re.search(p, feature) for p in SCREENER_ROUTE_PATTERNS):
        return "screener"
    return "core"


def month_bounds(year_month):
    y, m = (int(x) for x in year_month.split("-"))
    start = date(y, m, 1)
    end = date(y + (m == 12), m % 12 + 1, 1)
    return start, end


def partition(claude_rows, market_rows, unit_cost, render_monthly_usd):
    """claude_rows: (endpoint, calls, cost_usd, latency_ms_sum).
    market_rows: (feature, service, calls, failures).
    Returns {area: {...}} with direct costs, work units and the dyno share."""
    out = {a: {"claude_calls": 0, "claude_cost_usd": 0.0, "claude_latency_s": 0.0,
               "market_calls": 0, "market_failures": 0, "market_cost_usd": 0.0} for a in AREAS}
    for _endpoint, calls, cost, latency_ms in claude_rows:
        a = out["ai"]
        a["claude_calls"] += int(calls)
        a["claude_cost_usd"] += float(cost or 0)
        a["claude_latency_s"] += float(latency_ms or 0) / 1000
    for feature, service, calls, failures in market_rows:
        a = out[classify(feature)]
        a["market_calls"] += int(calls)
        a["market_failures"] += int(failures)
        a["market_cost_usd"] += int(calls) * unit_cost.get(service, 0.0)
    units = {k: v["claude_calls"] + v["market_calls"] for k, v in out.items()}
    total_units = sum(units.values())
    for k, v in out.items():
        v["work_units"] = units[k]
        v["work_unit_share"] = units[k] / total_units if total_units else 0.0
        v["render_share_usd"] = (render_monthly_usd or 0.0) * v["work_unit_share"]
        v["total_usd"] = v["claude_cost_usd"] + v["market_cost_usd"] + v["render_share_usd"]
    return out


def render_markdown(year_month, result, render_monthly_usd, data_date):
    lines = [
        f"### {year_month}",
        "",
        f"Data read {data_date}. Render dyno charge allocated: "
        + (f"${render_monthly_usd:.2f}" if render_monthly_usd is not None else "not given (dyno share shown as $0.00)")
        + ".",
        "",
        "| Feature area | Claude calls | Claude cost | Market-data calls (failed) | Market-data cost | Work-unit share | Render dyno share | Total |",
        "|--------------|-------------:|------------:|---------------------------:|-----------------:|----------------:|------------------:|------:|",
    ]
    for area in AREAS:
        v = result[area]
        lines.append(
            f"| {AREA_LABELS[area]} | {v['claude_calls']} | ${v['claude_cost_usd']:.4f} | "
            f"{v['market_calls']} ({v['market_failures']}) | ${v['market_cost_usd']:.4f} | "
            f"{v['work_unit_share'] * 100:.1f}% | ${v['render_share_usd']:.2f} | ${v['total_usd']:.2f} |"
        )
    tot = {k: sum(result[a][k] for a in AREAS) for k in
           ("claude_calls", "claude_cost_usd", "market_calls", "market_failures", "market_cost_usd",
            "render_share_usd", "total_usd")}
    lines.append(
        f"| **Total** | {tot['claude_calls']} | ${tot['claude_cost_usd']:.4f} | "
        f"{tot['market_calls']} ({tot['market_failures']}) | ${tot['market_cost_usd']:.4f} | 100% | "
        f"${tot['render_share_usd']:.2f} | ${tot['total_usd']:.2f} |"
    )
    return "\n".join(lines) + "\n"


CLAUDE_SQL = """
    SELECT endpoint, COUNT(*), COALESCE(SUM(cost_usd), 0), COALESCE(SUM(latency_ms), 0)
    FROM claude_audit_log
    WHERE generated_at >= %s AND generated_at < %s
    GROUP BY endpoint
"""
MARKET_SQL = """
    SELECT COALESCE(feature, 'unattributed'), service, COUNT(*), COUNT(*) FILTER (WHERE NOT success)
    FROM api_call_log
    WHERE called_at >= %s AND called_at < %s
      AND service = ANY(%s)
    GROUP BY 1, 2
"""


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--month", required=True, help="YYYY-MM (a complete calendar month)")
    parser.add_argument("--render-monthly-usd", type=float, default=None,
                        help="The month's Render dyno charge from the invoice")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", args.month):
        parser.error("--month must be YYYY-MM")

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
    from utils.api_attribution import UNIT_COST_USD, PROVIDER_SERVICES
    import psycopg2

    start, end = month_bounds(args.month)
    # UTC month bounds, as the audit tables store TIMESTAMPTZ.
    bounds = (f"{start.isoformat()} 00:00:00+00", f"{end.isoformat()} 00:00:00+00")
    with psycopg2.connect(os.environ["DATABASE_URL"]) as conn, conn.cursor() as cur:
        cur.execute("SET TRANSACTION READ ONLY")
        cur.execute(CLAUDE_SQL, bounds)
        claude_rows = cur.fetchall()
        cur.execute(MARKET_SQL, bounds + (list(PROVIDER_SERVICES),))
        market_rows = cur.fetchall()
    result = partition(claude_rows, market_rows, UNIT_COST_USD, args.render_monthly_usd)
    print(render_markdown(args.month, result, args.render_monthly_usd, date.today().isoformat()))


if __name__ == "__main__":
    main()
