# positions.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 2.8
**Last Updated:** 2026-08-17
**Design Source (v8.2 additions):** docs/design/2026-08-04__release-v8.2/compliance-recheck-all-pass-state/decision_record.md
**Design Source (v7.9 additions):** docs/design/2026-07-27__release-v7.9/trailing-stop-explainer-tooltip/ux_spec.md
**Design Source (v7.0 additions):** docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md, docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md
**Design Source (v6.9 additions):** docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md, docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md
**Design Source (v2.3 additions):** docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md
**Design Source (v3.3 additions):** docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md, docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md, docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md
**Design Source (v3.4 additions):** docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md, docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md
**Design Source (v3.5 additions):** docs/ux_specs/paper-trading/ux_spec.md
**Design Source (v6.2 additions):** docs/design/2026-06-24__release-v6.2/trailing-stop-display/ux_spec.md, docs/design/2026-06-24__release-v6.2/risk-off-exit-alert/ux_spec.md, docs/design/2026-06-24__release-v6.2/ai-chat-widget/ux_spec.md
**Design Source (v6.4 additions):** docs/specs/qa/ai_disclaimer_visibility_assessment.md (BLG-UX-02 remediation)
**Design Source (v6.7 additions):** docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md (BLG-FE-88 remediation)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.8 | 2026-08-17 | v8.9 ST-02 (BLG-BE-103, EPIC-01): §Trailing Stop Column — corrected currency-basis defect. `current_trailing_stop` (GBP-converted for US positions) was being rendered next to the native currency symbol alongside `initial_stop` (native), producing two numerically different values that were really the same stop. Table View and Grid View now render the new `current_trailing_stop_native` field, matching this section's pre-existing "Display format: Native currency" rule (which the implementation had not satisfied since v6.2). No column layout or design change — value-source correction only. |
| 2.7 | 2026-08-04 | v8.2 design gate — ST-02 (EPIC-01, BLG-FE-105): §Compliance Recheck Panel (Modal) — all-rules-pass state specified explicitly. Adds an affirmation line ("All 5 checks passed — no action needed.", `text-emerald-400`, existing pass colour token) in the same layout slot as the warn/fail acknowledgement block, shown only when `overall_status === "pass"`. Closes the previously-undesigned asymmetry between the warn/fail path (explicit acknowledgement block) and the pass path (nothing). No new colour or interactive element introduced. Design source: `docs/design/2026-08-04__release-v8.2/compliance-recheck-all-pass-state/decision_record.md`. Head of UX & Design sign-off: 2026-08-04. Product Owner approved: 2026-08-04. Head of Specs Team confirmed. |
| 2.6 | 2026-07-27 | ST-05 (BLG-FEAT-87, EPIC-05, v7.9) implementation: corrected §Trailing Stop Column's tooltip placement description — the v6.2-described separate "Trail Stop" column/stat label does not exist in the shipped UI (Table View has one combined "Stop" header; Grid View has no standalone label). Placed the explainer icon on the actual anchors instead (combined "Stop" header; inline with the "Init:" subtext line in the Grid tile) — closest faithful placement given the real UI, pre-existing gap noted but not fixed (out of this story's scope). |
| 2.5 | 2026-07-27 | v7.9 design gate: (ST-03, BLG-FEAT-87) §Trailing Stop Column — added "Why is my stop moving?" explainer tooltip (info icon after the "Trail Stop" column header / Grid View stat label; hover/focus reveals plain-language explanation of §7.2 profit-aware stop logic and §7.3 stop-movement constraint, reviewed against `strategy_rules.md` §7 for accuracy). Static text, no API dependency, no change to the underlying calculation or Trail Stop Modal. Design source: trailing-stop-explainer-tooltip/ux_spec.md. Approved: Product Owner 2026-07-27. Head of Specs Team confirmed. |
| 2.4 | 2026-07-14 | v7.1 sprint execution: (ST-03, BLG-FE-107) Closed `DEV-EPIC01-ST05-01` — Table View's `AlertsCell` RISK OFF badge brought into spec compliance (`#1E40AF` blue-800, label "RISK OFF", no icon), matching the v7.0 Grid View badge. No spec text change — §Alerts Column was already correct; only §Known Deviations updated to record the resolution. (ST-04, BLG-BE-61) §Last Reviewed Column — documented `NULL`/backfill semantics for `last_reviewed_at` (falls back to `entry_date`, verified against production data). §Position Lifecycle State Badge — added explicit confirmation that review-cadence is a metadata annotation, not a 5th lifecycle state (4 states unchanged). No visual/behavioural change — documentation only. |
| 2.3 | 2026-07-13 | v7.0 sprint execution: (ST-01, BLG-SPEC-80) Added explicit Grid View badge-placement subsection to §Alerts Column — documents the dedicated alert row (below header, above stat tiles) where RISK OFF/GAP RISK badges render in Grid View, closing the gap that was the root cause of `BLG-FE-102` (Grid View never had separately-specified badge placement, only Table View's Alerts column was documented in this much detail). No visual/behavioural change — documentation only, confirms placement ST-02 implements. |
| 2.2 | 2026-07-12 | v7.0 design gate: (ST-05, BLG-FE-104) Combined GAP RISK / RISK OFF badge differentiation review — confirmed existing hue (blue-800 vs amber-600) + mandatory text label already satisfy distinguishability; added stacking spacing rule (4px min gap, RISK OFF above GAP RISK, no truncation) for the previously-unreviewed combined/stacked state, Table and Grid View. (ST-15, BLG-FEAT-68) Last Reviewed column added — Table View (after Alerts, before Actions) and Grid View card footer; `last_reviewed_at` field; amber flag + clock icon at ≥14 days, suppressed when position already flagged by Grace Period or Drawdown prompts; inline "Mark Reviewed" icon-button calls `PATCH /positions/{id}/mark-reviewed`. §13 compliant — display-only, no automated action beyond explicit user-triggered timestamp update. Design sources: v7.0 additions listed above. Head of UX & Design sign-off: 2026-07-12. Product Owner approved: 2026-07-12. Head of Specs Team confirmed. |
| 2.1 | 2026-07-10 | v6.9 design gate: (ST-01, BLG-FEAT-64) Compliance Recheck Panel — "Recheck Compliance" action added to Table View Actions column and Grid View card footer for all open positions; opens modal reusing `PreEntryValidationPanel`'s pass/warn/fail visual pattern against the same 5 SI-01 rules, evaluated against current (not entry-time) conditions; session-local override acknowledgement, no persisted state. §13 compliant — re-application of existing deterministic rules, no new automation. (ST-02, BLG-FEAT-65) Gap Risk Badge added to the existing Alerts column — "GAP RISK" badge (amber-600 `#D97706`) when an earnings date falls before the next session or on Friday-close weekend holds; tooltip shows reason(s) plus historical average gap magnitude for the ticker or "insufficient history"; stacks with existing RISK OFF badge in the same cell. §13 compliant — informational only, no gap direction/magnitude prediction. Design sources: v6.9 additions listed above. Head of UX & Design sign-off: 2026-07-10. Product Owner approved: 2026-07-10. Head of Specs Team confirmed. |
| 2.0 | 2026-07-06 | v6.7 design gate — AI Trade Advisor Widget footer disclaimer light-theme fix (ST-02, BLG-FE-88): `text-slate-400` → `text-slate-600 dark:text-slate-400` (bare class had no light-mode companion; was 2.34–2.56:1 FAIL in light theme). Dark-theme value unchanged — already matches the canonical secondary-text token. Design source: `docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md` §4. Head of UX & Design sign-off: 2026-07-06. Head of Specs Team confirmed. |
| 1.9 | 2026-07-02 | v6.4 design gate — AI Trade Advisor Widget footer disclaimer contrast fix (ST-10, BLG-UX-02): `text-slate-600` → `text-slate-400` (≈1.9:1 → ≥4.5:1 on `bg-slate-800`, WCAG AA); `data-testid="ai-chat-advisory-footer"` added to footer container to enable Playwright assertion (resolves coverage gap noted in QA assessment). Design source: `docs/specs/qa/ai_disclaimer_visibility_assessment.md` (finding C5, approved 2026-06-29). Head of UX & Design sign-off: 2026-07-02. Head of Specs Team confirmed. |
| 1.8 | 2026-06-24 | v6.2 design gate: (ST-02) Trail Stop column added to Table View — displays `current_trailing_stop` alongside existing Initial Stop (renamed from "Stop"); breach badge "⚠ BREACH" (orange #EA580C) shown inline when `current_price ≤ current_trailing_stop`; Grid View adds Trail value and ⚠ icon. (ST-05) Alerts column added to Table View — shows "RISK OFF" badge (deep blue #1E40AF) when `risk_off_exit = true`; US/UK market isolation server-enforced. (ST-09) AI Trade Advisor Widget — fixed-position floating chat button (bottom-right); expands to 350×480px panel; display-only advisory; stateless per request; §13 compliant. Design sources: v6.2 additions listed above. Approved: Product Owner 2026-06-24. |
| 1.7 | 2026-05-15 | v3.5 design gate: (ST-03 IT-06) Paper Account Panel — collapsible panel below Strategy Compliance Panel in Table View; conditionally rendered when `ALPACA_PAPER_API_KEY` configured; displays US-market paper positions (ticker, paper entry price, current price, paper P&L $ and %, date opened, size); error state "Paper tracking temporarily unavailable"; hidden entirely when credentials absent. §13 compliant display-only. Design source: docs/ux_specs/paper-trading/ux_spec.md. Approved: Product Owner 2026-05-15. |
| 1.6 | 2026-05-14 | v3.4 design gate: (ST-05) Drawdown review prompt — amber banner above positions table when portfolio drawdown threshold breached; displays drawdown %, threshold, portfolio heat %, regime status, positions by lifecycle state counts; session-scoped dismissal; §13 compliant display-only. (ST-06) Concentration limits warning — amber summary card listing positions/sectors exceeding configurable thresholds; persistent (no dismiss); graceful degradation when DS-03 sector data absent. Design sources: v3.4 additions listed above. Approved: Product Owner 2026-05-14. |
| 1.5 | 2026-05-09 | v3.3 design gate: (ST-03) Arc 3 position lifecycle state badge — five-state set (GRACE/LOSING/PROFITABLE/EXIT ZONE/UNKNOWN) with days_in_state inline and next-trigger tooltip; (ST-05) Grace period alert zone at top of page for GRACE positions ≥ day 8; (ST-07) Trail Stop action and guided modal for PROFITABLE/EXIT ZONE positions. Design sources listed above. Approved: Product Owner 2026-05-09. |
| 1.4 | 2026-03-24 | ST-01 (BLG-FEAT-11, v2.3): §Strategy Compliance Panel — collapsible panel below Table View showing per-position ATR compliance data. Display-only. Design source: docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md. Approved: Product Owner 2026-03-24. Design gate: 2026-03-24__release-v2.3. |
| 1.3 | 2026-03-18 | (no change to positions.md — version increment noted for lineage) |
| 1.2 | 2026-02-26 | BLG-FEAT-06 (A-S08): Add `grace_days_remaining` column specification to Table View. Display format, null behaviour, and data source documented. Dependent on `position_endpoints.md` v1.8.3. |
| 1.1 | 2026-02-18 | Add Journal View. Tag filter. Expandable journal cards. View switcher. |
| 1.0 | — | Initial version. |

---

## Purpose & User Goals

The Positions page provides an overview of all **open positions**, including their performance, stop levels, days held, and journal information.
Its primary purpose is to help users:

- Monitor active trades
- Identify positions requiring attention (e.g., approaching stops, in grace period)
- Access entry/exit workflows
- Review or edit journal notes and tags
- Switch between different views depending on the task (table, grid, journal)

---

## Layout Structure

### View Switcher

A three‑way toggle enabling users to switch between:

1. **Grid View** – Card‑based layout showing key metrics
2. **Table View** – Detailed, sortable table of positions
3. **Journal View** – All positions displayed with notes, tags, and filters for reflection

Each view replaces the entire main content area. Switching views does not trigger a new data fetch — the same position data drives all three views.

---

### Table View (default)

Displays each open position as a row with:

- Ticker
- Market flag (US / UK)
- Entry price (native currency)
- Current price (native currency)
- Initial Stop *(renamed from "Stop"; shows £0.00 / $0.00 during grace period)*
- Trail Stop *(v6.2 — ST-02; see §Trailing Stop Column)*
- Shares (supports fractional values)
- P&L (GBP)
- P&L %
- Days held
  - Grace period indicator if under minimum hold days
- Status (lifecycle state badge — see §Position Lifecycle State Badge)
- Grace Days Remaining *(BLG-FEAT-06)*
- Alerts *(v6.2 — ST-05; see §Alerts Column)*
- Tags (as colored pills)
- Actions:
  - **Exit** (opens exit modal)
  - **Trail Stop** (opens trail stop modal — see §Trail Stop Action; visible only for PROFITABLE/EXIT ZONE positions)
  - **Recheck Compliance** *(v6.9 — ST-01; see §Compliance Recheck Panel)*
  - **View Journal** (opens position detail modal)

---

#### Position Lifecycle State Badge (v3.3 — ST-03 IT-01)

**Design source:** docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md

**Data sources:** `position_state`, `days_in_state` from `GET /positions` (Arc 3 fields).

**Column label:** "Status" (replaces prior GRACE/PROFITABLE/LOSING badge set).

**Badge format:** `STATE — Nd` (e.g. "GRACE — 3d")
- Filled pill, white text on state colour
- Width: content-fit

**State colour scheme:**

| State | Colour | Hex |
|-------|--------|-----|
| GRACE | Blue | `#2563EB` |
| LOSING | Red | `#DC2626` |
| PROFITABLE | Green | `#16A34A` |
| EXIT ZONE | Purple | `#7C3AED` |
| UNKNOWN | Grey | `#6B7280` |

**Tooltip (hover/focus on badge):**

| State | Tooltip |
|-------|---------|
| GRACE | "Exits grace when position moves > 0.5 ATR or after 10 trading days" |
| LOSING | "Exits when price rises above entry by 0.5 ATR" |
| PROFITABLE | "Advances to Exit Zone when P&L reaches 2R target" |
| EXIT ZONE | "Position has reached R-target. Review stop or exit." |
| UNKNOWN | "Set a stop and R-target on the linked trade plan to enable lifecycle tracking." |

**Null handling:** If `position_state` is null (pre-Arc 3 position pending back-fill), display UNKNOWN badge. Never display a dash or empty cell.

**§13 constraint:** Display-only. No automated recommendation generated from state display.

**Accessibility:** Badge has `aria-label="Position state: {STATE}, {N} days in state"`. Colour is never the sole differentiator — state label text is always present.

**Review-cadence is not a lifecycle state (v7.1 — ST-04, BLG-BE-61):** The position review-cadence nudge (`last_reviewed_at`, §Last Reviewed Column) is a metadata annotation only — a display flag tracking when a human last looked at a position — and does not participate in this state machine. The lifecycle state machine remains exactly the 4 states above (GRACE → LOSING → PROFITABLE → EXIT ZONE, with UNKNOWN as a display fallback for null/pending back-fill, not a 5th reachable state). A stale/flagged review status has no bearing on `position_state` or `days_in_state`, does not gate any transition between the 4 states, and is computed and stored entirely independently (`last_reviewed_at` on the `positions` row vs. `position_state`/`days_in_state` derived from price/stop logic).

---

#### Grace Days Remaining Column

**Data source:** `grace_days_remaining` from `GET /positions` (`position_endpoints.md` v1.8.3).

**Display when in grace period** (`grace_days_remaining` is an integer):
Display the string `"Day {holding_days + 1} of 10"`.

Examples:
| `holding_days` | Display |
|----------------|---------|
| 0 | Day 1 of 10 |
| 1 | Day 2 of 10 |
| 5 | Day 6 of 10 |
| 9 | Day 10 of 10 |

**Display when not in grace period** (`grace_days_remaining` is null):
Display a dash (`—`) or leave the cell visually empty. Do not display `"Day 0 of 10"`, `"0"`, or `"null"`.

**Column visibility:** Always present in the Table View for all open positions. The column is not hidden when a position is post-grace — the cell simply shows a dash.

**No sorting required.** This column is informational only; sorting is not required for v1.6.1.

---

### Grid View

Cards show a summarized snapshot of each position including:

- Ticker & market
- Entry vs current price
- P&L
- Stop level
- Days held
- Tags
- Alert badges (Trail Stop breach, RISK OFF, Gap Risk — *v6.9 addition, see §Alerts Column*)
- Last Reviewed indicator *(v7.0 addition, see §Last Reviewed Column)*
- Quick links to exit, recheck compliance *(v6.9 — ST-01)*, or view notes

Designed for readability and scannability.

---

### Journal View

The Journal View is a dedicated reflection interface accessible from the view switcher. It exists to support trade review, pattern recognition, and learning — the user's goal here is different from the Table and Grid views. They are not monitoring live positions; they are reading their own documented reasoning and outcomes.

#### Scope

- Shows **all positions** — both open and closed — unlike Table and Grid views which show only open positions.
- No live price refresh is needed. The data is sourced from the same position dataset already held by the page.

#### Filter Bar

The filter bar appears above the timeline and contains four independent filters that combine (AND logic — a position must satisfy all active filters):

| Filter | Type | Behaviour |
|--------|------|-----------|
| **Search** | Text input | Searches entry note and exit note content. Case-insensitive. Hides positions with no match in either note field |
| **Tag filter** | Multi-select dropdown | Selecting one or more tags hides positions that do not have at least one of the selected tags. Selected tags appear as dismissible pills below the dropdown |
| **Win / Loss** | Single-select (All / Winners / Losers) | Winners: P&L ≥ 0. Losers: P&L < 0. Defaults to All |
| **Date range** | From / To date inputs | Filters on entry date. Either bound is optional |

Active tag selections persist as dismissible pills below the filter row, allowing users to see and clear individual tag selections without reopening the dropdown.

Clearing all filters returns the full position list. Filters do not persist across view switches or page reloads.

#### Position Cards (Timeline Layout)

Positions are displayed as a vertical timeline of cards, ordered with the most recently entered position first.

Each card always shows:
- **Ticker** and market badge
- **CLOSED** badge (for closed positions only)
- **Entry date**
- **P&L badge** — profit/loss amount with percentage, color-coded (green / red). For open positions, reflects current unrealised P&L. For closed positions, reflects realised P&L
- **Entry note** — displayed in full if present. No truncation in this view; the Journal View is a reading experience
- **Tags** — all tags displayed as pills

For **closed positions only**, an expand control appears at the bottom of the card if an exit note exists:
- Label: "Exit Details" with chevron icon and the exit date shown on the right
- Clicking expands to reveal the exit note beneath
- The section collapses and expands with animation
- Only one position's exit details can be expanded at a time

#### Empty States

Two distinct empty states:

- **No positions at all**: Shown when the user has no positions of any kind. The card should explain the view is empty and offer a path to enter a position.
- **No results match current filters**: Shown when positions exist but none match the active filter combination. The message should indicate filters are hiding results and make it easy to clear them. Does not offer a "enter new position" action — the user is in a review context, not an entry context.

---

---

## Grace Period Alert Zone (v3.3 — ST-05 IT-02)

**Design source:** docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md

**Placement:** Above the View Switcher, at the top of the Positions page. A dedicated Alert Zone with amber background (`#FEF3C7`) and left border (`#D97706`, 4px).

**Trigger:** One or more open positions with `position_state = 'GRACE'` AND `days_in_state ≥ 8`. Data source: `GET /positions/grace-period-alerts`.

**One alert card per qualifying position.** Cards stack vertically in the Alert Zone.

### Alert Card Contents

- Header: "⚠ Grace Period Alert — {TICKER}" + "Day {days_in_state} of 10" sub-label + Dismiss (✕) button
- Body: "Your grace period ends in {10 - days_in_state} trading day(s). Review your original thesis before the window closes."
  - When `days_in_state = 10`: "Grace period has ended. Your position will transition to LOSING or PROFITABLE on next refresh."
- Trade plan context block (when `trade_plan_id` present): Thesis (first 120 chars), Entry zone, Stop, R-target
- "View Trade Plan →" text link (when `trade_plan_id` present)

### Dismiss Behaviour

- Per-position per-session via localStorage key `grace_alert_dismissed_{position_id}`
- Alert reappears on next browser session (no expiry)
- When all cards dismissed: Alert Zone collapses to zero height (no visual gap)

**§13 constraint:** Display-only. No automated recommendation. Human decides action.

**Accessibility:** Alert Zone has `role="alert"` and `aria-live="polite"`.

---

## Trail Stop Action (v3.3 — ST-07 IT-03)

**Design source:** docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md

### Trail Stop Button

- Placement: Actions column, after "Exit", before "View Journal"
- Label: "Trail Stop"
- Style: secondary (outlined)
- **Shown** for positions where `position_state` is `PROFITABLE` or `EXIT ZONE`
- **Disabled** (with tooltip "No current stop set. Add a stop to use trail management.") when `current_stop` is null
- **Hidden** for GRACE, LOSING, UNKNOWN states

### Trail Stop Modal

Opened by clicking enabled "Trail Stop" button. Data source: `GET /positions/{id}/stop-trail`.

**Modal header:** "Trail Stop — {TICKER}"

**Data rows:**

| Label | Source | Format |
|-------|--------|--------|
| Current Stop | `current_stop` | Native currency, 2dp |
| ATR Trail Stop | `atr_trail_stop` | Native currency, 2dp |
| Raise by | `trail_difference` | "+£X.XX" (positive) or "−£X.XX" (amber, negative) |
| Trail in R | `trail_r_terms` | "+X.XR" |

**Footnote (static):** "ATR trail stop = current price − (ATR × 2.0). ATR period: 14 days. Multiplier per strategy rules."

**Confirmation button:** "Update stop to {atr_trail_stop}" — calls `PUT /positions/{id}` with new `stop_price`.

On success: modal closes; position row updates; toast: "Stop updated to {atr_trail_stop}".

**Cancel / Dismiss:** "Cancel" text link; Escape key; ✕ button — no change made.

**§13 constraint:** System presents calculation. Human confirms. No automated stop update.

---

## Compliance Recheck Panel (v6.9 — ST-01 BLG-FEAT-64)

**Design source:** docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md

### Recheck Compliance Button

- Placement: Actions column (Table View) / card footer (Grid View), after "Trail Stop", before "View Journal"
- Label: "Recheck Compliance"
- Style: secondary (outlined)
- **Shown** for all open positions in Table View and Grid View
- **Hidden** in Journal View (read/reflection surface — no live actions)
- Loading state: inline spinner, button disabled during request

### Compliance Recheck Panel (Modal)

Opened by clicking "Recheck Compliance". Data source: `GET /positions/{id}/compliance-recheck`.

**Modal header:** "Compliance Recheck — {TICKER}" with overall status badge (Pass / Warn / Fail — same palette as `PreEntryValidationPanel`).

**Context line (static):** "Checked against current conditions, not entry-time."

**Check list:** the same 5 SI-01 rules, labels, and pass/warn/fail iconography already canonical in `PreEntryValidationPanel` (`src/pages/TradePlan.js`), evaluated against current regime/signal/heat/sizing state rather than the entry-time snapshot:

| Rule Key | Display Label |
|----------|---------------|
| `regime_gate` | Regime Gate |
| `cash_constraint` | Cash Constraint |
| `sector_concentration` | Sector Concentration |
| `earnings_proximity` | Earnings Proximity |
| `sizing_validity` | Sizing Validity |

**Override acknowledgement:** checkbox "I acknowledge the advisory result" shown only when overall status is Warn or Fail — display-only, session-local, not persisted (no state change on the position).

**All-pass affirmation (v2.7 — ST-02, BLG-FE-105):** when `overall_status === "pass"`, an affirmation line is shown in the same layout slot the acknowledgement block occupies for Warn/Fail — text **"All 5 checks passed — no action needed."**, `text-emerald-400` (existing pass colour token, no new colour introduced), plain text with no interactive element. Design source: `docs/design/2026-08-04__release-v8.2/compliance-recheck-all-pass-state/decision_record.md`.

**States:**

| State | Panel |
|-------|-------|
| Loading | Spinner in modal body, header shows ticker only |
| Success | Full check list |
| Error | "Recheck unavailable — try again" with retry button |

**Dismiss:** ✕ button, click-outside, or Escape — no persisted state change; this is a point-in-time check only.

**§13 constraint:** Re-application of the existing deterministic SI-01 rule set against current inputs — no new statistical model, scoring, or automated action. Does not replace or duplicate SI-02 (drift detection).

**Accessibility:** Modal is keyboard-navigable with focus trap. Status badge and each check-item carry `aria-label` text equivalents — colour/icon is never the sole differentiator.

---

## Paper Account Panel (v3.5 — ST-03 IT-06)

**Design source:** docs/ux_specs/paper-trading/ux_spec.md

**Placement:** Collapsible panel appended below the Strategy Compliance Panel in Table View only. Hidden in Grid View and Journal View.

**Conditional rendering:** Panel rendered only when `ALPACA_PAPER_API_KEY` is configured. When credentials are absent, `GET /portfolio/paper-positions` returns `{"paper_tracking_enabled": false}` and the panel is not rendered — no unconfigured state visible to the user.

**§13 constraint:** Display-only tracking view. Positions created only by human action via primary system workflow. No automated order execution.

### Panel Header

- Label: **"Paper Account"**
- Sub-label (static, muted): "Hypothetical tracking — US market positions only. Not real capital."
- Expand/collapse chevron. Default: expanded when positions present; collapsed when no positions.

### Paper Positions Table

| Column | Source Field | Format |
|--------|-------------|--------|
| Ticker | `ticker` | Uppercase |
| Paper Entry | `paper_entry_price` | USD to 2dp |
| Current Price | `current_market_price` | USD to 2dp |
| Paper P&L ($) | `paper_pnl_usd` | Signed USD, 2dp; green if positive, red if negative |
| Paper P&L (%) | `paper_pnl_pct` | Signed percentage, 2dp; green if positive, red if negative |
| Date Opened | `date_opened` | `DD MMM YYYY` |
| Size | `position_size` | Integer or decimal shares |

### Empty State (credentials configured, no paper positions)

Message: "No paper positions tracked. Open a US market position to begin tracking." Panel collapsed by default.

### Error State

When `GET /portfolio/paper-positions` returns 5xx or timeout: display **"Paper tracking temporarily unavailable."** (muted, no icon). Does not break the Positions page.

### API Dependency

| Endpoint | Purpose |
|----------|---------|
| `GET /portfolio/paper-positions` | Returns paper account positions with P&L comparison. Returns `{"paper_tracking_enabled": false}` when credentials absent. |

---

## Trailing Stop Column (v6.2 — ST-02)

**Design source:** docs/design/2026-06-24__release-v6.2/trailing-stop-display/ux_spec.md

**Data source:** `current_trailing_stop` from `GET /positions` (new field; nightly update by ST-01). **Correction (v8.9 — ST-02, BLG-BE-103):** `current_trailing_stop` is GBP-converted for US-market positions — it does not satisfy the "Display format: Native currency" rule below on its own. The frontend renders `current_trailing_stop_native` (added v8.9) instead; `current_trailing_stop` remains in the response for GBP-basis consumers (e.g. portfolio-level aggregation) but must not be paired with the native currency symbol.

**Column label:** "Trail Stop" (added after "Initial Stop" — existing "Stop" column renamed).

**Display format:** Native currency, 2dp (matches Initial Stop format). Null: dash ("—"). Prior to v8.9 this was violated for US-market positions — see Data source correction above.

**Breach Badge:**

Shown when `current_price ≤ current_trailing_stop`:

| Element | Spec |
|---------|------|
| Label | "⚠ BREACH" |
| Background | `#EA580C` (orange-600) |
| Text | White, weight 500, 11px |
| Shape | Rounded pill |
| Placement | Below trailing stop value in same cell |
| `aria-label` | "Trailing stop breach: current price is at or below trailing stop level" |

Not shown when price is above trailing stop (no reserved space).

**Grid View:** Trailing stop value shown in card summary alongside Initial Stop. Breach: ⚠ icon appended inline (icon only, no pill).

**§13 constraint:** Display-only. No automated action.

### "Why Is My Stop Moving" Explainer Tooltip (v7.9 — ST-05, BLG-FEAT-87)

**Design source:** docs/design/2026-07-27__release-v7.9/trailing-stop-explainer-tooltip/ux_spec.md

**Placement correction (implementation, agent-mediated Head of UX & Design review):** the section above (v6.2) describes a separate "Trail Stop" column "added after 'Initial Stop' — existing 'Stop' column renamed." The shipped Table View does not have this — `Positions.js` renders a single combined **"Stop"** header (`title="Initial stop (entry) / Current trailing stop (computed)"`), and Grid View's tile (`PositionCard.js`) has no standalone "Trail Stop" label either, only an "Init: {value}" subtext above the trailing-stop value. This is a pre-existing spec/implementation gap from v6.2, not introduced by this story — noted here rather than fixed, since restructuring the Stop column is out of this story's scope (a display-only tooltip addition). The info icon was placed on the actual anchors available: immediately after the combined "Stop" header text (Table View), and inline with the "Init:" subtext line in the tile (Grid View) — closest faithful placement to "next to the Trail Stop element" given what the real UI has.

An info icon (`ⓘ`) hover or keyboard focus reveals a static tooltip explaining the profit-aware stop logic (§7.2) and the never-loosens stop-movement rule (§7.3), reviewed against `strategy_rules.md` §7 for accuracy. One tooltip per view covers all rows — not a per-row/per-position value. Tunable parameters (`InitialATRMultiplier`, `ProfitATRMultiplier`) are not surfaced in the copy; the explainer describes behaviour, not internal constants subject to change control (§12).

No API dependency — static client-side text, no loading/error state.

**§13 constraint:** Display-only reference text. No automated action, no change to the trailing-stop calculation or Trail Stop Modal.

---

## Alerts Column (v6.2 — ST-05)

**Design source:** docs/design/2026-06-24__release-v6.2/risk-off-exit-alert/ux_spec.md

**Data source:** `risk_off_exit` (boolean) from `GET /positions` (new field; nightly regime check by ST-05).

**Column label:** "Alerts" (rightmost column before Actions).

**Risk-Off Badge:**

Shown when `risk_off_exit = true`:

| Element | Spec |
|---------|------|
| Label | "RISK OFF" |
| Background | `#1E40AF` (blue-800) |
| Text | White, weight 500, 11px |
| Shape | Rounded pill |
| `aria-label` | "Risk-off exit alert: regime signal indicates exit this {US/UK} position" |

No alert: dash ("—").

**Market isolation:** US positions flag only when SPY < MA200; UK positions flag only when FTSE < MA200. Enforced server-side — frontend renders `risk_off_exit` as-is.

**Alert clearing:** When `risk_off_exit = false` (regime recovered), badge absent automatically. No manual dismiss.

**§13 constraint:** Display-only. No automated exit triggered.

### Gap Risk Badge (v6.9 — ST-02)

**Design source:** docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md

**Data source:** `gap_risk` object from `GET /positions` (new field; server-computed from DS-04 earnings calendar + historical OHLCV).

Shown when `gap_risk.flagged = true` — trigger is either an earnings date before the position's next trading session, or a weekend hold flagged at Friday close:

| Element | Spec |
|---------|------|
| Label | "GAP RISK" |
| Background | `#D97706` (amber-600) |
| Text | White, weight 500, 11px |
| Shape | Rounded pill |
| `aria-label` | "Gap risk flag: {reason}, average gap {value or insufficient history}" |

**Stacking:** RISK OFF and GAP RISK badges are independent alert types and stack vertically in the same Alerts cell when both apply to a position — this realises the "future alert types" placeholder already noted in the v6.2 Alerts Column design.

**Stacked-state spacing (v7.0 — ST-05):** Minimum `4px` vertical gap between stacked badges (prevents visual merging). Stack order: RISK OFF above GAP RISK. Neither label may truncate — if horizontal space is insufficient (Grid View narrow card), badges wrap to full width individually rather than sharing a row. Reviewed and confirmed distinguishable per existing hue (blue-800 vs amber-600) + mandatory text label; no colour/label change required. Design source: `docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md`.

**Grid View badge placement (v7.0 — ST-01):** RISK OFF and GAP RISK badges render in a dedicated alert row within the position card — below the ticker/market header, above the Entry/Current/Trail Stop stat tiles. This is the "alert-icon row" referenced elsewhere in this document (see §Grid View and §Last Reviewed Column). When both badges apply to the same position, they stack vertically in this row per the Stacked-state spacing rule above (RISK OFF above GAP RISK, `4px` minimum gap, full-width wrap rather than truncation). When neither applies, the alert row is omitted entirely (no reserved space, no dash placeholder — unlike the Table View's Alerts column, which always renders a dash when empty). Same visual treatment (colour, label, pill shape) as Table View — no Grid-View-specific styling variant.

**Tooltip / expanded detail:** Hover or focus reveals earnings date and/or weekend-hold reason plus historical average gap magnitude for the ticker (`gap_risk.avg_gap_pct`, `gap_risk.event_count`), or "insufficient history" when `gap_risk.insufficient_history = true`. Tooltip content is also exposed via `aria-describedby` for keyboard/screen-reader access.

**No alert:** dash ("—"), consistent with existing Alerts column convention.

**Alert clearing:** Fully server-driven (earnings date passes, or Monday session opens for weekend holds). No manual dismiss.

**§13 constraint:** Display-only. Surfaces a known calendar event and historical statistic — no prediction of gap direction or magnitude.

---

## Last Reviewed Column (v7.0 — ST-15)

**Design source:** docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md

**Purpose:** Existing prompts (Grace Period Alert Zone, Drawdown Review Prompt) only fire on price/performance triggers — a quietly-performing position can go unreviewed indefinitely. This is a low-priority, ongoing informational nudge, not a new Alert Zone banner.

**Placement:** Table View — new "Last Reviewed" column, after "Alerts", before "Actions". Grid View — card footer, after the alert-icon row, before the Actions row.

**Data source:** `last_reviewed_at` (ISO timestamp, nullable) — new field on `GET /positions`.

**NULL / backfill semantics (v7.1 — ST-04, BLG-BE-61):** The column was added via `ALTER TABLE ... ADD COLUMN IF NOT EXISTS last_reviewed_at` with no default, so every position that existed before this feature shipped (v7.0) has `last_reviewed_at = NULL` and stays that way until explicitly marked reviewed — there is no retroactive backfill migration. `days_since_review` for a `NULL` value is computed against `entry_date`, not treated as `0` (which would hide a genuinely stale position) or as "infinite"/pre-flagged (which would mass-flag every pre-existing position the instant this feature shipped, regardless of how recently it was actually opened). This means a pre-existing position that was opened recently is correctly not flagged, while one opened long ago is correctly flagged immediately — the same rule a freshly-created position would get. Verified against production data 2026-07-14: 1 open position (`INTC`, entered 2026-07-02), `last_reviewed_at = NULL`, `days_since_review` = 12 (< 14 threshold) → correctly not flagged.

| Element | Spec |
|---------|------|
| Display (not flagged) | "Reviewed {N}d ago" — `text-slate-500 dark:text-slate-400` (existing secondary-text token, BLG-FE-89) |
| Display (never reviewed) | "Not yet reviewed" — same styling |
| Flag threshold | `days_since_review ≥ 14` (default; server-configurable constant, not user-editable this cycle) |
| Flagged display | Text switches to `text-amber-600 dark:text-amber-400` + small clock icon prefix; label unchanged. Icon + colour only — no separate badge/pill, keeps it visually subordinate to the Alerts column's pill badges |
| `aria-label` | "Position not reviewed in {N} days — consider reviewing" (flagged) / "Last reviewed {N} days ago" (not flagged) |

**Mark Reviewed action:** Small inline checkmark icon-button next to the text (not a full Actions-column button). Click → `PATCH /positions/{id}/mark-reviewed` (sets `last_reviewed_at = now()` server-side) → text resets to "Reviewed 0d ago", flagged state clears immediately (optimistic update). No confirmation modal.

**Suppression rule (AC-04):** The flagged/amber state does not fire when the position is already surfaced by the Grace Period Alert Zone (`position_state = 'GRACE'` AND `days_in_state ≥ 8`) or the Drawdown Review Prompt (position included in the portfolio-level drawdown banner's position count). The "Last Reviewed" text still renders in both cases (informational); only the amber/flagged styling is suppressed. `days_since_review` continues counting underneath — if the position later exits GRACE/drawdown scope while still stale, the flag can fire on the next refresh.

**§13 constraint:** Display-only. No automated action beyond timestamp update on explicit user click.

---

## AI Trade Advisor Widget (v6.2 — ST-09)

**Design source:** docs/design/2026-06-24__release-v6.2/ai-chat-widget/ux_spec.md

**Placement:** Fixed-position floating widget, `bottom: 24px; right: 24px; z-index: 100`. Present on Positions page; also on Signals page (AC-01: "signals or portfolio page").

### Collapsed State

Rounded pill button: chat icon + "Ask Advisor" text (white on `#1D4ED8` blue-700). Hover: `#1E3A8A`.

### Expanded State

350px × 480px floating panel above the collapsed button.

| Element | Spec |
|---------|------|
| Header | "AI Trade Advisor" + amber "Advisory" badge + ✕ close button |
| Messages area | Scrollable; user bubbles right-aligned (blue); AI bubbles left-aligned (grey) |
| Input row | Text field ("Ask about your portfolio…") + "Ask" button |
| Footer | Static advisory text: "AI responses are advisory only. All trade decisions require human confirmation." (`text-slate-600 dark:text-slate-400` italic, 11px, non-dismissible — contrast ≥4.5:1 on both `bg-slate-800` (dark) and `bg-slate-100` (light); was bare `text-slate-400` (dark-only, no light companion) prior to v2.0/BLG-FE-88, and `text-slate-600` (dark-only) prior to v1.9/BLG-UX-02); `data-testid="ai-chat-advisory-footer"` on footer container |

### States

| State | Behaviour |
|-------|-----------|
| Empty (just opened) | Prompt: "Ask about your portfolio, positions, or signals." |
| Loading (API call) | Typing indicator (three dots); input + Ask disabled |
| Error | Inline error in messages area: "Unable to get a response. Please try again." Input re-enabled |
| ✕ close | Collapses to button; message history cleared |

### Stateless per request

Each POST /ai/chat is stateless (no session state persisted to backend). In-memory conversation display only — cleared on widget close.

**§13 constraint:** Display-only advisory. No trade entry, exit, or modification action executable from widget.

---

## Key Components Used

- Position cards
- Positions table
- Journal cards (see `journal_components.md` — Expandable Journal Card)
- Exit Position Modal
- Position Detail Modal (journal editor)
- Tag pills (see `journal_components.md` — Tag List)
- Tag editor with autocomplete (see `journal_components.md` — Tag Editor)
- View switcher control

---

## States

### Loading State

- Skeleton rows or card placeholders
- During initial load or refresh after exit

### Empty State

Shown when no open positions exist (Table / Grid views):
- Message explaining there are no active trades
- Action: "Enter New Position"

For Journal View empty states, see the Journal View section above.

### Error State

- Global error banner if positions list fails to load
- Retry option for re‑fetching data

---

## API Dependencies

| Endpoint | Purpose |
|----------|---------|
| `GET /positions` | Primary data source for all three views. Returns open positions with live pricing, journal fields, `grace_days_remaining`, `position_state`, `state_entered_at`, `days_in_state`. |
| `GET /positions/tags` | Tag autocomplete source for the Journal View filter dropdown and for the Position Detail Modal's tag editor |
| `GET /positions/compliance` | *(v2.3 — ST-01)* Strategy Compliance Panel data source. Returns ATR-based per-position stop compliance, stop age, and size compliance flags. Display-only; §13.3 constraint applies. |
| `GET /positions/grace-period-alerts` | *(v3.3 — ST-05)* Returns positions in GRACE state with `days_in_state ≥ 8`, including trade plan context. Source for Grace Period Alert Zone. |
| `GET /positions/{id}/stop-trail` | *(v3.3 — ST-07)* Returns ATR trail stop calculation for a single position. Source for Trail Stop Modal. |
| `PUT /positions/{id}` | *(v3.3 — ST-07)* Updates stop price after user confirms trail stop action. |
| `GET /portfolio/paper-positions` | *(v3.5 — ST-03)* Paper Account Panel data source. Returns Alpaca paper positions with P&L. Returns `{"paper_tracking_enabled": false}` when ALPACA_PAPER_API_KEY absent. |
| `GET /positions` (extended) | *(v6.2 — ST-02/ST-05)* Now returns two new fields per position: `current_trailing_stop` (number \| null) for Trail Stop column; `risk_off_exit` (boolean) for Alerts column. |
| `GET /positions` (extended, v7.0 — ST-15) | Now also returns `last_reviewed_at` (ISO timestamp \| null) for Last Reviewed column. |
| `PATCH /positions/{id}/mark-reviewed` (v7.0 — ST-15) | New endpoint — sets `last_reviewed_at = now()` for the given position. |
| `POST /ai/chat` | *(v6.2 — ST-09)* AI Trade Advisor widget. Accepts `{ question: string, context?: { ticker?, position_id? } }`. Returns AI response grounded in live portfolio state. |

> For full dependency behaviour rules, see `patterns/api_dependencies.md`.

---

## Responsive Behavior

- Table collapses to cards on smaller screens
- Grid view reduces card width and stacks vertically
- Journal cards expand to full width on mobile
- Filter bar stacks vertically on narrow screens; tag pills wrap
- Action buttons move below card content on mobile
- Tags wrap gracefully on narrow screens

---

## Strategy Compliance Panel (v2.3 — ST-01 BLG-FEAT-11)

**Design source:** docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md
**Scope constraint (§13.3):** Display-only — no automated notification, alert, or action generated by this panel. Strategy Rules & System Intent Owner DoQ sign-off required at delivery verification.

### Placement

Collapsible panel appended below the Table View only. Hidden in Grid View and Journal View.

Label: **"Strategy Compliance"** with expand/collapse chevron.

### Panel Header

- Overall status badge: **"Compliant"** (green) / **"Needs Attention"** (amber) / **"Review Required"** (red)
- Summary label: "N of M positions fully compliant"
- Default: expanded if any position is non-compliant; collapsed if all compliant

### Per-Position Table

| Column | Source | Display |
|--------|--------|---------|
| Ticker | positions | text |
| Stop Compliance | backend compliance flag | ✅ / ⚠️ |
| Stop Age | days since last stop update | "N days" / "Not set" |
| Size Compliance | backend compliance flag | ✅ / ⚠️ |

### States

- Loading: spinner; panel collapses until data ready
- No positions: panel hidden
- All compliant: green header; collapsed by default
- Non-compliant present: amber/red header; expanded by default

### API Dependency

Backend must provide compliance flags per position (new endpoint or extension to `GET /positions`). openapi.yaml must be updated in same commit as implementation.

---

## UX Notes

- Grace period must be visually clear and distinguishable from normal stop logic
- Tags should be easily scannable and visually grouped
- Exit action should always feel safe — a modal confirmation protects from accidental exits
- Journal editing should feel lightweight, using inline editors where possible
- The user should be able to switch between views without losing filtering or scroll position
- Data should update smoothly after exits or journal edits
- The Journal View is a **reading and reflection experience**, not a live monitoring surface. Layout and density decisions should reflect this: more vertical space per entry, no live price indicators, no stop-level warnings

---

## Known Deviations

### DEV-EPIC01-ST05-01 — Positions Table View: RISK OFF badge colour/label diverges from spec

- **Description:** §Alerts Column specifies the RISK OFF badge as Label "RISK OFF", Background `#1E40AF` (blue-800). The shipped Table View implementation (`src/pages/Positions.js`, `AlertsCell` component) instead renders `bg-amber-900/60 text-amber-300` (amber, not blue), label "Risk-Off" (not "RISK OFF"), plus a `ShieldAlert` icon not mentioned in spec. Pre-existing since v6.2 — confirmed by the existing passing test `SC-RO-02` (`tests/e2e/epic01-v62-stops-alerts.spec.js`), which encodes the amber colour as expected. Discovered 2026-07-13 while building the v7.0 Grid View RISK OFF badge (ST-02), which correctly uses the spec's blue `#1E40AF` — Table View and Grid View are now visually inconsistent for the same badge. This also means the v7.0 combined-badge differentiation decision record's "hue separation" rationale (blue-800 vs amber-600) does not hold for Table View as shipped — both RISK OFF and GAP RISK render in the amber family there.
- **Canonical requirement:** §Alerts Column — Risk-Off Badge: Label "RISK OFF", Background `#1E40AF` (blue-800).
- **Priority:** P2
- **Target resolution release:** v7.1
- **Owner:** Frontend Specifications & UX Documentation Owner
- **Backlog reference:** BLG-FE-107 (filed sprint execution 2026-07-13, cycle 2026-07-12__release-v7.0, ST-05)
- **Resolution:** Resolved by ST-03, cycle 2026-07-14__release-v7.1. Design gate confirmed the spec was and always had been correct (option (a) — bring Table View into compliance; accepting amber as canonical was rejected as it would invalidate the combined-badge decision record's hue-separation rationale). `AlertsCell` (`src/pages/Positions.js`) now renders `#1E40AF` (blue-800), label "RISK OFF", no icon — matching the v7.0 Grid View badge (`PositionCard.js`). `SC-RO-02` updated in the same commit to assert the spec-correct values. Changelog: `docs/product/changelog.md#v71` (recorded at v7.1 post-ship closure)

### DEV-EPIC01-ST02-01 — Trail Stop tile rendered GBP-converted value with native currency symbol for US-market positions

- **Description:** §Trailing Stop Column specifies "Display format: Native currency, 2dp." The shipped implementation (`PositionCard.js`, `Positions.js`) rendered `current_trailing_stop` — GBP-converted for US-market positions — next to the native currency symbol derived from `position.market`, while the adjacent "Init:" subtext correctly used the native `initial_stop`. For a US position this produced two numerically different "$"-labelled values on the same tile that were really the same underlying stop expressed in two currencies. Pre-existing since v6.2; discovered 2026-08-17 during a live WDC position review (BLG-BE-103).
- **Canonical requirement:** §Trailing Stop Column — Display format: Native currency, 2dp (matches Initial Stop format).
- **Priority:** P0
- **Target resolution release:** v8.9
- **Owner:** Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
- **Backlog reference:** BLG-BE-103 (filed 2026-08-17, cycle 2026-08-17__release-v8.9)
- **Resolution:** Resolved by ST-02, cycle 2026-08-17__release-v8.9. Backend now returns `current_trailing_stop_native` (`get_positions_with_prices()`, `backend/services/position_service.py`); `PositionCard.js` and the Table View row (`Positions.js`) render it instead of the GBP-converted `current_trailing_stop`. Existing e2e fixtures (`epic01-v62-stops-alerts.spec.js`, `epic01-v70-grid-badge-parity.spec.js`) updated to populate the new field; new coverage added (`tests/e2e/position-stop-currency-basis.spec.js`, `tests/test_position_currency_basis.py`).

### DEV-EPIC02-ST05-03 — Positions Table View: P&L (GBP) column absent

- **Description:** The v2.3 implementation of the Positions Table View renders "P&L %" (percentage uplift) in green for positive positions but does not display the "P&L (GBP)" absolute value column. Only % is visible; the absolute £ value is absent.
- **Canonical requirement:** §Table View column list specifies both "P&L (GBP)" and "P&L %" as separate columns in the Table View.
- **Priority:** P2
- **Target resolution release:** v2.4
- **Owner:** Frontend Specifications & UX Documentation Owner
- **Backlog reference:** BLG-FE-06 (filed delivery verification 2026-03-30, cycle 2026-03-24__release-v2.3)
- **Resolution:** Resolved by ST-04, cycle 2026-03-31__release-v2.4 (shipped 2026-04-03). P&L (GBP) column added. Changelog: docs/product/changelog.md#v24
