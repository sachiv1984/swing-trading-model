**Owner:** Base44 Frontend Prompt Owner
**Class:** Class 2 — Supporting
**Status:** Supporting
**Canonical Source:** docs/specs/frontend/design_system.md
**Version:** 1.3
**Last Updated:** 2026-07-27
**Story:** ST-04 (BLG-SPEC-90, EPIC-03, v7.2); ST-04 (BLG-SPEC-91, EPIC-02, v7.3); ST-06 (BLG-SPEC-93, EPIC-04, v7.3); ST-13 (BLG-FE-129, EPIC-13, v7.9)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Base44 Prompt Template Library

## 1. Purpose

Every `delegated_frontend` story requires a complete six-section Base44 prompt draft (`execution_prompt.md §5.1`: Context, Change Required, API Contract, Behaviour Rules, Non-Functional Rules, Expected Outcome — see `claude/system/shared_standards.md §16.3` for the delegation log schema this feeds). Recurring UI patterns have historically been re-derived from scratch in each delegation record. This library holds pre-approved section fragments for known-recurring patterns so a delegation draft can cite a template entry instead of re-writing the pattern.

This document is Class 2 (Supporting) — it summarises and applies patterns whose authority lives in `design_system.md` (Class 1, Canonical). If this document and `design_system.md` ever disagree, `design_system.md` prevails.

## 2. Template: `DataState` Compact Empty-State (Card Context)

**Use when:** delegating a story that adds or modifies a small grid-context card (shares a row with 2+ siblings) whose underlying data can be legitimately empty (a meaningful "nothing here yet" state — not a valid zero value like "0% heat").

**Source pattern:** `design_system.md` §Shared UI Components → Cards → Data States; concrete precedent `docs/design/2026-07-15__release-v7.2/dashboard-empty-states/ux_spec.md` (ST-05).

**Reusable fragment — Behaviour Rules section:**
```
- Wrap the card's non-empty content in <DataState compact empty={<condition>} emptyIcon={<Icon>} emptyHeading="<heading>" emptyBody="<body>"> — do not pass loading/error props here if the card's outer shell (e.g. DashboardCard) already handles loading/error; compact only governs the empty branch.
- Empty condition must reflect "no meaningful data", not "value is zero and that zero is itself meaningful" — confirm which case applies before wiring the empty prop.
- No emptyAction CTA if the card already has a click-through destination (e.g. whole-card Link) — a second CTA competes with it.
- Icon choice: neutral ("nothing here yet") vs reassuring (e.g. ShieldCheck for "nothing at risk") depending on whether the empty state is a good or neutral outcome — do not default to a single icon for every card.
```

**Reusable fragment — Non-Functional Rules section:**
```
- Do not modify DataState's loading or error branches — compact affects the empty branch only.
- Any new background/border/label token must ship as an explicit light+dark Tailwind pair (`bg-x dark:bg-y`), never a bare dark-only class (recurring defect class: BLG-FE-87/88/95).
```

**Reusable fragment — Expected Outcome section:**
```
Card renders a compact icon+heading+body empty state (not a blank card or raw zero/null value) when its underlying data is empty; loading and error states for the card are unchanged; light and dark theme both render the empty state with adequate contrast.
```

## 3. Template: Primary vs Secondary Card Treatment

**Use when:** delegating a story that introduces or updates a page section meant to read as visually distinct from a neighbouring grid of status/data cards (e.g. an "intelligence" or "briefing" section vs live status cards).

**Source pattern:** `design_system.md` §Shared UI Components → Cards → Card Hierarchy; concrete precedent `docs/design/2026-07-15__release-v7.2/dashboard-briefing-hierarchy/ux_spec.md` (ST-06).

