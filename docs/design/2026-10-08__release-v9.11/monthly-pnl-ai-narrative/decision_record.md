**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Awaiting Product Owner approval
**Cycle:** 2026-10-08__release-v9.11
**Story:** ST-25 (EPIC-04, BLG-FEAT-59) — `stage4_backlog_slice_addendum.md` §ST-25 step 3

# Decision Record — AI Summary on the Monthly P&L Report

## 1. Problem

The Monthly P&L report (`reports.md` §Monthly P&L Report) is a table of figures: realised P&L, trade count and average per trade for each calendar month of the selected tax year, plus fee and restatement markers. `BLG-FEAT-59` asks for an optional plain-language summary of those months, written by an AI model.

Three records constrain the design:
- **§13 determination:** `docs/product/decisions/decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md`, CONDITIONAL, 12 conditions. The ones that bind the UX are Conditions 1, 4, 5, 6, 7 and 12:
  - backward-looking and descriptive;
  - a deterministic fallback;
  - kept apart from the financial record;
  - an advisory badge with `advisory: true`;
  - optional, on request and dismissible;
  - covers the system boundary only.
- **Security checklist** (`ai_endpoint_security_checklist.md`, same folder): a 10/min/IP rate limit and a 40-a-day call cap, both surfaced as 429; a fail-closed 503.
- **Cost estimate** (ST-23): the text is stored per tax year and figures, so a repeat view shows the stored text without a new call.

## 2. Decision

### 2.1 Placement and card

- A separate card, **"AI summary"**, directly **below** the Monthly Realised P&L table card (and its basis caption), above the Unrealised P&L Card. It is outside the table card, its header and the CSV button row above it, so it cannot be read as part of the record (§13 Condition 5).
- **Shell:** the same light+dark pair as the Unrealised P&L Card (`rounded-xl border border-slate-300 dark:border-slate-600/50 bg-white dark:bg-slate-800/30 p-5`). It uses the plain card tier, not the "intelligence-section" treatment in `design_system.md` §Card Hierarchy, so it stays visually subordinate to the authoritative table. Container `data-testid="monthly-narrative-card"`.
- **Rendered only when the Monthly table has at least one row** (`rows.length > 0`). The table has no separate error branch: a failed load yields no rows, so the card does not render then either.

### 2.2 Card header (all visible states)

- **Heading:** **"AI summary"**, in `text-sm font-semibold text-slate-700 dark:text-slate-300`, the same as the Unrealised card heading.
- **Badge:** below the heading, the advisory badge labelled **"AI Advisory"** with this non-dismissible caption: **"Describes your recorded figures only. Not a forecast, recommendation or tax advice."** (§13 Condition 6).
  - **Component:** there is no `AdvisoryBadge` file in `src/` yet. The shipped badge is `src/components/shared/AiDisclaimer.js` `variant="badge"`, whose caption is hard-coded to "All actions require your confirmation". The build adds an optional `caption` prop to that badge variant. It defaults to the current text, so the Dashboard briefing is unchanged. Styling is unchanged: `bg-amber-700 text-white` badge, caption `text-xs text-slate-700 dark:text-slate-300 italic`. There is no dismiss control. This is the `AdvisoryBadge` that `design_system.md` v1.14 describes. Extracting a separately named file is not required for ST-25.
  - **Test IDs:** the badge's own span gets `data-testid="monthly-narrative-badge"`; the caption uses the existing `testId` prop (`monthly-narrative-caption`).
- **Hide control:** on the right, an icon button (`X`, `ghost`, `size="icon"`) with `aria-label="Hide AI summary"` and `data-testid="monthly-narrative-hide"`.

### 2.3 Not yet generated (default)

- Body: muted line **"Get a short written summary of these months."**
- Button: **"Generate summary"** (`outline`, `size="sm"`), `data-testid="monthly-narrative-generate"`.
- Nothing is generated until the button is pressed. There is no automatic or background generation (§13 Condition 7).
- **On page load and on every tax-year change,** the page calls `GET /reports/monthly-pnl/narrative?year=YYYY`.
  - If a summary is stored for the current figures, it renders at once in the populated state. No `POST` fires.
  - Otherwise this state shows.

### 2.4 Generating

