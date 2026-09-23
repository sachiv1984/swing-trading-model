**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-23__release-v9.7
**Story:** ST-01 (EPIC-01, BLG-FEAT-74)

# Decision Record — PO-05: Lightweight Replay Mode (V1 Shape)

## 1. Problem

`BLG-FEAT-74` has no existing UI. Its own Scope note defers "exact scope (single trade replay vs. full historical window, output format)" to a canonical spec confirmed before implementation, and the item is phased as scope-confirmation sub-story → backend replay mechanics → frontend selector/output view (sealed slice Notes). This record establishes the V1 interaction shape and the constraints that any of those later sub-stories must build within — it is not a pixel-level spec of a not-yet-built backend response.

## 2. Decision

### 2.1 Navigation & entry point

New top-level nav item **"Replay"**, route `/replay`. No entry point from other pages in V1 (a future "Replay this period" shortcut from Trade History is out of scope here).

### 2.2 Selector

Two mutually exclusive input modes, tab-switched (reuses the existing tab pattern, e.g. `StrategyBenchmark.js`'s mode toggle):

| Mode | Control | Reuses |
|------|---------|--------|
| **Date Range** | `dateFrom` / `dateTo` native date inputs | Same field names/pattern as `TradeHistory.js`'s existing date filter |
| **Trade Set** | Multi-select list of the user's own closed trades (ticker, exit date, checkbox) | Reuses `TradeHistory.js`'s trade row rendering; own-data only, per §13 Criterion 2 |

A **"Run Replay"** primary button is disabled until at least one valid range or trade is selected. No default selection on page load (empty state, §2.5).

### 2.3 Output view

Rendered below the selector once a run completes:

- A non-dismissible `StandingAlert` Info-tone banner, always the first element of the output view, exact wording carrying forward the §13 pre-assessment's Binding Condition 2 verbatim: **"Retrospective result — shows what the current rules would have produced over this past period. Not a prediction of future performance."** `data-testid="replay-retrospective-banner"`.
- A summary row: trade count replayed, win rate, total simulated P&L (GBP) — same colour/format conventions as `design_system.md` §Number and Currency Formatting.
- A results table, one row per replayed trade: ticker, simulated entry/exit date, simulated P&L, exit reason. Reuses `StrategyBenchmark.js`'s exit-reason badge set (`EXIT_REASON_BADGE`) for visual consistency with the existing backtest-style view.
- **No interactive control anywhere in the output view writes to real or paper strategy parameters, stop multipliers, or risk percentages** (§13 Binding Condition 3 — no auto-remediation affordance).
- **Display-only:** no button in this view creates a real trade plan, position, or paper order from a replay row (§13 Binding Condition 1/4).

### 2.4 Rule set

No control anywhere in this page lets the user vary strategy parameters for the replay. The rule set is always "current" (§13 Binding Condition 4). If a future story adds parameter variation, it requires its own §13 review before any UI is added here.

### 2.5 States

| State | Treatment |
|-------|-----------|
| Initial (nothing selected) | Empty-state prompt: "Select a date range or trade set, then run a replay." No output section rendered. |
| Running | "Run Replay" shows a spinner and disables re-submission; no partial output rendered. |
| Success, 0 trades in scope | Output view renders the retrospective banner + "No closed trades in the selected range/set." — no summary row or table. |
| Success, ≥ 1 trade | Full output view per §2.3. |
| Failure | Non-blocking error banner: "Couldn't run the replay. Try again." Selector remains usable; nothing partially renders. |

### 2.6 Motion / timing

None beyond the design system's default (no new animation, debounce, or delay-before-show parameter introduced).

### 2.7 Scope explicitly deferred

Per `BLG-FEAT-74`'s own Scope note and the §13 pre-assessment's Binding Condition 6, the following are confirmed by the scope-confirmation sub-story (not this gate) before backend/frontend implementation sub-stories proceed, and must be checked against this record and against `po05_section13_preassessment.md`'s 6 binding conditions before either is built:
- Exact replay endpoint/request shape (this record assumes a single `POST /replay`-style call keyed on `date_from`/`date_to` or a `trade_ids[]` array; not yet contracted)
- Exact simulated-trade output field names (this record specifies the *displayed* columns only, not a wire format)
- Whether "Trade Set" mode allows mixing tickers with no chronological constraint, or requires a contiguous window

## 3. §13 Compliance

Covered by the standalone pre-assessment: `docs/product/decisions/po05_section13_preassessment.md` (PASS, 2026-09-23, 6 binding conditions). This record's §2.3–§2.4 decisions implement Binding Conditions 1–4 directly in the UI; §13's own Binding Condition 5 (IT-06 paper-data isolation) and 6 (implementation spec must be checked against the pre-assessment) are execution-time obligations, not UI decisions, and are carried forward to Sprint Execution via the frontend spec (§4 below).

## 4. Frontend Spec Impact

New file: `docs/specs/frontend/pages/replay_mode.md` v0.1 — new page, marked **Design Only — Implementation Pending** for the backend contract (consistent with this codebase's existing convention for stories phased ahead of their backend, e.g. `reports.md`'s Carried Forward Loss field and Arc 5 Compliance Summary sections).

## 5. Testability (CLAUDE.md §2)

Every AC in this record is observable UI behaviour and needs Playwright coverage once the backend sub-story lands: retrospective banner presence, disabled/enabled "Run Replay" state, empty/0-trade/populated/failure output states, and absence of any write-capable control in the output view. Coverage is scoped to the frontend implementation sub-story, not this gate.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-23.
Product Owner: confirmed, 2026-09-23 — approves the V1 shape as scoped above; the deferred items in §2.7 remain the scope-confirmation sub-story's to resolve before backend/frontend sub-stories are scheduled.
