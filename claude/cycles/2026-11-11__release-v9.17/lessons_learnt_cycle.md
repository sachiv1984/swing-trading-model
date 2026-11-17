Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-17
Cycle: 2026-11-11__release-v9.17

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-11-11__release-v9.17
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-11-17
**Reviewed by:** PMO Lead
**Invocation context:** invoking_routine `execution_prompt.md` (STEP 5.4); cycle_id `2026-11-11__release-v9.17`; phase Phase 3; prior_cycle_id `2026-11-06__release-v9.16`.
**Prior cycle checked:** 2026-11-06__release-v9.16 (`lessons_learnt_cycle.md` `## Phase 3`). It filed 6 friction items. I re-checked each one against `prompt_change_log.md` as of this run, and also read the named target file directly (BLG-GOV-312, LL-v9.1-Closure-01):
1. **Missed selector collisions (`LL-v9.16-P3-01`, `execution_prompt.md` §3.1.A step 13).** **Applied** in v3.93→v3.94 (2026-11-11). Step 13 now includes the new-always-visible-text clause. **This cycle shows a scope gap in it** (friction item 1).
2. **A state commit swept in staged deletions (`LL-v9.16-P3-02`, step 4a).** **Applied** in v3.94. Every state-only commit this cycle used explicit pathspecs, and it did not recur. **Resolved.**
3. **A duplicate scenario ID prefix (`LL-v9.16-P3-03`, step 2b).** **Applied** in v3.94. It did not recur. **Resolved.**
4. **A gate dated from the wrong deploy (`LL-v9.16-P3-04`, `release_planning_prompt.md` §1.4b).** **Applied** in `release_planning_prompt.md` v2.72→v2.73 (2026-11-11). This cycle had no conditional stories. **Resolved.**
5. **P2 found defects without an acceptance rationale (`LL-v9.16-P3-05`, STEP 4).** **Applied** in v3.94. Every EPIC's Merge Gate Confirmations section this cycle lists its P1/P2 found defects with the PO and DoQ acceptance, and STEP 5.3 only had to confirm them. **Resolved.**
6. **Met post-merge trackers had no banner path (`LL-v9.16-P3-06`, §7 and STEP 5.3).** **Applied** in v3.94. `BLG-BE-211` was bannered on 2026-11-16, after its post-merge backfill. **Resolved.**

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| **Locator collisions still reached CI.** ST-01's new caption ("Sorted by what needs attention first") and its row chevrons (`aria-expanded`) broke SC-COMP-03/07 (run 43256379461). The step 13 grep for new visible text was not run before `b2d93f6d`. Fixed in `6b475ae0`. At ST-03, SC-LBG-03 asserted banner body copy that the story had moved into a collapsed strip entry. Step 13 covers renamed selectors and new always-visible text, but not existing text that a story hides or moves. Fixed in `360bf177`. **Blast radius:** any story that adds, hides or moves visible text can break unrelated specs. Both were caught by CI on the story commit. Recovery cost was low: one extra commit each. **Recurrence:** Recurrence (scope gap of `LL-v9.16-P3-01`). | Phase 3 | A | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, §3.1.A step 13. (a) Extend the text grep to existing text the story hides, collapses or moves. (b) Make the step mechanical, the way step 2b runs a script: add a check, run from the `commit-check` skill, that lists the visible strings added or removed in the diff under `src/**` and greps `tests/e2e/` for unscoped `getByText`/`getByRole` matches. A prose-only step was missed once in its first cycle. | Head of Specs Team | Post-ship closure `2026-11-11__release-v9.17` |
| **Spec premises the code contradicted, found only at pre-commit review.** ST-09's spec said only the nightly job moves stops, but `GET /positions/analyze` does too. ST-10's "latest nightly run date" rule kept old moves under "Due today". ST-04's data source returns trade plans only for positions with 2 or fewer grace days left (`DEV-EPIC01-ST04-01`). Each needed an in-session owner ruling or a deviation. **Blast radius:** mid-story rulings and P3 deviations. All were caught before merge. Recovery cost was medium: three rulings, two deviations and 12 EPIC-01 backlog filings. **Recurrence:** No. No patch in the last 3 cycles targeted the design gate's STEP 2.2 premise checks. | Phase 3 | C | defer | **Deferred patch:** File `claude/system/design_gate_prompt.md`, STEP 2.2. Add the data-source, writer, competing-value and failure-state checks scoped in `BLG-GOV-422` (P2), with the three scope extensions the Product Owner directed on 2026-11-13 (the writer check from EPIC-04, the competing-value check from EPIC-07 and the failure-state check from EPIC-06). The Product Owner directed on 2026-11-12 that `BLG-GOV-422` be seated in v9.18. | Head of Specs Team | `v9.18` (Release Planning seats `BLG-GOV-422`) |
| **The visual baseline workflow cannot push to EPIC branches.** `update-visual-snapshots.yml` failed with a 403 on `exec/**` because `GITHUB_TOKEN` lacks write access. The EPIC-03 baselines were committed by hand from the run artifact. **Blast radius:** every story that changes page visuals needs a manual baseline commit, which risks committing the wrong artifact. It was caught during ST-08. Recovery cost was low: one manual commit. **Recurrence:** No. | Phase 3 | C | defer | **Deferred patch:** File `.github/workflows/update-visual-snapshots.yml`, job permissions and push step. Grant `contents: write`, or push with a scoped token, so that regenerated baselines land on the triggering `exec/**` branch. Tracked as `BLG-OPS-220` (P3). | Infrastructure & Operations Owner | `v9.18` Release Planning (seat `BLG-OPS-220` or record a reason) |
| **Process-note timestamps written as estimates.** Three EPIC-03 `process_notes` entries are stamped 2026-11-17T15:00Z, 18:00Z and 18:30Z, but PR #2262 merged at 14:38:11Z, after all three events. One EPIC-05 note had already been corrected on 2026-11-16 for the same reason. BLG-GOV-309 made `blocked_since_utc` a shell-clock read, but no rule covers `process_notes`. **Blast radius:** the audit trail shows events after the merge they came before, which misleads Delivery Verification or audit timing checks. It was caught at sprint close. Recovery cost was low: a note in `sprint_close.md`. **Recurrence:** No (a new field; BLG-GOV-309 covered `completed_utc` and `blocked_since_utc` only). | Phase 3 | A | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, §9.2 (State Update Rule). Every `process_notes` entry, and any other timestamp the engine writes, starts with a real clock read (`date -u +%Y-%m-%dT%H:%M:%SZ`) or a timestamp from git or `gh`. If no clock read is available, write the date only. Never write an estimated time of day. | Head of Specs Team | Post-ship closure `2026-11-11__release-v9.17` |
| **Story status not moved to `merged` at one EPIC's merge.** At EPIC-02's merge, ST-05, ST-06 and ST-07 were left `done` while every other merged EPIC's stories read `merged`. They were normalised at this close. STEP 4 step 2 sets only the EPIC's `pr_status` and `status`, and the consistency script accepts either value. **Blast radius:** an inconsistent sealed record. Low. It was caught at sprint close. **Recurrence:** No. | Phase 3 | A | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, STEP 4 step 2. At the merge write (and at the resume-sync), also set each of the EPIC's `done` stories to `merged`. Optionally add the check to `scripts/check_execution_state_consistency.py`. | Head of Specs Team | Post-ship closure `2026-11-11__release-v9.17` |

