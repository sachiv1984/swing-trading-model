**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-18__release-v9.18
**Stories:** ST-14 (BLG-SPEC-204), ST-15 (BLG-UX-15), ST-16 (BLG-UX-12), ST-17 (BLG-FEAT-103) — EPIC-03

# Decision Record — Weekly Digest as a Readable Weekly Summary

## 1. Scope of this record

The four EPIC-03 stories all change `WeeklyDigest.js` and `weekly_digest.md`, in slice order ST-14 → ST-15 + ST-16 → ST-17. This record fixes the page once so each story builds a part of it. Design direction: re-review §8 (finding C3), §14.4 "Review report" template, §15 "Conversion" row.

The page keeps its title "Weekly Digest", route and sidebar place. The re-review's rename to "Weekly review" (§14.2) is not in any v9.18 story; it is recorded as an observation (`design_gate.md` Notes).

Spec impact: `weekly_digest.md` v0.2 → v0.3 (rewritten §1, §2, §3, §5; new §2A This Week's Loop); `navigation.md` v2.5 §Onward Links (Weekly Digest row).

## 2. Data-source check

Every figure the page shows, traced to `docs/specs/api_contracts/digest_endpoints.md` v0.2 `GET /digest/weekly` and its writer `database.py::get_weekly_digest_data` (~5631):

| Figure | Field | Window | Writer basis | Gap |
|--------|-------|--------|--------------|-----|
| Realised P&L | `realised_pnl_7d` | `exit_date ≥ today − 7 days` (UTC) | `trade_history.pnl`, GBP | None |
| Change in open P&L | `unrealised_pnl_delta_7d` | latest `portfolio_history` snapshot minus the closest on or before the cutoff | GBP; `null` when history is short | None |
| Alerts sent / read | `alerts_fired_7d`, `alerts_dismissed_7d` | `notifications.created_at`, last 7 days | count | None |
| Journal completion | `compliance_score_current`, `_7d_ago` → `journal_completion_rate_current`, `_7d_ago` (ST-14) | all closed trades / closed before the window | % of `trade_history` rows with an entry or exit note | **Naming only** (ST-14) |
| Red flags | — | — | — | **Missing.** No digest field. **Product Owner decision (2026-11-18): ST-16 adds `red_flags_7d`** = `COUNT(*)` of `red_flag_events` with `created_at` in the last 7 UTC days, same window as the other 7-day fields; contract, `openapi.yaml` and pytest in ST-16. |
| Freshness | `staleness_hours`, `as_of_utc` | — | hours since last snapshot; compute time | None |

**Same value on two surfaces:** the journal completion rate also shows on Performance → Compliance → Discipline & Compliance (`GET /analytics/compliance-metrics` `journal_completion_rate`, "% of trades with at least one journal note", all closed trades). Both are computed over all closed trades from `trade_history` notes. ST-14 confirms the two SQL predicates are the same (`get_compliance_core_counts` vs the digest query: entry or exit note non-empty) and, if they differ, aligns the digest to the analytics definition in `metrics_definitions.md`. The two surfaces must show the same number for the same data.

**Red-flag window on two surfaces:** the Dashboard Red Flags card counts "since last digest"; this page counts the last 7 days. Different windows, so the labels must name them ("Red flags, last 7 days"); the numbers may differ and that is expected.

## 3. Layout (ST-15)

- **Description** (replaces "7-day trading summary"): "Your last 7 days in figures. Each figure links to the page where you review it."
- **Figures:** a definition list (`<dl>`), one row per figure: plain-language label, value right-aligned in tabular numerals, an optional muted second line. No table, no "Field" or "Unit" column, no unit words.

| Order | Label | Value | Second line | Link (ST-16) |
|-------|-------|-------|-------------|--------------|
| 1 | Realised P&L, last 7 days | `formatCurrency` (GBP, signed) | — | `/Performance?section=summary` |
| 2 | Change in open P&L, last 7 days | `formatCurrency` (GBP, signed); `null` → "Not enough history yet" (muted, not "—") | — | none (no page shows this delta) |
| 3 | Alerts sent, last 7 days | integer | "{n} marked read" (from `alerts_dismissed_7d`, linked to `/notifications?since_days=7&read=true`) | `/notifications?since_days=7` (unchanged from v0.2) |
| 4 | Journal completion (all closed trades) | `formatPercent` 1 dp | "A week ago: {x}%" | `/Performance?section=compliance` |
| 5 | Red flags, last 7 days | integer | — | `/Journal?section=red-flags` |

- **Freshness caption** under the list (`text-xs text-app-muted`, `data-testid="digest-as-of"`): "Figures as of {d MMM yyyy, HH:mm} UTC · portfolio snapshot {X.X} hours old". `staleness_hours` null → "· no portfolio snapshot yet". No raw ISO string, no "timestamp".
- **Links:** the value is the link (as v0.2 does for alerts), `data-testid="digest-link-{field}"`, accessible name "{label}: {value}". A null value is never linked.
- **Print:** unchanged (§4); the list prints as shown.

### Worked examples

| Input | Row 1 | Row 2 | Row 4 |
|-------|-------|-------|-------|
| No trades closed in 7 days | "£0.00" (linked) | delta as computed | unchanged rate |
| `unrealised_pnl_delta_7d: null` (new user, < 7 days of snapshots) | — | "Not enough history yet" | — |
| No closed trades at all | "£0.00" | — | "0.0%" and "A week ago: 0.0%" (the endpoint returns 0.0, not null, when there are no trades). ST-15 shows "No closed trades yet" instead of 0.0% when the trade count is 0. The digest has no trade count, so ST-14 adds `closed_trades_total` beside the renamed fields (contract + `openapi.yaml`); without it, 0.0% for "no trades" and 0.0% for "no notes" look the same |
| `realised_pnl_7d: -0.004` | "£0.00", unsigned, neutral (design_system zero rule) | — | — |

## 4. Rename (ST-14)

- Labels: "Journal completion" everywhere on this page; no UI label says "compliance" for this figure.
- API: `journal_completion_rate_current` and `journal_completion_rate_7d_ago` added; `compliance_score_current`/`_7d_ago` kept as deprecated aliases with the same values (`digest_endpoints.md` deprecation note, `openapi.yaml` `deprecated: true`). The page reads the new names.
- `closed_trades_total` (integer) added in the same change, per §3's worked example.

## 5. Onward links (ST-16)

- The slice's restated AC said the journal completion link goes to "the Journal section that shows journal completion". **No Journal section shows it** (`journal.md` v1.1 §4: Reflections, Red flags, Position notes). Journal completion is shown on Performance → Compliance (Discipline & Compliance card, `performance.md` §4). The link therefore goes to `/Performance?section=compliance`, recorded in `navigation.md` §Onward Links (addendum correction).
- Landing: each link lands on its section with the section heading in view, using the existing `?section=` behaviour of Performance (`SectionIndex`, focus to the `<h2>`) and Journal (tab selected).

## 6. This week's loop (ST-17)

- **Placement:** a section below the figures and freshness caption, `<h2>` "This week's loop", `data-testid="digest-loop"`.
- **Window caption:** "Monday {d MMM} to today (UTC)" — an ISO week, unlike the 7-day figures above, so the caption names the dates. On a Monday the section shows Monday only.
- **Content:** the five step counts as five labelled values in loop order, separated by a "→" glyph (`aria-hidden`), wrapping on narrow screens. Each count links to the page behind it. Labels and targets come from ST-17's `metrics_definitions.md` entries; the design fixes only this: label = the step's plain-language name (e.g. "Signals", "Plans", "Entries", "Reflections", "Reviews"), value = integer count, link = that step's list page (Signals, Trade Plans, Positions, Journal → Reflections, and for the review step this page itself, so it is not linked).
- **No completion rates on the page.** The step-to-step rates are defined in `metrics_definitions.md` for analysis, but with weekly counts of 0–5 a rate is noise ("0 of 0", "100%" from 1 of 1). The page shows counts only.
- **Zero week:** all five counts render as 0; no empty-state box. Worked examples for the metric definitions (quiet week, week with no signals, a reflection written the week after the exit) are ST-17's AC 1 and live in `metrics_definitions.md`.
- **Events:** opening this page writes one "Weekly Digest opened" event per page load (not per refetch or Refresh click); taking a Due today action writes one event per click on a Today list link (`Review exit`, a Grace/Stops row, `Research`, `Plan this`). Nothing else is tracked; no page-view tracking elsewhere.
- **§13:** counts of the user's own actions, no advice. No AI call.

## 7. Approvals

- Head of UX & Design: approved (agent-mediated, Design Gate Engine), 2026-11-18.
- Product Owner: approved (the user, in session, 2026-11-18); `red_flags_7d` chosen by the Product Owner.
