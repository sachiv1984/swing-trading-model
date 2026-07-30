Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-31

# Execution Escalations — 2026-07-30__release-v8.0 (EPIC-06 branch)

## ESC-EXEC-20260731-01

- **Raised at:** 2026-07-31T02:15:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-07-30__release-v8.0
- **Step:** STEP 3.1.D (delegated_decision item)
- **ST/EPIC item:** ST-19, EPIC-06
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-19 (BLG-GOV-263, RISK-04) requires a structural fix for the recurring cross-EPIC `execution_state.json` merge-conflict pattern. Per `sprint_backlog.md`'s own notes for this item: "No HoST design/technical-approach artefact exists yet for this item... a design/technical-approach session should be scheduled before execution begins. Head of Engineering sign-off required before the new mechanism is used live." This was already flagged as a known, non-blocking outstanding action at sprint planning seal (`sprint_backlog.md` "Outstanding Actions at Planning Seal" table). The engine cannot unilaterally design and ship a new cross-cutting governance mechanism (this would itself violate the item's own stated gate — no live use before Head of Engineering sign-off) — a named-authority design decision is required before implementation.
- **Owning authority:** Head of Engineering
- **Unblock criteria:** Head of Engineering (with Head of Specs Team, per the outstanding action) holds a design/technical-approach session, selects an approach, and signs off before the new mechanism is implemented and used live. A concrete proposal (see below) has been drafted as input to that session, informed by this sprint's own direct experience of the exact failure mode (see Proposal Input).
- **SLA due-by:** 2026-08-03T02:15:00Z (72 hours — architectural/governance-process decision, treated per the Strategy-boundary SLA tier given its cross-cutting nature)
- **Blocks execution:** No (per sprint planning's own classification of this outstanding action as non-blocking; the existing reactive mechanism in `shared_standards.md §12` remains the documented fallback in the meantime)
- **Disposition:** Open
- **Resolution summary:** *(to be completed when Head of Engineering's design session concludes and sign-off is recorded)*

---

## Proposal Input (drafted by Sprint Execution Engine — not a decision, input for the design session)

This sprint (`2026-07-30__release-v8.0`) is itself a live, fresh case study of the exact problem ST-19 targets: 6 EPIC branches were worked across this session, each cut from `main` at a different merge point, each carrying an independent copy of `execution_state.json` that only reflects whichever EPICs had merged into `main` *at the moment that branch was created* — not the branches merged afterward. Every branch switch during this session showed the working tree reverting to an older, EPIC-count-reduced version of the file, exactly matching the reactive-conflict pattern `shared_standards.md §12` and `execution_prompt.md` STEP 4 step 3c already work around after the fact (post-merge sibling-branch sync, orphaned-commit reconciliation).

**Candidate structural approaches for the design session to evaluate** (not a recommendation — input only):

1. **Per-EPIC state files.** Split `execution_state.json` into one file per EPIC (e.g. `execution_state_EPIC-01.json`) that each EPIC branch owns exclusively and never shares with another branch — eliminating the shared-file conflict surface entirely. A lightweight top-level `execution_state_index.json` (or a computed view) would be assembled by whichever routine needs the cross-EPIC summary (Delivery Verification, Post-Ship Closure), reading all per-EPIC files rather than one shared file. Trade-off: more files to track; STEP 0's "which items are done" resumability check would need to scan a directory instead of one file.
2. **CRDT-style append-only per-EPIC log, computed summary.** Similar to #1 but keep a single physical file, structured as an append-only sequence of per-EPIC-branch entries (never overwritten, only appended), with the "current state" computed by folding the log — git's own merge naturally unions appends without semantic conflict as long as no entry is ever edited in place. Trade-off: more complex read-side logic; the current schema's per-story mutable fields (status transitions) don't fit an append-only model without redesign.
3. **Formalize the existing reactive mechanism as the permanent answer.** Conclude that `shared_standards.md §12`'s existing rules (merge sequencing, "keep the more-recently-merged branch's version," GOVERNANCE commit after each merge) plus `execution_prompt.md` STEP 4's proactive sibling-sync (step 3c, added post-ship closure `2026-07-24__release-v7.8`) are sufficient, and RISK-04 is adequately mitigated already — no new mechanism needed, downgrade this story to a documentation-only closure (update `shared_standards.md §12` to cross-reference this decision).

This session's own experience is consistent with option 3 being *workable* (no correctness failures occurred — the STEP 4 step 3c proactive sync and CLAUDE.md §8 conflict-resolution rules would have handled reconciliation correctly at actual merge time), but confirms the underlying friction option 1/2 aim to eliminate is real (every branch switch this session showed stale cross-EPIC state, requiring active attention to not misinterpret it as data loss).
