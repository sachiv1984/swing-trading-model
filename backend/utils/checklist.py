"""Trade Plan checklist: which items are the trader's judgement, and how many
are unticked.

One rule for both readers (ST-13 pre-commit review, v9.18): the
checklist_skipped event writer (routers/trade_plans._unchecked_count) and the
rules-followed evidence (database.get_rules_followed_evidence). Judgement items
are every entry except the two system statuses (trade_plan.md v1.30 §6.2:
heat_limit_checked "Position size checks" and stop_defined "Stop level
defined") and anything saved with "auto": true (ESC-EXEC-20261126-01). A
non-dict entry counts as an unticked judgement item, as the writer has always
counted it.
"""
import json
from typing import Tuple

SYSTEM_CHECKLIST_IDS = frozenset({"heat_limit_checked", "stop_defined"})


def _as_list(checklist_items):
    items = checklist_items
    if isinstance(items, str):
        try:
            items = json.loads(items)
        except ValueError:
            return None
    return items if isinstance(items, list) else None


def is_judgement_item(item) -> bool:
    if not isinstance(item, dict):
        return True
    return item.get("auto") is not True and item.get("id") not in SYSTEM_CHECKLIST_IDS


def count_unchecked_judgement_items(checklist_items) -> Tuple[int, int]:
    """(unchecked, total) over the judgement items; (0, 0) for an empty,
    missing or unreadable checklist."""
    items = _as_list(checklist_items)
    if not items:
        return 0, 0
    judged = [item for item in items if is_judgement_item(item)]
    unchecked = sum(1 for item in judged if not (isinstance(item, dict) and item.get("checked") is True))
    return unchecked, len(judged)
