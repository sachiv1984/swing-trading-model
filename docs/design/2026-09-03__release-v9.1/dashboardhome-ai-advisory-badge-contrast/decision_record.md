**Owner:** Head of UX & Design
**Class:** Design Decision Record (Class 4)
**Status:** Approved
**Last Updated:** 2026-09-03
**Cycle:** 2026-09-03__release-v9.1
**Source backlog item:** BLG-FE-165
**Sprint item:** ST-01 (EPIC-01)

# Decision Record — "AI Advisory" Badge Colour-Contrast Fix

## 1. Problem

`AiDisclaimer.js`'s `badge` variant renders the "AI Advisory" pill (consumed by `DashboardHome.js`) as `bg-amber-600 text-white` (`#D97706` background, white text, `text-xs font-semibold`). axe-core's `color-contrast` rule flags this as a serious violation (`BLG-FE-165`) — confirmed by direct computation below. This is the sole occurrence of this exact colour pair in the codebase (the "footer" variant of the same component already uses a compliant slate-text-on-transparent treatment and is not affected).

## 2. Contrast Verification (WCAG 2.1 SC 1.4.3)

Badge text is 12px (`text-xs`) semibold — below the "large text" threshold (18.66px bold), so the 4.5:1 normal-text ratio applies, not the 3:1 large-text ratio.

| Combination | Relative luminance (bg) | Contrast ratio vs. white text | Result |
|---|---|---|---|
| `bg-amber-600` (`#D97706`) / white | 0.2798 | **3.18:1** | ❌ FAIL (<4.5:1) |
| `bg-amber-700` (`#B45309`) / white | 0.1590 | **5.02:1** | ✅ PASS (≥4.5:1) |

## 3. Decision

Change the badge background from `bg-amber-600` to `bg-amber-700`, text and all other properties (`text-white`, `text-xs font-semibold px-2 py-0.5 rounded`) unchanged. Same amber hue family — one shade darker — so the badge remains visually identifiable as the existing "AI Advisory" affordance; this is the same class of fix already established for this codebase's other contrast defects (deepen the shade within the same hue rather than change hue or introduce a border/outline treatment).

No dark/light theme split is required — the badge has always rendered identically in both themes (solid fill, not a `dark:`-conditional token), and `bg-amber-700`/white passes the same 5.02:1 ratio regardless of surrounding theme background.

## 4. Scope Boundary

This decision covers only `AiDisclaimer.js`'s `badge` variant background. It does not touch:
- The adjacent inline text ("All actions require your confirmation") — already compliant (`text-slate-700 dark:text-slate-300`, ≥4.5:1, fixed v6.4/v6.7).
- The `footer` variant of the same component (`text-slate-600 dark:text-slate-400` on transparent background) — not in scope, no violation reported.

## 5. Constraints Check

- Does not contradict `strategy_rules.md §13` — the badge is a non-dismissible compliance-disclosure affordance; this decision changes only its background shade, not its presence, dismissibility, or wording.
- No AI-provider-call boundary implication — this is a static colour-token change to an existing disclaimer badge, not a new or extended AI-calling endpoint. §13 boundary pre-check (STEP 1) does not apply.
- No analytics/metrics involvement.

## 6. Approval

- Head of UX & Design: confirmed 2026-09-03
- Product Owner: approved 2026-09-03

This artefact is authoritative for the STEP 3 frontend spec update to `docs/specs/frontend/pages/dashboard.md` §Advisory Label.
