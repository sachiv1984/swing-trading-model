**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Cycle:** 2026-05-18__release-v3.7
**Story:** ST-03 (EPIC-01) — BLG-FE-34
**Sources:** BLG-FE-34 (backlog), trade_plan.md v0.4, ST-01 + ST-02 (signal → watchlist linkage)
**Approved by:** Product Owner
**Approved date:** 2026-05-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# UX Spec — Trade Plan Form: Signal Context Panel (BLG-FE-34)

This spec defines the "Signal Context" panel displayed in the trade plan creation form when a linked signal exists for the ticker. It eliminates manual context-switching when writing entry rationale.

---

## 1. Design Intent

When a user creates a trade plan for a ticker that has a linked signal (i.e. the ticker came through the signals workflow), the relevant signal data is surfaced inline in the form. This provides the key data points needed to write rationale without leaving the form. The panel is read-only — it does not create automated entries, only contextual reference data.

---

## 2. Placement

The Signal Context panel is positioned **above the Pre-Trade Checklist section** (§6 of trade_plan.md) and **below the core plan fields** (Ticker, Market, Status, Stop Level, Risk/Reward Notes).

Layout order in trade plan creation form:
1. Core plan fields (ticker, market, status, stop level, risk/reward notes)
2. **Signal Context panel** ← new (conditional)
3. Pre-Trade Entry Checklist
4. Form footer (Save / Cancel)

---

## 3. Signal Context Panel — Presence Condition

The panel is shown when a linked signal exists for the ticker being planned. A "linked signal" is a signal record where:
- `ticker` matches the trade plan ticker
- `status = "watchlisted"` (signal was actioned via the Add to Watchlist flow from ST-02)

When no linked signal exists: the panel is hidden entirely. No placeholder or empty state is shown. The form behaves exactly as current (no regression).

---

## 4. Panel Content

| Field | Label | Source | Format |
|-------|-------|--------|--------|
| Signal Rank | "Rank" | Signal `rank` | Integer (e.g. `#3`) |
| Momentum % | "Momentum" | Signal `momentum_pct` | `+X.X%` (green) or `−X.X%` (red) |
| Price vs 200-day MA | "vs 200-day MA" | Derived: `(price − ma_200) / ma_200 × 100` | `X.X% above` or `X.X% below` |
| Regime | "Regime" | Signal `regime` | "On" (green badge) / "Off" (amber badge) |
| ATR value | "ATR (14d)" | Signal `atr` | Currency-formatted (e.g. `$4.20`) |
| Suggested stop | "Suggested stop" | `entry_price − (5 × atr)` | Currency-formatted; labelled "entry − 5×ATR" |

**Panel header:** "Signal Context" (section heading, muted styling — visually distinct from form field labels)

**Read-only indicator:** The panel uses a distinct background (e.g. light grey tint, `bg-gray-50`) and no interactive elements, making its read-only nature visually apparent.

---

## 5. Pre-Population Rules

When the Signal Context panel is shown, the following form fields are pre-populated on initial form load:

### 5.1 Entry Rationale field (`risk_reward_notes`)

Pre-populated with:
```
Rank {N} momentum signal. Price {above/below} 200-day MA by {x.x}%. {US/UK} regime on.
```
Where:
- `{N}` = signal rank
- `{above/below}` = determined by price vs 200-day MA calculation
- `{x.x}` = absolute value of the % deviation
- `{US/UK}` = derived from signal market

The user may edit this text freely. Pre-population is advisory; existing text is not overwritten if the form is re-opened with saved state.

### 5.2 Confirmation criteria field

If the trade plan form has a separate confirmation criteria field, pre-populate with:
```
Price above 200-day MA at entry. Regime on. Spare cash available.
```
User-editable.

**Note:** If the trade plan form does not currently have a "confirmation criteria" field as a distinct field, this pre-population applies to the `risk_reward_notes` textarea as a continuation of the rationale template. Do not add new form fields not already in the schema.

### 5.3 Stop Level field

Pre-filled with the suggested stop value: `entry_price − (5 × atr)`.

This applies only on initial form creation (when no stop level is set). If the user has already set a stop level (edit mode), do not overwrite.

---

## 6. §13 Compliance

- The Signal Context panel is display-only (read-only reference data)
- Pre-population of text fields is advisory; the user may edit or clear all pre-populated values
- No automated confirmation criteria evaluation is performed; the user confirms each condition manually
- The suggested stop value is a mathematical calculation presented as a reference point — the user decides whether to use it

---

## 7. Non-Regression Rules

- No regression when no linked signal exists — form behaves identically to current implementation
- No regression to pre-trade entry checklist (§6 of trade_plan.md)
- No regression to edit mode — edit form should not re-overwrite existing values from saved state
- The "Review research" link (§6.3 of trade_plan.md) remains present

---

## 8. Error / Loading States

- Signal data is loaded as part of the trade plan form initialisation. If the signal fetch fails: panel is hidden silently (same behaviour as "no linked signal"). Do not block form submission.
- While signal data is loading: panel shows a skeleton placeholder (single-line height, width matching panel)
- If no signal exists for the ticker: panel is hidden (no error, no skeleton)

---

## 9. Accessibility

- Panel heading "Signal Context" uses a semantic heading level consistent with the form section structure (`<h3>` or equivalent)
- All panel fields have visible labels
- Read-only nature communicated via visual styling (no interactive elements) and `aria-readonly` where applicable
- Pre-populated text fields are focusable and editable by keyboard
