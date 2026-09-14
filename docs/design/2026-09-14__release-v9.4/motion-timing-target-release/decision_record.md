**Owner:** Head of UX & Design
**Cycle:** 2026-09-14__release-v9.4
**Story:** ST-13 (BLG-SPEC-136, EPIC-04)
**Status:** Approved

# Decision Record — Motion-Vs-Contrast Ceiling: Target Release for the 4 Known Non-Compliant Components

## Context

`design_system.md` v1.12 (ST-05, v9.2) already documents the motion-vs-contrast guideline's 500ms combined `delay + duration` ceiling and already lists the 4 non-compliant components, split into two failure modes:

- **Unbounded/user-editable index-scaled stagger:** `src/pages/SystemStatus.js`, `src/pages/Signals.js`
- **Fixed stagger values already at/over the ceiling:** `src/pages/Reports.js`, `src/components/dashboard/widgets/RecentTradesWidget.js`

v1.12 filed the remediation as `BLG-SPEC-136` (this story) but did not assign a target release — the gap this decision closes.

## Decision

1. **Target release: v9.5** (next scheduled release) for bringing all 4 components into compliance. No component ships an app-wide animation audit or code change this cycle (ST-13 is spec-only, Effort XS) — this decision fixes the standard and the deadline, matching the `2026-08-05__release-v8.3`/`2026-07-24__release-v7.8` audit-standard-setting precedent (standard set at one gate, applied at a later one).
2. **Remediation approach per failure mode**, for the v9.5 implementer to follow without re-deriving:
   - **Fixed-value components (`Reports.js`, `RecentTradesWidget.js`):** reduce the max per-item `delay` so that `max(delay) + duration ≤ 500ms`. With Framer Motion's default tween (~0.3s), this caps max delay at ≤0.2s — both components' current max (`0.2s`) sits exactly at the edge combined with ~0.3s duration; an explicit shorter duration (e.g. `duration: 0.2`) is an acceptable alternative to reducing delay further, as long as the combined total is verified ≤500ms, not assumed.
   - **Unbounded/user-editable components (`SystemStatus.js`, `Signals.js`):** introduce a fixed stagger cap independent of the underlying list length or user-editable bound (e.g. `delay: Math.min(index, N) * step` with `N` chosen so `N * step + duration ≤ 500ms`) rather than removing staggering — preserves the visual effect for short lists while bounding the worst case for long ones. `Signals.js`'s `topN` remaining user-editable with no `max` is not itself a defect; only its use as an unbounded multiplier into `delay` is.
3. Each component's fix must be verified against its **own** current `duration` value (not assumed at Framer Motion's ~0.3–0.5s default) before being marked compliant — remove it from `design_system.md`'s known-non-compliant list only in the same commit that brings it into line, per the list's own existing convention (v1.12, line 320).
4. A single consolidated backlog item should track the actual v9.5 implementation across all 4 components — ST-13 itself does not implement. Filing it is a Product Owner/PMO Lead action outside this gate's write scope (§5 — this engine may not write to backlog documents); recorded as a follow-up in `design_gate.md`'s Notes section.

## Rationale

Splits a single "fix later" placeholder into an assignable, verifiable target with per-component guidance, so v9.5 sprint planning can pull `BLG-FE-176` in as a scoped, estimable item rather than re-investigating the mechanism from scratch.

## Sign-off

Head of UX & Design: Approved, 2026-09-14.
Product Owner: Approved, 2026-09-14.
