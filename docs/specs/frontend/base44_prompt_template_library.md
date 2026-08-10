**Owner:** Base44 Frontend Prompt Owner
**Class:** Class 2 — Supporting
**Status:** Supporting
**Canonical Source:** docs/specs/frontend/design_system.md
**Version:** 1.7
**Last Updated:** 2026-08-10
**Story:** ST-04 (BLG-SPEC-90, EPIC-03, v7.2); ST-04 (BLG-SPEC-91, EPIC-02, v7.3); ST-06 (BLG-SPEC-93, EPIC-04, v7.3); ST-13 (BLG-FE-129, EPIC-13, v7.9); ST-18 (BLG-FE-124, EPIC-03, v8.0); ST-12 (BLG-FE-121, EPIC-03, v8.3); ST-14 (BLG-FE-132, EPIC-03, v8.3); ST-17 (BLG-FE-99, EPIC-05, v8.5)
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
- Destructive bulk actions (delete/archive) require an explicit confirmation step before the API call fires — no existing precedent for a confirm-free destructive bulk action in this codebase. Use the shared `ConfirmationModal` component (§10) for this step; a bulk-remove action is the kind of case §10's undo-window variant exists for (optimistic execution + a few seconds to reverse, rather than a blocking pre-action confirm).
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

## 7. Template: Label+Value Skeleton Pair (Stat/Metric Card Grid)

**Use when:** delegating a story that adds or modifies a small grid of stat/metric values (e.g. a 2x4 or 4-column grid of label+value pairs) where each value loads asynchronously.

**Source pattern:** already-implemented precedent `src/pages/Research.js` (label+value skeleton pairs in a `grid-cols-2 md:grid-cols-4` layout) and `src/components/trades/SetupQualityScorePanel.js` (single label+value pair). Genuinely recurring — 2+ concrete precedents (ST-18, BLG-FE-124, EPIC-03, v8.0).

**Reusable fragment — Behaviour Rules section:**
```
- Loading state renders one `<Skeleton>` pair (label-width skeleton above a value-width skeleton) per grid cell, matching the exact grid layout the loaded content will use — this prevents layout shift when data arrives.
- Use the shared `Skeleton` primitive (`src/components/ui/skeleton.js`, `animate-pulse` + `bg-primary/10` or the page-local `bg-slate-700/50` variant already in use) — do not introduce a new skeleton implementation.
- Skeleton dimensions should approximate the real content's width (e.g. `w-16 h-3` for a label, `w-24 h-6` for a value) — do not use a single uniform skeleton size for both label and value.
- Do not render skeletons for cells whose data is already available from a prior fetch — only cells whose specific query is still loading show a skeleton (partial-loading grids are expected, not an all-or-nothing loading state).
```

**Reusable fragment — Non-Functional Rules section:**
```
- Any new skeleton background token must resolve correctly in both light and dark theme (BLG-FE-87/88/95 precedent) — the shared `Skeleton` primitive already handles this; do not override with a theme-specific class.
```

**Reusable fragment — Expected Outcome section:**
```
Grid renders one label+value skeleton pair per cell while its data is in flight, at the same dimensions as the final content (no layout shift on data arrival); cells with already-available data render immediately without waiting on sibling cells.
```

## 8. Template: Table/List Row Skeleton (Variable-Width Shimmer Placeholder)

**Use when:** delegating a story that adds or modifies a table or list whose rows load asynchronously (as opposed to a single spinner for the whole table).

**Source pattern:** already-implemented precedent `src/pages/Screener.js` (`SkeletonRow`, 8 rows) and `src/pages/NotificationsHistory.js` (`SkeletonRows`, 5 rows) — both render a fixed count of placeholder `<tr>` rows with per-cell shimmer bars of varied width. Genuinely recurring — 2+ concrete precedents (ST-18, BLG-FE-124, EPIC-03, v8.0).

