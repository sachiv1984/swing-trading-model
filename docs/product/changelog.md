# Product Changelog — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-16

> This document is a human-maintained record of what was shipped in each product version and when. It records delivery milestones and notable decisions. It is not an immutable system record — for point-in-time system status reports, see `docs/operations/status_reports/`.

---

## v5.5 — SI-05 Effectiveness Review, Governance Hardening & UX Debt Clearance — 2026-06-16
Cycle: 2026-06-10__release-v5.5
Verified: Verified
Verification report: claude/cycles/2026-06-10__release-v5.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance patches: sprint_planning_prompt.md within-sprint date gate advisory (ST-01); execution_prompt.md pr_status read-after-open improvement with mandatory persist-before-halt gate (ST-02 / LL-v5.5-EX-02); qa_evidence commit discipline advisory (ST-03) | claude/system/sprint_planning_prompt.md; claude/system/execution_prompt.md |
| EPIC-02 | Trade count gate-monitoring view: GET /portfolio/gate-metrics backend endpoint + SI-05 data density progress line in Telegram digest | docs/ops/api_performance_baseline.md; claude/cycles/2026-06-10__release-v5.5/stage4_backlog_slice.md |
| EPIC-03 | API performance baseline complete: 18 endpoints measured across v2.8–v5.4; formal regression test suite baseline document produced (387 scenarios, 66 endpoints, 41 e2e specs); SI-05 user journey map authored with 2 friction findings | docs/ops/api_performance_baseline.md; docs/qa/regression_test_suite_baseline.md; docs/ux/si05_user_journey_map.md |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] sprint_planning_prompt.md within-sprint date gate advisory — BLG-GOV-116 closed
- [ST-02] execution_prompt.md pr_status read-after-open improvement — BLG-GOV-117 closed
- [ST-03] qa_evidence commit discipline advisory in execution_prompt.md — BLG-GOV-118 closed
- [ST-04] Trade count gate-monitoring view (backend) — BLG-BE-34 closed
- [ST-05] Trade data density progress tracker (frontend display) — BLG-GOV-120 closed
- [ST-06] v2.8–v4.6 endpoint performance baseline re-run (24 endpoints) — BLG-OPS-13 closed
- [ST-07] v5.1–v5.4 endpoint baseline extension — BLG-OPS-61 closed
- [ST-08] POST /digest/si05/send to api_performance_baseline.md — BLG-OPS-54 closed
- [ST-09] Formal regression test suite baseline document — BLG-QA-50 closed
- [ST-10] User journey map: SI-05 Telegram digest to app action — BLG-FE-65 closed

### Items returned to backlog
- [ST-11] Red Flag Journal visual design review pre-brief — gate 2026-06-21 not met; BLG-FE-64 remains open (eligible from 2026-06-21)
- [ST-12] SI-05 p99 production latency baseline review — gate 2026-07-04 not met; BLG-OPS-59 remains open
- [ST-13] SI-05 digest weekly cadence review — gate 2026-07-04 not met; BLG-GOV-112 remains open
- [ST-14] SI-05 digest actionability metric definition — gate 2026-07-04 not met; BLG-GOV-115 remains open

Sign-off: Product Owner — 2026-06-16
QA sign-off: Director of Quality — 2026-06-16

---

## v5.4 — Ops Monitoring, UX Debt Clearance & Governance Patches — 2026-06-10
Cycle: 2026-06-09__release-v5.4
Verified: Verified
Verification report: claude/cycles/2026-06-09__release-v5.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Add v5.3 new endpoints to api_performance_baseline.md — 5 endpoint rows with live Render measurements (GET /ai/journal-summary/history, GET /news/AAPL, GET /watchlist) | docs/ops/api_performance_baseline.md#17. v5.3 New Endpoints |
| EPIC-02 | Pre-entry panel: separate warn/fail override acknowledgement flow — UX spec document produced | docs/product/ux/pre_entry_override_ux_spec.md |
| EPIC-03 | SI-05 Phase 2 activation criteria definition — governance doc produced, PO-approved | docs/governance/si05_phase2_activation_criteria.md |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] Add v5.3 new endpoints to api_performance_baseline.md — BLG-OPS-60 closed
- [ST-04] SI-05 Phase 2 activation criteria definition — BLG-GOV-92 closed

### Items returned to backlog
- [ST-03] RFJ visual design review pre-brief — returned; date gate (SI-03 live ≥30 days; 2026-06-21) not met; BLG-FE-64 remains open

Sign-off: Product Owner — 2026-06-10
QA sign-off: Director of Quality — 2026-06-10

---

## v5.3 — Spec Debt, Security Hardening & Ops Governance — 2026-06-09
Cycle: 2026-06-08__release-v5.3
Verified: Verified
Verification report: claude/cycles/2026-06-08__release-v5.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | API contract spec debt resolution: BLG-SPEC-53 — contract gap resolution plan; BLG-SPEC-54 — openapi.yaml completeness audit (50 routes); BLG-QA-51 — QA acceptance criteria template for SPEC-49–52; BLG-SPEC-49 — GET /ai/journal-summary/history contract; BLG-SPEC-50 — GET /analytics/compliance-metrics contract; BLG-SPEC-51 — GET /news/{ticker} contract; BLG-SPEC-52 — Watchlist endpoint contracts + test.py. All 6 known API contract gaps closed. | docs/specs/api_contracts/ai_endpoints.md; docs/specs/api_contracts/analytics_endpoints.md; docs/specs/api_contracts/news_endpoints.md; docs/specs/api_contracts/watchlist_endpoints.md; docs/reference/openapi.yaml; docs/qa/endpoint_contract_qa_criteria_template.md |
| EPIC-02 | Security hardening: BLG-BE-35 — POST /digest/si05/send API key authentication implemented; BLG-OPS-57 — SI-05 Telegram delivery failure alerting; BLG-OPS-58 — CI secret scanning gate (gitleaks). | docs/specs/api_contracts/digest_endpoints.md; docs/operations/deployment_runbook.md; .github/workflows/secret-scanning.yml; .gitleaks.toml |
| EPIC-03 | Governance patches and AI policy: LL-v5.2-P4-01 — qa_evidence_template.md signer format note; LL-v5.2-P4-02 — execution_prompt.md STEP 5.3A SSR sub-step; BLG-GOV-107 — SI-02 frontend activation criteria precision; BLG-GOV-108 — AI model pin update policy; BLG-GOV-109 — AI audit log retention policy; BLG-GOV-110 — Arc 4 trade_plan data completeness audit; BLG-GOV-104 — strategy_rules.md §11 parameter validation; BLG-GOV-113 — SI-05 effectiveness review protocol; BLG-GOV-114 — si05_digest_log schema validation. | claude/system/templates/qa_evidence_template.md; claude/system/execution_prompt.md; claude/roadmap/current_roadmap.md; docs/governance/ai_model_version_pinning_policy.md; docs/governance/ai_audit_log_retention_policy.md; docs/governance/arc4_trade_plan_data_completeness_audit.md; docs/governance/strategy_parameter_validation_v53.md; docs/governance/si05_effectiveness_review_protocol.md; docs/governance/si05_digest_log_schema_validation.md |
| EPIC-04 | QA coverage and UX review: BLG-QA-52 — Tax year P&L boundary edge case validation (6 test scenarios); BLG-QA-53 — SI-05 digest Playwright E2E coverage (4 scenarios); BLG-QA-54 — Playwright coverage matrix update post-v5.2; BLG-FE-66 — Red Flag Journal post-launch UX review; BLG-FE-67 — BLG-FE-64 visual design review scope definition. | tests/test_tax_year_pnl_boundary.py; tests/e2e/si05-digest-delivery.spec.js; docs/qa/playwright_coverage_matrix.md; docs/governance/rfj_ux_review_v53.md; docs/governance/blg_fe_64_scope_definition.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-SPEC-53 — API contract gap resolution plan
- [ST-02] BLG-SPEC-54 — openapi.yaml completeness audit
- [ST-03] BLG-QA-51 — QA acceptance criteria for SPEC-49–52
- [ST-04] BLG-SPEC-49 — GET /ai/journal-summary/history contract
- [ST-05] BLG-SPEC-50 — GET /analytics/compliance-metrics contract
- [ST-06] BLG-SPEC-51 — GET /news/{ticker} contract
- [ST-07] BLG-SPEC-52 — Watchlist endpoint contracts + test.py
- [ST-08] BLG-BE-35 — POST /digest/si05/send API key authentication
- [ST-09] BLG-OPS-57 — SI-05 Telegram delivery failure alerting
- [ST-10] BLG-OPS-58 — CI secret scanning gate
- [ST-11] LL-v5.2-P4-01 — qa_evidence_template.md signer format note
- [ST-12] LL-v5.2-P4-02 — execution_prompt.md STEP 5.3A SSR sub-step
- [ST-13] BLG-GOV-107 — SI-02 frontend activation criteria precision (roadmap annotation)
- [ST-14] BLG-GOV-108 — AI model pin update policy
- [ST-15] BLG-GOV-109 — AI audit log retention policy
- [ST-16] BLG-GOV-110 — Arc 4 trade_plan data completeness audit
- [ST-17] BLG-GOV-104 — strategy_rules.md §11 parameter validation
- [ST-18] BLG-QA-52 — Tax year P&L boundary edge case validation
- [ST-19] BLG-QA-53 — SI-05 digest Playwright E2E coverage
- [ST-20] BLG-QA-54 — Playwright coverage matrix update post-v5.2
- [ST-21] BLG-FE-66 — Red Flag Journal post-launch UX review
- [ST-22] BLG-FE-67 — BLG-FE-64 visual design review scope definition
- [ST-23] BLG-GOV-113 — SI-05 effectiveness review protocol
- [ST-24] BLG-GOV-114 — si05_digest_log schema validation

Sign-off: Product Owner — 2026-06-09
QA sign-off: Director of Quality — 2026-06-09

---

## v5.2 — Governance Debt, SI-05 Ops & Spec Compliance — 2026-06-08
Cycle: 2026-06-08__release-v5.2
Verified: Verified
Verification report: claude/cycles/2026-06-08__release-v5.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance patches: OA-01 — release_planning_prompt.md v2.33→v2.34 §-1.2 STEP 8.1 Option(b) path added; OA-02 — execution_prompt.md v3.36→v3.37 §3.1.A step 2c test-authoring spec_references guidance; BLG-SPEC-47 resolved — DEV-v51-EPIC01-01 closed, Option(a) pass_rate computation documented, si05-telegram-message-format-spec.md updated; BLG-SPEC-48 — digest_endpoints.md v0.2→v0.3 authentication requirements section added. | claude/system/release_planning_prompt.md v2.34; claude/system/execution_prompt.md v3.37; docs/specs/api_contracts/digest_endpoints.md v0.3; docs/product/decisions/si05-telegram-message-format-spec.md |
| EPIC-02 | SI-05 operational hardening: BLG-BE-32 — Telegram retry (max 2 retries, 30s/60s backoff; ERROR logging; 3 new unit tests; injectable sleep for CI); BLG-BE-33 — si05_digest_log table (schema: id, sent_at, status, event_count, telegram_message_id, error_message, created_at; CREATE TABLE IF NOT EXISTS guard; log rows on both paths; registered in main.py on_startup()); BLG-OPS-55 — production deployment runbook §6 (SI-05 env vars, cron schedule, failure detection, health check; v0.1→v0.2); BLG-OPS-56 — SI-05 health check procedure (3 check options; escalation path; weekly cadence). | backend/services/si05_digest_service.py; docs/specs/api_contracts/digest_endpoints.md; docs/ops/production_deployment_runbook.md v0.2; docs/ops/si05_health_check_procedure.md |
| EPIC-03 | Security reviews: BLG-GOV-97 — Claude API model deprecation check (PASS; claude-haiku-4-5-20251001 current; next review 2026-09-08); BLG-GOV-98 — Telegram bot token minimal-permission review (PASS with recommendation: send-only confirmed; BotFather manual check recommended); BLG-GOV-99 — digest endpoint authentication review (GAP_FOUND: POST /digest/si05/send unauthenticated; BLG-BE-35 P2 filed); BLG-GOV-100 — backend endpoint coverage audit (50 routes enumerated; 6 contract gaps; BLG-SPEC-49/50/51/52 filed). | docs/governance/ai_model_deprecation_check_v52.md; docs/security/security_register.md; docs/ops/endpoint_coverage_audit_v52.md |
| EPIC-04 | QA governance: BLG-QA-46 — SI-05 edge case gap analysis + 2 new tests (connection failure, message truncation; 26 tests total passing); BLG-QA-47 + BLG-GOV-94 — SI-05 Phase 1 acceptance test protocol + delivery verification protocol docs; BLG-QA-48 — regression baseline refresh (POST /digest/si05/send in test.py confirmed; 5 Playwright scenarios confirmed; BLG-QA-50 formal baseline doc filed); BLG-GOV-96 — SI-05 effectiveness measurement criteria (3 criteria; 30-day review 2026-07-04). | tests/test_si05_digest_service.py; backend/routers/test.py; docs/qa/si05_edge_case_gap_analysis.md; docs/qa/si05_acceptance_test_protocol.md; docs/qa/si05_delivery_verification_protocol.md; docs/qa/regression_baseline_refresh_v51.md; claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] OA-01 — release_planning_prompt.md §-1.2 STEP 8.1 Option(b) accommodation patch (v2.33→v2.34)
- [ST-02] OA-02 — execution_prompt.md §3.1.A test-authoring spec_references guidance (v3.36→v3.37)
- [ST-03] BLG-SPEC-47 — SI-05 pass_rate computation aligned with BLG-GOV-86 §5.2; DEV-v51-EPIC01-01 resolved
- [ST-04] BLG-SPEC-48 — POST /digest/si05/send API contract gap check and authoring (digest_endpoints.md v0.3)
- [ST-05] BLG-BE-32 — SI-05 Telegram delivery retry and failure handling (30s/60s backoff; ERROR logging; unit tests)
- [ST-06] BLG-BE-33 — SI-05 digest delivery log table (si05_digest_log) — Data Model Owner sign-off
- [ST-07] BLG-OPS-55 — Deployment runbook update for SI-05 operational environment (v0.1→v0.2)
- [ST-08] BLG-OPS-56 — SI-05 service scheduled run health check procedure
- [ST-09] BLG-GOV-97 — Claude API model deprecation compliance check (PASS; next review 2026-09-08)
- [ST-10] BLG-GOV-98 — Telegram bot token minimal-permission security review (PASS with recommendation)
- [ST-11] BLG-GOV-99 — SI-05 digest endpoint authentication review (GAP_FOUND: BLG-BE-35 P2 filed)
- [ST-12] BLG-GOV-100 — Backend endpoint documentation coverage audit post-v5.1 (50 routes; 6 gaps filed)
- [ST-13] BLG-QA-46 — SI-05 digest service edge case test gap analysis (2 new tests; 26 total passing)
- [ST-14] BLG-QA-47 + BLG-GOV-94 — SI-05 Phase 1 acceptance test protocol and delivery verification protocol
- [ST-15] BLG-QA-48 — Regression test suite baseline refresh post-v5.1
- [ST-16] BLG-GOV-96 — SI-05 Phase 1 effectiveness measurement criteria (30-day review 2026-07-04)

Sign-off: Product Owner — 2026-06-08
QA sign-off: Director of Quality — 2026-06-08

---

## v5.1 — SI-05 Phase 1 & Governance Debt — 2026-06-04
Cycle: 2026-06-21__release-v5.1
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-06-21__release-v5.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-05 Phase 1 — Weekly Strategy Integrity Digest via Telegram. BLG-GOV-67 delivered: `backend/services/si05_digest_service.py`; `POST /digest/si05/send` endpoint (openapi.yaml updated); 21 unit tests; SI-05 financial reporting scope verified as OUT OF SCOPE for Phase 1 (BLG-SPEC-45 resolved). | docs/product/decisions/si05-telegram-message-format-spec.md (Known Deviations section added); docs/specs/api_contracts/arc5_compliance_analytics.md; docs/specs/api_contracts/digest_endpoints.md |
| EPIC-02 | Governance patch — `delivery_verification_prompt.md` §-1.3 Tier 2: explicit acceptance of agent-mediated signer format added (v2.9→v3.0). Resolves v5.0 Phase 4 Tier 2 advisory (LL-RP-v5.0-D-2). | claude/system/delivery_verification_prompt.md v3.0 |
| EPIC-03 | QA & documentation debt: BLG-FE-61 — SignalCard `allocation_insufficient` badge Playwright E2E coverage (5 scenarios, SC-SIG-AI-01/02/03); BLG-QA-43 — `compliance_summary` field population validation by code review; BLG-GOV-89 — staged verification sprint protocol document v1.0. | docs/operations/staged_verification_sprint_protocol.md v1.0; docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl |

### Deviations accepted
1 minor deviation — see verification_report.md

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-v51-EPIC01-01 | P3 | `pass_rate` computation uses volume-weighted overall rate instead of mean-of-per-rule-rates per BLG-GOV-86 §5.2; `digest_endpoints.md` v0.2 documents "Overall pass/total ratio" creating spec-to-spec inconsistency with BLG-GOV-86 §5.2. BLG-SPEC-47 filed for resolution before next SI-05 feature increment. | PO |

### Tech backlog items shipped
- [ST-01] BLG-GOV-67 — SI-05 Phase 1 backend service + Telegram weekly digest implementation
- [ST-02] BLG-SPEC-45 — SI-05 financial reporting scope verification (confirmed OUT OF SCOPE for Phase 1)
- [ST-03] LL-RP-v5.0-D-2 — delivery_verification_prompt.md §-1.3 Tier 2 agent-mediated signer format acceptance (v2.9→v3.0)
- [ST-04] BLG-FE-61 — SignalCard allocation_insufficient badge Playwright E2E coverage (5 scenarios)
- [ST-05] BLG-QA-43 — compliance_summary field population validation
- [ST-06] BLG-GOV-89 — Staged verification sprint protocol document v1.0

Sign-off: Product Owner — 2026-06-21
QA sign-off: Director of Quality — 2026-06-21

---

