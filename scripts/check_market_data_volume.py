#!/usr/bin/env python3
"""
Weekly market-data volume check (ST-16, BLG-OPS-195, EPIC-06, v9.17).

Calls GET /ops/api-call-attribution?window=weekly and compares each source's
weekly calls, failures and estimated cost with the baseline recorded in
docs/ops/data_pipeline_cost_baseline.md §4. When any figure is more than 2x its
baseline (§5), it prints an advisory naming the source and its top features.

The baseline figures live only in that document's §4 table. This script reads
the table at run time, so re-recording §4 (for example after BLG-OPS-217's
post-fix report) changes the check without touching the script or workflow.

§5 rules, as applied here:
  - Volume: a source's calls > 2x its baseline calls, or combined calls > 2x
    the combined baseline.
  - Failures: the same rule applied to failure counts.
  - Cost: combined estimated cost > 2x the baseline cost. While the baseline
    is $0.00, any non-zero estimated cost exceeds it.
  - "More than" is strict: exactly 2x is not an advisory.
  - A source with a baseline of 0 (or not in the §4 table at all, such as
    alpaca_trading, twelve_data or stooq) exceeds it with any non-zero figure,
    the same way §5 treats a $0.00 cost baseline.

Exit codes (read by .github/workflows/market-data-volume-check.yml):
  0  no figure over 2x baseline
  1  advisory: at least one figure over 2x baseline; the message is printed
     and, with --message-file, written to that file
  2  the check could not run (report call failed, bad response, baseline
     table unreadable). The workflow fails loudly on this, as
     ai-daily-cost-check.yml does.

Usage:
    API_URL=... API_KEY=... python3 scripts/check_market_data_volume.py \
        [--baseline docs/ops/data_pipeline_cost_baseline.md] [--message-file out.txt]
"""
import argparse
import os
import re
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASELINE_PATH = REPO_ROOT / "docs" / "ops" / "data_pipeline_cost_baseline.md"
THRESHOLD_MULTIPLIER = 2
TOP_FEATURES = 3
COMBINED = "combined"


class CheckError(Exception):
    """The check could not run; the workflow must fail loudly."""


# ---------------------------------------------------------------------------
# Baseline (docs/ops/data_pipeline_cost_baseline.md §4)
# ---------------------------------------------------------------------------

_SERVICE_RE = re.compile(r"\(`([a-z_]+)`\)")


def _number(cell):
    cleaned = cell.replace("*", "").replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError as exc:
        raise CheckError(f"baseline §4: cannot read {cell.strip()!r} as a number") from exc


def parse_baseline(markdown_text):
    """Read the §4 Weekly Baseline table.

    Returns {service: {"calls", "failures", "cost_usd"}} plus a "combined" key.
    Raises CheckError if the section, a service row or the Combined row is
    missing, so a reworded table fails the check instead of silently passing.
    """
    match = re.search(r"^## 4\. Weekly Baseline\s*$(.*?)^## ", markdown_text, re.M | re.S)
    if not match:
        raise CheckError("baseline: '## 4. Weekly Baseline' section not found")

    baseline = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|- "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] == "Source":
            continue
        service_match = _SERVICE_RE.search(cells[0])
        if service_match:
            key = service_match.group(1)
        elif "Combined" in cells[0]:
            key = COMBINED
        else:
            continue
        baseline[key] = {
            "calls": _number(cells[1]),
            "failures": _number(cells[2]),
            "cost_usd": _number(cells[3]),
        }

    if COMBINED not in baseline or len(baseline) < 2:
        raise CheckError("baseline §4: table must have at least one source row and a Combined row")
    return baseline


def load_baseline(path=DEFAULT_BASELINE_PATH):
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise CheckError(f"baseline: cannot read {path}: {exc}") from exc
    return parse_baseline(text)


# ---------------------------------------------------------------------------
# Report (GET /ops/api-call-attribution?window=weekly)
# ---------------------------------------------------------------------------

def fetch_weekly_report(api_url, api_key, timeout=60):
    """Return the report's `data` object. Any failure raises CheckError: a
    failed report call is never treated as zero calls."""
    url = f"{api_url.rstrip('/')}/ops/api-call-attribution"
    try:
        resp = requests.get(url, params={"window": "weekly"},
                            headers={"X-API-Key": api_key}, timeout=timeout)
    except requests.RequestException as exc:
        raise CheckError(f"report call failed: {exc}") from exc
    if resp.status_code != 200:
        raise CheckError(f"report call returned HTTP {resp.status_code}: {resp.text[:500]}")
    try:
        body = resp.json()
    except ValueError as exc:
        raise CheckError("report call returned a body that is not JSON") from exc
    data = body.get("data") if isinstance(body, dict) else None
    if (not isinstance(data, dict) or body.get("status") != "ok"
            or not isinstance(data.get("by_service"), list)):
        raise CheckError(f"report call returned an unexpected body: {str(body)[:500]}")
    return data


