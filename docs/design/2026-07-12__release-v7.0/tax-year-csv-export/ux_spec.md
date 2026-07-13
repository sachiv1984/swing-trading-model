**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-12
**Approved by:** Product Owner — 2026-07-12
**Story:** ST-13 — Tax-year P&L CSV export (BLG-FEAT-69)
**Cycle:** 2026-07-12__release-v7.0

---

# UX Specification — Tax-Year P&L CSV Export

## 1. Pre-existing Spec Note (Superseded)

`reports.md` §API Reference (added v2.1, 2026-03-18, under that cycle's own "ST-13" — a coincidental sprint-numbering collision with the current story, not the same work item) currently reads:

> CSV export: `GET /reports/tax-year?format=csv&year=YYYY` — CSV download (no UI control beyond API — URL parameter only; no button on this page)

This was never implemented (confirmed — no `format=csv` handling exists in `backend/routers/`) and is inconsistent with the PDF export on the same page, which **does** have a header button (§Page Header Controls). A URL-parameter-only export is not realistically discoverable by an end user and does not satisfy this story's AC ("User can export a tax-year P&L as CSV"). This decision supersedes the v2.1 note.

## 2. Decision

Add a **"Download CSV"** button to the existing Page Header Controls, alongside "Download PDF", reusing the same approved interaction pattern (idle / generating / success / error) rather than inventing a new one.

**Layout:** `[Year Selector ▼]  [Download PDF]  [Download CSV]` — CSV button placed to the right of PDF (secondary button style, same visual weight as PDF; not primary — this is a records/export utility, not the primary page action).

**Narrow screens:** stacked vertically in the same order (year selector, PDF, CSV — each full width), consistent with the existing PDF stacking rule.

### Download CSV Button States

| State | Label | Behaviour |
|-------|-------|-----------|
| Idle | **"Download CSV"** (with download icon) | Enabled when page loaded successfully |
| Generating | **"Generating…"** (spinner replaces icon) | Button disabled; fires `GET /reports/tax-year?format=csv&year=YYYY` |
| Success | Returns to Idle | Browser file download begins; no success toast required |
| Error | Returns to Idle | Toast notification: `"CSV generation failed. Please try again."` (auto-dismiss 5s) |

Valid for empty years (zero closed trades) — same rule as PDF. Button always enabled once the page loads.

## 3. Data Requirement (AC-02)

Exported CSV figures must match the on-screen summary bar and monthly table exactly — no client-side recalculation (consistent with the page's existing "must not recalculate P&L" rule, §API Reference).

## 4. §13 Compliance

Display/export-only. No new automation or recommendation surface.

## 5. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-12
- **Product Owner:** Approved — 2026-07-12