## v5.0 — Governance Hardening, Product Correctness & SI-05 Pre-work — 2026-06-03
Cycle: 2026-06-03__release-v5.0
Verified: Verified
Verification report: claude/cycles/2026-06-03__release-v5.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance Document Patches — prompt_change_log.md verified complete (all 7 BLG-GOV-79 entries confirmed present; AUD-001 gap closed); 5 non-standard agent file headers corrected (ATX heading; trailing backslash removed): ai_compliance_governance_officer.md, cybersecurity_trust_lead.md, director_of_hr.md, financial_reporting_records_owner.md, finops_resource_architect.md; PR template updated with explicit "Product Owner Acceptance (Hard Gate)" section + GitHub Approve instruction (v1.2→v1.3) | claude/system/prompt_change_log.md; claude/agents/ (5 files); .github/pull_request_template.md |
| EPIC-02 | Governance Engine Structural Fixes — execution_prompt.md STEP 8 structural governance file edit check added (git-diff scan replaces operator memory; v3.35→v3.36; root-cause fix for BLG-GOV-79/80 pattern); post-ship audit advisory strengthened (dual-condition: % 3 == 0 OR gap ≥ 4, null-safe); last_audit_cycle_count field added to .claude_current_state.json and lifecycle_schema.json; post_ship_closure.md v2.12→v2.13 | claude/system/execution_prompt.md v3.36; docs/reference/OPERATIONAL_GUIDE.md; claude/system/post_ship_closure.md v2.13; claude/system/schemas/lifecycle_schema.json |
| EPIC-03 | Product Correctness Fixes & Ops Verification — allocation_insufficient signal status: new backend status value + reason field when price_gbp > allocation_gbp; frontend SignalCard orange "Cannot Size" badge + reason inline; openapi.yaml, test.py, SC-SS-01b updated; pre-entry regime gate fix: shared 5-min cache in check_market_regime() eliminates independent yf.download (all callers share one result per window); unit tests covering cache hit/miss added; Anthropic SDK (0.40.0 → 0.105.2) staging verification complete | docs/specs/api_contracts/signal_endpoints.md; docs/specs/api_contracts/pre_entry_validation.md; docs/specs/api_contracts/ai_thesis_generation.md; docs/specs/api_contracts/ai_endpoints.md |
| EPIC-04 | SI-05 Phase 1 Pre-work Documentation Suite — SI-05 notification channel trade-off doc + PO decision (Telegram confirmed); SI-05 Telegram message format spec v1.0 (section structure, data bindings GET /analytics/arc5-compliance, character budget ~265/4096, failure modes); SI-02 re-entry trigger criteria (hard gate ≥20 closed trades, soft advisory ≥3 months, PMO check from v5.1); SI-04 §13 binding conditions formal decisions document (all 6 conditions; Strategy Rules & System Intent Owner sign-off); SI-02 drift summary feasibility assessment (feasible with conditions; 3 UX risks + mitigations) | docs/product/decisions/si05-notification-channel-tradeoff.md; docs/product/decisions/si05-telegram-message-format-spec.md; docs/product/decisions/si02-reentry-trigger-criteria.md; docs/product/decisions/decisions--2026-06-03__release-v5.0--SI-04-binding-conditions.md; docs/product/decisions/si02-drift-summary-feasibility-assessment.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-79 — prompt_change_log.md: all 7 missing entries verified present (AUD-001 closed)
- [ST-02] BLG-GOV-81 — 5 agent file header corrections (ATX heading; no trailing backslash)
- [ST-03] BLG-GOV-83 — PR template: PO acceptance = GitHub Approve instruction added
- [ST-04] BLG-GOV-80 — execution_prompt.md STEP 8 structural governance check (v3.35→v3.36)
- [ST-05] BLG-GOV-82 — post-ship audit advisory dual-condition + last_audit_cycle_count schema (v2.12→v2.13)
- [ST-06] BLG-FEAT-43 — allocation_insufficient signal status + reason field + frontend badge (openapi.yaml + test.py updated)
- [ST-07] BLG-BE-25 — pre-entry regime gate fix: shared market status cache (5-min TTL; unit tests added)
- [ST-08] BLG-OPS-52 — Anthropic SDK 0.40.0 → 0.105.2 staging verification (POST /generate-thesis + POST /ai/check-daily-cost confirmed)
- [ST-09] BLG-FE-60 — SI-05 notification channel trade-off + PO decision (Telegram confirmed)
- [ST-10] BLG-GOV-86 — SI-05 Telegram message format specification v1.0
- [ST-11] BLG-GOV-87 — SI-02 re-entry trigger criteria definition
- [ST-12] BLG-GOV-88 — SI-04 §13 binding conditions formal decisions document
- [ST-13] BLG-BE-26 — SI-02 drift summary feasibility assessment

Sign-off: Product Owner — 2026-06-03
QA sign-off: Sprint Execution Engine (autonomous class) — 2026-06-03

---

## v4.9 — Security/CI Hardening & SI-05 Phase 1 — 2026-06-02
Cycle: 2026-06-02__release-v4.9
Verified: Verified
Verification report: claude/cycles/2026-06-02__release-v4.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Security & Dependency Hardening — 21 npm HIGH CVEs cleared via npm audit fix + overrides; 6 moderate remain (CRA chain, non-production) (ST-01); Anthropic Python SDK upgraded 0.40.0 → 0.105.2; Messages API changelog reviewed, no breaking changes; AC-04 staging validation deferred post-merge per BLG-OPS-52 (ST-02) | docs/security/security_register.md (Audit 001; Upgrade 001) |
| EPIC-02 | CI/QA Infrastructure Strengthening — Real Postgres service container (postgres:15) wired to Phase B CI; DATABASE_URL injected; 13 pre-existing Phase B test isolation failures surfaced and fixed; Phase A unaffected (ST-03); Schema lifecycle column smoke tests created in tests/test_schema.py: assert positions table has position_state, state_entered_at, state_history; skips in Phase A (stub), passes in Phase B (ST-04) | .github/workflows/ci-tests.yml; tests/test_schema.py |
| EPIC-03 | Governance Debt Clearance — roadmap_prompt.md STEP 8.1 converted from advisory-only to soft gate requiring explicit PO decision when Now horizon empty; both options documented with example formats (add section now / defer with rationale); OPERATIONAL_GUIDE.md v4.25→v4.26 (ST-05) | claude/system/roadmap_prompt.md v6.8; claude/system/OPERATIONAL_GUIDE.md v4.26; claude/system/prompt_change_log.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-OPS-49 — npm devDependency HIGH CVE remediation (21 HIGH CVEs cleared; docs/security/security_register.md Audit 001)
- [ST-02] BLG-OPS-50 — Anthropic SDK upgrade 0.40.0 → 0.105.2 (docs/security/security_register.md Upgrade 001; AC-04 staging deferred: BLG-OPS-52)
- [ST-03] BLG-QA-40 — Wire Phase B CI with real Postgres service (.github/workflows/ci-tests.yml; 13 pre-existing failures fixed)
- [ST-04] BLG-QA-41 — Schema smoke test: lifecycle columns on positions table (tests/test_schema.py)
- [ST-05] BLG-GOV-78 — roadmap_prompt.md STEP 8.1 gate strengthening (v6.7→v6.8; OPERATIONAL_GUIDE.md v4.25→v4.26)

Sign-off: Product Owner — 2026-06-02
QA sign-off: Director of Quality — 2026-06-02

---

## v4.8 — Governance Hardening, Ops/Security Debt & SI-05 Phase 1 — 2026-06-02
Cycle: 2026-06-01__release-v4.8
Verified: Verified
Verification report: claude/cycles/2026-06-01__release-v4.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance & Compliance Hardening — §14 self-metadata Version corrected 4.20→4.24; §13 and §14 entries for all 7 Class 6 prompts verified present (ST-01); agent charter **Role:** header format verified compliant across all 23 agent files — pre-met in v4.5 EPIC-02 ST-05 (ST-02); all 3 v4.4 deferred patches confirmed resolved in v4.5 — AUD-2026-05-30-006 gap formally closed (ST-03). Sprint close governance patch: execution_prompt.md v3.34→v3.35 (LL-v4.8-EX-01 — commit SHA record immediately after push). | claude/system/OPERATIONAL_GUIDE.md v4.25; claude/system/prompt_change_log.md; claude/system/execution_prompt.md v3.35 |
| EPIC-02 | Operations, Security & QA Debt — Build minutes monitoring policy created (docs/operations/build_minutes_monitoring_policy.md v1.0): monthly allocation 400 min, 80% threshold, billing reset, double-capacity assessment (ST-04); dependency audit complete (docs/security/security_register.md v1.0): pip clean, 45 npm vulns (21 HIGH devDep); BLG-OPS-49/50 filed (ST-05); coverage matrix updated with compliance_summary regression point; GET /reports/monthly-pnl v0.6 contract verified (ST-06); SI-04 strategy version comparison endpoint contract pre-authored (docs/specs/api_contracts/strategy_version_comparison_contract.md v0.1.0; placeholder in openapi.yaml — ST-07). | docs/operations/build_minutes_monitoring_policy.md v1.0; docs/security/security_register.md v1.0; docs/qa/playwright_coverage_matrix.md v1.1; docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl (v0.6 confirmed); docs/specs/api_contracts/strategy_version_comparison_contract.md v0.1.0; docs/reference/openapi.yaml |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-69: §13 register completion — OPERATIONAL_GUIDE.md §14 updated; all 7 Class 6 prompts verified in §13 and §14
- [ST-02] BLG-GOV-70: Agent charter header compliance remediation — pre-met in v4.5; verified resolved across all 23 agent files
- [ST-03] BLG-GOV-72: AUD-2026-05-30-006 gap resolution verification — all 3 v4.4 deferred patches confirmed resolved in v4.5; gap formally closed
- [ST-04] BLG-OPS-46: Build minutes monitoring policy — docs/operations/build_minutes_monitoring_policy.md v1.0 created
- [ST-05] BLG-OPS-47: Dependency audit post-v4.7 — docs/security/security_register.md v1.0; BLG-OPS-49/50 filed
- [ST-06] BLG-QA-39: Coverage matrix update and v4.7 contract verification — docs/qa/playwright_coverage_matrix.md v1.1; GET /reports/monthly-pnl v0.6 verified
- [ST-07] BLG-SPEC-43: SI-04 strategy version comparison endpoint contract — strategy_version_comparison_contract.md v0.1.0 created; placeholder in openapi.yaml

Sign-off: Product Owner (agent-mediated) — 2026-06-02
QA sign-off: Director of Quality (agent-mediated) — 2026-06-02

---

## v4.7 — Arc 5 Completion Pre-work, Staged Verifications & Aged Backlog Clearance — 2026-06-01
Cycle: 2026-05-31__release-v4.7
Verified: Verified
Verification report: claude/cycles/2026-05-31__release-v4.7/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-04 §13 Formal Pre-Assessment — §13 review applied; determination PASS; 6 binding conditions documented; Arc 5 completion path cleared (ST-01) | docs/product/decisions/si04_section13_preassessment.md (new) |
| EPIC-02 | Arc 5 Compliance Score in Monthly P&L Report — compliance_summary field (validation_pass_rate, override_count, red_flag_events_count, most_frequent_rule_breach) added to GET /reports/monthly-pnl; field renamed strategy_compliance → compliance_summary; 2 unit tests + SC-REP-05a/05b Playwright scenarios (ST-03) | docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl (v0.6); docs/reference/openapi.yaml |
| EPIC-03 | Staging Verifications & Ops Housekeeping — RENDER_STAGING_DEPLOY_HOOK confirmed; code-change deploy and docs-only filter verified (ST-04); all 5 DS-07 SI-02 columns and 3 indexes confirmed on staging (ST-05); severity column, default assignment, backfill confirmed (ST-06); Render 7-day log retention documented; database audit tables confirmed durable (ST-07) | docs/ops/staging_deploy_verification.md; docs/ops/ds07_migration_staging_verification.md; docs/ops/severity_field_staging_verification.md; docs/specs/data_model.md; docs/ops/render_log_retention_policy.md |
| EPIC-04 | Cost & UX Assessments — no Anthropic API tier upgrade required; $5/month trigger threshold defined (ST-08); PreEntryValidationPanel UX reviewed; 3 improvement candidates ranked; BLG-FE-56/57/58 filed (ST-09) | docs/ops/anthropic_api_tier_assessment.md; docs/product/ux/pre_entry_panel_ux_assessment.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] SI-04 §13 Formal Pre-Assessment (BLG-GOV-62) — §13 gate PASS; Arc 5 SI-04 sprint planning now unblocked
- [ST-03] Arc 5 Compliance Score in Monthly P&L (BLG-FEAT-38) — additive compliance_summary section in monthly P&L report; aged 3+ cycles
- [ST-04] Staging Deploy Live Verification (BLG-OPS-28) — Render staging deploy workflow confirmed end-to-end; aged 4+ cycles
- [ST-05] DS-07 Migration Staging Verification (BLG-OPS-44) — v4.6 staging debt closed; all SI-02 schema changes confirmed on staging
- [ST-06] Severity Field Staging Verification (BLG-OPS-45) — v4.6 staging debt closed; severity column confirmed with correct backfill
- [ST-07] Render Log Retention Policy (BLG-OPS-31) — policy documented; database tables sufficient; no additional archiving required
- [ST-08] Anthropic API Tier Cost Assessment (BLG-OPS-37) — cost threshold defined; free tier adequate at current usage
- [ST-09] Pre-Entry Validation Panel UX Assessment (BLG-FE-49) — 3 UX improvement candidates filed as BLG-FE-56/57/58

Sign-off: Product Owner — 2026-06-01
QA sign-off: Director of Quality — 2026-06-01

---

## v4.6 — SI-02 Behavioural Drift Detection & Arc 5 Completion — 2026-05-31
Cycle: 2026-05-30__release-v4.6
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-30__release-v4.6/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-02 Behavioural Drift Detection (Backend) — DS-07 data migration adding 5 SI-02 columns to trade_plans (ST-01); POST /trade-plans updated to capture 5 new SI-02 fields at plan creation (ST-02); 4-metric behavioural drift service (entry_timing_drift, sizing_adherence, consecutive_loss_sizing, regime_context; 90-day window; green/amber/red bands; §13 binding conditions enforced; ST-03); GET /analytics/behavioural-drift endpoint, openapi.yaml, and API contract (60 total endpoints; ST-04); 35-case SI-02 unit test suite (ST-05). | docs/specs/data_model/si02_data_schema.md; docs/specs/metrics/si02_drift_score.md; docs/specs/api_contracts/behavioural_drift_contract.md; docs/reference/openapi.yaml |
| EPIC-03 | Arc 5 Enablers & Gate-Cleared Items — red_flag_events severity field added (backfill + filter support; AC-08 Data Model sign-off accepted at EPIC level; ST-09); Arc 5 hosting cost projection assessment (current Render Starter tier adequate; no upgrade required at <50 trades; ST-10); Arc 5 nav cohesion review (maintain current structure; no changes recommended; ST-11); Red Flag Journal design review scope document (gate: 2026-06-21; ST-12). | docs/specs/api_contracts/portfolio_endpoints.md; docs/reference/openapi.yaml; docs/ops/arc5_hosting_cost_projection.md; docs/specs/frontend/arc5_nav_cohesion_review_v4.6.md; docs/specs/fe/rfj_design_review_scope.md |
| EPIC-04 | Governance, Spec Debt & OA Resolution — System_status_report.md v4.4 stale status correction (OA-01; ST-14); release_planning_prompt.md v2.33 gate scan + data density checkpoint (BLG-GOV-32/43; ST-15); closed trade count audit confirming data density gate NOT MET — 6 closed trades, 0 linked trade_plans (gate ≥20; EPIC-02 deferred 6th time; BLG-GOV-33; ST-16); Arc 4 data density risk trajectory assessment — Option A selected, gate dates ~Nov 2026 (SI-02), ~Sep 2026 (PT-04), ~Jun 2027 (PT-04 full; BLG-GOV-34; ST-17); Arc 6 Monte Carlo §13 pre-assessment — PASS with 10 binding conditions (BLG-GOV-45; ST-18); trade plan schema audit — 25 fields, 0 orphaned, 3 P3 process gaps (BLG-GOV-52; ST-19); sprint close automation investigation — workflow functioning as designed, no fix required (BLG-GOV-41; ST-20); external API integration spec template created (BLG-SPEC-32; ST-21); roadmap_prompt.md v6.7 next_release advisory added (OA-02; ST-22). | claude/system/release_planning_prompt.md v2.33; claude/system/roadmap_prompt.md v6.7; docs/product/decisions/arc4_data_density_trajectory_v4.6.md; docs/product/decisions/arc6_ps03_section13_preassessment.md; docs/specs/data_model/trade_plan_schema_audit_v4.6.md; docs/ops/sprint_close_reminder_investigation_v4.6.md; docs/specs/api_contracts/_external_api_template.md |

### Deviations accepted
2 minor deviations — see verification_report.md

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-DV4.6-01 | P3 | DS-07 migration staging verification pending — 5 SI-02 columns and 3 indexes not yet verified in staging environment; code-review verified; idempotent migration | DoQ + PO |
| DEV-DV4.6-02 | P3 | red_flag_events severity field staging ACs (AC-01/02/03) and AC-08 Data Model sign-off pending; code-review verified; idempotent migration pattern | DoQ + PO |

### Tech backlog items shipped
- [ST-15] BLG-GOV-32 + BLG-GOV-43: release_planning_prompt.md gate scan + data density checkpoint
- [ST-16] BLG-GOV-33: closed trade count audit (PT-04 + SI-02 data density gate)
- [ST-17] BLG-GOV-34: Arc 4 data density risk trajectory assessment
- [ST-18] BLG-GOV-45: Arc 6 Monte Carlo §13 pre-assessment
- [ST-19] BLG-GOV-52: trade plan schema field count gate check
- [ST-20] BLG-GOV-41: sprint close automation failure investigation
- [ST-21] BLG-SPEC-32: external API integration spec template
- [ST-09] BLG-BE-16: red_flag_events severity field
- [ST-10] BLG-OPS-40: Arc 5 hosting cost projection assessment
- [ST-11] BLG-FE-42: Arc 5 nav cohesion review
- [ST-12] BLG-FE-47: Red Flag Journal design review scope document

Sign-off: Product Owner — 2026-05-31
QA sign-off: Director of Quality — 2026-05-31

---

## v4.5 — Governance Prompt Hardening, Audit Debt & SI-02 Spec Pre-Planning — 2026-05-30
Cycle: 2026-05-30__release-v4.5
Verified: Verified
Verification report: claude/cycles/2026-05-30__release-v4.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance Prompt Patches — execution_prompt.md v3.34: two-phase DEL terminal-status write (sign_off_cleared at sign-off, commit_sha at push; ST-01); explicit pr_status sync in STEP 3.2.B after PR open + EPIC.status done→merged rule (ST-02); LL-v4.5-EX-01 verification-class sub-criterion for pre-planning sprints (ST-03); LL-v4.5-EX-02 spec_references policy for doc-creation stories (ST-04). All four v4.4 outstanding actions resolved. | claude/system/execution_prompt.md v3.34 |
| EPIC-02 | Agent Role Header Standardization — 5 agent files updated from `**Owner:**` to `**Role:**` format: api_contracts_documentation_owner.md, backend_engineering_patterns_owner.md, data_model_domain_schema_owner.md, frontend_specs_ux_documentation_owner.md, metrics_definitions_analytics_owner.md (AUD-2026-05-30-005 Tier 2 audit debt cleared; ST-05) | claude/agents/ — 5 agent files |
| EPIC-03 | SI-02 Spec Pre-Sprint — §13 formal boundary review (PASS; 9 binding conditions documented; ST-06); drift detection score metric definition (4 metrics; 90-day window; green/amber/red bands; SI-05 integration; ST-07); data schema pre-definition (5 new trade_plans columns; DS-07 migration script; ST-08). SI-02 sprint planning now unblocked. | docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md; docs/specs/metrics/si02_drift_score.md; docs/specs/data_model/si02_data_schema.md; docs/specs/si02_gap_analysis.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-75: execution_prompt.md two-phase DEL terminal-status write
- [ST-02] BLG-GOV-76: execution_prompt.md STEP 3.2.B pr_status sync after PR open
- [ST-03] BLG-GOV-77: execution_prompt.md verification-class sub-criterion for pre-planning sprints
- [ST-04] BLG-GOV-70: execution_prompt.md spec_references policy for documentation-creation stories
- [ST-05] AUD-2026-05-30-005: Agent file role header standardization (5 files)
- [ST-06] BLG-GOV-39: SI-02 §13 formal boundary review
- [ST-07] BLG-SPEC-41: SI-02 drift score metric definition
- [ST-08] BLG-SPEC-37: SI-02 data schema pre-definition

Sign-off: Product Owner — 2026-05-30
QA sign-off: Director of Quality — 2026-05-30

---

