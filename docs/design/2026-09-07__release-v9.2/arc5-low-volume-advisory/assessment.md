**Owner:** Metrics Definitions & Analytics Owner
**Class:** Planning Document (Class 4)
**Status:** Complete
**Cycle:** 2026-09-07__release-v9.2
**Story:** ST-01 (EPIC-01, BLG-FEAT-44)

# Assessment — Arc5ComplianceSection Low-Trade-Volume Advisory

## 1. Question

ST-01 AC-01 requires an assessment, produced during execution, concluding either "advisory warranted" or "advisory not needed" for `Arc5ComplianceSection`'s four compliance stat cards at low trade counts. `docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/decision_record.md` fixes the *design* conditionally, in advance of this conclusion.

## 2. Analysis

`Arc5ComplianceSection` renders four cards, each with a different underlying sample and window:

| Card | Metric | Denominator / window |
|------|--------|----------------------|
| Red Flag Events/Week | `events_per_week` | Fixed 7-day count, not a rate — no sample-size confidence concern in the same sense |
| Override Rate | `override_rate` | Validation attempts, fixed 7-day window |
| Top Rule Breach | `top_rule_breach` | Validation attempts, `period` param (7d/30d) |
| Trade Plan Adherence | `trade_plan_adherence_rate` | All-time closed trades |

The all-time closed-trade count is also the most user-recognisable "how much history does this cover" figure, and it is a strict function already computed server-side as `trade_plan_adherence_rate`'s own denominator (`get_arc5_trade_plan_adherence_rate` in `backend/database.py`) — it was simply not exposed in the API response prior to this story.

**Reused data check (before proposing a backend change):** `PerformanceAnalytics.js` (the page hosting this section) already gates its own analytics sections on `filteredTrades.length >= settingsData.min_trades_for_analytics` (default 10). This count is *not* a valid substitute for the advisory's "N" — it is scoped to the page's selected date-range filter dropdown, whereas `trade_plan_adherence_rate` is all-time. Passing the page's filtered count down would produce a caption that doesn't describe the data actually backing the card ("Based on N trades" while N is the wrong population is worse than no caption). No existing client-side data source correctly answers "how many closed trades back these stats" — an API change is required.

**Statistical read at low N:** a ratio computed on a single-digit or low-double-digit denominator swings by large increments per additional trade (e.g. 1 override on 2 closed trades reads as a 50.0% Override Rate; the adherence-rate card behaves the same way against its own all-time denominator). The component renders these with no visual distinction from a mature-sample reading. This is a genuine display-confidence gap, not a hypothetical one — it is exactly the scenario `PerformanceAnalytics.js`'s own ≥10-trade page gate already partially guards against (below 10, the section doesn't render at all), leaving the 10–19 all-time-trade band as the window where the section renders but the confidence caveat is still warranted.

## 3. Conclusion

**Advisory warranted.** Threshold: `total_closed_trades < 20` (the AC's own "sub-20-trade states" anchor), applied to the all-time closed-trade count exposed as the new `total_closed_trades` field (`arc5_compliance_analytics.md` v1.1.0). Implemented per the locked decision record: a static, non-dismissible Info-tone banner below the four-card grid, re-evaluated on each fetch.

Scope of the caveat is intentionally the all-time count rather than a per-card per-window count — precise per-window sample sizes for the 7-day/period-scoped cards are not currently exposed by the endpoint and are out of scope for this story; the all-time count is the best available single indicator and is explicit in the copy ("Based on N closed trades") rather than implying precision it doesn't have.

## 4. Follow-up not in this story's scope

Exposing per-card sample sizes (e.g. validation-attempt counts backing `override_rate`/`top_rule_breach`) would sharpen the caveat further but requires additional backend fields beyond `total_closed_trades`. Not filed as a backlog item — the current advisory already satisfies ST-01's AC without it, and the four-window mismatch is documented in `arc5_compliance_section.md` §Low-Trade-Volume Advisory for any future reader considering this extension.

## 5. Sign-off

Metrics Definitions & Analytics Owner: confirmed, 2026-09-07.
