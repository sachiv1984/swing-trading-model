**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-06__release-v9.10
**Story:** ST-10 (EPIC-02, BLG-FE-194)

# Decision Record — Neutral Glyph for Break-Even Trades in Recent Trades

## 1. Problem

v9.9 `BLG-FE-192` gave the Recent Trades icon badge a three-way colour (emerald, rose, neutral). The glyph inside the badge still uses a two-way `pnl >= 0` check (`RecentTradesWidget.js`). A break-even trade therefore shows a neutral-coloured badge containing an up-arrow, which still reads as "winner".

## 2. Decision

| `pnl` (null treated as 0, as today) | Glyph (lucide) | Badge colour (unchanged from v9.9) |
|-----|----------------|-------------------------------------|
| `> 0` | `TrendingUp` | emerald |
| `< 0` | `TrendingDown` | rose |
| `=== 0` | `Minus` | neutral slate |

- Same size (`w-4 h-4`) and same badge geometry for all three.
- No new colour.
- The glyph is decorative (`aria-hidden="true"`). The adjacent signed P&L text carries the meaning.

This applies the existing `design_system.md` v1.21 rule (§Consistency Rules → Number and Currency Formatting: "zero renders unsigned in the neutral tone") to the glyph as well as the colour.

## 3. §13 Compliance

Display-only, no AI.

## 4. Frontend Spec Impact

`dashboard.md` v3.7: §4 Card 5 — Recent Activity's v3.6 icon-badge bullet is extended to cover the glyph.

## 5. Testability (CLAUDE.md §2)

`tests/e2e/recent-trades-zero-pnl-badge.spec.js` is extended so that SC-RTB-01 and SC-RTB-04 assert the `Minus` glyph, and SC-RTB-02 and SC-RTB-03 assert the up and down arrows.

## 6. Approval

Head of UX & Design: confirmed, 2026-10-06.
Product Owner: confirmed, 2026-10-06.