## v4.4 — Governance Patches, SI-02 Pre-Planning Sprint & Ops Hardening — 2026-05-30
Cycle: 2026-05-29__release-v4.4
Verified: Verified
Verification report: claude/cycles/2026-05-29__release-v4.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance Prompt Patches — roadmap_prompt.md v6.6 (STEP 8.1 empty-Now-horizon advisory; ST-01); sprint_planning_prompt.md v3.8 (frontend classification fast-path for React-only stories; ST-02); execution_prompt.md v3.33 (auto-set deviations_filed on delegation clearance; ST-03); qa_evidence_template.md v1.4 (delegated_qa DoQ sign-off both format variants; ST-04); release_planning_prompt.md v2.32 (STEP 7 RESUME PRECHECK note; ST-05) | claude/system/roadmap_prompt.md v6.6; claude/system/sprint_planning_prompt.md v3.8; claude/system/execution_prompt.md v3.33; claude/system/templates/qa_evidence_template.md v1.4; claude/system/release_planning_prompt.md v2.32 |
| EPIC-04 | Ops Documentation Hardening — OPERATIONAL_GUIDE.md v4.19 §7.9 "Staging URL Disambiguation" subsection added (frontend SPA URL vs backend API URL distinction; health check guidance updated; ST-13) | claude/system/OPERATIONAL_GUIDE.md v4.19 §7.9 |
| EPIC-02 | SI-02 Backend Pre-Planning — drift detection query pre-design + HBE sign-off (ST-06); Arc 5 backend architecture review + ADR-001 cached-synchronous Option B recommendation (ST-07); query index pre-assessment with 3 migration-candidate indexes (ST-08); background job ADR-SI02-001 cached-synchronous selected, no worker/Redis/Celery on Render (ST-09) | docs/specs/si02/si02_query_predesign.md; docs/specs/si02/arc5_backend_architecture_review.md; docs/specs/si02/si02_index_preassessment.md; docs/specs/si02/si02_background_job_adr.md |
| EPIC-03 | SI-02 Frontend & QA Pre-Planning — drift detection result component pre-design (Option B percentage-deviation display, 4 component states; ST-10); interaction spec (5 states, non-dismissable, 13 Playwright DFT IDs; ST-11); Playwright scenario pre-design DFT-01–DFT-13 + 4 staging-only scenarios S-STG-01–S-STG-04 (ST-12) | docs/specs/si02/si02_fe_component_predesign.md; docs/specs/si02/si02_fe_interaction_spec.md; docs/qa/si02_playwright_predesign.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-71: roadmap_prompt.md STEP 8.1 advisory for empty Now horizon after Extended-tier rebalance
- [ST-02] BLG-GOV-72: sprint_planning_prompt.md frontend classification fast-path for React-only stories
- [ST-03] BLG-GOV-73: execution_prompt.md auto-set deviations_filed on delegation sign-off clearance
- [ST-04] BLG-GOV-69 + BLG-GOV-74: qa_evidence_template.md DoQ sign-off format for delegated_qa EPICs (both format variants)
- [ST-05] Release planning STEP 7 RESUME PRECHECK patch (v4.3 LL-2 carry-forward)
- [ST-06] BLG-BE-17: SI-02 drift detection query pre-design
- [ST-07] BLG-BE-18: Arc 5 backend architecture review for SI query patterns
- [ST-08] BLG-BE-23: SI-02 query index pre-assessment
- [ST-09] BLG-BE-20: SI-02 background job architecture design
- [ST-10] BLG-FE-52: SI-02 drift detection result component pre-design
- [ST-11] BLG-FE-53: SI-02 drift detection interaction spec
- [ST-12] BLG-QA-31: SI-02 Playwright scenario pre-design (DFT-01–DFT-13)
- [ST-13] BLG-OPS-43: Staging URL disambiguation in OPERATIONAL_GUIDE §7

Sign-off: Product Owner — 2026-05-30
QA sign-off: Director of Quality — 2026-05-30

---

## v4.3 — Governance Consolidation, QA Debt Clearance & Ops Hardening — 2026-05-29
Cycle: 2026-05-29__release-v4.3
Verified: Verified
Verification report: claude/cycles/2026-05-29__release-v4.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | v4.2 Governance Patch Resolution — execution_prompt.md v3.31→v3.32 (STEP 3.2.A qa_signed_off advisory; STEP 5.3/8 branch safety hard gate); qa_evidence_template.md v1.2→v1.3 (1:1 AC mapping advisory); OPERATIONAL_GUIDE.md v4.12→v4.13 (§7.8 staging-only AC pre-designation reference table); AI feature inventory document v1.0 (3 features with §13 compliance status) (ST-01–05) | claude/system/execution_prompt.md v3.32; claude/system/templates/qa_evidence_template.md v1.3; claude/system/OPERATIONAL_GUIDE.md v4.13; docs/ai/ai_feature_inventory.md |
| EPIC-04 | Frontend Fixes & Arc 5 P&L Section — pre-entry check entry price bug fix (PreEntryValidationPanel entryPrice/stopPrice props + URL params; SC-TP-21); Claude thesis generation UI copy audit (HAS_GEMINI→HAS_AI, isGeminiLoading→isAiLoading; SC-TP-22); Arc 5 compliance score in monthly P&L report (backend get_arc5_compliance_summary() + monthly-pnl strategy_compliance field; frontend Strategy Compliance section with 4 metric cards; SC-REP-05a/05b) (ST-16–18) | docs/specs/api_contracts/pre_entry_validation.md; docs/specs/frontend/pages/trade_plan.md; docs/specs/frontend/pages/reports.md; docs/specs/api_contracts/reports_endpoints.md v0.5; docs/specs/api_contracts/arc5_compliance_analytics.md |
| EPIC-03 | Ops & Security Documentation Hardening — API key rotation policy v1.0 + external API key security register v1.0 (5 credentials, 8-step staging-first procedure); staging environment parity audit v4.3 (env vars, DB schema, 4 endpoint health checks); claude-audit-log performance baseline §16 (p50=2,541ms, p95=2,858ms; BLG-OPS-42 closed); ANTHROPIC_API_KEY added to staging permanently (ST-13–15) | docs/ops/api_key_rotation_policy.md; docs/security/api_key_security_register.md; docs/ops/staging_parity_report_v4.3.md; docs/ops/api_performance_baseline.md v2.0 §16 |
| EPIC-02 | QA Debt Clearance — Playwright E2E for Arc5ComplianceSection (4 tests: SC-ARC5-01/02/03/04); Arc 5 E2E integration test spec v1.0 (20 scenarios); CI pipeline baseline v1.0 (p50=444s; BLG-QA-27 gate cleared); Playwright coverage matrix v1.0 (39 spec files) + Arc 5 coverage audit v1.0 (18 scenarios, 100% coverage); staging verifications: Claude thesis (AC-01/02/03 pass), ticker validation (HTTP 422 confirmed), Claude API cost alert (Telegram received) (ST-06–12) | docs/qa/arc5_e2e_integration_test_spec.md; docs/ops/ci_pipeline_baseline.md; docs/qa/playwright_coverage_matrix.md; docs/qa/arc5_coverage_audit.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] OA-1 (v4.2): execution_prompt.md STEP 3.2.A qa_signed_off advisory patch
- [ST-02] OA-2 (v4.2): execution_prompt.md STEP 5.3/STEP 8 sprint close branch safety hard gate
- [ST-03] OA-3 (v4.2): qa_evidence_template.md AC mapping 1:1 advisory
- [ST-04] BLG-GOV-42: staging-only AC pre-designation reference table
- [ST-05] BLG-GOV-47: AI feature inventory document
- [ST-06] BLG-QA-29: staging verification — Claude thesis generation
- [ST-07] BLG-QA-30: staging verification — ticker validation Yahoo Finance rejection path
- [ST-08] BLG-QA-35: staging verification — Claude API daily cost threshold alert
- [ST-09] BLG-QA-28: Playwright E2E coverage for Arc5ComplianceSection
- [ST-10] BLG-QA-36: Arc 5 end-to-end integration test specification
- [ST-11] BLG-QA-38: CI pipeline execution time baseline measurement
- [ST-12] BLG-QA-32 + BLG-QA-33: Playwright scenario coverage matrix + Arc 5 coverage audit
- [ST-13] BLG-OPS-33: staging environment parity audit
- [ST-14] BLG-OPS-42: claude-audit-log performance baseline (GET /ai/claude-audit-log)
- [ST-15] BLG-GOV-36 + BLG-GOV-50: API key rotation policy + external API key security register
- [ST-16] BLG-FE-50: pre-entry check entry price bug fix
- [ST-17] BLG-FE-51: Claude thesis generation UI copy audit (Gemini→AI variable rename)
- [ST-18] BLG-FE-38: Arc 5 compliance score in monthly P&L report

Sign-off: Product Owner — 2026-05-29
QA sign-off: Director of Quality — 2026-05-29

---

## v4.2 — Claude API Governance, SI-02 Pre-Work Readiness & Spec Debt — 2026-05-29
Cycle: 2026-05-27__release-v4.2
Verified: Verified
Verification report: claude/cycles/2026-05-27__release-v4.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Claude API Compliance & Security — Anthropic API accountability formally assigned (AI Compliance Officer charter §4.1 updated); ANTHROPIC_API_KEY security posture confirmed (docs/security/anthropic_api_key_scope_review.md, 3 sign-offs); model version pinning policy created (docs/governance/ai_model_version_pinning_policy.md v1.0; env-var override removed from ai_service.py); Claude API log hygiene policy produced and activated (docs/ops/claude_api_log_hygiene_policy.md v1.0; Render log inspection confirmed clean) (ST-01/02/03) | docs/security/anthropic_api_key_scope_review.md; claude/agents/ai_compliance_governance_officer.md; docs/governance/ai_model_version_pinning_policy.md; backend/services/ai_service.py; docs/ops/claude_api_log_hygiene_policy.md |
| EPIC-02 | Operational Monitoring & Baselines — POST /ai/check-daily-cost baseline added (p50=205ms, p95=518ms; 5 staging samples); Claude API first monthly cost review produced ($0.007387/6 calls; monthly cadence + $5/month alert threshold defined); Claude API thesis generation latency baseline established (p50=3,560ms, p95=3,923ms; 10 warm production samples; regression threshold 2× baseline) (ST-04/05/06) | docs/ops/api_performance_baseline.md v1.6→v1.7; docs/ops/claude_cost_review_2026-05.md |
| EPIC-03 | Gemini→Claude Spec Debt Clearance — claude_audit_log table + ensure/create/query functions in database.py; GET /ai/claude-audit-log endpoint; ai_endpoints.md v1.2; gemini_thesis_generation.md renamed to ai_thesis_generation.md v2.1.0 (Claude API token fields added); gemini_thesis_generation.md superseded; openapi.yaml updated; Claude API Playwright mock strategy document produced; prompt caching assessment: DEFER (prefix <1,024 tokens; <10 calls/day) (ST-07/08/09/10) | docs/specs/api_contracts/ai_endpoints.md v1.2; docs/specs/api_contracts/ai_thesis_generation.md v2.1.0; docs/specs/api_contracts/gemini_thesis_generation.md (Superseded); docs/reference/openapi.yaml; backend/database.py; backend/routers/ai.py; docs/team_skills/quality/claude_api_playwright_mock_strategy.md; docs/governance/claude_prompt_caching_assessment.md |
| EPIC-04 | SI-02/SI-04 Pre-Planning — si02_prerequisites_checklist.md v1.0 (13 items: 4 Complete, 1 gate-conditional, 8 Open); si04_scope_definition.md v1.0 (5 metrics, date-range versioning, comparison UI concept); v4.1 staging deviation trend review (IMPROVED: v4.1=2 vs v4.0=4); backlog namespace audit (287 BLG IDs, 0 collisions) (ST-11/12/13) | docs/governance/si02_prerequisites_checklist.md; docs/governance/si04_scope_definition.md; docs/governance/v41_staging_deviation_review.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-66 + BLG-GOV-65: Anthropic API accountability assignment + API key security review
- [ST-02] BLG-GOV-64: Anthropic model version pinning policy
- [ST-03] BLG-OPS-38: Claude API log hygiene policy
- [ST-04] BLG-OPS-35: API performance baseline — POST /ai/check-daily-cost (OA-3 resolution)
- [ST-05] BLG-OPS-36: Claude API first monthly cost review
- [ST-06] BLG-OPS-39: Claude API thesis generation latency baseline
- [ST-07] BLG-GOV-63: Claude API audit trail implementation
- [ST-08] BLG-SPEC-42: AI thesis API contract update for Claude
- [ST-09] BLG-QA-37: Claude API Playwright mock strategy
- [ST-10] BLG-BE-22: Claude API prompt caching assessment (deferred)
- [ST-11] BLG-GOV-60: SI-02 sprint planning prerequisites checklist
- [ST-12] BLG-GOV-57: SI-04 strategy version comparison pre-planning
- [ST-13] BLG-GOV-61 + BLG-GOV-59: v4.1 staging sign-off review + backlog namespace audit

Sign-off: Product Owner — 2026-05-29
QA sign-off: Director of Quality — 2026-05-29

---

## v4.1 — Governance Hardening, Spec Debt, Arc 5 Compliance + SI-02 Pre-Planning — 2026-05-27
Cycle: 2026-05-26__release-v4.1
Verified: Verified
Verification report: claude/cycles/2026-05-26__release-v4.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance prompt hardening — execution_prompt.md v3.27→v3.28 (merge-gate re-invocation HARD GATE after every EPIC merge; OA-01 resolved); sprint_planning_prompt.md v3.6→v3.7 (mandatory staging-only AC check at STEP 6.2 sign-off gate; OA-02 resolved); shared_standards.md v3.3→v3.4 (sprint_backlog.md template [REQUIRED] enforcement); delivery_verification_prompt.md v2.5→v2.6 (STEP -1.3A PR Number Recovery; OA-04 resolved) (ST-01/02/03) | claude/system/execution_prompt.md; claude/system/sprint_planning_prompt.md; claude/system/shared_standards.md; claude/system/delivery_verification_prompt.md |
| EPIC-02 | API contract spec debt clearance — four undocumented v3.8/v3.9/v4.0 endpoints verified and formally contracted: red_flag_journal.md v1.0.0 (SI-03), pre_entry_validation.md v1.0.0 (SI-01), arc5_compliance_analytics.md v1.0.0 (Arc 5), gemini_thesis_generation.md v2.0.0 (AI thesis); all openapi.yaml entries confirmed (ST-04/05/06/07) | docs/specs/api_contracts/red_flag_journal.md; docs/specs/api_contracts/pre_entry_validation.md; docs/specs/api_contracts/arc5_compliance_analytics.md; docs/specs/api_contracts/gemini_thesis_generation.md; docs/reference/openapi.yaml |
| EPIC-03 | Arc 5 P&L integration + Claude API cost alerting + frontend spec — metrics_definitions.md v1.10→v1.11 (Arc 5 composite score formula); reports.md v0.2→v0.3 (Arc 5 Compliance Summary section); POST /ai/check-daily-cost endpoint with Telegram alert ($1.00 default threshold) + 5 unit tests; research_view.md v1.1→v1.2 (signal_type Setup Type field + 4 Playwright tests); arc5_compliance_section.md v1.0 created (ST-08/09/10) | docs/specs/metrics_definitions.md; docs/specs/frontend/pages/reports.md; docs/specs/api_contracts/ai_endpoints.md v1.1; docs/specs/frontend/pages/research_view.md; docs/specs/frontend/components/arc5_compliance_section.md; docs/reference/openapi.yaml |
| EPIC-04 | SI-02 pre-planning + security review + operational reviews — si02_gap_analysis.md (5 gaps enumerated); section13_criteria.md, data_prerequisite_audit.md (gate NOT met: <20 closed trades), query_performance_assessment.md; ANTHROPIC_API_KEY scope review + credential inventory v1.1; delivery_verification_prompt.md v2.6→v2.7 (STEP 9.0 artefact presence check); OPERATIONAL_GUIDE.md v4.05→v4.06; api_performance_baseline.md v1.4→v1.5; gemini_cost_tracking.md v1.1→v1.2; pnl_attribution_gate_check.md v1.0 (ST-12/13/14/15) | docs/specs/si02_gap_analysis.md; docs/specs/si02/section13_criteria.md; docs/specs/si02/data_prerequisite_audit.md; docs/specs/si02/query_performance_assessment.md; docs/security/anthropic_api_key_scope_review.md; docs/ops/external_api_credential_inventory.md v1.1; claude/system/delivery_verification_prompt.md; docs/ops/api_performance_baseline.md; docs/ops/gemini_cost_tracking.md; docs/ops/pnl_attribution_gate_check.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] OA-01 (2nd-recurrence): execution_prompt.md merge-gate re-invocation as hard gate
- [ST-02] OA-02 (2nd-recurrence): sprint_planning_prompt.md staging-only AC designation at planning
- [ST-03] OA-04: delivery_verification_prompt.md PR number null guard (STEP -1.3A)
- [ST-04] BLG-SPEC-33: SI-03 Red Flag Journal API contract document
- [ST-05] BLG-SPEC-34: SI-01 Pre-Entry Validation API contract document
- [ST-06] BLG-SPEC-40: Arc 5 analytics endpoint API contract
- [ST-07] BLG-SPEC-38: AI thesis endpoint API contract (Claude API)
- [ST-08] BLG-FEAT-40 + BLG-FEAT-42: Arc 5 compliance metrics P&L integration (composite score formula + Reports page section)
- [ST-09] BLG-OPS-34: Claude API daily cost threshold alert via Telegram
- [ST-10] BLG-FE-44 + BLG-FE-48: Research view signal_type field + Arc5ComplianceSection component spec
- [ST-12] BLG-SPEC-39: SI-02 data model gap analysis
- [ST-13] BLG-GOV-44 + BLG-GOV-46 + BLG-GOV-51: SI-02 pre-planning (§13 criteria + data audit + query performance)
- [ST-14] BLG-GOV-49 + BLG-GOV-54 + BLG-GOV-56: Security review (ANTHROPIC_API_KEY) + SI-05 annotation + delivery_verification_prompt.md STEP 9.0
- [ST-15] BLG-OPS-29 + BLG-OPS-30 + BLG-OPS-32: API performance baseline v1.5 + first Claude usage review + P&L attribution gate check

Sign-off: Product Owner — 2026-05-27
QA sign-off: Director of Quality — 2026-05-27

---

## v4.0 — Arc 5 Analytics Foundation + Spec Closure + Gemini Compliance — 2026-05-25
Cycle: 2026-05-22__release-v4.0
Verified: Verified
Verification report: claude/cycles/2026-05-22__release-v4.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Arc 5 compliance analytics — GET /analytics/arc5-compliance delivering validation_pass_rate_by_rule, events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate; pre_entry_validation_log table; Arc5ComplianceSection.js frontend on PerformanceAnalytics §19; SI-01→SI-03 Playwright integration suite (8 scenarios) (ST-01/02/03/04) | docs/specs/api_contracts/analytics_endpoints.md v2.2.0; docs/specs/metrics_definitions.md#Arc 5 Compliance Metrics; docs/design/2026-05-22__release-v4.0/arc5-analytics-metrics/ux_spec.md; docs/reference/openapi.yaml |
| EPIC-02 | Ticker Quality & Security — live Yahoo Finance symbol validation at POST /ticker-universe (HTTP 422 on unknown symbol; SKIP_TICKER_VALIDATION CI bypass); red flag endpoint auth/PII security review (PASS); starlette CVE remediation (starlette==1.0.1; PYSEC-2026-161 closed) (ST-05/06/13) | docs/specs/api_contracts/ticker_universe_api_contract.md v1.2; docs/specs/api_contracts/red_flag_journal.md; backend/requirements.txt |
| EPIC-03 | AI Governance & CI/CD — Gemini Flash base wiring (POST /trade-plans/{plan_id}/generate-thesis; "Improve with AI" button on TradePlan edit); gemini_audit_log table (fire-and-forget, 90-day retention); token/cost tracking ($0.075/$0.30 per M tokens; 800k alert threshold); CI/CD staging auto-deploy (.github/workflows/staging-deploy.yml with path filter) (ST-07/08/09/12) | docs/specs/api_contracts/trade_plan_endpoints.md v0.3; docs/ops/gemini_cost_tracking.md; backend/routers/test.py (60→61) |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-FEAT-36: SI-01 validation pass/fail rate by rule — backend metric endpoint
- [ST-02] BLG-FEAT-37: Red flag event frequency metric — backend + frontend
- [ST-03] BLG-QA-25: E2E Playwright test — SI-01→SI-03 integration path
- [ST-04] BLG-FEAT-39: Trade plan adherence rate metric — backend + frontend
- [ST-05] BLG-BE-15: Validate ticker symbol on add
- [ST-06] BLG-GOV-37: Red flag endpoint auth and PII review
- [ST-07] BLG-GOV-35: Gemini audit trail — log AI thesis generation calls
- [ST-08] BLG-OPS-26: Gemini cost tracking — token usage and cost per call
- [ST-09] BLG-OPS-27: CI/CD automated staging re-deploy on main merge
- [ST-12] BLG-BE-19: Gemini Flash base wiring (hard-prerequisite; AMD-20260523-01)
- [ST-13] CVE PYSEC-2026-161: Starlette security upgrade to ≥1.0.1 (emergency; AMD-20260523-01)

