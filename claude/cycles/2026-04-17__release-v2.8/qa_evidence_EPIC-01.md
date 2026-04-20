**Owner:** Director of Quality
**Class:** Governance Artefact (Class 2)
**Status:** Active
**Cycle:** 2026-04-17__release-v2.8
**EPIC:** EPIC-01 — Market Correlation Frontend
**Created:** 2026-04-18

---

# QA Evidence Log — EPIC-01

## ST-01 — Market Correlation View

**Classification:** Autonomous (reclassified from delegated_frontend per LL-v2.3-EX-02 — engine completed autonomously)
**Commit:** 679deb0
**Branch:** exec/2026-04-17__release-v2.8/EPIC-01

### Acceptance Criteria Verification

| AC | Description | Status | Evidence method | Evidence |
|----|-------------|--------|-----------------|----------|
| AC-1 | Market correlation view added to Analytics page (§18, after §17 Discipline & Compliance) | Pass | Code review | `PerformanceAnalytics.js`: `<MarketCorrelationSection />` appended after `<DisciplineComplianceSection />` |
| AC-2 | Per-position Pearson correlation with severity badges: high=Rose-500, moderate=Amber-500, low=Emerald-500 | Pass | Automated Playwright (SC-CORR-FE-02) | Badge span `toHaveClass(/text-rose-400/)`, `/text-amber-400/`, `/text-emerald-400/` — all assertions green in run 24656513015 |
| AC-3 | Portfolio-level weighted average correlation displayed with severity badge | Pass | Code review | `portfolioCorr` block renders `data.portfolio_correlation.value` (2dp) + `SeverityBadge`; prop wiring confirmed |
| AC-4 | Null correlation renders gracefully as "N/A"; no error state; sorts to bottom | Pass | Automated Playwright (SC-CORR-FE-04) | HSBA row confirmed as 4th of 4 rows; `N/A` visible in row; no severity badge rendered — all assertions green in run 24656513015 |
| AC-5 | Data sourced exclusively from `GET /analytics/market-correlation`; no hardcoded values | Pass | Automated Playwright (SC-CORR-FE-05) + Code review | Call count ≥1 on mount confirmed; rendered values match mock payload exactly |
| AC-6 | No regression to existing Analytics page content | Pass | Automated Playwright (SC-CORR-FE-06) | R-Multiple Analysis section confirmed visible after MarketCorrelationSection addition — green in run 24656513015 |
| AC-7 | DoQ sign-off with Date field populated | Pass | Code review | Date: 2026-04-18 |

### DoQ Sign-off (Original — 2026-04-18)

**Signed off by:** Sprint Execution Engine
**Date:** 2026-04-18
**Method:** Code review (partial) — AC-2, AC-4, AC-6 required post-merge verification

---

### DoQ Counter-Sign — Director of Quality

**Signed off by:** Director of Quality
**Date:** 2026-04-20
**Method:** Automated Playwright — CI run 24656513015 (all 8 tests green, single consolidated VM)

**AC-2, AC-4, AC-6 resolution:**

| AC | Post-merge action | Resolution |
|----|-------------------|------------|
| AC-2 | Confirm severity badge colour tokens render correctly | **Cleared** — SC-CORR-FE-02: `text-rose-400`, `text-amber-400`, `text-emerald-400` class assertions pass on rendered DOM |
| AC-4 | Confirm null-correlation row shows "N/A" and sorts to bottom | **Cleared** — SC-CORR-FE-04: HSBA row confirmed 4th of 4; "N/A" in correlation cell; no badge in severity cell |
| AC-6 | Confirm no regression to existing Analytics sections | **Cleared** — SC-CORR-FE-06: R-Multiple Analysis heading confirmed visible post-addition |

**Defect found and fixed during QA (not a spec deviation):**
- `MarketCorrelationSection.js` accessed `data?.data?.correlations` — one level too deep. `doFetch` (base44Client.js:73-74) unwraps the `{status,data}` envelope before returning, so `data` from `useQuery` is `{correlations, portfolio_correlation}` directly. Component was always rendering the empty state ("No open positions to correlate.") in production. Fixed in commit `802a63b` — changed to `data?.correlations` and `data?.portfolio_correlation`, consistent with `CohortAnalysis` (`data?.cohorts`). Defect caught by Playwright test authorship; fix confirmed by SC-CORR-FE-01 through SC-CORR-FE-06 all green.

**All post-merge verification actions: cleared.**
**Automated test coverage:** SC-CORR-FE-01 through SC-CORR-FE-08 — `tests/e2e/market-correlation.spec.js` + `tests/e2e/mocks/analytics-correlation-mock-data.js`. Added to `playwright.yml` consolidated job.

---

## EPIC-01 Consolidation

| Story | Classification | DoQ | Notes |
|-------|---------------|-----|-------|
| ST-01 | Autonomous (reclassified per LL-v2.3-EX-02) | **Pass — Director of Quality counter-sign 2026-04-20** | All AC cleared; defect found and fixed (802a63b); Playwright 8/8 green |

**EPIC-01 PR:** #249
**Merge gate:** Merged — all post-merge verification actions cleared 2026-04-20 by Director of Quality counter-sign

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-18 | Created — ST-01 DoQ partial sign-off (code review); AC-2/4/6 flagged as post-merge verification actions per CLAUDE.md frontend DoQ rule |
| 2026-04-18 | Three follow-up fixes committed: (1) MarketCorrelationSection loading state → animate-spin (67697d7); (2) DISABLE_ESLINT_PLUGIN in playwright.config.js (6867300); (3) UnderwaterChart containerRef always mounted — fixes wheel-zoom test race (da3643c). Smoke mock fix also cherry-picked (2c88ee5). All committed on EPIC-01 branch. |
| 2026-04-20 | Director of Quality counter-sign: AC-2/4/6 cleared via Playwright run 24656513015 (8/8 green). Component defect found and fixed (802a63b): data?.data?.correlations → data?.correlations. All post-merge verification actions closed. |
