Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-27
Cycle: 2026-11-18__release-v9.18

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-11-18__release-v9.18
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-11-27
**Reviewed by:** PMO Lead
**Invocation context:** invoking_routine `execution_prompt.md` (STEP 5.4); cycle_id `2026-11-18__release-v9.18`; phase Phase 3; prior_cycle_id `2026-11-11__release-v9.17`.
**Prior cycle checked:** 2026-11-11__release-v9.17 (`lessons_learnt_cycle.md` `## Phase 3`). It filed 5 friction items, all deferred. Each was re-checked by patch ID against `prompt_change_log.md` as of this run, and the named target file was read directly (BLG-GOV-312, LL-v9.1-Closure-01):
1. **Locator collisions still reached CI (`LL-v9.17-P3-01`, `execution_prompt.md` §3.1.A step 13).** **Applied**: the hidden/moved-text clause in v3.94→v3.95 (2026-11-17), and the mechanical check in this cycle's ST-21 (`scripts/check_e2e_locator_collisions.py`, `commit-check` Check 13, v3.96). It did not recur. **Resolved.**
2. **Spec premises found only at pre-commit review (`LL-v9.17-P3-02`, `design_gate_prompt.md` STEP 2.2).** **Applied** by this cycle's ST-18 (`design_gate_prompt.md` v1.11→v1.12, 2026-11-23, `BLG-GOV-422`). Its first live use is v9.19's design gate. **This cycle shows a scope gap in it** (friction item 6).
3. **Visual baseline workflow could not push to EPIC branches (`BLG-OPS-220`, `update-visual-snapshots.yml`).** **Applied** by this cycle's ST-34 (`b6f03ef4`). **Resolved.**
4. **Process-note timestamps written as estimates (`LL-v9.17-P3-04`, `execution_prompt.md` §9.2).** **Applied** in v3.94→v3.95 (2026-11-17). **It recurred at this close** (friction item 1).
5. **Story status not moved to `merged` at merge (`LL-v9.17-P3-05`, STEP 4 step 2).** **Applied** in v3.95. Every EPIC's stories were set `merged` at its merge or resume-sync this cycle. **Resolved.**

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| **An estimated timestamp was written despite the clock-read rule.** The sprint-close resume-sync wrote process note 31 as `2026-11-27T17:20:00Z`, about 13 minutes after the real time (commit `d30c49a3` at 17:07:06Z). §9.2 has required a clock read since v3.95. Corrected before the seal. **Blast radius:** the sealed audit trail would have shown a note dated after the commit that carries it. Caught at STEP 5.4 while re-reading the rule for the recurrence check. Recovery cost was low: one field corrected before the seal. **Recurrence:** Recurrence (scope gap of `LL-v9.17-P3-04`). The prose rule exists and was missed in its first cycle, as with `LL-v9.16-P3-01`. | Phase 3 | A | defer | **Deferred patch:** File `scripts/check_execution_state_consistency.py`, with a line in `execution_prompt.md` §9.2. Fail any `process_notes` entry, or any `*_utc` field, whose leading timestamp is later than the script's own clock read, and any time of day ending `:00:00Z` that is not backed by a git or `gh` time. `commit-check` already runs the script on every state commit. | Head of Specs Team | Post-ship closure `2026-11-18__release-v9.18` |
| **Sprint start left `main` without the state file.** STEP 0 created `execution_state.json` on the EPIC-01 branch only, while `main` carried `Executing`. `test_execution_state_path_file_exists` failed on the unrelated PR #2306 and needed a user-directed fix (`f4b642d3`). The EPIC-01 QA record says it hit two sprint starts in a row. **Blast radius:** every PR to `main` fails until the file reaches `main`. Caught by CI on PR #2306. Recovery cost was low: one copy commit and a merge. **Recurrence:** No (not in the v9.17 Phase 3 record; no patch in the last 3 cycles targeted STEP 0). | Phase 3 | A | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, STEP 0 (and its multi-EPIC ownership note). Commit `execution_state.json` to `main` in the same commit that sets `Executing` in `.claude_current_state.json`. Tracked as `BLG-GOV-430` (P2, v9.19). The pre-commit hook added in PR #2308 blocks the failing commit meanwhile. | Head of Specs Team | `v9.19` (`BLG-GOV-430`) |
| **Backlog IDs collided across open EPIC branches.** Four IDs filed on EPIC-04 were already taken on the open EPIC-05 branch and were renumbered before acceptance (`BLG-SPEC-243→244`, `BLG-QA-276→280`, `BLG-QA-277→281`, `BLG-FE-329→332`). Commit messages before `a82923c8` and a PR review comment carry the old numbers. **Blast radius:** wrong cross-references in commits and reviews, and a merge that would have produced duplicate IDs. Caught before EPIC-04's acceptance. Recovery cost was medium: four renumberings across two files. **Recurrence:** No (no patch in the last 3 cycles targeted ID assignment across branches). | Phase 3 | C | defer | **Deferred patch:** File `claude/system/execution_prompt.md` §7 (backlog new-item exception), and `.claude/skills/backlog-add/SKILL.md`. Before assigning a new `BLG-xx` ID, `git fetch` and take the highest ID used in `backlog.md` on `main` and on every open `exec/<cycle_id>/*` branch. `BLG-QA-279` (P3) adds the commit-time check. | Head of Specs Team | `v9.19` Release Planning (seat `BLG-QA-279` or record a reason) |
| **An issue auto-close was skipped.** `governance_sync` did not close #2279 because ST-14's own commit (`a5438839`) recorded the story `in_progress`. The engine closed it by hand after CI passed. **Blast radius:** issues left open after a story is done, which misleads `sync gh` and status reads. Caught the same day. Recovery cost was low. **Recurrence:** No. | Phase 3 | A | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, §3.1.A "state update after push". The state commit that sets a story `done` carries that story's `[EPIC-xx][ST-xx]` tag, so `governance_sync` sees `done` on a tagged commit. | Head of Specs Team | Post-ship closure `2026-11-18__release-v9.18` |
| **A scheduled workflow shipped untried.** v9.17 ST-16 shipped `market-data-volume-check.yml` without a run against its real target. Its first real runs timed out on the production report (60 s read), so ST-32 needed the report by hand (`DEL-20261124-01`) and filed `BLG-OPS-223` (P2). **Blast radius:** a monitoring check that is silently not doing its job until someone needs it. Caught by ST-32. Recovery cost was medium: a manual report and a P2 follow-up. **Recurrence:** No. | Phase 3 | C | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, §3.1.A (story done criteria). A story that adds or changes a scheduled or `workflow_dispatch` workflow is done only after one `workflow_dispatch` run against its real target succeeds, with the run ID in the story notes. If the target is unreachable from the engine, record the run as a staging-only AC with a tracker. | Head of Specs Team | Post-ship closure `2026-11-18__release-v9.18` |
| **The design gate's new checks do not list every caller of a changed shared function.** ST-33 changed `get_earnings()`, and three callers outside the story's pages were found only in review: the Dashboard card (`BLG-FE-333`), pre-entry and Research (`BLG-BE-233`) and UK parity (`BLG-FE-334`). **Blast radius:** follow-up items after merge, for pages the design never looked at. Caught in EPIC-06 review. Recovery cost was low: three P3 follow-ups. **Recurrence:** Recurrence (scope gap of `LL-v9.17-P3-02`, applied by ST-18 this cycle). It is the first scope gap against that mechanism, so no escalation. | Phase 3 | C | defer | **Deferred patch:** File `claude/system/design_gate_prompt.md`, STEP 2.2 pre-approval checks. For any shared function, endpoint or stored field the design changes, list every caller (grep `src/` and `backend/`), and either cover each one in the design or name a backlog item for it. | Head of Specs Team | Post-ship closure `2026-11-18__release-v9.18` |

**What worked well:**
- All 40 stories merged in eight days (2026-11-19T16:36Z to 2026-11-27T17:05Z), across 7 EPICs in the sealed Merge Order, with none returned. Only one cross-EPIC merge was needed (EPIC-05 after EPIC-04), and every orphaned-commit check was empty.
- Nine owner rulings were raised as `ESC-EXEC-*` escalations, and every one was resolved in session, most within minutes. All three delegations were unblocked in session, including two production data reads.
- The v9.16 and v9.17 merge-gate patches worked. Every P2 found defect had its PO and DoQ acceptance and rationale in the Merge Gate Confirmations section before the merge, so STEP 5.3 only had to confirm them.
- Two post-merge trackers (`BLG-OPS-217`, `BLG-GOV-378`) were met in-sprint and bannered at this close rather than left for post-ship closure.
- The first-time-right checks (EPIC-04) were used by the later EPICs as soon as they merged. EPIC-06 turned its own retrospective into sharper checks in `.claude/skills/first-time-right/SKILL.md` the same day.

**Recurrence Notes:**
- All five v9.17 Phase 3 items are dispositioned **Applied** above, so every prior-cycle row has a disposition (AUD-2026-10-08-004). None was carried.
- Scope-gap check (AUD-2026-11-03-004):
  - Friction item 1 is **Recurrence (scope gap of `LL-v9.17-P3-04`)**: same file and section (§9.2). It is the first scope gap against that mechanism, so no escalation. The deferred patch makes the rule mechanical in the consistency script rather than adding more prose.
  - Friction item 6 is **Recurrence (scope gap of `LL-v9.17-P3-02`)**: same file and step (`design_gate_prompt.md` STEP 2.2, patched by ST-18). It is the first scope gap against it, so no escalation.
  - Items 2 to 5 are new. In the last 3 cycles, no patch targeted STEP 0's state-file commit, backlog ID assignment across branches, the tag on the `done` state commit, or workflow run checks.

## Recurrence Escalations

None.

## Escalations

None.

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Twelve P2 follow-ups are open, each accepted by the PO and DoQ with a rationale: `BLG-SEC-48` (v9.20), `BLG-SEC-49`, `BLG-GOV-430`, `BLG-GOV-431`, `BLG-FE-328`, `BLG-BE-226`, `BLG-AI-35`, `BLG-BE-228`, `BLG-QA-281`, `BLG-FE-339` (all v9.19), and `BLG-BE-231`, `BLG-OPS-223` (TBD) | Seat the v9.19 ones in the v9.19 slice ahead of P3 work, or record a dated PO reason for leaving each out. `BLG-SEC-49` is under 1 h and cuts discoverability until `BLG-SEC-48` ships | Release Planning |
| 2 | Post-merge trackers still open: `BLG-GOV-421` (ST-23 AC 3, met only if the next post-ship closure raises no prompt size baseline in a later PR) and `BLG-QA-276` (ST-30 AC 1 staging P&L match) | Record each when met and banner it then. Do not re-grade ST-23 or ST-30 | Post-Ship Closure; Delivery Verification |
| 3 | Shipped source items are not bannered yet, including `BLG-GOV-422`, `BLG-QA-262`, `BLG-QA-260` (ST-18 to ST-20) and `BLG-BE-208`, `BLG-BE-213`, `BLG-BE-223` (EPIC-05) | Banner them at post-ship closure STEP 3.1, and leave them out of v9.19 candidate selection | Post-Ship Closure |
| 4 | Production deploy of EPIC-03: `loop_events` is created by the first `POST /digest/events`; the planned production migration (Human-Delegation, Infrastructure & Operations Owner) is needed only if the production role cannot create tables | Confirm the table exists on production after deploy; until then Reviews reads "Not available" | Delivery Verification |