Sign-off: Product Owner — 2026-05-25
QA sign-off: Director of Quality — 2026-05-25

---

## v3.9 — Screener Quality & Reliability + Arc 5 Red Flag Journal + Governance Patches — 2026-05-22
Cycle: 2026-05-21__release-v3.9
Verified: Verified
Verification report: claude/cycles/2026-05-21__release-v3.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Screener Data Quality & Reliability: Yahoo Finance crumb/401 retry with exponential backoff+jitter (ST-01); sector/industry fields restored to screener results (ST-02); invalid ticker DAY removed with startup deactivation (ST-03); degraded-run warning banner when >20% fetch failures (ST-04) | backend/services/screener_data_service.py; backend/services/screener_batch_service.py; docs/specs/frontend/pages/screener_results.md; docs/specs/api_contracts/screener_api_contract.md v1.1; docs/reference/openapi.yaml |
| EPIC-02 | Ticker Universe Enhancements: .L suffix stripped from display labels while preserving API requests (ST-05); company_name column added with CSV backfill and management page display (ST-06) | docs/specs/frontend/pages/ticker_universe.md; docs/specs/api_contracts/ticker_universe_api_contract.md |
| EPIC-03 | Arc 5 Red Flag Journal (SI-03): red_flag_events table; GET /portfolio/red-flag-journal endpoint (paginated, filterable by event_type/ticker/since); SI-01 override event write path; RedFlagJournal.js frontend with filters, pagination, empty state, Trading nav link (ST-07/08) | docs/specs/api_contracts/portfolio_endpoints.md v2.3; docs/specs/frontend/pages/red_flag_journal.md; docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md; docs/reference/openapi.yaml; backend/routers/test.py (59→60) |
| EPIC-04 | Governance Patches — all 5 v3.8 carry-forward items resolved: execution_prompt.md v3.26 (test_scenarios scope rule + createPageUrl delegation note); sprint_planning_prompt.md v3.4 (deferred_at_planning state); release_planning_prompt.md v2.31 + delivery_verification_prompt.md v2.5 (--dry-run support); PR template v1.2 (QA evidence pre-merge checklist) (ST-09/10/11/12) | claude/system/execution_prompt.md v3.26; claude/system/sprint_planning_prompt.md v3.4; claude/system/release_planning_prompt.md v2.31; claude/system/delivery_verification_prompt.md v2.5; .github/pull_request_template.md v1.2 |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-TECH-10: Fix Yahoo Finance crumb/401 rate-limiting in screener batch
- [ST-02] BLG-BE-10: Fix sector/industry data dropped in screener batch
- [ST-03] BLG-BE-11: Remove DAY from ticker universe (invalid Yahoo Finance symbol)
- [ST-04] BLG-FE-38: Add degraded-run warning to screener when OHLCV failure rate exceeds 20%
- [ST-05] BLG-FE-37: Strip .L suffix from Ticker Universe page display labels
- [ST-06] BLG-BE-12: Add company_name column to ticker universe
- [ST-11] BLG-GOV-25: Add --dry-run support to plan release and run delivery verification engines

Sign-off: Product Owner — 2026-05-22
QA sign-off: Director of Quality — 2026-05-22

---

## v3.8 — Arc 5 Strategy Integrity Foundation + Trade Plan Form Enhancements + Ticker Universe Management — 2026-05-20
Cycle: 2026-05-19__release-v3.8
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-19__release-v3.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-04 | Ticker Universe Management Page (ST-09): TickerUniverse.js page with add/toggle/delete/filter; `public.tickers` startup sync retired; `ticker_universe` is sole authoritative source. Governance Debt Clearance (ST-10): gh_issue_template.md added to §14; DoQ enforcement via PR template; OPERATIONAL_GUIDE.md v3.90→v3.92. | docs/specs/api_contracts/ticker_universe_api_contract.md; claude/system/OPERATIONAL_GUIDE.md#§14 |
| EPIC-03 | Setup Type Classification Field (ST-06): `setup_type` dropdown on trade plan form, 6 options, persisted. News Context Panel (ST-07): collapsible Alpaca news panel on trade plan form, localStorage-persisted collapse state. AI-Assisted Thesis Generation (ST-08): "Generate thesis" template engine + "Improve with AI" (Gemini-gated). | docs/specs/api_contracts/trade_plan_endpoints.md; docs/specs/frontend/pages/trade_plan.md |
| EPIC-01 | §13 Review Gate for SI-01 (ST-01): 8 binding conditions documented; Category A + B checks authorised. SI-01 Backend (ST-02): `strategy_rules.md` v1.4 §4.2; `GET /portfolio/pre-entry-validation`; 17 unit tests; conftest.py stubs (BLG-QA-20 resolved). SI-01 Frontend (ST-03): PreEntryValidationPanel with override acknowledgement checkbox on trade plan form; SC-TP-17–20 Playwright pass. | docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/pre-entry-validation; docs/specs/frontend/pages/trade_plan.md; docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-EPIC04-ST09-01 | P3 | createPageUrl map missing TickerUniverse entry at time of EPIC-04 PR merge — resolved in same release (fix commit 75b7eda4, PR #456) | PO + DoQ |

### Tech backlog items shipped
- [ST-09] BLG-FEAT-22: Ticker Universe Management page
- [ST-10] BLG-GOV-24 + DoQ OA: Governance debt clearance (gh_issue_template.md §14 + PR template enforcement)
- [ST-06] BLG-FEAT-23: Setup type classification field on trade plans
- [ST-07] BLG-FE-36: News context panel on trade plan form
- [ST-08] BLG-FEAT-24: AI-assisted setup thesis generation

Sign-off: Product Owner — 2026-05-20
QA sign-off: Director of Quality — 2026-05-20

---

## v3.7 — Signal-to-Watchlist Workflow + Arc 2 Completion + Governance Hardening — 2026-05-18
Cycle: 2026-05-18__release-v3.7
Verified: Verified
Verification report: claude/cycles/2026-05-18__release-v3.7/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Signal-to-Watchlist Workflow (S2-01): `watchlisted` status added to signals table CHECK constraint; `PATCH /signals/{id}` accepts `status: "watchlisted"`; `SignalCard.js` primary CTA replaced with "Add to Watchlist" with watchlisted state badge; `SignalContextPanel.js` read-only signal context panel in trade plan form with entry_rationale + confirmation_criteria pre-population; 7 Playwright scenarios SC-SIG-WL-01/02/03 (signals-add-to-watchlist.spec.js) + SC-TP-SIG-01/02/03/04 (trade-plan-signal-context.spec.js) | docs/specs/api_contracts/signal_endpoints.md v1.2; docs/specs/data_model.md v2.8; docs/specs/frontend/pages/signals.md; docs/specs/frontend/pages/trade_plan.md; docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md |
| EPIC-03 | Governance hardening patches (S2-03): execution_prompt.md v3.23→v3.24 (deviations_filed atomic write, backlog verify guidance, spec_references path verify guidance); qa_evidence_template.md v1.0→v1.1 (BLG-GOV-19 criterion 3 fail-path); retroactive prompt_change_log.md entries for v3.18–v3.22 gap | claude/system/execution_prompt.md; claude/system/templates/qa_evidence_template.md |
| EPIC-04 | Tech debt clearance (S2-04): BLG-QA-20 database stub conftest consolidation (session-scoped `types.ModuleType("database")` stub in tests/conftest.py; CLAUDE.md §2 updated); BLG-OPS-16 pycache git hygiene (git rm -r --cached + .gitignore); BLG-FE-35 Research page typography staging sign-off (SC-RV-TYP-01 Playwright regression); BLG-GOV-23 scored_initiatives.md Arc 3–6 comprehensive refresh (OA-RP-05 resolved) | docs/frontend/design_system.md; claude/scoring/scored_initiatives.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-09] BLG-QA-20: Database stub conftest consolidation
- [ST-10] BLG-OPS-16 + BLG-FE-35: Pycache git hygiene + Research page typography staging sign-off
- [ST-11] BLG-GOV-23: scored_initiatives.md Arc 3–6 comprehensive refresh (resolves OA-RP-05)

Sign-off: Product Owner — 2026-05-18
QA sign-off: Director of Quality — 2026-05-18

---

## v3.6 — Arc 4 Data Integrity + Research Debt Clearance + Governance Patches — 2026-05-17
Cycle: 2026-05-16__release-v3.6
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-16__release-v3.6/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Arc 4 Data Integrity (S2-01): `planned_entry_price` column added to trade_history (nullable; ALTER TABLE IF NOT EXISTS); `exit_position()` captures signal's current_price at entry; `_compute_entry_delta_pct()` calculates (actual−planned)/planned×100; `PlanVsReality` component updated to display entry_delta_pct with emerald (favorable) / rose (unfavorable) colouring; null → 'data not available for historical trades'; 9 Playwright scenarios (SC-PVR-03a/b, SC-PVR-04a/b, SC-PVR-05a/b/c) | docs/specs/arc4/arc4_data_requirements.md §3.1; docs/specs/frontend/pages/trade_history.md §Expandable Journal Row — Plan vs Reality; openapi.yaml (planned_entry_price field added to TradeHistoryResponse) |
| EPIC-03 | Research QA/Spec/UX Debt (S2-03): SC-RV-18 and SC-RV-19 Playwright tests added (RESEARCH_REGIME_NULL, RESEARCH_ALL_NULL payloads); research_endpoint.md v1.2 §Error Responses updated; `_get_price_data()` returns `_YF_UNAVAILABLE`/`_TICKER_NOT_FOUND` sentinels → HTTP 503/404; partial failures still 200+nulls; Research.js error state shows specific messages; regime lozenge `whitespace-nowrap` fix (BLG-FE-26 wrapping bug) | docs/specs/api_contracts/research_endpoint.md v1.2; docs/qa/test_scenarios/research_view_scenarios.md v1.1; openapi.yaml (404/503 responses added); docs/frontend/design_system.md |
| EPIC-04 | Governance Patches (S2-04): execution_prompt.md v3.21→v3.22 — §13 gate story pattern formalised (LL-v3.5-SP-01); metadata + sprint_close + Phase 3 deferred patches applied; retroactive prompt_change_log.md entries for v3.18–v3.22 gap; OA-RP-01–04 resolved | claude/system/execution_prompt.md v3.22; OPERATIONAL_GUIDE.md §8+§14; claude/system/prompt_change_log.md |

### Deviations accepted
1 minor P3 deviation: ST-08 AC-02 — research page regime lozenge human staging sign-off deferred; backlog item BLG-FE-33 filed

### Tech backlog items shipped
- [ST-06] BLG-FE-32 + TEST-GAP-EPIC-03-v33: SC-RV-18 and SC-RV-19 Playwright coverage
- [ST-07] BLG-SPEC-27: Research endpoint HTTP 404/503 error code differentiation
- [ST-08] BLG-FE-26: Research page regime lozenge wrapping fix
- [ST-09] Governance: execution_prompt.md §13 gate story pattern formalisation + retroactive changelog entries (OA-RP-01–04)
- [ST-10] Governance: execution_prompt.md metadata + sprint_close + Phase 3 patches

### Deferred
- EPIC-02 (PT-04 Arc 2 Quality Score) — deferred to v3.7; PT-04 gate condition (≥20 closed trades) unconfirmed at sprint planning

Sign-off: Product Owner — 2026-05-17
QA sign-off: Director of Quality — 2026-05-17

---

## v3.5 — Arc 3 Completion + Arc 4 Foundation — 2026-05-15
Cycle: 2026-05-15__release-v3.5
Verified: Verified
Verification report: claude/cycles/2026-05-15__release-v3.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Arc 3 Completion — IT-06 Alpaca Paper Trading: §13 compliance review (PASS; four binding conditions documented); backend sync service `alpaca_paper_sync_service.py` + `GET /portfolio/paper-positions` endpoint (best-effort US market position mirroring); `PaperAccountPanel` frontend component on Positions page; 5 Playwright scenarios (SC-PA-01a/b/c, SC-PA-02a/b) | claude/strategy/strategy_rules.md#§13; docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md; docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/paper-positions; docs/ux_specs/paper-trading/ux_spec.md |
| EPIC-02 | Arc 4 Foundation — Arc 4 data requirements capture (`docs/product/arc4_data_requirements.md` v1.0, PO + HoUX sign-off); PO-01 Plan vs Reality backend calculation service + `GET /trades/{id}/plan-vs-reality` endpoint + `plan_vs_reality` JSONB field migration; `PlanVsReality` frontend component in TradeHistoryTable; 5 Playwright scenarios (SC-PVR-01a/b/c, SC-PVR-02a/b) | docs/specs/api_contracts/trade_endpoints.md#GET /trades/{trade_id}/plan-vs-reality; docs/data_model.md#trade_history; docs/data_model.md#trade_plans; docs/ux_specs/plan-vs-reality/ux_spec.md |
| EPIC-03 | Spec & QA Debt: BLG-SPEC-29 grace-period-alert ux_spec.md §5 sessionStorage correction; BLG-SPEC-30 stop-management-workflow ux_spec.md §4.4 PATCH correction; BLG-SPEC-31 React Query v5 onSuccess scan (1 fix applied TradePlan.js; SC-TP-08 Playwright 9/9); BLG-QA-19 research view regression protocol v1.0 | docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md; docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md; docs/qa/acceptance_protocols/research_view_regression_protocol.md |
| EPIC-04 | Governance Patches: BLG-GOV-22 sprint_planning_prompt.md v3.1 (shared execution_state.json ownership rule + multi-EPIC merge guidance); execution_prompt.md v3.20 (intent-check advisory, Known Deviations sync advisory, backlog ID uniqueness check, sprint_close readiness consistency rule, BLG ID completeness check) | claude/system/sprint_planning_prompt.md; claude/system/execution_prompt.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-07] BLG-SPEC-29: Correct grace-period-alert ux_spec.md §5 dismiss storage to sessionStorage
- [ST-08] BLG-SPEC-30: Correct stop-management-workflow ux_spec.md §4.4 stop-update HTTP verb to PATCH
- [ST-09] BLG-SPEC-31: React Query v5 onSuccess codebase scan and fix (TradePlan.js)
- [ST-10] BLG-QA-19: Research view regression test protocol
- [ST-04] BLG-GOV-21: Arc 4 data requirements capture
- [ST-11] BLG-GOV-22: sprint_planning_prompt.md shared ownership patch

Sign-off: Product Owner — 2026-05-15
QA sign-off: Director of Quality — 2026-05-15

---

## v3.4 — Arc 3 In-Trade Risk Management (continued) — 2026-05-14
Cycle: 2026-05-14__release-v3.4
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-14__release-v3.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Arc 3 Frontend Completion (IT-01/02/03): LifecycleBadge component on positions page (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN states) with arc3_lifecycle_display feature flag guard; GracePeriodAlertZone with sessionStorage dismiss; TrailStopModal with PATCH /positions/{id} stop update. 10/10 Playwright scenarios pass | docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md; docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md; docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md |
| EPIC-02 | Arc 3 Risk Prompts (IT-04/05): GET /portfolio/drawdown-status backend (drawdown % from peak, threshold breach, open positions by state); DrawdownReviewPrompt component (§13 display-only, session-scoped dismiss); GET /portfolio/concentration-status backend (per-position/sector heat); ConcentrationLimitsWarning component (DS-03 graceful degradation). 10/10 Playwright scenarios pass | docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md; docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md; docs/reference/openapi.yaml |
| EPIC-03 | Frontend Quick Wins: Research page UK suffix strip (BLG-FE-23); negative/zero earnings days display (BLG-FE-24); Signals page defaults to most recent day (BLG-FE-25); Watchlist research status indicator (BLG-FE-29); Trade plan status badges + abandonment UI (BLG-FE-30 + BLG-FEAT-21 frontend). 16/16 Playwright scenarios pass | docs/specs/frontend/pages/trade_plan.md#9 |
| EPIC-04 | Spec & QA Debt: Research view component library (BLG-FE-31); Screener morning routine UX spec (BLG-FE-22); trade_plan.md §6.2 entry checklist field references updated (BLG-SPEC-28); AI journal review cadence (BLG-AI-03); Screener accuracy test protocol (BLG-QA-18) | docs/frontend/component_library_research_view.md; docs/specs/frontend/pages/screener_morning_routine.md; docs/specs/frontend/pages/trade_plan.md#§6.2; docs/testing/screener_accuracy_protocol.md |

### Deviations accepted
4 minor P3 deviations — see verification_report.md §4 for full detail:
- EPIC-01/DEV-v3.4-01 [ST-02, P3]: sessionStorage used instead of localStorage for grace period dismiss — matches "same browser session" AC. Target: v3.5 (BLG-SPEC-29).
- EPIC-01/DEV-v3.4-02 [ST-03, P3]: PATCH /positions/{id} used instead of PUT for stop update — correct HTTP verb. Target: v3.5 (BLG-SPEC-30).
- EPIC-03/DEV-v3.4-01 [ST-10, P3]: React Query v5 removed onSuccess from useQuery — isAbandoned derived from query data. Codebase scan pending (BLG-SPEC-31).
- EPIC-02/DEV-v3.4-01 [ST-05, P3]: useState in-memory dismiss — spec §6 explicitly specifies in-memory state. Self-resolving.

### Tech backlog items shipped
- [ST-11] Research view component library (BLG-FE-31) — PT-02 component catalogue
- [ST-12] Screener morning routine UX spec (BLG-FE-22) — Arc 1→Arc 2 workflow spec
- [ST-13] trade_plan.md §6.2 spec update (BLG-SPEC-28) + AI journal review cadence (BLG-AI-03)
- [ST-14] Screener accuracy test protocol (BLG-QA-18) — §11 filter accuracy protocol
- [ST-07] Research page UK suffix strip (BLG-FE-23) + negative earnings days (BLG-FE-24)
- [ST-08] Signals page default to most recent day (BLG-FE-25)
- [ST-09] Watchlist research status indicator (BLG-FE-29)
- [ST-10] Trade plan status badges (BLG-FE-30) + abandonment UI (BLG-FEAT-21 frontend)

Sign-off: Product Owner — 2026-05-14
QA sign-off: Director of Quality — 2026-05-14

---

