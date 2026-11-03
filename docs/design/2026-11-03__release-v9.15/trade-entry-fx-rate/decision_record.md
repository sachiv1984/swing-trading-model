**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-03__release-v9.15
**Stories:** ST-02 (EPIC-01, BLG-FE-245), ST-03 (EPIC-01, BLG-FE-246)

# Decision Record — Trade Entry FX Rate: Live Pre-fill, Source and One Label

## 1. Problem

Trade Entry pre-fills the FX field with a fixed `"1.27"` for US trades (`TradeEntry.js:45` and `:213`). Since v9.14 the backend serves the live or last-good GBP/USD rate with its source and age, and US share counts scale with FX², so an untouched default distorts the suggested size. Separately, the FX input is labelled three ways: "FX Rate (USD/GBP)" (Trade Entry, Trade Plan what-if), "FX Rate (GBP/USD)" (Exit dialog). The value in every case is US dollars per £1, so "USD/GBP" is the wrong way round. Both stories change the same field, so this record covers both.

## 2. Decision

### 2.1 One label (ST-03)

Every FX **input** uses:

- **Label:** "FX rate — USD per £1 (GBP/USD)"
- **Hint** (one line under the field, `text-xs text-slate-600 dark:text-slate-400`, linked by `aria-describedby`): "How many US dollars £1 buys."

Sites: Trade Entry, the Exit dialog (`ExitModal.js`), and the Trade Plan What-If Sizing Preview (`WhatIfSizingPreview.js`). The developer greps `src/` for any other FX input at implementation (ST-03 Scope bullet 2). The Signals page FX tile is a read-only display, not an input, and keeps its "FX Rate" heading and its v9.14 source line.

### 2.2 Pre-fill (ST-02)

- **Source:** `GET /market/status`'s `fx_rate`, `fx_rate_source` and `fx_rate_as_of` (v9.14, `docs/design/2026-10-29__release-v9.14/fx-rate-source-indicator/decision_record.md`). Trade Entry already has no FX source of its own, and this endpoint is the one the Signals tile reads.
- When the market becomes US (prefill from a plan, or ticker detection), the field is filled with `fx_rate` at 4 dp, **unless the user has already typed a value**. A typed value is never overwritten.
- While the rate is loading, the field is empty with placeholder "Fetching live rate…". No number is pre-filled until a rate arrives.
- UK entries keep the hidden `fx_rate: 1`.

### 2.3 Source line (ST-02)

A second line under the hint (`data-testid="trade-entry-fx-source"`), reusing the v9.14 copy and tokens:

| State | Text | Style |
|-------|------|-------|
| `live` | "Live rate, {age}" | `text-xs text-slate-600 dark:text-slate-400` |
| `last_known` | "Not live: last rate from {age}" | `text-xs text-amber-700 dark:text-amber-400` |
| `constant` | "Fallback rate: no live rate is available" | `text-xs text-amber-700 dark:text-amber-400` |
| User has edited the value | "Entered by you (live rate {rate})" — or "(no live rate)" for `constant` | `text-xs text-slate-600 dark:text-slate-400` |
| Rate request failed | "No rate available: enter the rate" | `text-xs text-amber-700 dark:text-amber-400` |

`{age}` uses the v9.14 rule: "{m} min ago" under 1 h, "{h} h ago" under 48 h, then "{d} days ago". "Fallback rate" is the visible note ST-02 AC 2 asks for. The fixed fallback value is shown in the field like any other pre-fill, and is never labelled live.

If the request fails outright, the field stays empty and required. The existing "FX rate missing for US trades" validation covers save. No client-side constant is introduced to replace 1.27.

## 3. §13 Compliance

Display and pre-fill only. The rate stays editable, and nothing is decided for the user.

## 4. Frontend Spec Impact

- `components/position_form.md` v1.11 → v1.12: §FX Rate (label, hint, pre-fill, source line).
- `components/exit_modal.md` v1.1 → v1.2: §FX Rate label and hint.
- `pages/trade_plan.md` v1.20 → v1.21: §5d.2 FX row label.

## 5. Obligations for Sprint Execution

- Remove both `"1.27"` literals from `TradeEntry.js` (ST-02 AC 3). No other constant replaces them.
- No API change: `GET /market/status` already returns the three fields.

## 6. Testability (CLAUDE.md §2)

- Playwright (ST-02 AC 1): with `GET /market/status` mocked to `fx_rate: 1.35`, `fx_rate_source: "live"`, a US entry pre-fills 1.3500 and `trade-entry-fx-source` reads "Live rate, …".
- Playwright (ST-02 AC 2): with `fx_rate_source: "constant"`, the source line reads "Fallback rate: no live rate is available".
- Playwright: a typed value survives the rate arriving later.
- ST-03 is wording only, so code review of the static label text is the evidence (FI-P3-02, slice AC 2).

## 7. Approval

Head of UX & Design: confirmed, 2026-11-03 (agent-mediated, Design Gate Engine).
Product Owner: confirmed, 2026-11-03 (the user, in session).
