**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.2
**Last Updated:** 2026-09-25 (ST-01c, EPIC-01, v9.7, BLG-FEAT-74 — implementation lands: wire contract referenced, §13 item 5 IT-06 premise corrected, route/column-label corrections, FX-basis caption and independence/skipped-trade notice added); prior — 2026-09-23 (v9.7 design gate — ST-01/BLG-FEAT-74: new page, V1 shape)
**Design Source:** docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md
**Wire Contract:** docs/product/decisions/po05_replay_scope_confirmation.md (rev 3); implemented as `docs/specs/api_contracts/replay_endpoints.md` v1.0
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# replay_mode.md — Replay Mode (PO-05)

Lets the user replay a historical date range or a specific set of their own past
closed trades through the current strategy engine's exit rules (stop / risk-off), to
see what those rules would have produced. Retrospective only — never framed as, or
capable of, predicting future performance.

Users can:
- Select a historical date range, or a specific set of their own closed trades
- Run a deterministic replay of that scope under the current strategy rule set
- View a clearly retrospective-labelled summary and per-trade result

---

## Navigation & Route

- Top-level nav item: **"Replay"** (Analytics group, alongside Strategy Benchmark)
- Route: **`/Replay`** — corrected from the v0.1 `/replay` (lowercase); this
  application's page routes are generated from `pages.config.js`'s `PAGES` map keys
  (`/${key}`), and every sibling page (`/StrategyBenchmark`, `/TradePlan`, …) follows
  this same PascalCase convention. `/replay` was v0.1's idealised route name, written
  before implementation; `/Replay` is what actually renders.
- Page title: **"Replay Mode"**

---

## §13 Boundary (binding — do not implement around this)

Per `docs/product/decisions/po05_section13_preassessment.md` (PASS), as corrected by
the wire contract's Finding F1:

1. Read-only against real data — never writes to real `positions`/`trade_history`, and
   never updates strategy parameters, stop multipliers, or risk percentages.
2. Output always carries the retrospective/deterministic banner (§Output View below) —
   no future-facing phrasing anywhere near it.
3. No control in the output view may adjust real strategy parameters, risk percent, or
   stop multipliers.
4. Rule set is always "current" — no user-editable/hypothetical rule variation in this
   page.
5. **Corrected (v0.2):** this page does **not** reuse IT-06's Alpaca paper-trading
   mechanics — it makes no Alpaca call at all. The replay is an in-process,
   deterministic simulation built on the same engine as the existing "Backtest Rule
   Change" feature (`strategy_engine.py`). It reads only the user's own
   `trade_history` and public price history; it writes nothing anywhere. See the wire
   contract's Finding F1 for the full correction and rationale — this is a stronger
   isolation guarantee than the v0.1 wording implied, not a weaker one.

Any change to this page that touches one of the 5 conditions above requires a fresh
§13 review before merge, not just a design-gate pass.

---

## Selector

Two tab-switched, mutually exclusive modes:

| Mode | Control | Field names |
|------|---------|-------------|
| Date Range | Two native date inputs (`data-testid="replay-date-from"` / `replay-date-to`) | `date_from`, `date_to` (same field-naming convention as `TradeHistory.js`'s date filter) |
| Trade Set | Checkbox list of the user's own closed trades (ticker, exit date), sourced from `GET /trades` | `trade_ids` — own-data only, no third-party data |

**"Run Replay"** primary button (`data-testid="replay-run-button"`): disabled until a
valid range (both dates set) or ≥ 1 trade is selected. No selection is pre-filled on
page load. Switching tabs clears any prior run's output.

---

## Output View

Rendered below the selector after a run completes. Order is fixed:

1. **Retrospective banner** — non-dismissible `StandingAlert` Info tone, always first:
   `"Retrospective result — shows what the current rules would have produced over
   this past period. Not a prediction of future performance."` Rendered from the
   API response's `data.retrospective_notice` field (never hard-coded from a
   client-side copy, so a future wording change only needs a backend edit), with an
   identical hard-coded fallback literal so a missing field can never silently drop
   the banner. `data-testid="replay-retrospective-banner"`.
2. **Summary row** — trades replayed (count), win rate (%), total simulated P&L
   (GBP). Same colour/number conventions as `design_system.md` §Number and Currency
   Formatting (`formatCurrency`/`formatPercent`).
