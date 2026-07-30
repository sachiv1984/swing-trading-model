"""
Strategy Version Registry — SI-04 (ST-01, EPIC-01, v7.7, BLG-FEAT-75).

There is no `strategy_version` column on `trade_history` and no separate
version-tracking database table (confirmed absent at v7.7 sprint execution
research — contradicts a stale claim in claude/backlog/backlog.md BLG-FEAT-75
that version-tagged trade history "already exists"). Instead, trades are
attributed to a strategy version by `entry_date` falling within that
version's active window, where each version's effective date comes directly
from claude/strategy/strategy_rules.md's own Change Log table.

This registry is a living reference, not a database table (contract
`strategy_version_comparison_contract.md` §Implementation Notes 2 left the
format "TBD at implementation time" — a hardcoded list mirroring the
canonical Change Log was chosen over a new schema/migration to avoid
introducing storage for data that is already recorded, in a different shape,
in strategy_rules.md itself).

Maintenance obligation: this list must be updated in the same commit as any
new row added to strategy_rules.md's Change Log table (mirrors the living-
reference obligation on docs/specs/frontend/design_system.md).

Attribution rule (Strategy Rules & System Intent Owner decision, 2026-07-23,
v7.7 ST-01 sprint execution): each version's window is
[effective_date, next_version's effective_date) in Change Log order. Two
versions sharing the same effective date (1.1 and 1.2, both 18 Feb 2026) are
NOT a data-entry error — 1.1 was superseded same-day, so its window is
zero-width and it will correctly report zero attributable trades /
insufficient_data if ever queried directly.
"""

from datetime import date

# Ordered oldest -> newest, per strategy_rules.md "## Change log" table.
STRATEGY_VERSION_REGISTRY = [
    {"version": "1.0", "effective_date": date(2026, 2, 1)},   # "February 2026" — no day specified; first-of-month used for ordering only
    {"version": "1.1", "effective_date": date(2026, 2, 18)},
    {"version": "1.2", "effective_date": date(2026, 2, 18)},
    {"version": "1.3", "effective_date": date(2026, 2, 19)},
    {"version": "1.4", "effective_date": date(2026, 5, 20)},
]


def get_current_strategy_version() -> str:
    """Return the version label of the currently active (latest) strategy version.

    ST-01 (EPIC-01, v8.0, BLG-SPEC-78): used to stamp `strategy_version_at_entry`
    on trade_plans/positions at row-creation time — the registry's last entry is
    always the current version since it is maintained in the same commit as any
    new strategy_rules.md Change Log row (see module docstring).
    """
    return STRATEGY_VERSION_REGISTRY[-1]["version"]


def resolve_version_window(version_label: str):
    """Return (start_date, end_date_or_None) for a version label, or None if not found.

    end_date is exclusive; None means the window is still open (current version).
    """
    for i, entry in enumerate(STRATEGY_VERSION_REGISTRY):
        if entry["version"] == version_label:
            start = entry["effective_date"]
            end = (
                STRATEGY_VERSION_REGISTRY[i + 1]["effective_date"]
                if i + 1 < len(STRATEGY_VERSION_REGISTRY)
                else None
            )
            return (start, end)
    return None
