**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-16__release-v9.13
**Story:** ST-25 (EPIC-04, BLG-FE-221)

# Decision Record — Coloured Button Fills Render as Authored, at AA Contrast

## 1. Problem

`cn()` is plain `clsx`, so a `<Button className="bg-emerald-600 …">` keeps the default variant's `bg-primary` as well. Which one wins depends on where each utility lands in the built CSS, not on intent. In the current build (`build/static/css/main.8db847bf.css`):

| Utility | Offset | Beats `bg-primary` (30590)? |
|---------|--------|-----------------------------|
| `bg-amber-700` | 26869 | No (v9.12 used `!bg-` to force it) |
| `bg-emerald-600` | 29240 | **No** |
| `bg-red-600` | 31073 | Yes |
| `bg-rose-600` | 31625 | Yes |
| `bg-slate-800` | 33074 | Yes |
| `bg-slate-800/50` | 33365 | Yes |

Adding or removing any class can reorder this. The fix (`tailwind-merge` in `cn()`, or a no-background variant) makes the authored fill always win. That changes what some buttons show, so the authored fills must themselves pass.

## 2. Decision

### 2.1 Rule

A `<Button>` with a colour fill renders **that fill with `text-white`**, and both its rest and hover fills meet **4.5:1** against white text (`text-sm`/`text-xs` button labels are normal-size text). This applies whichever mechanism ST-25 picks. A coloured button never relies on the variant's `text-primary-foreground`, because that is near-black in dark theme.

White text on each fill:

| Fill | Contrast | Use |
|------|----------|-----|
| `emerald-600` | 3.77 | Not allowed |
| `emerald-700` | 5.48 | Positive action rest |
| `emerald-800` | 7.68 | Positive action hover |
| `rose-500` | 3.67 | Not allowed (current hover on 7 sites) |
| `rose-600` | 4.70 | Destructive action rest (unchanged) |
| `rose-700` | 6.29 | Destructive action hover |
| `red-600` / `red-700` | 4.83 / 6.47 | Unchanged |
| `amber-700` / `amber-800` | 5.02 / 7.09 | Unchanged; the `!` is dropped |
| `slate-800` / `slate-700` | 14.63 / 10.35 | Unchanged; `text-white` added |

### 2.2 Sites (audited 2026-10-16, every `<Button>` with a colour `bg-*`)

| Site | Today renders | After |
|------|---------------|-------|
| `Screener.js` ~329 "Add to Watchlist" | `bg-primary` | `bg-emerald-700 hover:bg-emerald-800 text-white` |
| `Screener.js` ~1065 "Run Screener" (empty state) | `bg-primary` | `bg-emerald-700 hover:bg-emerald-800 text-white` |
| `CashManagementModal.js` ~117 submit (deposit / withdraw) | `bg-primary` (deposit); rose (withdraw) | deposit `bg-emerald-700 hover:bg-emerald-800`, withdraw `bg-rose-600 hover:bg-rose-700`, both `text-white` |
| `TradePlan.js` ~1298 "Abandon Plan" | amber-700 via `!` | `bg-amber-700 hover:bg-amber-800 text-white`, with no `!` |
| `TradePlans.js` ~382, `ExitModal.js` ~501, `MonitorModal.js` ~167, `BulkActionToolbar.js` ~219, `SavedFiltersControl.js` ~160, `WatchlistDeleteConfirm.js` ~13, `CustomPriceAlertsSection.js` ~225 | rose-600 | rose-600 rest unchanged; hover `rose-500` → `rose-700` |
| `Research.js` ~146 | red-600 | Unchanged |
| `SystemStatus.js` ~296 "Refresh Health" | slate-800 with near-black text in dark theme | add `text-white` |

The outline and ghost buttons with a translucent slate fill (`bg-slate-800/50`, `bg-slate-700/50`) already render that fill today (see §1). They are visually unchanged and not in this table.

### 2.3 Why emerald moves to 700

Making `bg-emerald-600` finally render would ship white-on-emerald at 3.77:1, a new AA failure. `emerald-700` is the design system's positive-colour token (`design_system.md` §Light-Theme Colour Tokens), so the change aligns with it.

## 3. §13 Compliance

Visual only.

## 4. Frontend Spec Impact

- `screener_results.md` v1.9 → v1.10: the two Screener buttons' fills.
- `components/cash_management_modal.md` v1.2 → v1.3: submit-button fills.
- `design_system.md` (Class 1) is outside this gate's write scope. ST-25 adds §2.1's rule under §Shared UI Components → Button in-story.
- Destructive-button hover is not specified in any page spec, so §2.2 is the record for the rose sites.

## 5. Testability (CLAUDE.md §2)

- Playwright `toHaveCSS('background-color', …)` for Screener "Add to Watchlist" and "Run Screener" (emerald-700, `rgb(4, 120, 87)`), TradePlans ~382 (rose-600, `rgb(225, 29, 72)`) and Trade Plan "Abandon Plan" (amber-700, `rgb(180, 83, 9)`), in both themes. This is the AC 2 list, with emerald-700 replacing emerald-600 (see addendum).
- A scoped axe scan on the same buttons reports no `color-contrast` violation.
- `grep -rn '!bg-' src/` returns no match (AC 1).

## 6. Approval

Head of UX & Design: confirmed, 2026-10-16.
Product Owner: confirmed, 2026-10-16.
