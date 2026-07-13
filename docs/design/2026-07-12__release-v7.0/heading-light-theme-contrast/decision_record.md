**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-12
**Approved by:** Product Owner — 2026-07-12
**Story:** ST-08 — Dashboard/StrategyBenchmark page-title light-theme contrast gap (BLG-FE-95)
**Cycle:** 2026-07-12__release-v7.0

---

# UX Decision Record — Primary Page-Title Light-Theme Companion Value

## 1. Problem

Two primary page-title headings use a bare `text-white` class with no light-theme companion:

- `src/pages/DashboardHome.js:36` — `<h1 className="text-2xl font-bold text-white tracking-tight">Dashboard</h1>`
- `src/pages/StrategyBenchmark.js:497` — `<h1 className="text-lg font-semibold text-white">Strategy Benchmark</h1>`

On light theme (`bg-slate-100`, per `Layout.js` line 341 root container), white text is effectively invisible (~1.1:1 contrast) — same defect class as BLG-FE-87/88, which fixed the equivalent gap for *secondary* text (`text-slate-400/500` → paired with `text-slate-600 dark:text-slate-400`, locked into `design_system.md` v1.0 as BLG-FE-89). No equivalent token exists yet for *primary* heading text — this decision establishes it.

## 2. Decision

Reuse the value already established elsewhere in the codebase for primary text on the light surface — `Layout.js` line 447 already pairs `isDark ? "text-white" : "text-slate-900"` for the app's primary nav/brand text. Apply the same pairing via Tailwind's `dark:` variant to both headings:

```
text-slate-900 dark:text-white
```

| Surface | Value | Contrast |
|---|---|---|
| Light (`bg-slate-100`) | `text-slate-900` | ≈17.9:1 — passes WCAG AAA |
| Dark (`bg-slate-950`/`bg-slate-900`) | `text-white` (unchanged) | ≈19:1 — passes WCAG AAA, no regression |

No new colour introduced — this is the same `slate-900`/`white` pair the app already uses for primary text elsewhere, applied consistently rather than inventing a new token.

## 3. Scope

- `DashboardHome.js:36` and `StrategyBenchmark.js:497` only, per the story's named ACs.
- No layout, sizing, or weight change — `text-2xl font-bold` / `text-lg font-semibold` classes untouched, only the colour utility changes.
- Dashboard's `PageHeader`-driven title (`Dashboard.js` via `src/components/ui/PageHeader.js`) is **not** in scope — it already uses a theme-aware gradient (`dark:from-white ... from-slate-900 ...`) and is unaffected by this defect.

## 4. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-12
- **Product Owner:** Approved — 2026-07-12
