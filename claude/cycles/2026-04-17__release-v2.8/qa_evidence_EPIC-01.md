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
| AC-2 | Per-position Pearson correlation with severity badges: high=Rose-500, moderate=Amber-500, low=Emerald-500 | **Partial — local run required** | Code review confirms token assignment; visual rendering unverified | `SEVERITY_STYLES` map in `MarketCorrelationSection.js` assigns correct Tailwind tokens per spec; colour rendering requires browser run |
| AC-3 | Portfolio-level weighted average correlation displayed with severity badge | Pass | Code review | `portfolioCorr` block renders `data.portfolio_correlation.value` (2dp) + `SeverityBadge`; prop wiring confirmed |
| AC-4 | Null correlation renders gracefully as "N/A"; no error state; sorts to bottom | **Partial — local run required** | Code review confirms null-guard logic; null row sort and "N/A" display require live data to verify | Null guard: `row.correlation != null ? row.correlation.toFixed(2) : "N/A"`; `SEVERITY_ORDER.unknown = 3` forces bottom sort; live rendering unverified |
| AC-5 | Data sourced exclusively from `GET /analytics/market-correlation`; no hardcoded values | Pass | Code review | `api.analytics.marketCorrelation()` is the sole data source; no hardcoded correlation values in component |
| AC-6 | No regression to existing Analytics page content | **Partial — local run required** | Code review confirms no modifications to existing components or props; visual regression requires browser run | All prior `<DisciplineComplianceSection />` and earlier component usages unchanged; new component appended only |
| AC-7 | DoQ sign-off with Date field populated | Pass | Code review | Date: 2026-04-18 |

### DoQ Sign-off

**Signed off by:** Sprint Execution Engine
**Date:** 2026-04-18
**Method:** Code review (partial) — see post-merge verification actions below

**Criteria checked:**
- [x] AC-1, AC-3, AC-5, AC-7: fully verified by code review
- [ ] AC-2, AC-4, AC-6: logic verified by code review; observable UI behaviour (colour rendering, null display, regression) requires local run — listed as post-merge verification actions

**Post-merge verification actions (required before next sprint on this domain):**

| Action | AC | Owner |
|--------|-----|-------|
| Run Analytics page in browser; confirm severity badge colours match spec (high=Rose-500, moderate=Amber-500, low=Emerald-500) | AC-2 | Frontend Specifications & UX Owner |
| Confirm null-correlation position shows "N/A" and renders at bottom of table | AC-4 | Frontend Specifications & UX Owner |
| Scroll through all §1–§17 sections on Analytics page; confirm no regression | AC-6 | Frontend Specifications & UX Owner |
| QA & Testing Owner to author SC-CORR frontend scenario tests | — | QA & Testing Owner (deferred, sprint planning notes) |

**Automated test coverage:** None for this EPIC. Explicitly deferred to next sprint on this domain — see sprint_backlog.md ST-01 test scenarios gap note. This is a known gap, not an oversight.

---

## EPIC-01 Consolidation

| Story | Classification | DoQ | Notes |
|-------|---------------|-----|-------|
| ST-01 | Autonomous (reclassified per LL-v2.3-EX-02) | Partial — code review pass; AC-2/4/6 require local run post-merge | See post-merge verification actions above |

**EPIC-01 PR:** #249
**Merge gate:** Ready to merge — post-merge verification actions required before next sprint on this domain (AC-2/4/6 local run; automated tests deferred)

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-18 | Created — ST-01 DoQ partial sign-off (code review); AC-2/4/6 flagged as post-merge verification actions per CLAUDE.md frontend DoQ rule |
| 2026-04-18 | Three follow-up fixes committed: (1) MarketCorrelationSection loading state → animate-spin (67697d7); (2) DISABLE_ESLINT_PLUGIN in playwright.config.js (6867300); (3) UnderwaterChart containerRef always mounted — fixes wheel-zoom test race (da3643c). Smoke mock fix also cherry-picked (2c88ee5). All committed on EPIC-01 branch. |
