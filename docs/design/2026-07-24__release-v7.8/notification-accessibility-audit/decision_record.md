**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-24__release-v7.8
**Backlog source:** BLG-FE-127
**Maps to:** EPIC-03, ST-03

---

# Decision Record — Accessibility Pass on v7.7 Notification UX Components

## 1. Scope

This is an audit-and-fix story, not a new-surface design. The design gate's role is to fix the **standard** the audit is run against and the **components in scope**, so Sprint Planning can seal the story and execution can proceed straight to review without a separate design round-trip for whatever the audit finds (trivial findings are fixed directly per AC; non-trivial findings are filed as follow-up backlog items, not designed here).

**In scope (both shipped v7.7, EPIC-02/EPIC-04):**
- `StandingAlert` / `StandingAlertStack` shared primitive — `design_system.md` §Shared UI Components → Standing Alert (design source: `docs/design/2026-07-21__release-v7.7/standing-alert-component/ux_spec.md`)
- Notification/digest surface consolidation — nav dedup, alert-count badge, digest grouping — `notifications.md` (design source: `docs/design/2026-07-21__release-v7.7/nav-notification-digest-consolidation/ux_spec.md`)

**Out of scope:** any notification-adjacent component not shipped in v7.7 (e.g. Custom Price Alerts, v7.5 — already covered by its own design gate; Alert History table — pre-existing, not part of the v7.7 consolidation).

## 2. Standard Applied

Reuses the existing WCAG 2.1 AA contrast token already defined in `design_system.md` §Color Usage (no new token needed for text/background contrast — see that section's `text-slate-400`/`text-slate-600` worked example, ≥4.5:1 normal text).

**New this cycle — Focus Indicator standard**, added to `design_system.md` §Hover & Focus States (that section previously stated only "Form fields show focus outlines for accessibility" with no measurable threshold — insufficient to audit against):

> Any element receiving keyboard focus (buttons, dismiss controls, links, form fields) must render a focus indicator with ≥3:1 contrast against its immediately adjacent colour(s), per WCAG 2.1 SC 1.4.11 (Non-text Contrast). The default browser/Tailwind `focus-visible` ring token satisfies this where the ring colour has not been overridden; any component with a custom focus style must be checked individually.

Audit checks, per in-scope component:
1. Text/background contrast (heading, body, dismiss-button label) ≥4.5:1 both themes
2. Focus-visible ring contrast ≥3:1 both themes, on every interactive element (dismiss button, nav badge if focusable, digest expand/collapse control)
3. Icon-only controls (e.g. `StandingAlert`'s dismiss `X`) checked per WCAG 1.4.11 non-text contrast, consistent with the existing icon-only exemption note in `design_system.md` §Color Usage

## 3. Method

Head of UX & Design (or delegate) inspects each in-scope component in both light and dark theme, at both idle and focused states, against §2's thresholds. This is a manual review pass, not a new automated tool — no CI gate is introduced by this story (that would be separate scope).

## 4. Disposition Rule

- **Pass:** no findings, recorded as such in QA evidence — no spec change needed.
- **Trivial fix** (single class-token swap, no layout/behaviour change): fixed directly during sprint execution; documented as a spec Change Log entry on `design_system.md` and/or `notifications.md`, same pattern as prior contrast remediations (e.g. `secondary-text-contrast`, `heading-light-theme-contrast`).
- **Non-trivial fix** (requires new component states, layout change, or design judgement beyond a token swap): filed as a follow-up backlog item via `/backlog-add`, not designed here — consistent with the story's own AC ("filed as follow-up backlog items if not [trivial]").

## 5. Compliance Check

No conflict with `strategy_rules.md §13` — purely accessibility/visual, no automated-decision or trading-parameter surface. Not an analytics/metrics feature.

## 6. Sign-off

- **Head of UX & Design:** Approved — 2026-07-24 (standard and scope, per §2/§1)
- **Product Owner:** Approved — 2026-07-24 (disposition rule accepted — trivial-fix-or-file split, no blanket "all findings fixed this sprint" commitment)
