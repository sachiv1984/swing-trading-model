Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Release: v4.1
Cycle: 2026-05-26__release-v4.1 (Release Planning phase)
Last Updated: 2026-05-26

---

# Lessons Learnt — Release Planning — 2026-05-26__release-v4.1

---

## Release Planning Observations

### Observation 1 — Carry-Forward OA Items Driving Story Structure

**What happened:** All 4 carry-forward OA items from v4.0 post-ship closure were directly incorporated as sprint stories (OA-01 → ST-01, OA-02 → ST-02, OA-04 → ST-03, OA-07 → ST-15 partial). OA-03 (sprint_close_reminder.yml investigation) became a task AC within ST-01 rather than a standalone story — appropriate given it's an investigation, not an implementation.

**Why it matters:** Having OA items map cleanly to stories reduces the risk of OA items being "noted but not actioned." The mapping is explicit in the backlog slice.

**Action type:** Observation (positive pattern — retain)

---

### Observation 2 — Overdue Spec Debt (BLG-SPEC-33/34 missed v4.0 target)

**What happened:** BLG-SPEC-33 and BLG-SPEC-34 had Provisional-Target v4.0 but were not included in the v4.0 sprint — they were noted as rebalance adds in the v4.0 cycle, not as stories. The backlog age advisory at STEP 1.1 correctly flagged these as 2+ cycles without story assignment.

**Why it matters:** Spec debt items accumulating across cycles without story assignment is a drift pattern. The backlog age advisory (STEP 1.1) is working as designed.

**Action:** None required — items promoted to Sprint 1 stories (ST-04, ST-05). Pattern to watch in future cycles.

---

### Observation 3 — Capacity WARN with Sprint 2 Imbalance

**What happened:** Sprint 1 is well within capacity (~6 days); Sprint 2 is estimated at ~17 days against ~8–10 days available. The Sprint 2 imbalance is partly due to bundling SI-02 pre-planning, feature integration, and staging verification into one sprint.

**Why it matters:** The phasing recommendation in the capacity check section makes Sprint 2 imbalance explicit and actionable at sprint planning. Sprint planning should either defer ST-09 (M effort, cost alerting) or ST-11 (staging bundle — verifications only) to v4.2 if capacity is tight.

**Action type:** Deferred to sprint planning — phasing recommendation included in release_plan.md §Capacity Check.

---

## Carry-Forward to Sprint Execution

*(No carry-forward items from this release planning run — all items actioned as stories or advisory notes.)*

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-05-26__release-v4.1",
  "status": "Published",
  "lessons_recorded": 3,
  "action_items": 0,
  "carry_forward_items": 0,
  "generated_utc": "2026-05-26T00:20:00Z"
}