## v3.3 — Arc 3 In-Trade Risk Management — 2026-05-13
Cycle: 2026-05-09__release-v3.3
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-09__release-v3.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | IT-01 Position Lifecycle Manager (backend + state machine): DS-05 positions table lifecycle fields (position_state, state_entered_at, days_in_state) and direct SQL migration; position_lifecycle_service.py state machine (5 states: NEW → GRACE → LOSING/PROFITABLE → EXIT); GET /positions enriched with lifecycle fields; POST /positions/{id}/refresh-state endpoint; arc3_lifecycle_display feature flag. Frontend state display (ST-03) deferred to v3.4 | docs/specs/data_model.md#DS-05; backend/services/position_lifecycle_service.py; docs/reference/openapi.yaml |
| EPIC-02 | IT-02 Grace Period Decision Support (backend): GET /positions/grace-period-alerts endpoint — positions in grace period expiring within N days with trade plan join and §13-compliant display recommendation. IT-03 Stop Management Workflow (backend): GET /positions/{id}/stop-trail endpoint — ATR trail calculation, R-denominated recommendation, §13 display-only. Frontend alert card (ST-05) and trail stop panel (ST-07) deferred to v3.4 | docs/specs/api_contracts/grace_period_alert_endpoint.md; docs/reference/openapi.yaml |
| EPIC-03 | PT-02 research API contract (BLG-SPEC-25) and data source provenance spec (BLG-SPEC-26). Research view canonical spec (BLG-SPEC-24) and UX spec (BLG-FE-28). Test scenario library (BLG-QA-17): 19 scenarios SC-RV-01–19. Acceptance test protocol (BLG-QA-15). Entry checklist Playwright E2E tests (BLG-QA-14): entry-checklist.spec.js covering SC-CL-01–07. Research endpoint integration tests (BLG-QA-16), latency baseline (BLG-OPS-15), trade plan sensitivity classification (BLG-SEC-06), field extension governance policy (BLG-GOV-20) | docs/specs/api_contracts/research_endpoint.md; docs/specs/frontend/pages/research_view.md; docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md; docs/qa/test_scenarios/research_view_scenarios.md; docs/qa/acceptance_protocols/research_view_protocol.md; tests/e2e/entry-checklist.spec.js; docs/ops/api_performance_baseline.md#section-11; docs/specs/security/trade_plan_data_sensitivity.md; docs/governance/trade_plan_field_extension_policy.md |
| EPIC-04 | Governance patches: execution_prompt.md v3.16→v3.17 (OA-01/CF-01 sealed-file check, OA-02/CF-02 mock payload advisory); sprint_planning_prompt.md v2.7→v2.8 (OA-05 design gate before sprint planning check); backlog_management_prompt.md v1.5→v1.6 + backlog_deferral_policy.md (OA-03/CF-03 3-cycle deferral policy). PT-05 §13 compliance review (BLG-GOV-19). Feature flag infrastructure (BLG-FEAT-13): is_flag_enabled() utility, FEATURE_FLAGS env var, arc3_lifecycle_display POC. Trade plan abandonment backend (BLG-FEAT-21 partial): DS-06 abandonment_reason column migration, PUT /trade-plans/{id} abandonment guard. Frontend status badges (ST-17 sub-deliverables: BLG-FE-30/23/24/25/29) deferred to v3.4 | claude/system/execution_prompt.md v3.17; claude/system/sprint_planning_prompt.md v2.8; claude/system/backlog_management_prompt.md v1.6; docs/governance/backlog_deferral_policy.md; docs/specs/compliance/pt05_entry_checklist_s13_review.md; docs/specs/platform/feature_flags.md; backend/utils/feature_flags.py; docs/specs/data_model.md#DS-06 |

### Deviations accepted
4 minor P3 deviations — see verification_report.md §4 for full detail:
- DEV-v33-01 [ST-01, P3]: AC specified Alembic migration; implementation used project-standard direct SQL. Target: v3.4.
- DEV-v33-02 [ST-08, P3]: AC specified 404/503/429 error codes; implementation returns 200 with null sub-fields on source failure. Known limitation documented in research_endpoint.md §Error Responses. Target: v3.4. (Reclassified P2→P3 by Director of Quality 2026-05-13.)
- DEV-v33-03 [ST-11, P3]: Spec references stop_level/risk_reward_notes for pre-population; implementation uses early_exit_conditions/r_target. Tests cover actual behaviour. Target: v3.4.
- DEV-v33-04 [ST-16, P3]: QA evidence reclassification note in qa_evidence_EPIC-04.md. Target: v3.4.

### Tech backlog items shipped
- [ST-08] Research API contract (BLG-SPEC-25) + data source provenance spec (BLG-SPEC-26)
- [ST-09] Canonical research view spec (BLG-SPEC-24) + UX spec (BLG-FE-28)
- [ST-10] Research view test scenario library (BLG-QA-17) + acceptance test protocol (BLG-QA-15)
- [ST-11] Entry checklist Playwright E2E tests (BLG-QA-14)
- [ST-12] Research endpoint integration tests (BLG-QA-16) + latency baseline (BLG-OPS-15) + trade plan sensitivity classification (BLG-SEC-06) + field extension governance (BLG-GOV-20)
- [ST-15] PT-05 §13 compliance review (BLG-GOV-19)
- [ST-16] Feature flag rollout infrastructure (BLG-FEAT-13)
- [ST-17] Trade plan abandonment backend (BLG-FEAT-21 — backend only; frontend sub-deliverables deferred to v3.4)

Sign-off: Product Owner — 2026-05-13
QA sign-off: Director of Quality — 2026-05-13

---

## v3.2 — Arc 2 Pre-Trade Research & Planning — 2026-05-08
Cycle: 2026-05-05__release-v3.2
Verified: Verified
Verification report: claude/cycles/2026-05-05__release-v3.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Pre-Trade Research View (PT-02 + PT-03): Research page at /research/{ticker}, ticker fundamentals, momentum signal, prospective heat at entry, trade plan panel, news headlines, screener/watchlist nav integration | docs/specs/frontend/pages/research.md; docs/specs/api_contracts/pre_trade_research_endpoints.md |
| EPIC-02 | Pre-Trade Entry Checklist (PT-05): Checklist component in Trade Plan form, 4 default items, toggle/persist, pre-population from plan data, research view link | docs/specs/frontend/pages/trade_plan.md#Entry Checklist |
| EPIC-03 | Governance & process hardening (OA-02–OA-05): sprint_planning_prompt.md STEP 0 main-branch check, execution_prompt.md STEP 5.1 deviations_filed enforcement, §3.1.A test_scenarios advisory, Playwright waitFor standard. Test scenario registrations: SC-TP-01–07 (trade plan), SC-EARN-01–09 (earnings), SC-UK-01–04 (UK screener) | claude/system/sprint_planning_prompt.md; claude/system/execution_prompt.md; tests/e2e/ |
| EPIC-04 | Documentation & security backlog clearance: React component inventory, design system doc, Alpaca credential audit/rotation policy, external API dependency risk register, cycle artefact inventory review | docs/specs/frontend/component_inventory.md; docs/specs/frontend/design_system.md; docs/ops/alpaca_key_rotation_policy.md; docs/ops/external_api_dependency_register.md; claude/system/OPERATIONAL_GUIDE.md §16 |

### Deviations accepted
None — zero spec deviations filed this sprint.

### Tech backlog items shipped
- [ST-13] React component inventory (BLG-FE-16)
- [ST-14] Design system document (BLG-FE-21)
- [ST-15] Alpaca credential audit and rotation policy (BLG-SEC-05)
- [ST-16] External API dependency risk register (BLG-GOV-18)
- [ST-17] Cycle artefact inventory and maintenance review (BLG-GOV-11)

Sign-off: Product Owner — 2026-05-07
QA sign-off: Director of Quality — 2026-05-07

---

## v3.1 — Arc 2 Trade Plan Foundation — 2026-05-05
Cycle: 2026-04-29__release-v3.1
Verified: Verified
Verification report: claude/cycles/2026-04-29__release-v3.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | PT-01 Trade Plan Object: data model schema (trade_plans table + 3 indexes; data_model.md v2.5), 6-endpoint CRUD API (POST /trade-plans, GET /trade-plans/{id}, PUT /trade-plans/{id}, DELETE /trade-plans/{id}, GET /trade-plans/by-position/{position_id}, GET /trade-plans/by-ticker/{ticker}), frontend creation/edit/view form and plan-exists banner; test.py 43 entries | docs/specs/data_model.md#Trade Plan; docs/specs/api_contracts/trade_plan_endpoints.md v0.1 |
| EPIC-02 | PT-02 Pre-Trade Research View (backend only): GET /research/{ticker} aggregation endpoint (signal, regime, sector, screener, earnings — all null-safe); pre_trade_research_endpoints.md v0.1; test.py 49 entries. Frontend deferred to v3.2 | docs/specs/api_contracts/pre_trade_research_endpoints.md v0.1 |
| EPIC-03 | DS-04 Earnings Calendar: GET /earnings/{ticker} backend + openapi.yaml; EarningsBadge on screener/watchlist/positions (⚠ proximity warning ≤5 days). BLG-FE-20 UK screener fix: stripUkSuffix helper for display and watchlist POST. BLG-QA-10/11: screener_accuracy_protocol.md + screener_scenarios.md (10 scenarios SCN-01–10). E2E: earnings-calendar.spec.js (SC-EARN-01–09), screener-uk-suffix.spec.js (SC-UK-01–04) | docs/specs/api_contracts/earnings_endpoints.md v0.1; docs/specs/screener_results_schema.md; docs/qa/screener_accuracy_protocol.md; docs/qa/screener_scenarios.md |
| EPIC-04 | BLG-FEAT-19 Monthly P&L report: GET /reports/monthly-pnl endpoint + MonthlyPnlTable in Reports.js. BLG-SEC-03/04+BLG-GOV-17: alpaca_key_rotation_policy.md, external_api_credential_inventory.md, external_api_dependency_register.md. CF-01/CF-02: execution_prompt.md v3.11→v3.13 (reclassification backfill instruction + STEP 8.5 output target fix) | docs/specs/api_contracts/reports_endpoints.md; docs/ops/; claude/system/execution_prompt.md v3.13 |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01–03] PT-01 — Trade Plan Object (full): data model, backend CRUD, frontend creation/edit/view flow
- [ST-04–05] PT-02 — Pre-Trade Research View (backend): aggregation endpoint (frontend deferred v3.2)
- [ST-06] BLG-FE-20 — UK screener ticker display fix and watchlist POST correction
- [ST-07–08] DS-04 — Earnings Calendar (backend + frontend EarningsBadge)
- [ST-09] BLG-QA-11 — Screener accuracy test protocol
- [ST-10] BLG-QA-10 — Screener scenario test data library (10 scenarios)
- [ST-11] BLG-FEAT-19 — Monthly P&L summary report
- [ST-12] BLG-SEC-03/04 + BLG-GOV-17 — External API security policy docs and dependency risk register
- [ST-13] CF-01 — execution_prompt.md §3.1.A reclassification backfill instruction (v3.11→v3.12)
- [ST-14] CF-02 — execution_prompt.md STEP 8.5 output target fix (v3.12→v3.13)

Sign-off: Product Owner — 2026-05-05
QA sign-off: Director of Quality — 2026-05-05

---

## v3.0 — Arc 1 Screener Engine & Results Page — 2026-04-27
Cycle: 2026-04-25__release-v3.0
Verified: Verified
Verification report: claude/cycles/2026-04-25__release-v3.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Screener Engine Backend — ticker universe data model + endpoints (ST-01); OHLCV data pipeline service with Alpaca primary / Yahoo Finance fallback (ST-02); ATR + regime detection + signal scoring engine (ST-03); screener batch engine + API endpoints `/screener/run` and `/screener/results` (ST-04) | docs/specs/api_contracts/ticker_universe_api_contract.md; docs/specs/api_contracts/alpaca_integration_contract.md; docs/specs/screener_results_schema.md; docs/specs/api_contracts/screener_api_contract.md; docs/reference/openapi.yaml |
| EPIC-02 | Screener Frontend — results page with sort/filter/regime badge/freshness/skeleton/empty/error states (ST-05); watchlist promotion inline popover + POST /watchlist integration (ST-06); news panel attachment with badge + inline expand/collapse (ST-07); keyboard shortcuts n/w/r + sidebar hints (ST-11, cross-EPIC) | docs/specs/frontend/pages/screener_results.md |
| EPIC-03 | Operations, Observability & Test Quality — external API health check extension (Alpaca + Yahoo Finance in GET /health) (ST-08); AI journal monitoring metrics (usage_rate, error_rate, p95_latency_ms in GET /health) (ST-09); AI audit service unit tests 12 tests (ST-10) | docs/specs/api_contracts/health_endpoints.md |
| EPIC-04 | Technical Debt & Governance — execution_prompt.md §2 deferred patch (ST-12); execution_prompt.md §3.1.A deferred patch (ST-13); prompt_change_log.md retrospective entries (ST-14); consecutive losing streak metric in metrics_definitions.md (ST-15); AI journal model version contract (ST-16) | claude/system/execution_prompt.md; claude/system/prompt_change_log.md; docs/specs/metrics_definitions.md; docs/specs/ai_journal_model_contract.md |

### Deviations accepted
None. DEV-01 (P3 — screener results news panel deferred from v2.9) resolved this sprint by ST-07 delivery.

### Tech backlog items shipped
- [ST-01] BLG-DS-01/ticker-universe: Ticker universe data model + CRUD endpoints + DB table
- [ST-02] BLG-DS-02/ohlcv-pipeline: OHLCV data pipeline with Alpaca primary + Yahoo Finance fallback
- [ST-03] BLG-DS-03/screener-engine: ATR Wilder 14-period + regime detection + composite signal score (RSI+MACD+volume)
- [ST-04] BLG-DS-04/screener-api: Screener batch run engine + POST /screener/run + GET /screener/results
- [ST-05] BLG-FE-19/screener-page: Screener results page (React, HashRouter, DataState, RegimeBadge, filters)
- [ST-06] BLG-FE-20/watchlist-promo: Watchlist promotion inline popover flow
- [ST-07] BLG-FE-18/news-panel: Screener news panel — resolves DEV-01 from v2.9
- [ST-08] BLG-OPS-12/health-ext: External API health check extension (Alpaca + Yahoo Finance)
- [ST-09] BLG-OPS-13/ai-metrics: AI journal monitoring metrics in GET /health
- [ST-10] BLG-QA-10/ai-audit-tests: AI audit service unit tests (12 tests)
- [ST-11] BLG-FE-21/keyboard-shortcuts: Keyboard shortcuts (cross-EPIC: n/w/r + sidebar hints)
- [ST-12] PATCH-EP-§2: execution_prompt.md §2 deferred patch from v2.9
- [ST-13] PATCH-EP-§3.1.A: execution_prompt.md §3.1.A deferred patch from v2.9
- [ST-14] PATCH-PCL: prompt_change_log.md retrospective entries from v2.9
- [ST-15] BLG-FEAT-13/streak-metric: Consecutive losing streak metric + GET /analytics/streak-metric
- [ST-16] BLG-AI-02/model-contract: AI journal model version contract spec

Sign-off: Product Owner (agent-mediated) — 2026-04-27
QA sign-off: Director of Quality (agent-mediated) — 2026-04-27

---

## v2.9 — Arc 1 Foundation: Stock Discovery & Screening Spec & Infrastructure — 2026-04-24
Cycle: 2026-04-22__release-v2.9
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-04-22__release-v2.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-03 | Arc 1 Governance & QA Foundation — §13 review record for DS-06 (BLG-GOV-16 gate cleared); external API mock harness for CI (tests/mock_harness/, 7 smoke tests pass); screener test data library (12 scenarios, 10+ synthetic tickers) | claude/strategy/strategy_rules.md#§13 |
| EPIC-01 | Arc 1 Specification Foundation — screener results schema spec (Class 2); Alpaca API integration contract (Class 2, RISK-01 gate cleared); screener internal API contract (Class 2, openapi.yaml updated); screener results page UX spec (DS-02 implementation deferred to v3.0) | docs/specs/data_model/screener_results_schema.md; docs/specs/api_contracts/alpaca_integration_contract.md; docs/specs/api_contracts/screener_api_contract.md; docs/specs/frontend/pages/screener_results.md; docs/reference/openapi.yaml |
| EPIC-04 | Governance Debt & Quick Wins — execution_prompt.md §3.2 governance patches (v3.8→v3.10); SystemStatus.js /ai prefix fix; AI Journal summary audit log (ai_audit_log table + GET /ai/journal-summary/history); AI Journal test scenario coverage (4 scenarios in ai_scenarios.md) | claude/system/execution_prompt.md v3.10; src/pages/SystemStatus.js; docs/specs/api_contracts/ai_endpoints.md; docs/testing/ai_scenarios.md |
| EPIC-02 | Arc 1 Implementation Start — sector & industry classification (DS-03: sector_service.py, position enrichment, 9 unit tests); Alpaca US market data integration (DS-05: alpaca_service.py, US→Alpaca/UK→Yahoo routing, 10 integration tests); Alpaca news panel (DS-06: news_service.py, GET /news/{ticker}, Watchlist.js news panel; screener results page attachment deferred to v3.0 — DEV-01 P3) | docs/specs/data_model.md; docs/specs/api_contracts/alpaca_integration_contract.md |

### Deviations accepted
1 minor P3 deviation — see verification_report.md §4 for full detail. Backlog item filed: BLG-FE-18 (screener results news panel wiring, v3.0).

### Tech backlog items shipped
- [ST-01] BLG-SPEC-21: Screener results schema spec — screener_results_schema.md created; registered in Specs_Index.md §3.4b
- [ST-02] BLG-SPEC-22: Alpaca API integration contract — alpaca_integration_contract.md created; RISK-01 gate cleared
- [ST-03] BLG-SPEC-23: Screener internal API contract — screener_api_contract.md created; openapi.yaml updated
- [ST-04] BLG-FE-17: Screener results page UX spec — screener_results.md created
- [ST-08] BLG-GOV-16: §13 review record for DS-06 (Alpaca News Panel) — gate cleared
- [ST-09] BLG-QA-08: External API mock harness for CI — tests/mock_harness/; 7 smoke tests pass
- [ST-10] BLG-QA-09: Screener test data library — 12 scenarios, 10+ synthetic tickers
- [ST-11] BLG-GOV-14: execution_prompt.md §3.2 governance patches — reclassification counter-sign rule + EPIC-level consolidation note (v3.8→v3.9)
- [ST-12] BLG-GOV-15: execution_prompt.md STEP 5.1.B advisory — System_status_report capability cross-check added (v3.9→v3.10)
- [ST-13] BLG-FE-15: SystemStatus.js /ai prefix fix — /ai case added to categorizeEndpoint()
- [ST-14] BLG-AI-01: AI Journal summary audit log — ai_audit_log table, log_ai_summary_run integration, GET /ai/journal-summary/history endpoint
- [ST-15] TEST-GAP-EPIC-04: AI Journal test scenario coverage — docs/testing/ai_scenarios.md (4 scenarios)

Sign-off: Product Owner — 2026-04-24
QA sign-off: Director of Quality — 2026-04-24

---

## v2.8 — Frontend Completion, Test Quality & AI Journal Feature — 2026-04-20
Cycle: 2026-04-17__release-v2.8
Verified: Verified
Verification report: claude/cycles/2026-04-17__release-v2.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Market Correlation View — MarketCorrelationSection.js on Analytics page; per-position Pearson correlation with severity badges (high=Rose-500, moderate=Amber-500, low=Emerald-500); portfolio weighted average; nulls sort to bottom | docs/specs/api_contracts/analytics_endpoints.md v2.1.0; docs/specs/frontend/pages/analytics.md v1.7; docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md |
| EPIC-02 | Market Correlation Endpoint Scenarios — SC-CORR-01–04 added to docs/testing/analytics_scenarios.md v1.1 | docs/specs/api_contracts/analytics_endpoints.md v2.1.0 |
| EPIC-02 | Supplementary Indicator Field Scenarios — SC-SIG-IND-01–02 added to docs/testing/signals_scenarios.md v1.1 | docs/specs/api_contracts/signal_endpoints.md v1.1 |
| EPIC-03 | DoQ Date Field Reminder Patch — execution_prompt.md §3.2.A explicit Date: field pre-condition at PR open | claude/system/execution_prompt.md v3.7 |
| EPIC-03 | Sprint Close Terminology Clarification — execution_prompt.md §5.3 Deviations filed clarified: spec deviations only | claude/system/execution_prompt.md v3.8 |
| EPIC-03 | Backlog Archive Deduplication — 64 duplicate entries removed; 83 unique IDs retained | claude/backlog/backlog_archive.md |
| EPIC-04 | AI Journal Summary Backend — POST /ai/journal-summary; Anthropic API (claude-haiku-4-5-20251001); graceful LLM failure (HTTP 200 summary:null); display-only; SRB-v1.7 compliant | docs/specs/api_contracts/ai_endpoints.md v1.0; docs/reference/openapi.yaml v2.7.0 |
| EPIC-04 | AI Journal Summary Frontend — AI summary section in TradeHistory.js; collapsed by default; non-dismissible disclaimer; Strategy Rules owner sign-off 2026-04-18 confirming SRB-v1.7 | docs/specs/frontend/pages/trade_history.md v1.7; docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md |

