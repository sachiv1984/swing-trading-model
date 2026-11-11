Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-11
Cycle: 2026-11-06__release-v9.16

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-11-06__release-v9.16
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-11-11
**Reviewed by:** PMO Lead
**Invocation context:** invoking_routine `execution_prompt.md` (STEP 5.4); cycle_id `2026-11-06__release-v9.16`; phase Phase 3; prior_cycle_id `2026-11-03__release-v9.15`.
**Prior cycle checked:** 2026-11-03__release-v9.15 (`lessons_learnt_cycle.md` `## Phase 3`). It filed 2 friction items. I re-checked each against `prompt_change_log.md` as of this run, and also read the named target file directly (BLG-GOV-312, LL-v9.1-Closure-01):
1. **No step marks a same-PR fix complete in `backlog.md` (`LL-v9.15-P3-01`, target `execution_prompt.md` §3.2 and §7).** **Applied:** `execution_prompt.md` v3.92→v3.93 (2026-11-06). The same-branch fix banner text is in §7 write scope. **Resolved; not a recurrence.** This cycle shows a scope gap in it (friction item 6).
2. **No timing for the in-flight return note (`LL-v9.15-P3-02`, target `execution_prompt.md` STEP 5.2).** **Applied:** v3.93 (2026-11-06). The STEP 5.2 note now says to write it in the same commit as the status change. No story was returned this cycle, so it was not exercised. **Resolved; not a recurrence.**

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| **Missed selector collisions.** ST-01 made new sidebar text ("Today", "Watchlist") and area headers visible on every page. The STEP 3.1.A step 13 cross-spec selector check scanned only for renamed selectors. It missed bare `getByText` and role locators in other specs that now matched twice, and CI failed 6 times at ST-01 and 26 times at ST-03. **Blast radius:** any story that adds always-visible text can break unrelated Playwright specs. It was caught by CI on the story commit. Recovery cost was medium: two fix rounds across many specs before DoQ sign-off. | Phase 3 | B | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, section §3.1.A step 13. When a story makes new text or interactive elements visible on every page (shell, sidebar, header), also grep `tests/e2e/` for unscoped `getByText`/`getByRole` locators of that text, and scope them before pushing. | Head of Specs Team | Post-ship closure `2026-11-06__release-v9.16` |
| **State commit swept in staged deletions.** The ST-05 state commit `2d26da87` also committed two ST-06 file deletions that had been staged earlier with `git rm`. This broke the production build and Playwright at that commit, and ST-06's commit `739286e7` fixed it. **Blast radius:** any state-only commit can carry unrelated staged work onto the EPIC branch, giving a red commit and a misattributed change. It was caught by CI. Recovery cost was low, with no force-push. | Phase 3 | A | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, section §3.1.A step 4a (the state write after push). Commit `execution_state.json` updates with explicit pathspecs (`git commit -- <paths>`), or check that `git diff --cached --name-only` lists only the state files before a state-only commit. | Head of Specs Team | Post-ship closure `2026-11-06__release-v9.16` |
| **Duplicate scenario ID prefix caught only in CI.** ST-08's new spec reused the `SC-TPS` prefix. CI Pytest caught it through `check_e2e_scenario_id_uniqueness.py` (added at v9.15 ST-42), and it was renamed `SC-TPSZ` in `87d78b39`. **Blast radius:** a red CI run and one extra commit for each new spec that collides. Recovery cost was low. | Phase 3 | B | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, section §3.1.A step 2a (local checks before a frontend commit). When the commit adds or changes a file under `tests/e2e/`, run `python3 scripts/check_e2e_scenario_id_uniqueness.py` locally before committing. | Head of Specs Team | Post-ship closure `2026-11-06__release-v9.16` |
| **Gate dated from the wrong deploy.** Release Planning dated ST-13 and ST-14's conditional gates (§1.4b) from a 2026-11-02 deploy, but DS-36 actually reached production on 2026-10-28 (PR #2075). ST-14 cleared a day early, and ST-13 measured a later week than planned. **Blast radius:** a conditional story can be returned or held when its gate has already cleared, or measure the wrong window. It was caught during execution, by reading production data. Recovery cost was low: two baseline documents were corrected. | Phase 3 | C | defer | **Deferred patch:** File `claude/system/release_planning_prompt.md`, section §1.4b (Within-Sprint Date Gate Classification). When a gate date is derived from a deploy, cite the merged PR that shipped the dependency and its merge date, checked with `gh pr view`, not an adjacent release's merge. | Head of Specs Team | Next Release Planning (`v9.17`) |
| **P2 found defects reached close without an acceptance rationale.** `BLG-FE-281`, `BLG-FE-282` (EPIC-06) and `BLG-OPS-217` (EPIC-04) were listed only as follow-ups in the merge-gate PO acceptance. The DoQ acceptance did not name them, and neither recorded a rationale. The STEP 5.3 check (LL-v9.15-P4-02) caught it, and the user accepted all three at close (2026-11-11T15:13:05Z). **Blast radius:** without the STEP 5.3 check, Delivery Verification §7 would have stopped on three P2 items. It was caught at sprint close. Recovery cost was low: one question. | Phase 3 | A | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, section STEP 4 (`## Merge Gate Confirmations`). When asking for the human DoQ sign-off and PO acceptance, list every P1/P2 found defect filed during the EPIC and record the acceptance and rationale for each one there, so STEP 5.3 only checks it. | Head of Specs Team | Post-ship closure `2026-11-06__release-v9.16` |
| **Post-merge trackers met in-cycle have no banner path.** `BLG-OPS-215` and `BLG-OPS-218` were met on 2026-11-11 by human actions (secret deleted, console check), and `BLG-OPS-197` and `BLG-OPS-198` were met by ST-13 and ST-14. The §7 same-branch fix banner covers only an item fixed by a commit on the EPIC branch, so all four stay open in `backlog.md` at close. **Blast radius:** the next Release Planning or `groom backlog` could pick up items that are already met. Caught at sprint close. Recovery cost is low: four banners. | Phase 3 | C | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, §7 (the same-branch fix banner entry) and STEP 5.3. Extend the banner to a post-merge tracker filed for this cycle whose ACs are all recorded as met in `qa_evidence_EPIC-xx.md` before the seal, citing that record. | Head of Specs Team | Post-ship closure `2026-11-06__release-v9.16` |