**What worked well:**
- All 20 stories merged in five days (2026-11-12T21:07Z to 2026-11-17T14:38Z), across 7 EPICs in the sealed Merge Order, with none returned. Each later branch was cut from `main` after the previous merge, so no cross-EPIC conflict resolution was needed, and every orphaned-commit check was empty.
- The v9.16 merge-gate patch worked as intended. Every P1/P2 found defect (`BLG-FE-294`, `BLG-FE-300`, `BLG-FE-303`) had its PO and DoQ acceptance and rationale in the Merge Gate Confirmations section before the merge. STEP 5.3 had nothing to chase.
- Two P2 found defects (`BLG-FE-300`, `BLG-FE-303`) were fixed on their EPIC branches before merge and bannered with the §7 same-branch fix banner. Neither is left for the next Release Planning.
- The one escalation (`ESC-EXEC-20261116-01`) was ruled in session about 3 minutes after it was raised. The one delegation (`DEL-20261113-01`) was unblocked in session.
- `check_execution_state_consistency.py` passed after every state write. EPIC-03's follow-ups were turned straight into sharper first-time-right checks (`ba378df3`).

**Recurrence Notes:**
- All six v9.16 Phase 3 items are dispositioned **Applied** above, so every prior-cycle row has a disposition (AUD-2026-10-08-004). None was carried.
- Scope-gap check (AUD-2026-11-03-004):
  - Friction item 1 is **Recurrence (scope gap of `LL-v9.16-P3-01`)**: same file, same step 13. It is the first scope gap against that mechanism, so no escalation. The deferred patch makes the step mechanical rather than adding more prose.
  - Items 2 to 5 are new. In the last 3 cycles, no patch targeted `design_gate_prompt.md` STEP 2.2's premise checks, `update-visual-snapshots.yml`, the `process_notes` timestamp source in §9.2, or story status at STEP 4 step 2.

## Recurrence Escalations

None.

## Escalations

None.

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The Product Owner directed seating `BLG-GOV-422` and `BLG-QA-262` (P2) next release, with `BLG-QA-260` (P3, stale Provisional-Target v9.17, needs a recorded PO override). It also directed extending `BLG-GOV-422`'s scope with the writer, competing-value and failure-state checks | Seat them in the v9.18 slice, recording the override for `BLG-QA-260` | Release Planning |
| 2 | `BLG-FE-294` (P2) is open, accepted by the PO and DoQ at the EPIC-06 merge gate | Seat it in v9.18 ahead of P3 work, or record a dated PO reason for leaving it out | Release Planning |
| 3 | Shipped source items are not bannered yet, including `BLG-FE-278`, `BLG-FE-281` and `BLG-FE-282` (fixed by ST-12 to ST-14) and the other stories' source items | Banner them at post-ship closure STEP 3.1, and leave them out of v9.18 candidate selection | Post-Ship Closure |
| 4 | Post-merge trackers still open: `BLG-OPS-217` (ST-15 AC 2–3, needs 7 days of post-fix production data) and `BLG-GOV-419` (ST-18 AC 2, needs the next Release Planning gate clearance) | Record each one when it is met, and banner it then. Do not re-grade ST-15 or ST-18 | Post-Ship Closure; Release Planning |
