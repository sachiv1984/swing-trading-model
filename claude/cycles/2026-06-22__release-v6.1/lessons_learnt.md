Owner: PMO Lead
Class: Governance Record (Class 3)
Status: Draft — to be finalised at post-ship closure
Release: v6.1
Cycle: 2026-06-22__release-v6.1
Last Updated: 2026-06-22

---

# Lessons Learnt — v6.1 Governance Correctness, CI Quality & User Value Foundation

*Status: Seeded at release planning. To be completed at post-ship closure (run post-ship).*

---

## Planning-Phase Observations

### LP-01: Within-Sprint Date Gate Classification (STEP 1.4b) Working Correctly

BLG-FEAT-25/PT-04 gate clearing estimate (~2026-07-02) correctly triggered mandatory conditional classification under STEP 1.4b. No manual override was required. The rule is functioning as designed.

**Action:** None — monitor at sprint planning to confirm gate check is enforced at preflight once ST-02 (GOV-133) is shipped.

---

### LP-02: Carry-Forward Loop Risk for PT-04 Remains Elevated

PT-04 (BLG-FEAT-25) has been deferred 8+ consecutive cycles. Despite the accelerating trade trajectory (~7 new closed trades in 7 days to 2026-06-16), the gate has not yet cleared. The trade gate proximity indicator (ST-07, BLG-FE-78) should surface the count directly on the dashboard, reducing the friction of gate monitoring between cycles.

**Action at post-ship:** If PT-04 gate clears and EPIC-04 ships, close the carry-forward loop in the closure record. If gate does not clear (9th deferral), escalate to Product Owner for disposition reassessment — active disposition was set in v6.0 and must be re-confirmed by v6.2 planning.

---

### LP-03: Design Gate Sequencing — Confirmed Governance Gap Closed by This Release

v6.0 required a manual halt and state restoration because sprint planning started without design gate sign-off (design_gate_status=not_started, no bypass). This release (v6.1) includes the Correctness Fast-Track items (ST-01: GOV-132, ST-02: GOV-133) that close this gap systematically. Once EPIC-01 ships, future cycles with UI-facing scope will automatically detect design gate requirement at release planning and enforce the hard gate at sprint planning.

**Action at post-ship:** Confirm ST-01 and ST-02 ACs are met and the gap is closed. If any sprint planning in v6.1 runs before EPIC-01 is complete, note it in QA evidence.

---

### LP-04: Capacity Warn — Phasing Advisory Issued

Firm scope (~17 hrs) fits a single sprint but the phasing recommendation flags that the Skill-Silo ceiling (40% G+D+P) constrains how EPIC-01 (all G stories) and EPIC-02 (D stories) can be batched. Sprint planning is authoritative — this is seeded here as a planning-phase observation.

**Action at post-ship:** Record actual sprint phasing chosen and whether ceiling was respected.

---

## Sprint Planning Scope Intent (Pre-Sprint Note)

### SP-01: PO-directed scope additions for sprint planning

**Date noted:** 2026-06-22

Product Owner has directed that the following two items be included in the v6.1 sprint at sprint planning time, via explicit PO scope addition (not amendment cycle — routine scope change, not emergency):

| BLG ID | Title | Effort | Type | Notes |
|--------|-------|--------|------|-------|
| BLG-GOV-134 | CI: inline OpenAPI drift detection for api_performance_baseline.md | S (~0.5 day) | G | Advisory CI step; non-blocking |
| BLG-QA-62 | Playwright spec auto-registration via glob pattern | S (<0.5 day) | D | Root-cause fix for BLG-QA-60 class of bug |

These were deferred at release planning (scope-lock rule — not in rebalance Now section). PO confirmed intent to include them at sprint planning on 2026-06-22. Sprint planning engine must treat these as PO-directed additions at preflight. Story IDs ST-10 (BLG-GOV-134) and ST-11 (BLG-QA-62) are reserved for sprint planning to assign.

**Capacity note:** Both items are S/XS effort (~1 day combined). Firm scope is currently ~17 hrs; addition brings firm total to ~18 hrs — still within single-sprint range. Skill-Silo ceiling impact: +1G +1D against existing 3G+2D = 4G+3D out of 9 firm stories = 77.8% G+D before U stories — sprint planning must phase accordingly.

---

## Deferred to Post-Ship

The following observations require delivery data before they can be completed:

| Item | Notes |
|------|-------|
| Delivery accuracy | Did all firm stories ship? Were any conditionals included? |
| Sprint phasing | Was the Skill-Silo ceiling respected? Was two-sprint phasing needed? |
| Design gate outcome | Did design gate pass cleanly? Were BLG-FE-76 and BLG-FE-78 design decisions resolved without rework? |
| PT-04 gate outcome | Did gate clear by sprint planning? Was EPIC-04 executed or re-deferred? |
| EPIC-01 prompt patches | Were all §6 checklist steps completed in same commit for each prompt edit? |
| GOV-131 proposal | Was the governance overhead ceiling proposal produced and reviewed? |
