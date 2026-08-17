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

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-08-14__release-v8.8
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-08-17
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-08-12__release-v8.7 (`lessons_learnt_cycle.md` `## Phase 4`) — 2 friction items, both deferred, neither carrying a formal `LL-vX-P4-nn` patch-ID tag at filing. Searched `prompt_change_log.md` / `shared_standards.md` / `execution_prompt.md` for both topics ("CI-green restatement" per-fix clarification; canonical "Sandbox Access Constraint" disclosure block) — neither has been applied yet. This is the first cycle transition since filing (v8.7 → v8.8), so the §6.4 2-cycle-without-application escalation threshold is not yet crossed; both remain open, re-deferred below with their original owner/target unchanged. No recurrence escalation triggered.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `execution_state.json`'s `test_scenarios` field is represented two different ways across this cycle's two governance-only EPICs: EPIC-06 uses an empty array `[]` (matching STEP 5.2's documented short-circuit for `test_scenarios = []`), while EPIC-07 uses a populated array containing one descriptive prose string ("Manual acceptance review — governance prompt text + `.claude_current_state.json` schema/ownership-registry changes only; no application test suite affected") rather than either an empty array or a real file path. Both EPICs are equivalently autonomous/governance-only with no application test suite affected — the underlying situation is identical, but the field's shape diverges, and nothing in `execution_prompt.md`/`delivery_verification_prompt.md` states which convention is correct. | Phase 4 | B | defer | Clarify in `execution_prompt.md` (wherever `test_scenarios` is populated at Sprint Execution STEP 3/5) that "no automated test scenarios" must always be represented as an empty array `[]`; any manual-review rationale belongs in the `qa_evidence_EPIC-xx.md` "Test scenarios used" prose field instead, never smuggled into `execution_state.json`'s `test_scenarios` array as a string. This keeps the field machine-parseable (a future automation of STEP 5.1's coverage check could otherwise treat EPIC-07's entry as a literal file path and report a false "file not found"). | Head of Specs Team | next `execution_prompt.md` revision touching `test_scenarios` field population |

**Recurrence Notes:** No. This is a first occurrence — no prior cycle's Phase 4 record cites a `test_scenarios` field-shape inconsistency. (Not a recurrence of v8.7's two carried-forward items, which are unrelated topics and remain separately tracked — see "Prior cycle checked" above.)

## Recurrence Escalations (Phase 4)

None. The one friction item identified this cycle is newly observed, not a recurrence. Both of v8.7's deferred items remain open but have not yet crossed the 2-cycle-without-application threshold (§6.4) — re-deferred below rather than escalated.

## Process improvements actioned this run (Phase 4)

None applied this run (no action-now patches — see friction item above, deferred).

## Outstanding deferred patches (Phase 4)

- `execution_prompt.md`'s `test_scenarios` field population guidance should require an empty array `[]` for "no scenarios," never a descriptive string (friction item, this cycle) — Head of Specs Team, next `execution_prompt.md` revision touching `test_scenarios`.
- `qa_evidence_template.md`/`execution_prompt.md §5.3`'s CI-green restatement requirement should be clarified as per-fix, not per-EPIC (carried from v8.7 Phase 4, 1 cycle so far) — Head of Specs Team, next revision touching either file.
- Canonical "Sandbox Access Constraint" disclosure block for `shared_standards.md`, to reduce re-derived disclosure prose across qa_evidence entries hitting the same recurring no-live-access constraint (carried from v8.7 Phase 4, 1 cycle so far) — Head of Specs Team, next `shared_standards.md` revision.

## Escalations (Phase 4)

None.

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | This cycle shipped 29/29 stories `done` with zero deviations filed and zero QA `Fail` results — the cleanest delivery-verification pass on record for this project (no hard blocks, no traceability gaps, no test coverage gaps). | No action required; recorded for pattern visibility only — a run this clean is worth noting precisely because it is the exception, not the rule. | All |
