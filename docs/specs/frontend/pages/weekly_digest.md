# weekly_digest.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.3
**Last Updated:** 2026-11-18 (v9.18 design gate — ST-14/15/16/17: readable weekly summary, journal completion label, onward links, this week's loop); prior — 2026-07-21 (v7.7 design gate — nav placement and alert-count links); prior history retained — see prior entries in version control
**Design Source (v0.1 print/export PDF):** docs/design/2026-07-20__release-v7.6/print-pdf-export/ux_spec.md
**Design Source (v0.2 nav placement + alert-count links):** docs/design/2026-07-21__release-v7.7/nav-notification-digest-consolidation/ux_spec.md
**Design Source (v0.3 weekly summary, links, loop):** docs/design/2026-11-18__release-v9.18/weekly-review/decision_record.md
**API contract:** docs/specs/api_contracts/digest_endpoints.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

> **Gap recovery note:** `WeeklyDigest.js` (ST-09, BLG-FEAT-14, v2.4) shipped without a corresponding canonical frontend spec. This file is created at the v7.6 design gate to close that gap, both documenting the existing implementation as-built and specifying the new §4 Print / Export PDF addition (ST-01, BLG-FE-119).

---

## 1. Purpose and User Goals

*(v0.3 — rewritten at the v9.18 design gate for ST-14, ST-15, ST-16 and ST-17. Design source: `docs/design/2026-11-18__release-v9.18/weekly-review/decision_record.md`.)*

The Weekly Digest is the start of the weekly review: the last 7 days in plain-language figures, each linked to the page where the user reviews it, and this week's core loop (signal → plan → entry → reflection → review) as counts. It reports raw figures with no narrative or advice.

Users should be able to:
- Read the week's figures without knowing API field names or units
- Go from each figure to the page where it is reviewed in one click
- See how much of the core loop they used this week
- Refresh the digest, and print or export it

---

## 2. Layout Structure

### Page Header
- **Title:** `Weekly Digest` (unchanged; the re-review's "Weekly review" rename is not in v9.18)
- **Description:** "Your last 7 days in figures. Each figure links to the page where you review it." (v0.3, ST-15; was "7-day trading summary")
- **Actions:** "Print / Export PDF" (§4) and "Refresh" (icon `RefreshCw`, refetches the digest query)

### Figures (v0.3 — ST-15, ST-16)

A definition list (`<dl>`, `data-testid="digest-figures"`), one row per figure: label on the left, value right-aligned in tabular numerals, an optional muted second line. No table, no "Field" or "Unit" column, no unit words, no raw field names.

| Order | Label | Value | Second line | Link on the value |
|-------|-------|-------|-------------|-------------------|
| 1 | Realised P&L, last 7 days | `realised_pnl_7d`, GBP, signed (`formatCurrency`) | — | `/Performance?section=summary` |
| 2 | Change in open P&L, last 7 days | `unrealised_pnl_delta_7d`, GBP, signed; `null` → "Not enough history yet" (muted) | — | none |
| 3 | Alerts sent, last 7 days | `alerts_fired_7d` | "{n} marked read" from `alerts_dismissed_7d`, linked to `/notifications?since_days=7&read=true` | `/notifications?since_days=7` |
| 4 | Journal completion (all closed trades) | `journal_completion_rate_current`, 1 dp %; when `closed_trades_total` is 0 → "No closed trades yet" (muted, unlinked) | "A week ago: {journal_completion_rate_7d_ago}%" | `/Performance?section=compliance` (Discipline & Compliance shows the same rate) |
| 5 | Red flags, last 7 days | `red_flags_7d` (new field, ST-16) | — | `/Journal?section=red-flags` |

- Links: the value is the link, `data-testid="digest-link-{field}"`, accessible name "{label}: {value}". A null value is never linked. Each link lands on its section heading (Performance `?section=` via `SectionIndex`; Journal tab selected).
- Zero renders as a value ("£0.00" unsigned and neutral, "0"), never "—".
- **Label rule (ST-14):** no label on this page says "compliance" for the journal completion rate.

### Freshness Caption (v0.3 — ST-15)

Under the figures, `text-xs text-app-muted`, `data-testid="digest-as-of"`: "Figures as of {d MMM yyyy, HH:mm} UTC · portfolio snapshot {X.X} hours old" (from `as_of_utc` and `staleness_hours`; `staleness_hours` null → "· no portfolio snapshot yet"). No raw ISO string and no "timestamp" text.

### This Week's Loop (v0.3 — ST-17)

A section below the caption, `<h2>` "This week's loop", `data-testid="digest-loop"`.

- **Window caption:** "Monday {d MMM} to today (UTC)". This is an ISO week, unlike the 7-day figures above, so the caption names the dates.
- **Content:** the five step counts defined in `metrics_definitions.md` (ST-17), in loop order, as labelled integers separated by an `aria-hidden` "→", wrapping on narrow screens. Each count links to its step's list page (Signals, Trade Plans, Positions, Journal → Reflections); the review step's count is this page and is not linked. Labels are the step names from `metrics_definitions.md` in plain words.
- **Counts only.** Step-to-step completion rates are defined for analysis but not shown: with weekly counts of 0–5 a rate is noise.
- **Zero week:** five zeros; no empty-state box.
- **Events:** loading this page writes one "Weekly Digest opened" event per page load (not on refetch or Refresh); a click on a Today list item link writes one "Due today action" event. Nothing else is tracked.

---

## 3. API Reference

- `GET /digest/weekly` — returns `{ status: "ok" | error, data: {...}, message? }`. On `status !== "ok"`, the query throws and the error state (§5) is shown.
- **Fields this page reads (v0.3):** `realised_pnl_7d`, `unrealised_pnl_delta_7d`, `alerts_fired_7d`, `alerts_dismissed_7d`, `journal_completion_rate_current`, `journal_completion_rate_7d_ago` and `closed_trades_total` (ST-14: new names; the old `compliance_score_*` stay as deprecated aliases), `red_flags_7d` (ST-16: `red_flag_events` rows created in the last 7 UTC days), `staleness_hours`, `as_of_utc`; plus the five loop counts (ST-17 names their endpoint and fields in `digest_endpoints.md`). Each addition goes in `digest_endpoints.md` and `openapi.yaml` in its story's commit.
- **Same value, two surfaces:** the journal completion rate here and on Performance → Compliance (`GET /analytics/compliance-metrics` `journal_completion_rate`) must be the same figure for the same data (ST-14 confirms the predicates match).

---

## 4. Print / Export PDF (v7.6 — ST-01, BLG-FE-119)

**Design source:** docs/design/2026-07-20__release-v7.6/print-pdf-export/ux_spec.md

A **"Print / Export PDF"** action (outline button, `Printer` icon) is shown in the `PageHeader` actions, to the left of "Refresh". Shown only once digest data has loaded successfully (hidden while loading or on error, matching the `DataState` gate already governing the table).

`onClick` calls `window.print()`. No new backend endpoint — output is produced by a shared global print stylesheet (`@media print`), not server-side PDF rendering. The print stylesheet hides the app nav/sidebar and the `PageHeader` actions themselves, and forces a white background / dark text regardless of the active theme. Printed output shows the page title/description, the figures, the freshness caption and the loop section (v0.3).

---

## 5. States

| State | Behaviour |
|-------|-----------|
| Loading | `DataState` loading indicator; Print action hidden |
| Error | `DataState` error message with Retry; Print action hidden |
| Loaded | Figures, caption and loop section; Print and Refresh both available |

---

## Navigation

**(v0.2, ST-02/EPIC-02/v7.7):** nav item moved from the Analytics group to the System group, positioned directly above "Notifications" — both are activity-summary surfaces. See `navigation.md` v1.4 §Group Structure.

**Onward links (v0.3, ST-16):** Performance Summary, Performance Compliance, Journal Red flags and Notifications (`navigation.md` v2.5 §Onward Links).

## Testable Acceptance Criteria (v0.3)

| ID | Behaviour | Test |
|----|-----------|------|
| WD-01 | No "Field", "Unit" or "timestamp" text renders; each figure has its plain-language label | Playwright, light and dark (ST-15) |
| WD-02 | No UI label says "compliance" for the journal completion rate | Playwright (ST-14) |
| WD-03 | Realised P&L, journal completion and red flags each link to their section and land on it | Playwright (ST-16) |
| WD-04 | `unrealised_pnl_delta_7d: null` shows "Not enough history yet"; `closed_trades_total: 0` shows "No closed trades yet" | Playwright (ST-15) |
| WD-05 | The loop section shows five counts for the current ISO week, each linked except the review step | Playwright (ST-17) |
| WD-06 | Opening the page writes one event; a Refresh writes none | pytest + Playwright (ST-17) |

## Known Deviations

None.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.3 | 2026-11-18 | v9.18 design gate — rewritten as a readable weekly summary. (ST-15, BLG-UX-15) plain-language figure list, no Field/Unit table, freshness caption, new description. (ST-14, BLG-SPEC-204) "Journal completion" label; `journal_completion_rate_*` and `closed_trades_total` fields. (ST-16, BLG-UX-12) figures link to Performance Summary, Performance Compliance and Journal Red flags; new `red_flags_7d` field (Product Owner decision). (ST-17, BLG-FEAT-103) "This week's loop" section, counts only, and the two events. WD-01–WD-06. Design source: `docs/design/2026-11-18__release-v9.18/weekly-review/decision_record.md`. Approved: Product Owner 2026-11-18. Head of UX & Design sign-off 2026-11-18. Head of Specs Team confirmed. |
| 0.2 | 2026-07-21 | v7.7 design gate — ST-02 (EPIC-02, BLG-FE-114): nav item moved from Analytics to System group (adjacent to Notifications); `Alerts Fired (7d)` / `Alerts Dismissed (7d)` values now link to filtered Notification Feed views (`/notifications?since_days=7[&read=true]`). Design source: nav-notification-digest-consolidation/ux_spec.md. Approved: Product Owner 2026-07-21. Design gate: 2026-07-21__release-v7.7. Head of Specs Team confirmed. |
| 0.1 | 2026-07-20 | v7.6 design gate — initial file creation (gap recovery: `WeeklyDigest.js` shipped v2.4/ST-09/BLG-FEAT-14 without a canonical spec). Documents existing as-built layout, API reference, and states. Adds §4 Print / Export PDF (ST-01, BLG-FE-119). Design source: print-pdf-export/ux_spec.md. Approved: Product Owner 2026-07-20. Design gate: 2026-07-20__release-v7.6. Head of Specs Team confirmed. |
