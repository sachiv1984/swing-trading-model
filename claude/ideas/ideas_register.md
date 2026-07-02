**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 2.5
**Last Updated:** 2026-07-02 (idea intake window IW-20260702-01, inline STEP -1.6 of roadmap rebalance 2026-07-02__scheduled — 44 new Submitted rows appended (22 agents × 2); 19 prior Parked-cycle-2 rows carried, none resubmitted)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Ideas Register

Migrated from per-file model (44 submissions from IW-20260304-01) on 2026-03-17 per ST-19 (EPIC-06).
Schema: per `shared_standards.md §16.5`

| Idea ID | Title | Submitter | Window | Submitted At | Status | Park Count | Park Rationale | Step 4 | Step 5 |
|---------|-------|-----------|--------|--------------|--------|------------|----------------|--------|--------|
| IDEA-product-owner-20260626-01 | AI chat conversation history persistence across sessions | Product Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | v6.2 AI chat shipped 2026-06-25; only 6 days usage data as of 2026-07-01 (target ~30 days, clears ~2026-07-25); §13 review still required before persistence design | Park C2 | — |
| IDEA-product-owner-20260626-02 | Trade entry confirmation: AI-assisted setup thesis digest at order placement | Product Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | AI feature layer shipped 6 days ago; user adoption pattern not yet established; premature to add another AI touchpoint before existing ones validated | Park C2 | — |
| IDEA-head-of-specs-20260626-02 | Spec coverage gap detection: auto-compare frontend page specs against deployed routes | Head of Specs Team | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Useful but requires script design decision; timing depends on spec ecosystem maturity, unchanged since last park | Park C2 | — |
| IDEA-pmo-lead-20260626-02 | Post-ship closure duration metric: track time from cycle close to closure complete in velocity_metrics.md | PMO Lead | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Nice-to-have; velocity_metrics.md still captures sprint performance adequately; closure duration overhead not warranted | Park C2 | — |
| IDEA-director-of-quality-20260626-02 | Playwright test data fixtures and state reset between runs for isolation | Director of Quality | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | No empirical fixture-isolation failures demonstrated since last park; still premature | Park C2 | — |
| IDEA-strategy-owner-20260626-01 | Strategy parameter sensitivity analysis framework: systematic pre-process to evaluate §11 parameter changes using historical trade data | Strategy Rules & System Intent Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Requires 20+ closed trades AND historical data; trade count unchanged (~15–17) since last park; Arc 5/6 tooling prerequisite still not in place | Park C2 | — |
| IDEA-finops-20260626-01 | External data provider cost comparison: annual review of data provider costs | FinOps & Resource Architect | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Annual cadence appropriate but not urgent; gate ≥2026-06-25 (~12 months out) | Park C2 | — |
| IDEA-finops-20260626-02 | Compute cost trending by feature area: partition Render dyno costs by feature area | FinOps & Resource Architect | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | BLG-OPS-74 prerequisite re-confirmed still unshipped (STEP 4.0 re-check, 2026-07-01); premature | Park C2 | — |
| IDEA-challenger-20260626-02 | Governance overhead ceiling enforcement mechanism: formal quarterly review of G+D+P% against 40% ceiling | Challenger | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | BLG-GOV-131 (ceiling metric) re-confirmed still unshipped; enforcement premature before the metric it would enforce exists; Skill-Silo advisory (still active) argues against more governance-process scope | Park C2 | — |
| IDEA-backend-engineering-20260626-02 | Backend request tracing: per-request trace ID propagation across routers/services | Backend Engineering Patterns Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | No new evidence of multi-service call failures requiring tracing; scope remains large relative to demonstrated need | Park C2 | — |
| IDEA-base44-frontend-20260626-02 | Prompt template versioning: track which version of the Base44 generation prompt produced each delivered component | Base44 Frontend Prompt Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Iteration frequency on the Base44 prompt has not increased; versioning overhead still not warranted | Park C2 | — |
| IDEA-data-model-20260626-01 | AI interaction history data model: schema design for persisting user chat sessions (§13-compliant) | Data Model & Domain Schema Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | §13 review for chat persistence still not opened; SRB-v1.7 remains scoped to stateless chat | Park C2 | — |
| IDEA-data-model-20260626-02 | Trade annotation model: schema for user-authored annotations on individual trades | Data Model & Domain Schema Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Arc 4 PO-02 data model not yet established (gated ~6+ months AI journal data, clears ~2026-10-20); should be co-designed with PO-02 | Park C2 | — |
| IDEA-director-of-hr-20260626-02 | Role capacity documentation: formal record of which governance routines require which roles | Director of HR | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Role capacity remains implicit in run manifests at current governance maturity; formal documentation overhead still not warranted | Park C2 | — |
| IDEA-financial-reporting-20260626-01 | AI-assisted monthly P&L narrative: optional AI-generated commentary for monthly P&L report | Financial Reporting & Records Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Same AI-adoption timing constraint — 6 days post-v6.2 ship, too early to layer additional AI-generated content onto financial reporting | Park C2 | — |
| IDEA-frontend-specs-20260626-01 | AI chat conversation persistence spec: frontend specification for persisting and displaying chat session history | Frontend Specifications & UX Documentation Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Depends on the same §13 review gate as IDEA-data-model-20260626-01, still not opened | Park C2 | — |
| IDEA-head-of-engineering-20260626-02 | Frontend bundle size optimization assessment: assess current React bundle size and heavy dependencies | Head of Engineering | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | No user-reported performance issues from bundle size; defer until profiling indicates need | Park C2 | — |
| IDEA-head-of-ux-20260626-01 | AI chat UI interaction study protocol: 5-question user research protocol to assess chat advisor usage | Head of UX & Design | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | 6 days of usage insufficient to design a meaningful research protocol around interaction patterns that haven't stabilised | Park C2 | — |
| IDEA-metrics-20260626-02 | AI chat engagement metric: sessions per week, questions per session, and response acceptance rate | Metrics Definitions & Analytics Owner | IW-20260626-01 | 2026-06-26 | Parked-cycle-2 | 2 | Usage patterns remain unestablished at 6 days post-ship; metric definition would be premature | Park C2 | — |
| IDEA-product-owner-20260702-01 | Screener-to-watchlist promotion friction audit | Product Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-product-owner-20260702-02 | Trade plan template presets by setup type | Product Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-head-of-specs-20260702-01 | Spec staleness scan across owning code paths | Head of Specs Team | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-head-of-specs-20260702-02 | Governance prompt cross-reference integrity check | Head of Specs Team | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-pmo-lead-20260702-01 | Escalation SLA dashboard | PMO Lead | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-pmo-lead-20260702-02 | Cross-cycle friction-item recurrence tracker | PMO Lead | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-director-of-quality-20260702-01 | Playwright flake-rate tracking | Director of Quality | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-director-of-quality-20260702-02 | QA evidence cross-link audit | Director of Quality | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-strategy-owner-20260702-01 | §13 boundary drift early-warning scan | Strategy Rules & System Intent Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-strategy-owner-20260702-02 | Strategy parameter change impact preview | Strategy Rules & System Intent Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-finops-20260702-01 | Render dyno right-sizing review | FinOps & Resource Architect | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-finops-20260702-02 | Anthropic API budget alert threshold calibration | FinOps & Resource Architect | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-infra-ops-20260702-01 | Staging environment drift detector | Infrastructure & Operations Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-infra-ops-20260702-02 | Deploy rollback runbook dry-run | Infrastructure & Operations Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-challenger-20260702-01 | Governance overhead ceiling second threshold | Challenger | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-challenger-20260702-02 | Skill-Silo Alert historical trend chart | Challenger | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-ai-compliance-20260702-01 | AI feature §13 re-attestation checklist | AI Compliance & Governance Officer | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-ai-compliance-20260702-02 | AI output disclaimer consistency sweep | AI Compliance & Governance Officer | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-api-contracts-20260702-01 | OpenAPI example-response completeness sweep | API Contracts & Documentation Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-api-contracts-20260702-02 | API contract deprecation marker convention | API Contracts & Documentation Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-backend-engineering-20260702-01 | Ticker/market input sanitisation regression suite | Backend Engineering Patterns Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-backend-engineering-20260702-02 | Database read-path audit for deprecated tables | Backend Engineering Patterns Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-base44-frontend-20260702-01 | Base44 prompt draft changelog | Base44 Frontend Prompt Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-base44-frontend-20260702-02 | Disclaimer component extraction | Base44 Frontend Prompt Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-cybersecurity-20260702-01 | Injection risk assessment refresh cadence | Cybersecurity & Trust Lead | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-cybersecurity-20260702-02 | Rate-limit bypass test | Cybersecurity & Trust Lead | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-data-model-20260702-01 | Trade plan field usage audit | Data Model & Domain Schema Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-data-model-20260702-02 | Signal write-path schema consolidation | Data Model & Domain Schema Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-director-of-hr-20260702-01 | Agent role charter gap spot-check | Director of HR | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-director-of-hr-20260702-02 | Facilitator workload note | Director of HR | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-financial-reporting-20260702-01 | P&L report AI narrative cost estimate | Financial Reporting & Records Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-financial-reporting-20260702-02 | Trade cost field completeness check | Financial Reporting & Records Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-frontend-specs-20260702-01 | Open Positions panel spec backfill | Frontend Specifications & UX Documentation Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-frontend-specs-20260702-02 | Disclaimer contrast standard | Frontend Specifications & UX Documentation Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-head-of-engineering-20260702-01 | Playwright suite runtime trend | Head of Engineering | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-head-of-engineering-20260702-02 | Dependency update review | Head of Engineering | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-head-of-ux-20260702-01 | Open Positions panel visual consistency check | Head of UX & Design | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-head-of-ux-20260702-02 | Colour contrast audit sweep | Head of UX & Design | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-metrics-20260702-01 | Signal correctness fix impact measurement | Metrics Definitions & Analytics Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-metrics-20260702-02 | Security fix false-positive rate | Metrics Definitions & Analytics Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-qa-lead-20260702-01 | Regression suite gap check for BLG-SEC-01/02 | QA Lead | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-qa-lead-20260702-02 | DoQ sign-off audit spot-check | QA Lead | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-qa-testing-20260702-01 | Test data fixture staleness check | QA & Testing Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
| IDEA-qa-testing-20260702-02 | Dark spec resolution follow-up | QA & Testing Owner | IW-20260702-01 | 2026-07-02 | Submitted | — | — | — | — |
