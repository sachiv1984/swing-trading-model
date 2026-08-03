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
