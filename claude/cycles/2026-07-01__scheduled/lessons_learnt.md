**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-01__scheduled
**Last Updated:** 2026-07-01

---

# Lessons Learnt — Roadmap Rebalance 2026-07-01__scheduled

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-07-01__scheduled
Reviewed by: PMO Lead; Head of Specs Team
Date filed: 2026-07-01
Prior cycle checked: 2026-06-26__scheduled

---

## What worked well

1. **STEP -1.5 stale-release-target rule caught two silently-aging deferred patches.** FI-META-01 and FI-META-02 (both filed at the 2026-06-26__scheduled meta-review with Target: "v6.3") were both correctly flagged OVERDUE this cycle because v6.3 shipped 2026-06-30 without either being actioned. Without this rule (added v7.5, 2026-06-19), both would likely have continued to silently carry forward indefinitely.

2. **FI-1 was closed correctly rather than mechanically re-carried.** Instead of trusting the prior cycle's premise that `velocity_metrics.md` was at the wrong canonical path, this cycle cross-referenced the live `roadmap_prompt.md` STEP 1.1 text and `prompt_change_log.md`, which showed the `claude/cycles/velocity_metrics.md` path has been canonical since v4.7 (2026-04-01). The friction item was closed as based on an inaccurate premise rather than triggering an unnecessary prompt patch.

