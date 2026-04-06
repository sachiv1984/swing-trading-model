Owner: Head of Engineering + Frontend Specifications & UX Owner
Class: Working Document (Class 3)
Status: Active
Last Updated: 2026-04-06
Cycle: 2026-04-05__release-v2.5 (ST-04)

---

# Reports Page — Backend Integration Review

## Summary

The Reports page (`src/pages/Reports.js`) contains two tabs: **Performance** and **Tax Year P&L**. These tabs have fundamentally different integration patterns: the Performance tab relies on the legacy Base44 SDK, while the Tax Year P&L tab is fully wired to the FastAPI backend.

---

## Section-by-Section Mapping

### Performance Tab (default view)

| Section | Component | Data Source | Endpoint / Method | Status |
|---------|-----------|-------------|-------------------|--------|
| Positions data | inline `useQuery` | Base44 SDK | `base44.entities.Position.list("-exit_date")` | Legacy — not FastAPI |
| Portfolio data | inline `useQuery` | Base44 SDK | `base44.entities.Portfolio.list()` | Legacy — not FastAPI |
| Key Metrics (StatsCard row) | `StatsCard` | Derived client-side | Computed from positions in `metrics` useMemo | No backend call |
| Portfolio Growth Chart | `PortfolioGrowthChart` | Derived client-side | Props from `filteredPositions` | No backend call |
| Performance Summary | `PerformanceSummary` | Derived client-side | Props from `metrics` | No backend call |
| Trade Breakdown | `TradeBreakdown` | Derived client-side | Props from `filteredPositions` | No backend call |
| Export Modal | `ExportModal` | Client-side props | Props from `filteredPositions`, `metrics`, `portfolio` | No backend call |

**Note:** All Performance tab metrics (P&L, win rate, profit factor, avg win/loss, fees) are computed entirely in-browser from the Base44 Position entity list. There is no call to `/analytics/metrics`, `/portfolio`, `/trades`, or any other FastAPI endpoint.

### Tax Year P&L Tab

| Section | Component | Data Source | Endpoint | Status |
|---------|-----------|-------------|----------|--------|
| Report data (summary + trades table) | `TaxYearReport` → `useQuery` | FastAPI backend | `GET /reports/tax-year?year=<year>` | Wired |
| PDF download | Button → `handlePdfDownload` | FastAPI backend | `GET /reports/tax-year?year=<year>&format=pdf` | Wired |
| CSV download | Button → `handleCsvDownload` | FastAPI backend | `GET /reports/tax-year?year=<year>&format=csv` | Wired |
| Unrealised P&L card | Rendered from `reportData.estimated_unrealised_pnl` | FastAPI backend | Same `/reports/tax-year` response | Wired (conditional) |

The Tax Year P&L tab is fully wired. The `apiFetch` helper (which forwards `X-API-Key`) is used for all calls to `/reports/tax-year`.

---

## Integration Gaps

### GAP-R01: Performance tab bypasses FastAPI backend entirely

**Severity:** High
**Description:** The Performance tab fetches position and portfolio data via `base44.entities.Position.list()` and `base44.entities.Portfolio.list()` — the legacy Base44 platform SDK. This means:
- All Performance tab metrics are computed from Base44 data, not the authoritative FastAPI data model
- Any position or portfolio state maintained only in the FastAPI database (e.g. GBP-normalised values, FX-adjusted costs, ATR-based data) will not appear in these metrics
- The period filter, date range, and all derived metrics operate entirely client-side on Base44 records

**Impact:** Users may see inconsistent P&L/win-rate/profit-factor figures on the Reports page vs. the Portfolio and Trade History pages (which call the FastAPI backend directly).

**Follow-up:** BLG-BE-08-GAP-01 — Migrate Performance tab to call `/analytics/metrics?period=<period>` for headline metrics and `/portfolio/history` for growth chart data. Filed as a follow-up backlog item (see below).

### GAP-R02: No call to /analytics endpoints from Performance tab

**Severity:** Medium
**Description:** The FastAPI backend exposes `/analytics/metrics?period=all_time|last_7_days|ytd`, `/analytics/cohort`, `/analytics/r-multiple-distribution`, and `/analytics/compliance-metrics`. None of these are called from the Reports page. The Performance tab computes its own simplified equivalents from Base44 data.

**Follow-up:** Same as GAP-R01. The analytics endpoints should replace the client-side metric calculations when the Performance tab is migrated.

### GAP-R03: ExportModal operates on client-side data only

**Severity:** Low
**Description:** The `ExportModal` receives `filteredPositions`, `metrics`, and `portfolio` as props — all derived from Base44 data. Any export generated from the Performance tab therefore inherits the same data-source inconsistency as GAP-R01.

**Follow-up:** Addressed by GAP-R01 migration. No separate backlog item required.

---

## Improvement Proposals (Prioritised)

1. **[P1] Migrate Performance tab data fetching to FastAPI backend** — Replace `base44.entities.Position.list()` and `base44.entities.Portfolio.list()` with calls to `/analytics/metrics`, `/trades`, and `/portfolio`. This resolves GAP-R01 and GAP-R02 and ensures the Reports page shows consistent data. *Estimated effort: L (3–5 days frontend + backend contract alignment).*

2. **[P2] Add period-filtered analytics endpoint** — The current `/analytics/metrics` supports fixed periods (`all_time`, `last_7_days`, `ytd`). Adding `last_30_days`, `last_90_days`, and custom date-range support would allow the Performance tab period selector to drive a backend-computed metric response. *Estimated effort: M.*

3. **[P3] Surface ExportModal via backend** — Add a `GET /reports/performance?period=<period>&format=csv|pdf` endpoint mirroring the `/reports/tax-year` pattern, so exported Performance reports use authoritative backend data. *Estimated effort: M.*

---

## Follow-up Backlog Items

| ID | Title | Priority |
|----|-------|----------|
| BLG-BE-08-GAP-01 | Migrate Reports Performance tab to FastAPI backend analytics endpoints | P1 |

---

## Conclusion

The Tax Year P&L tab is correctly and fully wired to the FastAPI backend. The Performance tab is a legacy integration using the Base44 SDK with no backend calls; all metrics are client-side computed. This is a significant gap that should be addressed in a future sprint to ensure data consistency across the application.
