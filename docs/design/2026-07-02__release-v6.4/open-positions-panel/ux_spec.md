**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-02
**Cycle:** 2026-07-02__release-v6.4
**Story:** ST-08 (BLG-FEAT-54)
**Approved by:** Product Owner — 2026-07-02

---

# UX Spec — Open Positions Panel (Strategy Benchmark Page)

## Purpose

The Strategy Benchmark page's Panel 1/2 aggregates and Panel 3 trade log only reflect **closed** trades. When the backtest is fully invested, the page shows no activity past the last entry date — it reads as stalled even though real capital is actively deployed with real unrealized P&L (~£46k unrealized across 5 open positions observed 2026-06-30). This panel surfaces current unrealized exposure without touching any realized metric.

---

## Placement

New **Panel 0 — Open Positions**, inserted between the Sticky Filter Bar and Panel 1 (Performance Parity).

Rationale: this is the first thing a user should see — it answers "is anything live right now?" before the user reads historical/realized comparisons in Panels 1–3. Existing Panel 1/2/3 numbering is preserved unchanged (both TEST-GAP-EPIC-03 and the canonical spec reference "Panel 1" and "Panel 3" by number — renumbering would invalidate those references).

```
┌─────────────────────────────────────────────────────┐
│  Page Header: "Strategy Benchmark"                  │
├─────────────────────────────────────────────────────┤
│  [Sticky Filter Bar]  Year: [...]  Market: [...]    │
├─────────────────────────────────────────────────────┤
│  Panel 0: Open Positions                             │
│  "5 open positions · +£46,230 unrealized"            │
│  ┌───────────────────────────────────────────────┐  │
│  │ Ticker  Entry   Entry£  Current£  P&L£  P&L%  Days│
│  │ ...     ...     ...     ...       ...   ...   ...│
│  └───────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  Panel 1: Performance Parity                         │
├─────────────────────────────────────────────────────┤
│  Panel 2: Yearly Breakdown Table                     │
├─────────────────────────────────────────────────────┤
│  Panel 3: Trade Log                                  │
└─────────────────────────────────────────────────────┘
```

---

## Conditional Rendering

Panel is rendered **only when ≥1 open position exists** for the current filter context (see Filter Interaction below). When zero open positions exist, the panel is omitted entirely — no empty-state card, no placeholder. This matches the existing Paper Account Panel convention (`positions.md` §"Paper Account Panel") of not showing an unconfigured/empty state where absence itself is the expected common case.

---

## Panel Header

| Element | Spec |
|---------|------|
| Label | **"Open Positions"** |
| One-line summary | `"<N> open position<s> · <sign>£X,XXX unrealized"` — e.g. "5 open positions · +£46,230 unrealized" |
| Summary colour | Green (`text-emerald-400`) if aggregate unrealized P&L ≥ 0; red (`text-rose-400`) if negative |
| Expand/collapse | None — always expanded when rendered (small N expected; unlike Paper Account Panel this is the primary content, not a secondary tracking feature) |

---

## Open Positions Table

| Column | Source Field | Format |
|--------|-------------|--------|
| Ticker | `ticker` | Uppercase |
| Market | `market` | Badge — muted, matches existing market badge styling (only rendered when Market filter = All) |
| Entry Date | `entry_date` | `DD Mon YYYY` |
| Entry Price | `entry_price` | `£X.XX` |
| Current Price | `current_price` | `£X.XX` |
| Unrealized P&L (£) | `unrealized_pnl_gbp` | Signed `£X,XXX.XX`; profit `text-emerald-400`, loss `text-rose-400` |
| Unrealized P&L (%) | `unrealized_pnl_pct` | Signed `X.X%`; profit `text-emerald-400`, loss `text-rose-400` |
| Days Held | Derived: today − `entry_date` | Integer |

**Sorting:** Default sort is by Unrealized P&L (%) descending — surfaces the largest movers (winners and losers) first. No user-sortable columns in v1.0 (consistent with Panel 2's "no user-sortable columns" precedent).

**Scrolling:** Scrollable table body if row count exceeds viewport (consistent with Panel 2 pattern).

---

## Filter Interaction

| Filter | Applies to Panel 0? | Rationale |
|--------|---------------------|-----------|
| Market | **Yes** — filters rows to positions in the selected market | Consistent with all other panels; a position has a fixed market |
| Year | **No** — panel always shows all currently open positions regardless of Year filter selection | Open positions are current-state, not historical-per-year data. An open position may have been entered in a prior year and remain open today; forcing the user to select a specific year to see it would recreate the "stalled" problem this panel exists to solve. |

This is a deliberate exception to the page-level rule ("both filters apply simultaneously to all panels") stated in `strategy_benchmark.md` §3 — recorded here as the authoritative rationale; §3 must be updated to note the Year-filter exception for Panel 0.

---

## Realized Metric Isolation (AC-02)

**Hard rule:** Unrealized positions must never be included in Panel 1 stat cards, Panel 1 PnL bar chart, or Panel 2 yearly breakdown aggregates. Those panels remain strictly realized/closed-trade data. Panel 0 is visually and structurally separate — no shared totals, no combined "PnL" figure anywhere on the page that mixes realized and unrealized values.

---

## States

| State | Behaviour |
|-------|-----------|
| ≥1 open position (current filter context) | Panel renders, expanded, sorted by P&L% descending |
| 0 open positions | Panel omitted entirely — no placeholder card |
| Loading | Skeleton row placeholders within panel bounds (consistent with page-level "Skeleton placeholders per panel") |
| API error (5xx/timeout on open-positions endpoint) | Panel renders header only, with muted inline message **"Open positions temporarily unavailable."** — no icon, does not break rest of page (consistent with Paper Account Panel error-state precedent) |
| Market filter narrows to 0 matching open positions | Panel omitted for that filter selection (same as zero-position state) |

---

## Data Source & Import Behaviour (AC-03)

New `backtest_open_positions` table is **fully replaced** (not upserted) on each nightly import, consistent with the existing `backtest_trades` replace-on-import behaviour. This guarantees the table never accumulates stale positions that have since closed.

---

## API Endpoint (AC-04)

New endpoint: `GET /strategy/benchmark/open-positions` — returns current open positions with unrealized P&L. Must ship with `docs/reference/openapi.yaml` entry, a `## GET /strategy/benchmark/open-positions` contract heading in `docs/specs/api_contracts/`, and `backend/routers/test.py` registration in the same commit (per CLAUDE.md §2 hard rules). This is an execution-phase (Sprint Execution) obligation, recorded here for design-to-build continuity.

---

## Constraints

- Display-only — no trade entry, exit, or modification action executable from this panel (consistent with the rest of the Strategy Benchmark page, which is read-only)
- §13 does not apply — this panel displays live position data, not AI advisory content
- Badge/colour conventions (market badge, profit/loss colour) must match existing conventions used elsewhere on this page and on the Positions page, for visual consistency

---

## Accessibility

- Table: standard `<table>` with `<th>` headers; `scope="col"` on column headers (consistent with §10 of `strategy_benchmark.md`)
- Panel header summary line: plain text, not conveyed by colour alone (colour is a reinforcement, not the sole signal — sign `+`/`-` prefix always present in the summary text)
