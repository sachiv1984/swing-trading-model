Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-17
Cycle: 2026-08-14__release-v8.8

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-08-14__release-v8.8
**Section anchor:** `## Phase 3`
**Filed:** 2026-08-17
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `execution_state.json.merge_gate`/per-EPIC `pr_status` went stale on `main` five times this cycle (after PR #1423, then again after #1424, #1425, #1426, #1427), requiring a manual sync at every subsequent EPIC's conflict-resolution merge and a final direct sync commit after #1428. This is a 4th consecutive cycle showing this class of staleness (v8.1/v8.5/v8.6/v8.7 all recorded it), but this cycle reveals a broader recurrence mode than previously assessed: prior cycles' occurrences were session-*boundary* staleness, caught by the existing session-start sync check (LL-v3.9-P3-1/LL-v7.2-P3-01). This cycle's staleness recurred mid-session, once per individual human-driven PR merge, with no equivalent check re-firing between merges — the session-start check only runs once, at invocation. | Phase 3 | C | defer | No structural fix applied this run — the existing STEP 5.0A pre-seal sync and the per-conflict-resolution-commit sync (both already exercised successfully this cycle, catching every instance before seal) remain sufficient as a *backstop*, but nothing catches the staleness *between* merges for a user checking PR status mid-session. Recommend either (a) a `governance_sync.yml` GitHub Action triggered on merge to `main` that writes the sync directly, or (b) an explicit `execution_prompt.md` instruction for STEP 8's "next EPIC in queue" flow to re-run the LL-v3.9-P3-1 sync check on every "PR merged" report from the user, not only at session start. | Head of Specs Team | next `execution_prompt.md` revision |
| `EPIC-07`/ST-29 independently collided with `EPIC-03`/ST-13 on *both* `OPERATIONAL_GUIDE.md` v4.162 and `post_ship_closure.md` v2.27 in the same commit (both files bumped together per the normal §6 pattern) — the first collision was caught and disclosed at commit time (`CLAUDE.md` §8 step 2a check applied), but the second was missed entirely, only surfacing later via PR #1428's Director of Quality dual-role review running a real test merge. Root cause: the collision check was applied once and treated as clearing the whole commit, rather than being repeated against every file the commit touched. | Phase 3 | D | action-now | `CLAUDE.md` §8 step 2a extended with an explicit "check every co-bumped file individually" instruction, citing this exact recurrence as the precedent. Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`. | Head of Specs Team | — |

**Recurrence Notes:**
Friction item 1 (`merge_gate`/`pr_status` staleness) is a 4th consecutive cycle recurrence of the general staleness pattern (v8.1 → v8.5 → v8.6 → v8.7 → v8.8), but the specific mechanism identified this cycle (mid-session, per-merge staleness) is new — prior cycles' entries assessed the session-boundary variant as "by-design recovery behaviour, not a gap." This entry does not reconfirm that assessment; it identifies a distinct gap the prior fix does not cover, and defers a structural patch rather than closing it as before. Friction item 2 (undisclosed sibling collision) is a first occurrence — no prior cycle's lessons learnt record cites a co-bumped-file version collision.
