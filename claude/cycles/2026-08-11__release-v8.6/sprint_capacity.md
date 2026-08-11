**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-11
**Cycle:** 2026-08-11__release-v8.6

# Sprint Capacity — 2026-08-11__release-v8.6

## Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (workforce_capacity.md, Effective 2026-07-17); solo developer, evenings/weekends
Available FTE:      1 (solo developer; all governance roles agent-embodied over the single contributor)
Total capacity:     ~24-28 capacity-day units per sprint (confirmed band, unchanged since 2026-07-17, last re-affirmed 2026-07-28__scheduled)
Skill constraints:  None flagged — no scarce or role-locked skill identified in release_plan.md Execution Plan
```

## Item Effort Mapping

Source: `release_plan.md ## Capacity Check` (schema v2) and `stage4_backlog_slice.md` per-item effort bands. Midpoint days: M=1.75, S=1.00, XS=0.50.

| EPIC | ST | Item | Effort Band | Days |
|------|----|----|--------------|------|
| EPIC-01 | ST-01 | Trade plan completion rate tracking | S | 1.00 |
| EPIC-01 | ST-02 | AI-assisted setup thesis digest at order placement | M | 1.75 |
| EPIC-02 | ST-03 | Enforce trade-plan linkage + DB-level safeguard | M | 1.75 |
| EPIC-03 | ST-04 | Register remaining unregistered shadcn design tokens | M | 1.75 |
| EPIC-03 | ST-05 | Playwright coverage for remaining -muted call sites | S | 1.00 |
| EPIC-03 | ST-06 | Fix 6 drift instances against canonical secondary-text token | XS | 0.50 |
| EPIC-03 | ST-07 | Design decision: modal/dialog light theme | XS | 0.50 |
| EPIC-03 | ST-08 | Switch Layout.js dark-class sync to useLayoutEffect | XS | 0.50 |
| EPIC-03 | ST-09 | Correct nav exploration doc counts | S | 1.00 |
| EPIC-03 | ST-10 | Migrate CohortAnalysis.js to GET /analytics/cohort | S | 1.00 |
| EPIC-04 | ST-11 | get_regime_distribution NULL-exclusion dead code | S | 1.00 |
| EPIC-04 | ST-12 | Multi-currency cost-basis rounding consistency check | M | 1.75 |
| EPIC-04 | ST-13 | Closed-trade export completeness vs tax-year boundary | S | 1.00 |
| EPIC-04 | ST-14 | check_dependency_vuln_rescan.py failed-tool silent-pass fix | S | 1.00 |
| EPIC-05 | ST-15 | Endpoint regression test — GET /analytics/tag-performance | XS | 0.50 |
| EPIC-05 | ST-16 | Playwright coverage — AI-draft-badge clearing | S | 1.00 |
| EPIC-05 | ST-17 | Unit tests — check_dependency_vuln_rescan.py | S | 1.00 |
| EPIC-05 | ST-18 | Document one-directional fixture limitation | XS | 0.50 |
| EPIC-06 | ST-19 | Align alert-step grep with skip-guard ::error:: prefix | XS | 0.50 |
| EPIC-06 | ST-20 | Document CVE-2026-4539 ignore rationale | XS | 0.50 |
| EPIC-06 | ST-21 | Confirm dependency-vuln-rescan.yml post-merge run | XS | 0.50 |
| EPIC-06 | ST-22 | File retroactive DEV record — Layout.js fix | XS | 0.50 |
| EPIC-06 | ST-23 | shared_standards_changelog.md missing v3.27 entry | XS | 0.50 |
| EPIC-06 | ST-24 | execution_state.json deviations_filed field meaning | M | 1.75 |
| EPIC-06 | ST-25 | Annotate BLG-FE-146/BLG-FE-139 re-check | XS | 0.50 |
| EPIC-06 | ST-26 | Correct BLG-GOV-288 Acceptance Criteria text | XS | 0.50 |

All 26 items carry a defined effort estimate from `stage4_backlog_slice.md` / `release_plan.md`. No `[ESTIMATE REQUIRED]` placeholders.

### EPIC Subtotals

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 2.75 |
| EPIC-02 | 1.75 |
| EPIC-03 | 6.25 |
| EPIC-04 | 4.75 |
| EPIC-05 | 3.00 |
| EPIC-06 | 5.25 |
| **Total** | **23.75** |

## Total Effort vs Capacity

Total estimated effort: **23.75 days**. Confirmed capacity band: **~24-28 days**. Effort sits at the lower edge of the confirmed band (below the 24-day floor by 0.25 days on the most conservative reading, within the band on the reading `release_plan.md` itself certified as `PASS`). No over-allocation — all 26 candidate items proceed to `include` at STEP 3 without requiring Product Owner scope trimming.

## Conditional (Deferred)

No items are recorded `status: deferred_at_planning` with a `gate_condition` in `execution_state.json` for this cycle — no prior execution_state.json exists yet for `2026-08-11__release-v8.6` (this is the first sprint of the cycle). Not applicable; no re-invocation advisory required.

## Minimum Capacity Buffer Floor (Advisory)

`scope_effort ÷ confirmed_capacity` = 23.75 ÷ 24 (conservative lower bound) = **98.96%** — exceeds the 95% buffer-floor recommendation (§1.5). On the upper-bound reading (23.75 ÷ 28 = 84.8%) the floor is not exceeded.

**Product Owner disposition (recorded):** Proceed with full 26-item scope. This reading is consistent with, not a new risk introduced by, the explicit "use full capacity" instruction carried into this cycle from `plan release v8.6` (`cycle_summary.md`) and already certified `PASS` (not `warn`) at `release_plan.md ## Capacity Check`. No scope trim required. Standing ~5% buffer is not available this sprint on the conservative reading — accepted as a known, deliberate trade-off given the explicit full-capacity directive, not an oversight.
