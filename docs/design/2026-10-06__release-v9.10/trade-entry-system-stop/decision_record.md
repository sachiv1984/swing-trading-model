**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-06__release-v9.10
**Story:** ST-07 (EPIC-02, BLG-FE-197)

# Decision Record — Trade Entry Shows the Stop and Risk the System Will Store

## 1. Problem

Trade Entry (`TradeEntry.js`, spec `position_form.md`) misleads in three ways:

- **The Stop Price input has no effect on the stored stop.** `add_position` ignores the submitted `stop_price` and stores `Entry − 5×ATR`, fetching the ATR when the field is empty and falling back to 2% of entry if the fetch fails.
- **The "Suggested stop" hint is wrong.** It uses the Settings `atr_multiplier_initial`, whose form fallback is `2`, not 5.
- **The "Risk (to stop)" row and the Position Sizing widget can show a figure the system will never store.** They are driven by the typed stop, or by that 2× hint.
- **The ATR field label contradicts §4.** It says "ATR Value (Optional)" with the placeholder "For stop suggestion". In practice the ATR always sets the stored stop, and the backend fetches it when the field is blank.

## 2. Decision

### 2.1 The Stop Price input is removed and replaced with a read-only system stop

The Stop Price slot in the ATR/Stop grid becomes a read-only panel (`data-testid="system-initial-stop"`):

| State | Value | Caption (muted `text-xs`) |
|-------|-------|---------------------------|
| Entry price and ATR present | `Entry − {mult}× ATR`, native currency, 2 dp, in `text-rose-400` (the existing stop colour) | "Entry − {mult}× ATR (§5). This is the stop that will be stored." |
| Entry price present, ATR blank | "Calculated on save" | "The system fetches the 14-day ATR for {TICKER} and sets the stop at Entry − {mult}× ATR." |
| Entry price blank | "—" | (none) |

Label: **"Initial Stop (set by system)"**. `{mult}` comes from ST-01's single parameter source, never a hard-coded value or a Settings-form fallback.

### 2.2 The ATR field is relabelled

| | Before | After |
|-|--------|-------|
| Label | "ATR Value (Optional)" | "ATR (14-day)" |
| Placeholder | "For stop suggestion" | "Fetched automatically if blank" |
| "Suggested stop: … (n× ATR)" hint | shown | removed (superseded by §2.1) |

### 2.3 Risk and position sizing use only the system stop

- **"Risk (to stop)" row:** computed from the §2.1 system stop when it is known. When ATR is blank the row shows "Calculated on save" instead of a number, so no unbacked figure is displayed.
- **Position Sizing widget:** receives the system stop as `stopPrice` when it is known and `null` otherwise. The widget's existing empty state applies, with its copy updated to **"Enter an entry price and ATR to size this position."**

### 2.4 The trade plan's stop becomes a reference note

When Trade Entry is prefilled from a trade plan that has a `stop_price`, the plan's stop is no longer placed into an input. A muted note appears under the system-stop panel (`data-testid="plan-stop-reference"`): **"Trade plan stop: {value}. Shown for reference; the stored stop follows the strategy formula."** The plan itself is untouched.

### 2.5 Confirmation on save

The existing "position added" success toast appends the stored stop, which the API already returns as `initial_stop`: **"Initial stop {value}."** This closes the "Calculated on save" case: the user sees the stored value immediately. Toast duration follows the existing `design_system.md` toast-timing standard, with no new timing value.

## 3. §13 Compliance

Display-only and deterministic. The UI now describes system behaviour accurately and adds no recommendation.

## 4. Frontend Spec Impact

`position_form.md` v1.6 → v1.7:

- §Stop Price is replaced by §Initial Stop (set by system).
- §ATR Value is relabelled.
- The field order list is updated.
- The Position Sizing widget's stop input and empty-state copy are updated.

## 5. Testability (CLAUDE.md §2)

Playwright, with a mocked settings/parameter source:

- Entering an entry price and ATR shows the expected `Entry − 5×ATR` value, and the Risk row equals `(entry − system stop) × shares`.
- No stop-price input is present.
- With ATR blank, both the stop and risk show "Calculated on save".
- A plan prefill renders the reference note.

Backend: an `add_position` test pins that the stored `initial_stop` ignores any submitted `stop_price` (ST-07 AC 4).

## 6. Approval

Head of UX & Design: confirmed, 2026-10-06.
Product Owner: confirmed, 2026-10-06. Removal of the Stop Price input (the AC's "removed or relabelled as a note" choice, recorded here) is approved.
