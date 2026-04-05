**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.5
**Cycle:** 2026-04-05__release-v2.5
**Last Updated:** 2026-04-05

---

# v2.5 Sprint Backlog Slice — Integration Baseline, Quick Wins & Governance Debt

**Total stories:** 13
**EPICs:** 4
**Planned sprints:** 2

---

## EPIC-01: System Status Reliability

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Head of Engineering
**Sprint:** Sprint 1

> Fix the System Status page to correctly test all auth-protected endpoints and categorise all current routes. The System Status "Run Tests" button currently shows 1/17 pass rate due to missing API key forwarding — this epic makes it a reliable operational tool.

---

### ST-01 — Fix auth forwarding in POST /test/endpoints

**Maps to:** S2-01
**Backlog ref:** BLG-OPS-12
**Priority:** P2 (High)
**Effort:** XS (<1h)
**Owner:** Head of Engineering

**Description**
`backend/services/health_service.py` `test_all_endpoints()` makes internal HTTP calls without forwarding the `X-API-Key` header, causing all auth-protected endpoints to return 401. System Status "Run Tests" button shows 1/17 pass rate despite all endpoints being operational.

**Acceptance Criteria**
- [ ] `test_all_endpoints()` accepts and forwards the API key in internal calls
- [ ] `POST /test/endpoints` route extracts `X-API-Key` from the incoming request and passes it through
- [ ] All correctly implemented endpoints report "pass" when the system is healthy
- [ ] Success rate shown on System Status page reflects actual endpoint health (not 401 rejections)
- [ ] Implementation uses API key forwarding (not middleware bypass) to minimise security surface

---

### ST-02 — Sync endpoint test list with openapi.yaml

**Maps to:** S2-02
**Backlog ref:** BLG-OPS-13
**Priority:** P3 (Low)
**Effort:** XS (<1h)
**Owner:** Infrastructure & Operations Owner

**Description**
The endpoint test list in `health_service.py` was last updated for v2.2 (12 endpoints). All endpoints added in v2.3/v2.4 are not being tested, creating a structural coverage gap that worsens each sprint.

**Acceptance Criteria**
- [ ] All missing parameterless GET endpoints added to the test list: `/positions/compliance`, `/alerts/rules`, `/alerts/history`, `/notifications`, `/notifications/preferences`, `/digest/weekly`, `/analytics/cohort?period=month`, `/analytics/r-multiple-distribution`, `/analytics/compliance-metrics`, `/health/detailed`
- [ ] A comment block above the list references `docs/reference/openapi.yaml` as the source of truth
- [ ] System Status page placeholder text updated to match actual endpoint count
- [ ] Depends on: ST-01 (auth forwarding must work first for results to be meaningful)

---

### ST-03 — Fix System Status endpoint categorisation for v2.3/v2.4 routes

**Maps to:** S2-03
**Backlog ref:** BLG-FE-07
**Priority:** P4 (Low)
**Effort:** XS (<1h)
**Owner:** Frontend Engineer

**Description**
`src/pages/SystemStatus.js` `categorizeEndpoint()` does not cover `/alerts`, `/notifications`, or `/digest` routes added in v2.3/v2.4. These fall through to "Other" category.

**Acceptance Criteria**
- [ ] Alert endpoints appear under "Alerts" category in System Status Endpoint Tests panel
- [ ] Notification endpoints appear under "Notifications" category
- [ ] Digest endpoints appear under "Digest" category
- [ ] `categoryConfig` entries for "Alerts" and "Notifications" added with appropriate icons and colours
- [ ] No endpoints fall into "Other" except `/` (root) and any future unclassified additions

---

## EPIC-02: Backend Integration & Performance

**Maps to:** S2-04, S2-05, S2-06
**Owner:** Head of Engineering
**Sprint:** Sprint 2

> Review and document which sections of the Reports and Signals pages are wired to live backend endpoints vs. placeholder/hardcoded data. Investigate the root cause of high external latency on DB-backed endpoints (p50: 1.2–6.0s). Outputs are documentation and investigation findings; implementation fixes are out of scope for this epic.

