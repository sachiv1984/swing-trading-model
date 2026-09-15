**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.3
**Last Updated:** 2026-09-15 (v9.4 sprint execution — ST-25/BLG-FE-174: `SkeletonRow` implementation confirmed refactored to compose from the shared `Skeleton` primitive; no visual change, new Playwright coverage passes); prior — 2026-09-14 (v9.4 design gate — ST-25/BLG-FE-174: §8 loading state now cites the canonical loading-skeleton pattern/shared `Skeleton` primitive); prior — 2026-09-04 (v9.1 ST-07, BLG-SPEC-99: added §9 Keyboard Navigation Requirements)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v1.2):** docs/design/2026-09-14__release-v9.4/loading-skeleton-standardisation/decision_record.md
**Design Source:** docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md
**API contract:** docs/specs/api_contracts/portfolio_api_contract.md

---

# red_flag_journal.md — Red Flag Journal

**Purpose:** The Red Flag Journal is a display-only audit log of instances where the operator deviated from their stated trading strategy — pre-entry rule overrides, checklist skips, and stop/drawdown prompt dismissals. Introduced in v3.9 (Arc 5, SI-03, ST-08).

**§13 Compliance:** Display-only audit log. No automated decisions or recommendations.

---

## 1. Purpose and User Goals

Users should be able to:

- Review all instances where they overrode a strategy gate or dismissed a strategy prompt
- Filter events by type, ticker, and date range
- Understand the context of each deviation

---

## 2. Navigation and Route

- Route: `/red-flag-journal`
- Page title: **"Red Flag Journal"**
- Nav group: **Trading** (after Trade Reflection)
- Nav item label: **"Red Flag Journal"**
- `createPageUrl` key: `"RedFlagJournal"` (must be added to the `createPageUrl` map in `App.js`)

---

## 3. API Reference

`GET /portfolio/red-flag-journal?page={n}&page_size=20&event_type={type}&ticker={ticker}&since={date}`

Response: `{ total: int, page: int, page_size: int, items: [...] }`

Each item: `{ event_type, ticker, context (JSON), created_at }`

---

## 4. Filter Controls

Located above the event list.

| Control | Type | Options |
|---------|------|---------|
| Event Type | Dropdown | "All types" (default); "Pre-Entry Override"; "Checklist Skipped"; "Stop Prompt Dismissed"; "Drawdown Prompt Dismissed" |
| Ticker | Text input | Free-text; `ticker` query param |
| Date Range | From / To date inputs | ISO dates; From → `since` query param |

Filters applied additively (AND logic). Changing any filter triggers a new API request.

---

## 5. Event List

Paginated list. 20 events per page. Most recent first.

### Event Row Layout

| Element | Source | Display |
|---------|--------|---------|
| Icon | `event_type` | ⚠ pre_entry_override; ☑ checklist_skipped; ⏭ stop_prompt_dismissed; ⬇ drawdown_prompt_dismissed |
| Type label | `event_type` | "Pre-Entry Override" / "Checklist Skipped" / "Stop Prompt Dismissed" / "Drawdown Prompt Dismissed" |
| Ticker | `ticker` | Uppercase; `.L` suffix stripped for display (LSE tickers) |
| Context summary | `context` JSON | Short human-readable summary extracted from context (fallback: raw JSON string) |
| Date | `created_at` | Relative time (e.g. "2 hours ago"); absolute date shown on hover |

---

## 6. Pagination

- Previous / Next page buttons
- "Page {N} of {M}" indicator
- "{total} events recorded" count

---

## 7. Empty States

| Condition | Display |
|-----------|---------|
| No events, no active filters | "No strategy deviations recorded yet" + sub-text: "Override events will appear here when you proceed past a strategy gate warning." |
| No events, active filters | "No events match your current filters." + "Clear filters" link |

---

## 8. Loading and Error States

| State | Display |
|-------|---------|
| Loading | Skeleton rows (matching event row height) — Table/List Row Skeleton template (`base44_prompt_template_library.md` §8), backed by the shared `Skeleton` primitive (`design_system.md` §Shared UI Components → Data States), per the v9.4 canonical loading-skeleton pattern (ST-25, BLG-FE-174). **Implementation confirmed (v1.3):** `RedFlagJournal.js`'s `SkeletonRow` imports and renders `<Skeleton>` (previously page-local `bg-*/animate-pulse` divs), with `bg-slate-700`/`bg-slate-700/60` className overrides preserving the exact pre-existing colours. No visual change; new `tests/e2e/red-flag-journal.spec.js#SC-RFJ-06` passes. |
| Error | "Unable to load Red Flag Journal. Please try again." + Retry button |

---

## 9. Keyboard Navigation Requirements

*(v1.1 — ST-07, BLG-SPEC-99, EPIC-01, v9.1. Documentation-only requirements baseline for this table-based page — no implementation change ships with this addition; conformance is verified per-component as each is next touched.)*

- **Filter Controls:** the Event Type dropdown, Ticker text input, and From/To date inputs are all reachable via Tab in the order shown in §4 and operable via keyboard alone (dropdown opens/selects via Enter/Space + arrow keys, per native `<select>`/combobox behaviour).
- **Event List:** row order is the DOM/tab order (§5's "most recent first" ordering); rows themselves are not individually focusable unless a row exposes its own interactive control, in which case that control follows tab order top-to-bottom.
- **Pagination:** Previous / Next buttons are reachable via Tab and activate on Enter or Space; a disabled Previous/Next button (first/last page) is skipped in tab order or exposes `disabled`/`aria-disabled` rather than being silently inert.
- **"Clear filters" link (empty state):** reachable via Tab, activates on Enter.
- **Retry button (error state):** reachable via Tab, activates on Enter or Space.
- **Focus indicator:** every interactive element above renders a focus indicator meeting `docs/specs/frontend/design_system.md`'s "Focus indicator contrast" rule (≥3:1 against adjacent colour, both themes).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.3 | 2026-09-15 | v9.4 sprint execution — ST-25 (EPIC-06, BLG-FE-174): §8 implementation confirmed — `RedFlagJournal.js`'s `SkeletonRow` refactored to compose from the shared `Skeleton` primitive (colour overrides preserve visual output). New `SC-RFJ-06` Playwright coverage added, passes. |
| 1.2 | 2026-09-14 | v9.4 design gate — ST-25 (EPIC-06, BLG-FE-174): §8 Loading state now cites the canonical loading-skeleton pattern — Table/List Row Skeleton template (`base44_prompt_template_library.md` §8) backed by the shared `Skeleton` primitive. No visual change. Design source: `docs/design/2026-09-14__release-v9.4/loading-skeleton-standardisation/decision_record.md`. Head of UX & Design sign-off: 2026-09-14. Product Owner approved: 2026-09-14. Head of Specs Team confirmed. |
| 1.1 | 2026-09-04 | v9.1 ST-07 (BLG-SPEC-99, EPIC-01): added §9 Keyboard Navigation Requirements — documentation-only baseline covering Filter Controls, Event List, Pagination, empty/error-state controls, and focus-indicator contrast. No implementation change. |
| 1.0 | 2026-05-21 | Initial spec. v3.9 design gate — full page spec for Red Flag Journal (SI-03, EPIC-03, ST-08). Design source: docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md. Approved: Product Owner 2026-05-21. Head of Specs Team confirmed. |
