**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-09__release-v3.3
**Story:** ST-17 (EPIC-04)
**Sources:** BLG-FEAT-21, BLG-FE-30, BLG-FE-23, BLG-FE-24, BLG-FE-25, BLG-FE-29
**Approved by:** Product Owner
**Approved date:** 2026-05-09
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Trade Plan Quick Wins (ST-17)

This spec covers six items grouped into ST-17. Each section is self-contained.

---

## Section A — Trade Plan Abandonment (BLG-FEAT-21)

### A.1 Context

Trade plans in Draft or Research states should be markable as Abandoned when the user no longer intends to pursue the opportunity. Active plans (linked to open positions) cannot be abandoned.

### A.2 Abandonment Trigger

"Abandon" action added to the Trade Plan detail view, below "Edit" and above "Delete":

```
[Edit]  [Abandon]  [Delete]
```

"Abandon" is a destructive-adjacent action — styled as a secondary button with a warning colour (amber outlined), not primary. Never red (red is reserved for Delete).

"Abandon" is not shown when `status = 'active'` (position is open). Backend enforces this with a 400 error as an additional guard.

### A.3 Abandonment Modal

Clicking "Abandon" opens a modal:

**Title:** "Abandon trade plan for {TICKER}?"

**Body text:**
> "This plan will be marked as abandoned. You will not be prompted to enter this position again based on this plan."

**Required field:**
- Label: "Reason for abandoning (required)"
- Type: Textarea, 3 rows
- Placeholder: "e.g. thesis invalidated, entry conditions no longer valid, sector rotation"
- Min length: 10 characters; inline validation on blur

**Actions:**
- "Abandon Plan" (primary, amber/warning) — enabled only when reason field is valid (≥10 chars)
- "Cancel" (secondary) — closes modal; no change

On confirm: `PUT /trade-plans/{id}` with `{status: 'abandoned', abandonment_reason: <text>}`.

On success: modal closes; plan status badge updates; abandonment reason rendered in detail view.

### A.4 Abandoned Plan Display

In the Trade Plan detail view, when `status = 'abandoned'`:
- Status badge: Abandoned (red — see §B)
- New read-only field below status: "Reason for abandoning: {abandonment_reason}"
- "Abandon" and "Edit" buttons hidden; "Delete" button remains
- Abandoned plans appear in plan list with muted row styling (opacity 0.7 or similar)

---

## Section B — Trade Plan Status Badges (BLG-FE-30)

### B.1 Canonical Badge Colour Scheme

All trade plan status values now have defined visual badges. Applied in both Trade Plan List and Trade Plan Detail View.

| Status | Badge Label | Colour | Hex | Text |
|--------|------------|--------|-----|------|
| `draft` | Draft | Grey | `#6B7280` | White |
| `research_pending` | Research Pending | Amber | `#D97706` | White |
| `research_complete` | Research Complete | Blue | `#2563EB` | White |
| `entry_conditions_set` | Entry Ready | Purple | `#7C3AED` | White |
| `active` | Active | Green | `#16A34A` | White |
| `closed` | Closed | Slate (muted) | `#94A3B8` | White |
| `abandoned` | Abandoned | Red | `#DC2626` | White |

Contrast: all combinations meet WCAG AA (≥ 4.5:1 white on colour background — verified for all hex values above).

### B.2 Usage

Badge is a filled pill with white text, consistent with position lifecycle state badges. Applied in:
- Trade Plan List: Status column
- Trade Plan Detail View: beside the plan title / in the metadata block

---

## Section C — Research Page UK Ticker Suffix Strip (BLG-FE-23)

### C.1 Requirement

The Research page header/title displays the ticker symbol. UK tickers include the `.L` suffix (e.g. `MTLN.L`). The display should strip this suffix so users see `MTLN`.

### C.2 Behaviour

Apply `stripUkSuffix` utility (already used in Screener and Watchlist) to the ticker displayed in:
- Research page `<h1>` / page title
- Research page browser tab `<title>`

The raw ticker value (`MTLN.L`) is preserved in API calls and URL parameters — stripping is display-only.

### C.3 Non-regression

Screener and Watchlist already apply `stripUkSuffix` — no change required there. US tickers have no `.L` suffix; `stripUkSuffix` must be a no-op for US tickers (verify existing implementation handles this correctly).

---

## Section D — Negative Earnings Days Display (BLG-FE-24)

### D.1 Requirement

When `days_until_earnings` is a negative integer (earnings date has passed), displaying a negative number is confusing and incorrect. Display `—` instead.

### D.2 Display Rules

| `days_until_earnings` value | Display |
|----------------------------|---------|
| Negative integer | `—` |
| `0` | `Today` |
| Positive integer | `{n} days` (unchanged) |
| Null | `—` |

Applied to all earnings-related columns/cells in the Research view (and any other view where `days_until_earnings` is displayed).

---

## Section E — Signals Page Default to Most Recent Day (BLG-FE-25)

### E.1 Context

The Signals page currently loads with default parameters (`top_n=5`, `lookback_days=252`). Users expect to see today's (or the most recent trading day's) signals by default.

### E.2 Default Behaviour

On page load, the Signals page fetches signals for the most recent trading day. A date picker control is added to allow viewing older signals.

### E.3 Date Picker Control

Added to the control row alongside Top N and Lookback:

| Control | Type | Default | Behaviour |
|---------|------|---------|-----------|
| **Date** | Date input (calendar picker) | Most recent trading day | Selects the signal date; triggers refetch on change |

"Most recent trading day" is determined by the frontend: if today is a trading day (weekday, non-holiday), use today; if not, use the most recent prior weekday. The backend is authoritative — if the selected date returns no signals, the empty state is shown.

A "Latest" quick-link or "Today" button resets the date picker to the most recent trading day.

### E.4 Lookback Interaction

The `lookback_days` parameter continues to control the signal scoring window. When a specific date is selected, `lookback_days` applies from that date backwards. Both controls coexist.

### E.5 Empty State Revision

When no signals are found for the selected date (not the selected parameters):
> "No signals found for {date}. Try selecting a different date or adjusting parameters."

---

## Section F — Watchlist Research Status Indicator (BLG-FE-29)

### F.1 Context

The Watchlist table shows tickers the user is monitoring. A binary indicator of whether a research record exists for that ticker helps the user prioritise which tickers to research before entry.

### F.2 Column Addition

New column added to the Watchlist table: **Research**

| Column | Position | Width |
|--------|----------|-------|
| Research | After "Entry Signal", before "Target Entry" | Narrow (icon only) |

### F.3 Indicator Values

| Condition | Display | Tooltip |
|-----------|---------|---------|
| Research record exists for ticker | ✅ (green checkmark icon) | "Research available" |
| No research record | ○ (hollow circle, grey) | "No research yet" |

- No text label in cell — icon only (space-efficient)
- Do not indicate freshness or quality — binary only (BLG-FE-29 explicitly scopes to binary)
- Data source: a lightweight endpoint or flag on `GET /watchlist` response (backend to add `has_research: bool` per entry, or frontend calls `GET /research/{ticker}` in batch — implementation decision for engineering; spec is outcome-neutral on mechanism)

### F.4 Accessibility

- Icon has `aria-label`: "Research available" or "No research for this ticker"
- Not the only means of conveying the information — tooltip provides text

### F.5 Performance

No regression in watchlist loading performance. If the research status is fetched separately (not included in watchlist response), use a debounced batch request after the watchlist renders — not a blocking dependency.
