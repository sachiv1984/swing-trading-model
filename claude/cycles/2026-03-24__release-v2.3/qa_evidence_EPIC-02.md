Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-25

---

# QA Evidence Log — EPIC-02 (QA Automation Foundation)

**Cycle:** 2026-03-24__release-v2.3
**Sprint goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.
**Test scenarios:** `docs/testing/chart_interactivity_scenarios.md` (for ST-06)

---

## ST-03 — BLG-OPS-08: Staging Data Reset Script

**Spec reference:** No prior canonical spec.
**Commit:** Pending — delegated to Head of Engineering (DEL-20260325-02)
**Classification:** delegated_backend

**What was built:** *Pending delegation completion. Gates ST-04 and ST-05.*

**Acceptance criteria:**
- [ ] Script present in `scripts/` that resets staging database to clean state
- [ ] Script is idempotent — safe to run multiple times
- [ ] `--dry-run` flag shows what would be cleared without clearing
- [ ] Requires explicit confirmation before destructive operations
- [ ] Clears trades, positions, watchlist entries, alerts, notifications
- [ ] Output summary of what was cleared

**Test scenarios:** Infrastructure script — verified by running against staging and confirming clean state.

**Deviations:** *To be assessed at delivery verification.*

---

## ST-04 — BLG-QA-06: Test Data Seed Script Library

**Spec reference:** No prior canonical spec.
**Commit:** Pending — delegated to QA Lead (DEL-20260325-03; blocked on ST-03)
**Classification:** delegated_qa

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] Seeds for alerts (≥2 rules), watchlist (≥3 symbols), portfolio/trades (≥2 trades + 1 position)
- [ ] Scripts stored in `scripts/seeds/` or equivalent
- [ ] Each seed runnable independently or as a suite
- [ ] Works after `staging_reset` script has cleared the DB

**Test scenarios:** *N/A — data seeding infrastructure.*

**Deviations:** *To be assessed at delivery verification.*

---

## ST-05 — BLG-QA-05: Critical-Path Smoke Test (Playwright)

**Spec reference:** No prior canonical spec.
**Commit:** Pending — delegated to QA Lead (DEL-20260325-04; blocked on ST-03 + ST-04)
**Classification:** delegated_qa

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] 3 critical-path Playwright tests: add trade, view portfolio, view alerts
- [ ] Tests wired into CI against staging preview URL on every PR
- [ ] Playwright pass = supporting evidence for non-visual AC
- [ ] Flaky failures advisory only (do not block merge)

**Test scenarios:** The smoke tests themselves are the test scenarios.

**Deviations:** *To be assessed at delivery verification.*

---

## ST-06 — BLG-QA-01: Playwright E2E for Chart Interactivity

**Spec reference:** `docs/testing/chart_interactivity_scenarios.md`
**Commit:** Pending — delegated to QA Lead (DEL-20260325-05)
**Classification:** delegated_qa

**What was built:** *Pending delegation completion.*

**Acceptance criteria:**
- [ ] Playwright suite covers all 16 sub-scenarios (SC-CHART-IX-01 through SC-CHART-IX-06)
- [ ] CI runs tests against per-PR preview URL on every PR
- [ ] Known ST-11 bugs (zoom-out edge, tooltip %) would be caught by the suite
- [ ] Test run time < 5 minutes
- [ ] DoQ can rely on Playwright pass for non-visual AC; visual AC remain manual

**Test scenarios:** `docs/testing/chart_interactivity_scenarios.md` — all 16 sub-scenarios.

**Deviations:** *To be assessed at delivery verification.*

---

## EPIC-02 Consolidation Block

*(To be completed when all ST items are done — pending all 4 items)*

**EPIC:** EPIC-02 — QA Automation Foundation
**Cycle:** 2026-03-24__release-v2.3

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-03 | N/A | Staging data reset script | Idempotent, dry-run flag, confirmation | Pending | TBD |
| ST-04 | N/A | Test data seed scripts | Seeds for alerts/watchlist/portfolio | Pending | TBD |
| ST-05 | N/A | Critical-path Playwright smoke tests (3 paths) | Tests pass, CI wired | Pending | TBD |
| ST-06 | chart_interactivity_scenarios.md | Playwright E2E chart tests (16 sub-scenarios) | All scenarios covered, CI wired, < 5 min | Pending | TBD |

**QA sign-off block:** *(Director of Quality completes this when all 4 items are done)*
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction: confirm base URL variable exposed
- Signed off by: Director of Quality
- Date:
- Comments:
