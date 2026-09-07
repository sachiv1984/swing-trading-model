Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-07
Cycle: 2026-09-03__release-v9.1

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-09-03__release-v9.1
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-09-07
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-08-21__release-v9.0 (`lessons_learnt_cycle.md` `## Phase 3`) — 1 deferred patch carried in: STEP 3.1.A step 10a same-step self-verification read-back after the `deviations_filed` write (LL-v9.0-P3-01). Checked `prompt_change_log.md` by the patch's own ID tag (LL-v8.6-P4-01b method): applied and logged 2026-09-03, `execution_prompt.md` v3.70→v3.71, before this cycle's own execution began (the v3.71 header and this cycle's own STEP 3.1.A step 10a usage both confirm it). No recurrence.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| A human-initiated PR merge landed mid-session, 2 of 5 times (EPIC-02 PR #1536, EPIC-05 PR #1539), while the engine still had one more governance-only follow-up commit queued for that EPIC's branch — the commit landed on the now-inert branch after its own PR had already merged, stranding it. Caught both times only at the next explicit check (EPIC-02: same session, checking PR state before the next step; EPIC-05: the following session's STEP -1/STEP 4 resume-sync) via the LL-v6.8-P3-01 orphaned-post-merge-commit safety net, and reconciled cleanly by cherry-picking onto `main` both times (`2f425eb2`, `7fd58e56`) with no content lost. | Phase 3 | C | defer | Add an explicit "is this EPIC's PR already merged?" check (`gh pr view <pr_number> --json state`) immediately before any commit to an EPIC branch once that EPIC has reached STEP 3.2.B (PR opened) — not only at STEP 4's own merge flow. LL-v6.8-P3-02 already fixed the case where the *engine's own* STEP 4 merge causes the stray commit; this pattern is distinct — a *human* merge racing a live follow-up commit the engine doesn't yet know has been overtaken. Needs Head of Specs Team design input on exact placement (a new STEP 3.2.C, or a precondition folded into STEP 3.1.A step 3) before wording is finalised. | Head of Specs Team | next `execution_prompt.md` revision touching §3.2 |
| `git commit --amend` was mistakenly used on an already-pushed commit instead of creating a new commit, twice this cycle in immediate succession (EPIC-01's `8be831f5`, EPIC-02's `15db3691` — same class of mistake, same recovery). Both times git's own non-fast-forward push rejection caught it before any public history was rewritten; both were fixed via `git reset --soft <original-sha>` + a fresh commit rather than a force-push, so no content was lost or rewritten on the remote in either case. | Phase 3 | D | defer | Add an explicit guardrail line to `execution_prompt.md` §3.1.A step 3/4 ("Commit to the EPIC branch" / push): once a commit has been pushed to the remote branch, a follow-up fix must be a new commit — never `git commit --amend` a commit already on `origin`. Cheap to state, but needs Head of Specs Team confirmation before landing in a Class 6 document (this routine's own write scope excludes `claude/system/` without explicit instruction). | Head of Specs Team | next `execution_prompt.md` revision touching STEP 3.1.A |

**Recurrence Notes:**
Neither friction item appeared in `2026-08-21__release-v9.0`'s own Phase 3 record, so per the formal §3.7 check both are "No" (not a cross-cycle recurrence). Both are, however, *same-cycle* recurrences — each pattern fired twice independently within this one cycle (orphaned commit: EPIC-02 and EPIC-05; amend-on-pushed-commit: EPIC-01 and EPIC-02) — which is why both are recorded as findings rather than one-off notes, even though neither crosses the formal cross-cycle bar for an automatic Recurrence Escalation.

## Recurrence Escalations

None. Both friction items above are first occurrences against the immediately-prior cycle per the formal §3.7 check (see Recurrence Notes for their same-cycle, non-formal repeat pattern).

## Process improvements actioned this run

None applied this run — both friction items above are deferred pending Head of Specs Team design/confirmation, consistent with how STEP 3.1.A-touching patches have been handled in prior cycles (e.g. LL-v9.0-P3-01 itself was deferred at v9.0 Phase 3 and only applied at the subsequent post-ship closure, not in-session).

## New files created this run

None.

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | §3.2 (EPIC Completion / PR flow) | Add a "is this EPIC's PR already merged?" (`gh pr view <pr_number> --json state`) check before any commit to an EPIC branch once its PR is open, not only at STEP 4 — closes the human-merge-races-a-live-commit gap distinct from LL-v6.8-P3-02's engine-merge-flow fix | Head of Specs Team | next `execution_prompt.md` revision touching §3.2 |
| `claude/system/execution_prompt.md` | STEP 3.1.A step 3/4 (Commit / Push) | Add an explicit guardrail: never `git commit --amend` a commit already pushed to `origin` — a post-push fix must be a new commit | Head of Specs Team | next `execution_prompt.md` revision touching STEP 3.1.A |

## Escalations

None.

## What worked well

- The four `delegated_decision` items this cycle (ST-21, ST-26/EPIC-04; ST-34, ST-35/EPIC-05) were each resolved same-session via explicit user/Product Owner authorisation to act as the correctly-identified named role, with a genuine role-appropriate review performed and disclosed in each case (e.g. ST-21's CONDITIONAL-vs-clean-PASS distinction, ST-26's currency check before reusing pre-designed seed content) rather than a mechanical rubber-stamp.
- Proactive cross-branch version-collision avoidance (`CLAUDE.md` §8 step 2a) was applied twice this cycle before any conflict occurred — `strategy_rules.md` v1.8 chosen deliberately to avoid EPIC-04's in-flight v1.7 bump, and `OPERATIONAL_GUIDE.md`/`roadmap_prompt.md` v4.174 chosen to avoid EPIC-04's in-flight 4.172/4.173 — both documented in the affected file's own header and commit message at write time, not discovered after the fact at merge.
- `DEV-EPIC02-ST08-01`'s first-pass "likely sandbox-specific" assessment was not accepted at face value — a real CI run was forced (`workflow_dispatch` added to `playwright.yml`) to independently verify the claim, directly applying the LL-v8.6-P3-01 standard ("already verified" claims need evidence, not just reasoning) rather than repeating the exact failure pattern that standard exists to prevent.
- Both `git commit --amend`-on-pushed-commit mistakes were caught by git's own non-fast-forward push protection before any public history was rewritten — the safety mechanism worked as intended in both cases, with zero force-pushes and zero content loss.

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Human-initiated PR merges landed mid-session twice this cycle while the engine still had a queued follow-up commit for that EPIC's branch, producing an orphaned commit both times (safely reconciled via the existing LL-v6.8-P3-01 safety net, but only after the fact). | Sprint Execution should check `gh pr view <pr_number> --json state` before any commit to an EPIC branch once its PR is open, not rely solely on the STEP 4/resume-sync safety net to catch it after the fact. | Sprint Execution |
| 2 | `git commit --amend` was used on an already-pushed commit twice this cycle (caught safely both times by push rejection, never a force-push). | Add an explicit "never amend a pushed commit" guardrail to `execution_prompt.md`'s commit step so the mistake is prevented rather than merely recovered from cleanly. | Sprint Execution |

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-09-03__release-v9.1
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-09-07
**Reviewed by:** Director of Quality
**Prior cycle checked:** 2026-08-21__release-v9.0 (`lessons_learnt_cycle.md` `## Phase 4`) — 2 friction items carried in (QA evidence staleness on `qa_evidence_EPIC-01.md`'s ST-02 row, deferred to Director of Quality's next touch of that file; `execution_state.json` `test_scenarios` metadata-completeness gap, deferred to Head of Specs Team's next `execution_prompt.md` STEP 3 revision) — neither recurs this cycle: no QA evidence row was found stale against `execution_state.json`, and every EPIC's `test_scenarios` array this cycle was populated and matched real, executed test files at verification time. `prompt_change_log.md` checked for both patch-ID tags — neither shows an entry yet, so both remain open carries (not yet 2+ cycles carried without a log entry — v9.0 was their first filing).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| §7's Resolved-deviation carve-out (LL-v8.6-P4-03) instructs confirming "the canonical spec's own Known Deviations entry states RESOLVED ... with a resolution narrative" before applying the carve-out. `DEV-EPIC02-ST08-01` (P2) is a genuine Resolved-in-session deviation, but its two spec references are a policy doc (`quarterly_dependency_upgrade_cadence_policy.md`) and a test file (`signals-cash-balance.spec.js`) — neither carries a "Known Deviations" section of the kind product-facing page/component specs use. The carve-out's own wording assumes every deviation has a canonical-spec Known-Deviations home; a test-synchronization-class deviation (no product spec was actually violated — the AC gap was in the test file, not the app) does not. Applied the carve-out anyway on "or equivalent" resolution evidence (4 independent corroborating documents: `qa_evidence_EPIC-02.md`'s own Resolution narrative, `docs/System_status_report.md`, `docs/governance/quality_trend_index.md`, and an inline test-file comment) — a defensible reading, but one this engine had to construct rather than one the prompt stated directly. | Phase 4 | B | defer | Clarify §7's carve-out wording in `delivery_verification_prompt.md` to explicitly cover deviations whose spec_reference is a test file or ops/process document with no natural Known-Deviations section — name the qa_evidence file's own Resolution narrative (cross-referenced in `System_status_report.md`) as sufficient "equivalent" evidence for that deviation shape, rather than requiring interpretation each time. Cannot be applied in this run — `claude/system/delivery_verification_prompt.md` is outside this engine's write scope (§5). | Head of Specs Team | next `delivery_verification_prompt.md` revision touching §7 |

**Recurrence Notes:**
No recurrence against `2026-08-21__release-v9.0`'s own Phase 4 record — this is a first occurrence of the carve-out-wording-gap pattern.

## Recurrence Escalations (Phase 4)

None. The friction item above is a first occurrence.

## Process improvements actioned this run (Phase 4)

None applied this run — the friction item above is deferred pending Head of Specs Team action on a file outside this engine's write scope.

## Outstanding deferred patches (Phase 4)

- `qa_evidence_EPIC-01.md`'s ST-02 row correction (carried from v9.0, Director of Quality, next touch of that file) — not yet due for escalation (first carry).
- `execution_prompt.md` STEP 3 `test_scenarios` completeness check (carried from v9.0, Head of Specs Team, next `execution_prompt.md` revision) — not yet due for escalation (first carry).
- `delivery_verification_prompt.md` §7 carve-out wording clarification for test-file/ops-policy-class deviations (this cycle, Head of Specs Team, next `delivery_verification_prompt.md` revision touching §7).

## Escalations (Phase 4)

None.
