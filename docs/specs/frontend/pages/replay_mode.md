**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.1
**Last Updated:** 2026-09-23 (v9.7 design gate — ST-01/BLG-FEAT-74: new page, V1 shape)
**Design Source:** docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# replay_mode.md — Replay Mode (PO-05)

> **Design Only — Implementation Pending.** This page has no backend endpoint yet. `BLG-FEAT-74` is phased as scope-confirmation sub-story → backend replay mechanics → frontend selector/output view (sealed slice `2026-09-23__release-v9.7` note). This spec fixes the V1 UI contract and the §13 constraints binding on it; the exact request/response wire shape is confirmed by the scope-confirmation sub-story before the backend/frontend sub-stories are scheduled, per `po05_section13_preassessment.md` Binding Condition 6.

## Purpose & User Goals

Lets the user replay a historical date range or a specific set of their own past trades through the current strategy rules under the existing paper-trading mechanics, to see what those rules would have produced. Retrospective only — never framed as, or capable of, predicting future performance.

Users should be able to:
- Select a historical date range, or a specific set of their own closed trades
- Run a deterministic replay of that scope under the current strategy rule set
- View a clearly retrospective-labelled summary and per-trade result

---

## Navigation & Route

- Top-level nav item: **"Replay"**
- Route: `/replay`
- Page title: **"Replay Mode"**

---

## §13 Boundary (binding — do not implement around this)

Per `docs/product/decisions/po05_section13_preassessment.md` (PASS):
1. Read-only against real data — never writes to real `positions`/`trade_history`, and never updates strategy parameters, stop multipliers, or risk percentages.
2. Output always carries the retrospective/deterministic banner (§Output View below) — no future-facing phrasing anywhere near it.
3. No control in the output view may adjust real strategy parameters, risk percent, or stop multipliers.
4. Rule set is always "current" — no user-editable/hypothetical rule variation in this page.
5. Reuses IT-06 paper-trading mechanics under IT-06's own existing paper-data isolation condition (replay/paper data must not feed real-system signals, screener scoring, regime detection, or position-sizing logic).

Any change to this page that touches one of the 5 conditions above requires a fresh §13 review before merge, not just a design-gate pass.

---

## Selector

Two tab-switched, mutually exclusive modes:

| Mode | Control | Field names (reuse existing convention) |
|------|---------|------------------------------------------|
| Date Range | Two native date inputs | `dateFrom`, `dateTo` (same pattern as `TradeHistory.js`) |
| Trade Set | Multi-select checkbox list of the user's own closed trades (ticker, exit date) | Own-data only — sourced from the user's existing closed-trade history, no third-party data |

**"Run Replay"** primary button: disabled until a valid range or ≥ 1 trade is selected. No selection is pre-filled on page load.

---

## Output View

Rendered below the selector after a run completes. Order is fixed:

1. **Retrospective banner** — non-dismissible `StandingAlert` Info tone, always first: `"Retrospective result — shows what the current rules would have produced over this past period. Not a prediction of future performance."` `data-testid="replay-retrospective-banner"`.
2. **Summary row** — trades replayed (count), win rate (%), total simulated P&L (GBP). Same colour/number conventions as `design_system.md` §Number and Currency Formatting.
3. **Results table** — one row per replayed trade: Ticker, Simulated Entry Date, Simulated Exit Date, Simulated P&L, Exit Reason (reuses `StrategyBenchmark.js`'s exit-reason badge set for visual consistency).

No control anywhere in this view is write-capable against real data (§13 Boundary above).

---

## States

| State | Treatment |
|-------|-----------|
| Initial | "Select a date range or trade set, then run a replay." No output section rendered. |
| Running | "Run Replay" shows a spinner, disabled; nothing partially renders. |
| Success — 0 trades in scope | Retrospective banner + "No closed trades in the selected range/set." No summary row or table. |
| Success — ≥ 1 trade | Full output view per §Output View. |
| Failure | Non-blocking error banner: "Couldn't run the replay. Try again." Selector remains usable. |

---

## Motion / Timing

None beyond the design system's default. No new animation, debounce, or delay-before-show parameter is introduced by this page.

---

## API Reference

Not yet contracted — see the Design Only note at the top of this file. When contracted, the endpoint, `docs/specs/api_contracts/`, and `docs/reference/openapi.yaml` must all be updated in the same commit (CLAUDE.md §2).

---

## Testability (CLAUDE.md §2)

Playwright coverage required once implemented: retrospective banner always present in any populated/empty-result output; "Run Replay" disabled/enabled transitions; empty-scope, populated, and failure output states; no write-capable control present in the output view (a negative assertion, not just a positive one, given the §13 boundary above).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-09-23 | v9.7 design gate — ST-01 (EPIC-01, BLG-FEAT-74): new page, V1 shape (selector, output view, §13 boundary, states). Design source: `docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md`. Design Only — Implementation Pending (no backend endpoint yet). Authority: Head of Specs Team. |