- **First generation:**
  - The button shows **"Generating…"** and is disabled.
  - The body shows `DataState`'s default 3-bar skeleton composition (`design_system.md` §Data States, v1.7), coloured with the specified pair `bg-slate-300/60 dark:bg-slate-700/60`. `src/components/ui/skeleton.js` is the only skeleton file on disk and defaults to `bg-primary/10`, so the build passes the paired colours as `className` rather than relying on that default.
- **Regenerate:**
  - The button shows **"Regenerating…"** (the debrief convention) and is disabled.
  - The previous text stays visible. The skeleton is not used.

### 2.5 Populated

- **Body:** the summary text, one or two short paragraphs (`text-sm text-slate-700 dark:text-slate-300`), `data-testid="monthly-narrative-text"`.
- **Action row** below it, the same pattern as the debrief (v9.11 `debrief-regenerate-feedback` record):
  - left, muted `text-xs`: **"Generated {relative time}"**, with the absolute local time in `title`;
  - right: **"Regenerate"** (`outline`, `size="sm"`).
- Generate/Regenerate and Hide are the only actions. No links, and no "apply" or "create plan" affordance (§13 Condition 7).

### 2.6 Standard summary (fallback)

When the generated text fails its checks twice, the API returns a summary written by code from the same figures (`source: "fallback"`, §13 Condition 4).
- It renders in the populated layout, with one muted line above the text: **"The AI summary did not pass its accuracy checks, so a standard summary is shown."** (`data-testid="monthly-narrative-fallback-note"`).
- The badge and caption stay, because the section is still the AI feature.
- **Fixed template:** `{Tax year} so far` covers the in-progress tax year; a past tax year drops "so far".

  > "{Tax year} so far: realised P&L of {total} across {trades} closed trades in {months} months. Highest month: {best month and year}, {best value}. Lowest month: {worst month and year}, {worst value}. {profitable} months ended above zero and {losing} below."

  - A `{fees-caveat}` sentence is appended when any month has `null_fee_trade_count > 0`. It copies the table notice word for word (`Reports.js`):
    - for N = 1: **"1 closed trade has no fees recorded, so these figures may not reflect its costs."**
    - for N > 1: **"{N} closed trades have no fees recorded, so these figures may not reflect their costs."**
  - Signed values use the canonical money format with a minus sign.
  - The template uses no forward-looking, prescriptive or tax wording (Conditions 1 and 4).

### 2.7 Errors and limits

- **Failure** (non-2xx other than 429, including the fail-closed 503, or a network error): an inline message under the action row, **"Could not write the summary. Try again shortly."**
  - Styling follows the form-error pattern in `design_system.md` §Error States: `text-xs text-rose-700 dark:text-rose-400`, with `role="status"`.
  - Any summary already shown stays, and the table and every other section are unaffected.
- **429** (rate limit or daily cap): the same slot and style show the API's `message`, for example "Daily limit for AI summaries reached. Try again tomorrow." The per-minute rate-limit copy ("Rate limit exceeded. Try again later.") is the shared API wording, accepted as is. The button stays enabled.
- `data-testid="monthly-narrative-error"` for both. The message clears on the next Generate or Regenerate press.

### 2.8 Tax-year change during a request

- The `POST` and `GET` responses echo `year`.
- The UI discards any response whose `year` does not match the currently selected tax year. That stops a summary written for one year appearing under another year's table.
- A year change resets the card to whatever that year's `GET` returns.

### 2.9 Hidden

- Pressing Hide replaces the card with a single muted text button, **"Show AI summary"** (`ghost`, `size="sm"`, `data-testid="monthly-narrative-show"`), left-aligned in the card's place.
- Hiding cancels nothing on the server and deletes nothing. Show restores the card in whatever state it was in.
- The choice is remembered per browser in `localStorage` (key `reports.monthlyNarrative.hidden`). Reads and writes are wrapped so that blocked or throwing storage falls back to visible. Default: visible.
- This is the "dismissible" AC 1 asks for. The badge itself has no dismiss control; it goes away only with the content it labels, as `design_system.md` requires.

### 2.10 Layout