# ---------------------------------------------------------------------------
# Comparison (pure, no I/O)
# ---------------------------------------------------------------------------

def _exceeds(actual, base):
    return actual > THRESHOLD_MULTIPLIER * base


def find_exceedances(report, baseline):
    """Return a list of {"source", "measure", "actual", "baseline"} for every
    figure more than 2x its baseline. `source` is a service name or "combined".
    """
    found = []
    by_service = {row["service"]: row for row in report.get("by_service", [])}

    for service in sorted(by_service):
        row = by_service[service]
        base = baseline.get(service, {"calls": 0, "failures": 0})
        for measure, field in (("calls", "total_calls"), ("failures", "failure_count")):
            actual = row.get(field, 0) or 0
            if _exceeds(actual, base[measure]):
                found.append({"source": service, "measure": measure,
                              "actual": actual, "baseline": base[measure]})

    combined = baseline[COMBINED]
    combined_calls = sum((r.get("total_calls", 0) or 0) for r in by_service.values())
    combined_failures = sum((r.get("failure_count", 0) or 0) for r in by_service.values())
    combined_cost = report.get("estimated_cost_usd", 0) or 0
    for measure, actual in (("calls", combined_calls), ("failures", combined_failures),
                            ("cost_usd", combined_cost)):
        if _exceeds(actual, combined[measure]):
            found.append({"source": COMBINED, "measure": measure,
                          "actual": actual, "baseline": combined[measure]})
    return found


def top_features(report, source, n=TOP_FEATURES):
    """Features ranked by their calls to `source` (by_feature[].by_service),
    or, for "combined", the report's own top_contributors."""
    if source == COMBINED:
        return list(report.get("top_contributors", []))[:n]
    ranked = []
    for row in report.get("by_feature", []):
        calls = (row.get("by_service") or {}).get(source, 0) or 0
        if calls > 0:
            ranked.append((-calls, row["feature"], calls))
    ranked.sort()
    return [f"{feature} ({calls:,} calls)" for _, feature, calls in ranked[:n]]


def _fmt(measure, value):
    return f"${value:,.2f}" if measure == "cost_usd" else f"{value:,.0f}"


_MEASURE_LABEL = {"calls": "calls", "failures": "failures", "cost_usd": "estimated cost"}


def build_message(exceedances, report):
    """The advisory text, or None when nothing exceeds 2x baseline."""
    if not exceedances:
        return None
    lines = ["Market-data weekly volume advisory: over 2x the baseline in "
             "docs/ops/data_pipeline_cost_baseline.md §4."]
    for item in exceedances:
        source = item["source"]
        label = "all sources" if source == COMBINED else source
        features = top_features(report, source)
        lines.append(
            f"- {label}: {_MEASURE_LABEL[item['measure']]} {_fmt(item['measure'], item['actual'])} "
            f"vs baseline {_fmt(item['measure'], item['baseline'])}. "
            f"Top features: {', '.join(features) if features else 'none recorded'}."
        )
    lines.append("Check the report's by_feature breakdown for the feature that grew (§5).")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(api_url, api_key, baseline_path=DEFAULT_BASELINE_PATH):
    """Returns (exit_code, message_or_None). Raises CheckError on failure."""
    if not api_url or not api_key:
        raise CheckError("API_URL and API_KEY must be set")
    baseline = load_baseline(baseline_path)
    report = fetch_weekly_report(api_url, api_key)
    message = build_message(find_exceedances(report, baseline), report)
    return (1, message) if message else (0, None)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--baseline", default=str(DEFAULT_BASELINE_PATH))
    parser.add_argument("--message-file", default=None)
    args = parser.parse_args(argv)

    try:
        code, message = run(os.getenv("API_URL"), os.getenv("API_KEY"), args.baseline)
    except CheckError as exc:
        print(f"[ERROR] market-data volume check could not run: {exc}", file=sys.stderr)
        return 2

    if message:
        print(message)
        if args.message_file:
            Path(args.message_file).write_text(message, encoding="utf-8")
    else:
        print("[OK] no source over 2x its weekly baseline")
    return code


if __name__ == "__main__":
    sys.exit(main())
