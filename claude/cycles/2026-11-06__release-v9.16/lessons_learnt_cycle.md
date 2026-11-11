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

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-11-06__release-v9.16
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-11-11
**Reviewed by:** PMO Lead
**Invocation context:** invoking_routine `delivery_verification_prompt.md` (STEP 8.5); cycle_id `2026-11-06__release-v9.16`; phase Phase 4; prior_cycle_id `2026-11-03__release-v9.15`.
**Prior cycle checked:** 2026-11-03__release-v9.15 (`lessons_learnt_cycle.md` `## Phase 4`). It filed 2 friction items. Each was re-checked against `prompt_change_log.md` and `closure_record.md` as of this run (BLG-GOV-312, LL-v9.1-Closure-01):
1. **`LL-v9.15-P4-01`: STEP 1 did not name `deferred_at_planning`.** **Applied:** `delivery_verification_prompt.md` v3.16→v3.17 (`prompt_change_log.md` 2026-11-06; `2026-11-03__release-v9.15` `closure_record.md` line 75). STEP 1 now names it. No slice item was deferred at planning this cycle, so it was not exercised. **Resolved; not a recurrence.**
2. **`LL-v9.15-P4-02`: a P1/P2 found defect reached verification without a PO + DoQ acceptance record.** **Applied:** `execution_prompt.md` v3.93 (`closure_record.md` line 76). It worked live: the sprint-close check caught `BLG-FE-281`, `BLG-FE-282` and `BLG-OPS-217`, and the user accepted all three at close (2026-11-11T15:13:05Z). As a result, this run found every open P2 with an acceptance and a rationale already recorded, and did not have to stop at §9. The scope gap (the check runs at close, not at merge) is already Phase 3 friction item 5. **Resolved; not a recurrence.**

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| **Post-merge AC met before verification has no named disposition.** ST-12 AC 3 was moved post-merge by the PO at the merge gate, not at seal, so it is graded `Pass_with_deviation` (STEP 2.1, LL-v9.13-P3-03). Its tracker `BLG-OPS-218` was met on 2026-11-11, before this run. STEP 2.1 and STEP 3 do not say how to register a `Pass_with_deviation` gap that is fully closed by verification time. The LL-v8.6-P4-03 Resolved-deviation carve-out covers `DEV-*` records with `Status: Resolved`, not QA-evidence-only gaps. This run recorded it as "Resolved post-merge" by analogy. **Blast radius:** one AC this cycle. Severity was P3, so the outcome did not change, but a P1/P2-severity gap in the same shape would leave it unclear whether §7 acceptance is still required. Recovery cost: one written interpretation. Propagation: any cycle where a merge-gate post-merge AC is met before verification. Classification: Type B — Semantic Mismatch: The same concept was named or interpreted differently across documents or roles | Phase 4 | B | defer | **Deferred patch:** File `claude/system/delivery_verification_prompt.md`, section STEP 2.1, `Pass_with_deviation` paragraph. After the "Seal-marked post-merge ACs" sentence, add: "A `Pass_with_deviation` gap whose tracking item is met, with a dated record in the QA evidence log, before this run is entered in the Deviation Register as `Resolved post-merge`. It keeps its grade. The LL-v8.6-P4-03 carve-out applies to it on the same terms: no §7 acceptance is required whatever its severity, provided the met record is dated before this run." | Head of Specs Team | 2026-11-06__release-v9.16 post-ship closure |

**What worked well:**
- Every preflight gate passed on the first invocation, for the fifth cycle running. All seven QA evidence logs were signed, dated and carried `## Merge Gate Confirmations`. The readiness statement was all `Yes`, and GitHub confirmed all seven PRs `MERGED` at their recorded times.
- `sprint_close.md`'s deviation tables mapped one-to-one onto the §4 register: three `DEV-*` records, four `Pass_with_deviation` grades, and the found-defect rows under `Pass` grades with tracking-item priorities. No severity call needed reworking.
- All three `DEV-*` records already had complete Known Deviations entries with the correct backlog references. Nothing was routed to Post-Ship Closure STEP 5 for a missing entry.
- All 34 `test_scenarios` references resolved on disk and were cited in the QA evidence. No TSG rows.
- No backlog entries had to be added this run. Every outstanding item already had one.

**Recurrence Notes:**
None against the prior cycle. Both v9.15 Phase 4 rows are dispositioned **Applied** above (AUD-2026-10-08-004 row-completeness). The friction item this cycle is new: no patch in the last 3 cycles targeted STEP 2.1's handling of a post-merge gap met before verification.

Severity calls were not contested. The DoQ sign-offs, `sprint_close.md` and this run agree on P3 for the three `DEV-*` records and on P2 for the five found defects. The user, acting as Director of Quality and Product Owner, gave the §9 sign-off in one step (2026-11-11). The pre-seal gate (LL-v2.4-DV-01) held: the §9 dates were filled only after that decision.

### Phase 4 Recurrence Escalations

None.
