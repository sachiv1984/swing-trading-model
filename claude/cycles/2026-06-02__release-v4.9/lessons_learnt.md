**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v4.9
**Cycle:** 2026-06-02__release-v4.9
**Filed:** 2026-06-02

---

# Lessons Learnt — Release Planning v4.9

## Positive Observations

**LL-RP-v4.9-P1 — Carry-forward integration improving**
The v4.8 carry-forward items were both actioned correctly at STEP 1 without any friction. SI-05 Phase 1 gate proximity was confirmed via the STEP 1.4 gate scan. SI-02 monitor was correctly noted as background-only. The carry-forward mechanism is functioning as designed.

**LL-RP-v4.9-P2 — Backlog items are well-specified**
BLG-OPS-49, BLG-OPS-50, BLG-QA-40, BLG-QA-41 all had clear scope and acceptance criteria documented in the backlog. Scope extraction to stories was straightforward with no ambiguity. P1 security item (npm CVEs) provides clear sprint entry point.

## Friction Items

**LL-RP-v4.9-01 — BLG-GOV-74 Provisional-Target mismatch**
BLG-GOV-74 (AI quarterly review) was tagged Provisional-Target: v4.9 but has a gate date of 2026-08-29 — clearly incompatible with v4.9 shipping in June 2026. This required explicit exclusion with explanation. Recommendation: when adding backlog items with future gate dates, Provisional-Target should be set to "Unscheduled" or the actual target release rather than the next planned release.

*Classification:* advisory / action-deferred
*Action:* PMO Lead to update BLG-GOV-74 Provisional-Target from v4.9 to "v4.10 or first cycle after 2026-08-29" — can be done as a standalone backlog edit.

**LL-RP-v4.9-02 — Prompt change log gap advisory (recurring)**
4 prompts (execution_prompt.md v3.35, release_planning_prompt.md v2.33, post_ship_closure.md v2.12, roadmap_prompt.md v6.7) have versions not confirmed in prompt_change_log.md via grep. This advisory has appeared in prior cycles. If these entries genuinely exist but were not found by grep (due to file length), the advisory is a false positive. If entries are missing, this is a compliance gap. Recommend a targeted audit.

*Classification:* advisory / action-deferred
*Action:* Head of Specs Team to verify change log completeness for the 4 affected prompts. File BLG-GOV item if genuine gap found.

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-06-02__release-v4.9",
  "release": "v4.9",
  "status": "complete",
  "generated_utc": "2026-06-02T11:20:00Z"
}