### Deviations accepted
None

### Tech backlog items shipped
- [BLG-FE-14] Market Correlation frontend view — deferred from v2.7 AC-6
- [BLG-QA-13] Test scenario coverage (SC-CORR, SC-SIG-IND) — v2.7 gap closure
- [BLG-GOV-13] Backlog archive deduplication — ID uniqueness compliance
- [BLG-FEAT-16] AI Journal Summarisation — first AI feature (Arc 4 foundation)

Sign-off: Product Owner — 2026-04-20
QA sign-off: Director of Quality — 2026-04-20

---

## v2.7 — Performance, Governance Hardening & Market Intelligence — 2026-04-16

Cycle: 2026-04-13__release-v2.7
Verified: Verified
Verification report: claude/cycles/2026-04-13__release-v2.7/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Supabase Supavisor connection pooling enabled (staging + production); `get_portfolio_summary()` refactored to single DB connection — GET /portfolio p50 = 234ms | `docs/ops/api_performance_baseline.md` v1.2; `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio` |
| EPIC-02 | QA sign-off gate before PR (§3.2.B); autonomous DoQ sign-off class for code-review-only EPICs (§3.2.A); governance_sync.yml push-to-main trigger | `claude/system/execution_prompt.md` v3.6; `claude/system/delivery_verification_prompt.md` v2.0 |
| EPIC-03 | Playwright LIFO route ordering fix (30/30 pass across 4 spec files); System Status Playwright spec authored (16/16 pass, 28-endpoint mock, category routing verified) | `tests/e2e/system-status.spec.js`; all 4 existing e2e spec files patched |
| EPIC-04 | `GET /analytics/market-correlation` backend endpoint (Pearson, 252-day lookback, 8h cache, SPY/FTSE benchmark); four supplementary indicator fields on `POST /signals/generate` (display-only, §13 COMPLIANT) | `docs/specs/api_contracts/analytics_endpoints.md` v2.1.0; `docs/specs/api_contracts/signal_endpoints.md` v1.1; `docs/reference/openapi.yaml` v2.6.0 |
| EPIC-05 | Spec Dependency Map (`docs/specs/spec_dependency_map.md` v1.0); Governance Health Score (OPERATIONAL_GUIDE.md §15 + roadmap_prompt.md STEP -1.7, advisory) | `docs/specs/spec_dependency_map.md` v1.0; `claude/system/OPERATIONAL_GUIDE.md` v3.59 |

### Deviations accepted

None — no P0–P3 spec deviations filed this sprint. AC-6 (market correlation frontend rendering) is an in-spec deferred AC, not a deviation.

### Tech backlog items shipped

- [ST-01] Enable Supabase Supavisor connection pooling — BLG-OPS-14; DEL-20260414-01 unblocked 2026-04-16
- [ST-02] Refactor get_portfolio_summary() to use a single DB connection — BLG-BE-07-FIX
- [ST-03] Require QA evidence sign-off block complete before PR — BLG-GOV-18
- [ST-04] Define formal autonomous DoQ sign-off class — BLG-GOV-19
- [ST-05] Extend governance_sync.yml to push-to-main — BLG-GOV-16
- [ST-06] Fix Playwright page.route() intercepts — BLG-QA-11 (Playwright fix)
- [ST-07] System Status Playwright spec — BLG-QA-12
- [ST-08] Market Correlation Analysis — BLG-FEAT-17
- [ST-09] Add supplementary indicator fields — BLG-BE-10
- [ST-10] Spec Dependency Map — BLG-SPEC-D17
- [ST-11] Governance Health Score — BLG-GOV-14

Sign-off: Product Owner — 2026-04-16
QA sign-off: Director of Quality — 2026-04-16

---

## v2.5 — Integration Baseline, Quick Wins & Governance Debt — 2026-04-10

Cycle: 2026-04-05__release-v2.5
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-04-05__release-v2.5/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | System Status reliability: auth forwarding fixed in POST /test/endpoints (API key forwarded to all internal calls); endpoint test list synced to 26 endpoints (matches openapi.yaml); Alerts, Notifications, Digest categories added to SystemStatus.js categorisation | backend/services/health_service.py; backend/routers/test.py; src/pages/SystemStatus.js |
| EPIC-02 | Backend integration documentation: Reports page and Signals page integration status mapped (gaps, SDK usage, follow-up items); GET /notifications/preferences outlier latency fixed (redundant ensure_alerts_tables() removed); GET /portfolio architectural constraint documented; Supavisor pooling recommendation filed | docs/ops/reports_integration_review.md; docs/ops/signals_integration_review.md; docs/ops/api_performance_baseline.md v1.1; backend/services/alerts_service.py |
| EPIC-03 | Frontend & operations quick wins: GitHub Actions curl calls hardened with --max-time 120; Avg Slippage StatsCard gradient deviation DEV-ST14-01 closed; Fee Drag % metric delivered end-to-end (backend fee_drag_pct + avg_fee_drag_pct, API contract v2.2.0, openapi.yaml v2.5.0, Trade History table amber column + sortable, Avg Fee Drag StatsCard); DataTable.js TableHead onClick bug fixed | docs/specs/api_contracts/trade_endpoints.md v2.2.0; docs/specs/metrics_definitions.md v1.9.0; docs/reference/openapi.yaml v2.5.0; src/pages/TradeHistory.js; src/components/trades/TradeHistoryTable.js; src/components/ui/DataTable.js; docs/testing/slippage_scenarios.md v1.2 |
| EPIC-04 | Governance hardening: execution_prompt.md STEP 8 governance file edit check (CF-2); delivery_verification_prompt.md pre-seal Date gate (CF-2); governance_sync.yml batch push fix (git log range, all commit messages parsed); backlog entry placement rule formalised; test scenarios SC-ATR-01, SC-DEDUP-01/02, SC-STOP-01 created | claude/system/execution_prompt.md v3.1; claude/system/delivery_verification_prompt.md v1.8; .github/workflows/governance_sync.yml; docs/testing/atr_scenarios.md; docs/testing/dedup_scenarios.md; docs/testing/stop_price_scenarios.md |

### Deviations accepted

4 minor P3 deviations — see verification_report.md §4 for full detail. Backlog items filed: BLG-FE-11 (card layout), BLG-FE-12 (header styling), BLG-FE-13 (flexible sort), BLG-BE-07-FIX (portfolio connection refactor).

No P1/P2 deviations. DataTable.js TableHead onClick (P2) fixed in-sprint before merge.

### Tech backlog items shipped

- [ST-01] BLG-OPS-12: Fix auth forwarding in POST /test/endpoints
- [ST-02] BLG-OPS-13: Sync endpoint test list with openapi.yaml
- [ST-03] BLG-FE-07: Fix System Status endpoint categorisation for v2.3/v2.4 routes
- [ST-04] BLG-BE-08: Review and document Reports page backend integration
- [ST-05] BLG-BE-09: Review and document Signals page backend integration
- [ST-06] BLG-BE-07: Investigate high external baseline latency on DB-backed endpoints
- [ST-07] BLG-OPS-11: Add --max-time to GitHub Actions curl calls
- [ST-08] DEV-ST14-01 closure: Fix Avg Slippage StatsCard gradient rendering (documentation close)
- [ST-09] BLG-FEAT-15: Fee drag metric on Trade History (backend + API + frontend)
- [ST-10] BLG-GOV-12: Fix governance_sync.yml batch push issue closure
- [ST-11] BLG-GOV-13: Formalise backlog entry placement standard
- [ST-12] BLG-GOV-11 (CF-2): Apply v2.4 deferred governance prompt patches
- [ST-13] TEST-GAP-EPIC-01: Create test scenarios for EPIC-01 correctness fixes

Sign-off: Product Owner — 2026-04-10
QA sign-off: Director of Quality — 2026-04-10

---

## v2.4 — Correctness, Insight & Governance Hardening — 2026-04-03

Cycle: 2026-03-31__release-v2.4
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-31__release-v2.4/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Backend correctness fixes: ATR pence→GBP conversion for all .L tickers (always-on, no guard); notification dispatch deduplication (rule_id + trading_day); initial stop price exposed on analytics trade endpoint (stop_price field join) | backend/utils/pricing.py; docs/specs/api_contracts/alerts_endpoints.md §4; docs/specs/api_contracts/analytics_endpoints.md §trades_for_charts |
| EPIC-02 | Frontend & UX: P&L (GBP) absolute value column restored to Positions Table View; user-facing error message mapping layer (HTTP status + error code → readable message) | docs/specs/frontend/pages/positions.md; src/lib/apiError.js |
| EPIC-03 | Spec debt: portfolios and trade_history table schemas in data_model.md reconciled against live Supabase DB (8 divergences corrected on trade_history; initial_cash and created_at confirmed correct on portfolios) | docs/specs/data_model.md#portfolios; docs/specs/data_model.md#trade_history |
| EPIC-04 | Weekly trading digest: new GET /digest/weekly endpoint returning 7-day P&L, alert activity, compliance score trend, staleness summary; WeeklyDigest.js frontend component | backend/routers/digest.py; docs/specs/api_contracts/digest_endpoints.md; docs/reference/openapi.yaml; src/pages/WeeklyDigest.js |
| EPIC-05 | Operational readiness: Render hosting tier reviewed and documented (free tier sufficient — decision record filed); API endpoint performance baseline documented (all endpoints, p50/p95); slippage tracking test scenario file (SC-SLIP-01 through SC-SLIP-06); cycle velocity metric defined and backfilled 6 cycles | docs/ops/api_performance_baseline.md; docs/testing/slippage_scenarios.md; claude/cycles/velocity_metrics.md; claude/system/roadmap_prompt.md (velocity section) |
| EPIC-06 | Governance engine maintenance: execution_prompt.md action-now patches (second recurrences LL-v2.2-EX-01/02/04); delivery_verification_prompt.md deviation compliance check patch (LL-v2.3-CL-03); execution_prompt.md delegation model update + delegation log line count check; release planning cycle artefact sealing simplified (SHA-256 hash verification removed, sealed: true flag retained) | claude/system/execution_prompt.md; claude/system/delivery_verification_prompt.md; claude/system/release_planning_prompt.md |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-EPIC02-ST05-03 | P2 | Missing P&L (GBP) column on Positions page (accepted v2.3; **resolved this sprint by ST-04**) | PO + DoQ (v2.3); resolved v2.4 |
| DEV-ST14-01 | P3 | Avg Slippage StatsCard renders without gradient background (cosmetic, pre-existing). BLG-FE-08 filed. | DoQ 2026-03-20 (pre-accepted) |

### Tech backlog items shipped

- [ST-01] BLG-BE-05: Fix ATR pence→GBP conversion for all UK (.L) tickers
- [ST-02] BLG-BE-06: Alert evaluation notification dispatch deduplication
- [ST-03] BLG-BE-04: Expose initial stop price (stop_price) on analytics trade endpoint
- [ST-04] BLG-FE-06: Fix missing P&L (GBP) column on Positions page
- [ST-05] BLG-FE-03: User-facing error message mapping layer
- [ST-06] BLG-SPEC-D15: Reconcile portfolios table schema in data_model.md
- [ST-07] BLG-SPEC-D16: Reconcile trade_history table schema in data_model.md
- [ST-08/09] BLG-FEAT-14: Weekly trading review digest (backend endpoint + frontend component)
- [ST-10] BLG-OPS-10: Render hosting tier review and decision record
- [ST-11] BLG-OPS-05: API endpoint performance baseline document
- [ST-12] TEST-GAP-EPIC-05-SLIP: Slippage tracking test scenario file
- [ST-13] BLG-GOV-09: Cycle velocity metric defined and backfilled
- [ST-17] BLG-GOV-03: Release planning cycle artefact sealing simplified (SHA-256 removed)
- [ST-14/15/16] Governance carry-forward patches: execution_prompt.md + delivery_verification_prompt.md action-now items (LL-v2.2-EX-01/02/04, LL-v2.3-CL-02/03)

Sign-off: Product Owner — 2026-04-03
QA sign-off: Director of Quality — 2026-04-03

---

## v2.3 — Quality Automation & User Insight — 2026-03-30

Cycle: 2026-03-24__release-v2.3
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-24__release-v2.3/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | StrategyCompliancePanel (display-only; per-position stop compliance, stop age, size compliance; collapsible; auto-expands on violation); MetricsStalenessIndicator (data-freshness badge, staleness age, per-metric tooltip) | docs/specs/frontend/pages/positions.md#Strategy Compliance Panel; docs/specs/frontend/pages/analytics.md#Metrics Staleness Indicator; docs/specs/api_contracts/position_endpoints.md#GET /positions/compliance |
| EPIC-02 | UnderwaterChart zoom/pan; MonthlyHeatmap tile drill-down modal (per-trade table, R-Multiple, exit reason); R-Multiple Distribution histogram; critical-path smoke tests (3 paths, CI advisory); staging data reset script; test data seed scripts | docs/testing/chart_interactivity_scenarios.md |
| EPIC-03 | GET /health/database endpoint (DB size monitor, Telegram alert); health_endpoints.md v1.2; system health check playbook (3 failure modes); DEV-HEALTH-001 closed | docs/specs/api_contracts/health_endpoints.md v1.2 |
| EPIC-04 | Alert notification badge on Alerts nav item; Alert Thresholds empty state CTA form (closes DEV-EPIC02-ST04-01); loading state standardisation (5 pages); collapsible sidebar navigation groups (4 groups, sessionStorage persist, badge integration) | docs/specs/frontend/pages/notifications.md; docs/specs/frontend/patterns/loading_states.md; docs/specs/frontend/pages/navigation.md |
| EPIC-05 | Backend branch discipline invariant (execution_prompt.md §13); canonical test execution report template; integration test coverage CI report | claude/system/execution_prompt.md; docs/testing/test_execution_report_template.md; docs/reference/openapi.yaml |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-EPIC02-ST05-03 | P2 | P&L (GBP) column absent on Positions page — % uplift shown, absolute £ not rendered. BLG-FE-06 filed. | PO + DoQ |
| V-CHART-05a/b/c | P2 | R-Multiple chart visual AC staging-blocked by BLG-BE-04 (stop_price absent from /trades API). BLG-BE-04 existing item. | PO + DoQ |

### Tech backlog items shipped

- [ST-03] BLG-OPS-08: Staging data reset script
- [ST-04] BLG-QA-06: Test data seed script library
- [ST-05] BLG-QA-05: Critical-path smoke test (Playwright, advisory-only CI)
- [ST-14] BLG-GOV-07: Backend branch discipline invariant in execution_prompt.md §13
- [ST-15] BLG-QA-03: Canonical test execution report template
- [ST-16] BLG-QA-04: Integration test coverage CI report

Sign-off: Product Owner — 2026-03-30
QA sign-off: Director of Quality — 2026-03-30

---

## v2.2 — Security, Alert Maturity & Quality — 2026-03-24

Cycle: 2026-03-21__release-v2.2
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-21__release-v2.2/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | X-API-Key authentication middleware (all non-health endpoints); Content Security Policy meta tag | docs/specs/api_contracts/conventions.md §1 v1.1; public/index.html |
| EPIC-02 | Alert scheduling design (trigger mechanism, cooldown, cron); Alert Threshold Customisation UI (inline edit/validation); Alert History Table (evaluation log + backend: alert_evaluations table, GET /alerts/history, GitHub Actions cron) | docs/specs/api_contracts/alerts_endpoints.md v0.3; docs/specs/frontend/pages/notifications.md v0.2 §2 + §Page 3; docs/product/decisions/decisions--2026-03-21__release-v2.2.md §ST-03 |
| EPIC-03 | CSV export function name bug fix; Slippage StatsCard gradient key fix; Operational health check endpoint (db status, last evaluation timestamps) | docs/specs/api_contracts/trade_endpoints.md; docs/specs/frontend/pages/trade_history.md; docs/specs/api_contracts/health_endpoints.md |
| EPIC-04 | Notification scenario execution (SC-NOTIF-01–08, 9 Playwright tests); Watchlist test scenarios (SC-WATCH-01–06); Test automation readiness assessment; Spec-to-test traceability matrix (54 ACs, 22 TEST-GAP entries) | docs/testing/notifications_scenarios.md; docs/testing/watchlist_scenarios.md; docs/testing/test_automation_readiness.md; docs/testing/spec_to_test_traceability_matrix.md |
| EPIC-05 | Provisional-Target field at backlog promotion; scored_initiatives.md effort band handoff for release planning; Structured lessons learnt carry-forward block across all engines | claude/system/roadmap_prompt.md v4.5; claude/system/release_planning_prompt.md v2.24; claude/system/sprint_planning_prompt.md v2.3; claude/system/post_ship_closure.md v2.1; claude/system/shared_standards.md v2.7; claude/system/lessons_learnt_prompt.md v1.8 |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-HEALTH-001 | P2 | GET /health implementation schema differs from spec v1.0 — more informative schema; BLG-SPEC-D14 created for spec update | PO + DoQ 2026-03-24 |
| DEV-EPIC02-ST05-02 | P2 | ST-05 backend commits landed on main rather than EPIC-02 branch — process deviation, no functional impact; BLG-GOV-07 created | PO + DoQ 2026-03-24 |

2 minor deviations (P3/observation): DEV-EPIC02-ST04-01 (missing CTA in empty state — BLG-FE-04 created), DEV-EPIC02-ST05-01 (React fragment key — observation only). See verification_report.md.

### Tech backlog items shipped

- [ST-01] API Key Authentication for Render Deployment (BLG-SEC-01)
- [ST-02] Content Security Policy Headers (BLG-SEC-02)
- [ST-03] Alert Scheduling Design (BLG-OPS-04)
- [ST-04] Alert Threshold Customisation (BLG-FEAT-10)
- [ST-05] Alert History Table (BLG-FEAT-12)
- [ST-06] Fix CSV Export Import Bug (BLG-BE-03)
- [ST-07] Fix Slippage StatsCard Gradient Key (BLG-FE-01)
- [ST-08] Health Check Endpoint (BLG-OPS-06)
- [ST-09] Execute Notification Scenarios on Staging (TEST-GAP-EPIC-02)
- [ST-10] Create Watchlist Test Scenarios (TEST-GAP-EPIC-03)
- [ST-11] Test Automation Readiness Assessment (BLG-QA-02)
- [ST-12] Spec-to-Test Traceability Matrix (BLG-SPEC-T01)
- [ST-13] Roadmap Engine: Provisional-Target Field (BLG-GOV-04)
- [ST-14] Release Planning: Load scored_initiatives.md (BLG-GOV-05)
- [ST-15] Structured Lessons Learnt Carry-Forward Block (BLG-GOV-06)

Sign-off: Product Owner — 2026-03-24
QA sign-off: Director of Quality — 2026-03-24

---

## v2.1 — Alerts, Watchlists & Enhancements — 2026-03-21

