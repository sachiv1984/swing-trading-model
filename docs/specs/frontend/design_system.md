# design_system.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 1.9
**Last Updated:** 2026-08-11 (v8.6 design gate — Modal / Dialog Theming decision, ST-07)
**Header remediation note (v6.7 ST-03, shared_standards.md §9):** this document previously had no lifecycle header. Header applied now (version stamped at 1.0, reflecting no prior tracked version history) rather than backfilling an assumed version — content itself is unchanged by this remediation.
**v1.9 (ST-07, EPIC-03, v8.6, BLG-FE-150):** added the Modal / Dialog Theming subsection (§Shared UI Components) — confirms dark-only modal styling is unintentional legacy drift, not an intentional design choice; modals should use the shared theme-aware token set (`bg-background`/`text-foreground` or `bg-popover`/`text-popover-foreground`), matching `CommandDialog`'s already-correct reference implementation. Follow-up implementation item for the 4 known non-compliant consumers recommended for backlog filing (PMO Lead/Product Owner, outside this design gate's write scope). Design source: `docs/design/2026-08-11__release-v8.6/modal-light-theme-support/decision_record.md`.
**v1.8 (ST-10, EPIC-04, v8.5, BLG-FE-92):** added the empty-state microcopy pattern (§Shared UI Components → Cards → Data States) — heading/body wording and punctuation rules for `DataState`'s `empty` branch. The underlying component/layout mechanism was already consistently applied across the app; the gap was copy-tone consistency only. Design source: `docs/design/2026-08-08__release-v8.5/empty-state-microcopy-pattern/decision_record.md`.
**v1.7 (ST-12 + ST-13 + ST-21, EPIC-03 + EPIC-04, v8.3, BLG-FE-121 + BLG-FE-126 + BLG-SPEC-108):** added three new patterns, all genuinely new (no prior artefact existed for any of them): the `ConfirmationModal` shared component with an optional undo-window variant (§Shared UI Components → Confirmation Modal), a `Skeleton` loading-placeholder primitive and `DataState` `loadingVariant="skeleton"` prop (§Shared UI Components → Data States), and the canonical form-validation error-message pattern — trigger timing, placement, wording, and a corrected light-theme colour token closing a dark-only-token contrast gap found in two shipped instances (§Interaction States → Error States). Design sources: `docs/design/2026-08-05__release-v8.3/shared-confirmation-modal-undo-window/decision_record.md`, `docs/design/2026-08-05__release-v8.3/loading-skeleton-pattern/decision_record.md`, `docs/design/2026-08-05__release-v8.3/form-validation-error-message-pattern/decision_record.md`.
**v1.6 (ST-11, EPIC-11, v7.9, BLG-FE-130):** added a chart colour palette contrast checklist to §Accessibility — the existing WCAG contrast standard (v1.4) covered text and focus indicators but not chart data-ink. Documentation addendum only, no shipped UI change.
**v1.5 (ST-01, EPIC-01, v7.8, BLG-FE-128):** added optional `errorHeading`/`errorBody` props to `DataState` (§Shared UI Components → Cards → Data States) so a context needing a more specific error message (e.g. the What's New panel's "Unable to load release notes") can override the default "Something went wrong" copy without duplicating the shared error UI. Both default to the original strings — existing call sites unaffected. Design source: `docs/design/2026-07-24__release-v7.8/whats-new-panel/ux_spec.md`.
**v1.4 (ST-03 + ST-04, EPIC-03 + EPIC-04, v7.8, BLG-FE-127 + BLG-FE-125):** added the Focus Indicator contrast standard (§Hover & Focus States — ≥3:1 WCAG 1.4.11 threshold, previously unmeasured) for the EPIC-03 notification accessibility audit; and fixed scope/method for the EPIC-04 consolidated dark-mode contrast audit across all Base44-generated pages (§Accessibility). Both are audit-standard-setting entries — the audits themselves run during v7.8 sprint execution, findings recorded in each story's QA evidence. Design sources: `docs/design/2026-07-24__release-v7.8/notification-accessibility-audit/decision_record.md`, `docs/design/2026-07-24__release-v7.8/base44-dark-mode-contrast-audit/decision_record.md`.
**v1.3 (ST-04, EPIC-04, v7.7, BLG-FE-120):** added the `StandingAlert` / `StandingAlertStack` shared primitive (§Shared UI Components → Standing Alert) — a manually-dismissed, in-flow banner distinct from transient `sonner` toasts, for conditions requiring sustained user awareness until acknowledged. Enabler for `BLG-FE-116`'s future live custom-price-alert surfacing (integration point identified, not wired this cycle). Design source: `docs/design/2026-07-21__release-v7.7/standing-alert-component/ux_spec.md`.
**v1.2 (ST-01, EPIC-01, v7.5, BLG-FE-115):** formalised the `DataState` `inline` empty-state variant (§Shared UI Components → Cards → Data States) for compact-list contexts (e.g. the global command palette results list) where even the `compact` icon+heading+body stack is too tall. Generalises the decision approved for the command palette in `docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md` §2.5 (AC-06, per `docs/specs/blg_fe_115_pre_implementation_readiness_pass.md` §7).
**v1.1 (ST-04, EPIC-03, v7.2, BLG-SPEC-90):** formalised the `DataState` compact empty-state variant (§Shared UI Components → Cards → Data States) and defined primary vs secondary dashboard card treatment (§Shared UI Components → Cards → Card Hierarchy). Both generalise decisions already approved for `DashboardHome.js` in `docs/design/2026-07-15__release-v7.2/dashboard-empty-states/ux_spec.md` (ST-05) and `dashboard-briefing-hierarchy/ux_spec.md` (ST-06) so future cards/pages can reuse the same pattern without re-deriving it.

