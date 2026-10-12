**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-10-12__release-v9.12

# Post-Gate-Correction Addendum — 2026-10-12__release-v9.12

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

## ST-23 — Light mode ruled supported; the first AC branch applies
**Found at:** Design Gate STEP 2 (RISK-03 decision)
**Correction:** Head of UX & Design, with the Product Owner, rules that light mode is a supported theme. See `docs/design/2026-10-12__release-v9.12/light-theme-support/decision_record.md`. ST-23 takes AC 1. AC 2 (not supported) no longer applies. The 2.5-day estimate stands, so RISK-03's re-estimate fallback does not fire.

Two clarifications within AC 1's existing scope:
- The light-mode tokens added to `docs/specs/frontend/design_system.md` are the decision record's §3 table.
- The stale "dark-only in practice" statement in `docs/frontend/design_system.md` §6 (Class 2), which `BLG-FE-200` cites, is corrected to point to the canonical token table in the same story.

The four `:light` `color-contrast` entries are removed from `KNOWN_VIOLATIONS` in the same commit. Replay's light-theme baseline stays with its own backlog item.
**Date:** 2026-10-12

## ST-24 — The white-on-amber-600 sites the AC's literal grep misses
**Found at:** Design Gate STEP 1 (classification, code read)
**Correction:** The item's title and Problem cover white text on `amber-600` outside Replay. AC 1's check (`bg-amber-600 text-white` as a class pair) does not match three sites with the same 3.19:1 defect:
- `src/pages/TradePlans.js` `research_pending`, where `bg` and `text` are separate keys.
- `src/pages/TradePlan.js` "Abandon Plan" button, `bg-amber-600 hover:bg-amber-500 text-white`. The target is `bg-amber-700 hover:bg-amber-800`.
- The Gap Risk badge's inline `backgroundColor: "#D97706"` with white text, in `src/pages/Positions.js` and `src/components/positions/PositionCard.js`. The target is `#B45309`.

All of these move to amber-700, together with the three sites the item names. Their frontend specs were updated at this gate: `positions.md` v2.16, `dashboard.md` v3.9, `trade_plan.md` v1.18 and `strategy_benchmark.md` v0.8. `tests/e2e/strategy-benchmark.spec.js` (line 267, asserts `bg-amber-600`) is updated in the same commit. This corrects the item's own stated scope. It adds no scope.
**Date:** 2026-10-12

## ST-10 — No lower-stop control under either ruling; the spec is conditional
**Found at:** Design Gate STEP 2
**Correction:** The shipped modal offers "Lower stop to {value}" when `trail_difference < 0`, which `strategy_rules.md` §7.3 forbids. Whichever way the ruling goes, that label is removed, and a no-raise note shows instead (`positions.md` v2.16 §Trail Stop Action). The spec carries Branch A (manual raise via `PATCH /positions/{id}/stop`) and Branch B (read-only, button renamed "View Trail"). The story deletes the branch not taken in the same commit as the code. For AC 3, the design recommends rejecting a supplied entry `stop_price` with a 400 rather than storing it. Storing it would contradict the read-only Initial Stop on Trade Entry and would need its own design pass.
**Date:** 2026-10-12

## ST-22 — "Opens the Positions page showing that position" needs a new Positions deep link
**Found at:** Design Gate STEP 2
**Correction:** Positions has no deep link that brings a position into view. The only one, `?exit={id}`, opens the exit dialog. AC 1 is met with a new `?position={id}` link (`positions.md` v2.16 §Position Deep Link: scroll into view, 2000 ms highlight, parameter stripped), implemented in `Positions.js` as part of this story. The Product Owner prefers the spec's wording, so AC 2 resolves to aligning the shipped text to `risk_dashboard.md` §5.2. §5.2 is not amended to the shipped text.
**Date:** 2026-10-12
