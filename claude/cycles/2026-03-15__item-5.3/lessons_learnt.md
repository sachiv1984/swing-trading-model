
**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-15

---

# Lessons Learnt — 2026-03-15__item-5.3

**Cycle:** 2026-03-15__item-5.3
**Date:** 2026-03-15

---

## Lessons From This Cycle

---

### LL-01 (this cycle) — Development environment gap must precede feature work

**Observation:** v1.9 Sprint 2 surfaced a P1 infrastructure gap: CohortAnalysis.js computed cohort data client-side (BLG-TECH-06) rather than calling the canonical endpoint. This was caught post-merge, not pre-merge, because no staging environment exists for pre-merge QA.

**Root cause:** The absence of a development/staging environment means all QA runs against production. The Director of Quality sign-off workflow — which requires testing a live application — structurally forces merge-before-test.

**Action:** BLG-OPS-01 (Development Environment) has been elevated to roadmap as a v1.10 P1 item. The next release (v1.10) must ship BLG-OPS-01 before or alongside any new features. Release planning must enforce this sequencing.

**Owner:** Infrastructure & Operations Owner + PMO Lead
**Status:** Open — deferred to v1.10 release planning
**Applies to:** All future release planning cycles — BLG-OPS-01 must enter v1.10 as Prerequisite item, not a peer feature.

---

### LL-02 (this cycle) — Idea status normalisation needed

**Observation:** The idea pool contained 12 files with stale `Status: Advancing` or `Status: Promoted` labels — ideas that were advanced to the roadmap or backlog in prior cycles but whose file status was never updated. Additionally, 30 files used the old `Status: Parked` format (without the `Parked-cycle-N` suffix required since idea_intake_prompt.md v1.2).

**Root cause:** Post-roadmap-run idea file cleanup was not enforced in prior cycles. The status update step was completed for some files but not all.

**Action (this cycle):** Bulk status correction applied in STEP 8 — stale Advancing/Promoted → Promoted-Added; old-format Parked → Parked-cycle-2.

**Deferred patch:** The `run roadmap` post-run checklist should include a verification step confirming all idea files that were debated in the current cycle have had their status updated. Roadmap engine prompt (roadmap_prompt.md STEP 8) to be updated with a verification step. Apply at next governance session.

**Owner:** Head of Specs Team
**Status:** Open — deferred to next governance session (not time-critical)

---

### LL-03 (this cycle) — v1.9 fully delivered — user value sprint model validated

**Observation:** v1.9 Sprint 2 delivered all 6 committed items: trade reflection template, compliance metrics, cohort analysis, dashboard homepage, R-multiple distribution, and test scenario library. All verified and live. This completes the v1.9 "User Value & Insight" theme across both sprints.

**Positive:** The two-sprint phased approach (Sprint 1: infrastructure; Sprint 2: user value) worked well. Separating the Risk Dashboard fixes and test infrastructure into Sprint 1 gave Sprint 2 a clean focus on user-facing features.

**Action:** Carry the two-sprint phase model forward as the preferred approach when a release mix includes both infrastructure and user-facing work. Document in next release planning as the default structure.

**Owner:** PMO Lead
**Status:** Note only — no action required

---

## Prior Cycle Deferred Lessons Status

All 5 deferred patches from 2026-03-06__item-3.4 lessons_learnt.md were confirmed applied (AUD-2026-03-13 audit session 2026-03-15). No OVERDUE items carried forward to this cycle.

---

## Deferred Patches (for next governance session)

| Patch | Description | Prompt file | Owner | Priority |
|-------|------------|-------------|-------|----------|
| LL-02-patch | Add idea file status verification step to STEP 8 post-run checklist | roadmap_prompt.md | Head of Specs Team | Low |
