Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# QA Evidence Log — EPIC-04: Governance Documentation

**EPIC:** EPIC-04 — Governance Documentation
**Cycle:** 2026-03-04__release-v1.8
**Sprint goal:** Create lifecycle-compliant operational and API governance documents to close documentation debt from v1.7.
**Test scenarios used:** Derived from spec + AC (no dedicated scenario file — governance document creation)

---

## Per-Story Evidence

---

### ST-11 — Unavailability Failure Mode Documentation

**Spec references:** `docs/ops/unavailability_policy.md` v1.0.0

**Status:** Complete — committed to exec/2026-03-04__release-v1.8/EPIC-04

**Commit SHA:** d71aa67

**What was built:** `docs/ops/unavailability_policy.md` created at v1.0.0. Lifecycle-compliant header (Owner: Infrastructure & Operations Owner, Class: Class 1 Canonical, Status: Canonical, Version: 1.0.0, Last Updated: 2026-03-05). Document covers three failure scenarios:
1. Backend API unavailable — user action: wait/refresh, data integrity: no in-flight changes lost (read-only system)
2. Market data feed unavailable — user action: use manual price lookups, data integrity: stale prices displayed with warning
3. Partial degradation (one service down) — user action per degraded service, data integrity: healthy services continue normally

Each scenario includes user required actions and data integrity implications. `docs/ops/` directory created as part of this story.

**Deviation check:** No deviations. Document meets all AC dimensions.

---

### ST-12 — Running API Changelog Document

**Spec references:** `docs/specs/api_contracts/api_changelog.md` v1.0.0

**Status:** Complete — committed to exec/2026-03-04__release-v1.8/EPIC-04

**Commit SHA:** 1f65bc4

**What was built:** `docs/specs/api_contracts/api_changelog.md` created at v1.0.0. Lifecycle-compliant header (Owner: API Contracts & Documentation Owner, Class: Class 2 Supporting Document, Status: Active, Version: 1.0.0, Last Updated: 2026-03-05). Content:
- v1.9.0 EPIC-06 changes backfilled: `sharpe_ratio_trade_method` in analytics (analytics_endpoints.md v1.9.0), portfolio v1.9.0 field list (portfolio_endpoints.md v1.9.0), `holding_days` in trades (trade_endpoints.md v1.9.0), settings method correction (settings_endpoints.md v1.1.0)
- Maintenance obligation documented: changelog must be updated alongside every contract version bump
- Registered in `docs/specs/Specs_Index.md` §3.4

**Deviation check:** No deviations. All v1.9.0 changes backfilled; Specs_Index.md updated.

---

## EPIC-Level Consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-11 | `docs/ops/unavailability_policy.md` v1.0.0 | Lifecycle-compliant policy: 3 failure scenarios with user actions and data integrity implications | docs/ops/ created; all 3 scenarios covered; lifecycle-compliant; registered in index | Pass | None |
| ST-12 | `docs/specs/api_contracts/api_changelog.md` v1.0.0 | API changelog: v1.9.0 changes backfilled; maintenance obligation documented; Specs_Index registered | All v1.9.0 changes present; changelog maintenance obligation documented; Specs_Index.md updated | Pass | None |

**QA test coverage:**
- Scenarios run: manual acceptance review against AC (governance document creation)
- Regression areas checked: lifecycle header compliance, content completeness per AC, index registration
- Known deviations filed: None

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec — ST-11: `unavailability_policy.md` v1.0.0 spot-checked: sections 2.1 (Backend Down), 2.2 (Market Data Feed Unavailable), 2.3 (Partial Degradation) all present with user actions and data integrity implications; lifecycle header confirmed; `docs/ops/` directory created. ST-12: `api_changelog.md` v1.0.0 spot-checked: v1.9.0 section present with entries for analytics, portfolio, trade, and settings contracts; maintenance obligation section present; Specs_Index.md registration confirmed at §3.4.
- [x] No unresolved P0 or P1 deviations — no deviations filed for either story.
- [x] Regression areas checked — lifecycle header compliance verified for both documents; content completeness checked against AC for each story; Specs_Index.md registration confirmed.
- Signed off by: Director of Quality
- Date: 2026-03-05
- Comments: Clean delivery. Both items are governance documents created to spec. Lifecycle headers confirmed compliant. ST-11 note: the unavailability policy correctly reflects the system's read-only nature (no in-flight state changes to protect). ST-12 note: the changelog backfill is complete and the maintenance obligation is clearly stated. EPIC-04 QA gate: APPROVED. Recommend merge once Product Owner acceptance is confirmed on PR #30.
