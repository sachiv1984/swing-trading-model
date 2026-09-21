**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-21__release-v9.6
**Story:** ST-07 (EPIC-02, BLG-FR-04)

# Decision Record — "Fees Not Recorded" Visibility and P&L Basis Caption on Monthly P&L

## 1. Problem

`fees_paid` is nullable on closed trades and is not referenced by the reporting queries, so it is unclear whether Monthly P&L is gross or net of fees, and a closed trade with a NULL fee silently differs from one with a recorded fee. The story must (a) document the basis and (b) make NULL-fee closed trades **counted and visible** in Monthly P&L.

## 2. Decision

### 2.1 Aggregate notice above the table

Directly under the "Monthly Realised P&L" `h3`, shown **only when the total NULL-fee closed-trade count across the loaded range is ≥ 1**:

`StandingAlert` Info tone, non-dismissible (same primitive and precedent as the Arc 5 low-volume advisory): 
`"{N} closed trade(s) have no fees recorded, so these figures may not reflect their costs."`

`data-testid="monthly-fees-missing-notice"`. Hidden when N = 0, while loading, and on error.

### 2.2 Per-month indicator

In the **Trades** cell, when a month contains `k ≥ 1` NULL-fee closed trades, append a muted secondary text: `"{trade_count} · {k} no fees"`, with `aria-label` `"{trade_count} trades, {k} without fees recorded"`. Months with `k = 0` render exactly as today. `data-testid="monthly-fees-missing-count"`.

### 2.3 Basis caption

A one-line muted caption beneath the table: `"Realised P&L is {net|gross} of recorded fees."` The **wording is set by the story's audit** and mirrors the basis the story documents in `metrics_definitions.md`. If the audit finds a gross-vs-net discrepancy, the caption states the **actual current basis** and a fix item is filed — reported figures are not changed inside this story (per the sealed slice note). The caption is never omitted: an undocumented basis is the defect being fixed.

### 2.4 Data contract

`GET /reports/monthly-pnl` gains, per month, `fees_missing_count` (integer ≥ 0) and a top-level `fees_missing_total`. This is an additive response change; the endpoint's contract file and `openapi.yaml` must be updated in the same commit (CLAUDE.md §2).

### 2.5 CSV export — unchanged

The Monthly CSV export keeps its existing four columns (`Year`, `Month`, `Realised P&L (GBP)`, `Trades`). The NULL-fee count is **not** exported: doing so would alter the export's column contract and its documented reconciliation with the Tax Year CSV (`reports.md` §Monthly CSV Export).

### 2.6 Tax Year tab

Not changed by this story. If the audit shows the same NULL-fee blind spot affects tax-year figures, that is recorded as a follow-up.

### 2.7 Motion / timing

None.

## 3. §13 Compliance

Reports counts and a basis statement about existing data. No AI call, no recommendation. §13 pre-check does not apply.

## 4. Frontend Spec Impact

`reports.md` v0.17 → v0.18: §Monthly Financial Table gains the notice, per-month indicator and basis caption; response fields noted.

## 5. Testability (CLAUDE.md §2)

Playwright with a mocked `monthly-pnl` response: notice present with the right count when N ≥ 1 and absent at N = 0; a month with `fees_missing_count = 2` shows "· 2 no fees"; a month with 0 renders unchanged; CSV column set unchanged.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-21.
Product Owner: confirmed, 2026-09-21.