## Overview
The Design System defines the shared visual language, interaction patterns, and reusable UI elements for the Position Manager Web App. Its purpose is to ensure consistency, clarity, and accessibility across all pages and components.

---

## Theme & Colors

### Theme Modes
- Default theme: **Dark Mode**
- Optional: **Light Mode toggle** available in the header
- Theme preference is persisted locally so the user’s choice is retained on reload

### Color Usage
The original specification does not define hex values, but design intent indicates consistent usage:

- **Profit and loss colors**  
  - Positive values use a green/positive tone  
  - Negative values use a red/negative tone  

- **Status indicators**  
  - GRACE, PROFITABLE, and LOSING badges have distinct colors to differentiate positions  
  - Tags appear as visually distinct colored pills  

- **Error colors**  
  - Inline errors and error banners use a strong, high‑contrast color to remain visible in dark mode

- **Secondary/label text (canonical token, v6.7)**
  - Canonical class pair: `text-slate-600 dark:text-slate-400`
  - Use for all de-emphasised/label text (small `text-xs`/`text-sm` captions, sub-labels, muted values) that is not a status indicator, P&L value, or error
  - Contrast: `text-slate-400` = 5.71:1 vs `bg-slate-800` (dark, PASS); `text-slate-600` = 6.92:1 vs `bg-slate-100` (light, PASS) — both ≥4.5:1 WCAG-AA for normal-size text
  - Do not use a bare (non-`dark:`-paired) `text-slate-400` or `text-slate-500` value — Tailwind's `darkMode: ["class"]` strategy requires an explicit `dark:` variant to differ by theme; a bare class renders identically in both themes and will fail one of them
  - **Exception — elevated/compliance disclaimer text:** surfaces carrying §13 compliance-disclosure weight (e.g. AI Trade Advisor footer, Dashboard Advisory Label) may use a stronger-than-generic value for extra headroom on a compliance-sensitive surface (e.g. `text-slate-700 dark:text-slate-300`); do not collapse an existing elevated instance onto the generic token
  - Icon-only usages (Lucide icon `text-slate-*` classes, WCAG 1.4.11 non-text contrast) are governed separately and are not required to use this token
  - Design source: `docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md` §3, §4, §6 (BLG-FE-87/88/89)

