**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.4
**Cycle:** 2026-05-14__release-v3.4
**Published:** 2026-05-14

---

# Lessons Learnt — Release Planning v3.4

## Planning Observations

### R-01 — Carry-forward items acted upon in planning
All three v3.4-targeted carry-forward items from LL-v3.3 were directly addressed in this release plan:
- Item 1 (frontend front-loading): EPIC-03 assigned Sprint 1; EPIC-01 dedicated Arc 3 frontend.
- Item 2 (merge order discipline): Documented in decisions record; flagged for execution_state.json at sprint execution STEP 3.
- Item 3 (QA branch advisory): Noted for sprint execution team.

**Action:** None — process working as intended. The carry-forward mechanism is effective.

### R-02 — Design gate dependency on EPIC-02 (IT-04/05)
IT-04 and IT-05 are new Arc 3 features with no prior UX specs. This creates a hard sequencing dependency: design gate (Phase 1.5) must run before EPIC-02 stories can be sprint-planned. RISK-01 is High priority and appears in the Pre-sprint Required Decisions checklist.

**Action:** Deferred to design gate phase — design gate must produce IT-04/05 UX specs.

### R-03 — BLG-FE-22 aged 2 cycles without story assignment
BLG-FE-22 (Screener morning routine UX spec) was Provisional-Target v3.2 (missed), carried to v3.4. The §1.1 age advisory correctly fired. Item is now assigned as ST-12 in this release.

**Action:** Resolved — ST-12 EPIC-04.

### R-04 — Capacity WARN with risk buffer
Estimated effort (11 days) at upper end of capacity (~10–13 days). However, EPIC-02 (Sprint 2) can slip to v3.5 if EPIC-01 and EPIC-03 are complete — Arc 3 frontend and quick wins have independent value. This built-in risk buffer is appropriate given the WARN verdict.

**Action:** None — phasing recommendation in release_plan.md documents the buffer.

## Carry-Forward (for next cycle)

| # | Description | Target | Owner |
|---|-------------|--------|-------|
| 1 | LL-v3.3 item 4: Priority discrepancy — sprint_close "Deviations Filed" table priority must match DoQ assessment | v3.5 | Head of Specs Team |
| 2 | LL-v3.3 item 5: Protocol checkbox verification — sprint_close check for "backlog item filed" completeness | v3.5 | PMO Lead |

---

```json
// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-05-14__release-v3.4",
  "release": "v3.4",
  "status": "Published",
  "artefacts": {
    "run_manifest": "present",
    "state_json": "present",
    "release_plan": "present",
    "scope_document": "present",
    "decisions_record": "present",
    "stage4_backlog_slice": "present",
    "stage4_issue_manifest": "present",
    "cycle_summary": "present",
    "lessons_learnt": "present"
  },
  "publish_gate": "passed",
  "generated_utc": "2026-05-14T00:42:00Z"
}
```