Cycle: 2026-03-18__release-v2.1
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-18__release-v2.1/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Async notification delivery ADR — architecture decision: FastAPI BackgroundTasks (no Redis/Celery) | docs/adr/ADR-003-notification-delivery-architecture.md |
| EPIC-02 | Alerts & Notifications full stack — rules engine (4 alert types), Telegram delivery, notification preferences UI, in-app notification feed, QA scenarios | docs/specs/api_contracts/alerts_endpoints.md, docs/specs/frontend/pages/notifications.md, docs/testing/notifications_scenarios.md |
| EPIC-03 | Watchlist monitoring — spec, backend (4 endpoints, signal status join-on-read), frontend (add/edit/delete/Add-to-Position) | docs/specs/api_contracts/watchlist_endpoints.md, docs/specs/frontend/pages/watchlist.md |
| EPIC-04 | Chart interactivity — tooltips, zoom/pan, heatmap drill-down (all 16 SC-CHART-IX sub-scenarios verified) | docs/specs/frontend/pages/analytics.md |
| EPIC-05 | Tax Year P&L PDF + CSV exports; slippage tracking (fill price, slippage %, avg slippage); Render PR preview environments | docs/specs/api_contracts/reports_endpoints.md, docs/specs/frontend/pages/trade_history.md |
| EPIC-06 | Spec debt cleared — lifecycle headers, spec coverage inventory, chart QA scenarios, zero cross-EPIC process violations | docs/specs/spec_coverage_inventory.md, docs/testing/chart_interactivity_scenarios.md, docs/testing/reports_scenarios.md, docs/testing/signals_scenarios.md |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-ST04-01 | P2 | Notification delivery via Telegram instead of email — Gmail SMTP and Brevo blocked/unavailable on Render free tier | PO + DoQ 2026-03-20 |
| EPIC-03 cherry-pick | P2 | EPIC-03 delivered via cherry-pick to main (not branch PR) — branch divergence would have reverted EPIC-02/05/06 work | PO + DoQ 2026-03-21 |

1 minor deviation (P3): DEV-ST14-01 — StatsCard cosmetic null-state colour. See verification_report.md.

### Tech backlog items shipped

- [ST-12] Tax Year P&L PDF Export (BLG-FR-01)
- [ST-13] Tax Year P&L CSV Export (BLG-FR-02)
- [ST-14] Slippage Tracking (BLG-FEAT-03)
- [ST-15] Render PR Preview Environments (BLG-OPS-03)
- [ST-16] Bulk lifecycle header remediation (BLG-SPEC-D12)
- [ST-17] Spec maintenance batch (BLG-SPEC-D13, BLG-SPEC-G6, BLG-SPEC-D10, BLG-SPEC-D11)
- [ST-18] Missing test scenario documents (TEST-GAP-SIG-01, TEST-GAP-TAX-01)
- [ST-19] Cross-EPIC process compliance check (BLG-PROC-01)

Sign-off: Product Owner — 2026-03-21
QA sign-off: Director of Quality — 2026-03-21

---

## v2.0 — Reporting & Alerts — 2026-03-17

Cycle: 2026-03-17__release-v2.0
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-17__release-v2.0/verification_report.md

Fixes the P1 portfolio response defect (BLG-BE-01), delivers the UK tax-year P&L report endpoint and frontend view, and exposes the signal exposure controls (`top_n` and `lookback_days`) — making all three production-ready in a single sprint. Prospective heat endpoint (BLG-BE-02) shipped as stretch. EPIC-03 (Alerts & Notifications) deferred to v2.1 pending BLG-TECH-08 (async notification architecture ADR).

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-04 | Portfolio fix + prospective heat: `GET /portfolio` extended with 4 missing fields (`initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value`) — P1 BLG-BE-01 resolved. `GET /portfolio/prospective-heat` spec authored and implemented (ST-13 stretch — BLG-BE-02 closed). Tax-year P&L spec pre-completed (ST-03). | `docs/specs/api_contracts/portfolio_endpoints.md v2.0.0`; `docs/specs/api_contracts/reports_endpoints.md v0.1`; `docs/testing/v1.7-qa-scenario-gaps.md — GAP-03 PASS` |
| EPIC-01 | Signal Exposure Enhancement: signals page frontend spec authored; `top_n` and `lookback_days` controls implemented with 500ms debounce, invalid-input reset, and empty-state handling. | `docs/specs/frontend/pages/signals.md v0.1`; `docs/specs/api_contracts/signal_endpoints.md` |
| EPIC-02 | Tax-Year P&L Statement: `GET /reports/tax-year` endpoint implemented with UK 6 April tax-year boundary logic; frontend report view with year selector, P&L summary bar, trades table, disclaimer banner. Post-merge P1 hotfix bb66b69 (base44.baseUrl undefined on production — resolved same day). | `docs/specs/api_contracts/reports_endpoints.md v0.1`; `docs/specs/frontend/pages/reports.md v0.1` |
| EPIC-05 | Documentation & Standards Pack: Production Deployment Runbook; Positions Table Data Dictionary; Database Migration Governance Standard; Spec Coverage Inventory (38 documents, 7 actions); CohortAnalysis backend regression scenarios (stretch — ST-20). | `docs/ops/production_deployment_runbook.md`; `docs/specs/data_model_positions_dictionary.md`; `docs/ops/database_migration_governance.md`; `docs/specs/spec_coverage_inventory.md`; `docs/testing/analytics_scenarios.md v1.0` |
| EPIC-06 | Governance Tooling (parallel track): `roadmap_prompt.md` v3.0→v4.0 — all stage file references replaced with `cycle_record.md` sections for all tiers. `idea_intake_prompt.md` v1.3→v2.0 — per-file model replaced with `ideas_register.md`; 44 ideas migrated. | `claude/system/roadmap_prompt.md v4.0`; `claude/system/idea_intake_prompt.md v2.0`; `claude/ideas/ideas_register.md` |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| — | — | No deviations accepted. DEV-v2.0-02 (P1, base44.baseUrl) resolved by hotfix bb66b69 before verification — not an open deviation. 1 minor P3 deviation (DEV-v2.0-01 — ST-20 cross-branch process commit, CLAUDE.md §2 patch applied, BLG-PROC-01 filed). See verification_report.md §4. | — |

### Tech backlog items shipped

- [BLG-BE-01 / ST-12] GET /portfolio missing 4 fields (P1) — `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value` added; GAP-03 passes; 10/10 integration tests pass
- [BLG-BE-02 / ST-13] GET /portfolio/prospective-heat spec and implementation — endpoint specified and implemented; `@unittest.skip` removed; tests pass
- [BLG-OPS-02 / ST-14] Production Deployment Runbook — `docs/ops/production_deployment_runbook.md` created
- [BLG-DATA-01 / ST-15] Positions Table Data Dictionary — `docs/specs/data_model_positions_dictionary.md` created
- [BLG-TECH-07 / ST-16] Database Migration Governance Standard — `docs/ops/database_migration_governance.md` created
- [BLG-NEW-13 / ST-17] Spec Coverage Inventory — `docs/specs/spec_coverage_inventory.md` v1.0; 38 documents audited; 7 actions identified
- [BLG-GOV-01 / ST-18] Roadmap stage document consolidation — `roadmap_prompt.md` v4.0; all tiers use `cycle_record.md` sections
- [BLG-GOV-02 / ST-19] Ideas register — `idea_intake_prompt.md` v2.0; `ideas_register.md` created; 44 ideas migrated; 45 prior submissions archived

### Deferred items

- EPIC-03 (3.5 Alerts & Notifications — ST-06–ST-10) deferred to v2.1. No async notification infrastructure present. BLG-TECH-08 (ADR) required before v2.1 sprint planning may seal.

Sign-off: Product Owner — 2026-03-17
QA sign-off: Director of Quality — 2026-03-17

---

## v1.10 — Operations & Quality Foundation — 2026-03-16

Cycle: 2026-03-15__release-v1.10
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-15__release-v1.10/verification_report.md

Establishes staging as the canonical pre-merge QA environment, closes the CohortAnalysis architecture violation carried since v1.9, delivers FastAPI TestClient integration tests for portfolio endpoints with a CI merge gate, and formally closes the v1.7 QA scenario gaps (BLG-QA-01) — executing 4 scenarios against staging. Resolves prior P2 deviation DEV-EPIC02-ST03-01.

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Development Environment Foundation: staging environment provisioned (Render Blueprint — API + Static Site + Supabase staging project); CI/CD auto-deploy from `main` via Render native auto-deploy; QA sign-off governance updated — `OPERATIONAL_GUIDE.md` v3.19 now mandates staging URL as canonical pre-merge QA environment | `claude/system/OPERATIONAL_GUIDE.md` v3.18→v3.19 |
| EPIC-02 | Analytics Architecture Correctness: `CohortAnalysis.js` refactored to call `GET /analytics/cohort` via `useQuery` + `api.analytics.cohort(period)`; `buildCohorts()`, `getPeriodLabel()`, `getPeriodKey()` removed; `trades` prop removed from call site; resolves analytics.md §15 hard rule and closes DEV-EPIC02-ST03-01 (P2, carried since v1.9) | `docs/specs/frontend/pages/analytics.md` §15; `docs/specs/api_contracts/analytics_endpoints.md` #GET /analytics/cohort |
| EPIC-03 | QA Infrastructure & Coverage: 15 FastAPI TestClient integration tests for `GET /portfolio` (response shape, GBP conversion, portfolio heat, grace period/display_status); `.github/workflows/integration-tests.yml` CI step blocks merge on failure; 4 v1.7 scenario gaps (GAP-01–GAP-04) authored and executed in `docs/testing/v1.7-qa-scenario-gaps.md`; BLG-QA-01 closed; TEST-GAP-EPIC-06 retired | `docs/specs/api_contracts/portfolio_endpoints.md`; `docs/testing/v1.7-qa-scenario-gaps.md` (new) |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| 1 minor deviation (DEV-ST05-01) | P3 | `GET /portfolio/prospective-heat` endpoint not defined in `portfolio_endpoints.md` and not implemented in backend — TestClient tests skipped with `@unittest.skip`; BLG-BE-02 filed for v2.0 — see verification_report.md §4 | PO — 2026-03-16 |

**Prior-cycle deviation resolved this sprint:**
- DEV-EPIC02-ST03-01 (P2, v1.9 Sprint 2) — CohortAnalysis client-side cohort computation — resolved by ST-04 (EPIC-02).

### Tech backlog items shipped

- [BLG-OPS-01 / ST-01] Provision staging environment infrastructure — Render Blueprint (Web Service + Static Site); Supabase staging project; staging live at https://trading-assistant-staging.onrender.com and https://trading-assistant-api-staging.onrender.com
- [BLG-OPS-01 / ST-02] Configure CI/CD auto-deploy to staging — Render native auto-deploy from `main`; deploy time ~2–5 min; no manual intervention required
- [ST-03] Update QA sign-off governance process — `OPERATIONAL_GUIDE.md` v3.19; staging URL referenced in §8.2 and §8.5; LL-01 governance gap closed
- [ST-04] Refactor CohortAnalysis.js to use backend endpoint — architecture violation closed; DEV-EPIC02-ST03-01 (P2) resolved
- [ST-05] FastAPI TestClient integration tests for portfolio endpoints — 15 tests; `tests/test_portfolio_integration.py`; all CI checks green
- [ST-06] Add integration test CI step — `.github/workflows/integration-tests.yml`; PR #72 CI check visible and named
- [BLG-QA-01 / ST-07] Author v1.7 missing QA test scenarios — 4 scenarios (GAP-01–GAP-04) in `docs/testing/v1.7-qa-scenario-gaps.md`; GAP-01 PASS, GAP-02 PASS, GAP-03 FAIL (BLG-BE-01 P1 filed — see Known Issues), GAP-04 BLOCKED (no closed trades in staging — deferred)

### Known issues carried forward

- **BLG-BE-01 (P1):** `GET /portfolio` response missing 4 required fields (`initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value`) per `portfolio_endpoints.md` v1.9.0. Discovered via GAP-03 staging execution. Targeted for v1.11.
- **GAP-04** (staging data gap): scenario valid but not executable — no closed trades in staging environment. Deferred.

Sign-off: Product Owner — 2026-03-16
QA sign-off: Director of Quality — 2026-03-16

---

## v1.9 — Risk Dashboard Fixes & Foundation — Sprint 1 of 2 (March 2026)

**Shipped:** 2026-03-09
**Cycle:** 2026-03-06__release-v1.9
**Verified:** Verified
**Verification report:** `claude/cycles/2026-03-06__release-v1.9/verification_report.md`
**Director of Quality sign-off:** 2026-03-09
**Product Owner acceptance:** 2026-03-09
**Sprint:** 1 of 2 — Sprint 2 (user-facing features) pending execution

Resolves all 10 Risk Dashboard deviations carried from v1.8, establishes reproducible Playwright test infrastructure that closes the v1.8 scenario coverage gap, and completes the full documentation hygiene backlog. User-facing features (Structured Trade Reflection Template, Compliance Metrics, Cohort Analysis, Dashboard Homepage, R-Multiple Distribution) are deferred to Sprint 2.

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-04 | Risk Dashboard: all 10 v1.8 deviations resolved — error states (HeatGauge, DrawdownSummary, GracePeriodPanel, PositionRiskTable, ProspectiveHeatPanel), sort direction (ascending), Stop Price column, Days in Grace column, GRACE badge colour (blue), GBP value at risk in HeatGauge, threshold label badge, US position GBP conversion for entry price and current stop | `docs/specs/frontend/pages/risk_dashboard.md` v0.1.7→v0.1.8 |
| EPIC-05 (partial) | QA infrastructure: Playwright canonical test scenario library Phase 1 (17 Risk Dashboard scenarios automated, CI gate); Service Layer Test Coverage Standard authored and enforced via pytest-cov in CI | `docs/testing/risk_dashboard_scenarios.md` v1.0→v1.1; `docs/specs/backend_engineering_patterns.md` |
| EPIC-06 | Documentation hygiene: Canonical Terms Glossary; AI-Assisted Workflow Governance Policy; `GET /market/status` endpoint spec; `settings_model.md` canonical spec; Error Response Standard in `conventions.md §13`; API Contracts README updated to v1.9.0; `GET /positions/search/tags` documented; `System_status_report.md` lifecycle header added; broken cross-references to `document_lifecycle_guide.md` fixed; `structured_logging_standards.md` registered in Specs Index; ADR-002 relocated; `validation_system.md` owner field corrected | Multiple spec documents (see Tech Backlog below) |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| — | — | No deviations accepted this sprint — all 10 inherited v1.8 Risk Dashboard deviations resolved | — |

### Tech backlog items shipped

- [BLG-RD-01 / EPIC-04] Entity store fallback masks API error states — all 5 Risk Dashboard components now render independent error states; entity fallback suppresses positionError correctly
- [BLG-RD-02 / EPIC-04] GracePeriodPanel empty vs error state — distinct error card rendered on API failure
- [BLG-RD-03 / EPIC-04] PositionRiskTable sort direction — corrected to ascending (most at risk first)
- [BLG-RD-04 / EPIC-04] Stop Price column absent — Stop Price column added to PositionRiskTable (GBP, 2 dp)
- [BLG-RD-05 / EPIC-04] GRACE badge colour amber — corrected to blue per spec §6.3
- [BLG-RD-06 / EPIC-04] GBP value at risk absent from HeatGauge — SVG text added below gauge percentage
- [BLG-RD-07 / EPIC-04] Days in Grace column absent — `holding_days` column added to GracePeriodPanel
- [BLG-RD-09 / EPIC-04] ProspectiveHeatPanel threshold label absent — threshold label badge added
- [BLG-RD-10 / EPIC-04] US entry prices in USD — `portfolio_service.py` now converts `entry_price` to GBP for US positions using `stored_fx_rate`; 5 new golden output vectors (FX-01–FX-05)
- [BLG-RD-11 / EPIC-04] `current_stop` in USD for US positions — `portfolio_service.py` converts `current_stop` to GBP for US positions; Stop Distance % now uses matching currencies
- [BLG-NEW-10 Phase 1 / ST-11] Canonical Test Scenario Library Phase 1 — Playwright mock layer; 17 Risk Dashboard scenarios automated; CI gate `.github/workflows/playwright.yml`; mock data in `tests/e2e/mocks/portfolio-mock-data.js`
- [BLG-NEW-12 / ST-13] Service Layer Test Coverage Standard — coverage threshold enforced via pytest-cov in CI; standard documented in `docs/specs/backend_engineering_patterns.md`
- [BLG-NEW-04 / ST-15] AI-Assisted Workflow Governance Policy — policy document filed in `docs/governance/`
- [BLG-NEW-11 / ST-14] Canonical Terms Glossary — `docs/reference/glossary.md` Class 2 Supporting v1.1; minimum terms defined with canonical source links; registered in Specs Index §3.6
- [BLG-SPEC-D3 / ST-16] `GET /market/status` endpoint documented — `docs/specs/api_contracts/market_endpoints.md` Class 1 Canonical v0.1; openapi.yaml updated; registered in Specs Index §3.4
- [BLG-SPEC-G1 / ST-17] `settings_model.md` created — `docs/specs/data_model/settings_model.md` Class 1 Canonical v0.1; registered in Specs Index §3.2
- [BLG-SPEC-G2 / ST-18] Error Response Standard defined — `docs/specs/api_contracts/conventions.md` §13 added (canonical error envelope, HTTP status mapping)
- [BLG-SPEC-D1, D4, D8, D9, G3, G4, G5 / ST-19] Remaining SPEC debt batch resolved — API Contracts README v1.9.0; `GET /positions/search/tags` documented; `System_status_report.md` lifecycle header added; cross-references fixed; `structured_logging_standards.md` registered in Specs Index §3.5b; ADR-002 relocated to `docs/product/decisions/`; `validation_system.md` owner field corrected to named role

### Sprint 2 — pending

| Item | Description | EPIC |
|------|-------------|------|
| ST-01 | Structured Trade Reflection Template | EPIC-01 |
| ST-02 | Basic Compliance Metrics (pre-work gate for ST-01) | EPIC-01 |
| ST-03 | Cohort Analysis | EPIC-02 |
| ST-04 | Dashboard Homepage / Session Summary | EPIC-03 |
| ST-05 | R-Multiple Distribution Report | EPIC-02 |
| ST-12 | Canonical Test Scenario Library Phase 2 (feature scenarios for Sprint 2 deliveries) | EPIC-05 |

Sign-off: Product Owner — 2026-03-09
QA sign-off: Director of Quality — 2026-03-09

---

## v1.8 — Risk Dashboard (March 2026)

**Shipped:** 2026-03-06
**Cycle:** 2026-03-04__release-v1.8
**Verified:** Verified_with_deviations
**Verification report:** `claude/cycles/2026-03-04__release-v1.8/verification_report.md`
**Director of Quality sign-off:** 2026-03-06
**Product Owner acceptance:** 2026-03-06

