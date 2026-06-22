**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-06-22__scheduled
**Last Updated:** 2026-06-22

---

# Lessons Learnt — Roadmap Rebalance 2026-06-22__scheduled

**Run type:** Scheduled
**Reviewed by:** PMO Lead; Head of Specs Team
**Date filed:** 2026-06-22
**Prior cycle checked:** 2026-06-19__scheduled

---

## What worked well

1. **STEP 8.2 fired correctly on first use.** The deferred patch (active-backlog verification for Now horizon items) was applied as action-now in STEP -1.5, then immediately validated in STEP 8.2 during this same run. It caught two items (BLG-FE-52 and BLG-FE-53) that were referenced in the context-window session summary as "SI-02 frontend candidates" but are actually pre-design documents archived since v4.4. The error would have propagated to current_roadmap.md had STEP 8.2 not been in place. The deferred patch serves its intended purpose.

2. **Action-now deferred patch lifecycle completed cleanly.** The roadmap_prompt.md STEP 8.2 patch was filed at 2026-06-19__scheduled with a "Next run roadmap" target. It was applied at STEP -1.5 this run (not OVERDUE — first cycle at target) with correct authority (Head of Specs Team), governance checklist complete (all 4 CLAUDE.md §6 steps executed), and validation in STEP 8.2 this same run.

3. **Product Value Ratio improving but still critical.** Ratio moved from 0.093 (2026-06-19__scheduled) to 0.136 (this run) as v6.0's U-stories replaced the low-U v5.5 cycle in the rolling 5-cycle window. Still below the 0.30 alert threshold, but the trajectory is positive. The v6.1 Now section composition (2 firm U-stories + 1 conditional) should improve the next-run ratio toward 0.20+ if v6.1 delivers on commitment.

4. **Challenger PVC debate resolved constructively.** The Challenger Product Velocity Concern produced a concrete, named commitment (BLG-FE-76 + BLG-FE-78 as firm v6.1 scope) rather than abstract advisory language. The Challenger accepted the clearance statement. This is a model outcome for STEP 5 PVC debates.

---

## Friction Log

### Friction Item 1

**Classification:**
- Type B — Artefact Drift: A prior-session context summary cited archived BLG items (BLG-FE-52, BLG-FE-53) as active candidates without verification

**Recurrence:** First occurrence of this specific failure mode (but root cause is the same class as the 2026-06-19__scheduled BLG-GOV-113 error that motivated STEP 8.2)

**What happened:**
The context summary from the prior session (generated at compaction time) listed "BLG-FE-52/53 (SI-02 frontend display): same gate as PT-04" as conditional scope candidates for the v6.1 Now section. When STEP 8.2 verification ran, both items were found in `backlog_archive.md` (not active `backlog.md`). They are SI-02 pre-design documents shipped in v4.4 — not the SI-02 frontend implementation, which has no active BLG items.

**Where in the routine:**
STEP 8.2 — Now Horizon Item Verification (first firing of the new step)

**Root cause:**
Context compaction summaries cite backlog items by ID without verifying active status. When the next session reads the summary, it inherits these references as apparent facts. The items were never in the v6.0 Now section — they were only in the session's mental model of what would follow v6.0. STEP 8.2 is the structural fix.

**Blast radius analysis:**
- What would have propagated: BLG-FE-52/53 listed as conditional scope in current_roadmap.md; these items are archived and have no implementation story to back them
- When it would have surfaced: At v6.1 release planning, when STEP 8.2 or STEP 1 artefact verification would have caught the mismatch
- Recovery cost: Low (one-line removal from roadmap) but confusing for future operators reading archived BLG IDs in the roadmap

**Resolution:** STEP 8.2 excluded both items correctly. SI-02 frontend implementation (Behavioural Drift Detection UI) has no current BLG items — assess and file at v6.1 release planning once PT-04 gate review is complete.

**Process note:** This is exactly the failure class that motivated STEP 8.2. The patch validated itself on its first run.

---

## Consolidated Action Summary

### Immediate actions applied: 1

| Action | File | Change |
|--------|------|--------|
| roadmap_prompt.md STEP 8.2 deferred patch | `claude/system/roadmap_prompt.md` | v7.5→v7.6; STEP 8.2 inserted |

### Deferred to next cycle: 2

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | PT-04 (BLG-FEAT-25) closed trade count re-check — ~13 at v6.0, projected ~2026-07-02. If ≥20 at v6.1 sprint planning, PT-04 is eligible for conditional scope. Also: if gate clears, file SI-02 frontend implementation BLG items (no active BLG items currently). | PMO Lead | v6.1 sprint planning |
| 2 | v6.1 sprint planning must confirm BLG-FE-76 and BLG-FE-78 as firm scope per Challenger PVC clearance statement (DL-054). Challenger to re-raise if either item is deferred or made conditional. | Challenger; PMO Lead | v6.1 sprint planning |

### Monitor (no action required): 1

| # | Item |
|---|------|
| 1 | Product Value Ratio trajectory: 0.093 → 0.136 over two rebalance cycles. If v6.1 delivers BLG-FE-76, BLG-FE-78, and PT-04 (conditional), next 5-cycle window should show ratio approaching 0.18–0.20. Monitor at next rebalance. |

---

## Outstanding deferred patches

None — all prior deferred patches resolved (STEP 8.2 applied this run; all v6.0 closure patches applied by AUD-2026-06-22).

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | PT-04 gate (~13 closed trades, projected ~2026-07-02). SI-02 frontend BLG items do not yet exist. | At v6.1 sprint planning: (a) verify closed trade count; (b) if ≥20, PT-04 is conditional scope; (c) file SI-02 frontend BLG items at that point. | Sprint Planning → Release Planning |
| 2 | Challenger clearance statement: BLG-FE-76 and BLG-FE-78 must be firm scope at v6.1 sprint planning, not deferred. | Sprint planning engine must confirm both items are in sprint backlog as firm (not conditional) at plan seal. | Sprint Planning |
