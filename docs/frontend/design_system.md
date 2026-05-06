**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2) — Living Reference
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-06
**Source:** BLG-FE-21 (v3.2 ST-14)
**Depends on:** docs/frontend/component_inventory.md (v1.0)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Design System

**Purpose:** Document the current design system as-is: colour palette, typography, spacing conventions, icon set, and known inconsistencies. This is a descriptive capture of actual patterns, not an aspirational style guide.

**Maintenance Obligation:** This document is a mandatory living reference. It must be updated whenever the colour palette, typography scale, spacing tokens, or icon conventions change during Arc 2 development. Update this document in the same PR as the change.

---

## Cross-Reference

Component usage details: see [component_inventory.md](component_inventory.md).

---

## 1. Colour Palette

The app uses Tailwind CSS with a dark-first palette built on `slate` (neutral), with semantic accent colours.

### 1.1 Backgrounds

| Role | Tailwind Class | Hex (approx) | Usage |
|------|---------------|--------------|-------|
| Primary background | `bg-slate-950` / `bg-slate-900` | `#020617` / `#0f172a` | Page background, card base |
| Card surface | `bg-slate-900` → `bg-slate-800` (gradient) | `#0f172a` → `#1e293b` | `rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800` — standard card pattern |
| Elevated surface | `bg-slate-800` | `#1e293b` | Modals, popovers, inline panels |
| Input field | `bg-slate-800` | `#1e293b` | Text inputs, textareas, selects |
| Subtle fill | `bg-slate-700/50` | 50% opacity | Skeleton loaders, muted chips |
| Dark overlay | `bg-slate-900/40` | 40% opacity | Inline sub-row backgrounds (Screener news row) |

### 1.2 Text

| Role | Tailwind Class | Usage |
|------|---------------|-------|
| Primary text | `text-white` | Headings, primary data values |
| Secondary text | `text-slate-200` | Sub-values, table body |
| Muted text | `text-slate-300` | Normal table cells |
| Dimmed text | `text-slate-400` | Labels, metadata |
| Faded text | `text-slate-500` | Timestamps, secondary labels, empty states |
| Very faded | `text-slate-600` | Placeholder indicators, loading ellipsis |

**Heading gradient (PageHeader):** `bg-gradient-to-r from-slate-900 via-slate-700 to-slate-500 dark:from-white dark:to-slate-400 bg-clip-text text-transparent` — applied to `<h1>` via PageHeader component.

### 1.3 Semantic Accent Colours

| Semantic Role | Primary | Muted Fill | Border | Text |
|--------------|---------|-----------|--------|------|
| Positive / active / success | emerald-500 | `bg-emerald-500/20` | `border-emerald-500/30` | `text-emerald-400` |
| Warning / caution / watch | amber-500 | `bg-amber-500/20` | `border-amber-500/30` | `text-amber-400` |
| Danger / error / stop | red-500 / rose-500 | `bg-red-500/10` / `bg-rose-500/20` | `border-red-500/30` | `text-red-400` / `text-rose-400` |
| Info / link / primary action | cyan-500 | `bg-cyan-500/20` | `border-cyan-500/30` | `text-cyan-400` |
| Secondary action / brand | violet-500 | `bg-violet-500/20` | `border-violet-500/30` | `text-violet-400` |
| US market badge | violet-500 | `bg-violet-500/20` | `border-violet-500/30` | `text-violet-400` |
| UK market badge | blue-500 | `bg-blue-500/20` | `border-blue-500/30` | `text-blue-400` |
| Neutral / no-signal | slate-700 | `bg-slate-700/50` | `border-slate-600/30` | `text-slate-400` |

### 1.4 Primary CTA Gradient

Standard CTA button background (used on Add, Save, Create):
```
bg-gradient-to-r from-cyan-500 to-violet-500
hover:from-cyan-400 hover:to-violet-400
text-white border-0
```
Shadow accent (optional): `shadow-lg shadow-violet-500/25`

### 1.5 Portfolio Heat Colours

| Range | Colour |
|-------|--------|
| < 15% | `text-emerald-400` (green — safe) |
| 15–25% | `text-amber-400` (amber — caution) |
| > 25% | `text-red-400` (red — high) |

### 1.6 Inconsistencies

- Error states use both `red-500` and `rose-500` variants inconsistently. `red-500` is the normalised choice going forward (rose used in delete/danger confirmations only).
- `bg-gradient-to-br from-slate-900 to-slate-800` is the canonical card background but some older views use flat `bg-slate-800`. Harmonise in Arc 2.

---

## 2. Typography Scale

Built on Tailwind's default scale. No custom font families — system font stack.

