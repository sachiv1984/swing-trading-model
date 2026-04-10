Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-04-06

---

# QA Evidence Log — EPIC-02: Backend Integration Documentation

**Cycle:** 2026-04-05__release-v2.5
**Sprint:** Sprint 2

---

## ST-04 — Review and document Reports page backend integration

**Spec references:** `src/pages/Reports.js`

**Commit:** TBD (pending)

**What was built:**
Created `docs/ops/reports_integration_review.md` mapping each section of the Reports page to its data source. Key findings:
- Tax Year P&L tab: fully wired to FastAPI backend via `GET /reports/tax-year` (JSON, PDF, CSV variants)
- Performance tab: entirely wired to Base44 SDK (`base44.entities.Position.list()`, `base44.entities.Portfolio.list()`) with all metrics computed client-side; no FastAPI backend calls
- Two integration gaps identified (GAP-R01: Performance tab bypasses FastAPI; GAP-R02: analytics endpoints unused)
- Three improvement proposals filed (P1: migrate Performance tab to FastAPI, P2: add period-filtered analytics endpoint, P3: backend export for performance reports)
- One follow-up backlog item filed: BLG-BE-08-GAP-01

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | Review document exists at `docs/ops/reports_integration_review.md`; each section mapped to endpoint or gap | Pass |
| Quality | All identified gaps have follow-up backlog item or in-scope resolution; improvement proposals recorded with priority | Pass |
| Security | N/A | N/A |
| Verification | Code review confirming all Reports.js data fetches are accounted for; document filed at canonical path | Pass — DoQ 2026-04-10 (document complete; all sections mapped; BLG-BE-08-GAP-01 filed) |

---

## ST-05 — Review and document Signals page backend integration

**Spec references:** `src/pages/Signals.js`

**Commit:** TBD (pending)

**What was built:**
Created `docs/ops/signals_integration_review.md` mapping each section of the Signals page to its data source. Key findings:
- Signals list (`GET /signals?top_n=&lookback_days=`) and market status (`GET /market/status`) are correctly wired to FastAPI backend with appropriate auto-refresh (60s and 5min respectively)
- Signal dismissal, signal-to-position conversion, and portfolio cash balance all use legacy Base44 SDK
- Three integration gaps identified (GAP-S01: mutations bypass FastAPI; GAP-S02: cash balance from Base44; GAP-S03: "already held" check uses Base44 positions)
- Three improvement proposals filed with priority ranking
- Two follow-up backlog items filed: BLG-BE-09-GAP-01, BLG-BE-09-GAP-02

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | Review document exists at `docs/ops/signals_integration_review.md`; each section mapped to endpoint or gap | Pass |
| Quality | All identified gaps have follow-up backlog item or in-scope resolution; improvement proposals recorded with priority | Pass |
| Security | N/A | N/A |
| Verification | Code review confirming all Signals.js data fetches and mutations are accounted for; document filed at canonical path | Pass — DoQ 2026-04-10 (document complete; all sections mapped; BLG-BE-09-GAP-01/02 filed) |

---

## ST-06 — Investigate high external baseline latency on DB-backed endpoints

**Spec references:** `docs/ops/api_performance_baseline.md`

**Classification:** delegated_backend — assigned to Head of Engineering

**Status:** Not started — awaiting human delegation

**Delegation record:** To be filed in `claude/cycles/2026-04-05__release-v2.5/delegation_log.md` (see EPIC-02 delegation record for ST-06)

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | Root cause of GET /portfolio and GET /notifications/preferences outliers documented; fix applied or architectural constraint documented; pooling options evaluated | Pending human (delegated) |
| Quality | Updated baseline document filed at `docs/ops/api_performance_baseline.md` if any changes made | Pending human (delegated) |
| Security | N/A | N/A |
| Verification | DoQ sign-off after Head of Engineering files findings | Pending |

---

## EPIC-02 Consolidation

**EPIC:** EPIC-02 — Backend Integration Documentation
**Cycle:** 2026-04-05__release-v2.5
**Sprint goal:** Document backend integration status for Reports and Signals pages; investigate latency outliers.
**Test scenarios used:** None (documentation/investigation stories — no functional code changes)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|-------|
| ST-04 | src/pages/Reports.js | `docs/ops/reports_integration_review.md` — section mapping, gaps, proposals | Document exists with all sections mapped; gaps have follow-up items | Pass — DoQ 2026-04-10 | None |
| ST-05 | src/pages/Signals.js | `docs/ops/signals_integration_review.md` — section mapping, gaps, proposals | Document exists with all sections mapped; gaps have follow-up items | Pass — DoQ 2026-04-10 | None |
| ST-06 | docs/ops/api_performance_baseline.md | Delegation record filed; investigation assigned to Head of Engineering | Root cause documented; pooling options evaluated | Pending human | N/A (delegated) |

**QA test coverage:**
- Scenarios run: Manual — code review of Reports.js and Signals.js; cross-reference with FastAPI routers and openapi.yaml
- Regression areas checked: No functional code changes — documentation only
- Known deviations filed: None

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (no functional code changes — documentation only; no regression risk)
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A (no frontend changes in this EPIC)
- Signed off by: Director of Quality
- Date: 2026-04-10
- Comments: ST-04 PASS. ST-05 PASS. ST-06 N/A — delegated to Head of Engineering; sign-off deferred until findings filed. Both integration review documents are complete and well-structured: all page sections mapped, gaps clearly classified by severity, improvement proposals prioritised. Three follow-up backlog items filed as a result of this review: BLG-BE-08-GAP-01 (P1 — migrate Reports Performance tab to FastAPI), BLG-BE-09-GAP-01 (P1 — wire Signals mutations to FastAPI), BLG-BE-09-GAP-02 (P2 — replace Base44 cash balance with GET /cash/summary). Both parent items (BLG-BE-08, BLG-BE-09) marked shipped v2.5. No P0 or P1 deviations in delivered scope.
