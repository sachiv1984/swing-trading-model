**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v2.6
**Cycle:** 2026-04-11__release-v2.6
**Last Updated:** 2026-04-11

---

# Lessons Learnt — Release Planning v2.6

## What Worked Well

- **Carry-forward items from v2.5 cleanly mapped to scope:** Both CF-1 and CF-2 from the v2.5 lessons_learnt_closure.md carry-forward were included as EPIC-04 stories (ST-12 and ST-13). The carry-forward mechanism correctly surfaced unresolved action items for this planning cycle.
- **Design dependencies identified early:** STEP 1 §1.3 design-gate language scan correctly flagged BLG-FE-11/12/13 as requiring Head of UX decisions before implementation. Pre-sprint required decisions checklist surfaced in cycle_summary.md — Sprint Planning Engine will consume this at STEP -1.
- **Backlog grooming paid off:** 10 provisional targets updated to v2.6 during post-ship closure backlog groom made scope extraction straightforward. Backlog was in a clean state entering planning.
- **AUD-2026-04-11-009 (§1.3 design-gate scan) contributed immediately:** The new design-gate language scan rule (added to release_planning_prompt.md v2.26 per audit item) correctly caught 3 UX-gated items in this first run after the patch.

## Friction Log

### Friction Item 1

**Classification:** Type C — Minor Process Observation: v2.6 roadmap section has no theme/description pre-defined.

**What happened:** current_roadmap.md §1 shows "Next planned release: v2.6 (TBD)" — no theme or feature description defined before planning. This is expected at this stage (manage_roadmap runs before planning; themes are defined at planning time), but it means the release theme is entirely derived from the backlog at planning time rather than from a pre-defined roadmap entry.

**Impact:** None — PO decision authority covers scope selection. Backlog Provisional-Target fields provided enough signal. No hard gate impact.

**Process observation:** Consider whether the manage_roadmap routine should carry forward a tentative theme stub for the next release based on the top-priority backlog items. Not urgent — current process works.

**Action:** No action now. Noted for future consideration.

---

## Outstanding Actions

None.

---

// ARTEFACT_STATUS
```json
{
  "phase": "Release",
  "cycle_id": "2026-04-11__release-v2.6",
  "release": "v2.6",
  "status": "Published",
  "artefacts": {
    "run_manifest": "present",
    "release_plan": "present",
    "scope_document": "present",
    "decisions_record": "present",
    "stage4_backlog_slice": "present",
    "stage4_issue_manifest": "present",
    "cycle_summary": "present",
    "lessons_learnt": "present"
  },
  "open_escalations": 0,
  "deferred_execution_blockers": 0,
  "capacity_check": "pass",
  "stories": 15,
  "epics": 4
}
```
