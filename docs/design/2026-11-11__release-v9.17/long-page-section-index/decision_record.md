**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-11__release-v9.17
**Stories:** ST-07 (BLG-FE-263) — EPIC-02; reused by ST-06 (BLG-FE-259)

# Decision Record — In-Page Section Index for Long Pages

## 1. Decision

Trade Plan (`TradePlan.js`, ~1,300 lines) and Strategy Benchmark's Benchmark tab (`StrategyBenchmark.js`) get an **in-page section index**, not tabs. The Product Owner chose this at the gate (the user, in session, 2026-11-11).

**Why not tabs:** Trade Plan is a form. Tabs would hide fields, and a validation error or the Pre-Entry Validation result could sit in a hidden tab. An index keeps the content on one scroll, unchanged, and adds one-click reach to each section. Using one pattern on both pages (and on ST-06's Performance page) means one component and one set of tests.

## 2. Component: `SectionIndex`

A shared component in `src/components/ui/SectionIndex.js`.

**Props:** `sections: [{ id, label }]`, `ariaLabel` (default "On this page").

**Layout:**

- **At `lg` and up:** a sticky column to the right of the content (`sticky top-4`, width 12rem), headed "On this page" (`text-xs font-semibold uppercase text-app-muted`). One link per section (`text-sm text-app-muted hover:text-app-fg`).
- **Below `lg`:** a single row above the content that scrolls sideways inside itself (`overflow-x-auto`, the page itself does not scroll sideways), sticky under the page header. Links are pill-shaped and at least 44 px high.
- `<nav aria-label="On this page">` wrapping a list of `<a href="#{id}">` links. `data-testid="section-index"`, links `data-testid="section-link-{id}"`.

**Behaviour:**

- Clicking a link moves to the section's heading with an **instant** jump (`scrollIntoView({ block: "start" })`, no smooth scrolling), moves focus to the section heading (`tabIndex={-1}`) and updates `?section={id}` with a replace navigation. No motion means no reduced-motion branch (§6 motion rule).
- Loading a page with `?section={id}` jumps to that section once the content has rendered. An unknown id does nothing.
- **Current section:** the link for the section whose heading most recently crossed the top 25% of the viewport is marked `aria-current="true"` and styled `text-app-fg font-medium` with a 2 px left border (`border-cyan-600 dark:border-cyan-400`). Computed with `IntersectionObserver`; no scroll listener and no timing threshold.
- Each section's wrapper gets `id={id}` and `scroll-margin-top` equal to the sticky offset, so headings are not hidden under the header.
- The router uses hash routing (`/#/TradePlan`), so in-page anchors use `?section=`, never a second `#`.

## 3. Sections

### 3.1 Trade Plan (create and edit form)

Each section is an existing group of fields, wrapped in a `<section>` with a visible heading. Fields are not reordered (`trade_plan.md` §5f order stands).

| id | Label | Contents (current order) |
|----|-------|--------------------------|
| `basics` | Basics | Ticker, Market, Status, R Target, Regime at Entry, Tags |
| `setup` | Signal and setup | Signal Context panel (new plans), Setup Type, Setup Quality Score, News Context |
| `entry` | Entry, stop and size | Planned Entry/Stop, suggested size line, Planned Shares, Pre-Entry Validation |
| `thesis` | Thesis | Setup Thesis and its AI generation and feedback controls |
| `rules` | Rules | Entry Rationale, Confirmation Criteria, Early Exit Conditions, Invalidation Condition |
| `sizing` | What-if sizing | What-If Sizing Preview |
| `checklist` | Checklist | Pre-Entry Checklist |

A section with no visible content in the current mode (for example Signal Context on edit) still appears in the index when any of its fields render; a section with none is left out. The Trade Plan list view and the read-only detail view do not get an index.

### 3.2 Strategy Benchmark — Benchmark tab only

The Version Comparison and Backtest Rule Change tabs (`strategy_benchmark.md` §7.5, §7.6) keep their tabs. The index appears on the Benchmark tab only:

| id | Label |
|----|-------|
| `open-positions` | Open positions |
| `parity` | Performance parity |
| `yearly` | Yearly breakdown |
| `trade-log` | Trade log |

`?tab=` and `?section=` combine; `?section=` is ignored on the other two tabs.

## 4. Colour and tokens

New markup uses the `app-*` tokens (`design_system.md` §Semantic Colour Tokens). The cyan current-section border is a non-text indicator; cyan-600 on white measures above 3:1 (WCAG 1.4.11), and the link text carries `aria-current`, so colour is not the only signal.

## 5. Frontend spec impact (this gate)

- `pages/trade_plan.md` v1.24 → v1.25: new §5g Section Index.
- `pages/strategy_benchmark.md` v0.9 → v0.10: new §3a Section Index (Benchmark tab).

## 6. §13 Compliance

Navigation only. No content, calculation or AI call changes.

## 7. Testability (CLAUDE.md §2)

Playwright, on each page: `section-index` lists the §3 sections; clicking each link brings its heading into the viewport (heading `boundingBox().y` within the top quarter) in one click; `?section=rules` (Trade Plan) and `?section=trade-log` (Benchmark) open at that section; at 390 px the page has no horizontal scroll. One test asserts `aria-current` moves after scrolling to a later section.

## 8. Approval

Head of UX & Design: confirmed, 2026-11-11 (agent-mediated, Design Gate Engine).
Product Owner: confirmed, 2026-11-11 (the user, in session; chose the section index over tabs).