---

### ST-04 — Review and document Reports page backend integration

**Maps to:** S2-04
**Backlog ref:** BLG-BE-08
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Owner:** Head of Engineering + Frontend Specifications & UX Owner

**Description**
No documentation exists mapping which Reports page components are wired to backend endpoints vs. using placeholder or hardcoded data. This makes it impossible to assess coverage or plan improvements systematically.

**Acceptance Criteria**
- [ ] A review document exists mapping each Reports page section to its backend endpoint (or flagging a missing connection)
- [ ] Document filed at a canonical or cycle-level path (e.g. `docs/ops/reports_integration_review.md` or `claude/cycles/2026-04-05__release-v2.5/reports_integration_review.md`)
- [ ] All identified integration gaps have either a follow-up backlog item filed or are addressed within this scope
- [ ] Improvement proposals recorded as a prioritised list and available for roadmap input

---

### ST-05 — Review and document Signals page backend integration

**Maps to:** S2-05
**Backlog ref:** BLG-BE-09
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Owner:** Head of Engineering + Frontend Specifications & UX Owner

**Description**
The Signals page integration state is undocumented. Some sections may render without live data. Without a review, integration gaps are invisible until a user encounters incorrect or missing data.

**Acceptance Criteria**
- [ ] A review document exists mapping each Signals page section to its backend endpoint (or flagging a missing connection)
- [ ] Document filed at a canonical or cycle-level path
- [ ] All identified integration gaps have a follow-up backlog item filed or are addressed within this scope
- [ ] Improvement proposals recorded as a prioritised list and available for roadmap input

---

### ST-06 — Investigate high external baseline latency on DB-backed endpoints

**Maps to:** S2-06
**Backlog ref:** BLG-BE-07
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Owner:** Head of Engineering

**Description**
All DB-backed endpoints show p50 response times of 1.2–6.0s from external clients. Two outliers warrant investigation: `GET /portfolio` (p50=5,979ms) and `GET /notifications/preferences` (p50=4,631ms).

**Acceptance Criteria**
- [ ] Root cause of `GET /portfolio` outlier latency identified and documented
- [ ] Root cause of `GET /notifications/preferences` outlier latency identified and documented
- [ ] Either a fix is applied bringing outliers within 2× of peer endpoint latency, OR a documented architectural constraint explains why optimisation is not feasible on free tier
- [ ] Supabase connection pooling options evaluated for Render free tier (PgBouncer, SQLAlchemy pool settings)
- [ ] Updated baseline document filed at `docs/ops/api_performance_baseline.md` if any changes made

---

## EPIC-03: Frontend & Operations Quick Wins

**Maps to:** S2-07, S2-08, S2-09
**Owner:** Frontend + Backend + Operations
**Sprint:** Sprint 2

> Bundle of independent quick wins: operational reliability (curl timeout safety), a cosmetic deviation backlog clear (gradient), and a well-scoped analytical metric (fee drag). Fee drag requires canonical spec coordination.

---

### ST-07 — Add --max-time to GitHub Actions curl calls

**Maps to:** S2-07
**Backlog ref:** BLG-OPS-11
**Priority:** P3 (Low)
**Effort:** XS (<1h)
**Owner:** Infrastructure & Operations Owner

**Description**
`alert-evaluation.yml` and `daily-snapshot.yml` both invoke `curl` with no `--max-time` flag. On Render free tier, cold starts cause silent stall periods creating confusing workflow logs.

**Acceptance Criteria**
- [ ] `--max-time 120` added to every `curl` call in `.github/workflows/alert-evaluation.yml`
- [ ] `--max-time 120` added to every `curl` call in `.github/workflows/daily-snapshot.yml`
- [ ] If service fails to respond within 120s, workflow step fails with non-zero exit code (not hanging)

---

### ST-08 — Fix Avg Slippage StatsCard gradient rendering

