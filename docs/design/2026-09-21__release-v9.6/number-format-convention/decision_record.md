**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-21__release-v9.6
**Story:** ST-06 (EPIC-01, BLG-FE-182)

# Decision Record — Canonical Number and Currency Formatting Convention

## 1. Problem

`toFixed(` appears in 68 files under `src/` and `toLocaleString`/`Intl.NumberFormat` in 19, with no shared helper. The story's AC — "the three tables use the helper with identical negative/decimal conventions" — presupposes a convention that **does not exist in any spec**. Reading the three target pages shows the drift concretely:

- **Negative sign:** `Positions.js` renders a trail-stop diff with `−` (U+2212) but its P&L cell renders `£{Math.abs(pnl).toFixed(2)}` with a trend icon and colour as the only sign carriers (no textual sign), and its adjacent P&L % cell relies on `toFixed`'s ASCII hyphen for negatives; `TradeHistory.js` renders `-£{…}` (ASCII hyphen) for average loss and `+£…` for average win.
- **Positive sign:** explicit `+` on some P&L figures, none on others.
- **R-multiples:** `TradeHistoryTable.js` uses signed 2 dp (`+1.25R`); `Positions.js` trail diff uses 1 dp; `TradePlans.js` prints the raw `r_target` (`2.5R`).
- **Thousands separators:** none — `£12345.60`.

Because the convention is a visible-output decision, this story is **Design Required**, and the convention must be fixed here so the helper has something to implement.

## 2. Decision

### 2.1 Canonical formats

| Kind | Format | Examples |
|------|--------|----------|
| **Money (unsigned amount** — prices, stops, cash, fees) | symbol + en-GB grouping + **2 dp** | `£1,234.50`, `$48.20` |
| **Money (signed amount** — P&L, differences) | sign, then symbol, 2 dp | `+£150.00`, `−£80.00`; zero is `£0.00` (no sign) |
| **Percentage (default)** | 1 dp, `%` suffix; signed when it is a change/return | `+4.2%`, `−1.8%`, `12.5%` |
| **Percentage (small-magnitude cost metrics** — slippage, fee drag) | 2 dp | `+0.35%` |
| **R-multiple (computed/realised)** | signed, 2 dp, `R` suffix | `+1.25R`, `−0.50R` |
| **R-multiple (user-entered target)** | as entered, up to 2 dp, trailing zeros trimmed, unsigned | `2.5R`, `3R` |
| **Missing value** (`null`/`undefined`/`NaN`) | em dash `—` (U+2014) | `—` |

### 2.2 Negative sign

**The typographic minus `−` (U+2212), placed before the currency symbol** (`−£80.00`). Rationale: already used by the one existing sign-aware helper-like code path (`Positions.js` trail diff); reads correctly to screen readers; and the codebase is roughly evenly split (a grep of `src/` finds 8 `−` occurrences vs 6 `-£`-style ones), so no convention has a claim to be "the existing one" — the typographic form is the tie-break. CSV exports are **unaffected**: exports use plain numeric values (`-80`), never presentation strings (see the Screener/Watchlist export record).

### 2.3 Zero and colour

Zero P&L renders unsigned and in the neutral tone (matching the Reports rule: green > 0, red < 0, neutral = 0). **The helper returns strings only** — colour stays at the call site, which already owns the tone logic. A negative value must never be conveyed by colour alone: the `−` is always present.

### 2.4 Currency and basis

The helper takes the currency as an argument (`'GBP' | 'USD'`) and **never converts**. Which basis to display remains the caller's decision under the existing rules (`strategy_rules.md` §4.1.5; `design_system.md` §Currency-Basis Correctness Pattern for US-Market Positions). Grouping uses `en-GB` locale.

### 2.5 API shape (guidance to the story, not a mandate)

One module (e.g. `src/lib/format.js`) exporting `formatCurrency(value, { currency, signed })`, `formatPercent(value, { signed, dp })`, `formatR(value, { signed, trim })`. All return `—` for missing values. Implementation may refine names; the **output table above is the contract**.

### 2.6 Migration scope and visible-change disclosure

Migrate the three tables named in the AC: **Positions, TradeHistory, TradePlans**. The remaining ~60 files are follow-ups listed by the story, per the backlog scope. Expected user-visible changes, all intentional: thousands separators appear on values ≥ 1,000; hyphen-minus becomes `−` in Trade History; Positions' P&L cell gains an explicit sign; Positions' 1 dp R-multiple becomes 2 dp. Existing Playwright assertions that match the old strings must be updated **in the same commit**, and each such update recorded in the QA evidence file.

### 2.7 Known discrepancy left for a follow-up

`trade_reflection.md` §4 specifies `"–"` (en dash) for a missing R-multiple, where this convention is `—`. That modal is outside the three-table migration; file a follow-up rather than editing a Canonical spec at this gate.

### 2.8 Motion / timing

None.

## 3. §13 Compliance

Presentation-only formatting of already-computed values. No new computation; no AI call. §13 pre-check does not apply.

## 4. Frontend Spec Impact

`design_system.md` v1.20 → v1.21: new §Number and Currency Formatting subsection (§Consistency Rules).

## 5. Testability (CLAUDE.md §2)

Unit tests on the helper for every row of §2.1 (including zero, negative, null, grouping, both currencies) plus Playwright confirming the three tables render identical negative/decimal conventions for a fixture with a loss, a gain, a zero and a ≥ £1,000 value.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-21.
Product Owner: confirmed, 2026-09-21.
