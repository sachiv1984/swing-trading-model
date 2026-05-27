**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-27__release-v4.2
**Phase:** Release

---

# Lessons Learnt — Release Planning v4.2

## Observations

### Roadmap Section Gap (Process Gap — Minor)

**Observation:** The Extended-tier "no-change" rebalance (2026-05-27__scheduled) left the roadmap with "Next planned release: [TBD]" rather than adding a formal v4.2 planned release section. This triggered the STEP -1.2 hard gate when `plan release v4.2` was invoked, requiring manual Product Owner authority to add the v4.2 section before planning could proceed.

**Root cause:** The rebalance explicitly recorded "No roadmap-level changes this cycle" (cycle_record.md §8.1). The rebalance engine has no obligation to create the next release section when there are no scope changes — but this creates a planning dependency gap.

**Action:** advisory — roadmap_prompt.md could include an advisory at STEP 8.1 when the Now horizon is empty: "Now horizon is empty. If a next release is intended, Product Owner should add a planned release section to current_roadmap.md at this time, or release planning will require manual entry at STEP -1.2." This is a convenience improvement, not a hard process gap.

**Classification:** type D (process friction — known, documented, advisory action)
**Action disposition:** deferred — advisory only; add to backlog if pattern recurs

### BLG-GOV-58 Pre-Resolved

**Observation:** BLG-GOV-58 (execution_prompt.md STEP 5.2 clarification) was carried in the backlog as `Provisional-Target: v4.2 sprint seal` but was resolved by AUD-2026-05-27-003 / execution_prompt.md v3.29 before this release planning run commenced. The carry-forward in lessons_learnt_closure.md was already noted as "resolved" but the backlog item was not yet marked COMPLETE.

**Action:** Mark BLG-GOV-58 COMPLETE at next `groom backlog` run.
**Classification:** type E (positive — audit cycle resolved a carry-forward early)
**Action disposition:** action-now (advisory note only — no document edit required)

## Action Summary

| Classification | Count |
|----------------|-------|
| type D (deferred advisory) | 1 |
| type E (positive observation) | 1 |
| Immediate actions | 0 |

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-05-27__release-v4.2",
  "status": "complete",
  "items_total": 2,
  "items_immediate": 0,
  "items_deferred": 1,
  "items_positive": 1
}