| Level | Class | Typical Context |
|-------|-------|----------------|
| Page title (H1) | `text-2xl font-bold` + gradient clip | PageHeader component |
| Section heading | `text-lg font-semibold text-white` | Card section titles |
| Region label | `text-xs font-medium text-slate-400 uppercase tracking-wider` | Region labels within cards (e.g. "Price & Signal") |
| Table header | `text-xs font-medium text-slate-400 uppercase tracking-wider` | `<th>` cells |
| Body / label | `text-sm` | General text, field labels (via `text-xs text-slate-400`) |
| Data value (prominent) | `text-xl font-semibold text-white` | Primary metric (price, heat %) |
| Data value (normal) | `text-sm text-slate-200` | Secondary metric |
| Chip / badge | `text-xs font-medium` | Signal/status badges |
| Monospace ticker | `font-mono font-medium text-white` | Ticker symbols in tables |
| Muted caption | `text-xs text-slate-500` | Timestamps, source names |

---

## 3. Spacing Conventions

### 3.1 Layout Spacing

| Element | Pattern |
|---------|---------|
| Page content wrapper | `space-y-6` between major sections |
| Card internal padding | `p-6` (standard), `p-4` (compact), `px-5 py-4` (table cells) |
| Section header margin | `mb-4` below region label heading |
| Table cell padding | `px-5 py-4` (Watchlist), `px-3 py-3` (Screener — compact) |
| Grid gaps | `gap-4` (form fields), `gap-6` (metric pairs) |
| Flex gaps | `gap-2` (button groups), `gap-3` (action rows) |

### 3.2 Border Radius

| Element | Class |
|---------|-------|
| Card container | `rounded-2xl` |
| Inline panel / sub-row | `rounded-xl` or `rounded-lg` |
| Button | `rounded-lg` (via shadcn default) |
| Badge / chip | `rounded-full` |
| Input field | `rounded-lg` |
| Table container | `rounded-lg` |

### 3.3 Border Style

Standard card border: `border border-slate-700/50` — 50% opacity to soften.
Standard input border: `border border-slate-700` with focus `focus:border-cyan-500`.
Error border: `border border-red-500/30`.

---

## 4. Icon Set

All icons are from [lucide-react](https://lucide.dev/). No other icon libraries in use.

### 4.1 Icon Sizing Conventions

| Context | Class |
|---------|-------|
| Inline with text (button, badge) | `w-3 h-3` |
| Standard UI icon | `w-4 h-4` |
| Section icon / card icon | `w-5 h-5` |
| Empty state illustration | `w-10 h-10 text-slate-600` |

### 4.2 Icons in Active Use

| Icon | Used In | Semantic Role |
|------|---------|--------------|
| `ArrowLeft` | TradePlan, Research | Back navigation |
| `Save` | TradePlan | Save action |
| `BookOpen` | TradePlan (imported but not rendered currently) | Trade plan concept |
| `Plus` | Watchlist, Screener | Add action |
| `Trash2` | Watchlist | Delete action |
| `Eye` | Watchlist | View / watchlist empty state |
| `Newspaper` | Screener, Watchlist | News headlines |
| `ChevronDown`, `ChevronUp` | Screener, Watchlist | Expand/collapse, sort direction |
| `RefreshCw` | Screener | Refresh/re-scan |
| `Search` | Screener | Search / filter |
| `Loader2` | Screener | Spinner (animate-spin) |
| `Check` | Screener | Added to watchlist confirmation |
| `X` | Screener | Close / dismiss |
| `TrendingUp`, `TrendingDown` | Research | Price change direction |
| `Loader2` | Various | Loading spinner pattern |
| `AlertCircle` | DataState | Error state |
| `Info` | StatsCard | Tooltip trigger |

### 4.3 Inconsistencies

- `BookOpen` is imported in TradePlan.js but not used in any rendered JSX — clean up.
- Spinner pattern uses `Loader2 animate-spin` consistently — maintain this.

---

## 5. Animation

| Pattern | Library | Usage |
|---------|---------|-------|
| Page header fade-in-down | Framer Motion (`motion.div`, `initial/animate`) | PageHeader only |
| Watchlist row fade-out on remove | Tailwind `transition-all duration-200` + `opacity-0` | Watchlist.js `removing` state |
| Loading skeletons | Tailwind `animate-pulse` on `bg-slate-700/50` elements | DataState, Research.js |
| Button hover | Tailwind `transition-colors` | Inline buttons throughout |

Framer Motion is used only in `PageHeader.js`. All other animations are Tailwind utility classes.

---

## 6. Dark Mode

The app is dark-only in practice. Light mode is partially scaffolded via Tailwind's `dark:` prefix in `PageHeader.js` but no light theme is implemented elsewhere. Arc 2 should not assume light mode support.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-06 | Initial design system document. v3.2 ST-14 (BLG-FE-21). Captures current patterns at start of Arc 2 Sprint 2. |