3. **Independence note** (v0.2 addition, wire contract §7 item 3a) — a muted line:
   *"Each trade is replayed independently — there is no shared cash, position limit,
   or chronology between the trades shown here."* `data-testid="replay-independence-note"`.
4. **Skipped-trades notice** (v0.2 addition, wire contract §7 item 3b) — shown only
   when `run.skipped` is non-empty: a muted amber line naming how many trades could
   not be replayed and why (grouped by reason). `data-testid="replay-skipped-notice"`.
5. **FX-basis caption** (v0.2 addition, wire contract §7 item 2) — a muted line:
   *"GBP figures use each trade's recorded entry exchange rate."*
   `data-testid="replay-fx-basis-caption"`.
6. **Results table** — one row per replayed trade: Ticker, **Entry Date** (corrected
   from v0.1's "Simulated Entry Date" — entry is always the trade's real, recorded
   entry; only the exit is simulated), Simulated Exit Date, Simulated P&L (GBP), Exit
   Reason. Exit reason reuses `StrategyBenchmark.js`'s badge colours (`Stop` = red,
   `Risk-Off` = amber) for visual consistency; `"Actual Exit"` (no rule fired) is
   deliberately not in the badge set and renders as plain text.

No control anywhere in this view is write-capable against real data (§13 Boundary
above) — confirmed by a negative Playwright assertion (no `<button>`/`<a>`/`<input>`
inside the output view).

---

## States

| State | Treatment |
|-------|-----------|
| Initial | "Select a date range or trade set, then run a replay." No output section rendered. `data-testid="replay-empty-state"`. |
| Running | "Run Replay" shows a spinner, disabled; nothing partially renders. |
| Success — 0 trades in scope | Retrospective banner + "No closed trades in the selected range/set." (`data-testid="replay-empty-result"`). No summary row or table. If `run.skipped` is non-empty, the skipped-trades notice is still shown alongside this text (v0.2 — otherwise a request whose trades all failed for a real reason would misleadingly read the same as a request with genuinely nothing in scope). |
| Success — ≥ 1 trade | Full output view per §Output View. |
| Failure | Non-blocking error banner: "Couldn't run the replay. Try again." (`data-testid="replay-failure-banner"`). Selector remains usable. |

---

## Motion / Timing

None beyond the design system's default. No new animation, debounce, or delay-before-show parameter is introduced by this page.

---

## API Reference

`POST /replay/run` — `docs/specs/api_contracts/replay_endpoints.md` v1.0. Wire
contract locked in `docs/product/decisions/po05_replay_scope_confirmation.md` (rev 3).
Trade Set mode's checkbox list is sourced from the existing `GET /trades` endpoint
(`trade_endpoints.md`), not a new one.

---

## Testability (CLAUDE.md §2)

Playwright coverage (`tests/e2e/replay-mode.spec.js`): navigation from the sidebar;
mutually exclusive tab controls; "Run Replay" disabled/enabled transitions in both
modes; running-state spinner; retrospective banner presence and exact wording,
non-dismissible; populated success (summary, independence note, FX caption, badged
results table); 0-trade success with and without a skipped-trades notice; the
skipped-trades notice alongside a populated result; failure state wording and
selector usability after a failure; the no-write-capable-control negative assertion;
the Trade Set checkbox list itself (ticker, exit date, toggling).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.2 | 2026-09-25 | ST-01c (EPIC-01, BLG-FEAT-74): implementation. §13 item 5 corrected — no IT-06/Alpaca reuse, per the wire contract's Finding F1. Route corrected `/replay` → `/Replay` (actual `pages.config.js` convention). Results table column corrected "Simulated Entry Date" → "Entry Date" (entry is never simulated). Added the independence note, skipped-trades notice, and FX-basis caption (wire contract §7 items 2–3). API Reference filled in. Design source and V1 shape otherwise unchanged. Authority: Sprint Execution Engine (agent-mediated, Frontend Specifications & UX Documentation Owner role — §5.3), on the user's explicit direction. |
| 0.1 | 2026-09-23 | v9.7 design gate — ST-01 (EPIC-01, BLG-FEAT-74): new page, V1 shape (selector, output view, §13 boundary, states). Design source: `docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md`. Design Only — Implementation Pending (no backend endpoint yet). Authority: Head of Specs Team. |
