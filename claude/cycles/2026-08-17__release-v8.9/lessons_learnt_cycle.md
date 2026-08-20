Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-20
Cycle: 2026-08-17__release-v8.9

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-08-17__release-v8.9
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-08-20
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| A Sprint-2/gated story (ST-06, unblocked 2026-08-18 when its Sprint 1 gate story ST-23 reached `done`/CONDITIONAL) sat completely unbuilt for ~2 days with no check catching it. `execution_state.json` had no entry for it at all — it looked like a complete, closed sprint (22/22 recorded stories done, all 6 EPICs merged) when in fact 22 of 23 in-scope items were done. STEP 5.1's Acceptance Summary only iterates stories *already recorded* in `execution_state.json`; nothing cross-references the full item count declared in `sprint_backlog.md` (which itself states "22 backlog-slice items + ST-23 gate story, split Sprint 1 (22 items) / Sprint 2 (ST-06, gated)" in its own Product Owner Sign-Off section) against the story count actually present in `execution_state.json`. The gap was only found by a human-directed cross-check during this session's own preflight reading, not by any structural gate. | Phase 3 | A | defer | Add an explicit item-count reconciliation check — at STEP 5.1 (Acceptance Summary) or STEP -1.4 (Backlog Slice Integrity) — that counts total ST items declared across the full `sprint_backlog.md` (including any gated/Sprint-2 sections, using the Product Owner Sign-Off's own "Scope confirmed" count as the authoritative total) and compares it against the count of story entries actually present in `execution_state.json`; halt or flag Sprint Close if they don't match. This would have caught the gap automatically at the very first `run sprint` re-invocation after ST-23 unblocked ST-06, rather than requiring manual cross-referencing. | Head of Specs Team | next `execution_prompt.md` revision |
| `execution_state.json`/`execution_prompt.md` have no documented schema convention for a multi-sprint EPIC whose Sprint 1 PR merges and closes *before* its gated Sprint 2 story is picked up. When ST-06 was implemented, its own EPIC-02 branch's original PR (#1453) had already merged — a fresh branch/PR was needed, and no existing field anticipated this. An ad hoc `epics.EPIC-02.sprint2` sub-object (`pr_number`/`pr_status`/`status`, with an explanatory `note`) was invented in-session to track it without overwriting the Sprint 1 subset's accurate historical PR record. Reasonable, but undocumented — a future engine session would have to re-derive the same pattern from scratch, or worse, might overwrite the Sprint 1 PR's own `pr_number`/`pr_status` fields with the Sprint 2 PR's values, destroying accurate history. | Phase 3 | A | defer | Formalise a documented convention in `execution_state_schema.json` and `execution_prompt.md` §3.2.B for tracking additional PRs against an EPIC whose original PR has already merged — either generalise this cycle's ad hoc `sprint2` sub-object into a named, schema-documented field (e.g. `additional_prs: [{label, pr_number, pr_status, status}]`) or state explicitly that a new EPIC-suffix (e.g. `EPIC-02b`) should be used instead. Either resolution is acceptable; leaving it undocumented is not. | Head of Specs Team | next `execution_prompt.md`/`execution_state_schema.json` revision touching multi-sprint EPIC tracking |

**Recurrence Notes:**
Neither friction item above is a recurrence of a prior-cycle item — first occurrence for both (no prior cycle's Sprint Execution scope has included a gated Sprint-2 story continuing after its EPIC's own PR had already merged).

Separately (not a new friction item, tracked for continuity): `2026-08-14__release-v8.8`'s Phase 3 record (`claude/cycles/2026-08-14__release-v8.8/lessons_learnt_cycle.md` `## Phase 3`) filed a deferred patch recommending either a `governance_sync.yml` merge-triggered sync, or an `execution_prompt.md` instruction to re-run the merge-gate sync check on every "PR merged" report mid-session (not only at session start) — the specific gap being that v8.8 saw 5 separate mid-session staleness instances within one continuous session as sibling PRs merged one after another. Checked `prompt_change_log.md`: no entry addressing either option exists yet — this deferred patch has now carried 1 cycle without application (not yet at the §6.4 2-cycle escalation threshold). This cycle's own staleness (EPIC-06 omitted from `merge_gate` at session start) was the ordinary **session-boundary** variant — already assessed in v8.8's own record as "by-design recovery behaviour, not a gap" — resolved correctly and completely by the existing session-start sync check in a single pass. It is not a recurrence of v8.8's specific *mid-session, between-sequential-merges* mechanism, since this session only needed one recovery pass (all 6 EPICs' staleness was caught and corrected together at invocation, not 5 times across one session). No escalation triggered; the deferred patch remains open and re-deferred with its original owner/target unchanged.

## Recurrence Escalations (Phase 3)

None. Both new friction items are first occurrences. The one carried-forward deferred patch from v8.8 (merge_gate mid-session sync) has not crossed the 2-cycle-without-application threshold and did not recur in its specific flagged form this cycle.

## Process improvements actioned this run (Phase 3)

None applied this run (no action-now patches — both friction items above are deferred, requiring Head of Specs Team design input on the exact check/schema shape before implementation).

## Outstanding deferred patches (Phase 3)

- `execution_prompt.md` should gain an item-count reconciliation check (sprint_backlog.md total vs. execution_state.json recorded stories) at STEP 5.1 or STEP -1.4 (friction item, this cycle) — Head of Specs Team, next `execution_prompt.md` revision.
- `execution_state_schema.json`/`execution_prompt.md` §3.2.B should document a convention for tracking a second PR against an already-merged EPIC (friction item, this cycle) — Head of Specs Team, next revision touching multi-sprint EPIC tracking.
- `execution_prompt.md`'s merge_gate/pr_status mid-session staleness — governance_sync.yml merge-trigger or an explicit re-sync-on-every-merge-report instruction (carried from v8.8 Phase 3, 1 cycle so far) — Head of Specs Team, next `execution_prompt.md` revision.

## Escalations (Phase 3)

None.

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | This cycle's two-agent (Director of Quality + Product Owner) PR review, performed at explicit user request on PR #1460, surfaced two genuine, non-trivial findings (an unbacked cross-trade pattern-language claim in the debrief prompt; an ambiguous "journal entries" data-source choice) that the engine's own prior agent-mediated sign-offs on the same PR had not raised. This is the same class of value already observed in prior cycles' user-directed dual-role PR reviews (e.g. v8.8's process notes) — a second, differently-scoped review pass catching what the first pass's own author-adjacent review did not. Worth continued use as a deliberate practice, not just an ad hoc one-off. | No process patch required — this is a confirming data point for an already-known pattern (LL-v8.6-P3-01's "second differently-scoped review pass" principle), not a new gap. | Sprint Execution |
