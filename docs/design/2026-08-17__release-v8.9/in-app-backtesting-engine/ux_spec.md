**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-17__release-v8.9
**Story:** ST-07 (EPIC-02, BLG-FEAT-89)

# UX Spec — In-App Backtesting Engine for Strategy Rule Changes

## 1. Problem

`BLG-FEAT-89` asks for a way to run a candidate `strategy_rules.md` change against historical data from inside the app, with no external script step, producing win rate / R-multiple distribution / drawdown compared against the current live rule set, and persisting each run for later audit.

**Grounding:** The Strategy Benchmark page (`strategy_benchmark.md`) already has a two-tab structure — **"Benchmark"** (live-vs-backtest comparison) and **"Version Comparison"** (SI-04, comparing two already-shipped rule versions against each other). ST-07 is the natural third sibling: instead of comparing versions that already exist, it runs a *new, not-yet-shipped* candidate rule diff against history. Placing it alongside the existing two tabs keeps all strategy-evaluation workflows in one page rather than fragmenting them.

## 2. Decision

Add a third tab, **"Backtest Rule Change"**, to `strategy_benchmark.md` §2's sub-navigation bar (client-side `?tab=backtest-rule-change`, no new top-level route — same pattern as the existing `?tab=version-comparison`).

### 2.1 Tab Layout

**Left panel — Candidate Rule Input:**
- A textarea or diff-style input for the candidate `strategy_rules.md` change (implementation detail — raw text paste vs. structured parameter form — deferred to Backend Engineering Patterns Owner / Strategy Rules & System Intent Owner at sprint planning; this record fixes only the page/tab placement and the output contract below, not the input mechanism, since AC-01 only requires "no external script step", not a specific input UI).
- **"Run Backtest"** button (primary) — disabled while a run is in progress; shows inline spinner + "Running backtest…" label during execution (backtests over full history may take several seconds — no fixed timeout assumption in this record; Backend Engineering Patterns Owner to confirm expected runtime at implementation).

**Right panel — Results (shown after a run completes):**

| Element | Content |
|---------|---------|
| Win rate | Candidate vs. live rule set, side-by-side percentages |
| R-multiple distribution | Histogram (reuse existing chart component/styling already used elsewhere on this page for distribution displays, per `dataviz` skill conventions) — candidate overlaid against live |
| Max drawdown | Candidate vs. live, side-by-side |
| Run metadata | Timestamp, rule diff summary, "by {run initiator}" |

**Empty state (no run yet):** "Paste a candidate rule change and run a backtest to compare it against your live strategy." No chart/table shown.

### 2.2 Run Persistence (AC-03)

Each backtest run is persisted (new table/endpoint — backend scope) with: what was tested (the rule diff/parameters), when, by what rule diff, and the resulting win rate / R-distribution / drawdown output. A **"Run History"** collapsible list below the results panel shows prior runs (most recent first), each expandable to re-view its stored output without re-running. This satisfies AC-03's audit requirement without requiring a separate page.

### 2.3 §13 Boundary

This feature runs a deterministic simulation (the same `production_strategy.py`-class backtest logic already used by the existing "Benchmark" tab, applied to a candidate rule set instead of the live one) over the user's own/market historical data — no ML model, no adaptive inference, output is comparative statistical context for a human decision (whether to adopt the candidate rule change), not an automated action. This is the same category of feature already covered by the existing Benchmark/Version Comparison tabs' established §13 framing — **not** a new AI-provider call, so the mandatory §13 boundary pre-check (`design_gate_prompt.md` STEP 1, AI-calling proposals) does not apply. No output from this tab writes to `strategy_rules.md` or any live rule configuration — a candidate result is read-only, comparative context; adopting a rule change remains a separate, manual, human-authored edit to `strategy_rules.md` outside this feature's scope.

## 3. Constraints Checked

- Does not contradict `strategy_rules.md §13`.
- No new metric definitions required — win rate / R-multiple / drawdown are existing canonical metrics already computed by the Benchmark tab; this reuses the same computation over a different (candidate) rule input.
- Analytics/metrics features align with canonical metric definitions (`metrics_definitions.md`) — no new definitions introduced.

## 4. Product Owner Approval

Approved 2026-08-17 (design gate session).

## Notes

- Strategy Rules & System Intent Owner sign-off (per AC-04) is a Sprint/Delivery-stage requirement, separate from this design-gate approval — recorded here as a forward reference, not satisfied by this record.
- Candidate rule input mechanism (raw diff vs. structured form) is explicitly left open for Sprint Planning / implementation to resolve against actual engineering cost — this record's binding contract is the tab placement, results layout, and run-history persistence requirement only.