---

## Typography

No explicit font tokens are defined, but the system consistently uses clear hierarchy across:

- Page titles  
- Section headers  
- Card titles  
- Form labels  
- Data values  

Form labels use consistent patterns such as:
- Title case  
- Required vs optional noted explicitly (e.g., “Exit Note (Optional)”)  
- Inline helper text or character counters where applicable (journal notes)

---

## Spacing & Layout Principles

### Global Layout
The UI follows a consistent structure across pages:

- **Header** with navigation links and theme toggle  
- **Footer** with version and support links  
- **Mobile‑first layout**, adapting upward to larger screens  

### Responsive Behavior
The layout adapts at standard breakpoints:

- Tables collapse into card layouts on mobile  
- Sidebar-style navigation condenses into a mobile menu where applicable  
- Modals become full‑screen on smaller devices  
- Forms stack vertically on narrow viewports  

### Page Composition
Common layout elements include:
- Summary cards (Dashboard, Trade History)  
- Tables (Positions, Trade History)  
- Cards with expandable sections (Journal views)  

Consistent spacing ensures readability and clarity between sections.

---

## Shared UI Components

### Buttons
Buttons follow consistent conventions across pages:

- **Primary actions:**  
  “Enter New Position”, “Confirm Exit”, “Save”, “Daily Monitor”

- **Secondary actions:**  
  “Edit Note”, “Edit Tags”, “Go to Positions”

- **Critical/destructive actions:**  
  Exit flows trigger modals with clear confirmation steps

Buttons include:
- Hover states  
- Disabled states when validation fails  
- Clear loading/error handling where relevant  

### Tables
Used primarily for Positions and Trade History:

- Columns include values such as ticker, prices, P&L, tags, exit reason  
- Support expandable rows for journals  
- Collapse into cards on mobile  

### Cards
Cards appear across:
- Grid view of positions  
- Journal view (open and closed positions)  
- Expandable rows in trade history  

Cards support:
- Title area (ticker/market)  
- Metrics (P&L, dates)  
- Tag display  
- Expand/collapse interactions  

### Data States

The shared `DataState` component (`src/components/ui/DataState.js`) is the canonical wrapper for API-backed content: `loading` → `error` → `empty` → children, evaluated in that priority order. Full-page and table contexts use the default sizing (`py-16` outer padding, `w-10 h-10` icon).

**Compact variant** — for content living inside a small grid card (e.g. a dashboard status card sharing a row with 2–3 siblings), pass `compact` to shrink the `empty` branch only; `loading` and `error` are unaffected by `compact`:

| Element | Default (`compact=false`) | `compact=true` |
|---------|---------------------------|-----------------|
| Outer padding | `py-16` | `py-4` |
| Icon size | `w-10 h-10` | `w-6 h-6` |
| Gap | `gap-3` | `gap-2` |
| Heading | `text-sm font-semibold` | `text-xs font-semibold` |
| Body | `text-xs` (unchanged) | `text-xs` (unchanged) |

A genuinely empty card (e.g. "no open positions") must render `DataState`'s `empty` branch (icon + heading + body) rather than a bare muted zero/blank line — this applies wherever the underlying value's absence is meaningful (contrast with a card whose zero is itself a valid data point, e.g. "0% portfolio heat", which is not an empty state and should render normally). Card-level `emptyAction` CTAs are optional and should generally be omitted when the card already has a click-through destination (e.g. the whole card links to `/Positions`) — a second CTA competes with that existing affordance. See `docs/design/2026-07-15__release-v7.2/dashboard-empty-states/ux_spec.md` for the worked example this pattern was generalised from.

