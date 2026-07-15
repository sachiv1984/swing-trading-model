**Owner:** Base44 Frontend Prompt Owner
**Class:** Class 2 — Supporting
**Status:** Supporting
**Canonical Source:** docs/specs/frontend/design_system.md
**Version:** 1.0
**Last Updated:** 2026-07-15
**Story:** ST-04 (BLG-SPEC-90, EPIC-03, v7.2)
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

## 5. Maintenance

New entries are added to this library when a pattern is formalised in `design_system.md` and applied to two or more concrete stories (the same threshold `roadmap_prompt.md`'s STEP 4.2 idea-consolidation convention uses for "recurring" — a single application does not yet justify a library entry). Entries here must be kept consistent with `design_system.md`; if a `design_system.md` edit changes a pattern documented here, update this file in the same commit.

## 6. Known Deviations

None. This is a net-new artefact — no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-15 | 1.0 | Initial library — DataState compact empty-state, primary/secondary card hierarchy, dual-theme call-out (ST-04, EPIC-03, v7.2) |