Full Risk Dashboard page giving the trader daily visibility into portfolio heat, drawdown, grace period status, and per-position risk. Simultaneously established automated correctness gates and closed highest-priority spec and governance debt from v1.7.

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Risk Dashboard page: portfolio heat gauge (colour-coded thresholds), current drawdown summary, grace period status panel, per-position risk table, prospective heat indicator | `docs/specs/frontend/pages/risk_dashboard.md` v0.1.0–v0.1.6; `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio`; `docs/specs/metrics_definitions.md#Portfolio Heat` |
| EPIC-02 | CI Quality Gates: golden output regression (5 PS + 7 SL vectors, 30 tests), backtest vs live stop reconciliation, pip-audit CVE scanning (high/critical threshold), OpenAPI drift detection | `claude/strategy/strategy_rules.md`; `docs/reference/openapi.yaml` |
| EPIC-03 | Settings spec correction: PUT /settings replaced with PATCH /settings/{settings_id} and POST /settings; openapi.yaml updated to v1.9.0 | `docs/specs/api_contracts/settings_endpoints.md` v1.1.0; `docs/reference/openapi.yaml` v1.9.0 |
| EPIC-04 | Unavailability failure mode policy; running API changelog | `docs/ops/unavailability_policy.md` v1.0.0 (new); `docs/specs/api_contracts/api_changelog.md` v1.0.0 (new) |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-ST03-01 | P2 | Entity store fallback activates on `GET /portfolio` failure; error states not displayed when fallback data is available (§8) | PO — 2026-03-05 |
| DEV-ST03-03 | P2 | PositionRiskTable sorted descending by stop distance; spec §6.4 requires ascending | PO — 2026-03-05 |
| DEV-ST03-04 | P2 | Stop Price column absent from PositionRiskTable; spec §6.2 requires `current_stop` (GBP, 2 dp) | PO — 2026-03-05 |
| DEV-ST03-08 | P2 | Drawdown reads from `GET /portfolio`; spec §4.1 states `GET /analytics/metrics` — Head of Specs Team to verify | PO — 2026-03-05 |
| DEV-ST03-11 | P2 | US position entry prices display in native USD instead of GBP per spec §6.2 | PO — 2026-03-05 |
| DEV-ST03-12 | P2 | `current_stop` returned in USD for US positions; Stop Distance % derivation mixes currencies per spec §6.2 | PO — 2026-03-05 |
| P3 deviations | P3 | 5 minor deviations (DEV-ST03-02, DEV-ST03-05, DEV-ST03-06, DEV-ST03-07, DEV-ST03-09) — see `verification_report.md §4` | PO — 2026-03-05 |

All deviations accepted for v1.8; v1.9 resolution targets. Full register: `docs/specs/frontend/pages/risk_dashboard.md §11`.

### Tech backlog items shipped

- [BLG-NEW-01 / ST-05] Golden Output Regression Baseline — `tests/golden_outputs.json` created (5 PS + 7 SL vectors); CI workflow golden-outputs.yml added; 30 tests pass
- [BLG-NEW-02 / ST-06] Backtest vs Live Stop Reconciliation — stop formula reconciled against all 7 golden SL inputs; synthetic divergence detection confirmed sensitive
- [BLG-NEW-03 / ST-11] Unavailability Failure Mode Documentation — `docs/ops/unavailability_policy.md` created at v1.0.0
- [BLG-NEW-05 / ST-07] Dependency Vulnerability Scanning — `pip-audit` CI gate; high/critical CVEs block merge; requests package upgraded (pre-existing CVE resolved)
- [BLG-NEW-07 / ST-12] Running API Changelog — `docs/specs/api_contracts/api_changelog.md` created at v1.0.0; registered in Specs_Index.md §3.4
- [BLG-NEW-08 / ST-08] Automated OpenAPI Drift Detection — regex-based CI drift check; KNOWN_GAPS config supports managed transitions
- [BLG-SPEC-D2 / ST-09] Settings endpoint method drift resolved — `settings_endpoints.md` v1.1.0; PUT removed, PATCH/POST documented
- [BLG-SPEC-D7 / ST-10] openapi.yaml updated to v1.9.0 — PositionSummary, ValidationResponse, TradeHistory, Settings paths all aligned

### Test coverage gap

- [TEST-GAP-EPIC-01] 17/27 Risk Dashboard scenarios not executable — test infrastructure gap (no data injection mechanism). QA & Testing Owner to deliver seeded test environment before next sprint on Risk Dashboard spec sections. See `verification_report.md §6`.

Sign-off: Product Owner — 2026-03-06
QA sign-off: Director of Quality — 2026-03-06

---

## v1.7 — Foundation & Governance (March 2026)

**Shipped:** 2026-03-03
**Cycle:** 2026-03-02__release-v1.7
**Verified:** Verified
**Verification report:** `claude/cycles/2026-03-02__release-v1.7/verification_report.md`
**Director of Quality sign-off:** 2026-03-03
**Product Owner acceptance:** 2026-03-03

Non-user-facing governance and specification foundation release. Unlocks v1.8 pre-alignment (EPIC-03), v2.0 pre-alignment (EPIC-04, EPIC-05), and §13-gated features (EPIC-02).

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | CI/CD merge gate: `.github/workflows/validate-analytics.yml` — triggers on PR/push to main/develop; calls `POST /validate/calculations`; blocks merge on `critical_failed > 0`; posts severity breakdown as PR comment | `docs/specs/api_contracts/analytics_endpoints.md#POST /validate/calculations` |
| EPIC-02 | §13 Strategy Boundary Review: three features reviewed (Signal Params: COMPLIANT, AI Journal: CONDITIONALLY COMPLIANT, New Indicators: COMPLIANT if canonical). §13-gated features cleared to proceed | `claude/strategy/strategy_rules.md`; `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md` |
| EPIC-03 | Portfolio Heat metrics canonicalised: Position Risk (GBP-adjusted, FX-handled), Portfolio Heat (sum of Position Risks as % of portfolio value), explicit display thresholds with colour bands | `docs/specs/metrics_definitions.md` v1.5.8 → v1.6.0 |
| EPIC-04 | Structured Logging Standards: Class 1 Canonical Specification created — log levels (ERROR/WARNING/INFO/DEBUG), JSON log format (required + optional fields), correlation ID scheme (UUID v4, HTTP header propagation), async observability approach | `docs/specs/structured_logging_standards.md` v0.1.0 (new) |
| EPIC-05 | API Versioning Decision Record: URL path versioning deferred to first breaking change; 60-day deprecation notice; webhooks versioned from inception; existing endpoints grandfather-exempted | `docs/product/decisions/api-versioning-v1.7.md` |
| EPIC-06 | Spec Debt Resolution: `analytics_endpoints.md` v1.9.0 (14 validated metrics incl. `sharpe_ratio_trade_method`, OBS-01 resolved); `portfolio_endpoints.md` v1.9.0 (corrected to match live API, OBS-QWB-R1-01 resolved); `trade_endpoints.md` v1.9.0 (`holding_days` added, OBS-QWB-R3-01 resolved); `trade_service.py` updated | `docs/specs/api_contracts/analytics_endpoints.md` v1.8.1 → v1.9.0; `docs/specs/api_contracts/portfolio_endpoints.md` v1.8.2 → v1.9.0; `docs/specs/api_contracts/trade_endpoints.md` v1.8.4 → v1.9.0 |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| — | — | No deviations filed this sprint | — |

### Tech backlog items shipped

- [BLG-TECH-04] CI/CD GitHub Actions Validation Workflow — validate-analytics.yml workflow merged; merge gate live on main/develop
- [BLG-TECH-06] Canonicalise `sharpe_ratio_trade_method` — 14th validated metric added to analytics_endpoints.md v1.9.0; OBS-01 resolved
- [BLG-TECH-08] Align portfolio_endpoints.md positions summary — spec corrected to match live API (option a chosen); OBS-QWB-R1-01 resolved
- [BLG-TECH-09] Add `holding_days` to GET /trades — backend fix applied (option b chosen); OBS-QWB-R3-01 resolved

### Hard gates cleared by this release

| Gate | Cleared by |
|------|-----------|
| v1.8 pre-alignment | EPIC-03 — `metrics_definitions.md` v1.6.0 |
| v2.0 pre-alignment (logging) | EPIC-04 — `structured_logging_standards.md` Class 1 |
| v2.0 pre-alignment (API versioning) | EPIC-05 — `api-versioning-v1.7.md` |
| §13-gated features | EPIC-02 — SRB decision record filed |

### Test coverage gap

- [TEST-GAP-EPIC-06] 4 new scenarios required: `validate-analytics-14-metrics`, `validate-analytics-critical-count`, `portfolio-positions-field-alignment`, `trades-holding-days-present`. QA & Testing Owner to deliver before next sprint on analytics, portfolio, or trade endpoint domains. See `verification_report.md §6`.

Sign-off: Product Owner — 2026-03-03
QA sign-off: Director of Quality — 2026-03-03

---

## v1.6.1 — Quick Wins Bundle (March 2026)

**Shipped:** 2026-03-01
**Director of Quality sign-off:** 2026-03-01
**Verification report:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0
**Scope document:** `docs/product/scope/scope--QWB-quick-wins-bundle.md` (Superseded)

Six self-contained user-facing improvements. No new pages. No data model migrations.

---

### BLG-FEAT-01 — Current Drawdown Widget ✅ Complete

**Backend**
- `GET /portfolio` extended with two always-present fields: `current_drawdown_percent` (float, ≤ 0.0) and `peak_portfolio_value` (float, GBP)
- Calculated server-side: `(peak − current) / peak × 100`. Peak = `MAX(portfolio_history.total_value)` all-time. Both default to `0.0` when no `portfolio_history` exists
- Spec: `portfolio_endpoints.md` v1.8.2

**Frontend — Dashboard**
- Current Drawdown Widget added as fifth card in stats row
- Three display states: in-drawdown (% + peak equity + days underwater + progress bar), at-peak ("New Peak!"), no-history
- Progress bar sourced from `max_drawdown.percent` via `GET /analytics/metrics`. `days_underwater` sourced from `advanced_metrics.days_underwater` — no fallback calculation
- Spec: `dashboard.md` v1.1

---

### BLG-FEAT-02 — R-Multiple Column in Trade History ✅ Complete

**Frontend — Trade History**
- R-multiple column added to trade history table
- Frontend-only calculation: `R = (exit_price − entry_price) / (entry_price − stop_price)`. Source: `trades_for_charts` from `GET /analytics/metrics`, joined by trade `id`
- Display: signed, 2dp, R suffix (e.g. `+2.31R`, `−0.54R`). Em dash when `stop_price` absent or denominator is zero
- Column sortable; em-dash rows sort to end
- Spec: `trade_history.md` v1.1, `metrics_definitions.md` v1.5.8

---

### BLG-FEAT-04 — Best / Worst Trades Widget ✅ Complete

**Frontend — Performance Analytics**
- Best/Worst Trades component added below Top Performers on Performance Analytics page
- Two panels: top 3 and bottom 3 closed trades by R-multiple. Trades without `stop_price` excluded from ranking
- Partial panels when fewer than 3 qualifying trades; empty state when none
- Card content: ticker, R-multiple, P&L (GBP), exit date, exit reason
- Spec: `analytics.md` v1.2

---

### BLG-FEAT-05 — Win Rate by Month Chart ✅ Complete

**Frontend — Performance Analytics**
- Win Rate by Month bar chart added below Best/Worst Trades
- Source: `monthly_data` from `GET /analytics/metrics`
- Y-axis fixed 0–100. Bars green when `win_rate > 50%`, red at or below 50%. Dashed reference line at 50%
- Tooltip shows month, win rate %, and `trade_count`
- Returns null (no render) when `monthly_data` is empty
- Spec: `analytics.md` v1.2

---

### BLG-FEAT-06 — Grace Period Indicator ✅ Complete

**Backend**
- `GET /positions` extended with `grace_days_remaining` (integer | null) on every position object. Always present
- Formula: `max(0, 10 − holding_days)` when `grace_period = true`; `null` when `grace_period = false`. On day 10, `grace_period` becomes `false` → field returns `null`, not `0`
- Spec: `position_endpoints.md` v1.8.3

**Frontend — Positions**
- Grace Days Remaining column added to open positions table
- Display: `"Day {holding_days + 1} of 10"` when in grace; dash (`—`) when `null`
- Spec: `positions.md` v1.2

---

### BLG-FEAT-07 — CSV Export of Trade History ✅ Complete

**Backend**
- New endpoint: `GET /trades/export/csv`
- `Content-Type: text/csv`, `Content-Disposition: attachment; filename="trade_history.csv"`
- 14 columns: `ticker, market, entry_date, exit_date, shares, entry_price, exit_price, pnl, pnl_pct, holding_days, exit_reason, tags, entry_note, exit_note`
- Null fields → empty string. Tags array → semicolon-separated string. Empty history → header row only (HTTP 200)
- Spec: `trade_endpoints.md` v1.8.4

**Frontend — Trade History**
- CSV Export button added to Trade History page; triggers browser-native download
- Spec: `trade_history.md` v1.1

---

### Canonical Specs Updated

| Spec | Version | Change |
|------|---------|--------|
| `docs/specs/metrics_definitions.md` | v1.5.8 | New section: Current Drawdown |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.8.2 | New fields: `current_drawdown_percent`, `peak_portfolio_value` |
| `docs/specs/api_contracts/position_endpoints.md` | v1.8.3 | New field: `grace_days_remaining`; A-QA-05 day-10 contradiction corrected |
| `docs/specs/api_contracts/trade_endpoints.md` | v1.8.4 | New endpoint: `GET /trades/export/csv` |
| `docs/specs/frontend/pages/dashboard.md` | v1.1 | Current Drawdown Widget added |
| `docs/specs/frontend/pages/trade_history.md` | v1.1 | R-Multiple column + CSV Export button added |
| `docs/specs/frontend/pages/analytics.md` | v1.2 | Best/Worst Trades (§11) + Win Rate by Month (§12) added |
| `docs/specs/frontend/pages/positions.md` | v1.2 | Grace Days Remaining column added |
| `docs/specs/api_dependencies.md` | v1.2 | New dependencies added |

---

### Verification Summary

- **Scenarios:** 47 total — 45 pass, 2 deferred (F-17: data prerequisite; F-27: environment state), 0 fail
- **Defects:** 0 raised at any severity
- **Observations:** 2 pre-existing issues raised for backlog (BLG-TECH-08, BLG-TECH-09)
- **Sign-off:** Director of Quality, 2026-03-01. Verdict: Pass with logged deferrals

---

## v1.6 — Position Sizing Calculator (February 2026)

### Position Sizing Calculator ✅ Complete

**Sign-off:** Director of Quality, 2026-02-20
**Verification report:** `docs/product/verification/3.2-position-sizing-calculator-verification.md` (v1.4)

**Backend**
- `POST /portfolio/size` endpoint — calculates suggested share quantity for a prospective new position. Idempotent. No state mutation. Returns three distinct response shapes: valid result, insufficient cash (with `max_affordable_shares` always present), and invalid inputs (with machine-readable `reason` code)
- `default_risk_percent` field added to `settings` table — supports widget pre-population. Database migration applied; all existing rows default to `1.00`
- `GET /settings` and `PUT /settings` updated to expose and accept `default_risk_percent`

**Frontend**
- Position Sizing Calculator widget — always visible in Trade Entry form, directly above the Shares field
- Risk % field pre-populated from `settings.default_risk_percent` on form load
- Eight widget states implemented: idle, loading, valid auto-fill, valid with existing shares, insufficient cash, invalid input, invalid system, post-submit reset
- Auto-fills Shares field when result is valid and field is empty; "Use suggested shares" affordance shown when Shares already populated
- Debounced API call (300ms) on input change — does not block form submission in any state
- `default_risk_percent` field added to Settings page — Strategy Parameters section

**Canonical specifications updated**
- `strategy_rules.md` v1.3 — §4.1 sizing calculator rules
- `portfolio_endpoints.md` v1.8.0 — `POST /portfolio/size` contract
- `settings_endpoints.md` v1.8.0 — `default_risk_percent` field
- `data_model.md` v1.7 — settings column and migration script
- `position_form.md` v1.2 — widget spec and all eight states
- `settings.md` v1.1 — Strategy Parameters section
- `openapi.yaml` v1.8.0 — aligned with above contract changes

---

### BLG-TECH-01 — Sharpe Variance + Capital Efficiency Fix ✅ Complete

**Closed:** 2026-02-21
**Canonical Owner sign-off:** 2026-02-21
**Validation result:** 13/13 pass at 2026-02-21T00:24:41Z

This item was the v1.6 quality gate. v1.6 did not ship until these fixes were verified.

- `_calculate_sharpe()` updated to use sample variance (÷ n−1) for both portfolio-based and trade-based Sharpe methods
- Capital efficiency updated to use `Mean(total_cost)` in GBP from `trade_history` — eliminates USD/GBP mixing for portfolios with both markets
- `validation_data.py` expected values updated: `capital_efficiency` 0.17 → 0.22; `total_cost` fields added
- Validation metric count increased from 12 to 13 (capital efficiency added as explicitly validated metric)
- `metrics_definitions.md` v1.5.7 — Appendix E Backlog Items 1 and 2 marked resolved with closure detail
- `analytics_endpoints.md` v1.8.1 — resolved known limitations removed; severity contract added (A5/A6 actions completed alongside this closure)

---

## v1.5 — Performance Analytics (February 2026)

### Performance Analytics Page ✅ Complete

**Backend**
- Unified analytics endpoint: `GET /analytics/metrics?period=` (six period options: last 7 days, last month, last quarter, last year, YTD, all time)
- All metrics computed server-side from `trade_history` and `portfolio_history`; frontend performs no calculations
- Period filtering on both trade exit date and portfolio snapshot date
- `has_enough_data` gate: configurable minimum trade threshold (default 10, set via Settings)
- `POST /validate/calculations` endpoint: smoke-tests all metric calculations against a known 5-trade validation dataset with per-metric tolerance checks and CSV export

**Metrics delivered**
- Executive: Sharpe ratio (portfolio-based when 30+ snapshots available, trade-based fallback), max drawdown (percent, amount, date), recovery factor, expectancy per trade, profit factor, risk/reward ratio
- Advanced: win streak, loss streak, average hold time for winners vs losers, trade frequency (per week), capital efficiency, days underwater, portfolio peak equity
- Market comparison: win rate, total P&L, average win/loss, best and worst performer — UK and US independently
- Exit reason analysis: count, win rate, total P&L, average P&L, percentage of trades — per exit reason
- Monthly performance: P&L, trade count, win rate, cumulative — last 12 months
- Day of week: average P&L and trade count per weekday
- Holding period buckets: 1–5, 6–10, 11–20, 21–30, 31+ days — average P&L, count, win rate
- Top 5 winners and top 5 losers by P&L
- Consistency metrics: consecutive profitable months, current streak, win rate standard deviation, P&L standard deviation
- R-multiple analysis and tag performance derived from `trades_for_charts`

**Frontend**
- 12-component page render: executive summary cards, key insights, advanced metrics grid, monthly heatmap, underwater equity chart, market comparison, exit reason table, time-based charts, R-multiple analysis, top performers, consistency metrics, strategy tag performance
- Period selector drives single re-fetch of unified endpoint
- Loading, error, and not-enough-data states
- Key insights: up to 5 generated observations from metric values (Sharpe quality, hold time discipline check, profit factor commentary, expectancy edge, risk/reward)
- PDF export: print-optimised HTML report covering executive summary, key insights, and advanced metrics table
- snake_case → camelCase transformation on API response
- System Status page updated: analytics and validation endpoints categorised and included in automated endpoint testing suite

---

## v1.4 — Trade Journal & Notes System (February 2026)

### Trade Journal & Notes System ✅ Complete

- Entry notes when creating positions (500 character limit)
- Exit notes when closing positions (500 character limit)
- Tag system for categorising trades, with autocomplete from existing tags
- Tag validation: lowercase, hyphens only, up to 10 tags per position
- Tag filtering in trade history (OR logic)
- Expandable trade rows showing full journal entries
- Journal view mode in Positions page
- Visual entry/exit note cards with colour-coded headers
- Strategy tag pills with gradient styling
- Database schema updates: `entry_note`, `exit_note`, `tags` fields on positions and trade history
- GIN indexes on tags fields for fast filtering
- Backend endpoints: updateNote, updateTags, getTags

---

## v1.3 — System Health & Monitoring (February 2026)

- Health check endpoint (`GET /health`) for load balancers
- Detailed system status (`GET /health/detailed`)
- Automated endpoint testing (`POST /test/endpoints`) — 11 endpoints at launch
- Frontend status dashboard page with real-time monitoring
- Component-level health checks: Database, Yahoo Finance, Services, Config
- One-click endpoint testing with pass/fail results
- Auto-refresh at 5-second intervals
- Response time tracking
- 100% test pass rate at launch
