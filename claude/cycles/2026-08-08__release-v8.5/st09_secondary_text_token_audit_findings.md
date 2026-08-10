Owner: Frontend Specifications & UX Documentation Owner
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-10
Cycle: 2026-08-08__release-v8.5
Story: ST-09 (BLG-FE-91, EPIC-04)

# ST-09 — Design Token Audit: v6.7 Contrast Fix Consistency

## 1. Purpose

Audit the codebase for drift against the canonical secondary-text token established by the v6.7 contrast remediation (`docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md`): **`text-slate-600 dark:text-slate-400`** (or the equivalent `isDark ? "text-slate-400" : "text-slate-600"` JS-ternary form used in `src/Layout.js`).

Per this story's AC and the sprint backlog's Notes ("Audit-only completion is a valid, complete outcome... any drift found is filed as a follow-up backlog item, not fixed in-story"), this document records findings only. No code was changed by this story.

## 2. Method

`grep`-based scan of `src/**/*.js` for:
1. Bare `text-slate-500` instances (the pre-v6.7 failing dark-theme value, BLG-FE-87) not paired with a `dark:` variant, filtered to exclude icon-component `className` usages (out of scope per the v6.7 decision record §5 — icon contrast is a separate WCAG criterion).
2. Bare `text-slate-400` instances with no `dark:`/light companion (the pre-v6.7 no-light-variant gap, BLG-FE-88), same icon-usage filter applied.
3. `dark:text-slate-500` usages — would indicate the *wrong* value was used for the dark-theme branch specifically (none found — see §4).

Icon-only usages (Lucide icon components such as `Loader2`, `ChevronDown/Up/Left/Right`, `Calendar`, `RefreshCw`, etc. carrying a `text-slate-*` class for `currentColor` fill/stroke) were excluded per the v6.7 decision record's explicit scope boundary — BLG-FE-87/88 ACs are scoped to "secondary/label **text**", not icons.

## 3. Findings

Six real drift instances found, all genuine text (not icon) elements, falling into two sub-classes:

### 3a. Wrong light-theme shade (uses the failing `text-slate-500` instead of canonical `text-slate-600`)

| File | Line | Current | Issue |
|------|------|---------|-------|
| `src/pages/Positions.js` | 591 | `text-slate-500 dark:text-slate-400` | Light value `text-slate-500` fails against `bg-slate-100` (4.34:1 < 4.5:1 per the v6.7 decision's own contrast table) — should be `text-slate-600` |
| `src/components/positions/PositionCard.js` | 127 | `text-slate-500 dark:text-slate-400` | Same issue — appears to be the same conditional class pattern duplicated between the page and its card component |
| `src/components/watchlist/WatchlistRow.js` | 27 | `text-xs text-slate-500 dark:text-slate-400` | Same issue |
| `src/Layout.js` | 573–575 | `isDark ? "...text-slate-400..." : "...text-slate-500..."` (command palette search-affordance button, "Search…" label) | Light branch uses `text-slate-500` instead of `text-slate-600` |
| `src/Layout.js` | 580–586 | `isDark ? "...text-slate-500" : "...text-slate-500"` (⌘K keyboard-shortcut `kbd` badge) | **Both branches** use `text-slate-500` — the dark branch is the exact pre-v6.7 failing value (3.07:1), never fixed for this element; the light branch also fails |

### 3b. Missing dark-theme variant entirely (bare `text-slate-500`, no split — the original BLG-FE-87 failure pattern, present on instances added or missed after v6.7)

| File | Line | Current | Issue |
|------|------|---------|-------|
| `src/pages/Reports.js` | 660 | `<p className="text-xs text-slate-500">` (reconciliation sign-off note) | No `dark:` variant at all — fails dark theme (3.07:1), same failure class as BLG-FE-87 |
| `src/components/dashboard/home/WhatsNewCard.js` | 56 | `<span className="text-slate-500 shrink-0">•</span>` (bullet marker) | No `dark:` variant; sibling `<li>` on the line above correctly uses the canonical pair — this bullet span was left out |
| `src/components/dashboard/home/WhatsNewCard.js` | 61 | `<li className="text-xs text-slate-500 pl-4">+{overflowCount} more</li>` | No `dark:` variant; same file's other list items use the canonical pair |

## 4. Non-findings

- No `dark:text-slate-500` usages found anywhere in `src/` — the dark-theme value is never wrong when a `dark:` variant is present at all; every drift instance is either a missing variant or a wrong *light*-theme value.
- `src/Layout.js`'s five other `isDark ? "text-slate-400" : "text-slate-600"` ternaries (lines 292, 311, 628, 664, 685) are correctly paired — not drift.
- Icon-component `text-slate-400`/`text-slate-500` usages (the large majority of raw grep hits, ~35 of 45 for `text-slate-500` alone) are explicitly out of scope per the v6.7 decision record and are not counted as drift here.

## 5. Disposition

Filed as `BLG-FE-149` (P3, consolidated — 6 instances across 2 sub-classes) per this story's AC. Not fixed in-story (audit-only completion, per sprint backlog Notes).
