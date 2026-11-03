**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-03__release-v9.15
**Stories:** ST-06 (EPIC-01, BLG-BE-173), ST-17 (EPIC-03, BLG-FE-218)

# Decision Record — View Trail Modal Wording and Formula Footnote

## 1. Problem

Since the v9.12 ruling (ESC-EXEC-20261013-06) the Trail Stop modal is read-only, but its text still reads as an action: the heading says "Trail Stop", a row is "Raise by", and the disabled button's tooltip tells the user to "Add a stop". Its footnote states a fixed "ATR × 2.0" with no breakeven floor, while the live stop uses the §7.2 profit formula with the floor (ST-06). Both stories rewrite the same modal, so this record covers both.

## 2. Decision

### 2.1 Text changes

| Element | Current | New |
|---------|---------|-----|
| Modal heading (ST-17) | "Trail Stop — {TICKER}" | "View Trail — {TICKER}" |
| Row label (ST-17) | "Raise by (display only; not an action)" / "Raise by" | "Difference vs current stop" |
| Disabled button tooltip (ST-17) | "No current stop set. Add a stop to use trail management." | "No stop is recorded for this position yet, so there is no trail to compare." |
| Footnote (ST-06) | "ATR trail stop = current price − (ATR × 2.0). ATR period: 14 days. Multiplier per strategy rules." | "ATR trail stop = current price − (profit multiplier × 14-day ATR), never below your entry price. This is the strategy's profitable-position stop (§7.2)." |

- The footnote carries no number, so no literal multiplier remains in it (ST-06 AC 2), and it cannot drift from `backend/strategy_parameters.py`. The multiplier is already shown per row on the Positions page (`{mult}× ATR {atr}` provenance line).
- The value and sign formatting of the difference row is unchanged ("+£X.XX", or "−£X.XX" in amber).
- The no-raise note and the read-only note are unchanged.

### 2.2 Value (ST-06)

`atr_trail_stop` becomes the value `calculate_trailing_stop` produces, breakeven floor included. When the floor binds, the modal shows the entry price as the ATR trail stop. No extra label marks this, because the footnote states the floor.

## 3. §13 Compliance

Wording and a corrected display value. The modal stays read-only. No control changes a stop.

## 4. Frontend Spec Impact

- `pages/positions.md` v2.21 → v2.22: §Trail Stop Action (Trail Stop Button tooltip; Trail Stop Modal heading, row label and footnote).

## 5. Obligations for Sprint Execution

- ST-06 updates `position_endpoints.md`'s stop-trail description to say the value uses the §7.2 profit formula with the breakeven floor. The response shape does not change, so `openapi.yaml` needs no schema change. If the description field is mirrored there, update it in the same commit.
- ST-17 updates the Playwright SC-TS-* heading and label assertions. ST-42 renames the SC-TS-* IDs in the same sprint, so the two stories should agree on the final IDs.

## 6. Testability (CLAUDE.md §2)

- Playwright (ST-17): the modal heading reads "View Trail — {TICKER}" and the row label "Difference vs current stop".
- ST-06's footnote and ST-17's tooltip are wording only (FI-P3-02): code review of the static text.
- ST-06's value: unit test against `calculate_trailing_stop`, including a case where the floor binds (slice AC 1).

## 7. Approval

Head of UX & Design: confirmed, 2026-11-03 (agent-mediated, Design Gate Engine).
Product Owner: confirmed, 2026-11-03 (the user, in session).
