Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-16

---

# Delegation Log — 2026-09-15__release-v9.5

Append-only. Do not edit previous entries.

---

## DEL-20260916-01

- **ST Item:** ST-04 — Consolidate duplicated ATR trailing-stop recalculation logic
- **EPIC:** EPIC-01
- **Classification:** delegated_decision (reclassified from `autonomous` at Sprint Planning per §5.1 mid-sprint reclassification — see rationale below)
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1672
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-01
- **Delegated at:** 2026-09-16T20:35:00Z
- **What is needed:**
  Diffing the 3 named implementations before consolidating (per ST-04's own Notes: "diff all 3 existing implementations line-by-line ... file any unclear divergence as its own item rather than guess") surfaced a genuine, previously-uncaught behavioural divergence: `backend/utils/calculations.py::calculate_trailing_stop` (production — used by both `position_service.py` call sites) floors a profitable position's stop at `entry_price` (`max(current_stop, new_stop, entry_price)`); `claude/strategy/strategy_rules.md` §7.2/§7.3 (canonical spec), `backend/position_manager.py` (backtest tool), and `tests/test_stop_reconciliation.py`'s spec-formula helpers all agree on a two-term formula with no entry-price floor. No existing golden vector exercises the floor-binding case, so this has never been caught. Filed as `BLG-BE-119` with full detail. This is a live-trading risk-logic correctness question, not a documentation gap the engine can resolve unilaterally — resuming ST-04's consolidation requires a ratified answer to "is the entry-price floor intentional?" first (either update the spec + backtest tool to match production, or remove the floor from production — the latter is a live behaviour change on real capital).
- **Status:** Blocked — awaiting Strategy Rules & System Intent Owner decision on `BLG-BE-119`.

---