**Maps to:** S2-08
**Backlog ref:** BLG-FE-08
**Priority:** P3 (Low)
**Effort:** XS (<1h)
**Owner:** Frontend Engineer
**Deviation ref:** DEV-ST14-01 (P3 cosmetic — pre-accepted by Director of Quality 2026-03-20)

**Description**
The Avg Slippage StatsCard on the Reports/Slippage Tracking page renders without a gradient background. Clears the DEV-ST14-01 deviation from the backlog.

**Acceptance Criteria**
- [ ] Avg Slippage StatsCard renders with gradient background matching other StatsCard components
- [ ] No regression to functional slippage value display or colour coding
- [ ] DEV-ST14-01 deviation resolved — note resolution in `docs/testing/slippage_scenarios.md §5`

---

### ST-09 — Fee drag metric on Trade History

**Maps to:** S2-09
**Backlog ref:** BLG-FEAT-15
**Priority:** P3 (Low)
**Effort:** S (~0.5–1 day)
**Owner:** Metrics Definitions & Analytics Owner + Head of Engineering + Frontend Engineer

**Description**
Add a Fee Drag % metric (`exit_fees / gross_proceeds × 100`) as a new StatsCard ("Avg Fee Drag") and column in TradeHistoryTable. All data already stored — no schema migration required.

**Acceptance Criteria**
- [ ] `fee_drag_pct` field returned per trade in GET /trades response: `exit_fees / gross_proceeds × 100`, rounded to 2 dp
- [ ] `avg_fee_drag_pct` field returned at response envelope level: mean across all trades with gross_proceeds > 0
- [ ] "Avg Fee Drag" StatsCard visible on Trade History; displays `avg_fee_drag_pct` formatted as `+X.XX%`
- [ ] Fee Drag % column present in TradeHistoryTable; always populated (no `—` for missing data)
- [ ] `docs/specs/metrics_definitions.md` contains canonical definition of fee_drag_pct formula
- [ ] `docs/specs/frontend/pages/trade_history.md` spec updated with new column and StatsCard
- [ ] `docs/specs/api_contracts/trade_endpoints.md` updated with `fee_drag_pct` and `avg_fee_drag_pct` response fields
- [ ] `docs/reference/openapi.yaml` updated for new fields (same commit as contract update, per CLAUDE.md)
- [ ] Metric is labelled clearly as "Fee Drag %" throughout — never called "slippage"

---

## EPIC-04: Governance, Process & QA Hardening

**Maps to:** S2-10, S2-11, S2-12, S2-13
**Owner:** PMO Lead + Head of Specs Team + QA & Testing Owner
**Sprint:** Sprint 1

> Governance and process improvements: fix the batch push issue closure gap in CI, formalise the backlog placement rule, apply the two v2.4 deferred prompt patches (governance debt from post-ship closure), and create the EPIC-01 correctness test scenario gap.

---

### ST-10 — Fix governance_sync.yml batch push issue closure

**Maps to:** S2-10
**Backlog ref:** BLG-GOV-10
**Priority:** P2 (Medium)
**Effort:** XS (<1h)
**Owner:** DevOps / Infrastructure & Operations Owner

**Description**
`governance_sync.yml` uses `git log -1` to extract issue numbers, so only the last commit in a batch push closes its GitHub issue. Multi-commit pushes leave earlier issues open, requiring manual closure.

**Acceptance Criteria**
- [ ] `governance_sync.yml` updated to extract all commit messages in the push using `git log $BEFORE..$AFTER`
- [ ] Every GitHub issue referenced in the push range is closed (not just the last)
- [ ] Single-commit push behaviour unchanged
- [ ] Tested with a 2+ commit push on a test branch

---

### ST-11 — Formalise backlog entry placement standard

**Maps to:** S2-11
**Backlog ref:** BLG-GOV-12
**Priority:** P2 (Medium)
**Effort:** XS (<1h)
**Owner:** Head of Specs Team

