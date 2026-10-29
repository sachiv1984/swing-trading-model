**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-29__release-v9.14
**Stories:** ST-04 (EPIC-01, BLG-BE-194), ST-05 (EPIC-01, BLG-BE-169)

# Decision Record — FX Rate Source and Age Indicator

## 1. Problem

`get_live_fx_rate()` falls back to the constant 1.27 when Yahoo Finance fails. Every US value, P&L, heat figure and sizing is then converted at a guessed rate, and nothing on screen says so. ST-04 adds a last-known-good stored rate with its timestamp, ahead of the constant. ST-05 flags any non-live rate on the Dashboard and Risk Dashboard. Both stories need one indicator, so this record covers both.

## 2. Decision

### 2.1 Source states

The API reports `fx_rate_source`, one of three values:

| `fx_rate_source` | Meaning | Indicator |
|------------------|---------|-----------|
| `live` | Fetched in the current cache window | None |
| `last_known` | The fetch failed; the last stored rate is used (ST-04) | Amber notice with the rate's age |
| `constant` | The fetch failed and no rate has ever been stored | Amber notice naming the fixed fallback |

The age is shown for every `last_known` rate. ST-04's AC needs it at more than one trading day, and showing it at all ages is a superset. A short outage then reads "from 12 min ago", which is accurate and needs no threshold.

### 2.2 Copy

| Source | Visible text | Accessible description and tooltip |
|--------|--------------|------------------------------------|
| `last_known` | "⚠ FX rate not live: GBP/USD {rate} from {age}" | "The live GBP/USD rate is unavailable. US values, P&L and heat use the last fetched rate, {rate} at {dd MMM yyyy, HH:mm}. Reload the page to try again." |
| `constant` | "⚠ FX rate unavailable: using fixed GBP/USD {rate}" | "No GBP/USD rate could be fetched, so a fixed fallback of {rate} is used. US values, P&L and heat are approximate. Reload the page to try again." |

- `{rate}` is 4 dp. `{age}`: "{m} min ago" under 1 h, "{h} h ago" under 48 h, then "{d} days ago". The exact timestamp is in the description.
- The word "live" is never used for a non-live rate. The text never shows 1.27 (or any other value) as if it were live (ST-05 AC 2).

### 2.3 Placement

| Surface | Placement | `data-testid` |
|---------|-----------|---------------|
| Dashboard Card 2 — Portfolio Heat | A sub-line under the value, after the stale-price sub-line if both show. `text-xs text-amber-700 dark:text-amber-400`. The card stays one link to `/risk`, so the description is attached to the card link with `aria-describedby` (no nested focusable element). | `dashboard-fx-source-notice` |
| Risk Dashboard | A single line directly under the page heading, above the top row. It covers every FX-dependent figure on the page. Same tokens, with an `AlertTriangle` icon (`w-3.5 h-3.5`, `aria-hidden`). The line is a focusable element with the §2.2 description (stale-marker pattern). | `risk-fx-source-notice` |
| Signals page — FX Rate tile | Under "1 GBP = ${rate} USD": a muted line "Live" for `live`, or the §2.2 visible text without the "⚠ FX rate" prefix ("not live: from {age}", "fixed fallback") in amber. | `signals-fx-source` |

The Positions page is not in scope. Its prices are native and its P&L (GBP) column is FX-dependent, but neither story names it. The field is on `GET /positions` (ST-05 AC 1), so a Positions indicator can follow as its own item.

### 2.4 Tokens (light and dark)

`text-amber-700 dark:text-amber-400` (`design_system.md` §Light-Theme Colour Tokens, warning text, 5.02 / 4.58). Not `text-amber-600`, which fails on white.

## 3. §13 Compliance

Display only. The notice reports the basis of the figures shown. It changes no figure, size or stop.

## 4. Frontend Spec Impact

- `dashboard.md` v3.9 → v3.10: §Card 2 — FX source sub-line.
- `risk_dashboard.md` v0.1.13 → v0.1.14: new §2a FX Rate Source Notice.
- `signals.md` v0.6 → v0.7: §Market Status Bar, FX Rate tile.

## 5. Obligations for Sprint Execution

- `GET /portfolio` and `GET /positions` return `fx_rate`, `fx_rate_source` and `fx_rate_as_of` (ISO-8601, null for `constant`). `GET /market/status` returns the same three alongside its `fx_rate`, so the Signals tile has a source. Contracts and `openapi.yaml` in the same commit (ST-05 AC 1).
- The Signals page's own constant (`fxRate={marketStatus?.fx_rate || 1.3611}`, and the 1.3611 in its error fallback) must go. With no rate, the tile shows "—", not a made-up rate.
- ST-06 reads the same `fx_rate_source` for the System Status Yahoo check, so there is one staleness signal, not two (slice ST-05 Sequencing).
- The v9.11 stale-price text "converted at today's FX rate" becomes untrue under a fallback. It is replaced in ST-08 (stale-price-marker §2.2).

## 6. Testability (CLAUDE.md §2)

- Playwright (ST-04 AC 3, ST-05 AC 3): with `GET /portfolio` mocked to `last_known` and an `fx_rate_as_of` two days old, `dashboard-fx-source-notice` and `risk-fx-source-notice` show "from 2 days ago". With `constant`, both show "fixed GBP/USD". With `live`, neither renders.
- Playwright: `risk-fx-source-notice` has the §2.2 accessible description.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-29.
Product Owner: confirmed, 2026-10-29.
