# Lessons Learnt — Rebalance Cycle 2026-04-05__scheduled

**Cycle ID:** 2026-04-05__scheduled
**Date:** 2026-04-05
**Tier:** Standard

---

## Friction Items

### Friction Item 1 — velocity_metrics.md not updated at post-ship closure

**What happened:** The v2.4 post-ship closure (2026-04-04) did not include `docs/product/velocity_metrics.md` in its write scope. As a result, the v2.4 row in that file shows "In progress" at the time of this rebalance, even though v2.4 shipped and was verified on 2026-04-03.

**Impact:** Causes stale data visible to anyone reading velocity_metrics.md; creates an inaccurate picture of delivery state. Not a blocker for this rebalance, but represents a systemic gap.

**Root cause:** The post_ship_closure.md prompt write scope list does not explicitly include `velocity_metrics.md`. The post-ship closure completes after verification, at which point the velocity row should be updated from "In progress" to the verified velocity figure.

**Recommended fix:** Add `docs/product/velocity_metrics.md` to the write scope of `claude/system/post_ship_closure.md`. The post-ship closure should update the current release row with: actual velocity (stories completed / stories planned), verification status, and actual ship date.

**Action:** Raise as a prompt patch at the next roadmap rebalance or when v2.5 planning opens. Flag in CF carry-forward.

---

## Confirmations (approaches that worked well)

### Confirmation 1 — Bulk sed for ideas register cycle-N increments

Using `sed -i 's/| Parked-cycle-3 | 3 |/| Parked-cycle-4 | 4 |/g'` after individually editing the special rows (advancing, rejecting) prevented the bulk update from accidentally touching the wrong rows. This sequencing (special edits first, bulk sed second) is the correct approach for ideas register cycle updates.

### Confirmation 2 — Zero-sum displacement at backlog level

When ideas advance to backlog level (not roadmap initiative level), zero-sum is satisfied by naming displaced/deprioritised backlog items — not by counting idea kills vs advances. Roadmap net-zero (0 adds, 0 kills) is a separate check. This interpretation was applied consistently with cycle 2026-03-31__scheduled.

---

## Carry-Forward Advisories

| ID | Advisory | Status |
|----|---------|--------|
| CF-1 | Sprint planning governance hygiene (v2.4 closure carry-forward) | Open — applies at v2.5 sprint planning |
| CF-2 | delivery_verification_prompt.md patch — v2.5 release planning note | Open — apply before v2.5 release planning |
| CF-3 | trade_history.md DEV-ST14-01 | RESOLVED 2026-04-04 |
| CF-4 (new) | velocity_metrics.md write scope gap in post_ship_closure.md | Open — patch at v2.5 post-ship or sooner |
