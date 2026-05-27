Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-27

---

**EPIC:** EPIC-03 — Feature Integration + Quality (Arc 5 P&L, Claude cost alerting, Research view signal_type, staging verification)
**Cycle:** 2026-05-26__release-v4.1
**Sprint goal:** Resolve 2nd-recurrence governance failures in the execution, planning, and verification prompts; clear API contract spec debt for four undocumented v4.0 endpoints; and deliver Arc 5 P&L integration, Gemini cost alerting, and SI-02 pre-planning artefacts to unlock position drift monitoring sprint planning.
**Test scenarios used:** tests/e2e/research-view-signal-type.spec.js (SC-ST-01 – SC-ST-04), tests/e2e/arc5-compliance-section.spec.js (SC-ARC5-01 – SC-ARC5-04), tests/test_daily_cost_alert.py (5 unit tests), code review for spec docs

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-07 | docs/specs/api_contracts/gemini_thesis_generation.md, docs/reference/openapi.yaml | AC pre-met: gemini_thesis_generation.md v2.0.0 Canonical in main (Claude Haiku 4.5, both endpoints, ## headings). Gate condition (AC-01) met — ST-04 merged. Agent-mediated sign-off cleared. | AC-01: gate met (ST-04 merged); AC-02: contract at gemini_thesis_generation.md; AC-03: ## POST /trade-plans/{plan_id}/generate-thesis at line 43; AC-04: request schema (plan_id path param), response schema ({thesis, model_version, prompt_version}), error cases all present; AC-05: openapi.yaml entries at lines 3751 and 3815; AC-06: agent-mediated sign-off cleared | Pass | None |
| ST-08 | docs/specs/metrics_definitions.md, docs/specs/frontend/pages/reports.md | metrics_definitions.md v1.10.0→v1.11.0: Arc 5 Compliance Composite Score section added with 4-term weighted formula, severity mapping table, input fields. reports.md v0.2→v0.3: Arc 5 Compliance Summary section added (collapsible, after Unrealised P&L card, data from GET /analytics/arc5-compliance, composite score fallback). | AC-01: formula in metrics_definitions.md §Arc 5 Compliance Composite Score; AC-02: formula with input fields + agent-mediated Metrics Definitions & Analytics Owner review cleared; AC-03: Arc 5 compliance section in reports.md; AC-04: fields coverage (validation_pass_rate_by_rule top 3, override_rate, events_per_week, top_rule_breach); AC-05: composite score applied if FEAT-40 formula defined, individual fallback described; AC-06: agent-mediated Financial Reporting & Records Owner review cleared | Pass | None |
| ST-09 | docs/specs/api_contracts/ai_endpoints.md (new POST /ai/check-daily-cost) | backend/config.py: AI_DAILY_COST_THRESHOLD env var (default 1.00). database.py: get_daily_ai_cost() queries gemini_audit_log. gemini_service.py: check_and_alert_daily_cost() with Telegram alerting. ai.py: POST /ai/check-daily-cost endpoint. tests/test_daily_cost_alert.py: 5 unit tests. test.py + SystemStatus.js + system-status.spec.js updated (count 57→58). conftest.py: get_daily_ai_cost added to _DB_STUB_FUNCTIONS. docs/reference/openapi.yaml updated. BLG-QA-35 filed for AC-05 staging deferral. | AC-01: threshold check with configurable env var, default $1.00/day; AC-02: queries gemini_audit_log SUM(estimated_cost_usd) for current day; AC-03: Telegram alert with daily total and request count when exceeded; AC-04: 5 unit tests cover threshold not exceeded, exceeded, exact boundary, no credentials, custom threshold | Pass | AC-05 (staging verification) deferred to v4.2 — BLG-QA-35 filed |
| ST-10 | docs/specs/frontend/pages/research_view.md, docs/specs/frontend/components/arc5_compliance_section.md | src/pages/Research.js: Setup Type div added to signal panel displaying r?.signal?.signal_type ?? '—'. research_view.md v1.1→v1.2: signal_type added to §4.2 Signal Panel table. arc5_compliance_section.md created: props, rendering conditions (loading/error/data), stat card layout, data mapping from GET /analytics/arc5-compliance, 4 cards. tests/e2e/research-view-signal-type.spec.js: 4 tests (SC-ST-01 label visible, SC-ST-02 value rendered, SC-ST-03 null→"—", SC-ST-04 no-signal no-crash). | AC-01 (FE-44): signal_type displayed as Setup Type in Research view signal panel; AC-02 (FE-44): Playwright coverage SC-ST-01 verifies column visible; AC-03 (FE-48): spec doc created at docs/specs/frontend/components/arc5_compliance_section.md; AC-04 (FE-48): spec covers props, rendering conditions, stat card layout, data mapping; AC-05 (FE-48): agent-mediated Frontend Specs & UX Documentation Owner + Head of Specs Team review cleared | Pass | None |
| ST-11 | — | AC-01: tests/e2e/arc5-compliance-section.spec.js created — 4 scenarios (heading, 4 card titles, loading skeleton, error state). ACs 02–04 staging-only: returned to backlog for v4.2 per PO discretionary deferral authority. | AC-01: SC-ARC5-01 through SC-ARC5-04 implemented; AC-02 (QA-29), AC-03 (QA-30), AC-04 (OPS-28): deferred to v4.2 — delegation DEL-20260527-01 created | Partial — AC-01 Pass; ACs 02–04 returned to backlog | None (deferral is authorized) |

**QA test coverage:**
- Scenarios run: tests/e2e/research-view-signal-type.spec.js (SC-ST-01, SC-ST-02, SC-ST-03, SC-ST-04), tests/e2e/arc5-compliance-section.spec.js (SC-ARC5-01, SC-ARC5-02, SC-ARC5-03, SC-ARC5-04), tests/test_daily_cost_alert.py (5 unit tests: threshold not exceeded, threshold exceeded, exact boundary, no credentials, custom threshold)
- Regression areas checked: Research view signal panel (no selector conflicts found via LL-v3.2-P3-02 check), PerformanceAnalytics page Arc5ComplianceSection, backend ai.py router, test endpoint suite count (57→58), SystemStatus.js fallback and SC-SS-01b e2e test
- Known deviations filed: ST-09 AC-05 staging deferral (BLG-QA-35); ST-11 ACs 02–04 staging deferral (backlog note filed, DEL-20260527-01)

**Frontend testing gate (LL-v3.1-EX-01):**
- ST-10 (FE-44) observable AC (signal_type column visible in UI): Playwright coverage → tests/e2e/research-view-signal-type.spec.js SC-ST-01, SC-ST-02 ✅
- ST-11 (QA-28) Arc5ComplianceSection observable AC: Playwright coverage → tests/e2e/arc5-compliance-section.spec.js SC-ARC5-01 through SC-ARC5-04 ✅
- No observable AC has "code review only" status — frontend gate satisfied

**Items returned to backlog:**
- ST-11 ACs 02–04: BLG-QA-28 (Arc5 staging), BLG-QA-29 (AI thesis staging), BLG-QA-30 (ticker validation staging), BLG-OPS-28 (deploy hook staging) — deferred to v4.2 per PO authority

---

## Director of Quality Sign-Off

> **Note:** Autonomous class sign-off (BLG-GOV-19) does NOT apply to EPIC-03. Criterion 1 fails (ST-11 classification: delegated_qa), Criterion 2 fails (ST-10 has observable UI AC), Criterion 3 fails (ST-10 adds signal_type column to Research view). Director of Quality review required.

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked (research view, Arc5ComplianceSection, backend cost alerting, test suite count)
- [ ] Frontend observable ACs: Playwright test coverage confirmed (ST-10 SC-ST-01/ST-02, ST-11 SC-ARC5-01 through SC-ARC5-04)
- [ ] ST-11 AC-02/03/04 staging deferral to v4.2 acknowledged (PO-authorized)
- Signed off by: _(Director of Quality — signature required before PR merge)_
- Date: _(to be completed — must be non-blank before merge gate runs)_
- Comments:
