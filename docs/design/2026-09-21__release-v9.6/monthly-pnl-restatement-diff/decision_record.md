**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-21__release-v9.6
**Story:** ST-08 (EPIC-02, BLG-FR-05)

# Decision Record — Month-End Snapshot and Restatement Diff on Monthly P&L

## 1. Problem

A later edit to a closed-trade row silently restates an already-reviewed month; nothing records what the month showed when it was reviewed. The story persists an immutable per-month snapshot and must surface a diff when live figures for a snapshotted month differ.

## 2. Decision

### 2.1 Snapshot semantics (user-visible contract)

- A **closed month** is a calendar month that has ended (UK time). The current, in-progress month is never snapshotted and never shows a restatement indicator.
- The snapshot captures the month's **Realised P&L** and **Trade count** exactly as the Monthly table displayed them, plus the snapshot date.
- **Immutable and read-only.** Never overwritten, never "accepted" or re-baselined from the UI. (An "acknowledge restatement" action would mutate the record the feature exists to preserve; if wanted, it is a separate story.)
- **Baseline on first deployment:** months that are already closed when this ships are snapshotted once with their then-current figures. They are not retroactively "restated" — the feature protects from ship day forward.

### 2.2 Monthly table — restatement indicator

A month whose live figures differ from its snapshot shows a **"Restated"** marker in the **Month** cell:

| Element | Spec |
|---------|------|
| Text | `"Restated"` with a `RefreshCw`/history-style icon prefix |
| Style | `text-amber-600 dark:text-amber-400`, plain text + icon (same family as the Trade Plans stale marker and Watchlist staleness indicator); **not** red — a restatement is information, not an error |
| Control | The marker is a button (`aria-expanded`, keyboard operable) that expands an inline detail row beneath the month row |
| `data-testid` | `monthly-restated-marker`, `monthly-restatement-detail` |

### 2.3 Inline detail row

| Metric | As reviewed (snapshot, {snapshot date}) | Now (live) | Change |
|--------|------------------------------------------|------------|--------|
| Realised P&L | `£x` | `£y` | `±£d` |
| Trades | `n` | `m` | `±k` |

Change values use the standard P&L tone rule (green > 0, red < 0, neutral = 0) and the canonical number format (`number-format-convention/decision_record.md`). Only metrics that actually differ are emphasised; unchanged metrics render muted. The row uses the existing expandable-row pattern (`design_system.md` §Tables); no animation beyond the design system's default (≤ 200 ms, well under the 500 ms ceiling in §Accessibility). Collapsed by default.

### 2.4 Tax Year tab

The tax-year figures derive from the same ledger, so a restated month can move a tax-year total. The Tax Year Summary Bar gains a one-line muted notice **only when the selected tax year contains ≥ 1 restated month**: `"Includes {k} restated month(s) — see the Monthly tab for details."` with a link to the Monthly tab. No tax-year-level snapshot is stored or diffed by this story; the count is supplied by the API (`summary.restated_month_count`, computed server-side from the monthly snapshots) — the Reports page's standing rule is that the frontend never derives Summary Bar figures. (This resolves the slice's "and the tax-year table" wording without adding a second snapshot store.)

### 2.5 Exports and reconciliation

Monthly and Tax Year CSVs continue to export **live** figures with unchanged columns. The restatement is an on-screen review aid, not an export attribute. The documented reconciliation rule (monthly CSV sums equal the Tax Year CSV per year) is unaffected.

### 2.6 States

No snapshot for a month (in-progress month, or no data) → no marker, table renders as today. Snapshot fetch failure → the table renders normally without markers and a muted line `"Restatement check unavailable."`; the failure never blocks the P&L figures.

### 2.7 Data contract and schema

The monthly response gains, per month, an optional `restatement` object (`snapshot_date`, snapshot and live `realised_pnl_gbp`/`trade_count`) present only when they differ. Persisting snapshots needs **a new table/migration and a `data_model.md` entry**, and the API contract + `openapi.yaml` in the same commit (CLAUDE.md §2) — flagged as the risk the slice already notes (RISK-02: the M (~2d) estimate may be understated). Persistence design is the Data Model & Domain Schema Owner's, not this gate's.

### 2.8 Motion / timing

None beyond the default expand behaviour above.

## 3. §13 Compliance

A record-integrity display over the user's own realised figures. No AI call, no recommendation. §13 pre-check does not apply.

## 4. Frontend Spec Impact

`reports.md` v0.17 → v0.18: §Monthly Financial Table gains the Restated marker and detail row; §Tax Year Summary Bar gains the restated-months notice.

## 5. Testability (CLAUDE.md §2)

The slice marks the diff AC as frontend-visible: Playwright (mocked `restatement` payload) covering marker present/absent, expand/collapse by keyboard, detail values and tones, the Tax Year notice, and the fetch-failure fallback line — or a recorded staging run with the date in the DoQ block.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-21.
Product Owner: confirmed, 2026-09-21 (including "no acknowledge action" and the tax-year notice in place of a second snapshot store).