**What worked well:**
- All 30 stories merged in about two days (2026-11-09T11:27Z to 2026-11-11T12:59Z), with none returned. Both conditional stories (ST-13, ST-14) cleared in-sprint on production data.
- The P1 key exposure is fully closed in one cycle. The key was rotated, the secret removed from the public build and deleted, and the console confirmed one active key. All of it was delegated and recorded in session, with no live-system access by the engine.
- Each later EPIC branch was cut from `main` after the previous merge, so no cross-EPIC conflict resolution was needed. The orphaned-commit check was empty at every merge.
- `check_execution_state_consistency.py` passed after every state write, and the human merge-gate confirmations were recorded in the same format for all seven EPICs.
- Both escalations were ruled in session, within minutes of being raised. Neither breached its SLA.

**Recurrence Notes:**
- Neither of the two v9.15 Phase 3 items recurred. Both are dispositioned **Applied** above, so every prior-cycle row has a disposition (AUD-2026-10-08-004).
- Scope-gap check (AUD-2026-11-03-004):
  - Friction item 6 is **Recurrence (scope gap of `LL-v9.15-P3-01`)**: same file, same §7 banner entry. It is the first scope gap against that mechanism, so no escalation.
  - Friction item 5 is **Recurrence (scope gap of `LL-v9.15-P4-02`)**: the same P1/P2 acceptance mechanism, now at STEP 4 instead of STEP 5.3. It is the first scope gap against that mechanism, so no escalation.
  - Items 1 to 4 are new. No patch in the last 3 cycles targeted §3.1.A step 13, step 4a, step 2a's scenario-ID check, or `release_planning_prompt.md` §1.4b's deploy-date source.

## Recurrence Escalations

None.

## Escalations

None.

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Five P2 found defects are open, each accepted by the PO and DoQ: `BLG-FE-282` (recommended first), `BLG-FE-281`, `BLG-OPS-217`, `BLG-BE-211` and `BLG-FE-278` | Seat them in the v9.17 slice ahead of P3 work, or record a dated PO reason for leaving one out | Release Planning |
| 2 | Met but not bannered: `BLG-OPS-215`, `BLG-OPS-218` (post-merge, met 2026-11-11), `BLG-OPS-197`, `BLG-OPS-198` (met by ST-13, ST-14), plus the source items of the 30 shipped stories | Banner them at post-ship closure STEP 3.1, and leave them out of v9.17 candidate selection | Post-Ship Closure |
| 3 | `BLG-GOV-414` (ST-28 AC 2) is due at the first `groom backlog` after ST-28 merged | Run it at the next `groom backlog`. Do not re-grade ST-28 | Backlog Management |
| 4 | DS-36 reached production on 2026-10-28 (PR #2075), not 2026-11-02 | Use the corrected date in any later DS-36-gated planning (friction item 4) | Release Planning |
