**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-15
**Story:** ST-04 (BLG-SPEC-90, EPIC-03, v7.2)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# BLG-FE-110/111 Pre-Implementation Spec & Instrumentation Pass

## 1. Purpose

Close every pre-implementation information gap for `ST-05` (Dashboard empty/first-run state coverage, `BLG-FE-110`) and `ST-06` (Dashboard briefing visual hierarchy, `BLG-FE-111`) before they enter sprint planning.

## 2. AC-01 — `DataState` Empty-State Pattern Formalised

Done. See `docs/specs/frontend/design_system.md` §Shared UI Components → Cards → Data States (v1.1) and `docs/specs/frontend/base44_prompt_template_library.md` §2. Both generalise the compact-variant pattern from `docs/design/2026-07-15__release-v7.2/dashboard-empty-states/ux_spec.md` (already approved for `ST-05`) so the pattern is discoverable and reusable beyond this one story.

## 3. AC-02 — Primary vs Secondary Card Treatment Defined

Done. See `docs/specs/frontend/design_system.md` §Shared UI Components → Cards → Card Hierarchy (v1.1) and `base44_prompt_template_library.md` §3. Generalises the panel/label treatment from `docs/design/2026-07-15__release-v7.2/dashboard-briefing-hierarchy/ux_spec.md` (already approved for `ST-06`).

## 4. AC-03 — Basic View/Interaction Instrumentation

**Finding: no frontend event-instrumentation utility exists anywhere in the codebase today** (`grep` across `src/` for `trackEvent`/`analytics.track`/`logEvent`/`posthog`/`dataLayer` returns zero hits; `api.analytics.*` in `base44Client.js` is exclusively backend trading-analytics — cohort, R-multiple, compliance metrics — unrelated to UI event tracking). This is a from-scratch specification, not an extension of an existing pattern.

**Scope decision:** per `sprint_backlog.md`'s own framing of this item ("documentation/spec pass, no UI to verify visually", `Staging-only ACs: None`) and its consistency with `ST-02`'s identical "readiness pass" structure, this AC is satisfied by **specifying** the instrumentation to be added, not by writing the tracking code into `DashboardHome.js` in this story. Writing actual instrumentation code into `src/pages/DashboardHome.js` here would also disqualify `EPIC-03` from the autonomous DoQ sign-off class (`execution_prompt.md §3.2.A` Criterion 3 / BLG-GOV-135 — any file under `src/pages/**` touched, regardless of visual impact, disqualifies it), which is inconsistent with this EPIC's `sprint_backlog.md`-recorded `Staging-only ACs: None` characterisation. The specification below is scoped for `ST-05`/`ST-06` (or a dedicated follow-up if capacity requires) to implement alongside their own card changes, since both stories already touch the same card components.

**Instrumentation specification (for ST-05/ST-06 to implement):**

| Event | Trigger | Cards affected | Payload |
|---|---|---|---|
| `dashboard_card_view` | Card enters viewport (or component mount, if viewport tracking is out of scope for a first pass) | All `DashboardHome.js` cards (5 status cards + 5 Morning Briefing sub-cards + AI Daily Briefing) | `{ card_id: string, state: "loading" \| "empty" \| "populated" \| "error" }` |
| `dashboard_card_click` | User clicks/navigates via a card's click-through target | Cards with a `to` prop on `DashboardCard` (whole-card `Link`) | `{ card_id: string, destination: string }` |

No event-tracking backend/analytics endpoint exists to receive these events yet — this table is a specification of intent (event names, triggers, payload shape) for whichever implementation story wires up an actual sink (e.g. a lightweight `console.debug`-backed stub initially, per standard incremental-instrumentation practice, escalating to a real analytics sink only if a product need for the data is confirmed). Filing an actual sink is out of scope for both `ST-05` and `ST-06`'s stated AC — if `ST-05`/`ST-06` implementation finds this ambiguous, file a `delegated_decision` escalation rather than guessing at sink infrastructure.

## 5. AC-04 — Dual-Theme Verification Call-Out

**Already satisfied — no new artefact needed.** Both approved design artefacts already carry an explicit dual-theme verification requirement:
- `dashboard-empty-states/ux_spec.md` §5 ("Playwright coverage for this story must explicitly verify both light and dark theme rendering... Test file: shared spec named per ST-08")
- `dashboard-briefing-hierarchy/ux_spec.md` §5 (same requirement, naming the specific new tokens to verify: panel background/border pair, label text colour pair, both new icons' colour pairs)

This AC is additionally now backstopped by the reusable template fragment in `base44_prompt_template_library.md` §4, so future visual stories inherit the same call-out without re-deriving it.

## 6. AC-05 — Merge-Before-Planning Confirmation

Confirmed as a process requirement, not yet actionable — `ST-05`/`ST-06` remain out of sprint scope this cycle per the EPIC-03 sequencing constraint (`stage4_backlog_slice.md`). This document and the `design_system.md`/`base44_prompt_template_library.md` updates it references must be merged to `main` before `ST-05`/`ST-06` enter their own sprint planning cycle; both stories' AC should cross-reference this pass (`docs/specs/blg_fe_110_111_pre_implementation_spec_instrumentation_pass.md`) at that time, per the existing note already present in their approved `ux_spec.md` "Depends on" header fields.

## 7. Known Deviations

None. This is a net-new readiness/confirmation artefact; the `design_system.md` and `base44_prompt_template_library.md` changes it references are documented as version increments in those files' own change logs.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-15 | 1.0 | Initial spec & instrumentation pass (ST-04, EPIC-03, v7.2) |