**Reusable fragment — Behaviour Rules section:**
```
- Primary/intelligence-section treatment: enclosing panel with an explicit light+dark background/border pair, section label at text-sm font-semibold with a leading icon establishing a shared "intelligence section" visual language.
- Secondary/status-card treatment: plain shared card shell, no enclosing panel, no elevated label — this is the neutral default; do not add panel treatment to status cards.
- If multiple primary-tier sections exist on the same page, they should share the same icon-and-label visual language (even if container treatment differs) so a user recognises them as one category at a glance.
- Distinction must be apparent at the point the user reaches each section (self-evident), not dependent on scrolling back to compare — this does not require reordering existing sections.
```

**Reusable fragment — Non-Functional Rules section:**
```
- Any new panel/border/label token must ship as an explicit light+dark pair from the start (see BLG-FE-87/88/95 precedent).
- Child card components inside a primary-tier section are otherwise unchanged — same shell, same queries, same click targets; differentiation is carried by the enclosing panel/label only, not by altering the children.
```

## 4. Template: Dual-Theme Verification Call-Out (Mandatory for Any Visual Story)

**Use when:** any `delegated_frontend` story with an observable AC (colour, layout, rendering, interaction).

**Reusable fragment — append to every applicable Base44 prompt draft and its paired Playwright coverage:**
```
This story's Playwright coverage (or human staging sign-off) must explicitly verify both light and dark theme rendering — do not verify dark mode only. Any new colour/background/border token must be checked as an explicit light+dark pair.
```

**Dark-mode acceptance-criteria checklist item (v1.3, ST-13, EPIC-13, v7.9, BLG-FE-129):** the fragment above is a *verification* call-out, applied at test time. The v7.8 dark-mode contrast audit (`BLG-FE-125`) found and fixed several defects only after the fact, because no story stated a dark-mode requirement as its own acceptance criterion up front. Every Base44 prompt draft for a story with observable AC must therefore also include an explicit dark-mode line in its **Acceptance Criteria** — not only in the Playwright/staging verification note:

```
- Acceptance Criteria: [existing ACs] + "All new or modified colour/background/border tokens render correctly in both light and dark theme — checked as an explicit light+dark pair, not dark-only."
```

Adding this to the AC list (rather than only the verification call-out) makes dark-mode a stated requirement the delegate designs against from the start, not a defect found during a separate audit pass afterward.

## 5. Template: Global Command Palette (Cmd/Ctrl-K Pattern)

**Use when:** delegating `BLG-FE-115` (global command palette) or any future story adding a keyboard-invoked, searchable navigation/action overlay.

**Source pattern:** `docs/specs/blg_fe_115_pre_implementation_readiness_pass.md` (ST-04, EPIC-02, v7.3); primitives already scaffolded at `src/components/ui/command.js` (shadcn/`cmdk` wrapper — `cmdk` package itself is **not yet installed**, see readiness pass §2).

**Reusable fragment — Behaviour Rules section:**
```
- Global keyboard invocation: Cmd+K (macOS) / Ctrl+K (Windows/Linux) — must not fire when a text input/textarea already intercepts the combination (none currently do; re-verify at implementation time).
- Escape closes the palette; arrow keys navigate the filtered list; Enter navigates via react-router-dom's useNavigate.
- Index is two-tier: static page index from src/pages.config.js PAGES (all routes), dynamic entity index limited to tickers already present in the user's loaded data (open positions, watchlist, trade plans) — do not add a new backend search query for v1.
- Empty/no-results state must use the design_system.md DataState pattern (or a documented compact-list variant addendum) — not a bare CommandEmpty text string.
- Persistent, mouse-accessible affordance in the nav bar showing the shortcut hint — keyboard invocation must not be the only discovery path.
```

**Reusable fragment — Non-Functional Rules section:**
```
- First commit must add `cmdk` to package.json dependencies (pinned to a React-19-compatible version) — command.js already imports it but it is not currently installed.
- No new backend endpoint for v1 — index sources are client-side only (pages.config.js + already-fetched entity data).
- Any new background/border/label token on the palette dialog must ship as an explicit light+dark Tailwind pair, consistent with the project-wide rule (BLG-FE-87/88/95 precedent).
```

