**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-28__release-v9.8
**Story:** ST-03 (EPIC-01, BLG-FE-190)

# Decision Record — Tax Year Restated-Months Notice Links to a Monthly View That Actually Shows the Counted Months

## 1. Problem

`Reports.js`'s Tax Year tab shows the restated-months notice (`data-testid="taxyear-restated-notice"`, `reports.md` v0.19 §Restated-months notice) for whichever `selectedYear` the user has chosen, but the notice's "Monthly tab" link (`onViewMonthly`) only switches `activeTab` to `"monthly"` — it carries no year context, and `MonthlyPnlTable`'s `GET /reports/monthly-pnl` query is unscoped by year. For a tax year other than the current one, the months the notice is counting can be outside whatever window the Monthly tab actually renders, so the link lands the user somewhere that cannot show what the notice promised.

## 2. Decision

The link becomes year-aware: `onViewMonthly` passes the Tax Year tab's `selectedYear` through to the Monthly tab, which applies it as a filter on load —

- The Monthly tab gains a **Tax Year filter**, matching the existing Tax Year tab's year selector pattern (same control, same position above the table) so the two tabs share one mental model of "which tax year am I looking at."
- Arriving via the restated-months notice link pre-sets this filter to the tax year the notice was shown for; arriving via direct tab navigation defaults to the current tax year, same as today.
- The filter changes only which months are fetched/displayed — no change to the Restated marker, detail row, CSV export, or Unrealised P&L Card behaviour documented in `reports.md` §Monthly Restatement Marker.

This is the minimal fix that keeps the notice's promise true for every tax year, not just the current one, without introducing a second navigation paradigm.

## 3. §13 Compliance

Not applicable — no AI call.

## 4. Frontend Spec Impact

`reports.md` §Monthly Financial Table gains a **Tax Year filter** subsection (control, default value, interaction with the restated-months notice link) and §Restated-months notice is updated to state the link now carries the selected tax year. See spec diff in this cycle's commit.

## 5. Testability (CLAUDE.md §2)

Slice AC requires Playwright coverage of the older-tax-year case: select a non-current tax year with ≥1 restated month, click the notice link, assert the Monthly tab's Tax Year filter reflects that year and the counted month(s) are visible in the rendered table.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-28.
Product Owner: confirmed, 2026-09-28.
