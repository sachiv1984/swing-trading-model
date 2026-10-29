**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-29__release-v9.14
**Story:** ST-24 (EPIC-04, BLG-FEAT-99)

# Decision Record — Monthly P&L Breakdown by §8 Exit Condition

## 1. Problem

The Monthly P&L report cannot show how much realised P&L came from stop exits, risk-off exits and manual exits. That is the basic question for judging whether §7 and §8 are working. Since v9.13, every stored `exit_reason` maps to one §8 category (`metrics_definitions.md` §Exit Condition Category, `backend/exit_reasons.py`), so the breakdown can now be computed.

## 2. Decision

### 2.1 Placement

A new card, **"Realised P&L by exit condition"** (`data-testid="monthly-exit-condition-card"`), on the Monthly tab. It sits after the AI summary card and before the Unrealised P&L Card. The Monthly Realised P&L table stays first and authoritative, and the AI summary keeps its "directly below the table" position (`reports.md` §AI Summary). The card follows the Tax Year Filter and renders only when the table has at least one row.

### 2.2 Table

One row per month, in the same order and for the same months as the Monthly Financial Table.

| Column | Content |
|--------|---------|
| Month | Full month name and year ("October 2026"). A tax year can contain two Aprils. |
| Stop-loss (§8.1) | P&L, then a muted second line "{n} trade(s)" |
| Risk-off (§8.2) | Same |
| Manual (§8.3) | Same |
| Total | The month's `realised_pnl_gbp` and `trade_count`, the same figures as the Monthly Financial Table |

- A category with no trades in that month shows "—" with no trade line, not "£0.00". This follows the Avg P&L/Trade "—" convention.
- A footer row, **"Tax year total"**, sums each column for the months shown.
- Values use the canonical money format (`design_system.md` §Number and Currency Formatting) and the table's P&L tone rule: green if positive, red if negative, neutral if exactly zero.
- Column headers name the §8 condition, and the category names come from `metrics_definitions.md` §Exit Condition Category, not from raw `exit_reason` strings.
- **Caption** (muted, under the table): "Month-end rebalance exits (§8.4) are recorded as Manual Exit and counted under Manual until a separate exit reason exists." The caption is removed when BLG-SPEC-206 adds a §8.4 value.

### 2.3 States

| State | Display |
|-------|---------|
| Loading | Skeleton rows, as the Monthly table |
| No closed trades | Card not rendered (the Monthly table's empty state already shows) |
| Breakdown fields absent or failed | "Exit-condition breakdown unavailable." (muted, `data-testid="monthly-exit-condition-unavailable"`). The Monthly table is unaffected. |

### 2.4 Tokens (light and dark)

The Reports §Light Theme pairs: card `bg-white border-slate-200 dark:bg-slate-800/50 dark:border-slate-700/50`; figures `text-slate-900 dark:text-white`; trade lines and caption `text-slate-600 dark:text-slate-400`; P&L `text-emerald-700 dark:text-emerald-400` / `text-rose-700 dark:text-rose-400`. No bare dark-only class.

### 2.5 Narrow viewports

The table scrolls horizontally inside the card (`overflow-x-auto`), and the Month column stays visible (`sticky left-0`, card surface background). The page itself never scrolls sideways.

### 2.6 Not changed

The Monthly CSV, the Tax Year CSV and PDF, the AI summary's inputs and `monthly_pnl_snapshots` are unchanged. The breakdown is a display of existing figures.

## 3. §13 Compliance

Display only. A grouping of realised P&L by recorded exit reason. It judges no exit and makes no recommendation.

## 4. Frontend Spec Impact

`reports.md` v0.25 → v0.26: new §Exit Condition Breakdown under §Monthly P&L Report.

## 5. Obligations for Sprint Execution

- The breakdown comes from the backend, so the browser never maps `exit_reason` itself. `GET /reports/monthly-pnl` gains a per-month `by_exit_condition` object keyed by category (`stop_loss`, `risk_off`, `manual`), each `{ realised_pnl_gbp, trade_count }`. Contract (`reports_endpoints.md`) and `openapi.yaml` in the same commit.
- Each month's categories must sum to its `realised_pnl_gbp` and `trade_count`, using the same P&L basis (net or gross of fees) as the table (AC 2 test).
- `metrics_definitions.md` is edited by ST-24, ST-48 and ST-51 (RISK-04). Any wording ST-24 adds goes under §Exit Condition Category.

## 6. Testability (CLAUDE.md §2)

- Playwright (AC 3): with a mocked response, the card renders the three category columns and a Total equal to the month's realised P&L, in light and dark themes. The footer total matches the sum of the months.
- Playwright: with `by_exit_condition` absent, `monthly-exit-condition-unavailable` shows and the Monthly table still renders.
- axe: the Monthly tab in light theme with the card shown passes with no `color-contrast` entry (Reports §Light Theme acceptance).

## 7. Approval

Head of UX & Design: confirmed, 2026-10-29.
Product Owner: confirmed, 2026-10-29.
