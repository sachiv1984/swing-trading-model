**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-16__release-v9.13
**Story:** ST-06 (EPIC-02, BLG-BE-180)

# Decision Record — Trade Entry When the Fetched ATR Puts the Stop at or Below Zero

## 1. Problem

v9.12 ST-18 rejects a **typed** ATR when 5 × ATR ≥ entry. A **fetched** (preview) ATR has no such check. On a low-priced volatile ticker, Trade Entry's Initial Stop panel shows a negative "Initial Stop (set by system)" with no explanation, and save stores it.

The rule is decided in-sprint by the Strategy Rules & System Intent Owner: reject with 400, or apply a floor. Both branches are designed here, as the v9.12 Trail Stop precedent did.

## 2. Decision

A negative or zero stop is **never** displayed under either branch.

### 2.1 Branch A — reject

New row in the §Initial Stop state table, for when the preview ATR is available and `entry − {mult} × ATR ≤ 0`:

| Value | Caption |
|-------|---------|
| "No valid stop" (`text-rose-700 dark:text-rose-400`) | "{mult}× the fetched 14-day ATR ({ATR} {£\|$}) is at or above the entry price, so the stop would be at or below zero. §5 cannot set a stop for this entry." |

- `data-testid="initial-stop-invalid"` on the caption, `role="status"`.
- **Submit is disabled** while this shows, the same as the typed-ATR error. The §Validation Errors list gains this case.
- **Risk (to stop)** shows "—". The Position Sizing widget shows its empty hint and is not passed a stop.
- If the server rejects at save (for example the ATR moved between preview and save), the 400's message shows in the existing Error Banner.

### 2.2 Branch B — floor

| Value | Caption |
|-------|---------|
| The floored stop, native currency, 2 dp, `text-rose-400` (existing value style) | "Entry − {mult}× ATR would be at or below zero, so the stop is set at the §5 floor: {floor rule text}." |

- `{floor rule text}` is the ruling's wording as recorded in `strategy_rules.md` §5, for example "1% of the entry price".
- `data-testid="initial-stop-floored"` on the caption. Submit stays enabled.
- Risk and sizing use the floored stop. The save toast's "Initial stop {value}." already reports the stored value.

### 2.3 Unchanged

The typed-ATR inline error (`atr-implausible-error`) keeps its v9.12 wording and still takes precedence when the ATR field is filled. The other Initial Stop states are unchanged.

## 3. §13 Compliance

No automated action. Branch A refuses an entry the strategy cannot stop. Branch B applies a rule recorded in §5. Either way, the stop is never weaker than the strategy states.

## 4. Frontend Spec Impact

`components/position_form.md` v1.9 → v1.10: §Initial Stop gains the conditional rows (Branch A or B, whichever the ruling selects). §Validation Errors gains the Branch A case. The unused branch is deleted at implementation, as with the v9.12 Trail Stop branches.

## 5. Testability (CLAUDE.md §2)

- Playwright (AC 3): mocked preview ATR where 5 × ATR ≥ entry. No negative value is visible in `system-initial-stop`, and `initial-stop-invalid` (A) or `initial-stop-floored` (B) is visible. Branch A additionally checks that submit is disabled.

## 6. Approval

Head of UX & Design: confirmed, 2026-10-16.
Product Owner: confirmed, 2026-10-16.
