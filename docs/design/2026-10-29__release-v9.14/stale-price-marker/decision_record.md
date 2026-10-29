**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-29__release-v9.14
**Stories:** ST-07 (EPIC-01, BLG-BE-168), ST-08 (EPIC-01, BLG-FE-214)

# Decision Record — Stale Price Marker on Positions, Accessible on Every Surface

## 1. Problem

Since v9.11, `/risk` marks a position whose live price fetch failed (`risk_dashboard.md` §6.6), and Dashboard Card 2 counts them. The Positions page shows the same stored price as live, so the two pages disagree (ST-07). The v9.11 marker is a non-focusable `span` with `title` and `aria-label`, so touch and keyboard users cannot read the explanation. Assistive tech may announce only "stale", and the copy gives no next step (ST-08).

## 2. Decision

### 2.1 One marker component

A shared `StaleMarker` (`src/components/ui/`) replaces the copy in `PositionRiskTable.js` and is used on the Positions page. It looks as it does today: `Clock` icon (`w-3.5 h-3.5`, `aria-hidden`) and the word "stale", `text-xs`. The colour moves from `text-amber-400` to `text-amber-700 dark:text-amber-400` (`design_system.md` §Light-Theme Colour Tokens).

### 2.2 Interaction and accessibility

- The marker is a `<button type="button">` with a visible focus ring (`focus-visible:ring-2 ring-amber-500`). Its accessible name is "Price stale". Its accessible description is the explanation, through `aria-describedby` pointing at an `sr-only` element. The `title` attribute and the `aria-label` are removed, so the explanation is not read twice.
- **Hover and keyboard focus** open a tooltip (`src/components/ui/tooltip.js`) with the explanation.
- **Tap** toggles the same tooltip open and closed, since touch has no hover. Escape or a tap elsewhere closes it.
- Activating the marker does nothing else: it does not open the row, navigate or refetch.

### 2.3 Copy

| Surface | Explanation |
|---------|-------------|
| `/risk` Position Risk table (GBP values) | "Live price unavailable, so the last stored price is shown. Value, P&L and heat use this price until a live price is fetched. Reload the page to try again." |
| Positions page (native prices) | "Live price unavailable, so the last stored price is shown. Value and P&L use this price until a live price is fetched. Reload the page to try again." |
| Dashboard Card 2 sub-line | Visible text unchanged ("⚠ {N} position price(s) stale"). The `/risk` explanation is attached to the card link with `aria-describedby`. The sub-line is not focusable, because the whole card is one link (no nested interactive element). The per-row detail is one click away on `/risk`. |

The v9.11 text ended "converted at today's FX rate". That is untrue when the FX rate is itself a fallback (fx-rate-source-indicator §5), so the FX basis is left to the FX notice.

### 2.4 Positions page placement (ST-07)

- **Table view:** in the Current price cell, after the price, as on `/risk`.
- **Grid view:** after the current price in the card's "Entry vs current price" line.
- Shown only when `price_is_stale === true`. Nothing is shown for false, null or absent.
- `data-testid="price-stale-marker"`, the same id as on `/risk`.

## 3. §13 Compliance

Display only. The marker states the basis of a displayed price and suggests reloading the page. It recommends no trade.

## 4. Frontend Spec Impact

- `positions.md` v2.20 → v2.21: new §Stale Price Marker.
- `risk_dashboard.md` v0.1.13 → v0.1.14: §6.6 rewritten to this record (focusable, described, new copy, light-theme colour).
- `dashboard.md` v3.9 → v3.10: §Card 2 stale-price sub-line gains the card-link description and the new copy.

## 5. Obligations for Sprint Execution

- `GET /positions` returns `price_is_stale` (bool). Contract and `openapi.yaml` in the same commit (ST-07 AC 1).
- The shared component keeps one source for the copy. The two surface variants differ only in "Value and P&L" vs "Value, P&L and heat".

## 6. Testability (CLAUDE.md §2)

- Playwright (ST-07 AC 3): with one stale and one live position mocked, the Positions table and grid show `price-stale-marker` on the stale row only.
- Playwright (ST-08 AC 2): on `/risk` and on Positions, the marker is reachable by Tab, and `toHaveAccessibleDescription` matches the §2.3 text for that surface.
- axe (ST-08 AC 1): `/risk` with a stale row has no violations.
- Playwright: Dashboard Card 2's link has the `/risk` explanation as its accessible description when the sub-line shows.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-29. The copy was reviewed as the slice requires ("design-gate review of the wording").
Product Owner: confirmed, 2026-10-29.
