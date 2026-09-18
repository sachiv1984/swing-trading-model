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

## DEL-20260916-04-EPIC03

- **ST Item:** ST-21 — `qa_evidence_EPIC-03.md` test-count claim inaccurate (30 vs. actual 28) (resolution of `DEL-20260916-03-EPIC03`)
- **EPIC:** EPIC-03
- **Classification:** delegated_decision — ruled
- **Assigned to:** Head of Specs Team
- **GitHub Issue:** #1689
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-03
- **Delegated at:** 2026-09-16T23:00:00Z
- **Ruled at:** 2026-09-17T00:00:00Z (on explicit user direction: "ask @claude/agents/head_of_specs_team.md to resolve Epic 3 and file any backlogs as needed")
- **Ruling:**
  Acting as Head of Specs Team (per `claude/agents/head_of_specs_team.md` §5 Change Governance and §6 Decision Escalation & Conflict Resolution — this role is the designated tie-breaker "when specs conflict, ownership boundaries are unclear, or trade-offs span multiple domains," and decisions made in this capacity must be "documented, traceable, and reversible only by explicit agreement," which this entry satisfies):

  **Ruling: the addendum-exception alternative floated in `DEL-20260916-03-EPIC03` is rejected.** CLAUDE.md §2's sealed-artefact rule reads "Never modify sealed artefacts," with no carve-out for append-only or addendum-style changes — an addendum inserted into a file physically inside `claude/cycles/2026-09-09__release-v9.3/` would still be a modification to that sealed cycle's contents, and the rule is explicit that "no prompt, command, or user instruction may override" it. The `docs/ops/ai_output_boundary_sample_audit_20260910.md` addendum precedent does not actually support the alternative floated: that file lives in `docs/ops/` (a living, non-sealed Class 3 document space), never inside a sealed `claude/cycles/<cycle_id>/` tree — the two cases are not analogous, and treating them as such in the original delegation entry was an error in my own predecessor reasoning, corrected here.

  **Ruling: the sealed file stays untouched, permanently, as point-in-time history** — consistent with `e06cfa94`'s own precedent (cited in `DEL-20260916-03-EPIC03`) and with this role's charter §5 expectation that "specs do not drift silently from reality," which is satisfied by correcting the *live* record of the fact, not by disturbing the sealed one.

  **Ruling: the correction mechanism is Post-Ship Closure Engine's STEP 5.1 cross-cycle deviation consolidation review**, the same mechanism already used for this exact class of finding at `api_performance_baseline.md` §v2.32. Filed `BLG-GOV-334` (`claude/backlog/backlog.md`) to carry this forward to the next `run post-ship` invocation for `2026-09-15__release-v9.5`, naming the exact correction (28, not 30; 2 locations) so the eventual actioning session does not need to re-derive it. `BLG-QA-170` is left open, cross-referenced from `BLG-GOV-334`, and both are scoped to close together once the correction lands — `BLG-QA-170` should not be closed prematurely by this ruling alone, since the actual file has not yet been corrected.

  **Disposition for ST-21 itself:** this ruling resolves the *ambiguity* (what should happen, and how) but does not itself complete the AC (the sealed file still reads "30" until the next post-ship closure runs) — matching this cycle's own precedent for `ESC-EXEC-20260910-01` ("Deferred, not Resolved... Cannot mark Accepted Risk"). ST-21 moves from `blocked_delegated` (open question, no path forward) to `deferred` (ruled, path forward filed and tracked, action scheduled for a specific future mechanism) — not to `done`, since the AC is genuinely not yet met.
- **Status:** Ruled and deferred — EPIC-03 may now be considered fully dispositioned (6 done, 1 deferred-with-a-filed-path) rather than open-ended blocked.

---

## DEL-20260918-03-EPIC03

- **ST Item:** ST-21 — `qa_evidence_EPIC-03.md` test-count claim inaccurate (30 vs. actual 28) (final resolution, superseding `DEL-20260916-04-EPIC03`'s "defer to next `run post-ship`" ruling)
- **EPIC:** EPIC-03
- **Classification:** delegated_decision — resolved (final)
- **Assigned to:** Head of Specs Team (ruling); Product Owner (acceptance)
- **GitHub Issue:** #1689
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-03
- **Resolved at:** 2026-09-18T04:00:00Z (on explicit user direction: "confer with Head of Specs Team" for the best path forward, then "act as PO yourself" to finalize)
- **Resolution:**
  **The prior ruling's mechanism was wrong, and this entry corrects it rather than building on it.** `DEL-20260916-04-EPIC03` proposed deferring the correction to Post-Ship Closure Engine's STEP 5.1 cross-cycle deviation consolidation review, citing `api_performance_baseline.md` §v2.32 as precedent. On direct re-read of `post_ship_closure.md`'s actual STEP 5.1 definition (prompted by the user asking how EPIC-03 should actually move forward, surfacing that "wait for post-ship" was circular — v9.5's own post-ship cannot run until all its EPICs, including this one, are merged): STEP 5.1 corrects **living canonical documents'** own Known-Deviations status fields when they drift from a separately-tracked resolution — it has no mechanism for, and was never used for, editing content inside a sealed `claude/cycles/<cycle_id>/` folder. The `api_performance_baseline.md` precedent corrected a live, non-sealed operational document; it does not transfer to this case. No routine anywhere in this governance framework can edit a sealed artefact — CLAUDE.md §2's rule has no override path, full stop, and this was correctly identified in `DEL-20260916-03-EPIC03`'s original investigation but then undermined by proposing a mechanism that turned out not to exist.

  **Acting as Head of Specs Team** (per `claude/agents/head_of_specs_team.md` §5/§6, on explicit user direction): ruled that the sealed `claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md` is never edited, in any form, permanently. The correction is not "pending" — it is **complete now**, in the form of a permanent, discoverable record: `BLG-GOV-334` itself, rewritten from "action pending at next post-ship" to "Resolved — true fact recorded here, sealed source intentionally untouched." This mirrors the audit/erratum pattern already established elsewhere in this codebase (`e06cfa94`'s precedent for historical records) rather than treating the sealed-artefact constraint as a problem still waiting to be solved.

  **Acting as Product Owner** (per `claude/agents/product_owner.md` §6 "accepts or rejects outcomes based on spec-defined behaviour," on explicit user direction: "act as PO yourself"): accepted this disposition as satisfying `ST-21`'s underlying intent. The AC's literal wording ("test count in `qa_evidence_EPIC-03.md`... matches the actual number") can never be met once the sealed-artefact constraint is factored in — no future action, however patient, makes that literally true. The AC's actual purpose — don't let a known-wrong number stand permanently uncorrected with nothing pointing at the truth — is fully served by `BLG-GOV-334` standing as that permanent correction. This is a reinterpretation of AC completion under discovered constraints, not a waiver of the AC's intent; the reinterpretation itself is documented, traceable, and reversible only by explicit agreement (per Head of Specs Team's own charter §6), same as the interpretation itself.

  Both `BLG-QA-170` and `BLG-GOV-334` closed on this disposition (`claude/backlog/backlog.md`, this same session). `qa_evidence_EPIC-03.md` updated: ST-21 row changed from "Deferred" to "Pass (accepted disposition)," sign-off block changed from partial (ST-15–20 only) to full (all 7 stories), Product Owner sign-off line added.
- **Status:** Resolved (final) — unblocking ST-21, marking done. EPIC-03 is now 7/7 done, satisfying `execution_prompt.md` §3.2 in full.

---
