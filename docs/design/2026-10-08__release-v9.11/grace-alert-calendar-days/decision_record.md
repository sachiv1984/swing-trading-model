**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-08__release-v9.11
**Story:** ST-14 (EPIC-02, BLG-BE-147)

# Decision Record — Grace Alert Trigger and "Day N of 10" Label in Calendar Days

## 1. Problem

v9.10 (ST-12) moved the Grace Period Alert body text to the calendar-day `grace_days_remaining`. Three other grace readings on the Positions page still use `days_in_state`, which counts days since the position entered its current lifecycle state, not days since entry:

- the alert trigger (`days_in_state ≥ 8`, in `GET /positions/grace-period-alerts`);
- the "Day {days_in_state} of 10" sub-label (`Positions.js`);
- the review-cadence suppression rule (`GRACE_SUPPRESSION_DAYS_IN_STATE`).

If `state_entered_at` is reset (for example by a re-classification today), a day-8 position drops out of the alert list and is labelled with the wrong day. The alert therefore stays silent just before grace ends.

## 2. Decision

All grace readings on the Positions page use calendar days since entry, through `grace_days_remaining` (calendar days, `strategy_rules.md` §6). `grace_days_remaining = 10 − calendar days since entry`, with a floor of 0.

| Reading | Before | After |
|---------|--------|-------|
| Alert trigger | `position_state = 'GRACE'` AND `days_in_state ≥ 8` | `position_state = 'GRACE'` AND `grace_days_remaining ≤ 2` (≥ 8 calendar days since entry) |
| Sub-label | "Day {days_in_state} of 10" | "Day {min(11 − grace_days_remaining, 10)} of 10" |
| Body (ended) | when `days_in_state = 10` | when `grace_days_remaining = 0` |
| Review-cadence suppression | GRACE AND `days_in_state ≥ 8` | the same predicate as the alert trigger |

**Worked example (the ST-14 AC):** a position entered 8 calendar days ago, with `state_entered_at` today, has `grace_days_remaining = 2`. It appears in the alert list, labelled **"Day 9 of 10"**, with the body "Your grace period ends in 2 day(s)."

The day number is 1-based, so entry day is "Day 1". This matches the existing §Days-in-Grace convention ("0 → Day 1 of 10"). The `min(…, 10)` cap keeps the ended state at "Day 10 of 10", as before.

There is no visual change: same card, colours, copy and dismiss behaviour. Only the numbers and who qualifies change.

## 3. §13 Compliance

Display-only and deterministic. No AI.

## 4. Frontend Spec Impact

`positions.md` v2.14 → v2.15: §Grace Period Alert Zone (trigger, sub-label, ended body) and §Last Reviewed Column suppression rule. The ST-14 AC also requires `grace_period_alert_endpoint.md` to be updated. That is an API contract outside this gate's write scope, so the story does it.

## 5. Obligations for Sprint Execution

- `GET /positions/grace-period-alerts` selects on `grace_days_remaining ≤ 2` (calendar days), not `days_in_state ≥ 8`, and returns `grace_days_remaining`. Update `grace_period_alert_endpoint.md` and, if the response shape changes, `openapi.yaml` in the same commit. No new route.
- The `Math.max(0, 10 − days_in_state)` fallback in `Positions.js` is removed. If `grace_days_remaining` is null, the alert card shows no day label and no days-left sentence. It never falls back to `days_in_state`.

## 6. Testability (CLAUDE.md §2)

- Unit test on the alert selection: entry 8 calendar days ago with `state_entered_at` today is included, and `grace_days_remaining = 2`.
- Playwright, mocked alerts: the card shows "Day 9 of 10" and "ends in 2 day(s)".
- Playwright, mocked `grace_days_remaining: 0`: "Day 10 of 10" and the ended body.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-08.
Product Owner: confirmed, 2026-10-08.
