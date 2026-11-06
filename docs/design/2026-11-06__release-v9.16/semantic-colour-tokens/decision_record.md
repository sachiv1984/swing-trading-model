**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-06__release-v9.16
**Stories:** ST-09 (EPIC-03, BLG-FE-264), ST-10 (EPIC-03, BLG-FE-223)

# Decision Record — Semantic Colour Tokens and Input Text Pairs

## 1. Problem

`src/index.css` sets `body` to `bg-slate-950 text-white` in both themes. `DashboardCard.js` and `ui/DataTable.js` use dark-only fills. In the light baselines, the Positions empty-state heading is invisible, RISK-ON badges can't be read, and the gate strip renders black. `src/` has 376 bare `text-white` and 331 bare `bg-slate-800/900` classes, which have been fixed one element at a time. Separately, several inputs use `placeholder:text-slate-600 dark:text-slate-400`. The `dark:` variant there styles the typed text, not the placeholder. Both stories change how text colour is chosen, so this record covers both.

## 2. Decision

### 2.1 Tokens: no new colours

Each token maps a role to the pair that `design_system.md` §Light-Theme Colour Tokens (v1.23) has already measured, so no contrast is re-derived. Tokens are CSS custom properties on `:root` (light) and `.dark` (dark) in `src/index.css`. They are exposed as Tailwind colours under an `app` namespace in `tailwind.config.js`, so they cannot collide with shadcn's existing `--background`, `--card` and `--border` variables.

| Token (Tailwind) | Role | Light | Dark |
|------------------|------|-------|------|
| `app-surface` | Page base (`body`) | slate-100 `#f1f5f9` | slate-950 `#020617` |
| `app-raised` | Card and table shell | white `#ffffff` | slate-800 at 50% `rgb(30 41 59 / 0.5)` |
| `app-fg` | Primary text: headings, figures, typed input text | slate-900 `#0f172a` | white `#ffffff` |
| `app-muted` | Secondary and label text | slate-600 `#475569` | slate-400 `#94a3b8` |
| `app-line` | Borders and dividers | slate-200 `#e2e8f0` | slate-700 at 50% `rgb(51 65 85 / 0.5)` |
| `app-positive` | Positive P&L and status | emerald-700 `#047857` | emerald-400 `#34d399` |
| `app-negative` | Negative P&L and status | rose-700 `#be123c` | rose-400 `#fb7185` |
| `app-warning` | Warning and information text | amber-700 `#b45309` | amber-400 `#fbbf24` |

- **Usage:** `bg-app-surface`, `bg-app-raised`, `text-app-fg`, `text-app-muted`, `border-app-line`, `text-app-positive` and so on. One class themes itself, so no `dark:` pair is written.
- **No opacity modifiers:** the values are full colours, so `bg-app-raised/70` isn't supported. A surface needing another alpha keeps an explicit pair.
- **v1.23 rule 2 still applies:** the positive and warning tokens pass only on white, slate-50 and slate-100. Don't put them on `slate-200`.
- **Filled badges** (v1.23 rule 4) keep their fixed, theme-independent fills. They are not tokenised.

### 2.2 Shells converted by the token story

| Shell | Change |
|-------|--------|
| `body` (`index.css`) | `bg-app-surface text-app-fg` |
| `DashboardCard` | `bg-app-raised border-app-line`. Title `text-app-fg`, sub-label `text-app-muted`. |
| `DataTable` | Container `bg-app-raised border-app-line`. Header cells `text-app-muted`, body cells `text-app-fg`, row dividers `border-app-line`. |
| `PageHeader` | Title `text-app-fg`, subtitle `text-app-muted` |

Content inside these shells is not swept here. That is Phase 3 (`BLG-FE-265`). Existing explicit pairs stay valid. New code uses the tokens for these eight roles.

### 2.3 Input text

Every text, number and search input, and every textarea, in `src/`:

- **Placeholder:** `placeholder:text-slate-600 dark:placeholder:text-slate-400`
- **Typed text:** `text-app-fg` if ST-09 has merged. Otherwise `text-slate-900 dark:text-white`, swapped for the token when ST-09 lands.
- **Grep check (ST-10 AC 1):** `grep -rnE 'placeholder:text-[a-z]+-[0-9]+ +dark:text-' src/` returns nothing.

## 3. §13 Compliance

Presentation only. No data or behaviour changes.

## 4. Frontend Spec Impact

- `design_system.md` v1.24 → v1.25: new §Semantic Colour Tokens (§2.1–2.2) and §Input Text Colours (§2.3), both under §Theme & Colors.

## 5. Obligations for Sprint Execution

- EPIC-03 merges after EPIC-01 and EPIC-02. Visual baselines are regenerated for both themes after that merge (RISK-03).
- If axe finds a `color-contrast` failure in content (not a shell) on one of the four AC pages, fix that element with an explicit pair. Do not widen the shell list.

## 6. Testability (CLAUDE.md §2)

- axe `color-contrast` in the light theme on Dashboard, Positions (empty and populated), Trade Plan and Settings (ST-09 AC 1).
- Visual baselines in both themes (ST-09 AC 2).
- The ST-10 grep check. A Playwright check that a typed value in one Trade Entry input computes to `rgb(255, 255, 255)` in dark and `rgb(15, 23, 42)` in light.

## 7. Approval

Head of UX & Design: Approved (agent-mediated, Design Gate Engine, 2026-11-06). Product Owner: Approved (the user, in session, 2026-11-06).
