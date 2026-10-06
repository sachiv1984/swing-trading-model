**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-06__release-v9.10
**Story:** ST-06 (EPIC-02, BLG-FE-193)

# Decision Record — Showing ATR, Active Multiplier and Recalculation Source in the Stop Cell

## 1. Problem

The Stop cell (Table View, `Positions.js`) and the Stop tile (Grid View, `PositionCard.js`) show an initial stop and a trailing stop. They do not show how either number was produced. Three fields shipped in v9.9 (`BLG-BE-135`) and already appear on `GET /positions`: `atr_value`, `active_atr_multiplier` and `stop_calculated_at`. The header explainer (`TrailingStopExplainerIcon.js`) claims "ATR is recalculated daily". That is a static claim, and the row's actual recalculation event can contradict it.

## 2. Decision

### 2.1 Always-visible provenance line (both views)

A third, muted line sits under the trailing-stop value: `text-xs text-slate-600 dark:text-slate-400`, `data-testid="stop-provenance"`.

| Data | Line text |
|------|-----------|
| Multiplier and ATR present | `{mult}× ATR {atr}`, e.g. "2× ATR $3.21" |
| ATR present, multiplier null (not yet recalculated since DS-22) | `ATR {atr}` |
| ATR missing or 0 | `ATR unavailable` |

- **ATR** is formatted as native currency with 2 dp (`formatCurrency(atr_value, { currency })`), the same basis as the stop.
- **Multiplier** is printed without decimals when it is a whole number (`2×`) and with 1 dp otherwise (`2.5×`).
- If ST-02's `atr_source` has landed and equals `fallback`, append ` · estimated`. If it equals `user`, append ` · entered`. Nothing is appended when the field is absent.

The line makes the ATR value and the active multiplier visible without hovering, so Playwright can assert them directly.

### 2.2 Per-row stop details tooltip

The trailing-stop value becomes the trigger: a `button` with a dotted underline and `aria-label="Stop calculation details for {TICKER}"`. It uses the existing `Tooltip` component with the same delay as the header explainer (200 ms, no new timing parameter) and `data-testid="stop-details-tooltip"`.

| Row | Content |
|-----|---------|
| Title | "How this stop was set" |
| ATR | "ATR (14-day): {atr}" (with "estimated from 2% of entry price" when `atr_source = fallback`) |
| Multiplier | "Multiplier: 2× (profitable, tight)" or "Multiplier: 5× (losing or flat, wide)". If null: "Multiplier: not recorded yet" |
| Formula | Profitable: "Price − 2× ATR, never below entry (§7.2)". Losing/flat: "Price − 5× ATR (§7.2)". Use the actual multiplier value, not a constant |
| Ratchet | "A stop never loosens: the stop shown is the highest level reached (§7.3)." |
| Last recalculated | "Last recalculated {d MMM yyyy, HH:mm} — {source}", where source is "nightly update" or "when positions loaded". If `stop_calculated_at` is null: "Not recalculated since recalculation tracking began." |
| Grace (only when `grace_period` is true) | "Grace period: the stop is tracked but not enforced (§6.3)." |

**Source dependency:** neither `stop_calculated_at` nor any other existing field records *which* path recalculated the stop. ST-06 therefore needs a new nullable field on `GET /positions` that distinguishes the on-load path from the nightly path (`stop_calculation_source`: `on_load` | `nightly` is the working name; execution finalises it in the contract). When it is null, show the timestamp alone with no source. Because ST-01 already changes both recalculation paths, the field can land in ST-01's or ST-06's commit, together with `position_endpoints.md` and `openapi.yaml` (CLAUDE.md §2).

**Checkability:** with the ATR, multiplier, formula and ratchet rule all on the page, a reader can reproduce the stop from the current price. If the formula gives a lower number, the ratchet row explains why the stop shown is higher.

### 2.3 Header explainer copy (`TrailingStopExplainerIcon.js`)

Replace the sentence "ATR is recalculated daily (14-day period)." with:

> "ATR (14-day) is recalculated when positions load and by a nightly update. Each stop's details show when it was last recalculated."

All other explainer text is unchanged. The header stays static and shared across rows; the row-specific event lives only in the per-row tooltip (§2.2). This meets the AC that the copy reflects the row's actual event without putting per-row data into a per-column header.

### 2.4 Unchanged

The `Init:` line, the breach badge (colour, label, placement), the column header text and the Trail Stop modal are unchanged. No new colour is introduced.

## 3. §13 Compliance

Display-only. It explains a deterministic, already-computed stop and makes no recommendation. The explainer still does not surface parameters as tunable values: it shows the multiplier that was applied, not a control.

## 4. Frontend Spec Impact

- `positions.md` v2.10 → v2.11, new subsection "Stop Provenance Line and Per-Row Stop Details (v9.10)" under §Trailing Stop Column. The quoted explainer copy is updated in place.

## 5. Testability (CLAUDE.md §2)

Playwright, with mocked `GET /positions`:

- The provenance line shows the expected multiplier and ATR for one profitable and one losing row.
- Focusing the trigger shows the tooltip with the formula, the timestamp and the source text for both `nightly` and `on_load`.
- A null-field row shows the fallback strings.
- The header explainer no longer contains "recalculated daily".

## 6. Approval

Head of UX & Design: confirmed, 2026-10-06.
Product Owner: confirmed, 2026-10-06. This includes the new source field dependency.
