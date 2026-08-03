Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-03
Cycle: 2026-08-03__release-v8.1

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-08-03__release-v8.1
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-08-03
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `governance_sync.yml` auto-closes GitHub issues on any commit referencing the story ID, not only completion commits — fired twice this sprint on delegation-record commits (issue #1169 for ST-02, issue #1181 for ST-14), requiring manual reopen with clarifying comment each time | Phase 3 | C | defer | Reopened both issues in-session; permanent regex fix filed as `BLG-GOV-285` | Infrastructure & Operations Owner | BLG-GOV-285 |
| Cross-EPIC merge conflict between EPIC-04 and EPIC-03 included a silent same-line bad-merge: both branches independently bumped `sprint_planning_prompt.md` to the same version number (`3.14`) for two semantically different changes; git did not flag this as conflicting because the literal text matched, so it was not caught until manual line-by-line review during CLAUDE.md §8 resolution | Phase 3 | C | defer | Resolved in-session (renumbered EPIC-04's bump to `3.15`); CLAUDE.md §8's resolution procedure does not currently name this "identical-text masks differing semantics" failure mode explicitly — recommend adding it as a named check | Head of Specs Team | next sprint_planning_prompt.md / CLAUDE.md §8 revision cycle |
| `generate_execution_summary.py`'s regenerated `execution_state.json` output was left uncommitted after the EPIC pr_status/status sync commit (`f728279a`) — the script was run but its output diff was never staged, leaving a working-tree change that was only caught during STEP 5.1 of sprint close | Phase 3 | C | action-now | Caught and committed separately (`354b0ecd`) during STEP 5.1 pre-seal checks | Sprint Execution Engine | — |
| ST-16's acceptance criteria named a target spec location (`strategy_rules.md §5 (Arc 5)`) that does not exist under that name — §5 there is unrelated content; the AC's own "or a linked spec" fallback was already satisfied by `si02_drift_score.md §2`, so the story was reclassified `delegated_decision` → `autonomous` mid-execution per LL-v2.3-EX-02 rather than escalated | Phase 3 | B | action-now | Reclassified and resolved same session; no fresh decision was needed, threshold was already correctly product-decided, only missing a cross-reference | Sprint Execution Engine | — |

**Recurrence Notes:**
The `governance_sync.yml` false-positive is now a confirmed 3rd-plus recurrence across this cycle alone (2 fires) on top of prior-cycle occurrences implied by its own backlog filing — this crosses the threshold where a workaround-only response (reopen + comment) is no longer proportionate; `BLG-GOV-285` should be prioritized accordingly rather than left as routine backlog debt.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-08-03__release-v8.1
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-08-03
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-07-30__release-v8.0 (`lessons_learnt_cycle.md` `## Phase 4`) — one open friction item (sign-off format disagreement between `execution_prompt.md`'s EPIC consolidation step and `delivery_verification_prompt.md` STEP -1.3's recognised-format list, for `delegated_backend`/`delegated_decision`-heavy EPICs), plus one carried-forward deferred patch from v7.10 (`completed_items` cross-EPIC union reconciliation check not yet formally landed in `execution_prompt.md`). **Both checked this run:** the sign-off format friction item is confirmed resolved — the current `delivery_verification_prompt.md` (v3.6) already includes the named domain-authority class exception (`ESC-CLOSE-20260731-01`), which cleared EPIC-02's `Infrastructure & Operations Owner` signer directly with no counter-sign required this run. The `completed_items` reconciliation item was not directly testable (outside this routine's scope to confirm the prompt text), but `execution_state.json.completed_items` for this cycle correctly lists all 19/19 done stories with no staleness — consistent with, but not proof of, the formal fix having landed.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| EPIC-07's `qa_evidence_EPIC-07.md` flagged (via Head of Engineering agent-mediated review) that `delivery_verification_prompt.md` STEP -1.3A hand-writes a recovered `pr_number` directly into `execution_state.json` on PR-recovery, but under the new per-EPIC `execution_state/EPIC-xx.json` mechanism (ST-19, this cycle) that consolidated file is disposable/regenerate-on-read — such a write would be silently lost on the next regeneration. Not triggered this run (all 7 EPICs already had non-null `pr_number`), but will fire the next time PR recovery is needed against a per-EPIC-mechanism cycle. | Phase 4 | B | defer | Redirect STEP -1.3A's recovered-`pr_number` write to the owning `execution_state/EPIC-xx.json` file instead of the regenerate-on-read summary. File: `claude/system/delivery_verification_prompt.md` §STEP -1.3A. | Head of Specs Team | next `delivery_verification_prompt.md` revision, before PR recovery is next exercised |

**Recurrence Notes:**
Not a recurrence — first occurrence of this specific friction item. It is a direct, foreseeable consequence of this cycle's own ST-19 (per-EPIC execution state mechanism), surfaced proactively by the EPIC's own agent-mediated reviewer rather than discovered the hard way at a future verification run.

## Recurrence Escalations (Phase 4)

None — the one open prior-cycle friction item (sign-off format disagreement) is confirmed resolved, not escalated further.

## Process improvements actioned this run (Phase 4)

None applied to governance prompts this run — the one new friction item identified (STEP -1.3A write-target staleness) targets `delivery_verification_prompt.md`, outside this routine's write scope, and is not yet exercised in practice (no PR recovery was needed this run). Recorded as a deferred patch below rather than actioned now.

## Outstanding deferred patches (Phase 4)

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/delivery_verification_prompt.md` | STEP -1.3A — PR Number Recovery | Redirect the recovered `pr_number` write from the shared `execution_state.json` (now disposable/regenerate-on-read post-ST-19) to the owning `execution_state/EPIC-xx.json` file. | Head of Specs Team | before PR recovery is next exercised |
| `claude/system/execution_prompt.md` | STEP 5 — Sprint Close (seal step) | Carried forward from v7.10/v8.0 Phase 4 (still not confirmed landed in the prompt itself): add the `completed_items` cross-EPIC union reconciliation check formally, rather than relying on it being manually re-applied each cycle. | Head of Specs Team | next `run sprint` invocation |

## Escalations (Phase 4)

None.
