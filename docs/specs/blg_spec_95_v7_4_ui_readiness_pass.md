**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-17
**Story:** ST-01 (BLG-SPEC-95, EPIC-01, v7.4)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# v7.4 UI Feature Readiness Pass

## 1. Purpose

Produce one consolidated pre-implementation readiness pass covering dependency pre-flight, UX specs, a design review, a Playwright baseline scope, an analytics event schema, and a CI tagging scheme for the four UI features removed from this cycle's Sprint Planning scope by `AMD-20260717-01` (command palette `BLG-FE-115`/EPIC-02, custom price alerts `BLG-FE-116`/EPIC-03, bulk actions `BLG-FE-117`/EPIC-04, saved filters + calendar `BLG-FE-118`/EPIC-05 — all Design Gate BLOCKED this cycle, no approved artefacts). This is a spec/scoping pass only — no shippable UI is produced or implied by this document. It is forward-looking preparation for whichever future release re-introduces those EPICs, per the amendment's own note (`amended_backlog_slice.md` line 45) that this story's acceptance criteria are unchanged and remain valid despite the scope reduction.

This document's 7 sections map 1:1 to the 7 acceptance-criteria bullets recorded against ST-01 in `amended_backlog_slice.md#ST-01` (informal AC-01…AC-07 mapping per `sprint_planning_notes.md`).

## 2. AC-01 — Dependency Pre-Flight

**`cmdk` (^1.1.1) added to `package.json`.** Closes the gap flagged by the predecessor v7.3 readiness pass (`docs/specs/blg_fe_115_pre_implementation_readiness_pass.md` §2 AC-01): `src/components/ui/command.js` already wraps `cmdk`'s primitives (`Command`, `CommandDialog`, `CommandInput`, `CommandList`, `CommandEmpty`, `CommandGroup`, `CommandItem`) but the package itself was never declared. Confirmed no API mismatch — `command.js`'s usage (`CommandPrimitive` import, `cmdk-group`/`cmdk-item` data-attribute selectors) matches the installed `cmdk` v1 API.

**`react-day-picker` (^10.0.1) added to `package.json`.** **Finding — breaking API mismatch (new, this pass):** `src/components/ui/calendar.js` already wraps `react-day-picker` (imported, unused by any page today — zero consumers confirmed via repo-wide grep) but is written against the **v8** `DayPicker` API: `classNames` keys `nav_button_previous`/`nav_button_next`/`day_range_start`/`day_range_end`/`day_outside`/`day_range_middle`, and a `components={{ IconLeft, IconRight }}` override. `react-day-picker` v9 (carried into the v10 line just installed) replaced this entire API surface — `IconLeft`/`IconRight` became a single `Chevron` component, and the `classNames` key set was renamed (e.g. `range_start`/`range_end`/`range_middle`/`outside`/`today`/`selected`/`disabled`/`hidden`, no `day_`-prefixed keys). `calendar.js` will not render correctly against the version now declared in `package.json` — none of its `classNames` overrides will match, and the `IconLeft`/`IconRight` override will be silently ignored.

**Recommendation:** pin `react-day-picker` at the current major (v10, actively maintained) rather than downgrading to the legacy v8 API `calendar.js` currently assumes — v8 is off the maintained line and the component has no live consumer today, so there is no production behaviour at risk in taking the version forward now. `calendar.js` must be rewritten against the v9+ API as a pre-implementation step for EPIC-05 (`BLG-FE-118`), before the saved-filters/calendar-view work begins — flagged forward as a backlog item (`BLG-FE-122`, filed alongside this pass) rather than fixed here, consistent with this pass's scope (readiness/scoping only, no shippable UI). This mirrors the pattern set by the v7.3 predecessor pass, which flagged the `cmdk`-package-json gap as "the first commit" of its consuming story rather than fixing it as part of the readiness pass itself — the difference here is the gap is a version-API mismatch rather than an absent declaration, so the flagged fix is a `calendar.js` rewrite, not a one-line install.

**Lockfile:** `package-lock.json` regenerated (`npm install --package-lock-only --legacy-peer-deps`) in the same commit as the `package.json` change, per AC-01's "added to `package.json` in this same pass" wording — both files are part of the same dependency-pre-flight deliverable.

