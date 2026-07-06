**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-06
**Cycle:** 2026-07-04__release-v6.6

# Colour Contrast Audit Findings — ST-01 (BLG-FE-82)

## Scope and Method

BLG-UX-01/02 (v6.4) fixed two AI-disclaimer surfaces found via ad hoc review. This story's mandate (AC-01) is a *systematic* sweep app-wide, not a spot-check.

**Method:** Static/class-based contrast analysis rather than a live rendered-pixel review:

1. Enumerated every use of the secondary-text Tailwind utility classes conventionally used for de-emphasised/label text (`text-slate-400`, `text-slate-500`, plus the `gray`/`zinc`/`neutral`/`stone` 400/500 equivalents — none of the latter four families are actually used in this codebase) across `src/pages/` and `src/components/`.
2. Resolved each class to its documented Tailwind v3 default-palette hex value.
3. Identified the actual background surfaces these render against, confirmed from `src/Layout.js` (the shell background swaps `bg-slate-950` (dark, default theme) / `bg-slate-100` (light theme) via a real, user-facing `toggleTheme` control, persisted to `localStorage`, default `"dark"`) and from spot-checked page/component wrappers (e.g. `src/pages/Screener.js`, `src/pages/RedFlagJournal.js` — both render content directly on the ambient shell background with no card wrapper).
4. Computed WCAG 2.1 contrast ratios (standard relative-luminance formula) for each text/background pairing actually in use, treating all found instances as normal-size text (WCAG's 3:1 "large text" allowance requires ≥18pt regular or ≥14pt bold; virtually every instance found is `text-xs`/`text-sm`, i.e. 12–14px regular, so the 4.5:1 threshold applies throughout).
5. Cross-checked the methodology against the two known-good precedent fixes (`BLG-UX-01`: `text-slate-500`→`text-slate-300`; `BLG-UX-02`: `text-slate-600`→`text-slate-400`) — both are dark-theme-only fixes, which is itself a finding (see Finding 2).

**Not done:** a live browser pass toggling every page through both themes pixel-by-pixel. The class-based method is standard practice for a source-level accessibility audit and is considered sufficient for AC-01; a visual QA pass is recommended as part of implementing the resulting fix items (BLG-FE-87/88), not as part of this audit-only story (whose design-gate classification is "Design Not Applicable" precisely because it ships a findings report, not a UI change).

## Findings

### Finding 1 (P1) — `text-slate-500` fails WCAG-AA against the app's default (dark) theme, today

262 instances across ~90 files use bare `text-slate-500` (#64748b) for small secondary/label text against dark surface backgrounds (`bg-slate-950` #020617, `bg-slate-900` #0f172a, `bg-slate-800` #1e293b):

| Background | Ratio | Normal text (4.5:1) |
|---|---|---|
| `bg-slate-950` | 4.24 | FAIL |
| `bg-slate-900` | 3.75 | FAIL |
| `bg-slate-800` | 3.07 | FAIL |

This is the app's default theme — visible today to any user who has not toggled to light mode. Same defect class as `BLG-UX-01`, recurring at scale. Filed as **BLG-FE-87** (P1).

### Finding 2 (P2) — Secondary text has never been contrast-audited against the light theme

764 instances (502 `text-slate-400`, 262 `text-slate-500`) across 102 files carry no `dark:text-*` companion class and no `isDark` conditional — meaning the same literal colour renders in both themes (Tailwind's `darkMode: ["class"]` strategy requires an explicit `dark:` variant to differ by theme; a bare class does not adapt). Computed against light-theme surfaces:

| Text class | vs `white` | vs `bg-slate-50` | vs `bg-slate-100` |
|---|---|---|---|
| `text-slate-400` | 2.56 FAIL | 2.45 FAIL | 2.34 FAIL |
| `text-slate-500` | 4.76 PASS | 4.55 PASS | 4.34 FAIL |

`text-slate-400` — otherwise the "safe" dark-theme shade — fails badly in light mode (as low as 2.34:1, below even the 3:1 large-text floor). Both precedent fixes (`BLG-UX-01`, `BLG-UX-02`) only corrected the dark-theme case and introduced no light-theme variant, confirming light theme has never been audited here. A naive fix to Finding 1 that lands on `text-slate-400` would not resolve — and could reintroduce — this failure. Filed as **BLG-FE-88** (P2, sequenced after BLG-FE-87).

### Finding 3 (P3) — No shared token/component for secondary text

Three independent contrast defects (`BLG-UX-01`, `BLG-UX-02`, and Findings 1–2 above) share one root cause: secondary-text colour is chosen ad hoc per component, with nothing enforcing a WCAG-AA-safe value per theme. Filed as **BLG-FE-89** (P3) — generalises the existing `AiDisclaimer` shared-component idea app-wide.

## Reference Data

Full raw match list (file:line for all 757 grep hits used as the audit's starting index) is not attached to this document to keep it reviewable; it is reproducible via:

```
grep -rnE "text-(slate|gray|zinc|neutral|stone)-(400|500)\b" src/pages src/components
```

Top files by instance count (candidate remediation order for BLG-FE-87/88): `SystemStatus.js` (42), `Screener.js` (35), `Reports.js` (33), `TradeEntry.js` (31), `Research.js` (30), `StrategyBenchmark.js` (27), `Settings.js` (25), `TradePlan.js` (23), `ExitModal.js` (21), `Positions.js` (20).

## Follow-Up Backlog Items Filed

- `BLG-FE-87` (P1) — App-wide secondary-text contrast failure against dark theme (default theme)
- `BLG-FE-88` (P2) — App-wide secondary-text contrast failure against light theme (missing dark:/light: variants)
- `BLG-FE-89` (P3) — Shared secondary-text design token/component

No in-story fixes were made — per this story's "Design Not Applicable" design-gate classification and AC-02, findings are documented and filed as follow-ups, not remediated here.

## Sign-Off

**Signed off by:** Head of UX & Design
**Date:** 2026-07-06
**Disposition:** Audit complete. AC-01 (systematic audit completed), AC-02 (findings documented, 3 follow-up items filed: BLG-FE-87/88/89), AC-03 (this sign-off) all met.
