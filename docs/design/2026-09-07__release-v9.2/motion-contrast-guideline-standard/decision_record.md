**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-07__release-v9.2
**Story:** ST-05 (EPIC-02, BLG-SPEC-134)

# Decision Record — Motion-vs-Contrast Guideline Standard (Entrance Fade-In Animations)

## 1. Problem

`design_system.md` documents WCAG-AA text-contrast tokens (§Color Usage) and several `DataState`/interaction-timing patterns (loading skeletons, error copy, empty-state microcopy) but has no explicit guideline for the specific trade-off that occurs during an entrance fade-in: a text element's opacity ramps from 0→1 over the animation's duration, so for a portion of that window the element is on-screen at a contrast ratio below its resting-state value even though the resting value passes WCAG-AA. No prior instance in this codebase has been flagged as a defect, but the gap itself — no documented guideline either way — is what BLG-SPEC-134 asks to close. Per §6's motion/timing-sensitive-interactions rule (BLG-FE-131), this class of item is always Design Required, regardless of whether it ends up changing an actual shipped animation.

## 2. Decision (standard fixed at gate; content authored during execution)

Mirroring the `2026-07-24__release-v7.8` ST-03/ST-04 pattern (accessibility-audit standard-setting, findings/content produced during sprint execution): this record fixes the **scope and disposition rule** for the guideline, not its final prose — the guideline text itself is ST-05's own execution deliverable.

**Scope:** the guideline must cover, at minimum:
- Whether a minimum ramp-hold threshold applies (e.g. contrast only needs to clear WCAG-AA once the element reaches some minimum opacity, not from 0%) — WCAG 2.x's success criteria are commonly read as applying to the resting/final state of a transient effect, not every intermediate frame; the guideline should state this explicitly rather than leave it implicit.
- Whether any existing shipped animation duration/easing is long enough for a mid-fade frame to be plausibly read by a user (very short entrance fades are unlikely to register as a distinct low-contrast state at all) — a duration-based cutoff rather than a blanket rule.
- Applies to text elements only (per BLG-SPEC-134's scope); non-text decorative fades are out of scope.

**Disposition rule:** if the audit-during-execution finds the guideline is unnecessary (e.g. all current entrance animations are short enough, or already gated by a `prefers-reduced-motion` check that removes the fade entirely), record that explicit no-guideline-needed decision with rationale in `design_system.md` directly — per the story's own AC, either outcome (guideline added, or explicit decision that none is needed) satisfies the story; this record does not pre-judge which.

## 3. §13 Compliance

Documentation/guideline-authoring only; no AI-provider call introduced or extended. §13 boundary pre-check (STEP 1) does not apply.

## 4. Frontend Spec Impact

`design_system.md` (current: v1.11) gains either a new subsection under §Accessibility or an explicit no-guideline-needed note, version-bumped during sprint execution in the same commit as the content, per `CLAUDE.md` §6.

## 5. Approval

Head of UX & Design: confirmed, 2026-09-07.
Product Owner: confirmed, 2026-09-07.