```
                                                   [Download CSV]
┌ Monthly Realised P&L ─────────────────────────────────────────────┐
│  table …                                                          │
│  Realised P&L is net of recorded fees.                            │
└───────────────────────────────────────────────────────────────────┘
┌ AI summary                                                    [×] ┐
│ [AI Advisory] Describes your recorded figures only. Not a         │
│               forecast, recommendation or tax advice.             │
│                                                                   │
│ In the 2025/26 tax year so far you closed 23 trades, with         │
│ realised P&L of £1,240.50. March 2026 was the highest month at …  │
│                                                                   │
│ Generated 3 min ago                              [ Regenerate ]   │
└───────────────────────────────────────────────────────────────────┘
┌ Indicative Unrealised P&L …                                       ┐
```

### 2.11 Records, exports and other views

The summary is never written to, included in or used to annotate any of the following (§13 Condition 5, SRB-v1.7):
- the Monthly CSV, the Tax Year CSV or the Tax Year PDF;
- month-end snapshots (`monthly_pnl_snapshots`, DS-20) or any stored P&L figure;
- the Tax Year tab, the Reconciliation tab, the Dashboard or notifications.

**Snapshot side effect:** generating a summary calls `get_monthly_pnl_report()`, which already inserts closed-month snapshots the first time a month is read. That is the same effect as a page view, and the narrative path writes nothing to the snapshot rows.

### 2.12 Months and the tax year

- A UK tax year (6 April to 5 April) spans two Aprils: 6–30 April of the start year and 1–5 April of the next. The table can show both.
- Every month named in the summary, the range figures and the fallback carries its year (for example "April 2025", "April 2026"), so it is never ambiguous.
- The tax-year label (for example "2025/26") is passed as an allowed token so the numeric check accepts it (§13 determination §1).

## 3. States

| State | Body | Actions | Message |
|-------|------|---------|---------|
| Not rendered | — (`rows` empty) | — | — |
| Not generated | intro line | Generate summary, Hide | — |
| Generating (first) | skeleton | Generating… (disabled), Hide | — |
| Regenerating | previous text | Regenerating… (disabled), Hide | — |
| Populated | summary text, generated time | Regenerate, Hide | — |
| Fallback | fallback note, standard summary, generated time | Regenerate, Hide | — |
| Failed / 503 | previous body unchanged | Generate/Regenerate, Hide | error |
| Limited (429) | previous body unchanged | Generate/Regenerate, Hide | API message |
| Hidden | — | Show AI summary | — |

## 4. §13 Compliance

| Condition | How this design meets it |
|-----------|--------------------------|
| 1 Backward-looking | Enforced server-side by the prompt and the output scan. The UI copy ("summary of these months") and the fallback template make no forward claim. |
| 4 Deterministic fallback | §2.6 shows the fallback with an honest note and a fixed template. |
| 5 Separate from the record | A separate card below the table. Kept out of every export, snapshot, stored figure and other view (§2.1, §2.11). |
| 6 Advisory framing | Badge with the exact caption (§2.2); the UI reads `advisory: true` from the response (§7). |
| 7 Optional, on request, dismissible, no affordances | Generated only on a button press; Hide/Show; the only actions are Generate/Regenerate and Hide (§2.3, §2.5, §2.9). |
| 12 Scope | This record and the security checklist are separate reviews from the §13 determination; neither stands in for the other. |

Conditions 2, 3, 8, 9, 10 and 11 are server-side or record-keeping, and are outside this record's scope.

## 5. Accessibility

- The Hide icon button has an `aria-label`. All buttons are keyboard-operable with the standard focus ring.
- Error and limit messages use `role="status"`, so screen readers announce them, and use the paired rose token (≥4.5:1 in both themes, per `design_system.md` §Error States).
- The skeleton is `aria-hidden`; the button label carries the state.
- Contrast: the badge is the existing `AiDisclaimer` badge, and text uses the paired tokens above. The Reports-page axe scan must include the card in its populated state and its error state, in both themes.

## 6. Frontend Spec Impact

`reports.md` v0.20 → v0.21: a new §AI Summary subsection under §Monthly P&L Report, between §Monthly Financial Table (and its subsections) and §Monthly CSV Export. Made by the Frontend Specifications & UX Documentation Owner after the Product Owner approves this record. It carries the fallback template text (§2.6).

## 7. Implementation Notes (for the build, not decided here)

