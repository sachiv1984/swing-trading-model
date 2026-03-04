**Owner:** Metrics Definitions & Analytics Canonical Owner
**Class:** Planning Document (Class 4)
**Status:** Parked
**Submitted by:** Metrics Definitions & Analytics Canonical Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-metrics-analytics-20260304-02

---

# Idea: Metrics Staleness Indicator

## 1. Problem Statement

Analytics metrics are calculated and stored based on the current state of the database, but there is no indication in the UI or API response of when the last calculation was performed. If the background calculation job fails silently, or if data has not been updated for an extended period, the user could be making trading decisions based on analytics that are hours or days out of date without knowing it. A Sharpe ratio calculated on data that is 48 hours stale may lead to a decision that a current calculation would not support.

## 2. Strategic Alignment

Section reference: Metrics Definitions §5 — Data Dependency & Lineage Stewardship ("metrics fail safely and predictably; silent degradation is avoided")

Alignment rationale: The canonical requirement that metrics must not silently degrade applies directly here. A stale metric that appears current to the user is a silent degradation of analytical accuracy. Adding a staleness indicator is the mechanism for making any degradation visible rather than hidden. This is a data quality control, not a new feature.

## 3. Proposed Solution

Add a `last_calculated_utc` field to all analytics API responses (GET /analytics/*, GET /portfolio/*). Display a staleness indicator in the UI if the timestamp is older than 24 hours: a yellow warning for 24–48 hours, a red warning for >48 hours. The staleness threshold is a configuration value, not hardcoded. If `last_calculated_utc` is absent from a response (legacy endpoints), treat it as unknown and display a neutral indicator. No changes to calculation logic required.

## 4. Expected Value

Prevents trading decisions based on silently stale analytics. Reduces mean time to detect a background calculation failure from "until the user notices incorrect data" to "within the staleness threshold." Measurable as: time between a background job failure and the user seeing a staleness warning (target: ≤24 hours).

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires adding timestamp tracking to analytics calculation endpoints. Requires UI changes to display the staleness indicator. No strategy rule changes.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: Adding a display field is purely additive; removing it reverts to the current state.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Closing silent degradation in analytics is a data quality obligation, not an optional enhancement. It directly supports the "metrics fail safely and predictably" requirement.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | 🅿 Parked |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | N/A — not advanced to STEP 5 debate |
| Outcome date | N/A |
| Notes | |
