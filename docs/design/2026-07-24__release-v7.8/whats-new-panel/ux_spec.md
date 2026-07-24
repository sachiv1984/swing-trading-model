**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-24__release-v7.8
**Backlog source:** BLG-FE-128
**Maps to:** EPIC-01, ST-01

---

# UX Spec — In-App "What's New" Panel

## 1. Problem

Users have no in-app way to see what changed in the most recent release. The only record is `docs/product/changelog.md`, a repo file not exposed anywhere in the running app. AC requires a panel that shows the most recent release's `### Changes shipped` entries and updates automatically on the next release without manual wiring.

## 2. Placement

**Decision:** Dashboard section, not a dedicated page/nav entry. Rationale: the Dashboard is the app's single daily entry point (`dashboard.md` §1) and "what's new" is exactly the kind of low-frequency, glanceable, dismissible content that doesn't warrant its own nav slot or route — a dedicated page would be checked rarely and add a permanent nav item for content that's only novel once per release.

Placed **below** the existing five session-summary cards (§2 Session Summary Cards in `dashboard.md`), as its own full-width card — not inside the Morning Briefing row (§1A), which is reserved for actionable start-of-day intelligence, not release notes.

## 3. Content & Data Source

- Panel title: **"What's New — v{X.Y}"** (version pulled from the changelog's most recent `## vX.Y — <title> — <date>` heading)
- Body: bullet list, one line per row of the changelog's most recent `### Changes shipped` table, showing the `Description` column only (not `EPIC` or `Spec sections updated` — those are internal governance references, not user-facing copy)
- Max 8 bullets shown; if the shipped table has more rows, show the first 8 with a trailing "+N more" (non-interactive, no expand — keeps the card bounded)
- No manual re-wiring on each release: the frontend must parse the **most recent** `## vX.Y` block from `docs/product/changelog.md` at render time (server-side), not embed a hardcoded copy of the current release's notes in the frontend build. This requires a backend endpoint that reads and parses `changelog.md` server-side (no such endpoint exists today — implementation detail for sprint execution, contract to be filed in `docs/specs/api_contracts/` per `CLAUDE.md` §2 same-commit rule).

## 4. States (`DataState`, default sizing — full-width card, not a grid sibling)

| State | Rendering |
|-------|-----------|
| Loading | `DataState` `loading` branch — centered spinner, no skeleton |
| Error | `DataState` `error` branch — heading "Unable to load release notes", no numeric/content fallback |
| Empty (changelog has no parseable version block) | `DataState` `empty` branch — heading "Nothing to show", body "Check back after the next release." |
| Ready | Title + bullet list per §3 |

Follows `design_system.md` §Shared UI Components → Cards → Data States exactly — default (non-`compact`) sizing since this card is full-width, not sharing a row.

## 5. Visual Treatment

Secondary-tier card (per `design_system.md` §Card Hierarchy) — this is informational, not advisory/actionable like the Morning Briefing primary-tier cards. Plain card shell, no accent border/background tint. Icon: `Sparkles` (Lucide), muted, leading the title — establishes a distinct "release notes" visual identity from both the primary intelligence-section language (§1A) and the plain session-summary cards.

No dismiss/collapse control in this iteration — AC does not require one, and the panel is naturally low-noise (content only changes once per release, ~weekly cadence per `changelog.md` history).

## 6. Out of Scope

- Push/toast notification on new release (not requested; AC is passive/on-visit only)
- Historical changelog browsing beyond the most recent version (AC scope is "most recent release" only — older entries remain accessible via `docs/product/changelog.md` in the repo, not an in-app concern)
- Per-user "seen" tracking / read receipts

## 7. Compliance Check

No conflict with `strategy_rules.md §13` (not a trading-parameter or automated-decision surface). No analytics/metrics displayed — not subject to canonical metric definitions.

## 8. Sign-off

- **Head of UX & Design:** Approved — 2026-07-24
- **Product Owner:** Approved — 2026-07-24 (placement: Dashboard section, not dedicated page, per §2)
