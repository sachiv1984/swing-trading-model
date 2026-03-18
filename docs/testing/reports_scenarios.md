**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-03-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `docs/specs/frontend/pages/reports.md` v0.2; `docs/specs/api_contracts/reports_endpoints.md` v0.1
**Sprint:** 2026-03-18__release-v2.1 — ST-18 (closes TEST-GAP-TAX-01)

---

# Acceptance Test Scenarios — Tax Year P&L Report Page

---

## 1. Scope

These scenarios verify the Tax Year P&L report page against the canonical specification. They cover: year selector defaults and interaction, empty state rendering, and tax year boundary assignment. PDF/CSV export is out of scope here — those are covered by ST-12 and ST-13 QA evidence.

> Note: 29 backend integration tests exist in `tests/test_reports_integration.py`. These scenarios do not duplicate backend logic verification — they focus on frontend behaviour and boundary presentation.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| Year selector | `docs/specs/frontend/pages/reports.md §Year Selector` |
| Summary bar | `docs/specs/frontend/pages/reports.md §Summary Bar` |
| Trades table | `docs/specs/frontend/pages/reports.md §Trades Table` |
| Empty state | `docs/specs/frontend/pages/reports.md §Empty State` |
| Tax year boundary | `docs/specs/api_contracts/reports_endpoints.md §Tax Year Boundary` |
| API contract | `docs/specs/api_contracts/reports_endpoints.md §GET /reports/tax-year` |

---

## 3. Scenarios

---

### SC-TAX-01 — Year selector defaults to current tax year; year change triggers re-fetch and updates page

**Component:** Reports page — year selector, summary bar, trades table
**API:** `GET /reports/tax-year?year=YYYY`
**Priority:** P2

#### Preconditions

- User is authenticated and has closed trades in at least two different UK tax years.
- Browser dev tools Network tab is open to observe API calls.
- Today's date is known (to determine the expected default tax year).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to the Reports page. | Page loads. The year selector defaults to the current UK tax year (the tax year whose `tax_year_start` is on or before today's date). A `GET /reports/tax-year?year=YYYY` request fires where `YYYY` is the start year of the current tax year. |
| 2 | Observe the year selector label. | Label format is `"YYYY/YY"` (e.g. `"2025/26"`), matching the `tax_year_label` field in the API response. |
| 3 | Observe the summary bar. | Total Realised P&L, Gross Profit, Gross Loss, Win Rate, and Trades count all render. Values match the `summary` object in the API response exactly — no frontend recalculation. |
| 4 | Observe the trades table. | One row per closed trade in the selected tax year. Columns match the spec (`ticker`, `exit_date`, `realised_pnl_gbp`, etc.). Default sort is by `exit_date` ascending. |
| 5 | Change the year selector to a prior tax year. | A new `GET /reports/tax-year?year=YYYY-1` request fires. The summary bar and trades table re-render with the new year's data. The page does not require a full reload. |
| 6 | Observe the year selector options. | Future tax years (where `tax_year_start` is after today's date) are disabled — they cannot be selected. |

#### Pass criteria

- On load, year selector defaults to the current UK tax year without user action.
- On load, `GET /reports/tax-year?year=YYYY` fires with the correct current year.
- Year change fires a new API request immediately and updates summary bar and trades table.
- Future years are disabled in the year selector.
- All summary bar values match the API response `summary` object — no client-side derivation.

---

### SC-TAX-02 — Empty state renders correctly when no closed trades in selected year

**Component:** Reports page — empty state, summary bar, unrealised P&L card
**API:** `GET /reports/tax-year?year=YYYY` returning `trades: []`
**Priority:** P2

#### Preconditions

- A tax year exists in the selector with no closed trades attributed to it (e.g., a year before the user began trading, or a year with only open positions).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Select a tax year with no closed trades. | The trades table area is replaced by the empty state message: **"No closed trades recorded for the [tax_year_label] tax year."** where `[tax_year_label]` is the human-readable label (e.g. "2023/24 tax year"). |
| 2 | Observe the summary bar. | The summary bar still renders with zero values: Total Realised P&L = £0.00, Gross Profit = £0.00, Gross Loss = £0.00, Win Rate = 0%, Trades = 0. It is not hidden. |
| 3 | Observe the unrealised P&L card. | If `estimated_unrealised_pnl` is non-zero (open positions exist), the unrealised P&L card renders below the empty state. If no open positions exist, the card either renders with £0.00 or is omitted — per spec, it renders if non-zero. |
| 4 | Select a year with closed trades. | The empty state message disappears and the trades table renders normally. |

#### Pass criteria

- Empty state message is verbatim: `"No closed trades recorded for the [tax_year_label] tax year."` with the correct label substituted.
- Summary bar renders with zeroed values in the empty state — it is not hidden or removed.
- Unrealised P&L card renders if `estimated_unrealised_pnl` is non-zero, regardless of empty trades state.
- Transitioning from empty to populated state renders correctly without a page reload.

---

### SC-TAX-03 — Tax year boundary: trade exit date determines year attribution

**Component:** Reports page — trades table, tax year boundary
**API:** `GET /reports/tax-year?year=YYYY`
**Priority:** P1

#### Background

The UK tax year runs from 6 April to 5 April. A trade's tax year is determined by its `exit_date`:
- Exit on **5 April YYYY** → attributed to the **YYYY-1** tax year (the year starting 6 April YYYY-1)
- Exit on **6 April YYYY** → attributed to the **YYYY** tax year (the year starting 6 April YYYY)

This is a backend rule enforced in the API. The frontend must display the results faithfully.

#### Preconditions

- Test data exists with trades exiting on boundary dates: one trade exiting 5 April of a given year, one trade exiting 6 April of the same year.
- Both boundary dates are within the available year range in the selector.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Select the tax year ending 5 April YYYY (i.e., year `YYYY-1`). | The trade with `exit_date = YYYY-04-05` appears in the trades table. |
| 2 | Observe that the trade with `exit_date = YYYY-04-06` is absent. | The 6 April trade does not appear in the YYYY-1 tax year. |
| 3 | Select the tax year starting 6 April YYYY (i.e., year `YYYY`). | The trade with `exit_date = YYYY-04-06` appears in the trades table. |
| 4 | Observe that the trade with `exit_date = YYYY-04-05` is absent. | The 5 April trade does not appear in the YYYY tax year. |
| 5 | Verify summary bar figures for each year reflect only the trades attributed to that year. | Summary totals in each year account only for their respective boundary-date trades. No double-counting. |

#### Pass criteria

- Trade with `exit_date = YYYY-04-05` appears in year `YYYY-1` and not in year `YYYY`.
- Trade with `exit_date = YYYY-04-06` appears in year `YYYY` and not in year `YYYY-1`.
- Summary bar figures for each year include only trades attributed to that year.
- The frontend displays the API response faithfully — no client-side re-attribution of trades to tax years.

---

## 4. Out of Scope

- PDF export rendering — covered by ST-12 QA evidence (Director of Quality sign-off against staging).
- CSV export correctness — covered by ST-13 Head of Engineering sign-off.
- Backend tax year boundary logic — covered by `tests/test_reports_integration.py` (29 existing tests).
- Multi-user or multi-portfolio attribution — out of scope for v2.1 (single-user deployment).
