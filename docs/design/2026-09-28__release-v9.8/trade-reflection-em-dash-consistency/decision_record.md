**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-28__release-v9.8
**Story:** ST-27 (EPIC-05, BLG-SPEC-162)

# Decision Record — Trade Reflection Missing-Value Glyph and Shared-Helper Formatting

## 1. Problem

`trade_reflection.md` §4's hard rule states a missing R-multiple displays "–" (en dash, U+2013), but the canonical missing-value convention (`format.js`'s `MISSING` constant, `design_system.md` §Number and Currency Formatting) is an em dash (U+2014), and `TradeReflectionModal.js`'s `SummaryRow` fallback already renders the em dash — the spec text simply never matched the canonical convention or the shipped code. Separately, the modal's R-multiple, P&L and price fields (`entry_price`, `exit_price`, `rMultiple`) are hand-formatted with ad hoc `toFixed`/sign logic rather than the shared helper.

## 2. Decision

- **Glyph:** correct the spec to em dash, matching the already-shipped code and the canonical convention — documentation-only, no code change (same disposition as the `watchlist.md` v0.8 empty-state precedent: spec corrected to match already-shipped behaviour).
- **Formatting:** the modal's R-multiple, P&L and price fields are re-pointed to `formatR`/`formatCurrency` from `src/lib/format.js` in place of their ad hoc logic. Output is unchanged — the canonical helper's contract for signed money and signed R already matches what the modal's current hand-written logic produces (symbol + 2dp, signed R with 2dp) — this is a single-source-of-truth consolidation, not a visual redesign, in the same spirit as ST-01/ST-02 this cycle.

## 3. §13 Compliance

Not applicable — no AI call.

## 4. Frontend Spec Impact

`trade_reflection.md` §4's hard rule corrected from "–" to "—" (em dash), and a note added that R-multiple/P&L/price fields format via the shared helper (`src/lib/format.js`), not ad hoc logic.

## 5. Testability (CLAUDE.md §2)

No visual change expected (helper output matches existing ad hoc output; glyph already matches shipped code). Existing modal Playwright coverage, if any, continues to pass; no new observable AC is introduced beyond what CLAUDE.md's FI-P3-02 wording-only exception already covers for the glyph correction. The formatting-source change is verifiable by code review (no behavioural AC to assert beyond "same rendered output").

## 6. Approval

Head of UX & Design: confirmed, 2026-09-28.
Product Owner: confirmed, 2026-09-28.
