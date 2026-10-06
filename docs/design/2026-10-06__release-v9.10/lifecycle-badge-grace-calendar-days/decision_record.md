**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-06__release-v9.10
**Story:** ST-12 (EPIC-03, BLG-FE-196)

# Decision Record — Lifecycle Badge Agrees with the §6 Grace Window, in Calendar Days

## 1. Problem

`strategy_rules.md` §6.2 defines grace as **10 calendar days** (days 0–9), and `grace_period` / `grace_days_remaining` on `GET /positions` follow that rule. The lifecycle badge does not:

- `position_lifecycle_service.compute_position_state` checks the ±0.5 ATR bands *before* grace and counts **weekdays**. An in-grace position outside the band therefore shows LOSING or PROFITABLE, and the grace boundary drifts from the `grace_period` flag.
- The GRACE badge shows `days_in_state` ("GRACE — 3d"), which is days *in the state*, not days left.
- The GRACE tooltip says "after 10 trading days". The Grace Period Alert says "ends in N trading day(s)" and computes N from `days_in_state`.
- Every UNKNOWN badge has the same tooltip ("Set a stop and R-target…"), whatever the actual cause.

## 2. Decision

### 2.1 GRACE takes precedence during grace

While `grace_period` is true, the badge is **GRACE**, regardless of price relative to entry. The backend classification checks grace first, using the same calendar-day rule as `grace_period`. That is a backend change in ST-12's commit, and the frontend must not re-derive it.

### 2.2 GRACE badge label and tooltip

| Element | Before | After |
|---------|--------|-------|
| Label | `GRACE — {days_in_state}d` | `GRACE — {grace_days_remaining}d left` |
| Tooltip | "Exits grace when position moves > 0.5 ATR or after 10 trading days" | "Grace period: {n} calendar day(s) left. The stop is tracked but not enforced until the grace period ends (10 calendar days, §6)." |
| `aria-label` | "Position state: GRACE, N days in state" | "Position state: GRACE, {n} calendar days of grace left" |

If `grace_days_remaining` is null while the state is GRACE (a transient mismatch), the label falls back to plain "GRACE" with no number.

### 2.3 Grace Period Alert copy

- Days-left text: "Your grace period ends in {n} day(s)." where `n = grace_days_remaining`, replacing `10 − days_in_state`. The word "trading" is removed.
- The "Review your original thesis before the window closes." sentence and the ended-state sentence are unchanged.

This leaves no "trading days" wording for the grace period anywhere on the page.

### 2.4 UNKNOWN tooltip distinguishes the cause

The backend returns the reason a position is UNKNOWN. The working name is `lifecycle_reason`, a nullable field that is set only for UNKNOWN; execution finalises the name in `position_endpoints.md` and `openapi.yaml` in the same commit (CLAUDE.md §2). Values and copy:

| Reason | Tooltip |
|--------|---------|
| `missing_data` (no ATR, entry price or price) | "No lifecycle state: ATR or price data is missing for this position." |
| `flat_after_grace` (post-grace, within ±0.5 ATR of entry) | "No lifecycle state: the grace period has ended and the price is within 0.5 ATR of entry." |
| null or absent | "No lifecycle state is available for this position." |

The previous "Set a stop and R-target on the linked trade plan…" copy is retired. A missing initial stop only blocks EXIT ZONE; it never produces UNKNOWN.

**Interaction with ST-11:** if ST-11 rules that `strategy_rules.md` §9 governs (post-grace P&L ≤ 0 is LOSING and > 0 is PROFITABLE), `flat_after_grace` can no longer occur. Its copy then stays dormant, and ST-12 drops that value from the contract. In-grace behaviour (§2.1–§2.3) does not depend on ST-11.

### 2.5 Unchanged

The state colours, the other states' tooltips, the badge shape and the 4-state machine statement in `positions.md` are unchanged.

## 3. §13 Compliance

Display-only. It aligns displayed state with §6/§9 and adds no recommendation. No AI.

## 4. Frontend Spec Impact

`positions.md` v2.11:

- §Position Lifecycle State Badge: GRACE label and tooltip, UNKNOWN reason table, grace precedence.
- §Grace Period Alert Zone: the days-left basis.

## 5. Testability (CLAUDE.md §2)

Playwright, with mocked `GET /positions`:

- An in-grace position more than 0.5 ATR below entry shows "GRACE — 4d left" (backend classification covered by unit tests).
- No element contains "trading day".
- Each UNKNOWN reason renders its own tooltip text.

## 6. Approval

Head of UX & Design: confirmed, 2026-10-06.
Product Owner: confirmed, 2026-10-06. The label changing from days-in-state to days-left is approved.
