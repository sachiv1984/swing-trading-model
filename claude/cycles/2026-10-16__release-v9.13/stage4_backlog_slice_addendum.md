**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-10-16__release-v9.13

# Post-Gate-Correction Addendum — 2026-10-16__release-v9.13

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

## ST-03 — "No frontend file keeps its own exit-reason map" covers eight files, not five
**Found at:** Design Gate STEP 2 (exit-reason-badges design review, code read)
**Correction:** AC 3's parenthetical names five files: ExitModal, TradeReflection, TradeReflectionModal, PerformanceAnalytics and TradeHistoryTable. The AC's own rule ("no frontend file") also covers three more local maps:
- `src/components/reports/ExportModal.js`
- `src/components/reports/TradeBreakdown.js`
- `src/components/analytics/MonthlyHeatmap.js`

`src/lib/exitCondition.js`'s `EXIT_REASON_*` constants re-export from `src/constants/exitReasons.js` instead of redefining the strings. `StrategyBenchmark.js`'s map covers backtest-engine reasons, not stored `exit_reason` values, and stays out of scope.

The labels and badge tokens are fixed by `docs/design/2026-10-16__release-v9.13/exit-reason-badges/decision_record.md`. Both themes are in AC 4's colour tests. Sprint Planning should confirm that the S estimate (0.5–1 day) absorbs the three extra files.
**Date:** 2026-10-16

## ST-21 — The error-state axe scan needs the whole debrief section's light tokens, not only the error text
**Found at:** Design Gate STEP 2 (contrast measurement)
**Correction:** The source item's Scope names one change, `text-rose-600 dark:text-rose-400` on the error text. AC 1 scans the whole debrief section in its error state, in both themes. In the light theme, the section's other elements also fail on its `bg-slate-800/50` card: the violet heading, the "AI-generated" badge and the muted text.

The target is `trade_history.md` v1.16 §Post-Trade Debrief §Light Theme. The card gets `bg-white` in light, and the error text gets `text-rose-700 dark:text-rose-400`, not rose-600. Rose-600 measures 4.29:1 on `slate-100`, below AA; this is the `design_system.md` §Error States token. This stays within AC 1. The XS estimate may need to rise to S, which Sprint Planning should check.
**Date:** 2026-10-16

## ST-25 — The asserted fills are emerald-700 and white text, with AA hover shades
**Found at:** Design Gate STEP 2 (coloured-button-fills design review)
**Correction:** AC 2 asserts that each coloured `<Button>` "renders that colour". For the two Screener sites, the authored `bg-emerald-600` measures 3.77:1 with white text. Making it render would ship a new AA failure. Per `docs/design/2026-10-16__release-v9.13/coloured-button-fills/decision_record.md`:
- The Screener (~329, ~1065) and Cash Management deposit fills become `bg-emerald-700 hover:bg-emerald-800 text-white`. AC 2's `toHaveCSS` asserts emerald-700 (`rgb(4, 120, 87)`) for these sites.
- The rose-600 destructive buttons keep their rest fill. Their hover moves from `rose-500` (3.67:1) to `rose-700` (6.29:1). The fix makes the authored hover deterministic, so a failing hover would otherwise ship. The sites are listed in the decision record §2.2.
- `text-white` is added where a coloured button inherits `text-primary-foreground`, which is near-black in dark theme: Cash Management submit, and System Status "Refresh Health".
- The Trade Plan "Abandon Plan" `!bg-amber-700 hover:!bg-amber-800` becomes `bg-amber-700 hover:bg-amber-800` (AC 1).

The specs updated at this gate are `screener_results.md` v1.10 and `components/cash_management_modal.md` v1.3. The rule is added to `design_system.md` (Class 1) in-story.
**Date:** 2026-10-16
