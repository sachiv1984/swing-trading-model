Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-06
Cycle: 2026-07-04__release-v6.6

# Lessons Learnt (Cycle) — 2026-07-04__release-v6.6

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-04__release-v6.6
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-06
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-07-02__release-v6.5 (`lessons_learnt_cycle.md` `## Phase 3`)

### What went well

- All 4 stories delivered across both EPICs — zero items returned to backlog. One delegation (`DEL-20260706-01`, EPIC-01/ST-01 to Head of UX & Design) reached `Unblocked` cleanly with a full two-phase write (sign-off, then commit SHA).
- The v3.51 STEP 4 resume-sync branch check (applied last cycle, v6.5 Phase 3 friction item 1) worked exactly as designed on this session's resume: EPIC-01's PR #918 was found already `MERGED` on GitHub while `execution_state.json` on `main` still showed `status: done` / `pr_status: open`. The session was resumed on the `exec/2026-07-04__release-v6.6/EPIC-01` branch (not `main`); the gate's `git branch --show-current` check caught this, `git checkout main && git pull` ran before the sync write, and the write landed cleanly on `main` with no orphaned-branch rework needed. This is direct confirmation the applied patch closed the recurring defect (v6.3/v6.4/v6.5 pattern).
- `deviations_filed`, `qa_signed_off`, and `acceptance_verified` were all correctly set per-story during execution — no batch correction required at sprint close (5th consecutive cycle with this discipline holding).
- A mixed-class EPIC (EPIC-01: one `delegated_frontend` human sign-off + one `autonomous` story) was sign-off correctly under the agent-mediated format rather than misapplying the BLG-GOV-19 autonomous-class shortcut — the "mixed-class EPIC" rule in `qa_evidence_EPIC-xx.md` guidance was followed without ambiguity.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| v6.4 Phase 3 friction item 2 (`/commit-check` should diff `git add`'s target list against the intended file set before multi-file governance commits) — deferred at v6.4 (target v6.5), still unapplied at v6.5 (target reset to v6.6, this cycle) — remains unapplied. `.claude/skills/commit-check/SKILL.md` was checked again this session; no diff-verification step exists. This is now a 2-cycle carry-forward (v6.4 → v6.5 → v6.6) with no `prompt_change_log.md` entry, meeting the §3.7 automatic-escalation threshold. | Phase 3 | C | decision | Not applied — `run sprint`'s declared write scope (execution_prompt.md §7) does not include `.claude/skills/`. Escalating per §3.7/§6.4: a routine or explicit authority with skill-file write scope must apply this, or the target must be formally reassigned to a routine that can (e.g. a `/commit-check` skill update session, or Head of Specs Team direct edit outside a governed routine). | Head of Specs Team | Immediate — see Recurrence Escalations |

**Recurrence Notes:**
- v6.5 Phase 3 friction item 1 (STEP 4 resume-sync branch check, action-now, applied v3.51): **Not a recurrence — confirmed resolved.** The exact class of defect (orphaned sync write on a stale exec branch) was avoided this session because the v3.51 gate fired and redirected to `main` before any write. See "What went well" above.
- v6.5 Phase 3 friction item 2 (`/commit-check` diff-verification, deferred, target v6.6): **Recurred — still unresolved at its own named target cycle.** Now a 2-cycle carry-forward with no `prompt_change_log.md` entry. Escalated per §3.7 (see Recurrence Escalations below) rather than re-recorded as a fresh deferred action.
- v6.5 Phase 3 friction item 3 (`ESC-EXEC-20260703-01` credential identity, resolved same-cycle, no prompt change filed): **Not a recurrence.** No credential-identity ambiguity encountered this cycle — no escalations were filed at all this sprint.

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| `/commit-check` skill should diff `git add`'s target list against the intended file set before multi-file governance commits — deferred v6.4 (target v6.5), still deferred v6.5 (target v6.6), still unapplied this cycle | 2026-06-24__release-v6.4 | Deferred, owner Head of Specs Team, target 2026-07-04__release-v6.6 (this cycle) | Head of Specs Team |

## Outstanding Deferred Patches

None valid to record here — the one remaining deferred item (commit-check diff-verification) has crossed the 2-cycle threshold and is recorded under Recurrence Escalations instead, per §6.4.

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `/commit-check` skill diff-verification patch has been deferred across 3 cycles (v6.4 → v6.5 → v6.6) with no `prompt_change_log.md` entry, and remains outside `run sprint`'s write scope (`.claude/skills/` is not a permitted path per execution_prompt.md §7) | Recurrence / Missing write-scope authority | Head of Specs Team | No governed routine currently in scope can apply this patch; needs either an explicit out-of-routine directed edit or a write-scope amendment to whichever routine is meant to own `.claude/skills/` maintenance. |

If none: N/A — one escalation recorded above.