- **API:** `GET` and `POST /reports/monthly-pnl/narrative`. The UI needs these response fields:
  - `year`
  - `narrative` (string | null)
  - `source` (`"ai"` | `"fallback"`)
  - `generated_at`
  - `advisory` (always `true`)

  The full contract, OpenAPI entry, endpoint test registration, SystemStatus count, SC-SS-01b, performance-baseline row and `ai_s13_boundary_test_suite.md` entry follow the CLAUDE.md §2 chain and §13 Condition 6 in the implementation commit.
- **Storage:** one stored row per `(tax year, input-figure hash)`, in its own table (not `monthly_pnl_snapshots`). It is defined as a new DS block in `data_model.md` by the Data Model & Domain Schema Owner at implementation.
- **Tax-language scan:** Condition 4 lists example phrases. The build's list should also cover "capital gain(s)", "CGT", "taxable", "annual exempt amount", "loss relief", "carry forward", "bed and breakfast" and "30-day rule". This is a superset of Condition 4, so no change to the determination is needed.
- **Rounding:** the value check accepts a passed figure at 0–2 decimal places, so the prose may round a figure the table shows to the penny. That is acceptable because the table is authoritative. The prompt asks for figures as given.
- **Fees caveat:** when any month has `null_fee_trade_count > 0`, the prompt tells the model to include the same caveat as the table notice. The fallback carries it by template (§2.6).
- **ST-26:** `claude_audit_log` rows count model calls, including regenerations and failed calls, not generations. ST-26 must count generations, for example by counting stored-narrative writes or by filtering audit rows to one per request. ST-26 decides which.

## 8. Testability (CLAUDE.md §2)

Playwright, with `GET`/`POST /reports/monthly-pnl/narrative` mocked:
1. With monthly data and no stored summary, `monthly-narrative-card` renders in the Not-generated state, with `monthly-narrative-badge` and the exact caption. No `POST` fires until Generate is pressed (AC 1, optional).
2. When the `GET` returns a stored summary, the card renders populated with **no** `POST` (AC 1, on request only).
3. Generate → `monthly-narrative-text` shows the mocked text and "Generated …" (AC 1).
4. Hide → `monthly-narrative-card` is gone and `monthly-narrative-show` is visible. After a reload it stays hidden. Show restores it. With `localStorage` throwing, the card renders visible (AC 1, dismissible).
5. Changing tax year fires a new `GET` for that year. A delayed `POST` response for the old year is discarded.
6. A mocked `source: "fallback"` response shows `monthly-narrative-fallback-note`.
7. A mocked 500 shows `monthly-narrative-error` and keeps the previous text. A mocked 429 shows the API message.
8. With an empty month list, `monthly-narrative-card` is not rendered.
9. The axe scan of the Reports page with the card populated, and again in the error state, reports no violations in either theme.

Backend tests (pytest) cover:
- the §13 output checks: value, direction, and the prescriptive/forward/tax scan;
- regenerate-once and the fallback template;
- the daily cap and its fail-closed path;
- input-hash storage and invalidation on restatement;
- that the Monthly CSV, Tax Year CSV and PDF contain no summary text, and the narrative path writes nothing to `monthly_pnl_snapshots`.

## 9. Approval

Head of UX & Design: confirmed, 2026-10-09. Sprint Execution Engine (agent-mediated, Head of UX & Design role — §5.3), user-directed. First pass Blocked (no `AdvisoryBadge` component exists; bare `text-rose-400` fails light-theme contrast at ~2.8:1). Second pass Approved: the `AiDisclaimer` badge variant's hard-coded caption, existing `testId` prop and the Unrealised card's shell/heading tokens were checked against the code; the AC "optional and dismissible (Playwright)" is fully testable through §8 tests 1, 2 and 4, with edge cases in tests 5 and 8.
Financial Reporting & Records Owner: confirmed, 2026-10-09. Sprint Execution Engine (agent-mediated, Financial Reporting & Records Owner role — §5.3), user-directed. Approved on both passes. §2.11 names every record surface the text must stay out of, with pytest coverage. Two April rows per tax year were confirmed in `get_monthly_pnl_by_tax_year` and handled by year-qualified month names. The extra capital-gains terms, the fixed fallback template and ST-26's generation count cover the tax-related risks.
Product Owner: pending
