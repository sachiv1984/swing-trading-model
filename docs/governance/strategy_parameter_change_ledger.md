**Owner:** Strategy Rules & System Intent Owner
**Class:** Reference Document (Class 2)
**Status:** Active
**Last Updated:** 2026-10-01 (ST-22, EPIC-04, v9.9, BLG-GOV-344 — initial creation, backfilled from `claude/strategy/strategy_rules.md`'s own Change log, versions 1.0–1.12)

# Strategy Parameter Change Ledger

## Purpose

Tracks every change to `claude/strategy/strategy_rules.md` §11's **current production parameters** over time, so a reviewer can see at a glance when each parameter was set, whether it has ever changed, and which §12.3 change-control record (if any) justified a change — without re-deriving this from the full strategy_rules.md Change log table.

This ledger is a derived index, not a parallel source of truth: `claude/strategy/strategy_rules.md` §11 remains canonical for current values, and §12.3 remains canonical for the change-control requirements a future change must satisfy. This file exists to answer "when did X last change, and why" without re-reading the entire strategy_rules.md Change log.

## §11 Parameters Tracked

| Parameter | Current Value | Version Introduced | Date Introduced | Last Changed | Change-Control Record |
|---|---|---|---|---|---|
| Grace period | 10 days | 1.0 | February 2026 | Never changed since v1.0 | — |
| Initial / losing stop multiplier | 5 × ATR | 1.0 | February 2026 | Never changed since v1.0 | — |
| Profitable stop multiplier | 2 × ATR | 1.0 | February 2026 | Never changed since v1.0 | — |
| ATR period | 14 days | 1.0 | February 2026 | Never changed since v1.0 | — |

## Backfill Method

Cross-referenced every entry in `strategy_rules.md`'s Change log table (v1.0 through v1.12, the full history at the time of this ledger's creation) against the four §11 values above. No entry from v1.1 through v1.12 modifies any of these four values — each is either explicitly marked "no behavioural/calculation change," "documentation only," or scoped to a different section (§4.1, §4.2, §7, §12.2, §13.x, §15, §16) that does not touch §11 itself. All four parameters have held their v1.0 initial values for the entire recorded history as of this ledger's creation.

**Entries reviewed and confirmed not to change §11 values:** 1.1 (§13 expansion), 1.2 (§4.1 added), 1.3 (§4.1.7 revision), 1.4 (§4.2 added), 1.5 (§13.4 note), 1.6 (§13.5 cadence), 1.7 (§13.5 roster), 1.8 (§4.1.8 example), 1.9 (§12.2/§13.6/§15/§16 added), 1.10 (§7.2 breakeven floor, documentation-only per its own entry), 1.11 (§13.5 roster), 1.12 (§7.1 RISK-01 ATR-formula-identity ruling — clarifies which code paths use which formula; does not change the ATR period or either stop multiplier value).

## Maintenance

**When a future §11 parameter value actually changes:** add a new row's worth of history by updating the affected parameter's "Last Changed" / "Change-Control Record" columns in the table above, and append a dated entry below citing the `strategy_rules.md` Change log version/row that made the change and the §12.3 change-control record satisfying all five of its requirements (documented, versioned, rationale + impact stated, comparability-loss acknowledged, applied consistently across backtests/live logic/documentation).

### Change History (post-creation)

*(No entries yet — this ledger was created with all four parameters still at their v1.0 initial values. The first real parameter change will add its own dated row here.)*
