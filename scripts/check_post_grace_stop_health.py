#!/usr/bin/env python3
"""
Post-deploy synthetic check: post-grace positions have a stop and an
active_atr_multiplier in the strategy_rules.md §11 set.

ST-18 (BLG-OPS-179, EPIC-03, v9.11). v9.9 exposed `active_atr_multiplier`
and `stop_calculated_at` on GET /positions; nothing checked them after a
deploy, so a regression to a non-§11 multiplier or a missing stop would be
noticed only by the user. The allowed multipliers come from
backend/strategy_parameters.py, the single source fixed by the v9.10
ruling (a) on BLG-BE-138, so this check cannot drift from the live stop path.

Checks every open position whose grace period is over (grace_period false):
  1. current_stop is present and > 0
  2. active_atr_multiplier is one of the §11 values (INITIAL 5.0, PROFIT 2.0)
Grace positions are skipped: their stop is not enforced and
active_atr_multiplier is null by design (position_endpoints.md).

Awaiting first recompute (BLG-OPS-184, v9.11): since ST-16 (strategy_rules.md
§6.3 v1.15) nothing stamps active_atr_multiplier during grace, so a position
that has just left grace has a null multiplier and a null stop_calculated_at
until the next nightly run (22:30 UTC weekdays) recomputes it. Such a position
is reported as pending, not as a violation, while its holding days are at most
GRACE_PERIOD_DAYS + PENDING_TOLERANCE_DAYS (covers a weekend and one missed
nightly run). Past that window a null multiplier is a violation again. Check 1
(a stop is present) applies throughout.

Input: --fixture <json file>, or --api-url/--api-key (GET {api_url}/positions).
Accepts either a bare array or {"data": [...]}.
Exit 0 = healthy, 1 = violations found (printed one per line), 2 = could
not read positions. .github/workflows/post-deploy-stop-health.yml runs it
after each production deploy and alerts through the existing Telegram path.
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
from strategy_parameters import GRACE_PERIOD_DAYS, INITIAL_ATR_MULTIPLIER, PROFIT_ATR_MULTIPLIER  # noqa: E402

ALLOWED_MULTIPLIERS = (INITIAL_ATR_MULTIPLIER, PROFIT_ATR_MULTIPLIER)
PENDING_TOLERANCE_DAYS = 3


def _positions(payload):
    if isinstance(payload, dict):
        payload = payload.get("data", payload.get("positions", []))
    return [p for p in payload if (p.get("status") or "open") == "open"]


def awaiting_first_recompute(p):
    """True for a position just past grace that no path has recomputed yet (BLG-OPS-184)."""
    if p.get("active_atr_multiplier") is not None or p.get("stop_calculated_at"):
        return False
    try:
        days = int(p.get("holding_days"))
    except (TypeError, ValueError):
        return False
    return GRACE_PERIOD_DAYS <= days <= GRACE_PERIOD_DAYS + PENDING_TOLERANCE_DAYS


def find_violations(positions):
    violations = []
    for p in positions:
        if p.get("grace_period") is True:
            continue
        ticker = p.get("ticker", "?")
        stop = p.get("current_stop")
        try:
            stop_ok = stop is not None and float(stop) > 0
        except (TypeError, ValueError):
            stop_ok = False
        if not stop_ok:
            violations.append(f"{ticker}: post-grace position has no stop (current_stop={stop!r})")
        if awaiting_first_recompute(p):
            continue
        mult = p.get("active_atr_multiplier")
        try:
            mult_ok = mult is not None and any(abs(float(mult) - a) < 1e-9 for a in ALLOWED_MULTIPLIERS)
        except (TypeError, ValueError):
            mult_ok = False
        if not mult_ok:
            violations.append(
                f"{ticker}: active_atr_multiplier={mult!r} is not a §11 value {ALLOWED_MULTIPLIERS}"
            )
    return violations


def _load(args):
    if args.fixture:
        return json.loads(Path(args.fixture).read_text())
    req = urllib.request.Request(f"{args.api_url.rstrip('/')}/positions", headers={"X-API-Key": args.api_key or ""})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--fixture")
    src.add_argument("--api-url")
    ap.add_argument("--api-key")
    args = ap.parse_args(argv)
    try:
        positions = _positions(_load(args))
    except Exception as exc:  # network, auth or JSON failure
        print(f"ERROR: could not read positions: {exc}")
        return 2
    violations = find_violations(positions)
    checked = sum(1 for p in positions if p.get("grace_period") is not True)
    pending = [p.get("ticker", "?") for p in positions
               if p.get("grace_period") is not True and awaiting_first_recompute(p)]
    if pending:
        print(f"PENDING: {len(pending)} position(s) just past grace, awaiting first stop recompute: {', '.join(pending)}")
    if violations:
        print(f"FAIL: {len(violations)} stop-health violation(s) across {checked} post-grace position(s):")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"OK: {checked} post-grace position(s) have a stop and a §11 multiplier {ALLOWED_MULTIPLIERS}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
