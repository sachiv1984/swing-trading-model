**Owner:** Head of Specs Team
**Status:** Active
**Release:** v7.6
**Cycle:** 2026-07-20__release-v7.6
**Last Updated:** 2026-07-20

---

# Stage 4 Backlog Slice — v7.6

<!-- release-plan-marker: RP:v7.6:2026-07-20__release-v7.6 -->

This item is **conditional**, not firm — see `release_plan.md` RISK-01. Sprint Planning may not seal this story until `run design-gate --cycle 2026-07-20__release-v7.6` PASSes.

## EPIC-01 — PDF / print-friendly export
**Maps to:** S2-01
**Backlog source:** `BLG-FE-119`
**Sequencing:** Conditional on Design Gate PASS (RISK-01); standalone, no dependencies

### ST-01 — Add print/PDF export action to WeeklyDigest and TradePlan
**Acceptance Criteria:**
- A "Print / Export PDF" action is available on both `WeeklyDigest.js` and `TradePlan.js`
- Output is legible and correctly formatted without app chrome (nav/sidebar)

---

## EPIC-02 — Regression suite baseline update
**Maps to:** S2-02
**Backlog source:** `BLG-QA-112`
**Sequencing:** Gate-triggered companion to EPIC-01 (gate fired: `BLG-FE-119` entered release scope); no independent Design Gate dependency (documentation-only, no observable UI)

### ST-02 — Update regression suite baseline for BLG-FE-115-119 interaction surfaces
**Acceptance Criteria:**
- Regression baseline document updated with new scenario entries for the shipped item(s) (`BLG-FE-115`–`BLG-FE-118`, already shipped v7.4/v7.5, plus `BLG-FE-119` this cycle)
- Cross-referenced against the corresponding Playwright spec file(s)

---

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-20__release-v7.6",
  "phase": "Release",
  "status": "present",
  "generated_utc": "2026-07-20T16:15:00Z"
}
```
