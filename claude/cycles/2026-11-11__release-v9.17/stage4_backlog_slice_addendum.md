**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-11-11__release-v9.17

# Post-Gate-Correction Addendum — 2026-11-11__release-v9.17

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

## ST-01 — "Near stop" means within 5% of the trailing stop, post-grace
**Found at:** Design Gate STEP 1
**Correction:** The slice's urgency order names a "near stop" tier without a threshold. The Product Owner chose to reuse the Risk Dashboard's existing ≤ 5% stop-distance band (`risk_dashboard.md` §6), so no new threshold is introduced. In-grace positions never enter the stop tiers. Full rule: `positions.md` v2.25 §Decision-First Table.
**Date:** 2026-11-11

## ST-03 and ST-04 — how the warning strip's grace entry and the single grace view fit together
**Found at:** Design Gate STEP 2
**Correction:** The slice says ST-04 "removes `GracePeriodAlertZone`'s detail from the strip's grace entry". Read as: ST-03 builds the strip with the grace entry expanding to today's `GracePeriodAlertZone` content; ST-04 replaces that content with `GracePeriodView`, which is the single grace view (Product Owner). `GracePeriodView` lists every in-grace position, not only those within 2 days of the end, and has no dismiss, because it replaces the Risk Dashboard's per-position list. Dashboard Card 3 and the Risk Dashboard Grace panel link to `/Positions?grace=open`. Days-remaining pills, the Today list's "Grace ends today" rows and the Risk Dashboard's "Not enforced (grace)" cells are not grace detail and stay. Design source: `docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md` §5.
**Date:** 2026-11-11

## ST-06 — the build sub-step waits for the Head of UX & Design's approval of the Performance spec
**Found at:** Design Gate STEP 2
**Correction:** The Product Owner chose a brief at the gate and the spec in the sprint (v9.15 Journal precedent; RISK-04). ST-06's build may not start until `docs/specs/frontend/pages/performance.md` exists, meets the brief in `docs/design/2026-11-11__release-v9.17/performance-page-brief/decision_record.md` §2, and carries a dated Head of UX & Design approval. The brief's 390 px rule covers `BLG-FE-237` (Reports tab bar overflow); the story records whether `BLG-FE-237`'s AC is met so `groom backlog` can close it.
**Date:** 2026-11-11

## ST-07 — a section index, not tabs
**Found at:** Design Gate STEP 1
**Correction:** The slice allows "tabs or an index". The Product Owner chose a sticky in-page section index on both pages, because tabs would hide Trade Plan fields and validation results. On Strategy Benchmark the index covers the Benchmark tab only; the Version Comparison and Backtest Rule Change tabs stay. Sections: `trade_plan.md` v1.25 §5g, `strategy_benchmark.md` v0.10 §3a.
**Date:** 2026-11-11

## ST-14 — "entry" in the pre-fill AC is the signal's price, as the Signal Context panel shows it
**Found at:** Design Gate STEP 2
**Correction:** AC 1 says Stop Level is pre-filled with "entry − 5×ATR". The pre-fill uses the same value the Signal Context panel already shows as "Suggested stop" (the signal's `initial_stop`, else `current_price − 5 × atr_value`), from one shared helper, so the form and the panel cannot disagree. The stored-stop line (AC 2) compares the typed stop with Planned Entry − 5 × `atr_value`, the stop Trade Entry will compute. `trade_plan.md` v1.25 §5a.3, §5f.
**Date:** 2026-11-11
