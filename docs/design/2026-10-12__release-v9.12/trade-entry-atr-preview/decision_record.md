**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-12__release-v9.12
**Stories:** ST-17 (EPIC-03, BLG-BE-146), ST-18 (EPIC-03, BLG-FE-203)

# Decision Record — Trade Entry: ATR Preview, ATR Unit and Implausible-ATR Validation

## 1. Problem

Since v9.10 (ST-07), Trade Entry shows only the system stop: Entry − 5× ATR. With the ATR field blank, the backend fetches ATR only at save. Until then Initial Stop, Risk (to stop) and the Position Sizing widget show "Calculated on save", so a user who does not know the ATR cannot size the trade (ST-17).

The ATR field also shows no unit. A UK user who types ATR in pence gets a stop 100× too wide, stored with `atr_source = user` (ST-18).

## 2. Decision

### 2.1 ATR preview (ST-17)

- **Endpoint:** `GET /market/atr/{ticker}?market=UK|US` → `{ ticker, market, atr, atr_period: 14, as_of }`. `atr` is native currency, or `null` when unavailable. It uses the same `calculate_atr()` path as `add_position()`.
- **When called:** once the ticker and market are known and the ATR field is blank, reusing Trade Entry's existing 300 ms input debounce. No new timing parameter. It is not called while a typed ATR is present.
- **The fetched value is never placed into the ATR input.** The input stays blank, so `atr_source` at save remains `system`. A hint under the field (`data-testid="atr-fetched-hint"`, `text-xs text-slate-600 dark:text-slate-400`): "Fetched: {atr} (14-day, {as_of d MMM})".
- **Initial Stop panel**, one new state:

| State | Value | Caption |
|-------|-------|---------|
| Entry present, ATR blank, fetching | "Fetching ATR…" (muted) | — |
| Entry present, ATR blank, fetched ATR available | `Entry − 5× ATR`, native, 2 dp, existing rose token | "Entry − 5× ATR (§5), using the fetched 14-day ATR. The stop is recalculated at save and may differ slightly if prices update before then." |
| Entry present, ATR blank, endpoint returns `null` or fails | "Calculated on save" (existing) | existing caption |

- **Risk (to stop)** and the **Position Sizing widget** use the preview stop when it is shown, and keep their existing empty states otherwise. A fetch failure shows no error banner. It falls back silently to "Calculated on save".
- A typed ATR always takes precedence. Typing replaces the preview immediately, and the hint is hidden.

### 2.2 ATR unit (ST-18)

The label reads **"ATR (14-day, £)"** for UK and **"ATR (14-day, $)"** for US. It stays "ATR (14-day)" until the market is known.

### 2.3 Implausible typed ATR (ST-18)

- **Rule:** a typed ATR where `5 × ATR ≥ entry price` is invalid, because the stop would be at or below zero.
- **Inline error**, following the canonical form-validation pattern (`design_system.md` §Error States: blur-or-submit trigger, below the field, `text-xs text-rose-700 dark:text-rose-400`), `data-testid="atr-implausible-error"`: "This ATR puts the stop at or below zero. Check the unit: ATR is in {£|$}, not pence or cents."
- **Submit** is disabled while this error is shown. The field gets `aria-invalid="true"` and `aria-describedby` pointing to the message. This is the only Trade Entry validation that disables submit. The sizing widget remains decision support (§Form submission behaviour), and its own `INVALID_STOP_PRICE` state may also show.
- **API:** `POST /portfolio/position` rejects the same input with 400. The message states the same rule in plain words.

## 3. §13 Compliance

Deterministic. ATR is a §7.1 input, and the preview shows the existing §5 formula before save. No AI. No recommendation beyond the existing sizing widget.

## 4. Frontend Spec Impact

`docs/specs/frontend/components/position_form.md` v1.8 → v1.9: §ATR (14-day), §Initial Stop, §Widget inputs and §Validation Errors. The Trade Entry page spec lives in `components/`, not `pages/`. The v9.10 design gate updated it on the same basis.

## 5. Obligations for Sprint Execution

- ST-17 adds a route: a `##` contract heading, an `openapi.yaml` entry, a `backend/routers/test.py` entry (representative ticker `AAPL`), the `SystemStatus.js` fallback count and `SC-SS-01b`, all in the same commit (CLAUDE.md §2, RISK-04).
- ST-17 backend test: the preview stop equals `POST /portfolio/position`'s `initial_stop` for the same inputs (AC 2).
- ST-19 covers the sizing widget after these changes, so update its scenarios' mocks for the preview call.

## 6. Testability (CLAUDE.md §2)

- Playwright (mocked ATR endpoint): a numeric stop, risk and suggested shares show before save. With `atr: null`, "Calculated on save" remains.
- Playwright: the label shows £ for a UK ticker and $ for a US ticker.
- Playwright: entry 10, ATR 2 → inline error visible and submit disabled. ATR 1.5 → no error.
- Backend test: the 400 on `5 × ATR ≥ entry`.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-12.
Product Owner: confirmed, 2026-10-12.
