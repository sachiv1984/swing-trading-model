**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-03__release-v9.15
**Stories:** ST-07 (EPIC-01, BLG-FE-219)

# Decision Record — Signal Card Cost Label and Zero-ATR Sizing Reason

## 1. Problem

Since v9.12 a signal's `total_cost` is in GBP and includes entry fees, but the signal card labels it "Allocation Cost". The zero-ATR sizing reason renders as "⚠ Inv-vol sizing: ATR unavailable for this signal", which is jargon.

## 2. Decision

| Element | Current | New |
|---------|---------|-----|
| Cost label (`SignalCard.js`) | "Allocation Cost" | "Total cost (incl. fees)" |
| Zero-ATR reason (`sizing_service.py`, per-signal) | "Inv-vol sizing: ATR unavailable for this signal" | "No size suggested: this ticker's 14-day ATR (its average daily price range) isn't available." |
| Zero-ATR reason (`sizing_service.py`, no valid ATR in the batch) | "Inv-vol sizing: no valid ATR values" | "No size suggested: no ticker in this list has a 14-day ATR available." |

- The reason line keeps its existing position, ⚠ prefix and styling. The `reason` string is served by the backend and displayed as-is, so the copy lives in the backend and in `signal_endpoints.md`.
- The batch-level string is included because it reports the same condition to the same line. The other two `reason` strings (`price_gbp unavailable`, `yielded 0 shares`) are out of ST-07's scope and stay unchanged.

## 3. §13 Compliance

Wording only. "No size suggested" reports why a figure is missing and recommends nothing.

## 4. Frontend Spec Impact

- `pages/signals.md` v0.7 → v0.8: new §Signal Card Cost and Sizing Reason.

## 5. Obligations for Sprint Execution

- `signal_endpoints.md` lists the two new `reason` strings. The `reason` field's type is unchanged, so `openapi.yaml` changes only if it enumerates or exemplifies the old text.

## 6. Testability (CLAUDE.md §2)

- Playwright (ST-07 AC): with a mocked zero-ATR signal, the reason line reads the new per-signal text.
- The cost label is wording only (FI-P3-02): code review.

## 7. Approval

Head of UX & Design: confirmed, 2026-11-03 (agent-mediated, Design Gate Engine).
Product Owner: confirmed, 2026-11-03 (the user, in session).