**Reusable fragment — Behaviour Rules section:**
```
- Render a fixed, realistic number of skeleton rows while loading (5-8, matching the typical/expected page size for this table) — not a single row, and not an arbitrarily large count.
- Each cell's shimmer bar uses a varied width per column (e.g. `${50 + (i * 13) % 40}%`) rather than a uniform width for every cell — an all-identical-width grid of bars reads as a placeholder grid rather than a plausible loading table.
- Use `animate-pulse` on each bar (matching the shared `Skeleton` primitive's animation), rendered inside the same `<td>`/row structure the real rows use, so column alignment does not shift when data arrives.
```

**Reusable fragment — Non-Functional Rules section:**
```
- Skeleton row/cell background tokens must resolve correctly in both light and dark theme (BLG-FE-87/88/95 precedent).
- Do not fetch or reference the eventual row data inside the skeleton component — it renders unconditionally while the loading flag is true, with no data dependency.
```

**Reusable fragment — Expected Outcome section:**
```
Table shows a fixed set of shimmering placeholder rows (varied bar widths per column) while loading; column widths and row structure match the loaded state exactly, so no layout shift occurs when real data replaces the skeleton.
```

## 9. Template: Inline Partial-Value Skeleton (Async Sub-Value Within an Already-Rendered Shell)

**Use when:** delegating a story where only one or two values inside an already-visible card/section load asynchronously (e.g. a secondary metric that depends on a slower endpoint), while the rest of the card's labels and shell render immediately — as distinct from the whole-card or whole-grid skeleton patterns above.