**Reusable fragment — Expected Outcome section:**
```
Cmd/Ctrl-K opens a searchable palette listing pages and in-scope entities; Escape/click-away closes it; Enter/click navigates; empty search state renders the DataState pattern; a visible nav-bar affordance provides mouse-accessible discovery; both light and dark theme render correctly.
```

## 6. Template: Bulk-Action Toolbar (Multi-Select + Bulk-Action Pattern)

**Use when:** delegating `BLG-FE-117` (bulk actions) or any future story adding row-level multi-select with a bulk-action toolbar.

**Source pattern:** `docs/specs/blg_fe_117_pre_implementation_readiness_pass.md` (ST-06, EPIC-04, v7.3) — genuinely new pattern, no prior in-app precedent (existing checkbox usages are single-checkbox confirmation controls, not row-multi-select).

**Reusable fragment — Behaviour Rules section:**
```
- Row-level checkbox selection; bulk-action toolbar renders only when 1+ rows are selected (no zero-selected empty state to design).
- Toolbar shows a live selected-count and the available bulk actions for the current entity (tag / archive / remove).
- Destructive bulk actions (delete/archive) require an explicit confirmation step before the API call fires — no existing precedent for a confirm-free destructive bulk action in this codebase.
- Partial failures must be surfaced per-row (not a single opaque "some failed" toast) — read succeeded/failed arrays from the response and reflect the failed subset back to the user with per-item reasons.
```

**Reusable fragment — Non-Functional Rules section:**
```
- Any new toolbar background/border/badge token must ship as an explicit light+dark Tailwind pair (BLG-FE-87/88/95 precedent).
- Batch endpoint calls must be capped (recommend 100 IDs/call) — do not fire one API call per selected row from the client.
```

**Reusable fragment — Expected Outcome section:**
```
Selecting 1+ rows reveals a bulk-action toolbar with an accurate selected-count; bulk tag/archive/remove actions succeed or partially-fail with per-row feedback; destructive actions require confirmation; toolbar disappears at zero-selected; both light and dark theme render correctly.
```

## 7. Maintenance

New entries are added to this library when a pattern is formalised in `design_system.md` and applied to two or more concrete stories (the same threshold `roadmap_prompt.md`'s STEP 4.2 idea-consolidation convention uses for "recurring" — a single application does not yet justify a library entry). Entries here must be kept consistent with `design_system.md`; if a `design_system.md` edit changes a pattern documented here, update this file in the same commit.

**Threshold exception (v1.3, ST-13, EPIC-13, v7.9):** the 2+-story threshold above governs adding a *new* template section. The §4 dark-mode AC checklist addition is an addendum to an already-existing, already-approved section, not a new template — and the underlying defect class (light+dark token pair omissions) already has multiple documented precedents (`BLG-FE-87/88/95/125`) even without a literal second application of this specific checklist wording. Recorded here so this doesn't read as an inconsistency on a future audit.

## 8. Known Deviations

None. This is a net-new artefact — no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-27 | 1.3 | Added dark-mode acceptance-criteria checklist item to §4 — every Base44 prompt draft with observable AC must state a dark-mode requirement in its Acceptance Criteria, not only in the Playwright/staging verification call-out (ST-13, EPIC-13, v7.9, BLG-FE-129) |
| 2026-07-16 | 1.2 | Added Bulk-Action Toolbar (multi-select) template (ST-06, EPIC-04, v7.3, BLG-SPEC-93) |
| 2026-07-16 | 1.1 | Added Global Command Palette (Cmd/Ctrl-K) template (ST-04, EPIC-02, v7.3, BLG-SPEC-91) |
| 2026-07-15 | 1.0 | Initial library — DataState compact empty-state, primary/secondary card hierarchy, dual-theme call-out (ST-04, EPIC-03, v7.2) |
