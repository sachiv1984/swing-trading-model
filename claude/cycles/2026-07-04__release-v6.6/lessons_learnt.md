**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-04__release-v6.6
**Release:** v6.6
**Last Updated:** 2026-07-04

---

# Lessons Learnt — Release Planning v6.6

## What worked well

1. **LP-02/LP-03 fixes from v6.5 (release_planning_prompt.md v2.40) worked as intended on first live use.** STEP 5's new fallback wording ("if no formal `## vX.Y` roadmap section exists, annotate the `**Next planned release:**` line in §1 instead") applied cleanly without needing to improvise, unlike v6.5 which had to work around the gap ad hoc.
2. **The 1.4b calendar-gate check correctly distinguished "gate cleared before cycle open" from "within-sprint gate."** BLG-FE-40's 30-day RFJ usage gate cleared 2026-06-21, well before this cycle's sprint would start — the rule's literal scope (gates clearing *during* the sprint window) meant this item could be classified firm on PO confirmation rather than forced conditional, which is the correct outcome (the gate genuinely cleared, it just hadn't been re-visited).
3. **Cross-checking a named rebalance pull-forward candidate's own gate status before accepting it into scope caught a real mismatch.** BLG-FEAT-52 was named as a Skill-Silo pull-forward candidate by the `2026-07-03__scheduled` rebalance, but its own gate (PO-02 sprint planning imminent) is not met — accepting it into firm scope without this check would have produced another item destined to return to backlog at sprint close (the exact pattern §1.4b was designed to eliminate for calendar gates, here recurring for a state-based gate).

---

## Friction Log

### Friction Item 1 — STEP 4.1 / STEP 7 state-sync sequencing contradiction recurs (LP-01, 2nd consecutive cycle)

**Classification:** Type C — Prompt Gap (recurrence — not yet fixed; LP-01 was deferred at v6.5 post-ship closure per `closure_record.md` §5)

**Recurrence:** 2nd consecutive cycle (v6.5, v6.6). Per `lessons_learnt_prompt.md` §3.7, a 3rd-cycle recurrence (v6.7, if still unresolved) would trigger an automatic recurrence escalation.

**What happened:** Identical to v6.5's Friction Item 1 — STEP 4.1 wrote `design_gate_status: not_started` to `.claude_current_state.json` while `active_cycle` still pointed at `2026-07-02__release-v6.5`, overwriting v6.5's own completed `Passed` design-gate record before STEP 7's intermediate sync moved `active_cycle` forward. The same transient internally-contradictory window occurred (STEP 4 through STEP 6 of this session).

**Suggested fix:** Unchanged from v6.5 — either move the STEP 4.1 `.claude_current_state.json` write to occur atomically with STEP 7's intermediate sync (single write, not two), or have STEP 4.1 write only to `state.json` (cycle-scoped) and defer the `.claude_current_state.json` update entirely to STEP 7.

**Target:** Head of Specs Team, next `release_planning_prompt.md` revision — recommend prioritising this one specifically given it is now a confirmed 2-cycle recurrence with an identical fix already proposed and not yet applied.

### Friction Item 2 — Roadmap rebalance's pull-forward candidate naming does not verify the candidate's own gate status

**Classification:** Type C — Prompt Gap

**Recurrence:** First identified this cycle.

**What happened:** The `2026-07-03__scheduled` rebalance named BLG-FE-82 and BLG-FEAT-52 as Skill-Silo pull-forward candidates to help correct the worsening G+D+P rolling average. BLG-FE-82 was a valid candidate (ungated), but BLG-FEAT-52 carries its own unmet gate (Arc 4 PO-02 sprint planning imminent, itself blocked on a 6-months-AI-journal-entries data-density gate with no confirmed near-term clearance) — a fact discoverable directly from the item's own backlog entry. Had this release planning cycle not cross-checked it, BLG-FEAT-52 would likely have entered scope and returned to backlog at sprint close, a version of the exact within-sprint-gate pattern §1.4b already guards against for calendar gates, but here for a state-based gate that the rebalance engine's own candidate-selection step did not check.

**Suggested fix:** `roadmap_prompt.md`'s pull-forward candidate selection step should verify each named candidate's own gate condition (if any) is met or near-term before naming it, or explicitly flag it as "gate status unverified — release planning to confirm" when naming it.

**Target:** Head of Specs Team / PMO Lead, next `roadmap_prompt.md` revision.

---

## Monitoring Carried Forward

- **LP-04 continuation (Skill-Silo corrective, from v6.5):** v6.5 included 2 nominal U-items but only 1 classified as a true U-item on review. v6.6 includes 2 U-items again (BLG-FE-82, BLG-FE-40) — both are genuinely user-facing this time (a real accessibility fix and a real feature, not an assessment-only item). Next rebalance should check whether this cycle's classification holds and whether the rolling-3-cycle G+D+P average has begun to correct.
- **DF-09 (standing AI safety checklist proposal):** Still dormant — v6.6 has no AI/security-adjacent scope item.
- **DF-18 (`/commit-check` pathspec-diff reinforcement, from v6.5 carry-forward):** Still unapplied — 2nd cycle carry-forward as of v6.6 (v6.5→v6.6). Per `lessons_learnt_prompt.md` §3.7, if still unapplied at v6.7 this becomes a 3-cycle carry-forward triggering an automatic recurrence escalation. Not in this engine's write scope (`.claude/skills/` outside every routine's declared write scope) — Head of Specs Team should apply directly before that threshold.

---

## Action Items (to be completed at Post-Ship Closure)

| ID | Source | Summary | Classification | Owner | Target |
|----|--------|---------|----------------|-------|--------|
| LP-01 (v6.6) | Release Planning | STEP 4.1 / STEP 7 state-sync sequencing contradiction — 2nd consecutive cycle recurrence, fix proposed twice now | prompt-gap | Head of Specs Team | Next release_planning_prompt.md revision (priority) |
| LP-05 | Release Planning | Roadmap pull-forward candidates should have their own gate status verified before naming (Friction Item 2) | prompt-gap | Head of Specs Team / PMO Lead | Next roadmap_prompt.md revision |
| LP-06 | Release Planning | Confirm whether v6.6's 2 genuinely-classified U-items move the Skill-Silo rolling average | monitoring | PMO Lead | Post-ship / next rebalance |
| LP-07 | Release Planning | DF-18 `/commit-check` patch now 2-cycle carry-forward — apply before v6.7 to avoid automatic recurrence escalation | carry-forward | Head of Specs Team | Before v6.7 release planning |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle": "2026-07-04__release-v6.6",
  "release": "v6.6",
  "status": "seeded",
  "completed_at": ""
}
