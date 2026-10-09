Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-09

# QA Evidence — EPIC-02: Risk & Position Display Correctness

**EPIC:** EPIC-02 — Risk & Position Display Correctness (build-and-ship)
**Cycle:** 2026-10-08__release-v9.11
**Sprint goal:** Make the post-trade debrief state R achieved and the stop at exit, confirm every AI feature works after the v9.4–v9.10 import defect, and make the Risk Dashboard and Positions page show real prices, GBP entry values, true stop distance and calendar-day grace (BLG-BE-152, BLG-BE-150, BLG-BE-154, BLG-FE-206), while shipping the AI monthly P&L narrative and clearing v9.11's records, spec and governance hygiene items. See `sprint_goal.md`.
**Test scenarios used:** `tests/test_portfolio_price_integrity.py`, `tests/e2e/risk-price-integrity.spec.js`, `tests/test_grace_alert_calendar_days.py`, `tests/e2e/epic01-v34-lifecycle.spec.js`, `tests/e2e/position-review-cadence-nudge.spec.js`, `tests/test_portfolio_integration.py`, `tests/e2e/recent-trades-zero-pnl-badge.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-10 | `portfolio_endpoints.md#GET /portfolio`; `risk_dashboard.md` §6.6; `dashboard.md` §4 Card 2 | Failed live fetch falls back to the stored native price at live FX (×1.38 guess removed); `price_is_stale` per position; amber stale marker on the Risk Dashboard and a stale notice on Dashboard Card 2 | AC1 unit test (stored native at live FX, never ×1.38, `price_is_stale` true): `TestStalePriceFallback`. AC2 `grep -n "1.38" backend/services/portfolio_service.py` returns nothing (also asserted). AC3 Playwright SC-RPI-01a/b (Risk Dashboard) and SC-RPI-01c/d (Dashboard Card 2, the design-gate addition). AC4 `portfolio_endpoints.md` 2.9.0 and `openapi.yaml` 3.23.0 in commit `2269fe38` | Pass | None found |
| ST-11 | `risk_dashboard.md` §6.2, §6.2a, §6.4 | Entry (GBP) for every market; GRACE rows show "Not enforced (grace)" in Stop and Stop Dist % with no distance colour; GRACE sorted by days left | AC1 Playwright SC-RPI-02a (US Entry "£78.74"). AC2 SC-RPI-02b (two `stop-not-enforced` cells, no rose/amber class). AC3 `risk_dashboard.md` §6 (written at the design gate) matches what shipped; confirmed against the component | Pass | None found. Opportunistic in-file fix disclosed in `31fa13ed`: header "Status" → "State" per §6.2; contract note on `entry_price` currency corrected |
| ST-12 | `portfolio_endpoints.md#GET /portfolio` (`holding_days` note) | `live_holding_days()` computes calendar days from `entry_date`; used by GET /portfolio and by the three other stored-value readers (alerts, compliance, AI context) | AC1 `TestHoldingDaysComputedLive` (stored 9, entry 10 days ago → post-grace PROFITABLE, `grace_period` false). AC2 the three readers are fixed rather than filed (asserted by `test_other_readers_no_longer_read_the_stored_column`). Full backend suite 2212 passed | Pass | None found |
| ST-13 | `portfolio_endpoints.md#GET /portfolio`; `risk_dashboard.md` §6.2; `openapi.yaml` | `stop_distance_pct` computed in native currency by the API; the table shows and sorts by it | AC1 `TestStopDistanceNative::test_us_example_from_the_acceptance_criteria` (100 / 92 / 1.27 / 1.35 → 8.0). AC2 Playwright SC-RPI-03a (8.0% from the API where GBP figures would give 2.2%). AC3 `risk_dashboard.md` §6 (design gate), `portfolio_endpoints.md` 2.10.0 and `openapi.yaml` 3.24.0 together in `f74e45dc` | Pass | None found. Fixed in the same function and disclosed in `f74e45dc`: a NULL `current_stop` crashed `GET /portfolio` |
| ST-14 | `grace_period_alert_endpoint.md` v1.2.0; `positions.md` §Grace Period Alert Zone | Alert list selects on `grace_days_remaining ≤ 2`; label "Day {min(11 − left, 10)} of 10"; ended state at 0; review-cadence suppression uses the same predicate | AC1 unit test `test_day_eight_with_state_entered_today_is_included` and Playwright SC-GP-04 ("Day 9 of 10", 2 days left). The "Day 10 of 10" ended state (design-gate addition): SC-GP-05. AC2 no grace reading on the Positions page uses `days_in_state`; contract and positions.md updated | Pass | None found |
| ST-15 | `dashboard.md` §4 Card 5 (v3.8) | Glyph, badge and text colour test the P&L rounded to 2 dp | AC Playwright SC-RTB-06 (0.004 → neutral glyph and colour; 0.01 → up arrow) | Pass | None found |

**QA test coverage:**
- Scenarios run (locally, 2026-10-08): `tests/e2e/risk-price-integrity.spec.js` with `tests/e2e/risk-dashboard.spec.js` (25 passed); `tests/e2e/epic01-v34-lifecycle.spec.js`, `position-review-cadence-nudge.spec.js`, `lifecycle-badge-grace-calendar-days.spec.js` (27 passed); `tests/e2e/recent-trades-zero-pnl-badge.spec.js` (6 passed); backend full suite 2212 passed, 15 skipped.
- Real CI (frontend testing gate, LL-v9.10-P3-03): Playwright E2E passed on every story commit — ST-10 run 37781054800 (`2269fe38`), ST-11 run 37781530649 (`31fa13ed`), ST-13 run 37782662654 (`f74e45dc`), ST-14 run 37783382571 (`e22b6ff4`), ST-15 run 37783658772 (`441153b4`, branch head; CI Pytest, Critical-Path Smoke, Portfolio Integration, Golden Output, Service Layer Coverage and Endpoint Coverage also green on this SHA).
- Regression areas checked: Risk Dashboard (heat gauge, grace panel, prospective heat: `risk-dashboard.spec.js` unchanged and passing), Positions grace alert and review cadence, Dashboard cards, alerts/compliance/AI services (holding-days readers), `GET /portfolio` contract and openapi drift checks.
- Known deviations: None found — all six stories' deviation checks completed with nothing to file.

**Frontend testing gate:** every observable AC in this EPIC has Playwright coverage that passed in real CI (above). No AC relies on code review alone and no staging run was needed.

---

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- [ ] **Strategy values checked (conditional — ST-36, BLG-GOV-370, v9.11):** prepared by the Sprint Execution Engine for the Director of Quality to confirm. ST-11 — §6.3 (stop not enforced during grace; the table now says so). ST-12 — §6.1/§6.2 and §11 (10-day grace counted in calendar days from entry). ST-13 — §7.1/§7.2 (stop distance measured in the stop's own native currency; no multiplier or ATR value changed). ST-14 — §6.2 (grace window by calendar days since entry; alert at ≥ 8 days). ST-10 — no stop, grace, ATR or exit value touched (price source only). ST-15 — none.
- Signed off by:
- Date:
- Comments: Awaiting Director of Quality sign-off. EPIC-02 merges after EPIC-01 (sprint_backlog.md Merge Order).