3. **Ideas register 3-cycle hard cap (§4.5) processed cleanly.** IDEA-infra-ops-20260622-02 reached its terminal decision point and was resolved with a concrete, evidence-based PO rationale (System Status page already covers the proposed homepage widget's function) rather than being mechanically re-parked for a 3rd cycle.

4. **STEP 8.0 fast-track correctly discriminated between adjacent P1 items.** The priority-marker scan identified BLG-BE-40 as a genuine correctness bug requiring mandatory Now-horizon inclusion, while correctly excluding BLG-SPEC-35 (P1 but pre-work, not a correctness bug) from the same treatment.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type A — Governance Drift: A documented rule (OPERATIONAL_GUIDE.md §14 "Standing rule" requiring simultaneous phase-section-header and §14-table updates) was not followed on at least two prior edits

**Recurrence:** No — first occurrence identified at this cycle (no prior lessons_learnt.md flagged this specific drift).

**What happened:**
While applying the FI-META-02 action-now patch (roadmap_prompt.md v7.6→v7.7) and following the CLAUDE.md §6 Governance File Edit Checklist, OPERATIONAL_GUIDE.md was found out of sync with itself. The document header (top of file) read Version 4.65, but the §14 "Version" field read 4.63 — two versions behind. The §14 "Roadmap Engine Source" row still read `roadmap_prompt.md v7.5`, even though both the §6 phase-section header and the §13 artefact register already correctly showed v7.6 (updated at the 2026-06-22 bump). The §14 internal Change Log table was also missing the row documenting the 4.65 bump (execution_prompt.md v3.47→v3.48, 2026-06-24), even though that bump was correctly recorded the same day in `claude/system/prompt_change_log.md`.

**Where in the routine:**
CLAUDE.md §6 Governance File Edit Checklist / roadmap_prompt.md STEP 12 (Governance File Edit Checklist enforcement before commit)

**Root cause:**
Process gap — the OPERATIONAL_GUIDE.md §14 "Standing rule" requiring the phase-section header and the §14 table to be updated together is enforced only by convention, not tooling. At least one prior edit (the 2026-06-22 v7.6 bump) updated §6/§13 but missed the §14 "Roadmap Engine Source" row and the §14 "Version" field; a later edit (the 2026-06-24 v4.65 bump) updated the document header and `prompt_change_log.md` but not the internal §14 Change Log table.

**Blast radius analysis:**
- What would have propagated: any agent trusting the §14 table in isolation (rather than the document header or §6/§13) would cite `roadmap_prompt.md` as v7.5 — two versions stale — when reasoning about which prompt behaviours are currently active.
- When it would have surfaced: at the next lifecycle audit (`run audit`, due every 3 cycles) or the next time an agent needed to confirm the exact `roadmap_prompt.md` version from §14 alone.
- Recovery cost if uncaught: medium — could cause an agent to apply a patch against the wrong assumed baseline version, or to skip a change already present, believing it still pending.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/OPERATIONAL_GUIDE.md`
  - Section: §14 Playbook Governance (Version field, Roadmap Engine Source row, Change Log table)
  - Change: corrected Roadmap Engine Source `v7.5→v7.7`; bumped §14 Version `4.63→4.66` (catching up the un-recorded 4.65 bump plus this cycle's 4.66 bump); backfilled the missing 4.65 Change Log row; added the 4.66 Change Log row for this cycle's `roadmap_prompt.md` v7.7 bump.
  - Version: 4.63 → 4.66
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — two entries appended to `claude/system/prompt_change_log.md` (`roadmap_prompt.md v7.6→v7.7` and `OPERATIONAL_GUIDE.md v4.65→v4.66`)

---

### Friction Item 2

**Classification:**
- Type C — Dependency Stall: A deferred patch's synchronization point (a release version) was not a reliable gate — it could resolve incorrectly if the release shipped before the next check

**Recurrence:** Yes — appeared in 2026-06-26__scheduled (as the pattern underlying FI-META-01 and FI-META-02 themselves, both filed with Target: "v6.3")

**What happened:**
FI-META-01 and FI-META-02 were both filed at the 2026-06-26__scheduled meta-review with `Target: v6.3 (as a §6 governance checklist prompt patch)`. v6.3 shipped 2026-06-30 — before this rebalance ran (2026-07-01) and without either patch having been picked up during `plan release v6.3` or `run design-gate v6.3`. STEP -1.5's stale-release-target check (added v7.5, 2026-06-19) correctly caught this and forced disposition this cycle: FI-META-01 was found moot (Withdrawn-superseded, since its underlying premise — see Friction Item closure under "What worked well" #2 — was inaccurate) and FI-META-02 was applied action-now.

**Where in the routine:**
STEP 11.2 (Prompt Change Classification) at the originating cycle (2026-06-26__scheduled); STEP -1.5 (Stale Release Target Check) at this cycle

**Root cause:**
Naming inconsistency — STEP 11.2 permits a deferred patch's Target field to name a release version, but a release version is not a reliable synchronization point: it can ship before or after any given rebalance, independent of cycle cadence. A cycle_id or absolute date target would resolve deterministically under STEP -1.5, whereas a release-version target only resolves correctly if that release happens to still be unshipped at the next check.

**Blast radius analysis:**
- What would have propagated: without the STEP -1.5 rule (itself only added 2026-06-19), both patches could have sat unresolved indefinitely once v6.3 shipped and rolled off as the "current" release reference.
- When it would have surfaced: possibly never on its own — would require an explicit audit or manual grep of deferred patches to notice they reference a shipped release.
- Recovery cost if uncaught: medium — a valid improvement (FI-META-02, which addresses a genuine large-window budget risk) could have been silently lost.

**Process patch:**

→ Deferred patch (cannot apply this run — a wording change to STEP 11.2 itself should go through its own action-now/defer classification rather than being bundled into an already-large patch, to reduce risk of an incomplete edit):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 11.2 (Prompt Change Classification)
  - Change required: add a rule that deferred patch Target fields must name a cycle_id or absolute date, not a release version alone; if a release version is given at filing time, STEP 11.2 must also record a concrete date estimate (e.g., "v6.3 (target ships ~2026-06-28, revisit by 2026-07-01__scheduled)") so STEP -1.5 has a deterministic check even before the release name itself resolves.
  - Owner: Head of Specs Team
  - Target: next `run roadmap` scheduled cycle

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| FI-P3-01 — Playwright strict mode advisory to Base44 prompt draft §6 | 2026-06-26__scheduled (carried from v6.2 closure) | Owner: Director of Quality, Target: v6.3 — not actioned; v6.3 has now shipped | Head of Specs Team |
| FI-P3-02 — Frontend testing gate clarification (code review vs staging for wording-only ACs) | 2026-06-26__scheduled (carried from v6.2 closure) | Owner: Head of Specs Team, Target: v6.3 — not actioned; v6.3 has now shipped | Head of Specs Team |
| FI-P4-01 — CI/infra `spec_references` convention to execution_prompt.md §3.1.A | 2026-06-26__scheduled (carried from v6.2 closure); also recorded as DF-10 in the v6.3 closure Carry-Forward | Owner: Head of Specs Team, Target: v6.3 — not actioned; v6.3 has now shipped (second consecutive miss) | Head of Specs Team |

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/roadmap_prompt.md` | STEP -1.6 | Added large-window budget note (FI-META-02): when the inline intake window produces >30 submissions, budget additional context depth for STEPs 4 and 5; if advancing idea count exceeds 15, prioritise the highest-scoring ideas and park the remainder | v7.6→v7.7 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §14 (Version field, Roadmap Engine Source row, Change Log table) | Corrected stale Roadmap Engine Source row, backfilled missing 4.65 Change Log row, bumped Version (Friction Item 1) | v4.63→v4.66 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-01__scheduled/run_manifest.md`
- `claude/cycles/2026-07-01__scheduled/cycle_record.md`
- `claude/cycles/2026-07-01__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-01__scheduled/lessons_learnt.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 11.2 | Deferred patch Target fields must name a cycle_id or absolute date, not a release version alone (Friction Item 2) | Head of Specs Team | Next `run roadmap` scheduled cycle |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| FI-P3-01 (Playwright strict mode advisory) — target v6.3 shipped without action | Recurrence | Head of Specs Team | Deferred patch carried 2+ cycles (2026-06-26__scheduled → v6.3 closure → this cycle) past its named target release; needs a concrete new target at `plan release v6.4` |
| FI-P3-02 (frontend testing gate clarification) — target v6.3 shipped without action | Recurrence | Head of Specs Team | Same pattern as FI-P3-01 |
| FI-P4-01 (CI/infra `spec_references` convention) — target v6.3 shipped without action; matches DF-10 | Recurrence | Head of Specs Team | Same pattern as FI-P3-01; second consecutive miss, also flagged OVERDUE in `run_manifest.md` this cycle |

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | FI-P3-01, FI-P3-02, and FI-P4-01 all targeted "v6.3" and v6.3 shipped 2026-06-30 without any being actioned | Re-target all three to a concrete cycle_id (`plan release v6.4` and `run design-gate v6.4`) rather than leaving them pointed at a shipped release name | Release Planning |
| 2 | STEP 11.2's Target field allows a bare release-version target, which becomes silently stale once that release ships ahead of the next check (Friction Item 2) | Apply the deferred STEP 11.2 wording patch at the next roadmap rebalance | Roadmap |
| 3 | Skill-Silo Alert rolling-3-cycle average is 53.2%, above the 40% ceiling, with BLG-FEAT-54 identified as the pull-forward candidate | `plan release v6.4` should give BLG-FEAT-54 (or another U-story) firm consideration to bring the ratio down | Release Planning |
| 4 | BLG-GOV-144 flagged as a >12-month archive candidate during STEP 3.1 | `groom backlog` should review BLG-GOV-144 for archival at the next grooming pass | Backlog Management |

---

## STEP 11.4 — Meta-Review

**Trigger:** 1 cycle since last meta-review (2026-06-26__scheduled reset). Not due — threshold is 3 cycles.

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-01__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-01T00:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 3,
  "overdue_patches": 3,
  "status": "Complete"
}
```
