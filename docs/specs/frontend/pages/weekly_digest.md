# weekly_digest.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.2
**Last Updated:** 2026-07-21
**Design Source (v0.1 print/export PDF):** docs/design/2026-07-20__release-v7.6/print-pdf-export/ux_spec.md
**Design Source (v0.2 nav placement + alert-count links):** docs/design/2026-07-21__release-v7.7/nav-notification-digest-consolidation/ux_spec.md
**API contract:** docs/specs/api_contracts/digest_endpoints.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

> **Gap recovery note:** `WeeklyDigest.js` (ST-09, BLG-FEAT-14, v2.4) shipped without a corresponding canonical frontend spec. This file is created at the v7.6 design gate to close that gap, both documenting the existing implementation as-built and specifying the new §4 Print / Export PDF addition (ST-01, BLG-FE-119).

---

## 1. Purpose and User Goals

The Weekly Digest page gives the user a compact, 7-day structured summary of trading activity and system health — realised/unrealised P&L movement, alert activity, compliance score trend, and data freshness — as raw figures with no narrative interpretation.

Users should be able to:
- See the 7-day summary at a glance without navigating multiple pages
- Refresh the digest on demand
- Print or export the digest as a shareable document

---

## 2. Layout Structure

### Page Header
- **Title:** `Weekly Digest`
- **Description:** "7-day trading summary"
- **Actions:** "Print / Export PDF" (§4) and "Refresh" (icon `RefreshCw`, refetches the digest query)

### Content
Single data table, two columns of labels plus a right-aligned value column:

| Field | Unit | Value |
|-------|------|-------|
| Realised P&L (7d) | GBP | `£X.XX` |
| Unrealised P&L Delta (7d) | GBP | `£X.XX` |
| Alerts Fired (7d) | count | integer, **linked** (v0.2) |
| Alerts Dismissed (7d) | count | integer, **linked** (v0.2) |
| Compliance Score (current) | % | `X.X%` |
| Compliance Score (7d ago) | % | `X.X%` |
| Data Staleness | hours | `X.X h` |
| As of (UTC) | timestamp | raw ISO-8601 string |

Missing/null values render as `—` (link is suppressed when the value is `—`).

**Alert-count links (v0.2, ST-02/EPIC-02/v7.7):** `Alerts Fired (7d)` links to `/notifications?since_days=7`; `Alerts Dismissed (7d)` links to `/notifications?since_days=7&read=true` — both values are sourced from the `notifications` table (per `digest_endpoints.md` field definitions), the same table backing the Notification Feed, so both deep-link into the Feed (not Alert History, a separate evaluation-log table). See `docs/design/2026-07-21__release-v7.7/nav-notification-digest-consolidation/ux_spec.md` §2 AC3.

---

## 3. API Reference

- `GET /digest/weekly` — returns `{ status: "ok" | error, data: {...}, message? }`. On `status !== "ok"`, the query throws and the error state (§5) is shown.

---

## 4. Print / Export PDF (v7.6 — ST-01, BLG-FE-119)

**Design source:** docs/design/2026-07-20__release-v7.6/print-pdf-export/ux_spec.md

A **"Print / Export PDF"** action (outline button, `Printer` icon) is shown in the `PageHeader` actions, to the left of "Refresh". Shown only once digest data has loaded successfully (hidden while loading or on error, matching the `DataState` gate already governing the table).

`onClick` calls `window.print()`. No new backend endpoint — output is produced by a shared global print stylesheet (`@media print`), not server-side PDF rendering. The print stylesheet hides the app nav/sidebar and the `PageHeader` actions themselves, and forces a white background / dark text regardless of the active theme. Printed output shows the page title/description and the full data table.

---

## 5. States

| State | Behaviour |
|-------|-----------|
| Loading | `DataState` loading indicator; Print action hidden |
| Error | `DataState` error message with Retry; Print action hidden |
| Loaded | Table populated; Print and Refresh actions both available |

---

## Navigation

**(v0.2, ST-02/EPIC-02/v7.7):** nav item moved from the Analytics group to the System group, positioned directly above "Notifications" — both are activity-summary surfaces. See `navigation.md` v1.4 §Group Structure.

## Known Deviations

None.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.2 | 2026-07-21 | v7.7 design gate — ST-02 (EPIC-02, BLG-FE-114): nav item moved from Analytics to System group (adjacent to Notifications); `Alerts Fired (7d)` / `Alerts Dismissed (7d)` values now link to filtered Notification Feed views (`/notifications?since_days=7[&read=true]`). Design source: nav-notification-digest-consolidation/ux_spec.md. Approved: Product Owner 2026-07-21. Design gate: 2026-07-21__release-v7.7. Head of Specs Team confirmed. |
| 0.1 | 2026-07-20 | v7.6 design gate — initial file creation (gap recovery: `WeeklyDigest.js` shipped v2.4/ST-09/BLG-FEAT-14 without a canonical spec). Documents existing as-built layout, API reference, and states. Adds §4 Print / Export PDF (ST-01, BLG-FE-119). Design source: print-pdf-export/ux_spec.md. Approved: Product Owner 2026-07-20. Design gate: 2026-07-20__release-v7.6. Head of Specs Team confirmed. |
