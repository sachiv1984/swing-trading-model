# weekly_digest.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.6
**Last Updated:** 2026-11-27 (ST-17, v9.18 — This Week's Loop built: `GET /digest/weekly` `loop`, `POST /digest/events`); prior — 2026-11-27 (ST-15/ST-16, v9.18 — built; rulings: "Alerts, last 7 days", realised P&L link on Last 7 Days, red flags list newest first); prior — 2026-11-27 (ST-14, v9.18 — "A week ago" second line reads `closed_trades_total_7d_ago`; ruling 2026-11-27); prior history retained — see prior entries in version control
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
- **Description:** "Your last 7 days in figures. Most figures link to the page where you review them." (v0.5 wording ruling 2026-11-27: "Most figures", since the open P&L change and any "Not available" figure are not linked; v0.3 was "Each figure links…"; before that "7-day trading summary")
- **Actions:** "Print / Export PDF" (§4) and "Refresh" (icon `RefreshCw`, refetches the digest query)

### Figures (v0.3 — ST-15, ST-16)

A definition list (`<dl>`, `data-testid="digest-figures"`), one row per figure: label on the left, value right-aligned in tabular numerals, an optional muted second line. No table, no "Field" or "Unit" column, no unit words, no raw field names.

| Order | Label | Value | Second line | Link on the value |
|-------|-------|-------|-------------|-------------------|
| 1 | Realised P&L, last 7 days | `realised_pnl_7d`, GBP, signed (`formatCurrency`) | — | `/Performance?section=summary&period=last_7_days` (v0.5: the period makes Summary show the same 7-day figure) |
| 2 | Change in open P&L, last 7 days | `unrealised_pnl_delta_7d`, GBP, signed; `null` → "Not enough history yet" (muted) | — | none |
| 3 | Alerts, last 7 days (v0.5; was "Alerts sent": the count is every alert raised, and a Feed row can be "Not sent") | `alerts_fired_7d` | "{n} marked read" from `alerts_dismissed_7d`, linked to `/notifications?since_days=7&read=true` | `/notifications?since_days=7` |
| 4 | Journal completion (all closed trades) | `journal_completion_rate_current`, 1 dp %; when `closed_trades_total` is 0 → "No closed trades yet" (muted, unlinked); `null` (query failed) → "Not available" (muted, unlinked) (v0.4) | "A week ago: {journal_completion_rate_7d_ago}%"; when `closed_trades_total_7d_ago` is 0 → "A week ago: no closed trades" (v0.4, ruling 2026-11-27); `null` → line hidden | `/Performance?section=compliance` (Discipline & Compliance shows the same rate) |
| 5 | Red flags, last 7 days | `red_flags_7d` (new field, ST-16) | — | `/Journal?section=red-flags` (the list is unfiltered, newest first, each row with its age; accepted, v0.5) |

- Links: the value is the link, `data-testid="digest-link-{field}"`, accessible name "{label}: {value}". A null value is never linked. Each link lands on its section heading (Performance `?section=` via `SectionIndex`; Journal tab selected).
- Zero renders as a value ("£0.00" unsigned and neutral, "0"), never "—". A count or realised P&L that is `null` (its query failed) shows "Not available" (muted, unlinked) (v0.5).
- **Label rule (ST-14):** no label on this page says "compliance" for the journal completion rate.

### Freshness Caption (v0.3 — ST-15)

Under the figures, `text-xs text-app-muted`, `data-testid="digest-as-of"`: "Figures as of {d MMM yyyy, HH:mm} UTC · portfolio snapshot {X.X} hours old" (from `as_of_utc` and `staleness_hours`; `staleness_hours` null → "· no portfolio snapshot yet"). No raw ISO string and no "timestamp" text.

### This Week's Loop (v0.3 — ST-17)

A section below the caption, `<h2>` "This week's loop", `data-testid="digest-loop"`.

- **Window caption:** "Monday {d MMM} to today (UTC)". This is an ISO week, unlike the 7-day figures above, so the caption names the dates.
- **Data:** `GET /digest/weekly` `loop` (`week_start`, `signals`, `plans`, `entries`, `reflections`, `reviews`; `digest_endpoints.md` v0.8). The caption's Monday is `week_start`, so the caption and the counts share the server's window. A null or missing count shows "Not available" (muted, unlinked); with no `loop` object (an older backend) every step does, and the caption is hidden (v0.6).
- **Content:** the five step counts defined in `metrics_definitions.md` §Core Loop Metrics (ST-17), in loop order, as labelled integers separated by an `aria-hidden` arrow icon (`ArrowRight`, v0.6: an SVG, so axe can decide its contrast; a "→" text glyph is reported as incomplete), wrapping on narrow screens. Each count links to its step's list page (Signals `/Signals`, Plans `/TradePlans`, Entries `/Positions`, Reflections `/Journal?section=reflections`); the review step's count is this page and is not linked. Labels (v0.6): "Signals", "Plans", "Entries", "Reflections", "Reviews", each shown as "{label}: {n}", which is also the link's accessible name (label in name, WCAG 2.5.3).
- **Counts only.** Step-to-step completion rates are defined for analysis but not shown: with weekly counts of 0–5 a rate is noise.
- **Zero week:** five zeros; no empty-state box.
- **Events:** loading this page writes one `weekly_digest_opened` event per page load (not on refetch or Refresh) through `POST /digest/events`. The digest request waits for that write to settle, at most 1.5 s, so this week's Reviews always include the current visit; a failed write shows nothing. A click on a Today list item link writes one `due_today_action` event (`dashboard.md` TL-31). Nothing else is tracked. Reviews counts distinct UTC days with an open, so repeated loads on one day count once.

---

## 3. API Reference

- `GET /digest/weekly` — returns `{ status: "ok" | error, data: {...}, message? }`. On `status !== "ok"`, the query throws and the error state (§5) is shown.
- **Fields this page reads (v0.5):** `realised_pnl_7d`, `unrealised_pnl_delta_7d`, `alerts_fired_7d`, `alerts_dismissed_7d`, `journal_completion_rate_current`, `journal_completion_rate_7d_ago`, `closed_trades_total` and `closed_trades_total_7d_ago` (ST-14: new names; the old `compliance_score_*` stay as deprecated aliases), `red_flags_7d` (ST-16: `red_flag_events` rows created in the last 7 × 24h; `null` when its query fails), `staleness_hours`, `as_of_utc`; plus `loop` (ST-17: `week_start` and the five counts). Events: `POST /digest/events` (ST-17). Each addition goes in `digest_endpoints.md` and `openapi.yaml` in its story's commit.
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
| 0.6 | 2026-11-27 | ST-17 (EPIC-03, BLG-FEAT-103) built This Week's Loop: data from `GET /digest/weekly` `loop`, caption from its `week_start`, labels "Signals", "Plans", "Entries", "Reflections", "Reviews", null counts "Not available"; the opened event goes through `POST /digest/events`. Definitions approved by the Metrics Definitions & Analytics Owner 2026-11-27 (`ESC-EXEC-20261127-01`). |
| 0.5 | 2026-11-27 | ST-15/ST-16 (EPIC-03) built. Head of UX & Design rulings (the user in session, 2026-11-27): row 3 is "Alerts, last 7 days", not "Alerts sent"; the realised P&L link adds `period=last_7_days`; the Red flags list behind row 5 stays unfiltered, newest first. A null count or realised P&L shows "Not available". The description says "Most figures link…" (was "Each figure links…"). The realised P&L link and the digest share an `exit_date` cutoff only while the server runs on UTC (analytics uses the server date; BLG-BE-239). Figure rows are built in `src/lib/weeklyDigest.js` (unit-tested). |
| 0.4 | 2026-11-27 | ST-14 (EPIC-03, BLG-SPEC-204): row 4's "A week ago" line reads the new `closed_trades_total_7d_ago`; at 0 it says "A week ago: no closed trades" instead of "0.0%". The journal fields are `null` when their query fails: row 4 says "Not available" and hides the second line. Metrics Definitions & Analytics Owner / Product Owner ruling (the user in session, 2026-11-27). |
| 0.3 | 2026-11-18 | v9.18 design gate — rewritten as a readable weekly summary. (ST-15, BLG-UX-15) plain-language figure list, no Field/Unit table, freshness caption, new description. (ST-14, BLG-SPEC-204) "Journal completion" label; `journal_completion_rate_*` and `closed_trades_total` fields. (ST-16, BLG-UX-12) figures link to Performance Summary, Performance Compliance and Journal Red flags; new `red_flags_7d` field (Product Owner decision). (ST-17, BLG-FEAT-103) "This week's loop" section, counts only, and the two events. WD-01–WD-06. Design source: `docs/design/2026-11-18__release-v9.18/weekly-review/decision_record.md`. Approved: Product Owner 2026-11-18. Head of UX & Design sign-off 2026-11-18. Head of Specs Team confirmed. |
| 0.2 | 2026-07-21 | v7.7 design gate — ST-02 (EPIC-02, BLG-FE-114): nav item moved from Analytics to System group (adjacent to Notifications); `Alerts Fired (7d)` / `Alerts Dismissed (7d)` values now link to filtered Notification Feed views (`/notifications?since_days=7[&read=true]`). Design source: nav-notification-digest-consolidation/ux_spec.md. Approved: Product Owner 2026-07-21. Design gate: 2026-07-21__release-v7.7. Head of Specs Team confirmed. |
| 0.1 | 2026-07-20 | v7.6 design gate — initial file creation (gap recovery: `WeeklyDigest.js` shipped v2.4/ST-09/BLG-FEAT-14 without a canonical spec). Documents existing as-built layout, API reference, and states. Adds §4 Print / Export PDF (ST-01, BLG-FE-119). Design source: print-pdf-export/ux_spec.md. Approved: Product Owner 2026-07-20. Design gate: 2026-07-20__release-v7.6. Head of Specs Team confirmed. |