**Source pattern:** already-implemented precedent `src/pages/Research.js` (`heatLoading` gating a single inline `<Skeleton>` in place of one value, while the card's label and surrounding shell render unconditionally). Genuinely recurring — 2+ concrete precedents (ST-18, BLG-FE-124, EPIC-03, v8.0).

**Reusable fragment — Behaviour Rules section:**
```
- The card's static label/shell content renders immediately and unconditionally — only the specific value that depends on the slower query is replaced with a single `<Skeleton>` while its own `isLoading` flag is true.
- Do not gate the whole card (or a whole grid of cards) behind this one value's loading state — a partial-card skeleton is the correct pattern precisely because the rest of the card's content does not depend on the slow query.
- Once the value resolves, render its real formatted content (or an explicit error/fallback state, e.g. `HeatValue value={null} isError={true}`) in place of the skeleton — never leave the skeleton rendered after the query settles, whether it succeeded or failed.
```

**Reusable fragment — Non-Functional Rules section:**
```
- Skeleton background token must resolve correctly in both light and dark theme (BLG-FE-87/88/95 precedent).
```

**Reusable fragment — Expected Outcome section:**
```
Card shell and static labels render immediately; only the specific async value shows a skeleton while its own query is in flight; on resolution the skeleton is replaced with the real value or an explicit error state — the rest of the card is never blocked on this one value's load time.
```

## 10. Template: Shared Modal-Confirmation Component (with optional undo-window)

**Use when:** delegating `BLG-FE-116` (custom price alerts — delete/deactivate action), `BLG-FE-117` (bulk actions — destructive bulk action confirm step, see §6), or any future story needing a confirm-before-acting or confirm-with-undo interaction.

**Source pattern:** `docs/design/2026-08-05__release-v8.3/shared-confirmation-modal-undo-window/decision_record.md` (ST-12, EPIC-03, v8.3) — genuinely new interaction pattern (undo-window countdown); component: `src/components/ui/ConfirmationModal.js`.

**Reusable fragment — Behaviour Rules section:**
```
- Standard variant (undoWindow.enabled = false, the default): modal opens on trigger; Confirm executes the action on click and closes the modal; Cancel dismisses without action. This formalises the existing shipped confirmation-modal precedent (positions.md §Exit action, watchlist.md §Remove Confirmation Prompt) as the component's default — no behaviour change to either existing consumer unless they are explicitly migrated onto it.
- Undo-window variant (undoWindow.enabled = true, undoWindow.durationSeconds default 5): Confirm closes the modal immediately and executes the action optimistically (same optimistic-update pattern as "Mark Reviewed"/watchlist "Keep"); a toast then shows the action's past-tense confirmation text plus a live "Undo (Ns)" countdown button. Clicking Undo before expiry reverses the action (caller-supplied inverse operation) and replaces the toast with a brief "Undone." confirmation. If the window expires, the toast auto-dismisses and the action is final — no further confirmation shown.
- The countdown is always visible as text on the Undo button itself, never a bar/ring/colour alone (colour is never the sole differentiator, per design_system.md Accessibility).
- Modal: focus trap + restoration (existing Dialog primitive convention, TradePlan.js Abandon modal precedent); Escape = Cancel.
```

**Reusable fragment — Non-Functional Rules section:**
```
- Default undo-window duration (5s) intentionally overrides `sonner`'s ~4s auto-dismiss default — the undo toast is actionable, not purely informational, and needs enough time for a deliberate click.
- Any new modal/toast background/border/token must ship as an explicit light+dark Tailwind pair (BLG-FE-87/88/95 precedent).
- This component does not prescribe how a consumer reverses an optimistic action on Undo (re-POST, cancel a not-yet-fired request, etc.) — that is each consumer's own data shape.
```

**Reusable fragment — Expected Outcome section:**
```
Standard variant: Confirm/Cancel behave exactly as the existing shipped confirmation-modal precedent. Undo-window variant: Confirm executes optimistically and closes the modal; an actionable toast with a live countdown offers a genuine window to reverse the action; expiry without Undo is silent (no extra confirmation); both light and dark theme render correctly.
```

**Forward-reference note (ST-12 AC-2):** this entry is the reference point for `BLG-FE-116`/`BLG-FE-117`'s eventual Base44 prompt drafts — see the "Use when" line above and §6's updated destructive-bulk-action bullet. Neither story is in scope this sprint; confirm at each story's own delegation time that its prompt draft cites this section, and record that confirmation in this file's Change Log (same tracking convention as §12).

## 11. Template: Standard Theme-Compliance Section (Generation-Time)

**Use when:** drafting the Behaviour Rules or Non-Functional Rules section of **any** `delegated_frontend` Base44 prompt — unconditionally, not only stories already known to touch colour/background/border tokens. Paste this fragment into every prompt draft from the start.

**Source pattern:** `design_system.md` §Theme & Colors + §Accessibility, and the recurring defect class `BLG-FE-87/88/95/125/129` — four separate shipped dark-mode contrast/token defects, each caught only after generation (by a later audit or the §4 review-time checklist), never prevented at generation time. `BLG-FE-132`'s problem statement: the prompt template itself lacked a standard theme-compliance section, so each case was individually re-derived and caught late rather than instructed up front.

**Distinction from §4:** §4 (Dual-Theme Verification Call-Out) is a **review-time** instruction — it tells the delegate how the work will be *checked* (Playwright/staging must cover both themes) and adds a dark-mode line to the story's stated Acceptance Criteria. This section is a **generation-time** instruction — it tells the delegate the *rule to build against* before any code is written, so a violation is never generated in the first place. Both are required together on any story with observable AC; this section does not replace §4's checklist item.

**Reusable fragment — Behaviour Rules section (paste verbatim):**
```
- Every new or modified colour, background, or border Tailwind class must ship as an explicit light+dark pair (e.g. `bg-slate-100 dark:bg-slate-800`) — never a bare class that only resolves correctly in one theme. This is a standing project rule, not a one-off review comment (recurring defect: BLG-FE-87, BLG-FE-88, BLG-FE-95, BLG-FE-125, BLG-FE-129).
- Prefer an existing token pair already used for the same semantic role elsewhere in the app (see design_system.md §Theme & Colors) over inventing a new one — a new pair is only warranted when no existing token fits the specific UI role.
- CSS-variable-backed semantic classes (e.g. `bg-primary`, `text-muted-foreground`) are exempt from the explicit-pair requirement — they already resolve per-theme via the underlying CSS custom property, not via a Tailwind `dark:` variant.
```

**Reusable fragment — Non-Functional Rules section (paste verbatim):**
```
- Do not defer theme correctness to a follow-up audit pass — verify both themes render correctly before considering the story complete, not only when a dark-mode audit later flags it.
```

**Reusable fragment — Expected Outcome section (paste verbatim):**
```
Every new or modified colour/background/border token renders correctly in both light and dark theme, using an explicit light+dark Tailwind pair (or an already-theme-aware semantic class) — no bare dark-only or light-only token ships.
```

## 12. Template: Standard Full-Page/Section Empty-State (Non-Card Context)

**Use when:** delegating a story that adds or modifies a full page or major page section (not a small grid-context card — see §2 for that variant) whose underlying data can be legitimately empty (e.g. no trade plans yet, no closed trades in the selected calendar range, watchlist has no tickers). The two are visually and semantically distinct: this template renders `DataState`'s default (non-`compact`, non-`inline`) empty branch — the full icon + heading + body stack at `py-16` — as the page/section's entire content.

**Source pattern:** `design_system.md` §Shared UI Components → Cards → Data States (default variant + microcopy pattern v1.8); concrete precedent `EPIC-04/ST-10` (`2026-08-08__release-v8.5`, `BLG-FE-92`) — the decision record and its two shipped fixes (`TradePlans.js`, `CalendarView.js`) are the first two concrete applications establishing this as a genuinely recurring pattern (per §13's Maintenance 2+-story threshold).

**Reusable fragment — Behaviour Rules section:**
```
- Wrap the page/section's non-empty content in <DataState empty={<condition>} emptyIcon={<Icon>} emptyHeading="<heading>" emptyBody="<body>"> — do not pass `compact` (that variant is for small grid-context cards only, see the card-context template if this is a card, not a full page/section).
- emptyHeading: 2–5 words, sentence case, NO trailing period (it's a label, not a sentence) — this is a common generation-time mistake (`TradePlans.js`/`CalendarView.js` both shipped with a trailing period before EPIC-04/ST-10's fix). Use "No <noun>" / "No <noun> yet" for content that accrues over time (notifications, positions, trade plans, closed trades); use "Your <noun> is empty" for content the user actively curates (the watchlist).
- emptyBody: exactly one sentence, present tense, states the concrete next action that would populate the view, ends with a full stop.
- Icon: contextual to the content type — do not default to a single generic icon across unrelated pages; match existing call sites' icon choice for the same content category where one exists.
```

**Reusable fragment — Non-Functional Rules section:**
```
- Do not modify DataState's loading or error branches when implementing the empty branch.
- If this page/section already has an equivalent empty-state call site elsewhere in the app for the same content type (e.g. a filtered vs. unfiltered view of the same data), keep heading/body wording consistent between them unless the filtered context specifically warrants different copy (e.g. "No trades match your filters" vs "No trade plans yet").
```

**Reusable fragment — Expected Outcome section:**
```
Page/section renders a full icon+heading+body empty state (not a blank page, raw zero/null value, or a heading with a stray trailing period) when its underlying data is empty; loading and error states are unchanged; light and dark theme both render the empty state with adequate contrast; heading has no trailing period.
```

## 13. Forward-Reference Tracking (ST-18 AC-3)

ST-18's third acceptance criterion — "Referenced by at least one new story going forward" — cannot be satisfied within the same story that authors the library entries; no story in this sprint (`2026-07-30__release-v8.0`) delegates a card/loading-skeleton/empty-state UI change to cite them against. This mirrors the same "retrospectively confirmable" AC pattern already used elsewhere in this sprint's backlog (see `sprint_backlog.md` ST-19 AC-2). Track at the next story that delegates or implements a card-grid, table-row, or partial-value loading skeleton: confirm it cites the applicable §7/§8/§9 entry, and record that confirmation in this file's Change Log.

## 14. Maintenance

New entries are added to this library when a pattern is formalised in `design_system.md` and applied to two or more concrete stories (the same threshold `roadmap_prompt.md`'s STEP 4.2 idea-consolidation convention uses for "recurring" — a single application does not yet justify a library entry). Entries here must be kept consistent with `design_system.md`; if a `design_system.md` edit changes a pattern documented here, update this file in the same commit.

**Threshold exception (v1.3, ST-13, EPIC-13, v7.9):** the 2+-story threshold above governs adding a *new* template section. The §4 dark-mode AC checklist addition is an addendum to an already-existing, already-approved section, not a new template — and the underlying defect class (light+dark token pair omissions) already has multiple documented precedents (`BLG-FE-87/88/95/125`) even without a literal second application of this specific checklist wording. Recorded here so this doesn't read as an inconsistency on a future audit.

**§7/§8/§9 provenance note (v1.4, ST-18, EPIC-03, v8.0):** unlike prior entries, which were extracted from a `design_system.md`/`ux_spec.md` source pattern, these three entries were extracted directly from already-implemented, already-recurring component code (`src/pages/Research.js`, `src/pages/Screener.js`, `src/pages/NotificationsHistory.js`, `src/components/trades/SetupQualityScorePanel.js`) — no `ux_spec.md` or `design_system.md` section documents the loading-skeleton pattern yet. This is consistent with the "genuinely recurring" threshold in the paragraph above (2+ concrete precedents per entry), just sourced from implementation rather than a prior design spec. If `design_system.md` is later updated with a formal loading-skeleton section, reconcile these entries against it and update this file in the same commit per the rule above.

**§10 provenance note (v1.5, ST-12, EPIC-03, v8.3):** §10 was extracted from a UX decision record (`decision_record.md`, approved by Head of UX & Design), not from implementation code — this is genuinely new interaction design (no prior undo-window precedent in the app), consistent with the same-provenance convention `design_system.md`/`ux_spec.md`-sourced entries (§2/§3/§4/§5/§6) already use.

## 15. Known Deviations

None. This is a net-new artefact — no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-08-10 | 1.7 | Added §12 Standard Full-Page/Section Empty-State (Non-Card Context) — the full `DataState` empty-branch stack (icon+heading+body, `py-16`) for page/section-level empty states, distinct from §2's small-grid-card `compact` variant; incorporates the empty-state microcopy pattern (`design_system.md` v1.8) and the trailing-period generation mistake caught and fixed at `EPIC-04/ST-10` (`TradePlans.js`, `CalendarView.js`) this same cycle — the 2 concrete precedents satisfying §14's Maintenance threshold; renumbered old §12/§13/§14 → §13/§14/§15 (ST-17, EPIC-05, v8.5, BLG-FE-99) |
| 2026-08-06 | 1.6 | Added §11 Standard Theme-Compliance Section (Generation-Time) — a generation-time prompt fragment distinct from §4's review-time checklist, addressing the recurring dark-mode defect class (`BLG-FE-87/88/95/125/129`) at prompt-draft time instead of catching it after generation; renumbered old §11/§12/§13 → §12/§13/§14 (ST-14, EPIC-03, v8.3, BLG-FE-132) |
| 2026-08-06 | 1.5 | Added §10 Shared Modal-Confirmation Component (with optional undo-window) — extracted from the `ConfirmationModal` UX decision record, forward-referenced by both `BLG-FE-116` and `BLG-FE-117`'s eventual prompt drafts (§6 updated to cite it); renumbered old §10/§11/§12 → §11/§12/§13 (ST-12, EPIC-03, v8.3, BLG-FE-121) |
| 2026-07-30 | 1.4 | Added 3 loading-skeleton templates — §7 Label+Value Skeleton Pair (stat/metric card grid), §8 Table/List Row Skeleton (variable-width shimmer), §9 Inline Partial-Value Skeleton (async sub-value within an already-rendered shell) — extracted from already-recurring component precedent (`Research.js`, `Screener.js`, `NotificationsHistory.js`, `SetupQualityScorePanel.js`); §10 tracks the forward-reference AC (ST-18, EPIC-03, v8.0, BLG-FE-124) |
| 2026-07-27 | 1.3 | Added dark-mode acceptance-criteria checklist item to §4 — every Base44 prompt draft with observable AC must state a dark-mode requirement in its Acceptance Criteria, not only in the Playwright/staging verification call-out (ST-13, EPIC-13, v7.9, BLG-FE-129) |
| 2026-07-16 | 1.2 | Added Bulk-Action Toolbar (multi-select) template (ST-06, EPIC-04, v7.3, BLG-SPEC-93) |
| 2026-07-16 | 1.1 | Added Global Command Palette (Cmd/Ctrl-K) template (ST-04, EPIC-02, v7.3, BLG-SPEC-91) |
| 2026-07-15 | 1.0 | Initial library — DataState compact empty-state, primary/secondary card hierarchy, dual-theme call-out (ST-04, EPIC-03, v7.2) |
