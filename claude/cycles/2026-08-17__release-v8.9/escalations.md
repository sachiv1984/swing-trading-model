Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-17

---

## ESC-20260817-01

- **Raised at:** 2026-08-17T15:30:00Z
- **Routine:** Design Gate
- **Cycle ID:** 2026-08-17__release-v8.9
- **Step:** STEP 1 — Classify Each Item (§13 boundary pre-check for AI-calling proposals)
- **ST/EPIC item:** ST-06 (EPIC-02, BLG-FEAT-90 — Automated AI post-trade debrief)
- **Trigger type:** Strategy
- **Blocking statement:** ST-06 introduces a new AI-generated debrief synthesised from plan-vs-reality delta, red-flag journal entries, and SI-02 drift context, surfaced on the closed-trade detail view. This is a materially new use of the existing "AI thesis-generation pipeline" (Claude/Gemini), not covered by the existing `docs/specs/api_contracts/gemini_thesis_generation.md` §13 compliance note (scoped to thesis generation only, a different output shape and purpose) or by `docs/product/decisions/arc6_ps03_section13_preassessment.md` (covers PS-03 Monte Carlo simulation, an unrelated deterministic feature). No covering §13 review decision record exists for this specific proposal. Per `design_gate_prompt.md` STEP 1's mandatory §13 boundary pre-check, ST-06 cannot proceed past this gate as Design Required with design work starting immediately.
- **Owning authority:** Strategy Rules & System Intent Owner (§13 review), Product Owner (scoping the review as a delegated_decision gate story)
- **Unblock criteria:** A §13 System Boundary Review decision record for ST-06's AI post-trade debrief is produced and PASSes (or CONDITIONALLY PASSes with binding conditions), following the pattern already used for PS-03 (`arc6_ps03_section13_preassessment.md`) and the SI-01/SI-02 precedent reviews. Per `execution_prompt.md` §5.1's §13 gate story pattern (LL-v3.5-SP-01), Sprint Planning should scope this review as its own `delegated_decision` gate story ahead of any ST-06 implementation stories.
- **SLA due-by:** Before `plan sprint` is re-run for this cycle, or before ST-06 is carried into sprint scope (whichever is sooner)
- **Blocks execution:** Yes — this design gate's overall status is BLOCKED as a result (see `design_gate.md`); `sprint_planning_pre_condition` remains unmet until resolved.
- **Disposition:** Open
- **Resolution summary:** *(pending)*
