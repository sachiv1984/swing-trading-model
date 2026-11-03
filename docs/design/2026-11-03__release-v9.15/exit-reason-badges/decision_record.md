**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-03__release-v9.15
**Stories:** ST-18 (EPIC-03, BLG-FE-220)

# Decision Record — Strategy Benchmark Exit-Reason Badges: Filled, AA Contrast

## 1. Problem

`strategy_benchmark.md` §7.3 lists tinted Stop and Rebalance badges, but the page ships filled badges (`EXIT_REASON_BADGE` in `src/pages/StrategyBenchmark.js`). Only the Risk-Off row was corrected to the shipped filled style in v9.12. The shipped Rebalance badge, `bg-teal-600 text-white`, measures 3.74:1, below WCAG AA for its small text.

## 2. Decision

**Filled badges, white text, for every exit reason.** Filled is what ships, and it matches the Signals page's exit badges (`signals.md` §Signal Type Badge Styling). A solid fill with white text reads the same in light and dark themes, so one token pair passes in both.

| Reason | Label | Style | White-text contrast |
|--------|-------|-------|---------------------|
| Stop | Stop | `bg-red-600 text-white` (unchanged) | 4.83:1 |
| Risk-Off | Risk-Off | `bg-amber-700 text-white` (unchanged) | 5.02:1 |
| Rebalance | Rebalance | `bg-teal-700 text-white` (was `bg-teal-600`) | 5.47:1 |
| Other (unmapped reason) | The raw reason, or "—" | No badge: plain `text-xs text-slate-600 dark:text-slate-400` (unchanged; the shipped fallback) | Secondary-text token, AA in both themes |

Contrast is measured against the Tailwind default palette (`teal-700` = `#0F766E`). WCAG AA for normal text is 4.5:1. The spec's former "Other — Uppercased, Slate default" row described a badge that never shipped, so it is replaced with the shipped plain-text fallback.

## 3. §13 Compliance

Colour only.

## 4. Frontend Spec Impact

- `pages/strategy_benchmark.md` v0.8 → v0.9: §7.3 Exit Reason Badges.

## 5. Obligations for Sprint Execution

- Update `tests/e2e/strategy-benchmark.spec.js` SC-SB-04a's `bg-teal-600` assertion to `bg-teal-700`.
- Add a scoped axe `color-contrast` scan of the Trade Log in both themes (ST-18 AC 1).

## 6. Testability (CLAUDE.md §2)

- Playwright + axe: the Trade Log's exit-reason badges pass `color-contrast` with the light and dark themes applied (assert the applied theme in each scan, per the v9.14 ST-35 lesson).

## 7. Approval

Head of UX & Design: confirmed, 2026-11-03 (agent-mediated, Design Gate Engine).
Product Owner: confirmed, 2026-11-03 (the user, in session).
