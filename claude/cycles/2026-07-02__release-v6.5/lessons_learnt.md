**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-02__release-v6.5
**Release:** v6.5
**Last Updated:** 2026-07-02

---

# Lessons Learnt — Release Planning v6.5

## What worked well

1. **Backlog-add's mandatory ID pre-scan caught a real collision before any drafting was finalised.** The initial candidate IDs (BLG-GOV-155/156/157) were checked against both `backlog.md` and `backlog_archive.md` before writing; BLG-GOV-156 turned out to already be in use (unrelated "Base44 prompt template versioning" item, filed at the `2026-07-02__scheduled` rebalance) and BLG-GOV-155 was found to be a skipped/unused ID. Renumbered cleanly to 157/158/159 with no rework.
2. **The STEP 1.4a Perennial-Return Check surfaced BLG-QA-61 for an explicit disposition rather than allowing a 4th silent carry-forward.** Combined with the STEP 0 Carry-Forward Advisory (which independently flagged the same item from `2026-07-02__release-v6.4` lessons_learnt_closure.md), the item received a concrete resolution this cycle (promoted to firm scope, XS effort) rather than continuing to roll forward.
3. **The audit's own SLA section (`audit_report_AUD-2026-07-01.md` §9) directly informed scope prioritisation** — AUD-006 was pulled into EPIC-01 specifically because the audit flagged it as a P0-escalation risk if still open at the next audit, rather than being selected arbitrarily among the 10 open findings.

---

## Friction Log

### Friction Item 1 — STEP 4.1 field updates precede STEP 7's active_cycle sync, creating a transient state contradiction

**Classification:** Type C — Prompt Gap (the sequencing is as-written, not a misapplication)

**Recurrence:** First identified this cycle.

**What happened:** STEP 4.1 requires writing `design_gate_required`/`design_gate_status` into `.claude_current_state.json` "in same session" as STEP 4 — well before STEP 7's intermediate sync updates `active_cycle` and `status` to the new cycle. For several steps (STEP 4 through STEP 6), `.claude_current_state.json` read `active_cycle: 2026-07-02__release-v6.4` while simultaneously showing `design_gate_status: not_started` — overwriting v6.4's own completed `Passed` record before the file's `active_cycle` pointer had moved on. Any concurrent reader of `.claude_current_state.json` during that window would see an internally contradictory state (old cycle ID, new cycle's gate status).

**Suggested fix:** Either move the STEP 4.1 `.claude_current_state.json` write to occur atomically with STEP 7's intermediate sync (single write, not two), or have STEP 4.1 write only to `state.json` (cycle-scoped) and defer the `.claude_current_state.json` update entirely to STEP 7.

**Target:** Head of Specs Team, next `release_planning_prompt.md` revision.

### Friction Item 2 — STEP 5's "under the existing release section" instruction assumes a formal roadmap section that v6.5 did not have

**Classification:** Type C — Prompt Gap

**Recurrence:** First identified this cycle.

**What happened:** `current_roadmap.md` had no `## vX.Y` section for v6.5 — only the STEP 8.1 Option (b) deferral record consumed at §-1.2. STEP 5's instruction to annotate "under the existing release section only" had no literal target. Resolved by annotating the `**Next planned release:**` line in §1 (Current Version) instead, which is the closest existing anchor, and updating it from `[TBD]` to name v6.5 explicitly.

**Suggested fix:** STEP 5 should explicitly cover the Option (b)-deferred case: "if no formal `## vX.Y` roadmap section exists for this release, annotate the `**Next planned release:**` line in §1 instead."

**Target:** Head of Specs Team, next `release_planning_prompt.md` revision.

### Friction Item 3 — §1.4a's two-option disposition framing doesn't name a "resolve now" outcome

**Classification:** Type C — Prompt Gap

**Recurrence:** First identified this cycle (though the underlying rule has existed since it was introduced).

**What happened:** §1.4a frames the Perennial-Return disposition as exactly two options — (a) keep as conditional with updated gate evidence, or (b) remove from horizon. BLG-QA-61's actual resolution (promote to firm scope and complete it this cycle, since it is XS effort and was never really gate-blocked, just deprioritised) does not cleanly fit either label. Recorded as an explicit third disposition this cycle with rationale, consistent with the section's intent (an active decision, not silent re-entry) even though it doesn't match either named option.

**Suggested fix:** Add a third named option to §1.4a: "(c) resolve directly this cycle" for low-effort items where the cheapest fix is closure rather than further deferral or parking.

**Target:** Head of Specs Team, next `release_planning_prompt.md` revision.

---

## Monitoring Carried Forward

- **LP-02 continuation (Skill-Silo corrective):** v6.5 includes 2 user-facing items (BLG-FE-46, BLG-FEAT-41), directly responding to the `2026-07-02__scheduled` finding that a single U-item pull-forward did not correct the 64.8% rolling-3-cycle average. Next rebalance should check whether 2 U-items in one release moves the average meaningfully, informing whether "≥2 U-items per release" should become a standing rule rather than a per-cycle instruction.
- **DF-09 (standing AI safety checklist proposal):** Dormant this cycle — v6.5 has no AI/security-adjacent scope item, so the ad hoc-derivation pattern that would trigger LP-04's 3rd-cycle escalation condition did not recur. Still un-actioned; re-evaluate whenever the next AI/security item appears.

---

## Action Items (to be completed at Post-Ship Closure)

| ID | Source | Summary | Classification | Owner | Target |
|----|--------|---------|----------------|-------|--------|
| LP-01 | Release Planning | STEP 4.1 / STEP 7 state-sync sequencing contradiction (Friction Item 1) | prompt-gap | Head of Specs Team | Next release_planning_prompt.md revision |
| LP-02 | Release Planning | STEP 5 roadmap-annotation gap for Option(b)-deferred releases (Friction Item 2) | prompt-gap | Head of Specs Team | Next release_planning_prompt.md revision |
| LP-03 | Release Planning | §1.4a missing "resolve now" disposition option (Friction Item 3) | prompt-gap | Head of Specs Team | Next release_planning_prompt.md revision |
| LP-04 | Release Planning | Confirm whether 2 U-items in v6.5 moves the Skill-Silo rolling average meaningfully | monitoring | PMO Lead | Post-ship / next rebalance |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle": "2026-07-02__release-v6.5",
  "release": "v6.5",
  "status": "seeded",
  "completed_at": ""
}
