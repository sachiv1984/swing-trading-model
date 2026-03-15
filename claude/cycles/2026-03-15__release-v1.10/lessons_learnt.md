**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-15

---

# Lessons Learnt — 2026-03-15__release-v1.10

**Cycle:** 2026-03-15__release-v1.10
**Date:** 2026-03-15
**Phase:** Release Planning

---

## Lessons From This Cycle

---

### LL-01 (this cycle) — No mandatory staging approach decision before sprint planning

**Observation:** RISK-01 (staging environment scope ambiguity) requires a pre-sprint decision from the Infrastructure & Operations Owner on the hosting approach (cloud service vs same-host isolation). This decision gate is not currently enforced by the sprint planning engine preflight.

**Root cause:** The release planning engine records the risk but does not create a formal pre-sprint decision checkpoint that the sprint planning engine will verify at its preflight.

**Action:** Sprint Planning preflight should consume the `## Pre-sprint Planning Required Decisions` section from `cycle_summary.md`. For v1.10, the sprint planning session must confirm the staging approach decision is documented before sealing the sprint backlog.

**Owner:** Infrastructure & Operations Owner
**Status:** Open — to be resolved at sprint planning session (before sprint backlog seals)

---

### LL-02 (this cycle) — Backlog orphan item aged 3 cycles — STEP 1.1 advisory working as intended

**Observation:** TEST-GAP-EPIC-06 had been in the backlog for 3 release cycles (v1.7, v1.8, v1.9) without a story assignment. STEP 1.1 (Backlog Age Advisory, LL-v1.9-01) correctly flagged this item and recommended promotion to a sprint story. Item promoted to ST-07 (BLG-QA-01) in this release.

**Positive:** The LL-v1.9-01 improvement (STEP 1.1 advisory) caught a long-stale orphan item at planning time. No further action required — the advisory mechanism worked.

**Owner:** PMO Lead
**Status:** Note only — no action required

---

## Prior Cycle Deferred Lessons Status

**Deferred patches from 2026-03-15__item-5.3 (lessons_learnt.md):**
- LL-02-patch: Add idea file status verification step to roadmap_prompt.md STEP 8. Status: Open — not applied this cycle. Carry forward to next governance session.

---

## Deferred Patches (for next governance session)

| Patch | Description | Prompt file | Owner | Priority |
|-------|------------|-------------|-------|----------|
| LL-02-patch | Add idea file status verification step to STEP 8 post-run checklist | roadmap_prompt.md | Head of Specs Team | Low |

---

// ARTEFACT_STATUS
```json
{
  "phase": "Release",
  "cycle_id": "2026-03-15__release-v1.10",
  "release": "v1.10",
  "status": "Published",
  "artefacts_complete": true,
  "open_lessons": ["LL-01"],
  "deferred_patches": ["LL-02-patch"],
  "filed_utc": "2026-03-15T00:00:00Z"
}
```