**Inline variant** — for a compact-list context (e.g. the global command palette's results list, or any other single-line result row list) where even `compact`'s icon+heading+body stack is too tall for the surrounding component, pass `inline` to render `emptyHeading` (or `emptyBody` if no heading is given) alone as a single centered text line, no icon, no gap stack: `text-sm text-slate-600 dark:text-slate-400 text-center py-6`. `loading` and `error` are unaffected by `inline`. First used by the command palette's "No results for '{query}'." state (`src/components/CommandPalette.js`, via `cmdk`'s `CommandEmpty` — see `docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md` §2.5).

**Custom error copy (v1.5, ST-01, EPIC-01, v7.8, BLG-FE-128)** — pass `errorHeading`/`errorBody` to override the default "Something went wrong" / "Unable to load data. Please try again." text for a context where a more specific message is warranted. Both default to the original strings, so existing call sites render unchanged. First used by the What's New panel's "Unable to load release notes" error state (`src/components/dashboard/home/WhatsNewCard.js`).

**Empty-state microcopy pattern (v1.8, ST-10, EPIC-04, v8.5, BLG-FE-92)** — the `empty` branch's `emptyHeading`/`emptyBody` copy follows a shared wording pattern, distinct from the layout/sizing variants above:

- **Heading:** 2–5 words, sentence case, no trailing period (it's a label, not a sentence). Use `"No <noun>"` / `"No <noun> yet"` for content that accrues over time (notifications, positions, trade plans), or `"Your <noun> is empty"` for content the user actively curates (the watchlist).
- **Body:** exactly one sentence, present tense, states the concrete next action that would populate the view. Ends with a full stop.
- **Icon:** contextual to the content type, per existing call sites.

Design source: `docs/design/2026-08-08__release-v8.5/empty-state-microcopy-pattern/decision_record.md`.

**Skeleton loading variant (v1.7, ST-13, EPIC-03, v8.3, BLG-FE-126)** — pass `loadingVariant="skeleton"` (default remains `"spinner"`, unchanged) plus a `loadingSkeleton` node to render a content-shaped placeholder instead of the centered spinner for card-shaped async regions. Backing primitive: `src/components/ui/Skeleton.js` — a single rounded-rectangle `<div>` with `animate-pulse` (Tailwind default: `2s` ease, infinite), coloured `bg-slate-300/60 dark:bg-slate-700/60` (explicit light+dark pair — no dark-only token). Default card composition: 3 stacked bars (`h-4 w-3/5` title, `h-3 w-full` and `h-3 w-4/5` body lines, `gap-2`) — a starting point, not a mandate; a consumer may compose its own bar arrangement from the `Skeleton` primitive. Not retrofitted to any existing card this cycle — adoption is per-consumer. Design source: `docs/design/2026-08-05__release-v8.3/loading-skeleton-pattern/decision_record.md`.

### Card Hierarchy

Not all cards on a given page carry equal weight. Two treatment tiers apply:

- **Primary / intelligence-section cards** — cards presenting start-of-day or advisory intelligence rather than live position/portfolio status (e.g. a "briefing" section). These should be visually distinguished from the surrounding grid: an enclosing panel with an explicit (light+dark paired) background/border tint, a section label at `text-sm font-semibold` with a leading icon establishing a shared "intelligence section" visual language, distinct from the plain card shell below it. Related sections of this kind should share the same icon-and-label visual language even if their container treatment differs (e.g. one section already has strong inherent contrast via its own background), so a user recognises both as the same category of content at a glance.
- **Secondary / status cards** — cards presenting live, glanceable position/portfolio state (open positions count, heat level, grace period, signal status, recent activity). These use the plain shared card shell (`bg-slate-800/50 border border-slate-700/50`, no enclosing panel, no elevated label treatment) — the neutral default.

Any new background/border/label token introduced for a primary-tier treatment must ship as an explicit light+dark pair from the start, never a bare dark-only class — this project has twice shipped a dark-only-token-on-light-theme contrast defect (`BLG-FE-87/88`, `BLG-FE-95`). See `docs/design/2026-07-15__release-v7.2/dashboard-briefing-hierarchy/ux_spec.md` for the worked example this pattern was generalised from.

### Modal / Dialog Theming (v1.9, ST-07, EPIC-03, v8.6, BLG-FE-150)

Modals/dialogs are **not** an intentional dark-only exception — they follow the same light/dark theme-awareness as every other themed surface in the app. Use the shared `bg-background`/`text-foreground` token pair (or `bg-popover`/`text-popover-foreground` where a popover-elevation surface reads better than the page background) rather than hardcoded `bg-slate-900`/`text-white`.

**Canonical reference implementation:** `CommandDialog` (`src/components/ui/command.js`) — already uses the theme-aware token set correctly.

**Known non-compliant instances (pending their own follow-up implementation item — to be filed to the backlog separately, outside this design gate's write scope; not fixed by this decision alone):** `WatchlistModal.js`, `ExportModal.js`, `PositionEntryModal.js`, `WidgetLibrary.js` — found hardcoding `bg-slate-900 ... text-white` unconditionally at the v8.5 dark/light contrast audit (ST-13). Sequencing note: their conversion should not land before `bg-popover`/`text-popover-foreground` are registered in `tailwind.config.js` (this cycle's ST-04/BLG-FE-147), to avoid reproducing the "empty CSS rule" failure mode BLG-FE-147 exists to close.

Design source: `docs/design/2026-08-11__release-v8.6/modal-light-theme-support/decision_record.md`.

### Confirmation Modal (with optional undo window)

**Component:** `src/components/ui/ConfirmationModal.js` (v1.7, ST-12, EPIC-03, v8.3, BLG-FE-121) — shared reusable confirmation-modal component, extracted ahead of `BLG-FE-116`/`BLG-FE-117` to avoid near-duplicate implementations.

Props: `message` (required), `confirmLabel`/`cancelLabel` (default `"Confirm"`/`"Cancel"`), `destructive` (bool), `undoWindow` (`{ enabled, durationSeconds }`, default `{ enabled: false }`).

- **Standard variant** (`undoWindow.enabled = false`): Confirm executes on click, modal closes; Cancel dismisses without action. Formalises the existing shipped pattern (`positions.md` §Exit action, `watchlist.md` §Remove Confirmation Prompt) as the component default — no behaviour change for existing consumers migrating onto it.
- **Undo-window variant** (`undoWindow.enabled = true`): Confirm closes the modal and executes the action optimistically immediately (same optimistic-update precedent as "Mark Reviewed"/watchlist "Keep"); a `sonner` toast then shows the action's past-tense confirmation text plus an **"Undo (Ns)"** button whose label carries the countdown as text (never colour/shape alone). Default `durationSeconds = 5` — an explicit override of `sonner`'s ~4s auto-dismiss default, since this toast is actionable, not purely informational. Undo before expiry reverses the action and shows a brief `"Undone."` toast (default `sonner` duration); no click before expiry finalises the action silently.

Modal accessibility: focus trap + restoration (existing `Dialog` primitive convention), Escape = Cancel. Design source: `docs/design/2026-08-05__release-v8.3/shared-confirmation-modal-undo-window/decision_record.md`.

### Standing Alert

**Component:** `src/components/ui/StandingAlert.js` — exports `StandingAlert` (single banner) and `StandingAlertStack` (parent-owned array wrapper).

A condition requiring sustained user awareness until acknowledged is a distinct case from a transient toast (`sonner`):

| | Toast (`sonner`) | `StandingAlert` |
|---|---|---|
| Dismissal | Auto-dismiss (~4s) | Manual only (explicit ✕), or programmatic clear when the underlying condition resolves |
| Position | Floating, corner-anchored, overlays content | Inline banner, in document flow (does not overlay content) |
| Use case | Transient system feedback | Sustained condition requiring acknowledgement |
| Stacking | Library-managed stack | Parent-owned array; component renders what it's given |

**Layout:** full-width banner at the top of the page content area, below `PageHeader` and above primary content. Left-to-right: severity icon, message, optional action link, dismiss `✕` (right-aligned).

**Severity variants** (explicit light+dark pair, per Card Hierarchy precedent below — no dark-only token):

| Severity | Icon | Classes |
|----------|------|---------|
| Info | `Info` | `bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-950 dark:border-blue-800 dark:text-blue-200` |
| Warning | `AlertTriangle` | `bg-amber-50 border-amber-200 text-amber-800 dark:bg-amber-950 dark:border-amber-800 dark:text-amber-200` |
| Critical | `AlertOctagon` | `bg-red-50 border-red-200 text-red-800 dark:bg-red-950 dark:border-red-800 dark:text-red-200` |

**Stacking:** `StandingAlertStack` renders newest-first, vertically, capped at 3 visible; beyond that, a trailing "+N more" row expands the rest inline (no modal).

**Dismissal:** manual (`✕` → `onDismiss(id)`, optimistic removal, no undo) or programmatic (parent clears when the underlying condition resolves, same `onDismiss(id)` path). Not persisted across page reload — an in-session surface, distinct from the persisted Notification Feed row.

**Accessibility:** `role="alert"`, `aria-live="polite"` (Info/Warning) or `"assertive"` (Critical). Dismiss button has `aria-label="Dismiss alert"`.

**Integration point (identified, not wired this cycle):** the Notification Feed page (`/notifications`, top of content area, above the notification list) is the landing zone for `BLG-FE-116`'s future live-evaluation work — when implemented, a triggered custom price alert renders here as a `StandingAlert` in addition to (not instead of) the persisted Feed row.

### Inputs & Form Controls
Common input types used across multiple pages:

- **Number inputs** (shares, prices, ATR, FX rate) with decimal rules  
- **Date pickers** (entry date, exit date, transaction date)  
- **Text areas** with character counters for journal notes  
- **Tag input** with autocomplete, pill rendering, and removal  
- **Radio buttons** (for deposit/withdrawal)  
- **Dropdowns** (exit reason selection)

All follow shared validation rules defined in the system.

---

## Interaction States

### Hover & Focus States
- Cards and expandable sections respond visually on hover  
- Buttons show hover and focus states  
- Form fields show focus outlines for accessibility  

**Focus indicator contrast (v1.4, ST-03, EPIC-03, v7.8, BLG-FE-127):** any element receiving keyboard focus (buttons, dismiss controls, links, form fields) must render a focus indicator with ≥3:1 contrast against its immediately adjacent colour(s), per WCAG 2.1 SC 1.4.11 (Non-text Contrast), in both light and dark theme. The default browser/Tailwind `focus-visible` ring token satisfies this where the ring colour has not been overridden; any component with a custom focus style must be checked individually against this threshold. Design source: `docs/design/2026-07-24__release-v7.8/notification-accessibility-audit/decision_record.md`.

### Disabled States
Used when:
- Required fields are incomplete (e.g., Exit Price, FX Rate)  
- Validation rules fail (e.g., insufficient funds, invalid date)  

### Loading States
Used during:
- API data retrieval (Dashboard, Positions, Trade History, Journal)  
- Form submissions (Position Entry, Exit Modal, Cash Management)

### Error States
Errors appear consistently as:
- **Global error banner** for major API failures  
- **Inline field errors** for form-specific issues  
- Contextual messages (e.g., “Insufficient funds”, “FX rate required”)

**Canonical form-validation error-message pattern (v1.7, ST-21, EPIC-04, v8.3, BLG-SPEC-108)** — generalises two previously-divergent shipped instances (`WatchlistModal.js` submit-triggered, `TradePlan.js` blur-triggered) into one rule:
- **Trigger:** show a field's inline error when (a) the field has been blurred at least once and is currently invalid, **or** (b) a submit attempt has occurred, regardless of touched state. Clears immediately on the next input change that satisfies the rule.
- **Placement:** directly below the field, above any helper/example text, full field width, no icon.
- **Wording:** sentence case, ends with a period, plain language stating the violated rule (no backend/technical vocabulary); one message per field at a time.
- **Colour (v1.7):** `text-xs text-rose-700 dark:text-rose-400` — closes a dark-only-token gap present in both checked shipped instances (bare `text-rose-400`, no light-mode pair; same defect class as `BLG-FE-87/88/95`). `rose-700` measured 5.74:1 on `bg-slate-100` (light); `rose-600` measured 4.29:1, below the 4.5:1 AA threshold, so `rose-700` is used instead. `rose-400` on `bg-slate-800` (dark) measured 5.43:1, unchanged.

Design source: `docs/design/2026-08-05__release-v8.3/form-validation-error-message-pattern/decision_record.md`.

---

## Accessibility

The application adheres to core accessibility principles:

- Semantic HTML structure  
- Full keyboard navigation  
- Screen reader announcements for dynamic content  
- Color contrast meeting WCAG AA in both dark mode and light mode (v6.7 — secondary/label text now uses an explicit paired `dark:` class per theme; see §Color Usage "Secondary/label text" token)  
- **Consolidated dark-mode contrast audit (v1.4, ST-04, EPIC-04, v7.8, BLG-FE-125):** a systematic per-page dark-theme contrast pass across all Base44-generated pages runs this cycle, checking for the same dark-only/light-only token pairing defect class previously found twice (`BLG-FE-87/88`, `BLG-FE-95` — see §Card Hierarchy note below). Findings filed as a single consolidated backlog item, or fixed directly if trivial. Standard, scope and method fixed in `docs/design/2026-07-24__release-v7.8/base44-dark-mode-contrast-audit/decision_record.md`; results recorded in ST-04 QA evidence.
- Focus trapping and restoration in modals  
- ARIA labels where needed (tables, buttons, inputs)  
- **Chart colour palette contrast checklist (v1.6, ST-11, EPIC-11, v7.9, BLG-FE-130):** the WCAG contrast standard above covers text and focus indicators but not chart data-ink. For any new or modified chart (line, bar, area, heatmap, or other data-encoding colour use), confirm all of the following before shipping:
  - Each series/segment colour meets WCAG AA non-text contrast (≥3:1) against its immediate background, checked independently in both light mode and dark mode — a palette tuned for one theme does not automatically pass in the other (the same defect class as `BLG-FE-87/88/95/125`, but for chart fills/strokes rather than text).
  - No two adjacent series in the same chart rely on hue alone to be distinguished — pair colour with a second channel (position, pattern/dash style, or a direct label) so the chart remains legible for colour-vision-deficient users.
  - Any colour that also carries a semantic meaning elsewhere in the app (e.g. red = risk-off / loss, green = risk-on / profit) is used consistently in charts — do not introduce a chart-local palette that contradicts an existing status-colour convention.
  - Record the check (pass, or findings + fix) in the story's QA evidence log — the same location as other observable-AC staging/Playwright evidence.

---

## Consistency Rules

- Journal notes across the system share identical behaviors:
  - Optional  
  - Max 500 characters  
  - Character counter in editors  
  - Same inline editing pattern  

- Tag rules are consistent everywhere:
  - Lowercase only  
  - Hyphens and numbers allowed  
  - Max 20 characters per tag  
  - Max 10 tags per position  

- Forms across pages reuse consistent validation patterns:
  - Positive numeric values where appropriate  
  - Decimal place limits (e.g., shares, prices, FX rate)  
  - Date validity and ordering  
  - Error messages use consistent phrasing  

---

``
