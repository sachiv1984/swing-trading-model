"""Rules followed / rules broken per closed trade.

metrics_definitions.md §Rules Followed (per closed trade) — ST-13, BLG-FE-320,
EPIC-02, v9.18. Definition approved by the Metrics Definitions & Analytics
Owner (ESC-EXEC-20261124-03), revised ESC-EXEC-20261126-02: plan-time events
join through the plan, and the evidence date is when the position row was
created (positions.created_at), not the user-entered entry_date. A deterministic classification of the user's
own recorded events: no score, ranking or advice (strategy_rules.md §13).
"""
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

# From this date the pre-entry checks run on every Trade Entry route (v9.15
# ST-01, commit e0a78667), so a position created on or after it in the app
# went through them.
CHECKS_ON_EVERY_ROUTE_FROM = date(2026, 11, 4)

RED_FLAG_REASONS = frozenset({
    "pre_entry_override",
    "checklist_skipped",
    "stop_prompt_dismissed",
    "drawdown_prompt_dismissed",
})


def _as_date(value) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def classify_rules(trade: Dict, evidence: Dict[str, Dict]) -> Tuple[Optional[bool], List[str]]:
    """(rules_followed, rules_broken) for one trade_history row.

    `evidence` is database.get_rules_followed_evidence's mapping; the trade
    row carries `position_created_at` (positions.created_at). The exit reason
    never counts (strategy_rules.md §8.3: a manual exit is allowed).
    """
    position_id = trade.get("position_id")
    if position_id is None or str(position_id) == "":
        return None, []
    ev = evidence.get(str(position_id)) or {}
    broken = {e for e in ev.get("events", set()) if e in RED_FLAG_REASONS}
    if ev.get("override_acknowledged"):
        broken.add("pre_entry_override")
    if broken:
        return False, sorted(broken)
    created = _as_date(trade.get("position_created_at"))
    if ev.get("has_snapshot") or (created is not None and created >= CHECKS_ON_EVERY_ROUTE_FROM):
        return True, []
    return None, []
