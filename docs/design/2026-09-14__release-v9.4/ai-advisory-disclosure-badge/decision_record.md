**Owner:** Head of UX & Design
**Cycle:** 2026-09-14__release-v9.4
**Story:** ST-22 (BLG-AI-05, EPIC-05)
**Status:** Approved

# Decision Record — Reusable AI-Advisory Disclosure Badge

## Context

The Dashboard's AI Daily Briefing Card (`dashboard.md` §5) already carries a bespoke "AI Advisory" badge — an amber badge (`bg-amber-700`/white text) plus non-dismissible inline text ("All actions require your confirmation") — introduced at v2.5 (`BLG-UX-01`) and colour-corrected at v3.4 (`BLG-FE-165`). `design_system.md` §Color Usage (line 54) already references this instance as an example of §13-compliance-disclosure text, but no shared component exists — the pattern lives only inline in `dashboard.md`, uncopyable by any other surface without re-deriving the wording, colour, and dismissibility rules from scratch.

## Decision

1. **Extract a reusable `AdvisoryBadge` shared component** into `design_system.md` §Shared UI Components, generalising the existing Dashboard instance verbatim (no visual change to the shipped badge):
   - Amber badge, `bg-amber-700` background / white text (light+dark identical — the compliance-disclosure surface intentionally does not vary by theme, unlike most badges)
   - Fixed label prop (e.g. `"AI Advisory"`) plus an optional inline caption prop (e.g. "All actions require your confirmation") — both required to be **non-dismissible** wherever used
   - Governs any surface displaying an AI-generated, advisory-only output alongside deterministic system output, per `strategy_rules.md` §13.1/§13.2 (human-in-the-loop, non-blocking)
   - Not a replacement for `StandingAlert` (design_system.md §Shared UI Components → Standing Alert) — `StandingAlert` is for conditions requiring sustained *user acknowledgement*; `AdvisoryBadge` is a static provenance label with no dismiss/acknowledge affordance at all.
2. **First applied instance:** the daily-briefing surface (Dashboard AI Daily Briefing Card) already conforms — no code change required there. `dashboard.md` is updated to cite the new shared component definition in place of its own inline prose, per the same generalisation pattern as `design_system.md` v1.1/v1.2 (dashboard-originated patterns later formalised as shared components).
3. Any future surface introducing a new AI-generated/advisory output (e.g. Gemini thesis generation, AI Trade Advisor) should reuse `AdvisoryBadge` rather than re-deriving badge styling — flagged as a recommendation for `design_system.md` readers, not applied retroactively to those surfaces this cycle (out of scope for ST-22).

## Evidence-method note (CLAUDE.md frontend-visible-change standard)

The badge itself is not new/changed pixels on the daily-briefing surface (same shipped markup, now named/generalised) — no new Playwright coverage or staging run is required for the *existing* instance. Per `stage4_backlog_slice.md`'s own design-gate note on ST-22, the AC is satisfied by this documentation via `design_system.md`; the "documented in a canonical frontend spec" language in the original AC now correctly points at `design_system.md` (shared component) rather than only `dashboard.md` (page-local prose).

## Rationale

Generalising an already-shipped, already-approved pattern into a shared component (rather than authoring a new one) avoids introducing a second, subtly different advisory-badge convention the next time an AI-output surface needs one — the exact failure mode `design_system.md`'s Modal Theming and Card Hierarchy sections were extracted to prevent.

## Sign-off

Head of UX & Design: Approved, 2026-09-14.
Product Owner: Approved, 2026-09-14.