**Description**
New backlog items have been added to session sections instead of the correct type-based sections (§1–§8). The placement rule must be enforced via the `backlog-add` skill and documented in backlog.md.

**Acceptance Criteria**
- [ ] `.claude/skills/lessons_learnt.md` has an entry for `backlog-add` recording the placement rule: new items must be appended to the correct existing type section, not a new session section
- [ ] Placement rule note visible at the top of `backlog.md` (below the standing notice)
- [ ] Future backlog-add runs append to the correct type section

---

### ST-12 — Apply v2.4 deferred governance prompt patches

**Maps to:** S2-12
**Source:** CF-2 from v2.4 lessons_learnt_closure.md (outstanding deferred patches)
**Priority:** — (governance debt)
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team

**Description**
Two prompt patches were deferred from the v2.4 post-ship closure:
1. `execution_prompt.md` — Add governance file edit reminder at STEP 8: if any §6-governed file was modified during sprint execution (including applying deferred patches), engine must append to `prompt_change_log.md` before commit.
2. `delivery_verification_prompt.md` — Before sealing `verification_report.md`, verify §9 Product Owner and Director of Quality sign-off Date fields are both non-blank. Surface for completion if blank.

**Acceptance Criteria**
- [ ] `execution_prompt.md` STEP 8 (or new §6.1 sub-note) includes: "If any §6-governed file was modified during this sprint execution run (including applying deferred patches), append to `claude/system/prompt_change_log.md` in the same session as the edit. One entry per file modified."
- [ ] `delivery_verification_prompt.md` STEP 8/9 includes a pre-seal gate: verify §9 PO and DoQ sign-off Date fields are non-blank before sealing `verification_report.md`; surface for completion if blank
- [ ] Both files version-bumped per CLAUDE.md §6 checklist
- [ ] `OPERATIONAL_GUIDE.md` §14 and relevant source prompt headers updated for both files
- [ ] `claude/system/prompt_change_log.md` entries appended for both changes in the same commit
- [ ] CF-2 carry-forward resolved

---

### ST-13 — Create test scenarios for EPIC-01 correctness fixes

**Maps to:** S2-13
**Backlog ref:** TEST-GAP-EPIC-01-v24
**Priority:** P2 (Medium)
**Effort:** S (~0.5 day)
**Owner:** QA & Testing Owner

**Description**
EPIC-01 of v2.4 shipped three correctness-critical fixes (ATR conversion, notification deduplication, stop price join) with no automated test scenarios. Regressions in these areas will only be caught at staging observation or by user reports without coverage.

**Acceptance Criteria**
- [ ] SC-ATR-01: ATR pence→GBP conversion for .L tickers authored and filed in the canonical test scenario library
- [ ] SC-DEDUP-01: Notification dispatch deduplication (same rule, same day) scenario authored
- [ ] SC-DEDUP-02: Evaluation pipeline not suppressed when dedup fires scenario authored
- [ ] SC-STOP-01: stop_price field present on analytics endpoint response for trades with known initial_stop scenario authored
- [ ] All scenarios filed in the canonical test scenario library and cross-referenced in the QA evidence file

---

## Deferred from v2.5

| Item | Reason | Target |
|------|--------|--------|
| BLG-TECH-05 Prometheus endpoint | P3; multi-user prerequisite | v3.0+ |
| BLG-FE-09 Frontend Performance Budget | P3; Skill-Silo balance | v2.6 |
| BLG-SPEC-D17 Spec Dependency Map | P3; Skill-Silo balance | v2.6 |
| BLG-GOV-08 Engine prompt compression | P3; L effort | v2.6+ |
| BLG-GOV-11 Cycle artefact inventory | P3; Skill-Silo balance | v2.6 |
| BLG-GOV-14 Governance Health Score | P3; Skill-Silo balance | v2.6 |
| BLG-FEAT-13 Feature rollout capability | P3; M effort | v2.6 |
| Hook configuration fix (Friction Item 3) | User action; not a sprint story | Before sprint execution |
