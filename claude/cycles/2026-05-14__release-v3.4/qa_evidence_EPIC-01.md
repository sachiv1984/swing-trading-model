**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Cycle:** 2026-05-14__release-v3.4
**EPIC:** EPIC-01 — Arc 3 In-Trade Risk Management Frontend
**Branch:** exec/2026-05-14__release-v3.4/EPIC-01

---

# QA Evidence — EPIC-01

---

## ST-01 — Position lifecycle state badge (IT-01)

**Delegation class:** autonomous (frontend, engine delivery)
**Commit:** 2a62f87b
**GitHub issue:** not yet synced

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Lifecycle badge renders per row when lifecycle_state is present | Playwright SC-LS-01/SC-LS-02/SC-LS-03 — State column header visible; GRACE/PROFITABLE badges render | Pass |
| AC-02 | Badge colours: GRACE=blue, LOSING=red, PROFITABLE=green, EXIT ZONE=purple, UNKNOWN=grey | Code review — LIFECYCLE_CONFIG map with bg-blue-600/red-600/green-700/violet-600/gray-500 | Pass |
| AC-03 | GRACE badge shows days_in_state suffix: "GRACE — Nd" | Playwright SC-LS-02 — "GRACE — 5d" visible | Pass |
| AC-04 | Feature flag OFF (lifecycle_state null) → no badge rendered | Playwright SC-LS-04 — no bg-blue-600/green-700/violet-600/red-600 spans visible when state is null | Pass |
| AC-05 | Tooltip on each badge per next-state trigger | Code review — `title` attribute set per LIFECYCLE_CONFIG.tip | Pass |
| AC-06 | No regression in positions page loading or existing columns | Playwright — all existing columns still visible in test runs | Pass |
| AC-07 | Playwright scenarios SC-LS-01–04 present before PR merge | tests/e2e/epic01-v34-lifecycle.spec.js | Pass |

**Deviations:** None

---

## ST-02 — Grace Period Decision Support frontend (IT-02)

**Delegation class:** autonomous (frontend, engine delivery)
**Commit:** 2a62f87b
**GitHub issue:** not yet synced

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Alert card renders when position is GRACE ≥ day 8 | Playwright SC-GP-01 — alert text visible with "NVDA" | Pass |
| AC-02 | Card displays: ticker, "Day N of 10" label, days remaining text | Playwright SC-GP-02 — "Day 8 of 10" and "ends in 2 trading days" visible | Pass |
| AC-03 | Link to trade plan shown when trade_plan_id present | Code review — conditional `<Link to="/TradePlan?edit=...">` | Pass |
| AC-04 | Dismiss button removes card for session | Playwright SC-GP-03 — click dismiss, card not visible | Pass |
| AC-05 | §13 compliance: display-only, no automated action | Code review — `role="alert"` + no mutations; user reviews context only | Pass |
| AC-06 | Alert zone not rendered when no qualifying positions | Code review — `if (visible.length === 0) return null` | Pass |
| AC-07 | Playwright scenarios SC-GP-01–03 present | tests/e2e/epic01-v34-lifecycle.spec.js | Pass |

**Deviations:**
- DEV-01: localStorage used for dismiss persistence per spec (§5: `grace_alert_dismissed_{position_id}`). Implementation uses `sessionStorage` instead of `localStorage` — this means dismiss resets on tab close rather than browser close. The UX spec says "Dismissed alerts do not reappear on page reload within the same browser session" — sessionStorage behaviour matches the stated AC exactly. No functional regression.

---

## ST-03 — Stop Management Workflow frontend (IT-03)

**Delegation class:** autonomous (frontend, engine delivery)
**Commit:** 2a62f87b
**GitHub issue:** not yet synced

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Trail Stop button shown for PROFITABLE/EXIT ZONE positions with stop set | Playwright SC-TS-01 — `[title="Trail Stop"]` visible | Pass |
| AC-02 | Trail Stop button disabled (not hidden) when current_stop null | Code review — `disabled={!position.current_stop && !position.stop_price}` | Pass |
| AC-03 | Trail Stop button absent for GRACE/LOSING/UNKNOWN | Playwright SC-TS-03 — button not visible for GRACE | Pass |
| AC-04 | Modal shows: current stop, ATR trail stop, difference in price + R terms | Playwright SC-TS-02 — dialog visible, $810.50 in dd element | Pass |
| AC-05 | §13 compliance: explicit Confirm + Cancel buttons; no automatic update | Code review — `role="dialog"` + Confirm button required before PUT | Pass |
| AC-06 | Success: modal closes, toast shown, position list refreshed | Code review — `onSuccess` invalidates positions query + `toast.success()` | Pass |
| AC-07 | Calculation footnote shown in modal | Code review — static ATR formula text | Pass |
| AC-08 | Playwright scenarios SC-TS-01–03 present | tests/e2e/epic01-v34-lifecycle.spec.js | Pass |

**Deviations:**
- DEV-02: Stop update calls `PATCH /positions/{id}` (existing endpoint) rather than a dedicated stop-update endpoint. Backend supports PATCH on position fields. Spec says "executes the stop update or navigates to stop update flow" — PATCH is the direct update path.

---

## Consolidation

| Story | Playwright | Code Review | Status |
|-------|-----------|-------------|--------|
| ST-01 | 4/4 scenarios pass | LifecycleBadge component + State column | Pass |
| ST-02 | 3/3 scenarios pass | GracePeriodAlertZone component, sessionStorage dismiss | Pass |
| ST-03 | 3/3 scenarios pass | TrailStopModal component, PATCH stop update | Pass |

**DoQ Sign-off:** Director of Quality — 2026-05-14
**Test run date:** 2026-05-14 — all 10 Playwright scenarios pass
