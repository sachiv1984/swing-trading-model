**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-06-24__scheduled
**Last Updated:** 2026-06-24

---

# Lessons Learnt — Roadmap Rebalance 2026-06-24__scheduled

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-06-24__scheduled
Reviewed by: PMO Lead; Head of Specs Team
Date filed: 2026-06-24
Prior cycle checked: 2026-06-22__scheduled

---

## What worked well

1. **Prior cycle OAs both fully resolved.** Both carry-forward items from 2026-06-22__scheduled were closed via v6.1 delivery: PT-04 gate cleared at sprint planning (15 trades), EPIC-04 delivered all 4 stories; BLG-FE-76 and BLG-FE-78 both firm scope and shipped. No residual carry-forward from the prior rebalance cycle.

2. **STEP 8.2 operated correctly.** All 6 Now horizon items (BLG-FEAT-46–51) verified active in backlog.md. None archived. None carrying stale RA: annotations. The verification step added on STEP 8.2 (v7.6) continues to provide clean hygiene on the Now horizon.

3. **Idea hard-cap discipline applied cleanly.** 8 IW-20260619-01 ideas at their third park cycle were processed with concrete PO dispositions (4 Reject with documented rationale, 4 Backlog-gate-conditional with filed BLG items). The hard cap forced decisions that had been deferred for 3 rebalances. All 4 gate-conditional items have specific, testable gate conditions — not open-ended deferral.

4. **Product Value Ratio improving on trajectory.** 0.136 → 0.209 over two rebalance cycles. v[TBD] Now horizon contains 6 U-items (BLG-FEAT-46–51), which will drive the ratio materially higher when v[TBD] ships.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type C — Dependency Stall: A pre-condition artefact (velocity_metrics.md) was expected by the run manifest but does not exist

**Recurrence:** No — first occurrence identified at this cycle. (Prior cycle 2026-06-22__scheduled noted "velocity data exists in velocity_metrics.md" in the IDEA-pmo-lead-20260619-02 park rationale, implying the file was expected to exist.)

**What happened:**
At STEP 2.4, the Product Value Ratio computation required reading story delivery data from velocity_metrics.md. The file does not exist at claude/roadmap/velocity_metrics.md. The computation was performed manually by reading claude/cycles/*/closure_record.md and docs/product/changelog.md entry by entry, reconstructing the U/G/D classification from the 5 most recent release cycles. This approach is reliable but slow and error-prone at scale.

**Where in the routine:**
STEP 2.4 — Product Value Ratio computation

**Root cause:**
Missing artefact — velocity_metrics.md was never created. The run_manifest references it as a canonical input; the roadmap engine expects it to exist; but no governance step currently enforces its creation or updating.

**Blast radius analysis:**
- What would have propagated: Product Value Ratio computed from fallible manual reconstruction; if any cycle classification was wrong (e.g. mislabelled G as U), the ratio would be incorrect and the alert threshold decision (fire / no-fire) could be wrong
- When it would have surfaced: At a future cycle where manual reconstruction diverges from history — silent inconsistency unless audited
- Recovery cost if uncaught: Low per-cycle (easy to correct a ratio), but medium cumulative (trend data would be unreliable, undermining Product Value Alert purpose)

**Process patch:**

→ Deferred patch (cannot apply this run — requires new file creation and backfill from changelog):
  - File: `claude/roadmap/velocity_metrics.md` (new file — does not exist)
  - Section: New file — structure: table of last 10 release cycles with columns: cycle_id, release_version, U, G, D, total, delivery_rate
  - Change required: Create velocity_metrics.md with backfilled data from changelog for last 10 release cycles; add instruction to post-ship closure prompt (post_ship_closure.md) to update velocity_metrics.md as a closure step
  - Owner: PMO Lead
  - Target: next `run post-ship` closure (first opportunity to create and backfill the file within a governed write session)

---

## Recurrence Escalations

None. Friction Item 1 is a first occurrence. Prior cycle carry-forward items were both resolved. No deferred patches from 2+ cycles without a prompt_change_log entry.

---

## Process improvements actioned this run

None applied this run — Friction Item 1 requires new file creation that falls outside the roadmap rebalance write scope. Deferred to post-ship closure.

---

## New files created this run

None (velocity_metrics.md deferred to next post-ship closure).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/roadmap/velocity_metrics.md` (new) | Full file | Create with backfilled data from last 10 release cycles (U/G/D/total/delivery_rate per cycle); update post_ship_closure.md to include a velocity_metrics.md update step at closure | PMO Lead | Next `run post-ship` closure |

---

## Escalations

None.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | velocity_metrics.md does not exist; Product Value Ratio must be computed manually each rebalance | Create velocity_metrics.md and update post_ship_closure.md to add a velocity tracking step; resolves at next post-ship run | Roadmap (via Post-Ship) |
| 2 | BLG-BE-38 (P2, XS effort) — sector concentration panel shows all positions as "Unclassified" due to missing ticker_universe join; not in Now horizon | Release planning engine should consider BLG-BE-38 for v[TBD] inclusion given XS effort and direct data accuracy impact (STEP 8.0 advisory) | Release Planning |
| 3 | 8 remaining ideas (all Parked-cycle-2) — count < 20 threshold → STEP -1.6 will fire at next `run roadmap`, triggering an idea intake window | At next rebalance, idea intake will be invoked before STEP 1; ensure an idea intake window is open and participants notified | Roadmap (STEP -1.6) |
