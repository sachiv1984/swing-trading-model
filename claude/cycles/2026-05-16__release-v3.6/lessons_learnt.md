Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Release: v3.6
Cycle: 2026-05-16__release-v3.6
Last Updated: 2026-05-16

---

# Lessons Learnt — Release Planning v3.6

## Planning Phase Observations

1. **Arc 4 data accumulation gap identified early:** The planned_entry_price snapshot gap was caught at release planning scope extraction rather than mid-sprint. Surfacing deferred Arc 4 items explicitly in the scope document at planning time (rather than leaving them in lessons learnt) enabled direct resolution in the first sprint. Carry-forward item from v3.5 LL #1 (Release Planning engine) worked as intended.

2. **PT-04 gate requires explicit PO confirmation:** The "20+ closed trades" gate for PT-04 cannot be verified by the engine. Modeling this as a Sprint 1 delegated_decision story (ST-03) is the correct pattern — same approach proved effective for IT-06 §13 review in v3.5. Pattern now formalised in scope as EPIC-04 governance patch.

3. **Aged backlog items promote well as a bundle:** BLG-FE-32, TEST-GAP-EPIC-03-v33, BLG-SPEC-27, and BLG-FE-26 were all 2–3 cycles deferred. Bundling into EPIC-03 (S2-03) with shared sprint-1 timing gives each item a clear landing without inflating story count. Backlog age advisory (STEP 1.1) effectively surfaced these.

4. **Prompt version change log gaps: 4 unrecorded versions (OA-RP-01–04):** v3.5 sprint execution bumped sprint_planning_prompt, execution_prompt, delivery_verification_prompt, and backlog_management_prompt but did not add prompt_change_log.md entries. This gap was caught by STEP -1.7 advisory. Direct remediation: bundled into ST-09 AC-04. The advisory scan is working; the simultaneity rule (§11 of shared_standards.md) should be reinforced in the execution_prompt.md governance patch (ST-09).

5. **scored_initiatives.md staleness (8+ cycles):** Arc 3/4 features absent from the file. All STEP 4.5 effort estimates fell to Tier 3 (inline estimates). Advisory OA-RP-05 filed. The file needs a refresh before the next roadmap rebalance. Roadmap engine carry-forward item (v3.5 LL #5) still open.

## Process Notes

- Release plan completed in standard mode — no escalations raised, no hard gates fired.
- Publish gate PASS on first attempt — cleanest release planning run in recent cycles.
- EPIC-02 is explicitly conditional (RISK-02 gate); Sprint Planning must check gate before sealing.
- Design gate required for ST-02, ST-05, ST-08.

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-05-16__release-v3.6",
  "release": "v3.6",
  "status": "complete",
  "generated_utc": "2026-05-16T00:32:00Z",
  "scope_items": 4,
  "epics": 4,
  "stories": 10,
  "escalations_raised": 0,
  "capacity_outcome": "warn",
  "publish_gate": "pass"
}
