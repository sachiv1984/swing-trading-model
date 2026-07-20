Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-20__release-v7.6

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-20__release-v7.6
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-20
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| API performance baseline advisory (AUD-2026-06-22-006) missed for a new endpoint (`GET /ai/monthly-cost`, EPIC-07/ST-07) — `openapi.yaml` updated but the companion `docs/ops/api_performance_baseline.md` row was forgotten across an 8-file endpoint addition, caught only by the ST-12 CI gate after PR #1035 was already open | Phase 3 | D | action-now | New "API performance baseline pre-PR check (LL-v7.6-P3-01)" added to `execution_prompt.md` STEP 3.2.B (v3.57→v3.58) — mechanical grep check before `gh pr create`, not just a passive advisory. Logged: `prompt_change_log.md`, `changelogs/execution_prompt_changelog.md`, `OPERATIONAL_GUIDE.md` §14 (v4.103→v4.104). | PMO Lead | — |
| None of this sprint's 8 PRs received a formal GitHub approving review before merge (`reviewDecision: REVIEW_REQUIRED` on all) — the governance model's "Product Owner acceptance (comment on PR or in sprint_backlog.md)" condition was satisfied by an in-session chat authorization + PR comment, but GitHub's branch protection requires an actual Review object, forcing every merge through `gh pr merge --admin` to bypass it | Phase 3 | C | defer | Reconcile the documented merge-gate condition ("comment on PR or in sprint_backlog.md" satisfies Product Owner acceptance) against the repo's actual branch protection rule (requires an approving review) — either relax branch protection to accept a PO-authored comment, or update the governance model to require a real GitHub review and stop accepting comment-only acceptance. Whichever direction is chosen, `--admin` bypass should not be the routine path. | Infrastructure & Operations Owner | Next scheduled roadmap rebalance |
| ESC-EXEC-20260720-01 (EPIC-07/ST-07): the story's own AC and PO-approved UX spec assumed Gemini and Claude were two separate cost-generating providers — a premise never verified against the actual codebase (`gemini_service.py` calls only the Anthropic API; no Gemini integration exists anywhere) until sprint execution traced the implementation. Design Gate and sprint planning both passed this story through without catching it. | Phase 3 | B | decision | Escalated and resolved in-session by Product Owner (option (a), single-provider reframe) — not a prompt patch, a one-off content correction. No recurring pattern identified yet (first instance of this specific class of premise error); noting for awareness rather than filing a process patch on a single occurrence. | Product Owner | 2026-07-20 (resolved) |

**Recurrence Notes:**
The API performance baseline omission (row 1) is the same *shape* of friction as prior "documented-advisory-insufficient-under-load" patterns already fixed elsewhere in this prompt (e.g. LL-v3.7-EX-01/EX-02's atomic-write requirements, LL-v5.5-EX-02's persist-before-halt rule) — a passive note in prose is not reliably followed under multi-file task load; the fix pattern (convert to an active pre-step checklist item, ideally with a mechanical grep/check) is consistent with those prior fixes and was applied the same way here. If a third occurrence of "documented advisory missed under load" surfaces in a future cycle across a *different* rule, that would indicate a structural problem with advisory-only guidance in this prompt generally, not just this one rule.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-07-20__release-v7.6
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-20
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-07-17__release-v7.5 (`lessons_learnt_cycle.md` `## Phase 4`) — 2 deferred patches recorded (STEP 2.1 "Staging-deferred" Result value; agent-mediated `Signed off by:` naming pattern). Both confirmed resolved: `delivery_verification_prompt.md` STEP 2.1 (v3.5, read this run) now explicitly accepts `Staging-deferred (per CLAUDE.md §2 / shared_standards.md §16.11)` as a Result value, and this cycle's `qa_evidence_EPIC-01.md`/`EPIC-07.md` both use the `execution_prompt.md §5.3` agent-mediated naming pattern directly in the `Signed off by:` field. No recurrence — both prior friction items are closed.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `.claude_current_state.json`'s `amended_backlog_slice_path` field still points to `claude/cycles/2026-07-17__release-v7.4/amendments/AMD-20260717-01/amended_backlog_slice.md` — a stale pointer from the v7.4 amendment cycle that was never cleared after that amendment closed out. STEP -1.1's "if present and non-empty, treat as authoritative" instruction required manual reasoning (checking for an `amendments/` folder under this cycle's directory, cross-referencing `execution_state.json.backlog_slice_source`) to correctly dismiss it as inapplicable to `2026-07-20__release-v7.6`, rather than the state file itself reflecting that the pointer was resolved and closed. | Phase 4 | A | defer | No routine currently clears `amended_backlog_slice_path` (and companion fields `amendment_sealed_utc`, `active_amendment`, `amendment_status`) once the amendment's own cycle fully closes at Post-Ship Closure. Add a step to `claude/system/post_ship_closure.md` (or `claude/system/amendment_cycle_prompt.md` STEP 8) to reset these fields to empty/null once the amendment's originating cycle reaches `Closed_with_actions` or `Closed`, so a later cycle's `run delivery verification` STEP -1.1 does not need to manually dismiss a stale cross-cycle pointer. | Head of Specs Team | next roadmap review |

**Recurrence Notes:**
None — this is a new friction item, not previously recorded. It is a different root cause from either of v7.5's two now-resolved Phase 4 items (those were signer/Result-value taxonomy gaps in this prompt; this one is a stale-field cleanup gap in a different routine, `post_ship_closure.md`/`amendment_cycle_prompt.md`).

---

## Recurrence Escalations (Phase 4)

None.

## Process improvements actioned this run (Phase 4)

None applied this run — the one Phase 4 friction item is `defer` classification (`post_ship_closure.md`/`amendment_cycle_prompt.md` are outside this routine's write scope per `delivery_verification_prompt.md` §5 Write Scope Restriction).

## Outstanding deferred patches (Phase 4)

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/post_ship_closure.md` (or `claude/system/amendment_cycle_prompt.md` STEP 8) | New step — amendment field reset | Clear `amended_backlog_slice_path`, `amendment_sealed_utc`, `active_amendment`, `amendment_status` in `.claude_current_state.json` once the amendment's originating cycle closes | Head of Specs Team | next roadmap review |
