**Owner:** Head of Engineering
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Head of Engineering
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-head-of-engineering-20260304-02

---

# Idea: API Endpoint Performance Baseline

## 1. Problem Statement

There is no documented baseline of expected API response times for key endpoints. Changes to the backend (new queries, schema migrations, increased data volume) can degrade performance without any automated detection. A `GET /portfolio/positions` endpoint that takes 2 seconds to respond instead of 200ms represents a significant user experience degradation that would only be noticed when a user explicitly reports it. In a trading system where the user checks positions daily, slow endpoints directly reduce the value and reliability of the decision-support tool.

## 2. Strategic Alignment

Section reference: Head of Engineering §5.3 — "own production readiness and system reliability; ensure effective incident response and post-incident learning"

Alignment rationale: Operational readiness requires knowing what "normal" performance looks like before degraded performance can be detected. A performance baseline is the operational foundation for reliability monitoring — without it, there is no threshold to alert against, no SLA to hold engineering accountable to, and no baseline for post-incident analysis of whether performance was already degraded before an incident.

## 3. Proposed Solution

Add a performance test step to CI that calls key endpoints (GET /portfolio/positions, POST /portfolio/size, GET /analytics/summary) with realistic test data and measures response time. Define thresholds: e.g., p95 < 500ms for read endpoints, p95 < 1000ms for calculation endpoints. Fail the CI step if a threshold is exceeded. Store the performance results as a CI artefact for trending. Document the thresholds and rationale in `docs/team_skills/engineering/performance_sla.md`.

## 4. Expected Value

Catches performance regressions before deployment. Provides a documented SLA that gives the engineering team a clear target. Expected to detect performance degradations that the current CI pipeline misses (which only tests functional correctness, not performance). Measurable as: number of performance regressions caught in CI versus in production.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires realistic test data for the CI performance test environment (not the same as production data, but representative in volume). Requires careful threshold calibration — set too tight and the test is flaky; set too loose and regressions slip through.

## 6. Reversibility

- [x] Mostly reversible — minor rework required

Reasoning: If thresholds prove to be incorrectly set, they require recalibration. No architectural lock-in.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Soon — worth debating in the next 2–3 cycles

Reasoning: Important for operational reliability but requires careful threshold design. Should follow the dependency scanning work (simpler, immediate value) and be prioritised in the next cycle.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | |
| Classification date | |
| Classified by | Product Owner |
| STEP 5 outcome | |
| Outcome date | |
| Notes | |
