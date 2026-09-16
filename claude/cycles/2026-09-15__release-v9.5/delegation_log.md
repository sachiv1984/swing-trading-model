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

## DEL-20260916-02

- **ST Item:** ST-04 — Consolidate duplicated ATR trailing-stop recalculation logic (resolution of `DEL-20260916-01`)
- **EPIC:** EPIC-01
- **Classification:** delegated_decision — resolved
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1672
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-01
- **Delegated at:** 2026-09-16T20:35:00Z
- **Resolved at:** 2026-09-16T21:10:00Z (on explicit user direction: "act as relevant agent and resolve")
- **Resolution:**
  On re-investigation before rendering a decision, found `claude/backlog/backlog_archive.md`'s retired `BLG-BE-102` (P0, shipped v8.9, EPIC-01, ST-01) had already fully investigated and resolved this exact question: the entry-price breakeven floor in `calculate_trailing_stop` is intentional live-production behaviour (fixed a P0 bug where a profitable position's stop could stay frozen below entry), and `backend/position_manager.py`'s simpler backtest-tool formula is a deliberate, tested, documented exception (`tests/test_trailing_stop_breakeven_floor.py::TestPositionManagerNotOnLiveStopPath`) — not an unresolved divergence. `BLG-BE-119`'s framing as a fresh, unresolved "is this intentional?" question was therefore inaccurate; the only genuine gap was that `strategy_rules.md` §7.2 never had the already-shipped floor formalised into its formula text.

  Acting as Strategy Rules & System Intent Owner (on explicit user direction, matching the precedent already used for `qa_evidence_EPIC-04.md` ST-15 at `2026-09-14__release-v9.4`): ratified the floor, added it to `strategy_rules.md` §7.2 as a normative rule with full rationale and an explicit §12.3 comparability exception citing the `BLG-BE-102` precedent (v1.9 -> v1.10). No live code change — production already behaves this way. `position_manager.py` intentionally left unchanged, per the same precedent.

  `ST-04`/`BLG-BE-114`'s original scope is therefore resolved as: (a) the 2 production call sites in `position_service.py` already share one implementation (`calculate_trailing_stop`) — satisfies "single shared implementation exists; all call sites use it" for the production side; (b) `tests/test_stop_reconciliation.py`'s independent spec-formula helper is intentionally NOT consolidated — it exists specifically to catch backtest/live divergence on the shared base formula, and merging it into `calculate_trailing_stop` would defeat that purpose (same reasoning already applied to `position_manager.py` at v8.9). No further code consolidation is needed or desirable.
- **Status:** Resolved — unblocking ST-04, marking done.

---

## DEL-20260916-03-EPIC03

- **ST Item:** ST-21 — `qa_evidence_EPIC-03.md` test-count claim inaccurate (30 vs. actual 28)
- **EPIC:** EPIC-03
- **Classification:** delegated_decision (discovered mid-execution — this story's own AC requires an action this engine's write scope and CLAUDE.md's sealed-artefact rule both prohibit)
- **Assigned to:** Head of Specs Team (document lifecycle authority)
- **GitHub Issue:** #1689
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-03
- **Delegated at:** 2026-09-16T23:00:00Z
- **What is needed:**
  `BLG-QA-170`'s scope names the correction target as `claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md` — a file inside a **different, already-Published/sealed cycle** (`claude/cycles/2026-09-09__release-v9.3/state.json`: `"status": "Published"`, `"sealed": {"sealed_utc": "2026-09-09T02:20:00Z", ...}`). Two independent, non-negotiable constraints both block a direct fix from this session: (1) CLAUDE.md §2 — "Never modify sealed artefacts... immutable," a rule "no prompt, command, or user instruction may override"; (2) `execution_prompt.md` §7 Write Scope Restriction — this routine's write scope covers `claude/cycles/<cycle_id>/...` only for the *active* cycle (`2026-09-15__release-v9.5`), not `claude/cycles/2026-09-09__release-v9.3/...`.

  The consolidation commit that removed the analogous stale-filename references for ST-05's SignalCard work (`e06cfa94`) explicitly confirms this is intentional codebase practice, not an oversight: *"Historical changelog/report entries in `docs/product/changelog.md` and sealed cycle records were left untouched — they describe point-in-time history, not current state."* A qa_evidence log for a closed, Published cycle is exactly that class of record.

  The verified fact underneath (28 tests, not 30) is confirmed independently this session: `grep -c "^def test_" tests/test_cost_monitoring.py` on `main` (pre-EPIC-02, matching what existed at the v9.3 PR's head commit) returns 28. This is not in dispute — only the *mechanism* for recording the correction against a sealed record is blocked.

  Precedent for the correct resolution path exists in this same codebase: `api_performance_baseline.md`'s Document History §v2.32 entry shows exactly this class of cross-cycle historical correction being made by the **Post-Ship Closure Engine's STEP 5.1 cross-cycle deviation consolidation review** — a different governed routine with its own write scope, not Sprint Execution. Alternatively, an addendum-style correction note (matching `docs/ops/ai_output_boundary_sample_audit_20260910.md`'s "## Addendum" convention for correcting a Class-3-but-still-sealed-in-spirit record without altering the original claim) may be the right mechanism if Head of Specs Team judges the sealed-cycle boundary does not apply as strictly to a qa_evidence log specifically.
- **Status:** Blocked — awaiting Head of Specs Team ruling on the correction mechanism (cross-cycle deviation consolidation at next `run post-ship`, an addendum exception, or another disposition). The verified correct fact (28, not 30) is recorded here and in this commit so it is not lost regardless of which mechanism is eventually used.

---
