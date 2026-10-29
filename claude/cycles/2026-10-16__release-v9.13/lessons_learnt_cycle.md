Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-29
Cycle: 2026-10-16__release-v9.13

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-10-16__release-v9.13
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-10-29
**Reviewed by:** PMO Lead
**Invocation context:** invoking_routine `execution_prompt.md` (STEP 5.4); cycle_id `2026-10-16__release-v9.13`; phase Phase 3; prior_cycle_id `2026-10-12__release-v9.12`.
**Prior cycle checked:** 2026-10-12__release-v9.12 (`lessons_learnt_cycle.md` `## Phase 3`). It filed 2 friction items. Each was re-checked by patch ID against `prompt_change_log.md` as of this run, and by reading the named target file directly (BLG-GOV-312, LL-v9.1-Closure-01):
1. **Every CI workflow's conclusion for a story's SHA, not only Playwright (`LL-v9.12-P3-01`, target `execution_prompt.md` §3.1.A).** **Applied:** `execution_prompt.md` v3.86→v3.87 (2026-10-15), §3.1.A step 4d. It requires `ci-tests.yml` to succeed for any `backend/**` or `requirements*.txt` commit before `done`. No story this cycle reached `done` on a red CI run. **Resolved; not a recurrence.**
2. **Merged-PR check before merge-gate record commits (`LL-v9.12-P3-02`, target `execution_prompt.md` §3.2.B and STEP 4).** **Applied:** `execution_prompt.md` v3.87, §3.2.B step 7 and the STEP 4 note. It fired live at the EPIC-06 merge (PR #2072): the merge-gate record was redirected to `main`, and every orphaned post-merge commit check this cycle was empty. **Resolved; not a recurrence.**

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `.githooks/pre-commit` runs `scripts/check_local_openapi_contract_completeness.py`, which reads contract files and `openapi.yaml` from the working tree, not the staged index. During EPIC-02, a route that was still undocumented in another story's uncommitted work blocked ST-13's unrelated commit. It was recovered with a fresh commit, and no amend was needed. Blast radius: when two stories are in progress at once, the hook can block a commit for a reason outside the commit, which invites `--no-verify` or bundling unrelated stories into one commit; caught at commit time; recovery cost low (single-commit rework). | Phase 3 | C | defer | **Deferred patch:** File `scripts/check_local_openapi_contract_completeness.py` (as invoked by `.githooks/pre-commit`), section: file reading. When run from the hook, read each contract file and `docs/reference/openapi.yaml` from the index (`git show :<path>`), so only staged content is checked. Keep the working-tree mode for manual runs. | API Contracts & Documentation Owner | Next Sprint Execution run (the cycle after `2026-10-16__release-v9.13`) |
| The 2026-04-28 `commit-check` row in `.claude/skills/lessons_learnt.md` says to open a PR after every `git push` on an exec branch. `execution_prompt.md` §3.2.B (BLG-GOV-18) forbids opening the PR before the DoQ sign-off `Date:` is set. The engine followed the governance prompt both times. The conflict was noted in v9.12's `sprint_close.md` process notes and again this cycle (2026-10-28, EPIC-04), but never filed as a friction item. Blast radius: a run that follows the skill log over the prompt opens a PR before sign-off, which is review noise that the merge gate later blocks; would surface at the next exec-branch push; recovery cost low (close or retitle the PR). | Phase 3 | B | defer | **Deferred patch:** File `.claude/skills/lessons_learnt.md`, section: the 2026-04-28 `commit-check` row. Replace "always create a PR immediately" with "open the PR at EPIC completion, once the DoQ sign-off `Date:` is set (`execution_prompt.md` §3.2.B, BLG-GOV-18)". This file is outside Sprint Execution's write scope (§7), so it is not applied here. | Head of Specs Team | Next Sprint Execution run (the cycle after `2026-10-16__release-v9.13`) |
| Four EPIC-05 stories (ST-29 to ST-32) had acceptance criteria that only a run on `main` or production data gathered after merge can meet: a staging deploy from `main`, 7 days of call volumes, a production top-3 report, and 10 nightly screener runs. All four were graded `Pass_with_deviation`, and three delegations were carried past sprint close (BLG-OPS-196/197/198). v9.12 had the same shape once (ST-06 AC 2, closed post-merge under `ESC-EXEC-20261013-02`). Sprint Planning has no step that marks such an AC at seal time. Blast radius: a story can never meet such an AC in-sprint, so every cycle with one ends with carried delegations and `Pass_with_deviation` rows that read like defects; surfaces at DoQ review and delivery verification; recovery cost low per story, medium summed across a cycle (extra review rounds, backlog items and verification reconciliation). | Phase 3 | C | defer | **Deferred patch:** File `claude/system/sprint_planning_prompt.md`, section: the acceptance-criteria sign-off gate (STEP 6.2). Require every AC that can be met only after merge (a run on `main`, or production data over a period) to be marked `post-merge` at seal, with its tracking backlog item named. Sprint Execution then grades the in-sprint part on its own and records the post-merge part as planned, not as a deviation. | Head of Specs Team | Next Sprint Planning run |
| Two `execution_state.json` fields were stale at sprint close and corrected by hand. ST-28's `deviations_filed` was still `false`, although its notes said "Deviation check: none". This is the STEP 3.1.A step 10a write and read-back, which was missed on the delegated-unblock path. Also, `ESC-EXEC-20261016-01` and `ESC-EXEC-20261027-04` were absent from this cycle's `open_escalations` map, although both were mirrored in `.claude_current_state.json`. `scripts/check_execution_state_consistency.py` checks neither. §9.2 leaves `deviations_filed` to a read by eye. Blast radius: an unflagged `deviations_filed: false` would fail the delivery-verification completion check, and a missing escalation leaves a gap in the cycle's own audit record; caught only by the STEP 5.1 backstop; recovery cost low (field fix at close). | Phase 3 | A | defer | **Deferred patch:** File `scripts/check_execution_state_consistency.py`, together with `claude/system/execution_prompt.md` §9.2 (Mechanical form). Add two checks: every `done`/`merged` story has `deviations_filed: true`, and every `## ESC-EXEC-*` heading in the cycle's `execution_escalations.md` has a key in `execution_state.json` `open_escalations`. Update §9.2's list of what the script covers to match, under the CLAUDE.md §6 checklist. | Head of Specs Team | Next Sprint Execution run (the cycle after `2026-10-16__release-v9.13`) |

**What worked well:**
- The LL-v9.12-P3-02 merged-PR check worked as intended. When PR #2072 was merged straight after its sign-off comments were posted, the merge-gate record went to `main`. Every orphaned post-merge commit check this cycle was empty, against three stranded commits in v9.12.
- `scripts/check_execution_state_consistency.py` was the §9.2 read-back on every resume and at close, and exited 0 each time.
- Running the EPICs one at a time (each branch cut from `main` after the previous merge) again meant no cross-EPIC merge resolution and no sibling-branch sync.
- All ten escalations were resolved within SLA and mirrored into `.claude_current_state.json` (LL-v9.11-P3-02). Most closed within an hour of being raised.
- Five of eight delegations were unblocked in-session by the user. These were two live migrations (DS-34, DS-35), a forced failed workflow run, a staging manual check and a post-merge staging deploy.

**Recurrence Notes:**
None against the prior cycle's Phase 3 friction items. Both v9.12 Phase 3 deferred patches are dispositioned **Applied** above, so no prior-cycle row is left without a disposition (AUD-2026-10-08-004 row-completeness). Two items this cycle repeat observations that v9.12 recorded but did not file as friction items, so there is no prior outstanding action and no automatic escalation (§3.7):
- Friction Item 2 (skill lesson vs §3.2.B) was in v9.12's `sprint_close.md` process notes.
- Friction Item 3 (post-merge ACs) has the same shape as v9.12's ST-06 AC 2.
Both are filed now so that a third occurrence counts as a recurrence. Friction Item 4's `deviations_filed` half is the same failure mode as `LL-v9.0-P3-01` (`2026-08-21__release-v9.0`). That patch was applied at the time, and its read-back is still by eye, which this item's patch makes mechanical.

## Recurrence Escalations

None.

## Escalations

None. All four friction items have a named file, section, owner and target.

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Four stories had ACs that only post-merge production data can meet, and all ended `Pass_with_deviation` with carried delegations | At sprint planning, mark such ACs `post-merge` with a named tracking item, so execution does not grade a planned remainder as a deviation (Friction Item 3) | Sprint Planning |
| 2 | `deviations_filed` and the cycle's escalation map are not checked by the §9.2 script, and both were stale at close | Until Friction Item 4's patch lands, read `deviations_filed` back after every unblock path, and add each `ESC-EXEC-*` to `execution_state.json` in the same write that files it | All |

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-10-16__release-v9.13
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-10-29
**Reviewed by:** PMO Lead
**Invocation context:** invoking_routine `delivery_verification_prompt.md` (STEP 8.5); cycle_id `2026-10-16__release-v9.13`; phase Phase 4; prior_cycle_id `2026-10-12__release-v9.12`.
**Prior cycle checked:** 2026-10-12__release-v9.12 (`lessons_learnt_cycle.md` `## Phase 4`). It filed 1 friction item. It was re-checked by patch ID against `prompt_change_log.md` as of this run, and by reading the named target file directly (BLG-GOV-312, LL-v9.1-Closure-01):
1. **`LL-v9.12-P4-01`, separate deviation and tracking-item priorities.** **Applied:** `execution_prompt.md` v3.86→v3.87 (2026-10-15, `prompt_change_log.md` line 36). The text is present in STEP 5.3's "Deviations filed this sprint" item ("Two priorities for `Pass_with_deviation` rows (LL-v9.12-P4-01)"). It worked live: this cycle's `sprint_close.md` shows both columns, and the ST-29/`BLG-OPS-196` P3/P2 straddle was visible without reading the backlog.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| STEP 2.1's found-defect severity rule (`LL-v9.11-P4-01`) is worded for `Pass_with_deviation` results only. ST-14 was graded `Pass with notes`, because its ACs were met as written, yet its note carried a found pre-existing P2 defect (`BLG-BE-190`, US sizing FX inversion), and ST-14's own new oracle mirrors it. Neither the prompt nor `sprint_close.md` (whose two-priority rule is also scoped to `Pass_with_deviation` rows) routed it to §7's P2 path. The engine had to stop and ask the user whether it was a P2 deviation. The user chose P2 with PO + DoQ acceptance. Blast radius: one story this cycle. Any found defect above P3 recorded under a `Pass with notes` grade can skip the §7 hard block unnoticed, through sprint close and into verification. Recovery cost: low (two prompt sections). | Phase 4 | Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced | defer | `delivery_verification_prompt.md` STEP 2.1 ("Found-defect severity"): apply the rule to any result whose `Comments` name a found pre-existing defect filed at P1/P2, including `Pass with notes`, not only `Pass_with_deviation`. Matching change to `execution_prompt.md` STEP 5.3 ("Deviations filed this sprint"): list such found defects in the deviation table with their filed priority. | Head of Specs Team | Post-ship closure `2026-10-16__release-v9.13` STEP 8 |

**What worked well:**
- All six QA evidence logs were signed and dated before invocation, and `sprint_close.md`'s readiness statement was all `Yes`. Every preflight gate passed on the first invocation, for the second cycle running.
- Sprint close's path-existence check (`LL-v9.10-P4-01`) meant all 46 `test_scenarios` paths and every `spec_references` path resolved, so no correction was needed.
- The cycle's own DoQ and PR reviews had already backlogged every test-coverage weakness this run found (`BLG-QA-229`, `-230`, `-232`, `-237`), so no new TSG item was needed.
- The ST-05 §8.4 known deviation was written into `strategy_rules.md` during execution, so the Known Deviations sync found it present.

**Recurrence Notes:**
None against the prior cycle. The friction item is new relative to v9.12 Phase 4, and the single v9.12 Phase 4 row is dispositioned **Applied** above, so no prior-cycle row is left without a disposition (AUD-2026-10-08-004 row-completeness). The friction item extends `LL-v9.11-P4-01` (applied v3.15) to a result grade it did not cover. It is a scope gap in that patch, not a recurrence of an open action.

Severity calls were not contested once made. The DoQ sign-off, `sprint_close.md` and this run agree on P3 for all six `Pass_with_deviation` results and on P3 for the ST-05 §8.4 deviation. The pre-seal gate (`LL-v2.4-DV-01`) held: §9 dates were filled only after the user chose agent-mediated DoQ and PO sign-off (2026-10-29). This is the 6th consecutive cycle (v9.8–v9.13) where verification sign-off was agent-mediated at the user's direction. Minor observation, not filed: `qa_evidence_EPIC-04.md` says "the five files above" while `test_scenarios` lists six. The sixth (`trade-debrief.spec.js`) is cited elsewhere in the same file and was run.

### Phase 4 Recurrence Escalations

None.

### Phase 4 Escalations

None. The friction item has a named file, section, owner and target.

### Phase 4 Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | A `Pass with notes` story carried a found P2 defect that neither STEP 2.1 nor sprint close routed to §7 | Until the patch lands, read every `Pass with notes` comment for a backlog item filed at P1/P2, and treat it under the found-defect severity rule | Delivery Verification; Sprint Execution |
