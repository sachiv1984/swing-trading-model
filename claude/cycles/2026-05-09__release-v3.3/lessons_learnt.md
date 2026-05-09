**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Published
**Release:** v3.3
**Cycle:** 2026-05-09__release-v3.3
**Published:** 2026-05-09

---

# Release Planning Lessons Learnt — v3.3 Arc 3 In-Trade Risk Management

## Planning Session Observations

### R-01 — Arc 3 scope boundary discipline

**Observation:** Six Arc 3 items (IT-01 through IT-06) were reviewed. IT-01/02/03 selected for v3.3; IT-04/05 deferred to v3.4; IT-06 deferred (§13 gate). This boundary required explicit sequencing rationale and scope decisions — without which all 6 items might have been included, creating an over-loaded release.

**Action:** none — decision process worked correctly. Monitor at v3.4 planning to ensure IT-04/05 enter scope promptly (avoid consecutive deferral pattern).

**Owner:** PMO Lead
**action:** monitor

---

### R-02 — "Before sprint planning" backlog items are reliably in scope

**Observation:** 6 items marked `Provisional-Target: Before v3.3 sprint planning` were all included in EPIC-03 Sprint 1. This is the second cycle where this pattern works as intended (v3.2 also had "before sprint planning" items in EPIC-03). The pattern is stable.

**Action:** none — the design gate scan (OA-05 / EPIC-04 ST-14) will formally enforce this going forward.

**Owner:** Head of Specs Team
**action:** none

---

### R-03 — BLG-FEAT-13 mandatory deferral resolved by roadmap annotation

**Observation:** BLG-FEAT-13 (feature flag rollout) has been deferred from v3.0, v3.1, v3.2, and is now mandatory in v3.3. The roadmap annotation "mandatory for v3.3" provided unambiguous authority for inclusion. However, the backlog item's `Provisional-Target` field still reads "v3.2" (not yet updated). The backlog item should be updated at post-ship closure to reflect the final state.

**Action:** At post-ship closure, update BLG-FEAT-13 `Provisional-Target` to `v3.3 — COMPLETE` after ship.

**Owner:** PMO Lead
**action:** deferred-to-post-ship

---

## ARTEFACT_STATUS
```json
{
  "phase": "Release",
  "cycle_id": "2026-05-09__release-v3.3",
  "release": "v3.3",
  "items": [
    {"id": "R-01", "action": "monitor", "owner": "PMO Lead"},
    {"id": "R-02", "action": "none", "owner": "Head of Specs Team"},
    {"id": "R-03", "action": "deferred-to-post-ship", "owner": "PMO Lead"}
  ]
}
```
