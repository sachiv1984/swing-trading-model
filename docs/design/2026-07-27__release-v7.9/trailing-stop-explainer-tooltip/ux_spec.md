**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-27
**Cycle:** 2026-07-27__release-v7.9
**Backlog source:** BLG-FEAT-87
**Maps to:** EPIC-05, S2-05

---

# UX Spec — "Why Is My Stop Moving" Explainer Tooltip

## 1. Problem

The trailing-stop framework (`strategy_rules.md` §7) has non-obvious profit-aware logic (§7.2) and a hard stop-movement constraint (§7.3), but neither is explained anywhere in the trade UI. Users see the Trail Stop value and BREACH badge (`positions.md` §Trailing Stop Column) change over time with no in-app explanation of why.

## 2. Placement

An info icon (`ⓘ`, `w-3.5 h-3.5`, muted) placed immediately after the "Trail Stop" column header text, Table View (`positions.md` §Trailing Stop Column). Grid View: same icon after the "Trail Stop" stat label in the card summary. Hover or focus (keyboard-accessible) reveals the tooltip — no click required, consistent with the existing tooltip pattern already used for badge `aria-label`/hover text elsewhere on this page (e.g. Position Lifecycle State Badge tooltips, `positions.md` §Position Lifecycle State Badge).

Not placed per-row — this is an explanation of the mechanism, identical for every position, not a per-position value. One tooltip on the column header covers all rows.

## 3. Copy (reviewed against `strategy_rules.md` §7 for accuracy — AC-02)

> **Why is my stop moving?**
> Your stop tightens as a position becomes profitable and stays wide while it's losing or flat — this locks in gains without cutting winners short on noise. ATR is recalculated daily (14-day period). Once tightened, a stop never loosens, even if the position gives back some profit.

Rationale for wording, mapped to canonical source:
- "tightens as a position becomes profitable... stays wide while it's losing or flat" → §7.2 Profit-aware stop logic (`ProfitATRMultiplier` tighter than `InitialATRMultiplier`)
- "ATR is recalculated daily (14-day period)" → §7.1 ATR framework
- "Once tightened, a stop never loosens" → §7.3 Stop movement rule (hard constraint): `UpdatedStop = max(CurrentStop, NewlyCalculatedStop)`

No specific multiplier values (`InitialATRMultiplier` / `ProfitATRMultiplier`) are surfaced in the tooltip — these are internal parameters (`strategy_rules.md` §12 Parameter governance) subject to change control, and a plain-language explainer should describe behaviour, not restate tunable constants that could drift out of sync with the tooltip text. If the parameters change, this copy does not need updating.

## 4. Interaction & Accessibility

- Tooltip is a standard hover/focus tooltip component (existing pattern, no new component).
- `aria-label` on the icon: `"Why is my stop moving? Explanation of trailing stop behaviour."`
- Dismisses on blur/mouse-leave; no persisted dismiss state (unlike alert banners — this is reference information, always available, not a one-time notice).

## 5. States

No loading/error state — copy is static, client-side text, no API dependency.

## 6. Compliance Check

No conflict with `strategy_rules.md §13` — static explanatory text describing existing, already-implemented deterministic behaviour. No new automation, no recommendation, no trade action triggered from the tooltip.

## 7. Out of Scope

- Any change to the actual trailing-stop calculation or the Trail Stop Modal (`positions.md` §Trail Stop Action) — this is a read-only explainer layered on the existing column header only
- Surfacing tunable parameter values (§3 rationale)

## 8. Sign-off

- **Head of UX & Design:** Approved — 2026-07-27
- **Product Owner:** Approved — 2026-07-27
