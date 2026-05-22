# Product Changelog — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-22

> This document is a human-maintained record of what was shipped in each product version and when. It records delivery milestones and notable decisions. It is not an immutable system record — for point-in-time system status reports, see `docs/operations/status_reports/`.

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
