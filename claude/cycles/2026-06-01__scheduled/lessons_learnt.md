**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-01
**Cycle:** 2026-06-01__scheduled

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled run
Run: 2026-06-01__scheduled
Reviewed by: PMO Lead
Date filed: 2026-06-01
Prior cycle checked: 2026-05-27__scheduled (claude/cycles/2026-05-27__scheduled/lessons_learnt.md — found)

---

## What worked well

- **Prior OA resolution fully confirmed before run.** All 3 OAs from 2026-05-27__scheduled were verified as resolved via cycle records before STEP 2 began. No carry-forward ambiguity.
- **Terminal idea disposition was clean.** IDEA-director-of-hr-20260525-02 reached the 3-cycle hard cap. STEP 4.0 Gate-Condition Re-Check was applied correctly; PO dispositioned to Backlog (gate-conditional) → BLG-GOV-71 without debate friction.
- **Gate-cleared withdrawal during intake.** IDEA-financial-reporting-20260527-02 was correctly identified during IW-20260601-01 as having a shipped gate (BLG-FEAT-39 COMPLETE). Agent withdrew the idea voluntarily, preventing stale gate rationale from persisting into STEP 4.0.
- **Single-item STEP 5 debate completed efficiently.** IDEA-api-contracts-20260527-02 advanced cleanly through STEP 5 with a Challenger Clearance Statement. No Type A counter-argument was needed; the Clearance was thorough and §rules-referenced.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type D — Cognitive Fatigue: A detail was missed due to prompt length, context overload, or accumulated complexity

**Recurrence:** Yes — appeared in 2026-05-27__scheduled as LL-04 (34% duplication rate from IW-20260527-01)

**What happened:**
IDEA-head-of-specs-20260601-02 submitted by Head of Specs Team in IW-20260601-01 was substantively identical to IDEA-api-contracts-20260527-02, which had been parked since IW-20260527-01 and was visible in the parked queue. The idea_intake_prompt.md §STEP 1 instructs agents to surface and consider parked ideas, but Head of Specs did not check the parked queue before submitting a new idea on the same topic. This created a duplicate that required rejection in STEP 4.

**Where in the routine:**
IW-20260601-01 STEP 2 (idea submission) — failure to cross-check parked queue before submitting net-new idea.

**Root cause:**
Template omission — the idea template does not include a "parked queue check" field or reminder. Agents are expected to check the register (§STEP 1 of idea_intake_prompt.md) but there is no enforcement mechanism at submission time.

**Blast radius analysis:**
- What would have propagated: Duplicate in STEP 4 requiring extra classification work
- When it would have surfaced: STEP 4 — caught and rejected as duplicate (caught correctly this cycle)
- Recovery cost if uncaught: Low (duplicate would have advanced, debated, and been rejected as redundant at STEP 5 or STEP 8)

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/idea_intake_prompt.md`
  - Section: §STEP 2 (Solicit Submissions) — §2.2 Submission Quality Check
  - Change required: Add a "parked queue check" step to §2.2: before submitting, each agent must check claude/ideas/ideas_register.md for existing Parked ideas on the same topic from their agent slug or substantially similar scope; if found, note the overlap in the submission or resubmit the parked idea rather than creating a duplicate.
  - Owner: Head of Specs Team
  - Target: Next scheduled rebalance (2026-06-01__scheduled + 1 cycle)

---

### Friction Item 2

**Classification:** Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** No — first observation

**What happened:**
The `groom backlog` run recorded in .claude_current_state.json (`last_groom_backlog_outcome`: 8 items archived) indicates BLG-GOV-62, BLG-OPS-28/31/37/44/45, BLG-FE-49, and BLG-FEAT-38 were archived. However, during this rebalance cycle, grep confirmed these items still appear as section headers in claude/backlog/backlog.md. The groom outcome was recorded in state but the actual file edits may not have been applied, or were partially applied. This means the backlog.md may have slightly more than the stated ~49 active items.

**Where in the routine:**
STEP 3 — Backlog Health Review (advisory detection; did not block the run)

**Root cause:**
Process gap — `groom backlog` engine records its outcome in state.json but it's not verified that the file edits were applied. The advisory was noted in STEP 3 and will be resolved at the next `groom backlog` invocation.

**Blast radius analysis:**
- What would have propagated: Sprint planning pulling completed items into candidate list; inflated active item count reported in cycle_summary.md
- When it would have surfaced: Next `plan sprint` or `groom backlog` run
- Recovery cost if uncaught: Low (completed items cannot advance; they would be caught at sprint planning as already-shipped)

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/backlog_management_prompt.md`
  - Section: STEP that writes archive changes to backlog.md
  - Change required: After writing archive changes to backlog.md, add a verification step: grep backlog.md for archived item IDs and confirm they no longer appear as section headers. If found: halt and report which items were not successfully removed.
  - Owner: Head of Specs Team
  - Target: Next `groom backlog` invocation

---

## Deferred Patches

| # | File | Section | Change | Owner | Target |
|---|------|---------|--------|-------|--------|
| 1 | claude/system/idea_intake_prompt.md | §STEP 2 §2.2 Submission Quality Check | Add parked queue check before net-new submission | Head of Specs Team | Next scheduled rebalance |
| 2 | claude/system/backlog_management_prompt.md | Archive write verification step | Add post-write grep check to confirm archived items removed from backlog.md | Head of Specs Team | Next groom backlog |

## Outstanding Actions

None. Both items are deferred patches with named owners and target dates. No escalations.

---

## Process Observations (Not Friction)

| # | Observation | Owner | Action |
|---|-------------|-------|--------|
| LL-01 | CPS stable at 1.15 for two consecutive cycles. Low-complexity period post-v4.7. No drift concern. | Strategy Rules & System Intent Owner | Monitor. No action. |
| LL-02 | IDEA-challenger-20260601-02 raised a valid cadence overhead concern: 3+ consecutive scheduled rebalances with empty Now horizon and no items advancing. Filed as BLG-GOV-73 for meta-review consideration. | PMO Lead | BLG-GOV-73 filed; advance at meta-review (cycle 3). |
| LL-03 | Prior idea duplication rate was 34% (LL-04, 2026-05-27__scheduled). This cycle: 1 duplicate of 44 new = 2%. Significant improvement — but one duplicate is still one too many. Deferred patch filed (Friction Item 1). | PMO Lead | Monitor; deferred patch addresses root cause. |
| LL-04 | SI-05 Phase 1 gate approaching (2026-06-21 = 20 days). v4.8 should plan SI-05 Phase 1 inclusion. Filed as advisory in cycle_summary.md Carry-Forward. | Product Owner | Advisory noted at v4.8 release planning. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-06-01__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-06-01T14:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 2,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