## 3. AC-02 — UX Spec: Saved-Filters Empty State (EPIC-05) & Bulk-Actions Confirmation/Undo-Window Modal (EPIC-04)

### 3.1 Saved-Filters Empty State

Reuse the project's canonical `DataState` `empty` branch (`src/components/ui/DataState.js`) rather than a bespoke empty-state treatment — this is the documented pattern (`design_system.md` §Shared UI Components → Cards → Data States: "A genuinely empty card... must render `DataState`'s `empty` branch... rather than a bare muted zero/blank line").

| Element | Value |
|---|---|
| Icon | A "saved search / filter" glyph consistent with the `lucide-react` icon set already in use elsewhere (e.g. `ListFilter` or `BookmarkX`) — exact icon left to EPIC-05's implementation, no existing precedent to diverge from |
| Heading | "No saved filters yet" |
| Body | "Save your current filter settings to quickly reapply them later." |
| CTA (`emptyAction`) | "Save current filters" button, wired to the create-filter flow (EPIC-05's own scope) |
| Variant | `compact` (per `DataState`'s `compact` prop) — the saved-filters list is expected to render inside a dropdown/panel context (attached to a page's existing filter bar), not as a full-page card, so the default `py-16` padding would be disproportionate |

**Host page(s):** not fixed by this pass. `BLG-FE-118`'s own description ("saved filter presets and a calendar view") does not name which list surfaces (Watchlist, Trade Plans, Screener, or more than one) carry saved filters — left open for EPIC-05's own implementation-time scoping, consistent with the Design Gate record's note that "no page spec touched" applies to this readiness pass.

### 3.2 Bulk-Actions Confirmation/Undo-Window Modal

**Existing precedent reviewed:** `src/pages/TradePlans.js` (lines 205–229) implements a bespoke fixed-position delete-confirmation dialog (`AlertTriangle` icon, "This action cannot be undone" body copy, Cancel/Delete buttons) — a permanent, non-reversible confirmation pattern. A separate shadcn-style primitive, `src/components/ui/alert-dialog.js`, already exists in the codebase but is not the one `TradePlans.js` uses (its dialog predates that primitive's introduction — a minor duplication noted here, not in this pass's scope to fix).

**No existing undo-window precedent** was found — repo-wide grep for "undo" returns only `TradePlans.js`'s "cannot be undone" copy (the opposite pattern). `sonner` (`^2.0.7`, already a project dependency) natively supports an action-button toast (`toast(message, { action: { label, onClick } })`), which is the recommended implementation vehicle for the undo window — no new dependency is required.

**Cross-reference:** this same duplication risk is independently tracked by two already-filed backlog items — `BLG-FE-121` ("Extract a shared modal-confirmation component to de-dupe bulk-actions/alerts patterns") and `BLG-FE-120` ("Shared toast/notification primitive for alert-style UI"). This spec's recommendation (reuse `alert-dialog.js` for the confirm step, `sonner` for the undo toast) is consistent with both — EPIC-04's implementation should check whether `BLG-FE-121`'s shared component has landed before building a bespoke modal.

**Spec:**

1. **Confirm step (barrier), reversible actions skip it:** only irreversible or high-blast-radius bulk actions (e.g. bulk-delete of trade plans) show a confirmation modal before proceeding. Use `alert-dialog.js` (not a new bespoke modal) — standardising on the existing shared primitive rather than repeating `TradePlans.js`'s bespoke pattern. Reversible bulk actions (e.g. bulk status change, bulk add/remove watchlist membership) skip the modal entirely and go straight to step 2.
2. **Undo-window toast:** on confirm (or immediately, for reversible actions), the bulk mutation is **deferred** — an `alert-dialog.js`-triggered or direct `sonner` toast appears: "`{N}` items {action} — `[Undo]`", with a 5-second window (consistent with common undo-window convention). The action is committed only once the window elapses without an `Undo` click; clicking `Undo` cancels the pending mutation and dismisses the toast.
3. **Empty-state note:** not applicable to this modal — the modal only appears once ≥1 row is multi-selected, so there is no zero-state to design for here (contrast with §3.1's list-level empty state).

## 4. AC-03 — Design Review: Command-Palette Keyboard-Navigation Affordance (EPIC-02)

**Finding — no conflict with existing shortcuts, but the palette needs its own listener.** `src/Layout.js`'s global `keydown` handler (lines 205–223, "ST-11: Global keyboard shortcuts") explicitly bails on any modifier combination: `if (e.metaKey || e.ctrlKey || e.altKey) return;` (line 209), before dispatching its single-key shortcuts (`r`, `n`, `w`). This means `Cmd+K`/`Ctrl+K` passes through this handler untouched today — there is no collision with the existing shortcut map. However, it also means EPIC-02 **must register its own independent `keydown` listener** for the palette invocation; it cannot be added as a branch inside the existing `handleKeyDown` (which is scoped to non-modifier single-key shortcuts by design) without coupling two independently-scoped concerns.

**Escape / arrow / Enter behaviour:** no custom handling required — confirmed via `command.js` inspection: `CommandDialog` composes the existing `Dialog`/`DialogContent` primitives with `cmdk`'s `Command` wrapper, and `cmdk` provides arrow-key list navigation, `Enter`-to-select, and `Escape`-to-close natively.

**Discoverability affordance:** the predecessor v7.3 readiness pass (`blg_fe_115_pre_implementation_readiness_pass.md` §4 AC-03) already proposed a persistent top-nav-bar affordance (search icon + muted `⌘K`/`Ctrl K` badge, mouse-clickable fallback, first-session dismissible tooltip). This design review **confirms and endorses that plan** — it is visually consistent with the project's one existing keyboard-affordance precedent, the sidebar footer shortcut hints (`Layout.js`, covered by `tests/e2e/keyboard-shortcuts.spec.js` SC-KBD-09/SC-KBD-10 and `tests/e2e/visual-snapshots.spec.js` VS-10/VS-11). No changes to that plan are made here; this review's only new contribution is the listener-isolation finding above.

**Review outcome:** Approved — no blocking issues. One implementation note carried forward to EPIC-02: register the palette's `Cmd/Ctrl+K` listener independently of `Layout.js`'s existing `handleKeyDown`.

## 5. AC-04 — Playwright Visual-Regression Baseline Scope

**Established convention (confirmed, this pass):** although `playwright.config.js` configures `toHaveScreenshot` pixel-snapshot options (`snapshotDir: 'tests/e2e/__snapshots__'`, 2% diff tolerance), the committed suite does not use them — `tests/e2e/__snapshots__/` is empty, and the actual visual-regression test file, `tests/e2e/visual-snapshots.spec.js` (VS-01…VS-14), asserts CSS classes/attributes rather than comparing pixels ("converted to CSS assertions to ensure reliable cross-platform CI"). "Visual-regression baseline" in this codebase means the CSS-class-assertion pattern, not pixel diffing — the scope below follows that established convention.

| Surface (EPIC) | Scope | Target spec file (authored by the implementing EPIC) |
|---|---|---|
| Command palette (EPIC-02) | Dialog open/close state classes; selected-item highlight class; nav-bar discoverability badge classes (§4 above) | Extend `tests/e2e/visual-snapshots.spec.js`, or new `command-palette.spec.js` |
| Custom price alerts (EPIC-03) | Alert-state badge colour classes (active / triggered / dismissed); threshold-input validation state classes | New `price-alerts.spec.js` |
| Bulk actions (EPIC-04) | Multi-select toolbar visible/hidden classes; selected-row highlight class; confirm-modal classes; undo-window toast classes (§3.2 above) | New `bulk-actions.spec.js` |
| Saved filters / calendar (EPIC-05) | Saved-filters `DataState` empty-branch classes (§3.1 above); calendar day-cell selected/range/today classes — **written against the post-rewrite v9+ `classNames` key set** (§2 above), not the current v8-shaped `calendar.js` | New `saved-filters-calendar.spec.js` |

No test code is authored in this pass — there is no implementation yet to test against. Each of the four implementation EPICs owns authoring its own spec file against this scope when it ships, per the project's existing "spec files register automatically via glob, no manual inventory" convention (`playwright.yml` header comment).

## 6. AC-05 — Analytics Event Schema: Command-Palette Usage

**Metric definitions carried forward** from the predecessor v7.3 pass (`blg_fe_115_pre_implementation_readiness_pass.md` §5 AC-04): invocations/session, and search-to-navigation success rate. Re-confirmed this pass: the codebase still has no client-side analytics/event-logging pipeline (no `analytics.js`, no third-party event SDK declared in `package.json`).

**Event schema** (client-side-local; no new backend endpoint — consistent with the predecessor pass's AC-05 finding that command-palette v1 introduces no new API surface):

| Event | Trigger | Payload |
|---|---|---|
| `command_palette.open` | `Cmd/Ctrl+K` or nav-bar affordance click | `{ trigger: "keyboard" \| "click", timestamp }` |
| `command_palette.close` | `Escape`, click-away, or a selection was made | `{ reason: "escape" \| "click_away" \| "selection", timestamp }` |
| `command_palette.select` | `Enter` or click on a result item | `{ result_type: "page" \| "entity", result_key, query_length, timestamp }` |

**Storage:** local-only counters via the existing `BLG-FE-40` versioned-localStorage-envelope pattern, confirming the predecessor pass's option (a) recommendation as this schema's storage target. No backend metrics endpoint is scoped by this pass; if a future need for cross-session/cross-device aggregation arises, that is EPIC-02's own follow-on scoping decision (per the predecessor pass's option (b)), not decided here.

## 7. AC-06 — Regression-Suite CI Tagging Scheme

**Current state:** `.github/workflows/playwright.yml` runs the entire glob-discovered `tests/e2e/**/*.spec.js` suite unconditionally (`npx playwright test`, no filter), gated by a path filter on push/PR. `.github/workflows/smoke-tests.yml` runs one fixed spec file. Neither workflow uses tag-based filtering. `@playwright/test` (`^1.58.2`, already installed) supports native test tagging (the `tag` option on `test()`/`test.describe()`, available since Playwright 1.42) — unused in this repo today.

**Scheme:** each of the four spec files scoped in §5 (AC-04) above should tag its top-level `test.describe()` block with `{ tag: '@v7.4' }`. This enables `npx playwright test --grep @v7.4` as an opt-in scoped-subset run — for local developer iteration on v7.4-surface work, or a future PR-scoped CI job — without modifying `playwright.yml`'s existing full-suite gate, which must keep running every spec regardless of tag (narrowing the blocking gate's coverage is out of scope for a CI tagging convenience feature).

**Naming convention:** `@v<release>`, one tag per release cycle (e.g. `@v7.4`), applied only to new spec files introduced by that release's own EPICs. Retrofitting tags onto the ~pre-existing untagged spec files in `tests/e2e/` is out of scope for this pass.

**No workflow file is modified by this pass** — none of the four spec files exist yet to tag. This section defines the scheme; each implementing EPIC applies it when authoring its spec file (§5 above).

## 8. AC-07 — Consolidated Document

This document is the AC-07 deliverable: one file consolidating AC-01 through AC-06, to be referenced by EPIC-02/03/04/05's future implementation stories as their shared readiness baseline — the same referencing role the four separate v7.3 predecessor documents (`docs/specs/blg_fe_11{5,6,7,8}_pre_implementation_readiness_pass.md`) served for their respective stories, collapsed here into a single file since `AMD-20260717-01` reduced this cycle's shippable EPIC count to zero.

## 9. Scope Completeness Summary

All 7 acceptance criteria addressed: AC-01 (dependencies added to `package.json` + lockfile; new breaking-version finding flagged forward as `BLG-FE-122`), AC-02 (both UX specs delivered — saved-filters empty state and bulk-actions confirm/undo modal), AC-03 (design review delivered — no conflict found, one listener-isolation implementation note), AC-04 (Playwright baseline scope defined for all 4 surfaces, per the codebase's established CSS-assertion convention), AC-05 (analytics event schema delivered, building on the predecessor pass's metric definitions), AC-06 (CI tagging scheme defined, no workflow files touched), AC-07 (this document itself). `BLG-FE-122` (calendar.js react-day-picker v9+ rewrite) filed to `claude/backlog/backlog.md` in this same pass — a genuine pre-implementation blocker for EPIC-05 discovered during AC-01, not present in the original scope.

## 10. Known Deviations

None. This is a net-new readiness/confirmation artefact; no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-17 | 1.0 | Initial consolidated readiness pass (ST-01, EPIC-01, v7.4) |
