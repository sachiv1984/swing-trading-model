**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-29__release-v9.14
**Story:** ST-14 (EPIC-02, BLG-SPEC-192)

# Decision Record — Last Reviewed Flag Suppression When Grace Has Ended

## 1. Problem

`positions.md` §Last Reviewed Column suppresses the amber "not reviewed" flag while the Grace Period Alert Zone shows the position, and calls the two predicates the same. They are not the same once grace has ended:

- The Alert Zone (`GET /positions/grace-period-alerts`) uses the stored GRACE state and `max(0, 10 − days)`. On day 10 or later it shows "Grace period has ended…".
- The suppression check (`Positions.js` ~589, `PositionCard.js` ~97) reads `GET /positions`' `grace_days_remaining`, which is `null` from day 10. So it does not suppress.

A position whose stored state is still GRACE on day 10 or later shows both the Alert Zone card and the amber flag. That is the double prompt the suppression rule exists to prevent.

## 2. Decision

**Option (a): fix the predicate.** The slice allows either a code fix or a documented difference. The spec's intent is one prompt at a time, so the code is brought into line with it rather than the spec weakened.

The flag is suppressed when the position is in the Alert Zone, which is when **either** holds:

1. `position_state = 'GRACE'` and `grace_days_remaining ≤ 2` (unchanged), **or**
2. `position_state = 'GRACE'`, `grace_days_remaining` is `null` and `holding_days ≥ 10`. This is the ended-grace case, which the Alert Zone shows as "Grace period has ended".

The rest of the rule is unchanged. The "Last Reviewed" text still renders, and only the amber styling is suppressed. Once the position leaves GRACE on the next refresh, the flag can fire.

The predicate is one shared helper used by both `Positions.js` and `PositionCard.js`, so the table and grid views cannot drift apart.

## 3. §13 Compliance

Display only.

## 4. Frontend Spec Impact

`positions.md` v2.20 → v2.21: §Last Reviewed Column suppression rule states both conditions.

## 5. Obligations for Sprint Execution

- `holding_days` must be on the position object both views read. If it is absent there, the helper uses the same calendar-day count `GET /positions` uses for `grace_days_remaining`, not `days_in_state`. `days_in_state` resets with `state_entered_at` (positions.md §Grace Period Alert Zone, v2.15 note).

## 6. Testability (CLAUDE.md §2)

- Playwright (AC 2): stored GRACE, `grace_days_remaining: null`, `holding_days: 11`, last review 20 days ago: the Last Reviewed text renders without the amber flag, in table and grid.
- Playwright: the same position with `position_state: 'LOSING'` shows the flag.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-29.
Product Owner: confirmed, 2026-10-29.
